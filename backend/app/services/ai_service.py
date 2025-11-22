# app/services/ai_service.py
from __future__ import annotations
from typing import List

import json
import os
from typing import Tuple, Optional
from sqlalchemy import or_

from sqlalchemy.orm import Session

from app.models import Finding as FindingModel
from app.schemas.finding import Finding as FindingSchema

from openai import OpenAI


def _get_openai_client() -> Optional[OpenAI]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def _build_finding_prompt(finding: FindingModel) -> str:
    """
    Build a structured prompt for the LLM to produce risk_score + explanation.
    """
    base = {
        "id": finding.id,
        "rule_name": finding.rule_name,
        "severity": finding.severity,
        "description": finding.description,
        "user": finding.user,
    }

    return (
        "You are a security and compliance risk analyst.\n"
        "You receive a finding from a GRC/log monitoring system.\n"
        "You must:\n"
        "1) Evaluate its risk on a scale of 0–100 (integer).\n"
        "2) Provide a short explanation (2–3 sentences) in simple English.\n\n"
        "Return ONLY valid JSON with the following shape:\n"
        '{ "risk_score": <int from 0 to 100>, "explanation": "<text>" }\n\n'
        f"Finding JSON:\n{json.dumps(base, indent=2)}"
    )


def _fallback_risk_and_explanation(finding: FindingModel) -> Tuple[float, str]:
    """
    If OPENAI_API_KEY is not set, use simple logic to create risk_score and explanation.
    """
    severity = (finding.severity or "").lower()
    base_scores = {
        "low": 20,
        "medium": 50,
        "high": 80,
        "critical": 95,
    }
    score = base_scores.get(severity, 40)

    # Fine-tuning by rule_name
    rule = (finding.rule_name or "").lower()
    if "public_bucket" in rule:
        score = max(score, 90)
    if "admin" in rule or "privilege" in rule:
        score = max(score, 90)
    if "api_token_admin_scope" in rule:
        score = max(score, 92)
    if "deployment_failed" in rule and "prod" in finding.description.lower():
        score = max(score, 85)

    explanation = (
        f"Risk is estimated at {score}/100 based on severity='{finding.severity}' "
        f"and rule_name='{finding.rule_name}'. "
        "This is a heuristic fallback explanation generated without an AI model."
    )
    return float(score), explanation


def _call_openai_for_finding(finding: FindingModel) -> Tuple[float, str]:
    """
    Calls OpenAI and returns (risk_score, explanation).
    If there are issues with the response or an error, throw an Exception and allow the caller to fall back.
    """
    client = _get_openai_client()
    if client is None:
        raise RuntimeError("OPENAI_API_KEY not configured")

    prompt = _build_finding_prompt(finding)

    # Example call to GPT-4 mini / 4.1 using the new client
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Or any other model you have access to
        messages=[
            {"role": "system", "content": "You are a helpful security assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    content = completion.choices[0].message.content
    # Expected JSON – parsed
    data = json.loads(content)

    risk_score = float(data["risk_score"])
    explanation = str(data["explanation"])

    # small guard
    risk_score = max(0.0, min(100.0, risk_score))
    return risk_score, explanation


def enrich_finding_with_ai(db: Session, finding_id: int) -> FindingSchema:
    """
    Fetches Finding, calculates risk_score + ai_explanation (AI or fallback),
    saves and returns the updated Finding as a schema.
    """
    finding: FindingModel | None = (
        db.query(FindingModel).filter(FindingModel.id == finding_id).first()
    )
    if finding is None:
        raise ValueError(f"Finding with id={finding_id} not found")

    # First try with OpenAI, if it fails, fall back
    try:
        risk_score, explanation = _call_openai_for_finding(finding)
    except Exception as e:
        print(f"----------------------------------------------------------\nError calling OpenAI for finding {finding_id}: {e}")
        risk_score, explanation = _fallback_risk_and_explanation(finding)

    finding.risk_score = risk_score
    finding.ai_explanation = explanation

    db.add(finding)
    db.commit()
    db.refresh(finding)

    # Return schema (already defined with from_attributes/from_orm)
    return FindingSchema.from_orm(finding)


def enrich_missing_findings(
    db: Session,
    limit: int = 50,
) -> List[FindingSchema]:
    """
    Finds Findings that are missing risk_score or ai_explanation,
    runs enrichment (AI or fallback),
    and returns a list of updated Findings.

    limit – how many to process in each call (to avoid overloading ourselves).
    """
    # Finds all Findings that are missing risk_score or ai_explanation
    missing = (
        db.query(FindingModel)
        .filter(
            or_(
                FindingModel.risk_score.is_(None),
                FindingModel.ai_explanation.is_(None),
            )
        )
        .order_by(FindingModel.id.asc())
        .limit(limit)
        .all()
    )

    if not missing:
        return []

    updated_schemas: List[FindingSchema] = []

    for f in missing:
        # Use the same logic as enrich_finding_with_ai,
        # but without asking the DB again by id.
        try:
            risk_score, explanation = _call_openai_for_finding(f)
        except Exception:
            risk_score, explanation = _fallback_risk_and_explanation(f)

        f.risk_score = risk_score
        f.ai_explanation = explanation
        db.add(f)
        # Don't commit here – we'll commit at the end

    db.commit()

    # Reload for extra security and conversion to schema
    for f in missing:
        db.refresh(f)
        updated_schemas.append(FindingSchema.from_orm(f))

    return updated_schemas
# backend/app/api/routes/findings.py

from typing import List  ,Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException

from fastapi import APIRouter , Depends , Query
from sqlalchemy.orm import Session 

from app.db.deps import get_db
from app import schemas , models
from app.services.findings_service import query_findings
from app.schemas.finding import PaginatedFindings
from app.services.ai_service import enrich_finding_with_ai, enrich_missing_findings


findings_router = APIRouter()

@findings_router.get("" , response_model =PaginatedFindings)
def list_findings(
    page: int = Query(1 , ge=1),
    page_size:int = Query(20 , ge=1 , le=100),
    severity: Optional[str] =None,
    user: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    db : Session = Depends(get_db)
):
    return query_findings( db=db,
        page=page,
        page_size=page_size,
        severity=severity,
        user=user,
        from_date=from_date,
        to_date=to_date,
        )


@findings_router.post(
    "/{finding_id}/enrich_with_ai",
    response_model=schemas.Finding,
)
def enrich_finding(
    finding_id: int,
    db: Session = Depends(get_db),
):
    """
    Runs AI engine on a single Finding:
    - Calculates risk_score (0–100)
    - Creates ai_explanation
    - Saves and returns the updated Finding
    """
    try:
        updated = enrich_finding_with_ai(db, finding_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return updated




@findings_router.post(
    "/enrich_all_missing",
    response_model=List[schemas.Finding],
)
def enrich_all_missing_findings(
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """
    Runs enrichment on all Findings that are missing risk_score or ai_explanation.
    Processes up to 'limit' records in each call.
    """
    updated = enrich_missing_findings(db, limit=limit)
    return updated
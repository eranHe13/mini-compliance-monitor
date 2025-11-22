from datetime import datetime, timedelta
from typing import List, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import SourceEvent, Finding

MAX_EVENTS_PER_HOUR = 30  

def _create_finding(
    event: SourceEvent,
    rule_name: str,
    description: str,
    severity: str,
) -> Finding:
    """
    Helper function to create a Finding from an event.
    """
    return Finding(
        rule_name=rule_name,
        description=description,
        severity=severity,
        user=event.user,
    )


def _count_events(
    db: Session,
    user: str,
    event_type: str,
    since: datetime,
) -> int:
    return (
        db.query(func.count(SourceEvent.id))
        .filter(SourceEvent.user == user)
        .filter(SourceEvent.event_type == event_type)
        .filter(SourceEvent.timestamp >= since)
        .scalar()
        or 0
    )


def apply_rules_to_event(event: SourceEvent, db: Session) -> List[Finding]:
    """
    Takes a single event, returns a list of Findings created from it.
    """
    findings: List[Finding] = []
    raw = event.raw_data or {}
    now = datetime.utcnow()

    # ========== A. Auth / Login ==========
    if event.event_type == "login_failed":
        # How many login_failed events were there for the user in the last hour?
        since = now - timedelta(hours=1)
        failed_count = _count_events(db, event.user, "login_failed", since)

        if failed_count >= 8:
            findings.append(
                _create_finding(
                    event,
                    rule_name="too_many_failed_logins_critical",
                    description=(
                        f"User {event.user} had {failed_count} failed login attempts "
                        f"in the last hour."
                    ),
                    severity="critical",
                )
            )
        elif failed_count >= 5:
            findings.append(
                _create_finding(
                    event,
                    rule_name="too_many_failed_logins",
                    description=(
                        f"User {event.user} had {failed_count} failed login attempts "
                        f"in the last hour."
                    ),
                    severity="high",
                )
            )
        elif failed_count >= 3:
            findings.append(
                _create_finding(
                    event,
                    rule_name="multiple_failed_logins",
                    description=(
                        f"User {event.user} had {failed_count} failed login attempts "
                        f"in the last hour."
                    ),
                    severity="medium",
                )
            )
        else:
            # Also give some low to see some variety in the dashboard
            findings.append(
                _create_finding(
                    event,
                    rule_name="single_failed_login",
                    description=f"User {event.user} had a failed login attempt.",
                    severity="low",
                )
            )

    if event.event_type == "login_success":
        location = raw.get("location", "Unknown")
        # How many failures were there before this success?
        since = now - timedelta(minutes=30)
        failed_before = _count_events(db, event.user, "login_failed", since)
        unusual_locations = {"Russia", "China", "Other"}

        if failed_before >= 3 and location in unusual_locations:
            findings.append(
                _create_finding(
                    event,
                    rule_name="suspicious_login_after_failures",
                    description=(
                        f"User {event.user} logged in successfully from {location} "
                        f"after {failed_before} recent failed attempts."
                    ),
                    severity="critical",
                )
            )

    # ========== B. MFA ==========
    if event.event_type == "mfa_failed":
        since = now - timedelta(minutes=10)
        mfa_failed_count = _count_events(db, event.user, "mfa_failed", since)

        if mfa_failed_count >= 5:
            findings.append(
                _create_finding(
                    event,
                    rule_name="too_many_mfa_failures",
                    description=(
                        f"User {event.user} had {mfa_failed_count} MFA failures in the "
                        "last 10 minutes."
                    ),
                    severity="high",
                )
            )
        elif mfa_failed_count >= 3:
            findings.append(
                _create_finding(
                    event,
                    rule_name="multiple_mfa_failures",
                    description=(
                        f"User {event.user} had {mfa_failed_count} MFA failures in the "
                        "last 10 minutes."
                    ),
                    severity="medium",
                )
            )

    # Also give low on mfa_success after failures
    if event.event_type == "mfa_success":
        since = now - timedelta(minutes=10)
        mfa_failed_count = _count_events(db, event.user, "mfa_failed", since)
        if mfa_failed_count > 0:
            findings.append(
                _create_finding(
                    event,
                    rule_name="mfa_success_after_failures",
                    description=(
                        f"User {event.user} had MFA success after {mfa_failed_count} "
                        "recent failures."
                    ),
                    severity="low",
                )
            )

    # ========== C. Permissions / Roles ==========
    if event.event_type == "permission_changed":
        old_role = raw.get("old_role")
        new_role = raw.get("new_role")
        approved_by = raw.get("approved_by")

        if new_role == "admin" and old_role != "admin":
            severity = "critical" if not approved_by else "high"
            findings.append(
                _create_finding(
                    event,
                    rule_name="privilege_escalation_admin",
                    description=(
                        f"User {event.user} role changed from {old_role} to {new_role}. "
                        f"Approved by: {approved_by}."
                    ),
                    severity=severity,
                )
            )
        elif old_role == "viewer" and new_role == "developer":
            findings.append(
                _create_finding(
                    event,
                    rule_name="viewer_to_developer",
                    description=(
                        f"User {event.user} role changed from {old_role} to {new_role}."
                    ),
                    severity="medium",
                )
            )

    # ========== D. API Tokens ==========
    if event.event_type == "api_token_created":
        scopes = raw.get("scopes", [])
        has_expiry = raw.get("has_expiry", True)

        if "admin:*" in scopes:
            findings.append(
                _create_finding(
                    event,
                    rule_name="api_token_admin_scope",
                    description=(
                        f"User {event.user} created an API token with admin scope: "
                        f"{scopes}."
                    ),
                    severity="critical",
                )
            )
        elif not has_expiry:
            findings.append(
                _create_finding(
                    event,
                    rule_name="api_token_without_expiry",
                    description=(
                        f"User {event.user} created an API token without expiry."
                    ),
                    severity="high",
                )
            )
        else:
            findings.append(
                _create_finding(
                    event,
                    rule_name="api_token_created",
                    description=(
                        f"User {event.user} created an API token with scopes: {scopes}."
                    ),
                    severity="medium",
                )
            )

    # ========== E. Pull Requests / Code ==========
    if event.event_type == "pull_request_merged":
        lines_changed = raw.get("lines_changed", 0)
        repo = raw.get("repo", "unknown")

        if lines_changed > 400:
            severity = "high"
            rule_name = "large_pr_merged"
        elif lines_changed > 150:
            severity = "medium"
            rule_name = "medium_pr_merged"
        else:
            severity = "low"
            rule_name = "small_pr_merged"

        findings.append(
            _create_finding(
                event,
                rule_name=rule_name,
                description=(
                    f"Pull request merged into {repo} with {lines_changed} lines changed."
                ),
                severity=severity,
            )
        )

    # ========== F. Deployments ==========
    if event.event_type == "deployment_failed":
        env = raw.get("environment", "unknown")
        service = raw.get("service", "unknown")

        if env == "prod":
            severity = "high"
        elif env == "staging":
            severity = "medium"
        else:
            severity = "low"

        findings.append(
            _create_finding(
                event,
                rule_name="deployment_failed",
                description=f"Deployment failed for service {service} in {env}.",
                severity=severity,
            )
        )

    # ========== G. Storage / Buckets ==========
    if event.event_type in ("storage_bucket_created", "storage_bucket_permission_changed"):
        bucket_name = raw.get("bucket_name", "unknown")
        public = raw.get("public", False)

        if public:
            findings.append(
                _create_finding(
                    event,
                    rule_name="public_bucket_detected",
                    description=(
                        f"Bucket {bucket_name} is publicly accessible "
                        f"(event_type={event.event_type})."
                    ),
                    severity="critical",
                )
            )
        else:
            # low to see some variety in the dashboard
            findings.append(
                _create_finding(
                    event,
                    rule_name="bucket_checked",
                    description=(
                        f"Bucket {bucket_name} permission event "
                        f"(event_type={event.event_type}, public={public})."
                    ),
                    severity="low",
                )
            )

    # ========== H. High activity generic rule ==========
    # This is a reminder of the MAX_EVENTS_PER_HOUR concept.
    since = now - timedelta(hours=1)
    total_last_hour = (
        db.query(func.count(SourceEvent.id))
        .filter(SourceEvent.timestamp >= since)
        .scalar()
        or 0
    )

    if total_last_hour > MAX_EVENTS_PER_HOUR * 10:
        findings.append(
            _create_finding(
                event,
                rule_name="very_high_activity_last_hour",
                description=(
                    f"There were {total_last_hour} events in the last hour overall."
                ),
                severity="high",
            )
        )

    return findings


def run_rules_on_new_events(db: Session) -> Tuple[int, int]:
    """
    Runs all rules on events that haven't been processed yet (processed == False),
    marks them as processed, and returns:
    - How many events were processed
    - How many findings were created
    """
    new_events = (
        db.query(SourceEvent)
        .filter(SourceEvent.processed == False) 
        .order_by(SourceEvent.timestamp.asc())
        .all()
    )

    if not new_events:
        return 0, 0

    total_findings = 0

    for event in new_events:
        findings = apply_rules_to_event(event, db)
        for finding in findings:
            db.add(finding)
        event.processed = True
        total_findings += len(findings)

    db.commit()
    return len(new_events), total_findings

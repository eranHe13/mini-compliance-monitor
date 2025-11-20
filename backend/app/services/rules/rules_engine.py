from datetime import timedelta
from typing import List, Tuple

from sqlalchemy.orm import Session

from app.models import SourceEvent, Finding

# Max events per hour for a user to be considered "suspicious"
MAX_EVENTS_PER_HOUR = 30


def apply_rules_to_event(event: SourceEvent, db: Session) -> List[Finding]:
    """
    Takes a single SourceEvent, and returns a list of Findings (objects, not yet saved in the DB).
    Here we implement the rules.
    """
    findings: List[Finding] = []

    # Rule 1: If event_type = "login_failed" → severity="high"
    if event.event_type == "login_failed":
        findings.append(
            Finding(
                rule_name="login_failed_high_severity",
                severity="high",
                description=f"Login failed for user '{event.user}'.",
                user=event.user,
            )
        )

    # Rule 2: If a user has more than N events in an hour → severity="medium"
    # Calculate how many events the user has in the last hour up to the current event
    window_start = event.timestamp - timedelta(hours=1)

    events_count = (
        db.query(SourceEvent)
        .filter(
            SourceEvent.user == event.user,
            SourceEvent.timestamp >= window_start,
            SourceEvent.timestamp <= event.timestamp,
        )
        .count()
    )

    if events_count > MAX_EVENTS_PER_HOUR:
        findings.append(
            Finding(
                rule_name="high_activity_last_hour",
                severity="medium",
                description=(
                    f"User '{event.user}' has {events_count} events in the last hour. "
                    f"Threshold is {MAX_EVENTS_PER_HOUR}."
                ),
                user=event.user,
            )
        )

    return findings


def run_rules_on_new_events(db: Session) -> Tuple[int, int]:
    """
    Takes all events that haven't been processed yet (processed = False),
    Runs the rules on them, saves Findings in the DB,
    and marks the events as processed.

    Returns:
      (number of events processed, number of Findings created)
    """
    # Get all events that haven't been processed yet
    new_events = (
        db.query(SourceEvent)
        .filter(SourceEvent.processed == False)  # noqa: E712
        .order_by(SourceEvent.timestamp.asc())
        .all()
    )

    if not new_events:
        return 0, 0

    total_findings_created = 0

    for event in new_events:
        findings = apply_rules_to_event(event, db)
        for f in findings:
            db.add(f)
        total_findings_created += len(findings)

        # Mark the event as processed
        event.processed = True

    db.commit()
    return len(new_events), total_findings_created

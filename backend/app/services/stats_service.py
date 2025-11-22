# backend/app/services/stats_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models

def get_summary_stats(db: Session) -> dict:
    total_events = db.query(func.count(models.SourceEvent.id)).scalar() or 0
    total_findings = db.query(func.count(models.Finding.id)).scalar() or 0

    # findings_by_severity
    severity_map = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    rows = (
        db.query(models.Finding.severity, func.count(models.Finding.id))
        .group_by(models.Finding.severity)
        .all()
    )
    for severity, count in rows:
        if severity in severity_map:
            severity_map[severity] = count

    # events_over_time
    date_rows = (
        db.query(
            func.date(models.SourceEvent.timestamp),
            func.count(models.SourceEvent.id),
        )
        .group_by(func.date(models.SourceEvent.timestamp))
        .order_by(func.date(models.SourceEvent.timestamp))
        .all()
    )
    events_over_time = [
        {"date": str(day), "count": count}
        for day, count in date_rows
    ]

    return {
        "total_events": total_events,
        "total_findings": total_findings,
        "findings_by_severity": severity_map,
        "events_over_time": events_over_time,
    }

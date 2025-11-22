# backend/app/services/findings_service.py

from sqlalchemy.orm import Session
from app import   models
from app.schemas.finding import FindingFilter
from app import schemas
from datetime import datetime , time , date

def get_findings_paginated(
    db: Session,
    page: int,
    page_size: int,
    severity: str | None,
    user: str | None,
    from_date: date | None,
    to_date: date | None,
):
    # page,page_size → limit,offset
    limit = page_size
    offset = (page - 1) * page_size

    # from_date/to_date (date) → from_timestamp/to_timestamp (datetime)
    from_timestamp = None
    to_timestamp = None

    if from_date:
        from_timestamp = datetime.combine(from_date, time.min)
    if to_date:
        # עד סוף היום
        to_timestamp = datetime.combine(to_date, time.max)

    filter_obj = FindingFilter(
        severity=severity,
        user=user,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
        limit=limit,
        offset=offset,
    )

    # כאן או שנשתמש ב-filter_obj כדי לבנות query,
    # או שנעביר אותו לפונקציה אחרת (repository).
    query = db.query(models.Finding)

    if filter_obj.severity:
        query = query.filter(models.Finding.severity == filter_obj.severity)
    if filter_obj.user:
        query = query.filter(models.Finding.user == filter_obj.user)
    if filter_obj.from_timestamp:
        query = query.filter(models.Finding.created_at  >= filter_obj.from_timestamp)
    if filter_obj.to_timestamp:
        query = query.filter(models.Finding.created_at  <= filter_obj.to_timestamp)

    total = query.count()
    items = (
        query
        .order_by(models.Finding.created_at.desc())
        .offset(filter_obj.offset)
        .limit(filter_obj.limit)
        .all()
    )

    # החזרה בפורמט שהפרונט אוהב
    return {
        "items": [schemas.Finding.from_orm(f).dict() for f in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }



from sqlalchemy.orm import Session
from app import   models
from app.schemas.source_event import SourceEventFilter


def query_events(db:Session , filters: SourceEventFilter):
    q = db.query(models.SourceEvent)

    if filters.event_type :
        q.filter(models.SourceEvent.event_type == filters.event_type)
    
    if filters.user :
        q.filter(models.SourceEvent.user == filters.user)
    
    if filters.from_timestamp :
        q.filter(models.SourceEvent.timestamp >=  filters.from_timestamp)
    
    if filters.to_timestamp :
        q.filter(models.SourceEvent.timestamp <= filters.to_timestamp)
    
    q.order_by(models.SourceEvent.timestamp.desc())
    q = q.offset(filters.offset).limit(filters.limit)

    return q.all()
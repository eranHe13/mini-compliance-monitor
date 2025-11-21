

from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models


def get_summary_stats(db: Session) -> dict:
    '''
    Return basic stats summary :
    - total number of events 
    - total number of findings
    - finding by severity
    - events by events_type 

    '''
    total_events = db.query(func.count(models.SourceEvent.id)).scalar() or 0 
    total_findings = db.query(func.count(models.Finding.id)).scalar() or 0 

    findings_by_severity = [  
        {"severity": severity, "count": count}
        for severity, count in db.query(models.Finding.severity , func.count(models.Finding.id)).group_by(models.Finding.severity).all()
    ]


    #findings_by_severity =( db.query(models.Finding.severity , func.count(models.Finding.id)).group_by(models.Finding.severity).all() )

    events_by_type_raw = (db.query(models.SourceEvent.event_type , func.count(models.SourceEvent.id)).group_by(models.SourceEvent.event_type).all())

    events_by_type = [{
        "event_type" : event_type, 
        "count" : count }
        for event_type , count in events_by_type_raw]

    return {
        "total_events" : total_events,
        "total_findings" : total_findings , 
        "findings_by_severity" : findings_by_severity,
        "events_by_type" : events_by_type
    }
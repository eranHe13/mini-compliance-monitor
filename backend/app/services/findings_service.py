

from sqlalchemy.orm import Session
from app import   models
from app.schemas.finding import FindingFilter


def query_findings(db:Session , filters: FindingFilter):
    q = db.query(models.Finding)

    if filters.severity :
        q.filter(models.Finding.severity == filters.severity)
    
    if filters.user :
        q.filter(models.Finding.user == filters.user)
    
    if filters.from_timestamp :
        q.filter(models.Finding.timestamp >=  filters.from_timestamp)
    
    if filters.to_timestamp :
        q.filter(models.Finding.timestamp <= filters.to_timestamp)
    
    q.order_by(models.Finding.timestamp.desc())
    q = q.offset(filters.offset).limit(filters.limit)

    return q.all()
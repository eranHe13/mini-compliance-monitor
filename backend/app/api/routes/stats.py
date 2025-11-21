from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session 
from sqlalchemy import func

from app.db.deps import get_db
from app import  models
from app.services.stats_service import get_summary_stats

stats_router = APIRouter()

@stats_router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    '''
    Return basic stats summary :
    - total number of events 
    - total number of findings
    - finding by severity
    - events by events_type 

    '''
    return get_summary_stats(db)
from typing import List
from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session 

from app import schemas , models
from app.db.deps import get_db
from app.services.events_service import query_events
events_router = APIRouter()

@events_router.get("" , response_model=List[schemas.SourceEvent])
def list_events(
    filters: schemas.SourceEventFilter = Depends(),
    db: Session = Depends(get_db)):
    '''
    List source events with optional filters and basic pagination.
    - user: Filter by user
    - event_type: Filter by event type
    - from_timestamp: Filter by from timestamp
    - to_timestamp: Filter by to timestamp
    - limit: Max number of results to return
    - offset: Numbers of result to skip
    '''

    return query_events(db , filters)
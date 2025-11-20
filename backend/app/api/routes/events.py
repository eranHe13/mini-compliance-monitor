from typing import List
from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session 

from app import schemas , models
from app.db.deps import get_db

events_router = APIRouter()

@events_router.get("/" , response_model=List[schemas.SourceEvent])
def list_events(db: Session = Depends(get_db)):
    '''
    Return all source events (not filtered)
    '''

    events = db.query(models.SourceEvent).all()
    #print(events)
    return events

    
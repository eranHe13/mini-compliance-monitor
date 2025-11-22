# backend/app/schemas/source_event.py

from pydantic import BaseModel
from datetime import datetime
from typing import Any, Optional

class SourceEventBase(BaseModel):
    event_type: str
    user: str
    raw_data :Any

class SourceEventCreate(SourceEventBase):
    pass

class SourceEvent(SourceEventBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class SourceEventFilter(BaseModel):
    user: Optional[str] = None
    event_type: Optional[str]= None
    from_timestamp: Optional[datetime] = None
    to_timestamp: Optional[datetime] = None
    limit: int = 50
    offset: int = 0
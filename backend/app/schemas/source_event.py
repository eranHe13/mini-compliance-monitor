

from pydantic import BaseModel
from datetime import datetime
from typing import Any

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
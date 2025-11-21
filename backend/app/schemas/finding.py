from pydantic import BaseModel 
from datetime import datetime
from typing import Optional

class FindingBase(BaseModel):
    rule_name:str
    severity:str
    description:str
    user:str

class FindingCreate(FindingBase):
    pass

class Finding(FindingBase):
    id:int
    timestamp:datetime

    class Config: orm_mode = True
    
class FindingFilter(BaseModel):
    severity: Optional[str] = None
    user: Optional[str] = None
    from_timestamp: Optional[datetime] = None
    to_timestamp: Optional[datetime] = None
    limit: int = 50
    offset: int = 0


# backend/app/schemas/finding.py
from pydantic import BaseModel 
from datetime import datetime
from typing import Optional , List

class FindingBase(BaseModel):
    rule_name:str
    severity:str
    description:str
    user: Optional[str] = None

    ai_explanation: Optional[str] = None
    risk_score: Optional[float] = None

class FindingCreate(FindingBase):
    pass

class Finding(FindingBase):
    id:int
    created_at:datetime

    class Config: orm_mode = True
    
class FindingFilter(BaseModel):
    severity: Optional[str] = None
    user: Optional[str] = None
    from_timestamp: Optional[datetime] = None
    to_timestamp: Optional[datetime] = None
    limit: int = 50
    offset: int = 0

class PaginatedFindings(BaseModel):
    items: List[Finding]
    total: int
    page: int
    page_size: int

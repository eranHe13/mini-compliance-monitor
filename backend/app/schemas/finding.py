from pydantic import BaseModel
from datetime import datetime


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
    
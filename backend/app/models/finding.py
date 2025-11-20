from sqlalchemy import Column, Integer, String, DateTime, JSON
from app.db.base import Base
from datetime import datetime


class Finding(Base):
    __tablename__="findings"
    id = Column(Integer , primary_key=True , index=True)
    rule_name = Column(String , index =True)
    severity = Column(String , index =True)
    description = Column(String , index =True)
    user = Column(String , index = True)
    timestamp = Column(DateTime , default= datetime.utcnow)
    
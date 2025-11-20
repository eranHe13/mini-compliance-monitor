from sqlalchemy import Column , Integer , String , DateTime , JSON , Boolean
from app.db.base import Base
from datetime import datetime

class SourceEvent(Base):
    __tablename__= "source_events"

    id = Column(Integer , primary_key=True , index=True )
    event_type= Column(String , index=True) 
    user = Column(String , index=True)
    raw_data= Column(JSON)
    timestamp = Column(DateTime , default= datetime.utcnow)
    processed = Column(Boolean , default=False , index=True)

    
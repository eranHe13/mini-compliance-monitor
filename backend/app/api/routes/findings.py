from typing import List 
from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session 

from app.db.deps import get_db
from app import schemas , models

findings_router = APIRouter()

@findings_router.get("/" , response_model = List[schemas.Finding])
def list_findings(db : Session = Depends(get_db)):
    '''
    Return all findings (not filtered yet)
    '''

    findings = db.query(models.Finding).all( )
    return findings


from typing import List  ,Optional
from datetime import datetime

from fastapi import APIRouter , Depends , Query
from sqlalchemy.orm import Session 

from app.db.deps import get_db
from app import schemas , models
from app.services.findings_service import query_findings


findings_router = APIRouter()

@findings_router.get("" , response_model = List[schemas.Finding])
def list_findings(
    filters : schemas.FindingFilter = Depends(),
    db : Session = Depends(get_db)
):
    return query_findings(db , filters)



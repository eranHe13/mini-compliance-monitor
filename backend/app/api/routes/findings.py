# backend/app/api/routes/findings.py

from typing import List  ,Optional
from datetime import datetime

from fastapi import APIRouter , Depends , Query
from sqlalchemy.orm import Session 

from app.db.deps import get_db
from app import schemas , models
from app.services.findings_service import query_findings
from app.schemas.finding import PaginatedFindings

findings_router = APIRouter()

@findings_router.get("" , response_model =PaginatedFindings)
def list_findings(
    page: int = Query(1 , ge=1),
    page_size:int = Query(20 , ge=1 , le=100),
    severity: Optional[str] =None,
    user: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    db : Session = Depends(get_db)
):
    return query_findings( db=db,
        page=page,
        page_size=page_size,
        severity=severity,
        user=user,
        from_date=from_date,
        to_date=to_date,
        )



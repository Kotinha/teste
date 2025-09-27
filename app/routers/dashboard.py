from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/{church_id}", response_model=schemas.DashboardSummary)
def get_dashboard(church_id: int, db: Session = Depends(get_db)) -> schemas.DashboardSummary:
    summary = crud.build_dashboard_summary(db, church_id=church_id)
    return summary

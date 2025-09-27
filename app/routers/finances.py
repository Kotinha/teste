from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/finances", tags=["Finanças"])


@router.post("/tithes", response_model=schemas.TitheRead, status_code=status.HTTP_201_CREATED)
def create_tithe(
    tithe_in: schemas.TitheCreate, db: Session = Depends(get_db)
) -> schemas.TitheRead:
    tithe = crud.record_tithe(db, tithe_in)
    return schemas.TitheRead.from_orm(tithe)


@router.get("/tithes", response_model=List[schemas.TitheRead])
def read_tithes(
    member_id: Optional[int] = Query(default=None), db: Session = Depends(get_db)
) -> List[schemas.TitheRead]:
    tithes = crud.list_tithes(db, member_id=member_id)
    return [schemas.TitheRead.from_orm(tithe) for tithe in tithes]


@router.post(
    "/offerings",
    response_model=schemas.OfferingRead,
    status_code=status.HTTP_201_CREATED,
)
def create_offering(
    offering_in: schemas.OfferingCreate, db: Session = Depends(get_db)
) -> schemas.OfferingRead:
    offering = crud.record_offering(db, offering_in)
    return schemas.OfferingRead.from_orm(offering)


@router.get("/offerings", response_model=List[schemas.OfferingRead])
def read_offerings(
    church_id: Optional[int] = Query(default=None),
    ministry_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[schemas.OfferingRead]:
    offerings = crud.list_offerings(db, church_id=church_id, ministry_id=ministry_id)
    return [schemas.OfferingRead.from_orm(offering) for offering in offerings]

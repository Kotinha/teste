from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/ministries", tags=["Ministérios"])


@router.post("/", response_model=schemas.MinistryRead, status_code=status.HTTP_201_CREATED)
def create_ministry(
    ministry_in: schemas.MinistryCreate, db: Session = Depends(get_db)
) -> schemas.MinistryRead:
    ministry = crud.create_ministry(db, ministry_in)
    return schemas.MinistryRead.from_orm(ministry)


@router.get("/", response_model=List[schemas.MinistryRead])
def read_ministries(
    church_id: Optional[int] = Query(default=None), db: Session = Depends(get_db)
) -> List[schemas.MinistryRead]:
    ministries = crud.list_ministries(db, church_id=church_id)
    return [schemas.MinistryRead.from_orm(ministry) for ministry in ministries]


@router.get("/{ministry_id}", response_model=schemas.MinistryRead)
def read_ministry(ministry_id: int, db: Session = Depends(get_db)) -> schemas.MinistryRead:
    ministry = crud.get_ministry(db, ministry_id)
    if ministry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ministério não encontrado")
    return schemas.MinistryRead.from_orm(ministry)


@router.put("/{ministry_id}", response_model=schemas.MinistryRead)
def update_ministry(
    ministry_id: int, ministry_in: schemas.MinistryUpdate, db: Session = Depends(get_db)
) -> schemas.MinistryRead:
    ministry = crud.get_ministry(db, ministry_id)
    if ministry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ministério não encontrado")
    updated = crud.update_ministry(db, ministry, ministry_in)
    return schemas.MinistryRead.from_orm(updated)


@router.delete("/{ministry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ministry(ministry_id: int, db: Session = Depends(get_db)) -> None:
    ministry = crud.get_ministry(db, ministry_id)
    if ministry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ministério não encontrado")
    crud.delete_ministry(db, ministry)

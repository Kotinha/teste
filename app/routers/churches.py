from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/churches", tags=["Churches"])


@router.post("/", response_model=schemas.ChurchRead, status_code=status.HTTP_201_CREATED)
def create_church(
    church_in: schemas.ChurchCreate, db: Session = Depends(get_db)
) -> schemas.ChurchRead:
    church = crud.create_church(db, church_in)
    return schemas.ChurchRead.from_orm(church)


@router.get("/", response_model=List[schemas.ChurchRead])
def read_churches(db: Session = Depends(get_db)) -> List[schemas.ChurchRead]:
    churches = crud.list_churches(db)
    return [schemas.ChurchRead.from_orm(church) for church in churches]


@router.get("/{church_id}", response_model=schemas.ChurchRead)
def read_church(church_id: int, db: Session = Depends(get_db)) -> schemas.ChurchRead:
    church = crud.get_church(db, church_id)
    if church is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Igreja não encontrada")
    return schemas.ChurchRead.from_orm(church)


@router.delete("/{church_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_church(church_id: int, db: Session = Depends(get_db)) -> None:
    deleted = crud.delete_church(db, church_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Igreja não encontrada")

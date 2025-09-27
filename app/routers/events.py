from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/events", tags=["Eventos"])


@router.post("/", response_model=schemas.EventRead, status_code=status.HTTP_201_CREATED)
def create_event(
    event_in: schemas.EventCreate, db: Session = Depends(get_db)
) -> schemas.EventRead:
    event = crud.create_event(db, event_in)
    return schemas.EventRead.from_orm(event)


@router.get("/", response_model=List[schemas.EventRead])
def read_events(
    church_id: Optional[int] = Query(default=None),
    ministry_id: Optional[int] = Query(default=None),
    upcoming_only: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> List[schemas.EventRead]:
    events = crud.list_events(
        db,
        church_id=church_id,
        ministry_id=ministry_id,
        upcoming_only=upcoming_only,
    )
    return [schemas.EventRead.from_orm(event) for event in events]


@router.get("/{event_id}", response_model=schemas.EventRead)
def read_event(event_id: int, db: Session = Depends(get_db)) -> schemas.EventRead:
    event = crud.get_event(db, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado")
    return schemas.EventRead.from_orm(event)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db)) -> None:
    event = crud.get_event(db, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado")
    crud.delete_event(db, event)

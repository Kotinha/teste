from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/members", tags=["Membros"])


@router.post("/", response_model=schemas.MemberRead, status_code=status.HTTP_201_CREATED)
def create_member(
    member_in: schemas.MemberCreate, db: Session = Depends(get_db)
) -> schemas.MemberRead:
    member = crud.create_member(db, member_in)
    return schemas.MemberRead.from_orm(member)


@router.get("/", response_model=List[schemas.MemberRead])
def read_members(
    church_id: Optional[int] = Query(default=None),
    active_only: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> List[schemas.MemberRead]:
    members = crud.list_members(db, church_id=church_id, active_only=active_only)
    return [schemas.MemberRead.from_orm(member) for member in members]


@router.get("/{member_id}", response_model=schemas.MemberRead)
def read_member(member_id: int, db: Session = Depends(get_db)) -> schemas.MemberRead:
    member = crud.get_member(db, member_id)
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membro não encontrado")
    return schemas.MemberRead.from_orm(member)


@router.put("/{member_id}", response_model=schemas.MemberRead)
def update_member(
    member_id: int, member_in: schemas.MemberUpdate, db: Session = Depends(get_db)
) -> schemas.MemberRead:
    member = crud.get_member(db, member_id)
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membro não encontrado")
    updated = crud.update_member(db, member, member_in)
    return schemas.MemberRead.from_orm(updated)


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: Session = Depends(get_db)) -> None:
    member = crud.get_member(db, member_id)
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membro não encontrado")
    crud.delete_member(db, member)


@router.post(
    "/{member_id}/ministries",
    response_model=schemas.MinistryMembershipRead,
    status_code=status.HTTP_201_CREATED,
)
def add_member_ministry(
    member_id: int,
    payload: schemas.MinistryMembershipCreate,
    db: Session = Depends(get_db),
) -> schemas.MinistryMembershipRead:
    if member_id != payload.member_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="member_id inconsistente")
    membership = crud.add_member_to_ministry(db, payload)
    return schemas.MinistryMembershipRead.from_orm(membership)


@router.delete("/{member_id}/ministries/{ministry_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member_ministry(
    member_id: int, ministry_id: int, db: Session = Depends(get_db)
) -> None:
    removed = crud.remove_member_from_ministry(db, ministry_id=ministry_id, member_id=member_id)
    if not removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vínculo não encontrado")

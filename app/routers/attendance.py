from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/attendance", tags=["Presenças"])


@router.post("/", response_model=schemas.AttendanceRead, status_code=status.HTTP_201_CREATED)
def create_attendance(
    attendance_in: schemas.AttendanceCreate, db: Session = Depends(get_db)
) -> schemas.AttendanceRead:
    attendance = crud.record_attendance(db, attendance_in)
    return schemas.AttendanceRead.from_orm(attendance)


@router.get("/", response_model=List[schemas.AttendanceRead])
def read_attendance(
    event_id: Optional[int] = Query(default=None),
    member_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[schemas.AttendanceRead]:
    records = crud.list_attendance(db, event_id=event_id, member_id=member_id)
    return [schemas.AttendanceRead.from_orm(record) for record in records]


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)) -> None:
    attendance = db.get(models.Attendance, attendance_id)
    if attendance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro não encontrado")
    crud.delete_attendance(db, attendance)

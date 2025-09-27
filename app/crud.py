from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from . import models, schemas


# Church CRUD

def create_church(session: Session, church_in: schemas.ChurchCreate) -> models.Church:
    church = models.Church(**church_in.dict())
    session.add(church)
    session.commit()
    session.refresh(church)
    return church


def list_churches(session: Session) -> List[models.Church]:
    return session.execute(select(models.Church)).scalars().all()


def get_church(session: Session, church_id: int) -> Optional[models.Church]:
    return session.get(models.Church, church_id)


def delete_church(session: Session, church_id: int) -> bool:
    church = get_church(session, church_id)
    if church is None:
        return False
    session.delete(church)
    session.commit()
    return True


# Ministry CRUD

def create_ministry(
    session: Session, ministry_in: schemas.MinistryCreate
) -> models.Ministry:
    ministry = models.Ministry(**ministry_in.dict())
    session.add(ministry)
    session.commit()
    session.refresh(ministry)
    return ministry


def list_ministries(session: Session, church_id: Optional[int] = None) -> List[models.Ministry]:
    stmt = select(models.Ministry)
    if church_id is not None:
        stmt = stmt.where(models.Ministry.church_id == church_id)
    return session.execute(stmt).scalars().all()


def get_ministry(session: Session, ministry_id: int) -> Optional[models.Ministry]:
    return session.get(models.Ministry, ministry_id)


def update_ministry(
    session: Session, ministry: models.Ministry, ministry_in: schemas.MinistryUpdate
) -> models.Ministry:
    for field, value in ministry_in.dict(exclude_unset=True).items():
        setattr(ministry, field, value)
    session.add(ministry)
    session.commit()
    session.refresh(ministry)
    return ministry


def delete_ministry(session: Session, ministry: models.Ministry) -> None:
    session.delete(ministry)
    session.commit()


# Member CRUD

def create_member(session: Session, member_in: schemas.MemberCreate) -> models.Member:
    member = models.Member(**member_in.dict())
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


def list_members(
    session: Session, *, church_id: Optional[int] = None, active_only: bool = False
) -> List[models.Member]:
    stmt = select(models.Member)
    if church_id is not None:
        stmt = stmt.where(models.Member.church_id == church_id)
    if active_only:
        stmt = stmt.where(models.Member.is_active.is_(True))
    return session.execute(stmt).scalars().all()


def get_member(session: Session, member_id: int) -> Optional[models.Member]:
    return session.get(models.Member, member_id)


def update_member(
    session: Session, member: models.Member, member_in: schemas.MemberUpdate
) -> models.Member:
    for field, value in member_in.dict(exclude_unset=True).items():
        setattr(member, field, value)
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


def delete_member(session: Session, member: models.Member) -> None:
    session.delete(member)
    session.commit()


# Ministry Membership CRUD

def add_member_to_ministry(
    session: Session, membership_in: schemas.MinistryMembershipCreate
) -> models.MinistryMembership:
    membership = models.MinistryMembership(**membership_in.dict())
    session.add(membership)
    session.commit()
    session.refresh(membership)
    return membership


def remove_member_from_ministry(
    session: Session, ministry_id: int, member_id: int
) -> bool:
    membership = session.get(
        models.MinistryMembership, {"ministry_id": ministry_id, "member_id": member_id}
    )
    if membership is None:
        return False
    session.delete(membership)
    session.commit()
    return True


# Tithe CRUD

def record_tithe(session: Session, tithe_in: schemas.TitheCreate) -> models.Tithe:
    data = tithe_in.dict()
    if data.get("received_at") is None:
        data["received_at"] = datetime.utcnow()
    tithe = models.Tithe(**data)
    session.add(tithe)
    session.commit()
    session.refresh(tithe)
    return tithe


def list_tithes(session: Session, member_id: Optional[int] = None) -> List[models.Tithe]:
    stmt = select(models.Tithe)
    if member_id is not None:
        stmt = stmt.where(models.Tithe.member_id == member_id)
    stmt = stmt.order_by(models.Tithe.received_at.desc())
    return session.execute(stmt).scalars().all()


# Offering CRUD

def record_offering(
    session: Session, offering_in: schemas.OfferingCreate
) -> models.Offering:
    data = offering_in.dict()
    if data.get("received_at") is None:
        data["received_at"] = datetime.utcnow()
    offering = models.Offering(**data)
    session.add(offering)
    session.commit()
    session.refresh(offering)
    return offering


def list_offerings(
    session: Session,
    *,
    church_id: Optional[int] = None,
    ministry_id: Optional[int] = None,
) -> List[models.Offering]:
    stmt = select(models.Offering)
    if church_id is not None:
        stmt = stmt.where(models.Offering.church_id == church_id)
    if ministry_id is not None:
        stmt = stmt.where(models.Offering.ministry_id == ministry_id)
    stmt = stmt.order_by(models.Offering.received_at.desc())
    return session.execute(stmt).scalars().all()


# Event CRUD

def create_event(session: Session, event_in: schemas.EventCreate) -> models.Event:
    event = models.Event(**event_in.dict())
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


def list_events(
    session: Session,
    *,
    church_id: Optional[int] = None,
    ministry_id: Optional[int] = None,
    upcoming_only: bool = False,
) -> List[models.Event]:
    stmt = select(models.Event)
    if church_id is not None:
        stmt = stmt.where(models.Event.church_id == church_id)
    if ministry_id is not None:
        stmt = stmt.where(models.Event.ministry_id == ministry_id)
    if upcoming_only:
        stmt = stmt.where(models.Event.start_at >= datetime.utcnow())
    stmt = stmt.order_by(models.Event.start_at.asc())
    return session.execute(stmt).scalars().all()


def get_event(session: Session, event_id: int) -> Optional[models.Event]:
    return session.get(models.Event, event_id)


def delete_event(session: Session, event: models.Event) -> None:
    session.delete(event)
    session.commit()


# Attendance CRUD

def record_attendance(
    session: Session, attendance_in: schemas.AttendanceCreate
) -> models.Attendance:
    attendance = models.Attendance(**attendance_in.dict())
    session.add(attendance)
    session.commit()
    session.refresh(attendance)
    return attendance


def list_attendance(
    session: Session,
    *,
    event_id: Optional[int] = None,
    member_id: Optional[int] = None,
) -> List[models.Attendance]:
    stmt = select(models.Attendance)
    if event_id is not None:
        stmt = stmt.where(models.Attendance.event_id == event_id)
    if member_id is not None:
        stmt = stmt.where(models.Attendance.member_id == member_id)
    return session.execute(stmt).scalars().all()


def delete_attendance(session: Session, attendance: models.Attendance) -> None:
    session.delete(attendance)
    session.commit()


# Dashboard helpers

def build_dashboard_summary(
    session: Session, *, church_id: int
) -> schemas.DashboardSummary:
    total_members = session.scalar(
        select(func.count(models.Member.id)).where(models.Member.church_id == church_id)
    ) or 0
    active_members = session.scalar(
        select(func.count(models.Member.id)).where(
            models.Member.church_id == church_id, models.Member.is_active.is_(True)
        )
    ) or 0
    total_tithes = session.scalar(
        select(func.coalesce(func.sum(models.Tithe.amount), 0.0)).join(models.Member).where(
            models.Member.church_id == church_id
        )
    ) or 0.0
    total_offerings = session.scalar(
        select(func.coalesce(func.sum(models.Offering.amount), 0.0)).where(
            models.Offering.church_id == church_id
        )
    ) or 0.0

    upcoming_events = list_events(
        session, church_id=church_id, upcoming_only=True
    )
    upcoming_events_read = [schemas.EventRead.from_orm(event) for event in upcoming_events]

    return schemas.DashboardSummary(
        total_members=total_members,
        active_members=active_members,
        total_tithes=float(total_tithes),
        total_offerings=float(total_offerings),
        upcoming_events=upcoming_events_read,
    )

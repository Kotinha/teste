from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class MinistryMembershipBase(BaseModel):
    ministry_id: int
    member_id: int
    role: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class MinistryMembershipCreate(MinistryMembershipBase):
    pass


class MinistryMembershipRead(MinistryMembershipBase):
    class Config:
        orm_mode = True


class ChurchBase(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class ChurchCreate(ChurchBase):
    pass


class ChurchRead(ChurchBase):
    id: int

    class Config:
        orm_mode = True


class MinistryBase(BaseModel):
    name: str
    description: Optional[str] = None


class MinistryCreate(MinistryBase):
    church_id: int


class MinistryUpdate(MinistryBase):
    pass


class MinistryRead(MinistryBase):
    id: int
    church_id: int

    class Config:
        orm_mode = True


class MemberBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = Field(default=None)
    phone: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[date] = None
    join_date: Optional[date] = None
    is_active: Optional[bool] = True


class MemberCreate(MemberBase):
    church_id: int


class MemberUpdate(MemberBase):
    pass


class MemberRead(MemberBase):
    id: int
    church_id: int

    class Config:
        orm_mode = True


class TitheBase(BaseModel):
    amount: float
    received_at: Optional[datetime] = None
    method: Optional[str] = None
    notes: Optional[str] = None


class TitheCreate(TitheBase):
    member_id: int


class TitheRead(TitheBase):
    id: int
    member_id: int

    class Config:
        orm_mode = True


class OfferingBase(BaseModel):
    amount: float
    received_at: Optional[datetime] = None
    category: Optional[str] = None
    description: Optional[str] = None


class OfferingCreate(OfferingBase):
    church_id: int
    ministry_id: Optional[int] = None


class OfferingRead(OfferingBase):
    id: int
    church_id: int
    ministry_id: Optional[int]

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_at: datetime
    end_at: Optional[datetime] = None
    location: Optional[str] = None


class EventCreate(EventBase):
    church_id: int
    ministry_id: Optional[int] = None


class EventRead(EventBase):
    id: int
    church_id: int
    ministry_id: Optional[int]

    class Config:
        orm_mode = True


class AttendanceBase(BaseModel):
    status: Optional[str] = "present"
    notes: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    event_id: int
    member_id: int


class AttendanceRead(AttendanceBase):
    id: int
    event_id: int
    member_id: int

    class Config:
        orm_mode = True


class DashboardSummary(BaseModel):
    total_members: int
    active_members: int
    total_tithes: float
    total_offerings: float
    upcoming_events: List[EventRead]

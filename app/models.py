from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Church(Base):
    __tablename__ = "churches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    state: Mapped[Optional[str]] = mapped_column(String(100))
    country: Mapped[Optional[str]] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[Optional[str]] = mapped_column(String(150))

    ministries: Mapped[List["Ministry"]] = relationship(
        back_populates="church", cascade="all, delete-orphan"
    )
    members: Mapped[List["Member"]] = relationship(
        back_populates="church", cascade="all, delete-orphan"
    )
    offerings: Mapped[List["Offering"]] = relationship(
        back_populates="church", cascade="all, delete-orphan"
    )
    events: Mapped[List["Event"]] = relationship(
        back_populates="church", cascade="all, delete-orphan"
    )


class Ministry(Base):
    __tablename__ = "ministries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    church_id: Mapped[int] = mapped_column(ForeignKey("churches.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text())

    church: Mapped[Church] = relationship(back_populates="ministries")
    members: Mapped[List["MinistryMembership"]] = relationship(
        back_populates="ministry", cascade="all, delete-orphan"
    )
    offerings: Mapped[List["Offering"]] = relationship(back_populates="ministry")
    events: Mapped[List["Event"]] = relationship(back_populates="ministry")


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    church_id: Mapped[int] = mapped_column(ForeignKey("churches.id", ondelete="CASCADE"))
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    address: Mapped[Optional[str]] = mapped_column(String(255))
    birth_date: Mapped[Optional[date]] = mapped_column(Date())
    join_date: Mapped[date] = mapped_column(Date(), default=date.today)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    church: Mapped[Church] = relationship(back_populates="members")
    ministries: Mapped[List["MinistryMembership"]] = relationship(
        back_populates="member", cascade="all, delete-orphan"
    )
    tithes: Mapped[List["Tithe"]] = relationship(
        back_populates="member", cascade="all, delete-orphan"
    )
    attendances: Mapped[List["Attendance"]] = relationship(
        back_populates="member", cascade="all, delete-orphan"
    )


class MinistryMembership(Base):
    __tablename__ = "ministry_memberships"

    ministry_id: Mapped[int] = mapped_column(
        ForeignKey("ministries.id", ondelete="CASCADE"), primary_key=True
    )
    member_id: Mapped[int] = mapped_column(
        ForeignKey("members.id", ondelete="CASCADE"), primary_key=True
    )
    role: Mapped[Optional[str]] = mapped_column(String(150))
    start_date: Mapped[Optional[date]] = mapped_column(Date())
    end_date: Mapped[Optional[date]] = mapped_column(Date())

    ministry: Mapped[Ministry] = relationship(back_populates="members")
    member: Mapped[Member] = relationship(back_populates="ministries")


class Tithe(Base):
    __tablename__ = "tithes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(
        ForeignKey("members.id", ondelete="CASCADE"), nullable=False
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    method: Mapped[Optional[str]] = mapped_column(String(50))
    notes: Mapped[Optional[str]] = mapped_column(Text())

    member: Mapped[Member] = relationship(back_populates="tithes")


class Offering(Base):
    __tablename__ = "offerings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    church_id: Mapped[int] = mapped_column(
        ForeignKey("churches.id", ondelete="CASCADE"), nullable=False
    )
    ministry_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("ministries.id", ondelete="SET NULL"), nullable=True
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    category: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text())

    church: Mapped[Church] = relationship(back_populates="offerings")
    ministry: Mapped[Optional[Ministry]] = relationship(back_populates="offerings")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    church_id: Mapped[int] = mapped_column(
        ForeignKey("churches.id", ondelete="CASCADE"), nullable=False
    )
    ministry_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("ministries.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text())
    start_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    location: Mapped[Optional[str]] = mapped_column(String(255))

    church: Mapped[Church] = relationship(back_populates="events")
    ministry: Mapped[Optional[Ministry]] = relationship(back_populates="events")
    attendance: Mapped[List["Attendance"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )


class Attendance(Base):
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    member_id: Mapped[int] = mapped_column(
        ForeignKey("members.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(50), default="present")
    notes: Mapped[Optional[str]] = mapped_column(Text())

    event: Mapped[Event] = relationship(back_populates="attendance")
    member: Mapped[Member] = relationship(back_populates="attendances")

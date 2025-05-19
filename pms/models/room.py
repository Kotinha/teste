from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=False, default='available')
    type = Column(String, nullable=False, default='standard')

    reservations = relationship('Reservation', back_populates='room')

    def __repr__(self):
        return f"<Room {self.number} ({self.status})>"

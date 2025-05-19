from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True)
    guest_name = Column(String, nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'))

    room = relationship('Room', back_populates='reservations')

    def __repr__(self):
        return (
            f"<Reservation {self.guest_name} {self.check_in} - "
            f"{self.check_out}>"
        )

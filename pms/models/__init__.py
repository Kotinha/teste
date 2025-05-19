from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .room import Room

engine = create_engine('sqlite:///pms.db', echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()


def init_db():
    """Create database tables and default rooms."""
    Base.metadata.create_all(bind=engine)

    # Populate default rooms if none exist
    session = SessionLocal()
    if session.query(Room).count() == 0:
        for i in range(1, 10):
            room = Room(number=str(i), status="available", type="standard")
            session.add(room)
        session.commit()
    session.close()

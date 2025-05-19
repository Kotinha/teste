# Pousada Management System

This project provides a minimal PMS (Pousada Management System) using Flask and SQLAlchemy with SQLite.

## Requirements

- Python 3.8+
- Packages listed in `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Initialize the database and start the server:

```bash
python -m pms.app
```

The application will create a `pms.db` SQLite file in the project directory.

### Adding Rooms

To add the initial 9 rooms run the following commands in a Python shell:

```python
from pms.models import init_db, SessionLocal
from pms.models.room import Room

init_db()
session = SessionLocal()
for i in range(1, 10):
    room = Room(number=str(i), status='available', type='standard')
    session.add(room)
session.commit()
session.close()
```

## Project Structure

- `pms/models/` – SQLAlchemy models for rooms and reservations
- `pms/routes/` – API routes
- `pms/templates/` – basic HTML templates for rooms and reservations
- `pms/app.py` – Flask application entry point

This setup provides a simple starting point to manage room availability and reservations for a 9-room guesthouse.

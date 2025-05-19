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

The application will create a `pms.db` SQLite file in the project directory and
automatically populate nine default rooms if none exist.

### Checking Available Rooms

Use the `/rooms/available` endpoint to list rooms free for a date range:

```bash
GET /rooms/available?check_in=2024-01-01&check_out=2024-01-05
```

## Project Structure

- `pms/models/` – SQLAlchemy models for rooms and reservations
- `pms/routes/` – API routes
- `pms/templates/` – basic HTML templates for rooms and reservations
- `pms/app.py` – Flask application entry point

This setup provides a simple starting point to manage room availability and reservations for a 9-room guesthouse.

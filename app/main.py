from __future__ import annotations

from fastapi import FastAPI

from .database import Base, engine
from .routers import attendance, churches, dashboard, events, finances, members, ministries

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Gestão de Igrejas")

app.include_router(churches.router)
app.include_router(ministries.router)
app.include_router(members.router)
app.include_router(finances.router)
app.include_router(events.router)
app.include_router(attendance.router)
app.include_router(dashboard.router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Bem-vindo ao Sistema de Gestão de Igrejas"}

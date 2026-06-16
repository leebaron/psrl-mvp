"""services/api/routes/memory.py — Memory + Reminder routes."""

from fastapi import APIRouter
from services.api.memory import save, search
from services.api.db import get_conn

router = APIRouter()


@router.post("/")
def add_memory(data: dict):
    save(data.get("content", ""))
    return {"ok": True}


@router.get("/")
def list_memory(query: str = ""):
    return {"memories": search(query)}


@router.post("/reminder")
def set_reminder(data: dict):
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            remind_at TEXT,
            done INTEGER DEFAULT 0
        )
    """)
    conn.execute(
        "INSERT INTO reminders (content, remind_at) VALUES (?, ?)",
        (data.get("content", ""), data.get("time", ""))
    )
    conn.commit()
    conn.close()
    return {"ok": True}

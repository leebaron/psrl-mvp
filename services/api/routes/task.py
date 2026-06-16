"""services/api/routes/task.py — Task + Intent routes."""

from fastapi import APIRouter
from services.api.db import get_conn
from services.api.llm import parse_intent

router = APIRouter()


@router.post("/")
def create_task(content: str):
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("INSERT INTO tasks (content, status) VALUES (?, 'pending')", (content,))
    conn.commit()
    conn.close()
    return {"ok": True, "content": content}


@router.get("/")
def list_tasks():
    conn = get_conn()
    conn.row_factory = __import__('sqlite3').Row
    rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    conn.close()
    return {"tasks": [dict(r) for r in rows]}


@router.post("/done/{task_id}")
def done_task(task_id: int):
    conn = get_conn()
    conn.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return {"ok": True}


@router.post("/intent")
def intent(data: dict):
    result = parse_intent(data.get("text", ""))
    return result

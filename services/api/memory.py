"""services/api/memory.py — Memory with embedding-based semantic search.

SQLite fallback: cosine similarity computed in Python.
Production: pgvector (PostgreSQL extension).
"""

import json
import math
from services.api.db import get_conn
from services.api.embeddings import embed, configured as emb_ok


def _cosine_sim(a: list, b: list) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb + 1e-10)


def save(content: str) -> dict:
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            embedding TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    # Migrate: add embedding column if missing (ignore if exists)
    try:
        conn.execute("ALTER TABLE memory ADD COLUMN embedding TEXT")
        conn.commit()
    except Exception:
        pass
    vec = embed(content) if emb_ok() else None
    conn.execute(
        "INSERT INTO memory (content, embedding) VALUES (?, ?)",
        (content, json.dumps(vec) if vec else None),
    )
    conn.commit()
    conn.close()
    return {"saved": True, "content": content}


def search(query: str = "", limit: int = 10) -> list:
    conn = get_conn()
    conn.row_factory = __import__('sqlite3').Row
    rows = conn.execute(
        "SELECT * FROM memory ORDER BY id DESC LIMIT 100"
    ).fetchall()
    conn.close()

    results = [dict(r) for r in rows]

    # Embedding search
    if query and emb_ok():
        qvec = embed(query)
        scored = []
        for r in results:
            if r.get("embedding"):
                try:
                    rvec = json.loads(r["embedding"])
                    score = _cosine_sim(qvec, rvec)
                    scored.append((score, r))
                except (json.JSONDecodeError, TypeError):
                    scored.append((0.0, r))
            else:
                # Keyword fallback for unembedded records
                score = 1.0 if query.lower() in r.get("content", "").lower() else 0.0
                scored.append((score, r))
        scored.sort(key=lambda x: -x[0])
        results = [r for _, r in scored[:limit]]
    elif query:
        # Pure keyword fallback
        results = [r for r in results if query.lower() in r.get("content", "").lower()]
        results = results[:limit]

    return results

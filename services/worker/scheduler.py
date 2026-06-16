"""services/worker/scheduler.py — Reminder checker."""

import time
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))

from db import get_conn
from notify import send_telegram

CHECK_INTERVAL = int(os.environ.get("WORKER_INTERVAL", "30"))


def check_reminders() -> int:
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            remind_at TEXT,
            done INTEGER DEFAULT 0
        )
    """)
    conn.row_factory = __import__('sqlite3').Row
    rows = conn.execute(
        "SELECT id, content FROM reminders WHERE done=0 AND remind_at <= datetime('now')"
    ).fetchall()
    count = 0
    for row in rows:
        send_telegram(f"🔔 提醒：{row['content']}")
        conn.execute("UPDATE reminders SET done=1 WHERE id=?", (row["id"],))
        count += 1
    conn.commit()
    conn.close()
    return count


def run():
    print(f"🔄 PSRL Worker started (check every {CHECK_INTERVAL}s)")
    while True:
        try:
            count = check_reminders()
            if count:
                print(f"   → {count} reminders sent")
        except Exception as e:
            print(f"⚠️ worker error: {e}")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run()

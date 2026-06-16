"""worker/worker.py — Reminder worker entry."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.worker.scheduler import run

if __name__ == "__main__":
    run()

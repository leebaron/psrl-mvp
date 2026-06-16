"""services/worker/notify.py — Telegram notification."""

import os
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")


def send_telegram(text: str) -> bool:
    if not BOT_TOKEN or not CHAT_ID:
        print(f"⚠️ notify: {text[:50]}...")
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": text})
        return r.ok
    except Exception as e:
        print(f"⚠️ Telegram send error: {e}")
        return False

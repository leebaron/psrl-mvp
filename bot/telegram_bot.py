"""bot/telegram_bot.py — PSRL Telegram Bot (v0.2 with intent)."""

import os
import json
import requests

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

API = "http://api:8000"


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Query intent via API
    try:
        res = requests.post(f"{API}/task/intent", json={"text": text}, timeout=5)
        data = res.json()
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")
        return

    intent = data.get("intent", "query")
    content = data.get("content", text)

    if intent == "task":
        requests.post(f"{API}/task/", params={"content": content})
        await update.message.reply_text(f"✅ 任務已建立：{content[:50]}")

    elif intent == "memory":
        requests.post(f"{API}/memory/", json={"content": content})
        await update.message.reply_text(f"🧠 已記住：{content[:50]}")

    elif intent == "reminder":
        time = data.get("time")
        payload = {"content": content, "time": time or "2026-06-17 09:00"}
        requests.post(f"{API}/memory/reminder", json=payload)
        await update.message.reply_text(f"🔔 提醒已設定：{content[:50]}")

    elif intent == "query":
        res = requests.get(f"{API}/memory/", params={"query": text}).json()
        mems = res.get("memories", [])
        if mems:
            reply = "\n".join([f"  • {m['content'][:60]}" for m in mems[:5]])
            await update.message.reply_text(f"📖 記憶結果：\n{reply}")
        else:
            # Show tasks
            res = requests.get(f"{API}/task/").json()
            tasks = res.get("tasks", [])
            if tasks:
                reply = "\n".join([f"  {t['id']}. {t['content'][:50]} ({t['status']})" for t in tasks[:10]])
                await update.message.reply_text(f"📋 任務列表：\n{reply}")
            else:
                await update.message.reply_text(f"🤖 {text}")

    else:
        await update.message.reply_text(f"🤖 已收到：{text[:60]}")


def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        print("⚠️ TELEGRAM_TOKEN not set")
        return

    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
    print("🤖 PSRL Bot (v0.2) running")
    app.run_polling()


if __name__ == "__main__":
    main()

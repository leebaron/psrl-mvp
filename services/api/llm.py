"""services/api/llm.py — LLM Intent Engine (gpt-4o-mini, openai v1.x)."""

import os
import json
from openai import OpenAI

_client = None


def _get_client():
    global _client
    if _client is None:
        key = os.environ.get("OPENAI_API_KEY", "")
        if key:
            _client = OpenAI(api_key=key)
    return _client


def configured() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY"))


def parse_intent(text: str) -> dict:
    """Classify input into task/reminder/memory/query via LLM. Falls back to rule."""
    client = _get_client()
    if not client:
        return _rule_fallback(text)

    prompt = """你是私人秘書的意圖分類器。
把輸入分類為：task / reminder / memory / query
輸出 JSON: {"intent": "...", "content": "...", "time": "... or null"}
只輸出 JSON，不加說明。"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"{prompt}\n\n輸入：{text}"}],
            temperature=0.1,
        )
        content = res.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        return json.loads(content)
    except Exception as e:
        print(f"⚠️ LLM error: {e}")
        return _rule_fallback(text)


def _rule_fallback(text: str) -> dict:
    t = text.lower()
    if any(k in t for k in ["記住", "memory", "記錄", "記"]):
        return {"intent": "memory", "content": text, "time": None}
    if any(k in t for k in ["提醒", "remind"]):
        return {"intent": "reminder", "content": text, "time": None}
    if any(k in t for k in ["做", "task", "任務"]):
        return {"intent": "task", "content": text, "time": None}
    return {"intent": "query", "content": text, "time": None}

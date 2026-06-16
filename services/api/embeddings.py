"""services/api/embeddings.py — Embedding service (OpenAI v1.x)."""

import os
from openai import OpenAI

_client = None
MODEL = "text-embedding-3-small"


def _get_client():
    global _client
    if _client is None:
        key = os.environ.get("OPENAI_API_KEY", "")
        if key:
            _client = OpenAI(api_key=key)
    return _client


def configured() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY"))


def embed(text: str) -> list:
    """Return embedding vector for text."""
    client = _get_client()
    if not client:
        return [0.0] * 384
    try:
        r = client.embeddings.create(input=text, model=MODEL)
        return r.data[0].embedding
    except Exception as e:
        print(f"⚠️ embedding error: {e}")
        return [0.0] * 384

"""services/api/routes/health.py — Health check."""

from fastapi import APIRouter
from services.api.llm import configured as llm_ok

router = APIRouter()


@router.get("/")
def health():
    return {"status": "ok", "version": "0.2", "llm": llm_ok()}

"""services/api/main.py — PSRL FastAPI entry (v0.3)."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from services.api.routes.task import router as task_router
from services.api.routes.memory import router as memory_router
from services.api.routes.health import router as health_router
from services.web.ui import router as ui_router

app = FastAPI(title="PSRL v0.3", description="Personal Secretary Runtime Layer")

app.include_router(task_router, prefix="/task")
app.include_router(memory_router, prefix="/memory")
app.include_router(health_router, prefix="/health")
app.include_router(ui_router, prefix="")
app.mount("/static", StaticFiles(directory="services/web"), name="static")


@app.on_event("startup")
def startup():
    print("🧠 PSRL v0.3 ready")

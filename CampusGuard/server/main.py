from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import init_db
from .routers import admin, alerts, auth, health, insights, reports, sos
from .services.triage import warm_model

app = FastAPI(title="CampusGuard", description="Local campus safety prototype")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(sos.router)
app.include_router(reports.router)
app.include_router(alerts.router)
app.include_router(insights.router)
app.include_router(health.router)
app.include_router(admin.router)
app.include_router(auth.router)


@app.on_event("startup")
def startup() -> None:
    init_db()
    warm_model()

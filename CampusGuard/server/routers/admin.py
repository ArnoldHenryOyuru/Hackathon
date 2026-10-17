from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from ..db import connection
from ..schemas import ResponderRequest
from ..auth import admin_required
from ..services.stats import build_stats

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/overview")
def overview(_: dict[str, str] = Depends(admin_required)) -> dict[str, Any]:
    with connection() as db:
        rows = db.execute(
            """SELECT id, type, created_at, location, category, priority, status,
                      triage_source, triage_pending
               FROM alerts
               ORDER BY created_at DESC
               LIMIT 8"""
        ).fetchall()
    recent = [dict(row) for row in rows]
    with connection() as db:
        responders = [dict(row) for row in db.execute(
            "SELECT * FROM responders ORDER BY role, name"
        ).fetchall()]
    return {"stats": build_stats(), "recent_alerts": recent, "responders": responders}


@router.get("/responders")
def list_responders(_: dict[str, str] = Depends(admin_required)) -> list[dict[str, Any]]:
    with connection() as db:
        return [dict(row) for row in db.execute(
            "SELECT * FROM responders ORDER BY role, name"
        ).fetchall()]


@router.post("/responders")
def add_responder(payload: ResponderRequest, _: dict[str, str] = Depends(admin_required)) -> dict[str, Any]:
    with connection() as db:
        cursor = db.execute(
            "INSERT INTO responders (name, role, phone, email, notes) VALUES (?, ?, ?, ?, ?)",
            (payload.name.strip(), payload.role, payload.phone.strip(),
             payload.email.strip() if payload.email else None,
             payload.notes.strip() if payload.notes else None),
        )
        row = db.execute("SELECT * FROM responders WHERE id=?", (cursor.lastrowid,)).fetchone()
    return dict(row)


@router.delete("/responders/{responder_id}")
def remove_responder(responder_id: int, _: dict[str, str] = Depends(admin_required)) -> dict[str, Any]:
    with connection() as db:
        cursor = db.execute("DELETE FROM responders WHERE id=?", (responder_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Responder not found.")
    return {"id": responder_id, "message": "Responder removed."}

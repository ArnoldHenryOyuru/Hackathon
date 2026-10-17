from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi import HTTPException

from ..db import connection
from ..schemas import SOSRequest

router = APIRouter(prefix="/api/sos", tags=["sos"])


@router.post("")
def create_sos(payload: SOSRequest) -> dict[str, object]:
    created_at = payload.timestamp or datetime.now(timezone.utc).isoformat()
    with connection() as db:
        cursor = db.execute(
            """INSERT INTO alerts (type, created_at, lat, lng, priority, ai_summary,
               recommended_action, status) VALUES ('sos', ?, ?, ?, 'emergency',
               'Immediate SOS alert from student device.', 'Dispatch security to the reported location.', 'New')""",
            (created_at, payload.lat, payload.lng),
        )
        db.execute("INSERT INTO status_log (alert_id, status, changed_at) VALUES (?, 'New', ?)", (cursor.lastrowid, created_at))
    return {"id": cursor.lastrowid, "message": "Security has been notified."}


@router.post("/{alert_id}/cancel")
def cancel_sos(alert_id: int) -> dict[str, object]:
    now = datetime.now(timezone.utc)
    with connection() as db:
        row = db.execute(
            "SELECT type, created_at, status FROM alerts WHERE id=?", (alert_id,)
        ).fetchone()
        if row is None or row["type"] != "sos":
            raise HTTPException(status_code=404, detail="SOS alert not found.")
        created_at = datetime.fromisoformat(row["created_at"].replace("Z", "+00:00"))
        elapsed = (now - created_at).total_seconds()
        if elapsed < 0 or elapsed > 10 or row["status"] == "Resolved":
            raise HTTPException(status_code=409, detail="SOS can only be cancelled within 10 seconds.")
        note = "SOS cancelled by student within 10 seconds."
        db.execute(
            "UPDATE alerts SET status='Resolved', ai_summary=?, recommended_action=? WHERE id=?",
            (note, note, alert_id),
        )
        db.execute(
            "INSERT INTO status_log (alert_id, status, changed_at) VALUES (?, 'Resolved', ?)",
            (alert_id, now.isoformat()),
        )
    return {"id": alert_id, "status": "Resolved", "message": note}

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from ..db import connection
from ..schemas import StatusRequest
from ..auth import staff_required

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


def row_to_alert(row: Any) -> dict[str, Any]:
    item = dict(row)
    item["anonymous"] = bool(item["anonymous"])
    return item


@router.get("")
def list_alerts(_: dict[str, str] = Depends(staff_required)) -> list[dict[str, Any]]:
    with connection() as db:
        rows = db.execute(
            "SELECT * FROM alerts ORDER BY CASE WHEN type='sos' THEN 0 ELSE 1 END, created_at DESC"
        ).fetchall()
    return [row_to_alert(row) for row in rows]


@router.patch("/{alert_id}/status")
def update_status(alert_id: int, payload: StatusRequest, _: dict[str, str] = Depends(staff_required)) -> dict[str, object]:
    changed_at = datetime.now(timezone.utc).isoformat()
    with connection() as db:
        if db.execute("SELECT id FROM alerts WHERE id=?", (alert_id,)).fetchone() is None:
            raise HTTPException(status_code=404, detail="Alert not found.")
        db.execute("UPDATE alerts SET status=? WHERE id=?", (payload.status, alert_id))
        db.execute("INSERT INTO status_log (alert_id, status, changed_at) VALUES (?, ?, ?)", (alert_id, payload.status, changed_at))
    return {"id": alert_id, "status": payload.status, "changed_at": changed_at}

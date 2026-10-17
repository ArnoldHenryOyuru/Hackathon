from datetime import datetime, timezone

from fastapi import APIRouter

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


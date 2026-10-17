from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks

from ..db import connection
from ..schemas import ReportRequest
from ..services.fallback import fallback_triage
from ..services.triage import gemma_triage

router = APIRouter(prefix="/api/reports", tags=["reports"])


def complete_triage(alert_id: int, description: str, category: str, location: str) -> None:
    result = gemma_triage(description, category, location)
    if result is None:
        return
    with connection() as db:
        db.execute(
            """UPDATE alerts SET priority=?, location=?, ai_summary=?,
               recommended_action=?, triage_source='gemma' WHERE id=?""",
            (result["priority"], result["location"], result["summary"], result["recommended_action"], alert_id),
        )


@router.post("")
def create_report(payload: ReportRequest, background_tasks: BackgroundTasks) -> dict[str, object]:
    fallback = fallback_triage(payload.description, payload.category, payload.location)
    created_at = datetime.now(timezone.utc).isoformat()
    with connection() as db:
        cursor = db.execute(
            """INSERT INTO alerts (type, created_at, location, category, description,
               priority, ai_summary, recommended_action, anonymous, triage_source)
               VALUES ('report', ?, ?, ?, ?, ?, ?, ?, ?, 'fallback')""",
            (created_at, payload.location, payload.category, payload.description,
             fallback["priority"], fallback["summary"], fallback["recommended_action"], int(payload.anonymous)),
        )
        db.execute("INSERT INTO status_log (alert_id, status, changed_at) VALUES (?, 'New', ?)", (cursor.lastrowid, created_at))
    background_tasks.add_task(complete_triage, cursor.lastrowid, payload.description, payload.category, payload.location)
    return {"id": cursor.lastrowid, "message": "Report received.", "triage": fallback}


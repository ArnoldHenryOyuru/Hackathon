import json
from datetime import datetime, timezone

from fastapi import APIRouter

from ..db import connection
from ..services.narrative import generate_narrative
from ..services.stats import build_stats

router = APIRouter(prefix="/api/insights", tags=["insights"])


@router.post("/generate")
def generate_insights() -> dict[str, object]:
    stats = build_stats()
    narrative = generate_narrative(stats)
    generated_at = datetime.now(timezone.utc).isoformat()
    with connection() as db:
        cursor = db.execute(
            "INSERT INTO insights (generated_at, stats_json, narrative) VALUES (?, ?, ?)",
            (generated_at, json.dumps(stats), narrative),
        )
    return {"id": cursor.lastrowid, "generated_at": generated_at, "stats": stats, "narrative": narrative}


@router.get("/latest")
def latest_insights() -> dict[str, object] | None:
    with connection() as db:
        row = db.execute("SELECT * FROM insights ORDER BY id DESC LIMIT 1").fetchone()
    if row is None:
        return None
    return {"id": row["id"], "generated_at": row["generated_at"], "stats": json.loads(row["stats_json"]), "narrative": row["narrative"]}


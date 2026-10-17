from typing import Any

from ..db import connection


def build_stats() -> dict[str, Any]:
    with connection() as db:
        total = db.execute("SELECT COUNT(*) AS count FROM alerts WHERE type='report'").fetchone()["count"]
        sos = db.execute("SELECT COUNT(*) AS count FROM alerts WHERE type='sos'").fetchone()["count"]
        high = db.execute("SELECT COUNT(*) AS count FROM alerts WHERE priority IN ('high', 'emergency')").fetchone()["count"]
        open_count = db.execute("SELECT COUNT(*) AS count FROM alerts WHERE status != 'Resolved'").fetchone()["count"]
        resolved = db.execute("SELECT COUNT(*) AS count FROM alerts WHERE status='Resolved'").fetchone()["count"]
        category = [dict(row) for row in db.execute(
            "SELECT category AS label, COUNT(*) AS count FROM alerts WHERE type='report' GROUP BY category ORDER BY count DESC"
        )]
        location = [dict(row) for row in db.execute(
            "SELECT COALESCE(location, 'Unknown') AS label, COUNT(*) AS count FROM alerts GROUP BY location ORDER BY count DESC"
        )]
        hour = [dict(row) for row in db.execute(
            "SELECT strftime('%H', created_at, 'localtime') AS label, COUNT(*) AS count FROM alerts GROUP BY label ORDER BY label"
        )]
    return {
        "total_incidents": total, "total_sos": sos, "high_priority": high,
        "open": open_count, "resolved": resolved, "by_category": category,
        "by_location": location, "by_hour": hour,
    }


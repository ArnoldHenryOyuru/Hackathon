from typing import Any

from ..db import connection


def build_stats() -> dict[str, Any]:
    with connection() as db:
        total = db.execute("SELECT COUNT(*) AS count FROM alerts WHERE type='report'").fetchone()["count"]
        sos = db.execute("SELECT COUNT(*) AS count FROM alerts WHERE type='sos'").fetchone()["count"]
        high = db.execute("SELECT COUNT(*) AS count FROM alerts WHERE priority IN ('high', 'emergency')").fetchone()["count"]
        open_count = db.execute("SELECT COUNT(*) AS count FROM alerts WHERE status != 'Resolved'").fetchone()["count"]
        resolved = db.execute("SELECT COUNT(*) AS count FROM alerts WHERE status='Resolved'").fetchone()["count"]
        resolution_time = db.execute(
            """SELECT AVG((julianday(resolved.changed_at) - julianday(first_new.changed_at)) * 24 * 60) AS minutes
               FROM (SELECT alert_id, MIN(changed_at) AS changed_at FROM status_log
                     WHERE status='New' GROUP BY alert_id) first_new
               JOIN (SELECT alert_id, MIN(changed_at) AS changed_at FROM status_log
                     JOIN alerts ON alerts.id=status_log.alert_id
                     WHERE status_log.status='Resolved'
                       AND alerts.ai_summary != 'SOS cancelled by student within 10 seconds.'
                     GROUP BY alert_id) resolved
               ON resolved.alert_id = first_new.alert_id"""
        ).fetchone()["minutes"]
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
        "open": open_count, "resolved": resolved,
        "avg_resolution_minutes": round(resolution_time, 1) if resolution_time is not None else None,
        "by_category": category,
        "by_location": location, "by_hour": hour,
    }

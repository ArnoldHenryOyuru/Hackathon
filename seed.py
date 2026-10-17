from datetime import datetime, timedelta, timezone
import random

from server.db import connection, init_db
from server.services.fallback import fallback_triage

random.seed(7)
locations = ["Hostel Gate", "Library", "Parking Lot A", "Parking Lot B", "Main Gate", "Cafeteria", "Science Block", "Sports Field", "Admin Block"]
categories = ["suspicious person", "harassment", "theft", "unsafe area", "broken lighting", "vandalism", "medical concern", "other"]
examples = {
    "broken lighting": "Several lights are out and the walkway is very dark.",
    "suspicious person": "A person has been lingering near the entrance and watching students.",
    "unsafe area": "The path feels unsafe after dark because there is little visibility.",
    "theft": "A bicycle was taken from the rack.",
    "harassment": "A student reported repeated unwanted comments.",
    "vandalism": "A notice board was damaged.",
    "medical concern": "Someone appears dizzy and needs assistance.",
    "other": "A maintenance issue needs a safety review.",
}

init_db()
with connection() as db:
    db.execute("DELETE FROM status_log")
    db.execute("DELETE FROM alerts")
    db.execute("DELETE FROM insights")
    for index in range(30):
        day = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 6), hours=random.randint(0, 23))
        if index < 12:
            location = "Parking Lot B"
            category = random.choice(["broken lighting", "suspicious person"])
            day = day.replace(hour=random.randint(19, 22), minute=random.randint(0, 59))
        else:
            location, category = random.choice(locations), random.choice(categories)
        triage = fallback_triage(examples[category], category, location)
        status = "Resolved" if index % 4 == 0 else "New"
        created = day.isoformat()
        cursor = db.execute(
            """INSERT INTO alerts (type, created_at, location, category, description, priority,
               ai_summary, recommended_action, status, anonymous, triage_source)
               VALUES ('report', ?, ?, ?, ?, ?, ?, ?, ?, ?, 'fallback')""",
            (created, location, category, examples[category], triage["priority"], triage["summary"],
             triage["recommended_action"], status, index % 3 == 0),
        )
        db.execute("INSERT INTO status_log (alert_id, status, changed_at) VALUES (?, ?, ?)", (cursor.lastrowid, status, created))
    for index in range(3):
        created = (datetime.now(timezone.utc) - timedelta(days=index + 1, hours=2)).isoformat()
        cursor = db.execute(
            """INSERT INTO alerts (type, created_at, lat, lng, priority, ai_summary,
               recommended_action, status) VALUES ('sos', ?, ?, ?, 'emergency',
               'Immediate SOS alert from student device.', 'Dispatch security to the reported location.', 'Resolved')""",
            (created, 40.7128 + index / 1000, -74.0060 - index / 1000),
        )
        db.execute("INSERT INTO status_log (alert_id, status, changed_at) VALUES (?, 'Resolved', ?)", (cursor.lastrowid, created))
print("Seeded 30 reports and 3 SOS alerts.")

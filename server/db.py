import sqlite3
from contextlib import contextmanager
from typing import Iterator

from .config import DB_PATH


@contextmanager
def connection() -> Iterator[sqlite3.Connection]:
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    try:
        yield db
        db.commit()
    finally:
        db.close()


def init_db() -> None:
    with connection() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK(type IN ('sos', 'report')),
                created_at TEXT NOT NULL,
                lat REAL,
                lng REAL,
                location TEXT,
                category TEXT,
                description TEXT,
                priority TEXT NOT NULL DEFAULT 'medium',
                ai_summary TEXT,
                recommended_action TEXT,
                status TEXT NOT NULL DEFAULT 'New',
                anonymous INTEGER NOT NULL DEFAULT 0,
                triage_source TEXT NOT NULL DEFAULT 'fallback'
            );
            CREATE TABLE IF NOT EXISTS status_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_id INTEGER NOT NULL REFERENCES alerts(id),
                status TEXT NOT NULL,
                changed_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generated_at TEXT NOT NULL,
                stats_json TEXT NOT NULL,
                narrative TEXT NOT NULL
            );
            """
        )


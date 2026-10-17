import hashlib
import hmac
import secrets
from datetime import datetime, timezone

from fastapi import Header, HTTPException

from .db import connection

ROLES = {"student", "admin", "responder"}


def hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000)
    return f"{salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        salt_hex, digest_hex = stored.split("$", 1)
        expected = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), 120_000)
        return hmac.compare_digest(expected.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


def require_role(authorization: str | None, allowed: set[str]) -> dict[str, str]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Login required.")
    token = authorization[7:].strip()
    with connection() as db:
        row = db.execute(
            """SELECT users.username, users.role FROM sessions
               JOIN users ON users.id=sessions.user_id
               WHERE sessions.token=? AND sessions.expires_at>?""",
            (token, datetime.now(timezone.utc).isoformat()),
        ).fetchone()
    if row is None or row["role"] not in allowed:
        raise HTTPException(status_code=403, detail="You do not have permission for this area.")
    return dict(row)


def staff_required(authorization: str | None = Header(default=None)) -> dict[str, str]:
    return require_role(authorization, {"admin", "responder"})


def admin_required(authorization: str | None = Header(default=None)) -> dict[str, str]:
    return require_role(authorization, {"admin"})

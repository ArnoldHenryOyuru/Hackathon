from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from ..auth import ROLES, hash_password, verify_password
from ..db import connection

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=200)


@router.post("/login")
def login(payload: LoginRequest) -> dict[str, str]:
    with connection() as db:
        user = db.execute(
            "SELECT id, username, role, password_hash FROM users WHERE username=?",
            (payload.username.strip(),),
        ).fetchone()
    if user is None or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    token = __import__("secrets").token_urlsafe(32)
    expires_at = (datetime.now(timezone.utc) + timedelta(hours=12)).isoformat()
    with connection() as db:
        db.execute(
            "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
            (token, user["id"], expires_at),
        )
    return {"token": token, "username": user["username"], "role": user["role"]}


@router.post("/logout")
def logout(authorization: str | None = Header(default=None)) -> dict[str, str]:
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:].strip()
        with connection() as db:
            db.execute("DELETE FROM sessions WHERE token=?", (token,))
    return {"message": "Logged out."}

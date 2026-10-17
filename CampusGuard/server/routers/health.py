import json
import urllib.error
import urllib.request

from fastapi import APIRouter

from ..config import OLLAMA_TIMEOUT, OLLAMA_URL

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("")
def health() -> dict[str, object]:
    try:
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=OLLAMA_TIMEOUT) as response:
            json.loads(response.read().decode())
        return {"ai": "online"}
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError):
        return {"ai": "offline"}

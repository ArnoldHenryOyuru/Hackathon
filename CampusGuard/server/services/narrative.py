import json
import urllib.error
import urllib.request
from typing import Any

from ..config import OLLAMA_MODEL, OLLAMA_TIMEOUT, OLLAMA_URL


def fallback_narrative(stats: dict[str, Any]) -> str:
    hotspot = stats["by_location"][0]["label"] if stats["by_location"] else "the campus"
    return (
        f"This week recorded {stats['total_incidents']} incident reports and {stats['total_sos']} SOS alerts. "
        f"{hotspot} is the most reported location. There are {stats['high_priority']} high-priority alerts; "
        "increase patrols and review lighting and access controls in the busiest hotspot."
    )


def generate_narrative(stats: dict[str, Any]) -> str:
    prompt = """Write a short campus safety weekly summary and numbered recommendations using only
these JSON statistics. Do not invent facts, identify people, or make accusations. Return plain text.
Statistics:
""" + json.dumps(stats)
    payload = json.dumps({"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}).encode()
    request = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate", data=payload, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(request, timeout=OLLAMA_TIMEOUT) as response:
            text = json.loads(response.read().decode()).get("response", "").strip()
        return text or fallback_narrative(stats)
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return fallback_narrative(stats)


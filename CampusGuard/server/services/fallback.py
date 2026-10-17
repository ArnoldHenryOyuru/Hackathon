def fallback_triage(description: str, category: str, location: str) -> dict[str, str]:
    text = description.lower()
    emergency_words = ("weapon", "knife", "attack", "assault", "bleeding", "unconscious")
    high_words = ("followed", "stalking", "threat", "danger", "injured", "fire")
    if any(word in text for word in emergency_words):
        priority, action = "emergency", "Call emergency services and dispatch campus security immediately."
    elif any(word in text for word in high_words) or category in {"harassment", "medical concern"}:
        priority, action = "high", "Dispatch campus security to assess the situation promptly."
    elif category in {"suspicious person", "unsafe area", "theft"}:
        priority, action = "medium", "Have campus security review the report and patrol the area."
    else:
        priority, action = "low", "Add this report to the next facilities or safety review."
    return {
        "priority": priority,
        "location": location if location != "Other" else "unknown",
        "summary": "Report received for campus safety review.",
        "recommended_action": action,
    }


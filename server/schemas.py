from typing import Any, Literal

from pydantic import BaseModel, Field


class SOSRequest(BaseModel):
    lat: float | None = Field(default=None, ge=-90, le=90)
    lng: float | None = Field(default=None, ge=-180, le=180)
    timestamp: str | None = None


class ReportRequest(BaseModel):
    category: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=3000)
    location: str = Field(min_length=1, max_length=120)
    anonymous: bool = False


class StatusRequest(BaseModel):
    status: Literal["New", "Investigating", "Resolved"]


class TriageResult(BaseModel):
    priority: Literal["low", "medium", "high", "emergency"]
    location: str
    summary: str
    recommended_action: str


class Alert(BaseModel):
    id: int
    type: Literal["sos", "report"]
    created_at: str
    lat: float | None = None
    lng: float | None = None
    location: str | None = None
    category: str | None = None
    description: str | None = None
    priority: str
    ai_summary: str | None = None
    recommended_action: str | None = None
    status: str
    anonymous: bool
    triage_source: str


class Insight(BaseModel):
    id: int
    generated_at: str
    stats: dict[str, Any]
    narrative: str


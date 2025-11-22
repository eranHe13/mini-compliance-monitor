from pydantic import BaseModel
from typing import List

class EventOverTime(BaseModel):
    date: str
    count: int

class FindingsBySeverity(BaseModel):
    low: int
    medium: int
    high: int
    critical: int

class StatsSummary(BaseModel):
    total_events: int
    total_findings: int
    findings_by_severity: FindingsBySeverity
    events_over_time: List[EventOverTime]

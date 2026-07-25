"""Storage model definitions for TRIBUNAL persistent repository layer."""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class InvestigationRecord:
    """Persistent metadata record for an investigation execution."""
    id: str
    query: str
    dataset: str = "default"
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    planner_intent: str = "pattern_detection"
    risk_level: str = "MEDIUM"
    confidence: float = 0.0
    recommendation: str = ""
    status: str = "COMPLETED"
    duration_ms: float = 0.0
    version: str = "1.0.0"
    report_path: Optional[str] = None
    graph_path: Optional[str] = None
    case_path: Optional[str] = None


@dataclass
class ReportRecord:
    """Persistent report artifact location record."""
    investigation_id: str
    path: str
    format: str = "markdown"
    generated_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


@dataclass
class GraphRecord:
    """Persistent evidence graph statistics and location record."""
    investigation_id: str
    path: str
    node_count: int = 0
    edge_count: int = 0


@dataclass
class VerdictRecord:
    """Persistent tribunal verdict summary record."""
    investigation_id: str
    winning_hypothesis: str
    confidence: float
    recommendation: str
    runner_up: Optional[str] = None


@dataclass
class AuditRecord:
    """Persistent lifecycle audit trail event record."""
    investigation_id: str
    event: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    id: Optional[int] = None

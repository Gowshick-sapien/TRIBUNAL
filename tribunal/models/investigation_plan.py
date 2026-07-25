"""Investigation plan contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any


@dataclass
class InvestigationPlan:
    raw_query: str
    intent: str
    experts: list[str]
    run_eda: bool
    target_pattern: str | None = None
    customer_id: str | None = None
    date_range: tuple[date, date] | None = None
    country: str | None = None
    txn_type: str | None = None
    risk_level: str | None = None
    entities: list[str] = field(default_factory=list)
    filters: dict[str, Any] = field(default_factory=dict)
    requested_output: str = "investigation_report"

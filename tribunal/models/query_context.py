"""Query context for report generation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class QueryContext:
    raw_query: str
    intent: str
    target_pattern: str | None = None
    customer_id: str | None = None
    date_range: tuple[date, date] | None = None

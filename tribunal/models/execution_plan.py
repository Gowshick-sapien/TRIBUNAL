"""Execution plan contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExecutionPlan:
    run_eda: bool
    expert_sequence: list[str]
    filters: dict[str, Any]
    rationale: str
    target_pattern: str | None = None

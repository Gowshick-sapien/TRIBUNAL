"""Execution plan contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExecutionPlan:
    run_eda: bool = True
    expert_sequence: list[str] = field(default_factory=list)
    filters: dict[str, Any] = field(default_factory=dict)
    rationale: str = ""
    target_pattern: str | None = None
    assets: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    needs_tribunal: bool = True
    needs_report: bool = True
    output_format: str = "investigation_report"
    schema_version: str = "1.0"
    planner_version: str = "C.1"
    is_supported: bool = True
    intent: str = "pattern_detection"
    rejection_reason: str | None = None

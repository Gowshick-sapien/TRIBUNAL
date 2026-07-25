"""Planning result contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from tribunal.models.execution_plan import ExecutionPlan
from tribunal.models.investigation_plan import InvestigationPlan


@dataclass
class PlanningResult:
    """Consolidated result returned by the Planner containing plans, context, and profiling metrics."""
    investigation_plan: InvestigationPlan
    execution_plan: ExecutionPlan
    planner_context: Any = None
    metrics: dict[str, float] = field(default_factory=dict)

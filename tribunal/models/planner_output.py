"""Planner output contract."""

from __future__ import annotations

from dataclasses import dataclass

from tribunal.models.execution_plan import ExecutionPlan
from tribunal.models.investigation_plan import InvestigationPlan


@dataclass
class PlannerOutput:
    investigation_plan: InvestigationPlan
    execution_plan: ExecutionPlan

"""Execution Planner — interface only."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tribunal.models.execution_plan import ExecutionPlan
    from tribunal.models.investigation_plan import InvestigationPlan


class ExecutionPlanner:
    """Translates InvestigationPlan into deterministic ExecutionPlan."""

    def plan(self, investigation_plan: InvestigationPlan) -> ExecutionPlan:
        """Finalize expert sequence, filters, and rationale."""
        ...

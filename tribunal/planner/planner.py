"""Planner orchestrator — interface only."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tribunal.models.investigation_plan import InvestigationPlan
    from tribunal.models.planner_output import PlannerOutput
    from tribunal.models.user_query import UserQuery


class Planner:
    """Orchestrates query understanding and execution plan construction."""

    def create_plan(self, query: UserQuery) -> InvestigationPlan:
        """Parse query and return structured investigation plan."""
        ...

    def create_execution(self, query: UserQuery) -> PlannerOutput:
        """Parse query and return both investigation and execution plans."""
        ...

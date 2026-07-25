"""Planner output contract — alias for PlanningResult for backward compatibility."""

from __future__ import annotations

from tribunal.models.planning_result import PlanningResult

# PlannerOutput serves as a backward-compatible wrapper/alias for PlanningResult
PlannerOutput = PlanningResult

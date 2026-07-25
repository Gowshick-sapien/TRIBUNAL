"""Pipeline orchestrator — interface only."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tribunal.models.investigation_report import InvestigationReport
    from tribunal.models.user_query import UserQuery


class Pipeline:
    """Orchestrates the full investigation pipeline end to end."""

    def run(self, query: str) -> InvestigationReport:
        """Execute full investigation: query → report."""
        ...

    def run_query(self, query: UserQuery) -> InvestigationReport:
        """Execute pipeline from structured UserQuery."""
        ...

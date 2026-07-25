"""Report Generator — interface only."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tribunal.models.case_file import CaseFile
    from tribunal.models.execution_plan import ExecutionPlan
    from tribunal.models.investigation_card import InvestigationCard
    from tribunal.models.investigation_report import InvestigationReport
    from tribunal.models.query_context import QueryContext
    from tribunal.models.tribunal_verdict import TribunalVerdict


class ReportGenerator:
    """Transforms tribunal verdict into a human-readable investigation report."""

    def generate(
        self,
        verdict: TribunalVerdict,
        case_file: CaseFile,
        execution_plan: ExecutionPlan,
        query_context: QueryContext,
        all_cards: list[InvestigationCard],
    ) -> InvestigationReport:
        """Assemble structured report with full narrative text."""
        ...

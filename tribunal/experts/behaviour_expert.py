"""Customer Behaviour Expert — interface only."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

    from tribunal.models.case_file import CaseFile
    from tribunal.models.execution_plan import ExecutionPlan
    from tribunal.models.investigation_card import InvestigationCard


class BehaviourExpert:
    """Investigates behavioural deviations from customer baseline."""

    expert_id: str = "behaviour"

    def investigate(
        self,
        transactions: pd.DataFrame,
        case_file: CaseFile,
        execution_plan: ExecutionPlan,
    ) -> tuple[list[InvestigationCard], CaseFile]:
        """Investigate relative to the current dominant hypothesis."""
        ...

"""Abstract base class for domain expert investigators."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

    from tribunal.models.case_file import CaseFile
    from tribunal.models.execution_plan import ExecutionPlan
    from tribunal.models.expert_result import ExpertResult


class BaseExpert(ABC):
    """Interface for all domain expert investigators."""

    @property
    @abstractmethod
    def expert_id(self) -> str:
        """Unique expert identifier (e.g., 'financial', 'behaviour')."""

    @abstractmethod
    def investigate(
        self,
        transactions: pd.DataFrame,
        case_file: CaseFile,
        execution_plan: ExecutionPlan,
    ) -> ExpertResult:
        """Investigate transactions and return cards with updated case file."""

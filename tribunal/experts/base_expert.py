"""Abstract base class and pipeline orchestrator for domain expert investigators."""

from __future__ import annotations

from abc import ABC, abstractmethod
import logging
from typing import Any, TYPE_CHECKING
import pandas as pd

from tribunal.models.expert_result import ExpertResult

if TYPE_CHECKING:
    from tribunal.models.case_file import CaseFile
    from tribunal.models.execution_plan import ExecutionPlan

logger = logging.getLogger("tribunal.experts")


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


class BaseInvestigationExpert(BaseExpert, ABC):
    """Shared pipeline orchestrator for domain investigation experts.
    
    Owns generic 5-stage workflow: Candidate Selection -> Detector Execution -> Post-Processing Hook -> Confidence Aggregation -> Card Building.
    """

    def __init__(
        self,
        candidate_selector: Any,
        confidence_aggregator: Any,
        card_builder: Any,
        detectors: list[Any],
    ):
        self._candidate_selector = candidate_selector
        self._confidence_aggregator = confidence_aggregator
        self._card_builder = card_builder
        self._detectors = detectors

    def _post_process_findings(self, findings: list[Any]) -> list[Any]:
        """Protected hook method for expert-specific post-processing of raw findings before aggregation.
        
        Subclasses (e.g., NetworkExpert, BehaviourExpert, FinancialExpert) can override this hook
        to perform graph deduplication, merging, or clustering without replacing the core pipeline.
        """
        return findings

    def investigate(
        self,
        transactions: pd.DataFrame,
        case_file: CaseFile,
        execution_plan: ExecutionPlan,
    ) -> ExpertResult:
        """Execute 5-stage domain investigation pipeline."""
        if transactions is None or transactions.empty:
            return ExpertResult(cards=[], case_file=case_file)

        candidates = self._candidate_selector.select_candidates(transactions, execution_plan)
        expert_name = self.__class__.__name__
        acct_col = "from_account" if "from_account" in candidates.columns else ("Account" if "Account" in candidates.columns else None)
        accts = candidates[acct_col].unique() if acct_col else []
        logger.debug("%s Input Accounts: %s", expert_name, accts)

        if candidates.empty:
            return ExpertResult(cards=[], case_file=case_file)

        findings = []
        for detector in self._detectors:
            try:
                findings.extend(detector.detect(candidates))
            except Exception as err:
                logger.error(f"Detector {getattr(detector, 'detector_name', type(detector).__name__)} failed: {err}")

        # Execute protected hook for expert post-processing (deduplication, clustering, graph merging)
        findings = self._post_process_findings(findings)

        if not findings:
            return ExpertResult(cards=[], case_file=case_file)

        aggregated = self._confidence_aggregator.aggregate(findings)
        cards = self._card_builder.build_cards(aggregated)

        for card in cards:
            case_file.add_evidence_card(card)

        return ExpertResult(cards=cards, case_file=case_file)

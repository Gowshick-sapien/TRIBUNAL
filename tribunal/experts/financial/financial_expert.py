"""Financial Investigation Expert — Modular financial transaction investigation engine."""

from __future__ import annotations

import logging
from typing import Optional

from tribunal.experts.base_expert import BaseInvestigationExpert
from tribunal.experts.financial.candidate_selector import CandidateSelector
from tribunal.experts.financial.card_builder import CardBuilder
from tribunal.experts.financial.confidence import ConfidenceAggregator
from tribunal.experts.financial.frequency_detector import FrequencyDetector
from tribunal.experts.financial.large_transfer_detector import LargeTransferDetector
from tribunal.experts.financial.structuring_detector import StructuringDetector
from tribunal.experts.financial.velocity_detector import VelocityDetector

logger = logging.getLogger("tribunal.experts.financial")


class FinancialExpert(BaseInvestigationExpert):
    """Financial Investigation Expert.
    
    Analyzes financial transaction behavior using CandidateSelector, Pattern Modules,
    ConfidenceAggregator, and CardBuilder to produce structured InvestigationCards.
    Does not decide guilt.
    """

    expert_id: str = "financial"

    def __init__(
        self,
        candidate_selector: Optional[CandidateSelector] = None,
        confidence_aggregator: Optional[ConfidenceAggregator] = None,
        card_builder: Optional[CardBuilder] = None,
    ):
        selector = candidate_selector or CandidateSelector()
        aggregator = confidence_aggregator or ConfidenceAggregator()
        builder = card_builder or CardBuilder()
        detectors = [
            StructuringDetector(),
            VelocityDetector(),
            LargeTransferDetector(),
            FrequencyDetector(),
        ]
        super().__init__(
            candidate_selector=selector,
            confidence_aggregator=aggregator,
            card_builder=builder,
            detectors=detectors,
        )

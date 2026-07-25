"""Customer Behaviour Investigation Expert — Modular behavioural anomaly investigation engine."""

from __future__ import annotations

import logging
from typing import Optional

from tribunal.experts.base_expert import BaseInvestigationExpert
from tribunal.experts.behaviour.behaviour_drift_detector import BehaviourDriftDetector
from tribunal.experts.behaviour.candidate_selector import CandidateSelector
from tribunal.experts.behaviour.card_builder import CardBuilder
from tribunal.experts.behaviour.confidence import ConfidenceAggregator
from tribunal.experts.behaviour.counterparty_behaviour_detector import CounterpartyBehaviourDetector
from tribunal.experts.behaviour.currency_change_detector import CurrencyChangeDetector
from tribunal.experts.behaviour.dormancy_detector import DormancyDetector
from tribunal.experts.behaviour.payment_pattern_detector import PaymentPatternDetector
from tribunal.experts.behaviour.spending_pattern_detector import SpendingPatternDetector

logger = logging.getLogger("tribunal.experts.behaviour")


class BehaviourExpert(BaseInvestigationExpert):
    """Customer Behaviour Investigation Expert.
    
    Analyzes historical behavioural characteristics and account consistency over time
    using CandidateSelector, Behavioural Detectors, ConfidenceAggregator, and CardBuilder.
    Does not decide guilt.
    """

    expert_id: str = "behaviour"

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
            BehaviourDriftDetector(),
            DormancyDetector(),
            SpendingPatternDetector(),
            CurrencyChangeDetector(),
            PaymentPatternDetector(),
            CounterpartyBehaviourDetector(),
        ]
        super().__init__(
            candidate_selector=selector,
            confidence_aggregator=aggregator,
            card_builder=builder,
            detectors=detectors,
        )

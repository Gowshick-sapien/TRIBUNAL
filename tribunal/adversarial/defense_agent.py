"""Defense Agent — Orchestrates Adversarial Review Engine pipeline (Phase C.5)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from tribunal.adversarial.alternative_hypothesis_generator import AlternativeHypothesisGenerator
from tribunal.adversarial.confidence_adjuster import ConfidenceAdjuster
from tribunal.adversarial.contradiction_detector import ContradictionDetector
from tribunal.adversarial.evidence_reviewer import EvidenceReviewer
from tribunal.adversarial.evidence_strength_analyzer import EvidenceStrengthAnalyzer
from tribunal.adversarial.rebuttal_builder import RebuttalBuilder
from tribunal.adversarial.uncertainty_estimator import UncertaintyEstimator
from tribunal.models.investigation_card import InvestigationCard

if TYPE_CHECKING:
    from tribunal.models.case_file import CaseFile
    from tribunal.models.evidence_graph import EvidenceGraph
    from tribunal.models.execution_plan import ExecutionPlan


class DefenseAgent:
    """Orchestrates graph-centric adversarial review of prosecution evidence.

    Challenging hypotheses, identifying contradictions, generating plausible alternative
    explanations, and outputting Defense Investigation Cards (source_expert="defense").
    """

    def __init__(self) -> None:
        self.reviewer = EvidenceReviewer()
        self.contradiction_detector = ContradictionDetector()
        self.hypothesis_generator = AlternativeHypothesisGenerator()
        self.strength_analyzer = EvidenceStrengthAnalyzer()
        self.uncertainty_estimator = UncertaintyEstimator()
        self.rebuttal_builder = RebuttalBuilder()
        self.confidence_adjuster = ConfidenceAdjuster()

    def review(
        self,
        evidence_graph: EvidenceGraph,
        case_file: Optional[CaseFile] = None,
        execution_plan: Optional[ExecutionPlan] = None,
    ) -> list[InvestigationCard]:
        """Perform adversarial review of EvidenceGraph and return list of Defense Investigation Cards."""
        defense_cards: list[InvestigationCard] = []

        if not evidence_graph:
            return defense_cards

        # Stage 1: Traverse graph & extract findings context
        ctx = self.reviewer.review(evidence_graph)

        if not ctx.prosecution_cards:
            return defense_cards

        # Stage 2: Detect contradictions
        contradictions = self.contradiction_detector.detect(ctx)

        # Stage 3: Generate alternative non-malicious hypotheses
        alternatives = self.hypothesis_generator.generate(ctx)

        # Stage 4: Analyze evidence strength
        strength_map = self.strength_analyzer.analyze_all(ctx)

        # Stage 5: Estimate uncertainty
        uncertainty_map = self.uncertainty_estimator.estimate_all(ctx)

        # Stage 6: Build Rebuttal Cards
        # A. Alternative Hypothesis Cards
        for alt in alternatives:
            card_id = alt.target_card_id
            strength = strength_map.get(card_id, self.strength_analyzer.analyze_card(
                next((c for c in ctx.prosecution_cards if c.card_id == card_id), ctx.prosecution_cards[0]), ctx
            ))
            uncertainty = uncertainty_map.get(alt.account_id, self.uncertainty_estimator.estimate_for_account(alt.account_id, ctx))

            def_card = self.rebuttal_builder.build_alternative_card(alt, strength, uncertainty)
            defense_cards.append(def_card)

        # B. Contradiction Cards
        for finding in contradictions:
            strength = strength_map.get(finding.primary_card_id, self.strength_analyzer.analyze_card(ctx.prosecution_cards[0], ctx))
            uncertainty = uncertainty_map.get(finding.account_id, self.uncertainty_estimator.estimate_for_account(finding.account_id, ctx))

            def_card = self.rebuttal_builder.build_contradiction_card(finding, strength, uncertainty)
            defense_cards.append(def_card)

        # C. Weak Evidence Cards
        for card in ctx.prosecution_cards:
            strength = strength_map.get(card.card_id)
            if strength and strength.is_weak_evidence:
                acc_id = card.affected_accounts[0] if card.affected_accounts else "UNKNOWN"
                uncertainty = uncertainty_map.get(acc_id, self.uncertainty_estimator.estimate_for_account(acc_id, ctx))
                def_card = self.rebuttal_builder.build_weak_evidence_card(card, strength, uncertainty)
                defense_cards.append(def_card)

        return defense_cards

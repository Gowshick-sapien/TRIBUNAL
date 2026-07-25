"""Rebuttal Builder — Constructs defense investigation cards from review analysis."""

from __future__ import annotations

import datetime
import uuid
from typing import Any

from tribunal.adversarial.alternative_hypothesis_generator import AlternativeExplanation, AlternativeHypothesis
from tribunal.adversarial.confidence_adjuster import ConfidenceAdjuster
from tribunal.adversarial.contradiction_detector import ContradictionFinding
from tribunal.adversarial.evidence_reviewer import ReviewContext
from tribunal.adversarial.evidence_strength_analyzer import EvidenceStrengthScore
from tribunal.adversarial.uncertainty_estimator import UncertaintyScore
from tribunal.models.investigation_card import InvestigationCard


class RebuttalBuilder:
    """Constructs Defense Investigation Cards (source_expert="defense")."""

    def __init__(self) -> None:
        self.confidence_adjuster = ConfidenceAdjuster()

    def build_alternative_card(
        self,
        hypothesis: AlternativeExplanation | AlternativeHypothesis,
        strength: EvidenceStrengthScore,
        uncertainty: UncertaintyScore,
    ) -> InvestigationCard:
        """Build a Defense Investigation Card for a plausible alternative explanation mapping to a normalized top-level hypothesis."""
        def_conf = self.confidence_adjuster.compute_defense_confidence(
            plausibility_score=hypothesis.plausibility_score,
            uncertainty_score=uncertainty.uncertainty_score,
            strength_score=strength.strength_score,
        )

        card_uuid = uuid.uuid4().hex[:6]

        explanation_title = getattr(hypothesis, "explanation_title", hypothesis.title)
        top_hypothesis = getattr(hypothesis, "top_level_hypothesis", hypothesis.title)
        explanation_details = getattr(hypothesis, "explanation_details", hypothesis.explanation)

        features = list(hypothesis.supporting_signals)
        if explanation_title not in features:
            features.insert(0, explanation_title)

        return InvestigationCard(
            card_id=f"card_def_{card_uuid}",
            source_expert="defense",
            derived_from_transactions=[],
            generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            hypothesis=top_hypothesis,
            confidence=def_conf,
            severity="MEDIUM" if def_conf > 0.60 else "LOW",
            supporting_features=features,
            supporting_metrics={
                "plausibility_score": hypothesis.plausibility_score,
                "evidence_strength": strength.strength_score,
                "uncertainty_score": uncertainty.uncertainty_score,
            },
            provenance={
                "defense_type": "alternative_explanation",
                "target_card_id": hypothesis.target_card_id,
                "explanation_category": hypothesis.category,
                "explanation_title": explanation_title,
                "explanation_details": explanation_details,
            },
            affected_accounts=[hypothesis.account_id],
            supports=[top_hypothesis],
            counter_hypothesis=f"Prosecution Card {hypothesis.target_card_id}",
        )

    def build_contradiction_card(
        self,
        finding: ContradictionFinding,
        strength: EvidenceStrengthScore,
        uncertainty: UncertaintyScore,
    ) -> InvestigationCard:
        """Build a Defense Investigation Card for detected expert contradictions."""
        def_conf = self.confidence_adjuster.compute_defense_confidence(
            plausibility_score=0.75,
            uncertainty_score=uncertainty.uncertainty_score,
            strength_score=strength.strength_score,
        )

        card_uuid = uuid.uuid4().hex[:6]
        return InvestigationCard(
            card_id=f"card_def_{card_uuid}",
            source_expert="defense",
            derived_from_transactions=[],
            generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            hypothesis=f"Contradictory Expert Findings for Account {finding.account_id}",
            confidence=def_conf,
            severity=finding.severity,
            supporting_features=["expert_contradiction_detected"],
            supporting_metrics={
                "confidence_delta": finding.confidence_delta,
                "evidence_strength": strength.strength_score,
                "uncertainty_score": uncertainty.uncertainty_score,
            },
            provenance={
                "defense_type": "contradiction",
                "primary_card_id": finding.primary_card_id,
                "conflicting_card_id": finding.conflicting_card_id,
                "conflict_type": finding.conflict_type,
                "description": finding.description,
            },
            affected_accounts=[finding.account_id],
            counter_hypothesis=f"Primary Card {finding.primary_card_id}",
        )

    def build_weak_evidence_card(
        self,
        card: InvestigationCard,
        strength: EvidenceStrengthScore,
        uncertainty: UncertaintyScore,
    ) -> InvestigationCard:
        """Build a Defense Investigation Card highlighting weak or uncorroborated single-expert evidence."""
        def_conf = self.confidence_adjuster.compute_defense_confidence(
            plausibility_score=0.70,
            uncertainty_score=uncertainty.uncertainty_score,
            strength_score=strength.strength_score,
        )

        card_uuid = uuid.uuid4().hex[:6]
        acc_id = card.affected_accounts[0] if card.affected_accounts else "UNKNOWN"
        return InvestigationCard(
            card_id=f"card_def_{card_uuid}",
            source_expert="defense",
            derived_from_transactions=card.derived_from_transactions,
            generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            hypothesis=f"Weak Single-Expert Evidence for Card {card.card_id}",
            confidence=def_conf,
            severity="MEDIUM",
            supporting_features=["uncorroborated_single_expert", "low_strength_score"],
            supporting_metrics={
                "prosecution_confidence": card.confidence,
                "evidence_strength": strength.strength_score,
                "uncertainty_score": uncertainty.uncertainty_score,
            },
            provenance={
                "defense_type": "weak_evidence",
                "target_card_id": card.card_id,
                "target_expert": card.source_expert,
            },
            affected_accounts=[acc_id],
            counter_hypothesis=card.hypothesis,
        )

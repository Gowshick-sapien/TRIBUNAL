"""Evidence Strength Analyzer — Evaluates structural support and provenance completeness of evidence."""

from __future__ import annotations

from dataclasses import dataclass

from tribunal.adversarial.evidence_reviewer import ReviewContext
from tribunal.models.investigation_card import InvestigationCard


@dataclass
class EvidenceStrengthScore:
    """Strength analysis result for an investigation card or account."""

    card_id: str
    strength_score: float  # 0.0 (weak) to 1.0 (strong)
    corroboration_count: int
    contradiction_count: int
    provenance_completeness: float  # 0.0 to 1.0
    is_weak_evidence: bool


class EvidenceStrengthAnalyzer:
    """Evaluates the strength, corroboration depth, and provenance completeness of evidence cards."""

    def analyze_card(self, card: InvestigationCard, ctx: ReviewContext) -> EvidenceStrengthScore:
        """Calculate EvidenceStrengthScore for a specific prosecution card."""
        corroboration_count = 0
        contradiction_count = 0

        # Count graph-level corroborations & contradictions targeting this card
        for src, dst in ctx.corroborations:
            if src == card.card_id or dst == card.card_id:
                corroboration_count += 1

        for src, dst in ctx.contradictions:
            if src == card.card_id or dst == card.card_id:
                contradiction_count += 1

        # Check provenance completeness
        prov = card.provenance or {}
        tx_count = len(card.derived_from_transactions)
        detector_count = len(prov.get("detectors", []))

        prov_score = 0.0
        if tx_count > 0:
            prov_score += 0.5
        if detector_count > 0:
            prov_score += 0.5

        # Calculate strength score formula: base_conf * 0.4 + prov * 0.3 + corroboration_bonus - contradiction_penalty
        corrob_bonus = min(0.30, corroboration_count * 0.15)
        contradict_penalty = min(0.30, contradiction_count * 0.15)

        strength = (card.confidence * 0.40) + (prov_score * 0.30) + corrob_bonus - contradict_penalty
        strength = max(0.0, min(1.0, strength))

        is_weak = strength < 0.55 or (corroboration_count == 0 and card.confidence < 0.70)

        return EvidenceStrengthScore(
            card_id=card.card_id,
            strength_score=round(strength, 3),
            corroboration_count=corroboration_count,
            contradiction_count=contradiction_count,
            provenance_completeness=prov_score,
            is_weak_evidence=is_weak,
        )

    def analyze_all(self, ctx: ReviewContext) -> dict[str, EvidenceStrengthScore]:
        """Analyze all prosecution cards in ReviewContext and return a map from card_id to score."""
        return {card.card_id: self.analyze_card(card, ctx) for card in ctx.prosecution_cards}

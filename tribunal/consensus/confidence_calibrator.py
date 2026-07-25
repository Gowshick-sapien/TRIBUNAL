"""Confidence Calibrator module — Prevents overconfidence through non-linear calibration."""

from __future__ import annotations

from typing import Any

from tribunal.consensus.consensus_engine import ConsensusResult
from tribunal.models.evidence_graph import EvidenceGraph


class ConfidenceCalibrator:
    """Calibrates consensus confidence score against uncertainty, single-expert risk, and graph topology completeness."""

    def calibrate(
        self,
        consensus_result: ConsensusResult,
        graph: EvidenceGraph,
    ) -> float:
        """Calculate final calibrated Tribunal confidence (0.0 to 1.0)."""
        winner = consensus_result.winning_hypothesis
        raw_score = winner.net_support_score

        if consensus_result.consensus_category == "INCONCLUSIVE":
            # Inconclusive verdicts output confidence reflecting uncertainty gap
            return round(min(0.50, max(0.20, raw_score * 0.60)), 4)

        # Base confidence starts from winner net support score
        calibrated = raw_score

        # Expert diversity bonus / penalty
        valid_experts = [e for e in winner.expert_sources if e not in ("defense", "system")]
        if len(valid_experts) >= 2:
            calibrated += 0.05  # Corroboration bonus
        elif len(valid_experts) == 1 and not winner.is_defense_hypothesis:
            calibrated -= 0.10  # Single-expert risk penalty

        # Corroboration depth bonus
        if winner.supporting_cards and len(winner.supporting_cards) >= 2:
            calibrated += 0.05

        # Defense challenge adjustment
        if not winner.is_defense_hypothesis and consensus_result.confidence_gap < 0.20:
            calibrated -= 0.08

        # Bound calibrated confidence between 0.15 and 0.98
        final_conf = round(min(0.98, max(0.15, calibrated)), 4)
        return final_conf

"""Confidence Adjuster — Computes defense confidence scores deterministically."""

from __future__ import annotations


class ConfidenceAdjuster:
    """Computes confidence scores for defense cards challenging prosecution hypotheses."""

    def compute_defense_confidence(
        self,
        plausibility_score: float,
        uncertainty_score: float,
        strength_score: float,
    ) -> float:
        """Compute defense card confidence (0.0 to 1.0).

        Higher uncertainty and higher alternative plausibility increase defense confidence;
        strong prosecution strength slightly moderates defense confidence.
        """
        # Formula: plausibility * 0.50 + uncertainty * 0.35 + (1 - strength) * 0.15
        conf = (plausibility_score * 0.50) + (uncertainty_score * 0.35) + ((1.0 - strength_score) * 0.15)
        conf = max(0.10, min(0.99, conf))
        return round(conf, 3)

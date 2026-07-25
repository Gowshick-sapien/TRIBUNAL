"""Tribunal verdict contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TribunalVerdict:
    """Consolidated verdict issued by the Tribunal after multi-hypothesis deliberation."""

    verdict: str  # LIKELY_MALICIOUS, POSSIBLY_MALICIOUS, INCONCLUSIVE, LIKELY_LEGITIMATE
    winning_hypothesis: str
    winning_score: float
    confidence: float
    primary_hypothesis: str = ""
    primary_score: float = 0.0
    secondary_hypothesis: str | None = None
    secondary_score: float | None = None
    confidence_gap: float = 0.0
    alternative_hypotheses: list[str] = field(default_factory=list)
    rejected_hypotheses: list[dict[str, Any]] = field(default_factory=list)
    supporting_cards: list[str] = field(default_factory=list)
    defense_cards_considered: list[str] = field(default_factory=list)
    supporting_experts: list[str] = field(default_factory=list)
    deliberation_trace: list[dict[str, Any]] = field(default_factory=list)
    evidence_summary: dict[str, Any] = field(default_factory=dict)
    reasoning_metadata: dict[str, Any] = field(default_factory=dict)

    # Backward compatibility attributes
    winning_confidence: float = 0.0
    winning_chain: list[str] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    risk_level: str = "MEDIUM"
    recommendation: str = ""
    contradictions_applied: list[dict] = field(default_factory=list)
    runner_up_hypothesis: str | None = None
    runner_up_confidence: float | None = None
    rejection_reason: str | None = None

    def __post_init__(self) -> None:
        if not self.primary_hypothesis:
            self.primary_hypothesis = self.winning_hypothesis
        if self.primary_score == 0.0:
            self.primary_score = self.winning_score
        if self.secondary_hypothesis is None and self.runner_up_hypothesis is not None:
            self.secondary_hypothesis = self.runner_up_hypothesis
        if self.secondary_score is None and self.runner_up_confidence is not None:
            self.secondary_score = self.runner_up_confidence

        if self.winning_confidence == 0.0:
            self.winning_confidence = self.confidence
        if not self.recommendation:
            self.recommendation = f"Verdict: {self.verdict} for primary hypothesis '{self.primary_hypothesis}' (confidence: {self.confidence:.2f})"

"""Tribunal verdict contract."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TribunalVerdict:
    winning_hypothesis: str
    winning_confidence: float
    winning_chain: list[str]
    missing_evidence: list[str]
    risk_level: str
    recommendation: str
    contradictions_applied: list[dict] = field(default_factory=list)
    runner_up_hypothesis: str | None = None
    runner_up_confidence: float | None = None
    rejection_reason: str | None = None

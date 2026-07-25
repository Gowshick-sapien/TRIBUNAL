"""Investigation report output contract."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class InvestigationReport:
    query_recap: str
    experts_invoked: list[dict[str, str]]
    experts_skipped: list[dict[str, str]]
    winning_hypothesis: str
    winning_confidence: float
    evidence_chain: str
    missing_evidence: list[str]
    risk_level: str
    recommendation: str
    full_text: str
    runner_up_hypothesis: str | None = None
    runner_up_confidence: float | None = None
    rejection_reason: str | None = None

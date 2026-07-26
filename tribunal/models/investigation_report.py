"""Investigation report output contract."""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any


@dataclass
class InvestigationReport:
    """Human-readable, structured, and auditable investigation report output."""

    report_id: str = field(default_factory=lambda: "rpt_default")
    generated_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)
    executive_summary: dict[str, Any] = field(default_factory=dict)
    query_interpretation: dict[str, Any] = field(default_factory=dict)
    timeline: list[dict[str, Any]] = field(default_factory=list)
    expert_findings: list[dict[str, Any]] = field(default_factory=list)
    evidence_summary: dict[str, Any] = field(default_factory=dict)
    graph_summary: dict[str, Any] = field(default_factory=dict)
    defense_summary: dict[str, Any] = field(default_factory=dict)
    tribunal_summary: dict[str, Any] = field(default_factory=dict)
    provenance_details: list[dict[str, Any]] = field(default_factory=list)
    audit_trail: list[dict[str, Any]] = field(default_factory=list)
    markdown_content: str = ""
    html_content: str = ""
    json_payload: dict[str, Any] = field(default_factory=dict)

    # Backward compatibility attributes
    query_recap: str = ""
    experts_invoked: list[dict[str, str]] = field(default_factory=list)
    experts_skipped: list[dict[str, str]] = field(default_factory=list)
    winning_hypothesis: str = ""
    winning_confidence: float = 0.0
    evidence_chain: str = ""
    missing_evidence: list[str] = field(default_factory=list)
    risk_level: str = "MEDIUM"
    recommendation: str = ""
    full_text: str = ""
    runner_up_hypothesis: str | None = None
    runner_up_confidence: float | None = None
    rejection_reason: str | None = None

    def __post_init__(self) -> None:
        if not self.full_text:
            self.full_text = self.markdown_content
        if not self.winning_hypothesis and self.tribunal_summary:
            self.winning_hypothesis = self.tribunal_summary.get("primary_hypothesis", "")
        if self.winning_confidence == 0.0 and self.tribunal_summary:
            self.winning_confidence = self.tribunal_summary.get("confidence", 0.0)

    @property
    def confidence(self) -> float:
        """Calibrated tribunal confidence score."""
        return (
            self.winning_confidence
            or (self.executive_summary.get("calibrated_confidence", 0.0) if hasattr(self, "executive_summary") and self.executive_summary else 0.0)
            or (self.tribunal_summary.get("confidence", 0.0) if hasattr(self, "tribunal_summary") and self.tribunal_summary else 0.0)
        )

"""Investigation card evidence contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InvestigationCard:
    card_id: str
    source_expert: str
    derived_from_transactions: list[str]
    generated_at: str
    hypothesis: str
    confidence: float
    evidence: str | list[str] = field(default_factory=list)
    severity: str = "MEDIUM"
    supporting_features: list[str] = field(default_factory=list)
    supporting_metrics: dict[str, float] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)
    affected_accounts: list[str] = field(default_factory=list)
    time_window: Any = None
    supports: list[str] = field(default_factory=list)
    counter_hypothesis: str | None = None
    missing_data: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize card attributes for graph node creation."""
        return {
            "card_id": self.card_id,
            "source_expert": self.source_expert,
            "derived_from_transactions": self.derived_from_transactions,
            "generated_at": self.generated_at,
            "hypothesis": self.hypothesis,
            "confidence": self.confidence,
            "severity": self.severity,
            "evidence": self.evidence,
            "supporting_features": self.supporting_features,
            "supporting_metrics": self.supporting_metrics,
            "provenance": self.provenance,
            "affected_accounts": self.affected_accounts,
            "time_window": self.time_window,
            "supports": self.supports,
            "counter_hypothesis": self.counter_hypothesis,
            "missing_data": self.missing_data,
        }

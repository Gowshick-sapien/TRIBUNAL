"""Investigation card evidence contract."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class InvestigationCard:
    card_id: str
    source_expert: str
    derived_from_transactions: list[str]
    generated_at: str
    hypothesis: str
    confidence: float
    evidence: str
    supports: list[str] = field(default_factory=list)
    counter_hypothesis: str | None = None
    missing_data: str | None = None

    def to_dict(self) -> dict:
        """Serialize card attributes for graph node creation."""
        return {
            "card_id": self.card_id,
            "source_expert": self.source_expert,
            "derived_from_transactions": self.derived_from_transactions,
            "generated_at": self.generated_at,
            "hypothesis": self.hypothesis,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "supports": self.supports,
            "counter_hypothesis": self.counter_hypothesis,
            "missing_data": self.missing_data,
        }

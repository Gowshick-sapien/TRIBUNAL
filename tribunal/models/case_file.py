"""Case file shared working memory contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CaseFile:
    case_id: str | None = None
    dominant_confidence: float = 0.0
    contradictions_found: list[str] = field(default_factory=list)
    defense_skipped: bool = False
    dominant_hypothesis: str | None = None
    open_question: str | None = None
    active_investigation_stage: str | None = None
    evidence_cards: list[Any] = field(default_factory=list)

    def add_evidence_card(self, card: Any) -> None:
        """Add an investigation card to case file evidence repository."""
        self.evidence_cards.append(card)
        if hasattr(card, "confidence") and card.confidence > self.dominant_confidence:
            self.dominant_confidence = card.confidence
            if hasattr(card, "hypothesis"):
                self.dominant_hypothesis = card.hypothesis

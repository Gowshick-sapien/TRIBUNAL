"""Case file shared working memory contract."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CaseFile:
    dominant_confidence: float = 0.0
    contradictions_found: list[str] = field(default_factory=list)
    defense_skipped: bool = False
    dominant_hypothesis: str | None = None
    open_question: str | None = None
    active_investigation_stage: str | None = None

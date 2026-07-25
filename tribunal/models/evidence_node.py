"""Evidence graph node contract."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EvidenceNode:
    node_id: str
    hypothesis: str
    confidence: float
    evidence: str
    source_expert: str
    derived_from_transactions: list[str]
    counter_hypothesis: str | None = None
    missing_data: str | None = None

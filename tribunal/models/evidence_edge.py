"""Evidence graph edge contract."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EvidenceEdge:
    source: str
    target: str
    relation: str
    weight: float
    reason: str

"""Evidence graph edge contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvidenceEdge:
    """Represents a directional semantic relationship between nodes in the Evidence Graph."""
    source: str
    target: str
    relationship: str  # "HAS_EVIDENCE", "SUPPORTS", "CORROBORATES", "CONTRADICTS", "DERIVED_FROM", "SAME_ACCOUNT"
    weight: float = 1.0
    reason: str = ""
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize edge to dictionary."""
        return {
            "source": self.source,
            "target": self.target,
            "relationship": self.relationship,
            "weight": self.weight,
            "reason": self.reason,
            "confidence": self.confidence,
            "metadata": self.metadata,
        }

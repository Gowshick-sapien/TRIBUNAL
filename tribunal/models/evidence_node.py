"""Evidence graph node contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvidenceNode:
    """Represents an entity, card, hypothesis, or provenance node in the Evidence Graph."""
    node_id: str
    node_type: str  # "account", "card", "hypothesis", "provenance"
    label: str
    expert: str = "system"
    confidence: float = 1.0
    severity: str = "LOW"
    timestamp: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize node to dictionary."""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "label": self.label,
            "expert": self.expert,
            "confidence": self.confidence,
            "severity": self.severity,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "provenance": self.provenance,
        }

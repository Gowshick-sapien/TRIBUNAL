"""Evidence graph container contract."""

from __future__ import annotations

from dataclasses import dataclass, field

from tribunal.models.evidence_edge import EvidenceEdge
from tribunal.models.evidence_node import EvidenceNode


@dataclass
class EvidenceGraph:
    nodes: list[EvidenceNode] = field(default_factory=list)
    edges: list[EvidenceEdge] = field(default_factory=list)
    metadata: dict | None = None

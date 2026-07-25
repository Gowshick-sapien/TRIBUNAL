"""Evidence graph container contract wrapping networkx.DiGraph."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import logging
from pathlib import Path
from typing import Any
import networkx as nx

from tribunal.models.evidence_edge import EvidenceEdge
from tribunal.models.evidence_node import EvidenceNode

logger = logging.getLogger("tribunal.models.evidence_graph")


@dataclass
class EvidenceGraph:
    """EvidenceGraph container wrapping networkx.DiGraph."""
    nodes: list[EvidenceNode] = field(default_factory=list)
    edges: list[EvidenceEdge] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._graph = nx.DiGraph()
        self.sync_to_graph()

    def sync_to_graph(self) -> None:
        """Synchronize internal networkx.DiGraph with nodes and edges lists."""
        self._graph.clear()
        for node in self.nodes:
            self._graph.add_node(node.node_id, **node.to_dict())
        for edge in self.edges:
            self._graph.add_edge(edge.source, edge.target, **edge.to_dict())

    def add_node(self, node: EvidenceNode) -> None:
        """Add an EvidenceNode to graph."""
        self.nodes.append(node)
        self._graph.add_node(node.node_id, **node.to_dict())

    def add_edge(self, edge: EvidenceEdge) -> None:
        """Add an EvidenceEdge to graph."""
        self.edges.append(edge)
        self._graph.add_edge(edge.source, edge.target, **edge.to_dict())

    @property
    def graph(self) -> nx.DiGraph:
        """Return the underlying networkx.DiGraph."""
        return self._graph

    def to_dict(self) -> dict[str, Any]:
        """Serialize EvidenceGraph to dictionary."""
        return {
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
            "metrics": self.metrics,
            "metadata": self.metadata,
        }

    def save(self, filepath: str | Path) -> None:
        """Persist graph to JSON or gpickle file."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == ".gpickle":
            import pickle
            with open(path, "wb") as f:
                pickle.dump(self._graph, f)
        else:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, filepath: str | Path) -> EvidenceGraph:
        """Load graph from JSON or gpickle file."""
        path = Path(filepath)
        if path.suffix == ".gpickle":
            import pickle
            with open(path, "rb") as f:
                g = pickle.load(f)
            eg = cls()
            eg._graph = g
            # Extract nodes & edges from nx graph
            for node_id, data in g.nodes(data=True):
                eg.nodes.append(
                    EvidenceNode(
                        node_id=node_id,
                        node_type=data.get("node_type", "generic"),
                        label=data.get("label", node_id),
                        expert=data.get("expert", "system"),
                        confidence=float(data.get("confidence", 1.0)),
                        severity=data.get("severity", "LOW"),
                        timestamp=data.get("timestamp"),
                        metadata=data.get("metadata", {}),
                        provenance=data.get("provenance", {}),
                    )
                )
            for src, dst, data in g.edges(data=True):
                eg.edges.append(
                    EvidenceEdge(
                        source=src,
                        target=dst,
                        relationship=data.get("relationship", "CONNECTED"),
                        weight=float(data.get("weight", 1.0)),
                        reason=data.get("reason", ""),
                        confidence=float(data.get("confidence", 1.0)),
                        metadata=data.get("metadata", {}),
                    )
                )
            # Recompute metrics dictionary for loaded graph
            from tribunal.investigation.evidence.graph_metrics import GraphMetrics
            eg.metrics = GraphMetrics().compute_metrics(eg)
            return eg
        else:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            nodes = [EvidenceNode(**n) for n in data.get("nodes", [])]
            edges = [EvidenceEdge(**e) for e in data.get("edges", [])]
            eg = cls(nodes=nodes, edges=edges, metrics=data.get("metrics", {}), metadata=data.get("metadata", {}))
            if not eg.metrics:
                from tribunal.investigation.evidence.graph_metrics import GraphMetrics
                eg.metrics = GraphMetrics().compute_metrics(eg)
            return eg

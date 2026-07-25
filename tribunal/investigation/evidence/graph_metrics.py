"""Graph Metrics module — Computes structural graph topology statistics."""

from __future__ import annotations

import logging
from typing import Any, TYPE_CHECKING
import networkx as nx

if TYPE_CHECKING:
    from tribunal.models.evidence_graph import EvidenceGraph

logger = logging.getLogger("tribunal.investigation.evidence.metrics")


class GraphMetrics:
    """Computes structural analytics over an EvidenceGraph."""

    def compute_metrics(self, evidence_graph: EvidenceGraph) -> dict[str, Any]:
        """Calculate graph statistics over nodes and edges."""
        if not evidence_graph or not evidence_graph.nodes:
            return {
                "node_count": 0,
                "edge_count": 0,
                "connected_components": 0,
                "support_edges": 0,
                "corroboration_edges": 0,
                "contradiction_edges": 0,
                "average_confidence": 0.0,
                "graph_density": 0.0,
            }

        g = evidence_graph.graph
        node_count = g.number_of_nodes()
        edge_count = g.number_of_edges()

        support_cnt = sum(1 for e in evidence_graph.edges if e.relationship == "SUPPORTS")
        corroborate_cnt = sum(1 for e in evidence_graph.edges if e.relationship == "CORROBORATES")
        contradict_cnt = sum(1 for e in evidence_graph.edges if e.relationship == "CONTRADICTS")

        confidences = [n.confidence for n in evidence_graph.nodes if n.confidence is not None]
        avg_conf = round(sum(confidences) / len(confidences), 4) if confidences else 0.0

        # Calculate weakly connected components
        components_cnt = nx.number_weakly_connected_components(g) if node_count > 0 else 0
        density = round(nx.density(g), 4) if node_count > 1 else 0.0

        return {
            "node_count": node_count,
            "edge_count": edge_count,
            "connected_components": components_cnt,
            "support_edges": support_cnt,
            "corroboration_edges": corroborate_cnt,
            "contradiction_edges": contradict_cnt,
            "average_confidence": avg_conf,
            "graph_density": density,
        }

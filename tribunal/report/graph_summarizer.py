"""Graph Summarizer module — Summarizes topological EvidenceGraph metrics."""

from __future__ import annotations

from typing import Any

from tribunal.models.evidence_graph import EvidenceGraph


class GraphSummarizer:
    """Builds Section 6: Graph Topology Summary."""

    def build(self, graph: EvidenceGraph | None) -> dict[str, Any]:
        """Construct graph summary analytics payload."""
        if not graph:
            return {
                "node_count": 0,
                "edge_count": 0,
                "account_nodes": 0,
                "card_nodes": 0,
                "hypothesis_nodes": 0,
                "connected_components": 0,
                "corroboration_edges": 0,
                "contradiction_edges": 0,
                "average_confidence": 0.0,
                "graph_density": 0.0,
                "summary_statement": "No EvidenceGraph available.",
            }

        nx_graph = graph._graph
        metrics = graph.metrics or {}

        account_nodes = len([n for n, d in nx_graph.nodes(data=True) if d.get("node_type") == "account" or d.get("type") == "account" or n.startswith("acc_")])
        card_nodes = len([n for n, d in nx_graph.nodes(data=True) if d.get("node_type") == "card" or d.get("type") == "card" or n.startswith("card_")])
        hyp_nodes = len([n for n, d in nx_graph.nodes(data=True) if d.get("node_type") == "hypothesis" or d.get("type") == "hypothesis" or n.startswith("hyp_")])

        corroboration_edges = len([(u, v) for u, v, d in nx_graph.edges(data=True) if d.get("relationship") == "CORROBORATES"])
        contradiction_edges = len([(u, v) for u, v, d in nx_graph.edges(data=True) if d.get("relationship") == "CONTRADICTS"])

        n_count = len(graph.nodes)
        e_count = len(graph.edges)

        statement = f"Evidence Graph synthesized with {n_count} Nodes ({account_nodes} Accounts, {card_nodes} Cards, {hyp_nodes} Hypotheses) and {e_count} Edges ({corroboration_edges} Corroborations, {contradiction_edges} Contradictions)."

        return {
            "node_count": n_count,
            "edge_count": e_count,
            "account_nodes": account_nodes,
            "card_nodes": card_nodes,
            "hypothesis_nodes": hyp_nodes,
            "connected_components": metrics.get("connected_components", 1 if n_count > 0 else 0),
            "corroboration_edges": corroboration_edges,
            "contradiction_edges": contradiction_edges,
            "average_confidence": metrics.get("average_confidence", 0.0),
            "graph_density": metrics.get("graph_density", 0.0),
            "summary_statement": statement,
        }

"""Unit tests for GraphSummarizer (Phase C.7)."""

from __future__ import annotations

from tribunal.models.evidence_edge import EvidenceEdge
from tribunal.models.evidence_graph import EvidenceGraph
from tribunal.models.evidence_node import EvidenceNode
from tribunal.report.graph_summarizer import GraphSummarizer


def test_graph_summarizer_none():
    summarizer = GraphSummarizer()
    summary = summarizer.build(None)
    assert summary["node_count"] == 0
    assert summary["edge_count"] == 0
    assert "No EvidenceGraph available" in summary["summary_statement"]


def test_graph_summarizer_populated():
    graph = EvidenceGraph()
    graph.add_node(EvidenceNode(node_id="acc_1", node_type="account", label="Account 1"))
    graph.add_node(EvidenceNode(node_id="card_1", node_type="card", label="Card 1"))
    graph.add_edge(EvidenceEdge(source="acc_1", target="card_1", relationship="HAS_EVIDENCE"))

    summarizer = GraphSummarizer()
    summary = summarizer.build(graph)

    assert summary["node_count"] == 2
    assert summary["edge_count"] == 1
    assert "2 Nodes" in summary["summary_statement"]

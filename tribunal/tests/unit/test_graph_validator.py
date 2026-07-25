"""Unit tests for GraphValidator."""

import pytest
from tribunal.investigation.evidence.graph_validator import GraphValidator
from tribunal.models.evidence_edge import EvidenceEdge
from tribunal.models.evidence_graph import EvidenceGraph
from tribunal.models.evidence_node import EvidenceNode
from tribunal.models.investigation_card import InvestigationCard


def test_graph_validator_card_validation():
    validator = GraphValidator()
    valid_card = InvestigationCard(
        card_id="card_001",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring",
        confidence=0.85,
        provenance={"detectors": ["StructuringDetector"]},
    )
    assert validator.validate_card(valid_card) is True

    invalid_card = InvestigationCard(
        card_id="card_002",
        source_expert="unknown_expert",
        derived_from_transactions=[],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Test",
        confidence=1.5,
    )
    assert validator.validate_card(invalid_card) is False


def test_graph_validator_graph_integrity():
    validator = GraphValidator()

    node_a = EvidenceNode(node_id="A", node_type="account", label="Account A", confidence=1.0)
    node_b = EvidenceNode(node_id="B", node_type="card", label="Card B", confidence=0.8)
    edge = EvidenceEdge(source="A", target="B", relationship="HAS_EVIDENCE")

    eg = EvidenceGraph(nodes=[node_a, node_b], edges=[edge])
    assert validator.validate_graph(eg) is True

    # Test dangling edge
    dangling_edge = EvidenceEdge(source="A", target="MISSING", relationship="HAS_EVIDENCE")
    eg_dangling = EvidenceGraph(nodes=[node_a, node_b], edges=[dangling_edge])
    assert validator.validate_graph(eg_dangling) is False

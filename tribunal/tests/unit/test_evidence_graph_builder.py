"""Unit tests for EvidenceGraphBuilder."""

import pytest
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.case_file import CaseFile
from tribunal.models.evidence_graph import EvidenceGraph
from tribunal.models.investigation_card import InvestigationCard


def test_evidence_graph_builder_single_card():
    builder = EvidenceGraphBuilder()
    card = InvestigationCard(
        card_id="c_fin_01",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring",
        confidence=0.88,
        affected_accounts=["ACC_101"],
        provenance={"detectors": ["StructuringDetector"]},
    )

    eg = builder.build([card])
    assert isinstance(eg, EvidenceGraph)
    assert len(eg.nodes) == 3  # Account, Card, Hypothesis
    assert eg.metrics["node_count"] == 3
    assert eg.metrics["support_edges"] >= 1


def test_evidence_graph_builder_multi_expert_corroboration():
    builder = EvidenceGraphBuilder()
    fin_card = InvestigationCard(
        card_id="c_fin_02",
        source_expert="financial",
        derived_from_transactions=["TX10"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Dormant Structuring",
        confidence=0.85,
        affected_accounts=["ACC_202"],
        provenance={"detectors": ["StructuringDetector"]},
    )
    beh_card = InvestigationCard(
        card_id="c_beh_02",
        source_expert="behaviour",
        derived_from_transactions=["TX11"],
        generated_at="2026-07-25T12:05:00Z",
        hypothesis="Dormant Structuring",
        confidence=0.80,
        affected_accounts=["ACC_202"],
        provenance={"detectors": ["DormancyDetector"]},
    )

    eg = builder.build([fin_card, beh_card])
    assert eg.metrics["corroboration_edges"] >= 1
    assert eg.metrics["connected_components"] == 1


def test_evidence_graph_builder_unrelated_accounts():
    builder = EvidenceGraphBuilder()
    card_a = InvestigationCard(
        card_id="c_acc_a",
        source_expert="financial",
        derived_from_transactions=["TXA"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Structuring A",
        confidence=0.80,
        affected_accounts=["ACC_AAA"],
        provenance={"detectors": ["StructuringDetector"]},
    )
    card_b = InvestigationCard(
        card_id="c_acc_b",
        source_expert="behaviour",
        derived_from_transactions=["TXB"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Dormancy B",
        confidence=0.75,
        affected_accounts=["ACC_BBB"],
        provenance={"detectors": ["DormancyDetector"]},
    )

    eg = builder.build([card_a, card_b])
    assert eg.metrics["connected_components"] == 2


def test_evidence_graph_builder_invalid_card_rejection():
    builder = EvidenceGraphBuilder()
    invalid_card = InvestigationCard(
        card_id="c_invalid",
        source_expert="unknown",
        derived_from_transactions=[],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Invalid",
        confidence=1.5,
    )

    eg = builder.build([invalid_card])
    assert eg.metrics["node_count"] == 0
    assert eg.metrics["edge_count"] == 0

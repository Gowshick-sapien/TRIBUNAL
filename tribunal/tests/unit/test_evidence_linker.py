"""Unit tests for EvidenceLinker."""

import pytest
from tribunal.investigation.evidence.evidence_linker import EvidenceLinker
from tribunal.models.investigation_card import InvestigationCard


def test_evidence_linker_single_card():
    linker = EvidenceLinker()
    card = InvestigationCard(
        card_id="c_single",
        source_expert="financial",
        derived_from_transactions=["TX10"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring",
        confidence=0.85,
        affected_accounts=["ACC_555"],
        supporting_features=["threshold_proximity"],
    )

    nodes, edges = linker.generate_nodes_and_edges([card])
    assert len(nodes) == 3  # Account, Card, Hypothesis
    node_types = {n.node_type for n in nodes}
    assert node_types == {"account", "card", "hypothesis"}

    relationships = {e.relationship for e in edges}
    assert "HAS_EVIDENCE" in relationships
    assert "SUPPORTS" in relationships
    assert "DERIVED_FROM" in relationships


def test_evidence_linker_corroborating_cards():
    linker = EvidenceLinker()
    fin_card = InvestigationCard(
        card_id="c_fin",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Structuring Activity",
        confidence=0.80,
        affected_accounts=["ACC_777"],
    )
    beh_card = InvestigationCard(
        card_id="c_beh",
        source_expert="behaviour",
        derived_from_transactions=["TX2"],
        generated_at="2026-07-25T12:05:00Z",
        hypothesis="Structuring Activity",
        confidence=0.85,
        affected_accounts=["ACC_777"],
    )

    nodes, edges = linker.generate_nodes_and_edges([fin_card, beh_card])
    corroborate_edges = [e for e in edges if e.relationship == "CORROBORATES"]
    assert len(corroborate_edges) >= 1
    assert corroborate_edges[0].source == "c_fin"
    assert corroborate_edges[0].target == "c_beh"

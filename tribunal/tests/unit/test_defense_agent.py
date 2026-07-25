"""Unit tests for DefenseAgent — Adversarial Review Engine (Phase C.5)."""

from tribunal.adversarial.defense_agent import DefenseAgent
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.case_file import CaseFile
from tribunal.models.investigation_card import InvestigationCard


def test_defense_agent_review_multi_expert():
    fin_card = InvestigationCard(
        card_id="c_fin",
        source_expert="financial",
        derived_from_transactions=["TX1", "TX2"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring Activity",
        confidence=0.88,
        severity="HIGH",
        provenance={"detectors": ["StructuringDetector"]},
        affected_accounts=["ACC_100"],
    )

    beh_card = InvestigationCard(
        card_id="c_beh",
        source_expert="behaviour",
        derived_from_transactions=["TX3"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Multiple Behavioural Anomalies",
        confidence=0.90,
        severity="CRITICAL",
        provenance={"detectors": ["BehaviourDriftDetector"]},
        affected_accounts=["ACC_100"],
    )

    builder = EvidenceGraphBuilder()
    graph = builder.build([fin_card, beh_card])
    initial_node_count = len(graph.nodes)

    agent = DefenseAgent()
    case_file = CaseFile(case_id="case_test_001")
    defense_cards = agent.review(graph, case_file)

    assert len(defense_cards) >= 1
    for card in defense_cards:
        assert card.source_expert == "defense"
        assert card.affected_accounts == ["ACC_100"]

    # Augment graph with defense cards
    augmented_graph = builder.augment_graph(graph, defense_cards)
    assert len(augmented_graph.nodes) > initial_node_count
    assert augmented_graph.metrics["node_count"] == len(augmented_graph.nodes)


def test_defense_agent_weak_single_expert():
    weak_card = InvestigationCard(
        card_id="c_weak",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Velocity Spike",
        confidence=0.55,
        severity="LOW",
        affected_accounts=["ACC_200"],
    )

    builder = EvidenceGraphBuilder()
    graph = builder.build([weak_card])

    agent = DefenseAgent()
    defense_cards = agent.review(graph)

    assert len(defense_cards) >= 1
    weak_defense = [c for c in defense_cards if c.provenance.get("defense_type") == "weak_evidence"]
    assert len(weak_defense) >= 1

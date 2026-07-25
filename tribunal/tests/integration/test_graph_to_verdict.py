"""Integration test: EvidenceGraph to TribunalVerdict end-to-end flow."""

from tribunal.adversarial.defense_agent import DefenseAgent
from tribunal.consensus.tribunal import Tribunal
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.case_file import CaseFile
from tribunal.models.investigation_card import InvestigationCard


def test_end_to_end_graph_to_verdict_integration():
    # 1. Prosecution Cards
    fin_card = InvestigationCard(
        card_id="c_fin_e2e",
        source_expert="financial",
        derived_from_transactions=["TX101", "TX102"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring Activity for Account ACC_8000A94C0",
        confidence=0.98,
        severity="CRITICAL",
        affected_accounts=["ACC_8000A94C0"],
    )

    beh_card = InvestigationCard(
        card_id="c_beh_e2e",
        source_expert="behaviour",
        derived_from_transactions=["TX201"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Multiple Behavioural Anomalies for Account ACC_8000A94C0",
        confidence=0.95,
        severity="HIGH",
        affected_accounts=["ACC_8000A94C0"],
    )

    case_file = CaseFile(case_id="case_e2e_001")

    # 2. Build Evidence Graph
    builder = EvidenceGraphBuilder()
    graph = builder.build([fin_card, beh_card], case_file=case_file)

    # 3. Perform Adversarial Review
    agent = DefenseAgent()
    defense_cards = agent.review(graph, case_file)
    augmented_graph = builder.augment_graph(graph, defense_cards)

    # 4. Perform Tribunal Deliberation
    tribunal = Tribunal()
    verdict = tribunal.deliberate(augmented_graph, case_file)

    # 5. Assertions
    assert verdict is not None
    assert verdict.verdict in ("LIKELY_MALICIOUS", "POSSIBLY_MALICIOUS", "LIKELY_LEGITIMATE", "INCONCLUSIVE")
    assert verdict.confidence > 0.0
    assert len(verdict.deliberation_trace) >= 5
    assert verdict.evidence_summary["graph_node_count"] == len(augmented_graph.nodes)

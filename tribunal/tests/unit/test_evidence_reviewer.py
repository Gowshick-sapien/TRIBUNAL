"""Unit tests for EvidenceReviewer."""

from tribunal.adversarial.evidence_reviewer import EvidenceReviewer
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.investigation_card import InvestigationCard


def test_evidence_reviewer_traversal():
    card = InvestigationCard(
        card_id="c1",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring Activity",
        confidence=0.85,
        severity="HIGH",
        affected_accounts=["ACC_100"],
    )

    builder = EvidenceGraphBuilder()
    graph = builder.build([card])

    reviewer = EvidenceReviewer()
    ctx = reviewer.review(graph)

    assert len(ctx.account_nodes) == 1
    assert len(ctx.prosecution_cards) == 1
    assert len(ctx.hypotheses) == 1
    assert "financial" in ctx.expert_cards_map
    assert "ACC_100" in ctx.account_cards_map

    # Test new snapshot metadata
    assert ctx.graph_snapshot_id != ""
    assert ctx.review_timestamp != ""
    assert ctx.review_version == "C.5"

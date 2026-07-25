"""Unit tests for UncertaintyEstimator."""

from tribunal.adversarial.evidence_reviewer import EvidenceReviewer
from tribunal.adversarial.uncertainty_estimator import UncertaintyEstimator
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.investigation_card import InvestigationCard


def test_uncertainty_estimator_single_vs_multi():
    card1 = InvestigationCard(
        card_id="c1",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring",
        confidence=0.80,
        affected_accounts=["ACC_100"],
    )

    builder = EvidenceGraphBuilder()
    graph = builder.build([card1])

    reviewer = EvidenceReviewer()
    ctx = reviewer.review(graph)

    estimator = UncertaintyEstimator()
    score1 = estimator.estimate_for_account("ACC_100", ctx)

    assert score1.is_high_uncertainty is True
    assert score1.expert_diversity == 1

    # Add second expert card
    card2 = InvestigationCard(
        card_id="c2",
        source_expert="behaviour",
        derived_from_transactions=["TX2"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Behaviour Drift",
        confidence=0.85,
        affected_accounts=["ACC_100"],
    )
    graph2 = builder.build([card1, card2])
    ctx2 = reviewer.review(graph2)
    score2 = estimator.estimate_for_account("ACC_100", ctx2)

    assert score2.uncertainty_score < score1.uncertainty_score
    assert score2.expert_diversity == 2

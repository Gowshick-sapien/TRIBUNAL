"""Unit tests for EvidenceStrengthAnalyzer."""

from tribunal.adversarial.evidence_reviewer import EvidenceReviewer
from tribunal.adversarial.evidence_strength_analyzer import EvidenceStrengthAnalyzer
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.investigation_card import InvestigationCard


def test_evidence_strength_analyzer():
    card = InvestigationCard(
        card_id="c1",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring",
        confidence=0.60,
        severity="MEDIUM",
        provenance={"detectors": ["StructuringDetector"]},
        affected_accounts=["ACC_100"],
    )

    builder = EvidenceGraphBuilder()
    graph = builder.build([card])

    reviewer = EvidenceReviewer()
    ctx = reviewer.review(graph)

    analyzer = EvidenceStrengthAnalyzer()
    score = analyzer.analyze_card(card, ctx)

    assert 0.0 <= score.strength_score <= 1.0
    assert score.is_weak_evidence is True

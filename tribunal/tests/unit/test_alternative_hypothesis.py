"""Unit tests for AlternativeHypothesisGenerator."""

from tribunal.adversarial.alternative_hypothesis_generator import AlternativeHypothesisGenerator
from tribunal.adversarial.evidence_reviewer import EvidenceReviewer
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.investigation_card import InvestigationCard


def test_alternative_hypothesis_generator():
    structuring_card = InvestigationCard(
        card_id="c_struct",
        source_expert="financial",
        derived_from_transactions=["TX1", "TX2"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring Activity",
        confidence=0.88,
        severity="HIGH",
        affected_accounts=["ACC_100"],
    )

    builder = EvidenceGraphBuilder()
    graph = builder.build([structuring_card])

    reviewer = EvidenceReviewer()
    ctx = reviewer.review(graph)

    generator = AlternativeHypothesisGenerator()
    alternatives = generator.generate(ctx)

    assert len(alternatives) >= 1
    assert alternatives[0].category == "payroll"
    assert "Legitimate Business Activity" in alternatives[0].top_level_hypothesis
    assert alternatives[0].plausibility_score > 0.60

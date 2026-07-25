"""Unit tests for ContradictionDetector."""

from tribunal.adversarial.contradiction_detector import ContradictionDetector
from tribunal.adversarial.evidence_reviewer import EvidenceReviewer
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.investigation_card import InvestigationCard


def test_contradiction_detector_conflict():
    fin_card = InvestigationCard(
        card_id="c_fin",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring Activity",
        confidence=0.85,
        severity="HIGH",
        affected_accounts=["ACC_100"],
    )

    beh_card = InvestigationCard(
        card_id="c_beh",
        source_expert="behaviour",
        derived_from_transactions=["TX2"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Normal Behaviour",
        confidence=0.40,
        severity="LOW",
        affected_accounts=["ACC_100"],
        supporting_metrics={"behaviour_deviation_ratio": 1.1},
    )

    builder = EvidenceGraphBuilder()
    graph = builder.build([fin_card, beh_card])

    reviewer = EvidenceReviewer()
    ctx = reviewer.review(graph)

    detector = ContradictionDetector()
    findings = detector.detect(ctx)

    assert len(findings) >= 1
    assert findings[0].conflict_type == "financial_vs_behaviour"
    assert findings[0].account_id == "ACC_100"

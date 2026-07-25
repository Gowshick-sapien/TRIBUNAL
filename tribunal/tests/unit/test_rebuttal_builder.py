"""Unit tests for RebuttalBuilder."""

from tribunal.adversarial.alternative_hypothesis_generator import AlternativeExplanation
from tribunal.adversarial.evidence_strength_analyzer import EvidenceStrengthScore
from tribunal.adversarial.rebuttal_builder import RebuttalBuilder
from tribunal.adversarial.uncertainty_estimator import UncertaintyScore


def test_rebuttal_builder_alternative_card():
    builder = RebuttalBuilder()
    alt = AlternativeExplanation(
        account_id="ACC_100",
        target_card_id="c1",
        category="payroll",
        explanation_title="Routine Business Payroll & Invoice Batch Settlement",
        top_level_hypothesis="Legitimate Business Activity for Account ACC_100",
        explanation_details="Routine monthly payroll",
        plausibility_score=0.75,
        supporting_signals=["batch_payment_pattern"],
    )
    strength = EvidenceStrengthScore("c1", 0.60, 0, 0, 0.5, False)
    uncertainty = UncertaintyScore("ACC_100", 0.50, 1, 1, True)

    def_card = builder.build_alternative_card(alt, strength, uncertainty)

    assert def_card.source_expert == "defense"
    assert def_card.affected_accounts == ["ACC_100"]
    assert def_card.hypothesis == "Legitimate Business Activity for Account ACC_100"
    assert "payroll" in def_card.provenance.get("explanation_category", "")
    assert def_card.confidence > 0.0

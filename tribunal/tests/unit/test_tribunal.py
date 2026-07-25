"""Unit tests for Tribunal orchestrator covering the full Verification Matrix."""

import pytest
from tribunal.consensus.tribunal import Tribunal
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.case_file import CaseFile
from tribunal.models.investigation_card import InvestigationCard


@pytest.fixture
def tribunal_engine():
    return Tribunal()


def test_verification_scenario_1_likely_malicious(tribunal_engine):
    """Scenario 1: Strong financial + behaviour corroboration -> LIKELY_MALICIOUS."""
    fin_card = InvestigationCard(
        card_id="c_fin",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring Activity",
        confidence=0.90,
        severity="HIGH",
        affected_accounts=["ACC_100"],
        provenance={"detectors": ["StructuringDetector"], "transaction_ids": ["TX1"]},
    )
    beh_card = InvestigationCard(
        card_id="c_beh",
        source_expert="behaviour",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring Activity",
        confidence=0.88,
        severity="HIGH",
        affected_accounts=["ACC_100"],
        provenance={"detectors": ["BehaviourDriftDetector"], "transaction_ids": ["TX1"]},
    )

    builder = EvidenceGraphBuilder()
    graph = builder.build([fin_card, beh_card])
    case_file = CaseFile(case_id="case_s1")

    verdict = tribunal_engine.deliberate(graph, case_file)

    assert verdict.verdict == "LIKELY_MALICIOUS"
    assert verdict.confidence > 0.80
    assert "Possible Structuring Activity" in verdict.winning_hypothesis


def test_verification_scenario_2_likely_legitimate(tribunal_engine):
    """Scenario 2: Strong defense evidence dominates -> LIKELY_LEGITIMATE."""
    def_card = InvestigationCard(
        card_id="c_def",
        source_expert="defense",
        derived_from_transactions=[],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Legitimate Business Activity for Account ACC_100",
        confidence=0.85,
        severity="MEDIUM",
        affected_accounts=["ACC_100"],
        supporting_features=["Routine Business Payroll"],
        provenance={"defense_type": "alternative_explanation"},
    )

    builder = EvidenceGraphBuilder()
    graph = builder.build([])
    builder.augment_graph(graph, [def_card])
    case_file = CaseFile(case_id="case_s2")

    verdict = tribunal_engine.deliberate(graph, case_file)

    assert verdict.verdict == "LIKELY_LEGITIMATE"
    assert "Legitimate Business Activity" in verdict.winning_hypothesis


def test_verification_scenario_3_balanced_inconclusive(tribunal_engine):
    """Scenario 3: Balanced competing evidence -> INCONCLUSIVE."""
    fin_card = InvestigationCard(
        card_id="c_fin",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring Activity",
        confidence=0.55,
        severity="MEDIUM",
        affected_accounts=["ACC_100"],
        provenance={"detectors": ["StructuringDetector"], "transaction_ids": ["TX1"]},
    )
    def_card = InvestigationCard(
        card_id="c_def",
        source_expert="defense",
        derived_from_transactions=[],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Legitimate Business Activity for Account ACC_100",
        confidence=0.55,
        severity="MEDIUM",
        affected_accounts=["ACC_100"],
        provenance={"defense_type": "alternative_explanation"},
    )

    builder = EvidenceGraphBuilder()
    graph = builder.build([fin_card])
    builder.augment_graph(graph, [def_card])
    case_file = CaseFile(case_id="case_s3")

    verdict = tribunal_engine.deliberate(graph, case_file)

    assert verdict.verdict == "INCONCLUSIVE"


def test_verification_scenario_4_weak_evidence_inconclusive(tribunal_engine):
    """Scenario 4: Weak evidence -> INCONCLUSIVE."""
    fin_card = InvestigationCard(
        card_id="c_fin",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Unusual Low Activity",
        confidence=0.30,
        severity="LOW",
        affected_accounts=["ACC_100"],
        provenance={"detectors": ["StructuringDetector"], "transaction_ids": ["TX1"]},
    )

    builder = EvidenceGraphBuilder()
    graph = builder.build([fin_card])
    case_file = CaseFile(case_id="case_s4")

    verdict = tribunal_engine.deliberate(graph, case_file)

    assert verdict.verdict == "INCONCLUSIVE"


def test_verification_scenario_5_single_expert_possibly_malicious(tribunal_engine):
    """Scenario 5: Single expert only -> POSSIBLY_MALICIOUS."""
    fin_card = InvestigationCard(
        card_id="c_fin",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring Activity",
        confidence=0.85,
        severity="HIGH",
        affected_accounts=["ACC_100"],
        provenance={"detectors": ["StructuringDetector"], "transaction_ids": ["TX1"]},
    )

    builder = EvidenceGraphBuilder()
    graph = builder.build([fin_card])
    case_file = CaseFile(case_id="case_s5")

    verdict = tribunal_engine.deliberate(graph, case_file)

    assert verdict.verdict == "POSSIBLY_MALICIOUS"
    assert "financial" in verdict.supporting_experts

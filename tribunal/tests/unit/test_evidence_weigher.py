"""Unit tests for EvidenceWeigher."""

from tribunal.consensus.evidence_weigher import EvidenceWeigher
from tribunal.consensus.hypothesis_extractor import HypothesisExtractor
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.investigation_card import InvestigationCard


def test_evidence_weigher_multi_expert_boost():
    fin_card = InvestigationCard(
        card_id="c_fin",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Unusual Activity",
        confidence=0.80,
        severity="HIGH",
        affected_accounts=["ACC_100"],
        provenance={"detectors": ["StructuringDetector"], "transaction_ids": ["TX1"]},
    )

    beh_card = InvestigationCard(
        card_id="c_beh",
        source_expert="behaviour",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Unusual Activity",
        confidence=0.80,
        severity="HIGH",
        affected_accounts=["ACC_100"],
        provenance={"detectors": ["BehaviourDriftDetector"], "transaction_ids": ["TX1"]},
    )

    builder = EvidenceGraphBuilder()
    graph = builder.build([fin_card, beh_card])

    extractor = HypothesisExtractor()
    extracted = extractor.extract(graph)

    weigher = EvidenceWeigher()
    scores = weigher.weigh(extracted, graph)

    assert len(scores) >= 1
    assert scores[0].raw_support_score > 0.85
    assert scores[0].multi_expert_multiplier == 1.15

"""Unit tests for HypothesisExtractor."""

from tribunal.consensus.hypothesis_extractor import HypothesisExtractor
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.investigation_card import InvestigationCard


def test_hypothesis_extractor_prosecution_and_defense():
    prosecution_card = InvestigationCard(
        card_id="c_fin_1",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring Activity",
        confidence=0.85,
        severity="HIGH",
        affected_accounts=["ACC_100"],
        provenance={"detectors": ["StructuringDetector"], "transaction_ids": ["TX1"]},
    )

    defense_card = InvestigationCard(
        card_id="c_def_1",
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
    graph = builder.build([prosecution_card])
    builder.augment_graph(graph, [defense_card])

    extractor = HypothesisExtractor()
    extracted = extractor.extract(graph)

    assert len(extracted) == 2
    titles = [h.title for h in extracted]
    assert any("Structuring" in t for t in titles)
    assert any("Legitimate" in t for t in titles)

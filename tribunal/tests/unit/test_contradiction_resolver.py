"""Unit tests for ContradictionResolver."""

from tribunal.consensus.contradiction_resolver import ContradictionResolver
from tribunal.consensus.evidence_weigher import EvidenceWeigher
from tribunal.consensus.hypothesis_extractor import HypothesisExtractor
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.investigation_card import InvestigationCard


def test_contradiction_resolver_defense_penalty():
    fin_card = InvestigationCard(
        card_id="c_fin",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring",
        confidence=0.85,
        severity="HIGH",
        affected_accounts=["ACC_100"],
        provenance={"detectors": ["StructuringDetector"], "transaction_ids": ["TX1"]},
    )

    def_card = InvestigationCard(
        card_id="c_def",
        source_expert="defense",
        derived_from_transactions=[],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Legitimate Business Activity for Account ACC_100",
        confidence=0.70,
        severity="MEDIUM",
        affected_accounts=["ACC_100"],
        provenance={"defense_type": "alternative_explanation"},
    )

    builder = EvidenceGraphBuilder()
    graph = builder.build([fin_card])
    builder.augment_graph(graph, [def_card])

    extractor = HypothesisExtractor()
    extracted = extractor.extract(graph)

    weigher = EvidenceWeigher()
    scores = weigher.weigh(extracted, graph)

    resolver = ContradictionResolver()
    resolved = resolver.resolve(scores, extracted, graph)

    assert len(resolved) == 2
    structuring_res = next(r for r in resolved if "Structuring" in r.title)
    assert structuring_res.opposing_score > 0.0
    assert structuring_res.net_support_score < structuring_res.raw_support_score

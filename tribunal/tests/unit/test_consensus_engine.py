"""Unit tests for ConsensusEngine."""

from tribunal.consensus.consensus_engine import (
    INCONCLUSIVE,
    LIKELY_LEGITIMATE,
    LIKELY_MALICIOUS,
    POSSIBLY_MALICIOUS,
    ConsensusEngine,
)
from tribunal.consensus.contradiction_resolver import ResolvedHypothesis


def test_consensus_engine_likely_malicious():
    engine = ConsensusEngine()
    hyp1 = ResolvedHypothesis(
        hypothesis_id="h1",
        title="Possible Structuring",
        raw_support_score=0.92,
        opposing_score=0.10,
        net_support_score=0.82,
        expert_sources=["financial", "behaviour"],
        is_defense_hypothesis=False,
    )
    hyp2 = ResolvedHypothesis(
        hypothesis_id="h2",
        title="Legitimate Business Activity",
        raw_support_score=0.45,
        opposing_score=0.20,
        net_support_score=0.25,
        expert_sources=["defense"],
        is_defense_hypothesis=True,
    )

    result = engine.evaluate([hyp1, hyp2])
    assert result.consensus_category == LIKELY_MALICIOUS
    assert result.winning_hypothesis.title == "Possible Structuring"
    assert result.confidence_gap == 0.57


def test_consensus_engine_inconclusive():
    engine = ConsensusEngine()
    hyp1 = ResolvedHypothesis(
        hypothesis_id="h1",
        title="Possible Structuring",
        raw_support_score=0.50,
        opposing_score=0.25,
        net_support_score=0.25,
        expert_sources=["financial"],
        is_defense_hypothesis=False,
    )

    result = engine.evaluate([hyp1])
    assert result.consensus_category == INCONCLUSIVE
    assert "below minimum threshold" in result.rejection_reason

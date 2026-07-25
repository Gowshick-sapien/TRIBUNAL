"""Unit tests for ConfidenceCalibrator."""

from tribunal.consensus.confidence_calibrator import ConfidenceCalibrator
from tribunal.consensus.consensus_engine import ConsensusResult, LIKELY_MALICIOUS
from tribunal.consensus.contradiction_resolver import ResolvedHypothesis
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder


def test_confidence_calibrator():
    hyp1 = ResolvedHypothesis(
        hypothesis_id="h1",
        title="Possible Structuring",
        raw_support_score=0.90,
        opposing_score=0.10,
        net_support_score=0.80,
        expert_sources=["financial", "behaviour"],
        is_defense_hypothesis=False,
        supporting_cards=["c1", "c2"],
    )

    c_res = ConsensusResult(
        consensus_category=LIKELY_MALICIOUS,
        winning_hypothesis=hyp1,
        runner_up_hypothesis=None,
        confidence_gap=0.80,
        ranked_hypotheses=[hyp1],
    )

    builder = EvidenceGraphBuilder()
    graph = builder.build([])

    calibrator = ConfidenceCalibrator()
    calibrated = calibrator.calibrate(c_res, graph)

    assert calibrated >= 0.85
    assert calibrated <= 0.98

"""Unit tests for VerdictBuilder."""

from tribunal.consensus.consensus_engine import ConsensusResult, LIKELY_MALICIOUS
from tribunal.consensus.contradiction_resolver import ResolvedHypothesis
from tribunal.consensus.deliberation_trace import DeliberationTrace
from tribunal.consensus.verdict_builder import VerdictBuilder
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.case_file import CaseFile


def test_verdict_builder():
    hyp1 = ResolvedHypothesis(
        hypothesis_id="h1",
        title="Possible Structuring",
        raw_support_score=0.90,
        opposing_score=0.10,
        net_support_score=0.80,
        expert_sources=["financial", "behaviour"],
        is_defense_hypothesis=False,
        supporting_cards=["c_fin_1"],
    )

    c_res = ConsensusResult(
        consensus_category=LIKELY_MALICIOUS,
        winning_hypothesis=hyp1,
        runner_up_hypothesis=None,
        confidence_gap=0.80,
        ranked_hypotheses=[hyp1],
    )

    trace = DeliberationTrace()
    trace.add_step("Stage 1", "Test step")

    builder = EvidenceGraphBuilder()
    graph = builder.build([])
    case_file = CaseFile(case_id="case_1")

    vb = VerdictBuilder()
    verdict = vb.build_verdict(c_res, 0.88, trace, graph, case_file)

    assert verdict.verdict == LIKELY_MALICIOUS
    assert verdict.winning_hypothesis == "Possible Structuring"
    assert verdict.confidence == 0.88
    assert len(verdict.deliberation_trace) == 1

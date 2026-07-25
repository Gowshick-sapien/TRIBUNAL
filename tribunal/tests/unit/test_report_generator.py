"""Unit and integration tests for ReportGenerator (Phase C.7)."""

from __future__ import annotations

import datetime
from tribunal.models.case_file import CaseFile
from tribunal.models.evidence_edge import EvidenceEdge
from tribunal.models.evidence_graph import EvidenceGraph
from tribunal.models.evidence_node import EvidenceNode
from tribunal.models.investigation_card import InvestigationCard
from tribunal.models.tribunal_verdict import TribunalVerdict
from tribunal.report.report_generator import ReportGenerator


def test_report_generator_complete_investigation():
    now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
    verdict = TribunalVerdict(
        verdict="POSSIBLY_MALICIOUS",
        winning_hypothesis="Multiple Behavioural Anomalies",
        winning_score=0.76,
        confidence=0.58,
        primary_hypothesis="Multiple Behavioural Anomalies",
        primary_score=0.76,
        secondary_hypothesis="Possible Structuring Activity",
        secondary_score=0.74,
        confidence_gap=0.02,
        risk_level="MEDIUM",
    )
    case_file = CaseFile(case_id="case_complete")
    card = InvestigationCard(
        card_id="card_fin_01",
        source_expert="financial",
        derived_from_transactions=["TX_01"],
        generated_at=now_str,
        hypothesis="Possible Structuring Activity",
        confidence=0.74,
        supporting_metrics={"threshold_proximity": 0.95},
    )
    case_file.add_evidence_card(card)

    graph = EvidenceGraph()
    graph.add_node(EvidenceNode(node_id="acc_1", node_type="account", label="Account 1"))
    graph.add_node(EvidenceNode(node_id="card_fin_01", node_type="card", label="Card Fin 01"))
    graph.add_edge(EvidenceEdge(source="acc_1", target="card_fin_01", relationship="HAS_EVIDENCE"))

    generator = ReportGenerator()
    report = generator.generate(
        case_file=case_file,
        evidence_graph=graph,
        tribunal_verdict=verdict,
        query_text="Find structuring and unusual behaviour",
    )

    assert report.report_id.startswith("rpt_case_complete_")
    assert len(report.markdown_content) > 0
    assert "<!DOCTYPE html>" in report.html_content
    assert report.json_payload["executive_summary"]["verdict"] == "POSSIBLY_MALICIOUS"


def test_report_generator_no_defense_evidence():
    verdict = TribunalVerdict(verdict="LIKELY_MALICIOUS", winning_hypothesis="Structuring", winning_score=0.9, confidence=0.85)
    case_file = CaseFile(case_id="case_nodef")

    generator = ReportGenerator()
    report = generator.generate(case_file=case_file, tribunal_verdict=verdict)

    assert report.defense_summary["has_defense_evidence"] is False
    assert "No alternative hypotheses generated" in report.defense_summary["summary_statement"]


def test_report_generator_inconclusive_verdict():
    verdict = TribunalVerdict(verdict="INCONCLUSIVE", winning_hypothesis="Weak Evidence", winning_score=0.3, confidence=0.25)

    generator = ReportGenerator()
    report = generator.generate(tribunal_verdict=verdict)

    assert report.executive_summary["verdict"] == "INCONCLUSIVE"


def test_report_generator_empty_investigation():
    generator = ReportGenerator()
    report = generator.generate()

    assert report.report_id.startswith("rpt_default_")
    assert report.executive_summary["verdict"] == "INCONCLUSIVE"

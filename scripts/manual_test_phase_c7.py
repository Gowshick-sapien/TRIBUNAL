"""Manual Integration Test for Phase C.7 — Investigation Report & Explainability Engine.

Demonstrates complete end-to-end execution across:
Planner (C.1) -> Financial Expert (C.2) -> Customer Behaviour Expert (C.3)
 -> Evidence Graph Builder (C.4) -> Adversarial Review Engine (C.5)
 -> Tribunal Consensus Engine (C.6) -> Report Generator (C.7)
 -> InvestigationReport (Markdown, HTML, JSON).
"""

from __future__ import annotations

import os
import sys
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tribunal.adversarial.defense_agent import DefenseAgent
from tribunal.consensus.tribunal import Tribunal
from tribunal.experts.behaviour.behaviour_expert import BehaviourExpert
from tribunal.experts.financial.financial_expert import FinancialExpert
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.case_file import CaseFile
from tribunal.planner.planner import Planner
from tribunal.report.report_generator import ReportGenerator


def run_manual_test():
    print("=" * 70)
    print(" TRIBUNAL — PHASE C.7 MANUAL VERIFICATION & REPORT ENGINE TEST")
    print("=" * 70 + "\n")

    query = "Find structuring and unusual behaviour during the last month for account ACC_8000A94C0"
    print(f"[1] Executing Planner for Query: '{query}'...")
    planner = Planner()
    planning_result = planner.plan(query)
    exec_plan = planning_result.execution_plan
    print(f"    -> Intent parsed: {planning_result.investigation_plan.intent}")
    print(f"    -> Experts selected: {exec_plan.expert_sequence}\n")

    case_file = CaseFile(case_id="case_c7_manual_001")
    prosecution_cards = []

    if "financial" in exec_plan.expert_sequence:
        print("[2] Executing Financial Investigation Expert...")
        fin_df = pd.DataFrame([
            {"from_account": "ACC_8000A94C0", "to_account": "ACC_SUPPLIER_1", "amount_received": 9500.0, "receiving_currency": "USD", "payment_format": "Wire", "transaction_id": "TX_FIN_001"},
            {"from_account": "ACC_8000A94C0", "to_account": "ACC_SUPPLIER_2", "amount_received": 9800.0, "receiving_currency": "USD", "payment_format": "Wire", "transaction_id": "TX_FIN_002"},
            {"from_account": "ACC_8000A94C0", "to_account": "ACC_SUPPLIER_3", "amount_received": 9600.0, "receiving_currency": "USD", "payment_format": "Wire", "transaction_id": "TX_FIN_003"},
        ])
        fin_expert = FinancialExpert()
        res_fin = fin_expert.investigate(fin_df, case_file, exec_plan)
        prosecution_cards.extend(res_fin.cards)
        print(f"    -> Generated {len(res_fin.cards)} Financial Investigation Card(s).\n")
    else:
        print("[2] Skipping Financial Expert (not requested by ExecutionPlan).\n")

    if "behaviour" in exec_plan.expert_sequence:
        print("[3] Executing Customer Behaviour Investigation Expert...")
        beh_df = pd.DataFrame([
            {"from_account": "ACC_8000A94C0", "to_account": "ACC_COUNTERPARTY_X", "amount_received": 25000.0, "receiving_currency": "EUR", "preferred_currency": "GBP", "payment_format": "Cash", "preferred_payment_format": "ach", "baseline_daily_amount": 1000.0, "days_since_last_transaction": 120.0, "transaction_id": "TX_BEH_001"},
        ])
        beh_expert = BehaviourExpert()
        res_beh = beh_expert.investigate(beh_df, case_file, exec_plan)
        prosecution_cards.extend(res_beh.cards)
        print(f"    -> Generated {len(res_beh.cards)} Behavioural Investigation Card(s).\n")
    else:
        print("[3] Skipping Customer Behaviour Expert (not requested by ExecutionPlan).\n")

    print("[4] Executing Evidence Graph Builder (Phase C.4)...")
    builder = EvidenceGraphBuilder()
    graph = builder.build(prosecution_cards, case_file=case_file)
    print(f"    -> Prosecution EvidenceGraph built ({len(graph.nodes)} nodes, {len(graph.edges)} edges).\n")

    print("[5] Executing Adversarial Review Engine (Phase C.5)...")
    agent = DefenseAgent()
    defense_cards = agent.review(graph, case_file)
    augmented_graph = builder.augment_graph(graph, defense_cards)
    print(f"    -> Augmented EvidenceGraph built ({len(augmented_graph.nodes)} nodes, {len(augmented_graph.edges)} edges).\n")

    print("[6] Executing Tribunal Consensus & Deliberation Engine (Phase C.6)...")
    tribunal = Tribunal()
    verdict = tribunal.deliberate(augmented_graph, case_file)
    print(f"    -> Tribunal Verdict Issued: '{verdict.verdict}' (Confidence: {verdict.confidence:.4f})\n")

    print("[7] Executing Investigation Report & Explainability Engine (Phase C.7)...")
    report_generator = ReportGenerator()
    report = report_generator.generate(
        planner_context=planning_result,
        case_file=case_file,
        evidence_graph=augmented_graph,
        tribunal_verdict=verdict,
        query_text=query,
    )
    print(f"    -> InvestigationReport built: '{report.report_id}'\n")

    print("-" * 70)
    print(" REPORT SUMMARY & EXPLAINABILITY HIGHLIGHTS")
    print("-" * 70)
    print(f"  Report ID               : {report.report_id}")
    print(f"  Generated Timestamp     : {report.generated_at}")
    print(f"  Verdict Category        : {report.executive_summary['verdict']}")
    print(f"  Primary Hypothesis      : {report.executive_summary['primary_hypothesis']}")
    print(f"  Primary Support Score   : {report.executive_summary['primary_score']:.4f}")
    print(f"  Secondary Hypothesis    : {report.executive_summary['secondary_hypothesis']}")
    print(f"  Secondary Support Score : {report.executive_summary['secondary_score']:.4f}" if report.executive_summary['secondary_score'] is not None else "  Secondary Support Score : None")
    print(f"  Confidence Gap (Delta)  : {report.executive_summary['confidence_gap']:.4f}")
    print(f"  Calibrated Confidence   : {report.executive_summary['calibrated_confidence']:.4f}")
    print(f"  Risk Level              : {report.executive_summary['risk_level']}")
    print(f"  Report Markdown Size    : {len(report.markdown_content):,} bytes")
    print(f"  Report HTML Size        : {len(report.html_content):,} bytes")
    print(f"  Report JSON Payload Keys: {list(report.json_payload.keys())}\n")

    output_dir = os.path.join(PROJECT_ROOT, "tribunal", "datasets", "processed")
    os.makedirs(output_dir, exist_ok=True)
    md_path = os.path.join(output_dir, "report.md")
    html_path = os.path.join(output_dir, "report.html")
    json_path = os.path.join(output_dir, "report.json")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(report.markdown_content)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(report.html_content)
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump(report.json_payload, f, indent=2)

    print(f"    -> Saved Markdown Report : {md_path}")
    print(f"    -> Saved Standalone HTML : {html_path}")
    print(f"    -> Saved JSON Payload   : {json_path}")

    print("\n" + "=" * 70)
    print(" SUCCESS: Phase C.7 Report Engine Test & Artifact Generation Completed!")
    print("=" * 70)


if __name__ == "__main__":
    run_manual_test()

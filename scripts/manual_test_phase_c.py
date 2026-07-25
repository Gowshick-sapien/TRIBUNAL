"""Consolidated Manual Testing Protocol Script for Phase C (C.1 to C.7).

Demonstrates the complete end-to-end TRIBUNAL investigation lifecycle:
  1. Planner Framework (C.1) — Query parsing & deterministic execution planning
  2. Financial Investigation Expert (C.2) — Structuring, velocity & large transfer detectors
  3. Customer Behaviour Expert (C.3) — Baseline drift, dormancy, currency & payment format shifts
  4. Evidence Graph & Case Synthesis Engine (C.4) — Node inference & relationship linking
  5. Adversarial Review Engine (C.5) — Contradiction review & alternative explanation cards
  6. Tribunal Consensus & Deliberation Engine (C.6) — Multi-hypothesis deliberation & verdict
  7. Investigation Report & Explainability Engine (C.7) — 10-section report in Markdown, HTML, JSON
"""

from __future__ import annotations

import json
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


def run_consolidated_manual_testing():
    print("=" * 75)
    print(" TRIBUNAL — PHASE C CONSOLIDATED MANUAL TESTING & VERIFICATION PROTOCOL")
    print("=" * 75 + "\n")

    # -------------------------------------------------------------------------
    # STAGE 1: Planner Framework (Phase C.1)
    # -------------------------------------------------------------------------
    query = "Find structuring and unusual behaviour during the last month for account ACC_8000A94C0"
    print(f"[STAGE 1] Executing Planner Framework (Phase C.1)...")
    print(f"          Input Query: '{query}'")

    planner = Planner()
    planning_result = planner.plan(query)
    exec_plan = planning_result.execution_plan
    inv_plan = planning_result.investigation_plan

    print(f"          -> Parsed Intent    : {inv_plan.intent}")
    print(f"          -> Target Pattern   : {inv_plan.target_pattern}")
    print(f"          -> Target Entity    : {inv_plan.customer_id}")
    print(f"          -> Experts Selected : {exec_plan.expert_sequence}")
    print(f"          -> Assets Required  : {exec_plan.assets}")
    print(f"          -> Planner Profiling: {planning_result.metrics}\n")

    # -------------------------------------------------------------------------
    # STAGE 2: Investigation Domain Experts (Phase C.2 & Phase C.3)
    # -------------------------------------------------------------------------
    case_file = CaseFile(case_id="case_c_consolidated_001")
    prosecution_cards = []

    # Financial Expert (C.2)
    if "financial" in exec_plan.expert_sequence:
        print("[STAGE 2A] Executing Financial Investigation Expert (Phase C.2)...")
        fin_df = pd.DataFrame([
            {"from_account": "ACC_8000A94C0", "to_account": "ACC_SUPPLIER_1", "amount_received": 9500.0, "receiving_currency": "USD", "payment_format": "Wire", "transaction_id": "TX_FIN_001"},
            {"from_account": "ACC_8000A94C0", "to_account": "ACC_SUPPLIER_2", "amount_received": 9800.0, "receiving_currency": "USD", "payment_format": "Wire", "transaction_id": "TX_FIN_002"},
            {"from_account": "ACC_8000A94C0", "to_account": "ACC_SUPPLIER_3", "amount_received": 9600.0, "receiving_currency": "USD", "payment_format": "Wire", "transaction_id": "TX_FIN_003"},
        ])
        fin_expert = FinancialExpert()
        res_fin = fin_expert.investigate(fin_df, case_file, exec_plan)
        prosecution_cards.extend(res_fin.cards)
        print(f"           -> Generated {len(res_fin.cards)} Financial Investigation Card(s).")
        for card in res_fin.cards:
            print(f"              * [{card.card_id}] {card.hypothesis} (Severity: {card.severity}, Confidence: {card.confidence:.2f})")
        print("")
    else:
        print("[STAGE 2A] Skipping Financial Expert (not requested by ExecutionPlan).\n")

    # Behaviour Expert (C.3)
    if "behaviour" in exec_plan.expert_sequence:
        print("[STAGE 2B] Executing Customer Behaviour Investigation Expert (Phase C.3)...")
        beh_df = pd.DataFrame([
            {"from_account": "ACC_8000A94C0", "to_account": "ACC_COUNTERPARTY_X", "amount_received": 25000.0, "receiving_currency": "EUR", "preferred_currency": "GBP", "payment_format": "Cash", "preferred_payment_format": "ach", "baseline_daily_amount": 1000.0, "days_since_last_transaction": 120.0, "transaction_id": "TX_BEH_001"},
        ])
        beh_expert = BehaviourExpert()
        res_beh = beh_expert.investigate(beh_df, case_file, exec_plan)
        prosecution_cards.extend(res_beh.cards)
        print(f"           -> Generated {len(res_beh.cards)} Behavioural Investigation Card(s).")
        for card in res_beh.cards:
            print(f"              * [{card.card_id}] {card.hypothesis} (Severity: {card.severity}, Confidence: {card.confidence:.2f})")
        print("")
    else:
        print("[STAGE 2B] Skipping Customer Behaviour Expert (not requested by ExecutionPlan).\n")

    # -------------------------------------------------------------------------
    # STAGE 3: Evidence Graph Synthesis Engine (Phase C.4)
    # -------------------------------------------------------------------------
    print("[STAGE 3] Executing Evidence Graph & Case Synthesis Engine (Phase C.4)...")
    graph_builder = EvidenceGraphBuilder()
    prosecution_graph = graph_builder.build(prosecution_cards, case_file=case_file)
    print(f"          -> Prosecution EvidenceGraph built ({len(prosecution_graph.nodes)} nodes, {len(prosecution_graph.edges)} edges).\n")

    # -------------------------------------------------------------------------
    # STAGE 4: Adversarial Review Engine (Phase C.5)
    # -------------------------------------------------------------------------
    print("[STAGE 4] Executing Adversarial Review Engine (Phase C.5)...")
    defense_agent = DefenseAgent()
    defense_cards = defense_agent.review(prosecution_graph, case_file)
    augmented_graph = graph_builder.augment_graph(prosecution_graph, defense_cards)
    print(f"          -> Generated {len(defense_cards)} Defense Investigation Card(s).")
    print(f"          -> Augmented EvidenceGraph built ({len(augmented_graph.nodes)} nodes, {len(augmented_graph.edges)} edges).\n")

    # -------------------------------------------------------------------------
    # STAGE 5: Tribunal Consensus Engine (Phase C.6)
    # -------------------------------------------------------------------------
    print("[STAGE 5] Executing Tribunal Consensus & Deliberation Engine (Phase C.6)...")
    tribunal = Tribunal()
    verdict = tribunal.deliberate(augmented_graph, case_file)

    print("          ---------------------------------------------------")
    print("          TRIBUNAL VERDICT SUMMARY")
    print("          ---------------------------------------------------")
    print(f"            Consensus Category    : {verdict.verdict}")
    print(f"            Primary Hypothesis    : {verdict.primary_hypothesis}")
    print(f"            Primary Support Score : {verdict.primary_score:.4f}")
    print(f"            Secondary Hypothesis  : {verdict.secondary_hypothesis}")
    print(f"            Secondary Score       : {verdict.secondary_score:.4f}" if verdict.secondary_score is not None else "            Secondary Score       : None")
    print(f"            Confidence Gap (Delta): {verdict.confidence_gap:.4f}")
    print(f"            Calibrated Confidence : {verdict.confidence:.4f}")
    print(f"            Risk Level            : {verdict.risk_level}")
    print("          ---------------------------------------------------\n")

    # -------------------------------------------------------------------------
    # STAGE 6: Investigation Report & Explainability Engine (Phase C.7)
    # -------------------------------------------------------------------------
    print("[STAGE 6] Executing Investigation Report & Explainability Engine (Phase C.7)...")
    report_generator = ReportGenerator()
    report = report_generator.generate(
        planner_context=planning_result,
        case_file=case_file,
        evidence_graph=augmented_graph,
        tribunal_verdict=verdict,
        query_text=query,
    )
    print(f"          -> InvestigationReport generated successfully: '{report.report_id}'\n")

    # -------------------------------------------------------------------------
    # STAGE 7: Disk Persistence & Multi-Format Artifact Validation
    # -------------------------------------------------------------------------
    print("[STAGE 7] Persisting Multi-Format Report Artifacts...")
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
        json.dump(report.json_payload, f, indent=2)

    print(f"          -> Markdown Report : {md_path} ({len(report.markdown_content):,} bytes)")
    print(f"          -> Standalone HTML : {html_path} ({len(report.html_content):,} bytes)")
    print(f"          -> JSON Payload   : {json_path} (Keys: {list(report.json_payload.keys())})")

    print("\n" + "=" * 75)
    print(" SUCCESS: Phase C Consolidated Manual Verification Completed Successfully!")
    print("=" * 75)


if __name__ == "__main__":
    run_consolidated_manual_testing()

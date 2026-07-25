"""Manual Integration Test for Phase C.6 — Tribunal Consensus Engine.

Demonstrates complete end-to-end execution across:
Planner (C.1) -> Financial Expert (C.2) -> Customer Behaviour Expert (C.3)
 -> Evidence Graph Builder (C.4) -> Adversarial Review Engine (C.5)
 -> Tribunal Consensus Engine (C.6) -> TribunalVerdict.
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


def run_manual_test():
    print("=" * 65)
    print(" TRIBUNAL — PHASE C.6 MANUAL VERIFICATION & DELIBERATION TEST")
    print("=" * 65 + "\n")

    # 1. Execute Planner
    query = "Find structuring and unusual behaviour during the last month for account ACC_8000A94C0"
    print(f"[1] Executing Planner for Query: '{query}'...")
    planner = Planner()
    planning_result = planner.plan(query)
    exec_plan = planning_result.execution_plan
    print(f"    -> Intent parsed: {planning_result.investigation_plan.intent}")
    print(f"    -> Experts selected: {exec_plan.expert_sequence}\n")

    case_file = CaseFile(case_id="case_c6_manual_001")
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

    # 4. Evidence Graph Builder (C.4)
    print("[4] Executing Evidence Graph Builder (Phase C.4)...")
    builder = EvidenceGraphBuilder()
    graph = builder.build(prosecution_cards, case_file=case_file)
    print(f"    -> Prosecution EvidenceGraph built ({len(graph.nodes)} nodes, {len(graph.edges)} edges).\n")

    # 5. Adversarial Review Engine (C.5)
    print("[5] Executing Adversarial Review Engine (Phase C.5)...")
    agent = DefenseAgent()
    defense_cards = agent.review(graph, case_file)
    augmented_graph = builder.augment_graph(graph, defense_cards)
    print(f"    -> Augmented EvidenceGraph built ({len(augmented_graph.nodes)} nodes, {len(augmented_graph.edges)} edges).\n")

    # 6. Tribunal Consensus & Deliberation Engine (C.6)
    print("[6] Executing Tribunal Consensus & Deliberation Engine (Phase C.6)...")
    tribunal = Tribunal()
    verdict = tribunal.deliberate(augmented_graph, case_file)

    print("-" * 65)
    print(" TRIBUNAL VERDICT SUMMARY")
    print("-" * 65)
    print(f"  Verdict Category        : {verdict.verdict}")
    print(f"  Primary Hypothesis      : {verdict.primary_hypothesis}")
    print(f"  Primary Score           : {verdict.primary_score:.4f}")
    print(f"  Secondary Hypothesis    : {verdict.secondary_hypothesis}")
    print(f"  Secondary Score         : {verdict.secondary_score:.4f}" if verdict.secondary_score is not None else "  Secondary Score         : None")
    print(f"  Confidence Gap (Delta)  : {verdict.confidence_gap:.4f}")
    print(f"  Calibrated Confidence   : {verdict.confidence:.4f}")
    print(f"  Risk Level              : {verdict.risk_level}")
    print(f"  Supporting Experts      : {verdict.supporting_experts}")
    print(f"  Supporting Cards        : {verdict.supporting_cards}")

    print("\n--- REJECTED HYPOTHESES ---")
    for r in verdict.rejected_hypotheses:
        print(f"  * {r['title']} (Net Score: {r['net_support_score']:.2f}) -> {r['rejection_reason']}")

    print("\n--- PROFILED DELIBERATION TRACE ---")
    for step in verdict.deliberation_trace:
        print(f"  Step {step['step_number']} [{step['decision_id']} - {step['stage_name']} ({step['step_duration_ms']:.2f} ms)]: {step['description']}")

    print("\n" + "=" * 65)
    print(" SUCCESS: Phase C.6 Tribunal Deliberation Test Completed!")
    print("=" * 65)


if __name__ == "__main__":
    run_manual_test()

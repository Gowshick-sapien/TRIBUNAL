"""Diagnostic script to inspect confidence flow and multi-dimensional risk calibration across 5 investigation scenarios.

Diagnoses:
1. Expert confidence outputs
2. Raw support scores
3. Defense agent penalties
4. Net support scores ($S$)
5. Confidence Gap ($\Delta$)
6. Calibrated confidence ($C$)
7. Final Risk Level (CRITICAL, HIGH, MEDIUM, LOW)
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


def run_diagnostics():
    print("=" * 80)
    print(" TRIBUNAL — RISK CALIBRATION & CONFIDENCE DIAGNOSTIC SUITE")
    print("=" * 80 + "\n")

    scenarios = [
        {
            "name": "Scenario 1: High-Volume Structuring & Velocity (Critical Malicious)",
            "query": "Find structuring and unusual velocity during the last month for account ACC_CRIT_001",
            "fin_data": [
                {"from_account": "ACC_CRIT_001", "to_account": f"ACC_SUP_{i}", "amount_received": 9700.0 + i*50, "receiving_currency": "USD", "payment_format": "Wire", "transaction_id": f"TX_C1_{i}"}
                for i in range(12)
            ],
            "beh_data": [
                {"from_account": "ACC_CRIT_001", "to_account": "ACC_BEN_X", "amount_received": 50000.0, "receiving_currency": "EUR", "preferred_currency": "USD", "payment_format": "Cash", "preferred_payment_format": "ach", "baseline_daily_amount": 1000.0, "days_since_last_transaction": 180.0, "transaction_id": "TX_C1_BEH"}
            ]
        },
        {
            "name": "Scenario 2: Multi-Detector Behavioural Anomaly (High Risk)",
            "query": "Show behavioural anomalies and dormancy reactivation for account ACC_BEH_002",
            "fin_data": [],
            "beh_data": [
                {"from_account": "ACC_BEH_002", "to_account": "ACC_BEN_Y", "amount_received": 35000.0, "receiving_currency": "GBP", "preferred_currency": "USD", "payment_format": "Cash", "preferred_payment_format": "ach", "baseline_daily_amount": 800.0, "days_since_last_transaction": 150.0, "transaction_id": "TX_C2_BEH"}
            ]
        },
        {
            "name": "Scenario 3: Strong Defense / Legitimate Business Activity (Low Risk)",
            "query": "Investigate account ACC_LEGIT_003 for structuring",
            "fin_data": [
                {"from_account": "ACC_LEGIT_003", "to_account": "ACC_SUP_1", "amount_received": 450.0, "receiving_currency": "USD", "payment_format": "ACH", "transaction_id": "TX_C3_01"}
            ],
            "beh_data": []
        },
        {
            "name": "Scenario 4: Balanced Competing Evidence (Medium Risk / Inconclusive)",
            "query": "Investigate suspicious transactions for account ACC_BAL_004",
            "fin_data": [
                {"from_account": "ACC_BAL_004", "to_account": "ACC_SUP_1", "amount_received": 9500.0, "receiving_currency": "USD", "payment_format": "Wire", "transaction_id": "TX_C4_01"}
            ],
            "beh_data": [
                {"from_account": "ACC_BAL_004", "to_account": "ACC_BEN_Z", "amount_received": 2000.0, "receiving_currency": "USD", "preferred_currency": "USD", "payment_format": "ACH", "preferred_payment_format": "ach", "baseline_daily_amount": 2000.0, "days_since_last_transaction": 2.0, "transaction_id": "TX_C4_BEH"}
            ]
        },
        {
            "name": "Scenario 5: Low-Value Normal Activity (Low Risk)",
            "query": "Summarize activity for account ACC_NORM_005",
            "fin_data": [
                {"from_account": "ACC_NORM_005", "to_account": "ACC_STORE", "amount_received": 120.0, "receiving_currency": "USD", "payment_format": "ACH", "transaction_id": "TX_C5_01"}
            ],
            "beh_data": []
        }
    ]

    planner = Planner()
    fin_expert = FinancialExpert()
    beh_expert = BehaviourExpert()
    builder = EvidenceGraphBuilder()
    agent = DefenseAgent()
    tribunal = Tribunal()

    for idx, sc in enumerate(scenarios, start=1):
        print(f"--- [{idx}/5] {sc['name']} ---")
        print(f"  Query: '{sc['query']}'")
        plan_res = planner.plan(sc["query"])
        exec_plan = plan_res.execution_plan
        print(f"  Planner Intent: {plan_res.investigation_plan.intent} | Experts: {exec_plan.expert_sequence}")

        case_file = CaseFile(case_id=f"case_diag_{idx}")
        prosecution_cards = []

        if "financial" in exec_plan.expert_sequence and sc["fin_data"]:
            fin_df = pd.DataFrame(sc["fin_data"])
            res_fin = fin_expert.investigate(fin_df, case_file, exec_plan)
            prosecution_cards.extend(res_fin.cards)
            for c in res_fin.cards:
                print(f"    * Fin Card [{c.card_id}]: {c.hypothesis} (Conf: {c.confidence:.2f}, Sev: {c.severity})")

        if "behaviour" in exec_plan.expert_sequence and sc["beh_data"]:
            beh_df = pd.DataFrame(sc["beh_data"])
            res_beh = beh_expert.investigate(beh_df, case_file, exec_plan)
            prosecution_cards.extend(res_beh.cards)
            for c in res_beh.cards:
                print(f"    * Beh Card [{c.card_id}]: {c.hypothesis} (Conf: {c.confidence:.2f}, Sev: {c.severity})")

        if not prosecution_cards:
            print("    * No prosecution cards generated.")

        graph = builder.build(prosecution_cards, case_file=case_file)
        def_cards = agent.review(graph, case_file)
        aug_graph = builder.augment_graph(graph, def_cards)

        verdict = tribunal.deliberate(aug_graph, case_file)

        print(f"  ==> VERDICT CATEGORY    : {verdict.verdict}")
        print(f"  ==> PRIMARY HYPOTHESIS  : {verdict.primary_hypothesis}")
        print(f"  ==> PRIMARY NET SUPPORT : {verdict.primary_score:.4f}")
        print(f"  ==> CONFIDENCE GAP      : {verdict.confidence_gap:.4f}")
        print(f"  ==> CALIBRATED CONF.    : {verdict.confidence:.4f}")
        print(f"  ==> CALIBRATED RISK     : {verdict.risk_level}")
        print("-" * 80 + "\n")


if __name__ == "__main__":
    run_diagnostics()

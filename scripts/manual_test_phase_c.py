"""Manual testing script for Phase C — End-to-End verification of Planner, Financial Expert, Behaviour Expert, Evidence Graph Engine, and Adversarial Review Engine (Phase C.5)."""

from pathlib import Path
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from tribunal.adversarial.defense_agent import DefenseAgent
from tribunal.experts.behaviour.behaviour_expert import BehaviourExpert
from tribunal.experts.financial.financial_expert import FinancialExpert
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.case_file import CaseFile
from tribunal.models.execution_plan import ExecutionPlan
from tribunal.planner.planner import Planner


def run_manual_testing():
    print("=================================================================")
    print(" TRIBUNAL — PHASE C MANUAL VERIFICATION & INTEGRATION TEST")
    print("=================================================================\n")

    # 1. Test Planner (Phase C.1)
    planner = Planner()
    query = "Find structuring and unusual behaviour during the last month for account ACC_8000A94C0"
    print(f"[1] Executing Planner for Query: '{query}'...")
    planning_result = planner.plan(query)

    exec_plan = planning_result.execution_plan
    print(f"    -> Intent parsed: {planning_result.investigation_plan.intent}")
    print(f"    -> Experts selected: {exec_plan.expert_sequence}")
    print(f"    -> Execution Plan version: {exec_plan.planner_version} (schema {exec_plan.schema_version})")
    print(f"    -> Planner profiling metrics: {planning_result.metrics}\n")

    # 2. Prepare Sample Financial & Behavioural Transactions for ACC_8000A94C0
    fin_df = pd.DataFrame([
        {
            "from_account": "ACC_8000A94C0",
            "to_account": "ACC_SUPPLIER_1",
            "amount_received": 9500.0,
            "receiving_currency": "USD",
            "payment_format": "Wire",
            "transaction_id": "TX_FIN_001",
        },
        {
            "from_account": "ACC_8000A94C0",
            "to_account": "ACC_SUPPLIER_2",
            "amount_received": 9800.0,
            "receiving_currency": "USD",
            "payment_format": "Wire",
            "transaction_id": "TX_FIN_002",
        },
        {
            "from_account": "ACC_8000A94C0",
            "to_account": "ACC_SUPPLIER_3",
            "amount_received": 9600.0,
            "receiving_currency": "USD",
            "payment_format": "Wire",
            "transaction_id": "TX_FIN_003",
        },
    ])

    beh_df = pd.DataFrame([
        {
            "from_account": "ACC_8000A94C0",
            "to_account": "ACC_COUNTERPARTY_X",
            "amount_received": 25000.0,
            "receiving_currency": "EUR",
            "preferred_currency": "GBP",
            "payment_format": "Cash",
            "preferred_payment_format": "ach",
            "baseline_daily_amount": 1000.0,
            "days_since_last_transaction": 120.0,
            "transaction_id": "TX_BEH_001",
        },
    ])

    case_file = CaseFile(case_id="case_manual_verification_001")

    # 3. Test Financial Expert (Phase C.2)
    unfiltered_plan = ExecutionPlan(
        run_eda=True,
        expert_sequence=["financial", "behaviour"],
        filters={},
        rationale="Manual testing execution",
    )

    print("[2] Executing Financial Investigation Expert...")
    fin_expert = FinancialExpert()
    res_fin = fin_expert.investigate(fin_df, case_file, unfiltered_plan)
    print(f"    -> Generated {len(res_fin.cards)} Financial Investigation Card(s).")
    for card in res_fin.cards:
        print(f"       * Card ID: {card.card_id} | Severity: {card.severity} | Confidence: {card.confidence}")
        print(f"         Hypothesis: {card.hypothesis}")
        print(f"         Provenance: {card.provenance}\n")

    # 4. Test Behaviour Expert (Phase C.3)
    print("[3] Executing Customer Behaviour Investigation Expert...")
    beh_expert = BehaviourExpert()
    res_beh = beh_expert.investigate(beh_df, case_file, unfiltered_plan)
    print(f"    -> Generated {len(res_beh.cards)} Behavioural Investigation Card(s).")
    for card in res_beh.cards:
        print(f"       * Card ID: {card.card_id} | Severity: {card.severity} | Confidence: {card.confidence}")
        print(f"         Hypothesis: {card.hypothesis}")
        print(f"         Supporting Metrics: {card.supporting_metrics}\n")

    # 5. Test Evidence Graph Builder (Phase C.4)
    print("[4] Executing Evidence Graph Builder (Phase C.4)...")
    builder = EvidenceGraphBuilder()
    prosecution_cards = res_fin.cards + res_beh.cards
    graph = builder.build(prosecution_cards, case_file=case_file, execution_plan=unfiltered_plan)

    print(f"    -> Prosecution EvidenceGraph built ({len(graph.nodes)} nodes, {len(graph.edges)} edges).")

    # 6. Test Adversarial Review Engine (Phase C.5)
    print("\n[5] Executing Adversarial Review Engine (Phase C.5)...")
    defense_agent = DefenseAgent()
    defense_cards = defense_agent.review(graph, case_file, unfiltered_plan)
    print(f"    -> Generated {len(defense_cards)} Defense Investigation Card(s).")
    for def_card in defense_cards:
        print(f"       * Card ID: {def_card.card_id} | Type: {def_card.provenance.get('defense_type')} | Confidence: {def_card.confidence}")
        print(f"         Hypothesis: {def_card.hypothesis}")
        print(f"         Supporting Features: {def_card.supporting_features}\n")

    # Augment graph with defense cards
    augmented_graph = builder.augment_graph(graph, defense_cards)

    print("-----------------------------------------------------------------")
    print(" AUGMENTED EVIDENCE GRAPH TOPOLOGY METRICS (C.4 + C.5)")
    print("-----------------------------------------------------------------")
    for k, v in augmented_graph.metrics.items():
        print(f"  {k:<25}: {v}")
    print("-----------------------------------------------------------------\n")

    # Print Nodes & Edges summary
    print("--- GRAPH NODES ---")
    for node in augmented_graph.nodes:
        print(f"  [{node.node_type.upper():<10}] ID: {node.node_id:<25} | Expert: {node.expert:<10} | Label: {node.label}")

    print("\n--- GRAPH EDGES ---")
    for edge in augmented_graph.edges:
        print(f"  [{edge.relationship:<15}] {edge.source} ===> {edge.target} (Weight: {edge.weight})")

    # 7. Test Persistence & Round-Trip Deserialization
    output_path = Path("tribunal/datasets/processed/evidence_graph.gpickle")
    print(f"\n[6] Persisting Augmented EvidenceGraph to '{output_path}'...")
    builder.save(augmented_graph, output_path)

    loaded_graph = builder.load(output_path)
    print(f"    -> Loaded EvidenceGraph from disk successfully ({loaded_graph.metrics['node_count']} nodes, {loaded_graph.metrics['edge_count']} edges).")

    print("\n=================================================================")
    print(" SUCCESS: Phase C End-to-End Manual Testing Completed!")
    print("=================================================================")


if __name__ == "__main__":
    run_manual_testing()

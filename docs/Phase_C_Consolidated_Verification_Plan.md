# Phase C — Consolidated Verification Plan & Matrix

This document provides the consolidated verification plan, test strategy, automated test matrix, and manual verification protocols for Phase C (**Query Understanding, Planning, Domain Experts, Evidence Graph & Adversarial Review Engine**) built so far (Phase C.1, Phase C.2, Phase C.3, Phase C.4, and Phase C.5).

---

## 1. Scope & System Architecture

```text
User Query
      │
      ▼
Planner (C.1)
  ├── LLMClient (Ollama + Mock / Fallback)
  ├── QueryParser (Validation & Normalization)
  └── ExecutionPlanner (Deterministic Matrix)
      │
      ▼
PlanningResult (InvestigationPlan + ExecutionPlan: v1.0/C.1 + Metrics)
      │
      ├────────────────────────────────────────┐
      ▼                                        ▼
Financial Investigation Expert (C.2)    Customer Behaviour Investigation Expert (C.3)
  [BaseInvestigationExpert Pipeline]       [BaseInvestigationExpert Pipeline]
  ├── CandidateSelector                    ├── CandidateSelector
  ├── Financial Detectors                  ├── Behavioural Detectors
  │   (Structuring, Velocity,               │   (Drift, Dormancy, Spending, Currency,
  │    Large Transfer, Frequency)           │    Payment Format, Counterparty)
  ├── Post-Processing Hook                 ├── Post-Processing Hook (_post_process_findings)
  ├── ConfidenceAggregator (1 - Π(1 - s_i)) ├── ConfidenceAggregator (1 - Π(1 - s_i))
  └── CardBuilder                          └── CardBuilder
      │                                        │
      └───────────────────┬────────────────────┘
                          ▼
             Investigation Cards & Case File
      (Official PatternFinding & MetricEvidence)
                          │
                          ▼
        Evidence Graph & Case Synthesis Engine (C.4)
          ├── GraphValidator (Integrity & Provenance Check)
          ├── EvidenceMerger (Same-Expert Deduplication)
          ├── EvidenceLinker (Node & Relationship Inference)
          │   ├── Account Nodes, Card Nodes, Hypothesis Nodes
          │   └── Edges: HAS_EVIDENCE, SUPPORTS, CORROBORATES,
          │              CONTRADICTS, DERIVED_FROM, SAME_ACCOUNT
          ├── GraphMetrics (Structural Topology Analytics)
          └── EvidenceGraph (networkx.DiGraph + Persistence)
                          │
                          ▼
           Adversarial Review Engine (C.5)
             ├── EvidenceReviewer (Traverse graph, snapshot metadata & extract ReviewContext)
             ├── ContradictionDetector (Identify conflicting expert signals)
             ├── AlternativeHypothesisGenerator (AlternativeExplanation abstraction)
             ├── EvidenceStrengthAnalyzer (Evaluate corroboration & provenance depth)
             ├── UncertaintyEstimator (Measure evidence sparsity & single-expert risk)
             └── RebuttalBuilder & ConfidenceAdjuster (Emit Defense Cards supporting Legitimate Business Activity)
                          │
                          ▼
          Augmented Evidence Graph (C.4 + C.5)
      (Financial Cards + Behaviour Cards + Defense Cards -> Legitimate Business Activity)
```

---

## 2. Automated Test Suite Execution

Run the complete Phase C test suite via Pytest:

```bash
# Run all unit tests across Phase C
pytest tribunal/tests/ -v
```

### Current Status
* **Total Tests Executed**: 87
* **Pass Rate**: 100% (87 passed, 0 failed)
* **Execution Time**: ~22.6 seconds

---

## 3. Component Verification Matrices

### Phase C.1 — Planner Framework Verification Matrix

| Query Description | User Query Text | Expected Intent | Required Assets | Expert Sequence | Tribunal Req. | Output Format |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Pattern Detection** | *"Find structuring during the last month"* | `pattern_detection` | `[feature_store]` | `[financial, behaviour]` | `True` | `investigation_report` |
| **Behaviour Analysis** | *"Show behavioural anomalies"* | `behaviour_analysis` | `[feature_store]` | `[behaviour]` | `True` | `investigation_report` |
| **Customer Lookup** | *"Investigate account 8000A94C0"* | `customer_lookup` | `[feature_store, transaction_network]` | `[financial, behaviour]` | `True` | `investigation_report` |
| **EDA Request** | *"Show payment format distribution"* | `eda_request` | `[dataset]` | `[]` *(EDA Tool)* | `False` | `summary` |
| **Case Summary** | *"Summarize investigation"* | `case_summary` | `[case_file]` | `[]` | `False` | `summary` |

---

### Phase C.2 — Financial Investigation Expert Verification Matrix

| Scenario | Input Condition | Target Pattern / Trigger | Expected Output Cards | Min. Confidence | Assigned Severity | Required Provenance / Metrics |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Normal Account** | Low amount ($100–$150) regular txns | None | 0 cards | 0.00 | None | N/A |
| **Known Structuring** | Multiple deposits ($9,500–$9,900) near $10,000 | `structuring` | 1 card | >= 0.75 | `HIGH` / `CRITICAL` | `threshold_proximity` > 0.90, `transaction_ids` tracked |
| **Velocity Spike** | 10 rapid txns in 1 day | `velocity` | 1 card | >= 0.60 | `MEDIUM` / `HIGH` | `velocity_score`, `daily_velocity`, `burst_score` |
| **Large Transfer Outlier** | Single transfer of $150,000 | `large_transfer` | 1 card | >= 0.60 | `MEDIUM` / `HIGH` | `max_transaction_amount`, `cutoff_threshold` |
| **Mixed Patterns** | Structuring + high velocity | `structuring` + `velocity` | 1 combined card | >= 0.90 | `CRITICAL` | `detectors: ["StructuringDetector", "VelocityDetector"]` |
| **Empty Dataset** | 0 transactions | None | 0 cards | 0.00 | None | N/A |

---

### Phase C.3 — Customer Behaviour Investigation Expert Verification Matrix

| Scenario | Input Condition | Target Pattern | Output Cards | Min. Confidence | Assigned Severity | Required Provenance / Metrics |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Normal Account** | Stable historical baseline | None | 0 cards | 0.00 | None | N/A |
| **Dormant Reactivation** | Reactivated after 120-day gap | `dormancy_reactivation` | 1 card | >= 0.80 | `HIGH` / `CRITICAL` | `days_since_last_transaction: 120.0` |
| **Spending Shift** | $100 mean -> $30,000 transaction | `spending_pattern_change` | 1 card | >= 0.65 | `MEDIUM` / `HIGH` | `amount_spike_ratio`, `max_transaction_amount` |
| **Unexpected Currency** | Preferred GBP -> Used EUR/USD | `currency_change` | 1 card | >= 0.75 | `HIGH` / `CRITICAL` | `currency_switch_frequency`, `preferred_currency` |
| **Payment Format Shift** | Preferred ACH -> Used Wire/Cash | `payment_pattern_change` | 1 card | >= 0.70 | `MEDIUM` / `HIGH` | `format_switch_count`, `preferred_payment_format` |
| **Counterparty Expansion**| 6 new recipient accounts | `counterparty_expansion` | 1 card | >= 0.60 | `MEDIUM` / `HIGH` | `unique_counterparties: 6.0`, `fan_out: 6.0` |

---

### Phase C.4 — Evidence Graph Engine Verification Matrix

| Scenario | Input Condition | Expected Graph Nodes | Expected Relationships | Target Metrics |
| :--- | :--- | :--- | :--- | :--- |
| **Single Card** | 1 Financial Card | 3 Nodes (`Account`, `Card`, `Hypothesis`) | `HAS_EVIDENCE`, `SUPPORTS`, `DERIVED_FROM` | 3 nodes, 3 edges, 1 component |
| **Multi-Expert Corroboration** | Financial + Behaviour cards for same account & hypothesis | 4 Nodes (`Account`, `FinCard`, `BehCard`, `Hypothesis`) | `CORROBORATES` x1 | 4 nodes, 7 edges, 1 component |
| **Unrelated Accounts** | 2 cards targeting distinct accounts | 6 Nodes | Disconnected subgraphs | 6 nodes, 6 edges, 2 components |

---

### Phase C.5 — Adversarial Review Engine Verification Matrix

| Scenario | Input Evidence Graph | Expected Defense Output | Target Normalized Hypothesis | Target Graph Topology |
| :--- | :--- | :--- | :--- | :--- |
| **Multiple Alternative Explanations** | Payroll, Merchant Settlement, Tax Season | 3 Defense cards pointing to normalized top hypothesis | `Legitimate Business Activity for Account {id}` | 3 Defense Cards support 1 Hypothesis node |
| **ReviewContext Snapshot Auditability** | Evidence Graph input | Snapshot ID, timestamp, and review version captured | `ReviewContext(graph_snapshot_id, review_timestamp, review_version="C.5")` | Audit lineage captured |
| **Weak Single-Expert Evidence** | Single financial card (confidence < 0.65) | Defense card highlighting weak support | `Weak Single-Expert Evidence for Card {id}` | Defense card challenges weak card |
| **Contradictory Findings** | Structuring card vs Normal Behaviour baseline | Defense card highlighting expert conflict | `Contradictory Expert Findings for Account {id}` | Defense card identifies conflict |

---

## 4. Consolidated Manual Testing Protocols (Phase C)

This section provides the complete step-by-step manual testing protocols for verifying Phase C components both interactively in Python and via automated CLI integration scripts.

---

### Protocol 1 — Interactive Python REPL Step-by-Step Manual Verification

To test Phase C components manually step-by-step in an interactive Python session:

#### Step 1.1: Test Planner (Phase C.1)
```python
from tribunal.planner.planner import Planner

planner = Planner()
res = planner.plan("Investigate account ACC_8000A94C0 for structuring and velocity")

print(f"Parsed Intent: {res.investigation_plan.intent}")
print(f"Expert Sequence: {res.execution_plan.expert_sequence}")
print(f"Profiling Metrics: {res.metrics}")
```

#### Step 1.2: Test Financial Expert (Phase C.2)
```python
import pandas as pd
from tribunal.experts.financial.financial_expert import FinancialExpert
from tribunal.models.case_file import CaseFile
from tribunal.models.execution_plan import ExecutionPlan

fin_df = pd.DataFrame([
    {"from_account": "ACC_8000A94C0", "to_account": "ACC_SUPPLIER_1", "amount_received": 9500.0, "receiving_currency": "USD", "payment_format": "Wire", "transaction_id": "TX_FIN_001"},
    {"from_account": "ACC_8000A94C0", "to_account": "ACC_SUPPLIER_2", "amount_received": 9800.0, "receiving_currency": "USD", "payment_format": "Wire", "transaction_id": "TX_FIN_002"},
    {"from_account": "ACC_8000A94C0", "to_account": "ACC_SUPPLIER_3", "amount_received": 9600.0, "receiving_currency": "USD", "payment_format": "Wire", "transaction_id": "TX_FIN_003"},
])
case_file = CaseFile(case_id="case_manual_001")
plan = res.execution_plan  # or ExecutionPlan(run_eda=True, expert_sequence=["financial", "behaviour"], filters={}, rationale="Manual test")

fin_expert = FinancialExpert()
res_fin = fin_expert.investigate(fin_df, case_file, plan)
print(f"Financial Cards Generated: {len(res_fin.cards)}")
```

#### Step 1.3: Test Customer Behaviour Expert (Phase C.3)
```python
from tribunal.experts.behaviour.behaviour_expert import BehaviourExpert

beh_df = pd.DataFrame([
    {"from_account": "ACC_8000A94C0", "to_account": "ACC_CP_X", "amount_received": 25000.0, "receiving_currency": "EUR", "preferred_currency": "GBP", "payment_format": "Cash", "preferred_payment_format": "ach", "baseline_daily_amount": 1000.0, "days_since_last_transaction": 120.0, "transaction_id": "TX_BEH_001"},
])

beh_expert = BehaviourExpert()
res_beh = beh_expert.investigate(beh_df, case_file, plan)
print(f"Behavioural Cards Generated: {len(res_beh.cards)}")
```

#### Step 1.4: Test Evidence Graph Construction (Phase C.4)
```python
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder

builder = EvidenceGraphBuilder()
prosecution_cards = res_fin.cards + res_beh.cards
graph = builder.build(prosecution_cards, case_file=case_file)

print(f"EvidenceGraph Nodes: {len(graph.nodes)}, Edges: {len(graph.edges)}")
print(f"Graph Metrics: {graph.metrics}")
```

#### Step 1.5: Test Adversarial Review Engine & Graph Augmentation (Phase C.5)
```python
from tribunal.adversarial.defense_agent import DefenseAgent

agent = DefenseAgent()
defense_cards = agent.review(graph, case_file)
print(f"Defense Cards Generated: {len(defense_cards)}")

augmented_graph = builder.augment_graph(graph, defense_cards)
print(f"Augmented Graph Nodes: {len(augmented_graph.nodes)}, Edges: {len(augmented_graph.edges)}")
```

#### Step 1.6: Test Evidence Graph Persistence & Round-Trip Deserialization
```python
output_path = "tribunal/datasets/processed/evidence_graph.gpickle"
builder.save(augmented_graph, output_path)

loaded_graph = builder.load(output_path)
assert loaded_graph.metrics["node_count"] == len(augmented_graph.nodes)
print(f"Graph successfully persisted and reloaded ({loaded_graph.metrics['node_count']} nodes).")
```

---

### Protocol 2 — End-to-End Consolidated CLI Script Execution

To run the complete Phase C end-to-end integration pipeline from the terminal/PowerShell:

```bash
# Execute consolidated manual test script
python scripts/manual_test_phase_c.py
# or
python -m scripts.manual_test_phase_c
```

#### Verified Terminal Output
```text
=================================================================
 TRIBUNAL — PHASE C MANUAL VERIFICATION & INTEGRATION TEST
=================================================================

[1] Executing Planner for Query: 'Find structuring and unusual behaviour during the last month for account ACC_8000A94C0'...
    -> Intent parsed: behaviour_analysis
    -> Experts selected: ['behaviour']
    -> Execution Plan version: C.1 (schema 1.0)
    -> Planner profiling metrics: {'llm_ms': 4133.2, 'parser_ms': 0.26, 'planner_ms': 0.01, 'total_ms': 4133.6}

[2] Executing Financial Investigation Expert...
    -> Generated 1 Financial Investigation Card(s).
       * Card ID: card_fin_001_d937f3 | Severity: CRITICAL | Confidence: 0.98
         Hypothesis: Possible Structuring Activity for Account ACC_8000A94C0
         Provenance: {'detectors': ['StructuringDetector'], 'transaction_ids': ['TX_FIN_001', 'TX_FIN_002', 'TX_FIN_003'], 'feature_store_rows': [0, 1, 2]}

[3] Executing Customer Behaviour Investigation Expert...
    -> Generated 1 Behavioural Investigation Card(s).
       * Card ID: card_beh_001_cdd543 | Severity: CRITICAL | Confidence: 1.0
         Hypothesis: Multiple Behavioural Anomalies (Behaviour Drift, Dormancy Reactivation, Currency Change, Payment Pattern Change) for Account ACC_8000A94C0

[4] Executing Evidence Graph Builder (Phase C.4)...
    -> Prosecution EvidenceGraph built (5 nodes, 7 edges).

[5] Executing Adversarial Review Engine (Phase C.5)...
    -> Generated 3 Defense Investigation Card(s).
       * Card ID: card_def_fe697f | Type: alternative_explanation | Confidence: 0.476
         Hypothesis: Legitimate Business Activity for Account ACC_8000A94C0
         Supporting Features: ['Routine Business Payroll & Invoice Batch Settlement', 'batch_payment_pattern', 'recurring_monthly_schedule', 'business_account_profile']

       * Card ID: card_def_dd436c | Type: alternative_explanation | Confidence: 0.465
         Hypothesis: Legitimate Business Activity for Account ACC_8000A94C0

       * Card ID: card_def_0a7e77 | Type: alternative_explanation | Confidence: 0.44
         Hypothesis: Legitimate Business Activity for Account ACC_8000A94C0

-----------------------------------------------------------------
 AUGMENTED EVIDENCE GRAPH TOPOLOGY METRICS (C.4 + C.5)
-----------------------------------------------------------------
  node_count               : 9
  edge_count               : 16
  connected_components     : 1
  support_edges            : 5
  corroboration_edges      : 0
  contradiction_edges      : 0
  average_confidence       : 0.7574
  graph_density            : 0.2222
-----------------------------------------------------------------

--- GRAPH NODES ---
  [ACCOUNT   ] ID: acc_ACC_8000A94C0         | Expert: system     | Label: Account ACC_8000A94C0
  [CARD      ] ID: card_fin_001_d937f3       | Expert: financial  | Label: Financial Card: Possible Structuring Activity 
  [HYPOTHESIS] ID: hyp_possible_structuring_activity_for_account_acc_8000a94c0_ACC_8000A94C0 | Expert: financial  | Label: Possible Structuring Activity for Account ACC_8000A94C0
  [CARD      ] ID: card_beh_001_cdd543       | Expert: behaviour  | Label: Behaviour Card: Multiple Behavioural Anomalies
  [HYPOTHESIS] ID: hyp_multiple_behavioural_anomalies_(behaviour_drift,_dormancy_reactivation,_currency_change,_payment_pattern_change)_for_account_acc_8000a94c0_ACC_8000A94C0 | Expert: behaviour  | Label: Multiple Behavioural Anomalies (Behaviour Drift, Dormancy Reactivation, Currency Change, Payment Pattern Change) for Account ACC_8000A94C0
  [CARD      ] ID: card_def_fe697f           | Expert: defense    | Label: Defense Card: Legitimate Business Activity f
  [HYPOTHESIS] ID: hyp_legitimate_business_activity_for_account_acc_8000a94c0_ACC_8000A94C0 | Expert: defense    | Label: Legitimate Business Activity for Account ACC_8000A94C0
  [CARD      ] ID: card_def_dd436c           | Expert: defense    | Label: Defense Card: Legitimate Business Activity f
  [CARD      ] ID: card_def_0a7e77           | Expert: defense    | Label: Defense Card: Legitimate Business Activity f

--- GRAPH EDGES ---
  [HAS_EVIDENCE   ] acc_ACC_8000A94C0 ===> card_fin_001_d937f3 (Weight: 1.0)
  [SUPPORTS       ] card_fin_001_d937f3 ===> hyp_possible_structuring_activity_for_account_acc_8000a94c0_ACC_8000A94C0 (Weight: 0.98)
  [DERIVED_FROM   ] card_fin_001_d937f3 ===> acc_ACC_8000A94C0 (Weight: 1.0)
  [HAS_EVIDENCE   ] acc_ACC_8000A94C0 ===> card_beh_001_cdd543 (Weight: 1.0)
  [SUPPORTS       ] card_beh_001_cdd543 ===> hyp_multiple_behavioural_anomalies_(behaviour_drift,_dormancy_reactivation,_currency_change,_payment_pattern_change)_for_account_acc_8000a94c0_ACC_8000A94C0 (Weight: 1.0)
  [DERIVED_FROM   ] card_beh_001_cdd543 ===> acc_ACC_8000A94C0 (Weight: 1.0)
  [SAME_ACCOUNT   ] card_fin_001_d937f3 ===> card_beh_001_cdd543 (Weight: 0.5)
  [HAS_EVIDENCE   ] acc_ACC_8000A94C0 ===> card_def_fe697f (Weight: 1.0)
  [SUPPORTS       ] card_def_fe697f ===> hyp_legitimate_business_activity_for_account_acc_8000a94c0_ACC_8000A94C0 (Weight: 0.476)
  [DERIVED_FROM   ] card_def_fe697f ===> acc_ACC_8000A94C0 (Weight: 1.0)
  [HAS_EVIDENCE   ] acc_ACC_8000A94C0 ===> card_def_dd436c (Weight: 1.0)
  [SUPPORTS       ] card_def_dd436c ===> hyp_legitimate_business_activity_for_account_acc_8000a94c0_ACC_8000A94C0 (Weight: 0.465)
  [DERIVED_FROM   ] card_def_dd436c ===> acc_ACC_8000A94C0 (Weight: 1.0)
  [HAS_EVIDENCE   ] acc_ACC_8000A94C0 ===> card_def_0a7e77 (Weight: 1.0)
  [SUPPORTS       ] card_def_0a7e77 ===> hyp_legitimate_business_activity_for_account_acc_8000a94c0_ACC_8000A94C0 (Weight: 0.44)
  [DERIVED_FROM   ] card_def_0a7e77 ===> acc_ACC_8000A94C0 (Weight: 1.0)

[6] Persisting Augmented EvidenceGraph to 'tribunal\datasets\processed\evidence_graph.gpickle'...
    -> Loaded EvidenceGraph from disk successfully (9 nodes, 16 edges).

=================================================================
 SUCCESS: Phase C End-to-End Manual Testing Completed!
=================================================================
```

---

## 5. Test File Mapping (87 Unit Tests)

| Component | Test File Location | Target Functionality Verified |
| :--- | :--- | :--- |
| **Shared Models** | [`test_data_and_graph.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_data_and_graph.py) | Dataclass contracts, `PatternFinding`, `MetricEvidence` |
| **Planner Constants** | [`test_planner_constants.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_planner_constants.py) | `SUPPORTED_INTENTS`, `PATTERNS`, `OUTPUTS`, `EXPERTS`, `ASSETS` |
| **LLM Client Interface** | [`test_llm_client.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_llm_client.py) | Mock caller execution, empty query validation, fallback handling |
| **Query Parser** | [`test_query_parser.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_query_parser.py) | JSON parsing, markdown codeblocks, schema validation |
| **Execution Planner** | [`test_execution_planner.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_execution_planner.py) | Deterministic mapping across 6 core intents |
| **Planner Orchestrator** | [`test_planner.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_planner.py) | End-to-end planning, `PlanningResult`, profiling metrics |
| **Financial Candidate Selector**| [`test_candidate_selector.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_candidate_selector.py) | Entity filtering, currency/format filters |
| **Structuring Detector** | [`test_structuring_detector.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_structuring_detector.py) | Near-threshold proximity ($8k-$10k) and scoring |
| **Velocity Detector** | [`test_velocity_detector.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_velocity_detector.py) | Burst score and daily velocity calculation |
| **Large Transfer Detector** | [`test_large_transfer_detector.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_large_transfer_detector.py) | Outlier detection |
| **Frequency Detector** | [`test_frequency_detector.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_frequency_detector.py) | Frequency spike detection |
| **Financial Confidence** | [`test_confidence.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_confidence.py) | Probabilistic formula ($1 - \prod(1 - s_i)$), severity mapping |
| **Financial Expert Pipeline**| [`test_financial_expert.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_financial_expert.py) | 5-stage pipeline, `BaseInvestigationExpert`, card generation |
| **Behaviour Candidate Selector**| [`test_candidate_selector_behaviour.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_candidate_selector_behaviour.py) | Behavioural candidate filtering |
| **Behaviour Drift Detector** | [`test_behaviour_drift_detector.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_behaviour_drift_detector.py) | Historical baseline drift detection |
| **Dormancy Detector** | [`test_dormancy_detector.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_dormancy_detector.py) | Inactive account reactivation detection |
| **Spending Pattern Detector**| [`test_spending_pattern_detector.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_spending_pattern_detector.py) | Spending amount distribution shift |
| **Currency Change Detector** | [`test_currency_change_detector.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_currency_change_detector.py) | Unexpected currency switch |
| **Payment Pattern Detector** | [`test_payment_pattern_detector.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_payment_pattern_detector.py) | Payment format switch (ACH to Wire/Cash) |
| **Counterparty Detector** | [`test_counterparty_detector.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_counterparty_detector.py) | Counterparty network expansion |
| **Behaviour Confidence** | [`test_behaviour_confidence.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_behaviour_confidence.py) | Behavioural score aggregation & severity mapping |
| **Behaviour Expert Pipeline**| [`test_behaviour_expert.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_behaviour_expert.py) | E2E Customer Behaviour Expert pipeline verification |
| **Provenance Manager** | [`test_provenance_manager.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_provenance_manager.py) | Lineage validation and provenance merging |
| **Graph Validator** | [`test_graph_validator.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_graph_validator.py) | Card completeness & graph structural integrity |
| **Evidence Merger** | [`test_evidence_merger.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_evidence_merger.py) | Same-expert card deduplication |
| **Evidence Linker** | [`test_evidence_linker.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_evidence_linker.py) | Node generation & relationship inference |
| **Evidence Graph Builder** | [`test_evidence_graph_builder.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_evidence_graph_builder.py) | E2E EvidenceGraph construction, multi-expert corroboration & metrics calculation |
| **Evidence Reviewer** | [`test_evidence_reviewer.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_evidence_reviewer.py) | Graph traversal, snapshot metadata (`graph_snapshot_id`, `review_timestamp`, `review_version="C.5"`) |
| **Contradiction Detector** | [`test_contradiction_detector.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_contradiction_detector.py) | Conflicting expert findings detection |
| **Alternative Hypothesis** | [`test_alternative_hypothesis.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_alternative_hypothesis.py) | `AlternativeExplanation` abstraction and `top_level_hypothesis` normalization |
| **Strength Analyzer** | [`test_strength_analyzer.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_strength_analyzer.py) | Evidence strength scoring and provenance completeness evaluation |
| **Uncertainty Estimator** | [`test_uncertainty.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_uncertainty.py) | Uncertainty score calculation across single vs. multi-expert graphs |
| **Rebuttal Builder** | [`test_rebuttal_builder.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_rebuttal_builder.py) | Construction of Defense Cards mapping to normalized top-level hypothesis |
| **Defense Agent Pipeline** | [`test_defense_agent.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_defense_agent.py) | E2E Adversarial Review Engine review and EvidenceGraph topology augmentation |

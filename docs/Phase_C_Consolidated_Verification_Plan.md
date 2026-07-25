# Phase C — Consolidated Verification Plan & Manual Testing Protocols

This document provides the consolidated verification plan, automated test matrices, and step-by-step manual testing protocols for Phase C (**Query Understanding, Planning, Domain Experts, Evidence Graph, Adversarial Review Engine, Tribunal Consensus Engine, and Investigation Report & Explainability Engine**) — covering Phase C.1 through Phase C.7.

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
                          │
                          ▼
       Tribunal Consensus & Deliberation Engine (C.6)
         ├── Stage 1: Hypothesis Extractor (Extract candidate hypotheses & cards)
         ├── Stage 2: Evidence Weigher (Calculate raw support score per hypothesis)
         ├── Stage 3: Contradiction Resolver (Calculate Net Support Strength $N_h$)
         ├── Stage 4: Consensus Engine (Rank Primary vs Secondary hypotheses & Delta gap)
         ├── Stage 5: Confidence Calibrator (Calibrate confidence against risk & uncertainty)
         └── Stage 6: Verdict Builder & Trace (Assemble TribunalVerdict with decision_id & ms timing)
                          │
                          ▼
                   TribunalVerdict
  (PrimaryHypothesis, PrimaryScore, SecondaryHypothesis, SecondaryScore, ConfidenceGap, DeliberationTrace)
                          │
                          ▼
       Investigation Report & Explainability Engine (C.7)
         ├── Section Projection Pipeline (10 Architectural Projection Sections)
         ├── ExplainabilityEngine (Metric-to-Natural-Language Translation)
         ├── Renderers (Markdown, Standalone HTML, Structured JSON)
         └── ReportValidator (Quality & Completeness Enforcement)
                          │
                          ▼
                 InvestigationReport
 (Markdown Document, Interactive HTML Webpage, API JSON Payload)
```

---

## 2. Consolidated Manual Testing Protocols (Phase C.1 to C.7)

### Protocol 1 — Step-by-Step Interactive Python REPL Protocol

Execute the full Phase C lifecycle manually step-by-step in an interactive Python shell (`python`):

```python
import pandas as pd
from tribunal.planner.planner import Planner
from tribunal.experts.financial.financial_expert import FinancialExpert
from tribunal.experts.behaviour.behaviour_expert import BehaviourExpert
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.adversarial.defense_agent import DefenseAgent
from tribunal.consensus.tribunal import Tribunal
from tribunal.report.report_generator import ReportGenerator
from tribunal.models.case_file import CaseFile

# Step 1: Execute Planner Framework (Phase C.1)
query = "Find structuring and unusual behaviour during the last month for account ACC_8000A94C0"
planner = Planner()
planning_result = planner.plan(query)
exec_plan = planning_result.execution_plan

print("Parsed Intent :", planning_result.investigation_plan.intent)
print("Experts Selected:", exec_plan.expert_sequence)

# Step 2: Initialize CaseFile & Conditionally Execute Domain Experts (Phase C.2 & C.3)
case_file = CaseFile(case_id="case_manual_repl_001")
prosecution_cards = []

if "financial" in exec_plan.expert_sequence:
    fin_df = pd.DataFrame([
        {"from_account": "ACC_8000A94C0", "to_account": "ACC_SUPPLIER_1", "amount_received": 9500.0, "receiving_currency": "USD", "payment_format": "Wire", "transaction_id": "TX_FIN_001"},
        {"from_account": "ACC_8000A94C0", "to_account": "ACC_SUPPLIER_2", "amount_received": 9800.0, "receiving_currency": "USD", "payment_format": "Wire", "transaction_id": "TX_FIN_002"},
        {"from_account": "ACC_8000A94C0", "to_account": "ACC_SUPPLIER_3", "amount_received": 9600.0, "receiving_currency": "USD", "payment_format": "Wire", "transaction_id": "TX_FIN_003"},
    ])
    res_fin = FinancialExpert().investigate(fin_df, case_file, exec_plan)
    prosecution_cards.extend(res_fin.cards)
    print("Financial Cards Generated:", len(res_fin.cards))

if "behaviour" in exec_plan.expert_sequence:
    beh_df = pd.DataFrame([
        {"from_account": "ACC_8000A94C0", "to_account": "ACC_COUNTERPARTY_X", "amount_received": 25000.0, "receiving_currency": "EUR", "preferred_currency": "GBP", "payment_format": "Cash", "preferred_payment_format": "ach", "baseline_daily_amount": 1000.0, "days_since_last_transaction": 120.0, "transaction_id": "TX_BEH_001"},
    ])
    res_beh = BehaviourExpert().investigate(beh_df, case_file, exec_plan)
    prosecution_cards.extend(res_beh.cards)
    print("Behavioural Cards Generated:", len(res_beh.cards))

# Step 3: Synthesize Evidence Graph (Phase C.4)
graph_builder = EvidenceGraphBuilder()
prosecution_graph = graph_builder.build(prosecution_cards, case_file=case_file)
print("Prosecution Graph Topology:", len(prosecution_graph.nodes), "nodes,", len(prosecution_graph.edges), "edges")

# Step 4: Adversarial Review & Graph Augmentation (Phase C.5)
defense_cards = DefenseAgent().review(prosecution_graph, case_file)
augmented_graph = graph_builder.augment_graph(prosecution_graph, defense_cards)
print("Augmented Graph Topology  :", len(augmented_graph.nodes), "nodes,", len(augmented_graph.edges), "edges")

# Step 5: Deliberate Tribunal Verdict (Phase C.6)
verdict = Tribunal().deliberate(augmented_graph, case_file)
print("Tribunal Verdict Category :", verdict.verdict)
print("Primary Hypothesis       :", verdict.primary_hypothesis)
print("Primary Score            :", verdict.primary_score)
print("Secondary Hypothesis     :", verdict.secondary_hypothesis)
print("Confidence Gap (Delta)   :", verdict.confidence_gap)
print("Calibrated Confidence    :", verdict.confidence)

# Step 6: Generate Investigation Report (Phase C.7)
report = ReportGenerator().generate(
    planner_context=planning_result,
    case_file=case_file,
    evidence_graph=augmented_graph,
    tribunal_verdict=verdict,
    query_text=query,
)

print("Report ID                :", report.report_id)
print("Markdown Output Size     :", len(report.markdown_content), "bytes")
print("HTML Output Size         :", len(report.html_content), "bytes")
print("JSON Payload Sections    :", list(report.json_payload.keys()))
```

---

### Protocol 2 — E2E Command-Line Interface Script Protocol

Run the end-to-end automated manual integration script:

```bash
python scripts/manual_test_phase_c7.py
```

#### Expected Terminal Output
```text
======================================================================
 TRIBUNAL — PHASE C.7 MANUAL VERIFICATION & REPORT ENGINE TEST
======================================================================

[1] Executing Planner for Query: 'Find structuring and unusual behaviour during the last month for account ACC_8000A94C0'...
    -> Intent parsed: pattern_detection
    -> Experts selected: ['financial', 'behaviour']

[2] Executing Financial Investigation Expert...
    -> Generated 1 Financial Investigation Card(s).

[3] Executing Customer Behaviour Investigation Expert...
    -> Generated 1 Behavioural Investigation Card(s).

[4] Executing Evidence Graph Builder (Phase C.4)...
    -> Prosecution EvidenceGraph built (5 nodes, 7 edges).

[5] Executing Adversarial Review Engine (Phase C.5)...
    -> Augmented EvidenceGraph built (9 nodes, 16 edges).

[6] Executing Tribunal Consensus & Deliberation Engine (Phase C.6)...
    -> Tribunal Verdict Issued: 'POSSIBLY_MALICIOUS' (Confidence: 0.5796)

[7] Executing Investigation Report & Explainability Engine (Phase C.7)...
    -> InvestigationReport built: 'rpt_case_c7_manual_001_d8b976'

----------------------------------------------------------------------
 REPORT SUMMARY & EXPLAINABILITY HIGHLIGHTS
----------------------------------------------------------------------
  Report ID               : rpt_case_c7_manual_001_d8b976
  Generated Timestamp     : 2026-07-25T16:53:55.123058+00:00
  Verdict Category        : POSSIBLY_MALICIOUS
  Primary Hypothesis      : Multiple Behavioural Anomalies (Behaviour Drift, Dormancy Reactivation, Currency Change, Payment Pattern Change) for Account ACC_8000A94C0
  Primary Support Score   : 0.7596
  Secondary Hypothesis    : Possible Structuring Activity for Account ACC_8000A94C0
  Secondary Support Score : 0.7406
  Confidence Gap (Delta)  : 0.0190
  Calibrated Confidence   : 0.5796
  Risk Level              : MEDIUM
  Report Markdown Size    : 6,460 bytes
  Report HTML Size        : 7,007 bytes
  Report JSON Payload Keys: ['metadata', 'executive_summary', 'query_interpretation', 'timeline', 'expert_findings', 'evidence_summary', 'graph_summary', 'defense_summary', 'tribunal_summary', 'provenance_details', 'audit_trail']

    -> Saved Markdown Report : D:\TRIBUNAL\tribunal\datasets\processed\report.md
    -> Saved Standalone HTML : D:\TRIBUNAL\tribunal\datasets\processed\report.html
    -> Saved JSON Payload   : D:\TRIBUNAL\tribunal\datasets\processed\report.json

======================================================================
 SUCCESS: Phase C.7 Report Engine Test & Artifact Generation Completed!
======================================================================
```

---

### Protocol 3 — Query Intent & Expert Sequence Verification Protocol

Verify runtime adherence to the Planner's `ExecutionPlan` across intent scenarios:

#### Scenario A: Multi-Expert Pattern Detection Query
* **Input Query**: `"Find structuring and unusual behaviour for account ACC_8000A94C0"`
* **Expected Intent**: `pattern_detection`
* **Expected Expert Sequence**: `['financial', 'behaviour']`
* **Verified Runtime Output**: Both `Financial` and `Behaviour` experts execute.

#### Scenario B: Single-Expert Behaviour Analysis Query
* **Input Query**: `"Show behavioural anomalies for account ACC_8000A94C0"`
* **Expected Intent**: `behaviour_analysis`
* **Expected Expert Sequence**: `['behaviour']`
* **Verified Runtime Output**: `[2] Skipping Financial Expert (not requested by ExecutionPlan)` and Customer Behaviour Expert executes.

#### Scenario C: Single-Expert Financial Structuring Query
* **Input Query**: `"Find structuring during the last month"`
* **Expected Intent**: `pattern_detection` (target pattern `structuring`)
* **Expected Expert Sequence**: `['financial', 'behaviour']`
* **Verified Runtime Output**: Both experts execute to evaluate financial structuring and behavioural corroboration.

#### Scenario D: Non-Tribunal EDA Query
* **Input Query**: `"Show payment format distribution"`
* **Expected Intent**: `eda_request`
* **Expected Expert Sequence**: `[]` (EDA Tool)
* **Verified Runtime Output**: Skipping experts, Tribunal, and Report generation.

---

### Protocol 4 — Automated Test Suite Protocol

Run all 118 unit and integration tests across Phase C:

```bash
pytest tribunal/tests/ -v
```

* **Target Result**: `118 passed in ~43s` (100% pass rate).

---

## 3. Verification Matrices & File Mapping

### Component Test Suite Mapping (118 Tests across 52 Files)

| Component | Test File Location | Target Functionality Verified |
| :--- | :--- | :--- |
| **Shared Models** | [`test_data_and_graph.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_data_and_graph.py) | Dataclass contracts, `PatternFinding`, `MetricEvidence` |
| **Planner Constants** | [`test_planner_constants.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_planner_constants.py) | `SUPPORTED_INTENTS`, `PATTERNS`, `OUTPUTS`, `EXPERTS`, `ASSETS` |
| **LLM Client Interface** | [`test_llm_client.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_llm_client.py) | Mock caller execution, empty query validation, fallback handling |
| **Query Parser** | [`test_query_parser.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_query_parser.py) | JSON parsing, markdown codeblocks, regex entity extraction |
| **Execution Planner** | [`test_execution_planner.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_execution_planner.py) | Deterministic mapping across 6 core intents |
| **Planner Orchestrator** | [`test_planner.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_planner.py) | End-to-end planning, `PlanningResult`, profiling metrics |
| **Financial Expert** | [`test_financial_expert.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_financial_expert.py) | 5-stage financial pipeline, card generation |
| **Behaviour Expert** | [`test_behaviour_expert.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_behaviour_expert.py) | E2E Customer Behaviour Expert pipeline |
| **Evidence Graph Builder** | [`test_evidence_graph_builder.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_evidence_graph_builder.py) | E2E EvidenceGraph construction & synthesis topology |
| **Defense Agent Pipeline** | [`test_defense_agent.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_defense_agent.py) | E2E Adversarial Review Engine & alternative explanations |
| **Tribunal Consensus** | [`test_tribunal.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_tribunal.py) | Full Verification Matrix across all 5 deliberation scenarios |
| **Explainability Engine** | [`test_explainability.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_explainability.py) | Metric-to-natural-language translation |
| **Executive Summary** | [`test_executive_summary.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_executive_summary.py) | Section 1 Executive Summary payload generation |
| **Evidence Summarizer** | [`test_evidence_summary.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_evidence_summary.py) | Sections 4, 5, and 9 evidence card and provenance summary |
| **Graph Summarizer** | [`test_graph_summary.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_graph_summary.py) | Section 6 topological graph analytics summary |
| **Report Builder** | [`test_report_builder.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_report_builder.py) | 10-section report orchestration |
| **Markdown Renderer** | [`test_renderer_markdown.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_renderer_markdown.py) | GitHub-flavored Markdown text rendering |
| **HTML Renderer** | [`test_renderer_html.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_renderer_html.py) | Standalone interactive HTML webpage rendering |
| **JSON Renderer** | [`test_renderer_json.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_renderer_json.py) | Structured JSON API payload rendering |
| **Report Validator** | [`test_report_validator.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_report_validator.py) | Quality validation & completeness enforcement |
| **Report Generator** | [`test_report_generator.py`](file:///d:/TRIBUNAL/tribunal/tests/unit/test_report_generator.py) | Single public interface `ReportGenerator.generate(...)` verification |

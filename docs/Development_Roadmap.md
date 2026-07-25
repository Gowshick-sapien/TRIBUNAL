# TRIBUNAL — Development Roadmap

**Document Classification:** Implementation Checklist
**Version:** 1.0
**Purpose:** Track implementation progress. Not architecture — a living checklist.

---

> Check items off as they ship. Each stage produces a testable artifact.
> Companion: `docs/Data_Contracts.md` defines every object crossing module boundaries.

---

## Current Status

| Phase | Name | Status |
|---|---|---|
| A | Foundation | **Complete** |
| B | Core Engine (Data, Preprocessing, Graph, Feature Spec) | **In Progress** |
| C | Investigation Engine | Not Started |
| D | Product | Not Started |

---

## Phase A — Foundation

> Architecture and implementation specs are complete. This phase locks contracts and structure before any business logic.

### Documents

- [x] Architecture Design Specification v1.0
- [x] Implementation Specification v1.0
- [x] Data Contracts (`docs/Data_Contracts.md`)
- [x] Development Roadmap (`docs/Development_Roadmap.md`)

### Repository Skeleton

- [x] `tribunal/` project root
- [x] Module directories (`models/`, `planner/`, `experts/`, etc.)
- [x] `tests/` with unit / integration / e2e subdirectories
- [x] `datasets/` placeholder
- [x] `config/` settings module stub
- [x] `requirements.txt` stub
- [x] `app.py` entry point stub
- [x] `README.md`

### Interfaces (Signatures Only)

- [x] `planner/planner.py` — Planner orchestrator
- [x] `planner/query_parser.py` — QueryParser
- [x] `planner/execution_planner.py` — ExecutionPlanner
- [x] `experts/base_expert.py` — BaseExpert
- [x] `experts/financial_expert.py` — FinancialExpert
- [x] `experts/behaviour_expert.py` — BehaviourExpert
- [x] `investigation/graph_builder.py` — GraphBuilder
- [x] `adversarial/defense_agent.py` — DefenseAgent
- [x] `tribunal/consensus_engine.py` — Tribunal
- [x] `report/report_generator.py` — ReportGenerator
- [x] `pipeline.py` — Pipeline orchestrator

**Phase A exit criteria:** All contracts documented. Repository skeleton exists. All interfaces defined with type signatures. No business logic.

---

## Phase B — Core Engine

### Stage 1 — Models & Data Ingestion

- [x] Dataclass field definitions (mirrors Data_Contracts.md)
- [x] `models/transaction.py` — Transaction data contract
- [x] `models/account.py` — Account metadata contract
- [x] `data/loader.py` — DataLoader (canonical entry point for Parquet/CSV reading)
- [x] `data/validator.py` — DataValidator & `validation_report.json`
- [x] JSON serialization / validation helpers
- [x] Unit tests for model instantiation and data loader (`tests/unit/test_data_and_graph.py`)

**Verify:** All dataclasses instantiate. JSON serialization round-trips. DataLoader loads datasets cleanly.

---

### Stage 2 — Dataset Preprocessing, Profiling & Transaction Graph

> Dataset frozen (IBM AML Dataset `LI-Small_Trans.csv` & `LI-Small_accounts.csv`).

#### Accomplished Steps
- [x] **Step 2: DataLoader (`data/loader.py`)** — Canonical ingestion layer (`DataLoader.load_transactions()`, `DataLoader.load_accounts()`).
- [x] **Step 3: Data Validation (`data/validator.py`)** — Validates timestamps, account IDs, currencies, payment formats, producing `processed/validation_report.json`.
- [x] **Step 4: Transaction & Account Models (`models/transaction.py`, `models/account.py`)** — Typed contracts populated from raw dataset.
- [x] **Step 5: Preprocessing & Parquet Conversion (`scripts/preprocess_dataset.py`)** — Standardizes schema, converts CSVs to `processed/transactions.parquet` (6.92M rows) and `processed/accounts.parquet` (712K rows).
- [x] **Step 6: Empirical Dataset Profiling (`scripts/profile_dataset.py`)** — Analyzes amounts, payment formats, top banks, currencies, degree distributions, generating `processed/dataset_profile.json`.
- [x] **Step 7: Feature Specifications (`tools/feature_definitions.py`)** — Defines feature schemas for Financial Expert (`rolling_sum_7d`, `velocity`, `threshold_proximity`, etc.) and Behaviour Expert (`baseline_daily_amount`, `deviation_score`, etc.).
- [x] **Step 8: Transaction Graph Engine (`investigation/transaction_graph.py`)** — NetworkX graph built over account transfers to provide reusable graph-derived features (`fan_in`, `fan_out`, `total_degree`, `repeated_counterparties`, `neighbourhood_size_2hop`).

**Verify:** Parquet dataset preprocessed (6.9M transactions, 712K accounts). Validation & profiling reports generated. Graph engine unit tested and passing.

---

### Stage 2.1 — Phase B.4 Transaction Network Builder

> Structural foundation for feature engineering & network analytics. Built as an in-memory NetworkX MultiDiGraph and persisted to disk.

- [x] **`investigation/transaction_network_builder.py`** — `TransactionNetworkBuilder` class
  - [x] `build()` — Builds `nx.MultiDiGraph` with account nodes and transaction edges
  - [x] `save()` — Persists graph to `datasets/processed/transaction_network.gpickle`
  - [x] `load()` — Instant zero-overhead loading from disk
  - [x] `validate()` — Structural integrity checks (`network_validation_report.json`)
  - [x] `get_network_statistics()` — Network topology metrics (`network_profile.json`)
- [x] **CLI Script (`scripts/build_network.py`)** — One-command execution to build, validate, profile, and save graph.
- [x] **Verification Manual Plan (`docs/B.4_Verification_Plan.md`)** — Step-by-step verification protocol & 10-point test matrix.

**Verify:** MultiDiGraph built, validated, and persisted (`transaction_network.gpickle`). Network profile JSON generated. Unit tests passing. Refer `docs/B.4_Verification_Plan.md`.

---

### Stage 2.2 — Phase B.5 Feature Store Builder

> Reusable collection of 44 AML analytical features across 705,903 accounts. Persisted to disk (`feature_store.parquet`).

- [x] **`tools/feature_store_builder.py`** — `FeatureStoreBuilder` class
  - [x] `compute_financial_features()` — Amounts, quantiles, rolling 7d/30d sums, threshold proximity
  - [x] `compute_behaviour_features()` — Velocity, active days, preferred currency/formats, deviation
  - [x] `compute_network_features()` — Fan-in, fan-out, unique senders/receivers, degree, repeated counterparties
  - [x] `compute_temporal_features()` — Weekend ratio, hour of day mode, rapid successive txns count
  - [x] `compute_statistical_features()` — Z-score amount, IQR outlier score
  - [x] `compute_rule_ready_features()` — Structuring score, rapid cashout indicator, high frequency deposit indicator
  - [x] `validate()` — Completeness and type integrity (`feature_validation_report.json`)
  - [x] `get_feature_profile()` — Analytical profile stats (`feature_store_profile.json`)
  - [x] `save()` — Persists Parquet (`datasets/processed/feature_store.parquet`)
- [x] **`data/loader.py` Integration** — Added `load_feature_store()` canonical data access method.
- [x] **CLI Script (`scripts/build_feature_store.py`)** — One-command execution to compute, validate, profile, and save feature store.
- [x] **Verification Manual Plan (`docs/B.5_Verification_Plan.md`)** — Step-by-step verification protocol & 10-point test matrix.

**Verify:** Feature Store built (705,903 accounts x 44 features), validated (`Status: PASSED`), and persisted (`feature_store.parquet` - 65.5 MB). All unit tests passing. Refer `docs/B.5_Verification_Plan.md`.

---

### Stage 3 — Planner

- [ ] `planner/query_parser.py` — Ollama extraction + regex fallback
- [ ] `planner/execution_planner.py` — deterministic plan construction
- [ ] `planner/planner.py` — orchestrates parse → plan
- [ ] `tests/unit/test_query_parser.py`
- [ ] `tests/unit/test_execution_planner.py`

**First working milestone:**

```
Input:  "Find structuring during the last month"
Output: InvestigationPlan + ExecutionPlan (JSON)
```

**Verify:** Targeted query skips EDA. Broad query includes EDA. Different queries produce visibly different plans.

---

### Stage 4 — Feature Engineering

- [ ] `tools/feature_engineering.py`
  - [ ] Rolling sums (7d, 30d)
  - [ ] Transaction velocity
  - [ ] Transaction frequency
  - [ ] Amount deviation from baseline
  - [ ] Threshold proximity (sub-threshold count/ratio)
- [ ] `tools/anomaly_detection.py`
- [ ] `tools/eda_tool.py`
- [ ] `tests/unit/test_feature_engineering.py`
- [ ] `tests/unit/test_anomaly_detection.py`

**Verify:** Known structuring data produces `sub_threshold_ratio > 0.9`. Velocity spike detected. Empty input returns zero features without crash.

---

## Phase C — Investigation Engine

### Stage 5 — Experts

- [ ] `experts/financial_expert.py`
  - [ ] Structuring check
  - [ ] Velocity check
  - [ ] Anomaly check
  - [ ] Case File update
- [ ] `experts/behaviour_expert.py`
  - [ ] Historical deviation check
  - [ ] Hypothesis-directed investigation
  - [ ] Profile mismatch check
- [ ] `tests/unit/test_financial_expert.py`
- [ ] `tests/unit/test_behaviour_expert.py`
- [ ] `tests/integration/test_expert_pipeline.py`

**Verify:** Financial Expert emits cards from structuring data. Behaviour Expert reads Case File and produces supporting/contradicting cards. Cards match InvestigationCard schema.

---

### Stage 6 — Evidence Graph

- [ ] `investigation/graph_builder.py`
  - [ ] Node creation from cards
  - [ ] Support edges from `supports` field
  - [ ] Contradiction edges from `counter_hypothesis`
- [ ] `tests/unit/test_graph_builder.py`

**Verify:** Two supporting cards → 1 support edge. Counter-hypothesis match → contradiction edge. Orphan references skipped with warning.

---

### Stage 7 — Defense

- [ ] `adversarial/defense_agent.py`
  - [ ] LLM counter-explanation prompt
  - [ ] Plausibility threshold gate
  - [ ] Contradiction edge injection
- [ ] `tests/unit/test_defense_agent.py`

**Verify:** Plausible counter → edge added. Weak counter → graph unchanged. LLM failure → `defense_skipped = true`.

---

### Stage 8 — Tribunal

- [ ] `tribunal/consensus_engine.py`
  - [ ] Net support computation
  - [ ] Hypothesis ranking
  - [ ] Winning chain trace
  - [ ] Risk level mapping
- [ ] `tests/unit/test_consensus_engine.py`
- [ ] `tests/integration/test_graph_to_verdict.py`

**Verify:** Clear winner identified. Defense contradiction reduces confidence. Empty graph → `no_evidence`. Threshold mapping correct.

---

## Phase D — Product

### Stage 9 — Report

- [ ] `report/report_generator.py`
- [ ] `tests/unit/test_report_generator.py`

**Verify:** Full report with all sections. Runner-up section omitted when single hypothesis. Empty verdict handled gracefully.

---

### Stage 10 — Pipeline

- [ ] `pipeline.py` — full orchestration
  - [ ] Expert sequential execution
  - [ ] Adaptive re-investigation (bounded, one cycle)
  - [ ] End-to-end wiring
- [ ] `tests/e2e/test_full_pipeline.py`

**Verify:** Query in → InvestigationReport out. Known structuring data → correct winning hypothesis and recommendation.

---

### Stage 11 — Streamlit UI

- [ ] `app.py` — Streamlit entry point
- [ ] `ui/components.py` — query input, plan display, graph viz, report display
- [ ] Demo queries prepared (2–3 scenarios)

**Verify:** User types query. UI shows execution plan, expert invocations, evidence graph, final report. Different queries → different investigation paths.

---

### Stage 12 — Polish

- [ ] `README.md` — setup, usage, architecture summary
- [ ] Demo script / slides
- [ ] Coverage report (`pytest --cov`)
- [ ] Final demo rehearsal

---

## Quick Reference — Where Am I?

```
Phase A  Foundation          ✅ COMPLETE
         ├── Contracts       ✅
         ├── Roadmap         ✅
         ├── Skeleton        ✅
         └── Interfaces      ✅

Phase B  Core Engine         ← NEXT
         ├── Models
         ├── Dataset
         ├── Planner         ← First demo milestone
         └── Features

Phase C  Investigation Engine
         ├── Experts
         ├── Graph
         ├── Defense
         └── Tribunal

Phase D  Product
         ├── Report
         ├── Pipeline
         ├── Streamlit
         └── Demo
```

---

## Demo Queries (Prepare During Stage 10)

| # | Query | Expected Pattern | Expected Recommendation |
|---|---|---|---|
| 1 | "Find structuring in the last 30 days for customer 541" | structuring | review or report |
| 2 | "Show unusual activity across high-risk accounts this quarter" | anomaly / deviation | review |
| 3 | "Check customer 200" | broad detection | monitor or review |

---

## Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| Dataset lacks structuring signal | Demo fails | Pre-identify structuring scenarios; generate synthetic overlay if needed |
| Ollama unavailable | Query parsing degraded | Regex fallback already specified |
| LLM defense hallucination | False counter-explanation | Plausibility threshold + deterministic tribunal |
| Column mismatch | Feature engineering breaks | Document mapping in Dataset_Assumptions.md |

---

*Last updated: 2026-07-25 — Phase A complete*

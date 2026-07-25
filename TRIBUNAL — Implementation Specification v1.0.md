# TRIBUNAL — Implementation Specification v1.0

**Document Classification:** Engineering Blueprint
**Version:** 1.0
**Companion Document:** TRIBUNAL — Architecture Design Specification v1.0

---

> This document is the engineering contract.
>
> The Architecture Specification explains *why* the system exists.
> This document explains *how* every architectural component is realized in software.
>
> For every component we answer: What is its responsibility? What inputs does it receive? What outputs does it produce? What algorithm does it execute? Which modules does it depend on? What are its failure cases? How is it tested?
>
> When this document is complete, implementation becomes almost mechanical.

---

## Table of Contents

1. [System Implementation Overview](#1-system-implementation-overview)
2. [Repository Structure](#2-repository-structure)
3. [Component Specifications](#3-component-specifications)
4. [Module Interaction Sequence](#4-module-interaction-sequence)
5. [Internal Algorithms](#5-internal-algorithms)
6. [Configuration](#6-configuration)
7. [Logging Strategy](#7-logging-strategy)
8. [Error Handling](#8-error-handling)
9. [Testing Strategy](#9-testing-strategy)
10. [Implementation Milestones](#10-implementation-milestones)

---

## 1. System Implementation Overview

The TRIBUNAL architecture translates into a Python application organized across two distinct layers and arranged in a directed execution pipeline. Every module has a single responsibility, well-defined inputs and outputs, and communicates with adjacent modules through shared data contracts.

### Two-Layer Separation

```
══════════════════════════════════════════════════
  LANGUAGE UNDERSTANDING LAYER
══════════════════════════════════════════════════
  Natural Language Query (string)
          │
          ▼
  ┌──────────────────┐
  │  planner/         │  Query understanding (Ollama)
  │  query_parser      │  → InvestigationPlan
  └────────┬─────────┘
           │
═════════╬════════════════════════════════════════
  ANALYTICAL LAYER (deterministic)
══════════════════════════════════════════════════
           │
           ▼
  ┌──────────────────┐
  │  planner/         │  Plan construction
  │  execution_planner │  → ExecutionPlan
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │  models/          │  Case File initialized (empty)
  │  case_file         │  → CaseFile
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │  experts/         │  Sequential expert execution
  │  financial_expert  │  → InvestigationCard[]
  │  behaviour_expert  │  → CaseFile updated
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │  investigation/   │  Graph construction from cards
  │  graph_builder     │  → EvidenceGraph
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │  adversarial/     │  Hypothesis challenge
  │  defense_agent     │  → EvidenceGraph updated
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │  tribunal/        │  Graph reasoning + verdict
  │  consensus_engine  │  → TribunalVerdict
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │  report/          │  Structured output generation
  │  report_generator  │  → InvestigationReport
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │  ui/              │  Streamlit presentation layer
  │  app.py            │  → Rendered to user
  └──────────────────┘
```

Every arrow in this diagram corresponds to a function call. Every box corresponds to a Python module. Every label after `→` corresponds to a dataclass defined in `models/`. The horizontal divider between layers marks the boundary between non-deterministic language understanding and deterministic analytical processing.

---

## 2. Repository Structure

This is the canonical project layout. It should not change during development.

```
tribunal/
│
├── app.py                              # Streamlit entry point
│
├── pipeline.py                         # Orchestrates the full investigation pipeline
│
├── models/                             # Shared data contracts (dataclasses)
│   ├── __init__.py
│   ├── investigation_plan.py           # InvestigationPlan dataclass
│   ├── execution_plan.py               # ExecutionPlan dataclass
│   ├── case_file.py                    # CaseFile dataclass
│   ├── investigation_card.py           # InvestigationCard dataclass
│   ├── evidence_graph.py               # EvidenceGraph wrapper
│   ├── tribunal_verdict.py             # TribunalVerdict dataclass
│   └── investigation_report.py         # InvestigationReport dataclass
│
├── planner/                            # Query understanding & execution planning
│   ├── __init__.py
│   ├── planner.py                      # Orchestrates query understanding and plan construction
│   ├── query_parser.py                 # Natural language → InvestigationPlan (via Ollama)
│   └── execution_planner.py            # InvestigationPlan → ExecutionPlan
│
├── experts/                            # Domain expert investigators
│   ├── __init__.py
│   ├── base_expert.py                  # Abstract expert interface
│   ├── financial_expert.py             # Financial Pattern Expert
│   └── behaviour_expert.py             # Customer Behaviour Expert
│
├── tools/                              # Shared analytical tools
│   ├── __init__.py
│   ├── eda_tool.py                     # Exploratory data analysis
│   ├── feature_engineering.py          # AML feature computation
│   └── anomaly_detection.py            # Statistical outlier detection
│
├── investigation/                      # Evidence graph construction
│   ├── __init__.py
│   └── graph_builder.py               # Cards → NetworkX graph
│
├── adversarial/                        # Adversarial investigation phase
│   ├── __init__.py
│   └── defense_agent.py               # Dominant hypothesis challenger
│
├── tribunal/                           # Consensus engine
│   ├── __init__.py
│   └── consensus_engine.py            # Graph traversal → verdict
│
├── report/                             # Report generation
│   ├── __init__.py
│   └── report_generator.py            # Verdict → structured report
│
├── ui/                                 # Interface components
│   ├── __init__.py
│   └── components.py                   # Streamlit UI components
│
├── config/                             # Centralized configuration
│   ├── __init__.py
│   └── settings.py                     # All thresholds, paths, parameters
│
├── utils/                              # Shared utilities
│   ├── __init__.py
│   ├── logger.py                       # Structured logging
│   └── ollama_client.py                # Ollama inference wrapper (query parsing only)
│
├── datasets/                           # Transaction data
│   └── ...                             # CSV/Parquet files
│
├── tests/                              # Test suite
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_query_parser.py
│   │   ├── test_execution_planner.py
│   │   ├── test_feature_engineering.py
│   │   ├── test_financial_expert.py
│   │   ├── test_behaviour_expert.py
│   │   ├── test_graph_builder.py
│   │   ├── test_defense_agent.py
│   │   ├── test_consensus_engine.py
│   │   └── test_report_generator.py
│   ├── integration/
│   │   ├── test_expert_pipeline.py
│   │   └── test_graph_to_verdict.py
│   └── e2e/
│       └── test_full_pipeline.py
│
├── requirements.txt
└── README.md
```

### Design Decisions

- **`models/` is separate from logic.** Data contracts are shared across all modules. No module owns a dataclass — `models/` is the single source of truth for every data structure that crosses a module boundary.
- **`tools/` is shared infrastructure.** Feature engineering and anomaly detection are consumed by multiple experts. They do not belong inside any single expert module.
- **`pipeline.py` is the orchestrator.** It calls modules in sequence, passes data contracts between them, and handles the adaptive re-investigation decision. No module calls another module directly — all wiring goes through the pipeline.
- **`config/settings.py` is the single configuration source.** No threshold, path, or parameter is hardcoded in any module. Every configurable value is imported from `settings.py`.

---

## 3. Component Specifications

### 3.1 Query Understanding & Planning Agent

The Query Understanding & Planning Agent is organized into two sub-modules: the **Query Parser** (language understanding layer) and the **Execution Planner** (analytical layer). The Query Parser is the only component in the entire system that depends on a language model. Everything downstream is deterministic.

#### 3.1.1 Query Parser

**Module:** `planner/query_parser.py`

**Objective**
Transform an unrestricted natural-language query into a structured `InvestigationPlan` that downstream components can consume without further parsing. This is the single point in the system where natural language is converted to structured data.

**Implementation**
The Query Parser uses a lightweight LLM through a local inference runtime (Ollama) to transform unrestricted natural language into a deterministic structured investigation plan. The LLM is used exclusively for language understanding — it does not perform analysis, generate hypotheses, or make investigative decisions.

**Inputs**
| Parameter | Type | Description |
|---|---|---|
| `query` | `str` | Raw natural-language query from the user |

**Outputs**
| Parameter | Type | Description |
|---|---|---|
| `InvestigationPlan` | `dataclass` | Structured representation of the query |

**InvestigationPlan Schema**
```python
@dataclass
class InvestigationPlan:
    raw_query: str                          # Original query string
    intent: str                             # "pattern_detection" | "broad_scan" | "compliance_check"
    target_pattern: Optional[str]           # "structuring" | "smurfing" | "velocity" | "anomaly" | None
    customer_id: Optional[str]              # Specific customer, if targeted
    date_range: Optional[Tuple[date, date]] # Start and end dates
    country: Optional[str]                  # Geographic filter
    txn_type: Optional[str]                 # Transaction type filter
    risk_level: Optional[str]               # "high" | "medium" | "low" | None
    experts: List[str]                      # Ordered expert identifiers
    run_eda: bool                           # Whether to run EDA tool first
```

**Example InvestigationPlan**
```json
{
    "raw_query": "Find structuring in the last 30 days for customer 541",
    "intent": "pattern_detection",
    "target_pattern": "structuring",
    "customer_id": "541",
    "date_range": ["2026-06-24", "2026-07-24"],
    "country": null,
    "txn_type": null,
    "risk_level": null,
    "experts": ["financial", "behaviour"],
    "run_eda": false
}
```

**Internal Workflow**
1. Receive raw query string.
2. Construct a structured extraction prompt with query and field definitions.
3. Call Ollama with the extraction prompt.
4. Parse the model response into `InvestigationPlan` fields.
5. Validate all extracted fields — apply defaults for missing optional fields.
6. Return `InvestigationPlan`.

**Dependencies**
- `utils/ollama_client.py` — Ollama inference call for language understanding.
- `config/settings.py` — default values for optional fields, model name.

**Error Handling**
| Failure | Response |
|---|---|
| Ollama unavailable | Fall back to keyword-based regex extraction. Log degraded mode. |
| Unparseable query | Return `InvestigationPlan` with `intent="broad_scan"` and no filters. Log warning. |
| Invalid date range | Default to last 30 days. Log correction. |
| Model response unparseable | Fall back to regex extraction. Log error with raw response. |

**Unit Tests**
| Test | Input | Expected Output |
|---|---|---|
| Targeted structuring query | `"Find structuring in the last 30 days for customer 541"` | `intent="pattern_detection"`, `target_pattern="structuring"`, `customer_id="541"`, `experts=["financial", "behaviour"]`, `run_eda=False` |
| Broad scan query | `"Show unusual activity across high-risk accounts this quarter"` | `intent="broad_scan"`, `target_pattern="anomaly"`, `risk_level="high"`, `run_eda=True` |
| Minimal query | `"Check customer 200"` | `intent="pattern_detection"`, `customer_id="200"`, remaining fields default |
| Malformed query | `"asdf"` | `intent="broad_scan"`, all filters `None` |

---

#### 3.1.2 Execution Planner

**Module:** `planner/execution_planner.py`

**Objective**
Translate an `InvestigationPlan` into a concrete `ExecutionPlan` — finalizing expert ordering, resolving filter parameters, and preparing the configuration that the pipeline orchestrator consumes. This module is fully deterministic — no language model dependency.

**Inputs**
| Parameter | Type | Description |
|---|---|---|
| `investigation_plan` | `InvestigationPlan` | Structured plan from the query parser |

**Outputs**
| Parameter | Type | Description |
|---|---|---|
| `ExecutionPlan` | `dataclass` | Finalized execution configuration |

**ExecutionPlan Schema**
```python
@dataclass
class ExecutionPlan:
    run_eda: bool                           # Whether to run EDA tool first
    expert_sequence: List[str]              # Ordered list of expert identifiers
    target_pattern: Optional[str]           # Pattern to focus investigation on
    filters: Dict[str, Any]                 # Resolved filters for data loading
    rationale: str                          # Human-readable explanation of why this plan was chosen
```

**Internal Workflow**
1. Receive `InvestigationPlan`.
2. Validate and finalize the expert sequence:
   - If `investigation_plan.experts` is populated, use it directly.
   - If empty, determine expert sequence based on `target_pattern`:
     - Structuring / smurfing / velocity → Financial Expert first, then Behaviour Expert.
     - Anomaly / deviation → Behaviour Expert first, then Financial Expert.
     - No pattern specified → Financial Expert first, then Behaviour Expert (default).
3. Resolve `run_eda` from investigation plan.
4. Resolve filter parameters into concrete query constraints.
5. Construct `rationale` string describing the plan and why each expert was selected or skipped.
6. Return `ExecutionPlan`.

**Dependencies**
- `models/investigation_plan.py` — input dataclass.
- `config/settings.py` — expert registry (available experts and their identifiers).

**Error Handling**
| Failure | Response |
|---|---|
| Unknown intent | Default to `"broad_scan"` with full expert sequence. Log warning. |
| Empty expert sequence | Always include at least Financial Expert. |

**Unit Tests**
| Test | Input Intent | Expected `run_eda` | Expected Sequence |
|---|---|---|---|
| Targeted query | `pattern_detection`, `customer_id="541"` | `False` | `["financial", "behaviour"]` |
| Broad scan | `broad_scan`, no customer | `True` | `["financial", "behaviour"]` |
| Compliance check | `compliance_check`, `customer_id="200"` | `False` | `["behaviour", "financial"]` |

---

### 3.2 Feature Engineering Tool

**Module:** `tools/feature_engineering.py`

**Objective**
Compute AML-relevant derived features from raw transaction data. This module is shared infrastructure — consumed by both experts, never invoked directly by the pipeline.

**Inputs**
| Parameter | Type | Description |
|---|---|---|
| `transactions` | `pd.DataFrame` | Filtered transaction records |
| `customer_id` | `str` | Customer identifier for baseline computation |
| `window_days` | `int` | Rolling window size in days |

**Outputs**
| Parameter | Type | Description |
|---|---|---|
| `features` | `Dict[str, Any]` | Computed feature dictionary |

**Feature Dictionary Schema**
```python
{
    "rolling_sum_7d": float,                # Rolling sum of amounts over 7-day window
    "rolling_sum_30d": float,               # Rolling sum of amounts over 30-day window
    "txn_count_daily": float,               # Average daily transaction count
    "txn_velocity": float,                  # Transactions per day in analysis window
    "amount_mean": float,                   # Mean transaction amount
    "amount_std": float,                    # Standard deviation of amounts
    "amount_deviation_from_baseline": float, # Current vs. historical mean
    "max_single_amount": float,             # Largest single transaction
    "sub_threshold_count": int,             # Transactions just below reporting threshold
    "sub_threshold_ratio": float,           # Ratio of sub-threshold to total transactions
    "unique_beneficiaries": int,            # Count of distinct counterparties
    "weekend_txn_ratio": float,             # Proportion of weekend transactions
    "daily_volume_change_pct": float,       # % change in daily volume vs. baseline
}
```

**Internal Workflow**
1. Load historical baseline for `customer_id` (prior 90-day average).
2. Filter `transactions` to the specified `window_days`.
3. Compute rolling sums using pandas `rolling()`.
4. Compute velocity metrics: count / days.
5. Compute deviation metrics: current window vs. historical baseline.
6. Compute threshold-proximity metrics: count transactions within configurable range below reporting threshold.
7. Return feature dictionary.

**Dependencies**
- `pandas` — data manipulation and rolling calculations.
- `numpy` — statistical computations.
- `config/settings.py` — reporting threshold value, baseline window size.

**Error Handling**
| Failure | Response |
|---|---|
| No transactions found | Return feature dict with all values set to `0` or `None`. Log warning. |
| Insufficient history for baseline | Use available history as baseline, flag `baseline_incomplete = True` in output. |
| Missing columns in DataFrame | Raise `ValueError` with specific missing column names. |

**Unit Tests**
| Test | Scenario | Assertion |
|---|---|---|
| Structuring pattern | 10 transactions at $9,800 | `sub_threshold_count = 10`, `sub_threshold_ratio > 0.9` |
| Normal activity | Random amounts, no clustering | `sub_threshold_ratio < 0.2` |
| Velocity spike | 30 transactions in 2 days vs. baseline of 5/day | `daily_volume_change_pct > 200` |
| Empty input | No transactions | All numeric features = `0` |

---

### 3.3 Anomaly Detection Tool

**Module:** `tools/anomaly_detection.py`

**Objective**
Apply statistical outlier detection to transaction amounts. Provides a quantitative signal that complements the rule-based checks in the Financial Expert.

**Inputs**
| Parameter | Type | Description |
|---|---|---|
| `transactions` | `pd.DataFrame` | Transaction records with amount column |
| `features` | `Dict[str, Any]` | Pre-computed features from feature engineering |

**Outputs**
| Parameter | Type | Description |
|---|---|---|
| `anomaly_result` | `AnomalyResult` | Outlier flags, scores, and flagged transaction IDs |

**AnomalyResult Schema**
```python
@dataclass
class AnomalyResult:
    method: str                             # "zscore" | "isolation_forest"
    outlier_count: int                      # Number of flagged transactions
    outlier_txn_ids: List[str]              # IDs of flagged transactions
    outlier_scores: Dict[str, float]        # txn_id → anomaly score
    overall_anomaly_score: float            # Aggregate anomaly score (0.0–1.0)
```

**Internal Workflow**
1. Extract transaction amounts as a numeric array.
2. Compute z-scores for all transaction amounts.
3. Flag transactions with `|z-score| > threshold` (configurable, default 2.5).
4. If sufficient data points (≥ 20), fit Isolation Forest and compute anomaly scores.
5. Merge results — a transaction flagged by either method is included.
6. Compute aggregate anomaly score as the proportion of flagged transactions weighted by their scores.
7. Return `AnomalyResult`.

**Dependencies**
- `numpy` — z-score computation.
- `scikit-learn` — `IsolationForest`.
- `config/settings.py` — z-score threshold, Isolation Forest contamination parameter.

**Error Handling**
| Failure | Response |
|---|---|
| Fewer than 3 transactions | Skip statistical analysis. Return `AnomalyResult` with `outlier_count = 0`. Log warning. |
| Fewer than 20 transactions | Skip Isolation Forest, use z-score only. |
| All amounts identical | Z-score undefined (std = 0). Return no outliers. |

**Unit Tests**
| Test | Scenario | Assertion |
|---|---|---|
| Clear outlier | One transaction at $50,000 among $500 average | That transaction flagged |
| No outliers | Uniform distribution of amounts | `outlier_count = 0` |
| Small dataset | 5 transactions | Only z-score used, Isolation Forest skipped |

---

### 3.4 EDA Tool

**Module:** `tools/eda_tool.py`

**Objective**
Generate a lightweight statistical profile of the dataset for broad/exploratory queries. Skipped entirely for targeted single-entity queries.

**Inputs**
| Parameter | Type | Description |
|---|---|---|
| `transactions` | `pd.DataFrame` | Full or filtered transaction dataset |
| `filters` | `Dict[str, Any]` | Filters from the execution plan |

**Outputs**
| Parameter | Type | Description |
|---|---|---|
| `eda_summary` | `Dict[str, Any]` | Statistical summary for planner context |

**EDA Summary Schema**
```python
{
    "total_transactions": int,
    "date_range": Tuple[str, str],
    "unique_customers": int,
    "total_amount": float,
    "mean_amount": float,
    "median_amount": float,
    "high_risk_customer_count": int,
    "top_customers_by_volume": List[Dict],  # top 10 by transaction volume
    "amount_distribution": Dict[str, int],  # histogram buckets
}
```

**Internal Workflow**
1. Apply filters from the execution plan to the dataset.
2. Compute aggregate statistics (count, sum, mean, median).
3. Identify unique customers and high-risk customer count.
4. Rank customers by transaction volume.
5. Build amount distribution histogram.
6. Return summary dictionary.

**Dependencies**
- `pandas` — aggregation and grouping.
- `config/settings.py` — histogram bucket boundaries, top-N count.

**Error Handling**
| Failure | Response |
|---|---|
| Empty dataset after filters | Return summary with all counts = `0`. Log warning. |
| Missing expected columns | Raise `ValueError` with specifics. |

**Unit Tests**
| Test | Scenario | Assertion |
|---|---|---|
| Normal dataset | 1000 transactions, 50 customers | All summary fields populated, counts correct |
| Empty after filter | Date range yields no results | All counts = `0`, no crash |
| Single customer | One customer in dataset | `unique_customers = 1` |

---

### 3.5 Financial Pattern Expert

**Module:** `experts/financial_expert.py`

**Objective**
Investigate transactional evidence for known AML typologies — structuring, smurfing, velocity anomalies, and threshold-adjacent behaviour. Emit Investigation Cards with competing hypotheses.

**Inputs**
| Parameter | Type | Description |
|---|---|---|
| `transactions` | `pd.DataFrame` | Filtered transaction records |
| `case_file` | `CaseFile` | Current case state (may be empty on first expert) |
| `execution_plan` | `ExecutionPlan` | Planner's instructions |

**Outputs**
| Parameter | Type | Description |
|---|---|---|
| `cards` | `List[InvestigationCard]` | 1–3 Investigation Cards |
| `case_file` | `CaseFile` | Updated with dominant hypothesis |

**InvestigationCard Schema**
```python
@dataclass
class InvestigationCard:
    card_id: str                            # Unique identifier (e.g., "card_001")
    source_expert: str                      # "financial_pattern"
    derived_from_transactions: List[str]    # Transaction IDs that produced this card
    generated_at: str                       # ISO 8601 timestamp
    hypothesis: str                         # e.g., "structuring"
    confidence: float                       # 0.0 – 1.0
    evidence: str                           # Human-readable evidence summary
    counter_hypothesis: Optional[str]       # Alternative explanation
    missing_data: Optional[str]             # Data that would strengthen/weaken the hypothesis
    supports: List[str]                     # card_ids this card supports
```

**Internal Workflow**
1. Receive filtered transactions and execution plan.
2. Call `feature_engineering.compute_features()` to generate AML feature set.
3. **Structuring check:**
   - Count transactions within `[REPORTING_THRESHOLD - STRUCTURING_MARGIN, REPORTING_THRESHOLD)`.
   - If `sub_threshold_ratio > STRUCTURING_RATIO_THRESHOLD` → emit structuring card.
   - Confidence = `min(sub_threshold_ratio * 1.1, 0.95)`.
4. **Velocity check:**
   - Compare `txn_velocity` against customer baseline.
   - If `daily_volume_change_pct > VELOCITY_SPIKE_THRESHOLD` → emit velocity card.
   - Confidence = `min(daily_volume_change_pct / 1000, 0.90)`.
5. **Statistical outlier check:**
   - Call `anomaly_detection.detect()`.
   - If `overall_anomaly_score > ANOMALY_THRESHOLD` → emit anomaly card.
   - Confidence = `anomaly_result.overall_anomaly_score`.
6. Select the card with highest confidence as `dominant_hypothesis`.
7. Update Case File: write `dominant_hypothesis`, `dominant_confidence`, and `open_question`.
8. Return cards and updated Case File.

**Dependencies**
- `tools/feature_engineering.py` — feature computation.
- `tools/anomaly_detection.py` — statistical outlier detection.
- `models/investigation_card.py` — card dataclass.
- `models/case_file.py` — case file dataclass.
- `config/settings.py` — all thresholds.

**Error Handling**
| Failure | Response |
|---|---|
| No transactions after filtering | Emit one card with `hypothesis="insufficient_data"`, `confidence=0.0`. Log warning. |
| Feature engineering returns empty | Skip derived checks, run only anomaly detection. |
| Anomaly detection fails | Skip statistical layer, continue with rule-based checks only. Log error. |

**Unit Tests**
| Test | Scenario | Assertion |
|---|---|---|
| Clear structuring | 12 deposits at $9,700–$9,900 | Card emitted with `hypothesis="structuring"`, confidence > 0.7 |
| Velocity spike | 30 txns in 2 days, baseline 5/day | Card emitted with `hypothesis="velocity_anomaly"` |
| Normal activity | Random amounts, normal frequency | Either no cards or cards with low confidence |
| Mixed signals | Structuring + velocity both present | 2 cards emitted, highest confidence = dominant |
| No data | Empty transaction set | One card with `hypothesis="insufficient_data"` |

---

### 3.6 Customer Behaviour Expert

**Module:** `experts/behaviour_expert.py`

**Objective**
Investigate whether a customer's current activity deviates from their historical baseline — specifically targeting the hypothesis established by prior experts through the Case File.

**Inputs**
| Parameter | Type | Description |
|---|---|---|
| `transactions` | `pd.DataFrame` | Filtered transaction records |
| `case_file` | `CaseFile` | Current case state (contains dominant hypothesis from prior expert) |
| `execution_plan` | `ExecutionPlan` | Planner's instructions |

**Outputs**
| Parameter | Type | Description |
|---|---|---|
| `cards` | `List[InvestigationCard]` | 1–2 Investigation Cards |
| `case_file` | `CaseFile` | Updated if findings are stronger |

**Internal Workflow**
1. Read the Case File — extract `dominant_hypothesis` and `dominant_confidence`.
2. Call `feature_engineering.compute_features()` for historical baseline comparison.
3. **Historical deviation check:**
   - Compare current-window activity against the customer's 90-day baseline.
   - Compute `daily_volume_change_pct`, `amount_deviation_from_baseline`.
   - If deviation exceeds `BEHAVIOUR_DEVIATION_THRESHOLD` → emit deviation card.
   - Confidence = deviation metric normalized to [0.0, 1.0].
4. **Hypothesis-directed investigation:**
   - If `dominant_hypothesis == "structuring"` → check whether the deviation pattern is consistent with deliberate threshold avoidance (consistent sub-threshold clustering in recent window but not in historical window).
   - If `dominant_hypothesis == "velocity_anomaly"` → check whether the velocity spike aligns with known legitimate patterns (payroll dates, month-end).
5. **Profile-context check** (if data available):
   - Compare declared income/business type against transaction pattern.
   - Flag mismatches (e.g., declared income $40K but receiving $200K/month in deposits).
6. Determine if this expert's findings are stronger than the current dominant hypothesis:
   - If `max(card.confidence for card in cards) > case_file.dominant_confidence` → update Case File.
   - Otherwise → Case File retains prior expert's hypothesis.
7. Set `supports` fields on cards to reference prior expert's cards where corroborating.
8. Return cards and updated Case File.

**Dependencies**
- `tools/feature_engineering.py` — baseline computation.
- `models/investigation_card.py` — card dataclass.
- `models/case_file.py` — case file dataclass.
- `config/settings.py` — deviation thresholds, baseline window.

**Error Handling**
| Failure | Response |
|---|---|
| No historical data | Emit card with `missing_data="historical_baseline"`, confidence capped at 0.5. |
| Case File empty | Investigate without hypothesis direction — broad deviation check. |
| Profile data unavailable | Skip profile-context check. Note in card's `missing_data` field. |

**Unit Tests**
| Test | Scenario | Assertion |
|---|---|---|
| Supporting structuring | 430% volume spike, prior hypothesis = structuring | Card emitted with `supports` referencing financial expert's card |
| Contradicting structuring | Volume consistent with baseline, prior hypothesis = structuring | Card with low confidence, no support edge |
| No prior hypothesis | Empty Case File | Card based on deviation alone |
| Profile mismatch | Declared income $40K, deposits $200K/month | Card emitted noting profile inconsistency |

---

### 3.7 Evidence Graph Builder

**Module:** `investigation/graph_builder.py`

**Objective**
Translate all Investigation Cards into a directed, weighted NetworkX graph. Relationships are derived directly from each card's declared fields — translation, not inference.

**Inputs**
| Parameter | Type | Description |
|---|---|---|
| `cards` | `List[InvestigationCard]` | All cards from all experts |

**Outputs**
| Parameter | Type | Description |
|---|---|---|
| `graph` | `nx.DiGraph` | Directed evidence graph |

**Graph Structure**

*Nodes:*
```python
# Each node stores the full card data
graph.add_node(card.card_id, **{
    "hypothesis": card.hypothesis,
    "confidence": card.confidence,
    "evidence": card.evidence,
    "source_expert": card.source_expert,
    "derived_from_transactions": card.derived_from_transactions,
    "counter_hypothesis": card.counter_hypothesis,
    "missing_data": card.missing_data,
})
```

*Support Edges:*
```python
# Derived from card.supports field
graph.add_edge(card.card_id, supported_card_id, **{
    "relation": "supports",
    "weight": card.confidence,       # support strength = card's own confidence
    "reason": f"{card.card_id} supports {supported_card_id}",
})
```

*Contradiction Edges (candidates):*
```python
# Derived from card.counter_hypothesis field
# Links card to any existing card whose hypothesis matches counter_hypothesis
graph.add_edge(card.card_id, target_card_id, **{
    "relation": "contradicts",
    "weight": 1.0 - card.confidence, # contradiction strength = inverse confidence
    "reason": f"{card.hypothesis} counters {target_card.hypothesis}",
})
```

**Internal Workflow**
1. Initialize empty `nx.DiGraph`.
2. For each card, add a node with full card attributes.
3. For each card with non-empty `supports` list, add support edges to referenced card IDs.
4. For each card with a `counter_hypothesis`, scan existing nodes for matching hypotheses and add candidate contradiction edges.
5. Validate graph integrity: ensure no orphan edges (both source and target nodes exist).
6. Return graph.

**Dependencies**
- `networkx` — graph data structure.
- `models/investigation_card.py` — card dataclass.

**Error Handling**
| Failure | Response |
|---|---|
| No cards provided | Return empty graph. Log warning. |
| Card references non-existent card ID in `supports` | Skip that edge. Log warning with card IDs. |
| Duplicate card IDs | Raise `ValueError` — card IDs must be unique. |

**Unit Tests**
| Test | Scenario | Assertion |
|---|---|---|
| Two supporting cards | Card A supports Card B | Graph has 2 nodes, 1 support edge |
| Contradiction | Card A has `counter_hypothesis` matching Card B's hypothesis | Graph has contradiction edge from A to B |
| No relationships | Cards with empty `supports` and no `counter_hypothesis` | Graph has nodes only, no edges |
| Orphan reference | Card A supports "card_999" (doesn't exist) | Edge skipped, warning logged |
| Empty input | No cards | Empty graph returned |

---

### 3.8 Defense Agent

**Module:** `adversarial/defense_agent.py`

**Objective**
Challenge the dominant hypothesis with the strongest legitimate counter-explanation. Single pass, single LLM call. Adds at most one contradiction edge to the Evidence Graph.

**Inputs**
| Parameter | Type | Description |
|---|---|---|
| `case_file` | `CaseFile` | Current dominant hypothesis and evidence |
| `graph` | `nx.DiGraph` | Current Evidence Graph |
| `transactions` | `pd.DataFrame` | Transaction data (for the LLM to reference) |

**Outputs**
| Parameter | Type | Description |
|---|---|---|
| `graph` | `nx.DiGraph` | Evidence Graph with potential contradiction edge added |
| `defense_card` | `Optional[InvestigationCard]` | Defense card, if counter-explanation is plausible |

**Internal Workflow**
1. Read `dominant_hypothesis` and `dominant_confidence` from Case File.
2. Collect all supporting evidence from the graph for the dominant hypothesis.
3. Construct LLM prompt:
   ```
   The dominant hypothesis is: {dominant_hypothesis}
   Confidence: {dominant_confidence}
   Supporting evidence:
   {evidence_summary}
   Transaction data:
   {transaction_summary}

   Argue the strongest legitimate (innocent) explanation against this hypothesis.
   Consider: payroll patterns, seasonal business, known vendor relationships,
   cash-intensive business types, month-end settlement patterns.

   Respond with:
   - counter_explanation: the innocent explanation
   - plausibility: 0.0–1.0
   - reasoning: why this explanation fits the data
   ```
4. Parse LLM response.
5. If `plausibility > DEFENSE_PLAUSIBILITY_THRESHOLD`:
   - Create a defense Investigation Card.
   - Add a contradiction edge to the graph targeting the dominant hypothesis node.
   - Edge weight = `plausibility`.
6. If `plausibility ≤ DEFENSE_PLAUSIBILITY_THRESHOLD`:
   - No card or edge added. The dominant hypothesis stands unchallenged.
7. Return updated graph and optional defense card.

**Dependencies**
- `utils/ollama_client.py` — Ollama inference call for adversarial reasoning.
- `models/investigation_card.py` — card dataclass.
- `config/settings.py` — defense plausibility threshold.

**Error Handling**
| Failure | Response |
|---|---|
| LLM unavailable | Skip defense phase entirely. Log error. Add flag `defense_skipped = True` to Case File. |
| LLM response unparseable | Skip defense phase. Log error with raw response. |
| Case File has no dominant hypothesis | Skip defense — nothing to challenge. |

**Unit Tests**
| Test | Scenario | Assertion |
|---|---|---|
| Plausible counter | LLM returns `plausibility=0.65` (above threshold) | Contradiction edge added to graph |
| Implausible counter | LLM returns `plausibility=0.20` (below threshold) | No edge added |
| LLM failure | LLM call raises exception | Graph unchanged, `defense_skipped` flag set |
| Empty Case File | No dominant hypothesis | Defense skipped gracefully |

---

### 3.9 Tribunal (Consensus Engine)

**Module:** `tribunal/consensus_engine.py`

**Objective**
Reason over the Evidence Graph to identify the winning hypothesis, the runner-up, and the evidence that decided between them. Map confidence to an escalation recommendation. The Tribunal never reasons over raw transactions — only over the Case File and Evidence Graph.

**Inputs**
| Parameter | Type | Description |
|---|---|---|
| `graph` | `nx.DiGraph` | Complete Evidence Graph (post-defense) |
| `case_file` | `CaseFile` | Investigation context |

**Outputs**
| Parameter | Type | Description |
|---|---|---|
| `verdict` | `TribunalVerdict` | Complete verdict with reasoning |

**TribunalVerdict Schema**
```python
@dataclass
class TribunalVerdict:
    winning_hypothesis: str                 # Hypothesis with highest net support
    winning_confidence: float               # Net confidence after contradiction
    winning_chain: List[str]                # Ordered card IDs forming the evidence chain
    runner_up_hypothesis: Optional[str]     # Second-strongest hypothesis
    runner_up_confidence: Optional[float]   # Runner-up's net confidence
    rejection_reason: Optional[str]         # Why runner-up was rejected
    missing_evidence: List[str]             # Aggregated missing data from all cards
    risk_level: str                         # "low" | "medium" | "high"
    recommendation: str                     # "monitor" | "review" | "report"
    contradictions_applied: List[Dict]      # Contradiction edges that affected the verdict
```

**Internal Workflow**
1. **Collect all unique hypotheses** from graph nodes.
2. **For each hypothesis**, compute net support:
   - `support_total` = sum of weights on all incoming `"supports"` edges.
   - `contradiction_total` = sum of weights on all incoming `"contradicts"` edges.
   - `net_support` = base confidence + `support_total` − `contradiction_total`.
   - Clamp to `[0.0, 1.0]`.
3. **Rank hypotheses** by `net_support`.
4. **Winning hypothesis** = rank 1.
5. **Runner-up hypothesis** = rank 2 (if exists).
6. **Identify the deciding evidence**: the specific edge or card that created the gap between winner and runner-up.
7. **Aggregate missing evidence** from all cards' `missing_data` fields.
8. **Map confidence to risk level and recommendation:**
   - `confidence ≥ HIGH_RISK_THRESHOLD` → `risk_level = "high"`, `recommendation = "report"`
   - `confidence ≥ MEDIUM_RISK_THRESHOLD` → `risk_level = "medium"`, `recommendation = "review"`
   - `confidence < MEDIUM_RISK_THRESHOLD` → `risk_level = "low"`, `recommendation = "monitor"`
9. Return `TribunalVerdict`.

**Dependencies**
- `networkx` — graph traversal.
- `models/tribunal_verdict.py` — verdict dataclass.
- `config/settings.py` — risk thresholds.

**Error Handling**
| Failure | Response |
|---|---|
| Empty graph | Return verdict with `winning_hypothesis = "no_evidence"`, `recommendation = "monitor"`. |
| Single hypothesis (no competition) | Winner is the only hypothesis, no runner-up. |
| All hypotheses have net_support ≤ 0 | Winner is the least-negative, `recommendation = "monitor"`. |

**Unit Tests**
| Test | Scenario | Assertion |
|---|---|---|
| Clear winner | Structuring at 0.86, payroll at 0.42 | `winning_hypothesis = "structuring"`, `runner_up = "payroll"` |
| Winner after defense | Structuring at 0.82, defense contradiction at 0.30 | `winning_confidence ≈ 0.52`, adjusted by net support |
| Single hypothesis | Only structuring cards, no alternatives | Winner = structuring, no runner-up |
| Empty graph | No nodes | `winning_hypothesis = "no_evidence"`, `recommendation = "monitor"` |
| Threshold mapping | Confidence 0.90 | `risk_level = "high"`, `recommendation = "report"` |
| Threshold mapping | Confidence 0.65 | `risk_level = "medium"`, `recommendation = "review"` |
| Threshold mapping | Confidence 0.35 | `risk_level = "low"`, `recommendation = "monitor"` |

---

### 3.10 Report Generator

**Module:** `report/report_generator.py`

**Objective**
Transform the Tribunal's verdict into a structured, human-readable investigation report. This is the system's highest-leverage component — it is what a compliance analyst, auditor, or judge reads first.

**Inputs**
| Parameter | Type | Description |
|---|---|---|
| `verdict` | `TribunalVerdict` | Tribunal's structured output |
| `case_file` | `CaseFile` | Investigation context |
| `execution_plan` | `ExecutionPlan` | Which experts were invoked and why |
| `query_context` | `QueryContext` | Original query parameters |
| `all_cards` | `List[InvestigationCard]` | All investigation cards produced |

**Outputs**
| Parameter | Type | Description |
|---|---|---|
| `report` | `InvestigationReport` | Structured report object |

**InvestigationReport Schema**
```python
@dataclass
class InvestigationReport:
    query_recap: str                        # Original query restated
    experts_invoked: List[Dict[str, str]]   # [{name, reason}] for each expert
    experts_skipped: List[Dict[str, str]]   # [{name, reason}] for each skipped expert
    winning_hypothesis: str
    winning_confidence: float
    evidence_chain: str                     # Human-readable chain: card_001 → card_003
    runner_up_hypothesis: Optional[str]
    runner_up_confidence: Optional[float]
    rejection_reason: Optional[str]
    missing_evidence: List[str]
    risk_level: str
    recommendation: str
    full_text: str                          # Complete rendered report text
```

**Internal Workflow**
1. Reconstruct query recap from `QueryContext`.
2. Build expert invocation summary from `ExecutionPlan` — list each expert and why it was selected or skipped.
3. Build evidence chain narrative from `verdict.winning_chain` — translate card IDs to human-readable descriptions using card evidence fields.
4. Build runner-up section from verdict — explain why the alternative was rejected.
5. Collect missing evidence from verdict.
6. Assemble `full_text` following the report template:
   ```
   Investigation Summary
   Query: "{original_query}"
   Domains invoked: {expert_list} ({skipped_experts} — skipped because {reason})

   Winning Hypothesis: {hypothesis}
   Confidence: {confidence}%
   Supporting Evidence Chain: {card_chain}

   Runner-up Hypothesis: {runner_up} — {runner_up_confidence}% confidence
   Rejected because: {rejection_reason}

   Missing Evidence: {missing_evidence_list}

   Recommendation: {recommendation}
   ```
7. Return `InvestigationReport`.

**Dependencies**
- `models/tribunal_verdict.py` — verdict input.
- `models/investigation_card.py` — card details for narrative.

**Error Handling**
| Failure | Response |
|---|---|
| No runner-up | Omit runner-up section from report. |
| No missing evidence | State "No missing evidence identified." |
| Empty verdict | Generate report stating "Investigation produced insufficient evidence for a recommendation." |

**Unit Tests**
| Test | Scenario | Assertion |
|---|---|---|
| Full report | Complete verdict with winner, runner-up, missing data | All sections present in `full_text` |
| No runner-up | Single hypothesis verdict | Runner-up section absent, report still valid |
| No missing data | All cards have `missing_data = None` | Missing evidence section states "None identified" |
| Empty verdict | `winning_hypothesis = "no_evidence"` | Report communicates insufficient evidence |

---

## 4. Module Interaction Sequence

This section describes the exact software call chain. Every arrow is a function call. Every data label is a dataclass crossing a module boundary.

```
pipeline.run(query: str)
│
├── 1. planner.query_parser.parse(query)              # LANGUAGE UNDERSTANDING LAYER
│       → InvestigationPlan
│
╞═════════════════════════════════════════════  # ANALYTICAL LAYER (deterministic)
│
├── 2. planner.execution_planner.plan(investigation_plan)
│       → ExecutionPlan
│
├── 3. models.case_file.CaseFile()        # Initialize empty
│       → CaseFile
│
├── 4. [if execution_plan.run_eda]
│       tools.eda_tool.profile(transactions, filters)
│       → eda_summary (logged, not passed further)
│
├── 5. FOR expert_id IN execution_plan.expert_sequence:
│   │
│   ├── 5a. experts.{expert_id}.investigate(transactions, case_file, execution_plan)
│   │       → (List[InvestigationCard], CaseFile)
│   │
│   └── 5b. all_cards.extend(new_cards)
│            case_file = updated_case_file
│
├── 6. investigation.graph_builder.build(all_cards)
│       → nx.DiGraph
│
├── 7. adversarial.defense_agent.challenge(case_file, graph, transactions)
│       → (nx.DiGraph, Optional[InvestigationCard])
│       if defense_card: all_cards.append(defense_card)
│
├── 8. [ADAPTIVE CYCLE — BOUNDED]
│       IF case_file.dominant_confidence < REINVESTIGATION_THRESHOLD:
│           next_expert = select_from_priority_list()
│           expert.investigate(transactions, case_file, execution_plan)
│           → new_cards, updated_case_file
│           graph = graph_builder.rebuild(all_cards)    # Rebuild with new cards
│       STOP regardless of outcome.
│
├── 9. tribunal.consensus_engine.resolve(graph, case_file)
│       → TribunalVerdict
│
├── 10. report.report_generator.generate(verdict, case_file, execution_plan, investigation_plan, all_cards)
│        → InvestigationReport
│
└── return InvestigationReport
```

### Key Sequencing Rules

1. **No module calls another module directly.** All wiring flows through `pipeline.py`.
2. **The Case File is passed by reference.** Each expert reads and potentially mutates it. The pipeline enforces sequential execution — no concurrent writes.
3. **The graph is built once, then potentially modified twice** — once by the Defense Agent (adding a contradiction edge), and once by the adaptive cycle (adding new cards). If the adaptive cycle fires, the graph is rebuilt from scratch with the expanded card set.
4. **The Tribunal receives the final graph.** It never sees intermediate states.

---

## 5. Internal Algorithms

### 5.1 Query Parser — Query Understanding

```
ALGORITHM: ParseQuery(query)

INPUT:  query (string)
OUTPUT: InvestigationPlan

1. Construct extraction prompt with query and field definitions
2. Call Ollama with extraction prompt
3. Parse model response as JSON
4. FOR each field in InvestigationPlan:
     IF field present in response AND valid:
       Set field from response
     ELSE:
       Set field to default value
5. IF intent not in {"pattern_detection", "broad_scan", "compliance_check"}:
     Set intent = "broad_scan"
6. IF date_range missing:
     Set date_range = (today - 30 days, today)
7. IF experts list empty:
     Determine expert sequence from intent and target_pattern
8. RETURN InvestigationPlan

FALLBACK (if Ollama unavailable):
1. Search query for known pattern keywords: "structuring", "smurfing", "velocity", "unusual"
2. Search for customer ID pattern: "customer \d+"
3. Search for date expressions: "last N days", "this quarter"
4. Construct InvestigationPlan from regex matches
5. RETURN InvestigationPlan
```

---

### 5.2 Execution Planner — Plan Finalization

```
ALGORITHM: FinalizePlan(investigation_plan)

INPUT:  InvestigationPlan
OUTPUT: ExecutionPlan

1. SET run_eda = investigation_plan.run_eda
2. SET expert_sequence = investigation_plan.experts

3. IF expert_sequence is empty:
     IF investigation_plan.intent == "broad_scan":
       SET run_eda = TRUE

4.   IF investigation_plan.target_pattern IN {"structuring", "smurfing", "velocity"}:
       APPEND "financial" to expert_sequence
       APPEND "behaviour" to expert_sequence
5.   ELSE IF investigation_plan.target_pattern IN {"deviation", "anomaly"}:
     APPEND "behaviour" to expert_sequence
     APPEND "financial" to expert_sequence
6.   ELSE:
       APPEND "financial" to expert_sequence  # Default order
       APPEND "behaviour" to expert_sequence

7. Resolve filter parameters into concrete query constraints
8. Construct rationale string explaining selections
9. RETURN ExecutionPlan(run_eda, expert_sequence, target_pattern, filters, rationale)
```

---

### 5.3 Feature Engineering — AML Feature Computation

```
ALGORITHM: ComputeFeatures(transactions, customer_id, window_days)

INPUT:  transactions (DataFrame), customer_id (string), window_days (int)
OUTPUT: feature dictionary

1. LOAD historical transactions for customer_id (prior 90 days)
2. COMPUTE baseline_daily_volume = historical total / historical days
3. COMPUTE baseline_mean_amount = mean of historical amounts

4. FILTER transactions to window_days
5. IF filtered transactions empty:
     RETURN all-zero feature dictionary

6. COMPUTE rolling_sum_7d  = rolling sum over 7-day windows
7. COMPUTE rolling_sum_30d = rolling sum over 30-day windows
8. COMPUTE txn_velocity    = count(transactions) / window_days
9. COMPUTE amount_mean     = mean(amounts)
10. COMPUTE amount_std     = std(amounts)
11. COMPUTE amount_deviation = (amount_mean - baseline_mean_amount) / baseline_mean_amount

12. SET reporting_threshold = config.REPORTING_THRESHOLD
13. SET structuring_margin  = config.STRUCTURING_MARGIN
14. COMPUTE sub_threshold_count = count where amount IN [threshold - margin, threshold)
15. COMPUTE sub_threshold_ratio = sub_threshold_count / total_count

16. COMPUTE daily_volume_change_pct = ((current_daily_volume - baseline_daily_volume) / baseline_daily_volume) * 100

17. COMPUTE unique_beneficiaries = count distinct counterparties
18. COMPUTE weekend_txn_ratio    = weekend_count / total_count

19. RETURN feature dictionary
```

---

### 5.4 Financial Expert — Structuring Detection

```
ALGORITHM: InvestigateFinancialPatterns(transactions, case_file, plan)

INPUT:  transactions (DataFrame), case_file (CaseFile), plan (ExecutionPlan)
OUTPUT: cards (List[InvestigationCard]), updated case_file

1. features = ComputeFeatures(transactions, customer_id, window_days)
2. cards = []
3. card_counter = global_counter.next()

4. --- STRUCTURING CHECK ---
   IF features.sub_threshold_ratio > config.STRUCTURING_RATIO_THRESHOLD:
     confidence = min(features.sub_threshold_ratio * 1.1, 0.95)
     card = InvestigationCard(
       card_id = f"card_{card_counter}",
       source_expert = "financial_pattern",
       hypothesis = "structuring",
       confidence = confidence,
       evidence = f"{features.sub_threshold_count} transactions within ${config.STRUCTURING_MARGIN} of ${config.REPORTING_THRESHOLD} threshold",
       counter_hypothesis = "cash_intensive_business",
       missing_data = "merchant_category"
     )
     cards.append(card)

5. --- VELOCITY CHECK ---
   IF features.daily_volume_change_pct > config.VELOCITY_SPIKE_THRESHOLD:
     confidence = min(features.daily_volume_change_pct / 1000, 0.90)
     card = InvestigationCard(
       card_id = f"card_{card_counter}",
       hypothesis = "velocity_anomaly",
       confidence = confidence,
       evidence = f"{features.daily_volume_change_pct}% daily volume increase vs. baseline",
       counter_hypothesis = "seasonal_business",
       missing_data = "business_calendar"
     )
     cards.append(card)

6. --- STATISTICAL OUTLIER CHECK ---
   anomaly_result = AnomalyDetection.detect(transactions, features)
   IF anomaly_result.overall_anomaly_score > config.ANOMALY_THRESHOLD:
     card = InvestigationCard(
       card_id = f"card_{card_counter}",
       hypothesis = "statistical_anomaly",
       confidence = anomaly_result.overall_anomaly_score,
       evidence = f"{anomaly_result.outlier_count} statistical outliers detected",
       counter_hypothesis = "legitimate_large_transaction",
       missing_data = "transaction_purpose"
     )
     cards.append(card)

7. --- UPDATE CASE FILE ---
   IF cards not empty:
     dominant = max(cards, key=lambda c: c.confidence)
     case_file.dominant_hypothesis = dominant.hypothesis
     case_file.dominant_confidence = dominant.confidence
     case_file.open_question = f"does behaviour history support or undercut {dominant.hypothesis}?"

8. RETURN cards, case_file
```

---

### 5.5 Behaviour Expert — Deviation Analysis

```
ALGORITHM: InvestigateBehaviourPatterns(transactions, case_file, plan)

INPUT:  transactions (DataFrame), case_file (CaseFile), plan (ExecutionPlan)
OUTPUT: cards (List[InvestigationCard]), updated case_file

1. READ case_file.dominant_hypothesis, case_file.dominant_confidence
2. features = ComputeFeatures(transactions, customer_id, window_days=90)
3. cards = []

4. --- HISTORICAL DEVIATION CHECK ---
   IF features.daily_volume_change_pct > config.BEHAVIOUR_DEVIATION_THRESHOLD:
     IF case_file.dominant_hypothesis == "structuring":
       # Check if sub-threshold clustering is NEW (not in historical window)
       historical_sub_threshold = compute_historical_sub_threshold_ratio()
       current_sub_threshold = features.sub_threshold_ratio
       IF current_sub_threshold >> historical_sub_threshold:
         evidence = "Sub-threshold clustering is a recent pattern, not historical"
         confidence_boost = 0.10
       ELSE:
         evidence = "Sub-threshold pattern exists in historical data — may be normal"
         confidence_boost = -0.05

     card = InvestigationCard(
       card_id = f"card_{card_counter}",
       source_expert = "customer_behaviour",
       hypothesis = case_file.dominant_hypothesis,  # Supporting or refining
       confidence = min(case_file.dominant_confidence + confidence_boost, 0.95),
       evidence = f"{features.daily_volume_change_pct}% volume deviation. {evidence}",
       supports = [card for card matching dominant hypothesis]
     )
     cards.append(card)

5. --- PROFILE CONTEXT CHECK (if data available) ---
   IF profile_data available:
     IF declared_income * 12 < total_transaction_volume * config.INCOME_MISMATCH_FACTOR:
       card = InvestigationCard(
         hypothesis = "profile_mismatch",
         confidence = 0.70,
         evidence = f"Declared income ${declared_income}/yr vs. transaction volume ${total_volume}",
         missing_data = "updated_income_declaration"
       )
       cards.append(card)

6. --- UPDATE CASE FILE (only if stronger) ---
   IF cards not empty:
     strongest = max(cards, key=lambda c: c.confidence)
     IF strongest.confidence > case_file.dominant_confidence:
       case_file.dominant_hypothesis = strongest.hypothesis
       case_file.dominant_confidence = strongest.confidence

7. RETURN cards, case_file
```

---

### 5.6 Evidence Graph — Construction

```
ALGORITHM: BuildEvidenceGraph(cards)

INPUT:  cards (List[InvestigationCard])
OUTPUT: graph (nx.DiGraph)

1. graph = nx.DiGraph()

2. FOR each card in cards:
     graph.add_node(card.card_id, **card.to_dict())

3. FOR each card in cards:
     FOR each supported_id in card.supports:
       IF supported_id in graph.nodes:
         graph.add_edge(card.card_id, supported_id,
           relation = "supports",
           weight = card.confidence,
           reason = f"{card.card_id} corroborates {supported_id}"
         )
       ELSE:
         LOG warning: f"Card {card.card_id} references non-existent {supported_id}"

4. FOR each card in cards:
     IF card.counter_hypothesis is not None:
       FOR each other_card in cards:
         IF other_card.hypothesis == card.counter_hypothesis AND other_card.card_id != card.card_id:
           graph.add_edge(card.card_id, other_card.card_id,
             relation = "contradicts",
             weight = 1.0 - card.confidence,
             reason = f"{card.hypothesis} counters {other_card.hypothesis}"
           )

5. RETURN graph
```

---

### 5.7 Defense Agent — Adversarial Challenge

```
ALGORITHM: ChallengeHypothesis(case_file, graph, transactions)

INPUT:  case_file (CaseFile), graph (nx.DiGraph), transactions (DataFrame)
OUTPUT: graph (nx.DiGraph), defense_card (Optional[InvestigationCard])

1. IF case_file.dominant_hypothesis is None:
     RETURN graph, None

2. Collect evidence supporting dominant hypothesis from graph
3. Summarize transaction patterns relevant to hypothesis

4. Construct LLM prompt with:
   - Dominant hypothesis and confidence
   - Supporting evidence summary
   - Transaction pattern summary
   - Instruction to argue strongest innocent counter-explanation

5. Call LLM
6. Parse response → {counter_explanation, plausibility, reasoning}

7. IF plausibility > config.DEFENSE_PLAUSIBILITY_THRESHOLD:
     defense_card = InvestigationCard(
       source_expert = "defense",
       hypothesis = counter_explanation,
       confidence = plausibility,
       evidence = reasoning,
       counter_hypothesis = case_file.dominant_hypothesis
     )
     graph.add_node(defense_card.card_id, **defense_card.to_dict())

     # Find dominant hypothesis node
     dominant_node = find_node_by_hypothesis(graph, case_file.dominant_hypothesis)
     graph.add_edge(defense_card.card_id, dominant_node,
       relation = "contradicts",
       weight = plausibility,
       reason = reasoning
     )
     RETURN graph, defense_card

8. ELSE:
     RETURN graph, None
```

---

### 5.8 Tribunal — Consensus Resolution

```
ALGORITHM: ResolveVerdict(graph, case_file)

INPUT:  graph (nx.DiGraph), case_file (CaseFile)
OUTPUT: TribunalVerdict

1. IF graph has no nodes:
     RETURN TribunalVerdict(winning_hypothesis="no_evidence", recommendation="monitor")

2. --- COLLECT UNIQUE HYPOTHESES ---
   hypotheses = {node.hypothesis for node in graph.nodes}

3. --- COMPUTE NET SUPPORT PER HYPOTHESIS ---
   FOR each hypothesis h:
     base_cards = [node for node in graph if node.hypothesis == h]
     base_confidence = max(card.confidence for card in base_cards)

     support_total = 0
     FOR each edge targeting any base_card WHERE relation == "supports":
       support_total += edge.weight

     contradiction_total = 0
     contradictions_applied = []
     FOR each edge targeting any base_card WHERE relation == "contradicts":
       contradiction_total += edge.weight
       contradictions_applied.append(edge)

     net_support[h] = clamp(base_confidence + support_total - contradiction_total, 0.0, 1.0)

4. --- RANK HYPOTHESES ---
   ranked = sort hypotheses by net_support descending

5. --- DETERMINE WINNER ---
   winner = ranked[0]
   winning_confidence = net_support[winner]
   winning_chain = trace_support_path(graph, winner)  # Ordered card IDs

6. --- DETERMINE RUNNER-UP ---
   IF len(ranked) > 1:
     runner_up = ranked[1]
     runner_up_confidence = net_support[runner_up]
     rejection_reason = identify_deciding_evidence(graph, winner, runner_up)
   ELSE:
     runner_up = None

7. --- AGGREGATE MISSING EVIDENCE ---
   missing = [node.missing_data for node in graph.nodes if node.missing_data is not None]

8. --- MAP TO RISK LEVEL ---
   IF winning_confidence >= config.HIGH_RISK_THRESHOLD:
     risk_level = "high"
     recommendation = "report"
   ELSE IF winning_confidence >= config.MEDIUM_RISK_THRESHOLD:
     risk_level = "medium"
     recommendation = "review"
   ELSE:
     risk_level = "low"
     recommendation = "monitor"

9. RETURN TribunalVerdict(...)
```

---

### 5.9 Report Generator — Narrative Assembly

```
ALGORITHM: GenerateReport(verdict, case_file, plan, query_context, cards)

INPUT:  TribunalVerdict, CaseFile, ExecutionPlan, QueryContext, List[InvestigationCard]
OUTPUT: InvestigationReport

1. --- QUERY RECAP ---
   query_recap = f'Query: "{query_context.raw_query}"'

2. --- EXPERTS INVOKED ---
   experts_invoked = []
   FOR each expert_id in plan.expert_sequence:
     experts_invoked.append({name: expert_id, reason: plan.rationale})
   experts_skipped = [experts not in plan.expert_sequence with reasons]

3. --- EVIDENCE CHAIN ---
   chain_parts = []
   FOR each card_id in verdict.winning_chain:
     card = find_card(cards, card_id)
     chain_parts.append(f"{card_id} ({card.evidence})")
   evidence_chain = " → ".join(chain_parts)

4. --- RUNNER-UP ---
   IF verdict.runner_up_hypothesis:
     runner_up_text = f"{verdict.runner_up_hypothesis} ({verdict.runner_up_confidence}%) — {verdict.rejection_reason}"
   ELSE:
     runner_up_text = None

5. --- MISSING EVIDENCE ---
   missing_text = verdict.missing_evidence or ["None identified"]

6. --- ASSEMBLE FULL TEXT ---
   full_text = render_template(
     query_recap,
     experts_invoked,
     experts_skipped,
     verdict.winning_hypothesis,
     verdict.winning_confidence,
     evidence_chain,
     runner_up_text,
     missing_text,
     verdict.recommendation
   )

7. RETURN InvestigationReport(full_text=full_text, ...)
```

---

## 6. Configuration

All configurable values are centralized in `config/settings.py`. No threshold, path, or parameter is hardcoded anywhere in the codebase.

### 6.1 Risk Thresholds

```python
# Confidence → risk mapping
HIGH_RISK_THRESHOLD = 0.80           # Confidence ≥ 80% → high risk → "report"
MEDIUM_RISK_THRESHOLD = 0.50         # Confidence ≥ 50% → medium risk → "review"
# Below 50% → low risk → "monitor"
```

### 6.2 Structuring Detection

```python
REPORTING_THRESHOLD = 10_000         # Currency reporting threshold (e.g., $10,000 USD)
STRUCTURING_MARGIN = 500             # Range below threshold considered suspicious ($9,500–$10,000)
STRUCTURING_RATIO_THRESHOLD = 0.40   # If 40%+ of transactions are sub-threshold → structuring signal
```

### 6.3 Velocity Detection

```python
VELOCITY_SPIKE_THRESHOLD = 200       # % increase vs. baseline to flag as velocity anomaly
ROLLING_WINDOW_7D = 7                # Short rolling window in days
ROLLING_WINDOW_30D = 30              # Long rolling window in days
BASELINE_WINDOW_DAYS = 90            # Historical baseline window
```

### 6.4 Anomaly Detection

```python
ZSCORE_THRESHOLD = 2.5               # Z-score cutoff for outlier flagging
ISOLATION_FOREST_CONTAMINATION = 0.1 # Expected proportion of outliers
ISOLATION_FOREST_MIN_SAMPLES = 20    # Minimum samples required to run Isolation Forest
```

### 6.5 Behaviour Expert

```python
BEHAVIOUR_DEVIATION_THRESHOLD = 100  # % deviation from baseline to flag
INCOME_MISMATCH_FACTOR = 3           # Transaction volume > N× declared income → flag
```

### 6.6 Defense Agent

```python
DEFENSE_PLAUSIBILITY_THRESHOLD = 0.40  # Minimum plausibility to add contradiction edge
```

### 6.7 Adaptive Cycle

```python
REINVESTIGATION_THRESHOLD = 0.70     # Confidence below this triggers re-investigation
REINVESTIGATION_PRIORITY_LIST = [    # Ordered expert list for adaptive cycle
    "network",                       # Network intelligence (beneficiary count)
]
```

### 6.8 Ollama Configuration

```python
OLLAMA_HOST = "http://localhost:11434" # Ollama server address
OLLAMA_MODEL = "llama3.2"              # Model name for query understanding
OLLAMA_TEMPERATURE = 0.3               # Low temperature for structured extraction
OLLAMA_TIMEOUT_SECONDS = 30            # Request timeout
```

### 6.9 Dataset Configuration

```python
DATASET_PATH = "datasets/"           # Path to transaction data
DATASET_FORMAT = "csv"               # Expected format
REQUIRED_COLUMNS = [                 # Columns that must exist
    "transaction_id",
    "customer_id",
    "amount",
    "date",
    "type",
]
```

### 6.10 Application

```python
APP_TITLE = "TRIBUNAL"
APP_SUBTITLE = "AI Investigation Board for AML Compliance"
LOG_LEVEL = "INFO"
LOG_FORMAT = "structured"            # "structured" (JSON) or "text"
CARD_ID_PREFIX = "card"
```

---

## 7. Logging Strategy

Every module emits structured logs at defined points. Logs serve two purposes: debugging during development and transparency during demonstrations.

### Log Format

All logs are emitted as structured JSON via `utils/logger.py`:

```json
{
  "timestamp": "2026-07-24T15:22:10.432Z",
  "level": "INFO",
  "module": "financial_expert",
  "event": "card_generated",
  "data": {
    "card_id": "card_001",
    "hypothesis": "structuring",
    "confidence": 0.82
  }
}
```

### Log Events by Module

#### Query Understanding & Planning
| Event | Level | Data | When |
|---|---|---|---|
| `query_received` | INFO | `{raw_query}` | Query enters the system |
| `query_parsed` | INFO | `{intent, target_pattern, customer_id, date_range, experts, run_eda}` | Query parser completes |
| `plan_constructed` | INFO | `{run_eda, expert_sequence, rationale}` | Execution plan finalized |
| `query_parse_fallback` | WARN | `{reason, raw_query}` | Ollama unavailable, regex fallback used |

#### Experts
| Event | Level | Data | When |
|---|---|---|---|
| `expert_started` | INFO | `{expert_id, dominant_hypothesis_in}` | Expert begins investigation |
| `features_computed` | DEBUG | `{feature_summary}` | Feature engineering completes |
| `card_generated` | INFO | `{card_id, hypothesis, confidence}` | Investigation Card emitted |
| `case_file_updated` | INFO | `{dominant_hypothesis, dominant_confidence}` | Case File changed |
| `expert_completed` | INFO | `{expert_id, cards_count, dominant_hypothesis_out}` | Expert finishes |
| `no_evidence_found` | WARN | `{expert_id, reason}` | Expert produces no meaningful cards |

#### Evidence Graph
| Event | Level | Data | When |
|---|---|---|---|
| `graph_built` | INFO | `{node_count, support_edges, contradiction_edges}` | Graph construction completes |
| `orphan_reference` | WARN | `{card_id, referenced_id}` | Card references non-existent ID |

#### Defense Agent
| Event | Level | Data | When |
|---|---|---|---|
| `defense_started` | INFO | `{dominant_hypothesis, dominant_confidence}` | Defense begins |
| `defense_result` | INFO | `{counter_explanation, plausibility, edge_added}` | Defense completes |
| `defense_skipped` | WARN | `{reason}` | Defense was skipped (LLM failure, no hypothesis) |

#### Tribunal
| Event | Level | Data | When |
|---|---|---|---|
| `verdict_computed` | INFO | `{winning_hypothesis, confidence, runner_up, recommendation}` | Tribunal reaches verdict |
| `contradiction_applied` | DEBUG | `{source_card, target_card, weight}` | Contradiction edge affected verdict |

#### Adaptive Cycle
| Event | Level | Data | When |
|---|---|---|---|
| `reinvestigation_triggered` | INFO | `{confidence, threshold, next_expert}` | Confidence below threshold |
| `reinvestigation_skipped` | INFO | `{confidence, threshold}` | Confidence above threshold |

#### Report Generator
| Event | Level | Data | When |
|---|---|---|---|
| `report_generated` | INFO | `{recommendation, sections_count}` | Report assembly completes |

#### Pipeline
| Event | Level | Data | When |
|---|---|---|---|
| `pipeline_started` | INFO | `{query}` | Pipeline execution begins |
| `pipeline_completed` | INFO | `{recommendation, total_cards, total_time_ms}` | Pipeline finishes |
| `pipeline_error` | ERROR | `{stage, error_message, traceback}` | Unrecovered error |

---

## 8. Error Handling

TRIBUNAL is designed to degrade gracefully. No single component failure should crash the pipeline. The system should always produce a report — even if that report states "insufficient evidence."

### 8.1 Error Hierarchy

```
CRITICAL   → Pipeline cannot continue. Log error and return failure report.
DEGRADED   → Component failed but pipeline can continue with reduced capability.
WARNING    → Unexpected condition, but output is valid.
```

### 8.2 Failure Scenarios and Responses

| Scenario | Severity | Response |
|---|---|---|
| **Dataset missing or unreadable** | CRITICAL | Log error. Return report: "Investigation could not proceed — dataset unavailable." |
| **Required columns missing from dataset** | CRITICAL | Log error with column names. Return failure report. |
| **Malformed or empty query** | DEGRADED | Intent parser defaults to `broad_scan`. Log warning. Pipeline continues. |
| **LLM unavailable (intent parsing)** | DEGRADED | Fall back to regex extraction. Log degraded mode. Pipeline continues. |
| **LLM unavailable (defense agent)** | DEGRADED | Skip defense phase. Set `defense_skipped = True`. Log warning. Pipeline continues without adversarial challenge. |
| **LLM unavailable (report phrasing)** | DEGRADED | Use template-based report without LLM polishing. |
| **Expert returns no cards** | DEGRADED | Log warning. Continue to next expert. If all experts return no cards, Tribunal receives empty graph. |
| **All experts return no cards** | WARNING | Tribunal produces `winning_hypothesis = "no_evidence"`, `recommendation = "monitor"`. Report states insufficient evidence. |
| **Evidence Graph is empty** | WARNING | Tribunal produces default low-risk verdict. Report explains no evidence was gathered. |
| **Feature engineering fails** | DEGRADED | Expert skips derived feature checks, runs only with raw data available. Log error. |
| **Anomaly detection fails** | DEGRADED | Financial Expert skips statistical layer, runs rule-based checks only. Log error. |
| **Defense agent counter-explanation implausible** | WARNING | No contradiction edge added. Graph unchanged. Pipeline continues. |
| **Adaptive cycle expert not available** | WARNING | Skip adaptive cycle. Proceed to Tribunal. |
| **Graph builder receives duplicate card IDs** | CRITICAL (within module) | Raise `ValueError`. Pipeline catches, assigns new IDs, rebuilds. |

### 8.3 Error Propagation Pattern

Every module follows the same error pattern:

```python
def investigate(self, transactions, case_file, plan):
    try:
        # Core logic
        ...
        return cards, case_file
    except DataError as e:
        logger.error("expert_data_error", expert=self.id, error=str(e))
        return [], case_file  # Return empty cards, unchanged case file
    except LLMError as e:
        logger.error("expert_llm_error", expert=self.id, error=str(e))
        return self._fallback_investigation(transactions, case_file)
    except Exception as e:
        logger.critical("expert_unexpected_error", expert=self.id, error=str(e))
        raise  # Pipeline-level handler catches this
```

The pipeline wraps each module call:

```python
try:
    cards, case_file = expert.investigate(transactions, case_file, plan)
except Exception as e:
    logger.critical("pipeline_stage_failure", stage=expert.id, error=str(e))
    # Continue to next stage with what we have
```

---

## 9. Testing Strategy

### 9.1 Test Layers

```
Unit Tests         → Individual module correctness
                      Every public function in every module.
                      Mocked dependencies.
                      Fast, isolated, deterministic.
        ↓
Integration Tests  → Module interaction correctness
                      Two or more modules working together.
                      Real data structures, mocked external services (LLM).
        ↓
End-to-End Tests   → Full pipeline correctness
                      Query in, report out.
                      Known dataset with expected outcomes.
                      LLM calls mocked with fixed responses.
```

### 9.2 Unit Test Coverage

| Module | Test File | Key Test Cases |
|---|---|---|
| Intent Parser | `tests/unit/test_intent_parser.py` | Targeted query, broad scan, malformed input, missing fields, date parsing |
| Execution Planner | `tests/unit/test_execution_planner.py` | EDA decision, expert ordering by pattern type, unknown intent fallback |
| Feature Engineering | `tests/unit/test_feature_engineering.py` | Rolling sums, velocity, sub-threshold ratio, empty data, missing columns |
| Anomaly Detection | `tests/unit/test_anomaly_detection.py` | Z-score outliers, Isolation Forest, small dataset fallback, identical amounts |
| Financial Expert | `tests/unit/test_financial_expert.py` | Structuring detection, velocity spike, mixed signals, no data, card count |
| Behaviour Expert | `tests/unit/test_behaviour_expert.py` | Supporting hypothesis, contradicting hypothesis, no history, profile mismatch |
| Graph Builder | `tests/unit/test_graph_builder.py` | Support edges, contradiction edges, orphan references, empty input, duplicates |
| Defense Agent | `tests/unit/test_defense_agent.py` | Plausible counter, implausible counter, LLM failure, empty case file |
| Consensus Engine | `tests/unit/test_consensus_engine.py` | Clear winner, post-defense adjustment, single hypothesis, empty graph, threshold mapping |
| Report Generator | `tests/unit/test_report_generator.py` | Full report, no runner-up, no missing data, empty verdict |

### 9.3 Integration Tests

| Test | Modules Covered | Scenario |
|---|---|---|
| Expert Pipeline | Financial Expert → Behaviour Expert → Case File | Verify Case File carries hypothesis between experts correctly |
| Graph to Verdict | Graph Builder → Defense Agent → Consensus Engine | Verify defense contradiction affects verdict calculation |
| Plan to Execution | Intent Parser → Execution Planner → Expert Selection | Verify different queries produce different expert sequences |

### 9.4 End-to-End Tests

| Test | Input | Expected Output |
|---|---|---|
| Structuring detection | `"Find structuring in the last 30 days for customer 541"` with known structuring data | Report with `winning_hypothesis = "structuring"`, `recommendation = "review"` or `"report"` |
| Broad scan | `"Show unusual patterns across high-risk accounts"` with mixed data | Report with EDA invoked, multiple experts, valid recommendation |
| Clean customer | `"Check customer 200"` with normal transaction data | Report with `recommendation = "monitor"` |
| Edge case: empty data | Query targeting non-existent customer | Report stating "insufficient evidence" |

### 9.5 Test Fixtures

A shared test fixtures module provides:

```python
# tests/fixtures.py

def make_structuring_transactions(count=12, amount_range=(9700, 9900)):
    """Generate transactions that exhibit structuring patterns."""

def make_normal_transactions(count=50):
    """Generate transactions with no suspicious patterns."""

def make_velocity_spike(baseline_per_day=5, spike_per_day=30, spike_days=2):
    """Generate transactions with a velocity spike."""

def make_case_file(hypothesis="structuring", confidence=0.82):
    """Generate a pre-populated Case File."""

def make_investigation_card(card_id="card_001", hypothesis="structuring", confidence=0.82):
    """Generate a single Investigation Card."""

def mock_llm_response(counter_explanation="payroll", plausibility=0.65):
    """Generate a mock LLM response for defense agent testing."""
```

### 9.6 Running Tests

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run integration tests
pytest tests/integration/ -v

# Run end-to-end tests
pytest tests/e2e/ -v

# Run all tests with coverage
pytest --cov=tribunal --cov-report=term-missing

# Run specific module tests
pytest tests/unit/test_financial_expert.py -v
```

---

## 10. Implementation Milestones

Development proceeds in six stages. Each stage produces a working, testable artifact. No stage depends on a later stage — if development stops at any point, the completed stages form a functioning partial system.

### Stage 1 — Core Models

**Deliverable:** All shared data contracts in `models/`.

| Task | Output |
|---|---|
| Define `InvestigationPlan` dataclass | `models/investigation_plan.py` |
| Define `ExecutionPlan` dataclass | `models/execution_plan.py` |
| Define `CaseFile` dataclass | `models/case_file.py` |
| Define `InvestigationCard` dataclass | `models/investigation_card.py` |
| Define `TribunalVerdict` dataclass | `models/tribunal_verdict.py` |
| Define `InvestigationReport` dataclass | `models/investigation_report.py` |
| Define `AnomalyResult` dataclass | `tools/anomaly_detection.py` (inline) |
| Set up `config/settings.py` | All configurable values with defaults |
| Set up `utils/logger.py` | Structured logging utility |
| Set up `utils/ollama_client.py` | Ollama inference wrapper |

**Verification:** All dataclasses instantiate correctly. Config loads. Logger writes structured output. Ollama client connects successfully.

---

### Stage 2 — Planner

**Deliverable:** Query parser and execution planner.

| Task | Output |
|---|---|
| Implement query parser (Ollama + regex fallback) | `planner/query_parser.py` |
| Implement execution plan construction | `planner/execution_planner.py` |
| Implement planner orchestrator | `planner/planner.py` |
| Unit tests for all modules | `tests/unit/test_query_parser.py`, `test_execution_planner.py` |

**Verification:** Different queries produce visibly different execution plans. At minimum, a targeted query skips EDA and a broad query includes it. Query parser produces correct `InvestigationPlan` from natural language.

---

### Stage 3 — Experts + Tools

**Deliverable:** Feature engineering, anomaly detection, Financial Expert, Behaviour Expert.

| Task | Output |
|---|---|
| Implement feature engineering | `tools/feature_engineering.py` |
| Implement anomaly detection | `tools/anomaly_detection.py` |
| Implement EDA tool | `tools/eda_tool.py` |
| Implement Financial Expert | `experts/financial_expert.py` |
| Implement Behaviour Expert | `experts/behaviour_expert.py` |
| Define base expert interface | `experts/base_expert.py` |
| Unit tests for all modules | `tests/unit/test_*.py` |

**Verification:** Financial Expert produces Investigation Cards from known structuring data. Behaviour Expert reads Case File and produces supporting/contradicting cards. Cards have correct schema and provenance.

---

### Stage 4 — Evidence Graph + Defense

**Deliverable:** Graph builder, defense agent.

| Task | Output |
|---|---|
| Implement graph builder | `investigation/graph_builder.py` |
| Implement defense agent | `adversarial/defense_agent.py` |
| Unit tests for both modules | `tests/unit/test_graph_builder.py`, `test_defense_agent.py` |
| Integration test: graph → defense | `tests/integration/test_graph_to_verdict.py` (partial) |

**Verification:** Cards translate into correct graph nodes and edges. Defense agent adds contradiction edge when plausible. Graph remains unchanged when counter-explanation is weak.

---

### Stage 5 — Tribunal + Report

**Deliverable:** Consensus engine, report generator, full pipeline orchestrator.

| Task | Output |
|---|---|
| Implement consensus engine | `tribunal/consensus_engine.py` |
| Implement report generator | `report/report_generator.py` |
| Implement pipeline orchestrator | `pipeline.py` |
| Unit tests for consensus and report | `tests/unit/test_consensus_engine.py`, `test_report_generator.py` |
| Integration test: graph → verdict | `tests/integration/test_graph_to_verdict.py` (complete) |
| End-to-end test | `tests/e2e/test_full_pipeline.py` |

**Verification:** Full pipeline runs: query in, report out. Known structuring data produces correct winning hypothesis and recommendation. Report contains all required sections.

---

### Stage 6 — Interface

**Deliverable:** Working Streamlit demo.

| Task | Output |
|---|---|
| Implement Streamlit chat interface | `app.py`, `ui/components.py` |
| Integrate pipeline into UI | Pipeline called on query submission |
| Display investigation log, evidence graph, report | UI components for each |
| Test with 2–3 demo queries | Live verification |

**Verification:** User types a query. UI displays the execution plan, the expert invocations, the evidence graph, and the final report. Different queries produce visibly different investigation paths.

---

### Milestone Summary

```
Stage 1 — Core Models          ██░░░░░░░░  Foundation
Stage 2 — Planner              ████░░░░░░  Agentic proof point
Stage 3 — Experts + Tools      ██████░░░░  Investigation capability
Stage 4 — Graph + Defense      ████████░░  Adversarial rigour
Stage 5 — Tribunal + Report    ██████████  Complete pipeline
Stage 6 — Interface            ██████████  Demoable product
```

Each stage is independently testable. Each builds on the previous. If time runs short, the system is functional after Stage 5 — Stage 6 is presentation, not logic.

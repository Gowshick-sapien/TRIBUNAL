# TRIBUNAL — Data Contracts

**Document Classification:** System Contract — Canonical Data Structures
**Version:** 1.0
**Companion Documents:**
- TRIBUNAL — Architecture Design Specification v1.0
- TRIBUNAL — Implementation Specification v1.0

---

> Every module boundary in TRIBUNAL communicates through these contracts.
> No component may invent its own schema for objects defined here.
> Python implementations live in `tribunal/models/`. This document is the source of truth.

---

## Table of Contents

1. [Contract Overview](#1-contract-overview)
2. [Input Layer](#2-input-layer)
3. [Planning Layer](#3-planning-layer)
4. [Investigation Layer](#4-investigation-layer)
5. [Evidence Graph Layer](#5-evidence-graph-layer)
6. [Decision Layer](#6-decision-layer)
7. [Output Layer](#7-output-layer)
8. [Tool Layer](#8-tool-layer)
9. [Composite Types](#9-composite-types)
10. [Enumerations & Constants](#10-enumerations--constants)
11. [Contract Flow Diagram](#11-contract-flow-diagram)

---

## 1. Contract Overview

### Design Rules

1. **Single source of truth.** All cross-module data structures are defined here and implemented in `tribunal/models/`.
2. **JSON-serializable where possible.** Every contract includes a JSON Schema for validation, logging, and API boundaries.
3. **Immutable inputs, mutable Case File.** Planning objects are produced once. The Case File is the only shared mutable state during expert execution.
4. **Provenance required.** Investigation Cards and graph nodes must record source expert, transaction IDs, and timestamp.
5. **No raw transactions past experts.** The Tribunal and Report Generator reason over structured artefacts only.

### Object Index

| Object | Layer | Producer | Consumer |
|---|---|---|---|
| `UserQuery` | Input | UI / CLI | Query Parser |
| `InvestigationPlan` | Planning | Query Parser | Execution Planner |
| `ExecutionPlan` | Planning | Execution Planner | Pipeline, Experts |
| `PlannerOutput` | Planning | Planner | Pipeline |
| `CaseFile` | Investigation | Experts, Defense | Experts, Defense, Tribunal, Report |
| `InvestigationCard` | Investigation | Experts, Defense | Graph Builder, Report |
| `ExpertResult` | Investigation | Experts | Pipeline |
| `EvidenceNode` | Graph | Graph Builder | Tribunal |
| `EvidenceEdge` | Graph | Graph Builder, Defense | Tribunal |
| `EvidenceGraph` | Graph | Graph Builder | Defense, Tribunal |
| `TribunalVerdict` | Decision | Tribunal | Report Generator |
| `InvestigationReport` | Output | Report Generator | UI |
| `QueryContext` | Output | Pipeline | Report Generator |
| `AnomalyResult` | Tool | Anomaly Detection | Financial Expert |
| `FeatureDictionary` | Tool | Feature Engineering | Experts |

---

## 2. Input Layer

### 2.1 UserQuery

**Purpose**
Wraps the raw natural-language input from the user. The single entry point into the language understanding layer.

**Fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | Yes | Raw natural-language query |
| `submitted_at` | `string` (ISO 8601) | No | Timestamp of submission |
| `session_id` | `string` | No | UI session identifier for logging |

**JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tribunal://contracts/UserQuery",
  "type": "object",
  "required": ["text"],
  "properties": {
    "text": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2000
    },
    "submitted_at": {
      "type": "string",
      "format": "date-time"
    },
    "session_id": {
      "type": "string"
    }
  },
  "additionalProperties": false
}
```

**Validation Rules**

- `text` must be non-empty after trimming whitespace.
- `text` longer than 2000 characters is rejected with a validation error.

**Example**

```json
{
  "text": "Find structuring during the last month for customer 541",
  "submitted_at": "2026-07-25T00:02:00+05:30",
  "session_id": "sess_abc123"
}
```

---

## 3. Planning Layer

### 3.1 InvestigationPlan

**Purpose**
Structured representation of the user's intent, extracted from natural language. Produced exclusively by the Query Parser. Consumed by the Execution Planner and Report Generator.

**Fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `raw_query` | `string` | Yes | Original query string (copied from UserQuery) |
| `intent` | `string` | Yes | Investigation intent category |
| `target_pattern` | `string \| null` | No | AML typology to focus on |
| `customer_id` | `string \| null` | No | Target customer identifier |
| `date_range` | `[date, date] \| null` | No | Start and end dates (inclusive) |
| `country` | `string \| null` | No | Geographic filter (ISO 3166-1 alpha-2) |
| `txn_type` | `string \| null` | No | Transaction type filter |
| `risk_level` | `string \| null` | No | Customer risk tier filter |
| `experts` | `string[]` | Yes | Ordered expert identifiers |
| `run_eda` | `boolean` | Yes | Whether to run EDA before experts |

**JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tribunal://contracts/InvestigationPlan",
  "type": "object",
  "required": ["raw_query", "intent", "experts", "run_eda"],
  "properties": {
    "raw_query": { "type": "string", "minLength": 1 },
    "intent": {
      "type": "string",
      "enum": ["pattern_detection", "broad_scan", "compliance_check"]
    },
    "target_pattern": {
      "type": ["string", "null"],
      "enum": ["structuring", "smurfing", "velocity", "anomaly", "deviation", null]
    },
    "customer_id": { "type": ["string", "null"] },
    "date_range": {
      "type": ["array", "null"],
      "items": { "type": "string", "format": "date" },
      "minItems": 2,
      "maxItems": 2
    },
    "country": { "type": ["string", "null"], "maxLength": 2 },
    "txn_type": { "type": ["string", "null"] },
    "risk_level": {
      "type": ["string", "null"],
      "enum": ["high", "medium", "low", null]
    },
    "experts": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["financial", "behaviour"]
      },
      "minItems": 0
    },
    "run_eda": { "type": "boolean" }
  },
  "additionalProperties": false
}
```

**Validation Rules**

- If `intent` is invalid or missing, default to `"broad_scan"`.
- If `date_range` is missing, default to last 30 days from execution date.
- If `experts` is empty, derive sequence from `intent` and `target_pattern` (see Execution Planner).
- `customer_id` when present must match pattern `^[A-Za-z0-9_-]+$`.

**Example**

```json
{
  "raw_query": "Find structuring in the last 30 days for customer 541",
  "intent": "pattern_detection",
  "target_pattern": "structuring",
  "customer_id": "541",
  "date_range": ["2026-06-25", "2026-07-25"],
  "country": null,
  "txn_type": null,
  "risk_level": null,
  "experts": ["financial", "behaviour"],
  "run_eda": false
}
```

---

### 3.2 ExecutionPlan

**Purpose**
Finalized, deterministic execution configuration. Translates the Investigation Plan into concrete pipeline instructions. No language model dependency.

**Fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `run_eda` | `boolean` | Yes | Whether EDA runs before experts |
| `expert_sequence` | `string[]` | Yes | Ordered expert identifiers to invoke |
| `target_pattern` | `string \| null` | No | Pattern focus carried from investigation plan |
| `filters` | `object` | Yes | Resolved data-loading constraints |
| `rationale` | `string` | Yes | Human-readable plan explanation |

**Filters Object Schema**

| Key | Type | Description |
|---|---|---|
| `customer_id` | `string \| null` | Resolved customer filter |
| `date_start` | `string (date)` | Resolved start date |
| `date_end` | `string (date)` | Resolved end date |
| `country` | `string \| null` | Geographic filter |
| `txn_type` | `string \| null` | Transaction type filter |
| `risk_level` | `string \| null` | Risk tier filter |

**JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tribunal://contracts/ExecutionPlan",
  "type": "object",
  "required": ["run_eda", "expert_sequence", "filters", "rationale"],
  "properties": {
    "run_eda": { "type": "boolean" },
    "expert_sequence": {
      "type": "array",
      "items": { "type": "string", "enum": ["financial", "behaviour"] },
      "minItems": 1
    },
    "target_pattern": { "type": ["string", "null"] },
    "filters": {
      "type": "object",
      "properties": {
        "customer_id": { "type": ["string", "null"] },
        "date_start": { "type": "string", "format": "date" },
        "date_end": { "type": "string", "format": "date" },
        "country": { "type": ["string", "null"] },
        "txn_type": { "type": ["string", "null"] },
        "risk_level": { "type": ["string", "null"] }
      },
      "required": ["date_start", "date_end"]
    },
    "rationale": { "type": "string", "minLength": 1 }
  },
  "additionalProperties": false
}
```

**Validation Rules**

- `expert_sequence` must contain at least one expert. Default: `["financial", "behaviour"]`.
- `date_start` must be ≤ `date_end`.
- Unknown expert identifiers are rejected at validation time.

**Example**

```json
{
  "run_eda": false,
  "expert_sequence": ["financial", "behaviour"],
  "target_pattern": "structuring",
  "filters": {
    "customer_id": "541",
    "date_start": "2026-06-25",
    "date_end": "2026-07-25",
    "country": null,
    "txn_type": null,
    "risk_level": null
  },
  "rationale": "Targeted structuring query for customer 541. EDA skipped — single entity, specific pattern. Financial Expert first (structuring typology), Behaviour Expert second (baseline validation)."
}
```

---

### 3.3 PlannerOutput

**Purpose**
Composite output from the Planner orchestrator. Bundles both planning artefacts for the pipeline entry point.

**Fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `investigation_plan` | `InvestigationPlan` | Yes | Structured query understanding |
| `execution_plan` | `ExecutionPlan` | Yes | Finalized execution configuration |

**JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tribunal://contracts/PlannerOutput",
  "type": "object",
  "required": ["investigation_plan", "execution_plan"],
  "properties": {
    "investigation_plan": { "$ref": "tribunal://contracts/InvestigationPlan" },
    "execution_plan": { "$ref": "tribunal://contracts/ExecutionPlan" }
  },
  "additionalProperties": false
}
```

**Validation Rules**

- Both nested objects must independently pass their schemas.
- `execution_plan.target_pattern` should match `investigation_plan.target_pattern` when both are set.

**Example**

```json
{
  "investigation_plan": {
    "raw_query": "Find structuring during the last month",
    "intent": "pattern_detection",
    "target_pattern": "structuring",
    "customer_id": null,
    "date_range": ["2026-06-25", "2026-07-25"],
    "country": null,
    "txn_type": null,
    "risk_level": null,
    "experts": ["financial", "behaviour"],
    "run_eda": false
  },
  "execution_plan": {
    "run_eda": false,
    "expert_sequence": ["financial", "behaviour"],
    "target_pattern": "structuring",
    "filters": {
      "customer_id": null,
      "date_start": "2026-06-25",
      "date_end": "2026-07-25",
      "country": null,
      "txn_type": null,
      "risk_level": null
    },
    "rationale": "Pattern detection for structuring across all customers in date range."
  }
}
```

---

## 4. Investigation Layer

### 4.1 CaseFile

**Purpose**
Shared working memory of the investigation. Carries the evolving dominant hypothesis between sequential experts. The only mutable state during expert execution.

**Fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `dominant_hypothesis` | `string \| null` | No | Current leading hypothesis |
| `dominant_confidence` | `number` | Yes | Confidence of dominant hypothesis (0.0–1.0) |
| `contradictions_found` | `string[]` | Yes | Hypotheses contradicted during investigation |
| `open_question` | `string \| null` | No | Question for next expert to address |
| `active_investigation_stage` | `string \| null` | No | Currently active expert stage |
| `defense_skipped` | `boolean` | Yes | Whether defense phase was skipped |

**JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tribunal://contracts/CaseFile",
  "type": "object",
  "required": ["dominant_confidence", "contradictions_found", "defense_skipped"],
  "properties": {
    "dominant_hypothesis": { "type": ["string", "null"] },
    "dominant_confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "contradictions_found": {
      "type": "array",
      "items": { "type": "string" }
    },
    "open_question": { "type": ["string", "null"] },
    "active_investigation_stage": {
      "type": ["string", "null"],
      "enum": ["financial", "behaviour", "defense", "tribunal", null]
    },
    "defense_skipped": { "type": "boolean" }
  },
  "additionalProperties": false
}
```

**Validation Rules**

- Initial state: `dominant_hypothesis = null`, `dominant_confidence = 0.0`, `contradictions_found = []`, `defense_skipped = false`.
- Only an expert with higher-confidence findings may update `dominant_hypothesis`.
- `dominant_confidence` must be in `[0.0, 1.0]`.

**Example — Initial**

```json
{
  "dominant_hypothesis": null,
  "dominant_confidence": 0.0,
  "contradictions_found": [],
  "open_question": null,
  "active_investigation_stage": null,
  "defense_skipped": false
}
```

**Example — After Financial Expert**

```json
{
  "dominant_hypothesis": "structuring",
  "dominant_confidence": 0.86,
  "contradictions_found": [],
  "open_question": "does behaviour history support or undercut structuring?",
  "active_investigation_stage": "behaviour",
  "defense_skipped": false
}
```

---

### 4.2 InvestigationCard

**Purpose**
Atomic unit of structured evidence. Each card represents one hypothesis with supporting evidence, provenance, and optional counter-hypothesis. Never a final verdict.

**Fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `card_id` | `string` | Yes | Unique identifier (e.g., `"card_001"`) |
| `source_expert` | `string` | Yes | Expert that generated this card |
| `derived_from_transactions` | `string[]` | Yes | Transaction IDs that produced this card |
| `generated_at` | `string` (ISO 8601) | Yes | Creation timestamp |
| `hypothesis` | `string` | Yes | Hypothesis label |
| `confidence` | `number` | Yes | Confidence score (0.0–1.0) |
| `evidence` | `string` | Yes | Human-readable evidence summary |
| `counter_hypothesis` | `string \| null` | No | Alternative explanation |
| `missing_data` | `string \| null` | No | Data that would strengthen/weaken finding |
| `supports` | `string[]` | Yes | Card IDs this card supports |

**JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tribunal://contracts/InvestigationCard",
  "type": "object",
  "required": [
    "card_id", "source_expert", "derived_from_transactions",
    "generated_at", "hypothesis", "confidence", "evidence", "supports"
  ],
  "properties": {
    "card_id": {
      "type": "string",
      "pattern": "^card_[0-9]{3,}$"
    },
    "source_expert": {
      "type": "string",
      "enum": ["financial_pattern", "behaviour", "defense"]
    },
    "derived_from_transactions": {
      "type": "array",
      "items": { "type": "string" }
    },
    "generated_at": { "type": "string", "format": "date-time" },
    "hypothesis": { "type": "string", "minLength": 1 },
    "confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "evidence": { "type": "string", "minLength": 1 },
    "counter_hypothesis": { "type": ["string", "null"] },
    "missing_data": { "type": ["string", "null"] },
    "supports": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "additionalProperties": false
}
```

**Validation Rules**

- `card_id` must be unique within an investigation.
- `supports` entries must reference existing card IDs (validated at graph build time).
- `confidence` of `0.0` is valid for `insufficient_data` cards.
- Known hypothesis values: `structuring`, `velocity_anomaly`, `anomaly`, `behavioural_deviation`, `profile_mismatch`, `insufficient_data`, plus defense-generated counter-explanations.

**Example**

```json
{
  "card_id": "card_001",
  "source_expert": "financial_pattern",
  "derived_from_transactions": ["txn_1042", "txn_1043", "txn_1044"],
  "generated_at": "2026-07-25T00:05:12+05:30",
  "hypothesis": "structuring",
  "confidence": 0.86,
  "evidence": "12 deposits between $9,700 and $9,900 in 14 days (sub-threshold ratio 0.92)",
  "counter_hypothesis": "payroll_deposits",
  "missing_data": "merchant_category",
  "supports": []
}
```

---

### 4.3 ExpertResult

**Purpose**
Standardized output from any domain expert. Bundles emitted cards with the updated Case File.

**Fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `cards` | `InvestigationCard[]` | Yes | Cards emitted by this expert (1–3) |
| `case_file` | `CaseFile` | Yes | Updated shared working memory |

**JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tribunal://contracts/ExpertResult",
  "type": "object",
  "required": ["cards", "case_file"],
  "properties": {
    "cards": {
      "type": "array",
      "items": { "$ref": "tribunal://contracts/InvestigationCard" },
      "minItems": 0,
      "maxItems": 3
    },
    "case_file": { "$ref": "tribunal://contracts/CaseFile" }
  },
  "additionalProperties": false
}
```

**Validation Rules**

- Financial Expert: 0–3 cards.
- Behaviour Expert: 0–2 cards.
- Defense Agent: 0–1 cards (via separate return path).

**Example**

```json
{
  "cards": [
    {
      "card_id": "card_001",
      "source_expert": "financial_pattern",
      "derived_from_transactions": ["txn_1042", "txn_1043"],
      "generated_at": "2026-07-25T00:05:12+05:30",
      "hypothesis": "structuring",
      "confidence": 0.86,
      "evidence": "12 sub-threshold deposits in 14 days",
      "counter_hypothesis": "payroll_deposits",
      "missing_data": null,
      "supports": []
    }
  ],
  "case_file": {
    "dominant_hypothesis": "structuring",
    "dominant_confidence": 0.86,
    "contradictions_found": [],
    "open_question": "does behaviour history support or undercut structuring?",
    "active_investigation_stage": "behaviour",
    "defense_skipped": false
  }
}
```

---

## 5. Evidence Graph Layer

### 5.1 EvidenceNode

**Purpose**
Graph node representing one Investigation Card with full provenance. Derived directly from card fields — no inference.

**Fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `node_id` | `string` | Yes | Same as `card_id` |
| `hypothesis` | `string` | Yes | Hypothesis label |
| `confidence` | `number` | Yes | Base confidence (0.0–1.0) |
| `evidence` | `string` | Yes | Evidence summary |
| `source_expert` | `string` | Yes | Originating expert |
| `derived_from_transactions` | `string[]` | Yes | Source transaction IDs |
| `counter_hypothesis` | `string \| null` | No | Alternative explanation |
| `missing_data` | `string \| null` | No | Missing data caveat |

**JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tribunal://contracts/EvidenceNode",
  "type": "object",
  "required": [
    "node_id", "hypothesis", "confidence", "evidence",
    "source_expert", "derived_from_transactions"
  ],
  "properties": {
    "node_id": { "type": "string", "pattern": "^card_[0-9]{3,}$" },
    "hypothesis": { "type": "string" },
    "confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "evidence": { "type": "string" },
    "source_expert": { "type": "string" },
    "derived_from_transactions": {
      "type": "array",
      "items": { "type": "string" }
    },
    "counter_hypothesis": { "type": ["string", "null"] },
    "missing_data": { "type": ["string", "null"] }
  },
  "additionalProperties": false
}
```

**Validation Rules**

- One node per unique `card_id`.
- Node attributes must match the source Investigation Card exactly.

**Example**

```json
{
  "node_id": "card_001",
  "hypothesis": "structuring",
  "confidence": 0.86,
  "evidence": "12 sub-threshold deposits in 14 days",
  "source_expert": "financial_pattern",
  "derived_from_transactions": ["txn_1042", "txn_1043"],
  "counter_hypothesis": "payroll_deposits",
  "missing_data": "merchant_category"
}
```

---

### 5.2 EvidenceEdge

**Purpose**
Directed, weighted relationship between two evidence nodes. Derived from card `supports` fields and `counter_hypothesis` matching.

**Fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `source` | `string` | Yes | Source node ID |
| `target` | `string` | Yes | Target node ID |
| `relation` | `string` | Yes | Edge type |
| `weight` | `number` | Yes | Support or contradiction strength (0.0–1.0) |
| `reason` | `string` | Yes | Human-readable edge justification |

**JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tribunal://contracts/EvidenceEdge",
  "type": "object",
  "required": ["source", "target", "relation", "weight", "reason"],
  "properties": {
    "source": { "type": "string" },
    "target": { "type": "string" },
    "relation": {
      "type": "string",
      "enum": ["supports", "contradicts"]
    },
    "weight": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "reason": { "type": "string", "minLength": 1 }
  },
  "additionalProperties": false
}
```

**Validation Rules**

- Both `source` and `target` must reference existing nodes.
- Support edge weight = source card confidence.
- Contradiction edge weight = `1.0 - source confidence` (card-derived) or defense plausibility (defense-derived).
- No self-loops unless explicitly justified (defense contradicting dominant hypothesis node).

**Example — Support**

```json
{
  "source": "card_003",
  "target": "card_001",
  "relation": "supports",
  "weight": 0.78,
  "reason": "card_003 corroborates card_001 — 430% volume spike consistent with structuring pattern"
}
```

**Example — Contradiction**

```json
{
  "source": "card_004",
  "target": "card_001",
  "relation": "contradicts",
  "weight": 0.65,
  "reason": "Payroll deposits on consistent bi-weekly schedule inconsistent with irregular structuring deposits"
}
```

---

### 5.3 EvidenceGraph

**Purpose**
Container for the complete evidence reasoning structure. Wraps nodes and edges for Tribunal traversal. Implemented as a NetworkX `DiGraph` in code with this contract as the serializable view.

**Fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `nodes` | `EvidenceNode[]` | Yes | All evidence nodes |
| `edges` | `EvidenceEdge[]` | Yes | All support and contradiction edges |
| `metadata` | `object` | No | Graph-level metadata |

**Metadata Object**

| Key | Type | Description |
|---|---|---|
| `card_count` | `integer` | Total nodes |
| `edge_count` | `integer` | Total edges |
| `hypotheses` | `string[]` | Unique hypothesis labels |
| `built_at` | `string (ISO 8601)` | Graph construction timestamp |

**JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tribunal://contracts/EvidenceGraph",
  "type": "object",
  "required": ["nodes", "edges"],
  "properties": {
    "nodes": {
      "type": "array",
      "items": { "$ref": "tribunal://contracts/EvidenceNode" }
    },
    "edges": {
      "type": "array",
      "items": { "$ref": "tribunal://contracts/EvidenceEdge" }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "card_count": { "type": "integer", "minimum": 0 },
        "edge_count": { "type": "integer", "minimum": 0 },
        "hypotheses": {
          "type": "array",
          "items": { "type": "string" }
        },
        "built_at": { "type": "string", "format": "date-time" }
      }
    }
  },
  "additionalProperties": false
}
```

**Validation Rules**

- Duplicate node IDs are rejected.
- Orphan edges (referencing non-existent nodes) are skipped with a warning.
- Empty graph is valid (produces `"no_evidence"` verdict).

**Example**

```json
{
  "nodes": [
    {
      "node_id": "card_001",
      "hypothesis": "structuring",
      "confidence": 0.86,
      "evidence": "12 sub-threshold deposits in 14 days",
      "source_expert": "financial_pattern",
      "derived_from_transactions": ["txn_1042"],
      "counter_hypothesis": "payroll_deposits",
      "missing_data": null
    },
    {
      "node_id": "card_003",
      "hypothesis": "behavioural_deviation",
      "confidence": 0.78,
      "evidence": "430% daily volume increase vs 90-day baseline",
      "source_expert": "behaviour",
      "derived_from_transactions": ["txn_1042", "txn_1043"],
      "counter_hypothesis": null,
      "missing_data": null
    }
  ],
  "edges": [
    {
      "source": "card_003",
      "target": "card_001",
      "relation": "supports",
      "weight": 0.78,
      "reason": "card_003 corroborates card_001"
    }
  ],
  "metadata": {
    "card_count": 2,
    "edge_count": 1,
    "hypotheses": ["structuring", "behavioural_deviation"],
    "built_at": "2026-07-25T00:06:00+05:30"
  }
}
```

---

## 6. Decision Layer

### 6.1 TribunalVerdict

**Purpose**
Final structured decision from the Tribunal. Maps evidence graph reasoning to a risk classification and escalation recommendation.

**Fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `winning_hypothesis` | `string` | Yes | Hypothesis with highest net support |
| `winning_confidence` | `number` | Yes | Net confidence after contradictions |
| `winning_chain` | `string[]` | Yes | Ordered card IDs forming evidence chain |
| `runner_up_hypothesis` | `string \| null` | No | Second-strongest hypothesis |
| `runner_up_confidence` | `number \| null` | No | Runner-up net confidence |
| `rejection_reason` | `string \| null` | No | Why runner-up was rejected |
| `missing_evidence` | `string[]` | Yes | Aggregated missing data from all cards |
| `risk_level` | `string` | Yes | Risk classification |
| `recommendation` | `string` | Yes | Escalation action |
| `contradictions_applied` | `object[]` | Yes | Contradiction edges that affected verdict |

**Contradiction Applied Object**

| Key | Type | Description |
|---|---|---|
| `source` | `string` | Source card ID |
| `target` | `string` | Target card ID |
| `weight` | `number` | Contradiction weight applied |
| `reason` | `string` | Edge reason |

**JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tribunal://contracts/TribunalVerdict",
  "type": "object",
  "required": [
    "winning_hypothesis", "winning_confidence", "winning_chain",
    "missing_evidence", "risk_level", "recommendation", "contradictions_applied"
  ],
  "properties": {
    "winning_hypothesis": { "type": "string" },
    "winning_confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "winning_chain": {
      "type": "array",
      "items": { "type": "string" }
    },
    "runner_up_hypothesis": { "type": ["string", "null"] },
    "runner_up_confidence": { "type": ["number", "null"] },
    "rejection_reason": { "type": ["string", "null"] },
    "missing_evidence": {
      "type": "array",
      "items": { "type": "string" }
    },
    "risk_level": {
      "type": "string",
      "enum": ["low", "medium", "high"]
    },
    "recommendation": {
      "type": "string",
      "enum": ["monitor", "review", "report"]
    },
    "contradictions_applied": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source", "target", "weight", "reason"],
        "properties": {
          "source": { "type": "string" },
          "target": { "type": "string" },
          "weight": { "type": "number" },
          "reason": { "type": "string" }
        }
      }
    }
  },
  "additionalProperties": false
}
```

**Validation Rules**

- `winning_confidence ≥ 0.75` → `risk_level = "high"`, `recommendation = "report"`.
- `winning_confidence ≥ 0.50` → `risk_level = "medium"`, `recommendation = "review"`.
- `winning_confidence < 0.50` → `risk_level = "low"`, `recommendation = "monitor"`.
- Empty graph → `winning_hypothesis = "no_evidence"`, `recommendation = "monitor"`.

**Example**

```json
{
  "winning_hypothesis": "structuring",
  "winning_confidence": 0.72,
  "winning_chain": ["card_001", "card_003"],
  "runner_up_hypothesis": "payroll_deposits",
  "runner_up_confidence": 0.35,
  "rejection_reason": "Deposit timing inconsistent with historical payroll cycle",
  "missing_evidence": ["merchant_category"],
  "risk_level": "medium",
  "recommendation": "review",
  "contradictions_applied": [
    {
      "source": "card_004",
      "target": "card_001",
      "weight": 0.30,
      "reason": "Defense argued payroll pattern — partially reduced structuring confidence"
    }
  ]
}
```

---

## 7. Output Layer

### 7.1 QueryContext

**Purpose**
Preserves original query parameters for report generation. Subset of InvestigationPlan focused on narrative reconstruction.

**Fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `raw_query` | `string` | Yes | Original query string |
| `intent` | `string` | Yes | Investigation intent |
| `target_pattern` | `string \| null` | No | Target AML pattern |
| `customer_id` | `string \| null` | No | Target customer |
| `date_range` | `[date, date] \| null` | No | Investigation date range |

**JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tribunal://contracts/QueryContext",
  "type": "object",
  "required": ["raw_query", "intent"],
  "properties": {
    "raw_query": { "type": "string" },
    "intent": { "type": "string" },
    "target_pattern": { "type": ["string", "null"] },
    "customer_id": { "type": ["string", "null"] },
    "date_range": {
      "type": ["array", "null"],
      "items": { "type": "string", "format": "date" },
      "minItems": 2,
      "maxItems": 2
    }
  },
  "additionalProperties": false
}
```

**Validation Rules**

- Constructed from `InvestigationPlan` at pipeline start. Fields are read-only thereafter.

**Example**

```json
{
  "raw_query": "Find structuring in the last 30 days for customer 541",
  "intent": "pattern_detection",
  "target_pattern": "structuring",
  "customer_id": "541",
  "date_range": ["2026-06-25", "2026-07-25"]
}
```

---

### 7.2 InvestigationReport

**Purpose**
Human-readable investigation output. The artefact a compliance analyst, auditor, or regulator reads first.

**Fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `query_recap` | `string` | Yes | Original query restated |
| `experts_invoked` | `object[]` | Yes | Experts that ran, with reasons |
| `experts_skipped` | `object[]` | Yes | Experts skipped, with reasons |
| `winning_hypothesis` | `string` | Yes | Winning hypothesis label |
| `winning_confidence` | `number` | Yes | Winning confidence (0.0–1.0) |
| `evidence_chain` | `string` | Yes | Human-readable chain narrative |
| `runner_up_hypothesis` | `string \| null` | No | Runner-up label |
| `runner_up_confidence` | `number \| null` | No | Runner-up confidence |
| `rejection_reason` | `string \| null` | No | Why runner-up was rejected |
| `missing_evidence` | `string[]` | Yes | Missing data caveats |
| `risk_level` | `string` | Yes | Risk classification |
| `recommendation` | `string` | Yes | Escalation action |
| `full_text` | `string` | Yes | Complete rendered report |

**Expert Entry Object**

| Key | Type | Description |
|---|---|---|
| `name` | `string` | Expert identifier |
| `reason` | `string` | Why invoked or skipped |

**JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tribunal://contracts/InvestigationReport",
  "type": "object",
  "required": [
    "query_recap", "experts_invoked", "experts_skipped",
    "winning_hypothesis", "winning_confidence", "evidence_chain",
    "missing_evidence", "risk_level", "recommendation", "full_text"
  ],
  "properties": {
    "query_recap": { "type": "string" },
    "experts_invoked": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "reason"],
        "properties": {
          "name": { "type": "string" },
          "reason": { "type": "string" }
        }
      }
    },
    "experts_skipped": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "reason"],
        "properties": {
          "name": { "type": "string" },
          "reason": { "type": "string" }
        }
      }
    },
    "winning_hypothesis": { "type": "string" },
    "winning_confidence": { "type": "number" },
    "evidence_chain": { "type": "string" },
    "runner_up_hypothesis": { "type": ["string", "null"] },
    "runner_up_confidence": { "type": ["number", "null"] },
    "rejection_reason": { "type": ["string", "null"] },
    "missing_evidence": {
      "type": "array",
      "items": { "type": "string" }
    },
    "risk_level": { "type": "string", "enum": ["low", "medium", "high"] },
    "recommendation": { "type": "string", "enum": ["monitor", "review", "report"] },
    "full_text": { "type": "string", "minLength": 1 }
  },
  "additionalProperties": false
}
```

**Example**

```json
{
  "query_recap": "Query: \"Find structuring in the last 30 days for customer 541\"",
  "experts_invoked": [
    { "name": "financial", "reason": "Structuring typology — direct pattern match" },
    { "name": "behaviour", "reason": "Validate against customer baseline" }
  ],
  "experts_skipped": [],
  "winning_hypothesis": "structuring",
  "winning_confidence": 0.72,
  "evidence_chain": "card_001 (12 sub-threshold deposits) → card_003 (430% volume spike)",
  "runner_up_hypothesis": "payroll_deposits",
  "runner_up_confidence": 0.35,
  "rejection_reason": "Deposit timing inconsistent with historical payroll cycle",
  "missing_evidence": ["merchant_category"],
  "risk_level": "medium",
  "recommendation": "review",
  "full_text": "Investigation Summary\nQuery: \"Find structuring in the last 30 days for customer 541\"\n..."
}
```

---

## 8. Tool Layer

### 8.1 FeatureDictionary

**Purpose**
Computed AML features from raw transaction data. Shared infrastructure consumed by experts — never crosses module boundaries directly to Tribunal or Report.

**Fields**

| Field | Type | Description |
|---|---|---|
| `rolling_sum_7d` | `number` | Rolling sum over 7-day window |
| `rolling_sum_30d` | `number` | Rolling sum over 30-day window |
| `txn_count_daily` | `number` | Average daily transaction count |
| `txn_velocity` | `number` | Transactions per day in analysis window |
| `amount_mean` | `number` | Mean transaction amount |
| `amount_std` | `number` | Standard deviation of amounts |
| `amount_deviation_from_baseline` | `number` | Current vs historical mean (ratio) |
| `max_single_amount` | `number` | Largest single transaction |
| `sub_threshold_count` | `integer` | Transactions below reporting threshold |
| `sub_threshold_ratio` | `number` | Ratio of sub-threshold to total |
| `unique_beneficiaries` | `integer` | Distinct counterparties |
| `weekend_txn_ratio` | `number` | Proportion of weekend transactions |
| `daily_volume_change_pct` | `number` | % change in daily volume vs baseline |
| `baseline_incomplete` | `boolean` | Whether historical baseline was insufficient |

**Validation Rules**

- All numeric fields default to `0.0` when no transactions found.
- `baseline_incomplete = true` when fewer than 30 days of history available.

---

### 8.2 AnomalyResult

**Purpose**
Statistical outlier detection output. Complements rule-based checks in the Financial Expert.

**Fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `method` | `string` | Yes | Detection method used |
| `outlier_count` | `integer` | Yes | Number of flagged transactions |
| `outlier_txn_ids` | `string[]` | Yes | IDs of flagged transactions |
| `outlier_scores` | `object` | Yes | Map of txn_id → anomaly score |
| `overall_anomaly_score` | `number` | Yes | Aggregate score (0.0–1.0) |

**JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tribunal://contracts/AnomalyResult",
  "type": "object",
  "required": ["method", "outlier_count", "outlier_txn_ids", "outlier_scores", "overall_anomaly_score"],
  "properties": {
    "method": { "type": "string", "enum": ["zscore", "isolation_forest", "none"] },
    "outlier_count": { "type": "integer", "minimum": 0 },
    "outlier_txn_ids": { "type": "array", "items": { "type": "string" } },
    "outlier_scores": { "type": "object", "additionalProperties": { "type": "number" } },
    "overall_anomaly_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 }
  },
  "additionalProperties": false
}
```

**Example**

```json
{
  "method": "zscore",
  "outlier_count": 2,
  "outlier_txn_ids": ["txn_1099", "txn_1100"],
  "outlier_scores": { "txn_1099": 3.2, "txn_1100": 2.8 },
  "overall_anomaly_score": 0.45
}
```

---

## 9. Composite Types

### Transaction Record (Dataset Contract)

Raw transaction data is not a TRIBUNAL contract object — it comes from the dataset. All experts expect this column schema:

| Column | Type | Required | Description |
|---|---|---|---|
| `txn_id` | `string` | Yes | Unique transaction identifier |
| `customer_id` | `string` | Yes | Customer identifier |
| `amount` | `number` | Yes | Transaction amount |
| `timestamp` | `datetime` | Yes | Transaction datetime |
| `txn_type` | `string` | No | Transaction type (deposit, withdrawal, transfer) |
| `country` | `string` | No | Country code |
| `beneficiary_id` | `string` | No | Counterparty identifier |
| `is_laundering` | `boolean` | No | Ground truth label (evaluation only) |

---

## 10. Enumerations & Constants

| Enum | Values |
|---|---|
| Intent | `pattern_detection`, `broad_scan`, `compliance_check` |
| Target Pattern | `structuring`, `smurfing`, `velocity`, `anomaly`, `deviation` |
| Expert ID | `financial`, `behaviour` |
| Source Expert | `financial_pattern`, `behaviour`, `defense` |
| Edge Relation | `supports`, `contradicts` |
| Risk Level | `low`, `medium`, `high` |
| Recommendation | `monitor`, `review`, `report` |
| Investigation Stage | `financial`, `behaviour`, `defense`, `tribunal` |

**Threshold Constants** (defined in `config/settings.py`, referenced here for contract completeness):

| Constant | Default | Used By |
|---|---|---|
| `REPORTING_THRESHOLD` | `10000` | Feature Engineering, Financial Expert |
| `STRUCTURING_MARGIN` | `500` | Financial Expert |
| `STRUCTURING_RATIO_THRESHOLD` | `0.5` | Financial Expert |
| `VELOCITY_SPIKE_THRESHOLD` | `200` | Financial Expert |
| `ANOMALY_THRESHOLD` | `0.3` | Financial Expert |
| `BEHAVIOUR_DEVIATION_THRESHOLD` | `150` | Behaviour Expert |
| `DEFENSE_PLAUSIBILITY_THRESHOLD` | `0.4` | Defense Agent |
| `HIGH_RISK_THRESHOLD` | `0.75` | Tribunal |
| `MEDIUM_RISK_THRESHOLD` | `0.50` | Tribunal |
| `REINVESTIGATION_THRESHOLD` | `0.45` | Pipeline (adaptive cycle) |

---

## 11. Contract Flow Diagram

```
UserQuery
    │
    ▼
InvestigationPlan ──► ExecutionPlan ──► PlannerOutput
    │                        │
    │                        ▼
    │                   CaseFile (init)
    │                        │
    │                        ▼
    │              ExpertResult × N
    │              (cards + case_file)
    │                        │
    ▼                        ▼
QueryContext          InvestigationCard[]
                               │
                               ▼
                        EvidenceGraph
                     (nodes + edges)
                               │
                               ▼
                        TribunalVerdict
                               │
                               ▼
                      InvestigationReport
```

---

*End of Data Contracts v1.0*

# TRIBUNAL — Architecture Design Specification

**Document Classification:** Canonical Architecture Reference
**Version:** 2.0
**System Name:** TRIBUNAL — Transparent Review through Investigative Board Using Nuanced Agentic Logic

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Solution Philosophy](#3-solution-philosophy)
4. [Core Design Principles](#4-core-design-principles)
5. [Complete Proposed Solution](#5-complete-proposed-solution)
6. [Investigation Lifecycle](#6-investigation-lifecycle)
7. [Implemented System Architecture](#7-implemented-system-architecture)
8. [Investigation Engine](#8-investigation-engine)
9. [Persistence & Storage Layer](#9-persistence--storage-layer)
10. [REST API & Service Layer](#10-rest-api--service-layer)
11. [Investigation Dashboard](#11-investigation-dashboard)
12. [Adaptive Agentic Behaviour](#12-adaptive-agentic-behaviour)
13. [Explainability Strategy](#13-explainability-strategy)
14. [Technical Architecture](#14-technical-architecture)
15. [Future Improvements & Evolution Roadmap](#15-future-improvements--evolution-roadmap)
16. [Conclusion](#16-conclusion)
17. [Appendix A — Complete Implementation Package Map](#appendix-a--complete-implementation-package-map)

---

## 1. Executive Summary

Financial institutions worldwide rely on rule-based Anti-Money Laundering (AML) systems that produce overwhelming volumes of false positives while providing limited explainability. For every genuinely suspicious case flagged, analysts must manually triage dozens — sometimes hundreds — of benign alerts, each requiring hours of investigation with no structured reasoning trail. Existing AI approaches frequently replace rules with a single prediction model, but the fundamental problem remains: an isolated risk score with little transparency into how a conclusion was reached.

**TRIBUNAL proposes a different paradigm.**

Instead of allowing a single AI model to determine whether a transaction is suspicious, TRIBUNAL models the investigation process performed by compliance analysts. Specialized AI investigators collaboratively build evidence, challenge competing hypotheses, and collectively arrive at an explainable verdict through structured reasoning.

The system operates as an *AI Investigation Board* — a sequential panel of domain experts that each generate competing hypotheses as structured Investigation Cards. Those cards are wired into a weighted evidence graph — support and contradiction edges — which a tribunal reasons over to find the strongest explainable chain of evidence, before recommending an escalation action.

Every conclusion is fully traceable back to the supporting evidence, making the final recommendation understandable, auditable, and defensible.

TRIBUNAL does not produce scores. It produces verdicts — with reasoning.

### What Has Been Built

TRIBUNAL v1.0 is a fully operational, end-to-end investigation platform comprising four architectural layers:

| Layer | Technology | Purpose |
|---|---|---|
| **Investigation Engine** | Python, NetworkX, Ollama | Multi-expert agentic investigation pipeline |
| **Persistence Layer** | SQLite, Filesystem | Durable storage of investigations, verdicts, reports, and audit trails |
| **REST API** | FastAPI | Versioned HTTP interface exposing all investigation capabilities |
| **Investigation Dashboard** | React, TypeScript, Vite | Interactive frontend for launching, exploring, and comparing investigations |

The system has been verified with **142 passing tests** across unit, integration, and end-to-end test suites, covering the full pipeline from natural language query ingestion through to explainable verdict generation and multi-format report rendering.

---

## 2. Problem Statement

### The Current State of AML Compliance

Anti-Money Laundering systems today follow a pattern that has remained fundamentally unchanged for decades:

```
Static Rules & Thresholds
        ↓
Rule Explosion — hundreds of overlapping rules, each tuned to catch edge cases
        ↓
False Positive Epidemic — 95%+ of alerts are benign
        ↓
Manual Investigation — analysts spend hours per case with no automated reasoning support
        ↓
No Structured Reasoning — decisions exist as notes in case management systems, not traceable logic
        ↓
No Transparency — regulators and auditors cannot reconstruct why a decision was made
```

The cost is staggering. Financial institutions collectively spend billions annually on compliance operations, the majority of which is consumed by the manual triage of false positives. Analysts burn out. Genuinely suspicious activity hides in the noise. And when regulators ask *"why was this case closed?"* — the answer is often a paragraph of free-text notes rather than a structured chain of evidence.

### Why LLMs Alone Don't Solve This

Large Language Models offer remarkable reasoning capabilities, but deploying a single LLM as a replacement for rule-based systems introduces a different set of problems:

- **Single-point reasoning.** One model, one perspective, one conclusion. There is no mechanism for competing hypotheses to surface and be evaluated against each other.
- **Opaque confidence.** An LLM can state that it is "85% confident" a transaction is suspicious, but that number is not grounded in traceable evidence — it is a linguistic artefact, not a measured probability.
- **No adversarial challenge.** Without a structured mechanism to argue against the dominant hypothesis, confirmation bias is baked into the architecture.
- **No evidence provenance.** The model's reasoning is entangled within its response. There is no separation between the evidence, the hypothesis, and the conclusion — making audit impossible.
- **Hallucination risk.** In a compliance context, a plausible-sounding but fabricated justification is worse than no justification at all.

The problem is not a lack of intelligence. The problem is a lack of *structured investigation*.

---

## 3. Solution Philosophy

### Investigation, Not Classification

TRIBUNAL models AML compliance as a structured investigative procedure rather than a simple classification task.

Rather than asking one AI model *"Is this customer suspicious?"*, TRIBUNAL assembles a panel of domain experts — each with a distinct investigative lens — and asks them to *investigate the same case from different perspectives*.

Each expert contributes **structured evidence** instead of final decisions. No single expert renders a verdict. No single model has the authority to close a case.

A tribunal reasons over the accumulated evidence before producing a final recommendation.

### The Investigation Board Metaphor

Consider how a real-world compliance investigation works:

1. A financial analyst examines transaction patterns — amounts, frequencies, thresholds.
2. A behavioural analyst examines the customer's history — deviations, profile changes, contextual anomalies.
3. If warranted, a network analyst traces the flow of funds across counterparties.
4. A devil's advocate challenges the emerging theory — *could this be legitimate?*
5. A panel reviews the collected evidence and reaches a conclusion — with dissent noted.

TRIBUNAL replicates this process computationally. Each step produces artefacts. Each artefact is traceable. The final verdict is not a number — it is a reasoned conclusion built from evidence, challenge, and resolution.

### What Makes This Different

| Traditional AI Approach | TRIBUNAL |
|---|---|
| One model, one score | Multiple experts, multiple hypotheses |
| Score explains nothing | Every conclusion traces to evidence |
| No adversarial challenge | Defense agent argues against the dominant theory |
| Opaque confidence | Confidence derived from evidence graph traversal |
| Classification output | Investigation report with full reasoning chain |
| No persistence | Full investigation history with audit trail |
| CLI or batch output | Interactive dashboard for exploration and comparison |

This is where the innovation lies — not in a better model, but in a better *process*.

---

## 4. Core Design Principles

Six principles govern every architectural decision in TRIBUNAL. They are not aspirational — they are structural constraints.

### Principle 1 — Investigation Over Prediction

TRIBUNAL does not predict whether a customer is suspicious. It investigates. The output is not a probability — it is a structured body of evidence, a dominant hypothesis, a challenged alternative, and a reasoned recommendation. The distinction is fundamental: predictions can be wrong silently; investigations leave a trail.

### Principle 2 — Evidence Before Verdict

No component in the system is permitted to render a final verdict. Experts produce Investigation Cards — structured evidence artefacts. The Evidence Graph organizes relationships between those artefacts. Only the Tribunal, reasoning over the complete graph, produces a recommendation. This separation ensures that conclusions emerge from evidence, never from assumption.

### Principle 3 — Structural Explainability

Explainability in TRIBUNAL is an architectural property built into the system core. The architecture is designed so that every recommendation is *inherently* explainable — because it is constructed from traceable components. Investigation Cards carry provenance metadata. Evidence Graphs preserve relationship semantics. The final report reconstructs the reasoning chain from graph traversal, not from prompt engineering.

### Principle 4 — Sequential Collaborative Reasoning

Experts do not operate in isolation. They investigate sequentially, each reading the shared Case File before beginning work. The Customer Behaviour Expert does not start from scratch — it reads the Financial Expert's dominant hypothesis and specifically targets its investigation to support or undercut that hypothesis. This sequential, case-file-aware collaboration models how real compliance teams operate.

### Principle 5 — Query-Aware Execution

TRIBUNAL does not run the same pipeline for every query. The Query Understanding & Planning Agent analyses the user's intent, extracts entities and parameters, and constructs a tailored investigation plan. A broad exploratory query activates different experts and tools than a targeted single-entity investigation. The system adapts its investigative strategy to the question being asked.

### Principle 6 — Full Evidence Provenance

Every Investigation Card records which expert generated it, which transactions contributed to it, and when it was created. Every edge in the Evidence Graph records the relationship type, the weight, and the reason for the connection. The final report traces backward from recommendation to evidence to source data. Nothing is asserted without attribution.

---

## 5. Complete Proposed Solution

TRIBUNAL's complete architectural vision defines a comprehensive, multi-layered investigation framework. The following diagram represents the full proposed system — both what is currently implemented and what is designed for future expansion.

### 5.1 Full System Architecture

```
    ┌──────────────────────────────────────────────────────────────────────────┐
    │                     INVESTIGATION DASHBOARD                             │
    │         React · TypeScript · Vite · Interactive Exploration             │
    │                                                                         │
    │   ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌────────┐ │
    │   │   Home   │  │ Workspace│  │  History   │  │ Explorer │  │Compare │ │
    │   │          │  │   (New   │  │  (Past     │  │ (Search  │  │ (Side  │ │
    │   │          │  │  Invest.)│  │  Results)  │  │  & Tag)  │  │ by     │ │
    │   │          │  │          │  │            │  │          │  │ Side)  │ │
    │   └──────────┘  └──────────┘  └───────────┘  └──────────┘  └────────┘ │
    │   ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌──────────┐             │
    │   │ Report   │  │Evidence  │  │  System    │  │Settings  │             │
    │   │ Viewer   │  │  Graph   │  │  Health    │  │          │             │
    │   └──────────┘  └──────────┘  └───────────┘  └──────────┘             │
    └────────────────────────────┬──────────────────────────────────────────┘
                                 │ HTTP / REST
    ┌────────────────────────────▼──────────────────────────────────────────┐
    │                        REST API LAYER                                │
    │                  FastAPI · Versioned (v1) · CORS                     │
    │                                                                      │
    │   ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────────┐  │
    │   │ /investigate│  │ /report    │  │ /graph     │  │ /search      │  │
    │   │ /query      │  │ /export    │  │ /verdict   │  │ /metadata    │  │
    │   └──────┬─────┘  └─────┬──────┘  └─────┬──────┘  └──────┬───────┘  │
    │          │              │                │                │          │
    │   ┌──────▼──────────────▼────────────────▼────────────────▼───────┐  │
    │   │                 INVESTIGATION SERVICE                        │  │
    │   │           Central Orchestration Boundary                     │  │
    │   └──────────────────────┬───────────────────────────────────────┘  │
    │              Middleware: Logging · Timing · Error Handling           │
    └──────────────────────────┬──────────────────────────────────────────┘
                               │
    ┌──────────────────────────▼──────────────────────────────────────────┐
    │                   INVESTIGATION ENGINE                              │
    │              Pure Python · Deterministic Analytics                   │
    │                                                                     │
    │   ┌─────────────┐     ┌─────────────────────────────────────────┐  │
    │   │   Planner    │     │        Expert Investigation Board       │  │
    │   │              │     │                                         │  │
    │   │ Query Parser │     │  ┌─────────────┐  ┌─────────────────┐  │  │
    │   │  (Ollama +   │────▶│  │  Financial   │  │   Behaviour     │  │  │
    │   │   Regex      │     │  │  Expert      │──│   Expert        │  │  │
    │   │   Fallback)  │     │  │  (5 detect.) │  │   (6 detect.)   │  │  │
    │   │              │     │  └──────┬───────┘  └───────┬─────────┘  │  │
    │   │ Execution    │     │         └─────────┬────────┘            │  │
    │   │  Planner     │     │                   │                     │  │
    │   └─────────────┘     └───────────────────┼─────────────────────┘  │
    │                                            │                        │
    │   ┌────────────────────────────────────────▼─────────────────────┐  │
    │   │              Evidence Graph Builder                          │  │
    │   │   Nodes: Account · Card · Hypothesis · Provenance            │  │
    │   │   Edges: SUPPORTS · CONTRADICTS · CORROBORATES ·             │  │
    │   │          DERIVED_FROM · SAME_ACCOUNT · HAS_EVIDENCE          │  │
    │   └────────────────────────────┬─────────────────────────────────┘  │
    │                                │                                    │
    │   ┌────────────────────────────▼─────────────────────────────────┐  │
    │   │              Defense Agent (Adversarial Review)               │  │
    │   │   Evidence Review · Contradiction Detection · Alternative     │  │
    │   │   Hypothesis Gen. · Strength Analysis · Uncertainty Est.     │  │
    │   │   → Rebuttal Cards (source_expert="defense")                 │  │
    │   └────────────────────────────┬─────────────────────────────────┘  │
    │                                │                                    │
    │   ┌────────────────────────────▼─────────────────────────────────┐  │
    │   │              Tribunal (Consensus Engine)                      │  │
    │   │   Hypothesis Extraction · Evidence Weighing · Contradiction   │  │
    │   │   Resolution · Consensus Formation · Confidence Calibration  │  │
    │   │   → TribunalVerdict                                          │  │
    │   └────────────────────────────┬─────────────────────────────────┘  │
    │                                │                                    │
    │   ┌────────────────────────────▼─────────────────────────────────┐  │
    │   │              Report Generator (Explainability Engine)         │  │
    │   │   10-Section Structured Report · Markdown · HTML · JSON      │  │
    │   │   → InvestigationReport                                      │  │
    │   └──────────────────────────────────────────────────────────────┘  │
    └──────────────────────────┬──────────────────────────────────────────┘
                               │
    ┌──────────────────────────▼──────────────────────────────────────────┐
    │                   PERSISTENCE LAYER                                 │
    │                                                                     │
    │   ┌─────────────────────────┐    ┌───────────────────────────────┐  │
    │   │     SQLite Database     │    │     Filesystem Storage        │  │
    │   │  investigations         │    │  reports/   (MD, HTML, JSON)  │  │
    │   │  reports                │    │  graphs/    (JSON, gpickle)   │  │
    │   │  graphs                 │    │  cases/     (JSON)            │  │
    │   │  verdicts               │    │  audit/     (JSON)            │  │
    │   │  audit                  │    └───────────────────────────────┘  │
    │   │  bookmarks              │                                       │
    │   │  tags                   │                                       │
    │   │  saved_searches         │                                       │
    │   │  report_annotations     │                                       │
    │   └─────────────────────────┘                                       │
    └─────────────────────────────────────────────────────────────────────┘
```

#### Analytical Feature Store Scale

All analytical components in the engine operate on a pre-computed analytical foundation:

| Metric | Scale | Scope & Description |
|---|---|---|
| **Raw Transactions** | **6.92 Million** | Underlying payment dataset with timestamps, currencies, and formats |
| **Profiled Accounts** | **705,903** | Distinct customer accounts evaluated for baseline behaviour |
| **AML Feature Metrics** | **44 Features** | Calculated metrics spanning financial, behavioural, network, temporal, and statistical domains |

---

### 5.2 Core Components

| Component | Role | Status |
|---|---|---|
| **Query Understanding & Planning** | Accepts natural-language queries, extracts intent, entities, and filters, constructs a tailored execution plan. Uses Ollama for LLM understanding with a deterministic regex fallback. | ✅ Implemented |
| **Financial Pattern Expert** | Investigates transactional evidence for AML typologies — structuring, velocity anomalies, large transfers, frequency spikes, threshold-adjacent behaviour. 5 specialized detectors. | ✅ Implemented |
| **Customer Behaviour Expert** | Investigates behavioural deviations from historical baselines — drift, dormancy, spending shifts, currency changes, payment pattern shifts, counterparty expansion. 6 specialized detectors. | ✅ Implemented |
| **Network Intelligence Expert** | Traces fund flow across counterparties, identifies fan-out patterns and money laundering chains. |  Future |
| **Regulatory Rule Expert** | Matches jurisdiction-specific regulatory rules against investigation evidence. |  Future |
| **Case File** | Shared working memory carrying dominant hypothesis, confidence, contradictions, and open questions between sequential experts. | ✅ Implemented |
| **Evidence Graph** | Directed weighted graph (NetworkX DiGraph) where nodes are Investigation Cards and edges represent semantic relationships (support, contradiction, corroboration). | ✅ Implemented |
| **Defense Agent** | Adversarial reviewer that challenges dominant hypotheses through a 7-stage pipeline: evidence review, contradiction detection, alternative hypothesis generation, strength analysis, uncertainty estimation, confidence adjustment, and rebuttal building. | ✅ Implemented |
| **Tribunal (Consensus Engine)** | 6-stage deterministic deliberation: hypothesis extraction, evidence weighing, contradiction resolution, consensus formation, confidence calibration, and verdict building. | ✅ Implemented |
| **Report Generator** | 10-section explainability engine producing structured reports in Markdown, HTML, and JSON formats with full provenance chains. | ✅ Implemented |
| **Persistence Layer** | SQLite metadata database (8 tables) with filesystem artifact storage. Repository pattern with dedicated interfaces. | ✅ Implemented |
| **REST API** | FastAPI v1 with 6 route modules, structured schemas, middleware (CORS, logging, timing, exception handling), and OpenAPI documentation. | ✅ Implemented |
| **Investigation Dashboard** | React + TypeScript SPA with 10 pages: Home, Workspace, History, Explorer, Compare, Investigation Viewer, Report Viewer, Evidence Graph, System Health, and Settings. | ✅ Implemented |
| **Feature Store** | Pre-computed analytical feature store (44 AML features across 705,903 accounts) persisted as Parquet. | ✅ Implemented |
| **Transaction Network** | NetworkX MultiDiGraph of account-to-account transfers with graph-derived features (fan-in, fan-out, degree, neighbourhood). | ✅ Implemented |

---

## 6. Investigation Lifecycle

Every query that enters TRIBUNAL follows a structured investigation lifecycle. This section walks through the complete journey from question to recommendation as it operates in the current system.

### Stage 1 — Natural Language Query

The user poses an unrestricted natural-language question through the Investigation Dashboard or REST API. This may be a targeted investigation (*"Find structuring in the last 30 days for customer 541"*), an exploratory scan (*"Show unusual patterns across all high-risk accounts"*), or a compliance check (*"Check customer 200"*). The query's nature determines the investigation plan.

### Stage 2 — Query Understanding & Planning

The Planner accepts the natural-language query and passes it through the LLM Client (Ollama) for structured extraction — intent, entity identifiers, date ranges, target AML patterns, and filters. If the LLM is unavailable, a deterministic regex-based fallback parser handles extraction. The Query Parser validates and normalizes the output into an `InvestigationPlan`. The Execution Planner then constructs an `ExecutionPlan`: which experts to invoke, in what order, whether EDA is needed, and what feature subsets to extract. The entire planning stage is profiled to microsecond granularity.

### Stage 3 — Expert Investigation

Experts execute sequentially, each reading the current Case File before beginning their investigation. The Financial Pattern Expert investigates first without prior context. The Customer Behaviour Expert reads the evolving Case File and directs its investigation relative to the current dominant hypothesis — reinforcing, refuting, or refining it.

**Financial Expert Pipeline:**
1. Candidate Selection — Filters target accounts based on execution plan parameters
2. Structuring Detection — Near-threshold deposits ($8K–$10K range)
3. Velocity Detection — Rapid transaction burst scoring
4. Large Transfer Detection — Statistical outlier identification
5. Frequency Detection — High-frequency spike detection

**Behaviour Expert Pipeline:**
1. Candidate Selection — Baseline deviation filtering
2. Behaviour Drift Detection — Daily amount and frequency deviation
3. Dormancy Detection — Dormant account reactivation
4. Spending Pattern Detection — Distribution shift analysis
5. Currency Change Detection — Unexpected currency switching
6. Payment Pattern Detection — Format shift (ACH to Wire/Cash)
7. Counterparty Behaviour Detection — Network expansion

### Stage 4 — Investigation Cards

Each expert emits one or more Investigation Cards — structured evidence artefacts containing a hypothesis, supporting evidence, confidence score, severity classification, counter-hypothesis, missing data, provenance metadata, and supporting metrics. Cards are the atomic unit of reasoning in TRIBUNAL.

```json
{
  "card_id": "card_fin_001",
  "source_expert": "financial",
  "derived_from_transactions": ["txn_1042", "txn_1043", "txn_1050"],
  "generated_at": "2026-07-24T15:22:10",
  "hypothesis": "structuring",
  "confidence": 0.82,
  "severity": "HIGH",
  "evidence": "12 deposits of $9,700–$9,900 over 4 days, all below $10,000 reporting threshold",
  "supporting_metrics": {
    "threshold_proximity": 0.97,
    "structuring_score": 0.85,
    "velocity_ratio": 4.3
  },
  "provenance": {
    "detector": "structuring_detector",
    "feature_set": ["rolling_sum_7d", "threshold_proximity"],
    "accounts_analyzed": 147
  },
  "counter_hypothesis": "cash_intensive_business",
  "missing_data": "merchant_category",
  "supports": ["card_fin_003"]
}
```

### Stage 5 — Evidence Graph Construction

The Evidence Graph Builder translates Investigation Cards into a directed, weighted NetworkX DiGraph. The construction process involves:

1. **Node Generation** — Each card, account, hypothesis, and provenance record becomes a typed node (`account`, `card`, `hypothesis`, `provenance`)
2. **Edge Linking** — Semantic relationships are inferred: `SUPPORTS`, `CONTRADICTS`, `CORROBORATES`, `DERIVED_FROM`, `SAME_ACCOUNT`, `HAS_EVIDENCE`
3. **Validation** — Card completeness, confidence score ranges, and graph structural integrity are verified
4. **Deduplication** — Same-expert cards are merged where appropriate with provenance consolidation
5. **Metrics Computation** — Node count, edge count, connected components, average confidence, and graph density

**Graph Traversal & Deliberation Link:** Once constructed, the Evidence Graph forms the primary mathematical structure for consensus calculation. The Tribunal computes Net Evidence Strength by aggregating weighted `SUPPORTS` edges while subtracting weighted `CONTRADICTS` edges, ranking competing hypotheses by their resulting net support.

### Stage 6 — Adversarial Defense

The Defense Agent reads the complete Evidence Graph and orchestrates a 7-stage adversarial review:

1. **Evidence Review** — Traverses the graph and extracts prosecution findings into a `ReviewContext`
2. **Contradiction Detection** — Identifies conflicting expert findings (e.g., Financial Expert flags structuring while Behaviour Expert shows normal baseline)
3. **Alternative Hypothesis Generation** — Generates plausible non-malicious explanations (payroll patterns, merchant settlement, festival shopping, tax disbursement)
4. **Evidence Strength Analysis** — Scores evidence strength and evaluates provenance completeness
5. **Uncertainty Estimation** — Estimates uncertainty based on evidence sparsity and expert diversity
6. **Confidence Adjustment** — Computes deterministic defense card confidence
7. **Rebuttal Building** — Constructs `InvestigationCard` objects with `source_expert="defense"`

Defense cards are then augmented into the Evidence Graph via `augment_graph()`, creating `CONTRADICTS` edges against prosecution evidence without modifying or deleting existing prosecution nodes.

**Architectural Rationale:** Breaking adversarial reasoning into deterministic stages improves reproducibility, isolates responsibilities, and keeps each output independently inspectable—avoiding the opacity and non-reproducibility of a single unconstrained LLM prompt.

### Stage 7 — Tribunal Deliberation

The Tribunal performs a 6-stage deterministic deliberation over the augmented Evidence Graph:

1. **Hypothesis Extraction** — Identifies all candidate hypotheses from graph nodes
2. **Evidence Weighing** — Calculates raw support scores for each hypothesis based on edge weights
3. **Contradiction Resolution** — Evaluates opposing evidence penalties, computes Net Evidence Strength (support weight minus contradiction weight)
4. **Consensus Formation** — Ranks competing hypotheses, identifies winning and runner-up chains, computes confidence gap
5. **Confidence Calibration** — Calibrates final confidence score accounting for graph density, evidence diversity, and expert coverage
6. **Verdict Building** — Issues `TribunalVerdict` with verdict category, primary and secondary hypotheses, supporting cards, rejected hypotheses, deliberation trace, and recommendation

**Verdict Categories:**
- `LIKELY_MALICIOUS` — Strong evidence of suspicious activity
- `POSSIBLY_MALICIOUS` — Moderate evidence, warrants review
- `INCONCLUSIVE` — Insufficient or conflicting evidence
- `LIKELY_LEGITIMATE` — Evidence supports benign explanation

**Risk Levels:** `HIGH` (confidence ≥ 0.75), `MEDIUM` (confidence ≥ 0.50), `LOW` (confidence < 0.50)

### Stage 8 — Investigation Report

The Report Generator transforms the complete investigation lifecycle into a 10-section structured report:

| Section | Content |
|---|---|
| Executive Summary | Query, verdict, risk level, recommendation, key metrics |
| Query Interpretation | Extracted intent, entities, filters, and execution plan |
| Timeline | Chronological sequence of investigation stages with durations |
| Expert Findings | Per-expert cards, hypotheses, confidence scores, and evidence |
| Evidence Summary | Aggregated evidence chain from prosecution and defense |
| Graph Summary | Evidence Graph topology, node/edge counts, density metrics |
| Defense Summary | Adversarial findings, alternative hypotheses, rebuttals |
| Tribunal Summary | Deliberation trace, winning/runner-up hypotheses, confidence gap |
| Provenance | Full lineage tracing: transactions → features → detectors → cards |
| Audit Trail | Investigation lifecycle events with timestamps |

Reports are rendered in three formats:
- **Markdown** — Human-readable narrative with evidence chains
- **HTML** — Formatted output for web display and embedding
- **JSON** — Machine-readable structured payload for programmatic access

---

## 7. Implemented System Architecture

### 7.1 Four-Layer Architecture

TRIBUNAL is organized as a four-layer system with clear boundaries and directed data flow:

```
┌─────────────────────────────────────────────────────┐
│  Layer 4: Investigation Dashboard       (React/TS)  │
├─────────────────────────────────────────────────────┤
│  Layer 3: REST API & Service Layer      (FastAPI)   │
├─────────────────────────────────────────────────────┤
│  Layer 2: Persistence & Storage         (SQLite)    │
├─────────────────────────────────────────────────────┤
│  Layer 1: Investigation Engine          (Python)    │
└─────────────────────────────────────────────────────┘
```

**Layer 1 (Investigation Engine)** is a pure-Python analytical pipeline. It accepts a natural-language query and produces an `InvestigationReport` with a `TribunalVerdict`. It has zero knowledge of HTTP, databases, or UI concerns. All processing downstream of the `InvestigationPlan` is deterministic.

**Layer 2 (Persistence & Storage)** provides durable storage for investigation metadata (SQLite) and investigation artifacts (filesystem). It implements the Repository pattern with dedicated interfaces for investigations, reports, graphs, verdicts, and audit.

**Layer 3 (REST API & Service Layer)** exposes the Investigation Engine through versioned HTTP endpoints. The `InvestigationService` acts as the central orchestration boundary — it coordinates engine execution, repository persistence, transient caching, and API schema serialization.

**Layer 4 (Investigation Dashboard)** is a React single-page application that consumes the REST API. It provides interactive investigation launch, history exploration, evidence graph visualization, report viewing, investigation comparison, and system health monitoring.

### 7.2 Major System Modules Summary

A high-level view of TRIBUNAL's primary architectural packages is shown below. (For the complete, file-by-file implementation tree, see [Appendix A](#appendix-a--complete-implementation-package-map)).

| Package / Module | Layer | Primary Responsibility |
|---|---|---|
| `tribunal/models/` | Layer 1 | 18 shared dataclass domain contracts (InvestigationCard, EvidenceGraph, Verdict, etc.) |
| `tribunal/planner/` | Layer 1 | Natural language parsing (Ollama + regex fallback) and execution plan generation |
| `tribunal/experts/` | Layer 1 | Domain investigators (`financial/` with 5 detectors, `behaviour/` with 7 detectors) |
| `tribunal/investigation/`| Layer 1 | Evidence Graph builder, transaction network MultiDiGraph, and provenance tracking |
| `tribunal/adversarial/`  | Layer 1 | Defense Agent 7-stage adversarial review and rebuttal card generator |
| `tribunal/consensus/`    | Layer 1 | Tribunal 6-stage deterministic deliberation, graph traversal, and verdict generation |
| `tribunal/report/`       | Layer 1 | 10-section explainability engine and multi-format renderers (MD, HTML, JSON) |
| `storage/`               | Layer 2 | SQLite database manager (8 tables) and filesystem artifact repositories |
| `api/`                   | Layer 3 | FastAPI versioned REST application, routes (`/investigate`, `/report`, `/graph`, etc.), middleware |
| `dashboard/`             | Layer 4 | React 18 + TypeScript SPA with 10 application pages and evidence graph visualizers |

---

## 8. Investigation Engine

The Investigation Engine is the analytical core of TRIBUNAL. It is a pure-Python system with no knowledge of HTTP, databases, or user interfaces. Given a natural-language query and a transaction dataset, it produces an `InvestigationReport` containing a `TribunalVerdict` with full evidence provenance.

### 8.1 Data Flow

```
Natural Language Query
         │
         ▼
┌──────────────────┐
│     Planner      │  LLM Client → Query Parser → Execution Planner
│                  │  → InvestigationPlan → ExecutionPlan
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    Case File     │  Initialized with case_id, empty state
│ (Working Memory) │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│          Expert Investigation Board          │
│                                              │
│  Financial Expert ──→ Case File updated      │
│       │                                      │
│       ▼                                      │
│  Behaviour Expert ──→ Case File updated      │
│                                              │
│  Output: Investigation Cards[]               │
└────────────────────┬─────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────┐
│       Evidence Graph Builder                 │
│                                              │
│  Cards → Nodes (account, card, hypothesis)   │
│  Relationships → Edges (support, contradict) │
│  Validation → Integrity checks               │
│  Metrics → Topology analytics                │
│                                              │
│  Output: EvidenceGraph (NetworkX DiGraph)     │
└────────────────────┬─────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────┐
│           Defense Agent                      │
│                                              │
│  Review → Contradictions → Alternatives      │
│  Strength → Uncertainty → Rebuttals          │
│                                              │
│  Output: Defense Cards → Graph Augmented     │
└────────────────────┬─────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────┐
│           Tribunal                           │
│                                              │
│  Hypotheses → Weighing → Contradiction Res.  │
│  Consensus → Calibration → Verdict           │
│                                              │
│  Output: TribunalVerdict                     │
└────────────────────┬─────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────┐
│        Report Generator                      │
│                                              │
│  Explainability Engine → Report Builder      │
│  Markdown Renderer · HTML Renderer · JSON    │
│  Report Validator                            │
│                                              │
│  Output: InvestigationReport                 │
└──────────────────────────────────────────────┘
```

### 8.2 Data Contracts

Every boundary between engine components is defined by a shared dataclass contract. There are **18 data contracts** in `tribunal/models/`:

| Contract | Purpose | Key Fields |
|---|---|---|
| `UserQuery` | Raw natural language input | `text` |
| `InvestigationPlan` | Structured query decomposition | `intent`, `target_pattern`, `filters`, `entities` |
| `ExecutionPlan` | Deterministic execution instructions | `expert_sequence`, `eda_required`, `feature_subsets` |
| `PlanningResult` | Complete planner output with metrics | `execution_plan`, `planner_context`, profiling data |
| `CaseFile` | Shared working memory | `dominant_hypothesis`, `dominant_confidence`, `evidence_cards`, `contradictions_found` |
| `PatternFinding` | Raw detector output | `pattern_type`, `score`, `affected_accounts`, `metric_evidence` |
| `InvestigationCard` | Atomic unit of evidence | `hypothesis`, `confidence`, `severity`, `evidence`, `provenance`, `supports`, `counter_hypothesis` |
| `ExpertResult` | Expert execution output | `cards`, `expert_id`, `execution_metrics` |
| `EvidenceNode` | Graph node | `node_id`, `node_type`, `label`, `confidence`, `severity`, `provenance` |
| `EvidenceEdge` | Graph edge | `source`, `target`, `relationship`, `weight`, `reason`, `confidence` |
| `EvidenceGraph` | Graph container | `nodes`, `edges`, `metrics`, `metadata`, NetworkX DiGraph wrapper |
| `TribunalVerdict` | Final determination | `verdict`, `winning_hypothesis`, `confidence`, `risk_level`, `recommendation`, `deliberation_trace` |
| `InvestigationReport` | Complete report output | 10 structured sections, 3 rendered formats (MD, HTML, JSON) |
| `Transaction` | Transaction record | `amount`, `timestamp`, `sender`, `receiver`, `currency`, `payment_format` |
| `Account` | Account metadata | `account_id`, `bank`, `account_type` |

### 8.3 Expert Architecture

All domain experts share a common pipeline architecture through `BaseInvestigationExpert`:

```
                   BaseExpert (ABC)
                        │
                        ▼
            BaseInvestigationExpert
           ┌────────────┼─────────────────┐
           │            │                 │
    FinancialExpert  BehaviourExpert  [Future Experts]

    Generic 5-Stage Pipeline:
    ┌─────────────────────────────────────────┐
    │ 1. Candidate Selection                  │
    │ 2. Detector Execution (N detectors)     │
    │ 3. Post-Processing Hook (overridable)   │
    │ 4. Confidence Aggregation (1-∏(1-sᵢ))  │
    │ 5. Card Building → InvestigationCard[]  │
    └─────────────────────────────────────────┘
```

This architecture makes adding new experts straightforward: implement the `BaseInvestigationExpert` abstract methods, provide domain-specific detectors, and the generic pipeline handles candidate selection, confidence aggregation, and card construction.

### 8.4 Feature Store

The engine operates on a pre-computed Feature Store containing **44 AML analytical features** across **705,903 accounts**, derived from **6.92 million transactions**:

| Category | Feature Count | Examples |
|---|---|---|
| Financial | 12 | Amount quantiles, rolling sums, `threshold_proximity`, `structuring_score` |
| Behaviour | 10 | Velocity, active days, `baseline_daily_amount`, `deviation_score` |
| Network | 8 | Fan-in, fan-out, degree, `repeated_counterparties` |
| Temporal | 6 | Weekend ratio, hour mode, `rapid_successive_count` |
| Statistical | 4 | Z-score, `iqr_outlier_score` |
| Rule-Ready | 4 | Composite indicators, `rapid_cashout_indicator` |

The Feature Store is persisted as Parquet (`datasets/processed/feature_store.parquet`) and loaded on demand by the `DataLoader`.

---

## 9. Persistence & Storage Layer

### 9.1 Design Philosophy

The Persistence Layer follows the Repository pattern, separating storage concerns from business logic. The `SQLiteRepository` class implements all repository interfaces, providing a single concrete implementation that combines SQLite for metadata and the filesystem for artifact content.

### 9.2 SQLite Schema

The database contains **8 tables** managing investigation lifecycle metadata:

```sql
investigations           -- Core investigation records (id, query, verdict, metrics)
reports                  -- Report artifact references (path, format, timestamps)
graphs                   -- Graph statistics (node_count, edge_count)
verdicts                 -- Tribunal verdict summaries (hypothesis, confidence)
audit                    -- Lifecycle event trail (investigation creation, retrieval)
bookmarks                -- User-bookmarked investigations
tags                     -- Investigation tag associations
saved_searches           -- Persisted search configurations
report_annotations       -- Analyst annotations on reports
```

All tables use foreign keys referencing `investigations(id)` with `ON DELETE CASCADE`, ensuring referential integrity.

### 9.3 Artifact Storage

Investigation artifacts (reports, graphs, case files, audit records) are persisted as files:

```
storage/files/
├── reports/{investigation_id}/
│   ├── report.md          # Markdown report
│   ├── report.html        # HTML report
│   └── report.json        # JSON payload
├── graphs/{investigation_id}/
│   └── graph.json         # Serialized EvidenceGraph
├── cases/{investigation_id}/
│   └── case_file.json     # Case file snapshot
└── audit/{investigation_id}/
    └── audit.json         # Audit trail events
```

### 9.4 Repository Interfaces

| Repository | Responsibility |
|---|---|
| `InvestigationRepository` | Create, read, update, delete investigation records |
| `ReportRepository` | Report artifact CRUD + annotations + compliance HTML rendering |
| `GraphRepository` | Evidence graph serialization and retrieval |
| `VerdictRepository` | Tribunal verdict storage and lookup |
| `AuditRepository` | Lifecycle event recording and retrieval |
| `SearchRepository` | Full-text search, tag management, bookmarks, saved searches |

---

## 10. REST API & Service Layer

### 10.1 API Architecture

The REST API is built on FastAPI with a versioned routing structure (`/api/v1/`), automatic OpenAPI documentation, and structured middleware:

```
FastAPI Application
│
├── Middleware Stack
│   ├── CORS (allow_origins=["*"])
│   ├── RequestLoggingMiddleware
│   └── RequestTimingMiddleware
│
├── Exception Handlers
│   ├── ServiceError → 400/404/500
│   └── StorageError → 500
│
└── /api/v1/
    ├── /investigate          POST  — Launch full investigation
    ├── /query                POST  — Lightweight query
    ├── /report/{id}          GET   — Retrieve investigation report
    ├── /graph/{id}           GET   — Retrieve evidence graph
    ├── /verdict/{id}         GET   — Retrieve tribunal verdict
    ├── /search               POST  — Search investigations
    ├── /investigations       GET   — List all investigations
    ├── /investigations/{id}  GET   — Investigation detail
    ├── /health               GET   — System health check
    ├── /status               GET   — Engine status
    └── /metadata             GET   — System metadata
```

### 10.2 Investigation Service

The `InvestigationService` is the central orchestration boundary between the REST API and the Investigation Engine. It coordinates:

1. **Input validation** — Query length, dataset availability
2. **Engine execution** — Planner → Experts → Graph → Defense → Tribunal → Report
3. **Persistence** — Atomic save of investigation record, verdict, report artifacts, graph artifacts, case file, and audit events
4. **Transient caching** — In-memory store for active investigation artifacts (thread-safe)
5. **Schema serialization** — Engine domain objects → API response schemas
6. **Performance profiling** — Microsecond-level timing for each pipeline stage

---

## 11. Investigation Dashboard

### 11.1 Technology Stack

| Technology | Role |
|---|---|
| React 18 | Component framework |
| TypeScript | Type-safe development |
| Vite | Build tooling and dev server |
| React Router | Client-side navigation |
| Tailwind CSS | Utility-first styling |
| Axios | HTTP client for API communication |

### 11.2 Page Architecture

| Page | Route | Purpose |
|---|---|---|
| Home | `/` | Landing dashboard with investigation statistics and quick actions |
| Workspace | `/investigate` | Launch new investigations with query input and dataset selection |
| History | `/history` | Browse past investigations with filtering and sorting |
| Explorer | `/explorer` | Advanced search with full-text queries, tags, and saved searches |
| Compare | `/compare` | Side-by-side investigation comparison |
| Investigation Viewer | `/investigation/:id` | Full investigation detail view |
| Report Viewer | `/report/:id` | Rich report reading experience |
| Evidence Graph | `/graph/:id` | Interactive evidence graph visualization |
| System | `/system` | Engine health, database status, and diagnostics |
| Settings | `/settings` | Application configuration |

---

## 12. Adaptive Agentic Behaviour

### Language Understanding Layer

TRIBUNAL separates language understanding from analytical reasoning. A lightweight language understanding layer converts natural-language queries into a Structured Investigation Plan containing intent, entities, filters, and execution objectives. Once the investigation plan is generated, all subsequent analytical processing — including feature engineering, expert investigation, evidence graph construction, and tribunal reasoning — is performed deterministically.

This separation is one of the strongest architectural decisions in the system. It means that the non-deterministic component (natural language interpretation) is confined to a single, well-bounded entry point. Every component downstream of the investigation plan operates on structured data, produces traceable artefacts, and executes predictably. The investigation is reproducible given the same plan — regardless of how the plan was produced.

### Dual-Mode Query Parsing

The Planner implements a resilient dual-mode parsing strategy:

1. **LLM Mode** — Ollama (Llama 3.2) processes the query with structured JSON output constraints. The LLM extracts intent, entities, patterns, and filters into a schema-validated response.
2. **Regex Fallback Mode** — When Ollama is unavailable or returns unparseable output, a deterministic regex-based parser handles common query patterns. This ensures the system never fails due to LLM unavailability.

### Query-Driven Expert Selection

The Execution Planner evaluates each incoming query and makes active decisions about what to investigate and how.

**Example 1 — Targeted Entity Investigation**

> *"Find structuring in the last 30 days for customer 541"*

Query Understanding extracts: `{intent: pattern_detection, target_pattern: structuring, customer_id: 541, date_range: last_30_days}`

Execution plan:
- Skip exploratory data analysis — single entity, specific pattern.
- Invoke Financial Pattern Expert — directly relevant to structuring detection.
- Invoke Customer Behaviour Expert — validate against customer baseline.

**Example 2 — Broad Exploratory Scan**

> *"Show me unusual activity across high-risk accounts this quarter"*

Query Understanding extracts: `{intent: broad_scan, target_pattern: anomaly, filters: {risk_level: high, date_range: current_quarter}}`

Execution plan:
- Run exploratory data analysis — broad scope requires profiling before expert invocation.
- Invoke Financial Pattern Expert — scan for threshold-adjacent patterns across multiple accounts.
- Invoke Customer Behaviour Expert — identify behavioural deviations from baselines.

---

## 13. Explainability Strategy

Explainability is not a feature of TRIBUNAL — it is an architectural property. The system does not generate explanations after reaching a conclusion. The conclusion *is* the explanation, because it is assembled from traceable, structured components at every stage.

### The Explainability Chain

```
Investigation Cards
        ↓
  Each card carries: hypothesis, evidence, confidence,
  severity, counter-hypothesis, missing data,
  supporting metrics, provenance metadata
        ↓
Evidence Graph
        ↓
  Cards become nodes. Relationships become weighted edges.
  The graph preserves all support, contradiction,
  corroboration, and derivation semantics.
        ↓
Adversarial Challenge
        ↓
  Defense cards challenge the dominant theory
  with plausible alternative explanations.
  Rebuttal edges are added, not substituted.
        ↓
Tribunal Deliberation
        ↓
  6-stage deterministic deliberation with
  full trace recording at each step.
        ↓
Winning Chain
        ↓
  The hypothesis path with the highest net support
  after adversarial challenge — fully traceable.
        ↓
Runner-up
        ↓
  The second-strongest hypothesis and the specific
  evidence that decided against it.
        ↓
Missing Evidence
        ↓
  Data that was unavailable but would have materially
  affected the conclusion — surfaced as caveats, not hidden.
        ↓
Recommendation
        ↓
  Verdict category with risk level and recommendation —
  grounded in evidence, not derived from an opaque score.
```

### Why This Matters

Traditional AML systems produce an alert. An analyst must then reconstruct *why* the alert fired — often from scratch.

Single-model AI approaches produce a score and a natural-language explanation. But the explanation is generated *after* the score — it is a rationalization, not a derivation.

TRIBUNAL's explanation *is* the derivation. The report does not describe what the system concluded — it shows how the system concluded it. Every hypothesis traces to the expert that proposed it. Every piece of evidence traces to the transactions that produced it. Every rejection traces to the contradiction that defeated it.

This structural design makes transparency inherent to the process.

### Investigation Card Provenance

Every Investigation Card carries complete provenance metadata:

```json
{
  "card_id": "card_fin_001",
  "source_expert": "financial",
  "derived_from_transactions": ["txn_1042", "txn_1043", "txn_1050"],
  "generated_at": "2026-07-24T15:22:10",
  "hypothesis": "structuring",
  "confidence": 0.82,
  "severity": "HIGH",
  "evidence": "12 deposits of $9,700–$9,900 over 4 days, all below $10,000 reporting threshold",
  "supporting_metrics": {"threshold_proximity": 0.97, "structuring_score": 0.85},
  "provenance": {"detector": "structuring_detector", "feature_set": ["rolling_sum_7d"]},
  "counter_hypothesis": "cash_intensive_business",
  "missing_data": "merchant_category",
  "supports": ["card_fin_003"]
}
```

Each field maps directly to a graph element:
- `hypothesis` + `confidence` + `evidence` → the **node**.
- `supports` → an outgoing **support edge**.
- `counter_hypothesis` → a candidate **contradiction edge** the Defense Agent can strengthen.
- `missing_data` → a **caveat** surfaced directly in the final report.

---

## 14. Technical Architecture

### 14.1 Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| Language | Python 3.x | Unified ecosystem for data processing, graph operations, ML, and language understanding |
| Language Understanding | Ollama (Llama 3.2) | Local inference for converting natural-language queries into structured investigation plans |
| Graph Engine | NetworkX | In-memory directed graph — zero infrastructure overhead, sufficient for investigation-scale graphs |
| Statistical / ML | scikit-learn, NumPy | Isolation Forest for outlier detection, z-score computation |
| Data Processing | pandas | Transaction data manipulation, filtering, aggregation |
| Feature Persistence | Apache Parquet | Columnar storage for 44-feature × 705K-account feature store |
| REST API | FastAPI | High-performance async Python API with automatic OpenAPI documentation |
| Database | SQLite | Zero-configuration embedded database for investigation metadata |
| Frontend Framework | React 18 + TypeScript | Component-based interactive UI with type safety |
| Frontend Build | Vite | Fast development server and optimized production builds |
| Frontend Styling | Tailwind CSS | Utility-first CSS framework for rapid UI development |
| HTTP Client | Axios | Promise-based HTTP client for dashboard → API communication |

### 14.2 Configuration

All configurable parameters are centralized in `tribunal/config/settings.py`:

| Parameter | Default | Purpose |
|---|---|---|
| `REPORTING_THRESHOLD` | $10,000 | Currency Transaction Report filing threshold |
| `STRUCTURING_MARGIN` | $500 | Detection margin below reporting threshold |
| `VELOCITY_SPIKE_THRESHOLD` | 200% | Transaction velocity anomaly threshold |
| `BEHAVIOUR_DEVIATION_THRESHOLD` | 150% | Baseline deviation trigger |
| `DEFENSE_PLAUSIBILITY_THRESHOLD` | 0.40 | Minimum plausibility for defense card generation |
| `HIGH_RISK_THRESHOLD` | 0.75 | Confidence score for HIGH risk classification |
| `MEDIUM_RISK_THRESHOLD` | 0.50 | Confidence score for MEDIUM risk classification |
| `REINVESTIGATION_THRESHOLD` | 0.45 | Confidence below which re-investigation is triggered |
| `BASELINE_WINDOW_DAYS` | 90 | Historical window for baseline computation |
| `DEFAULT_QUERY_WINDOW_DAYS` | 30 | Default date range for targeted queries |
| `ZSCORE_THRESHOLD` | 2.5 | Z-score threshold for statistical outlier detection |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama inference server endpoint |
| `OLLAMA_MODEL` | `llama3.2` | Language model for query understanding |

### 14.3 Testing Architecture

The test suite is organized in three tiers:

| Tier | Count | Scope |
|---|---|---|
| **Unit Tests** | 54 files | Individual module correctness — detectors, parsers, builders, renderers |
| **Integration Tests** | 7 files | Cross-module interactions — API routes, storage, graph-to-verdict pipeline |
| **End-to-End Tests** | Stubs | Full pipeline: query in → report out |

**Total: 142 passing tests** across all tiers.

Key test fixtures generate realistic AML scenarios: structuring patterns, velocity spikes, dormancy reactivation, and mixed-signal cases.

---

## 15. Future Improvements & Evolution Roadmap

TRIBUNAL v1.0 implements the complete core investigation paradigm. The following improvements are designed to evolve the system toward the full proposed vision — a comprehensive, enterprise-grade investigation platform.

### 15.1 Investigation Engine Expansion

#### Network Intelligence Expert
**Priority:** High · **Complexity:** Medium

A third domain expert specializing in counterparty network analysis. Traces fund flow across the transaction graph (already built as `TransactionNetworkBuilder`) to detect:
- Fan-out patterns (one account distributing to many)
- Layering chains (A → B → C → D with similar amounts)
- Circular fund flows (money returning to origin through intermediaries)
- Counterparty risk clustering (shared counterparties among flagged accounts)

**Integration point:** The `BaseInvestigationExpert` architecture already supports plugging in new experts — implement `NetworkExpert(BaseInvestigationExpert)` with network-specific detectors.

#### Regulatory Rule Expert
**Priority:** Medium · **Complexity:** Medium

A compliance-focused expert that matches investigation evidence against jurisdiction-specific regulatory rules:
- FATF (Financial Action Task Force) red flag indicators
- BSA/AML (Bank Secrecy Act) reporting thresholds by jurisdiction
- EU Anti-Money Laundering Directive requirements
- PEP (Politically Exposed Persons) screening integration

This expert does not generate hypotheses from data analysis — it matches existing evidence against a regulatory rule library.

#### Geographic & Temporal Experts
**Priority:** Low · **Complexity:** High

Specialized experts for cross-border transaction analysis (geographic risk scoring, sanctions screening, correspondent banking chains) and time-series pattern analysis (seasonal normalization, trend detection, temporal clustering).

### 15.2 Adversarial System Enhancement

#### Multi-Round Adversarial Debate
**Priority:** Medium · **Complexity:** High

Evolve the current single-pass defense review into a structured multi-round debate:
1. **Prosecution** presents the evidence and dominant hypothesis
2. **Defense** challenges with alternative explanations
3. **Prosecution** responds with counter-rebuttals
4. **Tribunal** evaluates both sides after N rounds (bounded)

This models how real compliance review boards operate — iterative challenge and response — while remaining bounded to prevent infinite loops.

#### Confidence-Budget Planner
**Priority:** Low · **Complexity:** Medium

An expected-gain scoring system that evaluates whether invoking an additional expert or re-investigation round is worth the computational cost. If the marginal expected confidence gain exceeds a threshold, the system invokes; otherwise, it proceeds directly to the Tribunal.

### 15.3 Persistence & Data Architecture

#### Graph Database Backend
**Priority:** Medium · **Complexity:** High

Replace the in-memory NetworkX Evidence Graph with a persistent graph database (e.g., Neo4j) for:
- Cross-investigation evidence linking
- Historical pattern matching across past cases
- Graph queries that span multiple investigations
- Scalable storage beyond investigation-scale graphs

The `EvidenceGraph` wrapper class already abstracts graph operations, providing a natural migration path.

#### Continuous Investigation Memory
**Priority:** Medium · **Complexity:** Medium

A cross-investigation knowledge base that persists entity risk profiles, historical verdicts, and recurring patterns:
- "Has this account been flagged before?"
- "What was the verdict last time this pattern appeared?"
- Cumulative risk scoring across investigations for the same entity

### 15.4 Platform Capabilities

#### Security, Identity & Access Management
**Priority:** High · **Complexity:** High

Transform TRIBUNAL from a single-user investigation application into a secure multi-user platform:
- Authentication (JWT-based session management)
- Role-Based Access Control (Investigator, Reviewer, Admin)
- Investigation ownership and access permissions
- Audit trail attribution (who performed which investigation)
- API key management for programmatic access

#### Real-Time Investigation Streaming
**Priority:** Low · **Complexity:** Medium

Replace the current synchronous request-response pattern with WebSocket-based streaming:
- Live progress updates during investigation execution
- Per-stage results streamed as they complete
- Dashboard shows investigation progress in real-time

#### Domain Generalization
**Priority:** Low · **Complexity:** High

Extend the investigation framework beyond AML to adjacent domains:
- **Fraud detection** — Transaction fraud investigation with fraud-specific experts
- **Insider trading** — Trading pattern analysis with market-specific experts
- **Insurance claims** — Claims investigation with domain-specific detection
- **Cyber security** — Threat investigation with network and behavioural analysis

The expert architecture (`BaseInvestigationExpert`) and evidence graph framework are domain-agnostic by design — the investigation paradigm generalizes.

### 15.5 Evolution Priority Matrix

```
                          IMPACT
                    Low         High
              ┌──────────┬──────────┐
         Low  │ Temporal │ Reg.Rule │
              │ Experts  │ Expert   │
  EFFORT      │          │          │
              ├──────────┼──────────┤
         High │ Domain   │ Network  │
              │ General. │ Expert   │
              │ RT Stream│ Graph DB │
              │ Conf.    │ Auth/IAM │
              │ Budget   │ Multi-Rnd│
              │          │ Memory   │
              └──────────┴──────────┘
```

**Recommended next phase:** Network Intelligence Expert + Security/IAM — highest impact, leveraging existing infrastructure (transaction graph + API layer).

---

## 16. Conclusion

TRIBUNAL reimagines AML compliance through structured agentic investigation.

Where traditional systems produce alerts, TRIBUNAL produces investigations. Where single-model AI approaches produce scores, TRIBUNAL produces evidence chains. Where existing tools leave analysts to reconstruct reasoning from scratch, TRIBUNAL delivers a complete investigative narrative — from query to evidence to hypothesis to challenge to verdict.

The system's strength lies not in any single component, but in the architecture itself: specialized experts contribute structured evidence, an adversarial process challenges the dominant theory, and a tribunal reasons over the accumulated body of evidence to reach an explainable conclusion.

**What exists today** is a fully operational, four-layer investigation platform — an agentic engine with 11 specialized detectors, a 7-stage adversarial review, a 6-stage tribunal deliberation, a 10-section report generator, persistent storage with audit trails, a versioned REST API, and an interactive investigation dashboard — verified by 142 passing tests.

**What lies ahead** is the evolution from a powerful single-user investigation tool into an enterprise-grade compliance platform — with network intelligence, multi-round adversarial debates, persistent investigation memory, and secure multi-user access.

Every recommendation is traceable. Every hypothesis is contestable. Every verdict is auditable.

TRIBUNAL is not another fraud detection model.

It is an **explainable AI investigation framework**.

---

## Appendix A — Complete Implementation Package Map

```
TRIBUNAL/
│
├── tribunal/                              # Layer 1: Investigation Engine
│   ├── models/                            # 18 shared data contracts (dataclasses)
│   │   ├── investigation_plan.py          #   InvestigationPlan
│   │   ├── execution_plan.py              #   ExecutionPlan
│   │   ├── planning_result.py             #   PlanningResult
│   │   ├── case_file.py                   #   CaseFile (shared working memory)
│   │   ├── investigation_card.py          #   InvestigationCard (atomic evidence)
│   │   ├── expert_result.py               #   ExpertResult
│   │   ├── pattern_finding.py             #   PatternFinding, MetricEvidence
│   │   ├── evidence_node.py               #   EvidenceNode (graph node)
│   │   ├── evidence_edge.py               #   EvidenceEdge (graph edge)
│   │   ├── evidence_graph.py              #   EvidenceGraph (NetworkX wrapper)
│   │   ├── tribunal_verdict.py            #   TribunalVerdict
│   │   ├── investigation_report.py        #   InvestigationReport
│   │   ├── transaction.py                 #   Transaction
│   │   ├── account.py                     #   Account
│   │   ├── user_query.py                  #   UserQuery
│   │   ├── query_context.py               #   QueryContext
│   │   └── planner_output.py              #   PlannerOutput
│   │
│   ├── planner/                           # Query understanding & execution planning
│   │   ├── planner.py                     #   Orchestrator (UserQuery → PlanningResult)
│   │   ├── llm_client.py                  #   Ollama communication with retry logic
│   │   ├── query_parser.py                #   LLM output → InvestigationPlan
│   │   ├── execution_planner.py           #   InvestigationPlan → ExecutionPlan
│   │   ├── planner_constants.py           #   Vocabulary: intents, patterns, experts
│   │   ├── prompts.py                     #   System prompts and JSON schema defs
│   │   └── exceptions.py                  #   Planner exception hierarchy
│   │
│   ├── experts/                           # Domain expert investigators
│   │   ├── base_expert.py                 #   BaseExpert (ABC) + BaseInvestigationExpert
│   │   ├── financial/                     #   Financial Pattern Expert
│   │   │   ├── financial_expert.py        #     Entry point (5-stage pipeline)
│   │   │   ├── candidate_selector.py      #     Target entity filtering
│   │   │   ├── structuring_detector.py    #     Near-threshold structuring ($8K–$10K)
│   │   │   ├── velocity_detector.py       #     Rapid transaction velocity
│   │   │   ├── large_transfer_detector.py #     Statistical outlier detection
│   │   │   ├── frequency_detector.py      #     High-frequency spike detection
│   │   │   ├── confidence.py              #     Probabilistic confidence aggregator
│   │   │   └── card_builder.py            #     PatternFinding → InvestigationCard
│   │   └── behaviour/                     #   Customer Behaviour Expert
│   │       ├── behaviour_expert.py        #     Entry point (7-stage pipeline)
│   │       ├── candidate_selector.py      #     Baseline deviation filtering
│   │       ├── behaviour_drift_detector.py#     Daily amount/frequency deviation
│   │       ├── dormancy_detector.py       #     Dormant account reactivation
│   │       ├── spending_pattern_detector.py#    Distribution shift detection
│   │       ├── currency_change_detector.py#     Unexpected currency switching
│   │       ├── payment_pattern_detector.py#     Format shift (ACH→Wire/Cash)
│   │       ├── counterparty_behaviour_detector.py # Network expansion
│   │       ├── confidence.py              #     Probabilistic score aggregator
│   │       └── card_builder.py            #     PatternFinding → InvestigationCard
│   │
│   ├── investigation/                     # Evidence graph construction
│   │   ├── evidence/                      #   Graph construction sub-modules
│   │   │   ├── evidence_graph_builder.py  #     Main orchestrator (build + augment)
│   │   │   ├── evidence_linker.py         #     Node generation + relationship inference
│   │   │   ├── evidence_merger.py         #     Same-expert card deduplication
│   │   │   ├── graph_validator.py         #     Structural integrity validation
│   │   │   ├── graph_metrics.py           #     Topology analytics
│   │   │   └── provenance_manager.py      #     Lineage tracking
│   │   ├── transaction_network_builder.py #   Account transfer graph (MultiDiGraph)
│   │   └── transaction_graph.py           #   Graph-derived feature extraction
│   │
│   ├── adversarial/                       # Adversarial investigation phase
│   │   ├── defense_agent.py               #   7-stage review pipeline orchestrator
│   │   ├── evidence_reviewer.py           #   Graph traversal → ReviewContext
│   │   ├── contradiction_detector.py      #   Conflicting finding detection
│   │   ├── alternative_hypothesis_generator.py # Non-malicious explanation gen
│   │   ├── evidence_strength_analyzer.py  #   Evidence scoring + provenance check
│   │   ├── uncertainty_estimator.py       #   Sparsity + diversity estimation
│   │   ├── confidence_adjuster.py         #   Defense card confidence computation
│   │   └── rebuttal_builder.py            #   Defense InvestigationCard construction
│   │
│   ├── consensus/                         # Tribunal consensus engine
│   │   ├── tribunal.py                    #   6-stage deliberation orchestrator
│   │   ├── hypothesis_extractor.py        #   Candidate hypothesis identification
│   │   ├── evidence_weigher.py            #   Raw support score calculation
│   │   ├── contradiction_resolver.py      #   Net Evidence Strength computation
│   │   ├── consensus_engine.py            #   Hypothesis ranking + consensus
│   │   ├── confidence_calibrator.py       #   Final confidence calibration
│   │   ├── risk_calibrator.py             #   Confidence → risk level mapping
│   │   ├── verdict_builder.py             #   TribunalVerdict assembly
│   │   └── deliberation_trace.py          #   Step-by-step trace recording
│   │
│   ├── report/                            # Investigation report generation
│   │   ├── report_generator.py            #   Main orchestrator (single public interface)
│   │   ├── report_builder.py              #   10-section report construction
│   │   ├── report_validator.py            #   Report completeness validation
│   │   ├── explainability_engine.py       #   Evidence chain reconstruction
│   │   ├── executive_summary.py           #   Executive summary section builder
│   │   ├── evidence_summarizer.py         #   Evidence aggregation section builder
│   │   ├── graph_summarizer.py            #   Graph topology section builder
│   │   ├── investigation_timeline.py      #   Chronological timeline builder
│   │   ├── tribunal_summary.py            #   Deliberation narrative builder
│   │   ├── renderer_markdown.py           #   Markdown format renderer
│   │   ├── renderer_html.py               #   HTML format renderer
│   │   └── renderer_json.py               #   JSON payload renderer
│   │
│   ├── tools/                             # Shared analytical tools
│   │   ├── feature_store_builder.py       #   44-feature AML feature store (Parquet)
│   │   ├── feature_definitions.py         #   Feature schemas for both experts
│   │   ├── feature_engineering.py         #   Rolling sums, velocity, deviation
│   │   ├── anomaly_detection.py           #   Statistical outlier detection
│   │   └── eda_tool.py                    #   Exploratory data analysis
│   │
│   ├── data/                              # Data ingestion & validation
│   │   ├── loader.py                      #   DataLoader (Parquet/CSV + feature store)
│   │   ├── validator.py                   #   Schema & quality validation
│   │   └── dataset_resolver.py            #   Dataset path resolution
│   │
│   ├── config/                            # System configuration
│   │   └── settings.py                    #   Thresholds, URLs, paths
│   │
│   ├── utils/                             # Cross-cutting utilities
│   │   ├── logger.py                      #   Structured logging
│   │   └── ollama_client.py               #   Ollama inference wrapper
│   │
│   ├── datasets/                          # AML investigation datasets
│   │   ├── raw/                           #   Original CSV files
│   │   └── processed/                     #   Parquet, feature store, network graph
│   │
│   ├── tests/                             # Test suite (142 tests)
│   │   ├── unit/                          #   54 unit test files
│   │   ├── integration/                   #   7 integration test files
│   │   └── e2e/                           #   End-to-end test stubs
│   │
│   └── scripts/                           # Build & verification scripts
│       ├── preprocess_dataset.py          #   CSV → Parquet conversion
│       ├── build_network.py               #   Transaction network construction
│       ├── build_feature_store.py         #   Feature store computation
│       └── profile_dataset.py             #   Dataset statistical profiling
│
├── api/                                   # Layer 3: REST API & Service Layer
│   ├── app.py                             #   FastAPI application factory
│   ├── routes/                            #   Endpoint definitions
│   │   ├── investigate.py                 #     POST /investigate, /query
│   │   ├── reports.py                     #     GET /report/{id}, annotations
│   │   ├── graph.py                       #     GET /graph/{id}, /verdict/{id}
│   │   ├── search.py                      #     POST /search, bookmarks, tags
│   │   ├── metadata.py                    #     GET /investigations, /stats
│   │   └── health.py                      #     GET /health, /status
│   ├── services/                          #   Business logic orchestration
│   │   └── investigation_service.py       #     Central orchestration boundary
│   ├── schemas/                           #   Pydantic request/response models
│   │   ├── investigation.py              #     Investigation request/response
│   │   ├── report.py                      #     Report response schemas
│   │   ├── graph.py                       #     Graph/verdict response schemas
│   │   └── common.py                      #     Shared pagination, error schemas
│   ├── middleware/                         #   Request processing pipeline
│   │   ├── exceptions.py                 #     Global exception handlers
│   │   ├── logging.py                     #     Request logging middleware
│   │   └── timing.py                      #     Request timing middleware
│   └── dependencies/                      #   Dependency injection
│
├── storage/                               # Layer 2: Persistence & Storage
│   ├── database.py                        #   DatabaseManager + schema DDL (8 tables)
│   ├── models.py                          #   Storage record dataclasses
│   ├── session.py                         #   Connection session management
│   ├── repositories/                      #   Repository interfaces
│   │   ├── investigation_repository.py    #     Investigation CRUD
│   │   ├── report_repository.py           #     Report + annotation CRUD
│   │   ├── graph_repository.py            #     Graph artifact CRUD
│   │   ├── verdict_repository.py          #     Verdict CRUD
│   │   ├── audit_repository.py            #     Audit trail CRUD
│   │   └── search_repository.py           #     Full-text search + saved searches
│   ├── sqlite/                            #   Concrete implementations
│   │   └── sqlite_repository.py           #     SQLiteRepository (all interfaces)
│   └── files/                             #   Artifact filesystem storage
│       ├── reports/                        #     Report artifacts (MD, HTML, JSON)
│       ├── graphs/                        #     Graph artifacts (JSON, gpickle)
│       ├── cases/                         #     Case file snapshots (JSON)
│       └── audit/                         #     Audit trail records (JSON)
│
├── dashboard/                             # Layer 4: Investigation Dashboard
│   ├── src/
│   │   ├── App.tsx                        #   Application shell + routing
│   │   ├── pages/                         #   10 application pages
│   │   │   ├── HomePage.tsx               #     Dashboard landing + quick stats
│   │   │   ├── WorkspacePage.tsx           #     New investigation launch
│   │   │   ├── HistoryPage.tsx            #     Past investigation browser
│   │   │   ├── ExplorerPage.tsx           #     Search + filtering explorer
│   │   │   ├── ComparePage.tsx            #     Side-by-side comparison
│   │   │   ├── ViewerPage.tsx             #     Full investigation viewer
│   │   │   ├── ReportViewerPage.tsx       #     Report reading view
│   │   │   ├── EvidenceGraphPage.tsx      #     Interactive graph visualization
│   │   │   ├── SystemPage.tsx             #     System health & diagnostics
│   │   │   └── SettingsPage.tsx           #     Application settings
│   │   ├── components/                    #   Reusable UI components
│   │   │   ├── layout/                    #     Navbar, Sidebar
│   │   │   ├── graph/                     #     Evidence graph visualization
│   │   │   ├── report/                    #     Report rendering components
│   │   │   ├── search/                    #     Search & filter components
│   │   │   └── common/                    #     Shared UI elements
│   │   ├── services/                      #   API client modules
│   │   │   ├── api.ts                     #     Investigation API client
│   │   │   ├── graph_api.ts               #     Graph API client
│   │   │   ├── report_api.ts              #     Report API client
│   │   │   └── search_api.ts              #     Search API client
│   │   ├── hooks/                         #   React hooks
│   │   │   └── useEvidenceGraph.ts        #     Evidence graph data hook
│   │   └── types/                         #   TypeScript type definitions
│   │       ├── index.ts                   #     Core types
│   │       ├── graph.ts                   #     Graph types
│   │       ├── report.ts                  #     Report types
│   │       └── search.ts                  #     Search types
│   ├── index.html                         #   Application entry point
│   ├── vite.config.ts                     #   Vite build configuration
│   ├── tailwind.config.js                 #   Tailwind CSS configuration
│   └── package.json                       #   Node.js dependencies
│
└── docs/                                  # Project documentation
    ├── Data_Contracts.md                  #   Shared data contract specifications
    ├── Development_Roadmap.md             #   Phase-by-phase implementation tracker
    └── Phase_D/                           #   Phase D implementation records
```

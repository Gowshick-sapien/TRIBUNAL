# TRIBUNAL — Architecture Design Specification v1.0

**Document Classification:** Canonical Architecture Reference
**Version:** 1.0
**System Name:** TRIBUNAL — Transparent Review through Investigative Board Using Nuanced Agentic Logic

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Solution Philosophy](#3-solution-philosophy)
4. [Core Design Principles](#4-core-design-principles)
5. [High-Level Architecture](#5-high-level-architecture)
6. [Investigation Lifecycle](#6-investigation-lifecycle)
7. [Core Components](#7-core-components)
8. [Adaptive Agentic Behaviour](#8-adaptive-agentic-behaviour)
9. [Explainability Strategy](#9-explainability-strategy)
10. [Architecture Scope](#10-architecture-scope)
11. [Technical Architecture](#11-technical-architecture)
12. [Conclusion](#12-conclusion)

---

## 1. Executive Summary

Financial institutions worldwide rely on rule-based Anti-Money Laundering (AML) systems that produce overwhelming volumes of false positives while providing limited explainability. For every genuinely suspicious case flagged, analysts must manually triage dozens — sometimes hundreds — of benign alerts, each requiring hours of investigation with no structured reasoning trail. Existing AI approaches frequently replace rules with a single prediction model, but the fundamental problem remains: an isolated risk score with little transparency into how a conclusion was reached.

**TRIBUNAL proposes a different paradigm.**

Instead of allowing a single AI model to determine whether a transaction is suspicious, TRIBUNAL models the investigation process performed by compliance analysts. Specialized AI investigators collaboratively build evidence, challenge competing hypotheses, and collectively arrive at an explainable verdict through structured reasoning.

The system operates as an *AI Investigation Board* — a sequential panel of domain experts that each generate competing hypotheses as structured Investigation Cards. Those cards are wired into a weighted evidence graph — support and contradiction edges — which a tribunal reasons over to find the strongest explainable chain of evidence, before recommending an escalation action.

Every conclusion is fully traceable back to the supporting evidence, making the final recommendation understandable, auditable, and defensible.

TRIBUNAL does not produce scores. It produces verdicts — with reasoning.

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

TRIBUNAL treats AML analysis as an **investigation** rather than a **classification task**.

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

This is where the innovation lies — not in a better model, but in a better *process*.

---

## 4. Core Design Principles

Six principles govern every architectural decision in TRIBUNAL. They are not aspirational — they are structural constraints.

### Principle 1 — Investigation Over Prediction

TRIBUNAL does not predict whether a customer is suspicious. It investigates. The output is not a probability — it is a structured body of evidence, a dominant hypothesis, a challenged alternative, and a reasoned recommendation. The distinction is fundamental: predictions can be wrong silently; investigations leave a trail.

### Principle 2 — Evidence Before Verdict

No component in the system is permitted to render a final verdict. Experts produce Investigation Cards — structured evidence artefacts. The Evidence Graph organizes relationships between those artefacts. Only the Tribunal, reasoning over the complete graph, produces a recommendation. This separation ensures that conclusions emerge from evidence, never from assumption.

### Principle 3 — Explainability by Construction

Explainability in TRIBUNAL is not a post-hoc feature bolted onto a black-box model. The architecture is designed so that every recommendation is *inherently* explainable — because it is constructed from traceable components. Investigation Cards carry provenance metadata. Evidence Graphs preserve relationship semantics. The final report reconstructs the reasoning chain from graph traversal, not from prompt engineering.

### Principle 4 — Sequential Collaborative Reasoning

Experts do not operate in isolation. They investigate sequentially, each reading the shared Case File before beginning work. The Customer Behaviour Expert does not start from scratch — it reads the Financial Expert's dominant hypothesis and specifically targets its investigation to support or undercut that hypothesis. This sequential, case-file-aware collaboration models how real compliance teams operate.

### Principle 5 — Query-Aware Execution

TRIBUNAL does not run the same pipeline for every query. The Planner analyses the user's intent, extracts entities and parameters, and constructs a tailored execution plan. A broad exploratory query activates different experts and tools than a targeted single-entity investigation. The system adapts its investigative strategy to the question being asked.

### Principle 6 — Full Evidence Provenance

Every Investigation Card records which expert generated it, which transactions contributed to it, and when it was created. Every edge in the Evidence Graph records the relationship type, the weight, and the reason for the connection. The final report traces backward from recommendation to evidence to source data. Nothing is asserted without attribution.

---

## 5. High-Level Architecture

TRIBUNAL is composed of eight conceptual components arranged in a directed investigation pipeline. The user's query enters at the top and an explainable investigation report exits at the bottom.

```
                            ┌─────────────┐
                            │  User Query │
                            └──────┬──────┘
                                   │
                            ┌──────▼──────┐
                            │   Planner   │
                            │  (Intent &  │
                            │  Execution  │
                            │   Planning) │
                            └──────┬──────┘
                                   │
                            ┌──────▼──────┐
                            │  Case File  │
                            │  (Shared    │
                            │   Working   │
                            │   Memory)   │
                            └──────┬──────┘
                                   │
                     ┌─────────────▼─────────────┐
                     │  Expert Investigation     │
                     │  Board                    │
                     │  ┌───────────────────────┐ │
                     │  │ Financial Expert      │ │
                     │  │        ↓              │ │
                     │  │ Behaviour Expert      │ │
                     │  │        ↓              │ │
                     │  │ [Additional Experts]  │ │
                     │  └───────────────────────┘ │
                     └─────────────┬─────────────┘
                                   │
                          Investigation Cards
                                   │
                            ┌──────▼──────┐
                            │  Evidence   │
                            │  Graph      │
                            └──────┬──────┘
                                   │
                            ┌──────▼──────┐
                            │  Defense    │
                            │  Agent      │
                            └──────┬──────┘
                                   │
                            ┌──────▼──────┐
                            │  Tribunal   │
                            │  (Consensus │
                            │   Engine)   │
                            └──────┬──────┘
                                   │
                            ┌──────▼──────┐
                            │Investigation│
                            │   Report    │
                            └─────────────┘
```

| Component | Role |
|---|---|
| **User Query** | The natural-language question that initiates the investigation. |
| **Planner** | Parses intent and entities, decides which experts to invoke and in what order. |
| **Case File** | Shared working memory — carries the dominant hypothesis, confidence, and open questions between sequential experts. |
| **Expert Investigation Board** | A sequential panel of domain-specific investigators, each contributing structured evidence to the Case File. |
| **Evidence Graph** | A directed graph where nodes are Investigation Cards and edges represent support, contradiction, or missing-evidence relationships. |
| **Defense Agent** | An adversarial investigator that challenges the dominant hypothesis with the strongest legitimate counter-explanation. |
| **Tribunal** | The consensus engine that reasons over the Evidence Graph to identify the winning hypothesis, the runner-up, and the evidence that decided between them. |
| **Investigation Report** | The final output — a structured, explainable document tracing from query to evidence to verdict. |

---

## 6. Investigation Lifecycle

Every query that enters TRIBUNAL follows a structured investigation lifecycle. This section walks through the complete journey from question to recommendation.

### Stage 1 — User Query

The user poses a natural-language question. This may be a targeted investigation (*"Find structuring in the last 30 days for customer 541"*), an exploratory scan (*"Show unusual patterns across all high-risk accounts"*), or a compliance check (*"Has customer 1023 been flagged before?"*). The query's nature determines the investigation plan.

### Stage 2 — Planner

The Planner extracts structured parameters from the query — intent, entity identifiers, date ranges, target patterns, and filters. It then constructs an execution plan: which experts to invoke, in what order, and whether exploratory data analysis is needed. The Planner initializes an empty Case File and hands control to the Expert Investigation Board.

### Stage 3 — Expert Investigation

Experts execute sequentially, each reading the current Case File before beginning their investigation. The first expert investigates without prior context. Each subsequent expert reads the evolving Case File and directs its investigation relative to the current dominant hypothesis — reinforcing, refuting, or refining it.

### Stage 4 — Investigation Cards

Each expert emits one or more Investigation Cards — structured evidence artefacts containing a hypothesis, supporting evidence, confidence score, counter-hypothesis, missing data, and provenance metadata. An expert may produce multiple competing hypotheses from the same evidence. Cards are the atomic unit of reasoning in TRIBUNAL.

### Stage 5 — Evidence Graph

The Evidence Graph Construction Engine translates Investigation Cards into a directed graph. Each card becomes a node. Edges are derived directly from each card's declared relationships — `supports` fields become support edges, `counter_hypothesis` fields become candidate contradiction edges. Edge weights encode the strength of support or contradiction. The graph is the central reasoning structure.

### Stage 6 — Defense

The Defense Agent reads only the Case File's current dominant hypothesis and argues the strongest legitimate counter-explanation. If the counter-explanation holds against the evidence, a contradiction edge is added to the graph. If it does not survive scrutiny, no edge is added. The Defense Agent does not generate new evidence — it stress-tests existing conclusions.

### Stage 7 — Tribunal

The Tribunal walks the Evidence Graph, computing net support for each hypothesis chain (support weight minus contradiction weight). It identifies the winning hypothesis — the chain with the highest net support that survives adversarial challenge — and the runner-up hypothesis, along with the specific evidence that decided between them. Confidence maps to an escalation tier.

### Stage 8 — Investigation Report

The Report Generator produces the final output: a structured document that recaps the original query, lists the experts invoked and why, presents the winning evidence chain, explains why the runner-up was rejected, surfaces missing-evidence caveats, and delivers a final recommendation — **Monitor**, **Review**, or **Report**.

---

## 7. Core Components

### 7.1 Planner

**Purpose**
The Planner is the entry point of every investigation. It translates a natural-language query into a structured execution plan that determines what the system investigates and how.

**Responsibilities**
- Parse user queries to extract intent, entity identifiers, date ranges, geographic filters, transaction types, and target AML patterns.
- Classify the query type (single-entity investigation, broad pattern scan, compliance check).
- Determine which experts to invoke and in what order, based on the query's requirements.
- Decide whether exploratory data analysis is needed (broad queries) or can be skipped (targeted queries).
- Initialize the Case File with an empty state.

**Inputs**
- Natural-language user query.

**Outputs**
- Structured execution plan: `{intent, filters, target_pattern, expert_sequence, eda_required}`.
- Initialized Case File.

---

### 7.2 Financial Pattern Expert

**Purpose**
The Financial Pattern Expert investigates transactional evidence for known AML typologies — structuring, smurfing, velocity anomalies, and threshold-adjacent behaviour.

**Responsibilities**
- Detect deposits clustered below reporting thresholds (structuring/smurfing patterns).
- Compute rolling transaction sums, velocity metrics, and amount deviation from customer baselines.
- Apply statistical outlier detection where appropriate (z-score, Isolation Forest).
- Emit one to three Investigation Cards with competing hypotheses where the evidence supports multiple interpretations.
- Write the dominant hypothesis, confidence, and open questions to the Case File.

**Inputs**
- Transaction data filtered by the Planner's execution plan.
- Empty or initialized Case File.

**Outputs**
- One to three Investigation Cards.
- Updated Case File with dominant hypothesis and confidence.

---

### 7.3 Customer Behaviour Expert

**Purpose**
The Customer Behaviour Expert investigates whether a customer's current activity deviates from their historical baseline — and specifically targets the hypothesis established by prior experts.

**Responsibilities**
- Read the current Case File before beginning investigation.
- Direct investigation relative to the dominant hypothesis — if the Financial Expert flagged structuring, the Behaviour Expert specifically checks whether behavioural patterns support or undercut that hypothesis.
- Compute historical deviation metrics: current activity versus the customer's own baseline.
- Evaluate profile-context alignment: declared income, business type, and transaction pattern coherence.
- Emit one to two Investigation Cards and update the Case File if its findings are stronger.

**Inputs**
- Customer historical data and profile information.
- Current Case File (with dominant hypothesis from prior experts).

**Outputs**
- One to two Investigation Cards.
- Updated Case File (if findings override the current dominant hypothesis).

---

### 7.4 Case File

**Purpose**
The Case File is the shared working memory of the investigation. It carries the evolving state of the case between sequential experts, ensuring that each investigator builds upon — rather than duplicates — prior work.

**Responsibilities**
- Store the current dominant hypothesis, confidence score, and open questions.
- Track contradictions found during the investigation.
- Record which investigation stage is currently active.
- Provide a read interface for downstream experts and the Defense Agent.

**Inputs**
- Updates from each expert upon completion of their investigation.

**Outputs**
- Current investigation state available to all subsequent components.

**Schema**
```json
{
  "dominant_hypothesis": "structuring",
  "dominant_confidence": 0.82,
  "contradictions_found": [],
  "open_question": "does behaviour history support or undercut structuring?",
  "active_investigation_stage": "customer_behaviour"
}
```

---

### 7.5 Evidence Graph

**Purpose**
The Evidence Graph is the central reasoning structure of TRIBUNAL. It organizes all Investigation Cards and their relationships into a directed graph that the Tribunal traverses to reach a verdict.

**Responsibilities**
- Translate each Investigation Card into a graph node with full provenance metadata.
- Derive edges directly from each card's declared `supports` and `counter_hypothesis` fields — relationships are translated from the evidence, not inferred.
- Assign edge weights encoding support strength and contradiction strength.
- Maintain the graph in-memory for traversal by the Tribunal.

**Inputs**
- All Investigation Cards emitted during the investigation.
- Contradiction edges added by the Defense Agent.

**Outputs**
- A directed, weighted graph of evidence relationships.

**Edge Schema**
```json
{
  "source": "card_001",
  "target": "card_004",
  "relation": "contradicts",
  "weight": 0.71,
  "reason": "card_004 shows consistent payroll-day timing inconsistent with structuring's irregular deposit pattern"
}
```

---

### 7.6 Defense Agent

**Purpose**
The Defense Agent introduces adversarial rigour into the investigation. It examines the dominant hypothesis and argues the strongest legitimate counter-explanation — ensuring that conclusions survive challenge before reaching the Tribunal.

**Responsibilities**
- Read the Case File's current dominant hypothesis and supporting evidence.
- Construct the strongest plausible innocent explanation (e.g., payroll timing, seasonal business patterns, known vendor relationships).
- Evaluate whether the counter-explanation holds against the available evidence.
- If the counter-explanation is plausible, add a contradiction edge to the Evidence Graph with weight and reason.
- If the counter-explanation does not survive scrutiny, leave the graph unchanged.

**Inputs**
- Case File (dominant hypothesis and supporting evidence).
- Evidence Graph (current state).

**Outputs**
- Zero or one contradiction edges added to the Evidence Graph.

---

### 7.7 Tribunal (Consensus Engine)

**Purpose**
The Tribunal is the decision-making body. It reasons over the Evidence Graph — not over raw transactions — to identify the strongest explainable hypothesis and produce a final recommendation.

**Responsibilities**
- Traverse the Evidence Graph, computing net support for each hypothesis chain (support weight minus contradiction weight).
- Identify the winning hypothesis: the chain with the highest net support that survives counter-evidence.
- Identify the runner-up hypothesis and the specific evidence that tipped the decision.
- Resolve conflicts where contradiction weight outweighs support.
- Map final confidence to an escalation tier: Low / Medium / High risk.

**Inputs**
- Complete Evidence Graph.
- Case File (for context).

**Outputs**
- Winning hypothesis with confidence and supporting evidence chain.
- Runner-up hypothesis with reason for rejection.
- Risk classification and escalation recommendation.

---

### 7.8 Investigation Report Generator

**Purpose**
The Report Generator transforms the Tribunal's structured output into a human-readable investigation report — the artefact that a compliance analyst, auditor, or regulator would review.

**Responsibilities**
- Recap the original query and investigation parameters.
- List the experts invoked and explain why each was selected (or skipped).
- Present the winning evidence chain with full provenance.
- Present the runner-up hypothesis and explain why it was rejected.
- Surface missing-evidence caveats — data that was unavailable but would have strengthened or weakened the conclusion.
- Deliver a clear final recommendation: **Monitor**, **Review**, or **Report**.

**Inputs**
- Tribunal output (winning hypothesis, runner-up, confidence, evidence chains).
- Case File (investigation context).
- Original user query.

**Outputs**
- Structured investigation report.

**Report Structure**
```
Investigation Summary
Query: "Find structuring in the last 30 days for customer 541"
Domains invoked: Financial Pattern Expert, Customer Behaviour Expert
                 (Network skipped — query did not require it)

Winning Hypothesis: Structuring
Confidence: 86%
Supporting Evidence Chain:
  card_001 (12 sub-threshold deposits) → card_003 (velocity spike, 430% daily volume increase)

Runner-up Hypothesis: Payroll pattern (card_004) — 42% confidence
Rejected because: deposit timing inconsistent with historical payroll cycle

Missing Evidence: merchant category unavailable — would help confirm/reject
                  cash-intensive-business explanation

Recommendation: Review
```

---

## 8. Adaptive Agentic Behaviour

### Why Static Pipelines Fail

A system that runs the same sequence of operations for every query is a pipeline, not an agent. AML investigations are inherently varied — a broad scan across all high-risk customers demands different analytical tools and expert combinations than a targeted investigation of a single entity's recent transactions.

TRIBUNAL's Planner is the system's agentic core. It does not follow a fixed script. It analyses the query, understands the intent, and constructs a tailored execution plan.

### Query-Driven Expert Selection

The Planner evaluates each incoming query and makes active decisions about what to investigate and how.

**Example 1 — Targeted Entity Investigation**

> *"Find structuring in the last 30 days for customer 541"*

Planner extracts: `{intent: pattern_detection, target_pattern: structuring, customer_id: 541, date_range: last_30_days}`

Execution plan:
- Skip exploratory data analysis — single entity, specific pattern.
- Invoke Financial Pattern Expert — directly relevant to structuring detection.
- Invoke Customer Behaviour Expert — validate against customer baseline.
- Skip Network Intelligence Expert — query does not require counterparty analysis.

**Example 2 — Broad Exploratory Scan**

> *"Show me unusual activity across high-risk accounts this quarter"*

Planner extracts: `{intent: broad_scan, target_pattern: anomaly, filters: {risk_level: high, date_range: current_quarter}}`

Execution plan:
- Run exploratory data analysis — broad scope requires profiling before expert invocation.
- Invoke Financial Pattern Expert — scan for threshold-adjacent patterns across multiple accounts.
- Invoke Customer Behaviour Expert — identify behavioural deviations from baselines.
- Potentially invoke Network Intelligence Expert — broad scans may surface counterparty patterns.

### Adaptive Re-Investigation

After the Defense Agent challenges the dominant hypothesis, the system evaluates whether the remaining confidence justifies a final recommendation. If confidence falls below a defined threshold, the system invokes exactly one additional expert from a fixed priority list to gather further evidence — then stops, regardless of the outcome.

This is a bounded decision, not an open-ended loop. The system makes one adaptive choice and proceeds to the Tribunal. This design prevents runaway investigation cycles while preserving the ability to gather critical missing evidence when the initial investigation is inconclusive.

---

## 9. Explainability Strategy

Explainability is not a feature of TRIBUNAL — it is an architectural property. The system does not generate explanations after reaching a conclusion. The conclusion *is* the explanation, because it is assembled from traceable, structured components at every stage.

### The Explainability Chain

```
Investigation Cards
        ↓
  Each card carries: hypothesis, evidence, confidence,
  counter-hypothesis, missing data, provenance metadata
        ↓
Evidence Graph
        ↓
  Cards become nodes. Relationships become weighted edges.
  The graph preserves all support and contradiction semantics.
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
  Monitor / Review / Report — grounded in evidence,
  not derived from an opaque score.
```

### Why This Matters

Traditional AML systems produce an alert. An analyst must then reconstruct *why* the alert fired — often from scratch.

Single-model AI approaches produce a score and a natural-language explanation. But the explanation is generated *after* the score — it is a rationalization, not a derivation.

TRIBUNAL's explanation *is* the derivation. The report does not describe what the system concluded — it shows how the system concluded it. Every hypothesis traces to the expert that proposed it. Every piece of evidence traces to the transactions that produced it. Every rejection traces to the contradiction that defeated it.

This is explainability by construction — and it is TRIBUNAL's strongest differentiator.

### Investigation Card Provenance

Every Investigation Card carries complete provenance metadata:

```json
{
  "card_id": "card_001",
  "source_expert": "financial_pattern",
  "derived_from_transactions": ["txn_1042", "txn_1043", "txn_1050"],
  "generated_at": "2026-07-24T15:22:10",
  "hypothesis": "structuring",
  "confidence": 0.82,
  "evidence": "12 deposits of $9,700–$9,900 over 4 days, all below $10,000 reporting threshold",
  "counter_hypothesis": "cash_intensive_business",
  "missing_data": "merchant_category",
  "supports": ["card_003"]
}
```

Each field maps directly to a graph element:
- `hypothesis` + `confidence` + `evidence` → the **node**.
- `supports` → an outgoing **support edge**.
- `counter_hypothesis` → a candidate **contradiction edge** the Defense Agent can strengthen.
- `missing_data` → a **caveat** surfaced directly in the final report.

---

## 10. Architecture Scope

TRIBUNAL is intentionally scoped. The full architectural vision defines a comprehensive investigation framework. The current implementation delivers a complete, end-to-end pipeline that demonstrates every core concept — with clearly delineated boundaries between what is built and what is designed for future expansion.

### Implemented

| Component | Status | Notes |
|---|---|---|
| Planner (Intent & Execution Planning) | ✅ Built | Query-aware expert selection with visible branching |
| Financial Pattern Expert | ✅ Built | Structuring, velocity, threshold-adjacent detection |
| Customer Behaviour Expert | ✅ Built | Historical deviation, case-file-aware investigation |
| Evidence Graph (NetworkX) | ✅ Built | In-memory directed graph with weighted edges |
| Defense Agent | ✅ Built | Single targeted pass against dominant hypothesis |
| Tribunal (Consensus Engine) | ✅ Built | Graph traversal, winner/runner-up identification |
| Investigation Report Generator | ✅ Built | Full structured output with evidence chain |
| Adaptive Re-investigation Cycle | ✅ Built | Bounded single-shot, not an open loop |

### Architected for Future Work

| Component | Design Status | Rationale |
|---|---|---|
| Network Intelligence Expert | Architected | Counterparty fan-out and money-flow tracing |
| Regulatory Rule Expert | Architected | Jurisdiction-specific rule matching |
| Geographic / Temporal Experts | Architected | Cross-border and time-series pattern analysis |
| Multi-round Adversarial Debate | Architected | Prosecutor and Defense in structured exchange |
| Continuous Investigation Memory | Architected | Cross-query learning for repeat entities |
| Confidence-Budget Planner | Architected | Expected-gain scoring for expert invocation |
| Graph Database Backend | Architected | Persistent evidence storage for large-scale deployment |
| Domain Generalization | Architected | Extension to fraud, insider trading, insurance claims |

The boundary between implemented and architected is a deliberate engineering decision. The current system demonstrates every architectural principle end-to-end. Future work extends coverage and scale — it does not change the fundamental design.

---

## 11. Technical Architecture

### Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| Language | Python | Unified ecosystem for data processing, graph operations, ML, and LLM integration |
| Graph Engine | NetworkX | In-memory directed graph — zero infrastructure overhead, sufficient for investigation-scale graphs (~20 nodes) |
| Statistical / ML | scikit-learn, NumPy | Isolation Forest for outlier detection, z-score computation, well-established with minimal tuning |
| Data Processing | pandas | Transaction data manipulation, filtering, aggregation |
| LLM Integration | Single provider, single wrapper | Defense Agent reasoning and Report phrasing — no multi-provider abstraction |
| Demo Interface | Streamlit | Interactive chat-style interface for live investigation demonstrations |

### Project Structure

```
TRIBUNAL/
│
├── app.py                          # Streamlit application entry point
│
├── planner/
│   ├── intent_parser.py            # Query → structured parameters
│   └── execution_planner.py        # Parameters → expert sequence + configuration
│
├── experts/
│   ├── base_expert.py              # Abstract expert interface
│   ├── financial_expert.py         # Financial Pattern Expert
│   └── behaviour_expert.py         # Customer Behaviour Expert
│
├── investigation/
│   ├── case_file.py                # Shared investigation state
│   ├── investigation_card.py       # Investigation Card schema and factory
│   └── evidence_graph.py           # Evidence Graph construction and operations
│
├── adversarial/
│   └── defense_agent.py            # Adversarial hypothesis challenge
│
├── tribunal/
│   ├── consensus_engine.py         # Graph reasoning and verdict computation
│   └── report_generator.py         # Structured investigation report output
│
├── tools/
│   ├── eda_tool.py                 # Exploratory data analysis (broad queries)
│   ├── feature_engineering.py      # Rolling sums, velocity, deviation metrics
│   └── anomaly_detection.py        # Statistical outlier detection
│
├── data/
│   └── ...                         # Transaction datasets
│
├── config/
│   └── thresholds.py               # Configurable investigation parameters
│
└── README.md
```

### Internal Module Responsibilities

| Module | Hackathon Requirement Mapping | Description |
|---|---|---|
| `tools/eda_tool.py` | EDA Tool | Lightweight profiling module — invoked for broad/exploratory queries, skipped for single-entity investigations |
| `tools/feature_engineering.py` | Feature Engineering Tool | Rolling sums, transaction velocity, amount deviation, frequency metrics — shared across experts |
| `experts/financial_expert.py` + `tools/anomaly_detection.py` | Anomaly Detection Tool | Rule-based pattern detection combined with statistical outlier analysis (z-score, Isolation Forest) |
| `tribunal/consensus_engine.py` | Risk Classification Tool | Tribunal confidence → Low / Medium / High risk mapping and escalation recommendation |
| `tribunal/report_generator.py` | Explanation Component | Full investigation report tied to original query and winning evidence chain |

---

## 12. Conclusion

TRIBUNAL reimagines AML compliance as a structured investigation rather than a classification task.

Where traditional systems produce alerts, TRIBUNAL produces investigations. Where single-model AI approaches produce scores, TRIBUNAL produces evidence chains. Where existing tools leave analysts to reconstruct reasoning from scratch, TRIBUNAL delivers a complete investigative narrative — from query to evidence to hypothesis to challenge to verdict.

The system's strength lies not in any single component, but in the architecture itself: specialized experts contribute structured evidence, an adversarial process challenges the dominant theory, and a tribunal reasons over the accumulated body of evidence to reach an explainable conclusion.

Every recommendation is traceable. Every hypothesis is contestable. Every verdict is auditable.

TRIBUNAL is not another fraud detection model.

It is an **explainable AI investigation framework**.

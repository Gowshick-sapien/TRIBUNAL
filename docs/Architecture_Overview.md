# TRIBUNAL — System Architecture Overview

This document presents the high-level architecture, module breakdown, and data pipelines of the **TRIBUNAL** multi-expert legal/investigative framework.

---

## System Architecture Diagram

```
                 +---------------------------------------+
                 |       React / Vite Dashboard          |
                 |     (Interactive Evidence Graph)      |
                 +-------------------+-------------------+
                                     |
                                 REST API
                                     |
                 +-------------------+-------------------+
                 |           FastAPI Gateway             |
                 +-------------------+-------------------+
                                     |
              +----------------------+----------------------+
              |                      |                      |
     +--------+-------+     +--------+-------+     +--------+-------+
     | Financial      |     | Behavioral     |     | Defense        |
     | Expert Engine  |     | Expert Engine  |     | Agent Engine   |
     +--------+-------+     +--------+-------+     +--------+-------+
              |                      |                      |
              +----------------------+----------------------+
                                     |
                 +-------------------+-------------------+
                 |    Dynamic Evidence Graph Builder     |
                 +-------------------+-------------------+
                                     |
                 +-------------------+-------------------+
                 |  Consensus Engine & Calibrated    |
                 |         Verdict Generator             |
                 +-------------------+-------------------+
                                     |
                 +-------------------+-------------------+
                 |     Audit Storage & Report Engine     |
                 |        (HTML / MD / JSON / SQLite)    |
                 +---------------------------------------+
```

---

## Core Architectural Components

### 1. Multi-Expert Panel (`/tribunal/experts`)
- **Financial Expert**: Detects transaction anomalies including structuring ($10k threshold evasion), high-velocity transfers, large volume spikes, and counterparty clustering.
- **Behavioral Expert**: Evaluates historical account baselines, account dormancy reactivation, drift indicators, and behavioral frequency anomalies.
- **Defense Agent**: Constructs alternative hypotheses, checks for legitimate business explanations (e.g. standard payroll, supplier invoices), and challenges false positive assumptions.

### 2. Graph & Provenance Engine (`/tribunal/investigation`)
- Constructs directed multi-relational graphs combining accounts, transactions, flags, and expert hypotheses.
- Tracks exact provenance chain for every evidence node and edge.

### 3. Consensus Engine (`/tribunal/consensus`)
- Resolves contradictions between opposing expert claims.
- Applies calibrated confidence weighting to determine final verdict (Guilty / Suspicious / Innocent).

### 4. Report & Audit Engine (`/tribunal/report`)
- Exports reproducible investigation reports in Markdown, HTML, and JSON schemas.
- Persists audit trails in SQLite and structured JSON file storage (`/storage`).

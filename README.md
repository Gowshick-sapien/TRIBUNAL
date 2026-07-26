# TRIBUNAL — Autonomous Multi-Expert Legal & Financial Investigative AI Framework

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Hackathon Master Submission Package**  
> **TRIBUNAL** is an autonomous, multi-expert AI investigation framework designed to analyze complex financial transaction networks, detect structuring and money laundering anomalies, construct dynamic evidence graphs, and generate calibrated, defensible verdicts with adversarial defense reviews.

---

## Executive Summary & Problem Statement

Financial crime investigations, Anti-Money Laundering (AML) sweeps, and forensic transaction audits suffer from three critical bottlenecks:
1. **Siloed Analysis**: Financial transaction volume spikes, counterparty network shifts, and account dormancy drift are typically analyzed by separate tools or isolated manual teams.
2. **High False-Positive Rates**: Automated rules engines flag legitimate commercial operations (e.g. standard monthly payrolls or seasonal vendor invoices) as high-risk anomalies, overwhelming compliance teams.
3. **Opaque Black-Box Decisioning**: Traditional ML models produce monolithic risk scores without transparent provenance, evidence graphs, or adversarial cross-examination.

### The TRIBUNAL Solution
TRIBUNAL addresses these challenges by orchestrating a **Panel of Specialized AI Experts**:
- **Financial Expert**: Identifies transfer anomalies, structuring ($10,000 evasion thresholds), rapid velocity spikes, and currency swaps.
- **Behavioral Expert**: Evaluates account dormancy reactivation, historical baseline drift, frequency spikes, and peer network deviations.
- **Defense Agent**: Evaluates alternative hypotheses and legitimate commercial explanations (payroll, vendor invoices) to actively rebut false positives.
- **Consensus & Verdict Engine**: Synthesizes conflicting expert claims into a calibrated, explainable verdict backed by a dynamic evidence graph.

---

## Key Features & Innovations

- **Multi-Expert DAG Pipeline**: Asynchronous, directed execution pipeline coordinating domain experts.
- **Adversarial Defense Review**: Built-in Defense Agent that challenges prosecution hypotheses and flags false positives.
- **Dynamic Evidence Graph**: Interactive node-link graph (React Flow) rendering accounts, transactions, anomaly findings, and PageRank metrics.
- **Calibrated Confidence Scoring**: Mathematical evidence weighing and contradiction resolution returning transparent verdict confidence scores.
- **Multi-Format Export Engine**: One-click export of executive audit reports into interactive **HTML**, **Markdown**, and **JSON** formats.

---

## System Architecture & Data Flow

```
                                +-----------------------------------+
                                |    React / Vite Web Dashboard     |
                                |   (Interactive Evidence Graph)    |
                                +-----------------+-----------------+
                                                  |
                                              REST API
                                                  |
                                +-----------------+-----------------+
                                |         FastAPI Gateway           |
                                +-----------------+-----------------+
                                                  |
                         +------------------------+------------------------+
                         |                        |                        |
                +--------+-------+       +--------+-------+       +--------+-------+
                | Financial      |       | Behavioral     |       | Defense        |
                | Expert Engine  |       | Expert Engine  |       | Agent Engine   |
                +--------+-------+       +--------+-------+       +--------+-------+
                         |                        |                        |
                         +------------------------+------------------------+
                                                  |
                                +-----------------+-----------------+
                                | Dynamic Evidence Graph Builder    |
                                +-----------------+-----------------+
                                                  |
                                +-----------------+-----------------+
                                |  Consensus & Verdict Engine       |
                                +-----------------+-----------------+
                                                  |
                                +-----------------+-----------------+
                                | Audit Persistence & Report Engine |
                                |   (SQLite / File Store / JSON)    |
                                +-----------------------------------+
```

---

## Technology Stack

| Component | Technologies Used |
| :--- | :--- |
| **Backend Core** | Python 3.10+, FastAPI, Pydantic v2, Uvicorn |
| **Graph & Data Processing** | NetworkX, Pandas, NumPy |
| **LLM Reasoning Engine** | Ollama, Qwen 2.5 Coder (7B), Custom Mock Client Fallback |
| **Frontend Dashboard** | React 19, TypeScript, Vite, React Flow (@xyflow/react), TailwindCSS |
| **Testing & Quality** | Pytest, Pytest-Asyncio, Oxlint |

---

## Quick Start (Running in 2 Minutes)

### Prerequisites
- Python 3.10+ installed
- Node.js 18+ and `npm` installed

### 1. Backend Setup
```bash
# Navigate to project root
cd TRIBUNAL

# Create and activate Python virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate    # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Launch FastAPI Server (Port 8000)
uvicorn api.app:app --reload --port 8000
```

### 2. Frontend Dashboard Setup
```bash
# In a new terminal window:
cd dashboard
npm install
npm run dev
```

Open your browser to `http://localhost:5173`.

---

## Sample Investigative Queries

Try pasting these queries into the TRIBUNAL Dashboard search header:

1. **Structuring & Evasion**:
   > *"Investigate account ACC-90812 for structured transfers below the $10,000 threshold over the last 24 hours."*
2. **Account Dormancy Reactivation**:
   > *"Show behavioral drift and dormancy reactivation for account ACC-10492."*
3. **High-Risk Shell Counterparty Sweep**:
   > *"Sweep target accounts connected to shell entity ACC-44910 and build evidence graph."*

For 15+ curated test scenarios, see the complete [Sample Queries Guide](file:///D:/TRIBUNAL_RELEASE/docs/Sample_Queries.md).

---

## Repository Directory Structure

```
D:\TRIBUNAL_RELEASE
├── api/                       (FastAPI REST routes, schemas, and dependencies)
│   ├── routes/                (Endpoint handlers: /investigate, /reports, /search)
│   ├── schemas/               (Pydantic API request & response schemas)
│   └── services/              (Business logic & service bridges)
├── assets/                    (Media assets for jury evaluation)
│   ├── screenshots/           (Dashboard & evidence graph screenshots)
│   ├── ppt/                   (Pitch deck & slides)
│   ├── video/                 (Demonstration video)
│   ├── logo/                  (Project branding)
│   └── diagrams/              (Architecture diagrams)
├── dashboard/                 (React / Vite web dashboard application)
│   ├── src/components/        (React Flow graphs, cards, & report viewers)
│   └── src/pages/             (Workspace, Explorer, & History pages)
├── docs/                      (Comprehensive Jury & Technical Documentation)
│   ├── Architecture_Overview.md (System architecture specification)
│   ├── Installation_Guide.md  (Step-by-step installation instructions)
│   ├── Jury_Guide.md          (Complete Jury evaluation walkthrough)
│   ├── Quick_Start.md         (1-page quick start cheatsheet)
│   └── Sample_Queries.md      (15+ curated test queries)
├── scripts/                   (Demo execution launcher scripts)
├── storage/                   (Audit databases & JSON report stores)
├── submission_checklist.md    (Hackathon progress & deliverables checklist)
├── tribunal/                  (Core multi-expert reasoning engine)
│   ├── experts/               (Financial, Behavioral, & Defense expert engines)
│   ├── consensus/             (Contradiction resolver & calibrated verdict engine)
│   ├── investigation/         (Evidence graph builder & provenance manager)
│   ├── planner/               (Query parser & execution planner)
│   ├── report/                (HTML, Markdown, & JSON report generators)
│   └── tests/                 (142 automated unit & integration tests)
├── .env.example               (Environment configuration template)
├── requirements.txt           (Minimal Python dependencies)
└── README.md                  (Master Repository README)
```

---

## Complete Documentation Index

- [Jury Evaluation Guide](file:///D:/TRIBUNAL_RELEASE/docs/Jury_Guide.md)
- [Detailed Installation Guide](file:///D:/TRIBUNAL_RELEASE/docs/Installation_Guide.md)
- [1-Page Quick Start Guide](file:///D:/TRIBUNAL_RELEASE/docs/Quick_Start.md)
- [Architecture Overview](file:///D:/TRIBUNAL_RELEASE/docs/Architecture_Overview.md)
- [Curated Sample Queries](file:///D:/TRIBUNAL_RELEASE/docs/Sample_Queries.md)
- [Submission Checklist](file:///D:/TRIBUNAL_RELEASE/submission_checklist.md)

---

## Automated Testing & Quality

Run the complete 142-test automated suite:

```bash
pytest tribunal/tests/unit tribunal/tests/integration
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

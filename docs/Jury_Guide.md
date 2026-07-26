# TRIBUNAL — Hackathon Jury Evaluation Guide

Welcome to the **TRIBUNAL** Jury Evaluation Guide. This document provides hackathon judges, technical reviewers, and compliance auditors with a step-by-step evaluation protocol for testing TRIBUNAL's multi-expert legal/investigative AI framework.

---

## 🏛️ Executive Walkthrough Flow

Follow this 6-step evaluation protocol to test the complete multi-expert reasoning engine:

```
[Step 1] Launch Dashboard
        ↓
[Step 2] Select Pre-Loaded Scenario / Query
        ↓
[Step 3] Inspect Multi-Expert Panel Findings
        ↓
[Step 4] Navigate Dynamic Evidence Graph
        ↓
[Step 5] Review Defense Agent Rebuttal & Consensus Verdict
        ↓
[Step 6] Audit & Download Full Reports (HTML / MD / JSON)
```

---

## 🔍 Detailed Jury Evaluation Protocol

### Step 1: Launch System & Open Dashboard
- Follow the [Quick Start Guide](file:///D:/TRIBUNAL_RELEASE/docs/Quick_Start.md) or launch backend (`http://localhost:8000`) and frontend (`http://localhost:5173`).
- Open `http://localhost:5173` in Google Chrome or Microsoft Edge.
- Verify the header status indicator reads `API Connected`.

### Step 2: Choose Dataset & Select Scenario
In the top search bar, click on **Sample Queries** dropdown to select a pre-configured evaluation scenario:

1. **Scenario A — Account Structuring Sweep (`ACC-90812`)**:
   - Query: *"Investigate account ACC-90812 for structured transfers below the $10,000 threshold."*
2. **Scenario B — Account Dormancy Reactivation & Baseline Drift (`ACC-10492`)**:
   - Query: *"Show behavioral drift and dormancy reactivation for account ACC-10492."*
3. **Scenario C — High-Risk Shell Counterparty Sweep (`ACC-44910`)**:
   - Query: *"Sweep target accounts connected to shell entity ACC-44910 and build evidence graph."*

Click **Investigate**.

---

### Step 3: Inspect Multi-Expert Panel Findings

As the investigation finishes, observe the three domain expert cards in the main workspace:

#### 1. Financial Expert Card 💳
- **What to look for**: Structuring detection metrics, total transfer volume, and transaction velocity.
- **Verification Point**: Verify that transactions hovering between $9,000 and $9,900 within short time windows are flagged with `Structuring Suspicion = HIGH`.

#### 2. Behavioral Expert Card 📈
- **What to look for**: Historical account baseline comparisons, account dormancy reactivation alerts, and payment format changes.
- **Verification Point**: Check the `Dormancy Reactivation` alert for accounts that were inactive for >180 days and suddenly initiated high-volume transfers.

#### 3. Defense Agent Rebuttal Card 🛡️
- **What to look for**: Adversarial evaluation of alternative hypotheses.
- **Verification Point**: The Defense Agent cross-examines findings against known business logic (checking for registered payroll patterns or recurring vendor contracts) to challenge false positive assumptions.

---

### Step 4: Navigate Interactive Evidence Graph 🕸️
- Locate the central **Evidence Graph** component powered by React Flow.
- **Node Inspection**: Click on any account node (`ACC-90812`) or transaction edge to open the **Node Metadata Drawer**.
- **Graph Metrics**: Observe calculated PageRank score, degree centrality, and evidence weighting.
- **Exporting**: Click **Export Graph PNG** to save a high-resolution screenshot of the evidence topology.

---

### Step 5: Audit Tribunal Consensus & Final Verdict ⚖️
- Examine the top **Tribunal Verdict Banner**.
- **Verdict Categories**:
  - `GUILTY / HIGH RISK` (Multi-expert consensus with strong un-rebutted evidence)
  - `SUSPICIOUS / REVIEW` (Moderate evidence or partial defense challenge)
  - `INNOCENT / CLEARED` (Defense Agent successfully establishes legitimate business exception)
- **Confidence Calibration**: Review the transparent confidence score (e.g. `87.5% Confidence`) calculated via weighted mathematical evidence integration.

---

### Step 6: Download Audit Reports 📥
- Navigate to the **Export & Audit** section.
- Click on each export format button to test multi-format rendering:
  - **Download HTML Report**: Full standalone, styled HTML report with inline charts.
  - **Download Markdown Report**: GFM-formatted markdown summary.
  - **Download JSON Schema**: Structured machine-readable JSON object containing complete case file provenance.

---

## 🎯 Verification Matrix & Expected Results

| Scenario | Target Entity | Key Expert Trigger | Defense Outcome | Expected Final Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **SCN-01** | `ACC-90812` | $9.5k x 3 within 24h | No payroll contract found | **SUSPICIOUS (85%+)** |
| **SCN-02** | `ACC-10492` | 210-day dormancy reactivation | Frequency spike confirmed | **HIGH RISK (90%+)** |
| **SCN-03** | `ACC-77102` | High monthly payout volume | Verified corporate payroll | **CLEARED BY DEFENSE** |

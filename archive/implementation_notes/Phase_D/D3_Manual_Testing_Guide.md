# Phase D.3 — Investigation Dashboard Manual Testing Guide

This guide provides step-by-step instructions for launching and testing the **Phase D.3 Investigation Dashboard & User Experience Platform**.

---

## 1. Launching the Full Stack

To test the complete end-to-end platform, launch both the FastAPI REST API backend and the React Vite dashboard.

### Terminal 1: Launch FastAPI Backend Server
```bash
# In project root: D:\TRIBUNAL
uvicorn api.app:app --host 127.0.0.1 --port 8000 --reload
```

### Terminal 2: Launch React Vite Dashboard
```bash
# Navigate to dashboard directory
cd dashboard

# Start Vite local development server
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your web browser.

---

## 2. Step-by-Step UI Workstation Manual Verification

### Step 2.1: Home Overview Page (`http://localhost:5173/`)
- Verify the brand mark, terminal version badge `v1.0.0`, and top navigation bar.
- Check the **Engine Status** badge in top-right (displays `HEALTHY` or `ONLINE` when backend is running).
- Review the 3 **Pre-Configured Demo Scenarios**:
  - *Structuring & Velocity Analysis*
  - *Dormancy & Baseline Drift*
  - *Rapid Wire Transfer Burst*
- Click **Run Scenario &rarr;** on any card. Confirm you are navigated to the **Workspace** page with the query pre-filled.

---

### Step 2.2: Investigation Execution Workspace (`http://localhost:5173/investigate`)
- Observe the **Natural Language Query Input** and **Dataset Selector**.
- Click **Run Investigation Engine**.
- Observe the **Live 6-Step Execution Timeline**:
  - Step 01: Planner Framework
  - Step 02: Financial Expert
  - Step 03: Behaviour Expert
  - Step 04: Evidence Graph
  - Step 05: Adversarial Defense
  - Step 06: Tribunal Consensus
- Once complete, inspect the **Verdict Card**:
  - **Verdict Badge**: `LIKELY_MALICIOUS`, `POSSIBLY_MALICIOUS`, `LIKELY_LEGITIMATE`, or `INCONCLUSIVE`.
  - **Risk Chip**: `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW`.
  - **Confidence Meter**: Percentage readout (e.g. `95%`).
  - **Executive Findings Summary**: Plain language reasoning summary.
  - **Actionable Recommendation**: Compliance advice.
- Click **Open Full Investigation Viewer &rarr;**.

---

### Step 2.3: Multi-Tab Investigation Viewer (`http://localhost:5173/investigation/{id}`)
- Test switching between the 5 interactive tabs:
  1. **Executive Summary**: Primary hypothesis, risk level, confidence gauge, and recommendations.
  2. **Evidence & Graph**: Graph node count, edge count, density metrics, and node topology table.
  3. **Defense Counter-Review**: Adversarial defense findings and rebuttal status.
  4. **Tribunal Consensus**: Primary winning hypothesis, runner-up hypothesis, confidence gap, and step-by-step deliberation trace.
  5. **Full 10-Section Report**: Full Markdown generated report.
- Click **Export Markdown** button to download the `.md` report file locally.

---

### Step 2.4: Investigation History Browser (`http://localhost:5173/history`)
- Observe the table listing all historical investigations stored in the D.2 SQLite database.
- Use the **Search input** to filter by Case ID (e.g. `inv_`), query keywords, or intent.
- Use the **Risk Filter dropdown** (`ALL RISKS`, `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`).
- Click the **External Link icon** on any row to open its viewer page.
- Click the **Trash icon** to delete an investigation record from persistent storage.

---

### Step 2.5: System Health & Capabilities (`http://localhost:5173/system`)
- Verify the **REST API Status**, **Planner Ready**, **Tribunal Engine**, and **Uptime** status cards.
- Inspect the **Supported Domain Experts** (`financial`, `behaviour`).
- Inspect the **10 Supported AML Pattern Detectors** (`structuring`, `velocity`, `large_transfer`, `frequency`, `behaviour_drift`, `counterparty_behaviour`, `currency_change`, `dormancy`, `payment_pattern`, `spending_pattern`).

---

### Step 2.6: Settings (`http://localhost:5173/settings`)
- Change the **Backend REST API Base URL** (defaults to `http://127.0.0.1:8000/api/v1`).
- Click **Save Preferences**.
- Click **Reset to Defaults** to restore the default configuration.

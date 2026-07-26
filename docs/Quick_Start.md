# TRIBUNAL — 1-Page Quick Start Guide

Get **TRIBUNAL** up and running in under 2 minutes.

---

## Execution Flow (60-Second Overview)

```
Extract / Clone ZIP
       ↓
Install Python Dependencies (pip install -r requirements.txt)
       ↓
Install Dashboard Packages (cd dashboard && npm install)
       ↓
Run Backend (uvicorn api.app:app --port 8000)
       ↓
Run Frontend (npm run dev in /dashboard)
       ↓
Open http://localhost:5173
       ↓
Paste Query & Observe Multi-Expert Pipeline & Evidence Graph
```

---

## 1-Command Automated Launch (Windows PowerShell)

Run the automated launcher from the project root:

```powershell
.\scripts\run_demo.ps1
```

---

## Manual Commands Cheatsheet

### Terminal 1: Backend API
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn api.app:app --reload --port 8000
```

### Terminal 2: Frontend Dashboard
```bash
cd dashboard
npm install
npm run dev
```

---

## Quick Verification Query

Once `http://localhost:5173` opens in your browser, select **"ACC-90812 — Structuring Sweep"** from the top query selector and click **Investigate**.

Observe:
1. **Financial Expert Card**: Flags 3 transactions below $10,000 threshold within 24h.
2. **Behavioral Expert Card**: Displays rapid velocity score.
3. **Defense Agent Card**: Verifies absence of invoice credentials.
4. **Evidence Graph**: Renders interactive node-edge DAG.
5. **Verdict Banner**: `SUSPICIOUS / HIGH CONFIDENCE`.

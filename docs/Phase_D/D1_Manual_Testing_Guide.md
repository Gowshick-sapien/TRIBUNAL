# Phase D.1 — Manual Testing & API Verification Guide

This guide provides step-by-step instructions for launching the TRIBUNAL REST API server and executing manual testing across **Windows PowerShell**, **Windows Command Prompt (cmd.exe)**, **Linux/macOS Bash**, and **Python**.

---

## 1. Launching the API Server

Start the FastAPI application using Uvicorn from the project root directory:

```bash
uvicorn api.app:app --host 127.0.0.1 --port 8000 --reload
```

Server output confirms startup:
```text
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 2. Interactive Swagger UI & ReDoc (Easiest Method)

FastAPI automatically generates interactive OpenAPI documentation. You can test all endpoints directly in your browser:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **OpenAPI Spec**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

> **To test via Swagger UI**: Click on any endpoint (e.g. `POST /api/v1/investigate`), click **Try it out**, edit the JSON payload, and click **Execute**.

---

## 3. Manual Testing Commands

> [!IMPORTANT]
> **Windows Shell Note**: In Windows `cmd.exe` or PowerShell, standard `curl` with single quotes `'{"key":"value"}'` fails because the shell does not strip single quotes around JSON payloads, causing `422 Unprocessable Entity (JSON decode error)`. Use **PowerShell `Invoke-RestMethod`**, **escaped double quotes `\"`**, or **Python**.

### Step 3.1: Check Health & Metadata

**Health Check**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/health"
```

**Platform Metadata**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/metadata"
```

---

### Step 3.2: Trigger Full Investigation (`POST /api/v1/investigate`)

#### Option A: Windows PowerShell (`Invoke-RestMethod` - Recommended for Windows)
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/investigate" -Method Post -ContentType "application/json" -Body '{"query":"Is customer ACC_8000A94C0 engaged in structuring and velocity anomalies?","dataset":"default"}'
```

#### Option B: Windows CMD / PowerShell (`curl.exe` with Escaped Quotes)
```cmd
curl.exe -X POST "http://127.0.0.1:8000/api/v1/investigate" -H "Content-Type: application/json" -d "{\"query\":\"Is customer ACC_8000A94C0 engaged in structuring and velocity anomalies?\",\"dataset\":\"default\"}"
```

#### Option C: Linux / macOS Bash (`curl`)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/investigate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Is customer ACC_8000A94C0 engaged in structuring and velocity anomalies?",
    "dataset": "default"
  }'
```

*Sample Successful Response (200 OK)*:
```json
{
  "investigation_id": "inv_9a4b8c1d2e3f",
  "query": "Is customer ACC_8000A94C0 engaged in structuring and velocity anomalies?",
  "risk_level": "HIGH",
  "confidence": 0.95,
  "verdict": "LIKELY_MALICIOUS",
  "winning_hypothesis": "Structuring & Velocity Pattern Detected",
  "recommendation": "Verdict: LIKELY_MALICIOUS for primary hypothesis ...",
  "summary": "Investigation concluded verdict 'LIKELY_MALICIOUS' with confidence 0.95.",
  "report_url": "/api/v1/report/inv_9a4b8c1d2e3f",
  "graph_url": "/api/v1/graph/inv_9a4b8c1d2e3f",
  "verdict_url": "/api/v1/verdict/inv_9a4b8c1d2e3f",
  "metrics": {
    "planner_ms": 12.5,
    "experts_ms": 45.2,
    "graph_ms": 15.1,
    "tribunal_ms": 8.4,
    "report_ms": 11.2,
    "total_ms": 92.4
  }
}
```

---

### Step 3.3: Retrieve Artifacts by Investigation ID

> [!IMPORTANT]
> **Use Your Generated `investigation_id`**: `inv_9a4b8c1d2e3f` shown below is a placeholder example ID.
> You must replace `inv_9a4b8c1d2e3f` with the **actual `investigation_id`** returned in the JSON response of your `POST /api/v1/investigate` request (e.g., `inv_eb2a0c928a99`).
> 
> *Note*: In Phase D.1, completed investigations are retained in memory. If Uvicorn restarts (e.g., via `--reload`), the in-memory store resets. Persistent database storage is introduced in Phase D.2.

**Fetch Report (JSON)**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/report/inv_9a4b8c1d2e3f"
```

**Fetch Report (Markdown format)**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/report/inv_9a4b8c1d2e3f" -H "Accept: text/markdown"
```

**Fetch Evidence Graph**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/graph/inv_9a4b8c1d2e3f"
```

**Fetch Tribunal Verdict**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/verdict/inv_9a4b8c1d2e3f"
```

---

### Step 3.4: Conversational Endpoint (`POST /api/v1/query`)

**PowerShell**:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/query" -Method Post -ContentType "application/json" -Body '{"query":"Is customer 541 suspicious?","dataset":"default"}'
```

**Bash / CMD**:
```cmd
curl.exe -X POST "http://127.0.0.1:8000/api/v1/query" -H "Content-Type: application/json" -d "{\"query\":\"Is customer 541 suspicious?\",\"dataset\":\"default\"}"
```

---

### Step 3.5: Error Handling Verification

**Invalid Short Query (400 Bad Request)**:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/investigate" -Method Post -ContentType "application/json" -Body '{"query":"a"}'
```
*Expected Status*: `400 Bad Request`

**Nonexistent Dataset (404 Not Found)**:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/investigate" -Method Post -ContentType "application/json" -Body '{"query":"Investigate suspicious transfer","dataset":"nonexistent_ref_123"}'
```
*Expected Status*: `404 Not Found`

**Nonexistent Investigation ID (404 Not Found)**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/report/inv_unknown_123"
```
*Expected Status*: `404 Not Found`

---

## 4. Python Client Verification Script (Cross-Platform)

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

# 1. Trigger Investigation
resp = requests.post(f"{BASE_URL}/investigate", json={
    "query": "Check account ACC_8000A94C0 for anomalous activity",
    "dataset": "default"
})
assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
data = resp.json()
inv_id = data["investigation_id"]
print(f"✅ Investigation started successfully: ID={inv_id}, Verdict={data['verdict']}")

# 2. Fetch Report
report_resp = requests.get(f"{BASE_URL}/report/{inv_id}")
print(f"✅ Report retrieved: {len(report_resp.json()['sections'])} sections")

# 3. Fetch Evidence Graph
graph_resp = requests.get(f"{BASE_URL}/graph/{inv_id}")
print(f"✅ Graph retrieved: {graph_resp.json()['statistics']['node_count']} nodes")

# 4. Fetch Verdict
verdict_resp = requests.get(f"{BASE_URL}/verdict/{inv_id}")
print(f"✅ Verdict retrieved: Primary Hypothesis='{verdict_resp.json()['winning_hypothesis']}'")
```

# Phase D.2 — Manual Testing & Storage Verification Guide

This guide provides step-by-step instructions for testing the **Phase D.2 Persistent Investigation Repository**, SQLite database storage, filesystem artifact persistence, application restart survival, and extended REST API endpoints.

---

## 1. Launching the API Server

Start the FastAPI application using Uvicorn from the project root directory:

```bash
uvicorn api.app:app --host 127.0.0.1 --port 8000 --reload
```

Upon startup, the server automatically initializes `storage/tribunal.db` and `storage/files/` subdirectories (`reports/`, `graphs/`, `cases/`, `audit/`).

---

## 2. Interactive Swagger UI & ReDoc

FastAPI exposes interactive OpenAPI documentation with all new D.2 endpoints:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 3. End-to-End Manual Testing Workflow

> [!NOTE]
> **Windows Shell Note**: In Windows `cmd.exe` or PowerShell, standard `curl` with single quotes `'{"key":"value"}'` fails because the shell does not strip single quotes around JSON payloads, causing `422 Unprocessable Entity (JSON decode error)`. Use **PowerShell `Invoke-RestMethod`**, **escaped double quotes `\"`**, or **Python**.

---

### Step 3.1: Trigger Investigation & Persist Artifacts

**PowerShell (`Invoke-RestMethod`)**:
```powershell
$resp = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/investigate" -Method Post -ContentType "application/json" -Body '{"query":"Check account ACC_8000A94C0 for structuring and velocity anomalies","dataset":"default"}'
$id = $resp.investigation_id
Write-Host "Created investigation ID: $id"
```

**CMD / PowerShell (`curl.exe`)**:
```cmd
curl.exe -X POST "http://127.0.0.1:8000/api/v1/investigate" -H "Content-Type: application/json" -d "{\"query\":\"Check account ACC_8000A94C0 for structuring and velocity anomalies\",\"dataset\":\"default\"}"
```

**Linux / macOS Bash (`curl`)**:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/investigate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Check account ACC_8000A94C0 for structuring and velocity anomalies",
    "dataset": "default"
  }'
```

*Response (200 OK)*:
```json
{
  "investigation_id": "inv_a1b2c3d4e5f6",
  "risk_level": "HIGH",
  "confidence": 0.95,
  "verdict": "LIKELY_MALICIOUS",
  "winning_hypothesis": "Structuring & Velocity Pattern Detected",
  "report_url": "/api/v1/report/inv_a1b2c3d4e5f6",
  "graph_url": "/api/v1/graph/inv_a1b2c3d4e5f6",
  "verdict_url": "/api/v1/verdict/inv_a1b2c3d4e5f6"
}
```

---

### Step 3.2: List Stored Investigations (`GET /api/v1/investigations`)

Fetch all persistent historical investigations stored in the database:

**PowerShell**:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/investigations?limit=10"
```

**Bash / CMD**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/investigations?limit=10"
```

*Response*:
```json
{
  "total": 1,
  "limit": 10,
  "offset": 0,
  "investigations": [
    {
      "id": "inv_a1b2c3d4e5f6",
      "query": "Check account ACC_8000A94C0 for structuring and velocity anomalies",
      "dataset": "default",
      "created_at": "2026-07-25T23:45:00Z",
      "planner_intent": "pattern_detection",
      "risk_level": "HIGH",
      "confidence": 0.95,
      "recommendation": "Verdict: LIKELY_MALICIOUS ...",
      "status": "COMPLETED",
      "duration_ms": 1250.4,
      "version": "1.0.0"
    }
  ]
}
```

---

### Step 3.3: Fetch Investigation Detail Metadata (`GET /api/v1/investigation/{id}`)

**PowerShell**:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/investigation/$id"
```

**Bash / CMD**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/investigation/inv_a1b2c3d4e5f6"
```

---

### Step 3.4: Verify Survival Across Server Restarts

1. **Stop the Uvicorn server** (`CTRL + C` in your terminal window running Uvicorn).
2. **Restart the Uvicorn server**:
   ```bash
   uvicorn api.app:app --host 127.0.0.1 --port 8000 --reload
   ```
3. **Fetch Report, Graph, & Verdict**:
   ```powershell
   Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/report/$id"
   Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/graph/$id"
   Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/verdict/$id"
   ```
   *Result*: Data returns successfully with `200 OK`, proving artifacts survived server restart!

---

### Step 3.5: Delete Persistent Investigation (`DELETE /api/v1/investigation/{id}`)

**PowerShell**:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/investigation/$id" -Method Delete
```

**Bash / CMD**:
```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/investigation/inv_a1b2c3d4e5f6"
```
*Expected Status*: `204 No Content`

**Verify Deletion**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/investigation/inv_a1b2c3d4e5f6"
```
*Expected Status*: `404 Not Found`

---

## 4. SQLite Database Direct Inspection

You can inspect the SQLite database tables directly using the `sqlite3` CLI tool:

```bash
sqlite3 storage/tribunal.db
```

### Useful SQL Queries:
```sql
-- View all stored investigation records
SELECT id, created_at, query, risk_level, confidence, status FROM investigations;

-- View stored report locations
SELECT * FROM reports;

-- View evidence graph statistics
SELECT * FROM graphs;

-- View consensus verdicts
SELECT * FROM verdicts;

-- View complete audit trail history
SELECT * FROM audit ORDER BY id ASC;
```

---

## 5. Filesystem Artifact Inspection

Verify persisted disk files in `storage/files/`:

- **Reports**: `storage/files/reports/inv_<id>.md` & `inv_<id>.json`
- **Evidence Graphs**: `storage/files/graphs/inv_<id>.json`
- **Case Files**: `storage/files/cases/inv_<id>.json`
- **Audit Logs**: `storage/files/audit/inv_<id>.json`

---

## 6. Python Automated Verification Script (Cross-Platform)

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

# 1. Create Investigation
res = requests.post(f"{BASE_URL}/investigate", json={
    "query": "Check account ACC_8000A94C0 for structuring",
    "dataset": "default"
})
assert res.status_code == 200
inv_id = res.json()["investigation_id"]
print(f"✅ Created investigation: {inv_id}")

# 2. List Investigations
list_res = requests.get(f"{BASE_URL}/investigations")
assert list_res.status_code == 200
print(f"✅ Total stored investigations: {list_res.json()['total']}")

# 3. Get Detail
detail_res = requests.get(f"{BASE_URL}/investigation/{inv_id}")
assert detail_res.status_code == 200
print(f"✅ Metadata detail fetched: Status={detail_res.json()['record']['status']}")

# 4. Fetch Report & Graph
assert requests.get(f"{BASE_URL}/report/{inv_id}").status_code == 200
assert requests.get(f"{BASE_URL}/graph/{inv_id}").status_code == 200
print("✅ Report & Graph retrievable from persistent storage")

# 5. Delete Investigation
del_res = requests.delete(f"{BASE_URL}/investigation/{inv_id}")
assert del_res.status_code == 204
print("✅ Deleted investigation successfully")

# 6. Confirm Deletion (404)
assert requests.get(f"{BASE_URL}/investigation/{inv_id}").status_code == 404
print("✅ Confirmed 404 Not Found after deletion")
```

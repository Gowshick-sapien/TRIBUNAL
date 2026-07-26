# Phase D.2 — Persistent Investigation Repository Walkthrough

## Summary of Deliverables

Successfully transformed TRIBUNAL from an in-memory investigation platform into a persistent investigation management system by introducing a durable storage abstraction layer.

---

## Architecture & Data Flow

```
                Browser / Dashboard / API Client
                          │
                          ▼
                FastAPI REST API (/api/v1)
                          │
                          ▼
              Investigation Service Layer
                          │
        ┌─────────────────┴──────────────────┐
        │                                    │
        ▼                                    ▼
 Phase C Investigation Engine        Repository Layer
                                          │
                 ┌────────────────────────┴─────────────────────────┐
                 │                                                  │
                 ▼                                                  ▼
           SQLite Database                              File Storage
                 │                                                  │
                 ▼                                                  ▼
      Investigation Metadata                       Reports / Graphs / Cases / Audit
```

---

## Storage Layout

1. **SQLite Database (`storage/tribunal.db`)**:
   - `investigations`: ID, timestamps, query, dataset, planner intent, risk level, confidence, duration, status, version, artifact file paths.
   - `reports`: Investigation ID, file path, format, generation timestamp.
   - `graphs`: Investigation ID, file path, node count, edge count.
   - `verdicts`: Investigation ID, winning hypothesis, runner-up hypothesis, confidence, recommendation.
   - `audit`: Auto-increment ID, investigation ID, event name, timestamp, details JSON payload.

2. **Filesystem Storage (`storage/files/`)**:
   - `reports/`: `inv_<id>.md` (Markdown) & `inv_<id>.json` (Structured JSON payload).
   - `graphs/`: `inv_<id>.json` (Serialized Evidence Graph node-edge topology).
   - `cases/`: `inv_<id>.json` (Serialized CaseFile state).
   - `audit/`: `inv_<id>.json` (Complete audit trail log).

---

## Extended REST Endpoints Summary

- `GET /api/v1/investigations`: Returns paginated list of historical persistent investigation metadata records.
- `GET /api/v1/investigation/{id}`: Fetches complete investigation metadata and artifact URLs.
- `DELETE /api/v1/investigation/{id}`: Deletes database records and disk files while retaining an immutable audit trail entry.
- `GET /api/v1/report/{id}`, `GET /api/v1/graph/{id}`, `GET /api/v1/verdict/{id}`: Retain fallback to persistent storage if artifacts are not present in transient memory.

---

## Verification Results

| Component | Status | Details |
| :--- | :---: | :--- |
| **Repository Abstraction** | PASSED | Abstract interfaces (`InvestigationRepository`, `ReportRepository`, etc.) isolate business logic |
| **SQLite Persistence** | PASSED | Database table schema initializes automatically; records survive server restarts |
| **File Storage** | PASSED | Markdown reports, JSON graphs, case files, and audit logs written to `storage/files/` |
| **Atomic Persistence** | PASSED | `save_full_investigation()` commits DB records and disk files atomically |
| **Audit Trail** | PASSED | `CREATED`, `PERSISTED`, `RETRIEVED`, `DELETED` events recorded in SQLite DB and JSON logs |
| **REST API Extensions** | PASSED | `GET /investigations`, `GET /investigation/{id}`, `DELETE /investigation/{id}` operational |

### Test Suite Execution
- **Phase D.2 Storage Integration Suite (`test_storage_d2.py`)**: `4/4 PASSED`
- **Entire Workspace Test Suite (`pytest`)**: `131/131 PASSED` (100% pass rate across 131 tests, 0 regressions)

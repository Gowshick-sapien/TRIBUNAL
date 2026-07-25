# Phase D.1 — Investigation Service Layer & REST API Specification & Plan

## Objective

Transform the completed Phase C Investigation Framework into a service-oriented platform by exposing every investigation capability through a versioned REST API (`/api/v1`).

The **Investigation Service Layer** acts as the boundary between external clients (dashboard, CLI, evaluation scripts, future integrations) and the internal Tribunal Investigation Engine. No investigation logic is introduced or modified in this phase. All reasoning continues to reside inside the Phase C modules.

The API layer is responsible only for:
- Request validation
- Orchestration
- Lifecycle management
- Serialization
- Error handling
- Response formatting

---

## Architectural Principles

1. **Investigation Engine Independence**: REST layer contains no investigation logic. It delegates execution to `InvestigationService`.
2. **Stateless Requests**: Every HTTP request is self-contained. The Investigation Service reconstructs the entire investigation state for each execution request. Phase D.1 maintains only transient execution artifacts required for subsequent retrieval endpoints. Long-term persistence is introduced in Phase D.2.
3. **Stable Public Contract**: Internal implementation may evolve while public Pydantic schemas remain stable.
4. **Versioned API**: All endpoints reside under `/api/v1/`.
5. **Modular Routing**: Capabilities split into separate routers (`investigate.py`, `reports.py`, `graph.py`, `health.py`, `metadata.py`).
6. **Typed Schemas**: Request/response contracts enforced via Pydantic models.

---

## Service Layer & ID Lifecycle

Every successful investigation is assigned a globally unique **Investigation ID** (`investigation_id`). Subsequent report, graph, and verdict endpoints operate using this identifier.

```
POST /api/v1/investigate
          │
          ▼
    investigation_id (e.g. inv_a1b2c3d4e5f6)
          │
          ├─────────────────────────┼─────────────────────────┐
          ▼                         ▼                         ▼
GET /api/v1/report/{id}   GET /api/v1/graph/{id}   GET /api/v1/verdict/{id}
```

---

## Repository Structure

```
tribunal/
├── api/
│   ├── app.py
│   ├── routes/
│   │   ├── investigate.py
│   │   ├── reports.py
│   │   ├── graph.py
│   │   ├── health.py
│   │   └── metadata.py
│   ├── schemas/
│   │   ├── common.py
│   │   ├── investigation.py
│   │   ├── report.py
│   │   └── graph.py
│   ├── services/
│   │   └── investigation_service.py
│   ├── dependencies/
│   │   └── __init__.py
│   ├── middleware/
│   │   ├── logging.py
│   │   ├── timing.py
│   │   └── exceptions.py
│   └── utils/
└── docs/
    └── Phase_D/
        ├── Phase_D1_Implementation_Plan.md
        ├── Phase_D1_Walkthrough.md
        └── D1_Manual_Testing_Guide.md
```

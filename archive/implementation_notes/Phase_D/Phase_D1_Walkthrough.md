# Phase D.1 — Investigation Service Layer & REST API Walkthrough

## Summary of Deliverables

Phase D.1 converts TRIBUNAL into an application platform by exposing Phase C engine capabilities over FastAPI REST endpoints.

> [!NOTE]
> **Stateless Engine & Persistence Boundary**:
> The Investigation Service reconstructs the entire investigation state for each execution request. Phase D.1 maintains only transient execution artifacts required for subsequent retrieval endpoints. Long-term persistence is introduced in Phase D.2.

---

## Architectural Flow

```
             Browser / CLI / Dashboard / External Clients
                                   │
                                   ▼
             FastAPI Versioned REST Router (/api/v1)
    (Request Validation, Middleware, Error Handling, OpenAPI Specs)
                                   │
                                   ▼
                   Investigation Service Layer
                 (api.services.investigation_service)
                                   │
  ┌────────────────────────────────┴────────────────────────────────┐
  │                                                                 │
  ▼                                                                 ▼
Planner (C.1) ──► Domain Experts (C.2) ──► Evidence Graph Builder (C.3-C.4)
                                                                    │
                                                                    ▼
Report Generator (C.7) ◄── Tribunal Consensus (C.6) ◄── Adversarial Defense (C.5)
```

---

## Endpoint Specification & ID Lifecycle

Every successful investigation initiated via `POST /api/v1/investigate` is assigned a globally unique **Investigation ID** (`investigation_id`). Subsequent report, graph, and verdict endpoints operate using this identifier.

### Endpoints Overview

1. `POST /api/v1/investigate`
   - Input: `{ "query": "...", "dataset": "default", "options": { ... } }`
   - Output: `InvestigationResponse` containing `investigation_id`, `verdict`, `confidence`, `risk_level`, `report_url`, `graph_url`, `verdict_url`, and metrics.

2. `POST /api/v1/query`
   - Input: `{ "query": "Is customer 541 suspicious?", "dataset": "default" }`
   - Output: `QueryResponse` with short answer, verdict classification, and invoked experts list.

3. `GET /api/v1/report/{id}`
   - Input: `id` path parameter (`investigation_id`). Accepts `Accept: text/markdown` or `application/json`.
   - Output: Full 10-section report in Markdown or JSON format.

4. `GET /api/v1/graph/{id}`
   - Input: `id` path parameter.
   - Output: Serialized node-edge Evidence Graph (`nodes`, `edges`, `statistics`).

5. `GET /api/v1/verdict/{id}`
   - Input: `id` path parameter.
   - Output: Concise Tribunal consensus verdict (`winning_hypothesis`, `confidence`, `confidence_gap`, `deliberation_trace`).

6. `GET /api/v1/health`
   - Output: Health indicators, uptime, and engine readiness.

7. `GET /api/v1/metadata`
   - Output: Supported experts, supported AML patterns, and build details.

---

## Verification Results

### Automated Test Suite (`tribunal/tests/integration/test_api_d1.py`)
- `test_root_endpoint`: PASSED
- `test_health_endpoint`: PASSED
- `test_metadata_endpoint`: PASSED
- `test_investigate_and_artifacts_flow`: PASSED
- `test_conversational_query_endpoint`: PASSED
- `test_invalid_query_validation`: PASSED
- `test_nonexistent_dataset`: PASSED
- `test_nonexistent_investigation_artifact`: PASSED
- `test_openapi_schema`: PASSED

**Result**: 9/9 PASSED (100% pass rate).
**Overall Workspace Result**: 127/127 PASSED (0 regressions).

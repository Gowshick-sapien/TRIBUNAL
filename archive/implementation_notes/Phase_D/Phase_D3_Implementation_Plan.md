# Phase D.3 — Investigation Dashboard & User Experience Platform Specification

## Objective

Transform TRIBUNAL from a backend REST API service into a human investigation workstation ("Bloomberg Terminal for AML Investigations") using React, TypeScript, Vite, and TailwindCSS.

D.3 creates the primary interactive web dashboard for AML compliance investigators and hackathon judges, exposing the query-driven multi-expert workflow built in Phase C, D.1, and D.2 without adding client-side reasoning or bypassing the REST API boundary.

---

## Architectural Position

```text
                    Investigator / Judge
                              │
                              ▼
                 React Investigation Dashboard
                              │
                    REST API (/api/v1)
                              │
                 Investigation Service Layer
                              │
    ───────────────────────────────────────────────────
            Phase C Investigation Engine
    ───────────────────────────────────────────────────
                              │
                    Repository Layer
                              │
                        SQLite + Files
```

### Key Constraints:
1. **Strict REST Boundary**: The dashboard interacts exclusively with `/api/v1` (`POST /investigate`, `POST /query`, `GET /report/{id}`, `GET /graph/{id}`, `GET /verdict/{id}`, `GET /investigations`, `GET /investigation/{id}`, `GET /health`, `GET /metadata`).
2. **Stateless Execution**: UI state lives in React/localStorage; business logic stays on the server.
3. **Dedicated Phase Division**: Interactive node-physics Evidence Graph visualization is cleanly delegated to **Phase D.4**.

---

## Deliverable Modules

1. **Dashboard Shell (D3.1)**: Header with brand & API health status badge, left navigation sidebar, responsive dark mode glassmorphism layout.
2. **Investigation Workspace (D3.2)**: Natural language query box, dataset dropdown selector, run button, live step-by-step animated execution timeline (Planner $\rightarrow$ Financial Expert $\rightarrow$ Behaviour Expert $\rightarrow$ Evidence Graph $\rightarrow$ Defense $\rightarrow$ Tribunal Consensus), verdict badge, risk chip, calibrated confidence progress meter.
3. **Investigation History (D3.3)**: Persistent investigation browser fetching from `GET /api/v1/investigations`, filterable by risk level & search query, with inline record deletion (`DELETE /api/v1/investigation/{id}`).
4. **Investigation Viewer (D3.4)**: Interactive 5-tab workstation (Executive Summary, Evidence & Graph, Defense Counter-Review, Tribunal Consensus, Full 10-Section Report) calling `/report/{id}`, `/graph/{id}`, `/verdict/{id}`.
5. **Platform Status (D3.5)**: System health & capability workstation calling `GET /health` and `GET /metadata` displaying API status, uptime, supported domain experts, and 10 AML pattern detectors.
6. **Settings (D3.6)**: Connection & default preferences page (API Base URL, default dataset, reset defaults).

---

## Verification Matrix

| Component | Verification |
| :--- | :--- |
| **Dashboard Shell** | Responsive navigation across all 6 pages (`/`, `/investigate`, `/history`, `/investigation/:id`, `/system`, `/settings`) |
| **Investigation Workspace** | Query submission triggers live 6-step animated execution timeline and renders persisted verdict |
| **History Repository** | Persistent SQLite records from D.2 listed with search/risk filters and delete actions |
| **Investigation Viewer** | 5-tab interactive viewer loads report, graph metrics, defense findings, and tribunal traces |
| **System Status** | Real-time health check & metadata rendering displaying 10 supported AML pattern detectors |
| **Build & Type Safety** | Zero TypeScript compiler (`tsc -b`) or Vite bundle errors |

# Phase D.2 — Persistent Investigation Repository Specification & Plan

## Objective

Transform TRIBUNAL from an in-memory investigation platform into a persistent investigation management system by introducing a durable, database-independent storage layer.

D.2 introduces a storage abstraction and repository layer that persists investigations, reports, evidence graphs, tribunal verdicts, case files, and audit metadata to disk while preserving the stateless execution model of the Phase C Investigation Engine and the REST API boundary established in Phase D.1.

---

## Architectural Principles

1. **Storage Transparency**: Neither the Planner nor domain experts are aware of storage implementations. All operations proceed through repository interfaces.
2. **Repository Pattern**: Business logic never executes SQL directly. `SQLiteRepository` implements the interfaces; future migration to `PostgreSQLRepository` will require no code changes above the repository layer.
3. **Immutable Investigation Records**: Investigation records are immutable once persisted. Updates are limited to metadata or audit trail logs.
4. **Separation of Metadata and Artifacts**: Metadata (IDs, timestamps, intent, risk level, confidence, execution duration, status) is stored in SQLite tables (`storage/tribunal.db`). Large artifacts (Markdown/JSON reports, JSON evidence graphs, JSON case files, JSON audit logs) are persisted on the filesystem (`storage/files/`).
5. **Atomic Persistence**: Execution saves atomically: either all database records and disk files persist successfully, or the entire operation rolls back and cleans up orphan files.
6. **Database Independence**: Zero-configuration SQLite setup for immediate hackathon MVP deployment with built-in PostgreSQL migration path.

---

## Storage Model & Interfaces

Each investigation consists of five persistent objects:

```
storage/
├── database.py                        # SQLite connection manager & schema init
├── session.py                         # Global session & database manager provider
├── models.py                          # Storage dataclasses (InvestigationRecord, ReportRecord, etc.)
├── repositories/                      # Abstract interfaces
│   ├── investigation_repository.py
│   ├── report_repository.py
│   ├── graph_repository.py
│   ├── verdict_repository.py
│   └── audit_repository.py
├── sqlite/                            # Concrete SQLite & File Repository
│   └── sqlite_repository.py
└── files/                             # Disk file storage
    ├── reports/
    ├── graphs/
    ├── cases/
    └── audit/
```

---

## Extended REST API Endpoints

- `GET /api/v1/investigations`: Returns paginated list of historical persistent investigation records.
- `GET /api/v1/investigation/{id}`: Returns complete investigation record metadata and artifact links.
- `DELETE /api/v1/investigation/{id}`: Deletes database records and disk files while retaining an immutable audit trail entry.
- `GET /api/v1/report/{id}`, `GET /api/v1/graph/{id}`, `GET /api/v1/verdict/{id}`: Updated to fetch persisted artifacts from disk/database, allowing data to survive application restarts.

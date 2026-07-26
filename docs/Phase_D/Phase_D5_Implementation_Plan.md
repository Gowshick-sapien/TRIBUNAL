# Phase D.5 — Investigation Repository Explorer & Advanced Search Platform (Implementation Plan)

## Objective

Transform the persistent investigation repository introduced in Phase D.2 into a comprehensive discovery, exploration, similarity analysis, and side-by-side comparison workstation.

Phase D.5 provides investigators with fast metadata-driven discovery capabilities across large investigation repositories without executing new investigations or modifying Tribunal reasoning logic.

---

## Architectural Position

```text
                  Investigator
                        │
                        ▼
      Repository Explorer & Search Platform (D.5)
                        │
                        ▼
            REST Search API (/api/v1/search/*)
                        │
                        ▼
              Search Repository Layer
                        │
      ┌─────────────────┴──────────────────┐
      │                                    │
      ▼                                    ▼
 SQLite Metadata                    Investigation Files
      │                                    │
      ▼                                    ▼
 Cases / Reports / Graphs / Audit / Verdicts
```

---

## Design Principles

1. **Repository-Driven**: All searches operate exclusively on persisted SQLite metadata and JSON artifacts.
2. **Read-Only Operations**: D.5 retrieves, filters, compares, ranks by similarity, and annotates without re-executing investigation pipelines.
3. **Lazy Loading**: Heavy artifacts (Evidence Graphs, Markdown Reports) are fetched on-demand when requested.
4. **Zero Duplication**: Reuses existing D.1 REST APIs, D.2 Repository, D.3 Dashboard, and D.4 Graph Viewer.

---

## Components & Modules Built

### 1. Storage & Search Repository Layer (`storage/`)
- [database.py](file:///d:/TRIBUNAL/storage/database.py): Extended SQLite schema adding `bookmarks`, `tags`, and `saved_searches` tables with foreign key cascades and indexes.
- [search_repository.py](file:///d:/TRIBUNAL/storage/repositories/search_repository.py): Implements `SearchRepository` with:
  - Multi-criteria SQL search (query text, risk level, confidence ranges, dataset aliases, status, date ranges, sorting, and pagination).
  - Metadata Similarity Ranking Engine (`get_similar()`).
  - Bookmark toggles & user tags management (`AML`, `Payroll`, `Structuring`, `Escalated`).
  - CSV & JSON data exporters.

### 2. REST Search API Router (`api/routes/`)
- [search.py](file:///d:/TRIBUNAL/api/routes/search.py): Versioned endpoints under `/api/v1`:
  - `GET /api/v1/search`: Multi-criteria search and pagination.
  - `GET /api/v1/search/recent`: Recent investigations.
  - `GET /api/v1/search/bookmarks`: Bookmarked investigations.
  - `POST /api/v1/search/bookmarks/{id}`: Toggle bookmark status.
  - `GET /api/v1/search/similar/{id}`: Metadata similarity engine.
  - `POST /api/v1/search/tags/{id}` & `DELETE /api/v1/search/tags/{id}`: Tag management.
  - `GET /api/v1/search/export`: Download CSV or JSON export.

### 3. Frontend Types & API Client (`dashboard/src/`)
- [types/search.ts](file:///d:/TRIBUNAL/dashboard/src/types/search.ts): Data contracts for `SearchResultItem`, `SearchResponse`, `SimilarListResponse`, and `SearchFilterState`.
- [services/search_api.ts](file:///d:/TRIBUNAL/dashboard/src/services/search_api.ts): Axios API client wrapper for `/api/v1/search/*`.

### 4. Workstations & Search Components (`dashboard/src/`)
- [ExplorerPage.tsx](file:///d:/TRIBUNAL/dashboard/src/pages/ExplorerPage.tsx): Repository Explorer page at `/explorer`.
- [ComparePage.tsx](file:///d:/TRIBUNAL/dashboard/src/pages/ComparePage.tsx): Side-by-side Investigation Comparison page at `/compare`.
- [SearchBar.tsx](file:///d:/TRIBUNAL/dashboard/src/components/search/SearchBar.tsx): Multi-field live text search.
- [FilterPanel.tsx](file:///d:/TRIBUNAL/dashboard/src/components/search/FilterPanel.tsx): Collapsible filter drawer (Risk, dataset, status, confidence slider, sorting).
- [SavedSearches.tsx](file:///d:/TRIBUNAL/dashboard/src/components/search/SavedSearches.tsx): One-click preset search chips.
- [ResultTable.tsx](file:///d:/TRIBUNAL/dashboard/src/components/search/ResultTable.tsx): Rich result table with compare selection, bookmarking, and CSV/JSON export actions.
- [InvestigationPreview.tsx](file:///d:/TRIBUNAL/dashboard/src/components/search/InvestigationPreview.tsx): Slide-over preview drawer.
- [ComparisonPanel.tsx](file:///d:/TRIBUNAL/dashboard/src/components/search/ComparisonPanel.tsx): Side-by-side comparison workspace.

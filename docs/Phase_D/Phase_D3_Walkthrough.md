# Phase D.3 — Investigation Dashboard & User Experience Platform Walkthrough

## Summary of Deliverables

Successfully built and verified **Phase D.3 — Investigation Dashboard & User Experience Platform**, creating a human investigation workstation ("Bloomberg Terminal for AML Investigations") using React, TypeScript, Vite, and TailwindCSS.

---

## Workspace Structure (`dashboard/`)

```
dashboard/
├── index.html                         # Google Fonts (Inter + JetBrains Mono) & title
├── package.json                       # React 19, React Router 7, Axios, Lucide, Tailwind v3
├── postcss.config.js                  # PostCSS configuration
├── tailwind.config.js                 # Bloomberg Terminal dark palette & glow animations
├── vite.config.ts                     # Vite build configuration
└── src/
    ├── App.tsx                        # Main Router & Layout shell
    ├── main.tsx                       # React root renderer
    ├── index.css                      # Tailwind base & glassmorphism utilities
    ├── types/
    │   └── index.ts                   # Typed contracts matching REST API schemas
    ├── services/
    │   └── api.ts                     # Axios API client for /api/v1 endpoints
    ├── components/
    │   ├── common/
    │   │   ├── ConfidenceMeter.tsx    # Calibrated confidence bar meter
    │   │   ├── ExecutionTimeline.tsx  # Live 6-step animated engine pipeline
    │   │   ├── RiskChip.tsx           # CRITICAL, HIGH, MEDIUM, LOW risk chip
    │   │   └── VerdictBadge.tsx       # LIKELY_MALICIOUS, POSSIBLY_MALICIOUS badges
    │   └── layout/
    │       ├── Navbar.tsx             # Header with brand mark & health status badge
    │       └── Sidebar.tsx            # Left navigation console
    └── pages/
        ├── HomePage.tsx               # Demo landing station with pre-configured scenarios
        ├── WorkspacePage.tsx          # Primary investigation workspace & live execution
        ├── HistoryPage.tsx            # Persistent D.2 repository browser & filters
        ├── ViewerPage.tsx             # Interactive 5-tab investigation viewer
        ├── SystemPage.tsx             # Real-time health & 10 AML pattern detector status
        └── SettingsPage.tsx           # API Base URL & default dataset settings
```

---

## Key Features & UI Capabilities

1. **Bloomberg Terminal Dark Theme**: Sleek backdrop (`#090d16`), cyan/sky blue accents (`#38bdf8`), emerald verdict badges (`#10b981`), rose risk chips (`#f43f5e`), glassmorphism cards, and monospace typography.
2. **Pre-Configured Demo Scenarios**: Home page features 3 one-click scenarios (Structuring & Velocity Analysis, Dormancy & Baseline Drift, Rapid Wire Transfer Burst) ideal for hackathon judge presentations.
3. **Live Execution Timeline**: Workspace animates 6 engine pipeline stages in real time (Planner $\rightarrow$ Financial Expert $\rightarrow$ Behaviour Expert $\rightarrow$ Evidence Graph $\rightarrow$ Defense $\rightarrow$ Tribunal) with duration profiling metrics.
4. **Interactive 5-Tab Viewer**: Allows investigators to inspect Executive Summaries, Evidence Topology metrics, Defense Counter-Reviews, Tribunal Multi-Hypothesis Consensus, and full 10-section Markdown reports.
5. **Persistent History Browser**: Interacts directly with D.2 SQLite repository endpoints (`GET /api/v1/investigations`, `DELETE /api/v1/investigation/{id}`) with search and risk filters.

---

## Verification Results

| Component | Status | Details |
| :--- | :---: | :--- |
| **TypeScript Compilation** | PASSED | `npx tsc -b` completed with **0 errors and 0 warnings** |
| **Vite Bundle Build** | PASSED | `npm run build` generated `dist/` production bundle in 1.91s |
| **REST API Integration** | PASSED | Pure REST API communication with `/api/v1` backend |
| **Responsive Workstations** | PASSED | All 6 pages operational (`/`, `/investigate`, `/history`, `/investigation/:id`, `/system`, `/settings`) |

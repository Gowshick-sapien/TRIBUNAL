# Phase D.4 — Manual Testing Guide

This guide provides step-by-step instructions for manually testing the **Phase D.4 Interactive Evidence Graph Visualization Platform**.

---

## Step 1: Start Backend API & Dashboard

1. Launch FastAPI backend API:
   ```cmd
   uvicorn api.app:app --host 127.0.0.1 --port 8000 --reload
   ```
2. Launch Vite frontend dev server:
   ```cmd
   cd dashboard
   npm run dev
   ```
3. Open `http://localhost:5173/` in your browser.

---

## Step 2: Run an Investigation to Generate Evidence Graph

1. Navigate to `/investigate` (Investigation Workspace).
2. Submit a query:
   ```text
   Is customer ACC_8000A94C0 engaged in structuring and velocity anomalies?
   ```
3. Wait for the pipeline execution to complete.
4. Click **"Open Full Investigation Viewer →"**.

---

## Step 3: Test Embedded Canvas Viewer (Tab 2: Evidence & Graph)

1. Select **Tab 2: Evidence & Topology**.
2. Verify the interactive React Flow graph canvas loads directly inside the viewer tab.
3. Verify directional Dagre layouting (cards arranged left-to-right).
4. Click **"Open Fullscreen Studio"** in the top right.

---

## Step 4: Test Fullscreen Graph Studio Features (`/graph/:id`)

1. **Node Selection**:
   - Click any **Investigation Card** node. Verify the right **Node Inspector** side-panel opens, displaying:
     - Card ID and Severity Risk Chip
     - Calibrated Confidence Meter
     - Hypothesis text
     - Provenance & Verified Transaction IDs
2. **Edge Selection**:
   - Click any edge connecting two nodes. Verify the right **Edge Inspector** side-panel opens, displaying:
     - Relationship Type (`SUPPORT` or `CONTRADICTION`)
     - Support weight score
     - Reason description
3. **Highlight Winning Chain Overlay**:
   - Click the **"Highlight Winning Chain"** button on the floating toolbar.
   - Verify non-essential nodes/edges dim, while the winning Tribunal consensus chain illuminates in neon cyan.
4. **Search & Filters**:
   - Enter `ACC_8000A94C0` or `Structuring` in the live search bar. Verify matching nodes highlight.
   - Filter by Expert (`Financial Expert`, `Behaviour Expert`) or Severity (`CRITICAL`, `HIGH`).
5. **Canvas Controls & Export**:
   - Test Zoom In, Zoom Out, Fit Screen, and Reset buttons.
   - Click **PNG** export button. Verify a PNG screenshot file `evidence_graph_inv_<id>.png` is downloaded.

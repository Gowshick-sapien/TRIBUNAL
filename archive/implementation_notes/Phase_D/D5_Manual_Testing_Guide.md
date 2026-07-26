# Phase D.5 — Manual Testing Guide

This guide provides step-by-step instructions for manually testing the **Phase D.5 Investigation Repository Explorer & Advanced Search Platform**.

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

## Step 2: Access Repository Explorer Workstation (`/explorer`)

1. Click **"Repository Explorer"** on the left sidebar navigation console.
2. Verify the page header displays:
   `Repository Explorer & Advanced Search Platform`
3. Verify the main table populates with historical investigations stored in the repository.

---

## Step 3: Test Multi-Criteria Search & Filtering

1. **Text Search**:
   - Type `ACC_8000A94C0` or `Structuring` into the search bar.
   - Verify the table live-filters to matching investigation records.
2. **Advanced Filters Drawer**:
   - Click **"Advanced Filters"**.
   - Select Risk Classification = `CRITICAL` or `HIGH`.
   - Adjust the **Min Confidence Threshold** slider to `80%`.
   - Select Dataset Reference = `Default Dataset`.
   - Select Sort Order = `Highest Confidence` or `Fastest Execution`.
   - Verify matching items update accurately.
3. **One-Click Saved Search Presets**:
   - Click the **"CRITICAL Risk Cases"** preset chip.
   - Verify the risk filter applies automatically.
   - Click **"High Confidence (>80%)"** or **"Bookmarked"**.

---

## Step 4: Test Slide-Over Investigation Preview Drawer

1. Click the **Eye icon** action button on any investigation row.
2. Verify the slide-over preview drawer opens from the right side of the screen.
3. Verify the drawer displays:
   - Target Query & Planner Intent
   - Winning Hypothesis & Confidence Meter
   - Tribunal Recommendation
   - Topology Statistics (Node count & Edge count)
   - **Similar Investigations (Ranked by Metadata)** with percentage similarity scores.
4. Click **"Open Full Investigation Viewer"** or **"Open Interactive Graph Studio"** from inside the preview drawer.

---

## Step 5: Test Side-by-Side Comparison Workspace (`/compare?left=...&right=...`)

1. In the Repository Explorer table, check the **Compare checkbox** for Investigation A (`inv_001`).
2. Check the **Compare checkbox** for Investigation B (`inv_002`).
3. Notice the top floating action button appears: **"Compare Selected (2/2) →"**.
4. Click **"Compare Selected (2/2) →"**.
5. Verify navigation to `/compare?left=inv_001&right=inv_002` (URL parameter transfer: refresh-safe and bookmarkable).
6. Verify the header displays:
   `Compare inv_001 vs inv_002`
7. Verify the side-by-side comparison workstation renders dual cards comparing:
   - Target Query & Intent
   - Winning Hypothesis & Calibrated Confidence
   - Tribunal Recommendation & Risk level
   - Dataset & Execution duration
   - Topology Node & Edge counts
   - Direct action buttons to view each investigation's report or graph.

---

## Step 6: Test Bookmarks & File Exports

1. **Bookmarking**:
   - Click the **Bookmark icon** on any table row. Verify the bookmark fills with amber color.
   - Click **"Advanced Filters"** and check **"Filter Bookmarks Only"**. Verify only bookmarked items are listed.
2. **CSV Export**:
   - Click **"Export CSV"** in the table header.
   - Verify a file `tribunal_search_results.csv` is downloaded.
3. **JSON Export**:
   - Click **"Export JSON"** in the table header.
   - Verify a file `tribunal_search_results.json` is downloaded.

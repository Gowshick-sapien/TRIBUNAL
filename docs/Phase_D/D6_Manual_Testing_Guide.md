# Phase D.6 — Manual Testing Guide

This guide provides step-by-step instructions for manually testing the **Phase D.6 Interactive Investigation Report & Export Platform**.

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

## Step 2: Access Interactive Report Workstation (`/report/:id`)

1. Run an investigation from `/investigate` or select an existing case from `/history` or `/explorer`.
2. Click **"Open Full Investigation Viewer"** or navigate directly to `/report/<investigation_id>`.
3. Verify the page header displays:
   - Case ID & Risk Badge (`CRITICAL`, `HIGH`, `MEDIUM`)
   - Calibrated Confidence Score Meter
   - Assessed Executive Recommendation
   - Dataset & Execution Timestamp

---

## Step 3: Test Section Navigation Sidebar

1. On the left sidebar, click **"Executive Summary"**. Verify smooth scroll to Section 1.
2. Click **"Evidence Graph"**. Verify smooth scroll to Evidence Cards.
3. Click **"Defense Review"**. Verify counter-hypotheses accepted/rejected breakdown renders.
4. Click **"Tribunal Deliberation"**. Verify winning hypothesis, runner-up, support margin, and confidence gap render.
5. Click **"Audit Trail"**. Verify pipeline execution timeline renders.

---

## Step 4: Test Evidence Card Cross-Linking to D.4 Graph Studio

1. Scroll to **Section 5: Evidence Cards & Topology**.
2. Locate an Evidence Card (e.g. `c_fin_structuring_01`).
3. Click **"Highlight Node in Graph →"**.
4. Verify seamless navigation to the D.4 Interactive Evidence Graph Studio (`/graph/<investigation_id>`).

---

## Step 5: Test Investigator Annotations

1. On the report toolbar, click the **"Notes"** button.
2. Verify the slide-over **Investigator Annotations** panel opens from the right.
3. Type an author name (e.g., `Senior Compliance Officer`).
4. Type note text:
   `Escalated for immediate SAR filing due to structuring velocity.`
5. Click **"Attach Annotation"**.
6. Verify the note appears in the list with timestamp and author.
7. Refresh the page (`F5`) and open **"Notes"** again. Verify the annotation persisted.
8. Click the **Trash icon** to delete the test annotation.

---

## Step 6: Test Multi-Format Exports & Print PDF Layout

1. **Markdown Export**:
   - Click **"Export Report"** -> **"Markdown (.md)"**.
   - Verify a `.md` file download starts.
2. **HTML Export**:
   - Click **"Export Report"** -> **"HTML Document"**.
   - Verify styled HTML document opens in browser.
3. **JSON Export**:
   - Click **"Export Report"** -> **"Structured JSON"**.
   - Verify JSON payload download starts.
4. **Print / PDF Layout**:
   - Click **"Print / Save PDF"**.
   - Verify browser print preview opens with clean compliance CSS formatting (sidebars and toolbars hidden).

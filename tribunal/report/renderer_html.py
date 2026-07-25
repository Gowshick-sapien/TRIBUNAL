"""HTML Renderer module — Renders InvestigationReport into standalone interactive HTML."""

from __future__ import annotations

import html
from tribunal.models.investigation_report import InvestigationReport


class HTMLRenderer:
    """Renders structured InvestigationReport into styled, interactive standalone HTML."""

    def render(self, report: InvestigationReport) -> str:
        """Transform InvestigationReport into full HTML string."""
        es = report.executive_summary
        meta = report.metadata
        gs = report.graph_summary
        ts = report.tribunal_summary

        verdict_color = "#3b82f6"
        verdict_str = es.get("verdict", "INCONCLUSIVE")
        if verdict_str == "LIKELY_MALICIOUS":
            verdict_color = "#ef4444"
        elif verdict_str == "POSSIBLY_MALICIOUS":
            verdict_color = "#f59e0b"
        elif verdict_str == "LIKELY_LEGITIMATE":
            verdict_color = "#10b981"

        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TRIBUNAL Investigation Report — {html.escape(str(meta.get('report_id', 'TRIBUNAL')))}</title>
    <style>
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
            margin: 0;
            padding: 40px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }}
        h1 {{ font-size: 28px; margin-top: 0; color: #38bdf8; }}
        h2 {{ font-size: 20px; border-bottom: 2px solid #334155; padding-bottom: 8px; margin-top: 32px; color: #94a3b8; }}
        .badge {{
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
            color: white;
            background-color: {verdict_color};
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin: 20px 0;
        }}
        .card {{
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 16px;
        }}
        .card .title {{ font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; }}
        .card .val {{ font-size: 20px; font-weight: bold; margin-top: 6px; color: #f8fafc; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
        }}
        th, td {{
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid #334155;
            font-size: 14px;
        }}
        th {{ background-color: #0f172a; color: #38bdf8; }}
        code {{ background: #0f172a; padding: 2px 6px; border-radius: 4px; color: #38bdf8; font-family: monospace; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>TRIBUNAL Investigation Report</h1>
        <p><strong>Report ID:</strong> <code>{html.escape(str(meta.get('report_id')))}</code> | <strong>Date:</strong> {html.escape(str(meta.get('generated_at')))} | <strong>Case:</strong> <code>{html.escape(str(meta.get('case_id')))}</code></p>
        
        <h2>1. Executive Summary</h2>
        <p><span class="badge">{html.escape(verdict_str)}</span></p>
        <div class="grid">
            <div class="card">
                <div class="title">Primary Hypothesis</div>
                <div class="val" style="font-size: 14px;">{html.escape(str(es.get('primary_hypothesis', 'N/A')))}</div>
            </div>
            <div class="card">
                <div class="title">Primary Score</div>
                <div class="val">{es.get('primary_score', 0.0):.4f}</div>
            </div>
            <div class="card">
                <div class="title">Calibrated Confidence</div>
                <div class="val">{es.get('calibrated_confidence', 0.0):.2f}</div>
            </div>
            <div class="card">
                <div class="title">Risk Level</div>
                <div class="val">{html.escape(str(es.get('risk_level', 'MEDIUM')))}</div>
            </div>
        </div>
        <p><strong>Recommendation:</strong> {html.escape(str(es.get('recommendation', '')))}</p>

        <h2>2. Query Interpretation & Pipeline Timeline</h2>
        <p><strong>Original Query:</strong> <em>"{html.escape(str(report.query_interpretation.get('raw_query')))}"</em></p>
        <table>
            <thead>
                <tr><th>Stage #</th><th>Stage Name</th><th>Action</th><th>Status</th><th>Duration</th></tr>
            </thead>
            <tbody>
"""
        for t in report.timeline:
            html_doc += f"<tr><td>{t.get('stage_index')}</td><td>{html.escape(str(t.get('stage_name')))}</td><td>{html.escape(str(t.get('action')))}</td><td><code>{html.escape(str(t.get('status')))}</code></td><td>{t.get('duration_ms')} ms</td></tr>\n"

        html_doc += f"""
            </tbody>
        </table>

        <h2>3. Evidence Graph Topology & Findings</h2>
        <p>{html.escape(str(gs.get('summary_statement')))}</p>
        
        <h2>4. Tribunal Consensus & Audit Trail</h2>
        <p>{html.escape(str(ts.get('reasoning_narrative')))}</p>
        <table>
            <thead>
                <tr><th>Step #</th><th>Stage Name</th><th>Decision ID</th><th>Duration</th><th>Description</th></tr>
            </thead>
            <tbody>
"""
        for st in report.audit_trail:
            html_doc += f"<tr><td>{st.get('step_number')}</td><td>{html.escape(str(st.get('stage_name')))}</td><td><code>{html.escape(str(st.get('decision_id')))}</code></td><td>{st.get('step_duration_ms')} ms</td><td>{html.escape(str(st.get('description')))}</td></tr>\n"

        html_doc += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""
        return html_doc

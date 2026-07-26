"""Markdown Renderer module — Renders InvestigationReport into GitHub-flavored Markdown."""

from __future__ import annotations

from tribunal.models.investigation_report import InvestigationReport


class MarkdownRenderer:
    """Renders structured InvestigationReport into clear, formatted Markdown."""

    def render(self, report: InvestigationReport) -> str:
        """Transform InvestigationReport into full Markdown document string."""
        lines: list[str] = []

        es = report.executive_summary
        meta = report.metadata

        lines.append(f"# Investigation Report — {meta.get('report_id', 'TRIBUNAL')}")
        lines.append(f"**Generated Date:** `{meta.get('generated_at', '')}` | **Case ID:** `{meta.get('case_id', '')}` | **Engine Version:** `C.7`\n")

        lines.append("---")
        lines.append("## 1. Executive Summary\n")
        lines.append(f"> [!IMPORTANT]\n> **Verdict:** `{es.get('verdict', 'INCONCLUSIVE')}` | **Calibrated Confidence:** `{es.get('calibrated_confidence', 0.0):.2f}` | **Risk Level:** `{es.get('risk_level', 'MEDIUM')}`\n")
        if es.get("key_takeaway"):
            lines.append(f"> {es.get('key_takeaway')}\n")
        lines.append(f"- **Primary Hypothesis:** {es.get('primary_hypothesis', 'N/A')} (Net Score: `{es.get('primary_score', 0.0):.4f}`)")
        if es.get("secondary_hypothesis"):
            lines.append(f"- **Secondary Hypothesis:** {es.get('secondary_hypothesis')} (Net Score: `{es.get('secondary_score', 0.0):.4f}`)")
            lines.append(f"- **Confidence Gap (Delta):** `{es.get('confidence_gap', 0.0):.4f}`")
        lines.append(f"- **Recommendation:** {es.get('recommendation', '')}\n")

        lines.append("---")
        lines.append("## 2. Query Interpretation & Planning\n")
        qi = report.query_interpretation
        lines.append(f"- **Original Query:** *\"{qi.get('raw_query', '')}\"*")
        lines.append(f"- **Parsed Intent:** `{qi.get('parsed_intent', '')}`")
        target_str = qi.get("resolved_target_id", "N/A")
        status_str = qi.get("target_resolution_status", "N/A")
        lines.append(f"- **Requested Target Entity:** `{target_str}` (`{status_str}`)")
        lines.append(f"- **Experts Invoked:** `{qi.get('experts_invoked', [])}`\n")

        lines.append("---")
        lines.append("## 3. Investigation Pipeline Timeline\n")
        lines.append("| Stage # | Stage Name | Action Executed | Status | Duration (ms) |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for item in report.timeline:
            lines.append(f"| {item.get('stage_index')} | {item.get('stage_name')} | {item.get('action')} | `{item.get('status')}` | {item.get('duration_ms')} ms |")
        lines.append("")

        lines.append("---")
        lines.append("## 4. Expert Investigation Findings\n")
        if not report.expert_findings:
            lines.append("*No expert investigation cards generated.*\n")
        else:
            for f in report.expert_findings:
                lines.append(f"### Expert Card: `{f.get('card_id')}` ({f.get('expert').upper()})")
                lines.append(f"- **Hypothesis:** {f.get('hypothesis')}")
                lines.append(f"- **Confidence:** `{f.get('confidence'):.2f}` | **Severity:** `{f.get('severity')}`")
                lines.append(f"- **Affected Accounts:** `{f.get('affected_accounts')}`")
                lines.append("#### Natural Language Explanations:")
                for nle in f.get("natural_language_explanations", []):
                    lines.append(f"  * {nle}")
                lines.append("")

        lines.append("---")
        lines.append("## 5. Evidence Synthesis & Graph Topology\n")
        gs = report.graph_summary
        lines.append(f"> [!NOTE]\n> {gs.get('summary_statement', '')}\n")
        lines.append(f"- **Total Nodes:** {gs.get('node_count')} ({gs.get('account_nodes')} Accounts, {gs.get('card_nodes')} Cards, {gs.get('hypothesis_nodes')} Hypotheses)")
        lines.append(f"- **Total Edges:** {gs.get('edge_count')} ({gs.get('corroboration_edges')} Corroboration, {gs.get('contradiction_edges')} Contradiction)")
        lines.append(f"- **Connected Components:** {gs.get('connected_components')} | **Graph Density:** {gs.get('graph_density'):.4f}\n")

        lines.append("---")
        lines.append("## 6. Adversarial Review & Defense Summary\n")
        ds = report.defense_summary
        lines.append(f"- **Defense Summary:** {ds.get('summary_statement')}")
        if ds.get("has_defense_evidence"):
            for dc in ds.get("defense_cards", []):
                lines.append(f"  * **Defense Card `{dc.get('card_id')}`**: {dc.get('hypothesis')} (Confidence: `{dc.get('confidence'):.2f}`)")
        lines.append("")

        lines.append("---")
        lines.append("## 7. Tribunal Consensus & Deliberation Details\n")
        ts = report.tribunal_summary
        lines.append(f"- **Consensus Verdict:** `{ts.get('verdict')}`")
        lines.append(f"- **Reasoning Narrative:** {ts.get('reasoning_narrative')}")
        lines.append("#### Rejected Hypotheses:")
        for r in ts.get("rejected_hypotheses", []):
            lines.append(f"  * **{r.get('title')}** (Net Score: `{r.get('net_support_score'):.2f}`) — *{r.get('rejection_reason')}*")
        lines.append("")

        lines.append("---")
        lines.append("## 8. Evidence Provenance Lineage\n")
        if not report.provenance_details:
            lines.append("*No provenance lineage recorded.*\n")
        else:
            for p in report.provenance_details:
                lines.append(f"- **Card `{p.get('card_id')}` ({p.get('expert')})**: Detectors: `{p.get('detectors')}` | Transaction IDs: `{p.get('transaction_ids')}`")
        lines.append("")

        lines.append("---")
        lines.append("## 9. Profiled Audit Trail & Traceability\n")
        lines.append("| Step | Stage Name | Decision ID | Duration (ms) | Description |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for st in report.audit_trail:
            lines.append(f"| {st.get('step_number')} | {st.get('stage_name')} | `{st.get('decision_id')}` | {st.get('step_duration_ms')} ms | {st.get('description')} |")
        lines.append("")

        return "\n".join(lines)

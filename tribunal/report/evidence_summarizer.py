"""Evidence Summarizer module — Synthesizes expert findings, metrics, and transaction provenance."""

from __future__ import annotations

from typing import Any

from tribunal.report.explainability_engine import ExplainabilityEngine


class EvidenceSummarizer:
    """Builds Section 4 (Expert Findings), Section 5 (Evidence Summary), and Section 9 (Evidence Provenance)."""

    def __init__(self, explainability_engine: ExplainabilityEngine | None = None) -> None:
        self.explainability_engine = explainability_engine or ExplainabilityEngine()

    def build_expert_findings(self, case_file: Any) -> list[dict[str, Any]]:
        """Group and format investigation cards by domain expert."""
        findings: list[dict[str, Any]] = []
        if not case_file or not hasattr(case_file, "evidence_cards"):
            return findings

        for card in case_file.evidence_cards:
            c_expert = getattr(card, "source_expert", "unknown")
            c_id = getattr(card, "card_id", "c_unk")
            c_hyp = getattr(card, "hypothesis", "")
            c_conf = getattr(card, "confidence", 0.0)
            c_sev = getattr(card, "severity", "MEDIUM")
            c_metrics = getattr(card, "supporting_metrics", {})
            c_prov = getattr(card, "provenance", {})
            c_txns = getattr(card, "derived_from_transactions", [])
            c_accs = getattr(card, "affected_accounts", [])

            explanations = self.explainability_engine.explain_finding(c_hyp, c_metrics)

            findings.append({
                "card_id": c_id,
                "expert": c_expert,
                "hypothesis": c_hyp,
                "confidence": c_conf,
                "severity": c_sev,
                "affected_accounts": c_accs,
                "transaction_count": len(c_txns),
                "transaction_ids": c_txns,
                "supporting_metrics": c_metrics,
                "provenance": c_prov,
                "natural_language_explanations": explanations,
            })

        return findings

    def build_provenance_details(self, case_file: Any) -> list[dict[str, Any]]:
        """Construct Section 9: Evidence Provenance trace."""
        provenance_list: list[dict[str, Any]] = []
        if not case_file or not hasattr(case_file, "evidence_cards"):
            return provenance_list

        for card in case_file.evidence_cards:
            c_id = getattr(card, "card_id", "c_unk")
            c_expert = getattr(card, "source_expert", "unknown")
            c_prov = getattr(card, "provenance", {})
            c_txns = getattr(card, "derived_from_transactions", [])

            detectors = c_prov.get("detectors", [c_prov.get("defense_type", "StandardDetector")])
            feature_rows = c_prov.get("feature_store_rows", [])

            provenance_list.append({
                "card_id": c_id,
                "expert": c_expert,
                "detectors": detectors,
                "transaction_ids": c_txns,
                "feature_store_rows": feature_rows,
                "provenance_raw": c_prov,
            })

        return provenance_list

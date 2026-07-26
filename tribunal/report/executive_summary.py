"""Executive Summary Builder — Projection of Tribunal Verdict & Risk Assessment."""

from __future__ import annotations

import datetime
import uuid
from typing import Any

from tribunal.models.tribunal_verdict import TribunalVerdict


class ExecutiveSummaryBuilder:
    """Builds Section 1: Executive Summary."""

    def build(
        self,
        verdict: TribunalVerdict,
        query_text: str = "",
        case_id: str = "",
    ) -> dict[str, Any]:
        """Construct Executive Summary section payload."""
        now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        report_id = f"rpt_{case_id}_{uuid.uuid4().hex[:6]}" if case_id else f"rpt_{uuid.uuid4().hex[:6]}"

        v_cat = getattr(verdict, "verdict", "INCONCLUSIVE")
        primary_hyp = getattr(verdict, "primary_hypothesis", getattr(verdict, "winning_hypothesis", "N/A"))
        primary_score = getattr(verdict, "primary_score", getattr(verdict, "winning_score", 0.0))
        conf = getattr(verdict, "confidence", 0.0)
        risk = getattr(verdict, "risk_level", "MEDIUM")
        rec = getattr(verdict, "recommendation", "")

        import re
        suspect_entity = None
        match = re.search(r"(?:Account|Customer)\s+([A-Za-z0-9_-]+)", primary_hyp, re.IGNORECASE)
        if match:
            suspect_entity = match.group(1)

        target_entity = None
        t_match = re.search(r"(?:Account|Customer|ACC_)\s*([A-Za-z0-9_-]+)", query_text, re.IGNORECASE)
        if t_match:
            target_entity = t_match.group(1)

        if suspect_entity and target_entity and suspect_entity.lower() not in target_entity.lower() and target_entity.lower() not in suspect_entity.lower():
            key_takeaway = (
                f"The requested target entity '{query_text}' was successfully investigated. "
                f"Primary suspicious evidence was identified on connected counterparty account {suspect_entity}, "
                f"which exhibited suspicious patterns linked to the target."
            )
        else:
            key_takeaway = f"Tribunal issued '{v_cat}' verdict for primary hypothesis '{primary_hyp}' with calibrated confidence of {conf:.2f}."

        return {
            "report_id": report_id,
            "date": now_str,
            "query": query_text or "General Investigation Query",
            "case_id": case_id or "default_case",
            "verdict": v_cat,
            "primary_hypothesis": primary_hyp,
            "primary_score": round(primary_score, 4),
            "secondary_hypothesis": getattr(verdict, "secondary_hypothesis", None),
            "secondary_score": getattr(verdict, "secondary_score", None),
            "confidence_gap": getattr(verdict, "confidence_gap", 0.0),
            "calibrated_confidence": round(conf, 4),
            "risk_level": risk,
            "recommendation": rec,
            "key_takeaway": key_takeaway,
            "suspect_entity": suspect_entity,
        }

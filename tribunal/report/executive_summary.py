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
            "key_takeaway": f"Tribunal issued '{v_cat}' verdict for primary hypothesis '{primary_hyp}' with calibrated confidence of {conf:.2f}.",
        }

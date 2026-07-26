"""Risk Calibrator module — Multi-dimensional Risk Calibration Layer (Phase C.6)."""

from __future__ import annotations

import logging
from typing import Any

from tribunal.consensus.consensus_engine import ConsensusResult
from tribunal.models.case_file import CaseFile
from tribunal.models.evidence_graph import EvidenceGraph

logger = logging.getLogger("tribunal.consensus.risk_calibrator")


class RiskCalibrator:
    """Evaluates multi-dimensional risk level (CRITICAL, HIGH, MEDIUM, LOW).
    
    Rather than relying solely on a single threshold, evaluates:
    1. Consensus Category (LIKELY_MALICIOUS, POSSIBLY_MALICIOUS, INCONCLUSIVE, LIKELY_LEGITIMATE)
    2. Net Support Score (S_primary)
    3. Calibrated Confidence (C_final)
    4. Support Margin / Confidence Gap (Delta)
    5. Evidence Severities (CRITICAL, HIGH cards) & Expert Corroboration Count
    """

    def calibrate_risk(
        self,
        consensus_result: ConsensusResult,
        calibrated_confidence: float,
        graph: EvidenceGraph | None = None,
        case_file: CaseFile | None = None,
    ) -> str:
        """Assign realistic multi-dimensional risk category."""
        cat = consensus_result.consensus_category
        winner = consensus_result.winning_hypothesis
        net_support = winner.net_support_score
        gap = consensus_result.confidence_gap

        # Inspect supporting card severities from case file or graph
        has_critical_card = False
        has_high_card = False
        if case_file and hasattr(case_file, "evidence_cards"):
            for card in case_file.evidence_cards:
                c_id = getattr(card, "card_id", "")
                if c_id in winner.supporting_cards or not winner.supporting_cards:
                    sev = str(getattr(card, "severity", "MEDIUM")).upper()
                    if sev == "CRITICAL":
                        has_critical_card = True
                    elif sev == "HIGH":
                        has_high_card = True

        valid_experts = [e for e in winner.expert_sources if e not in ("defense", "system")]
        is_multi_expert = len(valid_experts) >= 2

        # 1. CRITICAL Risk Conditions
        if cat == "LIKELY_MALICIOUS":
            if net_support >= 0.70 or calibrated_confidence >= 0.70 or has_critical_card or (is_multi_expert and net_support >= 0.65):
                return "CRITICAL"
        elif cat == "POSSIBLY_MALICIOUS":
            if net_support >= 0.75 and (has_critical_card or (is_multi_expert and gap >= 0.01)):
                return "CRITICAL"

        # 2. HIGH Risk Conditions
        if cat == "LIKELY_MALICIOUS":
            return "HIGH"
        elif cat == "POSSIBLY_MALICIOUS":
            if net_support >= 0.60 or calibrated_confidence >= 0.55 or has_critical_card or has_high_card or is_multi_expert:
                return "HIGH"
            return "MEDIUM"

        # 3. MEDIUM Risk Conditions
        if cat == "POSSIBLY_MALICIOUS":
            return "MEDIUM"
        elif cat == "INCONCLUSIVE":
            if net_support >= 0.40 or calibrated_confidence >= 0.40 or has_high_card:
                return "MEDIUM"
            return "LOW"

        # 4. LOW Risk Conditions (LIKELY_LEGITIMATE or weak INCONCLUSIVE)
        if cat == "LIKELY_LEGITIMATE":
            return "LOW"

        return "LOW"

"""Consensus Engine module — Ranks competing hypotheses and determines consensus verdict."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from tribunal.consensus.contradiction_resolver import ResolvedHypothesis


# Consensus Verdict Constants
LIKELY_MALICIOUS = "LIKELY_MALICIOUS"
POSSIBLY_MALICIOUS = "POSSIBLY_MALICIOUS"
INCONCLUSIVE = "INCONCLUSIVE"
LIKELY_LEGITIMATE = "LIKELY_LEGITIMATE"


@dataclass
class ConsensusResult:
    consensus_category: str
    winning_hypothesis: ResolvedHypothesis
    runner_up_hypothesis: ResolvedHypothesis | None
    confidence_gap: float
    ranked_hypotheses: list[ResolvedHypothesis]
    rejected_hypotheses: list[dict[str, Any]] = field(default_factory=list)
    rejection_reason: str = ""


class ConsensusEngine:
    """Ranks competing hypotheses and applies deterministic consensus rules to determine the winning hypothesis and category."""

    def evaluate(
        self,
        resolved_hypotheses: list[ResolvedHypothesis],
        target_pattern: str | None = None,
    ) -> ConsensusResult:
        """Deterministically rank hypotheses and evaluate consensus rules."""
        if not resolved_hypotheses:
            default_hyp = ResolvedHypothesis(
                hypothesis_id="hyp_none",
                title="No Hypothesis Extracted",
                raw_support_score=0.0,
                opposing_score=0.0,
                net_support_score=0.0,
            )
            return ConsensusResult(
                consensus_category=INCONCLUSIVE,
                winning_hypothesis=default_hyp,
                runner_up_hypothesis=None,
                confidence_gap=0.0,
                ranked_hypotheses=[default_hyp],
                rejection_reason="No hypotheses available for deliberation",
            )

        candidates = list(resolved_hypotheses)
        rejected_list: list[dict[str, Any]] = []

        # Intent & Pattern Filtering: If a specific target pattern was requested, prioritize matching hypotheses
        if target_pattern and str(target_pattern).lower() not in ("general", "none"):
            pat = str(target_pattern).lower().strip()
            matching_candidates = [
                h for h in candidates
                if h.is_defense_hypothesis or pat in h.title.lower()
            ]
            if matching_candidates:
                non_matching = [h for h in candidates if h not in matching_candidates]
                for r in non_matching:
                    rejected_list.append({
                        "hypothesis_id": r.hypothesis_id,
                        "title": r.title,
                        "net_support_score": r.net_support_score,
                        "raw_support_score": r.raw_support_score,
                        "rejection_reason": f"Hypothesis pattern does not match target query pattern '{target_pattern}'. Higher-confidence anomalies in other pattern categories were not selected because the investigation objective was specifically to identify '{target_pattern}' patterns.",
                    })
                candidates = matching_candidates

        # Sort hypotheses by net_support_score descending, then raw_support_score descending
        ranked = sorted(
            candidates,
            key=lambda h: (h.net_support_score, h.raw_support_score),
            reverse=True,
        )

        winner = ranked[0]
        runner_up = ranked[1] if len(ranked) > 1 else None
        confidence_gap = round(winner.net_support_score - (runner_up.net_support_score if runner_up else 0.0), 4)

        # Format remaining rejected hypotheses list with explicit rejection reasons
        for r in ranked[1:]:
            reason = f"Lower net support score ({r.net_support_score:.2f} vs winner {winner.net_support_score:.2f})"
            if r.opposing_score > 0.30:
                reason += f" with higher opposing evidence penalty ({r.opposing_score:.2f})"
            rejected_list.append({
                "hypothesis_id": r.hypothesis_id,
                "title": r.title,
                "net_support_score": r.net_support_score,
                "raw_support_score": r.raw_support_score,
                "rejection_reason": reason,
            })

        # Apply deterministic Consensus Rules
        category = INCONCLUSIVE
        rejection_reason = ""

        prosecution_candidates = [h for h in ranked if not h.is_defense_hypothesis]
        defense_candidates = [h for h in ranked if h.is_defense_hypothesis]

        top_prosecution = prosecution_candidates[0] if prosecution_candidates else None
        top_defense = defense_candidates[0] if defense_candidates else None

        # Rule 1: Strong defense evidence dominates
        if winner.is_defense_hypothesis and winner.net_support_score >= 0.40 and winner.raw_support_score >= 0.60:
            category = LIKELY_LEGITIMATE
            rejection_reason = "Alternative legitimate business activity hypothesis supported by defense evidence"

        # Rule 2: Balanced competing evidence or weak support -> INCONCLUSIVE
        elif winner.net_support_score < 0.35:
            category = INCONCLUSIVE
            rejection_reason = f"Winning net support score ({winner.net_support_score:.2f}) below minimum threshold (0.35)"

        elif top_prosecution and top_defense and abs(top_prosecution.net_support_score - top_defense.net_support_score) < 0.10:
            category = INCONCLUSIVE
            rejection_reason = f"Balanced competing prosecution vs defense evidence (gap: {confidence_gap:.2f})"

        # Rule 3: Malicious prosecution hypotheses
        elif not winner.is_defense_hypothesis:
            valid_experts = [e for e in winner.expert_sources if e not in ("defense", "system")]
            if len(valid_experts) >= 2 and winner.net_support_score >= 0.60:
                category = LIKELY_MALICIOUS
            elif winner.net_support_score >= 0.45:
                category = POSSIBLY_MALICIOUS
            else:
                category = INCONCLUSIVE
                rejection_reason = "Insufficient net evidence strength to confirm malicious classification"

        return ConsensusResult(
            consensus_category=category,
            winning_hypothesis=winner,
            runner_up_hypothesis=runner_up,
            confidence_gap=confidence_gap,
            ranked_hypotheses=ranked,
            rejected_hypotheses=rejected_list,
            rejection_reason=rejection_reason,
        )

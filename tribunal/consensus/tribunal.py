"""Tribunal — Core Consensus & Deliberation Engine (Phase C.6)."""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

from tribunal.consensus.confidence_calibrator import ConfidenceCalibrator
from tribunal.consensus.consensus_engine import ConsensusEngine
from tribunal.consensus.contradiction_resolver import ContradictionResolver
from tribunal.consensus.deliberation_trace import DeliberationTrace
from tribunal.consensus.evidence_weigher import EvidenceWeigher
from tribunal.consensus.hypothesis_extractor import HypothesisExtractor
from tribunal.consensus.verdict_builder import VerdictBuilder

if TYPE_CHECKING:
    from tribunal.models.case_file import CaseFile
    from tribunal.models.evidence_graph import EvidenceGraph
    from tribunal.models.tribunal_verdict import TribunalVerdict

logger = logging.getLogger("tribunal.consensus.tribunal")


class Tribunal:
    """Performs explainable multi-hypothesis deliberation over the augmented Evidence Graph.
    
    Public Interface:
        deliberate(evidence_graph, case_file) -> TribunalVerdict
    """

    def __init__(self) -> None:
        self.hypothesis_extractor = HypothesisExtractor()
        self.evidence_weigher = EvidenceWeigher()
        self.contradiction_resolver = ContradictionResolver()
        self.consensus_engine = ConsensusEngine()
        self.confidence_calibrator = ConfidenceCalibrator()
        self.verdict_builder = VerdictBuilder()

    def deliberate(
        self,
        evidence_graph: EvidenceGraph,
        case_file: CaseFile,
    ) -> TribunalVerdict:
        """Perform 6-stage deterministic deliberation and issue final TribunalVerdict."""
        logger.info("Executing Phase C.6 Tribunal Deliberation Engine...")
        trace = DeliberationTrace()

        # Stage 1: Hypothesis Extraction
        t0 = time.perf_counter()
        extracted = self.hypothesis_extractor.extract(evidence_graph)
        dur1 = (time.perf_counter() - t0) * 1000.0
        trace.add_step(
            stage_name="Hypothesis Extraction",
            description=f"Extracted {len(extracted)} candidate hypotheses from EvidenceGraph.",
            data={"extracted_count": len(extracted), "titles": [h.title for h in extracted]},
            step_duration_ms=dur1,
        )

        # Stage 2: Evidence Weighing
        t0 = time.perf_counter()
        weighted_scores = self.evidence_weigher.weigh(extracted, evidence_graph)
        dur2 = (time.perf_counter() - t0) * 1000.0
        trace.add_step(
            stage_name="Evidence Weighing",
            description=f"Calculated raw support scores across {len(weighted_scores)} hypotheses.",
            data={"weighted_scores": [{s.title: s.raw_support_score} for s in weighted_scores]},
            step_duration_ms=dur2,
        )

        # Stage 3: Contradiction Resolution
        t0 = time.perf_counter()
        resolved_scores = self.contradiction_resolver.resolve(weighted_scores, extracted, evidence_graph)
        dur3 = (time.perf_counter() - t0) * 1000.0
        trace.add_step(
            stage_name="Contradiction Resolution",
            description="Evaluated opposing evidence penalties and calculated Net Evidence Strength.",
            data={"resolved_scores": [{r.title: r.net_support_score} for r in resolved_scores]},
            step_duration_ms=dur3,
        )

        # Stage 4: Consensus Engine
        t0 = time.perf_counter()
        consensus_res = self.consensus_engine.evaluate(resolved_scores)
        dur4 = (time.perf_counter() - t0) * 1000.0
        trace.add_step(
            stage_name="Consensus Formation",
            description=f"Ranked competing hypotheses and formed consensus category '{consensus_res.consensus_category}'.",
            data={
                "consensus_category": consensus_res.consensus_category,
                "winner": consensus_res.winning_hypothesis.title,
                "confidence_gap": consensus_res.confidence_gap,
            },
            step_duration_ms=dur4,
        )

        # Stage 5: Confidence Calibration
        t0 = time.perf_counter()
        calibrated_conf = self.confidence_calibrator.calibrate(consensus_res, evidence_graph)
        dur5 = (time.perf_counter() - t0) * 1000.0
        trace.add_step(
            stage_name="Confidence Calibration",
            description=f"Calibrated final Tribunal confidence score to {calibrated_conf:.4f}.",
            data={"calibrated_confidence": calibrated_conf},
            step_duration_ms=dur5,
        )

        # Stage 6: Verdict Building
        t0 = time.perf_counter()
        verdict = self.verdict_builder.build_verdict(
            consensus_result=consensus_res,
            calibrated_confidence=calibrated_conf,
            deliberation_trace=trace,
            graph=evidence_graph,
            case_file=case_file,
        )
        dur6 = (time.perf_counter() - t0) * 1000.0
        trace.add_step(
            stage_name="Verdict Output",
            description=f"Issued final TribunalVerdict: '{verdict.verdict}' (Confidence: {verdict.confidence:.2f}).",
            data={"verdict": verdict.verdict, "winning_hypothesis": verdict.winning_hypothesis},
            step_duration_ms=dur6,
        )

        logger.info(f"Tribunal Deliberation Completed: {verdict.verdict} ({verdict.winning_hypothesis})")
        return verdict

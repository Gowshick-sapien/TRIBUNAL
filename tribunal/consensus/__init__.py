"""Tribunal Consensus & Deliberation Engine package (Phase C.6)."""

from tribunal.consensus.confidence_calibrator import ConfidenceCalibrator
from tribunal.consensus.consensus_engine import (
    INCONCLUSIVE,
    LIKELY_LEGITIMATE,
    LIKELY_MALICIOUS,
    POSSIBLY_MALICIOUS,
    ConsensusEngine,
    ConsensusResult,
)
from tribunal.consensus.contradiction_resolver import ContradictionResolver, ResolvedHypothesis
from tribunal.consensus.deliberation_trace import DeliberationTrace, TraceStep
from tribunal.consensus.evidence_weigher import EvidenceWeigher, HypothesisScore
from tribunal.consensus.hypothesis_extractor import ExtractedHypothesis, HypothesisExtractor
from tribunal.consensus.tribunal import Tribunal
from tribunal.consensus.verdict_builder import VerdictBuilder

__all__ = [
    "Tribunal",
    "HypothesisExtractor",
    "ExtractedHypothesis",
    "EvidenceWeigher",
    "HypothesisScore",
    "ContradictionResolver",
    "ResolvedHypothesis",
    "ConsensusEngine",
    "ConsensusResult",
    "ConfidenceCalibrator",
    "VerdictBuilder",
    "DeliberationTrace",
    "TraceStep",
    "LIKELY_MALICIOUS",
    "POSSIBLY_MALICIOUS",
    "INCONCLUSIVE",
    "LIKELY_LEGITIMATE",
]

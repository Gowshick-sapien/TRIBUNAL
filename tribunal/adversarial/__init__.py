"""Adversarial Review Engine package (Phase C.5)."""

from tribunal.adversarial.alternative_hypothesis_generator import (
    AlternativeExplanation,
    AlternativeHypothesis,
    AlternativeHypothesisGenerator,
)
from tribunal.adversarial.confidence_adjuster import ConfidenceAdjuster
from tribunal.adversarial.contradiction_detector import (
    ContradictionDetector,
    ContradictionFinding,
)
from tribunal.adversarial.defense_agent import DefenseAgent
from tribunal.adversarial.evidence_reviewer import EvidenceReviewer, ReviewContext
from tribunal.adversarial.evidence_strength_analyzer import (
    EvidenceStrengthAnalyzer,
    EvidenceStrengthScore,
)
from tribunal.adversarial.rebuttal_builder import RebuttalBuilder
from tribunal.adversarial.uncertainty_estimator import (
    UncertaintyEstimator,
    UncertaintyScore,
)

__all__ = [
    "DefenseAgent",
    "EvidenceReviewer",
    "ReviewContext",
    "ContradictionDetector",
    "ContradictionFinding",
    "AlternativeHypothesisGenerator",
    "AlternativeHypothesis",
    "AlternativeExplanation",
    "EvidenceStrengthAnalyzer",
    "EvidenceStrengthScore",
    "UncertaintyEstimator",
    "UncertaintyScore",
    "RebuttalBuilder",
    "ConfidenceAdjuster",
]

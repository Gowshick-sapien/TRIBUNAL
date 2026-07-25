"""Official shared PatternFinding and MetricEvidence domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MetricEvidence:
    """Standardized quantitative metric evidence produced by detection modules."""
    name: str
    value: float
    threshold: float | None = None
    comparison: str | None = None  # e.g., ">=", ">", "==", "ratio", "pct"

    def to_dict(self) -> dict[str, Any]:
        """Serialize metric evidence."""
        return {
            "name": self.name,
            "value": self.value,
            "threshold": self.threshold,
            "comparison": self.comparison,
        }


@dataclass
class PatternFinding:
    """Official shared intermediate finding produced by all expert detection modules."""
    pattern_name: str
    score: float
    supporting_features: list[str]
    affected_accounts: list[str]
    evidence_details: list[str]
    detector_name: str = "generic_detector"
    detector_version: str = "1.0"
    supporting_metrics: dict[str, float] = field(default_factory=dict)
    metric_evidence: list[MetricEvidence] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)
    transaction_ids: list[str] = field(default_factory=list)
    time_window: Any = None

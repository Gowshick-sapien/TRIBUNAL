"""Anomaly detection result contract."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AnomalyResult:
    """Statistical outlier detection output — see docs/Data_Contracts.md §8.2."""

    method: str
    outlier_count: int
    outlier_txn_ids: list[str]
    outlier_scores: dict[str, float]
    overall_anomaly_score: float

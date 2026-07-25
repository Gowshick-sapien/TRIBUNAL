"""Anomaly Detection — interface only."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pandas as pd

    from tribunal.tools.anomaly_result import AnomalyResult


class AnomalyDetection:
    """Applies statistical outlier detection to transaction amounts."""

    def detect(
        self,
        transactions: pd.DataFrame,
        features: dict[str, Any],
    ) -> AnomalyResult:
        """Return outlier flags, scores, and aggregate anomaly score."""
        ...

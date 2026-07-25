"""Feature Engineering — interface only."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pandas as pd


class FeatureEngineering:
    """Computes AML-relevant derived features from transaction data."""

    def compute_features(
        self,
        transactions: pd.DataFrame,
        customer_id: str,
        window_days: int,
    ) -> dict[str, Any]:
        """Return feature dictionary per Data_Contracts FeatureDictionary."""
        ...

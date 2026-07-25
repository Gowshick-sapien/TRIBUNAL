"""EDA Tool — interface only."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pandas as pd


class EDATool:
    """Generates statistical profile for broad/exploratory queries."""

    def profile(
        self,
        transactions: pd.DataFrame,
        filters: dict[str, Any],
    ) -> dict[str, Any]:
        """Return EDA summary dictionary."""
        ...

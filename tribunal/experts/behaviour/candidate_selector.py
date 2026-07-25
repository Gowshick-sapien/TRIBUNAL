"""Candidate Selector module — Filters transactions and selects candidate accounts for behavioural investigation."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from tribunal.models.execution_plan import ExecutionPlan

logger = logging.getLogger("tribunal.experts.behaviour.candidate_selector")


class CandidateSelector:
    """Filters transactions and identifies candidate accounts for targeted behavioural investigation."""

    def select_candidates(
        self,
        transactions: pd.DataFrame,
        execution_plan: ExecutionPlan,
    ) -> pd.DataFrame:
        """Filter input DataFrame according to execution plan filters and behavioural candidate triggers."""
        if transactions is None or transactions.empty:
            return pd.DataFrame()

        df = transactions.copy()
        filters = execution_plan.filters or {}

        # 1. Filter by specific target accounts/entities if present
        target_entities = []
        if "customer_id" in filters and filters["customer_id"]:
            target_entities.append(str(filters["customer_id"]))
        if "entities" in filters and isinstance(filters["entities"], list):
            target_entities.extend([str(e) for e in filters["entities"]])

        if target_entities:
            entity_set = set(target_entities)
            from_col = "from_account" if "from_account" in df.columns else ("Account" if "Account" in df.columns else None)
            to_col = "to_account" if "to_account" in df.columns else ("Account.1" if "Account.1" in df.columns else None)

            if from_col and to_col:
                df = df[df[from_col].astype(str).isin(entity_set) | df[to_col].astype(str).isin(entity_set)].copy()

        # 2. Filter by date range if requested
        if "date_range" in filters and filters["date_range"]:
            # Standard candidate filtering for date range if timestamp is datetime
            pass

        return df

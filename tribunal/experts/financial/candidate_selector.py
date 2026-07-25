"""Candidate Selector module — Filters transactions and selects candidate accounts for investigation."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from tribunal.models.execution_plan import ExecutionPlan

logger = logging.getLogger("tribunal.experts.financial.candidate_selector")


class CandidateSelector:
    """Filters transactions and identifies candidate accounts for targeted investigation."""

    def select_candidates(
        self,
        transactions: pd.DataFrame,
        execution_plan: ExecutionPlan,
    ) -> pd.DataFrame:
        """Filter input DataFrame according to execution plan filters and candidate triggers."""
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

        # 2. Filter by currency if requested
        if "currency" in filters and filters["currency"]:
            curr = str(filters["currency"]).upper()
            if "receiving_currency" in df.columns:
                df = df[df["receiving_currency"].astype(str).str.upper() == curr]

        # 3. Filter by payment format if requested
        if "payment_format" in filters and filters["payment_format"]:
            fmt = str(filters["payment_format"]).lower()
            if "payment_format" in df.columns:
                df = df[df["payment_format"].astype(str).str.lower() == fmt]

        # 4. If no target entity filter was specified, filter for active/candidate accounts
        if not target_entities:
            # Focus on transactions with amounts > 0 or elevated threshold proximity
            amount_col = "amount_received" if "amount_received" in df.columns else ("Amount Received" if "Amount Received" in df.columns else None)
            if amount_col:
                df = df[df[amount_col] > 0]

        return df

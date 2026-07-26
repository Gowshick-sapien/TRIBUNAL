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
            entity_set = set()
            for entity in target_entities:
                s = str(entity).strip()
                entity_set.add(s)
                if s.upper().startswith("ACC_"):
                    entity_set.add(s[4:])
                elif s.upper().startswith("ACC"):
                    entity_set.add(s[3:])
                elif s.upper().startswith("ACCOUNT_"):
                    entity_set.add(s[8:])

            from_col = "from_account" if "from_account" in df.columns else ("Account" if "Account" in df.columns else None)
            to_col = "to_account" if "to_account" in df.columns else ("Account.1" if "Account.1" in df.columns else None)

            if from_col and to_col:
                matched_df = df[
                    df[from_col].astype(str).isin(entity_set) | df[to_col].astype(str).isin(entity_set)
                ].copy()

                df = matched_df

        # 2. Filter by currency if requested
        if "currency" in filters and filters["currency"]:
            curr = str(filters["currency"]).upper()
            if "receiving_currency" in df.columns:
                curr_df = df[df["receiving_currency"].astype(str).str.upper() == curr]
                if not curr_df.empty:
                    df = curr_df

        # 3. Filter by payment format if requested
        if "payment_format" in filters and filters["payment_format"]:
            fmt = str(filters["payment_format"]).lower()
            if "payment_format" in df.columns:
                fmt_df = df[df["payment_format"].astype(str).str.lower() == fmt]
                if not fmt_df.empty:
                    df = fmt_df

        # 4. Filter active transactions
        amount_col = "amount_received" if "amount_received" in df.columns else ("Amount Received" if "Amount Received" in df.columns else None)
        if amount_col:
            active_df = df[df[amount_col] > 0]
            if not active_df.empty:
                df = active_df

        acct_col = "from_account" if "from_account" in df.columns else ("Account" if "Account" in df.columns else None)
        candidate_accounts = df[acct_col].unique() if acct_col else []
        print("=" * 80)
        print("Candidate Selector (Financial)")
        print("Planner Entities:", target_entities)
        print("Candidates:", candidate_accounts)
        print("=" * 80)

        return df

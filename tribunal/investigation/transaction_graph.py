"""Transaction Graph Engine for TRIBUNAL.

Builds NetworkX transaction graph over accounts and money transfers BEFORE feature engineering,
providing reusable graph-derived features: fan-in, fan-out, degree, repeated counterparties,
and neighbourhood size.
"""

import logging
from typing import Any, Dict, List, Set
import networkx as nx
import pandas as pd

logger = logging.getLogger("tribunal.investigation.transaction_graph")


class TransactionGraph:
    """NetworkX-backed Directed Graph representing account transactions.
    
    Constructed directly from transaction records, enabling graph topology analysis
    and graph-derived feature extraction.
    """

    def __init__(self):
        self.graph = nx.DiGraph()

    def build_from_dataframe(self, df: pd.DataFrame) -> "TransactionGraph":
        """Build directed transaction graph from transactions DataFrame.
        
        Args:
            df: DataFrame containing from_account, to_account, amount_paid/amount_received, timestamp
        """
        logger.info(f"Building Transaction Graph from {len(df)} transactions...")
        self.graph.clear()

        # Handle column naming flexibility
        from_col = "from_account" if "from_account" in df.columns else "Account"
        to_col = "to_account" if "to_account" in df.columns else "Account.1"
        amt_col = "amount_paid" if "amount_paid" in df.columns else ("Amount Paid" if "Amount Paid" in df.columns else "amount_received")
        ts_col = "timestamp" if "timestamp" in df.columns else "Timestamp"
        fmt_col = "payment_format" if "payment_format" in df.columns else "Payment Format"

        for _, row in df.iterrows():
            u = str(row[from_col])
            v = str(row[to_col])
            amt = float(row[amt_col]) if pd.notna(row[amt_col]) else 0.0
            ts = row[ts_col]
            fmt = str(row[fmt_col]) if fmt_col in df.columns and pd.notna(row[fmt_col]) else "unknown"

            # Add nodes
            if not self.graph.has_node(u):
                self.graph.add_node(u)
            if not self.graph.has_node(v):
                self.graph.add_node(v)

            # Update edge properties
            if self.graph.has_edge(u, v):
                edge = self.graph[u][v]
                edge["transaction_count"] += 1
                edge["total_amount"] += amt
                edge["max_amount"] = max(edge["max_amount"], amt)
                edge["min_amount"] = min(edge["min_amount"], amt)
                edge["formats"].add(fmt)
            else:
                self.graph.add_edge(
                    u, v,
                    transaction_count=1,
                    total_amount=amt,
                    max_amount=amt,
                    min_amount=amt,
                    formats={fmt},
                )

        logger.info(
            f"Transaction Graph built: {self.graph.number_of_nodes()} nodes, "
            f"{self.graph.number_of_edges()} edges"
        )
        return self

    def get_fan_in(self, account_id: str) -> int:
        """Calculate in-degree (unique incoming senders)."""
        account_id = str(account_id)
        if not self.graph.has_node(account_id):
            return 0
        return self.graph.in_degree(account_id)

    def get_fan_out(self, account_id: str) -> int:
        """Calculate out-degree (unique outgoing receivers)."""
        account_id = str(account_id)
        if not self.graph.has_node(account_id):
            return 0
        return self.graph.out_degree(account_id)

    def get_degree(self, account_id: str) -> int:
        """Calculate total unique counterparties (fan_in + fan_out)."""
        account_id = str(account_id)
        if not self.graph.has_node(account_id):
            return 0
        return self.graph.degree(account_id)

    def get_repeated_counterparties(self, account_id: str, min_txns: int = 2) -> List[str]:
        """Find counterparties with transaction count >= min_txns."""
        account_id = str(account_id)
        if not self.graph.has_node(account_id):
            return []

        repeated = []
        # Check outgoing
        for _, nbr, data in self.graph.out_edges(account_id, data=True):
            if data.get("transaction_count", 0) >= min_txns:
                repeated.append(nbr)
        # Check incoming
        for nbr, _, data in self.graph.in_edges(account_id, data=True):
            if data.get("transaction_count", 0) >= min_txns and nbr not in repeated:
                repeated.append(nbr)

        return repeated

    def get_neighbourhood_size(self, account_id: str, max_hops: int = 2) -> int:
        """Calculate number of reachable account nodes within max_hops."""
        account_id = str(account_id)
        if not self.graph.has_node(account_id):
            return 0

        visited: Set[str] = {account_id}
        current_layer: Set[str] = {account_id}

        for _ in range(max_hops):
            next_layer: Set[str] = set()
            for node in current_layer:
                # Add successors (outgoing) and predecessors (incoming)
                neighbors = set(self.graph.successors(node)).union(set(self.graph.predecessors(node)))
                for nbr in neighbors:
                    if nbr not in visited:
                        visited.add(nbr)
                        next_layer.add(nbr)
            current_layer = next_layer
            if not current_layer:
                break

        return len(visited) - 1  # Exclude self

    def get_account_graph_metrics(self, account_id: str) -> Dict[str, Any]:
        """Extract all graph-derived features for a given account."""
        account_id = str(account_id)
        return {
            "fan_in": self.get_fan_in(account_id),
            "fan_out": self.get_fan_out(account_id),
            "total_degree": self.get_degree(account_id),
            "repeated_counterparties_count": len(self.get_repeated_counterparties(account_id)),
            "neighbourhood_size_2hop": self.get_neighbourhood_size(account_id, max_hops=2),
        }

"""Transaction Network Builder for TRIBUNAL (Stage 2.1).

Constructs an in-memory NetworkX MultiDiGraph representing the full transaction
network from transactions.parquet and accounts.parquet.

Extracted features, metrics, and structural properties are persisted to disk
for instant zero-overhead runtime loading.
"""

import json
import logging
import pickle
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import networkx as nx
import numpy as np
import pandas as pd

from tribunal.data.loader import DataLoader

logger = logging.getLogger("tribunal.investigation.transaction_network_builder")


class TransactionNetworkBuilder:
    """Builder, validator, and manager for the transaction network MultiDiGraph.
    
    Serves as the structural foundation for graph-derived features and network analytics.
    Constructs an nx.MultiDiGraph where:
    - Nodes represent bank accounts
    - Edges represent individual transactions
    """

    def __init__(self, dataset_dir: Union[str, Path] = "datasets"):
        self.dataset_dir = Path(dataset_dir)
        self.processed_dir = self.dataset_dir / "processed"
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        self.loader = DataLoader(self.dataset_dir)
        self.graph: Optional[nx.MultiDiGraph] = None

    def build(
        self,
        transactions_df: Optional[pd.DataFrame] = None,
        accounts_df: Optional[pd.DataFrame] = None,
    ) -> nx.MultiDiGraph:
        """Build nx.MultiDiGraph from transactions and accounts DataFrames.
        
        Args:
            transactions_df: Optional DataFrame of transactions (loaded if None)
            accounts_df: Optional DataFrame of account metadata (loaded if None)

        Returns:
            Constructed nx.MultiDiGraph
        """
        if transactions_df is None:
            logger.info("Loading transactions dataset for graph construction...")
            transactions_df = self.loader.load_transactions(as_dataclasses=False)
        
        if accounts_df is None:
            logger.info("Loading accounts dataset for metadata attachment...")
            try:
                accounts_df = self.loader.load_accounts(as_dataclasses=False)
            except FileNotFoundError:
                logger.warning("Accounts dataset not found. Proceeding with transaction nodes only.")
                accounts_df = None

        logger.info(f"Building MultiDiGraph from {len(transactions_df)} transaction records...")
        G = nx.MultiDiGraph()

        # 1. Populate Account Metadata Nodes if available
        account_meta_map: Dict[str, Dict[str, str]] = {}
        if accounts_df is not None and not accounts_df.empty:
            acc_no_col = "account_number" if "account_number" in accounts_df.columns else "Account Number"
            bank_id_col = "bank_id" if "bank_id" in accounts_df.columns else "Bank ID"
            bank_name_col = "bank_name" if "bank_name" in accounts_df.columns else "Bank Name"
            ent_id_col = "entity_id" if "entity_id" in accounts_df.columns else "Entity ID"
            ent_name_col = "entity_name" if "entity_name" in accounts_df.columns else "Entity Name"

            for row in accounts_df.itertuples(index=False):
                acc_num = str(getattr(row, acc_no_col))
                account_meta_map[acc_num] = {
                    "account_id": acc_num,
                    "bank_id": str(getattr(row, bank_id_col, "")),
                    "bank_name": str(getattr(row, bank_name_col, "")),
                    "entity_id": str(getattr(row, ent_id_col, "")),
                    "entity_name": str(getattr(row, ent_name_col, "")),
                }

        # 2. Extract column names from transactions_df
        from_acc_col = "from_account" if "from_account" in transactions_df.columns else "Account"
        to_acc_col = "to_account" if "to_account" in transactions_df.columns else "Account.1"
        from_bank_col = "from_bank" if "from_bank" in transactions_df.columns else "From Bank"
        to_bank_col = "to_bank" if "to_bank" in transactions_df.columns else "To Bank"
        amt_paid_col = "amount_paid" if "amount_paid" in transactions_df.columns else "Amount Paid"
        amt_rec_col = "amount_received" if "amount_received" in transactions_df.columns else "Amount Received"
        pay_curr_col = "payment_currency" if "payment_currency" in transactions_df.columns else "Payment Currency"
        rec_curr_col = "receiving_currency" if "receiving_currency" in transactions_df.columns else "Receiving Currency"
        fmt_col = "payment_format" if "payment_format" in transactions_df.columns else "Payment Format"
        ts_col = "timestamp" if "timestamp" in transactions_df.columns else "Timestamp"
        label_col = "is_laundering" if "is_laundering" in transactions_df.columns else "Is Laundering"
        id_col = "transaction_id" if "transaction_id" in transactions_df.columns else None

        # 3. Add Edges and Nodes using high-performance tuple iteration
        logger.info("Processing transaction rows into graph edges...")
        
        # Pre-ensure node existence for fast batch addition
        all_unique_accounts = set(transactions_df[from_acc_col].astype(str)).union(
            set(transactions_df[to_acc_col].astype(str))
        )
        
        for acc in all_unique_accounts:
            meta = account_meta_map.get(acc, {
                "account_id": acc,
                "bank_id": "",
                "bank_name": "",
                "entity_id": "",
                "entity_name": "",
            })
            G.add_node(acc, **meta)

        # Iterate rows for edges
        for idx, row in enumerate(transactions_df.itertuples(index=False)):
            u = str(getattr(row, from_acc_col))
            v = str(getattr(row, to_acc_col))
            
            f_bank = str(getattr(row, from_bank_col, ""))
            t_bank = str(getattr(row, to_bank_col, ""))

            # Update bank_id on nodes if missing from account metadata
            if f_bank and not G.nodes[u].get("bank_id"):
                G.nodes[u]["bank_id"] = f_bank
            if t_bank and not G.nodes[v].get("bank_id"):
                G.nodes[v]["bank_id"] = t_bank

            txn_id = str(getattr(row, id_col)) if id_col and hasattr(row, id_col) else f"txn_{idx+1:07d}"
            ts = str(getattr(row, ts_col))
            amt_paid = float(getattr(row, amt_paid_col, 0.0))
            amt_rec = float(getattr(row, amt_rec_col, 0.0))
            p_curr = str(getattr(row, pay_curr_col, ""))
            r_curr = str(getattr(row, rec_curr_col, ""))
            fmt = str(getattr(row, fmt_col, ""))
            lbl = int(getattr(row, label_col, 0))

            G.add_edge(
                u,
                v,
                transaction_id=txn_id,
                timestamp=ts,
                amount_paid=amt_paid,
                amount_received=amt_rec,
                payment_currency=p_curr,
                receiving_currency=r_curr,
                payment_format=fmt,
                from_bank=f_bank,
                to_bank=t_bank,
                label=lbl,  # Retained for evaluation only
            )

        # 4. Attach pre-computed degree metrics to node attributes
        logger.info("Computing node-level summary degree metrics...")
        for node in G.nodes():
            in_deg = G.in_degree(node)
            out_deg = G.out_degree(node)
            G.nodes[node]["in_degree"] = in_deg
            G.nodes[node]["out_degree"] = out_deg
            G.nodes[node]["transaction_count"] = in_deg + out_deg

        self.graph = G
        logger.info(
            f"Transaction MultiDiGraph build complete: {G.number_of_nodes()} nodes, "
            f"{G.number_of_edges()} edges."
        )
        return G

    def save(self, path: Optional[Union[str, Path]] = None) -> Path:
        """Persist constructed MultiDiGraph to disk.
        
        Args:
            path: Target file path (defaults to datasets/processed/transaction_network.gpickle)

        Returns:
            Path object of written file
        """
        if self.graph is None:
            raise ValueError("Graph has not been built or loaded yet. Call build() first.")

        if path is None:
            target_path = self.processed_dir / "transaction_network.gpickle"
        else:
            target_path = Path(path)

        target_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Saving transaction network graph to {target_path}...")
        
        with open(target_path, "wb") as f:
            pickle.dump(self.graph, f, protocol=pickle.HIGHEST_PROTOCOL)

        logger.info(f"Successfully saved {target_path} ({target_path.stat().st_size / (1024*1024):.2f} MB)")
        return target_path

    def load(self, path: Optional[Union[str, Path]] = None) -> nx.MultiDiGraph:
        """Load persisted MultiDiGraph from disk instantly.
        
        Args:
            path: Target file path (defaults to datasets/processed/transaction_network.gpickle)

        Returns:
            Loaded nx.MultiDiGraph
        """
        if path is None:
            candidates = [
                self.processed_dir / "transaction_network.gpickle",
                self.processed_dir / "transaction_network.pkl",
                self.dataset_dir / "transaction_network.gpickle",
            ]
            target_path = None
            for p in candidates:
                if p.exists():
                    target_path = p
                    break
            if target_path is None:
                raise FileNotFoundError(
                    f"No persisted transaction network graph found in {self.processed_dir}"
                )
        else:
            target_path = Path(path)

        logger.info(f"Loading transaction network graph from {target_path}...")
        with open(target_path, "rb") as f:
            self.graph = pickle.load(f)

        logger.info(
            f"Successfully loaded graph: {self.graph.number_of_nodes()} nodes, "
            f"{self.graph.number_of_edges()} edges."
        )
        return self.graph

    def validate(self) -> Dict[str, Any]:
        """Validate structural integrity of constructed MultiDiGraph."""
        if self.graph is None:
            raise ValueError("Graph has not been built or loaded yet.")

        logger.info("Validating Transaction Network MultiDiGraph...")

        report: Dict[str, Any] = {
            "node_count": self.graph.number_of_nodes(),
            "edge_count": self.graph.number_of_edges(),
            "checks": {},
            "issues": [],
            "status": "PASSED",
        }

        # Check 1: No malformed/null nodes
        null_nodes = [n for n in self.graph.nodes() if n is None or str(n) == "nan" or str(n) == "None" or not str(n).strip()]
        report["checks"]["no_null_nodes"] = {
            "passed": len(null_nodes) == 0,
            "null_node_count": len(null_nodes),
        }
        if null_nodes:
            report["issues"].append(f"Found {len(null_nodes)} null or empty node IDs.")

        # Check 2: Node attribute completeness
        missing_acc_id = sum(1 for n, d in self.graph.nodes(data=True) if "account_id" not in d)
        report["checks"]["node_attributes_complete"] = {
            "passed": missing_acc_id == 0,
            "missing_account_id_count": missing_acc_id,
        }

        # Check 3: Edge attribute completeness
        sample_edges = list(self.graph.edges(data=True))[:1000]
        missing_attrs = 0
        required_edge_attrs = {"amount_paid", "payment_format", "timestamp", "from_bank", "to_bank"}
        for u, v, d in sample_edges:
            if not required_edge_attrs.issubset(d.keys()):
                missing_attrs += 1
        
        report["checks"]["edge_attributes_valid"] = {
            "passed": missing_attrs == 0,
            "sample_missing_attrs_count": missing_attrs,
        }

        # Status assignment
        all_passed = all(chk["passed"] for chk in report["checks"].values())
        report["status"] = "PASSED" if all_passed else "FAILED_WITH_ISSUES"

        report_path = self.processed_dir / "network_validation_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        logger.info(f"Network Validation Report saved to {report_path}")
        return report

    def get_network_statistics(self) -> Dict[str, Any]:
        """Compute network statistics and persist network_profile.json."""
        if self.graph is None:
            raise ValueError("Graph has not been built or loaded yet.")

        logger.info("Computing Transaction Network Statistics...")

        total_nodes = self.graph.number_of_nodes()
        total_edges = self.graph.number_of_edges()

        # Component analysis (on underlying directed graph)
        weak_components = list(nx.weakly_connected_components(self.graph))
        strong_components = list(nx.strongly_connected_components(self.graph))
        largest_weak_comp_size = max(len(c) for c in weak_components) if weak_components else 0
        largest_strong_comp_size = max(len(c) for c in strong_components) if strong_components else 0

        # Degree calculations
        in_degrees = [d for n, d in self.graph.in_degree()]
        out_degrees = [d for n, d in self.graph.out_degree()]
        
        max_in_deg_node = max(self.graph.nodes(), key=lambda n: self.graph.in_degree(n)) if total_nodes > 0 else None
        max_out_deg_node = max(self.graph.nodes(), key=lambda n: self.graph.out_degree(n)) if total_nodes > 0 else None

        avg_degree = (2.0 * total_edges / total_nodes) if total_nodes > 0 else 0.0
        
        # Multi-edge / repeated transaction count
        # Count node pairs (u, v) that have > 1 edge between them
        pair_counts: Dict[Tuple[str, str], int] = {}
        for u, v in self.graph.edges():
            pair_counts[(u, v)] = pair_counts.get((u, v), 0) + 1
        repeated_pairs_count = sum(1 for count in pair_counts.values() if count > 1)

        # Self-loops
        self_loops_count = nx.number_of_selfloops(self.graph)

        # Network density (for MultiDiGraph: E / (V * (V - 1)))
        density = (total_edges / (total_nodes * (total_nodes - 1))) if total_nodes > 1 else 0.0

        stats: Dict[str, Any] = {
            "total_nodes": total_nodes,
            "total_edges": total_edges,
            "weakly_connected_components_count": len(weak_components),
            "strongly_connected_components_count": len(strong_components),
            "largest_weak_component_size": largest_weak_comp_size,
            "largest_strong_component_size": largest_strong_comp_size,
            "average_degree": float(avg_degree),
            "max_in_degree": {
                "account_id": max_in_deg_node,
                "in_degree": int(max(in_degrees)) if in_degrees else 0,
            },
            "max_out_degree": {
                "account_id": max_out_deg_node,
                "out_degree": int(max(out_degrees)) if out_degrees else 0,
            },
            "network_density": float(density),
            "self_loops_count": int(self_loops_count),
            "repeated_transaction_pairs_count": int(repeated_pairs_count),
        }

        output_file = self.processed_dir / "network_profile.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)

        logger.info(f"Network Statistics written to {output_file}")
        return stats

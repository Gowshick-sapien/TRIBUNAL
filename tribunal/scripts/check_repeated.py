import sys
from pathlib import Path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from tribunal.investigation.transaction_network_builder import TransactionNetworkBuilder

builder = TransactionNetworkBuilder(root_dir / "tribunal" / "datasets")
graph = builder.load()

print("--- Self-loop Repeated Pair (u == v) ---")
for u, v in graph.edges():
    if u == v:
        edges = graph.get_edge_data(u, v)
        if len(edges) > 1:
            print(f"Self-loop pair: {u} -> {v} ({len(edges)} transactions)")
            for k, attrs in list(edges.items())[:3]:
                print(f"  Edge Key {k}: txn_id={attrs['transaction_id']}, timestamp={attrs['timestamp']}, amount=${attrs['amount_paid']}, format={attrs['payment_format']}")
            break

print("\n--- Distinct Accounts Repeated Pair (u != v) ---")
for u, v in graph.edges():
    if u != v:
        edges = graph.get_edge_data(u, v)
        if len(edges) > 1:
            print(f"Distinct pair: {u} -> {v} ({len(edges)} transactions)")
            for k, attrs in list(edges.items())[:3]:
                print(f"  Edge Key {k}: txn_id={attrs['transaction_id']}, timestamp={attrs['timestamp']}, amount=${attrs['amount_paid']}, format={attrs['payment_format']}")
            break

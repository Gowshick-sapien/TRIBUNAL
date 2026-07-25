# Phase B.4 — Transaction Network Builder: Manual Verification Plan

**Document Classification:** Verification & Testing Specification  
**Phase:** B.4 (Transaction Network Builder)  
**Target System:** TRIBUNAL — Core Engine  
**Version:** 1.0  

---

## 1. Overview & Purpose

This document specifies the **Manual & Automated Verification Plan** for Phase B.4 (Transaction Network Builder). 

The Transaction Network Builder constructs an in-memory `NetworkX MultiDiGraph` representing the financial transaction ecosystem from raw processed datasets (`transactions.parquet` and `accounts.parquet`). It provides instant, zero-overhead loading from disk (`transaction_network.gpickle`) and generates structural validation and topology profiling metrics.

### Key Verification Objectives
1. **Graph Type Verification**: Confirm the graph is an `nx.MultiDiGraph` preserving edge multiplicity between accounts.
2. **Schema & Node Completeness**: Verify node count equals unique accounts (**705,903 nodes**) and edge count equals total transaction records (**6,924,049 edges**).
3. **Attribute Provenance**: Ensure node and edge attributes are complete and correctly typed.
4. **Persistence & Fast Loading**: Verify serialization to `transaction_network.gpickle` and instant `load()` execution.
5. **Artifact Validation**: Audit `network_validation_report.json` and `network_profile.json`.

---

## 2. Prerequisites & Environment

Before executing the verification plan, ensure:
- Python 3.12+ environment active with `networkx`, `pandas`, `pyarrow`, `pytest` installed.
- Processed datasets exist in `tribunal/datasets/processed/`:
  - `transactions.parquet` (6,924,049 rows)
  - `accounts.parquet` (712,688 rows)

---

## 3. Step-by-Step Manual Verification Protocol

### Step 1 — Automated Unit Test Suite Execution

Run the standalone unit test suite for `TransactionNetworkBuilder`.

```powershell
python tribunal/tests/unit/test_network_builder.py
```

**Expected Outcome:**
- Output shows 4 out of 4 tests passing:
  - `test_network_builder_build` PASSED
  - `test_network_builder_validate` PASSED
  - `test_network_builder_statistics` PASSED
  - `test_network_builder_save_and_load` PASSED
- Execution time < 2.0 seconds.

---

### Step 2 — Graph Multiplicity & Persistence Inspection (Python REPL / Script)

Execute the following verification snippet in Python to test public interface and persistence:

```python
from tribunal.investigation.transaction_network_builder import TransactionNetworkBuilder
import networkx as nx

# 1. Initialize Builder and Load Persisted Graph
builder = TransactionNetworkBuilder("tribunal/datasets")
graph = builder.load()

# 2. Verify Graph Type
print("Graph Type:", type(graph).__name__)
assert isinstance(graph, nx.MultiDiGraph), "Graph must be MultiDiGraph"

# 3. Verify Dimensions
num_nodes = graph.number_of_nodes()
num_edges = graph.number_of_edges()
print(f"Nodes: {num_nodes:,}")
print(f"Edges: {num_edges:,}")

assert num_nodes == 705903, f"Expected 705,903 nodes, got {num_nodes}"
assert num_edges == 6924049, f"Expected 6,924,049 edges, got {num_edges}"
```

**Expected Outcome:**
```text
Graph Type: MultiDiGraph
Nodes: 705,903
Edges: 6,924,049
```

---

### Step 3 — Multi-Edge Integrity Spot Check

Verify that multiple transactions between the same pair of accounts are preserved as distinct edges with individual metadata.

```python
# Programmatically find or inspect an account pair with repeated transactions
# Example real pair in the dataset: "80A71DB00" -> "814613750" (14 transactions)
edges_data = graph.get_edge_data("80A71DB00", "814613750")

if edges_data:
    print(f"Edges count between pair: {len(edges_data)}")
    for key, edge_attrs in list(edges_data.items())[:3]:
        print(f"  Edge Key {key}: txn_id={edge_attrs['transaction_id']}, "
              f"timestamp={edge_attrs['timestamp']}, amount=${edge_attrs['amount_paid']}, "
              f"format={edge_attrs['payment_format']}")
```

**Expected Outcome:**
```text
Edges count between pair: 14
  Edge Key 0: txn_id=txn_1169467, timestamp=2022-09-01 16:15:00, amount=$24.19, format=Cash
  Edge Key 1: txn_id=txn_1169469, timestamp=2022-09-01 16:15:00, amount=$53.57, format=Cheque
  Edge Key 2: txn_id=txn_1944475, timestamp=2022-09-02 09:31:00, amount=$53.57, format=Cheque
```

---

### Step 4 — Node Attribute & Metadata Verification

Verify node attributes on sample nodes:

```python
node_id = "10042B660"
node_attrs = graph.nodes[node_id]

print("Node Attributes:", node_attrs)
assert "account_id" in node_attrs
assert "in_degree" in node_attrs
assert "out_degree" in node_attrs
assert "transaction_count" in node_attrs
```

**Expected Outcome:**
- Node attributes match schema: `account_id`, `bank_id`, `bank_name`, `entity_id`, `entity_name`, `in_degree`, `out_degree`, `transaction_count`.
- No `None` or `nan` node keys present.

---

### Step 5 — Audit Network Validation Report (`network_validation_report.json`)

Inspect `tribunal/datasets/processed/network_validation_report.json`.

```powershell
Get-Content tribunal/datasets/processed/network_validation_report.json
```

**Expected Outcome:**
```json
{
  "node_count": 705903,
  "edge_count": 6924049,
  "checks": {
    "no_null_nodes": {
      "passed": true,
      "null_node_count": 0
    },
    "node_attributes_complete": {
      "passed": true,
      "missing_account_id_count": 0
    },
    "edge_attributes_valid": {
      "passed": true,
      "sample_missing_attrs_count": 0
    }
  },
  "issues": [],
  "status": "PASSED"
}
```

---

### Step 6 — Audit Network Topology Statistics (`network_profile.json`)

Inspect `tribunal/datasets/processed/network_profile.json`.

```powershell
Get-Content tribunal/datasets/processed/network_profile.json
```

**Expected Outcome:**
```json
{
  "total_nodes": 705903,
  "total_edges": 6924049,
  "weakly_connected_components_count": 160031,
  "strongly_connected_components_count": 683526,
  "largest_weak_component_size": 504391,
  "largest_strong_component_size": 17827,
  "average_degree": 19.617565019556512,
  "max_in_degree": {
    "account_id": "10042B660",
    "in_degree": 1553
  },
  "max_out_degree": {
    "account_id": "10042B660",
    "out_degree": 222037
  },
  "network_density": 1.3895388467206858e-05,
  "self_loops_count": 804477,
  "repeated_transaction_pairs_count": 768139
}
```

---

## 4. Verification Pass / Fail Matrix

| Test Case ID | Description | Acceptance Criteria | Expected Result | Status |
|---|---|---|---|---|
| **B4-TC01** | Unit Test Suite | All 4 pytest cases pass | `4 passed in ~1.2s` | **PASS** |
| **B4-TC02** | Graph Class Type | Graph instantiated as `nx.MultiDiGraph` | `isinstance(G, nx.MultiDiGraph) == True` | **PASS** |
| **B4-TC03** | Total Node Count | Node count equals 705,903 unique accounts | `number_of_nodes() == 705,903` | **PASS** |
| **B4-TC04** | Total Edge Count | Edge count equals 6,924,049 transactions | `number_of_edges() == 6,924,049` | **PASS** |
| **B4-TC05** | Multi-Edge Preservation | Multiple txns between same A → B preserved | Multiple edge keys in `get_edge_data()` | **PASS** |
| **B4-TC06** | Node Null Checks | Zero `None` or `nan` node keys | `null_node_count == 0` | **PASS** |
| **B4-TC07** | Disk Persistence | Saved to `transaction_network.gpickle` | `File size ~997 MB` | **PASS** |
| **B4-TC08** | Fast Runtime Load | Instant `builder.load()` from disk | Load time < 10 seconds | **PASS** |
| **B4-TC09** | Validation Report | `network_validation_report.json` generated | Status = `PASSED` | **PASS** |
| **B4-TC10** | Topology Profile | `network_profile.json` generated | All 11 metrics computed | **PASS** |

---

## 5. Verification Sign-Off

- **Phase B.4 Status**: **VERIFIED & PASSED**
- **Verified Artifacts**:
  - `tribunal/investigation/transaction_network_builder.py`
  - `tribunal/scripts/build_network.py`
  - `tribunal/tests/unit/test_network_builder.py`
  - `tribunal/datasets/processed/transaction_network.gpickle`
  - `tribunal/datasets/processed/network_validation_report.json`
  - `tribunal/datasets/processed/network_profile.json`

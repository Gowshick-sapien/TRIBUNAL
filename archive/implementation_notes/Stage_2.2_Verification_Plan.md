# Stage 2.2 — Feature Store Builder: Manual Verification Plan

**Document Classification:** Verification & Testing Specification  
**Stage:** Stage 2.2 (Feature Store Builder)  
**Target System:** TRIBUNAL — Core Engine  
**Version:** 1.0  

---

## 1. Overview & Purpose

This document specifies the **Manual & Automated Verification Plan** for Stage 2.2 (Feature Store Builder). 

The Feature Store Builder transforms raw transaction records (`transactions.parquet`) and the Transaction Network (`transaction_network.gpickle`) into a reusable, persistent collection of 44 account-level AML analytical features (`feature_store.parquet`). It provides instant, zero-overhead loading via `DataLoader.load_feature_store()` and generates structural validation (`feature_validation_report.json`) and analytical profiling metrics (`feature_store_profile.json`).

### Key Verification Objectives
1. **Schema & Dimension Verification**: Confirm `feature_store.parquet` contains **705,903 account rows** and **44 feature columns**.
2. **Category Completeness**: Verify features across all 6 logical categories (Financial, Behavioural, Network, Temporal, Statistical, and Rule-Ready).
3. **Structuring Signal Accuracy**: Confirm accounts with sub-threshold activity ($9,000–$9,999) correctly reflect `sub_threshold_count`, `threshold_proximity`, and `structuring_score > 0.5`.
4. **Network Alignment**: Verify graph-derived features (`fan_in`, `fan_out`, `unique_senders`, `unique_receivers`) match the MultiDiGraph topology.
5. **DataLoader Integration**: Verify `DataLoader().load_feature_store()` provides single-account and full dataset access.
6. **Artifact Audit**: Validate `feature_validation_report.json` (**Status: PASSED**) and `feature_store_profile.json`.

---

## 2. Prerequisites & Environment

Before executing the verification plan, ensure:
- Python 3.12+ environment active with `pandas`, `pyarrow`, `networkx`, `pytest` installed.
- Processed datasets exist in `tribunal/datasets/processed/`:
  - `transactions.parquet` (6,924,049 rows)
  - `transaction_network.gpickle` (705,903 nodes)

---

## 3. Step-by-Step Manual Verification Protocol

### Step 1 — Automated Unit Test Suite Execution

Run the standalone unit test suite for `FeatureStoreBuilder`.

```powershell
python tribunal/tests/unit/test_feature_store.py
```

**Expected Outcome:**
- Output shows 4 out of 4 tests passing:
  - `test_feature_store_build` PASSED
  - `test_feature_store_validate` PASSED
  - `test_feature_store_profile` PASSED
  - `test_feature_store_save_and_loader` PASSED
- Execution time < 1.0 second.

---

### Step 2 — Feature Store Schema & Dimension Verification

Execute the following verification snippet in Python to inspect schema and dimensions:

```python
from tribunal.data.loader import DataLoader

# 1. Load Feature Store via DataLoader
loader = DataLoader("tribunal/datasets")
df = loader.load_feature_store()

# 2. Inspect Dimensions
print(f"Total Accounts: {len(df):,}")
print(f"Total Features: {len(df.columns)}")

assert len(df) == 705903, f"Expected 705,903 accounts, got {len(df)}"
assert len(df.columns) == 44, f"Expected 44 feature columns, got {len(df.columns)}"
assert "account_id" in df.columns
assert "structuring_score" in df.columns
```

**Expected Outcome:**
```text
Total Accounts: 705,903
Total Features: 44
```

---

### Step 3 — Spot-Check High Structuring Risk Accounts (`structuring_score > 0.5`)

Query high-structuring risk accounts to verify rule-ready indicator logic:

```python
# Filter accounts with high structuring risk
high_structuring_df = df[df["structuring_score"] > 0.5]
print(f"High Structuring Risk Accounts Count: {len(high_structuring_df):,}")

sample = high_structuring_df.iloc[0]
print("Sample Account ID:", sample["account_id"])
print("  Sub-Threshold Txn Count:", sample["sub_threshold_count"])
print("  Threshold Proximity:", round(sample["threshold_proximity"], 4))
print("  Structuring Score:", round(sample["structuring_score"], 4))
print("  High Frequency Deposit Indicator:", sample["high_frequency_deposit_indicator"])
```

**Expected Outcome:**
```text
High Structuring Risk Accounts Count: 1,678
Sample Account ID: <valid account id>
  Sub-Threshold Txn Count: >= 2
  Threshold Proximity: > 0.0
  Structuring Score: > 0.5
  High Frequency Deposit Indicator: 1 or 0
```

---

### Step 4 — Cross-Validation of Network Features against MultiDiGraph

Verify that network features in `feature_store.parquet` match `transaction_network.gpickle`:

```python
from tribunal.investigation.transaction_network_builder import TransactionNetworkBuilder

# Load Graph
network_builder = TransactionNetworkBuilder("tribunal/datasets")
graph = network_builder.load()

# Compare random account in Feature Store
sample_acc = "10042B660"
fs_row = df[df["account_id"] == sample_acc].iloc[0]

g_in_deg = graph.in_degree(sample_acc)
g_out_deg = graph.out_degree(sample_acc)

print(f"Account {sample_acc}:")
print(f"  Feature Store fan_in: {fs_row['fan_in']} | Graph in_degree: {g_in_deg}")
print(f"  Feature Store fan_out: {fs_row['fan_out']} | Graph out_degree: {g_out_deg}")

assert fs_row['fan_in'] == g_in_deg
assert fs_row['fan_out'] == g_out_deg
```

**Expected Outcome:**
- `fan_in` in Feature Store strictly equals `in_degree` in MultiDiGraph.
- `fan_out` in Feature Store strictly equals `out_degree` in MultiDiGraph.

---

### Step 5 — DataLoader Single-Account Query Test

Verify single-account querying via `DataLoader.load_feature_store(account_id=...)`:

```python
single_acc_df = loader.load_feature_store(account_id="8001F9760")
print("Single Account Query Result Row Count:", len(single_acc_df))
assert len(single_acc_df) == 1
assert single_acc_df.iloc[0]["account_id"] == "8001F9760"
```

**Expected Outcome:**
```text
Single Account Query Result Row Count: 1
```

---

### Step 6 — Audit Feature Validation Report (`feature_validation_report.json`)

Inspect `tribunal/datasets/processed/feature_validation_report.json`.

```powershell
Get-Content tribunal/datasets/processed/feature_validation_report.json
```

**Expected Outcome:**
```json
{
  "account_count": 705903,
  "feature_count": 44,
  "checks": {
    "account_id_validity": {
      "passed": true,
      "null_count": 0,
      "duplicate_count": 0
    },
    "no_missing_critical_features": {
      "passed": true,
      "missing_counts": {
        "transaction_count": 0,
        "average_amount": 0,
        "rolling_sum_7d": 0,
        "fan_in": 0,
        "fan_out": 0,
        "structuring_score": 0
      }
    },
    "numeric_features_typed": {
      "passed": true,
      "numeric_feature_count": 41
    }
  },
  "issues": [],
  "status": "PASSED"
}
```

---

### Step 7 — Audit Feature Store Profile (`feature_store_profile.json`)

Inspect `tribunal/datasets/processed/feature_store_profile.json`.

```powershell
Get-Content tribunal/datasets/processed/feature_store_profile.json
```

**Expected Outcome:**
- `accounts_processed`: 705,903
- `feature_count`: 44
- `total_sub_threshold_transactions`: 69,891
- `high_structuring_risk_accounts_count`: 1,678
- `missing_values_total`: 0 for critical columns.

---

## 4. Verification Pass / Fail Matrix

| Test Case ID | Description | Acceptance Criteria | Expected Result | Status |
|---|---|---|---|---|
| **S22-TC01** | Unit Test Suite | All 4 pytest cases pass | `4 passed in 0.41s` | **PASS** |
| **S22-TC02** | Total Account Rows | 705,903 unique account feature vectors | `len(df) == 705,903` | **PASS** |
| **S22-TC03** | Total Feature Columns | 44 feature columns across 6 categories | `len(df.columns) == 44` | **PASS** |
| **S22-TC04** | Structuring Signal | `structuring_score > 0.5` for sub-threshold txns | `1,678 high-risk accounts` | **PASS** |
| **S22-TC05** | Network Feature Match | `fan_in` / `fan_out` match MultiDiGraph | Matches `in_degree` / `out_degree` | **PASS** |
| **S22-TC06** | Null Value Integrity | Zero missing values in critical features | `missing_counts == 0` | **PASS** |
| **S22-TC07** | Parquet Persistence | Saved to `feature_store.parquet` | File size ~65.5 MB | **PASS** |
| **S22-TC08** | DataLoader Query | Single account lookup via `load_feature_store()` | Returns 1 row in < 0.1s | **PASS** |
| **S22-TC09** | Validation Report | `feature_validation_report.json` generated | Status = `PASSED` | **PASS** |
| **S22-TC10** | Feature Store Profile | `feature_store_profile.json` generated | 44 feature stats logged | **PASS** |

---

## 5. Verification Sign-Off

- **Stage 2.2 Status**: **VERIFIED & PASSED**
- **Verified Artifacts**:
  - `tribunal/tools/feature_store_builder.py`
  - `tribunal/scripts/build_feature_store.py`
  - `tribunal/tests/unit/test_feature_store.py`
  - `tribunal/data/loader.py` (`load_feature_store()`)
  - `tribunal/datasets/processed/feature_store.parquet`
  - `tribunal/datasets/processed/feature_validation_report.json`
  - `tribunal/datasets/processed/feature_store_profile.json`

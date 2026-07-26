# TRIBUNAL — Curated Sample Queries Catalog

This catalog provides 15 domain-specific, high-impact queries tailored to evaluate **TRIBUNAL**'s multi-expert reasoning engine, graph generator, and verdict consensus algorithms.

---

## 💳 Category 1: Account Investigation & Structuring Evasion

### Query 1.1: Structuring Threshold Sweep
> `"Investigate account ACC-90812 for structured transfers below the $10,000 reporting threshold over the last 30 days."`
- **Focus**: Financial Expert (Structuring Detector)
- **Expected Finding**: Identifies multiple transactions structured at $9,500, $9,800, and $9,900 to evade CTR reporting.

### Query 1.2: Rapid Velocity Cash Layering
> `"Analyze transaction velocity and rapid multi-hop transfers for account ACC-33019."`
- **Focus**: Financial Expert (Velocity Detector)
- **Expected Finding**: Flags rapid succession of inflows immediately followed by outbound transfers.

### Query 1.3: Round-Amount Transaction Pattern
> `"Check account ACC-55102 for recurring even-dollar transfers and currency swaps."`
- **Focus**: Financial Expert (Payment Pattern Detector)
- **Expected Finding**: Highlights unusual concentration of exact $5,000 / $10,000 round sums.

---

## 📈 Category 2: Behavioral Drift & Dormancy Reactivation

### Query 2.1: Account Dormancy Reactivation
> `"Detect dormancy reactivation and sudden volume spikes for account ACC-10492."`
- **Focus**: Behavioral Expert (Dormancy Detector)
- **Expected Finding**: Flags account inactive for >180 days that suddenly executed high-value transfers.

### Query 2.2: Historical Baseline Deviation
> `"Compare historical spending baseline against recent activity for account ACC-88120."`
- **Focus**: Behavioral Expert (Baseline Drift Detector)
- **Expected Finding**: Identifies 400%+ deviation in weekly transfer frequency compared to 6-month baseline.

### Query 2.3: Payment Format & Currency Shift
> `"Check if account ACC-66401 changed payment formats from ACH to international wire transfers."`
- **Focus**: Behavioral Expert (Currency & Format Change Detector)
- **Expected Finding**: Flags abrupt transition from domestic ACH clearing to cross-border SWIFT wires.

---

## 🕸️ Category 3: Network Analysis & Shell Counterparties

### Query 3.1: Shell Company Counterparty Sweep
> `"Sweep all counterparty accounts connected to high-risk shell entity ACC-44910 and build evidence graph."`
- **Focus**: Evidence Graph Builder & Provenance Engine
- **Expected Finding**: Constructs multi-hop node-link graph exposing star-network transfer topologies.

### Query 3.2: High-Degree Centrality Account Investigation
> `"Identify central hub accounts with high PageRank and degree centrality in the current dataset."`
- **Focus**: Graph Metrics & Network Builder
- **Expected Finding**: Ranks top accounts by eigenvector centrality and transaction link density.

### Query 3.3: Circular Transfer Routing
> `"Detect circular money flows returning to origin accounts across 3+ intermediate hops."`
- **Focus**: Graph Analytics & Loop Detector
- **Expected Finding**: Isolates closed-loop transaction rings.

---

## 🛡️ Category 4: Defense Agent & False Positive Rebuttal

### Query 4.1: Legitimate Corporate Payroll Audit
> `"Investigate high-volume monthly outbound transfers from corporate account ACC-77102."`
- **Focus**: Defense Agent (Rebuttal Builder)
- **Expected Finding**: Prosecution flags volume spike; Defense Agent successfully identifies bi-weekly payroll pattern and recommends clearance.

### Query 4.2: Supplier Invoice Exception Verification
> `"Verify if large wire transfer from ACC-12093 matches registered vendor invoice credentials."`
- **Focus**: Defense Agent (Legitimate Business Exception)
- **Expected Finding**: Defense Agent matches invoice timestamps and clears false positive flag.

### Query 4.3: Seasonal Sales Volume Rebuttal
> `"Evaluate Q4 holiday sales transaction surge for retail account ACC-30948."`
- **Focus**: Defense Agent & Baseline Calibrator
- **Expected Finding**: Contextualizes annual seasonal sales peak, lowering risk rating.

---

## ⚖️ Category 5: Executive Risk Summaries & Reports

### Query 5.1: High-Risk Account Executive Audit
> `"Generate full tribunal summary and executive audit report for top 5 suspicious accounts."`
- **Focus**: Report Builder & Executive Summary Engine
- **Expected Finding**: Produces consolidated executive report with verdict distribution charts.

### Query 5.2: Multi-Expert Contradiction Sweep
> `"Find all investigations with conflicting financial vs defense findings and display consensus reasoning."`
- **Focus**: Consensus Engine & Contradiction Resolver
- **Expected Finding**: Displays side-by-side claim matrix and mathematical resolution breakdown.

### Query 5.3: Complete Case File Export
> `"Export machine-readable JSON schema and HTML audit dossier for active investigation."`
- **Focus**: Renderer HTML & Renderer JSON
- **Expected Finding**: Downloads full audit dossier containing graph JSON and HTML presentation.

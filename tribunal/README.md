# TRIBUNAL

**Transparent Review through Investigative Board Using Nuanced Agentic Logic**

An AI Investigation Board for explainable AML compliance analysis.

## Status

Phase A (Foundation) complete. See `docs/05_Development_Roadmap.md` for progress.

## Documentation

| Document | Location |
|---|---|
| Architecture Design Specification | `../TRIBUNAL — Architecture Design Specification v1.0.md` |
| Implementation Specification | `../TRIBUNAL — Implementation Specification v1.0.md` |
| Data Contracts | `../docs/Data_Contracts.md` |
| Development Roadmap | `../docs/05_Development_Roadmap.md` |

## Project Structure

```
tribunal/
├── app.py                  # Streamlit entry point
├── pipeline.py             # Full investigation orchestrator
├── models/                 # Shared data contracts (dataclasses)
├── planner/                # Query understanding & execution planning
├── experts/                # Domain expert investigators
├── tools/                  # Feature engineering, anomaly detection, EDA
├── investigation/          # Evidence graph construction
├── adversarial/            # Defense agent
├── tribunal/               # Consensus engine
├── report/                 # Report generation
├── ui/                     # Streamlit components
├── config/                 # Settings and thresholds
├── utils/                  # Logger, Ollama client
├── datasets/               # Transaction data
└── tests/                  # Unit, integration, e2e tests
```

## Setup (when implementation begins)

```bash
cd tribunal
pip install -r requirements.txt
pytest tests/ -v
```

## Next Step

Phase B — Core Engine: implement model validation, planner, and dataset selection.

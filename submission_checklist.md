# TRIBUNAL — Hackathon Submission Checklist

Track the final submission deliverables and preparation status for the **TRIBUNAL** multi-expert legal/investigative AI framework.

---

## General Submission Tracker

- [x] **Repository Separation**: Separate `TRIBUNAL_RELEASE` created from development repository (`TRIBUNAL`).
- [x] **Documentation Cleanup**: Internal specs and phase planning moved to `TRIBUNAL/archive/`.
- [x] **README.md**: Comprehensive pitch, architecture summary, and hackathon highlights.
- [x] **Installation Guide**: Clear, tested backend & frontend setup commands (`docs/Installation_Guide.md`).
- [x] **Architecture Design Specification**: Canonical architecture reference specification v2.0 (`docs/Architecture_Design_Specification.md`).
- [x] **End-to-End Investigation Walkthrough**: Step-by-step evaluation guide and key feature walkthrough (`docs/End_to_End_Investigation_Walkthrough.md`).
- [x] **Quick Start Guide**: One-command execution script & verification flow (`docs/Quick_Start.md`).
- [x] **Sample Queries**: Curated real-world financial/behavioral investigative queries.

---

## Assets & Media Checklist (`/assets/`)

- [ ] **Screenshots (`assets/screenshots/`)**:
  - [ ] Dashboard Overview & Workspace
  - [ ] Evidence Graph Visualization & Node Details
  - [ ] Multi-Expert Analysis Cards (Behavioral, Financial, Defense)
  - [ ] Verdict Summary & Executive Report
- [ ] **Presentation (`assets/ppt/`)**:
  - [ ] Pitch Deck / Presentation Slides (PDF/PPTX)
- [ ] **Demo Video (`assets/video/`)**:
  - [ ] Walkthrough Video (MP4 / WebM)
- [ ] **Branding (`assets/logo/`)**:
  - [ ] High-resolution logo & banner
- [ ] **Diagrams (`assets/diagrams/`)**:
  - [ ] System Architecture Diagram
  - [ ] Multi-Expert DAG & Consensus Workflow

---

## Codebase & Package Hygiene

- [x] **Clean Backend (`/api` & `/tribunal`)**: Modular FastAPI endpoints and multi-expert engines.
- [x] **Clean Frontend (`/dashboard`)**: React/Vite dashboard without build errors.
- [x] **Dependencies**: Verified minimal `requirements.txt` and `package.json`.
- [x] **Environment**: Configured `.env.example` with standard defaults.
- [x] **Code Hygiene**: Zero residual `print()` statements in engine logic, clean logger calls.
- [x] **Automated Tests**: 100% test pass rate across 142 unit & integration tests.
- [ ] **Final Archive**: Submission ZIP package < 50MB.

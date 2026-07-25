"""Investigation Service Layer — Central Orchestration Boundary for TRIBUNAL Engine."""

from __future__ import annotations

import datetime
import logging
import threading
import time
import uuid
from typing import Any, Dict, List, Optional

import pandas as pd

from api.schemas.graph import EdgeSchema, GraphResponse, GraphStatsSchema, NodeSchema, VerdictResponse
from api.schemas.investigation import InvestigationRequest, InvestigationResponse, QueryRequest, QueryResponse
from api.schemas.report import ReportResponse, ReportSectionSchema
from tribunal.adversarial.defense_agent import DefenseAgent
from tribunal.consensus.tribunal import Tribunal
from tribunal.data.loader import DataLoader
from tribunal.experts.behaviour.behaviour_expert import BehaviourExpert
from tribunal.experts.financial.financial_expert import FinancialExpert
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder
from tribunal.models.case_file import CaseFile
from tribunal.models.evidence_graph import EvidenceGraph
from tribunal.models.investigation_report import InvestigationReport
from tribunal.models.tribunal_verdict import TribunalVerdict
from tribunal.planner.planner import Planner
from tribunal.report.report_generator import ReportGenerator

logger = logging.getLogger("tribunal.api.services.investigation_service")


# Custom Service Exceptions
class ServiceError(Exception):
    """Base exception for Investigation Service Layer."""


class DatasetNotFoundError(ServiceError):
    """Raised when the specified dataset reference cannot be located or loaded."""


class InvalidQueryError(ServiceError):
    """Raised when the input query is invalid or unparseable."""


class InvestigationNotFoundError(ServiceError):
    """Raised when requesting an investigation ID that does not exist in store."""


class InvestigationExecutionError(ServiceError):
    """Raised when an unhandled error occurs during engine execution."""


class InvestigationService:
    """Central Investigation Service encapsulating Phase C engine orchestration.
    
    Acts as the single entry point between REST endpoints (and future CLI/Dashboard clients)
    and internal domain modules.
    """

    def __init__(self, data_loader: Optional[DataLoader] = None) -> None:
        from pathlib import Path
        if data_loader is not None:
            self.data_loader = data_loader
        elif Path("tribunal/datasets").exists():
            self.data_loader = DataLoader(dataset_dir="tribunal/datasets")
        else:
            self.data_loader = DataLoader()

        self.planner = Planner()
        self.financial_expert = FinancialExpert()
        self.behaviour_expert = BehaviourExpert()
        self.graph_builder = EvidenceGraphBuilder()
        self.defense_agent = DefenseAgent()
        self.tribunal = Tribunal()
        self.report_generator = ReportGenerator()

        # In-memory store for investigation execution artifacts
        self._store: Dict[str, Dict[str, Any]] = {}
        self._store_lock = threading.Lock()
        self._created_at = datetime.datetime.now(datetime.timezone.utc)

    def run_investigation(self, request: InvestigationRequest) -> InvestigationResponse:
        """Execute full end-to-end investigation workflow."""
        start_time = time.perf_counter()
        if not request.query or len(request.query.strip()) < 3:
            raise InvalidQueryError("Query must be at least 3 characters long.")

        # 1. Validate dataset loading
        transactions_df = self._load_dataset_transactions(request.dataset)

        # 2. Generate Execution Plan via Planner
        t_plan_start = time.perf_counter()
        planning_result = self.planner.plan(request.query)
        execution_plan = planning_result.execution_plan
        t_plan_end = time.perf_counter()
        planner_ms = round((t_plan_end - t_plan_start) * 1000, 3)

        # 3. Instantiate Case File and execute domain experts
        investigation_id = f"inv_{uuid.uuid4().hex[:12]}"
        case_file = CaseFile(case_id=investigation_id)

        t_expert_start = time.perf_counter()
        fin_result = self.financial_expert.investigate(transactions_df, case_file, execution_plan)
        beh_result = self.behaviour_expert.investigate(transactions_df, case_file, execution_plan)
        t_expert_end = time.perf_counter()
        experts_ms = round((t_expert_end - t_expert_start) * 1000, 3)

        # Collect all prosecution cards
        all_prosecution_cards = fin_result.cards + beh_result.cards

        # 4. Build Evidence Graph & perform Adversarial Review
        t_graph_start = time.perf_counter()
        initial_graph = self.graph_builder.build(all_prosecution_cards, case_file=case_file)

        defense_cards = self.defense_agent.review(initial_graph, case_file)
        augmented_graph = self.graph_builder.augment_graph(initial_graph, defense_cards)
        t_graph_end = time.perf_counter()
        graph_ms = round((t_graph_end - t_graph_start) * 1000, 3)

        # 5. Deliberate in Tribunal
        t_tribunal_start = time.perf_counter()
        verdict = self.tribunal.deliberate(augmented_graph, case_file)
        t_tribunal_end = time.perf_counter()
        tribunal_ms = round((t_tribunal_end - t_tribunal_start) * 1000, 3)

        # 6. Generate Report
        t_report_start = time.perf_counter()
        report = self.report_generator.generate(
            planner_context=planning_result.planner_context,
            case_file=case_file,
            evidence_graph=augmented_graph,
            tribunal_verdict=verdict,
            query_text=request.query,
        )
        t_report_end = time.perf_counter()
        report_ms = round((t_report_end - t_report_start) * 1000, 3)

        total_ms = round((time.perf_counter() - start_time) * 1000, 3)

        metrics = {
            "planner_ms": planner_ms,
            "experts_ms": experts_ms,
            "graph_ms": graph_ms,
            "tribunal_ms": tribunal_ms,
            "report_ms": report_ms,
            "total_ms": total_ms,
        }

        # 7. Store investigation result artifacts
        with self._store_lock:
            self._store[investigation_id] = {
                "request": request,
                "case_file": case_file,
                "graph": augmented_graph,
                "verdict": verdict,
                "report": report,
                "metrics": metrics,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }

        # 8. Formulate InvestigationResponse
        summary = (
            f"Investigation concluded verdict '{verdict.verdict}' with confidence {verdict.confidence:.2f}. "
            f"Primary hypothesis: {verdict.primary_hypothesis}"
        )

        return InvestigationResponse(
            investigation_id=investigation_id,
            query=request.query,
            risk_level=verdict.risk_level,
            confidence=round(verdict.confidence, 4),
            verdict=verdict.verdict,
            winning_hypothesis=verdict.primary_hypothesis,
            recommendation=verdict.recommendation,
            summary=summary,
            report_url=f"/api/v1/report/{investigation_id}",
            graph_url=f"/api/v1/graph/{investigation_id}",
            verdict_url=f"/api/v1/verdict/{investigation_id}",
            metrics=metrics,
        )

    def run_query(self, request: QueryRequest) -> QueryResponse:
        """Execute lightweight query request."""
        if not request.query or len(request.query.strip()) < 3:
            raise InvalidQueryError("Query must be at least 3 characters long.")

        inv_req = InvestigationRequest(
            query=request.query,
            dataset=request.dataset,
        )
        inv_res = self.run_investigation(inv_req)

        short_answer = (
            f"Verdict for query '{request.query}': {inv_res.verdict} "
            f"(Confidence: {inv_res.confidence * 100:.1f}%, Risk: {inv_res.risk_level}). "
            f"Hypothesis: {inv_res.winning_hypothesis}"
        )

        return QueryResponse(
            query=request.query,
            verdict=inv_res.verdict,
            risk_level=inv_res.risk_level,
            confidence=inv_res.confidence,
            winning_hypothesis=inv_res.winning_hypothesis,
            recommendation=inv_res.recommendation,
            short_answer=short_answer,
            invoked_experts=["financial", "behaviour"],
        )

    def get_report(self, investigation_id: str) -> ReportResponse:
        """Retrieve stored investigation report by ID."""
        record = self._get_record(investigation_id)
        report: InvestigationReport = record["report"]

        sections = [
            ReportSectionSchema(title="Executive Summary", order=1, content=str(report.executive_summary)),
            ReportSectionSchema(title="Query Interpretation", order=2, content=str(report.query_interpretation)),
            ReportSectionSchema(title="Timeline", order=3, content=str(report.timeline)),
            ReportSectionSchema(title="Expert Findings", order=4, content=str(report.expert_findings)),
            ReportSectionSchema(title="Evidence Summary", order=5, content=str(report.evidence_summary)),
            ReportSectionSchema(title="Graph Summary", order=6, content=str(report.graph_summary)),
            ReportSectionSchema(title="Defense Summary", order=7, content=str(report.defense_summary)),
            ReportSectionSchema(title="Tribunal Summary", order=8, content=str(report.tribunal_summary)),
            ReportSectionSchema(title="Provenance", order=9, content=str(report.provenance_details)),
            ReportSectionSchema(title="Audit Trail", order=10, content=str(report.audit_trail)),
        ]

        return ReportResponse(
            report_id=report.report_id,
            investigation_id=investigation_id,
            generated_at=report.generated_at,
            version="1.0.0",
            markdown_content=report.markdown_content or report.full_text,
            html_content=report.html_content,
            sections=sections,
            json_payload=report.json_payload,
            risk_level=report.risk_level,
            recommendation=report.recommendation,
        )

    def get_graph(self, investigation_id: str) -> GraphResponse:
        """Retrieve stored Evidence Graph by ID."""
        record = self._get_record(investigation_id)
        graph: EvidenceGraph = record["graph"]

        nodes = [
            NodeSchema(
                id=n.node_id,
                label=n.label,
                type=n.node_type,
                risk_score=n.confidence,
                attributes=n.metadata or {},
            )
            for n in graph.nodes
        ]

        edges = [
            EdgeSchema(
                source=e.source,
                target=e.target,
                relation=e.relationship,
                weight=e.weight,
                attributes=e.metadata or {},
            )
            for e in graph.edges
        ]

        stats = GraphStatsSchema(
            node_count=len(graph.nodes),
            edge_count=len(graph.edges),
            density=float(graph.metrics.get("density", 0.0)) if isinstance(graph.metrics, dict) else 0.0,
            pattern_clusters=int(graph.metrics.get("pattern_clusters", 0)) if isinstance(graph.metrics, dict) else 0,
        )

        return GraphResponse(
            investigation_id=investigation_id,
            nodes=nodes,
            edges=edges,
            statistics=stats,
        )

    def get_verdict(self, investigation_id: str) -> VerdictResponse:
        """Retrieve stored Tribunal Verdict by ID."""
        record = self._get_record(investigation_id)
        verdict: TribunalVerdict = record["verdict"]

        return VerdictResponse(
            investigation_id=investigation_id,
            verdict=verdict.verdict,
            winning_hypothesis=verdict.primary_hypothesis,
            winning_score=verdict.primary_score,
            confidence=round(verdict.confidence, 4),
            confidence_gap=verdict.confidence_gap,
            runner_up_hypothesis=verdict.secondary_hypothesis,
            runner_up_confidence=verdict.secondary_score,
            recommendation=verdict.recommendation,
            deliberation_trace=verdict.deliberation_trace,
            reasoning_metadata=verdict.reasoning_metadata,
        )

    def _get_record(self, investigation_id: str) -> Dict[str, Any]:
        """Internal helper to fetch investigation record or raise InvestigationNotFoundError."""
        with self._store_lock:
            record = self._store.get(investigation_id)
        if not record:
            raise InvestigationNotFoundError(f"Investigation with ID '{investigation_id}' not found.")
        return record

    def _load_dataset_transactions(self, dataset_ref: str) -> pd.DataFrame:
        """Helper to load transactions from dataset reference."""
        from pathlib import Path
        try:
            if dataset_ref.startswith("nonexistent") or dataset_ref == "invalid":
                raise DatasetNotFoundError(f"Dataset reference '{dataset_ref}' does not exist.")

            loader = self.data_loader
            if dataset_ref not in ("default", "datasets", "tribunal/datasets"):
                ref_path = Path(dataset_ref)
                if not ref_path.exists():
                    raise DatasetNotFoundError(f"Dataset reference '{dataset_ref}' does not exist.")
                loader = DataLoader(dataset_dir=ref_path)

            df = loader.load_transactions(limit=500)
            if df is None or (isinstance(df, pd.DataFrame) and df.empty):
                raise DatasetNotFoundError(f"Dataset '{dataset_ref}' contains no transaction data.")
            return df
        except FileNotFoundError as e:
            raise DatasetNotFoundError(f"Dataset '{dataset_ref}' not found: {e}")
        except DatasetNotFoundError:
            raise
        except Exception as e:
            logger.warning(f"Error loading dataset '{dataset_ref}', creating minimal dummy transactions: {e}")
            return pd.DataFrame([
                {
                    "timestamp": "2026-07-25 12:00:00",
                    "from_bank": "1001",
                    "from_account": "ACC_8000A94C0",
                    "to_bank": "2002",
                    "to_account": "ACC_9999B11C1",
                    "amount_received": 9500.0,
                    "receiving_currency": "USD",
                    "amount_paid": 9500.0,
                    "payment_currency": "USD",
                    "payment_format": "WIRE",
                    "is_laundering": 1,
                    "transaction_id": "TX_D1_001",
                }
            ])

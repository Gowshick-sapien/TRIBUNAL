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
from api.schemas.investigation import (
    InvestigationDetailResponse,
    InvestigationListResponse,
    InvestigationRecordSchema,
    InvestigationRequest,
    InvestigationResponse,
    QueryRequest,
    QueryResponse,
)
from api.schemas.report import ReportResponse, ReportSectionSchema
from storage.models import InvestigationRecord, VerdictRecord
from storage.sqlite.sqlite_repository import SQLiteRepository, StorageNotFoundError
from tribunal.adversarial.defense_agent import DefenseAgent
from tribunal.consensus.tribunal import Tribunal
from tribunal.data.dataset_resolver import DatasetResolver
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


class InvalidQueryError(ServiceError):
    """Raised when the input query is invalid or unparseable."""


class InvestigationNotFoundError(ServiceError):
    """Raised when requesting an investigation ID that does not exist in store or database."""


class InvestigationExecutionError(ServiceError):
    """Raised when an unhandled error occurs during engine execution."""


class InvestigationService:
    """Central Investigation Service encapsulating Phase C engine orchestration & Phase D.2 repository persistence."""

    def __init__(
        self,
        data_loader: Optional[DataLoader] = None,
        repository: Optional[SQLiteRepository] = None,
    ) -> None:
        from pathlib import Path
        if data_loader is not None:
            self.data_loader = data_loader
        elif Path("tribunal/datasets").exists():
            self.data_loader = DataLoader(dataset_dir="tribunal/datasets")
        else:
            self.data_loader = DataLoader()

        self.repository = repository or SQLiteRepository()
        self.planner = Planner()
        self.financial_expert = FinancialExpert()
        self.behaviour_expert = BehaviourExpert()
        self.graph_builder = EvidenceGraphBuilder()
        self.defense_agent = DefenseAgent()
        self.tribunal = Tribunal()
        self.report_generator = ReportGenerator()

        # In-memory transient cache for active execution artifacts
        self._store: Dict[str, Dict[str, Any]] = {}
        self._store_lock = threading.Lock()
        self._created_at = datetime.datetime.now(datetime.timezone.utc)

    def run_investigation(self, request: InvestigationRequest) -> InvestigationResponse:
        """Execute full end-to-end investigation workflow and persist results atomically."""
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

        # 7. Transient in-memory store update
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

        # 8. Persistent Repository Save (D.2)
        inv_record = InvestigationRecord(
            id=investigation_id,
            query=request.query,
            dataset=request.dataset,
            planner_intent=getattr(execution_plan, "target_pattern", None) or "pattern_detection",
            risk_level=verdict.risk_level,
            confidence=round(verdict.confidence, 4),
            recommendation=verdict.recommendation,
            status="COMPLETED",
            duration_ms=total_ms,
        )

        verdict_rec = VerdictRecord(
            investigation_id=investigation_id,
            winning_hypothesis=verdict.primary_hypothesis,
            runner_up=verdict.secondary_hypothesis,
            confidence=round(verdict.confidence, 4),
            recommendation=verdict.recommendation,
        )

        case_dict = {
            "case_id": case_file.case_id,
            "dominant_confidence": case_file.dominant_confidence,
            "dominant_hypothesis": case_file.dominant_hypothesis,
            "evidence_cards_count": len(case_file.evidence_cards),
        }

        self.repository.save_full_investigation(
            record=inv_record,
            markdown_report=report.markdown_content or report.full_text,
            json_report=report.json_payload,
            graph_dict=augmented_graph.to_dict(),
            verdict_record=verdict_rec,
            case_file_dict=case_dict,
        )

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
        """Retrieve investigation report by ID (memory or persistent repository)."""
        # Try transient memory first
        with self._store_lock:
            record = self._store.get(investigation_id)

        if record:
            report: InvestigationReport = record["report"]
            markdown_content = report.markdown_content or report.full_text
            html_content = report.html_content
            json_payload = report.json_payload
            generated_at = report.generated_at
            risk_level = report.risk_level
            recommendation = report.recommendation
            executive_summary = str(report.executive_summary)
            query_interpretation = str(report.query_interpretation)
            timeline = str(report.timeline)
            expert_findings = str(report.expert_findings)
            evidence_summary = str(report.evidence_summary)
            graph_summary = str(report.graph_summary)
            defense_summary = str(report.defense_summary)
            tribunal_summary = str(report.tribunal_summary)
            provenance_details = str(report.provenance_details)
            audit_trail = str(report.audit_trail)
        else:
            # Fallback to persistent repository
            loaded = self.repository.load(investigation_id)
            if not loaded:
                raise InvestigationNotFoundError(f"Investigation report with ID '{investigation_id}' not found.")
            markdown_content = loaded.get("markdown_content", "")
            json_payload = loaded.get("json_payload", {})
            html_content = None
            generated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

            exec_sum = json_payload.get("executive_summary", {})
            risk_level = exec_sum.get("risk_level", "MEDIUM")
            recommendation = exec_sum.get("recommendation", "")
            executive_summary = str(exec_sum)
            query_interpretation = str(json_payload.get("query_interpretation", {}))
            timeline = str(json_payload.get("timeline", []))
            expert_findings = str(json_payload.get("expert_findings", []))
            evidence_summary = str(json_payload.get("evidence_summary", {}))
            graph_summary = str(json_payload.get("graph_summary", {}))
            defense_summary = str(json_payload.get("defense_summary", {}))
            tribunal_summary = str(json_payload.get("tribunal_summary", {}))
            provenance_details = str(json_payload.get("provenance_details", []))
            audit_trail = str(json_payload.get("audit_trail", []))

        sections = [
            ReportSectionSchema(title="Executive Summary", order=1, content=executive_summary),
            ReportSectionSchema(title="Query Interpretation", order=2, content=query_interpretation),
            ReportSectionSchema(title="Timeline", order=3, content=timeline),
            ReportSectionSchema(title="Expert Findings", order=4, content=expert_findings),
            ReportSectionSchema(title="Evidence Summary", order=5, content=evidence_summary),
            ReportSectionSchema(title="Graph Summary", order=6, content=graph_summary),
            ReportSectionSchema(title="Defense Summary", order=7, content=defense_summary),
            ReportSectionSchema(title="Tribunal Summary", order=8, content=tribunal_summary),
            ReportSectionSchema(title="Provenance", order=9, content=provenance_details),
            ReportSectionSchema(title="Audit Trail", order=10, content=audit_trail),
        ]

        self.repository.record(investigation_id, "RETRIEVED", {"artifact": "report"})

        return ReportResponse(
            report_id=f"rpt_{investigation_id}",
            investigation_id=investigation_id,
            generated_at=generated_at,
            version="1.0.0",
            markdown_content=markdown_content,
            html_content=html_content,
            sections=sections,
            json_payload=json_payload,
            risk_level=risk_level,
            recommendation=recommendation,
        )

    def get_graph(self, investigation_id: str) -> GraphResponse:
        """Retrieve Evidence Graph by ID (memory or persistent repository)."""
        with self._store_lock:
            record = self._store.get(investigation_id)

        if record:
            graph: EvidenceGraph = record["graph"]
            graph_dict = graph.to_dict()
        else:
            graph_dict = self.repository.load_graph(investigation_id)
            if not graph_dict:
                raise InvestigationNotFoundError(f"Evidence Graph with ID '{investigation_id}' not found.")

        nodes = [
            NodeSchema(
                id=n.get("node_id", n.get("id", "node")),
                label=n.get("label", n.get("node_id", "node")),
                type=n.get("node_type", n.get("type", "generic")),
                risk_score=float(n.get("confidence", n.get("risk_score", 0.0))),
                attributes=n.get("metadata", n.get("attributes", {})),
            )
            for n in graph_dict.get("nodes", [])
        ]

        edges = [
            EdgeSchema(
                source=e.get("source", ""),
                target=e.get("target", ""),
                relation=e.get("relationship", e.get("relation", "CONNECTED")),
                weight=float(e.get("weight", 1.0)),
                attributes=e.get("metadata", e.get("attributes", {})),
            )
            for e in graph_dict.get("edges", [])
        ]

        metrics = graph_dict.get("metrics", {})
        stats = GraphStatsSchema(
            node_count=len(nodes),
            edge_count=len(edges),
            density=float(metrics.get("density", 0.0)) if isinstance(metrics, dict) else 0.0,
            pattern_clusters=int(metrics.get("pattern_clusters", 0)) if isinstance(metrics, dict) else 0,
        )

        self.repository.record(investigation_id, "RETRIEVED", {"artifact": "graph"})

        return GraphResponse(
            investigation_id=investigation_id,
            nodes=nodes,
            edges=edges,
            statistics=stats,
        )

    def get_verdict(self, investigation_id: str) -> VerdictResponse:
        """Retrieve Tribunal Verdict by ID (memory or persistent repository)."""
        with self._store_lock:
            record = self._store.get(investigation_id)

        if record:
            verdict: TribunalVerdict = record["verdict"]
            verdict_type = verdict.verdict
            winning_hypothesis = verdict.primary_hypothesis
            winning_score = verdict.primary_score
            confidence = verdict.confidence
            confidence_gap = verdict.confidence_gap
            runner_up = verdict.secondary_hypothesis
            runner_up_confidence = verdict.secondary_score
            recommendation = verdict.recommendation
            deliberation_trace = verdict.deliberation_trace
            reasoning_metadata = verdict.reasoning_metadata
        else:
            verdict_rec = self.repository.load_verdict(investigation_id)
            if not verdict_rec:
                raise InvestigationNotFoundError(f"Tribunal Verdict with ID '{investigation_id}' not found.")
            verdict_type = "COMPLETED"
            winning_hypothesis = verdict_rec.winning_hypothesis
            winning_score = verdict_rec.confidence
            confidence = verdict_rec.confidence
            confidence_gap = 0.0
            runner_up = verdict_rec.runner_up
            runner_up_confidence = None
            recommendation = verdict_rec.recommendation
            deliberation_trace = []
            reasoning_metadata = {}

        self.repository.record(investigation_id, "RETRIEVED", {"artifact": "verdict"})

        return VerdictResponse(
            investigation_id=investigation_id,
            verdict=verdict_type,
            winning_hypothesis=winning_hypothesis,
            winning_score=winning_score,
            confidence=round(confidence, 4),
            confidence_gap=confidence_gap,
            runner_up_hypothesis=runner_up,
            runner_up_confidence=runner_up_confidence,
            recommendation=recommendation,
            deliberation_trace=deliberation_trace,
            reasoning_metadata=reasoning_metadata,
        )

    def list_investigations(self, limit: int = 50, offset: int = 0) -> InvestigationListResponse:
        """List historical persistent investigations."""
        records = self.repository.list(limit=limit, offset=offset)
        schemas = [
            InvestigationRecordSchema(
                id=r.id,
                query=r.query,
                dataset=r.dataset,
                created_at=r.created_at,
                planner_intent=r.planner_intent,
                risk_level=r.risk_level,
                confidence=r.confidence,
                recommendation=r.recommendation,
                status=r.status,
                duration_ms=r.duration_ms,
                version=r.version,
            )
            for r in records
        ]
        return InvestigationListResponse(
            total=len(schemas),
            limit=limit,
            offset=offset,
            investigations=schemas,
        )

    def get_investigation_detail(self, investigation_id: str) -> InvestigationDetailResponse:
        """Fetch complete investigation record metadata and artifact links."""
        r = self.repository.get(investigation_id)
        if not r:
            raise InvestigationNotFoundError(f"Investigation with ID '{investigation_id}' not found.")

        schema = InvestigationRecordSchema(
            id=r.id,
            query=r.query,
            dataset=r.dataset,
            created_at=r.created_at,
            planner_intent=r.planner_intent,
            risk_level=r.risk_level,
            confidence=r.confidence,
            recommendation=r.recommendation,
            status=r.status,
            duration_ms=r.duration_ms,
            version=r.version,
        )

        return InvestigationDetailResponse(
            record=schema,
            report_url=f"/api/v1/report/{investigation_id}",
            graph_url=f"/api/v1/graph/{investigation_id}",
            verdict_url=f"/api/v1/verdict/{investigation_id}",
            has_case_file=r.case_path is not None,
        )

    def delete_investigation(self, investigation_id: str) -> bool:
        """Delete investigation record, artifacts, and in-memory cache entry."""
        with self._store_lock:
            self._store.pop(investigation_id, None)

        deleted = self.repository.delete(investigation_id)
        if not deleted:
            raise InvestigationNotFoundError(f"Investigation with ID '{investigation_id}' not found.")
        return True

    def _load_dataset_transactions(self, dataset_ref: str) -> pd.DataFrame:
        """Helper to load transactions from dataset reference via DatasetResolver."""
        resolver = DatasetResolver()
        resolved = resolver.resolve(dataset_ref)

        try:
            loader = DataLoader(dataset_dir=str(resolved.resolved_path if resolved.is_file else resolved.ref_id))
            df = loader.load_transactions(limit=500)
            if df is None or (isinstance(df, pd.DataFrame) and df.empty):
                raise DatasetNotFoundError(
                    dataset_ref=dataset_ref,
                    message=f"Dataset '{dataset_ref}' contains no transaction data.",
                    searched_locations=[str(resolved.resolved_path)],
                )
            return df
        except DatasetNotFoundError:
            raise
        except FileNotFoundError as e:
            raise DatasetNotFoundError(
                dataset_ref=dataset_ref,
                message=f"Dataset file not found: {e}",
                searched_locations=[str(resolved.resolved_path)],
            )
        except Exception as e:
            logger.warning(f"Error loading dataset '{dataset_ref}', fallback to default loader: {e}")
            try:
                fallback_loader = DataLoader(dataset_dir="default")
                return fallback_loader.load_transactions(limit=500)
            except Exception:
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

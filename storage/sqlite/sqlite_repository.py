"""Concrete SQLite & File Storage Repository Implementation for TRIBUNAL."""

from __future__ import annotations

import datetime
import json
import logging
from pathlib import Path
import sqlite3
from typing import Any, Dict, List, Optional, Union

from storage.database import DatabaseManager, DEFAULT_DB_PATH
from storage.models import AuditRecord, GraphRecord, InvestigationRecord, ReportRecord, VerdictRecord
from storage.repositories.audit_repository import AuditRepository
from storage.repositories.graph_repository import GraphRepository
from storage.repositories.investigation_repository import InvestigationRepository
from storage.repositories.report_repository import ReportRepository
from storage.repositories.verdict_repository import VerdictRepository

logger = logging.getLogger("tribunal.storage.sqlite")


# Custom Storage Exceptions
class StorageError(Exception):
    """Base storage exception."""


class DatabaseUnavailableError(StorageError):
    """Raised when SQLite database cannot be accessed."""


class InvestigationAlreadyExistsError(StorageError):
    """Raised when attempting to insert a duplicate investigation ID."""


class StorageNotFoundError(StorageError):
    """Raised when requested investigation or artifact is missing."""


class PersistenceFailureError(StorageError):
    """Raised when atomic persistence operation fails."""


class SQLiteRepository(
    InvestigationRepository,
    ReportRepository,
    GraphRepository,
    VerdictRepository,
    AuditRepository,
):
    """Concrete repository implementation backing SQLite database and disk file storage."""

    def __init__(
        self,
        db_manager: Optional[DatabaseManager] = None,
        base_file_dir: Optional[Union[str, Path]] = None,
    ) -> None:
        self.db_manager = db_manager or DatabaseManager(DEFAULT_DB_PATH)
        self.base_file_dir = Path(base_file_dir or Path(__file__).resolve().parent.parent / "files")

        self.reports_dir = self.base_file_dir / "reports"
        self.graphs_dir = self.base_file_dir / "graphs"
        self.cases_dir = self.base_file_dir / "cases"
        self.audit_dir = self.base_file_dir / "audit"

        for d in [self.reports_dir, self.graphs_dir, self.cases_dir, self.audit_dir]:
            d.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------
    # InvestigationRepository Implementation
    # -------------------------------------------------------------------------

    def create(self, record: InvestigationRecord) -> InvestigationRecord:
        """Insert a new investigation record into SQLite DB."""
        if self.exists(record.id):
            raise InvestigationAlreadyExistsError(f"Investigation ID '{record.id}' already exists.")

        try:
            with self.db_manager.get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO investigations (
                        id, created_at, query, dataset, planner_intent, risk_level,
                        confidence, recommendation, status, duration_ms, version,
                        report_path, graph_path, case_path
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record.id,
                        record.created_at,
                        record.query,
                        record.dataset,
                        record.planner_intent,
                        record.risk_level,
                        record.confidence,
                        record.recommendation,
                        record.status,
                        record.duration_ms,
                        record.version,
                        record.report_path,
                        record.graph_path,
                        record.case_path,
                    ),
                )
                conn.commit()
            return record
        except sqlite3.Error as e:
            logger.error(f"Failed to create investigation record '{record.id}': {e}")
            raise PersistenceFailureError(f"Failed to store investigation record: {e}")

    def get(self, investigation_id: str) -> Optional[InvestigationRecord]:
        """Fetch investigation record by ID."""
        try:
            with self.db_manager.get_connection() as conn:
                cur = conn.execute("SELECT * FROM investigations WHERE id = ?", (investigation_id,))
                row = cur.fetchone()
                if not row:
                    return None
                return InvestigationRecord(**dict(row))
        except sqlite3.Error as e:
            logger.error(f"Failed to fetch investigation '{investigation_id}': {e}")
            raise DatabaseUnavailableError(f"Database query error: {e}")

    def list(self, limit: int = 50, offset: int = 0) -> List[InvestigationRecord]:
        """List investigation records ordered by creation date descending."""
        try:
            with self.db_manager.get_connection() as conn:
                cur = conn.execute(
                    "SELECT * FROM investigations ORDER BY created_at DESC LIMIT ? OFFSET ?",
                    (limit, offset),
                )
                rows = cur.fetchall()
                return [InvestigationRecord(**dict(r)) for r in rows]
        except sqlite3.Error as e:
            logger.error(f"Failed to list investigations: {e}")
            raise DatabaseUnavailableError(f"Database query error: {e}")

    def delete(self, investigation_id: str) -> bool:
        """Delete investigation record, associated database entries, and disk files."""
        if not self.exists(investigation_id):
            return False

        try:
            with self.db_manager.get_connection() as conn:
                conn.execute("DELETE FROM investigations WHERE id = ?", (investigation_id,))
                conn.commit()

            # Delete file artifacts if present
            file_candidates = [
                self.reports_dir / f"{investigation_id}.md",
                self.reports_dir / f"{investigation_id}.json",
                self.graphs_dir / f"{investigation_id}.json",
                self.cases_dir / f"{investigation_id}.json",
            ]
            for fc in file_candidates:
                if fc.exists():
                    try:
                        fc.unlink()
                    except OSError as err:
                        logger.warning(f"Could not delete artifact file '{fc}': {err}")

            self.record(investigation_id, "DELETED", {"status": "Deleted investigation and files"})
            return True
        except sqlite3.Error as e:
            logger.error(f"Failed to delete investigation '{investigation_id}': {e}")
            raise PersistenceFailureError(f"Failed to delete investigation: {e}")

    def exists(self, investigation_id: str) -> bool:
        """Check if an investigation ID exists."""
        try:
            with self.db_manager.get_connection() as conn:
                cur = conn.execute("SELECT 1 FROM investigations WHERE id = ?", (investigation_id,))
                return cur.fetchone() is not None
        except sqlite3.Error as e:
            logger.error(f"Database check failed for ID '{investigation_id}': {e}")
            raise DatabaseUnavailableError(f"Database error: {e}")

    # -------------------------------------------------------------------------
    # ReportRepository Implementation
    # -------------------------------------------------------------------------

    def save_report(self, investigation_id: str, markdown_content: str, json_payload: Dict[str, Any]) -> ReportRecord:
        """Save report content to files and insert DB record."""
        md_file = self.reports_dir / f"{investigation_id}.md"
        json_file = self.reports_dir / f"{investigation_id}.json"

        with open(md_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_payload, f, indent=2)

        record = ReportRecord(
            investigation_id=investigation_id,
            path=str(md_file),
            format="markdown",
        )

        try:
            with self.db_manager.get_connection() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO reports (investigation_id, path, format, generated_at) VALUES (?, ?, ?, ?)",
                    (record.investigation_id, record.path, record.format, record.generated_at),
                )
                conn.commit()
            return record
        except sqlite3.Error as e:
            logger.error(f"Failed to save report record for '{investigation_id}': {e}")
            raise PersistenceFailureError(f"Failed to store report metadata: {e}")

    def save(self, investigation_id: str, markdown_content: str, json_payload: Dict[str, Any]) -> ReportRecord:
        """Interface method for ReportRepository.save."""
        return self.save_report(investigation_id, markdown_content, json_payload)

    def load_report(self, investigation_id: str) -> Optional[Dict[str, Any]]:
        """Load report markdown and JSON payload by investigation ID."""
        md_file = self.reports_dir / f"{investigation_id}.md"
        json_file = self.reports_dir / f"{investigation_id}.json"

        if not md_file.exists() and not json_file.exists():
            return None

        markdown_content = ""
        if md_file.exists():
            with open(md_file, "r", encoding="utf-8") as f:
                markdown_content = f.read()

        json_payload = {}
        if json_file.exists():
            with open(json_file, "r", encoding="utf-8") as f:
                json_payload = json.load(f)

        return {
            "investigation_id": investigation_id,
            "markdown_content": markdown_content,
            "json_payload": json_payload,
        }

    def load(self, investigation_id: str) -> Optional[Dict[str, Any]]:
        """Interface method default to loading report."""
        return self.load_report(investigation_id)

    def export(self, investigation_id: str, target_path: str, format: str = "markdown") -> str:
        """Export report artifact to target file path."""
        report_data = self.load_report(investigation_id)
        if not report_data:
            raise StorageNotFoundError(f"Report for investigation '{investigation_id}' not found.")

        out_path = Path(target_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if format == "json":
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(report_data["json_payload"], f, indent=2)
        else:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(report_data["markdown_content"])
        return str(out_path)

    # -------------------------------------------------------------------------
    # GraphRepository Implementation
    # -------------------------------------------------------------------------

    def save_graph(self, investigation_id: str, graph_dict: Dict[str, Any]) -> GraphRecord:
        """Save Evidence Graph artifact to JSON file and insert DB record."""
        graph_file = self.graphs_dir / f"{investigation_id}.json"
        with open(graph_file, "w", encoding="utf-8") as f:
            json.dump(graph_dict, f, indent=2)

        node_count = len(graph_dict.get("nodes", []))
        edge_count = len(graph_dict.get("edges", []))

        record = GraphRecord(
            investigation_id=investigation_id,
            path=str(graph_file),
            node_count=node_count,
            edge_count=edge_count,
        )

        try:
            with self.db_manager.get_connection() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO graphs (investigation_id, path, node_count, edge_count) VALUES (?, ?, ?, ?)",
                    (record.investigation_id, record.path, record.node_count, record.edge_count),
                )
                conn.commit()
            return record
        except sqlite3.Error as e:
            logger.error(f"Failed to save graph record for '{investigation_id}': {e}")
            raise PersistenceFailureError(f"Failed to store graph metadata: {e}")

    def load_graph(self, investigation_id: str) -> Optional[Dict[str, Any]]:
        """Load graph structure by investigation ID."""
        graph_file = self.graphs_dir / f"{investigation_id}.json"
        if not graph_file.exists():
            return None
        with open(graph_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def statistics(self, investigation_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve graph record statistics."""
        try:
            with self.db_manager.get_connection() as conn:
                cur = conn.execute("SELECT * FROM graphs WHERE investigation_id = ?", (investigation_id,))
                row = cur.fetchone()
                if not row:
                    return None
                return dict(row)
        except sqlite3.Error as e:
            logger.error(f"Failed to fetch graph statistics for '{investigation_id}': {e}")
            raise DatabaseUnavailableError(f"Database error: {e}")

    # -------------------------------------------------------------------------
    # VerdictRepository Implementation
    # -------------------------------------------------------------------------

    def save_verdict(self, verdict_record: VerdictRecord) -> VerdictRecord:
        """Save Tribunal Verdict record."""
        try:
            with self.db_manager.get_connection() as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO verdicts (
                        investigation_id, winning_hypothesis, runner_up, confidence, recommendation
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        verdict_record.investigation_id,
                        verdict_record.winning_hypothesis,
                        verdict_record.runner_up,
                        verdict_record.confidence,
                        verdict_record.recommendation,
                    ),
                )
                conn.commit()
            return verdict_record
        except sqlite3.Error as e:
            logger.error(f"Failed to save verdict record for '{verdict_record.investigation_id}': {e}")
            raise PersistenceFailureError(f"Failed to store verdict: {e}")

    def load_verdict(self, investigation_id: str) -> Optional[VerdictRecord]:
        """Load Tribunal Verdict record."""
        try:
            with self.db_manager.get_connection() as conn:
                cur = conn.execute("SELECT * FROM verdicts WHERE investigation_id = ?", (investigation_id,))
                row = cur.fetchone()
                if not row:
                    return None
                return VerdictRecord(**dict(row))
        except sqlite3.Error as e:
            logger.error(f"Failed to load verdict for '{investigation_id}': {e}")
            raise DatabaseUnavailableError(f"Database error: {e}")

    # -------------------------------------------------------------------------
    # AuditRepository Implementation
    # -------------------------------------------------------------------------

    def record(self, investigation_id: str, event: str, details: Dict[str, Any] = None) -> AuditRecord:
        """Record an audit trail event in database and append to audit file."""
        details_dict = details or {}
        details_json = json.dumps(details_dict)
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

        try:
            with self.db_manager.get_connection() as conn:
                cur = conn.execute(
                    "INSERT INTO audit (investigation_id, event, timestamp, details) VALUES (?, ?, ?, ?)",
                    (investigation_id, event, timestamp, details_json),
                )
                audit_id = cur.lastrowid
                conn.commit()

            # Append to file audit log
            audit_file = self.audit_dir / f"{investigation_id}.json"
            audit_entries = []
            if audit_file.exists():
                try:
                    with open(audit_file, "r", encoding="utf-8") as f:
                        audit_entries = json.load(f)
                except Exception:
                    audit_entries = []

            audit_entries.append({
                "id": audit_id,
                "investigation_id": investigation_id,
                "event": event,
                "timestamp": timestamp,
                "details": details_dict,
            })

            with open(audit_file, "w", encoding="utf-8") as f:
                json.dump(audit_entries, f, indent=2)

            return AuditRecord(
                id=audit_id,
                investigation_id=investigation_id,
                event=event,
                timestamp=timestamp,
                details=details_dict,
            )
        except sqlite3.Error as e:
            logger.error(f"Failed to record audit event for '{investigation_id}': {e}")
            raise PersistenceFailureError(f"Failed to record audit event: {e}")

    def history(self, investigation_id: str) -> List[AuditRecord]:
        """Fetch audit trail history for investigation ID."""
        try:
            with self.db_manager.get_connection() as conn:
                cur = conn.execute(
                    "SELECT * FROM audit WHERE investigation_id = ? ORDER BY id ASC",
                    (investigation_id,),
                )
                rows = cur.fetchall()
                records = []
                for r in rows:
                    row_dict = dict(r)
                    d_json = row_dict.get("details", "{}")
                    try:
                        details_obj = json.loads(d_json) if isinstance(d_json, str) else d_json
                    except Exception:
                        details_obj = {}
                    records.append(
                        AuditRecord(
                            id=row_dict["id"],
                            investigation_id=row_dict["investigation_id"],
                            event=row_dict["event"],
                            timestamp=row_dict["timestamp"],
                            details=details_obj,
                        )
                    )
                return records
        except sqlite3.Error as e:
            logger.error(f"Failed to fetch audit history for '{investigation_id}': {e}")
            raise DatabaseUnavailableError(f"Database error: {e}")

    # -------------------------------------------------------------------------
    # Atomic Multi-Artifact Save Helper
    # -------------------------------------------------------------------------

    def save_full_investigation(
        self,
        record: InvestigationRecord,
        markdown_report: str,
        json_report: Dict[str, Any],
        graph_dict: Dict[str, Any],
        verdict_record: VerdictRecord,
        case_file_dict: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Atomically persist investigation record, reports, graph, verdict, case file, and audit trail."""
        created_files = []
        try:
            # 1. Write disk files
            md_file = self.reports_dir / f"{record.id}.md"
            json_report_file = self.reports_dir / f"{record.id}.json"
            graph_file = self.graphs_dir / f"{record.id}.json"
            case_file_path = self.cases_dir / f"{record.id}.json"

            with open(md_file, "w", encoding="utf-8") as f:
                f.write(markdown_report)
            created_files.append(md_file)

            with open(json_report_file, "w", encoding="utf-8") as f:
                json.dump(json_report, f, indent=2)
            created_files.append(json_report_file)

            with open(graph_file, "w", encoding="utf-8") as f:
                json.dump(graph_dict, f, indent=2)
            created_files.append(graph_file)

            if case_file_dict:
                with open(case_file_path, "w", encoding="utf-8") as f:
                    json.dump(case_file_dict, f, indent=2)
                created_files.append(case_file_path)

            record.report_path = str(md_file)
            record.graph_path = str(graph_file)
            record.case_path = str(case_file_path) if case_file_dict else None

            node_count = len(graph_dict.get("nodes", []))
            edge_count = len(graph_dict.get("edges", []))

            # 2. Database atomic transaction
            with self.db_manager.get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO investigations (
                        id, created_at, query, dataset, planner_intent, risk_level,
                        confidence, recommendation, status, duration_ms, version,
                        report_path, graph_path, case_path
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record.id,
                        record.created_at,
                        record.query,
                        record.dataset,
                        record.planner_intent,
                        record.risk_level,
                        record.confidence,
                        record.recommendation,
                        record.status,
                        record.duration_ms,
                        record.version,
                        record.report_path,
                        record.graph_path,
                        record.case_path,
                    ),
                )

                conn.execute(
                    "INSERT INTO reports (investigation_id, path, format, generated_at) VALUES (?, ?, ?, ?)",
                    (record.id, str(md_file), "markdown", record.created_at),
                )

                conn.execute(
                    "INSERT INTO graphs (investigation_id, path, node_count, edge_count) VALUES (?, ?, ?, ?)",
                    (record.id, str(graph_file), node_count, edge_count),
                )

                conn.execute(
                    """
                    INSERT INTO verdicts (
                        investigation_id, winning_hypothesis, runner_up, confidence, recommendation
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        record.id,
                        verdict_record.winning_hypothesis,
                        verdict_record.runner_up,
                        verdict_record.confidence,
                        verdict_record.recommendation,
                    ),
                )

                conn.commit()

            # 3. Record audit trail
            self.record(record.id, "PERSISTED", {"status": "Successfully persisted all artifacts"})

        except Exception as e:
            logger.error(f"Atomic persistence failed for investigation '{record.id}': {e}. Rolling back files.")
            for f_path in created_files:
                if f_path.exists():
                    try:
                        f_path.unlink()
                    except OSError:
                        pass
            raise PersistenceFailureError(f"Atomic persistence failed: {e}")

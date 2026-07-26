"""Abstract Report Repository interface and Report Annotation repository."""

from __future__ import annotations

import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from storage.database import DatabaseManager, DEFAULT_DB_PATH
from storage.models import ReportRecord


class ReportRepository(ABC):
    """Abstract interface for storing and retrieving report artifacts."""

    @abstractmethod
    def save(self, investigation_id: str, markdown_content: str, json_payload: Dict[str, Any]) -> ReportRecord:
        """Save report content to storage and return ReportRecord."""

    @abstractmethod
    def load(self, investigation_id: str) -> Optional[Dict[str, Any]]:
        """Load report data (markdown content, json payload, metadata) by investigation ID."""

    @abstractmethod
    def export(self, investigation_id: str, target_path: str, format: str = "markdown") -> str:
        """Export report artifact to specified path and format."""


@dataclass
class ReportAnnotation:
    id: int
    investigation_id: str
    author: str
    text: str
    created_at: str


class ReportAnnotationRepository:
    """Repository for managing investigator notes attached to reports."""

    def __init__(self, db_manager: Optional[DatabaseManager] = None) -> None:
        self.db_manager = db_manager or DatabaseManager(DEFAULT_DB_PATH)

    def add_annotation(self, investigation_id: str, author: str, text: str) -> ReportAnnotation:
        created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO report_annotations (investigation_id, author, text, created_at) VALUES (?, ?, ?, ?)",
                (investigation_id, author, text, created_at),
            )
            note_id = cur.lastrowid
            conn.commit()
            return ReportAnnotation(
                id=note_id,
                investigation_id=investigation_id,
                author=author,
                text=text,
                created_at=created_at,
            )

    def get_annotations(self, investigation_id: str) -> List[ReportAnnotation]:
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(
                "SELECT * FROM report_annotations WHERE investigation_id = ? ORDER BY id ASC",
                (investigation_id,),
            )
            rows = cur.fetchall()
            return [
                ReportAnnotation(
                    id=row["id"],
                    investigation_id=row["investigation_id"],
                    author=row["author"],
                    text=row["text"],
                    created_at=row["created_at"],
                )
                for row in rows
            ]

    def delete_annotation(self, note_id: int) -> bool:
        with self.db_manager.get_connection() as conn:
            cur = conn.execute("DELETE FROM report_annotations WHERE id = ?", (note_id,))
            conn.commit()
            return cur.rowcount > 0


def render_compliance_html(
    investigation_id: str,
    title: str,
    markdown_text: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """Render HTML document with compliance styling for print/pdf export."""
    metadata_dict = metadata or {}
    risk = metadata_dict.get("risk_level", "MEDIUM")
    confidence = metadata_dict.get("confidence", 0.0)
    gen_at = metadata_dict.get("generated_at", "")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TRIBUNAL Report - {investigation_id}</title>
    <style>
        body {{ font-family: monospace; color: #0f172a; margin: 2rem; background: #ffffff; }}
        h1, h2, h3 {{ color: #0284c7; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem; }}
        .header {{ border: 2px solid #0284c7; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; }}
        .badge {{ font-weight: bold; padding: 0.25rem 0.5rem; border-radius: 0.25rem; background: #e0f2fe; color: #0369a1; }}
        .content {{ line-height: 1.6; white-space: pre-wrap; }}
        @media print {{ body {{ margin: 0; }} }}
    </style>
</head>
<body>
    <div class="header">
        <h1>TRIBUNAL AML Investigation Report</h1>
        <p><strong>Case ID:</strong> {investigation_id}</p>
        <p><strong>Risk Level:</strong> <span class="badge">{risk}</span> | <strong>Confidence:</strong> {confidence}</p>
        <p><strong>Generated At:</strong> {gen_at}</p>
    </div>
    <div class="content">
{markdown_text}
    </div>
</body>
</html>"""
    return html_content

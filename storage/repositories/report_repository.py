"""Abstract Report Repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

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

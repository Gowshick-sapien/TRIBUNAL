"""Abstract Audit Repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from storage.models import AuditRecord


class AuditRepository(ABC):
    """Abstract interface for recording and querying audit trail events."""

    @abstractmethod
    def record(self, investigation_id: str, event: str, details: Dict[str, Any] = None) -> AuditRecord:
        """Record an audit trail event."""

    @abstractmethod
    def history(self, investigation_id: str) -> List[AuditRecord]:
        """Fetch audit trail history for an investigation ID."""

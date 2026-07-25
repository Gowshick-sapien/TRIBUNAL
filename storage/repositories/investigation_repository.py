"""Abstract Investigation Repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from storage.models import InvestigationRecord


class InvestigationRepository(ABC):
    """Abstract interface for storing and querying investigation metadata records."""

    @abstractmethod
    def create(self, record: InvestigationRecord) -> InvestigationRecord:
        """Create and persist a new investigation record."""

    @abstractmethod
    def get(self, investigation_id: str) -> Optional[InvestigationRecord]:
        """Fetch investigation record by ID."""

    @abstractmethod
    def list(self, limit: int = 50, offset: int = 0) -> List[InvestigationRecord]:
        """List investigation records ordered by creation date descending."""

    @abstractmethod
    def delete(self, investigation_id: str) -> bool:
        """Delete investigation record and associated artifacts."""

    @abstractmethod
    def exists(self, investigation_id: str) -> bool:
        """Check if an investigation record exists."""

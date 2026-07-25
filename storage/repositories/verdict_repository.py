"""Abstract Tribunal Verdict Repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from storage.models import VerdictRecord


class VerdictRepository(ABC):
    """Abstract interface for storing and retrieving Tribunal Verdict summaries."""

    @abstractmethod
    def save(self, verdict_record: VerdictRecord) -> VerdictRecord:
        """Save Tribunal Verdict record."""

    @abstractmethod
    def load(self, investigation_id: str) -> Optional[VerdictRecord]:
        """Load Tribunal Verdict record by investigation ID."""

"""Abstract Evidence Graph Repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from storage.models import GraphRecord


class GraphRepository(ABC):
    """Abstract interface for storing and retrieving Evidence Graph artifacts."""

    @abstractmethod
    def save(self, investigation_id: str, graph_dict: Dict[str, Any]) -> GraphRecord:
        """Save Evidence Graph structure to storage and return GraphRecord."""

    @abstractmethod
    def load(self, investigation_id: str) -> Optional[Dict[str, Any]]:
        """Load Evidence Graph dictionary by investigation ID."""

    @abstractmethod
    def statistics(self, investigation_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve graph statistics for investigation ID."""

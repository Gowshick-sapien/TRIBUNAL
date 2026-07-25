"""Evidence Graph Builder — interface only."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tribunal.models.evidence_graph import EvidenceGraph
    from tribunal.models.investigation_card import InvestigationCard


class GraphBuilder:
    """Translates Investigation Cards into a directed evidence graph."""

    def build(self, cards: list[InvestigationCard]) -> EvidenceGraph:
        """Build evidence graph from investigation cards."""
        ...

    def rebuild(self, cards: list[InvestigationCard]) -> EvidenceGraph:
        """Rebuild graph after adaptive re-investigation adds new cards."""
        ...

"""Tribunal Consensus Engine — interface only."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tribunal.models.case_file import CaseFile
    from tribunal.models.evidence_graph import EvidenceGraph
    from tribunal.models.tribunal_verdict import TribunalVerdict


class Tribunal:
    """Reasons over the evidence graph to produce a structured verdict."""

    def deliberate(
        self,
        graph: EvidenceGraph,
        case_file: CaseFile,
    ) -> TribunalVerdict:
        """Compute net support, rank hypotheses, and map to recommendation."""
        ...

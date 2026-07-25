"""Defense Agent — interface only."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import pandas as pd

    from tribunal.models.case_file import CaseFile
    from tribunal.models.evidence_graph import EvidenceGraph
    from tribunal.models.investigation_card import InvestigationCard


class DefenseAgent:
    """Challenges the dominant hypothesis with a legitimate counter-explanation."""

    def challenge(
        self,
        case_file: CaseFile,
        graph: EvidenceGraph,
        transactions: pd.DataFrame,
    ) -> tuple[EvidenceGraph, Optional[InvestigationCard]]:
        """Argue against dominant hypothesis; add contradiction edge if plausible."""
        ...

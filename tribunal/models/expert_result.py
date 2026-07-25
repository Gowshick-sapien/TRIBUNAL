"""Expert result contract."""

from __future__ import annotations

from dataclasses import dataclass

from tribunal.models.case_file import CaseFile
from tribunal.models.investigation_card import InvestigationCard


@dataclass
class ExpertResult:
    cards: list[InvestigationCard]
    case_file: CaseFile

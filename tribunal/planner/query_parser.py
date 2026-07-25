"""Query Parser — interface only."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tribunal.models.investigation_plan import InvestigationPlan
    from tribunal.models.user_query import UserQuery


class QueryParser:
    """Transforms natural language into a structured InvestigationPlan."""

    def parse(self, query: UserQuery) -> InvestigationPlan:
        """Parse a user query into an InvestigationPlan."""
        ...

    def parse_text(self, query_text: str) -> InvestigationPlan:
        """Convenience wrapper accepting raw query string."""
        ...

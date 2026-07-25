"""FastAPI Dependency Injection helpers for TRIBUNAL REST API."""

from typing import Generator
from api.services.investigation_service import InvestigationService

# Global service singleton instance
_investigation_service_instance: InvestigationService | None = None


def get_investigation_service() -> InvestigationService:
    """Dependency provider for InvestigationService singleton instance."""
    global _investigation_service_instance
    if _investigation_service_instance is None:
        _investigation_service_instance = InvestigationService()
    return _investigation_service_instance

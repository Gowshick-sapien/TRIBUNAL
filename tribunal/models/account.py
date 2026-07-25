"""Account model representing a bank account and its entity metadata."""

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Account:
    """Canonical Account data model.
    
    Attributes:
        bank_name: Name of the bank
        bank_id: Unique bank identifier
        account_number: Account identifier number/code
        entity_id: Owner entity identifier
        entity_name: Owner entity name (e.g., Corporation #1234, Individual, etc.)
    """

    bank_name: str
    bank_id: str
    account_number: str
    entity_id: str
    entity_name: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert Account instance to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Account":
        """Create Account instance from dictionary."""
        return cls(
            bank_name=str(data["bank_name"]),
            bank_id=str(data["bank_id"]),
            account_number=str(data["account_number"]),
            entity_id=str(data["entity_id"]),
            entity_name=str(data["entity_name"]),
        )

"""Transaction model representing an individual financial transaction."""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Transaction:
    """Canonical Transaction data model.
    
    Attributes:
        timestamp: Transaction datetime object
        from_bank: Originating bank identifier
        from_account: Originating account identifier
        to_bank: Destination bank identifier
        to_account: Destination account identifier
        amount_received: Amount received by beneficiary
        receiving_currency: Currency of amount received
        amount_paid: Amount paid by remitter
        payment_currency: Currency of amount paid
        payment_format: Format/channel of payment (e.g. ACH, Cheque, Credit Card, Reinvestment)
        is_laundering: Label indicating whether transaction is laundering (1) or benign (0)
        transaction_id: Unique identifier generated or assigned to transaction
    """

    timestamp: datetime
    from_bank: str
    from_account: str
    to_bank: str
    to_account: str
    amount_received: float
    receiving_currency: str
    amount_paid: float
    payment_currency: str
    payment_format: str
    is_laundering: int = 0
    transaction_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary with ISO timestamp format."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Transaction":
        """Create Transaction instance from dictionary."""
        ts = data["timestamp"]
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts)
        return cls(
            timestamp=ts,
            from_bank=str(data["from_bank"]),
            from_account=str(data["from_account"]),
            to_bank=str(data["to_bank"]),
            to_account=str(data["to_account"]),
            amount_received=float(data["amount_received"]),
            receiving_currency=str(data["receiving_currency"]),
            amount_paid=float(data["amount_paid"]),
            payment_currency=str(data["payment_currency"]),
            payment_format=str(data["payment_format"]),
            is_laundering=int(data.get("is_laundering", 0)),
            transaction_id=data.get("transaction_id"),
        )

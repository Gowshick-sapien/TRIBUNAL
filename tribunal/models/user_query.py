"""User query input contract."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class UserQuery:
    text: str
    submitted_at: str | None = None
    session_id: str | None = None

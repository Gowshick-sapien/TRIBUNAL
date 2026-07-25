"""Deliberation Trace — Records step-by-step audit lineage of Tribunal deliberation."""

from __future__ import annotations

import datetime
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TraceStep:
    step_number: int
    stage_name: str
    description: str
    decision_id: str = field(default_factory=lambda: f"dec_{uuid.uuid4().hex[:6]}")
    step_duration_ms: float = 0.0
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


class DeliberationTrace:
    """Maintains a complete reconstructable trace of every decision during Tribunal deliberation."""

    def __init__(self) -> None:
        self.steps: list[TraceStep] = []
        self._counter: int = 1

    def add_step(
        self,
        stage_name: str,
        description: str,
        data: dict[str, Any] | None = None,
        step_duration_ms: float = 0.0,
    ) -> TraceStep:
        dec_id = f"dec_{uuid.uuid4().hex[:6]}"
        step = TraceStep(
            step_number=self._counter,
            stage_name=stage_name,
            description=description,
            decision_id=dec_id,
            step_duration_ms=round(step_duration_ms, 3),
            data=data or {},
        )
        self.steps.append(step)
        self._counter += 1
        return step

    def to_dict_list(self) -> list[dict[str, Any]]:
        return [
            {
                "step_number": s.step_number,
                "stage_name": s.stage_name,
                "decision_id": s.decision_id,
                "step_duration_ms": s.step_duration_ms,
                "description": s.description,
                "data": s.data,
                "timestamp": s.timestamp,
            }
            for s in self.steps
        ]

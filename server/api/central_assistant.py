"""API-facing contract for the single human-facing GABON 360 AI."""
from __future__ import annotations
from typing import Any

from monitoring.central_ai_orchestrator import CentralAIOrchestrator
from monitoring.continuous_monitor import ContinuousMonitor

_monitor = ContinuousMonitor()
_central = CentralAIOrchestrator()


def get_central_situation(lookback_hours: int = 168, limit: int = 50) -> dict[str, Any]:
    snapshot = _monitor.poll(lookback_hours=lookback_hours, limit=limit)
    packets = snapshot.get("observations", [])
    # Existing monitor observations are preserved as evidence; the central AI
    # is only the human-facing fusion layer.
    return _central.ingest(packets)


def ask_central_ai(message: str, situation: dict[str, Any] | None = None) -> dict[str, Any]:
    return _central.answer(message, situation)

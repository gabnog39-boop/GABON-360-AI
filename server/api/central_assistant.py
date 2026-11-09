"""API-facing contract for the single human-facing GABON 360 AI."""
from __future__ import annotations
from typing import Any

from monitoring.central_ai_orchestrator import CentralAIOrchestrator
from monitoring.runtime import monitor as _monitor

_central = CentralAIOrchestrator()


def get_central_situation(lookback_hours: int = 168, limit: int = 50) -> dict[str, Any]:
    snapshot = _monitor.poll(lookback_hours=lookback_hours, limit=limit)
    packets = []
    for observation in snapshot.get("observations", []):
        if isinstance(observation, dict):
            packets.append(observation)
    for alert in snapshot.get("alert_candidates", []):
        if isinstance(alert, dict):
            packets.append({
                **alert,
                "kind": "alert",
                "domain": alert.get("type") or "alertes",
                "priority": alert.get("severity") or "WARNING",
            })
    result = _central.ingest(packets)
    result["monitor_snapshot"] = {
        "checked_at": snapshot.get("checked_at"),
        "coverage": snapshot.get("coverage"),
        "new_observations": snapshot.get("new_observations", 0),
        "alert_candidates": len(snapshot.get("alert_candidates", [])),
        "live_video": snapshot.get("live_video", False),
    }
    return result


def ask_central_ai(message: str, situation: dict[str, Any] | None = None) -> dict[str, Any]:
    return _central.answer(message, situation)

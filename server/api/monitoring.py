"""API-facing monitoring snapshot for the GABON 360 AI situation center."""
from __future__ import annotations

from monitoring.continuous_monitor import ContinuousMonitor
from api.monitoring_contract import build_situation_contract

_monitor = ContinuousMonitor()


def get_situation_overview(lookback_hours: int = 168, limit: int = 20) -> dict:
    """Run one catalog check and return the automatic surveillance snapshot."""
    snapshot = _monitor.poll(lookback_hours=lookback_hours, limit=limit)
    contract = build_situation_contract(snapshot)
    contract["observations"] = snapshot["observations"]
    contract["validation_required"] = snapshot["human_validation_required"]
    return contract


def get_monitor_health() -> dict:
    return _monitor.health()

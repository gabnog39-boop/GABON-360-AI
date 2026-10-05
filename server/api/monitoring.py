"""API-facing monitoring snapshot for the GABON 360 AI situation center."""
from __future__ import annotations

from monitoring.continuous_monitor import ContinuousMonitor

_monitor = ContinuousMonitor()


def get_situation_overview(lookback_hours: int = 168, limit: int = 20) -> dict:
    """Run one catalog check and return the automatic surveillance snapshot."""
    snapshot = _monitor.poll(lookback_hours=lookback_hours, limit=limit)
    return {
        "coverage": "Gabon",
        "automatic_surveillance": True,
        "selection_required": False,
        "status": snapshot["status"],
        "checked_at": snapshot["checked_at"],
        "new_observations": snapshot["new_observations"],
        "observations": snapshot["observations"],
        "alerts": snapshot["alert_candidates"],
        "validation_required": snapshot["human_validation_required"],
        "live_satellite_video": False,
    }


def get_monitor_health() -> dict:
    return _monitor.health()

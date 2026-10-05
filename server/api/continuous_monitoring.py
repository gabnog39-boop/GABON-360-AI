"""API-facing helpers for the autonomous Gabon monitoring layer."""
from __future__ import annotations

from monitoring.continuous_monitor import ContinuousMonitor

_monitor = ContinuousMonitor()


def run_monitoring_cycle(lookback_hours: int = 168, limit: int = 20) -> dict:
    """Run one automatic whole-Gabon catalog check."""
    return _monitor.poll(lookback_hours=lookback_hours, limit=limit)


def monitoring_overview() -> dict:
    """Return monitoring status for the Centre national de situation."""
    return _monitor.health()

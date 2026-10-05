"""Alert API helpers for the GABON 360 AI situation center."""
from __future__ import annotations

from monitoring.continuous_monitor import ContinuousMonitor

_monitor = ContinuousMonitor()


def get_alerts(limit: int = 50) -> dict:
    if limit < 1 or limit > 200:
        raise ValueError("limit must be between 1 and 200")
    alerts = list(reversed(_monitor.alerts[-limit:]))
    return {
        "coverage": "Gabon",
        "alerts": alerts,
        "count": len(alerts),
        "validation_required": True,
        "automatic_surveillance": True,
    }

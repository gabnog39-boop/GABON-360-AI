"""Unified control-center API helpers."""
from __future__ import annotations

from monitoring.center_state import build_center_state
from monitoring.continuous_monitor import ContinuousMonitor

_monitor = ContinuousMonitor()


def get_center_state() -> dict:
    health = _monitor.health()
    return build_center_state(health, alerts_total=len(_monitor.alerts))

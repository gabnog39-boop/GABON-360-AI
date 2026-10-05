"""Stable response contract consumed by the Android situation center."""
from __future__ import annotations

from typing import Any


def build_situation_contract(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "1.0",
        "centre": "GABON 360 AI",
        "coverage": "Gabon",
        "automatic_surveillance": True,
        "selection_required": False,
        "status": snapshot.get("status", "unknown"),
        "checked_at": snapshot.get("checked_at"),
        "observation_count": snapshot.get("new_observations", 0),
        "alerts": snapshot.get("alert_candidates", []),
        "alerts_total": snapshot.get("alerts_total", 0),
        "map_action": "center_on_alert_geometry",
        "manual_action": "analyser_cette_zone",
        "live_satellite_video": False,
        "human_validation_required": True,
        "source_policy": "authorized_or_public_observations_only",
    }

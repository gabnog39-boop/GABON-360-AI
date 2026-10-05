"""Unified state model for the future GABON 360 AI control center."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from monitoring.domain_registry import domain_summary


def build_center_state(monitor_health: dict[str, Any], alerts_total: int = 0) -> dict[str, Any]:
    """Build a screen-friendly national situation snapshot."""
    return {
        "centre": "GABON 360 AI",
        "mode": "national_situation_center",
        "coverage": "Gabon",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "surveillance": {
            "automatic": True,
            "status": monitor_health.get("status", "unknown"),
            "last_check": monitor_health.get("last_check"),
            "selection_required": False,
        },
        "alerts": {
            "total": alerts_total,
            "validation_required": True,
            "map_action": "center_on_alert_geometry",
        },
        "domains": domain_summary(),
        "display_modes": ["mobile", "tablet", "desktop", "wall_display"],
        "source_policy": "public_or_authorized_sources_only",
        "live_satellite_video": False,
    }

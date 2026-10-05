"""Continuous territory monitoring coordinator for GABON 360 AI.

The coordinator periodically checks permitted public observation catalogs for
new Gabon-wide products and sends newly discovered observations through the
central-AI review boundary. It does not claim continuous live satellite video.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from integrations.satellite.cdse_service import discover_gabon_satellite_data
from integrations.satellite.central_ai import analyze_observation


class ContinuousMonitor:
    """Stateful coordinator for scheduled, Gabon-wide observation checks."""

    def __init__(self) -> None:
        self.last_check: datetime | None = None
        self.seen_product_ids: set[str] = set()

    def poll(self, lookback_hours: int = 168, limit: int = 20) -> dict[str, Any]:
        """Check for recent public observations without requiring map selection."""
        if not 1 <= lookback_hours <= 720:
            raise ValueError("lookback_hours must be between 1 and 720")

        now = datetime.now(timezone.utc)
        start = now - timedelta(hours=lookback_hours)
        discovery = discover_gabon_satellite_data(
            datetime_range=f"{start.isoformat().replace('+00:00', 'Z')}/{now.isoformat().replace('+00:00', 'Z')}",
            cloud_cover_max=60,
            limit=limit,
        )

        new_records = []
        for record in discovery.get("records", []):
            product_id = record.get("id")
            if not product_id or product_id in self.seen_product_ids:
                continue
            self.seen_product_ids.add(product_id)
            new_records.append(record)

        self.last_check = now
        return {
            "monitor": "gabon_wide_continuous_observation_monitor",
            "checked_at": now.isoformat(),
            "coverage": "Gabon",
            "selection_required": False,
            "live_video": False,
            "new_observations": len(new_records),
            "observations": new_records,
            "alert_candidates": [],
            "status": "monitoring",
            "human_validation_required": True,
        }

    def health(self) -> dict[str, Any]:
        """Return monitor state for the Centre national de situation."""
        return {
            "status": "running" if self.last_check else "ready",
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "selection_required": False,
            "coverage": "Gabon",
        }

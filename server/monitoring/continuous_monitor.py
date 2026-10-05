"""Continuous whole-Gabon monitoring coordinator."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from integrations.satellite.cdse_service import discover_gabon_satellite_data
from integrations.satellite.central_ai import analyze_observation
from integrations.satellite.change_detection import compare_indicators

STATE_FILE = Path(__file__).resolve().parents[2] / "monitoring_state.json"


class ContinuousMonitor:
    """Persistent coordinator for scheduled, Gabon-wide observation checks."""

    def __init__(self) -> None:
        self.last_check: datetime | None = None
        self.seen_product_ids: set[str] = set()
        self.previous_indicators: dict[str, dict[str, Any]] = {}
        self.alerts: list[dict[str, Any]] = []
        self._load_state()

    def _load_state(self) -> None:
        if not STATE_FILE.exists():
            return
        try:
            state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            self.seen_product_ids = set(state.get("seen_product_ids", []))
            self.previous_indicators = state.get("previous_indicators", {})
            self.alerts = state.get("alerts", [])[-100:]
            value = state.get("last_check")
            if value:
                self.last_check = datetime.fromisoformat(value)
        except (OSError, ValueError, TypeError):
            # Corrupt state must never prevent a new monitoring cycle.
            self.seen_product_ids = set()
            self.previous_indicators = {}
            self.alerts = []

    def _save_state(self) -> None:
        state = {
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "seen_product_ids": sorted(self.seen_product_ids),
            "previous_indicators": self.previous_indicators,
            "alerts": self.alerts[-100:],
        }
        STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def _record_to_observation(record: dict[str, Any]) -> dict[str, Any]:
        """Create a metadata observation packet for central-AI screening."""
        return {
            "source": "copernicus_sentinel_2_l2a",
            "kind": "satellite_catalog_observation",
            "bbox_wgs84": record.get("geometry"),
            "time_range": {"from": record.get("datetime"), "to": record.get("datetime")},
            "image": {"base64": ""},
            "ndvi": {"base64": ""},
            "catalog_record": record,
            "live": False,
            "simulation": False,
        }

    def poll(self, lookback_hours: int = 168, limit: int = 20) -> dict[str, Any]:
        """Check all Gabon for new public observations without zone selection."""
        if not 1 <= lookback_hours <= 720:
            raise ValueError("lookback_hours must be between 1 and 720")
        now = datetime.now(timezone.utc)
        start = now - timedelta(hours=lookback_hours)
        discovery = discover_gabon_satellite_data(
            datetime_range=f"{start.isoformat().replace('+00:00', 'Z')}/{now.isoformat().replace('+00:00', 'Z')}",
            cloud_cover_max=60,
            limit=limit,
        )

        new_records: list[dict[str, Any]] = []
        cycle_alerts: list[dict[str, Any]] = []
        for record in discovery.get("records", []):
            product_id = record.get("id")
            if not product_id or product_id in self.seen_product_ids:
                continue
            self.seen_product_ids.add(product_id)
            new_records.append(record)

            observation = self._record_to_observation(record)
            analysis = analyze_observation(observation)
            # Metadata alone cannot establish a physical anomaly. Real image-derived
            # indicators are accepted when an authorized processor supplies them.
            key = str(record.get("collection") or "sentinel")
            current_indicators = record.get("derived_indicators") or {}
            if current_indicators:
                comparison = compare_indicators(current_indicators, self.previous_indicators.get(key))
                observation["derived_indicators"] = comparison
                analysis = analyze_observation(observation)
                self.previous_indicators[key] = current_indicators
            for finding in analysis.get("findings", []):
                alert = {
                    "alert_id": f"g360-alert-{product_id}",
                    "product_id": product_id,
                    "zone": record.get("geometry"),
                    "observed_at": record.get("datetime"),
                    "source": record.get("collection"),
                    "type": finding.get("type"),
                    "label": finding.get("label"),
                    "confidence": finding.get("confidence"),
                    "evidence": finding.get("evidence"),
                    "status": "À vérifier",
                    "requires_human_validation": True,
                }
                cycle_alerts.append(alert)

        self.alerts.extend(cycle_alerts)
        self.last_check = now
        self._save_state()
        return {
            "monitor": "gabon_wide_continuous_observation_monitor",
            "checked_at": now.isoformat(),
            "coverage": "Gabon",
            "selection_required": False,
            "live_video": False,
            "new_observations": len(new_records),
            "observations": new_records,
            "alert_candidates": cycle_alerts,
            "alerts_total": len(self.alerts),
            "status": "monitoring",
            "human_validation_required": True,
        }

    def health(self) -> dict[str, Any]:
        return {
            "status": "running" if self.last_check else "ready",
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "selection_required": False,
            "coverage": "Gabon",
            "alerts_total": len(self.alerts),
        }

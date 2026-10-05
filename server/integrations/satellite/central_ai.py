"""Central-AI boundary for GABON 360 AI satellite observations.

The central layer returns structured, reviewable findings rather than pretending
that an image alone proves an incident. Sensitive conclusions remain pending
human validation.
"""
from __future__ import annotations

from datetime import datetime, timezone


def analyze_observation(packet: dict) -> dict:
    """Normalize an observation for the central AI and operator review queue."""
    source = packet.get("source", "unknown")
    bbox = packet.get("bbox_wgs84")
    time_range = packet.get("time_range", {})
    has_image = bool(packet.get("image", {}).get("base64"))
    has_ndvi = bool(packet.get("ndvi", {}).get("base64"))

    return {
        "analysis_id": f"g360-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "source": source,
        "kind": packet.get("kind", "observation"),
        "area": {"bbox_wgs84": bbox},
        "time_range": time_range,
        "inputs": {
            "image_received": has_image,
            "ndvi_received": has_ndvi,
        },
        "findings": [],
        "status": "ready_for_central_ai_analysis",
        "validation": {
            "required": True,
            "state": "pending_human_validation",
        },
        "live": bool(packet.get("live", False)),
        "simulation": False,
        "message": "Observation reçue. Aucune anomalie n'est affirmée sans analyse et validation.",
    }

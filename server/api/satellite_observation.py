"""HTTP-facing satellite observation boundary for GABON 360 AI.

This module keeps Copernicus credentials on the server and exposes only a
validated observation request to the Android client. Protected/live sources
remain disabled until explicitly authorized and connected.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from ..integrations.satellite.transmitter_service import request_observation


GABON_BBOX = (8.5, -4.0, 14.5, 2.5)
MAX_PIXELS = 4096


def _iso_datetime(value: str) -> str:
    """Validate an ISO-8601 datetime and return a normalized UTC string."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("datetime must include a timezone")
    return parsed.isoformat().replace("+00:00", "Z")


def build_satellite_observation(request: dict[str, Any]) -> dict[str, Any]:
    """Build an observation response from a client request.

    The Android app sends an AOI and time range. Secrets are never accepted
    from the client. The response is explicitly an observation, not live video.
    """
    bbox = tuple(request.get("bbox", GABON_BBOX))
    if len(bbox) != 4:
        raise ValueError("bbox must contain west,south,east,north")
    west, south, east, north = map(float, bbox)
    if not (-180 <= west < east <= 180 and -90 <= south < north <= 90):
        raise ValueError("invalid bbox")

    start = _iso_datetime(str(request["start"]))
    end = _iso_datetime(str(request["end"]))
    if start >= end:
        raise ValueError("start must be before end")

    width = max(256, min(int(request.get("width", 1024)), MAX_PIXELS))
    height = max(256, min(int(request.get("height", 1024)), MAX_PIXELS))
    cloud = max(0.0, min(float(request.get("max_cloud_cover", 60)), 100.0))
    include_ndvi = bool(request.get("include_ndvi", True))

    packet = request_observation(
        (west, south, east, north),
        start,
        end,
        width=width,
        height=height,
        max_cloud_cover=cloud,
        include_ndvi=include_ndvi,
    )

    packet["api"] = {
        "status": "ready_for_central_ai_analysis",
        "live": False,
        "source_type": "public_satellite_observation",
        "human_validation_required_for_operational_decisions": True,
    }
    return packet

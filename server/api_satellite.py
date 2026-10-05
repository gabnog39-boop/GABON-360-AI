"""Application-facing satellite transmitter endpoint helpers.

A web framework can mount these handlers without ever sending CDSE secrets to
the Android application. Environment credentials stay in the server runtime.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from integrations.satellite.transmitter_service import request_observation
from integrations.satellite.central_ai import analyze_observation

DEFAULT_BBOX = (8.5, -4.0, 14.5, 2.5)


def request_gabon_observation(
    bbox: tuple[float, float, float, float] = DEFAULT_BBOX,
    hours: int = 168,
    max_cloud_cover: float = 60,
    include_ndvi: bool = True,
) -> dict:
    """Request a recent Gabon observation and pass it across the central-AI boundary."""
    if hours < 1 or hours > 720:
        raise ValueError("hours must be between 1 and 720")
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    packet = request_observation(
        bbox=bbox,
        start=start.isoformat().replace("+00:00", "Z"),
        end=end.isoformat().replace("+00:00", "Z"),
        max_cloud_cover=max_cloud_cover,
        include_ndvi=include_ndvi,
    )
    analysis = analyze_observation(packet)
    return {"observation": packet, "central_ai": analysis}

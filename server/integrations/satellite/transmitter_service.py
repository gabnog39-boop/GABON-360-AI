"""Satellite -> central-AI transmitter service for GABON 360 AI.

This module is deliberately transport-neutral: the future HTTP/API layer can call
`request_observation` without exposing Copernicus credentials to Android.
"""
from __future__ import annotations

from .sentinelhub_client import make_transmitter_packet


def request_observation(
    bbox: tuple[float, float, float, float],
    start: str,
    end: str,
    *,
    width: int = 1024,
    height: int = 1024,
    max_cloud_cover: float = 60,
    include_ndvi: bool = True,
) -> dict:
    """Acquire a rendered Sentinel-2 observation and package it for central AI."""
    packet = make_transmitter_packet(
        bbox=bbox,
        start=start,
        end=end,
        width=width,
        height=height,
        max_cloud_cover=max_cloud_cover,
        include_ndvi=include_ndvi,
    )
    packet["transmitter"] = {
        "name": "GABON 360 AI Satellite Transmitter",
        "status": "observation_transmitted_to_central_ai_boundary",
        "authorization_required_for_protected_sources": True,
    }
    return packet

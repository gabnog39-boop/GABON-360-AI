"""Authenticated Sentinel Hub Process API client for GABON 360 AI.

The mobile application must never contain the CDSE client secret. Keep
credentials on the server and expose only application endpoints to the app.
"""
from __future__ import annotations

import base64
import json
import os
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
PROCESS_URL = "https://sh.dataspace.copernicus.eu/process/v1"

_token_cache: dict[str, object] = {"access_token": None, "expires_at": 0.0}

TRUE_COLOR_EVALSCRIPT = """//VERSION=3
function setup() {
  return { input: [\"B02\", \"B03\", \"B04\"], output: { bands: 3, sampleType: \"AUTO\" } };
}
function evaluatePixel(sample) {
  return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
}
"""

NDVI_EVALSCRIPT = """//VERSION=3
function setup() {
  return { input: [\"B04\", \"B08\"], output: { bands: 1, sampleType: \"FLOAT32\" } };
}
function evaluatePixel(sample) {
  return [(sample.B08 - sample.B04) / (sample.B08 + sample.B04)];
}
"""


def _credentials() -> tuple[str, str]:
    client_id = os.environ.get("CDSE_CLIENT_ID", "").strip()
    client_secret = os.environ.get("CDSE_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        raise RuntimeError("CDSE_CLIENT_ID and CDSE_CLIENT_SECRET must be configured on the server")
    return client_id, client_secret


def get_access_token() -> str:
    """Return a cached OAuth client-credentials token, refreshing when needed."""
    now = time.time()
    cached = _token_cache.get("access_token")
    if isinstance(cached, str) and now < float(_token_cache.get("expires_at", 0)) - 60:
        return cached

    client_id, client_secret = _credentials()
    body = urlencode({
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode("utf-8")
    request = Request(
        TOKEN_URL,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    token = payload.get("access_token")
    if not token:
        raise RuntimeError("CDSE OAuth response did not contain an access token")
    expires_in = int(payload.get("expires_in", 3600))
    _token_cache["access_token"] = token
    _token_cache["expires_at"] = now + expires_in
    return token


def process_image(
    bbox: tuple[float, float, float, float],
    start: str,
    end: str,
    width: int = 1024,
    height: int = 1024,
    max_cloud_cover: float = 60,
    output_format: str = "image/jpeg",
    evalscript: str = TRUE_COLOR_EVALSCRIPT,
) -> bytes:
    """Render a Sentinel-2 L2A image for an AOI and time range."""
    if len(bbox) != 4:
        raise ValueError("bbox must be (west, south, east, north)")
    if not 1 <= width <= 4096 or not 1 <= height <= 4096:
        raise ValueError("image dimensions must be between 1 and 4096")
    if not 0 <= max_cloud_cover <= 100:
        raise ValueError("max_cloud_cover must be between 0 and 100")
    if output_format not in {"image/jpeg", "image/png", "image/tiff"}:
        raise ValueError("unsupported output format")

    payload = {
        "input": {
            "bounds": {
                "bbox": list(bbox),
                "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
            },
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {"from": start, "to": end},
                    "maxCloudCoverage": max_cloud_cover,
                    "mosaickingOrder": "leastCC",
                },
            }],
        },
        "output": {
            "width": width,
            "height": height,
            "responses": [{"identifier": "default", "format": {"type": output_format}}],
        },
        "evalscript": evalscript,
    }

    request = Request(
        PROCESS_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {get_access_token()}",
            "Content-Type": "application/json",
            "Accept": output_format,
            "User-Agent": "GABON-360-AI/1.0",
        },
        method="POST",
    )
    with urlopen(request, timeout=120) as response:
        return response.read()


def make_transmitter_packet(
    bbox: tuple[float, float, float, float],
    start: str,
    end: str,
    width: int = 1024,
    height: int = 1024,
    max_cloud_cover: float = 60,
    include_ndvi: bool = False,
) -> dict:
    """Build an application packet for the central AI.

    Images are returned as base64 in this transport-neutral packet. A production
    API may instead store the bytes and return short-lived URLs to reduce payloads.
    """
    rgb = process_image(bbox, start, end, width, height, max_cloud_cover)
    packet = {
        "source": "copernicus_sentinel_2_l2a",
        "kind": "satellite_observation",
        "bbox_wgs84": list(bbox),
        "time_range": {"from": start, "to": end},
        "selection": {"max_cloud_cover": max_cloud_cover, "mosaicking": "leastCC"},
        "image": {"mime_type": "image/jpeg", "base64": base64.b64encode(rgb).decode("ascii")},
        "live": False,
        "analysis_status": "raw_observation_ready_for_central_ai",
    }
    if include_ndvi:
        ndvi = process_image(
            bbox, start, end, width, height, max_cloud_cover,
            output_format="image/tiff", evalscript=NDVI_EVALSCRIPT,
        )
        packet["ndvi"] = {"mime_type": "image/tiff", "base64": base64.b64encode(ndvi).decode("ascii")}
    return packet

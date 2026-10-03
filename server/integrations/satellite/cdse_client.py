"""Read-only Copernicus Data Space STAC client for GABON 360 AI.

This module discovers public Earth-observation products; it does not claim
continuous live imagery and never enables protected satellite feeds.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

CONFIG_PATH = "server/integrations/satellite/cdse_config.json"
DEFAULT_CATALOG = "https://stac.dataspace.copernicus.eu/v1/"
DEFAULT_COLLECTIONS = ("sentinel-2-l2a", "sentinel-2-l1c", "sentinel-1-grd")
DEFAULT_BBOX = (8.5, -4.0, 14.5, 2.5)


def load_config(path: str = CONFIG_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def search_gabon(
    bbox=DEFAULT_BBOX,
    collections=DEFAULT_COLLECTIONS,
    datetime_range: str | None = None,
    cloud_cover_max: float | None = 80,
    limit: int = 20,
    timeout: int = 20,
) -> dict:
    """Query the public STAC catalog for products intersecting Gabon."""
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")

    config = load_config()
    if not config.get("enabled") or config.get("auth_required_for_catalog"):
        raise RuntimeError("Public CDSE catalog is not enabled for discovery")

    endpoint = config.get("search_endpoint", DEFAULT_CATALOG.rstrip("/") + "/search")
    payload = {
        "bbox": list(bbox),
        "collections": list(collections),
        "limit": limit,
    }
    if datetime_range:
        payload["datetime"] = datetime_range
    if cloud_cover_max is not None:
        payload["query"] = {"eo:cloud_cover": {"lte": cloud_cover_max}}

    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Accept": "application/geo+json", "Content-Type": "application/json", "User-Agent": "GABON-360-AI/1.0"},
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def health_check(timeout: int = 10) -> dict:
    """Return a small source-health record for the public STAC catalog."""
    config = load_config()
    catalog = config.get("catalog", DEFAULT_CATALOG)
    request = Request(catalog, headers={"Accept": "application/json", "User-Agent": "GABON-360-AI/1.0"})
    checked_at = datetime.now(timezone.utc).isoformat()
    try:
        with urlopen(request, timeout=timeout) as response:
            return {"provider": "copernicus_data_space_ecosystem", "status": "online", "http_status": response.status, "checked_at": checked_at}
    except Exception as exc:  # network health must never crash the situation center
        return {"provider": "copernicus_data_space_ecosystem", "status": "unavailable", "error": str(exc), "checked_at": checked_at}

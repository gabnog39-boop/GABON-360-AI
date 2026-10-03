"""GABON 360 AI satellite service facade.

Exposes a small, application-friendly interface around the public CDSE STAC
client. Results are metadata/discovery records unless an asset is explicitly
retrieved by an authorized downstream component.
"""
from __future__ import annotations

from .cdse_client import DEFAULT_BBOX, DEFAULT_COLLECTIONS, search_gabon


def discover_gabon_satellite_data(
    datetime_range: str | None = None,
    cloud_cover_max: float = 60,
    limit: int = 20,
) -> dict:
    """Discover public Sentinel products intersecting the Gabon AOI."""
    raw = search_gabon(
        bbox=DEFAULT_BBOX,
        collections=DEFAULT_COLLECTIONS,
        datetime_range=datetime_range,
        cloud_cover_max=cloud_cover_max,
        limit=limit,
    )
    features = raw.get("features", [])
    records = []
    for item in features:
        props = item.get("properties", {})
        records.append({
            "id": item.get("id"),
            "collection": item.get("collection"),
            "datetime": props.get("datetime"),
            "cloud_cover": props.get("eo:cloud_cover"),
            "geometry": item.get("geometry"),
            "assets": item.get("assets", {}),
            "source_status": "received_from_public_catalog",
            "live": False,
            "requires_human_validation_for_analysis": True,
        })
    return {
        "provider": "copernicus_data_space_ecosystem",
        "area": "Gabon",
        "status": "catalog_results_received",
        "live": False,
        "count": len(records),
        "records": records,
    }

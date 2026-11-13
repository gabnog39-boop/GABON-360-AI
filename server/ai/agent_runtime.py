"""Shared runtime for the 22 application agents.

Each agent executes a deterministic evidence triage against the same event packet.
This is an actual consultation step, not a claim that external AI models, sensors,
or protected data feeds are connected. Missing evidence is returned explicitly.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION = "g360-shared-evidence-router-1.0"

CAPABILITIES: dict[str, tuple[str, ...]] = {
    "accueil": ("situation", "synthese", "event"),
    "carte": ("geometry", "bbox", "coordinates", "location"),
    "satellites": ("catalog_record", "image", "ndvi", "derived_indicators", "sentinel"),
    "drones": ("drone", "video", "flight", "telemetry"),
    "navigation": ("route", "track", "waypoint", "position"),
    "geoloc": ("coordinates", "lat", "lon", "gps", "location"),
    "cyber": ("security", "auth", "audit", "vulnerability", "log"),
    "memoire": ("history", "timestamp", "observed_at", "event_type"),
    "alertes": ("severity", "priority", "alert", "finding"),
    "rapports": ("report", "observation", "evidence", "finding"),
    "stats": ("count", "metric", "indicator", "value"),
    "meteo": ("weather", "precipitation", "temperature", "wind", "forecast"),
    "parcs": ("forest", "vegetation", "park", "biodiversity", "ndvi"),
    "eaux": ("water", "river", "basin", "flood", "coastal", "marine"),
    "frontieres": ("border", "boundary", "crossing", "frontier"),
    "air": ("airspace", "aircraft", "flight", "aviation"),
    "centre": ("source", "timestamp", "observation", "event", "finding"),
    "admin": ("role", "permission", "admin", "account"),
    "users": ("user", "profile", "account", "session"),
    "paiements": ("payment", "subscription", "invoice", "transaction"),
    "missions": ("mission", "patrol", "team", "route", "track"),
    "garmin": ("gpx", "garmin", "waypoint", "track", "coordinates"),
}


def _flatten_keys(value: Any, prefix: str = "") -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            name = str(key).lower()
            keys.add(name)
            keys.update(_flatten_keys(child, prefix + name + "."))
    elif isinstance(value, list):
        for child in value[:50]:
            keys.update(_flatten_keys(child, prefix))
    return keys


def execute_agent_consultation(agent_id: str, evidence: list[dict[str, Any]]) -> dict[str, Any]:
    """Run a bounded, transparent evidence triage for one registered agent."""
    if agent_id not in CAPABILITIES:
        return {
            "agent": agent_id,
            "engine": ENGINE_VERSION,
            "status": "agent_not_registered",
            "evidence_count": 0,
            "findings": [],
            "limitations": ["Agent absent du registre d'exécution."],
        }

    rows = [item for item in evidence if isinstance(item, dict)][:50]
    expected = CAPABILITIES[agent_id]
    matched: list[dict[str, Any]] = []
    for item in rows:
        keys = _flatten_keys(item)
        searchable = " ".join(str(v).lower() for v in item.values() if isinstance(v, (str, int, float)))
        if any(token in keys or token in searchable for token in expected):
            matched.append(item)

    status = "evidence_received_for_review" if matched else "no_relevant_evidence"
    limitations = []
    if not rows:
        limitations.append("Aucune preuve transmise à cet agent.")
    elif not matched:
        limitations.append("Les preuves reçues ne contiennent pas les champs attendus pour ce domaine.")
    limitations.append("Triage déterministe uniquement : aucune conclusion physique ou opérationnelle n'est confirmée.")
    return {
        "agent": agent_id,
        "engine": ENGINE_VERSION,
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "evidence_count": len(matched),
        "evidence": matched[:10],
        "expected_evidence": list(expected),
        "limitations": limitations,
        "requires_human_validation": True,
    }


def execute_collaboration(plan: dict[str, Any], evidence: list[dict[str, Any]]) -> dict[str, Any]:
    """Execute every planned consultation and return a traceable team response."""
    consultations = plan.get("consulted_agents") or []
    results = [
        execute_agent_consultation(str(item.get("id", "")), evidence)
        for item in consultations if isinstance(item, dict)
    ]
    return {
        "source_agent": plan.get("source_agent"),
        "engine": ENGINE_VERSION,
        "planned_count": len(consultations),
        "executed_count": len(results),
        "results": results,
        "status": "triage_completed",
        "autonomous_ai_models_connected": False,
        "external_sources_connected_by_this_engine": False,
        "requires_human_validation": True,
    }

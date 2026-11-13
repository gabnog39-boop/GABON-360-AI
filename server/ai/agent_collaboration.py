"""Bounded collaboration plan for the 22 GABON 360 AI application agents.

This module routes an observation to relevant domains. It does not pretend that
an agent has executed an analysis: downstream work is marked as requested until
a real engine/provider returns evidence.
"""
from __future__ import annotations

from typing import Any

AGENTS: dict[str, str] = {
    "accueil": "Synthèse nationale",
    "carte": "Cartographie et couches",
    "satellites": "Imagerie satellitaire",
    "drones": "Drones et vidéos",
    "navigation": "Navigation terrain",
    "geoloc": "Géolocalisation GPS",
    "cyber": "Cybersécurité",
    "memoire": "Mémoire territoriale",
    "alertes": "Alertes",
    "rapports": "Rapports",
    "stats": "Statistiques",
    "meteo": "Météo",
    "parcs": "Parcs nationaux",
    "eaux": "Eaux et océan",
    "frontieres": "Frontières",
    "air": "Espace aérien",
    "centre": "Centre national",
    "admin": "Administration",
    "users": "Utilisateurs",
    "paiements": "Paiements",
    "missions": "Missions",
    "garmin": "Garmin / GPX",
}

# Directed consultation graph. Keep operational domains connected to evidence,
# location, memory, reporting and central alerting without creating a full mesh.
ROUTES: dict[str, tuple[str, ...]] = {
    "accueil": ("centre", "alertes", "stats", "rapports"),
    "carte": ("geoloc", "satellites", "parcs", "frontieres"),
    "satellites": ("carte", "parcs", "eaux", "memoire", "alertes"),
    "drones": ("carte", "geoloc", "missions", "alertes"),
    "navigation": ("geoloc", "missions", "garmin", "parcs"),
    "geoloc": ("carte", "navigation", "missions", "alertes"),
    "cyber": ("users", "admin", "centre", "alertes"),
    "memoire": ("parcs", "alertes", "missions", "rapports", "stats"),
    "alertes": ("centre", "memoire", "carte", "rapports", "missions"),
    "rapports": ("memoire", "missions", "stats", "centre"),
    "stats": ("alertes", "missions", "rapports", "centre"),
    "meteo": ("navigation", "missions", "parcs", "eaux", "alertes"),
    "parcs": ("satellites", "drones", "carte", "missions", "memoire"),
    "eaux": ("satellites", "meteo", "carte", "alertes"),
    "frontieres": ("carte", "geoloc", "drones", "air", "alertes"),
    "air": ("drones", "carte", "frontieres", "alertes"),
    "centre": ("accueil", "alertes", "memoire", "stats", "rapports"),
    "admin": ("cyber", "users", "paiements", "centre"),
    "users": ("cyber", "admin", "centre"),
    "paiements": ("admin", "users", "cyber"),
    "missions": ("navigation", "geoloc", "parcs", "meteo", "garmin", "rapports"),
    "garmin": ("missions", "navigation", "geoloc", "memoire"),
}

# Backend service/page identifiers mapped to the 22 user-facing application agents.
PAGE_ALIASES = {
    "satellite": "satellites", "forets": "parcs", "maritime": "eaux",
    "statistiques": "stats", "cybersecurite": "cyber", "surveillance": "centre",
    "orchestrateur": "centre", "proprietaire": "admin", "abonnements": "paiements",
    "administration": "admin", "risques": "centre", "infrastructures": "carte",
    "cameras": "drones", "crise": "alertes", "logistique": "missions",
    "fusion": "centre", "sources": "centre", "avatar": "accueil",
    "forest": "parcs", "forests": "parcs", "forest-observation": "parcs",
    "water": "eaux", "marine": "eaux", "weather": "meteo",
    "satellite_catalog_observation": "satellites",
    "copernicus_sentinel_2_l2a": "satellites",
    "security": "cyber", "mission": "missions", "gpx": "garmin",
    "alert": "alertes", "alertes": "alertes", "flood-risk": "eaux",
    "forest-change": "parcs", "biodiversity-observation": "parcs",
    "water-observation": "eaux", "marine-observation": "eaux",
    "weather-alert": "meteo", "weather-forecast": "meteo",
    "drone-observation": "drones", "camera-observation": "drones",
    "position": "geoloc", "waypoint": "garmin", "track": "garmin",
    "border": "frontieres", "airspace": "air",
}

SEVERITY_PRIORITY = {"CRITICAL": 4, "ALERT": 4, "CRITIQUE": 4,
                     "HIGH": 3, "WARNING": 3, "IMPORTANT": 3,
                     "MEDIUM": 2, "INFO": 1, "LOW": 0}


def build_collaboration_plan(page: str, severity: str = "INFO",
                             evidence: list[dict[str, Any]] | None = None,
                             max_agents: int = 6) -> dict[str, Any]:
    """Return a deterministic, bounded consultation plan for one event."""
    source = page if page in AGENTS else PAGE_ALIASES.get(page, "centre")
    limit = max(1, min(int(max_agents), 8))
    selected = list(ROUTES[source][:limit])
    evidence_count = len(evidence or [])
    priority = SEVERITY_PRIORITY.get(str(severity).upper(), 1)
    if priority >= 3:
        # High-priority events must reach the central alert and memory domains.
        for required in ("alertes", "centre", "memoire"):
            if required != source and required not in selected:
                if len(selected) >= limit:
                    selected[-1] = required
                else:
                    selected.append(required)
    return {
        "source_page": page,
        "source_agent": source,
        "source_label": AGENTS[source],
        "consultation_status": "requested" if selected else "not_required",
        "consulted_agents": [
            {"id": agent, "label": AGENTS[agent], "status": "pending_engine_response"}
            for agent in selected
        ],
        "consultation_count": len(selected),
        "evidence_items_received": evidence_count,
        "evidence_policy": "Aucune conclusion sans retour d'un moteur et preuve traçable.",
        "human_validation_required": True,
        "execution_note": (
            "Plan de consultation préparé; les agents listés ne sont pas déclarés "
            "comme ayant répondu tant qu'un moteur spécialisé n'a pas retourné de résultat."
        ),
    }

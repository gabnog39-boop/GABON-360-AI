"""Domain registry for the GABON 360 AI national situation center.

Domains describe what the platform can observe/analyse. Protected sources remain
inactive until an authorized gateway is configured. This registry contains no
individual tracking or autonomous coercive action capability.
"""
from __future__ import annotations

DOMAINS = [
    {"id": "territory", "name": "Territoire & SIG", "ai": "Cartographie, changement territorial, couches SIG", "status": "core"},
    {"id": "environment", "name": "Forêts & biodiversité", "ai": "Végétation, déforestation, zones brûlées, conservation", "status": "core"},
    {"id": "water", "name": "Eaux & bassins", "ai": "Plans d'eau, changements de surface, risques hydrologiques", "status": "planned"},
    {"id": "ocean", "name": "Océan & littoral", "ai": "Littoral, turbidité, changements côtiers, contexte maritime", "status": "planned"},
    {"id": "weather", "name": "Météo & climat", "ai": "Prévisions, tendances, risques météo", "status": "planned"},
    {"id": "disaster", "name": "Risques & catastrophes", "ai": "Incendies, inondations, glissements, événements extrêmes", "status": "planned"},
    {"id": "infrastructure", "name": "Infrastructures", "ai": "Évolution des infrastructures et contexte territorial", "status": "planned"},
    {"id": "maritime", "name": "Situation maritime", "ai": "Sources maritimes autorisées, événements et anomalies de contexte", "status": "authorized_sources_only"},
    {"id": "security", "name": "Sécurité nationale", "ai": "Corrélation d'événements et aide à la situation pour autorités habilitées", "status": "authorized_sources_only"},
    {"id": "cyber", "name": "Cybersécurité défensive", "ai": "Santé des services, événements techniques, corrélation défensive", "status": "planned"},
    {"id": "logistics", "name": "Logistique & missions", "ai": "Planification, ressources, synchronisation et comptes rendus", "status": "planned"},
    {"id": "crisis", "name": "Gestion de crise", "ai": "Chronologie, synthèse, plans d'action et retour d'expérience", "status": "planned"},
    {"id": "data_quality", "name": "Qualité des données", "ai": "Fraîcheur, latence, couverture, cohérence et disponibilité", "status": "core"},
]


def list_domains() -> list[dict[str, str]]:
    return [dict(item) for item in DOMAINS]


def domain_summary() -> dict[str, object]:
    return {
        "total": len(DOMAINS),
        "core": sum(x["status"] == "core" for x in DOMAINS),
        "planned": sum(x["status"] == "planned" for x in DOMAINS),
        "authorized_sources_only": sum(x["status"] == "authorized_sources_only" for x in DOMAINS),
        "domains": list_domains(),
    }

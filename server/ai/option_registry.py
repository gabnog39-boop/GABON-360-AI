"""Registre fin des options GABON 360 AI.

Chaque option d'une page est déclarée avec son IA spécialisée, ses droits,
son niveau de validation humaine et son contrat d'événement. Le registre est
déterministe : il ne fabrique aucune donnée opérationnelle.
"""
from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class AIOption:
    page: str
    option: str
    ai: str
    event: str
    permission: str = "user"
    human_validation: bool = True
    proactive: bool = False


PAGE_OPTIONS: tuple[AIOption, ...] = (
    AIOption("avatar", "page_suivante", "avatar", "navigation-next", proactive=True),
    AIOption("avatar", "page_precedente", "avatar", "navigation-previous", proactive=True),
    AIOption("avatar", "commande_vocale", "avatar", "voice-command"),
    AIOption("carte", "selection_zone", "sig", "zone-selected"),
    AIOption("carte", "coordonnees", "sig", "coordinates-selected"),
    AIOption("carte", "couches", "sig", "layer-change"),
    AIOption("carte", "situation_territoriale", "sig", "territorial-situation"),
    AIOption("navigation", "position_gnss", "navigation", "position"),
    AIOption("navigation", "waypoint", "navigation", "waypoint"),
    AIOption("navigation", "trace", "navigation", "track"),
    AIOption("navigation", "gpx", "navigation", "gpx-export"),
    AIOption("satellite", "recherche_stac", "satellite", "acquisition"),
    AIOption("satellite", "comparaison_periodes", "satellite", "change-detection"),
    AIOption("satellite", "sentinel_2", "satellite", "sentinel-2-query"),
    AIOption("satellite", "sentinel_1", "satellite", "sentinel-1-query"),
    AIOption("forets", "observation", "forests", "forest-observation"),
    AIOption("forets", "changement", "forests", "forest-change"),
    AIOption("forets", "biodiversite", "forests", "biodiversity-observation"),
    AIOption("eaux", "observation", "water", "water-observation"),
    AIOption("eaux", "risque_inondation", "water", "flood-risk"),
    AIOption("maritime", "observation", "maritime", "marine-observation"),
    AIOption("maritime", "risque_littoral", "maritime", "coastal-risk"),
    AIOption("meteo", "prevision", "weather", "weather-forecast"),
    AIOption("meteo", "alerte", "weather", "weather-alert"),
    AIOption("risques", "analyse", "risk", "hazard"),
    AIOption("risques", "catastrophe", "risk", "disaster-risk"),
    AIOption("infrastructures", "observation", "infrastructure", "infrastructure-observation"),
    AIOption("drones", "mission", "drones", "drone-observation", permission="operator", human_validation=True),
    AIOption("drones", "controle", "drones", "drone-control-request", permission="admin", human_validation=True),
    AIOption("cameras", "source", "cameras", "camera-observation"),
    AIOption("cameras", "controle", "cameras", "camera-control-request", permission="admin", human_validation=True),
    AIOption("alertes", "creer", "alerts", "alert-created"),
    AIOption("alertes", "corrélation", "alerts", "correlation"),
    AIOption("rapports", "creer", "reports", "report-created"),
    AIOption("rapports", "exporter", "reports", "report-export"),
    AIOption("statistiques", "indicateurs", "stats", "metric-updated"),
    AIOption("sources", "sante", "sources", "source-status"),
    AIOption("sources", "qualite", "sources", "source-quality"),
    AIOption("cybersecurite", "diagnostic", "cyber", "security-health"),
    AIOption("cybersecurite", "audit", "cyber", "cyber-audit"),
    AIOption("crise", "ouvrir", "crisis", "crisis-opened"),
    AIOption("crise", "plan_action", "crisis", "action-plan", permission="operator", human_validation=True),
    AIOption("logistique", "ressources", "logistics", "resource-status"),
    AIOption("logistique", "mission", "logistics", "mission-logistics"),
    AIOption("memoire", "recherche", "memory", "memory-updated"),
    AIOption("memoire", "comparaison", "memory", "historical-context"),
    AIOption("memoire", "recurrence", "memory", "recurring-event"),
    AIOption("fusion", "correlation", "fusion", "correlation"),
    AIOption("fusion", "anomalie_multisource", "fusion", "cross-domain-anomaly"),
    AIOption("surveillance", "veille", "continuous-watch", "watch-update", proactive=True),
    AIOption("surveillance", "nouvelle_acquisition", "continuous-watch", "new-acquisition", proactive=True),
    AIOption("orchestrateur", "sante_relais", "orchestrator", "relay-health", proactive=True),
    AIOption("proprietaire", "permissions", "governance", "permission-change", permission="owner", human_validation=True),
    AIOption("proprietaire", "autorisations", "governance", "authorization-change", permission="owner", human_validation=True),
    AIOption("abonnements", "verification_paiement", "access", "payment-verification", permission="owner"),
    AIOption("abonnements", "activation", "access", "access-change", permission="owner", human_validation=True),
    AIOption("administration", "utilisateurs", "admin", "user-change", permission="owner", human_validation=True),
    AIOption("administration", "roles", "admin", "role-change", permission="owner", human_validation=True),
    AIOption("qualite_donnees", "fraicheur", "sources", "data-freshness", proactive=True),
    AIOption("qualite_donnees", "couverture", "sources", "coverage-quality", proactive=True),
    AIOption("crise", "chronologie", "crisis", "incident-timeline"),
    AIOption("crise", "retour_experience", "crisis", "after-action-review"),
    AIOption("preuves", "integrite", "memory", "evidence-integrity", permission="operator", human_validation=True),
    AIOption("preuves", "historique", "memory", "evidence-history", permission="operator"),
    AIOption("hors_ligne", "file_synchronisation", "orchestrator", "sync-queue", proactive=True),
    AIOption("hors_ligne", "reprise_connexion", "orchestrator", "sync-recovered", proactive=True),
    AIOption("sauvegardes", "etat", "admin", "backup-status", permission="admin", proactive=True),
    AIOption("sauvegardes", "restauration_test", "admin", "restore-test", permission="admin", human_validation=True),
    AIOption("maintenance", "sante_services", "orchestrator", "service-health", proactive=True),
    AIOption("maintenance", "erreurs", "orchestrator", "runtime-error", proactive=True),
    AIOption("administration", "sessions", "admin", "session-status", permission="owner", human_validation=True),
    AIOption("navigation", "alerte_hors_route", "navigation", "off-route-alert", proactive=True),
    AIOption("navigation", "proximite_danger", "navigation", "proximity-hazard", proactive=True),
    AIOption("navigation", "risque_terrain", "navigation", "terrain-risk", proactive=True),
    AIOption("navigation", "guidage_vocal", "navigation", "voice-guidance", proactive=True),
    AIOption("navigation", "cap_boussole", "navigation", "heading-compass"),
    AIOption("navigation", "distance_eta", "navigation", "distance-eta"),
    AIOption("navigation", "retour_depart", "navigation", "trackback"),
    AIOption("navigation", "enregistrement_trace", "navigation", "track-recording"),
    AIOption("navigation", "import_export_gpx", "navigation", "gpx-transfer"),
    AIOption("navigation", "cartes_hors_ligne", "navigation", "offline-map-status", proactive=True),
    AIOption("navigation", "etat_gnss", "navigation", "gnss-status", proactive=True),
    AIOption("navigation", "sync_centre", "navigation", "navigation-center-sync", proactive=True),
    AIOption("navigation", "rendezvous_secours", "navigation", "emergency-location-share", permission="operator", human_validation=True),
    AIOption("satellite", "couche_navigation", "satellite", "satellite-navigation-layer"),
    AIOption("satellite", "etat_connexion", "satellite", "satellite-connection-status", proactive=True),
    AIOption("satellite", "alerte_changement_terrain", "satellite", "terrain-change-alert", proactive=True),
)


def option_registry() -> list[dict[str, Any]]:
    return [asdict(item) for item in PAGE_OPTIONS]


def get_option(page: str, option: str) -> AIOption:
    for item in PAGE_OPTIONS:
        if item.page == page and item.option == option:
            return item
    raise KeyError(f"{page}:{option}")

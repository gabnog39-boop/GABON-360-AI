"""Registre des IA spécialisées GABON 360 AI.

Chaque page/service possède une identité IA, ses types d'événements et sa politique
de notification. Ce registre ne prétend pas créer une IA autonome : il définit le
contrat d'orchestration utilisé par les moteurs réels.
"""

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class SpecializedAI:
    key: str
    page: str
    domain: str
    events: tuple[str, ...]
    proactive: bool = True
    human_validation: bool = True


SPECIALIZED_AI = (
    SpecializedAI("sig", "carte", "Territoire & SIG", ("zone-selected", "territorial-change")),
    SpecializedAI("satellite", "satellite", "Observation satellite", ("acquisition", "change-detection")),
    SpecializedAI("forests", "forets", "Forêts & biodiversité", ("forest-change", "biodiversity-observation")),
    SpecializedAI("water", "eaux", "Eaux & bassins", ("water-observation", "flood-risk")),
    SpecializedAI("maritime", "maritime", "Océan & littoral", ("marine-observation", "coastal-risk")),
    SpecializedAI("weather", "meteo", "Météo & climat", ("weather-alert", "climate-anomaly")),
    SpecializedAI("risk", "risques", "Risques & catastrophes", ("hazard", "disaster-risk")),
    SpecializedAI("infrastructure", "infrastructures", "Infrastructures", ("infrastructure-observation",)),
    SpecializedAI("navigation", "navigation", "Navigation & missions terrain", ("position", "waypoint", "route-risk")),
    SpecializedAI("drones", "drones", "Drones", ("drone-observation", "drone-health"), human_validation=True),
    SpecializedAI("cameras", "cameras", "Caméras", ("camera-observation", "camera-health"), human_validation=True),
    SpecializedAI("alerts", "alertes", "Événements & alertes", ("alert-created", "alert-updated")),
    SpecializedAI("reports", "rapports", "Rapports", ("report-created",)),
    SpecializedAI("stats", "statistiques", "Statistiques", ("metric-updated",)),
    SpecializedAI("sources", "sources", "Qualité & santé des sources", ("source-status", "source-quality")),
    SpecializedAI("cyber", "cybersecurite", "Cybersécurité défensive", ("cyber-ai-alert", "security-health")),
    SpecializedAI("crisis", "crise", "Gestion de crise", ("crisis-opened", "crisis-updated")),
    SpecializedAI("logistics", "logistique", "Logistique", ("resource-status", "mission-logistics")),
    SpecializedAI("memory", "memoire", "Mémoire territoriale", ("memory-updated", "historical-context")),
    SpecializedAI("fusion", "fusion", "Fusion & corrélation", ("correlation", "cross-domain-anomaly")),
    SpecializedAI("continuous-watch", "surveillance", "Surveillance territoriale continue", ("watch-update", "new-acquisition")),
    SpecializedAI("orchestrator", "orchestrateur", "Orchestrateur national", ("relay-health", "ai-escalation")),
    SpecializedAI("governance", "proprietaire", "Gouvernance propriétaire", ("permission-change", "authorization-change")),
    SpecializedAI("access", "abonnements", "Accès & abonnements", ("access-change", "subscription-change")),
    SpecializedAI("admin", "administration", "Administration", ("user-change", "role-change")),
    SpecializedAI("avatar", "avatar", "Avatar / communication humaine", ("ai-notification", "ai-speak")),
)


def registry() -> list[dict[str, Any]]:
    return [asdict(item) for item in SPECIALIZED_AI]


def get_ai(key: str) -> SpecializedAI:
    for item in SPECIALIZED_AI:
        if item.key == key:
            return item
    raise KeyError(key)


def event_contract(
    *,
    module: str,
    source: str,
    observation: str,
    timestamp: str,
    confidence: float | None = None,
    severity: str = "INFO",
    status: str = "AI_DETECTED",
    location: dict[str, Any] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    recommended_action: str | None = None,
    requires_human_validation: bool = True,
) -> dict[str, Any]:
    """Normalise un événement avant publication au relais central."""

    return {
        "module": module,
        "source": source,
        "timestamp": timestamp,
        "location": location or {},
        "observation": observation,
        "confidence": confidence,
        "severity": severity,
        "status": status,
        "evidence": evidence or [],
        "recommended_action": recommended_action,
        "requires_human_validation": requires_human_validation,
    }

"""Orchestrateur central GABON 360 AI.

Flux:
page -> option -> IA spécialisée -> contrat événement -> corrélation ->
notification -> Avatar -> humain.

Le module est volontairement sans dépendance externe afin de pouvoir être
utilisé dans le runtime local, le mode hors ligne et les tests.
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any

from .option_registry import get_option


CRITICAL = {"CRITICAL", "ALERT", "CRITIQUE"}
IMPORTANT = {"HIGH", "WARNING", "IMPORTANT", "ALERTE"}


@dataclass
class AIEvent:
    page: str
    option: str
    ai: str
    event: str
    timestamp: str
    observation: str
    source: str = "local-runtime"
    location: dict[str, Any] = field(default_factory=dict)
    confidence: float | None = None
    severity: str = "INFO"
    status: str = "AI_DETECTED"
    evidence: list[dict[str, Any]] = field(default_factory=list)
    recommended_action: str | None = None
    requires_human_validation: bool = True

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class CentralAIOrchestrator:
    """Point central unique de corrélation et de notification."""

    def __init__(self) -> None:
        self.events: list[AIEvent] = []

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def dispatch(
        self,
        *,
        page: str,
        option: str,
        observation: str,
        source: str = "local-runtime",
        location: dict[str, Any] | None = None,
        confidence: float | None = None,
        severity: str = "INFO",
        status: str = "AI_DETECTED",
        evidence: list[dict[str, Any]] | None = None,
        recommended_action: str | None = None,
        requires_human_validation: bool | None = None,
    ) -> dict[str, Any]:
        spec = get_option(page, option)
        event = AIEvent(
            page=page,
            option=option,
            ai=spec.ai,
            event=spec.event,
            timestamp=self._now(),
            observation=observation,
            source=source,
            location=location or {},
            confidence=confidence,
            severity=severity.upper(),
            status=status,
            evidence=evidence or [],
            recommended_action=recommended_action,
            requires_human_validation=(
                spec.human_validation
                if requires_human_validation is None
                else requires_human_validation
            ),
        )
        self.events.append(event)
        return self._route(event)

    def _route(self, event: AIEvent) -> dict[str, Any]:
        urgent = event.severity in CRITICAL
        important = urgent or event.severity in IMPORTANT
        return {
            "event": event.as_dict(),
            "relay": {
                "accepted": True,
                "central_correlation": True,
                "avatar_notification": important,
                "human_validation_required": event.requires_human_validation,
            },
            "avatar": self.avatar_message(event) if important else None,
        }

    @staticmethod
    def avatar_message(event: AIEvent) -> dict[str, Any]:
        status = {
            "CRITICAL": "ALERTE CRITIQUE",
            "ALERT": "ALERTE",
            "HIGH": "ALERTE IMPORTANTE",
            "WARNING": "ANOMALIE À VÉRIFIER",
        }.get(event.severity, "INFORMATION")
        confidence = (
            f" Confiance {event.confidence:.0%}."
            if event.confidence is not None
            else ""
        )
        validation = (
            " Validation humaine requise."
            if event.requires_human_validation
            else ""
        )
        location = event.location.get("label") or event.location.get("name")
        where = f" Zone: {location}." if location else ""
        text = (
            f"{status}. {event.observation}."
            f"{where} Source: {event.source}."
            f" Heure: {event.timestamp}."
            f"{confidence}{validation}"
        )
        return {
            "speak": True,
            "priority": "critical" if event.severity in CRITICAL else "high",
            "text": text,
            "event_id": f"{event.ai}:{event.event}:{event.timestamp}",
        }

    def health(self) -> dict[str, Any]:
        return {
            "status": "healthy",
            "events": len(self.events),
            "specialized_routing": True,
            "central_correlation": True,
            "avatar_connected": True,
            "human_validation_boundary": True,
        }

    def recent(self, limit: int = 50) -> list[dict[str, Any]]:
        return [item.as_dict() for item in self.events[-max(1, limit):]]

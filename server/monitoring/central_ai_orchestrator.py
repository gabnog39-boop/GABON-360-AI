"""Single human-facing AI that fuses specialized engine observations.

Specialized engines remain backend components. This module produces one
traceable, human-facing situation message without inventing observations.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any, Iterable


class CentralAIOrchestrator:
    """Fuse packets from specialized engines into one central AI response."""

    def __init__(self, name: str = "GABON 360 AI") -> None:
        self.name = name

    @staticmethod
    def _priority(packet: dict[str, Any]) -> int:
        value = str(packet.get("priority", packet.get("severity", "normal"))).lower()
        return {"critical": 4, "high": 3, "medium": 2, "normal": 1, "low": 0}.get(value, 1)

    def ingest(self, packets: Iterable[dict[str, Any]]) -> dict[str, Any]:
        items = [p for p in packets if isinstance(p, dict)]
        findings = []
        sources = Counter()
        domains = Counter()
        for packet in items:
            source = packet.get("source") or packet.get("engine") or "source_inconnue"
            sources[str(source)] += 1
            domain = packet.get("domain") or packet.get("type") or "territoire"
            domains[str(domain)] += 1
            for finding in packet.get("findings", packet.get("alerts", [])) or []:
                if isinstance(finding, dict):
                    findings.append({**finding, "source": source})

        findings.sort(key=self._priority, reverse=True)
        top = findings[:20]
        priority = "critical" if any(self._priority(f) >= 4 for f in top) else (
            "high" if any(self._priority(f) >= 3 for f in top) else "normal"
        )
        if top:
            first = top[0]
            message = f"J'ai reçu {len(items)} flux spécialisés. Point prioritaire : {first.get('label') or first.get('type') or 'anomalie à vérifier'}."
        else:
            message = f"J'ai reçu {len(items)} flux spécialisés. Aucun événement confirmé n'est actuellement remonté."

        return {
            "centre": self.name,
            "assistant": "central",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "message": message,
            "voice_text": message,
            "priority": priority,
            "source_count": len(sources),
            "sources": list(sources),
            "domain_count": len(domains),
            "domains": dict(domains),
            "findings": top,
            "status": "review_required" if top else "no_confirmed_event",
            "requires_human_validation": True,
            "selection_required": False,
            "map_focus": top[0].get("geometry") if top else None,
            "live_satellite_video": False,
            "source_policy": "public_or_authorized_sources_only",
        }

    def answer(self, message: str, situation: dict[str, Any] | None = None) -> dict[str, Any]:
        """Return a grounded human-facing reply; never fabricate a new event."""
        situation = situation or {}
        context = situation.get("findings") or []
        if message.strip():
            if context:
                reply = f"Je prends votre demande en compte. {len(context)} élément(s) sont actuellement disponibles pour vérification."
            else:
                reply = "Je prends votre demande en compte. Je n'ai pas de constat confirmé à présenter sans données reçues."
        else:
            reply = situation.get("message", "Aucune information nouvelle.")
        return {
            "centre": self.name,
            "assistant": "central",
            "message": reply,
            "voice_text": reply,
            "grounded": True,
            "requires_human_validation": True,
            "status": situation.get("status", "no_confirmed_event"),
        }

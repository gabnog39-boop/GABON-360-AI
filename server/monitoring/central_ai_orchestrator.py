"""Single human-facing AI that fuses specialized engine observations.

Specialized engines remain backend components. This module produces one
traceable, human-facing situation message without inventing observations.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any, Iterable

try:
    from ai.agent_collaboration import build_collaboration_plan
except ModuleNotFoundError:  # repository-root test/import context
    from server.ai.agent_collaboration import build_collaboration_plan


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
        collaboration_inputs: dict[str, tuple[str, str, list[dict[str, Any]]]] = {}
        for packet in items:
            source = packet.get("source") or packet.get("engine") or "source_inconnue"
            sources[str(source)] += 1
            domain = packet.get("domain") or packet.get("kind") or packet.get("type") or source
            domains[str(domain)] += 1
            route_key = str(domain)
            packet_evidence = packet.get("findings", packet.get("alerts", [])) or []
            collaboration_inputs[route_key] = (
                route_key,
                str(packet.get("priority", packet.get("severity", "INFO"))),
                list(packet_evidence)[:20] if isinstance(packet_evidence, list) else [],
            )
            for finding in packet_evidence:
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

        collaboration_plans = [
            build_collaboration_plan(page=page, severity=severity, evidence=evidence)
            for page, severity, evidence in list(collaboration_inputs.values())[:8]
        ]

        return {
            "centre": self.name,
            "collaboration_plans": collaboration_plans,
            "collaboration_status": "plans_created_agents_pending_real_engine_responses",
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

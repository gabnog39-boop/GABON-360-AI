"""Moteur IA de mémoire territoriale GABON 360 AI.

Le moteur conserve uniquement des observations/événements fournis par des sources
identifiées. Il ne fabrique pas d'historique. Il compare des périodes, repère des
récurrences et produit des événements normalisés destinés au relais central.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class MemoryRecord:
    id: str
    source: str
    timestamp: str
    location: dict[str, Any]
    domain: str
    observation: str
    status: str = "RECORDED"
    confidence: float | None = None
    evidence: tuple[dict[str, Any], ...] = ()
    event_type: str = "observation"


class TerritorialMemoryAI:
    """Analyse historique déterministe; aucune donnée fictive n'est générée."""

    key = "memory"

    def __init__(self) -> None:
        self._records: list[MemoryRecord] = []

    def ingest(self, record: MemoryRecord) -> MemoryRecord:
        self._records.append(record)
        self._records.sort(key=lambda r: r.timestamp)
        return record

    def records(
        self,
        *,
        domain: str | None = None,
        source: str | None = None,
        start: str | None = None,
        end: str | None = None,
    ) -> list[dict[str, Any]]:
        out = self._records
        if domain:
            out = [r for r in out if r.domain == domain]
        if source:
            out = [r for r in out if r.source == source]
        if start:
            out = [r for r in out if r.timestamp >= start]
        if end:
            out = [r for r in out if r.timestamp <= end]
        return [asdict(r) for r in out]

    def compare_periods(
        self,
        *,
        start_a: str,
        end_a: str,
        start_b: str,
        end_b: str,
        domain: str | None = None,
        location_key: str | None = None,
    ) -> dict[str, Any]:
        a = self.records(domain=domain, start=start_a, end=end_a)
        b = self.records(domain=domain, start=start_b, end=end_b)

        def key(r: dict[str, Any]) -> str:
            loc = r.get("location") or {}
            if location_key and location_key in loc:
                return str(loc[location_key])
            return f"{loc.get('lat','?')}:{loc.get('lon','?')}"

        ka = {key(r) for r in a}
        kb = {key(r) for r in b}
        return {
            "period_a": {"start": start_a, "end": end_a, "records": len(a)},
            "period_b": {"start": start_b, "end": end_b, "records": len(b)},
            "persistent_locations": sorted(ka & kb),
            "new_locations": sorted(kb - ka),
            "locations_no_longer_seen": sorted(ka - kb),
            "records_a": a,
            "records_b": b,
            "status": "AI_ANALYSIS",
            "requires_human_validation": True,
        }

    def recurring_events(
        self,
        *,
        domain: str | None = None,
        min_occurrences: int = 3,
    ) -> list[dict[str, Any]]:
        groups: dict[tuple[str, str], list[MemoryRecord]] = {}
        for r in self._records:
            if domain and r.domain != domain:
                continue
            loc = r.location or {}
            loc_key = f"{loc.get('lat','?')}:{loc.get('lon','?')}"
            groups.setdefault((loc_key, r.event_type), []).append(r)

        results = []
        for (location, event_type), rows in groups.items():
            if len(rows) < min_occurrences:
                continue
            results.append({
                "location": location,
                "event_type": event_type,
                "occurrences": len(rows),
                "first_seen": rows[0].timestamp,
                "last_seen": rows[-1].timestamp,
                "sources": sorted({r.source for r in rows}),
                "status": "ANOMALY_PROBABLE",
                "requires_human_validation": True,
            })
        return results

    def build_event(
        self,
        *,
        source: str,
        observation: str,
        timestamp: str | None = None,
        location: dict[str, Any] | None = None,
        confidence: float | None = None,
        severity: str = "INFO",
        event_type: str = "historical-context",
        evidence: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        return {
            "module": "memory",
            "source": source,
            "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
            "location": location or {},
            "observation": observation,
            "confidence": confidence,
            "severity": severity,
            "status": "AI_ANALYSIS",
            "event_type": event_type,
            "evidence": evidence or [],
            "recommended_action": "Comparer avec les observations et rapports précédents.",
            "requires_human_validation": True,
        }

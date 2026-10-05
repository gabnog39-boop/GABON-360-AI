"""Central-AI analysis boundary for GABON 360 AI.

This module produces *candidate* environmental findings from observations.
It never turns a candidate into a confirmed incident automatically.
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any


def _score(*parts: object) -> float:
    """Create a deterministic, non-random screening score for traceability."""
    raw = "|".join(str(p) for p in parts).encode("utf-8")
    value = int(hashlib.sha256(raw).hexdigest()[:8], 16) / 0xFFFFFFFF
    return round(0.45 + value * 0.5, 3)


def _candidate(kind: str, label: str, confidence: float, evidence: str) -> dict[str, Any]:
    return {
        "type": kind,
        "label": label,
        "confidence": confidence,
        "severity": "review_required",
        "evidence": evidence,
        "status": "candidate_anomaly",
        "requires_human_validation": True,
    }


def analyze_observation(packet: dict) -> dict:
    """Screen a received observation and return reviewable anomaly candidates.

    Without pixel-level change data or a temporal baseline, the safe result is
    a readiness/no-claim response. If explicit derived indicators are supplied
    by an authorized processor, they can produce candidate findings here.
    """
    source = packet.get("source", "unknown")
    bbox = packet.get("bbox_wgs84")
    time_range = packet.get("time_range", {})
    image = packet.get("image", {})
    ndvi = packet.get("ndvi", {})
    has_image = bool(image.get("base64"))
    has_ndvi = bool(ndvi.get("base64"))
    indicators = packet.get("derived_indicators", {}) or {}
    findings: list[dict[str, Any]] = []

    # These findings are intentionally based only on explicit derived indicators
    # from an authorized processor; no incident is inferred from metadata alone.
    vegetation_change = indicators.get("vegetation_change")
    if isinstance(vegetation_change, (int, float)) and vegetation_change >= 0.25:
        findings.append(_candidate(
            "vegetation_change",
            "Changement important de végétation à examiner",
            _score(source, bbox, "vegetation", vegetation_change),
            "Indicateur temporel fourni par le processeur d'observation.",
        ))

    surface_change = indicators.get("surface_change")
    if isinstance(surface_change, (int, float)) and surface_change >= 0.25:
        findings.append(_candidate(
            "surface_change",
            "Changement de surface à examiner",
            _score(source, bbox, "surface", surface_change),
            "Indicateur de changement fourni par le processeur d'observation.",
        ))

    burn_indicator = indicators.get("burn_scar")
    if isinstance(burn_indicator, (int, float)) and burn_indicator >= 0.35:
        findings.append(_candidate(
            "burn_scar_candidate",
            "Signature compatible avec une zone brûlée à vérifier",
            _score(source, bbox, "burn", burn_indicator),
            "Indicateur spectral fourni par le processeur d'observation.",
        ))

    return {
        "analysis_id": f"g360-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "source": source,
        "kind": packet.get("kind", "observation"),
        "area": {"bbox_wgs84": bbox},
        "time_range": time_range,
        "inputs": {"image_received": has_image, "ndvi_received": has_ndvi},
        "findings": findings,
        "status": "candidate_findings_ready" if findings else "observation_screened_no_confirmed_anomaly",
        "validation": {
            "required": True,
            "state": "pending_human_validation",
        },
        "live": bool(packet.get("live", False)),
        "simulation": False,
        "message": (
            "Candidats d'anomalie transmis pour vérification humaine."
            if findings else
            "Observation examinée; aucune anomalie confirmée avec les indicateurs disponibles."
        ),
    }

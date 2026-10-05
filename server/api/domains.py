"""Situation-center domain catalog exposed to the application."""
from __future__ import annotations

from monitoring.domain_registry import domain_summary


def get_domains() -> dict:
    result = domain_summary()
    result["centre"] = "GABON 360 AI"
    result["coverage"] = "Gabon"
    result["human_validation_for_sensitive_use"] = True
    return result

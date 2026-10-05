"""Safe temporal change screening for GABON 360 AI observations."""
from __future__ import annotations

from typing import Any


def _mean_abs_difference(current: list[float], previous: list[float]) -> float:
    if not current or not previous:
        return 0.0
    n = min(len(current), len(previous))
    return sum(abs(current[i] - previous[i]) for i in range(n)) / n


def compare_indicators(current: dict[str, Any], previous: dict[str, Any] | None) -> dict[str, Any]:
    """Compare derived normalized indicators from two authorized observations.

    The function deliberately returns screening indicators, not confirmed events.
    """
    if not previous:
        return {
            "baseline_available": False,
            "vegetation_change": None,
            "surface_change": None,
            "burn_scar": None,
            "status": "baseline_required",
        }

    result: dict[str, Any] = {"baseline_available": True}
    for key in ("vegetation_index", "surface_index", "burn_index"):
        now = current.get(key)
        old = previous.get(key)
        if isinstance(now, list) and isinstance(old, list):
            result[key.replace("_index", "_change")] = round(_mean_abs_difference(now, old), 4)
        elif isinstance(now, (int, float)) and isinstance(old, (int, float)):
            result[key.replace("_index", "_change")] = round(abs(float(now) - float(old)), 4)

    result["vegetation_change"] = result.get("vegetation_change")
    result["surface_change"] = result.get("surface_change")
    result["burn_scar"] = result.get("burn_change")
    result["status"] = "screened"
    return result

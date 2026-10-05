"""Run one scheduled Gabon-wide monitoring cycle and persist its status."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "server"
if str(SERVER) not in sys.path:
    sys.path.insert(0, str(SERVER))

from api.continuous_monitoring import run_monitoring_cycle  # noqa: E402

result = run_monitoring_cycle(lookback_hours=168, limit=20)
out = ROOT / "monitoring_output.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({
    "status": result.get("status"),
    "new_observations": result.get("new_observations", 0),
    "selection_required": result.get("selection_required"),
}, ensure_ascii=False))

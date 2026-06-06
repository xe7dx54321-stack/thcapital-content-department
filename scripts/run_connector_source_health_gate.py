#!/usr/bin/env python3
"""Run Phase 27 connector regression and source health gate."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.connector_source_health_gate import build_connector_source_health_gate
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_connector_source_health_gate(paths, ROOT)
    summary = payload.get("summary", {})
    print("Connector Source Health Gate")
    print("============================")
    print(f"gate_status: {payload.get('gate_status')}")
    for key in ("pass", "warn", "fail", "healthy_connectors", "weak_connectors", "failed_connectors", "normalized_item_count"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

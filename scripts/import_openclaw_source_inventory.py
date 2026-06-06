#!/usr/bin/env python3
"""Import the OpenClaw source inventory as a read-only sidecar."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.openclaw_source_inventory import build_openclaw_source_inventory
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_openclaw_source_inventory(paths, ROOT)
    summary = payload.get("summary", {})
    print("OpenClaw Source Inventory")
    print("=========================")
    print(f"openclaw_available: {payload.get('openclaw_available')}")
    print(f"gateway_detected: {payload.get('gateway_detected')}")
    for key in ("job_count", "enabled_job_count", "source_count", "web", "wechat", "trend", "candidate", "x", "youtube"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

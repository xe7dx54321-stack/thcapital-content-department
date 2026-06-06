#!/usr/bin/env python3
"""Run selected OpenClaw metadata connectors."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.openclaw_metadata_connectors import run_openclaw_metadata_connectors
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = run_openclaw_metadata_connectors(paths, ROOT)
    summary = payload.get("summary", {})
    print("OpenClaw Metadata Connectors")
    print("============================")
    for key in ("connector_count", "success_connectors", "failed_connectors", "manual_only_connectors", "item_count", "weak_signal_items"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

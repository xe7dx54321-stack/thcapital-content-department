#!/usr/bin/env python3
"""Build the acquisition-to-content bridge sidecar."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.acquisition_to_content_bridge import build_acquisition_to_content_bridge
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_acquisition_to_content_bridge(paths, ROOT)
    summary = payload.get("summary", {})
    print("Acquisition-to-Content Bridge")
    print("=============================")
    for key in ("bridge_item_count", "ready_for_brief", "needs_evidence", "watch", "rejected"):
        print(f"{key}: {summary.get(key, 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

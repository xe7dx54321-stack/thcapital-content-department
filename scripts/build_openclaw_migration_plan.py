#!/usr/bin/env python3
"""Build the OpenClaw P0/P1 migration plan."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.openclaw_migration_plan import build_openclaw_migration_plan
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_openclaw_migration_plan(paths, ROOT)
    summary = payload.get("summary", {})
    print("OpenClaw Migration Plan")
    print("=======================")
    for key in ("candidate_count", "p0", "p1", "reddit", "funding_startup", "builder_research", "chinese_ai_media", "youtube_signal", "x_signal", "manual_only"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

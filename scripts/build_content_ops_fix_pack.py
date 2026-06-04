#!/usr/bin/env python3
"""Build Phase 22 content ops fix pack."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.content_ops_fix_pack import build_content_ops_fix_pack
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_content_ops_fix_pack(paths, ROOT)
    summary = payload.get("summary", {})
    print("Content Ops Fix Pack")
    print("====================")
    print(f"fix_count: {summary.get('fix_count', 0)}")
    print(f"quick_fix: {summary.get('quick_fix', 0)}")
    print(f"manual_intervention: {summary.get('manual_intervention', 0)}")
    print(f"next_phase: {summary.get('next_phase', 0)}")
    print(f"high_priority: {summary.get('high_priority', 0)}")
    print(f"latest: {paths.logs_root / 'latest_content_ops_fix_pack.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build Phase 21 trial fix pack."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.trial_fix_pack import build_trial_fix_pack


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_trial_fix_pack(paths, ROOT)
    summary = payload.get("summary", {})
    print("Trial Fix Pack")
    print("==============")
    for key in ("fix_count", "quick_fix", "next_phase", "manual_ops_note", "high_severity"):
        print(f"{key}: {summary.get(key)}")
    print(f"latest: {paths.logs_root / 'latest_trial_fix_pack.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

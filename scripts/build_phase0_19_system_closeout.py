#!/usr/bin/env python3
"""Build Phase 0-19 system closeout."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.system_closeout import build_phase0_19_system_closeout


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_phase0_19_system_closeout(paths, ROOT)
    readiness = payload.get("trial_readiness", {})
    print("Phase 0-19 System Closeout")
    print("==========================")
    print(f"trial_readiness.status: {readiness.get('status', 'UNKNOWN')}")
    print(f"known_gaps_count: {len(payload.get('known_gaps', []))}")
    print(f"latest: {paths.logs_root / 'latest_phase0_19_system_closeout.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

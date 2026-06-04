#!/usr/bin/env python3
"""Execute Phase 23 quick-fix candidates as sidecar results."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.quick_fix_candidate_executor import build_quick_fix_execution_results


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_quick_fix_execution_results(paths, ROOT)
    summary = payload.get("summary", {})
    print("Quick Fix Execution Results")
    print("===========================")
    print(f"fix_count: {summary.get('fix_count', 0)}")
    print(f"applied_sidecar: {summary.get('applied_sidecar', 0)}")
    print(f"skipped: {summary.get('skipped', 0)}")
    print(f"needs_manual: {summary.get('needs_manual', 0)}")
    print(f"failed: {summary.get('failed', 0)}")
    print(f"latest: {paths.logs_root / 'latest_quick_fix_execution_results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

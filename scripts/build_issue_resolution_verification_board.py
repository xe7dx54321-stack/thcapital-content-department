#!/usr/bin/env python3
"""Build Phase 23 issue resolution verification board."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.issue_resolution_verification import build_issue_resolution_verification
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_issue_resolution_verification(paths, ROOT)
    summary = payload.get("summary", {})
    print("Issue Resolution Verification")
    print("=============================")
    print(f"verification_count: {summary.get('verification_count', 0)}")
    print(f"verified: {summary.get('verified', 0)}")
    print(f"partial: {summary.get('partial', 0)}")
    print(f"unresolved: {summary.get('unresolved', 0)}")
    print(f"needs_manual: {summary.get('needs_manual', 0)}")
    print(f"latest: {paths.logs_root / 'latest_issue_resolution_verification.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

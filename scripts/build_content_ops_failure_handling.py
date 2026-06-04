#!/usr/bin/env python3
"""Build Phase 20 content ops failure handling guidance."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.content_ops_failure_handling import build_content_ops_failure_handling
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_content_ops_failure_handling(paths, ROOT)
    summary = payload.get("summary", {})
    print("Content Ops Failure Handling")
    print("============================")
    for key in ("issue_count", "blocker_count", "warn_count", "can_continue"):
        print(f"{key}: {summary.get(key)}")
    print(f"latest: {paths.logs_root / 'latest_content_ops_failure_handling.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

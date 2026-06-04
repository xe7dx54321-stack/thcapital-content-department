#!/usr/bin/env python3
"""Run Phase 20 publishing checklist regression."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.publishing_checklist_regression import build_publishing_checklist_regression


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_publishing_checklist_regression(paths, ROOT)
    summary = payload.get("summary", {})
    print("Publishing Checklist Regression")
    print("================================")
    for key in ("check_count", "pass", "warn", "fail", "regression_status"):
        print(f"{key}: {summary.get(key)}")
    print(f"latest: {paths.logs_root / 'latest_publishing_checklist_regression.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

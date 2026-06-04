#!/usr/bin/env python3
"""Build Phase 24 content quality calibration."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.content_quality_calibration import build_content_quality_calibration
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_content_quality_calibration(paths, ROOT)
    summary = payload.get("summary", {})
    print("Content Quality Calibration")
    print("===========================")
    print(f"article_count: {summary.get('article_count', 0)}")
    print(f"quality_issue_count: {summary.get('quality_issue_count', 0)}")
    print(f"publish_blocking_quality_issues: {summary.get('publish_blocking_quality_issues', 0)}")
    print(f"calibration_recommendation_count: {summary.get('calibration_recommendation_count', 0)}")
    print(f"latest: {paths.logs_root / 'latest_content_quality_calibration.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

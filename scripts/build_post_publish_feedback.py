#!/usr/bin/env python3
"""Build post-publish content ops feedback."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.content_ops_performance_feedback import build_content_ops_performance_feedback
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_content_ops_performance_feedback(paths, ROOT)
    summary = payload.get("summary", {})
    print("Post-publish Feedback")
    print("=====================")
    print(f"published_article_count: {summary.get('published_article_count', 0)}")
    print(f"with_metrics_count: {summary.get('with_metrics_count', 0)}")
    print(f"visual_performance_record_count: {summary.get('visual_performance_record_count', 0)}")
    print(f"recommendation_count: {summary.get('recommendation_count', 0)}")
    print(f"latest: {paths.logs_root / 'latest_post_publish_feedback.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

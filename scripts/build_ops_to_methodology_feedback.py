#!/usr/bin/env python3
"""Build Phase 24 ops-to-methodology feedback."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.ops_to_methodology_feedback import build_ops_to_methodology_feedback
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_ops_to_methodology_feedback(paths, ROOT)
    summary = payload.get("summary", {})
    print("Ops-to-Methodology Feedback")
    print("===========================")
    print(f"feedback_count: {summary.get('feedback_count', 0)}")
    print(f"topic_methodology: {summary.get('topic_methodology', 0)}")
    print(f"article_methodology: {summary.get('article_methodology', 0)}")
    print(f"recipe: {summary.get('recipe', 0)}")
    print(f"visual_methodology: {summary.get('visual_methodology', 0)}")
    print(f"latest: {paths.logs_root / 'latest_ops_to_methodology_feedback.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run Phase 32 autonomous topic-to-article pipeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.phase32_content_production import run_topic_to_article_pipeline  # noqa: E402


def main() -> int:
    payload, _ = run_topic_to_article_pipeline(get_project_paths(ROOT), ROOT)
    print(json.dumps(payload.get("summary", {}), ensure_ascii=False))
    print(f"status: {payload.get('status')}")
    return 0 if payload.get("status") in {"SUCCESS", "SUCCESS_EMPTY", "ACTIONABLE_EMPTY", "ACTIONABLE"} else 1


if __name__ == "__main__":
    raise SystemExit(main())


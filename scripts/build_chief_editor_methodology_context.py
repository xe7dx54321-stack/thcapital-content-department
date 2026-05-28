#!/usr/bin/env python3
"""Build methodology context for Chief Editor Agent."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.chief_editor_methodology_adapter import build_chief_editor_methodology_context  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Chief Editor methodology context.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload, outputs = build_chief_editor_methodology_context(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {key: str(path) for key, path in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        article = payload.get("selected_article_review", {})
        topic = payload.get("selected_topic_score", {})
        print("Chief Editor Methodology Context")
        print("================================")
        print(f"selected_article_id: {payload.get('selected_article_id')}")
        print(f"article_score: {article.get('methodology_total_score')}")
        print(f"topic_score: {topic.get('methodology_total_score')}")
        print(f"latest: {outputs['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Review articles using the article quality methodology."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.methodology_article_review import build_methodology_article_review  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build methodology-based article review.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload, outputs = build_methodology_article_review(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {key: str(path) for key, path in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        summary = payload.get("summary", {})
        print("Methodology Article Review")
        print("==========================")
        for key in ("article_count", "ready", "revise", "hold"):
            print(f"{key}: {summary.get(key, 0)}")
        print(f"latest: {outputs['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

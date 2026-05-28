#!/usr/bin/env python3
"""Score topics using the topic selection methodology."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.methodology_topic_scoring import build_methodology_topic_scores  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build methodology-based topic scores.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload, outputs = build_methodology_topic_scores(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {key: str(path) for key, path in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        summary = payload.get("summary", {})
        print("Methodology Topic Scores")
        print("========================")
        for key in ("topic_count", "write", "watch", "hold", "reject"):
            print(f"{key}: {summary.get(key, 0)}")
        print(f"latest: {outputs['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

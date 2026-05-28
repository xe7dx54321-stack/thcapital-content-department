#!/usr/bin/env python3
"""Validate the article visual methodology config."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.article_visual_methodology import load_article_visual_methodology, visual_methodology_summary  # noqa: E402


def main() -> int:
    summary = visual_methodology_summary(load_article_visual_methodology(REPO_ROOT))
    print("Article Visual Methodology")
    print("==========================")
    for key, value in summary.items():
        if key != "issues":
            print(f"{key}: {value}")
    print(f"issues: {len(summary.get('issues') or [])}")
    for issue in summary.get("issues") or []:
        print(f"- {issue}")
    print(json.dumps(summary, ensure_ascii=False, indent=2) if "--json" in sys.argv else "OK" if not summary.get("issues") else "FAILED")
    return 1 if summary.get("issues") else 0


if __name__ == "__main__":
    raise SystemExit(main())

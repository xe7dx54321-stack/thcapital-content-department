#!/usr/bin/env python3
"""Validate topic selection methodology config."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.topic_selection_methodology import load_topic_selection_methodology, methodology_summary, validate_topic_selection_methodology  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate topic selection methodology.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    methodology = load_topic_selection_methodology(REPO_ROOT)
    issues = validate_topic_selection_methodology(methodology)
    payload = {"status": "FAILED" if issues else "OK", "summary": methodology_summary(methodology), "issues": issues}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("Topic Selection Methodology")
        print("===========================")
        for key, value in payload["summary"].items():
            print(f"{key}: {value}")
        print(f"issues: {len(issues)}")
        for issue in issues:
            print(f"- {issue}")
        print(payload["status"])
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate content strategy recipes config."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.content_strategy_recipes import load_content_strategy_recipes, methodology_summary, validate_content_strategy_recipes  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate content strategy recipes.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    registry = load_content_strategy_recipes(REPO_ROOT)
    issues = validate_content_strategy_recipes(registry)
    payload = {"status": "FAILED" if issues else "OK", "summary": methodology_summary(registry), "issues": issues}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("Content Strategy Recipes")
        print("========================")
        for key, value in payload["summary"].items():
            print(f"{key}: {value}")
        print(f"issues: {len(issues)}")
        for issue in issues:
            print(f"- {issue}")
        print(payload["status"])
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())

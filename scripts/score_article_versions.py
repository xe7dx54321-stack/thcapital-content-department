#!/usr/bin/env python3
"""Score generated article versions against the original article."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.version_comparison_scoring import build_version_comparison_scores  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Score article versions.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = build_version_comparison_scores(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"result": asdict(result), "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Version Comparison Scores")
        print("=========================")
        print(f"comparisons: {result.comparison_count}")
        print(f"accept_recommended: {result.accept_recommended}")
        print(f"reject_recommended: {result.reject_recommended}")
        print(f"revise_more_recommended: {result.revise_more_recommended}")
        print(f"output: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build performance-to-learning feedback."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.performance_learning_feedback import build_performance_learning_feedback  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build performance learning feedback.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = build_performance_learning_feedback(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"result": asdict(result), "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Performance Learning Feedback")
        print("=============================")
        print(f"performance_records: {result.performance_record_count}")
        print(f"high_performing: {result.high_performing_count}")
        print(f"low_performing: {result.low_performing_count}")
        print(f"suggestions: {result.suggestion_count}")
        print(f"output: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

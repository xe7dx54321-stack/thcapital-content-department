#!/usr/bin/env python3
"""Run LLM Proponent Agent v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.llm_proponent_agent import build_llm_proponent_review_report, report_to_dict, write_llm_proponent_review_report  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run LLM Proponent Agent v1.")
    parser.add_argument("--provider", default=None)
    parser.add_argument("--mode", default=None, choices=("dry_run", "live"))
    parser.add_argument("--model", default=None)
    parser.add_argument("--limit", type=int, default=None, help="Limit review item count. Live mode defaults to 1 if omitted.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    limit = 1 if args.mode == "live" and args.limit is None else args.limit
    report = build_llm_proponent_review_report(paths, REPO_ROOT, args.provider, args.mode, args.model, limit=limit)
    outputs = write_llm_proponent_review_report(report, paths)
    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
    else:
        print("LLM Proponent Reviews v1")
        print("========================")
        print(f"run_date: {report.run_date}")
        print(f"provider: {report.provider_id}")
        print(f"mode: {report.mode}")
        print(f"review_count: {report.review_count}")
        for key, path in outputs.items():
            print(f"  {key}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

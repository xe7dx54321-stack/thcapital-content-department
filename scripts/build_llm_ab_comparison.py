#!/usr/bin/env python3
"""Build LLM Agent A/B comparison report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.llm_ab_comparison import build_llm_ab_comparison_report, report_to_dict, write_llm_ab_comparison_report  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build LLM A/B comparison report.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    report = build_llm_ab_comparison_report(paths)
    outputs = write_llm_ab_comparison_report(report, paths)
    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
    else:
        print("LLM A/B Comparison")
        print("==================")
        print(f"status: {report.status}")
        print(f"decision_match_rate: {report.summary.get('rule_vs_llm_decision_match_rate')}")
        print(f"judge_conflicts: {report.summary.get('judge_decision_conflict_count')}")
        print(f"fallback_count: {report.summary.get('fallback_count')}")
        for key, path in outputs.items():
            print(f"  {key}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

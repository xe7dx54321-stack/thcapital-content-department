#!/usr/bin/env python3
"""Check the daily LLM cost and call budget guard."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.cost_budget_guard import build_cost_budget_guard, report_to_dict, write_cost_budget_guard  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Check cost budget guard.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    report = build_cost_budget_guard(paths)
    write_cost_budget_guard(report, paths, REPO_ROOT)
    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
    else:
        print("Cost Budget Guard")
        print("=================")
        print(f"status: {report.status}")
        print(f"estimated_cost_today_usd: {report.estimated_cost_today_usd}")
        print(f"calls_today: {report.calls_today}")
        print(f"recommended_mode: {report.recommended_mode}")
    return 0 if report.status in {"ALLOW", "WARN", "BLOCK"} else 1


if __name__ == "__main__":
    raise SystemExit(main())

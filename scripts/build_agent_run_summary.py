#!/usr/bin/env python3
"""Build Phase 6 agent run summary."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.agent_run_log import build_agent_run_summary, write_agent_run_summary  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Agent Run Summary v1.")
    parser.add_argument("--run-date", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    summary = build_agent_run_summary(paths, args.run_date)
    outputs = write_agent_run_summary(summary, paths, args.run_date)
    if args.json:
        print(json.dumps(asdict(summary), ensure_ascii=False, indent=2))
    else:
        print("Agent Run Summary v1")
        print("====================")
        for key, value in summary.summary.items():
            print(f"{key}: {value}")
        for key, path in outputs.items():
            print(f"  {key}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Local CLI for autonomous runtime control."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.runtime_control import cancel_run, list_jobs, list_runs, request_shutdown, run_named, runtime_status, set_pause  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Runtime control CLI.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("jobs")
    sub.add_parser("runs")
    run_parser = sub.add_parser("run")
    run_parser.add_argument("target")
    retry_parser = sub.add_parser("retry")
    retry_parser.add_argument("job_run_id")
    cancel_parser = sub.add_parser("cancel")
    cancel_parser.add_argument("job_run_id")
    sub.add_parser("pause")
    sub.add_parser("resume")
    sub.add_parser("shutdown")
    args = parser.parse_args()
    paths = get_project_paths(ROOT)
    if args.command == "status":
        result = runtime_status(paths)
    elif args.command == "jobs":
        result = list_jobs(ROOT)
    elif args.command == "runs":
        result = list_runs(paths)
    elif args.command == "run":
        result = run_named(ROOT, args.target)
    elif args.command == "retry":
        result = {"job_run_id": args.job_run_id, "status": "QUEUED_FOR_RETRY_REVIEW", "note": "retry remains governed by runtime retry policy"}
    elif args.command == "cancel":
        result = cancel_run(paths, args.job_run_id)
    elif args.command == "pause":
        result = set_pause(paths, True)
    elif args.command == "resume":
        result = set_pause(paths, False)
    else:
        result = request_shutdown(paths)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

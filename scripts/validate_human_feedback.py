#!/usr/bin/env python3
"""Validate Human Feedback v1 files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.human_feedback import issues_to_dict, read_json, validate_feedback_payload  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def default_path() -> Path:
    paths = get_project_paths(REPO_ROOT)
    return paths.market_content_root / "07_publishing" / "latest_human_feedback_template.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Human Feedback v1 JSON.")
    parser.add_argument("path", nargs="?", help="Feedback JSON path. Defaults to latest template.")
    parser.add_argument("--json", action="store_true", help="Print validation JSON.")
    args = parser.parse_args()
    path = Path(args.path).expanduser() if args.path else default_path()
    payload = read_json(path)
    issues = validate_feedback_payload(payload)
    errors = [item for item in issues if item.severity == "ERROR"]
    warns = [item for item in issues if item.severity == "WARN"]
    if args.json:
        print(json.dumps({"path": str(path), "error_count": len(errors), "warn_count": len(warns), "issues": issues_to_dict(issues)}, ensure_ascii=False, indent=2))
    else:
        print("Human Feedback Validation")
        print("=========================")
        print(f"path: {path}")
        print(f"ERROR: {len(errors)}")
        print(f"WARN: {len(warns)}")
        for issue in issues:
            print(f"{issue.severity}: {issue.feedback_id or '-'} {issue.field}: {issue.message}")
        print("OK" if not errors else "FAILED")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

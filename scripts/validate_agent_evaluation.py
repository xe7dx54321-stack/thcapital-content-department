#!/usr/bin/env python3
"""Validate an agent evaluation template."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.agent_evaluation import validate_agent_evaluation_payload  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Agent Evaluation Template v1.")
    parser.add_argument("path", nargs="?", type=Path, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    target = args.path or paths.market_content_root / "07_publishing" / "latest_agent_evaluation_template.json"
    payload = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
    issues = validate_agent_evaluation_payload(payload)
    counts = Counter(issue.severity for issue in issues)
    summary = {
        "path": str(target),
        "evaluation_count": len(payload.get("evaluation_items", [])) if isinstance(payload.get("evaluation_items"), list) else 0,
        "error_count": counts.get("ERROR", 0),
        "warn_count": counts.get("WARN", 0),
        "issues": [asdict(issue) for issue in issues],
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print("Agent Evaluation Validation")
        print("===========================")
        print(f"path: {target}")
        print(f"evaluation_count: {summary['evaluation_count']}")
        print(f"ERROR: {summary['error_count']}")
        print(f"WARN: {summary['warn_count']}")
        for issue in issues:
            print(f"  {issue.severity}: {issue.evaluation_id or '<item>'}.{issue.field or '<unknown>'}: {issue.message}")
        print("\nOK" if summary["error_count"] == 0 else "\nFAILED")
    return 1 if summary["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

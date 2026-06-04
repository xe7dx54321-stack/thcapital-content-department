#!/usr/bin/env python3
"""Build the Phase 20 operator runbook."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.operator_runbook import build_operator_runbook
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_operator_runbook(paths, ROOT)
    status = payload.get("current_status", {})
    print("Operator Runbook")
    print("================")
    print(f"sections: {len(payload.get('sections', []))}")
    print(f"failure_issue_count: {status.get('failure_issue_count', 0)}")
    print(f"regression_status: {status.get('regression_status', 'UNKNOWN')}")
    print(f"latest: {paths.logs_root / 'latest_operator_runbook.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

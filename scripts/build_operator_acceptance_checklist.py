#!/usr/bin/env python3
"""Build the operator acceptance checklist."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.operator_acceptance_checklist import build_operator_acceptance_checklist
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_operator_acceptance_checklist(paths, ROOT)
    summary = payload.get("operator_acceptance_summary", {})
    print("Operator Acceptance Checklist")
    print("=============================")
    print(f"acceptance_status: {payload.get('acceptance_status')}")
    print(f"pass: {summary.get('pass')}")
    print(f"warn: {summary.get('warn')}")
    print(f"fail: {summary.get('fail')}")
    print(f"manual_review_required: {summary.get('manual_review_required')}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

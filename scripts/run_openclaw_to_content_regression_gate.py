#!/usr/bin/env python3
"""Run OpenClaw-to-content regression gate."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.openclaw_to_content_regression_gate import run_openclaw_to_content_regression_gate
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = run_openclaw_to_content_regression_gate(paths, ROOT)
    summary = payload.get("summary", {})
    print("OpenClaw-to-Content Regression Gate")
    print("===================================")
    print(f"gate_status: {payload.get('gate_status')}")
    for key in ("pass", "warn", "fail", "blocking_failures", "activated_topics", "can_enter_brief_pipeline"):
        print(f"{key}: {summary.get(key, 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

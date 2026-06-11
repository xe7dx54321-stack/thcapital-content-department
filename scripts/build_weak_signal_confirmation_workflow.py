#!/usr/bin/env python3
"""Build weak signal confirmation workflow for OpenClaw migrated signals."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.weak_signal_confirmation_workflow import build_weak_signal_confirmation_workflow


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_weak_signal_confirmation_workflow(paths, ROOT)
    summary = payload.get("summary", {})
    print("Weak Signal Confirmation Workflow")
    print("=================================")
    for key in (
        "confirmation_count",
        "confirmable",
        "needs_primary_source",
        "needs_second_source",
        "manual_review",
        "watch",
        "blocked",
        "can_promote_to_topic",
    ):
        print(f"{key}: {summary.get(key, 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build OpenClaw signal evidence backfill tasks."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.openclaw_signal_evidence_backfill import build_openclaw_signal_evidence_backfill
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_openclaw_signal_evidence_backfill(paths, ROOT)
    summary = payload.get("summary", {})
    print("OpenClaw Signal Evidence Backfill")
    print("=================================")
    for key in (
        "backfill_count",
        "ready_for_confirmation",
        "needs_primary_source",
        "needs_manual_review",
        "watch",
        "blocked",
        "eligible_for_topic_activation",
    ):
        print(f"{key}: {summary.get(key, 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

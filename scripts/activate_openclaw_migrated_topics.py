#!/usr/bin/env python3
"""Activate confirmed OpenClaw migrated signals as topic candidates."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.openclaw_topic_activation import activate_openclaw_migrated_topics
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = activate_openclaw_migrated_topics(paths, ROOT)
    summary = payload.get("summary", {})
    print("OpenClaw Topic Activation")
    print("=========================")
    for key in (
        "candidate_count",
        "activated",
        "needs_evidence",
        "watch",
        "rejected",
        "can_enter_brief_pipeline",
    ):
        print(f"{key}: {summary.get(key, 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

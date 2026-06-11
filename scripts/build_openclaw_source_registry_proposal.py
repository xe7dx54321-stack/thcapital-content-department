#!/usr/bin/env python3
"""Build OpenClaw source registry proposal sidecar."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.openclaw_source_registry_proposal import build_openclaw_source_registry_proposal
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_openclaw_source_registry_proposal(paths, ROOT)
    summary = payload.get("summary", {})
    print("OpenClaw Source Registry Proposal")
    print("=================================")
    for key in ("proposal_count", "add_as_enabled", "add_as_disabled", "manual_backfill_only", "do_not_add"):
        print(f"{key}: {summary.get(key, 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

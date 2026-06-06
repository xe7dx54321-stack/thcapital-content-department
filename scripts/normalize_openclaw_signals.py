#!/usr/bin/env python3
"""Normalize OpenClaw metadata connector output."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.openclaw_signal_normalizer import normalize_openclaw_signals
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = normalize_openclaw_signals(paths, ROOT)
    summary = payload.get("summary", {})
    print("Normalized OpenClaw Signals")
    print("===========================")
    for key in ("signal_count", "weak_signal_count", "candidate_for_hot_material_pool", "hard_evidence_allowed"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

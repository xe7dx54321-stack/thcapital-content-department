#!/usr/bin/env python3
"""Build the Phase 26 source coverage gap audit."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.source_coverage_gap_audit import build_source_coverage_gap_audit


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_source_coverage_gap_audit(paths, ROOT)
    coverage = payload.get("coverage_summary", {})
    summary = payload.get("summary", {})
    print("Source Coverage Gap Audit")
    print("=========================")
    print(f"configured_sources: {coverage.get('configured_sources', 0)}")
    print(f"enabled_sources: {coverage.get('enabled_sources', 0)}")
    print(f"observed_sources: {coverage.get('observed_sources', 0)}")
    print(f"gap_count: {summary.get('gap_count', 0)}")
    print(f"high_severity: {summary.get('high_severity', 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

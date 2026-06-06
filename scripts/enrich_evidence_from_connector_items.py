#!/usr/bin/env python3
"""Build connector evidence packets from normalized upstream metadata."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.connector_evidence_enrichment import build_connector_evidence_packets
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_connector_evidence_packets(paths, ROOT)
    summary = payload.get("summary", {})
    print("Connector Evidence Enrichment")
    print("=============================")
    for key in ("packet_count", "high_strength", "medium_strength", "low_strength", "eligible_for_topic_promotion"):
        print(f"{key}: {summary.get(key, 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Phase 33 historical data availability audit entrypoint."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import get_project_paths
from content_system.phase33_historical_replay import audit_historical_data_availability


def run(repo_root: Path | None = None):
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    return audit_historical_data_availability(get_project_paths(root), root)

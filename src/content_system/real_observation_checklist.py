"""Phase 33 real observation checklist entrypoint."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import get_project_paths
from content_system.phase33_historical_replay import build_real_observation_checklist


def run(repo_root: Path | None = None):
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    return build_real_observation_checklist(get_project_paths(root), root)

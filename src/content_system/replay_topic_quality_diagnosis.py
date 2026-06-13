"""Phase 33 replay topic quality diagnosis entrypoint."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import get_project_paths
from content_system.phase33_historical_replay import diagnose_replay_topic_quality


def run(repo_root: Path | None = None):
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    return diagnose_replay_topic_quality(get_project_paths(root), root)

"""Phase 33 replay topic scoring entrypoint."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import get_project_paths
from content_system.phase33_historical_replay import run_replay_topic_scoring


def run(repo_root: Path | None = None):
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    return run_replay_topic_scoring(get_project_paths(root), root)

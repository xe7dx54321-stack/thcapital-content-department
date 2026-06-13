"""Phase 33 human review checklist builder entrypoint."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import get_project_paths
from content_system.phase33_historical_replay import build_human_review_checklists


def run(repo_root: Path | None = None):
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    return build_human_review_checklists(get_project_paths(root), root)

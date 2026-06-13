"""Autonomous confirmed topic scoring entry point."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import score_autonomous_topics


def build_autonomous_topic_scores(paths: ProjectPaths, repo_root: Path):
    return score_autonomous_topics(paths, repo_root)


"""Daily autonomous main topic selection entry point."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import select_daily_main_topics


def build_daily_main_topic_selection(paths: ProjectPaths, repo_root: Path):
    return select_daily_main_topics(paths, repo_root)


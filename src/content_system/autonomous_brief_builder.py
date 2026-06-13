"""Autonomous writing brief builder entry point."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import build_autonomous_briefs


def build_autonomous_brief_report(paths: ProjectPaths, repo_root: Path):
    return build_autonomous_briefs(paths, repo_root)


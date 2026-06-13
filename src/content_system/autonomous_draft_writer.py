"""Autonomous draft writer entry point."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import write_autonomous_drafts


def build_autonomous_draft_report(paths: ProjectPaths, repo_root: Path):
    return write_autonomous_drafts(paths, repo_root)


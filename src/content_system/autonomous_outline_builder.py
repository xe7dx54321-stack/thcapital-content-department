"""Autonomous article outline builder entry point."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import build_autonomous_outlines


def build_autonomous_outline_report(paths: ProjectPaths, repo_root: Path):
    return build_autonomous_outlines(paths, repo_root)


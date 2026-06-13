"""Legacy-vs-new autonomous content quality regression entry point."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import run_quality_regression


def build_legacy_vs_new_quality_regression(paths: ProjectPaths, repo_root: Path):
    return run_quality_regression(paths, repo_root)


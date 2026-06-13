"""Autonomous article review pipeline entry point."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import run_article_review_pipeline


def build_autonomous_article_review_pipeline(paths: ProjectPaths, repo_root: Path):
    return run_article_review_pipeline(paths, repo_root)


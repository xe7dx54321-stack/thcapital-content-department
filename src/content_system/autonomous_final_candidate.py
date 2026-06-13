"""Autonomous final candidate assembly entry point."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import build_final_candidates


def build_autonomous_final_candidate_report(paths: ProjectPaths, repo_root: Path):
    return build_final_candidates(paths, repo_root)


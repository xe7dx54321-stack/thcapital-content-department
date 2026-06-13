"""Legacy know-how to current methodology mapping entry point."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import map_legacy_knowhow


def build_legacy_knowhow_methodology_mapping(paths: ProjectPaths, repo_root: Path):
    return map_legacy_knowhow(paths, repo_root)


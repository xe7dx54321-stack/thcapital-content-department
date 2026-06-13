"""Legacy content asset audit entry point."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import audit_legacy_content_assets


def build_legacy_content_asset_audit(paths: ProjectPaths, repo_root: Path):
    return audit_legacy_content_assets(paths, repo_root)


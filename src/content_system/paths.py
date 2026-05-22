"""Central path helpers for the content system repository."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    repo_root: Path
    market_content_root: Path
    legacy_content_root: Path
    console_root: Path
    scripts_root: Path
    frontstage_root: Path
    logs_root: Path


def get_project_paths(repo_root: Path | None = None) -> ProjectPaths:
    """Return important project paths derived from the repository root."""

    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    market_content_root = root / "同行资本市场内容系统"

    return ProjectPaths(
        repo_root=root,
        market_content_root=market_content_root,
        legacy_content_root=root / "内容生产系统",
        console_root=root / "内容工厂控制台",
        scripts_root=market_content_root / "09_runbooks" / "scripts",
        frontstage_root=market_content_root / "11_frontstage",
        logs_root=market_content_root / "10_logs",
    )

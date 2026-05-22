"""Central path helpers for the content system repository."""

from __future__ import annotations

import os
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


def env_path(name: str, fallback: Path) -> Path:
    """Return an environment-provided path or a fallback.

    Empty environment values fall back. User home markers are expanded. The path
    is resolved for consistency, but existence is checked by callers.
    """

    value = os.environ.get(name, "").strip()
    if not value:
        return fallback.resolve()
    return Path(value).expanduser().resolve()


def env_path_any(names: tuple[str, ...], fallback: Path) -> Path:
    """Return the first configured env path from names, otherwise fallback."""

    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return Path(value).expanduser().resolve()
    return fallback.resolve()


def path_config_sources() -> dict[str, str]:
    """Expose path source names for diagnostics without changing ProjectPaths."""

    return {
        "market_content_root": "THCAP_MARKET_CONTENT_ROOT or repo fallback",
        "legacy_content_root": "THCAP_LEGACY_CONTENT_ROOT or repo fallback",
        "console_root": "THCAP_CONTENT_CONSOLE_ROOT or repo fallback",
    }


def get_project_paths(repo_root: Path | None = None) -> ProjectPaths:
    """Return important project paths derived from the repository root."""

    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    market_content_root = env_path_any(
        ("THCAP_MARKET_CONTENT_ROOT", "MARKET_CONTENT_ROOT"),
        root / "同行资本市场内容系统",
    )
    legacy_content_root = env_path_any(
        ("THCAP_LEGACY_CONTENT_ROOT", "LEGACY_CONTENT_ROOT"),
        root / "内容生产系统",
    )
    console_root = env_path_any(
        ("THCAP_CONTENT_CONSOLE_ROOT", "CONTENT_FACTORY_CONSOLE_ROOT"),
        root / "内容工厂控制台",
    )

    return ProjectPaths(
        repo_root=root,
        market_content_root=market_content_root,
        legacy_content_root=legacy_content_root,
        console_root=console_root,
        scripts_root=market_content_root / "09_runbooks" / "scripts",
        frontstage_root=market_content_root / "11_frontstage",
        logs_root=market_content_root / "10_logs",
    )

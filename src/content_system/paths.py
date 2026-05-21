"""项目路径配置。

第一阶段先提供最小路径抽象，避免后续脚本继续散落硬编码路径。
默认以仓库根目录为基准；如需覆盖，可通过环境变量传入绝对路径。
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    """项目关键路径集合。"""

    repo_root: Path
    market_content_root: Path
    legacy_content_root: Path
    console_root: Path
    scripts_root: Path
    frontstage_root: Path
    logs_root: Path
    data_root: Path
    sqlite_root: Path


def _env_path(name: str, default: Path) -> Path:
    """读取环境变量路径；未设置时使用默认值。"""

    value = os.environ.get(name)
    if not value:
        return default
    return Path(value).expanduser().resolve()


def get_project_paths(repo_root: Path | None = None) -> ProjectPaths:
    """返回当前项目的关键路径。

    Args:
        repo_root: 仓库根目录。为空时使用当前文件向上推导。

    Environment variables:
        THCAP_REPO_ROOT: 仓库根目录。
        THCAP_MARKET_CONTENT_ROOT: 活跃市场内容系统目录。
        THCAP_LEGACY_CONTENT_ROOT: 旧版内容生产系统目录。
        THCAP_CONSOLE_ROOT: 内容工厂控制台目录。
        THCAP_DATA_ROOT: 工程化数据目录。
    """

    if repo_root is None:
        inferred_repo_root = Path(__file__).resolve().parents[2]
    else:
        inferred_repo_root = Path(repo_root).expanduser().resolve()

    repo_root_path = _env_path("THCAP_REPO_ROOT", inferred_repo_root)

    market_content_root = _env_path(
        "THCAP_MARKET_CONTENT_ROOT",
        repo_root_path / "同行资本市场内容系统",
    )
    legacy_content_root = _env_path(
        "THCAP_LEGACY_CONTENT_ROOT",
        repo_root_path / "内容生产系统",
    )
    console_root = _env_path(
        "THCAP_CONSOLE_ROOT",
        repo_root_path / "内容工厂控制台",
    )
    data_root = _env_path(
        "THCAP_DATA_ROOT",
        repo_root_path / "data",
    )

    return ProjectPaths(
        repo_root=repo_root_path,
        market_content_root=market_content_root,
        legacy_content_root=legacy_content_root,
        console_root=console_root,
        scripts_root=market_content_root / "09_runbooks" / "scripts",
        frontstage_root=market_content_root / "11_frontstage",
        logs_root=market_content_root / "10_logs",
        data_root=data_root,
        sqlite_root=data_root / "sqlite",
    )

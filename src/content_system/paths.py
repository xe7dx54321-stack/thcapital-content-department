"""项目路径解析工具。

设计目标：
- 不再在新增代码里写死 `/Users/apple/Documents/...`。
- 默认以当前 Git 仓库为根目录。
- 允许通过环境变量覆盖本机真实路径。
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


REPO_MARKERS = ("README.md", ".gitignore")


@dataclass(frozen=True)
class ProjectPaths:
    repo_root: Path
    market_content_root: Path
    legacy_content_root: Path
    console_root: Path
    frontstage_root: Path
    logs_root: Path
    scripts_root: Path


def _load_dotenv(repo_root: Path) -> None:
    """轻量读取 .env；不引入 python-dotenv 依赖。

    已存在的环境变量优先级更高，不会被 .env 覆盖。
    """
    env_path = repo_root / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def find_repo_root(start: Path | None = None) -> Path:
    """从 start 向上寻找仓库根目录。"""
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if all((candidate / marker).exists() for marker in REPO_MARKERS):
            return candidate
    return current


def _env_path(name: str, default: Path) -> Path:
    value = os.environ.get(name, "").strip()
    if not value:
        return default.resolve()
    return Path(value).expanduser().resolve()


def get_project_paths(start: Path | None = None) -> ProjectPaths:
    repo_root = _env_path("THCAP_CONTENT_REPO_ROOT", find_repo_root(start))
    _load_dotenv(repo_root)

    repo_root = _env_path("THCAP_CONTENT_REPO_ROOT", repo_root)
    market_root = _env_path("MARKET_CONTENT_ROOT", repo_root / "同行资本市场内容系统")
    legacy_root = _env_path("LEGACY_CONTENT_ROOT", repo_root / "内容生产系统")
    console_root = _env_path("CONTENT_FACTORY_CONSOLE_ROOT", repo_root / "内容工厂控制台")

    return ProjectPaths(
        repo_root=repo_root,
        market_content_root=market_root,
        legacy_content_root=legacy_root,
        console_root=console_root,
        frontstage_root=market_root / "11_frontstage",
        logs_root=market_root / "10_logs",
        scripts_root=market_root / "09_runbooks" / "scripts",
    )

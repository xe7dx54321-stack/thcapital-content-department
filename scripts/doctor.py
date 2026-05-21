#!/usr/bin/env python3
"""同行资本内容部门项目健康检查。

本脚本是后续工程化改造的第一个稳定入口：
- 检查项目根目录和关键业务目录是否存在。
- 检查活跃市场内容系统的核心脚本是否存在。
- 检查 frontstage/logs 目录是否可写。
- 可选检查网络访问能力。

运行：
    python3 scripts/doctor.py
    make doctor
"""

from __future__ import annotations

import json
import os
import socket
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

# 允许直接从仓库根目录运行，不要求安装包。
REPO_ROOT_CANDIDATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT_CANDIDATE / "src"))

from content_system.paths import get_project_paths  # noqa: E402


@dataclass
class CheckResult:
    name: str
    status: str
    detail: str


def ok(name: str, detail: str) -> CheckResult:
    return CheckResult(name=name, status="OK", detail=detail)


def warn(name: str, detail: str) -> CheckResult:
    return CheckResult(name=name, status="WARN", detail=detail)


def fail(name: str, detail: str) -> CheckResult:
    return CheckResult(name=name, status="FAIL", detail=detail)


def check_exists(name: str, path: Path) -> CheckResult:
    if path.exists():
        return ok(name, str(path))
    return fail(name, f"missing: {path}")


def check_optional_exists(name: str, path: Path) -> CheckResult:
    if path.exists():
        return ok(name, str(path))
    return warn(name, f"missing optional path: {path}")


def check_writable(name: str, path: Path) -> CheckResult:
    if not path.exists():
        return fail(name, f"directory missing: {path}")
    if not path.is_dir():
        return fail(name, f"not a directory: {path}")

    probe = path / ".doctor_write_probe"
    try:
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return ok(name, str(path))
    except OSError as exc:
        return fail(name, f"not writable: {path} ({exc})")


def check_network(hosts: Iterable[str], timeout: float = 2.0) -> list[CheckResult]:
    results: list[CheckResult] = []
    for host in hosts:
        try:
            socket.create_connection((host, 443), timeout=timeout).close()
            results.append(ok(f"network:{host}", "tcp/443 reachable"))
        except OSError as exc:
            results.append(warn(f"network:{host}", f"unreachable or blocked: {exc}"))
    return results


def print_results(results: list[CheckResult]) -> None:
    width = max(len(item.name) for item in results) if results else 20
    for item in results:
        icon = {"OK": "✅", "WARN": "⚠️", "FAIL": "❌"}.get(item.status, "•")
        print(f"{icon} {item.name.ljust(width)} {item.status:<4} {item.detail}")


def main() -> int:
    paths = get_project_paths(REPO_ROOT_CANDIDATE)
    results: list[CheckResult] = []

    results.append(ok("python", sys.version.split()[0]))
    results.append(check_exists("repo_root", paths.repo_root))
    results.append(check_exists("market_content_root", paths.market_content_root))
    results.append(check_optional_exists("legacy_content_root", paths.legacy_content_root))
    results.append(check_optional_exists("console_root", paths.console_root))
    results.append(check_exists("scripts_root", paths.scripts_root))
    results.append(check_exists("frontstage_root", paths.frontstage_root))
    results.append(check_exists("logs_root", paths.logs_root))

    required_scripts = [
        "market_topic_capture_round.py",
        "market_official_update_lane.py",
        "market_wechat_rss_refresh.py",
        "market_wechat_deep_capture_round.py",
        "market_learning_memo_builder.py",
        "market_learning_pool_board_builder.py",
    ]
    for script_name in required_scripts:
        results.append(check_exists(f"script:{script_name}", paths.scripts_root / script_name))

    results.append(check_writable("frontstage_writable", paths.frontstage_root))
    results.append(check_writable("logs_writable", paths.logs_root))

    if os.environ.get("THCAP_DOCTOR_NETWORK_CHECK", "0") == "1":
        results.extend(check_network(["github.com", "r.jina.ai", "openai.com"]))
    else:
        results.append(warn("network_check", "skipped; set THCAP_DOCTOR_NETWORK_CHECK=1 to enable"))

    print("\n同行资本内容部门 · 项目健康检查")
    print("=" * 60)
    print_results(results)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "paths": {key: str(value) for key, value in asdict(paths).items()},
        "results": [asdict(item) for item in results],
    }
    report_path = paths.logs_root / "latest_doctor_report.json"
    try:
        paths.logs_root.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n报告已写入：{report_path}")
    except OSError as exc:
        print(f"\n⚠️ 无法写入健康检查报告：{exc}")

    has_fail = any(item.status == "FAIL" for item in results)
    return 1 if has_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())

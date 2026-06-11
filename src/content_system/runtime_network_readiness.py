"""Network readiness checks for acquisition routing."""

from __future__ import annotations

import os
import socket
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import repo_relative, today_token, utc_now, write_json_and_markdown


def _dns_ok(host: str, timeout: float = 2.0) -> bool:
    socket.setdefaulttimeout(timeout)
    try:
        socket.gethostbyname(host)
    except OSError:
        return False
    return True


def check_runtime_network_readiness() -> dict[str, Any]:
    override = os.environ.get("THCAP_RUNTIME_NETWORK_MODE", "").strip().upper()
    if override in {"FULL", "DOMESTIC_ONLY", "INTERNATIONAL_ONLY", "OFFLINE", "UNKNOWN"}:
        status = override
        dns_ok = status != "OFFLINE"
        international_ok = status in {"FULL", "INTERNATIONAL_ONLY"}
        domestic_ok = status in {"FULL", "DOMESTIC_ONLY"}
        return _payload(status, dns_ok, dns_ok, international_ok, domestic_ok, [{"check": "env_override", "status": status}])
    general = _dns_ok("example.com")
    domestic = _dns_ok("www.baidu.com")
    international = _dns_ok("www.openai.com") or _dns_ok("github.com")
    if general and domestic and international:
        status = "FULL"
    elif domestic and not international:
        status = "DOMESTIC_ONLY"
    elif international and not domestic:
        status = "INTERNATIONAL_ONLY"
    elif not general and not domestic and not international:
        status = "OFFLINE"
    else:
        status = "UNKNOWN"
    checks = [
        {"check": "general_dns", "host": "example.com", "ok": general},
        {"check": "domestic_dns", "host": "www.baidu.com", "ok": domestic},
        {"check": "international_dns", "host": "www.openai.com/github.com", "ok": international},
    ]
    return _payload(status, general or domestic or international, general, international, domestic, checks)


def _payload(status: str, dns_ok: bool, general_ok: bool, international_ok: bool, domestic_ok: bool, checks: list[dict[str, Any]]) -> dict[str, Any]:
    routes = {
        "FULL": ["run domestic sources", "run international sources", "run local processing"],
        "DOMESTIC_ONLY": ["run domestic sources", "delay international acquisition", "continue local processing"],
        "INTERNATIONAL_ONLY": ["run international sources", "delay domestic acquisition", "continue local processing"],
        "OFFLINE": ["skip external acquisition", "run local processing", "queue acquisition retry"],
        "UNKNOWN": ["run local processing", "route acquisition conservatively"],
    }.get(status, ["run local processing"])
    return {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": status,
        "dns_ok": dns_ok,
        "general_internet_ok": general_ok,
        "international_source_ok": international_ok,
        "domestic_source_ok": domestic_ok,
        "checks": checks,
        "recommended_routes": routes,
    }


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__runtime-network-readiness.json",
        "dated_md": paths.logs_root / f"{run_date}__runtime-network-readiness.md",
        "latest_json": paths.logs_root / "latest_runtime_network_readiness.json",
        "latest_md": paths.logs_root / "latest_runtime_network_readiness.md",
    }


def write_network_readiness_report(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    payload = check_runtime_network_readiness()
    outputs = output_paths(paths, payload["run_date"])
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    routes = "\n".join(f"- {item}" for item in payload.get("recommended_routes", []))
    return f"""# Runtime Network Readiness

- status: `{payload.get('status')}`
- dns_ok: `{payload.get('dns_ok')}`
- international_source_ok: `{payload.get('international_source_ok')}`
- domestic_source_ok: `{payload.get('domestic_source_ok')}`

## Recommended Routes

{routes}
"""

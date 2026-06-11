"""Route acquisition work based on network readiness."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.runtime_network_readiness import check_runtime_network_readiness


def build_route_plan_from_readiness(readiness: dict[str, Any]) -> dict[str, Any]:
    status = str(readiness.get("status") or "UNKNOWN")
    if status == "FULL":
        routes = [
            {"lane": "international_sources", "action": "RUN_NOW", "reason": "international checks passed"},
            {"lane": "domestic_sources", "action": "RUN_NOW", "reason": "domestic checks passed"},
            {"lane": "local_processing", "action": "RUN_NOW", "reason": "always safe"},
        ]
    elif status == "DOMESTIC_ONLY":
        routes = [
            {"lane": "domestic_sources", "action": "RUN_NOW", "reason": "domestic checks passed"},
            {"lane": "international_sources", "action": "DELAY_RETRY", "reason": "international checks failed"},
            {"lane": "local_processing", "action": "RUN_NOW", "reason": "offline-safe"},
        ]
    elif status == "INTERNATIONAL_ONLY":
        routes = [
            {"lane": "international_sources", "action": "RUN_NOW", "reason": "international checks passed"},
            {"lane": "domestic_sources", "action": "DELAY_RETRY", "reason": "domestic checks failed"},
            {"lane": "local_processing", "action": "RUN_NOW", "reason": "offline-safe"},
        ]
    elif status == "OFFLINE":
        routes = [
            {"lane": "external_acquisition", "action": "QUEUE_RETRY", "reason": "network offline"},
            {"lane": "local_processing", "action": "RUN_NOW", "reason": "no network required"},
            {"lane": "workbench_build", "action": "RUN_NOW", "reason": "local artifacts can still refresh"},
        ]
    else:
        routes = [
            {"lane": "external_acquisition", "action": "DELAY_RETRY", "reason": "readiness unknown"},
            {"lane": "local_processing", "action": "RUN_NOW", "reason": "safe fallback"},
        ]
    return {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "network_status": status,
        "routes": routes,
        "summary": {
            "route_count": len(routes),
            "run_now": sum(1 for item in routes if item["action"] == "RUN_NOW"),
            "delay_retry": sum(1 for item in routes if item["action"] == "DELAY_RETRY"),
            "queue_retry": sum(1 for item in routes if item["action"] == "QUEUE_RETRY"),
        },
    }


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__acquisition-route-plan.json",
        "dated_md": paths.logs_root / f"{run_date}__acquisition-route-plan.md",
        "latest_json": paths.logs_root / "latest_acquisition_route_plan.json",
        "latest_md": paths.logs_root / "latest_acquisition_route_plan.md",
    }


def build_acquisition_route_plan(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    readiness = read_json(paths.logs_root / "latest_runtime_network_readiness.json") or check_runtime_network_readiness()
    payload = build_route_plan_from_readiness(readiness)
    outputs = output_paths(paths, payload["run_date"])
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(f"- {item.get('lane')}: `{item.get('action')}` - {item.get('reason')}" for item in payload.get("routes", []))
    return f"""# Acquisition Route Plan

- network_status: `{payload.get('network_status')}`

## Routes

{rows}
"""

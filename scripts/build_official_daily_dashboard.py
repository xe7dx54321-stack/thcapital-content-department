#!/usr/bin/env python3
"""Build a compact daily dashboard for the official update lane.

P0-015 is a report-only dashboard:
- It reads existing sidecar artifacts produced by the official-lane daily flow.
- It does not run fetchers.
- It does not retry or block anything.
- It writes JSON/Markdown summaries for quick human review.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT_CANDIDATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT_CANDIDATE / "src"))

from content_system.paths import get_project_paths  # noqa: E402


@dataclass(frozen=True)
class DashboardPaths:
    manifest: Path
    source_runtime_health: Path
    daily_summary: Path
    quality_gate: Path


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    return payload if isinstance(payload, dict) else None


def first_int(*values: Any, default: int = 0) -> int:
    for value in values:
        if isinstance(value, bool):
            continue
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
    return default


def nested_get(payload: dict[str, Any] | None, *keys: str) -> Any:
    if payload is None:
        return None

    current: Any = payload
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def collect_warnings(
    manifest: dict[str, Any] | None,
    runtime_health: dict[str, Any] | None,
    daily_summary: dict[str, Any] | None,
    quality_gate: dict[str, Any] | None,
) -> list[str]:
    warnings: list[str] = []

    if manifest is None:
        warnings.append("Missing latest official runtime manifest.")
    if runtime_health is None:
        warnings.append("Missing latest source runtime health report.")
    if daily_summary is None:
        warnings.append("Missing latest daily source run summary.")
    if quality_gate is None:
        warnings.append("Missing latest official lane quality gate report.")

    manifest_status = nested_get(manifest, "status")
    if manifest_status and manifest_status != "SUCCESS":
        warnings.append(f"Official runtime manifest status is {manifest_status}.")

    gate_level = (
        nested_get(quality_gate, "gate", "level")
        or nested_get(quality_gate, "gate_status")
        or nested_get(quality_gate, "level")
    )
    if gate_level and gate_level != "GREEN":
        warnings.append(f"Official lane quality gate is {gate_level}.")

    missing_expected = first_int(
        nested_get(daily_summary, "source_runtime_health", "missing_expected"),
        nested_get(daily_summary, "missing_expected"),
        nested_get(runtime_health, "summary", "missing_expected"),
        default=0,
    )
    if missing_expected > 10:
        warnings.append(f"Source runtime health missing_expected is high: {missing_expected}.")

    error_hint_sources = first_int(
        nested_get(daily_summary, "source_runtime_health", "error_hint_sources"),
        nested_get(daily_summary, "error_hint_sources"),
        nested_get(runtime_health, "summary", "error_hint_sources"),
        default=0,
    )
    if error_hint_sources > 0:
        warnings.append(f"Source runtime health has error hints: {error_hint_sources} source(s).")

    return warnings


def build_dashboard_payload(
    run_date: str,
    paths: DashboardPaths,
    manifest: dict[str, Any] | None,
    runtime_health: dict[str, Any] | None,
    daily_summary: dict[str, Any] | None,
    quality_gate: dict[str, Any] | None,
) -> dict[str, Any]:
    source_count = first_int(
        nested_get(manifest, "summary", "source_count"),
        nested_get(manifest, "source_count"),
        nested_get(daily_summary, "official_lane", "source_count"),
        nested_get(daily_summary, "source_count"),
        default=0,
    )
    total_items_found = first_int(
        nested_get(manifest, "summary", "total_items_found"),
        nested_get(manifest, "total_items_found"),
        nested_get(daily_summary, "official_lane", "total_items_found"),
        nested_get(daily_summary, "total_items_found"),
        default=0,
    )
    total_items_written = first_int(
        nested_get(manifest, "summary", "total_items_written"),
        nested_get(manifest, "total_items_written"),
        nested_get(daily_summary, "official_lane", "total_items_written"),
        nested_get(daily_summary, "total_items_written"),
        default=0,
    )

    enabled_sources = first_int(
        nested_get(runtime_health, "summary", "enabled_sources"),
        nested_get(runtime_health, "summary", "enabled"),
        nested_get(daily_summary, "source_runtime_health", "enabled_sources"),
        default=0,
    )
    observed_sources = first_int(
        nested_get(runtime_health, "summary", "observed_sources"),
        nested_get(runtime_health, "summary", "observed"),
        nested_get(daily_summary, "source_runtime_health", "observed_sources"),
        default=0,
    )
    missing_expected = first_int(
        nested_get(runtime_health, "summary", "missing_expected"),
        nested_get(daily_summary, "source_runtime_health", "missing_expected"),
        nested_get(daily_summary, "missing_expected"),
        default=0,
    )
    error_hint_sources = first_int(
        nested_get(runtime_health, "summary", "error_hint_sources"),
        nested_get(daily_summary, "source_runtime_health", "error_hint_sources"),
        nested_get(daily_summary, "error_hint_sources"),
        default=0,
    )

    gate_level = (
        nested_get(quality_gate, "gate", "level")
        or nested_get(quality_gate, "gate_status")
        or nested_get(quality_gate, "level")
        or nested_get(quality_gate, "status")
        or "UNKNOWN"
    )
    gate_status = nested_get(quality_gate, "status") or gate_level

    warnings = collect_warnings(manifest, runtime_health, daily_summary, quality_gate)
    status = "GREEN"
    if gate_level == "RED" or manifest is None or quality_gate is None:
        status = "RED"
    elif warnings or gate_level in {"YELLOW", "WARN", "WARNING"}:
        status = "YELLOW"

    return {
        "schema_version": "v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "run_date": run_date,
        "status": status,
        "official_lane": {
            "manifest_status": nested_get(manifest, "status") or "UNKNOWN",
            "source_count": source_count,
            "total_items_found": total_items_found,
            "total_items_written": total_items_written,
        },
        "source_runtime_health": {
            "enabled_sources": enabled_sources,
            "observed_sources": observed_sources,
            "missing_expected": missing_expected,
            "error_hint_sources": error_hint_sources,
        },
        "quality_gate": {
            "status": gate_status,
            "level": gate_level,
        },
        "warnings": warnings,
        "inputs": {
            "manifest": str(paths.manifest),
            "source_runtime_health": str(paths.source_runtime_health),
            "daily_summary": str(paths.daily_summary),
            "quality_gate": str(paths.quality_gate),
        },
    }


def render_markdown(payload: dict[str, Any]) -> str:
    official = payload["official_lane"]
    health = payload["source_runtime_health"]
    gate = payload["quality_gate"]
    warnings = payload["warnings"]

    lines = [
        "# Official Daily Dashboard",
        "",
        f"- Generated at: `{payload['generated_at']}`",
        f"- Run date: `{payload['run_date']}`",
        f"- Dashboard status: **{payload['status']}**",
        "",
        "## Official Lane",
        "",
        f"- Manifest status: `{official['manifest_status']}`",
        f"- Source count: `{official['source_count']}`",
        f"- Total items found: `{official['total_items_found']}`",
        f"- Total items written: `{official['total_items_written']}`",
        "",
        "## Source Runtime Health",
        "",
        f"- Enabled sources: `{health['enabled_sources']}`",
        f"- Observed sources: `{health['observed_sources']}`",
        f"- Missing expected: `{health['missing_expected']}`",
        f"- Error hint sources: `{health['error_hint_sources']}`",
        "",
        "## Quality Gate",
        "",
        f"- Gate status: `{gate['status']}`",
        f"- Gate level: `{gate['level']}`",
        "",
        "## Warnings",
        "",
    ]

    if warnings:
        lines.extend([f"- {item}" for item in warnings])
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Inputs",
            "",
            f"- Runtime manifest: `{payload['inputs']['manifest']}`",
            f"- Source runtime health: `{payload['inputs']['source_runtime_health']}`",
            f"- Daily source summary: `{payload['inputs']['daily_summary']}`",
            f"- Quality gate: `{payload['inputs']['quality_gate']}`",
            "",
            "## Notes",
            "",
            "This dashboard is report-only. It does not block, retry, or modify the capture pipeline.",
            "",
        ]
    )

    return "\n".join(lines)


def write_outputs(payload: dict[str, Any], markdown: str) -> dict[str, str]:
    paths = get_project_paths(REPO_ROOT_CANDIDATE)
    logs_root = paths.logs_root
    frontstage_root = paths.frontstage_root
    logs_root.mkdir(parents=True, exist_ok=True)
    frontstage_root.mkdir(parents=True, exist_ok=True)

    run_date = payload["run_date"]
    outputs = {
        "dated_json": logs_root / f"{run_date}__official-daily-dashboard.json",
        "latest_json": logs_root / "latest_official_daily_dashboard.json",
        "dated_md": logs_root / f"{run_date}__official-daily-dashboard.md",
        "latest_md": logs_root / "latest_official_daily_dashboard.md",
        "frontstage_dated_md": frontstage_root / f"{run_date}__official-daily-dashboard.md",
        "frontstage_latest_md": frontstage_root / "latest_official_daily_dashboard.md",
    }

    for key, path in outputs.items():
        if path.suffix == ".json":
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            path.write_text(markdown, encoding="utf-8")

    return {key: str(path) for key, path in outputs.items()}


def default_input_paths() -> DashboardPaths:
    paths = get_project_paths(REPO_ROOT_CANDIDATE)
    logs_root = paths.logs_root

    return DashboardPaths(
        manifest=logs_root / "latest_official_runtime_manifest.json",
        source_runtime_health=logs_root / "latest_source_runtime_health.json",
        daily_summary=logs_root / "latest_daily_source_run_summary.json",
        quality_gate=logs_root / "latest_official_lane_quality_gate.json",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build official daily dashboard.")
    parser.add_argument("--run-date", default=datetime.now().strftime("%Y%m%d"))
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--source-runtime-health", type=Path)
    parser.add_argument("--daily-summary", type=Path)
    parser.add_argument("--quality-gate", type=Path)
    parser.add_argument("--json", action="store_true", help="Print dashboard JSON to stdout.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    defaults = default_input_paths()
    inputs = DashboardPaths(
        manifest=args.manifest or defaults.manifest,
        source_runtime_health=args.source_runtime_health or defaults.source_runtime_health,
        daily_summary=args.daily_summary or defaults.daily_summary,
        quality_gate=args.quality_gate or defaults.quality_gate,
    )

    manifest = read_json(inputs.manifest)
    runtime_health = read_json(inputs.source_runtime_health)
    daily_summary = read_json(inputs.daily_summary)
    quality_gate = read_json(inputs.quality_gate)

    payload = build_dashboard_payload(
        args.run_date,
        inputs,
        manifest,
        runtime_health,
        daily_summary,
        quality_gate,
    )
    markdown = render_markdown(payload)
    outputs = write_outputs(payload, markdown)

    if args.json:
        print(json.dumps({**payload, "outputs": outputs}, ensure_ascii=False, indent=2))
        return 0

    print("Official Daily Dashboard")
    print("========================")
    print(f"status: {payload['status']}")
    print(f"run_date: {payload['run_date']}")
    print(f"manifest_status: {payload['official_lane']['manifest_status']}")
    print(f"source_count: {payload['official_lane']['source_count']}")
    print(f"total_items_found: {payload['official_lane']['total_items_found']}")
    print(f"missing_expected: {payload['source_runtime_health']['missing_expected']}")
    print(f"quality_gate: {payload['quality_gate']['level']}")
    print("")
    print("Reports:")
    for key, value in outputs.items():
        print(f"  {key}: {value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build a compact daily source run summary.

P0-013 reads the latest official runtime manifest and source runtime health
reports, then writes a small daily summary for human review. It does not fetch
remote sources, retry failed sources, or modify existing pipeline outputs.
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
class DailySourceRunSummary:
    schema_version: str
    generated_at: str
    run_date: str
    status: str
    manifest_path: str | None
    source_runtime_health_path: str | None
    source_count: int
    total_items_found: int
    total_items_written: int
    enabled_sources: int | None
    observed_sources: int | None
    missing_expected: int | None
    error_hint_sources: int | None
    status_distribution: dict[str, int]
    key_outputs: dict[str, str | None]
    warnings: list[str]


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def int_or_zero(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return 0
    return 0


def first_int(*values: Any) -> int | None:
    for value in values:
        if value is None:
            continue
        if isinstance(value, dict):
            continue
        return int_or_zero(value)
    return None


def read_manifest_counts(manifest: dict[str, Any] | None) -> tuple[str, int, int, int, str | None]:
    if not manifest:
        return "MISSING_MANIFEST", 0, 0, 0, None

    sources = manifest.get("sources")
    if not isinstance(sources, list):
        sources = []

    source_count = first_int(manifest.get("source_count"), len(sources)) or 0
    items_found = first_int(
        manifest.get("total_items_found"),
        manifest.get("items_found"),
        sum(int_or_zero(item.get("items_found") or item.get("item_count")) for item in sources if isinstance(item, dict)),
    ) or 0
    items_written = first_int(
        manifest.get("total_items_written"),
        manifest.get("items_written"),
        sum(int_or_zero(item.get("items_written") or item.get("written_count")) for item in sources if isinstance(item, dict)),
    ) or 0
    status = str(manifest.get("status") or "UNKNOWN")
    run_date = manifest.get("run_date") or manifest.get("date")
    return status, source_count, items_found, items_written, str(run_date) if run_date else None


def find_summary_dict(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not payload:
        return {}
    summary = payload.get("summary")
    if isinstance(summary, dict):
        return summary
    return payload


def read_runtime_health_counts(payload: dict[str, Any] | None) -> tuple[int | None, int | None, int | None, int | None, dict[str, int]]:
    summary = find_summary_dict(payload)
    if not summary:
        return None, None, None, None, {}

    distribution = summary.get("status_distribution") or payload.get("status_distribution") if payload else {}
    if not isinstance(distribution, dict):
        distribution = {}
    normalized_distribution = {str(k): int_or_zero(v) for k, v in distribution.items()}

    enabled = first_int(summary.get("enabled"), summary.get("enabled_sources"), summary.get("enabled_count"))
    observed = first_int(summary.get("observed"), summary.get("observed_sources"), normalized_distribution.get("OBSERVED"))
    missing = first_int(summary.get("missing_expected"), normalized_distribution.get("MISSING_EXPECTED"))
    error_hints = first_int(
        summary.get("error_hint_sources"),
        summary.get("observed_with_error_hints"),
        normalized_distribution.get("OBSERVED_WITH_ERROR_HINTS"),
    )
    return enabled, observed, missing, error_hints, normalized_distribution


def build_markdown(summary: DailySourceRunSummary) -> str:
    warnings = "\n".join(f"- {item}" for item in summary.warnings) if summary.warnings else "- 无"
    distribution = "\n".join(
        f"- {key}: {value}" for key, value in sorted(summary.status_distribution.items())
    ) or "- 无"
    outputs = "\n".join(
        f"- {key}: `{value}`" for key, value in summary.key_outputs.items() if value
    ) or "- 无"

    return f"""# Daily Source Run Summary

生成时间：{summary.generated_at}
运行日期：{summary.run_date}
状态：{summary.status}

## Official Lane

- source_count：{summary.source_count}
- total_items_found：{summary.total_items_found}
- total_items_written：{summary.total_items_written}
- runtime_manifest：`{summary.manifest_path}`

## Source Runtime Health

- enabled_sources：{summary.enabled_sources if summary.enabled_sources is not None else '未知'}
- observed_sources：{summary.observed_sources if summary.observed_sources is not None else '未知'}
- missing_expected：{summary.missing_expected if summary.missing_expected is not None else '未知'}
- error_hint_sources：{summary.error_hint_sources if summary.error_hint_sources is not None else '未知'}
- source_runtime_health：`{summary.source_runtime_health_path}`

## Status Distribution

{distribution}

## Key Outputs

{outputs}

## Warnings

{warnings}
"""


def write_outputs(summary: DailySourceRunSummary, logs_root: Path, frontstage_root: Path) -> dict[str, Path]:
    logs_root.mkdir(parents=True, exist_ok=True)
    frontstage_root.mkdir(parents=True, exist_ok=True)

    dated_json = logs_root / f"{summary.run_date}__daily-source-run-summary.json"
    latest_json = logs_root / "latest_daily_source_run_summary.json"
    dated_md = logs_root / f"{summary.run_date}__daily-source-run-summary.md"
    latest_md = logs_root / "latest_daily_source_run_summary.md"
    frontstage_dated = frontstage_root / f"{summary.run_date}__daily-source-run-summary-board.md"
    frontstage_latest = frontstage_root / "latest_daily_source_run_summary_board.md"

    payload = json.dumps(asdict(summary), ensure_ascii=False, indent=2)
    markdown = build_markdown(summary)

    for path in (dated_json, latest_json):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (dated_md, latest_md, frontstage_dated, frontstage_latest):
        path.write_text(markdown, encoding="utf-8")

    return {
        "dated_json": dated_json,
        "latest_json": latest_json,
        "dated_md": dated_md,
        "latest_md": latest_md,
        "frontstage_dated_md": frontstage_dated,
        "frontstage_latest_md": frontstage_latest,
    }


def build_summary(run_date: str | None = None) -> tuple[DailySourceRunSummary, dict[str, Path]]:
    paths = get_project_paths(REPO_ROOT_CANDIDATE)
    logs_root = paths.logs_root
    frontstage_root = paths.frontstage_root

    official_manifest_path = logs_root / "latest_official_runtime_manifest.json"
    source_runtime_health_path = logs_root / "latest_source_runtime_health.json"

    manifest = load_json(official_manifest_path)
    runtime_health = load_json(source_runtime_health_path)

    manifest_status, source_count, total_items_found, total_items_written, manifest_run_date = read_manifest_counts(manifest)
    enabled, observed, missing, error_hints, distribution = read_runtime_health_counts(runtime_health)

    warnings: list[str] = []
    if manifest is None:
        warnings.append("latest_official_runtime_manifest.json not found or unreadable; run make official-lane-daily first.")
    if runtime_health is None:
        warnings.append("latest_source_runtime_health.json not found or unreadable; run make source-runtime-health first.")

    final_run_date = run_date or manifest_run_date or datetime.now().strftime("%Y%m%d")
    if "-" in final_run_date:
        final_run_date = final_run_date.replace("-", "")

    status = "SUCCESS" if manifest_status == "SUCCESS" and runtime_health is not None else "DEGRADED"
    if manifest is None and runtime_health is None:
        status = "MISSING_DATA"

    summary = DailySourceRunSummary(
        schema_version="v1",
        generated_at=datetime.now(timezone.utc).isoformat(),
        run_date=final_run_date,
        status=status,
        manifest_path=str(official_manifest_path) if official_manifest_path.exists() else None,
        source_runtime_health_path=str(source_runtime_health_path) if source_runtime_health_path.exists() else None,
        source_count=source_count,
        total_items_found=total_items_found,
        total_items_written=total_items_written,
        enabled_sources=enabled,
        observed_sources=observed,
        missing_expected=missing,
        error_hint_sources=error_hints,
        status_distribution=distribution,
        key_outputs={
            "official_runtime_manifest": str(official_manifest_path) if official_manifest_path.exists() else None,
            "source_runtime_health": str(source_runtime_health_path) if source_runtime_health_path.exists() else None,
        },
        warnings=warnings,
    )
    outputs = write_outputs(summary, logs_root, frontstage_root)
    return summary, outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Build daily source run summary.")
    parser.add_argument("--date", dest="run_date", help="Run date in YYYYMMDD or YYYY-MM-DD format.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary to stdout.")
    args = parser.parse_args()

    summary, outputs = build_summary(args.run_date)

    if args.json:
        print(json.dumps(asdict(summary), ensure_ascii=False, indent=2))
        return 0

    print("Daily Source Run Summary")
    print("========================")
    print(f"status: {summary.status}")
    print(f"run_date: {summary.run_date}")
    print(f"source_count: {summary.source_count}")
    print(f"total_items_found: {summary.total_items_found}")
    print(f"missing_expected: {summary.missing_expected if summary.missing_expected is not None else 'unknown'}")
    print(f"error_hint_sources: {summary.error_hint_sources if summary.error_hint_sources is not None else 'unknown'}")
    print("\nReports:")
    for name, path in outputs.items():
        print(f"  {name}: {path}")

    if summary.warnings:
        print("\nWarnings:")
        for warning in summary.warnings:
            print(f"  - {warning}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

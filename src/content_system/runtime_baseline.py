"""Official lane runtime baseline helpers for Phase 1.

P1-001 keeps a small daily baseline for the official lane. It reads the
generated Phase 0 sidecar artifacts, upserts one record per run date, and writes
JSON/Markdown reports. It does not fetch remote sources or change fetcher
behavior.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class RuntimeBaselineRecord:
    run_date: str
    status: str
    quality_gate_status: str
    source_count: int
    total_items_found: int
    total_items_written: int
    missing_expected: int
    error_hint_sources: int
    dashboard_status: str
    official_runtime_manifest: str
    daily_summary: str
    quality_gate: str
    full_run: str


@dataclass(frozen=True)
class RuntimeBaseline:
    schema_version: str
    updated_at: str
    records: tuple[RuntimeBaselineRecord, ...]
    summary: dict[str, Any]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def safe_int(value: Any, default: int = 0) -> int:
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
            return default
    return default


def nested_get(payload: dict[str, Any], *keys: str) -> Any:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def normalize_date(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return today_token()
    return text.replace("-", "")[:8]


def baseline_paths(paths: ProjectPaths) -> dict[str, Path]:
    return {
        "json": paths.logs_root / "official_runtime_baseline.json",
        "md": paths.logs_root / "official_runtime_baseline.md",
        "frontstage_md": paths.frontstage_root / "official_runtime_baseline_board.md",
    }


def build_record(paths: ProjectPaths, run_date: str | None = None) -> RuntimeBaselineRecord:
    logs_root = paths.logs_root
    manifest_path = logs_root / "latest_official_runtime_manifest.json"
    summary_path = logs_root / "latest_daily_source_run_summary.json"
    gate_path = logs_root / "latest_official_lane_quality_gate.json"
    dashboard_path = logs_root / "latest_official_daily_dashboard.json"
    full_run_path = logs_root / "latest_official_daily_full_run.json"

    manifest = read_json(manifest_path)
    daily_summary = read_json(summary_path)
    quality_gate = read_json(gate_path)
    dashboard = read_json(dashboard_path)
    full_run = read_json(full_run_path)

    final_run_date = normalize_date(
        run_date
        or full_run.get("run_date")
        or manifest.get("run_date")
        or daily_summary.get("run_date")
        or dashboard.get("run_date")
    )

    return RuntimeBaselineRecord(
        run_date=final_run_date,
        status=str(full_run.get("status") or dashboard.get("status") or manifest.get("status") or "UNKNOWN"),
        quality_gate_status=str(
            full_run.get("summary", {}).get("quality_gate_status")
            or quality_gate.get("gate_status")
            or quality_gate.get("level")
            or quality_gate.get("status")
            or "UNKNOWN"
        ),
        source_count=safe_int(
            full_run.get("summary", {}).get("source_count")
            or manifest.get("source_count")
            or daily_summary.get("source_count")
        ),
        total_items_found=safe_int(
            full_run.get("summary", {}).get("total_items_found")
            or manifest.get("total_items_found")
            or daily_summary.get("total_items_found")
        ),
        total_items_written=safe_int(
            full_run.get("summary", {}).get("total_items_written")
            or manifest.get("total_items_written")
            or daily_summary.get("total_items_written")
        ),
        missing_expected=safe_int(
            nested_get(dashboard, "source_runtime_health", "missing_expected")
            or daily_summary.get("missing_expected")
        ),
        error_hint_sources=safe_int(
            nested_get(dashboard, "source_runtime_health", "error_hint_sources")
            or daily_summary.get("error_hint_sources")
        ),
        dashboard_status=str(dashboard.get("status") or "UNKNOWN"),
        official_runtime_manifest=repo_relative(manifest_path, paths.repo_root) if manifest_path.exists() else "",
        daily_summary=repo_relative(summary_path, paths.repo_root) if summary_path.exists() else "",
        quality_gate=repo_relative(gate_path, paths.repo_root) if gate_path.exists() else "",
        full_run=repo_relative(full_run_path, paths.repo_root) if full_run_path.exists() else "",
    )


def summarize_records(records: tuple[RuntimeBaselineRecord, ...]) -> dict[str, Any]:
    item_counts = [record.total_items_found for record in records]
    success_count = sum(1 for record in records if record.status == "SUCCESS")
    green_count = sum(1 for record in records if record.quality_gate_status == "GREEN")
    yellow_count = sum(1 for record in records if record.quality_gate_status == "YELLOW")
    red_count = sum(1 for record in records if record.quality_gate_status == "RED")
    return {
        "record_count": len(records),
        "success_count": success_count,
        "green_count": green_count,
        "yellow_count": yellow_count,
        "red_count": red_count,
        "avg_total_items_found": round(sum(item_counts) / len(item_counts), 2) if item_counts else 0.0,
        "min_total_items_found": min(item_counts) if item_counts else 0,
        "max_total_items_found": max(item_counts) if item_counts else 0,
    }


def record_from_dict(payload: dict[str, Any]) -> RuntimeBaselineRecord:
    return RuntimeBaselineRecord(
        run_date=str(payload.get("run_date") or ""),
        status=str(payload.get("status") or "UNKNOWN"),
        quality_gate_status=str(payload.get("quality_gate_status") or "UNKNOWN"),
        source_count=safe_int(payload.get("source_count")),
        total_items_found=safe_int(payload.get("total_items_found")),
        total_items_written=safe_int(payload.get("total_items_written")),
        missing_expected=safe_int(payload.get("missing_expected")),
        error_hint_sources=safe_int(payload.get("error_hint_sources")),
        dashboard_status=str(payload.get("dashboard_status") or "UNKNOWN"),
        official_runtime_manifest=str(payload.get("official_runtime_manifest") or ""),
        daily_summary=str(payload.get("daily_summary") or ""),
        quality_gate=str(payload.get("quality_gate") or ""),
        full_run=str(payload.get("full_run") or ""),
    )


def load_existing_baseline(path: Path) -> tuple[RuntimeBaselineRecord, ...]:
    payload = read_json(path)
    records = payload.get("records")
    if not isinstance(records, list):
        return ()
    return tuple(record_from_dict(item) for item in records if isinstance(item, dict))


def upsert_record(records: tuple[RuntimeBaselineRecord, ...], record: RuntimeBaselineRecord) -> tuple[RuntimeBaselineRecord, ...]:
    by_date = {item.run_date: item for item in records if item.run_date}
    by_date[record.run_date] = record
    return tuple(by_date[key] for key in sorted(by_date))


def update_runtime_baseline(paths: ProjectPaths, run_date: str | None = None) -> RuntimeBaseline:
    output_paths = baseline_paths(paths)
    existing = load_existing_baseline(output_paths["json"])
    record = build_record(paths, run_date=run_date)
    records = upsert_record(existing, record)
    return RuntimeBaseline(
        schema_version=SCHEMA_VERSION,
        updated_at=utc_now(),
        records=records,
        summary=summarize_records(records),
    )


def baseline_to_dict(baseline: RuntimeBaseline) -> dict[str, Any]:
    return asdict(baseline)


def render_markdown(baseline: RuntimeBaseline) -> str:
    rows = []
    for record in baseline.records[-30:]:
        rows.append(
            "| "
            + " | ".join(
                [
                    record.run_date,
                    record.status,
                    record.quality_gate_status,
                    str(record.source_count),
                    str(record.total_items_found),
                    str(record.missing_expected),
                    str(record.error_hint_sources),
                    record.dashboard_status,
                ]
            )
            + " |"
        )
    table = "\n".join(rows) if rows else "| - | - | - | 0 | 0 | 0 | 0 | - |"
    summary = baseline.summary
    return f"""# Official Runtime Baseline

## Summary

- Updated at: `{baseline.updated_at}`
- Records: `{summary['record_count']}`
- Success runs: `{summary['success_count']}`
- Green quality gates: `{summary['green_count']}`
- Avg total items found: `{summary['avg_total_items_found']}`
- Min total items found: `{summary['min_total_items_found']}`
- Max total items found: `{summary['max_total_items_found']}`

## Records

| Date | Status | Gate | Sources | Items Found | Missing Expected | Error Hint Sources | Dashboard |
|---|---|---|---:|---:|---:|---:|---|
{table}

## Notes

- 同一天重复运行会更新同一条 record，而不是追加重复日期。
- 该 baseline 只记录官方 lane 日常运行指标，不做 retry/fallback，不改变 fetcher。
"""


def write_runtime_baseline(baseline: RuntimeBaseline, paths: ProjectPaths) -> dict[str, Path]:
    output_paths = baseline_paths(paths)
    for path in output_paths.values():
        path.parent.mkdir(parents=True, exist_ok=True)

    payload = json.dumps(baseline_to_dict(baseline), ensure_ascii=False, indent=2)
    markdown = render_markdown(baseline)
    output_paths["json"].write_text(payload + "\n", encoding="utf-8")
    output_paths["md"].write_text(markdown, encoding="utf-8")
    output_paths["frontstage_md"].write_text(markdown, encoding="utf-8")
    return output_paths

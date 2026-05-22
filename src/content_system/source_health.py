"""Source health reporting helpers.

P0-006 deliberately keeps this module static and registry-driven. It does not
fetch remote sources, retry failed fetches, or change existing ingestion scripts.
It turns the Source Registry into a daily coverage/health snapshot so that the
next step can add runtime fetch status without changing the registry contract.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from content_system.paths import ProjectPaths
from content_system.sources import SourceConfig, SourceRegistry, ValidationIssue, validate_registry


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class SourceHealthRecord:
    """Static health view for one configured source."""

    source_id: str
    label: str
    tier: str
    category: str
    language: str
    enabled: bool
    fetch_method: str
    primary_url: str
    fallback_methods: tuple[str, ...]
    expected_frequency: str
    expected_min_items_per_run: int
    health_status: str
    health_reason: str
    registry_warnings: tuple[str, ...]


@dataclass(frozen=True)
class SourceHealthReport:
    """Static source-health report generated from config/sources.yaml."""

    schema_version: str
    generated_at: str
    registry_schema_version: str
    source_count: int
    enabled_count: int
    disabled_count: int
    issue_summary: dict[str, int]
    tier_distribution: dict[str, int]
    category_distribution: dict[str, int]
    method_distribution: dict[str, int]
    records: tuple[SourceHealthRecord, ...]
    validation_issues: tuple[ValidationIssue, ...]


def _issue_summary(issues: Iterable[ValidationIssue]) -> dict[str, int]:
    counts = Counter(issue.severity for issue in issues)
    return {
        "ERROR": counts.get("ERROR", 0),
        "WARN": counts.get("WARN", 0),
    }


def _source_warnings(source: SourceConfig) -> tuple[str, ...]:
    warnings: list[str] = []

    if not source.fallback_methods:
        warnings.append("missing fallback_methods")

    if source.enabled and source.expected_frequency == "ad_hoc":
        warnings.append("enabled source is ad_hoc; source health should not expect daily updates")

    if source.expected_min_items_per_run > 0 and source.expected_frequency == "weekly":
        warnings.append("weekly source has positive per-run expectation; review alert thresholds later")

    return tuple(warnings)


def _health_status(source: SourceConfig, warnings: tuple[str, ...]) -> tuple[str, str]:
    if not source.enabled:
        return "DISABLED", "source disabled in registry"

    if warnings:
        return "WATCH", "; ".join(warnings)

    return "READY", "registry entry is enabled and structurally complete"


def _record_from_source(source: SourceConfig) -> SourceHealthRecord:
    warnings = _source_warnings(source)
    status, reason = _health_status(source, warnings)

    return SourceHealthRecord(
        source_id=source.source_id,
        label=source.label,
        tier=source.tier,
        category=source.category,
        language=source.language,
        enabled=source.enabled,
        fetch_method=source.fetch_method,
        primary_url=source.primary_url,
        fallback_methods=source.fallback_methods,
        expected_frequency=source.expected_frequency,
        expected_min_items_per_run=source.expected_min_items_per_run,
        health_status=status,
        health_reason=reason,
        registry_warnings=warnings,
    )


def build_source_health_report(registry: SourceRegistry) -> SourceHealthReport:
    """Build a static health report from the registry.

    This is intentionally not a live network health check. Runtime fetch status,
    retry/fallback outcomes, and per-source success metrics are left for P0-007+
    once the existing fetchers are wired into the registry.
    """

    issues = validate_registry(registry)
    records = tuple(_record_from_source(source) for source in registry.sources)
    enabled_count = sum(1 for source in registry.sources if source.enabled)

    return SourceHealthReport(
        schema_version=SCHEMA_VERSION,
        generated_at=datetime.now(timezone.utc).isoformat(),
        registry_schema_version=registry.schema_version,
        source_count=len(registry.sources),
        enabled_count=enabled_count,
        disabled_count=len(registry.sources) - enabled_count,
        issue_summary=_issue_summary(issues),
        tier_distribution=dict(sorted(registry.tier_counts().items())),
        category_distribution=dict(sorted(registry.category_counts().items())),
        method_distribution=dict(sorted(Counter(source.fetch_method for source in registry.sources).items())),
        records=records,
        validation_issues=issues,
    )


def report_to_dict(report: SourceHealthReport) -> dict:
    """Convert a report into a JSON-serializable dictionary."""

    payload = asdict(report)
    return payload


def write_json_report(report: SourceHealthReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2), encoding="utf-8")


def _escape_table_cell(value: object) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def render_markdown_report(report: SourceHealthReport, max_records: int = 200) -> str:
    lines: list[str] = []
    lines.append("# Source Health v1 报告")
    lines.append("")
    lines.append("> P0-006：静态 source health / coverage 报告。此报告只基于 `config/sources.yaml`，不进行网络抓取。")
    lines.append("")
    lines.append("## 摘要")
    lines.append("")
    lines.append(f"- 生成时间：`{report.generated_at}`")
    lines.append(f"- Registry schema：`{report.registry_schema_version}`")
    lines.append(f"- Sources 总数：`{report.source_count}`")
    lines.append(f"- Enabled：`{report.enabled_count}`")
    lines.append(f"- Disabled：`{report.disabled_count}`")
    lines.append(f"- Validation ERROR：`{report.issue_summary.get('ERROR', 0)}`")
    lines.append(f"- Validation WARN：`{report.issue_summary.get('WARN', 0)}`")
    lines.append("")

    lines.append("## Tier 分布")
    lines.append("")
    for tier, count in report.tier_distribution.items():
        lines.append(f"- `{tier}`：{count}")
    lines.append("")

    lines.append("## Category 分布")
    lines.append("")
    for category, count in report.category_distribution.items():
        lines.append(f"- `{category}`：{count}")
    lines.append("")

    lines.append("## Fetch Method 分布")
    lines.append("")
    for method, count in report.method_distribution.items():
        lines.append(f"- `{method}`：{count}")
    lines.append("")

    lines.append("## Source Health 明细")
    lines.append("")
    lines.append("| Source | Tier | Category | Enabled | Method | Frequency | Status | Reason |")
    lines.append("|---|---:|---|---:|---|---|---|---|")
    for record in report.records[:max_records]:
        lines.append(
            "| "
            + " | ".join(
                [
                    _escape_table_cell(record.source_id),
                    _escape_table_cell(record.tier),
                    _escape_table_cell(record.category),
                    _escape_table_cell(record.enabled),
                    _escape_table_cell(record.fetch_method),
                    _escape_table_cell(record.expected_frequency),
                    _escape_table_cell(record.health_status),
                    _escape_table_cell(record.health_reason),
                ]
            )
            + " |"
        )
    if len(report.records) > max_records:
        lines.append("")
        lines.append(f"> 仅展示前 {max_records} 条；JSON 报告保留全部 records。")
    lines.append("")

    if report.validation_issues:
        lines.append("## Validation Issues")
        lines.append("")
        lines.append("| Severity | Source | Field | Message |")
        lines.append("|---|---|---|---|")
        for issue in report.validation_issues:
            lines.append(
                "| "
                + " | ".join(
                    [
                        _escape_table_cell(issue.severity),
                        _escape_table_cell(issue.source_id or "<registry>"),
                        _escape_table_cell(issue.field or "<unknown>"),
                        _escape_table_cell(issue.message),
                    ]
                )
                + " |"
            )
        lines.append("")
    else:
        lines.append("## Validation Issues")
        lines.append("")
        lines.append("无。")
        lines.append("")

    lines.append("## 下一步")
    lines.append("")
    lines.append("- P0-007 可开始把现有抓取脚本的运行结果回填到 source health。")
    lines.append("- 暂不做网络抓取、不做 retry、不改变 fetcher 输出格式。")
    lines.append("")
    return "\n".join(lines)


def write_markdown_report(report: SourceHealthReport, path: Path, max_records: int = 200) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown_report(report, max_records=max_records), encoding="utf-8")


def default_report_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    """Return default generated report paths for logs and frontstage."""

    return {
        "dated_json": paths.logs_root / f"{run_date}__source-health.json",
        "dated_md": paths.logs_root / f"{run_date}__source-health.md",
        "latest_json": paths.logs_root / "latest_source_health.json",
        "latest_md": paths.logs_root / "latest_source_health.md",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__source-health-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_source_health_board.md",
    }


def write_default_reports(
    report: SourceHealthReport,
    paths: ProjectPaths,
    run_date: str,
    max_records: int = 200,
) -> dict[str, Path]:
    output_paths = default_report_paths(paths, run_date)

    write_json_report(report, output_paths["dated_json"])
    write_json_report(report, output_paths["latest_json"])
    write_markdown_report(report, output_paths["dated_md"], max_records=max_records)
    write_markdown_report(report, output_paths["latest_md"], max_records=max_records)
    write_markdown_report(report, output_paths["frontstage_dated_md"], max_records=max_records)
    write_markdown_report(report, output_paths["frontstage_latest_md"], max_records=max_records)

    return output_paths

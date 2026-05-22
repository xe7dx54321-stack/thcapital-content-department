"""Source registry coverage alignment for Phase 1.

P1-002 compares config/sources.yaml with runtime manifest and runtime health
artifacts. It is a read-only alignment report: it does not rename existing
fetcher source IDs or change capture behavior.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.runtime_manifest import RuntimeManifest, SourceRunRecord, load_runtime_manifest
from content_system.sources import SourceConfig, SourceRegistry

SCHEMA_VERSION = "v1"

RUNTIME_TO_REGISTRY_ALIASES = {
    "web__openai_news": "openai_blog",
    "x__openai": "openai_blog",
    "x__openaidevs": "openai_blog",
    "web__anthropic_news": "anthropic_news",
    "x__anthropic_ai": "anthropic_news",
    "web__deepmind_blog": "google_deepmind_blog",
    "web__google_blog_ai": "google_ai_blog",
    "web__nvidia_blog": "nvidia_technical_blog",
}


@dataclass(frozen=True)
class RuntimeCoverageEvidence:
    artifact: str
    runtime_source_id: str
    status: str
    items_found: int
    matched_by: str


@dataclass(frozen=True)
class SourceCoverageRecord:
    source_id: str
    label: str
    tier: str
    category: str
    enabled: bool
    coverage_status: str
    runtime_evidence: tuple[RuntimeCoverageEvidence, ...]
    notes: str


@dataclass(frozen=True)
class RuntimeOnlySource:
    source_id: str
    label: str
    status: str
    items_found: int
    artifact: str
    notes: str


@dataclass(frozen=True)
class SourceCoverageReport:
    schema_version: str
    generated_at: str
    run_date: str
    registry_source_count: int
    runtime_source_count: int
    covered_count: int
    registry_only_count: int
    runtime_only_count: int
    status_distribution: dict[str, int]
    sources: tuple[SourceCoverageRecord, ...]
    runtime_only_sources: tuple[RuntimeOnlySource, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def normalize_date(value: str | None) -> str:
    if not value:
        return today_token()
    return value.replace("-", "")[:8]


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


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def runtime_source_label(source: SourceRunRecord) -> str:
    return source.notes or source.source_id


def load_latest_manifest(paths: ProjectPaths) -> RuntimeManifest | None:
    path = paths.logs_root / "latest_official_runtime_manifest.json"
    if not path.exists():
        return None
    try:
        return load_runtime_manifest(path)
    except (OSError, json.JSONDecodeError, ValueError):
        return None


def runtime_health_observed_ids(paths: ProjectPaths) -> set[str]:
    payload = read_json(paths.logs_root / "latest_source_runtime_health.json")
    records = payload.get("records")
    if not isinstance(records, list):
        return set()
    observed: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            continue
        if safe_int(record.get("evidence_count")) > 0 or str(record.get("runtime_status")) in {
            "OBSERVED",
            "OBSERVED_WITH_ERROR_HINTS",
        }:
            source_id = str(record.get("source_id") or "")
            if source_id:
                observed.add(source_id)
    return observed


def build_source_coverage_report(
    registry: SourceRegistry,
    paths: ProjectPaths,
    run_date: str | None = None,
) -> SourceCoverageReport:
    manifest = load_latest_manifest(paths)
    final_run_date = normalize_date(run_date or (manifest.run_date if manifest else None))
    manifest_path = paths.logs_root / "latest_official_runtime_manifest.json"
    manifest_rel = repo_relative(manifest_path, paths.repo_root)

    registry_ids = {source.source_id for source in registry.sources}
    evidence_by_registry: dict[str, list[RuntimeCoverageEvidence]] = {source.source_id: [] for source in registry.sources}
    runtime_only: list[RuntimeOnlySource] = []
    runtime_source_count = 0

    if manifest is not None:
        runtime_source_count = len(manifest.sources)
        for source_run in manifest.sources:
            matched_registry_id = source_run.source_id if source_run.source_id in registry_ids else RUNTIME_TO_REGISTRY_ALIASES.get(source_run.source_id)
            matched_by = "source_id" if matched_registry_id == source_run.source_id else "alias"
            if matched_registry_id and matched_registry_id in registry_ids:
                evidence_by_registry[matched_registry_id].append(
                    RuntimeCoverageEvidence(
                        artifact=manifest_rel,
                        runtime_source_id=source_run.source_id,
                        status=source_run.status,
                        items_found=source_run.items_found,
                        matched_by=matched_by,
                    )
                )
            else:
                runtime_only.append(
                    RuntimeOnlySource(
                        source_id=source_run.source_id,
                        label=runtime_source_label(source_run),
                        status=source_run.status,
                        items_found=source_run.items_found,
                        artifact=manifest_rel,
                        notes="Runtime source is not yet defined in config/sources.yaml.",
                    )
                )

    observed_by_health = runtime_health_observed_ids(paths)
    records: list[SourceCoverageRecord] = []
    for source in registry.sources:
        evidence = tuple(evidence_by_registry.get(source.source_id, ()))
        if not source.enabled:
            coverage_status = "DISABLED"
            notes = "Source disabled in registry."
        elif evidence:
            coverage_status = "COVERED_BY_RUNTIME_MANIFEST"
            notes = "Matched official runtime manifest by source_id or known alias."
        elif source.source_id in observed_by_health:
            coverage_status = "OBSERVED_BY_HEALTH_SCAN"
            notes = "Observed by source runtime health scan, but not present in latest official manifest."
        else:
            coverage_status = "REGISTRY_ONLY"
            notes = "Configured in registry, but no runtime evidence in latest official artifacts."

        records.append(
            SourceCoverageRecord(
                source_id=source.source_id,
                label=source.label,
                tier=source.tier,
                category=source.category,
                enabled=source.enabled,
                coverage_status=coverage_status,
                runtime_evidence=evidence,
                notes=notes,
            )
        )

    status_counts = Counter(record.coverage_status for record in records)
    return SourceCoverageReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        registry_source_count=len(registry.sources),
        runtime_source_count=runtime_source_count,
        covered_count=status_counts.get("COVERED_BY_RUNTIME_MANIFEST", 0)
        + status_counts.get("OBSERVED_BY_HEALTH_SCAN", 0),
        registry_only_count=status_counts.get("REGISTRY_ONLY", 0),
        runtime_only_count=len(runtime_only),
        status_distribution=dict(sorted(status_counts.items())),
        sources=tuple(records),
        runtime_only_sources=tuple(runtime_only),
    )


def report_to_dict(report: SourceCoverageReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: SourceCoverageReport) -> str:
    source_rows = []
    for record in report.sources:
        runtime_ids = ", ".join(item.runtime_source_id for item in record.runtime_evidence) or "-"
        items = sum(item.items_found for item in record.runtime_evidence)
        source_rows.append(
            "| "
            + " | ".join(
                [
                    escape_cell(record.source_id),
                    escape_cell(record.tier),
                    escape_cell(record.category),
                    escape_cell(record.coverage_status),
                    escape_cell(runtime_ids),
                    str(items),
                    escape_cell(record.notes),
                ]
            )
            + " |"
        )

    runtime_only_rows = []
    for source in report.runtime_only_sources:
        runtime_only_rows.append(
            "| "
            + " | ".join(
                [
                    escape_cell(source.source_id),
                    escape_cell(source.label),
                    escape_cell(source.status),
                    str(source.items_found),
                    escape_cell(source.notes),
                ]
            )
            + " |"
        )

    status_lines = "\n".join(f"- `{key}`: {value}" for key, value in report.status_distribution.items())
    return f"""# Source Coverage Alignment

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Registry sources: `{report.registry_source_count}`
- Runtime sources: `{report.runtime_source_count}`
- Covered sources: `{report.covered_count}`
- Registry-only sources: `{report.registry_only_count}`
- Runtime-only sources: `{report.runtime_only_count}`

## Coverage Status

{status_lines or '- None'}

## Registry Sources

| Source | Tier | Category | Coverage | Runtime IDs | Items Found | Notes |
|---|---:|---|---|---|---:|---|
{chr(10).join(source_rows)}

## Runtime-only Sources

| Runtime Source | Label | Status | Items Found | Notes |
|---|---|---|---:|---|
{chr(10).join(runtime_only_rows) if runtime_only_rows else '| - | - | - | 0 | None |'}

## Notes

- Alias matches are explicit and conservative; this report does not rename fetcher source IDs.
- Registry-only sources are expected in v1 while non-official lanes are not fully manifest-backed.
"""


def default_output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__source-coverage-alignment.json",
        "dated_md": paths.logs_root / f"{run_date}__source-coverage-alignment.md",
        "latest_json": paths.logs_root / "latest_source_coverage_alignment.json",
        "latest_md": paths.logs_root / "latest_source_coverage_alignment.md",
        "frontstage_md": paths.frontstage_root / "latest_source_coverage_alignment_board.md",
    }


def write_source_coverage_report(report: SourceCoverageReport, paths: ProjectPaths) -> dict[str, Path]:
    output_paths = default_output_paths(paths, report.run_date)
    for path in output_paths.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)
    for path in (output_paths["dated_json"], output_paths["latest_json"]):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (output_paths["dated_md"], output_paths["latest_md"], output_paths["frontstage_md"]):
        path.write_text(markdown, encoding="utf-8")
    return output_paths

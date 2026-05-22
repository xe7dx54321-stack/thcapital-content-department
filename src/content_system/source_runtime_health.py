"""Runtime source health adapter.

P0-007 connected the Source Registry with existing generated runtime artifacts
(manifests, source packets, and logs) without changing fetchers, retry behavior,
fallback behavior, scheduling, or persistence.

P0-011A upgrades the adapter to prefer structured P0-008 runtime manifests when
those manifests are available. The older best-effort text scan remains as a
fallback for legacy artifacts that do not yet implement the manifest contract.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from content_system.paths import ProjectPaths
from content_system.runtime_manifest import RuntimeManifest, load_runtime_manifest
from content_system.sources import SourceConfig, SourceRegistry

SCHEMA_VERSION = "v1"
MAX_TEXT_BYTES = 800_000

RUNTIME_MANIFEST_GLOBS = (
    "10_logs/*runtime-manifest*.json",
    "10_logs/*runtime_manifest*.json",
    "10_logs/latest_*runtime_manifest*.json",
)

RUNTIME_ARTIFACT_GLOBS = (
    "10_logs/*manifest*.md",
    "10_logs/*manifest*.json",
    "10_logs/*source*.md",
    "10_logs/*source*.json",
    "02_topic_radar/source_packets/**/*.md",
    "02_topic_radar/source_packets/**/*.json",
)

ERROR_PATTERNS = (
    re.compile(r"\b(error|failed|failure|exception|traceback|timeout|unreachable)\b", re.IGNORECASE),
    re.compile(r"失败|错误|异常|超时|不可达"),
)

GENERATED_REPORT_NAME_MARKERS = (
    "source-coverage-alignment",
    "source_coverage_alignment",
    "runtime-baseline",
    "runtime_baseline",
    "phase1-daily-pipeline",
    "phase1_daily_pipeline",
    "evidence-packets",
    "evidence_packets",
    "topic-clusters",
    "topic_clusters",
    "topic-cluster-scores",
    "topic_cluster_scores",
    "high-value-candidates",
    "high_value_candidates",
    "content-briefs",
    "content_briefs",
    "content-outlines",
    "content_outlines",
    "content-drafts",
    "content_drafts",
    "content-quality-review",
    "content_quality_review",
    "platform-packages",
    "platform_packages",
    "content-workbench",
    "content_workbench",
    "phase2-daily-pipeline",
    "phase2_daily_pipeline",
)


@dataclass(frozen=True)
class RuntimeEvidence:
    """One artifact that appears to mention a source."""

    source_id: str
    artifact_path: str
    artifact_kind: str
    matched_by: str
    line: int | None
    snippet: str


@dataclass(frozen=True)
class SourceRuntimeRecord:
    """Runtime status for one registry source."""

    source_id: str
    label: str
    tier: str
    category: str
    enabled: bool
    expected_frequency: str
    fetch_method: str
    runtime_status: str
    runtime_reason: str
    evidence_count: int
    artifact_count: int
    error_hint_count: int
    evidence: tuple[RuntimeEvidence, ...]


@dataclass(frozen=True)
class SourceRuntimeHealthReport:
    """Registry-aligned runtime health report."""

    schema_version: str
    generated_at: str
    run_date: str
    source_count: int
    enabled_count: int
    observed_count: int
    missing_expected_count: int
    status_distribution: dict[str, int]
    artifact_count: int
    manifest_count: int
    artifact_roots: tuple[str, ...]
    records: tuple[SourceRuntimeRecord, ...]
    unmatched_artifacts: tuple[str, ...]
    unmatched_manifest_sources: tuple[str, ...]


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _normalize_date(value: str | None) -> str:
    if not value:
        return ""
    return value.replace("-", "")[:8]


def _artifact_kind(path: Path) -> str:
    name = path.name.lower()
    parts = [part.lower() for part in path.parts]
    if "runtime-manifest" in name or "runtime_manifest" in name:
        return "runtime_manifest"
    if "source_packets" in parts:
        return "source_packet"
    if "manifest" in name:
        return "manifest"
    if "source-health" in name or "source_runtime" in name or "source-runtime" in name:
        return "generated_health"
    if "10_logs" in parts:
        return "log"
    return "artifact"


def _is_generated_phase1_report(path: Path) -> bool:
    name = path.name.lower()
    return any(marker in name for marker in GENERATED_REPORT_NAME_MARKERS)


def _safe_read_text(path: Path, max_bytes: int = MAX_TEXT_BYTES) -> str:
    try:
        raw = path.read_bytes()
    except OSError:
        return ""

    if len(raw) > max_bytes:
        raw = raw[:max_bytes]

    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace")


def _iter_runtime_manifests(paths: ProjectPaths, run_date: str | None = None) -> tuple[Path, ...]:
    """Return structured runtime manifest JSON files for a selected date."""

    date_id = _normalize_date(run_date)
    manifests: set[Path] = set()

    for pattern in RUNTIME_MANIFEST_GLOBS:
        for path in paths.market_content_root.glob(pattern):
            if not path.is_file():
                continue
            if "source-runtime-health" in path.name or "source_runtime_health" in path.name:
                continue
            if "path-hardcode-audit" in path.name or "path_hardcode_audit" in path.name:
                continue
            if date_id and not path.name.startswith(date_id) and not path.name.startswith("latest_"):
                # Dated manifests should stay focused on the selected day; latest
                # manifests are allowed because their internal run_date is checked
                # after parsing.
                continue
            manifests.add(path)

    return tuple(sorted(manifests))


def _iter_runtime_artifacts(paths: ProjectPaths, run_date: str | None = None) -> tuple[Path, ...]:
    artifacts: set[Path] = set()

    for pattern in RUNTIME_ARTIFACT_GLOBS:
        for path in paths.market_content_root.glob(pattern):
            if not path.is_file():
                continue
            if _is_generated_phase1_report(path):
                continue
            kind = _artifact_kind(path)
            if kind in {"generated_health", "runtime_manifest"}:
                continue
            if run_date and run_date not in path.name and run_date not in path.as_posix():
                # Source packet directories often include run date; skip unrelated
                # artifacts so daily reports remain focused.
                continue
            artifacts.add(path)

    return tuple(sorted(artifacts))


def _line_for_index(text: str, index: int) -> tuple[int, str]:
    line_number = text.count("\n", 0, index) + 1
    line_start = text.rfind("\n", 0, index) + 1
    line_end = text.find("\n", index)
    if line_end == -1:
        line_end = len(text)
    line_text = text[line_start:line_end].strip()
    if len(line_text) > 220:
        line_text = line_text[:217] + "..."
    return line_number, line_text


def _source_patterns(source: SourceConfig) -> tuple[tuple[str, re.Pattern[str]], ...]:
    label_token = re.escape(source.label)
    source_id_token = re.escape(source.source_id)
    patterns: list[tuple[str, re.Pattern[str]]] = [
        ("source_id", re.compile(rf"(?<![a-z0-9_]){source_id_token}(?![a-z0-9_])", re.IGNORECASE)),
    ]
    if len(source.label) >= 4:
        patterns.append(("label", re.compile(label_token, re.IGNORECASE)))
    return tuple(patterns)


def _count_error_hints(text: str) -> int:
    count = 0
    for pattern in ERROR_PATTERNS:
        count += len(pattern.findall(text))
    return count


def _manifest_matches_date(manifest: RuntimeManifest, path: Path, run_date: str) -> bool:
    date_id = _normalize_date(run_date)
    manifest_date_id = _normalize_date(manifest.run_date)
    if manifest_date_id:
        return manifest_date_id == date_id
    return date_id in path.name or date_id in path.as_posix()


def _manifest_source_error_hint(status: str, error_type: str | None, error_message: str | None) -> int:
    if status.upper() == "FAILED":
        return 1
    if error_type or error_message:
        return 1
    return 0


def collect_manifest_evidence(
    registry: SourceRegistry,
    paths: ProjectPaths,
    run_date: str,
) -> tuple[dict[str, list[RuntimeEvidence]], dict[str, int], tuple[str, ...], int]:
    """Collect structured evidence from P0-008 runtime manifests.

    Runtime manifests are the preferred runtime signal because they directly
    report source status and item counts. Legacy text scan remains a fallback
    for artifacts that predate the contract.
    """

    registry_ids = {source.source_id for source in registry.sources}
    evidence_by_source: dict[str, list[RuntimeEvidence]] = {source.source_id: [] for source in registry.sources}
    error_hints_by_source: dict[str, int] = {source.source_id: 0 for source in registry.sources}
    unmatched_sources: list[str] = []
    manifest_count = 0

    for manifest_path in _iter_runtime_manifests(paths, run_date=run_date):
        try:
            manifest = load_runtime_manifest(manifest_path)
        except (OSError, json.JSONDecodeError, ValueError):
            continue

        if not _manifest_matches_date(manifest, manifest_path, run_date):
            continue

        manifest_count += 1
        artifact_rel = _relative(manifest_path, paths.repo_root)

        for source_run in manifest.sources:
            source_id = source_run.source_id
            snippet = (
                f"manifest={manifest.pipeline_name}; status={source_run.status}; "
                f"items_found={source_run.items_found}; items_written={source_run.items_written}"
            )
            if source_run.error_type or source_run.error_message:
                snippet += f"; error={source_run.error_type or ''} {source_run.error_message or ''}".strip()

            if source_id in registry_ids:
                evidence_by_source[source_id].append(
                    RuntimeEvidence(
                        source_id=source_id,
                        artifact_path=artifact_rel,
                        artifact_kind="runtime_manifest",
                        matched_by="runtime_manifest.source_id",
                        line=None,
                        snippet=snippet,
                    )
                )
                error_hints_by_source[source_id] += _manifest_source_error_hint(
                    source_run.status,
                    source_run.error_type,
                    source_run.error_message,
                )
            else:
                unmatched_sources.append(f"{source_id} @ {artifact_rel}")

    return evidence_by_source, error_hints_by_source, tuple(unmatched_sources), manifest_count


def collect_text_runtime_evidence(
    registry: SourceRegistry,
    paths: ProjectPaths,
    run_date: str | None = None,
) -> tuple[dict[str, list[RuntimeEvidence]], dict[str, int], tuple[str, ...]]:
    """Collect best-effort runtime evidence from legacy text artifacts."""

    evidence_by_source: dict[str, list[RuntimeEvidence]] = {source.source_id: [] for source in registry.sources}
    error_hints_by_source: dict[str, int] = {source.source_id: 0 for source in registry.sources}
    unmatched_artifacts: list[str] = []

    artifacts = _iter_runtime_artifacts(paths, run_date=run_date)

    for artifact in artifacts:
        text = _safe_read_text(artifact)
        if not text:
            unmatched_artifacts.append(_relative(artifact, paths.repo_root))
            continue

        artifact_matched = False
        artifact_errors = _count_error_hints(text)
        artifact_rel = _relative(artifact, paths.repo_root)

        for source in registry.sources:
            source_matches: list[RuntimeEvidence] = []
            for matched_by, pattern in _source_patterns(source):
                for match in pattern.finditer(text):
                    line, snippet = _line_for_index(text, match.start())
                    source_matches.append(
                        RuntimeEvidence(
                            source_id=source.source_id,
                            artifact_path=artifact_rel,
                            artifact_kind=_artifact_kind(artifact),
                            matched_by=matched_by,
                            line=line,
                            snippet=snippet,
                        )
                    )
                    if len(source_matches) >= 10:
                        break
                if len(source_matches) >= 10:
                    break

            if source_matches:
                artifact_matched = True
                evidence_by_source[source.source_id].extend(source_matches)
                if artifact_errors:
                    error_hints_by_source[source.source_id] += artifact_errors

        if not artifact_matched:
            unmatched_artifacts.append(artifact_rel)

    return evidence_by_source, error_hints_by_source, tuple(unmatched_artifacts)


def collect_runtime_evidence(
    registry: SourceRegistry,
    paths: ProjectPaths,
    run_date: str,
) -> tuple[dict[str, list[RuntimeEvidence]], dict[str, int], tuple[str, ...], tuple[str, ...], int]:
    """Collect structured manifest evidence first, then legacy text evidence."""

    manifest_evidence, manifest_errors, unmatched_manifest_sources, manifest_count = collect_manifest_evidence(
        registry=registry,
        paths=paths,
        run_date=run_date,
    )
    text_evidence, text_errors, unmatched_artifacts = collect_text_runtime_evidence(
        registry=registry,
        paths=paths,
        run_date=run_date,
    )

    evidence_by_source: dict[str, list[RuntimeEvidence]] = {source.source_id: [] for source in registry.sources}
    error_hints_by_source: dict[str, int] = {source.source_id: 0 for source in registry.sources}

    for source in registry.sources:
        source_id = source.source_id
        evidence_by_source[source_id].extend(manifest_evidence.get(source_id, []))
        evidence_by_source[source_id].extend(text_evidence.get(source_id, []))
        error_hints_by_source[source_id] = manifest_errors.get(source_id, 0) + text_errors.get(source_id, 0)

    return (
        evidence_by_source,
        error_hints_by_source,
        unmatched_artifacts,
        unmatched_manifest_sources,
        manifest_count,
    )


def _expected_today(source: SourceConfig) -> bool:
    if not source.enabled:
        return False
    return source.expected_frequency in {"hourly", "daily"}


def _has_manifest_evidence(evidence: Iterable[RuntimeEvidence]) -> bool:
    return any(item.artifact_kind == "runtime_manifest" for item in evidence)


def _runtime_status(source: SourceConfig, evidence: tuple[RuntimeEvidence, ...], error_hint_count: int) -> tuple[str, str]:
    evidence_count = len(evidence)
    if not source.enabled:
        return "DISABLED", "source disabled in registry"
    if evidence_count > 0 and error_hint_count > 0:
        if _has_manifest_evidence(evidence):
            return "OBSERVED_WITH_ERROR_HINTS", "structured runtime manifest reports source and includes failed/error status"
        return "OBSERVED_WITH_ERROR_HINTS", "runtime artifacts mention source and contain error/failure hints"
    if evidence_count > 0:
        if _has_manifest_evidence(evidence):
            return "OBSERVED", "structured runtime manifest reports source"
        return "OBSERVED", "runtime artifacts mention source"
    if _expected_today(source):
        return "MISSING_EXPECTED", "enabled daily/hourly source has no runtime evidence for selected date"
    return "NOT_OBSERVED", "no runtime evidence found; source frequency is not daily/hourly"


def build_source_runtime_health_report(
    registry: SourceRegistry,
    paths: ProjectPaths,
    run_date: str,
) -> SourceRuntimeHealthReport:
    (
        evidence_by_source,
        error_hints_by_source,
        unmatched_artifacts,
        unmatched_manifest_sources,
        manifest_count,
    ) = collect_runtime_evidence(
        registry=registry,
        paths=paths,
        run_date=run_date,
    )

    records: list[SourceRuntimeRecord] = []
    for source in registry.sources:
        evidence = tuple(evidence_by_source.get(source.source_id, ()))
        artifact_count = len({item.artifact_path for item in evidence})
        error_hint_count = error_hints_by_source.get(source.source_id, 0)
        status, reason = _runtime_status(source, evidence, error_hint_count)
        records.append(
            SourceRuntimeRecord(
                source_id=source.source_id,
                label=source.label,
                tier=source.tier,
                category=source.category,
                enabled=source.enabled,
                expected_frequency=source.expected_frequency,
                fetch_method=source.fetch_method,
                runtime_status=status,
                runtime_reason=reason,
                evidence_count=len(evidence),
                artifact_count=artifact_count,
                error_hint_count=error_hint_count,
                evidence=evidence[:20],
            )
        )

    status_counts = Counter(record.runtime_status for record in records)
    artifact_paths = {
        evidence.artifact_path
        for record in records
        for evidence in record.evidence
    }

    return SourceRuntimeHealthReport(
        schema_version=SCHEMA_VERSION,
        generated_at=datetime.now(timezone.utc).isoformat(),
        run_date=run_date,
        source_count=len(registry.sources),
        enabled_count=sum(1 for source in registry.sources if source.enabled),
        observed_count=sum(1 for record in records if record.evidence_count > 0),
        missing_expected_count=status_counts.get("MISSING_EXPECTED", 0),
        status_distribution=dict(sorted(status_counts.items())),
        artifact_count=len(artifact_paths),
        manifest_count=manifest_count,
        artifact_roots=tuple(RUNTIME_MANIFEST_GLOBS + RUNTIME_ARTIFACT_GLOBS),
        records=tuple(records),
        unmatched_artifacts=unmatched_artifacts[:200],
        unmatched_manifest_sources=unmatched_manifest_sources[:200],
    )


def report_to_dict(report: SourceRuntimeHealthReport) -> dict:
    return asdict(report)


def write_json_report(report: SourceRuntimeHealthReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2), encoding="utf-8")


def _escape_table_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown_report(report: SourceRuntimeHealthReport, max_records: int = 200) -> str:
    lines: list[str] = []
    lines.append("# Source Runtime Health v1 报告")
    lines.append("")
    lines.append(
        "> P0-011A：优先读取 P0-008 runtime manifest；legacy manifest/source packet/log 文本扫描作为 fallback。"
    )
    lines.append("")
    lines.append("## 摘要")
    lines.append("")
    lines.append(f"- 生成时间：`{report.generated_at}`")
    lines.append(f"- 运行日期：`{report.run_date}`")
    lines.append(f"- Registry sources：`{report.source_count}`")
    lines.append(f"- Enabled sources：`{report.enabled_count}`")
    lines.append(f"- Observed sources：`{report.observed_count}`")
    lines.append(f"- Missing expected sources：`{report.missing_expected_count}`")
    lines.append(f"- Structured runtime manifests：`{report.manifest_count}`")
    lines.append(f"- Matched artifact count：`{report.artifact_count}`")
    lines.append("")

    lines.append("## Runtime Status 分布")
    lines.append("")
    for status, count in report.status_distribution.items():
        lines.append(f"- `{status}`：{count}")
    lines.append("")

    lines.append("## Source 明细")
    lines.append("")
    lines.append("| Source | Tier | Category | Frequency | Status | Evidence | Artifacts | Error hints | Reason |")
    lines.append("|---|---:|---|---|---|---:|---:|---:|---|")
    for record in report.records[:max_records]:
        lines.append(
            "| "
            + " | ".join(
                [
                    _escape_table_cell(record.source_id),
                    _escape_table_cell(record.tier),
                    _escape_table_cell(record.category),
                    _escape_table_cell(record.expected_frequency),
                    _escape_table_cell(record.runtime_status),
                    _escape_table_cell(record.evidence_count),
                    _escape_table_cell(record.artifact_count),
                    _escape_table_cell(record.error_hint_count),
                    _escape_table_cell(record.runtime_reason),
                ]
            )
            + " |"
        )
    if len(report.records) > max_records:
        lines.append("")
        lines.append(f"> 仅展示前 {max_records} 个 source；JSON 报告保留全部 records。")
    lines.append("")

    lines.append("## Evidence 示例")
    lines.append("")
    evidence_rows = [
        evidence
        for record in report.records
        for evidence in record.evidence[:3]
    ][:max_records]
    if not evidence_rows:
        lines.append("暂无匹配 evidence。")
    else:
        lines.append("| Source | Artifact | Kind | Matched by | Line | Snippet |")
        lines.append("|---|---|---|---|---:|---|")
        for evidence in evidence_rows:
            lines.append(
                "| "
                + " | ".join(
                    [
                        _escape_table_cell(evidence.source_id),
                        _escape_table_cell(evidence.artifact_path),
                        _escape_table_cell(evidence.artifact_kind),
                        _escape_table_cell(evidence.matched_by),
                        _escape_table_cell(evidence.line or ""),
                        _escape_table_cell(evidence.snippet),
                    ]
                )
                + " |"
            )
    lines.append("")

    lines.append("## Runtime manifest 中未匹配到 registry 的 source")
    lines.append("")
    if report.unmatched_manifest_sources:
        for source in report.unmatched_manifest_sources[:50]:
            lines.append(f"- `{source}`")
        if len(report.unmatched_manifest_sources) > 50:
            lines.append(f"- ... 另有 {len(report.unmatched_manifest_sources) - 50} 个未展示")
    else:
        lines.append("无。")
    lines.append("")

    lines.append("## 未匹配 artifact")
    lines.append("")
    if report.unmatched_artifacts:
        for artifact in report.unmatched_artifacts[:50]:
            lines.append(f"- `{artifact}`")
        if len(report.unmatched_artifacts) > 50:
            lines.append(f"- ... 另有 {len(report.unmatched_artifacts) - 50} 个未展示")
    else:
        lines.append("无。")
    lines.append("")

    lines.append("## 下一步")
    lines.append("")
    lines.append("- P0-011B 可继续观察 wrapper 入口，或再决定是否把 manifest writer 嵌入 official lane 主脚本。")
    lines.append("- 暂不做 retry/fallback，不新增数据库，不改变现有抓取输出。")
    lines.append("")
    return "\n".join(lines)


def write_markdown_report(report: SourceRuntimeHealthReport, path: Path, max_records: int = 200) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown_report(report, max_records=max_records), encoding="utf-8")


def default_runtime_report_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__source-runtime-health.json",
        "dated_md": paths.logs_root / f"{run_date}__source-runtime-health.md",
        "latest_json": paths.logs_root / "latest_source_runtime_health.json",
        "latest_md": paths.logs_root / "latest_source_runtime_health.md",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__source-runtime-health-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_source_runtime_health_board.md",
    }


def write_default_runtime_reports(
    report: SourceRuntimeHealthReport,
    paths: ProjectPaths,
    run_date: str,
    max_records: int = 200,
) -> dict[str, Path]:
    output_paths = default_runtime_report_paths(paths, run_date)
    write_json_report(report, output_paths["dated_json"])
    write_json_report(report, output_paths["latest_json"])
    write_markdown_report(report, output_paths["dated_md"], max_records=max_records)
    write_markdown_report(report, output_paths["latest_md"], max_records=max_records)
    write_markdown_report(report, output_paths["frontstage_dated_md"], max_records=max_records)
    write_markdown_report(report, output_paths["frontstage_latest_md"], max_records=max_records)
    return output_paths

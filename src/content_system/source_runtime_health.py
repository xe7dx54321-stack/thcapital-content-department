"""Runtime source health adapter.

P0-007 connects the Source Registry with existing generated runtime artifacts
(manifests, source packets, and logs) without changing fetchers, retry behavior,
fallback behavior, scheduling, or persistence.

The adapter is deliberately best-effort: existing manifests are not yet a stable
machine contract, so this module records evidence found in current artifacts and
marks registry sources as observed or missing.
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
from content_system.sources import SourceConfig, SourceRegistry

SCHEMA_VERSION = "v1"
MAX_TEXT_BYTES = 800_000

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
    artifact_roots: tuple[str, ...]
    records: tuple[SourceRuntimeRecord, ...]
    unmatched_artifacts: tuple[str, ...]


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _artifact_kind(path: Path) -> str:
    name = path.name.lower()
    parts = [part.lower() for part in path.parts]

    if "source_packets" in parts:
        return "source_packet"
    if "manifest" in name:
        return "manifest"
    if "source-health" in name or "source_runtime" in name or "source-runtime" in name:
        return "generated_health"
    if "10_logs" in parts:
        return "log"
    return "artifact"


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


def _iter_runtime_artifacts(paths: ProjectPaths, run_date: str | None = None) -> tuple[Path, ...]:
    artifacts: set[Path] = set()

    for pattern in RUNTIME_ARTIFACT_GLOBS:
        for path in paths.market_content_root.glob(pattern):
            if not path.is_file():
                continue
            if _artifact_kind(path) == "generated_health":
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
        (
            "source_id",
            re.compile(rf"(?<![A-Za-z0-9_]){source_id_token}(?![A-Za-z0-9_])", re.IGNORECASE),
        )
    ]

    # Labels are useful for official sources whose existing manifests predate
    # source_id. Avoid overly short labels to limit false positives.
    if len(source.label.strip()) >= 4:
        patterns.append(("label", re.compile(label_token, re.IGNORECASE)))

    return tuple(patterns)


def _count_error_hints(text: str) -> int:
    count = 0
    for pattern in ERROR_PATTERNS:
        count += len(pattern.findall(text))
    return count


def collect_runtime_evidence(
    registry: SourceRegistry,
    paths: ProjectPaths,
    run_date: str | None = None,
) -> tuple[dict[str, list[RuntimeEvidence]], dict[str, int], tuple[str, ...]]:
    """Collect best-effort runtime evidence from existing artifacts."""

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


def _expected_today(source: SourceConfig) -> bool:
    if not source.enabled:
        return False
    return source.expected_frequency in {"hourly", "daily"}


def _runtime_status(source: SourceConfig, evidence_count: int, error_hint_count: int) -> tuple[str, str]:
    if not source.enabled:
        return "DISABLED", "source disabled in registry"

    if evidence_count > 0 and error_hint_count > 0:
        return "OBSERVED_WITH_ERROR_HINTS", "runtime artifacts mention source and contain error/failure hints"

    if evidence_count > 0:
        return "OBSERVED", "runtime artifacts mention source"

    if _expected_today(source):
        return "MISSING_EXPECTED", "enabled daily/hourly source has no runtime evidence for selected date"

    return "NOT_OBSERVED", "no runtime evidence found; source frequency is not daily/hourly"


def build_source_runtime_health_report(
    registry: SourceRegistry,
    paths: ProjectPaths,
    run_date: str,
) -> SourceRuntimeHealthReport:
    evidence_by_source, error_hints_by_source, unmatched_artifacts = collect_runtime_evidence(
        registry=registry,
        paths=paths,
        run_date=run_date,
    )

    records: list[SourceRuntimeRecord] = []

    for source in registry.sources:
        evidence = tuple(evidence_by_source.get(source.source_id, ()))
        artifact_count = len({item.artifact_path for item in evidence})
        error_hint_count = error_hints_by_source.get(source.source_id, 0)
        status, reason = _runtime_status(source, len(evidence), error_hint_count)

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
        artifact_roots=tuple(RUNTIME_ARTIFACT_GLOBS),
        records=tuple(records),
        unmatched_artifacts=unmatched_artifacts[:200],
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
    lines.append("> P0-007：把 Source Registry 与现有运行产物/manifest 做 best-effort 对齐；不抓取、不 retry、不改 fetcher。")
    lines.append("")
    lines.append("## 摘要")
    lines.append("")
    lines.append(f"- 生成时间：`{report.generated_at}`")
    lines.append(f"- 运行日期：`{report.run_date}`")
    lines.append(f"- Registry sources：`{report.source_count}`")
    lines.append(f"- Enabled sources：`{report.enabled_count}`")
    lines.append(f"- Observed sources：`{report.observed_count}`")
    lines.append(f"- Missing expected sources：`{report.missing_expected_count}`")
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
    lines.append("- P0-008 可开始把活跃抓取脚本写出的 manifest 规范化为稳定 runtime contract。")
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

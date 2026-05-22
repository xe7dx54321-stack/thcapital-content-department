"""Runtime manifest writer helpers.

P0-009 adds the first writer layer for the runtime manifest contract introduced
in P0-008.  It does not execute fetchers and it does not change existing output
formats.  It only converts existing source packet JSON artifacts into a stable
runtime manifest JSON document.
"""

from __future__ import annotations

import json
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from content_system.paths import get_project_paths
from content_system.runtime_manifest import (
    RuntimeManifest,
    SourceRunRecord,
    manifest_to_dict,
    validate_runtime_manifest,
)
from content_system.sources import SourceRegistry, load_source_registry

SOURCE_ID_ALIASES: dict[str, str] = {
    # Official lane ids used by existing scripts.
    "web__openai_news": "openai_blog",
    "web__anthropic_news": "anthropic_news",
    "web__google_blog_ai": "google_ai_blog",
    "web__deepmind_blog": "google_deepmind_blog",
    "web__nvidia_blog": "nvidia_technical_blog",
    "web__xai_news": "xai_news",
    "x__openai": "openai_blog",
    "x__openaidevs": "openai_blog",
    "x__anthropic_ai": "anthropic_news",
    # Common topic-capture aliases. Unknown ids are preserved and validated later.
    "github_trending": "github_trending_ai",
    "hn_ai": "hacker_news_ai",
    "hacker_news": "hacker_news_ai",
    "hf_papers": "huggingface_papers",
    "huggingface": "huggingface_papers",
    "arxiv": "arxiv_ai",
    "arxiv_ai_papers": "arxiv_ai",
}


def discover_latest_source_packet_dir(market_content_root: Path) -> Path | None:
    """Return the latest source packet directory if one exists."""

    root = market_content_root / "02_topic_radar" / "source_packets"
    if not root.exists():
        return None

    candidates = [path for path in root.iterdir() if path.is_dir()]
    if not candidates:
        return None

    return sorted(candidates, key=lambda item: item.name)[-1]


def build_runtime_manifest_from_packet_dir(
    source_packets_dir: Path,
    *,
    registry: SourceRegistry | None = None,
    repo_root: Path | None = None,
    run_date: str | None = None,
    pipeline_name: str = "source_packets_adapter",
    script_name: str = "write_runtime_manifest_from_packets.py",
    notes: str = "Generated from existing source packet JSON artifacts.",
) -> RuntimeManifest:
    """Build a RuntimeManifest from JSON source packet artifacts."""

    if repo_root is None:
        repo_root = get_project_paths().repo_root

    if run_date is None:
        run_date = _infer_run_date(source_packets_dir)

    packet_paths = sorted(source_packets_dir.rglob("*.json")) if source_packets_dir.exists() else []
    records = collect_source_run_records(packet_paths, repo_root=repo_root)
    status = _manifest_status(records)

    return RuntimeManifest(
        schema_version="v1",
        generated_at=datetime.now(timezone.utc).isoformat(),
        run_id=f"{run_date}__{pipeline_name}",
        run_date=run_date,
        pipeline_name=pipeline_name,
        script_name=script_name,
        status=status,
        sources=tuple(records),
        notes=notes,
    )


def collect_source_run_records(packet_paths: Iterable[Path], *, repo_root: Path) -> list[SourceRunRecord]:
    """Collect SourceRunRecord values from one or more JSON packet files."""

    records_by_source: dict[str, SourceRunRecord] = {}

    for packet_path in packet_paths:
        for raw_packet in _load_packet_records(packet_path):
            record = _packet_to_record(raw_packet, packet_path=packet_path, repo_root=repo_root)
            if record is None:
                continue
            previous = records_by_source.get(record.source_id)
            if previous is None:
                records_by_source[record.source_id] = record
            else:
                records_by_source[record.source_id] = _merge_records(previous, record)

    return sorted(records_by_source.values(), key=lambda item: item.source_id)


def write_runtime_manifest(manifest: RuntimeManifest, output_path: Path) -> Path:
    """Write a runtime manifest JSON file and return the written path."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(manifest_to_dict(manifest), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path


def default_runtime_manifest_output(run_date: str | None = None, repo_root: Path | None = None) -> Path:
    """Return the default dated runtime manifest output path."""

    paths = get_project_paths(repo_root)
    if run_date is None:
        run_date = datetime.now().strftime("%Y%m%d")
    safe_date = run_date.replace("-", "")
    return paths.logs_root / f"{safe_date}__runtime-manifest.json"


def default_latest_runtime_manifest_output(repo_root: Path | None = None) -> Path:
    """Return the default latest runtime manifest output path."""

    return get_project_paths(repo_root).logs_root / "latest_runtime_manifest.json"


def validate_and_summarize(manifest: RuntimeManifest, registry: SourceRegistry | None = None) -> tuple[int, int]:
    """Return (error_count, warning_count) for a manifest."""

    issues = validate_runtime_manifest(manifest, registry=registry)
    errors = sum(1 for issue in issues if issue.severity == "ERROR")
    warnings = sum(1 for issue in issues if issue.severity == "WARN")
    return errors, warnings


def load_default_registry(repo_root: Path | None = None) -> SourceRegistry:
    """Load the repository source registry."""

    return load_source_registry(repo_root=repo_root)


def _load_packet_records(packet_path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(packet_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return []

    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        # Some artifacts may wrap packets under a named key.
        for key in ("packets", "sources", "source_packets"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [payload]
    return []


def _packet_to_record(packet: dict[str, Any], *, packet_path: Path, repo_root: Path) -> SourceRunRecord | None:
    raw_source_id = str(packet.get("source_id") or packet.get("_source") or packet.get("id") or "").strip()
    if not raw_source_id:
        return None

    source_id = SOURCE_ID_ALIASES.get(raw_source_id, raw_source_id)
    entry_count = _entry_count(packet)
    error_message = _error_message(packet)
    status = "FAILED" if error_message else "SUCCESS"
    artifact_path = _repo_relative(packet_path, repo_root)

    notes_parts = []
    label = packet.get("label") or packet.get("source_label")
    if label:
        notes_parts.append(f"label={label}")
    if source_id != raw_source_id:
        notes_parts.append(f"alias={raw_source_id}->{source_id}")

    return SourceRunRecord(
        source_id=source_id,
        status=status,
        items_found=entry_count,
        items_written=entry_count,
        started_at=None,
        finished_at=str(packet.get("captured_at") or packet.get("generated_at") or "") or None,
        error_type="packet_error" if error_message else None,
        error_message=error_message,
        artifact_paths=(artifact_path,),
        notes="; ".join(notes_parts),
    )


def _entry_count(packet: dict[str, Any]) -> int:
    for key in ("entry_count", "items_found", "items_written", "count"):
        value = packet.get(key)
        if isinstance(value, int):
            return max(value, 0)
        if isinstance(value, str) and value.isdigit():
            return int(value)

    for key in ("entries", "items", "records", "results"):
        value = packet.get(key)
        if isinstance(value, list):
            return len(value)

    return 0


def _error_message(packet: dict[str, Any]) -> str | None:
    for key in ("error_message", "error", "exception"):
        value = packet.get(key)
        if value:
            return str(value)

    status = str(packet.get("status") or "").lower()
    if status in {"failed", "error", "timeout"}:
        return f"packet status is {status}"
    return None


def _merge_records(left: SourceRunRecord, right: SourceRunRecord) -> SourceRunRecord:
    status = _merge_status(left.status, right.status)
    artifact_paths = tuple(dict.fromkeys([*left.artifact_paths, *right.artifact_paths]))
    error_message = left.error_message or right.error_message
    error_type = left.error_type or right.error_type
    notes = "; ".join(part for part in (left.notes, right.notes) if part)
    return replace(
        left,
        status=status,
        items_found=left.items_found + right.items_found,
        items_written=left.items_written + right.items_written,
        error_type=error_type,
        error_message=error_message,
        artifact_paths=artifact_paths,
        notes=notes,
    )


def _merge_status(left: str, right: str) -> str:
    statuses = {left, right}
    if "FAILED" in statuses and "SUCCESS" in statuses:
        return "PARTIAL"
    if "FAILED" in statuses:
        return "FAILED"
    if "PARTIAL" in statuses:
        return "PARTIAL"
    if "SUCCESS" in statuses:
        return "SUCCESS"
    return "UNKNOWN"


def _manifest_status(records: list[SourceRunRecord]) -> str:
    if not records:
        return "UNKNOWN"
    statuses = {record.status for record in records}
    if statuses == {"SUCCESS"}:
        return "SUCCESS"
    if "SUCCESS" in statuses and ("FAILED" in statuses or "PARTIAL" in statuses):
        return "PARTIAL"
    if "FAILED" in statuses:
        return "FAILED"
    return "UNKNOWN"


def _infer_run_date(source_packets_dir: Path) -> str:
    # Common folder names: 20260522__source_packets, 20260522__official_lane.
    token = source_packets_dir.name.split("__", 1)[0]
    if len(token) == 8 and token.isdigit():
        return f"{token[:4]}-{token[4:6]}-{token[6:]}"
    return datetime.now().strftime("%Y-%m-%d")


def _repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return path.name

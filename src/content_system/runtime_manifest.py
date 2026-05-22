"""Runtime manifest contract helpers.

P0-008 introduces a stable JSON contract for ingestion/runtime scripts to report
which registry sources actually ran, how many items they produced, and whether
any error hints were observed. This module intentionally does not execute any
fetcher or scheduler; it only validates and summarizes manifest documents.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    from content_system.paths import get_project_paths
    from content_system.sources import SourceRegistry, load_source_registry
except ModuleNotFoundError:  # pragma: no cover - useful when imported before sys.path setup
    get_project_paths = None  # type: ignore[assignment]
    load_source_registry = None  # type: ignore[assignment]
    SourceRegistry = Any  # type: ignore[misc,assignment]

SCHEMA_VERSION = "v1"
VALID_RUN_STATUS = {"SUCCESS", "PARTIAL", "FAILED", "SKIPPED", "UNKNOWN"}
VALID_MANIFEST_STATUS = {"SUCCESS", "PARTIAL", "FAILED", "UNKNOWN"}
SOURCE_ID_PATTERN = re.compile(r"^[a-z0-9_]+$")
LOCAL_PATH_MARKERS = ("/Users/", "file://", "D:/", "C:/", "\\Users\\")


@dataclass(frozen=True)
class ValidationIssue:
    severity: str  # ERROR or WARN
    field: str
    message: str
    source_id: str | None = None


@dataclass(frozen=True)
class SourceRunRecord:
    source_id: str
    status: str
    items_found: int
    items_written: int
    started_at: str | None = None
    finished_at: str | None = None
    error_type: str | None = None
    error_message: str | None = None
    artifact_paths: tuple[str, ...] = ()
    notes: str = ""


@dataclass(frozen=True)
class RuntimeManifest:
    schema_version: str
    generated_at: str
    run_id: str
    run_date: str
    pipeline_name: str
    script_name: str
    status: str
    sources: tuple[SourceRunRecord, ...]
    notes: str = ""

    @property
    def source_count(self) -> int:
        return len(self.sources)

    @property
    def total_items_found(self) -> int:
        return sum(item.items_found for item in self.sources)

    @property
    def total_items_written(self) -> int:
        return sum(item.items_written for item in self.sources)

    def status_distribution(self) -> dict[str, int]:
        distribution = {status: 0 for status in sorted(VALID_RUN_STATUS)}
        for source in self.sources:
            distribution[source.status] = distribution.get(source.status, 0) + 1
        return distribution


def default_manifest_path(repo_root: Path | None = None) -> Path:
    """Return the example manifest path used by P0-008 validation."""
    if repo_root is None:
        if get_project_paths is not None:
            repo_root = get_project_paths().repo_root
        else:
            repo_root = Path(__file__).resolve().parents[2]
    return repo_root / "config" / "runtime_manifest_example.json"


def load_runtime_manifest(path: Path) -> RuntimeManifest:
    """Load a runtime manifest JSON document."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    return parse_runtime_manifest(payload)


def parse_runtime_manifest(payload: dict[str, Any]) -> RuntimeManifest:
    """Parse a dict into RuntimeManifest without performing full validation."""
    sources_payload = payload.get("sources", [])
    sources: list[SourceRunRecord] = []

    if isinstance(sources_payload, list):
        for raw in sources_payload:
            if not isinstance(raw, dict):
                continue
            sources.append(
                SourceRunRecord(
                    source_id=str(raw.get("source_id", "")),
                    status=str(raw.get("status", "UNKNOWN")),
                    items_found=_safe_int(raw.get("items_found", 0)),
                    items_written=_safe_int(raw.get("items_written", 0)),
                    started_at=_optional_str(raw.get("started_at")),
                    finished_at=_optional_str(raw.get("finished_at")),
                    error_type=_optional_str(raw.get("error_type")),
                    error_message=_optional_str(raw.get("error_message")),
                    artifact_paths=tuple(str(item) for item in raw.get("artifact_paths", []) if item is not None),
                    notes=str(raw.get("notes", "")),
                )
            )

    return RuntimeManifest(
        schema_version=str(payload.get("schema_version", "")),
        generated_at=str(payload.get("generated_at", "")),
        run_id=str(payload.get("run_id", "")),
        run_date=str(payload.get("run_date", "")),
        pipeline_name=str(payload.get("pipeline_name", "")),
        script_name=str(payload.get("script_name", "")),
        status=str(payload.get("status", "UNKNOWN")),
        sources=tuple(sources),
        notes=str(payload.get("notes", "")),
    )


def validate_runtime_manifest(
    manifest: RuntimeManifest,
    registry: SourceRegistry | None = None,
) -> tuple[ValidationIssue, ...]:
    """Validate a runtime manifest against the P0-008 contract and registry."""
    issues: list[ValidationIssue] = []

    if manifest.schema_version != SCHEMA_VERSION:
        issues.append(ValidationIssue("ERROR", "schema_version", f"expected {SCHEMA_VERSION}, got {manifest.schema_version!r}"))

    for field_name in ("generated_at", "run_id", "run_date", "pipeline_name", "script_name"):
        if not getattr(manifest, field_name):
            issues.append(ValidationIssue("ERROR", field_name, "field is required"))

    if manifest.status not in VALID_MANIFEST_STATUS:
        issues.append(ValidationIssue("ERROR", "status", f"invalid manifest status: {manifest.status}"))

    if not manifest.sources:
        issues.append(ValidationIssue("WARN", "sources", "manifest contains no source run records"))

    registry_ids: set[str] = set()
    disabled_ids: set[str] = set()
    if registry is not None:
        for source in registry.sources:
            registry_ids.add(source.source_id)
            if not source.enabled:
                disabled_ids.add(source.source_id)

    seen: set[str] = set()
    for source in manifest.sources:
        prefix = f"sources[{source.source_id}]"
        if not source.source_id:
            issues.append(ValidationIssue("ERROR", f"{prefix}.source_id", "source_id is required", source.source_id or None))
        elif not SOURCE_ID_PATTERN.match(source.source_id):
            issues.append(ValidationIssue("ERROR", f"{prefix}.source_id", "source_id must use lowercase letters, numbers, underscores", source.source_id))

        if source.source_id in seen:
            issues.append(ValidationIssue("ERROR", f"{prefix}.source_id", "duplicate source_id in manifest", source.source_id))
        seen.add(source.source_id)

        if registry_ids and source.source_id not in registry_ids:
            issues.append(ValidationIssue("WARN", f"{prefix}.source_id", "source_id not found in config/sources.yaml", source.source_id))
        if source.source_id in disabled_ids:
            issues.append(ValidationIssue("WARN", f"{prefix}.source_id", "source is disabled in registry but appears in runtime manifest", source.source_id))

        if source.status not in VALID_RUN_STATUS:
            issues.append(ValidationIssue("ERROR", f"{prefix}.status", f"invalid status: {source.status}", source.source_id))

        if source.items_found < 0:
            issues.append(ValidationIssue("ERROR", f"{prefix}.items_found", "must be non-negative", source.source_id))
        if source.items_written < 0:
            issues.append(ValidationIssue("ERROR", f"{prefix}.items_written", "must be non-negative", source.source_id))
        if source.items_written > source.items_found:
            issues.append(ValidationIssue("WARN", f"{prefix}.items_written", "items_written is greater than items_found", source.source_id))

        if source.status == "FAILED" and not (source.error_type or source.error_message):
            issues.append(ValidationIssue("WARN", f"{prefix}.error_message", "FAILED source should include error_type or error_message", source.source_id))

        for artifact_path in source.artifact_paths:
            if _contains_local_path(artifact_path):
                issues.append(ValidationIssue("ERROR", f"{prefix}.artifact_paths", "artifact path must be repo-relative, not local absolute", source.source_id))

    return tuple(issues)


def summarize_manifest(manifest: RuntimeManifest, issues: Iterable[ValidationIssue]) -> dict[str, Any]:
    """Return a compact summary used by CLI scripts and reports."""
    issue_list = list(issues)
    return {
        "schema_version": manifest.schema_version,
        "run_id": manifest.run_id,
        "run_date": manifest.run_date,
        "pipeline_name": manifest.pipeline_name,
        "script_name": manifest.script_name,
        "status": manifest.status,
        "source_count": manifest.source_count,
        "total_items_found": manifest.total_items_found,
        "total_items_written": manifest.total_items_written,
        "status_distribution": manifest.status_distribution(),
        "errors": sum(1 for item in issue_list if item.severity == "ERROR"),
        "warnings": sum(1 for item in issue_list if item.severity == "WARN"),
    }


def manifest_to_dict(manifest: RuntimeManifest) -> dict[str, Any]:
    """Serialize a RuntimeManifest to a JSON-ready dict."""
    return {
        "schema_version": manifest.schema_version,
        "generated_at": manifest.generated_at,
        "run_id": manifest.run_id,
        "run_date": manifest.run_date,
        "pipeline_name": manifest.pipeline_name,
        "script_name": manifest.script_name,
        "status": manifest.status,
        "notes": manifest.notes,
        "sources": [
            {
                "source_id": source.source_id,
                "status": source.status,
                "items_found": source.items_found,
                "items_written": source.items_written,
                "started_at": source.started_at,
                "finished_at": source.finished_at,
                "error_type": source.error_type,
                "error_message": source.error_message,
                "artifact_paths": list(source.artifact_paths),
                "notes": source.notes,
            }
            for source in manifest.sources
        ],
    }


def _safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None


def _contains_local_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    return any(marker in normalized for marker in LOCAL_PATH_MARKERS)

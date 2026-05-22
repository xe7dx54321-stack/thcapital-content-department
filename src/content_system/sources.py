"""Source registry loading and validation helpers."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


REQUIRED_SOURCE_FIELDS = (
    "source_id",
    "label",
    "tier",
    "category",
    "language",
    "enabled",
    "fetch_method",
    "primary_url",
    "fallback_methods",
    "expected_frequency",
    "expected_min_items_per_run",
    "owner",
    "notes",
)

ALLOWED_TIERS = {"A", "B", "C", "D", "E"}
ALLOWED_CATEGORIES = {
    "official",
    "developer_community",
    "research",
    "chinese_media",
    "social_signal",
    "benchmark",
    "tooling",
    "other",
}
ALLOWED_LANGUAGES = {"en", "zh", "multi"}
ALLOWED_FETCH_METHODS = {
    "rss",
    "html",
    "rss_or_html",
    "api",
    "search",
    "manual",
    "wechat_search",
    "youtube",
    "github",
    "arxiv",
    "huggingface",
    "other",
}
ALLOWED_FREQUENCIES = {"hourly", "daily", "weekly", "ad_hoc"}
SOURCE_ID_RE = re.compile(r"^[a-z0-9_]+$")
LOCAL_PATH_MARKERS = (
    "/" + "Users" + "/",
    "/" + "Volumes" + "/",
    "D:" + "/",
    "D:" + "\\",
    "C:" + "/",
    "C:" + "\\",
    "file" + "://",
)


class SourceRegistryError(ValueError):
    """Raised when the source registry file cannot be parsed."""


@dataclass(frozen=True)
class SourceConfig:
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
    owner: str
    notes: str


@dataclass(frozen=True)
class SourceRegistry:
    schema_version: str
    updated_at: str
    description: str
    sources: tuple[SourceConfig, ...]

    def enabled_sources(self) -> tuple[SourceConfig, ...]:
        return tuple(source for source in self.sources if source.enabled)

    def by_tier(self, tier: str) -> tuple[SourceConfig, ...]:
        normalized = tier.upper()
        return tuple(source for source in self.sources if source.tier == normalized)

    def by_category(self, category: str) -> tuple[SourceConfig, ...]:
        return tuple(source for source in self.sources if source.category == category)

    def get(self, source_id: str) -> SourceConfig | None:
        for source in self.sources:
            if source.source_id == source_id:
                return source
        return None

    def tier_counts(self) -> Counter[str]:
        return Counter(source.tier for source in self.sources)

    def category_counts(self) -> Counter[str]:
        return Counter(source.category for source in self.sources)


@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    source_id: str | None
    field: str | None
    message: str


def _repo_root_from_module() -> Path:
    return Path(__file__).resolve().parents[2]


def _parse_scalar(raw_value: str) -> str | int | bool:
    value = raw_value.strip()
    if not value:
        return ""
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def _split_key_value(text: str, line_number: int) -> tuple[str, str]:
    if ":" not in text:
        raise SourceRegistryError(f"Line {line_number}: expected key-value pair")
    key, value = text.split(":", 1)
    key = key.strip()
    if not key:
        raise SourceRegistryError(f"Line {line_number}: empty key")
    return key, value.strip()


def _parse_sources_yaml(text: str) -> dict[str, Any]:
    """Parse the small YAML subset used by config/sources.yaml.

    Supported syntax is intentionally narrow: top-level scalar key-values,
    a top-level ``sources:`` list, source scalar fields, and one nested string
    list field such as ``fallback_methods``.
    """

    data: dict[str, Any] = {}
    sources: list[dict[str, Any]] = []
    in_sources = False
    current_source: dict[str, Any] | None = None
    current_list_key: str | None = None

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()

        if indent == 0:
            if stripped == "sources:":
                in_sources = True
                current_list_key = None
                data["sources"] = sources
                continue
            key, value = _split_key_value(stripped, line_number)
            data[key] = _parse_scalar(value)
            in_sources = False
            current_list_key = None
            continue

        if not in_sources:
            raise SourceRegistryError(f"Line {line_number}: unexpected indentation outside sources")

        if indent == 2 and stripped.startswith("- "):
            if current_source is not None:
                sources.append(current_source)
            current_source = {}
            current_list_key = None
            remainder = stripped[2:].strip()
            if remainder:
                key, value = _split_key_value(remainder, line_number)
                current_source[key] = _parse_scalar(value)
            continue

        if current_source is None:
            raise SourceRegistryError(f"Line {line_number}: source field before source item")

        if indent == 4:
            if stripped.endswith(":"):
                current_list_key = stripped[:-1].strip()
                current_source[current_list_key] = []
                continue
            key, value = _split_key_value(stripped, line_number)
            current_source[key] = _parse_scalar(value)
            current_list_key = None
            continue

        if indent == 6 and stripped.startswith("- "):
            if current_list_key is None:
                raise SourceRegistryError(f"Line {line_number}: list item without list field")
            list_value = current_source.setdefault(current_list_key, [])
            if not isinstance(list_value, list):
                raise SourceRegistryError(f"Line {line_number}: field is not a list")
            list_value.append(_parse_scalar(stripped[2:].strip()))
            continue

        raise SourceRegistryError(f"Line {line_number}: unsupported YAML shape")

    if current_source is not None:
        sources.append(current_source)
    data["sources"] = sources
    return data


def _require_string(mapping: dict[str, Any], field: str) -> str:
    value = mapping[field]
    if not isinstance(value, str):
        raise SourceRegistryError(f"{mapping.get('source_id', '<unknown>')}: {field} must be a string")
    return value


def _source_from_mapping(mapping: dict[str, Any]) -> SourceConfig:
    missing = [field for field in REQUIRED_SOURCE_FIELDS if field not in mapping]
    if missing:
        source_id = mapping.get("source_id", "<unknown>")
        raise SourceRegistryError(f"{source_id}: missing required fields: {', '.join(missing)}")

    fallback_methods = mapping["fallback_methods"]
    if not isinstance(fallback_methods, list):
        raise SourceRegistryError(f"{mapping.get('source_id', '<unknown>')}: fallback_methods must be a list")

    enabled = mapping["enabled"]
    if not isinstance(enabled, bool):
        raise SourceRegistryError(f"{mapping.get('source_id', '<unknown>')}: enabled must be a boolean")

    min_items = mapping["expected_min_items_per_run"]
    if not isinstance(min_items, int):
        raise SourceRegistryError(
            f"{mapping.get('source_id', '<unknown>')}: expected_min_items_per_run must be an integer"
        )

    return SourceConfig(
        source_id=_require_string(mapping, "source_id"),
        label=_require_string(mapping, "label"),
        tier=_require_string(mapping, "tier"),
        category=_require_string(mapping, "category"),
        language=_require_string(mapping, "language"),
        enabled=enabled,
        fetch_method=_require_string(mapping, "fetch_method"),
        primary_url=_require_string(mapping, "primary_url"),
        fallback_methods=tuple(str(item) for item in fallback_methods),
        expected_frequency=_require_string(mapping, "expected_frequency"),
        expected_min_items_per_run=min_items,
        owner=_require_string(mapping, "owner"),
        notes=_require_string(mapping, "notes"),
    )


def load_source_registry(path: Path | None = None, repo_root: Path | None = None) -> SourceRegistry:
    root = (repo_root or _repo_root_from_module()).resolve()
    registry_path = path or (root / "config" / "sources.yaml")
    parsed = _parse_sources_yaml(registry_path.read_text(encoding="utf-8"))
    sources = tuple(_source_from_mapping(item) for item in parsed.get("sources", []))
    return SourceRegistry(
        schema_version=str(parsed.get("schema_version", "")),
        updated_at=str(parsed.get("updated_at", "")),
        description=str(parsed.get("description", "")),
        sources=sources,
    )


def _has_local_path_marker(value: str) -> bool:
    return any(marker in value for marker in LOCAL_PATH_MARKERS)


def _validate_source(source: SourceConfig) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    sid = source.source_id

    def error(field: str, message: str) -> None:
        issues.append(ValidationIssue("ERROR", sid, field, message))

    if not SOURCE_ID_RE.fullmatch(sid):
        error("source_id", "must contain only lowercase letters, digits and underscores")
    if source.tier not in ALLOWED_TIERS:
        error("tier", f"must be one of {sorted(ALLOWED_TIERS)}")
    if source.category not in ALLOWED_CATEGORIES:
        error("category", f"must be one of {sorted(ALLOWED_CATEGORIES)}")
    if source.language not in ALLOWED_LANGUAGES:
        error("language", f"must be one of {sorted(ALLOWED_LANGUAGES)}")
    if source.fetch_method not in ALLOWED_FETCH_METHODS:
        error("fetch_method", f"must be one of {sorted(ALLOWED_FETCH_METHODS)}")
    if source.expected_frequency not in ALLOWED_FREQUENCIES:
        error("expected_frequency", f"must be one of {sorted(ALLOWED_FREQUENCIES)}")
    if not isinstance(source.enabled, bool):
        error("enabled", "must be a bool")
    if source.expected_min_items_per_run < 0:
        error("expected_min_items_per_run", "must be a non-negative integer")
    if not source.primary_url.strip():
        error("primary_url", "must not be empty")
    if not isinstance(source.fallback_methods, tuple):
        error("fallback_methods", "must be a tuple/list")

    text_fields: Iterable[tuple[str, str]] = (
        ("source_id", source.source_id),
        ("label", source.label),
        ("primary_url", source.primary_url),
        ("owner", source.owner),
        ("notes", source.notes),
    )
    for field, value in text_fields:
        if _has_local_path_marker(value):
            error(field, "must not contain a local machine path or file URL")
    for method in source.fallback_methods:
        if _has_local_path_marker(method):
            error("fallback_methods", "must not contain a local machine path or file URL")

    return issues


def validate_registry(registry: SourceRegistry) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    if registry.schema_version != "v1":
        issues.append(ValidationIssue("ERROR", None, "schema_version", "must be v1"))
    if not registry.sources:
        issues.append(ValidationIssue("ERROR", None, "sources", "must contain at least one source"))

    seen: set[str] = set()
    for source in registry.sources:
        if source.source_id in seen:
            issues.append(ValidationIssue("ERROR", source.source_id, "source_id", "must be unique"))
        seen.add(source.source_id)
        issues.extend(_validate_source(source))

    return tuple(issues)

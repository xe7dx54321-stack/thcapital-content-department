"""WeChat RSS Source Registry v1.

Supports env variable injection in RSS URLs and validates that URLs don't
contain sensitive information.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any


SCHEMA_VERSION = "v1"

ALLOWED_TIERS = {"A", "B", "C", "D", "E"}
ALLOWED_LANGUAGES = {"zh", "en", "multi"}

FORBIDDEN_URL_PATTERNS = (
    r"(?i)(?:password|secret|token|api[_-]key|auth[_-]token|access[_-]key|secret[_-]key)",
    r"(?i)(?:github\.com/[^/]+/[^/]+/settings|github\.com/[^/]+/[^/]+/keys)",
    r"(?i)(?:@[^:]+:[^@]+@)",
)

ENV_VAR_RE = re.compile(r"\$\{([^}]+)\}")


@dataclass(frozen=True)
class WechatRssSource:
    schema_version: str
    source_id: str
    label: str
    tier: str
    language: str
    enabled: bool
    is_official: bool
    rss_url: str
    owner: str
    notes: str


@dataclass(frozen=True)
class WechatRssRegistry:
    schema_version: str
    sources: tuple[WechatRssSource, ...]

    def enabled_sources(self) -> tuple[WechatRssSource, ...]:
        return tuple(source for source in self.sources if source.enabled)

    def by_tier(self, tier: str) -> tuple[WechatRssSource, ...]:
        normalized = tier.upper()
        return tuple(source for source in self.sources if source.tier == normalized)

    def get(self, source_id: str) -> WechatRssSource | None:
        for source in self.sources:
            if source.source_id == source_id:
                return source
        return None

    def official_sources(self) -> tuple[WechatRssSource, ...]:
        return tuple(source for source in self.sources if source.is_official)


@dataclass(frozen=True)
class RegistryValidationIssue:
    severity: str
    source_id: str | None
    field: str | None
    message: str


def resolve_env_variables(text: str) -> str:
    def replace_match(match: re.Match[str]) -> str:
        var_name = match.group(1)
        return os.environ.get(var_name, match.group(0))

    return ENV_VAR_RE.sub(replace_match, text)


def contains_forbidden_pattern(url: str) -> bool:
    for pattern in FORBIDDEN_URL_PATTERNS:
        if re.search(pattern, url):
            return True
    return False


def validate_source(source: WechatRssSource) -> list[RegistryValidationIssue]:
    issues: list[RegistryValidationIssue] = []
    sid = source.source_id

    def error(field: str, message: str) -> None:
        issues.append(RegistryValidationIssue("ERROR", sid, field, message))

    def warn(field: str, message: str) -> None:
        issues.append(RegistryValidationIssue("WARNING", sid, field, message))

    if not re.fullmatch(r"^[a-z0-9_]+$", sid):
        error("source_id", "must contain only lowercase letters, digits and underscores")

    if source.tier not in ALLOWED_TIERS:
        error("tier", f"must be one of {sorted(ALLOWED_TIERS)}")

    if source.language not in ALLOWED_LANGUAGES:
        error("language", f"must be one of {sorted(ALLOWED_LANGUAGES)}")

    if not isinstance(source.enabled, bool):
        error("enabled", "must be a boolean")

    if not isinstance(source.is_official, bool):
        error("is_official", "must be a boolean")

    resolved_url = resolve_env_variables(source.rss_url)

    if not resolved_url.strip():
        error("rss_url", "must not be empty after env resolution")

    if resolved_url != source.rss_url:
        warn("rss_url", "contains env variable references")

    if contains_forbidden_pattern(resolved_url):
        error("rss_url", "contains potential sensitive information")

    if not resolved_url.startswith(("http://", "https://")):
        error("rss_url", "must be a valid http/https URL")

    if not source.owner.strip():
        error("owner", "must not be empty")

    return issues


def validate_registry(registry: WechatRssRegistry) -> tuple[RegistryValidationIssue, ...]:
    issues: list[RegistryValidationIssue] = []

    if registry.schema_version != SCHEMA_VERSION:
        issues.append(RegistryValidationIssue("ERROR", None, "schema_version", f"must be {SCHEMA_VERSION}"))

    if not registry.sources:
        issues.append(RegistryValidationIssue("ERROR", None, "sources", "must contain at least one source"))

    seen: set[str] = set()
    for source in registry.sources:
        if source.source_id in seen:
            issues.append(RegistryValidationIssue("ERROR", source.source_id, "source_id", "must be unique"))
        seen.add(source.source_id)
        issues.extend(validate_source(source))

    return tuple(issues)


def source_from_mapping(mapping: dict[str, Any]) -> WechatRssSource:
    return WechatRssSource(
        schema_version=SCHEMA_VERSION,
        source_id=str(mapping.get("source_id", "")).strip(),
        label=str(mapping.get("label", "")).strip(),
        tier=str(mapping.get("tier", "C")).strip().upper(),
        language=str(mapping.get("language", "zh")).strip(),
        enabled=bool(mapping.get("enabled", True)),
        is_official=bool(mapping.get("is_official", False)),
        rss_url=str(mapping.get("rss_url", "")).strip(),
        owner=str(mapping.get("owner", "")).strip(),
        notes=str(mapping.get("notes", "")).strip(),
    )


def registry_from_config(config: dict[str, Any]) -> WechatRssRegistry:
    sources = tuple(source_from_mapping(item) for item in config.get("sources", []))
    return WechatRssRegistry(
        schema_version=SCHEMA_VERSION,
        sources=sources,
    )
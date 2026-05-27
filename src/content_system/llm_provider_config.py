"""LLM provider configuration helpers for Phase 6.

Phase 6 defaults to mock/dry-run. Live provider entries are configuration
placeholders until an explicit adapter is introduced in a later phase.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "v1"
ALLOWED_MODES = {"dry_run", "live"}
SECRET_MARKERS = (
    "sk-",
    "sk_",
    "AIza",
    "xoxb-",
    "xapp-",
    "anthropic_",
)
ENV_NAME_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


class LLMProviderConfigError(ValueError):
    """Raised when the LLM provider config cannot be loaded."""


@dataclass(frozen=True)
class LLMProvider:
    provider_id: str
    label: str
    enabled: bool
    mode: str
    api_key_env: str
    default_model: str
    supports_live: bool
    base_url: str
    base_url_env: str
    default_base_url: str
    api_model: str
    model_env: str
    api_style: str
    adapter_type: str
    request_path: str
    auth_header: str
    anthropic_version: str
    stream: bool
    live_agent_allowlist: tuple[str, ...]
    estimated_cost_per_1k_input_tokens_usd: float
    estimated_cost_per_1k_output_tokens_usd: float
    notes: str


@dataclass(frozen=True)
class AgentModelPreference:
    agent_id: str
    preferred_provider: str
    preferred_model: str
    task_class: str
    reason: str


@dataclass(frozen=True)
class LLMLimits:
    daily_cost_limit_usd: float
    max_tokens_per_call: int
    timeout_seconds: int
    max_calls_per_run: int


@dataclass(frozen=True)
class LLMProviderConfig:
    schema_version: str
    default_provider: str
    default_mode: str
    default_light_provider: str
    default_light_model: str
    default_reasoning_provider: str
    default_reasoning_model: str
    providers: tuple[LLMProvider, ...]
    agent_model_map: tuple[AgentModelPreference, ...]
    limits: LLMLimits

    def get_provider(self, provider_id: str) -> LLMProvider | None:
        for provider in self.providers:
            if provider.provider_id == provider_id:
                return provider
        return None

    def get_agent_model(self, agent_id: str) -> AgentModelPreference | None:
        for preference in self.agent_model_map:
            if preference.agent_id == agent_id:
                return preference
        return None


@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    provider_id: str | None
    field: str | None
    message: str


def repo_root_from_module() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LLMProviderConfigError(f"failed to read {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise LLMProviderConfigError("llm provider config must be a JSON object")
    return payload


def provider_from_mapping(mapping: dict[str, Any]) -> LLMProvider:
    required = (
        "provider_id",
        "label",
        "enabled",
        "mode",
        "api_key_env",
        "default_model",
        "supports_live",
        "base_url",
        "notes",
    )
    missing = [field for field in required if field not in mapping]
    if missing:
        raise LLMProviderConfigError(f"provider missing fields: {', '.join(missing)}")
    live_agent_allowlist_raw = mapping.get("live_agent_allowlist", [])
    live_agent_allowlist = tuple(str(item) for item in live_agent_allowlist_raw if item) if isinstance(live_agent_allowlist_raw, list) else ()
    return LLMProvider(
        provider_id=str(mapping["provider_id"]),
        label=str(mapping["label"]),
        enabled=bool(mapping["enabled"]),
        mode=str(mapping["mode"]),
        api_key_env=str(mapping["api_key_env"]),
        default_model=str(mapping["default_model"]),
        supports_live=bool(mapping["supports_live"]),
        base_url=str(mapping["base_url"]),
        base_url_env=str(mapping.get("base_url_env", "")),
        default_base_url=str(mapping.get("default_base_url", mapping.get("base_url", ""))),
        api_model=str(mapping.get("api_model", mapping["default_model"])),
        model_env=str(mapping.get("model_env", "")),
        api_style=str(mapping.get("api_style", "")),
        adapter_type=str(mapping.get("adapter_type", mapping.get("api_style", ""))),
        request_path=str(mapping.get("request_path", "")),
        auth_header=str(mapping.get("auth_header", "")),
        anthropic_version=str(mapping.get("anthropic_version", "")),
        stream=bool(mapping.get("stream", False)),
        live_agent_allowlist=live_agent_allowlist,
        estimated_cost_per_1k_input_tokens_usd=float(mapping.get("estimated_cost_per_1k_input_tokens_usd", 0.0)),
        estimated_cost_per_1k_output_tokens_usd=float(mapping.get("estimated_cost_per_1k_output_tokens_usd", 0.0)),
        notes=str(mapping["notes"]),
    )


def agent_model_from_mapping(mapping: dict[str, Any]) -> AgentModelPreference:
    required = ("agent_id", "preferred_provider", "preferred_model", "task_class", "reason")
    missing = [field for field in required if field not in mapping]
    if missing:
        raise LLMProviderConfigError(f"agent model preference missing fields: {', '.join(missing)}")
    return AgentModelPreference(
        agent_id=str(mapping["agent_id"]),
        preferred_provider=str(mapping["preferred_provider"]),
        preferred_model=str(mapping["preferred_model"]),
        task_class=str(mapping["task_class"]),
        reason=str(mapping["reason"]),
    )


def load_llm_provider_config(path: Path | None = None, repo_root: Path | None = None) -> LLMProviderConfig:
    root = (repo_root or repo_root_from_module()).resolve()
    config_path = path or root / "config" / "llm_providers.json"
    payload = read_json(config_path)
    providers_raw = payload.get("providers")
    if not isinstance(providers_raw, list):
        raise LLMProviderConfigError("providers must be a list")
    agent_model_raw = payload.get("agent_model_map", [])
    if not isinstance(agent_model_raw, list):
        raise LLMProviderConfigError("agent_model_map must be a list")
    limits_raw = payload.get("limits")
    if not isinstance(limits_raw, dict):
        raise LLMProviderConfigError("limits must be an object")
    limits = LLMLimits(
        daily_cost_limit_usd=float(limits_raw.get("daily_cost_limit_usd", 0.0)),
        max_tokens_per_call=int(limits_raw.get("max_tokens_per_call", 0)),
        timeout_seconds=int(limits_raw.get("timeout_seconds", 0)),
        max_calls_per_run=int(limits_raw.get("max_calls_per_run", 0)),
    )
    return LLMProviderConfig(
        schema_version=str(payload.get("schema_version", "")),
        default_provider=str(payload.get("default_provider", "")),
        default_mode=str(payload.get("default_mode", "")),
        default_light_provider=str(payload.get("default_light_provider", "")),
        default_light_model=str(payload.get("default_light_model", "")),
        default_reasoning_provider=str(payload.get("default_reasoning_provider", "")),
        default_reasoning_model=str(payload.get("default_reasoning_model", "")),
        providers=tuple(provider_from_mapping(item) for item in providers_raw if isinstance(item, dict)),
        agent_model_map=tuple(agent_model_from_mapping(item) for item in agent_model_raw if isinstance(item, dict)),
        limits=limits,
    )


def looks_like_secret(value: str) -> bool:
    stripped = value.strip()
    return any(marker in stripped for marker in SECRET_MARKERS) or (len(stripped) > 80 and not re.search(r"\s", stripped) and not stripped.startswith("http"))


def validate_llm_provider_config(config: LLMProviderConfig, provider_filter: str | None = None) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    if config.schema_version != SCHEMA_VERSION:
        issues.append(ValidationIssue("ERROR", None, "schema_version", "schema_version must be v1"))
    if config.default_mode not in ALLOWED_MODES:
        issues.append(ValidationIssue("ERROR", None, "default_mode", "default_mode must be dry_run or live"))

    provider_ids = [provider.provider_id for provider in config.providers]
    if "mock" not in provider_ids:
        issues.append(ValidationIssue("ERROR", None, "providers", "mock provider is required"))
    if config.default_provider not in provider_ids:
        issues.append(ValidationIssue("ERROR", None, "default_provider", "default_provider must exist in providers"))
    if config.default_light_provider and config.default_light_provider not in provider_ids:
        issues.append(ValidationIssue("ERROR", None, "default_light_provider", "default_light_provider must exist in providers"))
    if config.default_reasoning_provider and config.default_reasoning_provider not in provider_ids:
        issues.append(ValidationIssue("ERROR", None, "default_reasoning_provider", "default_reasoning_provider must exist in providers"))
    duplicates = sorted({item for item in provider_ids if provider_ids.count(item) > 1})
    for provider_id in duplicates:
        issues.append(ValidationIssue("ERROR", provider_id, "provider_id", "provider_id must be unique"))

    for provider in config.providers:
        if provider_filter and provider.provider_id != provider_filter:
            continue
        if provider.mode not in ALLOWED_MODES:
            issues.append(ValidationIssue("ERROR", provider.provider_id, "mode", "mode must be dry_run or live"))
        for field, value in (
            ("provider_id", provider.provider_id),
            ("api_key_env", provider.api_key_env),
            ("default_model", provider.default_model),
            ("base_url", provider.base_url),
            ("base_url_env", provider.base_url_env),
            ("default_base_url", provider.default_base_url),
            ("api_model", provider.api_model),
            ("model_env", provider.model_env),
            ("notes", provider.notes),
        ):
            if value and looks_like_secret(value):
                issues.append(ValidationIssue("ERROR", provider.provider_id, field, "config appears to contain a secret value"))
        for field, value in (("api_key_env", provider.api_key_env), ("base_url_env", provider.base_url_env), ("model_env", provider.model_env)):
            if value and not ENV_NAME_RE.fullmatch(value):
                issues.append(ValidationIssue("ERROR", provider.provider_id, field, f"{field} must be an environment variable name"))
        if provider.mode == "live" and not provider.supports_live:
            issues.append(ValidationIssue("ERROR", provider.provider_id, "mode", "live mode is not supported for this provider"))
        if provider.mode == "live" and provider.api_key_env and not os.environ.get(provider.api_key_env):
            issues.append(ValidationIssue("ERROR", provider.provider_id, "api_key_env", f"missing environment variable {provider.api_key_env} for live mode"))
        if provider.enabled and provider.supports_live and provider.mode == "dry_run" and provider.api_key_env and not os.environ.get(provider.api_key_env):
            issues.append(ValidationIssue("WARN", provider.provider_id, "api_key_env", f"{provider.api_key_env} is not set; live mode remains unavailable"))
        if provider.provider_id == "manimax":
            if provider.adapter_type != "openai_compatible_chat_completions":
                issues.append(ValidationIssue("ERROR", provider.provider_id, "adapter_type", "MiniMax pilot requires openai_compatible_chat_completions"))
            if provider.stream:
                issues.append(ValidationIssue("ERROR", provider.provider_id, "stream", "MiniMax pilot must use non-streaming calls"))
        if provider.provider_id == "anthropic":
            if provider.adapter_type != "anthropic_messages":
                issues.append(ValidationIssue("ERROR", provider.provider_id, "adapter_type", "Claude critic pilot requires anthropic_messages"))
            if provider.stream:
                issues.append(ValidationIssue("ERROR", provider.provider_id, "stream", "Claude critic pilot must use non-streaming calls"))
            if "llm_critic_agent" not in provider.live_agent_allowlist:
                issues.append(ValidationIssue("ERROR", provider.provider_id, "live_agent_allowlist", "Claude critic pilot requires llm_critic_agent in provider allowlist"))
            if not provider.anthropic_version:
                issues.append(ValidationIssue("ERROR", provider.provider_id, "anthropic_version", "Anthropic Messages API requires anthropic_version"))

    agent_ids = [preference.agent_id for preference in config.agent_model_map]
    for agent_id in sorted({item for item in agent_ids if agent_ids.count(item) > 1}):
        issues.append(ValidationIssue("ERROR", agent_id, "agent_model_map", "agent_id must be unique"))
    for preference in config.agent_model_map:
        if preference.preferred_provider not in provider_ids:
            issues.append(ValidationIssue("ERROR", preference.agent_id, "preferred_provider", "preferred_provider must exist in providers"))
        if preference.task_class not in {"light", "reasoning"}:
            issues.append(ValidationIssue("ERROR", preference.agent_id, "task_class", "task_class must be light or reasoning"))
        if preference.preferred_model and looks_like_secret(preference.preferred_model):
            issues.append(ValidationIssue("ERROR", preference.agent_id, "preferred_model", "preferred_model appears to contain a secret"))

    if config.limits.daily_cost_limit_usd < 0:
        issues.append(ValidationIssue("ERROR", None, "limits.daily_cost_limit_usd", "daily cost limit must be non-negative"))
    if config.limits.max_calls_per_run <= 0:
        issues.append(ValidationIssue("ERROR", None, "limits.max_calls_per_run", "max_calls_per_run must be positive"))
    return tuple(issues)


def resolve_provider_from_env(config: LLMProviderConfig, provider_id: str | None = None) -> LLMProvider:
    requested = provider_id or os.environ.get("THCAP_LLM_DEFAULT_PROVIDER") or config.default_provider
    provider = config.get_provider(requested)
    if provider is None:
        provider = config.get_provider(config.default_provider)
    if provider is None:
        raise LLMProviderConfigError("no usable provider found")
    return provider


def resolve_mode_from_env(config: LLMProviderConfig, mode: str | None = None) -> str:
    resolved = mode or os.environ.get("THCAP_LLM_MODE") or config.default_mode
    return resolved if resolved in ALLOWED_MODES else config.default_mode


def resolve_model_from_env(provider: LLMProvider, model: str | None = None) -> str:
    return model or os.environ.get("THCAP_LLM_DEFAULT_MODEL") or provider.default_model


def resolve_agent_provider_and_model(
    config: LLMProviderConfig,
    agent_id: str,
    provider_id: str | None = None,
    model: str | None = None,
) -> tuple[LLMProvider, str]:
    preference = config.get_agent_model(agent_id)
    requested_provider = provider_id or os.environ.get("THCAP_LLM_DEFAULT_PROVIDER") or (preference.preferred_provider if preference else config.default_provider)
    provider = config.get_provider(requested_provider) or config.get_provider(config.default_provider)
    if provider is None:
        raise LLMProviderConfigError("no usable provider found")
    requested_model = model or os.environ.get("THCAP_LLM_DEFAULT_MODEL") or (preference.preferred_model if preference else provider.default_model)
    return provider, requested_model


def is_live_enabled(provider: LLMProvider, mode: str) -> bool:
    return provider.provider_id != "mock" and mode == "live" and provider.supports_live and bool(provider.api_key_env and os.environ.get(provider.api_key_env))


def redact_sensitive_values(mapping: dict[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for key, value in mapping.items():
        if "key" in key.lower() or "token" in key.lower() or (isinstance(value, str) and looks_like_secret(value)):
            redacted[key] = "<redacted>"
        else:
            redacted[key] = value
    return redacted

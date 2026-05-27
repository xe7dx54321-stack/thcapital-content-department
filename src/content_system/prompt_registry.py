"""Prompt registry for Phase 6 LLM agent prompts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "v1"
REQUIRED_PROMPT_FIELDS = (
    "prompt_id",
    "version",
    "agent_role",
    "description",
    "system_prompt",
    "user_prompt_template",
    "input_schema",
    "output_schema",
    "safety_notes",
)
REQUIRED_PROMPTS = {
    "llm_proponent_agent",
    "llm_critic_agent",
    "llm_judge_agent",
    "llm_rewrite_agent",
}
SAFETY_PHRASES = ("evidence", "Return JSON", "Do not invent", "Do not publish")


class PromptRegistryError(ValueError):
    """Raised when prompt registry loading or rendering fails."""


@dataclass(frozen=True)
class AgentPrompt:
    prompt_id: str
    version: str
    agent_role: str
    preferred_provider: str
    preferred_model: str
    description: str
    system_prompt: str
    user_prompt_template: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    safety_notes: tuple[str, ...]


@dataclass(frozen=True)
class PromptRegistry:
    schema_version: str
    updated_at: str
    prompts: tuple[AgentPrompt, ...]

    def get(self, prompt_id: str) -> AgentPrompt | None:
        for prompt in self.prompts:
            if prompt.prompt_id == prompt_id:
                return prompt
        return None

    def list_prompts(self) -> tuple[AgentPrompt, ...]:
        return self.prompts


@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    prompt_id: str | None
    field: str | None
    message: str


def repo_root_from_module() -> Path:
    return Path(__file__).resolve().parents[2]


def prompt_from_mapping(mapping: dict[str, Any]) -> AgentPrompt:
    missing = [field for field in REQUIRED_PROMPT_FIELDS if field not in mapping]
    if missing:
        raise PromptRegistryError(f"prompt missing fields: {', '.join(missing)}")
    safety = mapping["safety_notes"]
    if not isinstance(safety, list):
        raise PromptRegistryError(f"{mapping.get('prompt_id', '<unknown>')}: safety_notes must be a list")
    return AgentPrompt(
        prompt_id=str(mapping["prompt_id"]),
        version=str(mapping["version"]),
        agent_role=str(mapping["agent_role"]),
        preferred_provider=str(mapping.get("preferred_provider", "")),
        preferred_model=str(mapping.get("preferred_model", "")),
        description=str(mapping["description"]),
        system_prompt=str(mapping["system_prompt"]),
        user_prompt_template=str(mapping["user_prompt_template"]),
        input_schema=dict(mapping["input_schema"]) if isinstance(mapping["input_schema"], dict) else {},
        output_schema=dict(mapping["output_schema"]) if isinstance(mapping["output_schema"], dict) else {},
        safety_notes=tuple(str(item) for item in safety),
    )


def load_prompt_registry(path: Path | None = None, repo_root: Path | None = None) -> PromptRegistry:
    root = (repo_root or repo_root_from_module()).resolve()
    prompt_path = path or root / "config" / "agent_prompts.json"
    try:
        payload = json.loads(prompt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PromptRegistryError(f"failed to read {prompt_path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise PromptRegistryError("prompt registry must be a JSON object")
    raw_prompts = payload.get("prompts")
    if not isinstance(raw_prompts, list):
        raise PromptRegistryError("prompts must be a list")
    return PromptRegistry(
        schema_version=str(payload.get("schema_version", "")),
        updated_at=str(payload.get("updated_at", "")),
        prompts=tuple(prompt_from_mapping(item) for item in raw_prompts if isinstance(item, dict)),
    )


def validate_prompt_registry(registry: PromptRegistry, prompt_filter: str | None = None) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    if registry.schema_version != SCHEMA_VERSION:
        issues.append(ValidationIssue("ERROR", None, "schema_version", "schema_version must be v1"))
    prompt_ids = [prompt.prompt_id for prompt in registry.prompts]
    for prompt_id in sorted(REQUIRED_PROMPTS - set(prompt_ids)):
        issues.append(ValidationIssue("ERROR", prompt_id, "prompt_id", "required prompt is missing"))
    for prompt_id in sorted({item for item in prompt_ids if prompt_ids.count(item) > 1}):
        issues.append(ValidationIssue("ERROR", prompt_id, "prompt_id", "prompt_id must be unique"))
    for prompt in registry.prompts:
        if prompt_filter and prompt.prompt_id != prompt_filter:
            continue
        if not prompt.version:
            issues.append(ValidationIssue("ERROR", prompt.prompt_id, "version", "version is required"))
        if not prompt.preferred_provider:
            issues.append(ValidationIssue("WARN", prompt.prompt_id, "preferred_provider", "preferred_provider is not set"))
        if not prompt.preferred_model:
            issues.append(ValidationIssue("WARN", prompt.prompt_id, "preferred_model", "preferred_model is not set"))
        input_required = prompt.input_schema.get("required_fields")
        output_required = prompt.output_schema.get("required_fields")
        if not isinstance(input_required, list) or not input_required:
            issues.append(ValidationIssue("ERROR", prompt.prompt_id, "input_schema", "required_fields must be a non-empty list"))
        if not isinstance(output_required, list) or not output_required:
            issues.append(ValidationIssue("ERROR", prompt.prompt_id, "output_schema", "required_fields must be a non-empty list"))
        combined = "\n".join((prompt.system_prompt, prompt.user_prompt_template, "\n".join(prompt.safety_notes)))
        for phrase in SAFETY_PHRASES:
            if phrase not in combined:
                issues.append(ValidationIssue("WARN", prompt.prompt_id, "safety_notes", f"safety phrase not found: {phrase}"))
    return tuple(issues)


def render_prompt(prompt_id: str, inputs: dict[str, Any], registry: PromptRegistry | None = None, repo_root: Path | None = None) -> tuple[str, str, dict[str, Any]]:
    loaded = registry or load_prompt_registry(repo_root=repo_root)
    prompt = loaded.get(prompt_id)
    if prompt is None:
        raise PromptRegistryError(f"unknown prompt_id: {prompt_id}")
    rendered_inputs: dict[str, str] = {}
    for key, value in inputs.items():
        rendered_inputs[key] = json.dumps(value, ensure_ascii=False, indent=2) if not isinstance(value, str) else value
    try:
        user_prompt = prompt.user_prompt_template.format(**rendered_inputs)
    except KeyError as exc:
        raise PromptRegistryError(f"missing prompt input: {exc}") from exc
    return prompt.system_prompt, user_prompt, prompt.output_schema

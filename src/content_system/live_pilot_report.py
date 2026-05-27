"""Shared live pilot readiness report helpers for Phase 7."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.llm_provider_config import load_llm_provider_config
from content_system.paths import get_project_paths


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class ReadyChecks:
    provider_configured: bool
    provider_supports_live: bool
    live_enabled: bool
    mode_live: bool
    agent_allowlisted: bool
    api_key_present: bool
    adapter_supported: bool


@dataclass(frozen=True)
class LivePilotReport:
    schema_version: str
    generated_at: str
    run_date: str
    status: str
    agent_name: str
    provider_id: str
    ready_checks: ReadyChecks
    command: str
    returncode: int | None
    live_call_attempted: bool
    live_call_succeeded: bool
    fallback_used: bool
    fallback_reason: str
    item_count: int
    warnings: tuple[str, ...]
    outputs: dict[str, str]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def live_allowlist() -> set[str]:
    raw = os.environ.get("THCAP_LLM_LIVE_AGENT_ALLOWLIST", "")
    return {item.strip() for item in raw.split(",") if item.strip()}


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def build_ready_checks(
    *,
    repo_root: Path,
    provider_id: str,
    agent_name: str,
    api_key_env: str,
    adapter_type: str,
) -> ReadyChecks:
    config = load_llm_provider_config(repo_root=repo_root)
    provider = config.get_provider(provider_id)
    return ReadyChecks(
        provider_configured=provider is not None,
        provider_supports_live=bool(provider and provider.supports_live),
        live_enabled=os.environ.get("THCAP_LLM_ENABLE_LIVE", "").strip() == "1",
        mode_live=os.environ.get("THCAP_LLM_MODE", "").strip() == "live",
        agent_allowlisted=agent_name in live_allowlist(),
        api_key_present=bool(os.environ.get(api_key_env)),
        adapter_supported=bool(provider and provider.adapter_type == adapter_type),
    )


def readiness_warnings(checks: ReadyChecks, *, provider_label: str, agent_name: str, api_key_env: str, adapter_type: str) -> tuple[str, ...]:
    warnings: list[str] = []
    if not checks.provider_configured:
        warnings.append(f"{provider_label} provider is not configured.")
    if not checks.provider_supports_live:
        warnings.append(f"{provider_label} provider does not support live mode in config.")
    if not checks.live_enabled:
        warnings.append("THCAP_LLM_ENABLE_LIVE is not 1.")
    if not checks.mode_live:
        warnings.append("THCAP_LLM_MODE is not live.")
    if not checks.agent_allowlisted:
        warnings.append(f"{agent_name} is not in THCAP_LLM_LIVE_AGENT_ALLOWLIST.")
    if not checks.api_key_present:
        warnings.append(f"{api_key_env} is not set.")
    if not checks.adapter_supported:
        warnings.append(f"{provider_label} adapter_type is not {adapter_type}.")
    return tuple(warnings)


def is_ready(checks: ReadyChecks) -> bool:
    return all(asdict(checks).values())


def output_paths(repo_root: Path, slug: str, run_date: str) -> dict[str, Path]:
    paths = get_project_paths(repo_root)
    return {
        "dated_json": paths.logs_root / f"{run_date}__{slug}.json",
        "dated_md": paths.logs_root / f"{run_date}__{slug}.md",
        "latest_json": paths.logs_root / f"latest_{slug.replace('-', '_')}.json",
        "latest_md": paths.logs_root / f"latest_{slug.replace('-', '_')}.md",
    }


def summarize_payload(payload: dict[str, Any], list_key: str) -> dict[str, Any]:
    raw_items = payload.get(list_key)
    items = [item for item in raw_items if isinstance(item, dict)] if isinstance(raw_items, list) else []
    fallback_reasons = [str(item.get("fallback_reason") or "") for item in items if item.get("fallback_reason")]
    return {
        "item_count": len(items),
        "live_call_attempted": any(bool(item.get("live_call_attempted")) for item in items),
        "live_call_succeeded": any(bool(item.get("live_call_succeeded")) for item in items),
        "fallback_used": any(bool(item.get("fallback_used")) for item in items),
        "fallback_reason": "; ".join(fallback_reasons[:3]),
    }


def render_markdown(report: LivePilotReport, title: str) -> str:
    checks = asdict(report.ready_checks)
    check_lines = "\n".join(f"- {key}: `{value}`" for key, value in checks.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    output_lines = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    return f"""# {title}

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**
- Agent: `{report.agent_name}`
- Provider: `{report.provider_id}`
- Command: `{report.command or '-'}`
- Return code: `{report.returncode if report.returncode is not None else '-'}`

## Ready Checks

{check_lines}

## Result

- Items: `{report.item_count}`
- Live attempted: `{report.live_call_attempted}`
- Live succeeded: `{report.live_call_succeeded}`
- Fallback used: `{report.fallback_used}`
- Fallback reason: `{report.fallback_reason or '-'}`

## Outputs

{output_lines}

## Warnings

{warnings}
"""


def write_report(report: LivePilotReport, repo_root: Path, slug: str, title: str) -> dict[str, Path]:
    outputs = output_paths(repo_root, slug, report.run_date)
    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(asdict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report, title)
    for path in (outputs["dated_json"], outputs["latest_json"]):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (outputs["dated_md"], outputs["latest_md"]):
        path.write_text(markdown, encoding="utf-8")
    return outputs


def build_report(
    *,
    repo_root: Path,
    slug: str,
    status: str,
    agent_name: str,
    provider_id: str,
    checks: ReadyChecks,
    command: list[str] | None = None,
    returncode: int | None = None,
    summary: dict[str, Any] | None = None,
    warnings: tuple[str, ...] = (),
) -> LivePilotReport:
    payload = summary or {}
    outputs = output_paths(repo_root, slug, today_token())
    return LivePilotReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=today_token(),
        status=status,
        agent_name=agent_name,
        provider_id=provider_id,
        ready_checks=checks,
        command=" ".join(command or []),
        returncode=returncode,
        live_call_attempted=bool(payload.get("live_call_attempted")),
        live_call_succeeded=bool(payload.get("live_call_succeeded")),
        fallback_used=bool(payload.get("fallback_used")),
        fallback_reason=str(payload.get("fallback_reason") or ""),
        item_count=int(payload.get("item_count") or 0),
        warnings=warnings,
        outputs={key: repo_relative(path, repo_root) for key, path in outputs.items()},
    )


def run_pilot(
    *,
    repo_root: Path,
    title: str,
    slug: str,
    agent_name: str,
    provider_id: str,
    provider_label: str,
    api_key_env: str,
    adapter_type: str,
    runner_script: str,
    artifact_path: Path,
    list_key: str,
    dry_run_check: bool,
    as_json: bool,
) -> int:
    checks = build_ready_checks(
        repo_root=repo_root,
        provider_id=provider_id,
        agent_name=agent_name,
        api_key_env=api_key_env,
        adapter_type=adapter_type,
    )
    warnings = readiness_warnings(checks, provider_label=provider_label, agent_name=agent_name, api_key_env=api_key_env, adapter_type=adapter_type)
    command = [sys.executable, runner_script, "--provider", provider_id, "--mode", "live", "--limit", "1"]
    if dry_run_check:
        status = "READY" if is_ready(checks) else "DRY_RUN_REQUIRED"
        report = build_report(repo_root=repo_root, slug=slug, status=status, agent_name=agent_name, provider_id=provider_id, checks=checks, warnings=warnings)
    elif not is_ready(checks):
        report = build_report(repo_root=repo_root, slug=slug, status="READY_CHECK_FAILED", agent_name=agent_name, provider_id=provider_id, checks=checks, warnings=warnings)
    else:
        completed = subprocess.run(command, cwd=repo_root, text=True, capture_output=True, check=False)
        summary = summarize_payload(read_json(artifact_path), list_key)
        if completed.returncode != 0:
            status = "FAILED"
        elif summary.get("live_call_succeeded"):
            status = "LIVE_SUCCEEDED"
        elif summary.get("live_call_attempted"):
            status = "LIVE_FALLBACK"
        else:
            status = "LIVE_NOT_ATTEMPTED"
        extra_warnings = list(warnings)
        if completed.returncode != 0:
            stderr_tail = "\n".join(completed.stderr.strip().splitlines()[-10:])
            extra_warnings.append(f"live command failed: {stderr_tail}")
        report = build_report(
            repo_root=repo_root,
            slug=slug,
            status=status,
            agent_name=agent_name,
            provider_id=provider_id,
            checks=checks,
            command=command,
            returncode=completed.returncode,
            summary=summary,
            warnings=tuple(extra_warnings),
        )
    written = write_report(report, repo_root, slug, title)
    if as_json:
        print(json.dumps({**asdict(report), "written": {key: str(value) for key, value in written.items()}}, ensure_ascii=False, indent=2))
    else:
        print(title)
        print("=" * len(title))
        print(f"status: {report.status}")
        print(f"ready: {is_ready(report.ready_checks)}")
        print(f"live_call_attempted: {report.live_call_attempted}")
        print(f"live_call_succeeded: {report.live_call_succeeded}")
        print(f"fallback_used: {report.fallback_used}")
        if report.fallback_reason:
            print(f"fallback_reason: {report.fallback_reason}")
        if report.warnings:
            print("\nWarnings:")
            for item in report.warnings:
                print(f"  - {item}")
        print("\nReports:")
        for key, path in written.items():
            print(f"  {key}: {path}")
    return 0 if report.status != "FAILED" else 1

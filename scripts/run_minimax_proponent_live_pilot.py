#!/usr/bin/env python3
"""Run the MiniMax live pilot readiness check for llm_proponent_agent."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.llm_provider_config import load_llm_provider_config  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


AGENT_NAME = "llm_proponent_agent"
PROVIDER_ID = "manimax"
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
class MiniMaxProponentLivePilotReport:
    schema_version: str
    generated_at: str
    run_date: str
    status: str
    ready_checks: ReadyChecks
    command: str
    returncode: int | None
    live_call_attempted: bool
    live_call_succeeded: bool
    fallback_used: bool
    fallback_reason: str
    review_count: int
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


def build_ready_checks() -> ReadyChecks:
    config = load_llm_provider_config(repo_root=REPO_ROOT)
    provider = config.get_provider(PROVIDER_ID)
    return ReadyChecks(
        provider_configured=provider is not None,
        provider_supports_live=bool(provider and provider.supports_live),
        live_enabled=os.environ.get("THCAP_LLM_ENABLE_LIVE", "").strip() == "1",
        mode_live=os.environ.get("THCAP_LLM_MODE", "").strip() == "live",
        agent_allowlisted=AGENT_NAME in live_allowlist(),
        api_key_present=bool(os.environ.get("MINIMAX_API_KEY")),
        adapter_supported=bool(provider and provider.adapter_type == "openai_compatible_chat_completions"),
    )


def readiness_warnings(checks: ReadyChecks) -> tuple[str, ...]:
    warnings: list[str] = []
    if not checks.provider_configured:
        warnings.append("MiniMax provider is not configured.")
    if not checks.provider_supports_live:
        warnings.append("MiniMax provider does not support live mode in config.")
    if not checks.live_enabled:
        warnings.append("THCAP_LLM_ENABLE_LIVE is not 1.")
    if not checks.mode_live:
        warnings.append("THCAP_LLM_MODE is not live.")
    if not checks.agent_allowlisted:
        warnings.append("llm_proponent_agent is not in THCAP_LLM_LIVE_AGENT_ALLOWLIST.")
    if not checks.api_key_present:
        warnings.append("MINIMAX_API_KEY is not set.")
    if not checks.adapter_supported:
        warnings.append("MiniMax adapter_type is not openai_compatible_chat_completions.")
    return tuple(warnings)


def is_ready(checks: ReadyChecks) -> bool:
    return all(asdict(checks).values())


def output_paths(run_date: str) -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    return {
        "dated_json": paths.logs_root / f"{run_date}__minimax-proponent-live-pilot.json",
        "dated_md": paths.logs_root / f"{run_date}__minimax-proponent-live-pilot.md",
        "latest_json": paths.logs_root / "latest_minimax_proponent_live_pilot.json",
        "latest_md": paths.logs_root / "latest_minimax_proponent_live_pilot.md",
    }


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def latest_proponent_payload() -> dict[str, Any]:
    paths = get_project_paths(REPO_ROOT)
    return read_json(paths.market_content_root / "06_review_queue" / "latest_llm_proponent_reviews.json")


def summarize_proponent_payload(payload: dict[str, Any]) -> dict[str, Any]:
    raw_reviews = payload.get("reviews")
    reviews = [item for item in raw_reviews if isinstance(item, dict)] if isinstance(raw_reviews, list) else []
    fallback_reasons = [str(item.get("fallback_reason") or "") for item in reviews if item.get("fallback_reason")]
    return {
        "review_count": len(reviews),
        "live_call_attempted": any(bool(item.get("live_call_attempted")) for item in reviews),
        "live_call_succeeded": any(bool(item.get("live_call_succeeded")) for item in reviews),
        "fallback_used": any(bool(item.get("fallback_used")) for item in reviews),
        "fallback_reason": "; ".join(fallback_reasons[:3]),
    }


def render_markdown(report: MiniMaxProponentLivePilotReport) -> str:
    checks = asdict(report.ready_checks)
    check_lines = "\n".join(f"- {key}: `{value}`" for key, value in checks.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    output_lines = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    return f"""# MiniMax Proponent Live Pilot

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**
- Command: `{report.command or '-'}`
- Return code: `{report.returncode if report.returncode is not None else '-'}`

## Ready Checks

{check_lines}

## Result

- Reviews: `{report.review_count}`
- Live attempted: `{report.live_call_attempted}`
- Live succeeded: `{report.live_call_succeeded}`
- Fallback used: `{report.fallback_used}`
- Fallback reason: `{report.fallback_reason or '-'}`

## Outputs

{output_lines}

## Warnings

{warnings}
"""


def write_report(report: MiniMaxProponentLivePilotReport) -> dict[str, Path]:
    outputs = output_paths(report.run_date)
    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(asdict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)
    for path in (outputs["dated_json"], outputs["latest_json"]):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (outputs["dated_md"], outputs["latest_md"]):
        path.write_text(markdown, encoding="utf-8")
    return outputs


def build_report(
    *,
    status: str,
    checks: ReadyChecks,
    command: list[str] | None = None,
    returncode: int | None = None,
    proponent_summary: dict[str, Any] | None = None,
    warnings: tuple[str, ...] = (),
) -> MiniMaxProponentLivePilotReport:
    summary = proponent_summary or {}
    outputs = output_paths(today_token())
    return MiniMaxProponentLivePilotReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=today_token(),
        status=status,
        ready_checks=checks,
        command=" ".join(command or []),
        returncode=returncode,
        live_call_attempted=bool(summary.get("live_call_attempted")),
        live_call_succeeded=bool(summary.get("live_call_succeeded")),
        fallback_used=bool(summary.get("fallback_used")),
        fallback_reason=str(summary.get("fallback_reason") or ""),
        review_count=int(summary.get("review_count") or 0),
        warnings=warnings,
        outputs={key: repo_relative(path) for key, path in outputs.items()},
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MiniMax live pilot for llm_proponent_agent.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    parser.add_argument("--dry-run-check", action="store_true", help="Only print readiness checks; do not attempt live.")
    args = parser.parse_args()

    checks = build_ready_checks()
    warnings = readiness_warnings(checks)
    command = [
        sys.executable,
        "scripts/run_llm_proponent_reviews.py",
        "--provider",
        PROVIDER_ID,
        "--mode",
        "live",
        "--limit",
        "1",
    ]

    if args.dry_run_check:
        status = "READY" if is_ready(checks) else "DRY_RUN_REQUIRED"
        report = build_report(status=status, checks=checks, warnings=warnings)
    elif not is_ready(checks):
        report = build_report(status="READY_CHECK_FAILED", checks=checks, warnings=warnings)
    else:
        completed = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
        payload = latest_proponent_payload()
        summary = summarize_proponent_payload(payload)
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
            status=status,
            checks=checks,
            command=command,
            returncode=completed.returncode,
            proponent_summary=summary,
            warnings=tuple(extra_warnings),
        )

    written = write_report(report)
    if args.json:
        print(json.dumps({**asdict(report), "written": {key: str(value) for key, value in written.items()}}, ensure_ascii=False, indent=2))
    else:
        print("MiniMax Proponent Live Pilot")
        print("============================")
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


if __name__ == "__main__":
    raise SystemExit(main())

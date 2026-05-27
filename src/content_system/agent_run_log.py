"""Agent run log and cost/error tracking for Phase 6."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class AgentRunRecord:
    request_id: str
    run_date: str
    agent_name: str
    provider_id: str
    model: str
    mode: str
    status: str
    latency_ms: int
    estimated_input_tokens: int
    estimated_output_tokens: int
    estimated_cost_usd: float
    error: str
    fallback_used: bool
    source_artifact: str
    output_artifact: str


@dataclass(frozen=True)
class AgentRunLog:
    schema_version: str
    updated_at: str
    records: tuple[AgentRunRecord, ...]
    summary: dict[str, Any]


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


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def record_from_mapping(mapping: dict[str, Any]) -> AgentRunRecord:
    return AgentRunRecord(
        request_id=str(mapping.get("request_id") or ""),
        run_date=str(mapping.get("run_date") or ""),
        agent_name=str(mapping.get("agent_name") or ""),
        provider_id=str(mapping.get("provider_id") or ""),
        model=str(mapping.get("model") or ""),
        mode=str(mapping.get("mode") or ""),
        status=str(mapping.get("status") or ""),
        latency_ms=int(mapping.get("latency_ms") or 0),
        estimated_input_tokens=int(mapping.get("estimated_input_tokens") or 0),
        estimated_output_tokens=int(mapping.get("estimated_output_tokens") or 0),
        estimated_cost_usd=float(mapping.get("estimated_cost_usd") or 0.0),
        error=str(mapping.get("error") or ""),
        fallback_used=bool(mapping.get("fallback_used")),
        source_artifact=str(mapping.get("source_artifact") or ""),
        output_artifact=str(mapping.get("output_artifact") or ""),
    )


def summary_for(records: tuple[AgentRunRecord, ...]) -> dict[str, Any]:
    return {
        "record_count": len(records),
        "failed_count": sum(1 for record in records if record.status == "FAILED"),
        "dry_run_count": sum(1 for record in records if record.status == "DRY_RUN"),
        "success_count": sum(1 for record in records if record.status == "SUCCESS"),
        "fallback_count": sum(1 for record in records if record.fallback_used),
        "estimated_cost_usd": round(sum(record.estimated_cost_usd for record in records), 6),
    }


def log_paths(paths: ProjectPaths) -> dict[str, Path]:
    return {
        "json": paths.logs_root / "agent_run_log.json",
        "md": paths.logs_root / "agent_run_log.md",
        "frontstage": paths.frontstage_root / "agent_run_log_board.md",
    }


def load_agent_run_log(paths: ProjectPaths) -> AgentRunLog:
    payload = read_json(log_paths(paths)["json"])
    raw = payload.get("records")
    records = tuple(record_from_mapping(item) for item in raw if isinstance(item, dict)) if isinstance(raw, list) else ()
    return AgentRunLog(SCHEMA_VERSION, str(payload.get("updated_at") or utc_now()), records, summary_for(records))


def render_log_markdown(log: AgentRunLog) -> str:
    rows = []
    for idx, record in enumerate(log.records[-100:], start=1):
        error = record.error.replace("|", "\\|").replace("\n", " ")
        rows.append(
            f"| {idx} | {record.run_date} | {record.agent_name} | {record.provider_id} | {record.mode} | {record.status} | {record.estimated_cost_usd:.4f} | {error} |"
        )
    return f"""# Agent Run Log

## Summary

- Updated at: `{log.updated_at}`
- Records: `{log.summary.get('record_count')}`
- Dry-run: `{log.summary.get('dry_run_count')}`
- Failed: `{log.summary.get('failed_count')}`
- Estimated cost USD: `{log.summary.get('estimated_cost_usd')}`

## Recent Records

| # | Run Date | Agent | Provider | Mode | Status | Cost USD | Error |
|---:|---|---|---|---|---|---:|---|
{chr(10).join(rows) if rows else '| 0 | - | - | - | - | - | 0 | None |'}
"""


def write_agent_run_log(log: AgentRunLog, paths: ProjectPaths) -> dict[str, Path]:
    outputs = log_paths(paths)
    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(asdict(log), ensure_ascii=False, indent=2)
    markdown = render_log_markdown(log)
    outputs["json"].write_text(payload + "\n", encoding="utf-8")
    outputs["md"].write_text(markdown, encoding="utf-8")
    outputs["frontstage"].write_text(markdown, encoding="utf-8")
    return outputs


def upsert_agent_run_record(paths: ProjectPaths, record: AgentRunRecord) -> AgentRunLog:
    existing = load_agent_run_log(paths)
    merged = {item.request_id: item for item in existing.records if item.request_id}
    merged[record.request_id] = record
    records = tuple(sorted(merged.values(), key=lambda item: (item.run_date, item.agent_name, item.request_id)))
    log = AgentRunLog(SCHEMA_VERSION, utc_now(), records, summary_for(records))
    write_agent_run_log(log, paths)
    return log


def response_to_record(
    *,
    response: Any,
    agent_name: str,
    run_date: str,
    fallback_used: bool,
    source_artifact: str,
    output_artifact: str,
) -> AgentRunRecord:
    usage = getattr(response, "usage", {}) if response is not None else {}
    return AgentRunRecord(
        request_id=str(getattr(response, "request_id", "")),
        run_date=run_date,
        agent_name=agent_name,
        provider_id=str(getattr(response, "provider_id", "")),
        model=str(getattr(response, "model", "")),
        mode=str(getattr(response, "mode", "")),
        status=str(getattr(response, "status", "")),
        latency_ms=int(getattr(response, "latency_ms", 0)),
        estimated_input_tokens=int(usage.get("estimated_input_tokens", 0)),
        estimated_output_tokens=int(usage.get("estimated_output_tokens", 0)),
        estimated_cost_usd=float(getattr(response, "estimated_cost_usd", 0.0)),
        error=str(getattr(response, "error", "")),
        fallback_used=fallback_used,
        source_artifact=source_artifact,
        output_artifact=output_artifact,
    )


def build_agent_run_summary(paths: ProjectPaths, run_date: str | None = None) -> AgentRunLog:
    log = load_agent_run_log(paths)
    date = run_date or (max((record.run_date for record in log.records if record.run_date), default=today_token()))
    records = tuple(record for record in log.records if record.run_date == date)
    return AgentRunLog(SCHEMA_VERSION, utc_now(), records, summary_for(records))


def summary_output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__agent-run-summary.json",
        "dated_md": paths.logs_root / f"{run_date}__agent-run-summary.md",
        "latest_json": paths.logs_root / "latest_agent_run_summary.json",
        "latest_md": paths.logs_root / "latest_agent_run_summary.md",
    }


def write_agent_run_summary(summary: AgentRunLog, paths: ProjectPaths, run_date: str | None = None) -> dict[str, Path]:
    date = run_date or (max((record.run_date for record in summary.records if record.run_date), default=today_token()))
    outputs = summary_output_paths(paths, date)
    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(asdict(summary), ensure_ascii=False, indent=2)
    markdown = render_log_markdown(summary).replace("# Agent Run Log", "# Agent Run Summary")
    for path in (outputs["dated_json"], outputs["latest_json"]):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (outputs["dated_md"], outputs["latest_md"]):
        path.write_text(markdown, encoding="utf-8")
    return outputs

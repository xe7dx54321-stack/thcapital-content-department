"""Detect OpenClaw schedule conflicts without modifying OpenClaw."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import repo_relative, today_token, utc_now, write_json_and_markdown


OPENCLAW_JOBS_PATH = Path("/Users/apple/.openclaw/cron/jobs.json")


def _load_jobs(path: Path = OPENCLAW_JOBS_PATH) -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    if not path.exists():
        return [], [f"Missing OpenClaw jobs file: {path}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [], [f"Could not parse OpenClaw jobs file: {exc}"]
    if isinstance(payload, list):
        jobs = payload
    elif isinstance(payload, dict):
        raw = payload.get("jobs") or payload.get("items") or []
        jobs = raw if isinstance(raw, list) else []
    else:
        jobs = []
    return [item for item in jobs if isinstance(item, dict)], warnings


def _job_text(job: dict[str, Any]) -> str:
    return " ".join(str(job.get(key, "")) for key in ("id", "job_id", "agent", "name", "description", "prompt", "source_id", "source_ids")).lower()


def classify_conflict(job: dict[str, Any]) -> dict[str, str]:
    text = _job_text(job)
    agent = str(job.get("agent") or job.get("agent_id") or "")
    if any(token in text for token in ("publish", "draft", "wechat draft", "草稿", "发布")):
        return {"runtime_job_id": "none", "conflict_type": "DUPLICATE_CONTENT_GENERATION", "severity": "HIGH", "recommended_action": "DISABLE_OPENCLAW_JOB", "reason": "legacy job appears to touch publishing or draft flow"}
    if any(token in text for token in ("signal", "harvest", "reddit", "techcrunch", "finsmes", "product hunt", "youtube", "x__")) or "signal-harvester" in agent:
        return {"runtime_job_id": "acquisition_phase29", "conflict_type": "OVERLAPPING_SIGNAL_CAPTURE", "severity": "MEDIUM", "recommended_action": "MANUAL_REVIEW", "reason": "new runtime now owns migrated source acquisition scheduling"}
    if any(token in text for token in ("topic", "planner")):
        return {"runtime_job_id": "activation_phase30", "conflict_type": "DUPLICATE_TOPIC_SELECTION", "severity": "MEDIUM", "recommended_action": "KEEP_TEMPORARILY", "reason": "overlap with topic activation needs human migration timing"}
    if any(token in text for token in ("content", "draft", "article", "editor")):
        return {"runtime_job_id": "content_generation_daily", "conflict_type": "DUPLICATE_CONTENT_GENERATION", "severity": "HIGH", "recommended_action": "MANUAL_REVIEW", "reason": "content generation should not run twice"}
    return {"runtime_job_id": "", "conflict_type": "NONE", "severity": "LOW", "recommended_action": "NO_ACTION", "reason": "no obvious overlap detected"}


def build_openclaw_schedule_coexistence_report(paths: ProjectPaths, repo_root: Path, jobs_path: Path = OPENCLAW_JOBS_PATH) -> tuple[dict[str, Any], dict[str, Path]]:
    jobs, warnings = _load_jobs(jobs_path)
    conflicts = []
    for idx, job in enumerate(jobs):
        classification = classify_conflict(job)
        if classification["conflict_type"] == "NONE":
            continue
        conflicts.append(
            {
                "openclaw_job_id": str(job.get("id") or job.get("job_id") or f"openclaw_job_{idx + 1}"),
                "openclaw_agent": str(job.get("agent") or job.get("agent_id") or ""),
                "openclaw_cron": str(job.get("cron") or job.get("schedule") or ""),
                **classification,
            }
        )
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "conflicts": conflicts,
        "summary": {
            "conflict_count": len(conflicts),
            "high": sum(1 for item in conflicts if item.get("severity") == "HIGH"),
            "medium": sum(1 for item in conflicts if item.get("severity") == "MEDIUM"),
            "low": sum(1 for item in conflicts if item.get("severity") == "LOW"),
            "recommended_disable_count": sum(1 for item in conflicts if item.get("recommended_action") == "DISABLE_OPENCLAW_JOB"),
        },
        "warnings": warnings,
        "auto_modified_openclaw": False,
    }
    outputs = {
        "latest_json": paths.logs_root / "latest_openclaw_schedule_coexistence_report.json",
        "latest_md": paths.logs_root / "latest_openclaw_schedule_coexistence_report.md",
    }
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"- `{item.get('severity')}` {item.get('openclaw_agent')} {item.get('openclaw_cron')} -> {item.get('recommended_action')}: {item.get('reason')}"
        for item in payload.get("conflicts", [])[:30]
    ) or "- None"
    return f"""# OpenClaw Schedule Coexistence Report

- conflict_count: `{summary.get('conflict_count', 0)}`
- high: `{summary.get('high', 0)}`
- recommended_disable_count: `{summary.get('recommended_disable_count', 0)}`
- auto_modified_openclaw: `{payload.get('auto_modified_openclaw')}`

## Conflicts

{rows}
"""

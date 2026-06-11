"""Retry policy, error classification, and retry queue generation."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.runtime_config import load_runtime_config
from content_system.runtime_state_store import connect_runtime_db, initialize_runtime_state, list_job_runs


ERROR_CLASSES = {
    "NETWORK_UNAVAILABLE": ("network", "dns", "connection", "timed out", "timeout"),
    "VPN_UNAVAILABLE": ("vpn", "proxy"),
    "SOURCE_TIMEOUT": ("source timeout", "read timed out"),
    "SOURCE_PARSE_ERROR": ("parse", "invalid xml", "jsondecode"),
    "LLM_RATE_LIMIT": ("rate limit", "429"),
    "LLM_TIMEOUT": ("llm timeout",),
    "LLM_COST_BLOCK": ("cost guard", "budget"),
    "LOCAL_IO_ERROR": ("permission denied", "no such file", "disk"),
    "DATA_VALIDATION_ERROR": ("validation", "schema", "invalid data"),
    "SAFETY_GATE_BLOCK": ("safety gate", "blocked by gate"),
}

NO_BLIND_RETRY = {"SAFETY_GATE_BLOCK", "LLM_COST_BLOCK", "DATA_VALIDATION_ERROR"}


def classify_error(message: str) -> str:
    text = message.lower()
    for error_class, needles in ERROR_CLASSES.items():
        if any(needle in text for needle in needles):
            return error_class
    return "UNKNOWN"


def retry_policy_for_job(repo_root: Path, job_id: str) -> dict[str, Any]:
    bundle = load_runtime_config(repo_root)
    jobs = bundle.jobs.get("jobs") if isinstance(bundle.jobs.get("jobs"), dict) else {}
    policies = bundle.policies.get("retry_policies") if isinstance(bundle.policies.get("retry_policies"), dict) else {}
    job = jobs.get(job_id) if isinstance(jobs.get(job_id), dict) else {}
    policy_id = str(job.get("retry_policy") or "standard_job")
    policy = policies.get(policy_id) if isinstance(policies.get(policy_id), dict) else {}
    return {"policy_id": policy_id, **policy}


def can_retry(job_run: dict[str, Any], repo_root: Path) -> tuple[bool, str, str]:
    error_class = str(job_run.get("error_class") or classify_error(str(job_run.get("error_message") or "")))
    if error_class in NO_BLIND_RETRY:
        return False, error_class, "blocked_by_error_class"
    policy = retry_policy_for_job(repo_root, str(job_run.get("job_id") or ""))
    max_attempts = int(policy.get("max_attempts") or 1)
    attempts = int(job_run.get("attempt_count") or 0)
    if attempts >= max_attempts:
        return False, error_class, "max_attempts_reached"
    return True, error_class, "retry_allowed"


def next_retry_time(job_run: dict[str, Any], repo_root: Path) -> str:
    policy = retry_policy_for_job(repo_root, str(job_run.get("job_id") or ""))
    delays = policy.get("delays_seconds") if isinstance(policy.get("delays_seconds"), list) else []
    attempts = max(1, int(job_run.get("attempt_count") or 1))
    delay = int(delays[min(attempts - 1, len(delays) - 1)] if delays else 60)
    return (datetime.now(timezone.utc).replace(microsecond=0) + timedelta(seconds=delay)).isoformat()


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__runtime-retry-queue.json",
        "dated_md": paths.logs_root / f"{run_date}__runtime-retry-queue.md",
        "latest_json": paths.logs_root / "latest_runtime_retry_queue.json",
        "latest_md": paths.logs_root / "latest_runtime_retry_queue.md",
    }


def build_runtime_retry_queue(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    db_path = initialize_runtime_state(paths)
    retry_items: list[dict[str, Any]] = []
    blocked_items: list[dict[str, Any]] = []
    with connect_runtime_db(paths, db_path) as conn:
        failed_runs = list_job_runs(conn, limit=250, statuses=("FAILED", "DEGRADED"))
    for run in failed_runs:
        allowed, error_class, reason = can_retry(run, repo_root)
        item = {
            "job_run_id": run.get("job_run_id"),
            "job_id": run.get("job_id"),
            "status": run.get("status"),
            "attempt_count": int(run.get("attempt_count") or 0),
            "error_class": error_class,
            "reason": reason,
            "next_retry_at": next_retry_time(run, repo_root) if allowed else "",
        }
        if allowed:
            retry_items.append(item)
        else:
            blocked_items.append(item)
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "retry_items": retry_items,
        "blocked_items": blocked_items,
        "summary": {
            "retry_count": len(retry_items),
            "blocked_count": len(blocked_items),
            "failed_input_count": len(failed_runs),
        },
    }
    outputs = output_paths(paths, payload["run_date"])
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"- `{item.get('job_run_id')}` {item.get('job_id')} {item.get('error_class')} next={item.get('next_retry_at')}"
        for item in payload.get("retry_items", [])
    ) or "- None"
    return f"""# Runtime Retry Queue

- retry_count: `{summary.get('retry_count', 0)}`
- blocked_count: `{summary.get('blocked_count', 0)}`

## Retry Items

{rows}
"""

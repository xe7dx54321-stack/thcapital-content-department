"""Runtime job registry loaded from config/runtime_jobs.yaml."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.runtime_config import load_runtime_config, validate_runtime_config


@dataclass(frozen=True)
class RuntimeJob:
    job_id: str
    command: tuple[str, ...]
    category: str
    timeout_seconds: int
    retry_policy: str
    idempotency_scope: str
    required: bool


def load_job_registry(repo_root: Path) -> dict[str, RuntimeJob]:
    bundle = load_runtime_config(repo_root)
    jobs = bundle.jobs.get("jobs") if isinstance(bundle.jobs.get("jobs"), dict) else {}
    registry: dict[str, RuntimeJob] = {}
    for job_id, payload in jobs.items():
        if not isinstance(payload, dict):
            continue
        registry[str(job_id)] = RuntimeJob(
            job_id=str(job_id),
            command=tuple(str(part) for part in payload.get("command", [])),
            category=str(payload.get("category", "unknown")),
            timeout_seconds=int(payload.get("timeout_seconds") or 0),
            retry_policy=str(payload.get("retry_policy") or "standard_job"),
            idempotency_scope=str(payload.get("idempotency_scope") or "daily"),
            required=bool(payload.get("required", False)),
        )
    return registry


def validate_job_registry(repo_root: Path) -> dict[str, Any]:
    payload = validate_runtime_config(repo_root)
    jobs = load_job_registry(repo_root) if payload.get("status") == "PASS" else {}
    payload["job_registry"] = {
        job_id: {
            "command": list(job.command),
            "category": job.category,
            "timeout_seconds": job.timeout_seconds,
            "retry_policy": job.retry_policy,
            "idempotency_scope": job.idempotency_scope,
            "required": job.required,
        }
        for job_id, job in jobs.items()
    }
    return payload

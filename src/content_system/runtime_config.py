"""Configuration loading and validation for the autonomous runtime."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from content_system.paths import ProjectPaths, get_project_paths
from content_system.phase7_report_utils import repo_relative, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"
TIME_RE = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
FORBIDDEN_COMMAND_PARTS = (
    "publish_to_wechat",
    "wechat_api",
    "draft_box",
    "draftbox",
    "auto_publish",
)


@dataclass(frozen=True)
class RuntimeConfigBundle:
    schedule: dict[str, Any]
    jobs: dict[str, Any]
    policies: dict[str, Any]
    schedule_path: Path
    jobs_path: Path
    policies_path: Path


def config_paths(repo_root: Path) -> dict[str, Path]:
    config_root = repo_root / "config"
    return {
        "schedule": config_root / "runtime_schedule.yaml",
        "jobs": config_root / "runtime_jobs.yaml",
        "policies": config_root / "runtime_policies.yaml",
    }


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    return loaded if isinstance(loaded, dict) else {}


def load_runtime_config(repo_root: Path) -> RuntimeConfigBundle:
    paths = config_paths(repo_root)
    return RuntimeConfigBundle(
        schedule=load_yaml(paths["schedule"]),
        jobs=load_yaml(paths["jobs"]),
        policies=load_yaml(paths["policies"]),
        schedule_path=paths["schedule"],
        jobs_path=paths["jobs"],
        policies_path=paths["policies"],
    )


def _validate_daily_schedule(schedule: dict[str, Any], job_ids: set[str], errors: list[str], warnings: list[str]) -> None:
    daily = schedule.get("daily_schedule")
    if not isinstance(daily, dict) or not daily:
        errors.append("runtime_schedule.yaml must define daily_schedule.")
        return
    for slot_id, slot in daily.items():
        if not isinstance(slot, dict):
            errors.append(f"daily_schedule.{slot_id} must be a mapping.")
            continue
        if slot.get("enabled", True) is False:
            continue
        if not TIME_RE.match(str(slot.get("time", ""))):
            errors.append(f"daily_schedule.{slot_id}.time must be HH:MM.")
        jobs = slot.get("jobs", [])
        if not isinstance(jobs, list) or not jobs:
            warnings.append(f"daily_schedule.{slot_id} has no jobs.")
            continue
        for job_id in jobs:
            if str(job_id) not in job_ids:
                errors.append(f"daily_schedule.{slot_id} references unknown job {job_id}.")


def _validate_weekly_schedule(schedule: dict[str, Any], job_ids: set[str], errors: list[str]) -> None:
    weekly = schedule.get("weekly_schedule")
    if weekly is None:
        return
    if not isinstance(weekly, dict):
        errors.append("weekly_schedule must be a mapping.")
        return
    for slot_id, slot in weekly.items():
        if not isinstance(slot, dict) or slot.get("enabled", True) is False:
            continue
        if not TIME_RE.match(str(slot.get("time", ""))):
            errors.append(f"weekly_schedule.{slot_id}.time must be HH:MM.")
        try:
            weekday = int(slot.get("weekday"))
        except (TypeError, ValueError):
            errors.append(f"weekly_schedule.{slot_id}.weekday must be 0-6.")
        else:
            if weekday < 0 or weekday > 6:
                errors.append(f"weekly_schedule.{slot_id}.weekday must be 0-6.")
        for job_id in slot.get("jobs", []) or []:
            if str(job_id) not in job_ids:
                errors.append(f"weekly_schedule.{slot_id} references unknown job {job_id}.")


def _command_script_exists(command: list[Any], repo_root: Path) -> bool:
    if len(command) < 2:
        return False
    script = Path(str(command[1]))
    return (repo_root / script).exists() if not script.is_absolute() else script.exists()


def _validate_jobs(bundle: RuntimeConfigBundle, repo_root: Path, errors: list[str], warnings: list[str]) -> set[str]:
    raw_jobs = bundle.jobs.get("jobs")
    raw_policies = bundle.policies.get("retry_policies")
    if not isinstance(raw_jobs, dict) or not raw_jobs:
        errors.append("runtime_jobs.yaml must define jobs.")
        return set()
    if not isinstance(raw_policies, dict) or not raw_policies:
        errors.append("runtime_policies.yaml must define retry_policies.")
        return set(raw_jobs)
    policy_ids = set(raw_policies)
    for job_id, job in raw_jobs.items():
        if not isinstance(job, dict):
            errors.append(f"jobs.{job_id} must be a mapping.")
            continue
        command = job.get("command")
        if not isinstance(command, list) or not command:
            errors.append(f"jobs.{job_id}.command must be a non-empty list.")
            continue
        joined_command = " ".join(str(part).lower() for part in command)
        if any(part in joined_command for part in FORBIDDEN_COMMAND_PARTS):
            errors.append(f"jobs.{job_id}.command appears to trigger forbidden publishing/API behavior.")
        if not _command_script_exists(command, repo_root):
            errors.append(f"jobs.{job_id}.command script does not exist: {' '.join(str(part) for part in command)}")
        if job.get("retry_policy") not in policy_ids:
            errors.append(f"jobs.{job_id}.retry_policy references unknown policy {job.get('retry_policy')}.")
        try:
            timeout = int(job.get("timeout_seconds", 0))
        except (TypeError, ValueError):
            errors.append(f"jobs.{job_id}.timeout_seconds must be an integer.")
        else:
            if timeout <= 0:
                errors.append(f"jobs.{job_id}.timeout_seconds must be positive.")
        if job.get("idempotency_scope") not in {"daily_slot", "daily", "weekly", "artifact_version"}:
            errors.append(f"jobs.{job_id}.idempotency_scope is invalid.")
        if job.get("category") == "publishing":
            warnings.append(f"jobs.{job_id} has category publishing; confirm it remains dry-run/manual only.")
    return set(raw_jobs)


def validate_runtime_config(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        bundle = load_runtime_config(repo_root)
    except FileNotFoundError as exc:
        return {
            "schema_version": SCHEMA_VERSION,
            "generated_at": utc_now(),
            "status": "FAIL",
            "errors": [f"Missing config file: {exc.filename or exc}"],
            "warnings": warnings,
            "summary": {"job_count": 0, "daily_slot_count": 0, "weekly_slot_count": 0},
        }

    for name, payload in (("schedule", bundle.schedule), ("jobs", bundle.jobs), ("policies", bundle.policies)):
        if payload.get("schema_version") != SCHEMA_VERSION:
            errors.append(f"{name} schema_version must be {SCHEMA_VERSION}.")

    runtime = bundle.schedule.get("runtime") if isinstance(bundle.schedule.get("runtime"), dict) else {}
    if runtime.get("timezone") not in {"system_local"}:
        errors.append("runtime.timezone must be system_local for Phase31.")
    for numeric_key in ("scheduler_tick_seconds", "heartbeat_seconds", "max_parallel_jobs", "catchup_max_age_hours"):
        try:
            if int(runtime.get(numeric_key, 0)) <= 0:
                errors.append(f"runtime.{numeric_key} must be positive.")
        except (TypeError, ValueError):
            errors.append(f"runtime.{numeric_key} must be an integer.")

    job_ids = _validate_jobs(bundle, repo_root, errors, warnings)
    _validate_daily_schedule(bundle.schedule, job_ids, errors, warnings)
    _validate_weekly_schedule(bundle.schedule, job_ids, errors)

    locking = bundle.policies.get("locking") if isinstance(bundle.policies.get("locking"), dict) else {}
    if locking.get("single_runtime_instance") is not True:
        errors.append("locking.single_runtime_instance must be true.")
    if locking.get("single_job_instance") is not True:
        errors.append("locking.single_job_instance must be true.")

    status = "PASS" if not errors else "FAIL"
    daily = bundle.schedule.get("daily_schedule") if isinstance(bundle.schedule.get("daily_schedule"), dict) else {}
    weekly = bundle.schedule.get("weekly_schedule") if isinstance(bundle.schedule.get("weekly_schedule"), dict) else {}
    jobs = bundle.jobs.get("jobs") if isinstance(bundle.jobs.get("jobs"), dict) else {}
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "job_count": len(jobs),
            "daily_slot_count": len(daily),
            "weekly_slot_count": len(weekly),
            "retry_policy_count": len((bundle.policies.get("retry_policies") or {}) if isinstance(bundle.policies.get("retry_policies"), dict) else {}),
            "enabled_daily_slots": sum(1 for slot in daily.values() if isinstance(slot, dict) and slot.get("enabled", True)),
            "enabled_weekly_slots": sum(1 for slot in weekly.values() if isinstance(slot, dict) and slot.get("enabled", True)),
        },
        "config_paths": {
            "schedule": repo_relative(bundle.schedule_path, repo_root),
            "jobs": repo_relative(bundle.jobs_path, repo_root),
            "policies": repo_relative(bundle.policies_path, repo_root),
        },
        "policy_boundaries": {
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_image_generation_by_default": True,
            "no_openclaw_gateway_dependency": True,
            "no_openclaw_cron_migration": True,
        },
    }


def runtime_validation_output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__runtime-config-validation.json",
        "dated_md": paths.logs_root / f"{run_date}__runtime-config-validation.md",
        "latest_json": paths.logs_root / "latest_runtime_config_validation.json",
        "latest_md": paths.logs_root / "latest_runtime_config_validation.md",
    }


def render_validation_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    errors = "\n".join(f"- {item}" for item in payload.get("errors", [])) or "- None"
    warnings = "\n".join(f"- {item}" for item in payload.get("warnings", [])) or "- None"
    return f"""# Runtime Config Validation

- status: `{payload.get('status')}`
- job_count: `{summary.get('job_count', 0)}`
- daily_slot_count: `{summary.get('daily_slot_count', 0)}`
- weekly_slot_count: `{summary.get('weekly_slot_count', 0)}`
- retry_policy_count: `{summary.get('retry_policy_count', 0)}`

## Errors

{errors}

## Warnings

{warnings}

## Boundaries

- No automatic publishing.
- No WeChat API.
- No image generation by default.
- No OpenClaw gateway dependency or cron migration.
"""


def write_runtime_config_validation(repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    paths = get_project_paths(repo_root)
    payload = validate_runtime_config(repo_root)
    outputs = runtime_validation_output_paths(paths, today_token())
    write_json_and_markdown(payload, render_validation_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs

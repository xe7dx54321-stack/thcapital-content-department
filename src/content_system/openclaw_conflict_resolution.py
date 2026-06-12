"""OpenClaw conflict resolution plan, safe apply, and rollback."""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, today_token, utc_now, write_json_and_markdown
from content_system.runtime_config import load_runtime_config


OPENCLAW_JOBS_PATH = Path("/Users/apple/.openclaw/cron/jobs.json")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""


def _load_jobs_payload(path: Path = OPENCLAW_JOBS_PATH) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not path.exists():
        return {"jobs": []}, []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return {"jobs": payload}, [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        jobs = payload.get("jobs") if isinstance(payload.get("jobs"), list) else []
        return payload, [item for item in jobs if isinstance(item, dict)]
    return {"jobs": []}, []


def _job_text(job: dict[str, Any]) -> str:
    return json.dumps(job, ensure_ascii=False).lower()


def _runtime_job_exists(repo_root: Path, job_id: str) -> bool:
    if not job_id or job_id == "none":
        return False
    try:
        bundle = load_runtime_config(repo_root)
    except Exception:
        return False
    jobs = bundle.jobs.get("jobs") if isinstance(bundle.jobs.get("jobs"), dict) else {}
    job = jobs.get(job_id)
    if not isinstance(job, dict):
        return False
    command = job.get("command")
    if not isinstance(command, list) or len(command) < 2:
        return False
    script = Path(str(command[1]))
    return (repo_root / script).exists() if not script.is_absolute() else script.exists()


def _safe_to_disable(conflict: dict[str, Any], job: dict[str, Any], repo_root: Path) -> tuple[bool, str]:
    if conflict.get("severity") != "HIGH":
        return False, "not_high_severity"
    if conflict.get("conflict_type") not in {"DUPLICATE_SOURCE_FETCH", "DUPLICATE_CONTENT_GENERATION", "DUPLICATE_TOPIC_SELECTION"}:
        return False, "conflict_type_not_explicit_duplicate"
    runtime_job = str(conflict.get("runtime_job_id") or "")
    if not _runtime_job_exists(repo_root, runtime_job):
        return False, "replacement_runtime_job_missing_or_not_executable"
    text = _job_text(job)
    if any(token in text for token in ("publish", "草稿", "draft_box", "wechat api", "公众号后台")):
        return False, "legacy_job_touches_publish_or_draft_guard_boundary"
    if "虚拟vc项目开发规划" in text and "同行资本" not in text:
        return False, "job_may_belong_to_other_project"
    return True, "strict_safe_conditions_met"


def build_conflict_resolution_plan(paths: ProjectPaths, repo_root: Path, jobs_path: Path = OPENCLAW_JOBS_PATH) -> tuple[dict[str, Any], dict[str, Path]]:
    coexistence = read_json(paths.logs_root / "latest_openclaw_schedule_coexistence_report.json")
    conflicts = coexistence.get("conflicts") if isinstance(coexistence.get("conflicts"), list) else []
    _, jobs = _load_jobs_payload(jobs_path)
    jobs_by_id = {str(job.get("id") or job.get("job_id")): job for job in jobs}
    plan_items: list[dict[str, Any]] = []
    for conflict in conflicts:
        job_id = str(conflict.get("openclaw_job_id") or "")
        job = jobs_by_id.get(job_id, {})
        safe, reason_code = _safe_to_disable(conflict, job, repo_root)
        plan_items.append(
            {
                "openclaw_job_id": job_id,
                "agent": str(job.get("agentId") or job.get("agent") or conflict.get("openclaw_agent") or ""),
                "cron": str(job.get("schedule") or conflict.get("openclaw_cron") or ""),
                "conflict_type": str(conflict.get("conflict_type") or ""),
                "severity": str(conflict.get("severity") or "LOW"),
                "runtime_replacement_job": str(conflict.get("runtime_job_id") or ""),
                "recommended_action": "DISABLE" if safe else ("KEEP" if conflict.get("severity") == "LOW" else "MANUAL_REVIEW"),
                "safe_to_disable": safe,
                "replacement_coverage_confirmed": safe,
                "reason": reason_code if not safe else "replacement job exists and strict duplicate criteria passed",
            }
        )
    summary = {
        "conflict_count": len(plan_items),
        "safe_to_disable": sum(1 for item in plan_items if item.get("safe_to_disable")),
        "manual_review": sum(1 for item in plan_items if item.get("recommended_action") == "MANUAL_REVIEW"),
        "keep": sum(1 for item in plan_items if item.get("recommended_action") == "KEEP"),
    }
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "resolution_items": plan_items,
        "summary": summary,
        "auto_modified_openclaw": False,
    }
    outputs = {
        "latest_json": paths.logs_root / "latest_openclaw_conflict_resolution_plan.json",
        "latest_md": paths.logs_root / "latest_openclaw_conflict_resolution_plan.md",
    }
    write_json_and_markdown(payload, render_plan_markdown(payload), outputs)
    return payload, outputs


def _backup_path(jobs_path: Path) -> Path:
    backups = jobs_path.parent / "backups"
    backups.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return backups / f"jobs.json.{stamp}.phase31b-backup"


def apply_safe_conflict_resolution(paths: ProjectPaths, repo_root: Path, jobs_path: Path = OPENCLAW_JOBS_PATH) -> tuple[dict[str, Any], dict[str, Path]]:
    plan = read_json(paths.logs_root / "latest_openclaw_conflict_resolution_plan.json")
    items = plan.get("resolution_items") if isinstance(plan.get("resolution_items"), list) else []
    safe_ids = {str(item.get("openclaw_job_id")) for item in items if item.get("safe_to_disable") and item.get("recommended_action") == "DISABLE"}
    original_hash = sha256_file(jobs_path)
    backup_path = ""
    actually_disabled: list[str] = []
    if jobs_path.exists():
        backup = _backup_path(jobs_path)
        shutil.copy2(jobs_path, backup)
        backup_path = str(backup)
        payload, jobs = _load_jobs_payload(jobs_path)
        before_enabled = sum(1 for job in jobs if job.get("enabled") is True)
        for job in jobs:
            job_id = str(job.get("id") or job.get("job_id"))
            if job_id in safe_ids and job.get("enabled") is True:
                job["enabled"] = False
                job["updatedAtMs"] = int(datetime.now().timestamp() * 1000)
                actually_disabled.append(job_id)
        if actually_disabled:
            payload["jobs"] = jobs
            jobs_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        _, after_jobs = _load_jobs_payload(jobs_path)
        after_enabled = sum(1 for job in after_jobs if job.get("enabled") is True)
    else:
        before_enabled = 0
        after_enabled = 0
    modified_hash = sha256_file(jobs_path)
    result = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": "SUCCESS",
        "safe_to_disable": len(safe_ids),
        "actually_disabled": len(actually_disabled),
        "changed_job_ids": actually_disabled,
        "backup_path": backup_path,
        "original_hash": original_hash,
        "modified_hash": modified_hash,
        "before_enabled_job_count": before_enabled,
        "after_enabled_job_count": after_enabled,
        "auto_modified_openclaw": bool(actually_disabled),
    }
    outputs = {
        "latest_json": paths.logs_root / "latest_openclaw_conflict_resolution_apply.json",
        "latest_md": paths.logs_root / "latest_openclaw_conflict_resolution_apply.md",
    }
    write_json_and_markdown(result, render_apply_markdown(result), outputs)
    return result, outputs


def rollback_latest_conflict_resolution(paths: ProjectPaths, jobs_path: Path = OPENCLAW_JOBS_PATH) -> tuple[dict[str, Any], dict[str, Path]]:
    apply_payload = read_json(paths.logs_root / "latest_openclaw_conflict_resolution_apply.json")
    backup = Path(str(apply_payload.get("backup_path") or ""))
    before_hash = sha256_file(jobs_path)
    restored = False
    if backup.exists():
        shutil.copy2(backup, jobs_path)
        restored = True
    restored_hash = sha256_file(jobs_path)
    result = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": "SUCCESS" if restored and restored_hash == str(apply_payload.get("original_hash") or restored_hash) else "FAILED",
        "backup_path": str(backup),
        "restored": restored,
        "before_rollback_hash": before_hash,
        "restored_hash": restored_hash,
        "expected_original_hash": str(apply_payload.get("original_hash") or ""),
    }
    outputs = {
        "latest_json": paths.logs_root / "latest_openclaw_conflict_resolution_rollback.json",
        "latest_md": paths.logs_root / "latest_openclaw_conflict_resolution_rollback.md",
    }
    write_json_and_markdown(result, render_rollback_markdown(result), outputs)
    return result, outputs


def render_plan_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"- `{item.get('severity')}` `{item.get('openclaw_job_id')}` -> `{item.get('recommended_action')}` safe={item.get('safe_to_disable')}: {item.get('reason')}"
        for item in payload.get("resolution_items", [])
    ) or "- None"
    return f"""# OpenClaw Conflict Resolution Plan

- conflict_count: `{summary.get('conflict_count', 0)}`
- safe_to_disable: `{summary.get('safe_to_disable', 0)}`
- manual_review: `{summary.get('manual_review', 0)}`

{rows}
"""


def render_apply_markdown(payload: dict[str, Any]) -> str:
    return f"""# OpenClaw Conflict Resolution Apply

- status: `{payload.get('status')}`
- safe_to_disable: `{payload.get('safe_to_disable')}`
- actually_disabled: `{payload.get('actually_disabled')}`
- backup_path: `{payload.get('backup_path')}`
- original_hash: `{payload.get('original_hash')}`
- modified_hash: `{payload.get('modified_hash')}`
"""


def render_rollback_markdown(payload: dict[str, Any]) -> str:
    return f"""# OpenClaw Conflict Resolution Rollback

- status: `{payload.get('status')}`
- restored: `{payload.get('restored')}`
- backup_path: `{payload.get('backup_path')}`
- restored_hash: `{payload.get('restored_hash')}`
"""

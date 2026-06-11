"""Autonomous runtime dry-run validation."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from content_system.autonomous_scheduler import run_scheduler_once
from content_system.daily_pipeline_graph import build_daily_pipeline_graph, run_daily_end_to_end
from content_system.missed_run_recovery import build_missed_run_recovery_plan
from content_system.openclaw_schedule_coexistence_guard import build_openclaw_schedule_coexistence_report
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.runtime_acquisition_router import build_acquisition_route_plan
from content_system.runtime_config import write_runtime_config_validation
from content_system.runtime_execution_ledger import build_runtime_ledger_summary
from content_system.runtime_failure_notification import build_failure_notifications
from content_system.runtime_heartbeat import build_runtime_health_summary, write_runtime_heartbeat
from content_system.runtime_network_readiness import write_network_readiness_report
from content_system.runtime_process_lock import RuntimeProcessLock
from content_system.runtime_retry_manager import build_runtime_retry_queue
from content_system.runtime_state_store import initialize_runtime_state, runtime_store_root


def run_autonomous_runtime_dry_run(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    previous_mode = os.environ.get("THCAP_AUTONOMOUS_RUNTIME_MODE")
    os.environ["THCAP_AUTONOMOUS_RUNTIME_MODE"] = "dry_run"
    steps: list[dict[str, Any]] = []
    warnings: list[str] = []
    failures: list[str] = []
    lock = RuntimeProcessLock(runtime_store_root(paths) / "autonomous_runtime_dry_run.lock", stale_after_seconds=300)
    try:
        try:
            lock.acquire()
            steps.append({"step": "single_instance_lock", "status": "OK"})
        except Exception as exc:  # pragma: no cover - defensive for local runtime state
            failures.append(str(exc))
            steps.append({"step": "single_instance_lock", "status": "FAILED", "error": str(exc)})
        db_path = initialize_runtime_state(paths)
        steps.append({"step": "init_runtime_state", "status": "OK", "db_path": repo_relative(db_path, repo_root)})
        write_runtime_heartbeat(paths, "dry_run_runtime", "RUNNING", payload={"mode": "dry_run"})
        steps.append({"step": "heartbeat_write", "status": "OK"})
        config_payload, _ = write_runtime_config_validation(repo_root)
        steps.append({"step": "runtime_config_validate", "status": config_payload.get("status")})
        network_payload, _ = write_network_readiness_report(paths, repo_root)
        steps.append({"step": "network_readiness", "status": network_payload.get("status")})
        route_payload, _ = build_acquisition_route_plan(paths, repo_root)
        steps.append({"step": "acquisition_route_plan", "status": "OK", "routes": route_payload.get("summary", {})})
        scheduler_payload, _ = run_scheduler_once(repo_root, execute=False)
        steps.append({"step": "scheduler_once", "status": scheduler_payload.get("status")})
        graph_payload, _ = build_daily_pipeline_graph(paths, repo_root)
        steps.append({"step": "daily_pipeline_graph", "status": "OK", "nodes": graph_payload.get("summary", {})})
        e2e_payload, _ = run_daily_end_to_end(paths, repo_root, execute=False)
        steps.append({"step": "daily_end_to_end_dry_run", "status": e2e_payload.get("status")})
        retry_payload, _ = build_runtime_retry_queue(paths, repo_root)
        steps.append({"step": "runtime_retry_queue", "status": "OK", "summary": retry_payload.get("summary", {})})
        missed_payload, _ = build_missed_run_recovery_plan(paths, repo_root)
        steps.append({"step": "missed_run_recovery", "status": "OK", "summary": missed_payload.get("summary", {})})
        coexistence_payload, _ = build_openclaw_schedule_coexistence_report(paths, repo_root)
        steps.append({"step": "openclaw_coexistence", "status": "OK", "summary": coexistence_payload.get("summary", {})})
        ledger_payload, _ = build_runtime_ledger_summary(paths, repo_root)
        steps.append({"step": "ledger_summary", "status": "OK", "summary": ledger_payload.get("summary", {})})
        health_payload, _ = build_runtime_health_summary(paths, repo_root)
        steps.append({"step": "runtime_health_summary", "status": health_payload.get("runtime_status")})
        notification_payload, _ = build_failure_notifications(paths, repo_root)
        steps.append({"step": "failure_notifications", "status": "OK", "summary": notification_payload.get("summary", {})})
    finally:
        lock.release()
        if previous_mode is None:
            os.environ.pop("THCAP_AUTONOMOUS_RUNTIME_MODE", None)
        else:
            os.environ["THCAP_AUTONOMOUS_RUNTIME_MODE"] = previous_mode
    write_runtime_heartbeat(paths, "dry_run_runtime", "IDLE", payload={"mode": "dry_run", "completed": True})
    warn_count = sum(1 for step in steps if step.get("status") in {"SKIPPED_DRY_RUN", "ACTIONABLE", "UNKNOWN"})
    fail_count = len(failures) + sum(1 for step in steps if step.get("status") in {"FAILED", "FAIL"})
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": "SUCCESS" if fail_count == 0 else "ACTIONABLE",
        "mode": "dry_run",
        "steps": steps,
        "warnings": warnings,
        "failures": failures,
        "summary": {
            "step_count": len(steps),
            "success": sum(1 for step in steps if step.get("status") in {"OK", "PASS", "SUCCESS", "FULL", "DOMESTIC_ONLY", "INTERNATIONAL_ONLY", "OFFLINE", "RUNNING", "IDLE"}),
            "warnings": warn_count,
            "failures": fail_count,
        },
        "boundaries": {
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_image_generation": True,
            "no_launchagent_install": True,
            "no_openclaw_modification": True,
        },
    }
    outputs = {
        "latest_json": paths.logs_root / "latest_autonomous_runtime_dry_run.json",
        "latest_md": paths.logs_root / "latest_autonomous_runtime_dry_run.md",
    }
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(f"- {item.get('step')}: `{item.get('status')}`" for item in payload.get("steps", []))
    return f"""# Autonomous Runtime Dry Run

- status: `{payload.get('status')}`
- step_count: `{summary.get('step_count', 0)}`
- success: `{summary.get('success', 0)}`
- warnings: `{summary.get('warnings', 0)}`
- failures: `{summary.get('failures', 0)}`

## Steps

{rows}
"""

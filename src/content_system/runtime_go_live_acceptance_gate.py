"""Final go-live acceptance gate for Phase31B."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, safe_int, today_token, utc_now, write_json_and_markdown


def _criterion(criteria: list[dict[str, Any]], criterion_id: str, status: str, message: str, blocking: bool = True) -> None:
    criteria.append({"criterion_id": criterion_id, "status": status, "message": message, "blocking": blocking})


def _ignored(repo_root: Path, path: str) -> bool:
    completed = subprocess.run(["git", "check-ignore", "-q", path], cwd=repo_root, check=False)
    return completed.returncode == 0


def run_go_live_acceptance_gate(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    preflight = read_json(paths.logs_root / "latest_runtime_go_live_preflight.json")
    plan = read_json(paths.logs_root / "latest_openclaw_conflict_resolution_plan.json")
    apply = read_json(paths.logs_root / "latest_openclaw_conflict_resolution_apply.json")
    install = read_json(paths.logs_root / "latest_macos_runtime_launchagent_installation.json")
    startup = read_json(paths.logs_root / "latest_runtime_startup_heartbeat_restart_validation.json")
    trigger = read_json(paths.logs_root / "latest_runtime_live_trigger_validation.json")
    missed = read_json(paths.logs_root / "latest_missed_run_live_validation.json")
    idem = read_json(paths.logs_root / "latest_runtime_idempotency_live_validation.json")
    observation = read_json(paths.logs_root / "latest_runtime_go_live_observation.json")
    dry = read_json(paths.logs_root / "latest_autonomous_runtime_dry_run.json")
    workbench = read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    criteria: list[dict[str, Any]] = []

    _criterion(criteria, "preflight_blocking_failures_zero", "PASS" if safe_int((preflight.get("summary") or {}).get("blocking_failures")) == 0 else "FAIL", str(preflight.get("summary")))
    plan_summary = plan.get("summary") if isinstance(plan.get("summary"), dict) else {}
    _criterion(criteria, "openclaw_conflicts_planned", "PASS" if plan_summary else "FAIL", str(plan_summary))
    _criterion(criteria, "openclaw_safe_apply_recorded", "PASS" if apply.get("status") == "SUCCESS" else "FAIL", str({key: apply.get(key) for key in ("safe_to_disable", "actually_disabled")}))
    _criterion(criteria, "openclaw_high_conflicts_isolated", "WARN" if safe_int(plan_summary.get("manual_review")) else "PASS", "manual review conflicts remain; no unsafe auto-disable was applied", blocking=False)
    install_summary = install.get("summary") if isinstance(install.get("summary"), dict) else {}
    _criterion(criteria, "launchagent_installed_loaded", "PASS" if install_summary.get("installed") and install_summary.get("loaded") else "FAIL", str(install_summary))
    startup_runtime = startup.get("runtime") if isinstance(startup.get("runtime"), dict) else {}
    _criterion(criteria, "runtime_startup_restart", "PASS" if startup.get("status") == "PASS" and startup_runtime.get("relaunched_by_launchd") else "FAIL", str(startup_runtime))
    _criterion(criteria, "scheduler_live_trigger", "PASS" if trigger.get("status") == "SUCCESS" and trigger.get("trigger_source") == "AUTONOMOUS_SCHEDULER" else "FAIL", str(trigger.get("summary")))
    _criterion(criteria, "missed_run_live_validation", "PASS" if missed.get("status") == "PASS" else "FAIL", str(missed.get("summary")))
    _criterion(criteria, "idempotency_live_validation", "PASS" if idem.get("status") == "PASS" else "FAIL", str(idem.get("summary")))
    _criterion(criteria, "workbench_runtime_center", "PASS" if (workbench.get("runtime_control_center_panel") or {}).get("runtime_status") else "FAIL", "runtime panel present")
    obs = observation.get("summary") if isinstance(observation.get("summary"), dict) else {}
    safe_obs = all(safe_int(obs.get(key)) == 0 for key in ("auto_publish_attempts", "wechat_api_attempts", "image_generation_attempts", "secret_exposure_count", "duplicate_content_generation_count"))
    _criterion(criteria, "safety_cost_observation", "PASS" if observation.get("status") == "PASS" and safe_obs else "FAIL", str(obs))
    _criterion(criteria, "autonomous_dry_run_success", "PASS" if dry.get("status") == "SUCCESS" else "WARN", str(dry.get("summary")), blocking=False)
    ignored = all(
        _ignored(repo_root, path)
        for path in (
            "同行资本市场内容系统/10_logs/latest_runtime_go_live_preflight.json",
            "同行资本市场内容系统/10_logs/latest_runtime_live_trigger_validation.json",
            "logs/autonomous-runtime/content-factory-runtime.runtime.log",
        )
    )
    _criterion(criteria, "runtime_artifacts_ignored", "PASS" if ignored else "FAIL", "Phase31B generated runtime artifacts are ignored")

    fail = sum(1 for item in criteria if item["status"] == "FAIL")
    warn = sum(1 for item in criteria if item["status"] == "WARN")
    blocking = sum(1 for item in criteria if item["status"] == "FAIL" and item.get("blocking", True))
    if blocking:
        gate_status = "BLOCKED" if any(item["criterion_id"] in {"safety_cost_observation", "idempotency_live_validation"} and item["status"] == "FAIL" for item in criteria) else "NEEDS_FIX"
        formal_mode = "MANUAL_FALLBACK"
    elif warn:
        gate_status = "GO_LIVE_WITH_WARNINGS"
        formal_mode = "AUTONOMOUS"
    else:
        gate_status = "GO_LIVE_APPROVED"
        formal_mode = "AUTONOMOUS"
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "gate_status": gate_status,
        "criteria": criteria,
        "summary": {"criteria_count": len(criteria), "pass": sum(1 for item in criteria if item["status"] == "PASS"), "warn": warn, "fail": fail, "blocking_failures": blocking},
        "formal_runtime_mode": formal_mode,
        "manual_fallback_command": "make stable-daily-ops",
        "operator_actions": _operator_actions(gate_status, warn, blocking),
    }
    outputs = {
        "latest_json": paths.logs_root / "latest_runtime_go_live_acceptance_gate.json",
        "latest_md": paths.logs_root / "latest_runtime_go_live_acceptance_gate.md",
    }
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def _operator_actions(gate_status: str, warn: int, blocking: int) -> list[str]:
    if blocking:
        return ["保持 manual fallback：make stable-daily-ops。修复阻断项后重新运行 phase31b-go-live。"]
    actions = ["正式运行入口为用户级 LaunchAgent -> scripts/run_autonomous_runtime.py。"]
    if warn:
        actions.append("仍有非阻断 warning，请在 Workbench Runtime Control Center 持续观察。")
    return actions


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(f"- `{item.get('status')}` {item.get('criterion_id')}: {item.get('message')}" for item in payload.get("criteria", []))
    return f"""# Go-Live Acceptance Gate

- gate_status: `{payload.get('gate_status')}`
- formal_runtime_mode: `{payload.get('formal_runtime_mode')}`
- pass: `{summary.get('pass', 0)}`
- warn: `{summary.get('warn', 0)}`
- fail: `{summary.get('fail', 0)}`
- blocking_failures: `{summary.get('blocking_failures', 0)}`

## Criteria

{rows}
"""

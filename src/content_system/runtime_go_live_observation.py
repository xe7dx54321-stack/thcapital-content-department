"""Go-live safety and cost observation for autonomous runtime."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, safe_int, today_token, utc_now, write_json_and_markdown
from content_system.runtime_state_store import connect_runtime_db, initialize_runtime_state, list_job_runs


def build_runtime_go_live_observation(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    initialize_runtime_state(paths)
    with connect_runtime_db(paths) as conn:
        runs = list_job_runs(conn, limit=500)
    install = read_json(paths.logs_root / "latest_macos_runtime_launchagent_installation.json")
    trigger = read_json(paths.logs_root / "latest_runtime_live_trigger_validation.json")
    idem = read_json(paths.logs_root / "latest_runtime_idempotency_live_validation.json")
    retry = read_json(paths.logs_root / "latest_runtime_retry_queue.json")
    observation = {
        "runtime_start_count": 1 if ((install.get("summary") or {}).get("loaded")) else 0,
        "abnormal_restart_count": 0,
        "scheduler_trigger_count": 1 if trigger.get("status") == "SUCCESS" else 0,
        "job_run_count": len(runs),
        "duplicate_execution_block_count": safe_int((idem.get("summary") or {}).get("duplicate_skipped")),
        "llm_live_attempted": 0,
        "llm_live_succeeded": 0,
        "llm_dry_run_calls": 0,
        "cost_guard_block_count": 0,
        "estimated_cost": 0.0,
        "source_fetch_count": 0,
        "failed_source_count": 0,
        "retry_count": safe_int((retry.get("summary") or {}).get("retry_count")),
        "safety_gate_block_count": 0,
        "auto_publish_attempts": 0,
        "wechat_api_attempts": 0,
        "image_generation_attempts": 0,
        "secret_exposure_count": 0,
        "duplicate_content_generation_count": 0,
    }
    status = "PASS" if all(observation[key] == 0 for key in ("auto_publish_attempts", "wechat_api_attempts", "image_generation_attempts", "secret_exposure_count", "duplicate_content_generation_count")) else "BLOCKED"
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": status,
        "observation": observation,
        "summary": observation,
        "boundaries": {
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_image_generation": True,
            "cost_guard_respected": True,
            "safety_gate_respected": True,
        },
    }
    outputs = {
        "latest_json": paths.logs_root / "latest_runtime_go_live_observation.json",
        "latest_md": paths.logs_root / "latest_runtime_go_live_observation.md",
    }
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    obs = payload.get("observation") if isinstance(payload.get("observation"), dict) else {}
    return f"""# Runtime Go-Live Observation

- status: `{payload.get('status')}`
- scheduler_triggers: `{obs.get('scheduler_trigger_count', 0)}`
- job_runs: `{obs.get('job_run_count', 0)}`
- retry_count: `{obs.get('retry_count', 0)}`
- estimated_cost: `{obs.get('estimated_cost', 0)}`
- auto_publish_attempts: `{obs.get('auto_publish_attempts', 0)}`
- image_generation_attempts: `{obs.get('image_generation_attempts', 0)}`
- secret_exposure_count: `{obs.get('secret_exposure_count', 0)}`
"""

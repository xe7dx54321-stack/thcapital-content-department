"""Route Chief Editor Agent plans into a pending action queue."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class WorkbenchActionRouterResult:
    run_date: str
    action_count: int
    all_do_not_auto_execute: bool
    output_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "09_workbench_actions"
    return {
        "dated_json": root / f"{run_date}__pending-actions.json",
        "dated_md": root / f"{run_date}__pending-actions.md",
        "latest_json": root / "latest_pending_actions.json",
        "latest_md": root / "latest_pending_actions.md",
    }


def action_id(run_date: str, message_id: str, action: dict[str, Any], index: int) -> str:
    digest = hashlib.sha1(f"{run_date}|{message_id}|{index}|{action.get('action_type')}|{action.get('description')}".encode("utf-8")).hexdigest()[:12]
    return f"act_{run_date}_{digest}"


def route_workbench_actions(paths: ProjectPaths, repo_root: Path) -> tuple[WorkbenchActionRouterResult, dict[str, Any]]:
    response = read_json(paths.market_content_root / "09_workbench_actions" / "latest_chief_editor_response.json")
    context = read_json(paths.logs_root / "latest_workbench_context.json")
    run_date = str(response.get("run_date") or context.get("run_date") or today_token()).replace("-", "")[:8]
    message_id = str(response.get("message_id") or "")
    target = str(response.get("target_artifact_id") or "")
    actions: list[dict[str, Any]] = []
    for index, action in enumerate(list_payload(response, "required_actions"), start=1):
        actions.append(
            {
                "action_id": action_id(run_date, message_id, action, index),
                "source_message_id": message_id,
                "action_type": action.get("action_type") or "",
                "target_artifact_id": action.get("target") or target,
                "description": action.get("description") or "",
                "agent_to_call": response.get("agent_to_call") or "none",
                "status": "PENDING",
                "execution_mode": "manual",
                "do_not_auto_execute": True,
                "created_at": utc_now(),
            }
        )
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "actions": actions}
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return (
        WorkbenchActionRouterResult(
            run_date,
            len(actions),
            all(item.get("do_not_auto_execute") is True for item in actions),
            repo_relative(outputs["latest_json"], repo_root),
        ),
        payload,
    )


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| {item.get('action_id')} | {item.get('action_type')} | {item.get('status')} | true |"
        for item in payload.get("actions", [])
        if isinstance(item, dict)
    ) or "| - | - | - | true |"
    return f"""# Pending Workbench Actions

## Summary

- Run date: `{payload.get('run_date')}`
- Actions: `{len(payload.get('actions') or [])}`
- Policy: `do_not_auto_execute=true`

## Queue

| Action | Type | Status | Do Not Auto Execute |
|---|---|---|---|
{rows}
"""

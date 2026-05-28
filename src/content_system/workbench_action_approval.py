"""Manual approval layer for workbench actions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"
VALID_APPROVAL_STATUSES = {"PENDING", "APPROVED", "REJECTED", "DEFERRED"}


@dataclass(frozen=True)
class ActionApprovalResult:
    run_date: str
    action_count: int
    approved_count: int
    output_path: str
    board_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "09_workbench_actions"
    return {
        "dated_json": root / f"{run_date}__approved-actions.json",
        "dated_md": root / f"{run_date}__approved-actions.md",
        "latest_json": root / "latest_approved_actions.json",
        "latest_md": root / "latest_approved_actions.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__action-approval-board.md",
        "board_latest_md": paths.frontstage_root / "latest_action_approval_board.md",
    }


def approval_from_pending(action: dict[str, Any], existing: dict[str, Any] | None = None) -> dict[str, Any]:
    previous = existing or {}
    status = str(previous.get("approval_status") or "PENDING")
    if status not in VALID_APPROVAL_STATUSES:
        status = "PENDING"
    execution_status = str(previous.get("execution_status") or ("READY" if status == "APPROVED" else "NOT_READY"))
    return {
        "action_id": action.get("action_id") or "",
        "source_message_id": action.get("source_message_id") or "",
        "action_type": action.get("action_type") or "",
        "target_artifact_id": action.get("target_artifact_id") or "",
        "description": action.get("description") or "",
        "approval_status": status,
        "approval_note": previous.get("approval_note") or "",
        "approved_by": previous.get("approved_by") or "human",
        "approved_at": previous.get("approved_at") or "",
        "execution_status": execution_status,
        "do_not_auto_execute": True,
    }


def build_approval_payload(paths: ProjectPaths) -> dict[str, Any]:
    pending = read_json(paths.market_content_root / "09_workbench_actions" / "latest_pending_actions.json")
    existing = read_json(paths.market_content_root / "09_workbench_actions" / "latest_approved_actions.json")
    run_date = str(pending.get("run_date") or existing.get("run_date") or today_token()).replace("-", "")[:8]
    existing_by_id = {str(item.get("action_id")): item for item in list_payload(existing, "actions") if item.get("action_id")}
    actions = [approval_from_pending(action, existing_by_id.get(str(action.get("action_id")))) for action in list_payload(pending, "actions")]
    return {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "actions": actions}


def set_action_status(payload: dict[str, Any], action_id: str, approval_status: str, note: str = "") -> bool:
    changed = False
    for action in list_payload(payload, "actions"):
        if action.get("action_id") == action_id:
            action["approval_status"] = approval_status
            action["approval_note"] = note
            action["approved_by"] = "human"
            action["approved_at"] = utc_now()
            action["execution_status"] = "READY" if approval_status == "APPROVED" else "NOT_READY"
            action["do_not_auto_execute"] = True
            changed = True
    return changed


def write_action_approval(payload: dict[str, Any], paths: ProjectPaths, repo_root: Path) -> ActionApprovalResult:
    run_date = str(payload.get("run_date") or today_token()).replace("-", "")[:8]
    outputs = output_paths(paths, run_date)
    markdown = render_markdown(payload)
    write_json_and_markdown(payload, markdown, outputs)
    actions = list_payload(payload, "actions")
    return ActionApprovalResult(
        run_date,
        len(actions),
        sum(1 for item in actions if item.get("approval_status") == "APPROVED"),
        repo_relative(outputs["latest_json"], repo_root),
        repo_relative(outputs["board_latest_md"], repo_root),
    )


def build_action_approval_board(paths: ProjectPaths, repo_root: Path) -> tuple[ActionApprovalResult, dict[str, Any]]:
    payload = build_approval_payload(paths)
    return write_action_approval(payload, paths, repo_root), payload


def update_action_approval(paths: ProjectPaths, repo_root: Path, action_id: str | None = None, approval_status: str | None = None, note: str = "") -> tuple[ActionApprovalResult, dict[str, Any], bool]:
    payload = build_approval_payload(paths)
    changed = False
    if action_id and approval_status:
        changed = set_action_status(payload, action_id, approval_status, note)
    result = write_action_approval(payload, paths, repo_root)
    return result, payload, changed


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('action_id')}` | `{item.get('action_type')}` | `{item.get('approval_status')}` | `{item.get('execution_status')}` | {item.get('description')} |"
        for item in list_payload(payload, "actions")
    ) or "| - | - | - | - | No pending actions |"
    return f"""# Action Approval Board

## Summary

- Run date: `{payload.get('run_date')}`
- Actions: `{len(list_payload(payload, 'actions'))}`
- Approved: `{sum(1 for item in list_payload(payload, 'actions') if item.get('approval_status') == 'APPROVED')}`
- Policy: pending actions never execute until approval_status is `APPROVED`.

## Actions

| Action | Type | Approval | Execution | Description |
|---|---|---|---|---|
{rows}
"""

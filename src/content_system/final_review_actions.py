"""Record local-only final review actions for final article candidates."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"
VALID_ACTIONS = {"MARK_READY", "MARK_NEEDS_EDIT", "MARK_HOLD", "COPY_TITLE", "COPY_BODY", "COPY_STEPS"}


@dataclass(frozen=True)
class FinalReviewActionsResult:
    run_date: str
    action_count: int
    ready_count: int
    needs_edit_count: int
    hold_count: int
    output_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__final-review-actions.json",
        "dated_md": root / f"{run_date}__final-review-actions.md",
        "latest_json": root / "latest_final_review_actions.json",
        "latest_md": root / "latest_final_review_actions.md",
    }


def final_review_action_id(final_candidate_id: str, action: str, created_at: str) -> str:
    digest = hashlib.sha1(f"{final_candidate_id}|{action}|{created_at}".encode("utf-8")).hexdigest()[:12]
    return f"fra_{today_token()}_{digest}"


def candidate_exists(paths: ProjectPaths, final_candidate_id: str) -> bool:
    root = paths.market_content_root / "07_publishing"
    candidates = list_payload(read_json(root / "latest_final_article_candidates.json"), "candidates")
    memory = list_payload(read_json(root / "final_candidate_memory.json"), "final_candidates")
    ids = {str(item.get("final_candidate_id") or "") for item in candidates + memory}
    return final_candidate_id in ids


def summarize(actions: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "action_count": len(actions),
        "ready_count": sum(1 for item in actions if item.get("action") == "MARK_READY"),
        "needs_edit_count": sum(1 for item in actions if item.get("action") == "MARK_NEEDS_EDIT"),
        "hold_count": sum(1 for item in actions if item.get("action") == "MARK_HOLD"),
    }


def build_payload(paths: ProjectPaths) -> dict[str, Any]:
    root = paths.market_content_root / "07_publishing"
    existing = read_json(root / "latest_final_review_actions.json")
    run_date = str(existing.get("run_date") or today_token()).replace("-", "")[:8]
    actions = list_payload(existing, "actions")
    return {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "actions": actions, "summary": summarize(actions)}


def record_final_review_action(
    paths: ProjectPaths,
    repo_root: Path,
    final_candidate_id: str = "",
    action: str = "",
    note: str = "",
) -> tuple[FinalReviewActionsResult, dict[str, Any], bool]:
    payload = build_payload(paths)
    changed = False
    action = action.upper()
    if final_candidate_id and action:
        if action not in VALID_ACTIONS:
            raise ValueError(f"Unsupported final review action: {action}")
        if not candidate_exists(paths, final_candidate_id):
            raise ValueError(f"Unknown final_candidate_id: {final_candidate_id}")
        created_at = utc_now()
        payload["actions"].append(
            {
                "final_review_action_id": final_review_action_id(final_candidate_id, action, created_at),
                "final_candidate_id": final_candidate_id,
                "action": action,
                "status": "RECORDED",
                "human_note": note,
                "created_at": created_at,
                "do_not_publish": True,
            }
        )
        changed = True
    payload["summary"] = summarize(list_payload(payload, "actions"))
    result = write_final_review_actions(payload, paths, repo_root)
    return result, payload, changed


def write_final_review_actions(payload: dict[str, Any], paths: ProjectPaths, repo_root: Path) -> FinalReviewActionsResult:
    run_date = str(payload.get("run_date") or today_token()).replace("-", "")[:8]
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return FinalReviewActionsResult(
        run_date,
        int(summary.get("action_count", 0)),
        int(summary.get("ready_count", 0)),
        int(summary.get("needs_edit_count", 0)),
        int(summary.get("hold_count", 0)),
        repo_relative(outputs["latest_json"], repo_root),
    )


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('final_review_action_id')}` | `{item.get('final_candidate_id')}` | `{item.get('action')}` | `{item.get('created_at')}` | {item.get('human_note') or ''} |"
        for item in list_payload(payload, "actions")
    ) or "| - | - | - | - | No final review actions recorded |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Final Review Actions

## Summary

- Run date: `{payload.get('run_date')}`
- Actions: `{summary.get('action_count', 0)}`
- Ready marks: `{summary.get('ready_count', 0)}`
- Needs edit marks: `{summary.get('needs_edit_count', 0)}`
- Hold marks: `{summary.get('hold_count', 0)}`
- Policy: actions record local human state only; they never publish.

| Action ID | Final Candidate | Action | Created At | Note |
|---|---|---|---|---|
{rows}
"""

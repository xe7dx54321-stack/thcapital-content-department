"""Track manual publish sessions without publishing anything automatically."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"
VALID_STATUSES = {"PLANNED", "MANUALLY_PUBLISHED", "CANCELLED", "DEFERRED"}


@dataclass(frozen=True)
class ManualPublishSessionResult:
    run_date: str
    session_count: int
    planned: int
    published: int
    cancelled: int
    deferred: int
    output_path: str
    board_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__manual-publish-sessions.json",
        "dated_md": root / f"{run_date}__manual-publish-sessions.md",
        "latest_json": root / "latest_manual_publish_sessions.json",
        "latest_md": root / "latest_manual_publish_sessions.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__manual-publish-session-board.md",
        "board_latest_md": paths.frontstage_root / "latest_manual_publish_session_board.md",
    }


def by_key(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(key)): item for item in items if item.get(key)}


def session_id(final_candidate_id: str, created_at: str) -> str:
    digest = hashlib.sha1(f"{final_candidate_id}|{created_at}".encode("utf-8")).hexdigest()[:12]
    return f"pubsess_{today_token()}_{digest}"


def summarize(sessions: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "session_count": len(sessions),
        "planned": sum(1 for item in sessions if item.get("publish_status") == "PLANNED"),
        "published": sum(1 for item in sessions if item.get("publish_status") == "MANUALLY_PUBLISHED"),
        "cancelled": sum(1 for item in sessions if item.get("publish_status") == "CANCELLED"),
        "deferred": sum(1 for item in sessions if item.get("publish_status") == "DEFERRED"),
    }


def load_payload(paths: ProjectPaths) -> dict[str, Any]:
    root = paths.market_content_root / "07_publishing"
    existing = read_json(root / "latest_manual_publish_sessions.json")
    run_date = str(existing.get("run_date") or today_token()).replace("-", "")[:8]
    sessions = list_payload(existing, "sessions")
    return {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "sessions": sessions, "summary": summarize(sessions)}


def final_candidate_lookup(paths: ProjectPaths) -> dict[str, dict[str, Any]]:
    root = paths.market_content_root / "07_publishing"
    candidates = list_payload(read_json(root / "latest_final_article_candidates.json"), "candidates")
    memory = list_payload(read_json(root / "final_candidate_memory.json"), "final_candidates")
    merged = by_key(memory, "final_candidate_id")
    merged.update(by_key(candidates, "final_candidate_id"))
    return merged


def update_manual_publish_session(
    paths: ProjectPaths,
    repo_root: Path,
    final_candidate_id: str = "",
    publish_session_id: str = "",
    status: str = "",
    url: str = "",
    note: str = "",
    planned_publish_at: str = "",
) -> tuple[ManualPublishSessionResult, dict[str, Any], bool]:
    payload = load_payload(paths)
    sessions = list_payload(payload, "sessions")
    changed = False
    candidates = final_candidate_lookup(paths)
    if final_candidate_id:
        candidate = candidates.get(final_candidate_id)
        if not candidate:
            raise ValueError(f"Unknown final_candidate_id: {final_candidate_id}")
        created_at = utc_now()
        sessions.append(
            {
                "publish_session_id": session_id(final_candidate_id, created_at),
                "final_candidate_id": final_candidate_id,
                "version_id": candidate.get("version_id") or "",
                "platform": "wechat",
                "publish_mode": "manual_copy",
                "planned_publish_at": planned_publish_at,
                "actual_publish_at": "",
                "publish_status": "PLANNED",
                "published_url": "",
                "manual_note": note,
                "created_at": created_at,
                "do_not_auto_publish": True,
            }
        )
        changed = True
    if publish_session_id and status:
        if status not in VALID_STATUSES:
            raise ValueError(f"Unsupported publish status: {status}")
        for item in sessions:
            if item.get("publish_session_id") == publish_session_id:
                item["publish_status"] = status
                if status == "MANUALLY_PUBLISHED":
                    item["actual_publish_at"] = utc_now()
                if url:
                    item["published_url"] = url
                if note:
                    item["manual_note"] = note
                item["do_not_auto_publish"] = True
                changed = True
                break
    payload["sessions"] = sessions
    payload["summary"] = summarize(sessions)
    result = write_manual_publish_sessions(payload, paths, repo_root)
    return result, payload, changed


def write_manual_publish_sessions(payload: dict[str, Any], paths: ProjectPaths, repo_root: Path) -> ManualPublishSessionResult:
    run_date = str(payload.get("run_date") or today_token()).replace("-", "")[:8]
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return ManualPublishSessionResult(
        run_date,
        int(summary.get("session_count", 0)),
        int(summary.get("planned", 0)),
        int(summary.get("published", 0)),
        int(summary.get("cancelled", 0)),
        int(summary.get("deferred", 0)),
        repo_relative(outputs["latest_json"], repo_root),
        repo_relative(outputs["board_latest_md"], repo_root),
    )


def build_publish_session_board(paths: ProjectPaths, repo_root: Path) -> tuple[ManualPublishSessionResult, dict[str, Any]]:
    payload = load_payload(paths)
    return write_manual_publish_sessions(payload, paths, repo_root), payload


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('publish_session_id')}` | `{item.get('final_candidate_id')}` | `{item.get('publish_status')}` | `{item.get('published_url') or ''}` | {item.get('manual_note') or ''} |"
        for item in list_payload(payload, "sessions")
    ) or "| - | - | - | - | No manual publish sessions recorded |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Manual Publish Session Board

## Summary

- Sessions: `{summary.get('session_count', 0)}`
- Planned: `{summary.get('planned', 0)}`
- Manually published: `{summary.get('published', 0)}`
- Cancelled: `{summary.get('cancelled', 0)}`
- Deferred: `{summary.get('deferred', 0)}`
- Policy: manual session tracking only; no WeChat API or draft-box action.

| Session | Final Candidate | Status | URL | Note |
|---|---|---|---|---|
{rows}
"""

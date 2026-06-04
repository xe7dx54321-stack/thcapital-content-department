"""Build issue resolution verification board."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__issue-resolution-verification.json",
        "dated_md": paths.logs_root / f"{run_date}__issue-resolution-verification.md",
        "latest_json": paths.logs_root / "latest_issue_resolution_verification.json",
        "latest_md": paths.logs_root / "latest_issue_resolution_verification.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__issue-resolution-verification-board.md",
        "board_latest_md": paths.frontstage_root / "latest_issue_resolution_verification_board.md",
    }


def build_issue_resolution_verification(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    plan = read_json(paths.logs_root / "latest_high_priority_issue_resolution_plan.json")
    quick = read_json(paths.logs_root / "latest_quick_fix_execution_results.json")
    queue_repair = read_json(paths.market_content_root / "07_publishing" / "latest_content_queue_readiness_repair.json")
    calendar = read_json(paths.market_content_root / "07_publishing" / "latest_publishing_calendar_readiness_calibration.json")
    stabilizer = read_json(paths.logs_root / "latest_trial_day_status_stabilizer.json")
    results_by_resolution = {str(item.get("resolution_id") or ""): item for item in list_payload(quick, "fix_results")}
    queue_summary = queue_repair.get("summary") if isinstance(queue_repair.get("summary"), dict) else {}
    calendar_summary = calendar.get("summary") if isinstance(calendar.get("summary"), dict) else {}
    stable_summary = stabilizer.get("stabilization_summary") if isinstance(stabilizer.get("stabilization_summary"), dict) else {}
    verifications = []
    for issue in list_payload(plan, "issues"):
        resolution_id = str(issue.get("resolution_id") or "")
        result = results_by_resolution.get(resolution_id, {})
        evidence: list[str] = []
        remaining: list[str] = []
        status = "UNRESOLVED"
        if result.get("status") == "APPLIED_SIDECAR":
            status = "PARTIAL"
            evidence.append(f"quick fix sidecar applied: {result.get('fix_type')}")
            if int(queue_summary.get("improved") or 0) > 0:
                status = "VERIFIED"
                evidence.append(f"queue readiness improved: {queue_summary.get('improved')}")
            if int(calendar_summary.get("actionable_days") or 0) > 0:
                evidence.append(f"calendar actionable days: {calendar_summary.get('actionable_days')}")
        elif result.get("status") == "NEEDS_MANUAL" or issue.get("current_status") == "NEEDS_MANUAL":
            status = "NEEDS_MANUAL"
            remaining.append(issue.get("recommended_fix") or "Manual operator action required.")
        elif issue.get("current_status") == "MONITOR":
            status = "NOT_APPLICABLE"
            evidence.append("monitor-only issue does not require quick-fix execution.")
        if stable_summary.get("can_continue") and status in {"PARTIAL", "VERIFIED", "NOT_APPLICABLE"}:
            evidence.append("trial stabilizer reports can_continue=true")
        if status == "UNRESOLVED":
            remaining.append("No sidecar result or manual closure evidence yet.")
        verifications.append(
            {
                "verification_id": make_id("ver", run_date, resolution_id),
                "resolution_id": resolution_id,
                "source_issue_id": issue.get("source_issue_id", ""),
                "fix_result_id": result.get("fix_result_id", ""),
                "verification_status": status,
                "evidence": evidence,
                "remaining_work": remaining,
                "operator_note": "Do not mark closed until operator confirms action outcome." if status in {"NEEDS_MANUAL", "PARTIAL"} else "",
            }
        )
    summary = {
        "verification_count": len(verifications),
        "verified": sum(1 for item in verifications if item.get("verification_status") == "VERIFIED"),
        "partial": sum(1 for item in verifications if item.get("verification_status") == "PARTIAL"),
        "unresolved": sum(1 for item in verifications if item.get("verification_status") == "UNRESOLVED"),
        "needs_manual": sum(1 for item in verifications if item.get("verification_status") == "NEEDS_MANUAL"),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "verifications": verifications,
        "summary": summary,
        "policy": {"sidecar_only": True, "no_auto_close": True, "no_auto_publish": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        f"| `{item.get('verification_status')}` | {item.get('source_issue_id')} | {', '.join(item.get('evidence') or [])} | {', '.join(item.get('remaining_work') or [])} |"
        for item in list_payload(payload, "verifications")
    ]
    return f"""# Issue Resolution Verification

## Summary

- verification_count: `{summary.get('verification_count', 0)}`
- verified: `{summary.get('verified', 0)}`
- partial: `{summary.get('partial', 0)}`
- unresolved: `{summary.get('unresolved', 0)}`
- needs_manual: `{summary.get('needs_manual', 0)}`

| Status | Source issue | Evidence | Remaining work |
|---|---|---|---|
{chr(10).join(rows)}
"""

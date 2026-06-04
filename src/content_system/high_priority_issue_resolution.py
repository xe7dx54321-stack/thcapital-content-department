"""Build a resolution plan for high-priority recurring ops issues."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


AREAS = {"source", "topic", "draft", "visual", "publishing", "metrics", "workbench", "system", "docs"}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__high-priority-issue-resolution-plan.json",
        "dated_md": paths.logs_root / f"{run_date}__high-priority-issue-resolution-plan.md",
        "latest_json": paths.logs_root / "latest_high_priority_issue_resolution_plan.json",
        "latest_md": paths.logs_root / "latest_high_priority_issue_resolution_plan.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__high-priority-issue-resolution-plan-board.md",
        "board_latest_md": paths.frontstage_root / "latest_high_priority_issue_resolution_plan_board.md",
    }


def read_first_json(paths: list[Path]) -> dict[str, Any]:
    for path in paths:
        payload = read_json(path)
        if payload:
            return payload
    return {}


def area_of(item: dict[str, Any]) -> str:
    area = str(item.get("area") or "system")
    return area if area in AREAS else "system"


def classify_issue(issue: dict[str, Any], fix_by_issue: dict[str, dict[str, Any]]) -> tuple[str, str, str]:
    area = area_of(issue)
    description = str(issue.get("description") or issue.get("title") or "")
    source_id = str(issue.get("recurring_issue_id") or issue.get("source_issue_id") or "")
    linked_fix = fix_by_issue.get(source_id, {})
    if linked_fix.get("fix_type") == "quick_fix" or issue.get("quick_fix_candidate"):
        return "quick_fix", "READY_TO_FIX", "quick fix sidecar can clarify status, create reminders, or generate operator action."
    if area in {"topic", "draft"}:
        return "manual_intervention", "NEEDS_MANUAL", "content quality/evidence/rewrite issue requires operator judgment."
    if area in {"workbench", "system", "source"}:
        return "monitor_only", "MONITOR", "system/workbench/source issue should be observed unless it produces a blocker."
    if area == "metrics":
        return "manual_intervention", "NEEDS_MANUAL", "metrics must be entered manually after publication."
    return "next_phase", "BLOCKED", "issue needs future implementation beyond safe sidecar quick fixes."


def root_cause(area: str, description: str) -> str:
    lowered = description.lower()
    if "today" in lowered:
        return "queue has no TODAY-ready item; publishing calendar cannot recommend same-day release."
    if "visual" in lowered or "asset" in lowered or "图片" in description:
        return "visual assets or visual checklist are missing, so publishing readiness is ambiguous."
    if "evidence" in lowered or "证据" in description:
        return "topic has insufficient evidence or source support for publish-ready status."
    if "rewrite" in lowered or "重写" in description:
        return "draft still needs rewrite/review before it can move into publishing readiness."
    if "metrics" in lowered:
        return "post-publish feedback loop lacks manual metric input."
    return "trial issue is recurring across day records and needs operator-visible resolution."


def verification_method(resolution_type: str, area: str) -> str:
    if resolution_type == "quick_fix":
        return "quick-fix execution result exists and queue/calendar/stabilizer references its sidecar payload."
    if resolution_type == "manual_intervention":
        return "operator has a next action and issue is marked NEEDS_MANUAL rather than blocking the pipeline."
    if resolution_type == "monitor_only":
        return "issue appears in monitoring board without failing stable trial readiness gate."
    if area == "publishing":
        return "calendar calibration creates READY or ACTIONABLE days with explicit manual action."
    return "verification board records remaining work and owner."


def expected_impact(resolution_type: str, area: str) -> str:
    if area == "publishing":
        return "improve_ready_days"
    if area in {"topic", "draft", "visual"}:
        return "reduce_blockers"
    if resolution_type == "monitor_only":
        return "operator_clarity"
    return "reduce_degraded"


def build_high_priority_issue_resolution_plan(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    recurring = read_first_json(
        [
            paths.logs_root / "latest_recurring_issue_board.json",
            paths.logs_root / "latest_recurring_issue_tracker.json",
        ]
    )
    content_fix = read_json(paths.logs_root / "latest_content_ops_fix_pack.json")
    trial_fix = read_json(paths.logs_root / "latest_trial_fix_pack.json")
    failure = read_json(paths.logs_root / "latest_content_ops_failure_handling.json")
    closeout = read_json(paths.logs_root / "latest_content_ops_closeout.json")
    warnings = []
    if not recurring:
        warnings.append("Missing recurring issue tracker/board input.")
    if not content_fix:
        warnings.append("Missing content ops fix pack input.")

    fixes = list_payload(content_fix, "fixes")
    fix_by_issue = {str(item.get("source_issue_id") or ""): item for item in fixes}
    source_issues = list_payload(recurring, "issues")
    if not source_issues:
        source_issues = [
            {
                "recurring_issue_id": item.get("issue_id"),
                "area": item.get("area"),
                "description": item.get("description"),
                "severity": item.get("severity", "WARN"),
                "quick_fix_candidate": False,
            }
            for item in list_payload(failure, "issues")
        ]
    resolutions: list[dict[str, Any]] = []
    for issue in source_issues:
        severity = str(issue.get("severity") or "LOW")
        if severity not in {"HIGH", "MEDIUM", "LOW"}:
            severity = "HIGH" if str(issue.get("urgency")) == "P0" else "MEDIUM"
        area = area_of(issue)
        source_issue_id = str(issue.get("recurring_issue_id") or issue.get("issue_id") or make_id("issue", run_date, area, issue.get("description")))
        resolution_type, current_status, reason = classify_issue(issue, fix_by_issue)
        description = str(issue.get("description") or "Recurring ops issue.")
        recommended_fix = str(issue.get("recommended_fix") or reason)
        resolutions.append(
            {
                "resolution_id": make_id("res", run_date, source_issue_id, resolution_type),
                "source_issue_id": source_issue_id,
                "title": description[:120],
                "area": area,
                "severity": severity,
                "resolution_type": resolution_type,
                "current_status": current_status,
                "root_cause": root_cause(area, description),
                "recommended_fix": recommended_fix,
                "verification_method": verification_method(resolution_type, area),
                "expected_impact": expected_impact(resolution_type, area),
                "auto_apply": False,
                "safe_to_execute": resolution_type in {"quick_fix", "monitor_only"},
            }
        )
    if not resolutions:
        resolutions.append(
            {
                "resolution_id": make_id("res", run_date, "no_issue"),
                "source_issue_id": "",
                "title": "No high-priority recurring issue detected.",
                "area": "system",
                "severity": "LOW",
                "resolution_type": "monitor_only",
                "current_status": "MONITOR",
                "root_cause": "No recurring issue input.",
                "recommended_fix": "Continue stable trial and monitor daily ops outputs.",
                "verification_method": "stable gate remains PASS or ACTIONABLE_WITH_WARNINGS.",
                "expected_impact": "operator_clarity",
                "auto_apply": False,
                "safe_to_execute": True,
            }
        )
    summary = {
        "issue_count": len(resolutions),
        "high_priority": sum(1 for item in resolutions if item.get("severity") == "HIGH"),
        "quick_fix": sum(1 for item in resolutions if item.get("resolution_type") == "quick_fix"),
        "manual_intervention": sum(1 for item in resolutions if item.get("resolution_type") == "manual_intervention"),
        "next_phase": sum(1 for item in resolutions if item.get("resolution_type") == "next_phase"),
        "monitor_only": sum(1 for item in resolutions if item.get("resolution_type") == "monitor_only"),
        "failure_issue_count": len(list_payload(failure, "issues")),
        "closeout_actions": len(closeout.get("operator_actions", [])) if isinstance(closeout.get("operator_actions"), list) else 0,
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "issues": resolutions,
        "summary": summary,
        "warnings": warnings,
        "policy": {"sidecar_only": True, "auto_apply": False, "no_auto_publish": True, "no_config_prompt_rule_changes": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        f"| `{item.get('severity')}` | `{item.get('resolution_type')}` | `{item.get('current_status')}` | {item.get('area')} | {item.get('title')} | {item.get('recommended_fix')} |"
        for item in list_payload(payload, "issues")
    ]
    return f"""# High-priority Issue Resolution Plan

## Summary

- issue_count: `{summary.get('issue_count', 0)}`
- high_priority: `{summary.get('high_priority', 0)}`
- quick_fix: `{summary.get('quick_fix', 0)}`
- manual_intervention: `{summary.get('manual_intervention', 0)}`
- next_phase: `{summary.get('next_phase', 0)}`
- monitor_only: `{summary.get('monitor_only', 0)}`

| Severity | Resolution type | Current status | Area | Issue | Recommended fix |
|---|---|---|---|---|---|
{chr(10).join(rows)}

All items are sidecar-only and `auto_apply=false`.
"""

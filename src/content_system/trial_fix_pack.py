"""Build a trial fix pack from weekly retrospective and hardening reports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__trial-fix-pack.json",
        "dated_md": paths.logs_root / f"{run_date}__trial-fix-pack.md",
        "latest_json": paths.logs_root / "latest_trial_fix_pack.json",
        "latest_md": paths.logs_root / "latest_trial_fix_pack.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__trial-fix-pack-board.md",
        "board_latest_md": paths.frontstage_root / "latest_trial_fix_pack_board.md",
    }


def fix(run_date: str, area: str, severity: str, fix_type: str, description: str, recommended_change: str, owner: str) -> dict[str, Any]:
    return {
        "fix_id": make_id("trial_fix", run_date, area, fix_type, description),
        "area": area,
        "severity": severity,
        "fix_type": fix_type,
        "description": description,
        "recommended_change": recommended_change,
        "owner": owner,
        "auto_apply": False,
        "status": "PLANNED",
    }


def severity_from_issue(issue: dict[str, Any]) -> str:
    severity = str(issue.get("severity") or "")
    if severity == "BLOCKER":
        return "HIGH"
    if severity == "WARN":
        return "MEDIUM"
    return "LOW"


def build_trial_fix_pack(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    retrospective = read_json(paths.logs_root / "latest_weekly_trial_retrospective.json")
    failure = read_json(paths.logs_root / "latest_content_ops_failure_handling.json")
    regression = read_json(paths.logs_root / "latest_publishing_checklist_regression.json")
    runbook = read_json(paths.logs_root / "latest_operator_runbook.json")
    closeout = read_json(paths.logs_root / "latest_phase0_19_system_closeout.json")
    fixes: list[dict[str, Any]] = []
    for item in list_payload(retrospective, "recurring_issues")[:8]:
        area = str(item.get("area") or "system")
        fixes.append(
            fix(
                run_date,
                area,
                "MEDIUM",
                "next_phase",
                item.get("description") or "Recurring trial issue.",
                "在 Phase22 中降低该 recurring issue 的出现频率，并在 workbench 中给出更明确的优先级。",
                "future_phase",
            )
        )
    for item in list_payload(failure, "issues")[:8]:
        fixes.append(
            fix(
                run_date,
                str(item.get("area") or "system"),
                severity_from_issue(item),
                "manual_ops_note" if item.get("severity") == "INFO" else "next_phase",
                item.get("description") or "Content ops failure issue.",
                item.get("recommended_action") or "按 failure handling 建议人工处理。",
                "operator" if item.get("severity") == "INFO" else "future_phase",
            )
        )
    regression_summary = regression.get("summary") if isinstance(regression.get("summary"), dict) else {}
    if regression_summary.get("regression_status") != "PASS":
        fixes.append(
            fix(
                run_date,
                "publishing",
                "HIGH",
                "quick_fix",
                "Publishing checklist regression is not PASS.",
                "先修复 checklist safety regression，再恢复 trial execution。",
                "system",
            )
        )
    if not list_payload(runbook, "sections"):
        fixes.append(fix(run_date, "docs", "MEDIUM", "quick_fix", "Operator runbook has no sections.", "重建 operator runbook 并验证工作台可读。", "system"))
    readiness = closeout.get("trial_readiness") if isinstance(closeout.get("trial_readiness"), dict) else {}
    if readiness.get("status") == "NEEDS_FIX":
        fixes.append(
            fix(
                run_date,
                "system",
                "MEDIUM",
                "next_phase",
                "Phase0-19 closeout reports NEEDS_FIX.",
                "把 closeout known gaps 拆成 Phase22 high-severity fixes、workbench friction fixes 和 queue/calendar calibration。",
                "future_phase",
            )
        )
    if not fixes:
        fixes.append(fix(run_date, "system", "LOW", "manual_ops_note", "No trial fixes required from current artifacts.", "继续真实跨日 trial，并记录人工反馈。", "operator"))
    seen: set[str] = set()
    unique_fixes = []
    for item in fixes:
        key = f"{item.get('area')}::{item.get('fix_type')}::{item.get('description')}"
        if key in seen:
            continue
        seen.add(key)
        unique_fixes.append(item)
    summary = {
        "fix_count": len(unique_fixes),
        "quick_fix": sum(1 for item in unique_fixes if item.get("fix_type") == "quick_fix"),
        "next_phase": sum(1 for item in unique_fixes if item.get("fix_type") == "next_phase"),
        "manual_ops_note": sum(1 for item in unique_fixes if item.get("fix_type") == "manual_ops_note"),
        "high_severity": sum(1 for item in unique_fixes if item.get("severity") == "HIGH"),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "fixes": unique_fixes,
        "summary": summary,
        "policy": {"auto_apply": False, "no_prompt_rule_config_changes": True, "no_large_refactor": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [f"| `{item.get('severity')}` | `{item.get('fix_type')}` | {item.get('area')} | {item.get('description')} | {item.get('recommended_change')} |" for item in list_payload(payload, "fixes")]
    return f"""# Trial Fix Pack

## Summary

- fix_count: `{summary.get('fix_count', 0)}`
- quick_fix: `{summary.get('quick_fix', 0)}`
- next_phase: `{summary.get('next_phase', 0)}`
- manual_ops_note: `{summary.get('manual_ops_note', 0)}`
- high_severity: `{summary.get('high_severity', 0)}`

| Severity | Type | Area | Description | Recommended change |
|---|---|---|---|---|
{chr(10).join(rows)}

All fixes are `auto_apply=false`.
"""

"""Track and prioritize recurring content-ops issues from trial records."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


HIGH_RISK_AREAS = {"publishing", "visual", "metrics"}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__recurring-issue-tracker.json",
        "dated_md": paths.logs_root / f"{run_date}__recurring-issue-tracker.md",
        "latest_json": paths.logs_root / "latest_recurring_issue_tracker.json",
        "latest_md": paths.logs_root / "latest_recurring_issue_tracker.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__recurring-issue-board.md",
        "board_latest_md": paths.frontstage_root / "latest_recurring_issue_board.md",
    }


def normalize_area(value: Any) -> str:
    text = str(value or "system")
    return text if text in {"source", "topic", "draft", "visual", "publishing", "metrics", "workbench", "system", "docs"} else "system"


def severity_score(severity: str) -> int:
    return {"BLOCKER": 100, "WARN": 55, "INFO": 20}.get(severity, 20)


def issue_recommendation(area: str, description: str) -> tuple[str, str]:
    lowered = description.lower()
    if "today" in lowered or "可发" in description:
        return "先从 THIS_WEEK 队列挑选最高 ready 内容，补齐发布日历 slot；若无 ready 内容，保持不发布。", "queue_calendar_calibration"
    if "visual" in lowered or "asset" in lowered or "图片" in description or area == "visual":
        return "优先补齐图片资产、视觉 checklist 或把该条内容降级为本周候选，避免卡住 TODAY。", "visual_readiness_repair"
    if "metrics" in lowered or "published metrics" in lowered or area == "metrics":
        return "人工录入已发布文章表现数据，再运行 post-publish-feedback 形成学习建议。", "metrics_feedback_repair"
    if "source runtime" in lowered or area == "source":
        return "检查 source-runtime-health，确认缺失来源是否影响今日选题；必要时切换到已有队列。", "source_health_repair"
    if "copy pack" in lowered or area == "publishing":
        return "检查 copy pack、visual checklist 和 manual publish session，补齐人工发布准备状态。", "publishing_pack_repair"
    return "按 operator runbook 处理，并在下一次 phase22-daily 中复核是否仍重复出现。", "ops_review"


def risk_category(area: str, description: str) -> str:
    lowered = description.lower()
    if area == "publishing" or "publish" in lowered or "发布" in description:
        return "publishing_readiness"
    if area == "visual" or "visual" in lowered or "asset" in lowered or "图片" in description:
        return "visual_asset"
    if area == "metrics" or "metrics" in lowered:
        return "performance_feedback"
    if area == "topic":
        return "content_queue"
    if area == "workbench":
        return "operator_ux"
    return "system_ops"


def build_recurring_issue_tracker(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    retrospective = read_json(paths.logs_root / "latest_weekly_trial_retrospective.json")
    trial_fix_pack = read_json(paths.logs_root / "latest_trial_fix_pack.json")
    failure = read_json(paths.logs_root / "latest_content_ops_failure_handling.json")
    groups: dict[tuple[str, str], dict[str, Any]] = defaultdict(lambda: {"count": 0, "source_issue_ids": [], "severities": []})

    for item in list_payload(retrospective, "recurring_issues"):
        area = normalize_area(item.get("area"))
        description = str(item.get("description") or "Recurring trial issue.")
        key = (area, description)
        groups[key]["count"] += int(item.get("count") or 1)
        groups[key]["source_issue_ids"].append(item.get("issue_id") or "")
        groups[key]["severities"].append("WARN")

    for day in range(1, 6):
        payload = read_json(paths.logs_root / f"latest_trial_day_{day}_execution.json")
        for item in list_payload(payload, "issues"):
            area = normalize_area(item.get("area"))
            description = str(item.get("description") or "Trial issue.")
            key = (area, description)
            groups[key]["count"] += 1
            groups[key]["source_issue_ids"].append(item.get("issue_id") or "")
            groups[key]["severities"].append(str(item.get("severity") or "INFO"))

    for item in list_payload(failure, "issues"):
        area = normalize_area(item.get("area"))
        description = str(item.get("description") or "Content ops issue.")
        key = (area, description)
        groups[key]["count"] += 1
        groups[key]["source_issue_ids"].append(item.get("issue_id") or "")
        groups[key]["severities"].append(str(item.get("severity") or "INFO"))

    issues: list[dict[str, Any]] = []
    for (area, description), meta in groups.items():
        count = int(meta.get("count") or 0)
        severities = [str(value) for value in meta.get("severities", [])]
        base = max((severity_score(value) for value in severities), default=20)
        area_bonus = 18 if area in HIGH_RISK_AREAS else 8 if area in {"topic", "draft"} else 0
        priority_score = min(100, base + count * 6 + area_bonus)
        if priority_score >= 85:
            urgency = "P0"
            priority = "HIGH"
        elif priority_score >= 65:
            urgency = "P1"
            priority = "MEDIUM"
        else:
            urgency = "P2"
            priority = "LOW"
        recommendation, fix_lane = issue_recommendation(area, description)
        quick_fix = area in {"visual", "publishing", "metrics"} or "today" in description.lower()
        issues.append(
            {
                "recurring_issue_id": make_id("rec_issue", run_date, area, description),
                "area": area,
                "description": description,
                "occurrence_count": count,
                "source_issue_ids": [value for value in dict.fromkeys(meta.get("source_issue_ids", [])) if value],
                "severity": priority,
                "risk_category": risk_category(area, description),
                "urgency": urgency,
                "priority_score": priority_score,
                "fix_lane": fix_lane,
                "recommended_fix": recommendation,
                "quick_fix_candidate": quick_fix,
                "manual_required": True,
                "auto_apply": False,
                "status": "OPEN",
            }
        )
    issues.sort(key=lambda item: (-int(item.get("priority_score") or 0), str(item.get("area"))))
    for index, item in enumerate(issues, start=1):
        item["recommended_order"] = index

    fix_summary = trial_fix_pack.get("summary") if isinstance(trial_fix_pack.get("summary"), dict) else {}
    summary = {
        "issue_count": len(issues),
        "high": sum(1 for item in issues if item.get("severity") == "HIGH"),
        "medium": sum(1 for item in issues if item.get("severity") == "MEDIUM"),
        "low": sum(1 for item in issues if item.get("severity") == "LOW"),
        "quick_fix_candidates": sum(1 for item in issues if item.get("quick_fix_candidate")),
        "manual_required": sum(1 for item in issues if item.get("manual_required")),
        "trial_fix_count": fix_summary.get("fix_count", 0),
        "can_continue": not any(item.get("urgency") == "P0" for item in issues),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "issues": issues,
        "summary": summary,
        "policy": {"sidecar_only": True, "auto_apply": False, "no_auto_publish": True, "no_config_prompt_rule_changes": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        f"| {item.get('recommended_order')} | `{item.get('urgency')}` | `{item.get('severity')}` | {item.get('area')} | {item.get('occurrence_count')} | {item.get('description')} | {item.get('recommended_fix')} |"
        for item in list_payload(payload, "issues")
    ]
    return f"""# Recurring Issue Tracker

## Summary

- issue_count: `{summary.get('issue_count', 0)}`
- high: `{summary.get('high', 0)}`
- medium: `{summary.get('medium', 0)}`
- low: `{summary.get('low', 0)}`
- quick_fix_candidates: `{summary.get('quick_fix_candidates', 0)}`
- can_continue: `{summary.get('can_continue', True)}`

| Order | Urgency | Severity | Area | Count | Issue | Recommended fix |
|---:|---|---|---|---:|---|---|
{chr(10).join(rows) or "| - | - | - | - | - | No recurring issue | - |"}

All recommendations are `auto_apply=false`.
"""

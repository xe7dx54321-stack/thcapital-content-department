"""Build content-ops failure handling guidance for operators."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__content-ops-failure-handling.json",
        "dated_md": paths.logs_root / f"{run_date}__content-ops-failure-handling.md",
        "latest_json": paths.logs_root / "latest_content_ops_failure_handling.json",
        "latest_md": paths.logs_root / "latest_content_ops_failure_handling.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__content-ops-failure-handling-board.md",
        "board_latest_md": paths.frontstage_root / "latest_content_ops_failure_handling_board.md",
    }


def issue(run_date: str, area: str, severity: str, detected_from: str, description: str, recommended_action: str, can_continue: bool = True) -> dict[str, Any]:
    return {
        "issue_id": make_id("ops_issue", run_date, area, detected_from, description),
        "area": area,
        "severity": severity,
        "detected_from": detected_from,
        "description": description,
        "recommended_action": recommended_action,
        "can_continue": can_continue,
        "manual_required": True,
    }


def pipeline_issues(run_date: str, payload: dict[str, Any], name: str) -> list[dict[str, Any]]:
    status = str(payload.get("status") or "UNKNOWN")
    if not payload:
        return [issue(run_date, "pipeline", "WARN", name, f"{name} output missing.", f"运行 make {name.replace('_', '-')} 或查看对应 latest 日志。")]
    if status not in {"SUCCESS", "OK"}:
        return [issue(run_date, "pipeline", "WARN", name, f"{name} status is {status}.", "查看 pipeline steps 中 FAILED/DEGRADED 的子命令，先修复前置产物。")]
    return []


def build_content_ops_failure_handling(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    logs = paths.logs_root
    publishing_root = paths.market_content_root / "07_publishing"
    phase19 = read_json(logs / "latest_phase19_daily_ops_pipeline.json")
    phase18 = read_json(logs / "latest_phase18_daily_publishing_pack_pipeline.json")
    phase17 = read_json(logs / "latest_phase17_daily_visual_production_pipeline.json")
    phase16 = read_json(logs / "latest_phase16_daily_live_pilot_pipeline.json")
    runtime = read_json(logs / "latest_source_runtime_health.json")
    closeout = read_json(logs / "latest_content_ops_closeout.json")
    queue = read_json(publishing_root / "latest_content_queue_priority.json")
    visual_checklist = read_json(publishing_root / "latest_visual_publishing_checklist.json")
    issues: list[dict[str, Any]] = []
    for name, payload in (
        ("phase19_daily", phase19),
        ("phase18_daily", phase18),
        ("phase17_daily", phase17),
        ("phase16_daily", phase16),
    ):
        issues.extend(pipeline_issues(run_date, payload, name))
    runtime_summary = runtime.get("summary") if isinstance(runtime.get("summary"), dict) else {}
    missing_expected = safe_int(runtime_summary.get("missing_expected"))
    if missing_expected:
        issues.append(issue(run_date, "source", "WARN", "latest_source_runtime_health", f"{missing_expected} expected sources are missing runtime observations.", "先看 source-runtime-health board；official lane 可继续，但不要把缺失来源当作真实无信号。"))
    queue_summary = queue.get("summary") if isinstance(queue.get("summary"), dict) else {}
    if safe_int(queue_summary.get("today")) == 0:
        issues.append(issue(run_date, "publishing", "INFO", "latest_content_queue_priority", "No TODAY priority item is ready.", "不要硬发；从 THIS_WEEK 里挑 READY_FOR_REVIEW 内容或补图/补证据。"))
    if safe_int(queue_summary.get("item_count")) and safe_int(queue_summary.get("today")) == 0 and safe_int(queue_summary.get("this_week")) == 0:
        issues.append(issue(run_date, "topic", "WARN", "latest_content_queue_priority", "Queue has no TODAY or THIS_WEEK items.", "回到 methodology-topic-score 和 high-value candidates，补新选题或降低发布节奏。"))
    queue_items = list_payload(queue, "items")
    needs_visual = [item for item in queue_items if item.get("readiness_status") == "NEEDS_VISUAL_ASSET"]
    needs_evidence = [item for item in queue_items if item.get("readiness_status") == "NEEDS_EVIDENCE"]
    needs_rewrite = [item for item in queue_items if item.get("readiness_status") == "NEEDS_REWRITE"]
    if needs_visual:
        issues.append(issue(run_date, "visual", "WARN", "latest_content_queue_priority", f"{len(needs_visual)} queue items need visual assets.", "先跑 image asset / visual review 流程；缺图内容不能进入 TODAY。"))
    if needs_evidence:
        issues.append(issue(run_date, "topic", "WARN", "latest_content_queue_priority", f"{len(needs_evidence)} queue items need evidence.", "补至少 3 条证据和来源说明，再进入写作或发布。"))
    if needs_rewrite:
        issues.append(issue(run_date, "draft", "INFO", "latest_content_queue_priority", f"{len(needs_rewrite)} queue items need rewrite.", "使用 Chief Editor 快捷命令或 methodology rewrite，生成候选版本后人工审。"))
    checklist_summary = visual_checklist.get("summary") if isinstance(visual_checklist.get("summary"), dict) else {}
    if safe_int(checklist_summary.get("needs_attention")) or safe_int(checklist_summary.get("blocked")):
        issues.append(issue(run_date, "visual", "WARN", "latest_visual_publishing_checklist", "Visual publishing checklist has NEEDS_ATTENTION or BLOCKED items.", "逐项检查图片版权、清晰度、插入位置和 slot marker；未通过前不发布。"))
    closeout_summary = closeout.get("summary") if isinstance(closeout.get("summary"), dict) else {}
    blocked = safe_int(closeout_summary.get("blocked_count"))
    if blocked:
        issues.append(issue(run_date, "workbench", "WARN", "latest_content_ops_closeout", f"Content ops closeout reports {blocked} blockers.", "优先处理 closeout operator_actions 中的前 3 项。"))
    if not (paths.frontstage_root / "latest_wechat_workbench.html").exists():
        issues.append(issue(run_date, "workbench", "BLOCKER", "latest_wechat_workbench.html", "Workbench HTML missing.", "运行 make wechat-workbench；如果仍缺失，检查前端构建脚本。", can_continue=False))
    if not read_json(publishing_root / "latest_manual_publish_sessions.json"):
        issues.append(issue(run_date, "metrics", "INFO", "latest_manual_publish_sessions", "Manual publish session data is missing.", "真实发布后用 create_manual_publish_session.py 记录 session；未发布时可继续试运行。"))
    if not read_json(publishing_root / "latest_post_publish_metrics.json"):
        issues.append(issue(run_date, "metrics", "INFO", "latest_post_publish_metrics", "Post-publish metrics are missing.", "发布后 24h 人工录入 views/likes/wows/shares/comments。"))
    blocker_count = sum(1 for item in issues if item.get("severity") == "BLOCKER")
    warn_count = sum(1 for item in issues if item.get("severity") == "WARN")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "issues": issues,
        "summary": {"issue_count": len(issues), "blocker_count": blocker_count, "warn_count": warn_count, "can_continue": blocker_count == 0},
        "policy": {"manual_required": True, "no_auto_publish": True, "no_wechat_api": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = []
    for item in list_payload(payload, "issues"):
        rows.append(f"| `{item.get('severity')}` | {item.get('area')} | {item.get('description')} | {item.get('recommended_action')} |")
    return f"""# Content Ops Failure Handling

## Summary

- issue_count: `{summary.get('issue_count', 0)}`
- blocker_count: `{summary.get('blocker_count', 0)}`
- warn_count: `{summary.get('warn_count', 0)}`
- can_continue: `{summary.get('can_continue', True)}`

| Severity | Area | Description | Recommended action |
|---|---|---|---|
{chr(10).join(rows) if rows else '| INFO | ops | No issues detected. | Continue manual trial. |'}
"""

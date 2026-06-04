"""Build a one-week manual content-ops trial protocol."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__one-week-trial-run-protocol.json",
        "dated_md": paths.logs_root / f"{run_date}__one-week-trial-run-protocol.md",
        "latest_json": paths.logs_root / "latest_one_week_trial_run_protocol.json",
        "latest_md": paths.logs_root / "latest_one_week_trial_run_protocol.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__one-week-trial-run-protocol-board.md",
        "board_latest_md": paths.frontstage_root / "latest_one_week_trial_run_protocol_board.md",
    }


def missing_inputs(paths: ProjectPaths, repo_root: Path) -> list[str]:
    expected = [
        repo_root / "docs/PROJECT_STATE.md",
        repo_root / "docs/DEVELOPMENT_TASKS.md",
        paths.logs_root / "latest_phase19_daily_ops_pipeline.json",
        paths.market_content_root / "07_publishing/latest_content_queue_priority.json",
        paths.market_content_root / "07_publishing/latest_weekly_publishing_rhythm.json",
        paths.market_content_root / "07_publishing/latest_publishing_session_calendar.json",
        paths.logs_root / "latest_content_ops_closeout.json",
    ]
    return [repo_relative(path, repo_root) for path in expected if not path.exists()]


def routine_for_day(day: int) -> dict[str, Any]:
    commands = ["make phase20-daily"] if day == 1 else ["make phase19-daily", "make content-ops-closeout"]
    if day in {3, 5}:
        commands.append("make post-publish-metrics-review")
    boards = [
        "latest_content_queue_priority_board.md",
        "latest_publishing_session_calendar_board.md",
        "latest_weekly_publishing_rhythm_board.md",
        "latest_content_ops_closeout_board.md",
    ]
    manual_actions = [
        "判断今天是否有 TODAY / THIS_WEEK 且无 blocker 的内容。",
        "对缺图、缺证据、需重写标题的内容写入人工处理备注。",
        "如人工发布，先创建 publish session，再手动复制到公众号后台。",
        "发布后只人工录入 metrics，不抓取后台数据。",
    ]
    if day == 7:
        manual_actions.append("汇总一周 trial issue log，决定是否进入稳定运营或进入修复包。")
    return {
        "day": day,
        "operator_goal": "检查今日内容队列与发布准备状态" if day == 1 else "执行人工运营例行检查与复盘",
        "commands": commands,
        "boards_to_review": boards,
        "manual_actions": manual_actions,
        "success_criteria": [
            "phase pipeline SUCCESS 或明确 DEGRADED 原因。",
            "今日可发/不可发判断清楚。",
            "所有发布动作仍由人工完成。",
        ],
        "failure_conditions": [
            "copy pack 缺失且无法定位候选稿。",
            "visual checklist BLOCKED 但仍准备发布。",
            "未创建 publish session 就声称已发布。",
        ],
    }


def build_one_week_trial_protocol(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    phase19 = read_json(paths.logs_root / "latest_phase19_daily_ops_pipeline.json")
    queue = read_json(paths.market_content_root / "07_publishing/latest_content_queue_priority.json")
    rhythm = read_json(paths.market_content_root / "07_publishing/latest_weekly_publishing_rhythm.json")
    calendar = read_json(paths.market_content_root / "07_publishing/latest_publishing_session_calendar.json")
    closeout = read_json(paths.logs_root / "latest_content_ops_closeout.json")
    warnings = [f"Missing input: {item}" for item in missing_inputs(paths, repo_root)]
    queue_summary = queue.get("summary") if isinstance(queue.get("summary"), dict) else {}
    closeout_summary = closeout.get("summary") if isinstance(closeout.get("summary"), dict) else {}
    daily_checklist = [
        "早上运行 make phase20-daily 或 make phase19-daily。",
        "打开工作台审稿模式，先看今日运营区域。",
        "确认 TODAY 内容是否 READY_TO_PUBLISH。",
        "若缺图，先进入 image asset / visual checklist 流程，不发布。",
        "若缺证据，回到 evidence / topic 阶段补证据，不发布。",
        "若标题或开头弱，走 Chief Editor / rewrite，不发布。",
        "人工发布前检查 copy pack、图片槽位、视觉 checklist。",
        "人工发布后创建或更新 publish session。",
        "人工录入阅读、点赞、在看、转发、评论等指标。",
        "收盘前查看 content ops closeout，记录 issue log。",
    ]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "trial_period": {"days": 7, "mode": "manual_ops_only", "auto_publish": False, "wechat_api": False},
        "daily_routine": [routine_for_day(day) for day in range(1, 8)],
        "daily_checklist": daily_checklist,
        "issue_log_template": [
            {"field": "date", "prompt": "问题发生日期"},
            {"field": "area", "prompt": "source/topic/draft/visual/publishing/metrics/workbench/pipeline"},
            {"field": "symptom", "prompt": "发生了什么"},
            {"field": "operator_decision", "prompt": "人工怎么处理"},
            {"field": "follow_up", "prompt": "下次要改什么"},
        ],
        "success_criteria": [
            "连续 5 个工作日 phase20-daily 不崩。",
            "每天能明确 today / this_week / blocked 内容。",
            "至少完成一次人工 publish session 记录和 metrics 录入演练。",
            "operator 能按 runbook 处理缺图、缺证据、pipeline degraded。",
        ],
        "exit_criteria": [
            "无 BLOCKER 级别运营失败未处理。",
            "发布 checklist regression 为 PASS 或只有可解释 WARN。",
            "工作台今日运营、图文发布包、失败处理、runbook 面板可读。",
        ],
        "current_signals": {
            "phase19_status": phase19.get("status") or "UNKNOWN",
            "queue_today": safe_int(queue_summary.get("today")),
            "queue_this_week": safe_int(queue_summary.get("this_week")),
            "blocked_count": safe_int(closeout_summary.get("blocked_count")),
            "calendar_days": safe_int((calendar.get("summary") or {}).get("calendar_days")) if isinstance(calendar.get("summary"), dict) else 0,
            "rhythm_ready_days": safe_int((rhythm.get("summary") or {}).get("ready_days")) if isinstance(rhythm.get("summary"), dict) else 0,
        },
        "warnings": warnings,
        "policy": {"no_auto_publish": True, "no_wechat_api": True, "no_auto_metrics_input": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    signals = payload.get("current_signals") if isinstance(payload.get("current_signals"), dict) else {}
    routine_rows = []
    for item in payload.get("daily_routine", []):
        routine_rows.append(f"- Day {item.get('day')}: {item.get('operator_goal')} / commands: `{', '.join(item.get('commands') or [])}`")
    checklist = "\n".join(f"- {item}" for item in payload.get("daily_checklist", []))
    success = "\n".join(f"- {item}" for item in payload.get("success_criteria", []))
    warnings = "\n".join(f"- {item}" for item in payload.get("warnings", [])) or "- None."
    return f"""# One-week Trial Run Protocol

## Current Signals

- phase19_status: `{signals.get('phase19_status', 'UNKNOWN')}`
- queue_today: `{signals.get('queue_today', 0)}`
- queue_this_week: `{signals.get('queue_this_week', 0)}`
- blocked_count: `{signals.get('blocked_count', 0)}`

## Daily Routine

{chr(10).join(routine_rows)}

## Daily Checklist

{checklist}

## Success Criteria

{success}

## Warnings

{warnings}

Policy: manual ops only, no WeChat API, no auto publish.
"""

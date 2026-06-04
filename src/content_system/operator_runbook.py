"""Build the operator runbook for daily manual content operations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__operator-runbook.json",
        "dated_md": paths.logs_root / f"{run_date}__operator-runbook.md",
        "latest_json": paths.logs_root / "latest_operator_runbook.json",
        "latest_md": paths.logs_root / "latest_operator_runbook.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__operator-runbook-board.md",
        "board_latest_md": paths.frontstage_root / "latest_operator_runbook_board.md",
    }


def build_operator_runbook(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    trial = read_json(paths.logs_root / "latest_one_week_trial_run_protocol.json")
    failure = read_json(paths.logs_root / "latest_content_ops_failure_handling.json")
    regression = read_json(paths.logs_root / "latest_publishing_checklist_regression.json")
    closeout = read_json(paths.logs_root / "latest_content_ops_closeout.json")
    issue_summary = failure.get("summary") if isinstance(failure.get("summary"), dict) else {}
    regression_summary = regression.get("summary") if isinstance(regression.get("summary"), dict) else {}
    startup = [
        "make phase20-daily",
        "make wechat-workbench",
        "python3 scripts/serve_wechat_workbench.py --port 8765",
    ]
    sections = [
        {"title": "每日启动命令", "items": startup},
        {"title": "每日检查顺序", "items": ["今日运营", "内容队列", "图文发布包", "失败处理", "发布后复盘", "运营 closeout"]},
        {"title": "今天没有可发内容", "items": ["不要硬发。查看 THIS_WEEK / WATCH。补图、补证据或重写后再进入发布准备。"]},
        {"title": "缺图", "items": ["查看 image asset library 和 visual checklist。图片未 AVAILABLE / APPROVED 前不发布。"]},
        {"title": "缺证据", "items": ["回到 source/evidence packet，补至少 3 条证据和来源说明。"]},
        {"title": "工作台打不开", "items": ["运行 make wechat-workbench；再运行 python3 scripts/serve_wechat_workbench.py --port 8765。"]},
        {"title": "pipeline degraded", "items": ["打开 latest_content_ops_failure_handling.md，优先处理 BLOCKER，再处理 WARN。"]},
        {"title": "创建 publish session", "items": ["python3 scripts/create_manual_publish_session.py --create <final_candidate_id> --note '准备手动发布'"]},
        {"title": "记录已发布", "items": ["python3 scripts/create_manual_publish_session.py --mark-published <publish_session_id> --url '<url>' --note '已手动发布'"]},
        {"title": "录入 metrics", "items": ["python3 scripts/record_post_publish_metrics.py --session <publish_session_id> --views 1000 --likes 20 --wows 5 --shares 3 --comments 2 --note '人工录入'"]},
        {"title": "一周复盘", "items": ["查看 trial issue log、content ops closeout、metrics review、visual feedback，再决定进入 Phase21 trial fix pack。"]},
    ]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "startup_commands": startup,
        "sections": sections,
        "current_status": {
            "trial_days": ((trial.get("trial_period") or {}).get("days") if isinstance(trial.get("trial_period"), dict) else 7),
            "failure_issue_count": issue_summary.get("issue_count", 0),
            "failure_blocker_count": issue_summary.get("blocker_count", 0),
            "regression_status": regression_summary.get("regression_status", "UNKNOWN"),
            "closeout_blocked_count": ((closeout.get("summary") or {}).get("blocked_count") if isinstance(closeout.get("summary"), dict) else 0),
        },
        "operator_actions": closeout.get("operator_actions") if isinstance(closeout.get("operator_actions"), list) else [],
        "known_failure_examples": list_payload(failure, "issues")[:8],
        "policy": {"manual_ops_only": True, "no_auto_publish": True, "no_wechat_api": True, "no_auto_metrics_input": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    docs_path = repo_root / "docs/OPERATOR_RUNBOOK.md"
    docs_path.write_text(render_docs_markdown(payload), encoding="utf-8")
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    payload["outputs"]["docs_runbook"] = repo_relative(docs_path, repo_root)
    return payload, outputs


def render_docs_markdown(payload: dict[str, Any]) -> str:
    body = render_markdown(payload)
    return body + "\n## Hard Boundaries\n\n- 不自动发布。\n- 不接公众号 API。\n- 不进入公众号草稿箱。\n- 不自动抓取后台数据。\n- 不自动生成图片。\n- 所有发布和 metrics 都由人工确认。\n"


def render_markdown(payload: dict[str, Any]) -> str:
    sections = []
    for section in list_payload(payload, "sections"):
        items = "\n".join(f"- {item}" for item in section.get("items", []))
        sections.append(f"## {section.get('title')}\n\n{items}")
    status = payload.get("current_status") if isinstance(payload.get("current_status"), dict) else {}
    return f"""# Operator Runbook

## Current Status

- trial_days: `{status.get('trial_days', 7)}`
- failure_issue_count: `{status.get('failure_issue_count', 0)}`
- failure_blocker_count: `{status.get('failure_blocker_count', 0)}`
- regression_status: `{status.get('regression_status', 'UNKNOWN')}`
- closeout_blocked_count: `{status.get('closeout_blocked_count', 0)}`

{chr(10).join(sections)}
"""

"""Build Phase 0-19 system closeout."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__phase0-19-system-closeout.json",
        "dated_md": paths.logs_root / f"{run_date}__phase0-19-system-closeout.md",
        "latest_json": paths.logs_root / "latest_phase0_19_system_closeout.json",
        "latest_md": paths.logs_root / "latest_phase0_19_system_closeout.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase0-19-system-closeout-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase0_19_system_closeout_board.md",
    }


def capability_map() -> list[dict[str, str]]:
    return [
        {"phase": "0-1", "capability": "official lane, source registry, topic candidates, value scoring"},
        {"phase": "2-3", "capability": "brief/outline/draft, quality review, agent review, human exception queue"},
        {"phase": "4-5", "capability": "publishing prep, feedback memory, head media pattern learning"},
        {"phase": "6-8", "capability": "LLM infra, live safety, runtime store, cost guard, dry-run publish"},
        {"phase": "9-13", "capability": "WeChat workbench, chief editor, version loop, final review, metrics memory"},
        {"phase": "14-16", "capability": "methodology core, methodology generation, live pilot sidecars"},
        {"phase": "17-18", "capability": "image asset flow, article-with-images preview, WeChat copy pack"},
        {"phase": "19", "capability": "publishing calendar, content queue, weekly rhythm, archive, ops closeout"},
    ]


def build_phase0_19_system_closeout(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    phase19 = read_json(paths.logs_root / "latest_phase19_daily_ops_pipeline.json")
    closeout = read_json(paths.logs_root / "latest_content_ops_closeout.json")
    regression = read_json(paths.logs_root / "latest_publishing_checklist_regression.json")
    failure = read_json(paths.logs_root / "latest_content_ops_failure_handling.json")
    failure_summary = failure.get("summary") if isinstance(failure.get("summary"), dict) else {}
    regression_summary = regression.get("summary") if isinstance(regression.get("summary"), dict) else {}
    closeout_summary = closeout.get("summary") if isinstance(closeout.get("summary"), dict) else {}
    known_gaps = []
    if safe_int(failure_summary.get("blocker_count")):
        known_gaps.append("存在 BLOCKER 级运营失败处理项。")
    if regression_summary.get("regression_status") == "FAIL":
        known_gaps.append("发布 checklist regression 未通过。")
    if safe_int(closeout_summary.get("blocked_count")):
        known_gaps.append(f"内容队列仍有 {closeout_summary.get('blocked_count')} 个 blocked item。")
    known_gaps.extend([
        "真实公众号发布仍需人工复制，不接 API。",
        "发布后数据仍需人工录入，不自动抓取后台。",
        "图片生成仍需人工批准和外部生成，不自动调用图片模型。",
    ])
    readiness_status = "BLOCKED" if safe_int(failure_summary.get("blocker_count")) or regression_summary.get("regression_status") == "FAIL" else "READY_FOR_TRIAL"
    if readiness_status == "READY_FOR_TRIAL" and safe_int(failure_summary.get("warn_count")):
        readiness_status = "NEEDS_FIX"
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "capability_map": capability_map(),
        "daily_workflow": [
            "make phase20-daily",
            "打开 latest_wechat_workbench.html 或本地 server。",
            "先看今日运营，再看图文发布包和失败处理。",
            "人工决定是否发布；发布后人工记录 session 和 metrics。",
            "收盘前看 content ops closeout。",
        ],
        "manual_boundaries": [
            "最终发布必须人工确认。",
            "publish session 必须人工创建或更新。",
            "post-publish metrics 必须人工录入。",
            "图片使用必须经过人工视觉审查。",
        ],
        "automation_boundaries": [
            "不接公众号 API。",
            "不进入公众号草稿箱。",
            "不自动发布。",
            "不自动生成图片。",
            "不自动改 config/prompt/rules。",
        ],
        "known_gaps": known_gaps,
        "trial_readiness": {
            "status": readiness_status,
            "reasons": [
                f"phase19_status={phase19.get('status', 'UNKNOWN')}",
                f"regression_status={regression_summary.get('regression_status', 'UNKNOWN')}",
                f"failure_blockers={failure_summary.get('blocker_count', 0)}",
                f"failure_warns={failure_summary.get('warn_count', 0)}",
            ],
        },
        "next_phase_recommendation": "Phase 21：One-week Real Trial Execution v1",
        "policy": {"system_closeout_only": True, "no_auto_publish": True, "no_wechat_api": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    docs_path = repo_root / "docs/PHASE0_19_SYSTEM_CLOSEOUT.md"
    docs_path.write_text(render_markdown(payload), encoding="utf-8")
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    payload["outputs"]["docs_closeout"] = repo_relative(docs_path, repo_root)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    readiness = payload.get("trial_readiness") if isinstance(payload.get("trial_readiness"), dict) else {}
    capabilities = "\n".join(f"- Phase {item.get('phase')}: {item.get('capability')}" for item in payload.get("capability_map", []))
    workflow = "\n".join(f"- {item}" for item in payload.get("daily_workflow", []))
    gaps = "\n".join(f"- {item}" for item in payload.get("known_gaps", []))
    return f"""# Phase 0-19 System Closeout

## Trial Readiness

- status: `{readiness.get('status', 'UNKNOWN')}`
- reasons: `{'; '.join(readiness.get('reasons', []))}`

## Capability Map

{capabilities}

## Daily Workflow

{workflow}

## Known Gaps

{gaps}

## Next Phase

{payload.get('next_phase_recommendation')}
"""

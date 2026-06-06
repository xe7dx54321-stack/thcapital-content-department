"""Build a manual-first fallback search and backfill queue."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, detect_lane, markdown_table, stable_id


QUERY_TEMPLATES = {
    "official_ai_lab": "AI model product updates OpenAI Anthropic Google DeepMind Meta Microsoft this week",
    "model_release": "new LLM model release benchmark context window tool use this week",
    "agent_framework": "AI agent framework LangChain LlamaIndex AutoGen CrewAI release",
    "open_source": "GitHub trending AI agent LLM open source project this week",
    "paper_research": "arXiv LLM agents AI infra retrieval reasoning latest papers",
    "ai_infra": "NVIDIA AI infra GPU inference chip optical interconnect latest",
    "funding_startup": "AI agent startup funding Series A seed latest",
    "developer_community": "Hacker News Product Hunt AI agent developer tools today",
    "china_ai_media": "机器之心 量子位 新智元 AI Agent 大模型 今日",
    "global_ai_media": "AI agent model release VentureBeat Decoder latest",
    "social_weak_signal": "AI agents Reddit X developer complaints adoption signal",
}


METHOD_BY_LANE = {
    "official_ai_lab": "official_site",
    "model_release": "official_site",
    "agent_framework": "github",
    "open_source": "github",
    "paper_research": "arxiv",
    "ai_infra": "media_scan",
    "funding_startup": "search_query",
    "developer_community": "community_scan",
    "china_ai_media": "media_scan",
    "global_ai_media": "media_scan",
    "social_weak_signal": "community_scan",
}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__fallback-backfill-queue.json",
        "dated_md": paths.logs_root / f"{run_date}__fallback-backfill-queue.md",
        "latest_json": paths.logs_root / "latest_fallback_backfill_queue.json",
        "latest_md": paths.logs_root / "latest_fallback_backfill_queue.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__fallback-backfill-queue-board.md",
        "board_latest_md": paths.frontstage_root / "latest_fallback_backfill_queue_board.md",
    }


def task_for_lane(lane_id: str, reason: str, priority: str, target_sources: list[str] | None = None) -> dict[str, Any]:
    method = METHOD_BY_LANE.get(lane_id, "search_query")
    return {
        "task_id": stable_id("backfill", lane_id, reason),
        "lane_id": lane_id,
        "priority": priority,
        "reason": compact_text(reason, 240),
        "suggested_method": method,
        "suggested_query": QUERY_TEMPLATES.get(lane_id, f"{lane_id} AI latest"),
        "target_sources": target_sources or [],
        "expected_output": "raw_items" if method in {"official_site", "rss", "github", "arxiv"} else "manual_notes",
        "requires_api_key": False,
        "requires_manual": True,
        "do_not_auto_fetch": True,
    }


def build_fallback_backfill_queue(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    hot = read_json(paths.logs_root / "latest_hot_signal_capture.json")
    audit = read_json(paths.logs_root / "latest_source_coverage_gap_audit.json")
    expansion = read_json(paths.logs_root / "latest_high_value_source_expansion_plan.json")
    queue = read_json(paths.market_content_root / "07_publishing" / "latest_content_queue_priority.json")
    stable = read_json(paths.logs_root / "latest_stable_daily_ops.json")

    tasks_by_key: dict[str, dict[str, Any]] = {}
    for lane in list_payload(hot, "lanes"):
        lane_id = str(lane.get("lane_id") or "")
        status = str(lane.get("status") or "")
        if status in {"EMPTY", "MISSING_INPUT", "WEAK"}:
            priority = "HIGH" if lane_id in {"official_ai_lab", "agent_framework", "open_source", "paper_research", "ai_infra"} else "MEDIUM"
            tasks_by_key[lane_id] = task_for_lane(
                lane_id,
                f"Lane status is {status}; signal_count={lane.get('signal_count', 0)}.",
                priority,
                [str(item) for item in lane.get("missing_sources", []) if item][:5],
            )
    for gap in list_payload(audit, "coverage_gaps"):
        area = str(gap.get("area") or "")
        lane_id = detect_lane(area, area)
        if area == "papers":
            lane_id = "paper_research"
        elif area == "funding":
            lane_id = "funding_startup"
        elif area == "china_media":
            lane_id = "china_ai_media"
        elif area == "social_signal":
            lane_id = "social_weak_signal"
        severity = str(gap.get("severity") or "MEDIUM")
        priority = "HIGH" if severity == "HIGH" else "MEDIUM"
        tasks_by_key.setdefault(
            f"{lane_id}:{gap.get('gap_id')}",
            task_for_lane(lane_id, f"{gap.get('description')} Impact: {gap.get('impact_on_content')}", priority),
        )
    expansion_sources = list_payload(expansion, "source_candidates")
    for task in tasks_by_key.values():
        lane_id = str(task.get("lane_id"))
        if not task.get("target_sources"):
            task["target_sources"] = [
                item.get("source_name")
                for item in expansion_sources
                if detect_lane(item.get("category", ""), item.get("source_name", "")) == lane_id
            ][:5]
    queue_summary = queue.get("summary") if isinstance(queue.get("summary"), dict) else {}
    if safe_int(queue_summary.get("today")) == 0:
        tasks_by_key.setdefault(
            "queue:no_today",
            task_for_lane(
                "agent_framework",
                "Content queue has no TODAY items; upstream needs fresh high-conviction material before downstream promotion.",
                "HIGH",
            ),
        )
    if stable.get("status") in {"ACTIONABLE", "DEGRADED"}:
        tasks_by_key.setdefault(
            "stable:actionable",
            task_for_lane(
                "official_ai_lab",
                f"stable-daily-ops status is {stable.get('status')}; add source backfill before treating content queue as exhausted.",
                "MEDIUM",
            ),
        )
    tasks = sorted(tasks_by_key.values(), key=lambda item: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}.get(str(item.get("priority")), 3))
    summary = {
        "task_count": len(tasks),
        "high_priority": sum(1 for item in tasks if item.get("priority") == "HIGH"),
        "requires_manual": sum(1 for item in tasks if item.get("requires_manual")),
        "requires_api_key": sum(1 for item in tasks if item.get("requires_api_key")),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "backfill_tasks": tasks,
        "summary": summary,
        "policy": {
            "do_not_auto_fetch": True,
            "manual_first": True,
            "no_paid_or_login_bypass": True,
        },
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        {
            "priority": item.get("priority"),
            "lane": item.get("lane_id"),
            "method": item.get("suggested_method"),
            "manual": item.get("requires_manual"),
            "query": compact_text(item.get("suggested_query"), 80),
        }
        for item in list_payload(payload, "backfill_tasks")[:30]
    ]
    return f"""# Fallback Search & Backfill Queue

## Summary

- task_count: `{summary.get('task_count', 0)}`
- high_priority: `{summary.get('high_priority', 0)}`
- requires_manual: `{summary.get('requires_manual', 0)}`
- requires_api_key: `{summary.get('requires_api_key', 0)}`

## Backfill Tasks

{markdown_table(rows, ('priority', 'lane', 'method', 'manual', 'query'))}

## Boundary

Every task is manual-first and `do_not_auto_fetch=true`. This queue does not run searches, bypass logins, or modify source configuration.
"""

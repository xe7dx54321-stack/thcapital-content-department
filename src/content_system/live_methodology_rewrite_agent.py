"""Phase 16 live methodology rewrite pilot sidecar."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import (
    SCHEMA_VERSION,
    live_summary,
    make_id,
    render_policy_section,
    run_pilot_llm,
    short_json,
    status_for_response,
    write_pilot_payload,
)
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, today_token, utc_now


AGENT_NAME = "live_methodology_rewrite_agent"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "09_workbench_actions" / "versions"
    return {
        "dated_json": root / f"{run_date}__live-methodology-rewrite-pilot.json",
        "dated_md": root / f"{run_date}__live-methodology-rewrite-pilot.md",
        "latest_json": root / "latest_live_methodology_rewrite_pilot.json",
        "latest_md": root / "latest_live_methodology_rewrite_pilot.md",
    }


def lowest_issues(review: dict[str, Any]) -> list[str]:
    scores = review.get("scores") if isinstance(review.get("scores"), dict) else {}
    ordered = sorted(scores.items(), key=lambda item: item[1] if isinstance(item[1], (int, float)) else 99)
    focus = [str(key) for key, _ in ordered[:3]]
    focus.extend(str(item) for item in review.get("rewrite_priorities", [])[:3] if item)
    return list(dict.fromkeys(focus))[:5]


def rule_live_rewrite(draft: dict[str, Any], review: dict[str, Any], action: dict[str, Any], run_date: str) -> dict[str, Any]:
    source_id = str(review.get("article_id") or draft.get("draft_id") or "article")
    focus = lowest_issues(review) or ["strengthen_core_judgment", "improve_opening_tension", "add_risk_balance"]
    body = str(draft.get("body_markdown") or "")
    new_opening = f"{draft.get('opening') or draft.get('selected_title') or '这篇文章'}\n\n主编重写重点：{'; '.join(focus[:3])}。"
    rewritten = f"{body}\n\n## 方法论重写补强\n\n本版优先处理：{'; '.join(focus)}。所有改动都是 sidecar，不覆盖原稿，不自动发布。"
    return {
        "live_rewrite_id": make_id("lrew", run_date, source_id, action.get("action_id") or ""),
        "source_article_id": source_id,
        "source_action_id": action.get("action_id") or "",
        "rewrite_focus": focus,
        "new_title": draft.get("selected_title") or "方法论重写候选",
        "new_opening": new_opening,
        "new_body_markdown": rewritten,
        "change_summary": "按方法论低分项补强核心判断、开头张力、证据对齐和风险平衡。",
        "methodology_issues_addressed": focus,
        "remaining_issues": review.get("weaknesses") or [],
        "do_not_overwrite_original": True,
        "status": "GENERATED",
    }


def normalize_live_rewrites(response_json: dict[str, Any], fallback: list[dict[str, Any]], run_date: str) -> list[dict[str, Any]]:
    raw = response_json.get("rewrites")
    items = [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []
    if not items and isinstance(response_json.get("rewrite"), dict):
        items = [response_json["rewrite"]]
    if not items:
        return fallback
    result = []
    for index, item in enumerate(items):
        normalized = dict(item)
        normalized.setdefault("live_rewrite_id", make_id("lrew", run_date, normalized.get("source_article_id") or index))
        normalized.setdefault("do_not_overwrite_original", True)
        normalized.setdefault("status", "GENERATED")
        result.append(normalized)
    return result


def run_live_methodology_rewrite_pilot(paths: ProjectPaths, repo_root: Path, *, mode: str = "dry_run", limit: int = 1) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    draft_root = paths.market_content_root / "05_draft_packs"
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    action_root = paths.market_content_root / "09_workbench_actions"
    review_payload = read_json(draft_root / "latest_methodology_article_review.json")
    draft_payload = read_json(draft_root / "latest_methodology_content_drafts.json")
    action_payload = read_json(action_root / "latest_approved_actions.json")
    context_payload = read_json(paths.logs_root / "latest_chief_editor_methodology_context.json")
    rule_rewrite_payload = read_json(versions_root / "latest_methodology_rewrite_versions.json")
    reviews = list_payload(review_payload, "articles")
    drafts = list_payload(draft_payload, "drafts")
    actions = list_payload(action_payload, "actions")
    selected_review = sorted(reviews, key=lambda item: item.get("methodology_total_score") or 999)[0] if reviews else {}
    selected_draft = drafts[0] if drafts else {}
    selected_action = actions[0] if actions else {}
    outputs = output_paths(paths, run_date)
    response, provider_id, model, ready_status, ready_reason, cost_guard = run_pilot_llm(
        paths=paths,
        repo_root=repo_root,
        agent_name=AGENT_NAME,
        mode=mode,
        item_id=str(selected_review.get("article_id") or selected_draft.get("draft_id") or "none"),
        metadata={"review": selected_review, "draft": selected_draft, "action": selected_action},
        expected_output_schema={"rewrites": "array"},
        system_prompt="You are the live methodology rewrite agent. Return strict JSON only; sidecar output, no overwrite, no publish.",
        user_prompt=f"""Rewrite one draft by fixing the lowest methodology dimensions.

Review:
{short_json(selected_review)}

Rule draft:
{short_json(selected_draft)}

Approved action:
{short_json(selected_action)}

Chief editor methodology context:
{short_json(context_payload)}

Rule methodology rewrite versions:
{short_json(rule_rewrite_payload)}

Return JSON with top-level `rewrites` array.""",
        source_artifact="同行资本市场内容系统/05_draft_packs/latest_methodology_article_review.json",
        output_artifact="同行资本市场内容系统/09_workbench_actions/versions/latest_live_methodology_rewrite_pilot.json",
    )
    status = status_for_response(response, mode, ready_status)
    fallback = [rule_live_rewrite(selected_draft, selected_review, selected_action, run_date)] if status != "READY_CHECK_FAILED" and (selected_draft or selected_review) else []
    rewrites = normalize_live_rewrites(response.output_json, fallback, run_date)[:limit]
    summary = {"rewrite_count": len(rewrites), **live_summary(response, ready_status, ready_reason, cost_guard)}
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "agent_name": AGENT_NAME,
        "provider": provider_id,
        "model": model,
        "mode": mode,
        "status": status,
        "rewrites": rewrites,
        "summary": summary,
        "policy": {"sidecar_only": True, "do_not_overwrite_original": True, "do_not_replace_existing_rewrite_versions": True},
    }
    write_pilot_payload(payload, render_markdown(payload), outputs, repo_root)
    return payload, outputs


def escape_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('live_rewrite_id')}` | `{item.get('source_article_id')}` | `{item.get('status')}` | {escape_cell(item.get('change_summary') or '')} |"
        for item in list_payload(payload, "rewrites")
    ) or "| - | - | - | No live rewrite sidecar |"
    return f"""# Live Methodology Rewrite Pilot

## Summary

- status: `{payload.get('status')}`
- mode: `{payload.get('mode')}`
- rewrite_count: `{summary.get('rewrite_count', 0)}`
- live_attempted: `{summary.get('live_attempted')}`
- live_succeeded: `{summary.get('live_succeeded')}`
- ready_check_status: `{summary.get('ready_check_status')}`

| Live Rewrite | Source Article | Status | Change Summary |
|---|---|---|---|
{rows}

{render_policy_section()}
"""

"""Phase 16 live methodology brief pilot sidecar."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import (
    SCHEMA_VERSION,
    bullet_list,
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


AGENT_NAME = "live_methodology_brief_agent"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__live-methodology-brief-pilot.json",
        "dated_md": root / f"{run_date}__live-methodology-brief-pilot.md",
        "latest_json": root / "latest_live_methodology_brief_pilot.json",
        "latest_md": root / "latest_live_methodology_brief_pilot.md",
    }


def rule_live_brief(topic: dict[str, Any], rule_brief: dict[str, Any], run_date: str) -> dict[str, Any]:
    topic_id = str(topic.get("topic_id") or rule_brief.get("topic_id") or "topic")
    title = str(topic.get("title") or rule_brief.get("title") or "未命名选题")
    return {
        "live_brief_id": make_id("lbrief", run_date, topic_id, title),
        "source_topic_id": topic_id,
        "source_methodology_brief_id": rule_brief.get("brief_id") or "",
        "title": title,
        "core_question": rule_brief.get("core_question") or f"{title} 到底代表什么变化？",
        "core_judgment": rule_brief.get("core_judgment") or topic.get("core_judgment") or f"{title} 值得写的前提，是它改变了读者对 AI/Agent 主线的判断。",
        "why_now": rule_brief.get("why_now") or topic.get("why_now") or "当前窗口期需要更多一手证据确认。",
        "expectation_gap": rule_brief.get("expectation_gap") or "市场可能把它视作普通更新，但文章需要拆出预期差。",
        "industry_chain_impact": rule_brief.get("industry_chain_impact") or "需要明确影响产品入口、开发者生态或产业链定价。",
        "reader_value": rule_brief.get("reader_value") or topic.get("reader_value_summary") or "帮助读者形成可复述的投资/产业判断。",
        "evidence_plan": rule_brief.get("evidence_plan") or [],
        "counterarguments": rule_brief.get("counterarguments") or ["这可能只是局部信号，仍需观察连续性。"],
        "visual_opportunities": rule_brief.get("visual_opportunities") or ["framework_diagram: 展示核心判断框架。"],
        "improvements_over_rule_brief": [
            "强化 core question / core judgment 的直接对应关系。",
            "把读者收益和产业链影响显式拆出。",
        ],
        "risks": rule_brief.get("risks") or ["证据不足时不能做绝对化结论。"],
        "status": "GENERATED",
    }


def normalize_live_briefs(response_json: dict[str, Any], fallback: list[dict[str, Any]], run_date: str) -> list[dict[str, Any]]:
    raw = response_json.get("briefs")
    items = [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []
    if not items and isinstance(response_json.get("brief"), dict):
        items = [response_json["brief"]]
    if not items:
        return fallback
    result = []
    for index, item in enumerate(items):
        normalized = dict(item)
        normalized.setdefault("live_brief_id", make_id("lbrief", run_date, normalized.get("source_topic_id") or index))
        normalized.setdefault("status", "GENERATED")
        result.append(normalized)
    return result


def build_system_prompt() -> str:
    return (
        "You are the methodology brief agent for a Chinese WeChat editorial system. "
        "Return strict JSON only. Improve the methodology brief while preserving policy: sidecar output, no publishing."
    )


def build_user_prompt(topic: dict[str, Any], rule_brief: dict[str, Any], context: dict[str, Any]) -> str:
    return f"""Create one stronger methodology-aware brief.

Topic:
{short_json(topic)}

Rule-based brief:
{short_json(rule_brief)}

Methodology context:
{short_json(context)}

Return JSON with a top-level `briefs` array matching the required schema."""


def run_live_methodology_brief_pilot(paths: ProjectPaths, repo_root: Path, *, mode: str = "dry_run", limit: int = 1) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    topic_payload = read_json(paths.market_content_root / "03_topic_candidates" / "latest_methodology_topic_scores.json")
    brief_payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_methodology_content_briefs.json")
    context_payload = read_json(paths.logs_root / "latest_chief_editor_methodology_context.json")
    alignment_payload = read_json(paths.logs_root / "latest_methodology_performance_alignment.json")
    topics = list_payload(topic_payload, "topics")[: max(1, limit)]
    rule_briefs = list_payload(brief_payload, "briefs")
    rule_by_topic = {str(item.get("topic_id")): item for item in rule_briefs if item.get("topic_id")}
    selected_topic = topics[0] if topics else {}
    selected_rule = rule_by_topic.get(str(selected_topic.get("topic_id") or ""), rule_briefs[0] if rule_briefs else {})
    outputs = output_paths(paths, run_date)
    response, provider_id, model, ready_status, ready_reason, cost_guard = run_pilot_llm(
        paths=paths,
        repo_root=repo_root,
        agent_name=AGENT_NAME,
        mode=mode,
        item_id=str(selected_topic.get("topic_id") or "none"),
        metadata={"topic": selected_topic, "rule_brief": selected_rule},
        expected_output_schema={"briefs": "array"},
        system_prompt=build_system_prompt(),
        user_prompt=build_user_prompt(selected_topic, selected_rule, {"chief_editor": context_payload, "alignment": alignment_payload}),
        source_artifact="同行资本市场内容系统/05_draft_packs/latest_methodology_content_briefs.json",
        output_artifact="同行资本市场内容系统/05_draft_packs/latest_live_methodology_brief_pilot.json",
    )
    status = status_for_response(response, mode, ready_status)
    fallback = [rule_live_brief(topic, rule_by_topic.get(str(topic.get("topic_id") or ""), selected_rule), run_date) for topic in topics] if status != "READY_CHECK_FAILED" else []
    briefs = normalize_live_briefs(response.output_json, fallback, run_date)[:limit]
    summary = {"brief_count": len(briefs), **live_summary(response, ready_status, ready_reason, cost_guard)}
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "agent_name": AGENT_NAME,
        "provider": provider_id,
        "model": model,
        "mode": mode,
        "status": status,
        "briefs": briefs,
        "summary": summary,
        "policy": {"sidecar_only": True, "do_not_replace_rule_briefs": True, "do_not_publish": True},
    }
    write_pilot_payload(payload, render_markdown(payload), outputs, repo_root)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    def escape_cell(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    rows = "\n".join(
        f"| `{item.get('live_brief_id')}` | `{item.get('source_topic_id')}` | `{item.get('status')}` | {escape_cell(item.get('title') or '')} |"
        for item in list_payload(payload, "briefs")
    ) or "| - | - | - | No live brief sidecar |"
    return f"""# Live Methodology Brief Pilot

## Summary

- status: `{payload.get('status')}`
- mode: `{payload.get('mode')}`
- brief_count: `{summary.get('brief_count', 0)}`
- live_attempted: `{summary.get('live_attempted')}`
- live_succeeded: `{summary.get('live_succeeded')}`
- ready_check_status: `{summary.get('ready_check_status')}`
- ready_check_reason: `{summary.get('ready_check_reason')}`

| Live Brief | Source Topic | Status | Title |
|---|---|---|---|
{rows}

## Improvements

{bullet_list([item for brief in list_payload(payload, 'briefs') for item in brief.get('improvements_over_rule_brief', [])][:8])}

{render_policy_section()}
"""

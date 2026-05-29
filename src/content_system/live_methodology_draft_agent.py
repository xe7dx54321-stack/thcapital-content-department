"""Phase 16 live methodology draft pilot sidecar."""

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


AGENT_NAME = "live_methodology_draft_agent"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__live-methodology-draft-pilot.json",
        "dated_md": root / f"{run_date}__live-methodology-draft-pilot.md",
        "latest_json": root / "latest_live_methodology_draft_pilot.json",
        "latest_md": root / "latest_live_methodology_draft_pilot.md",
    }


def by_id(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(key)): item for item in items if item.get(key)}


def rule_live_draft(draft: dict[str, Any], brief: dict[str, Any], outline: dict[str, Any], run_date: str) -> dict[str, Any]:
    title = str(draft.get("selected_title") or brief.get("title") or "AI/Agent 方法论草稿")
    opening = str(draft.get("opening") or brief.get("core_judgment") or title)
    body = str(draft.get("body_markdown") or "")
    enhanced_body = body
    if "## 文章主线" not in enhanced_body:
        enhanced_body += f"\n\n## 文章主线\n\n这篇稿件的核心不是复述材料，而是回答：{brief.get('core_question') or title}。\n"
    if "## 发布前检查" not in enhanced_body:
        enhanced_body += "\n\n## 发布前检查\n\n本稿是 live pilot sidecar，不覆盖原稿，不自动发布；证据、风险和标题承诺仍需人工确认。\n"
    return {
        "live_draft_id": make_id("ldraft", run_date, draft.get("draft_id") or title),
        "source_draft_id": draft.get("draft_id") or "",
        "source_outline_id": draft.get("outline_id") or outline.get("outline_id") or "",
        "title_options": draft.get("title_options") or [title],
        "selected_title": title,
        "opening": opening,
        "body_markdown": enhanced_body,
        "closing": draft.get("closing") or outline.get("closing_framework") or "形成一句可复述的判断框架。",
        "visual_placeholders": draft.get("visual_slots") or outline.get("sections") or [],
        "methodology_self_check": draft.get("methodology_self_check") or {},
        "improvements_over_rule_draft": [
            "补充文章主线说明，避免材料堆叠。",
            "保留人工发布和证据核验边界。",
        ],
        "remaining_weaknesses": draft.get("generic_language_flags") or [],
        "do_not_overwrite_original": True,
        "status": "GENERATED",
    }


def normalize_live_drafts(response_json: dict[str, Any], fallback: list[dict[str, Any]], run_date: str) -> list[dict[str, Any]]:
    raw = response_json.get("drafts")
    items = [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []
    if not items and isinstance(response_json.get("draft"), dict):
        items = [response_json["draft"]]
    if not items:
        return fallback
    result = []
    for index, item in enumerate(items):
        normalized = dict(item)
        normalized.setdefault("live_draft_id", make_id("ldraft", run_date, normalized.get("source_draft_id") or index))
        normalized.setdefault("do_not_overwrite_original", True)
        normalized.setdefault("status", "GENERATED")
        result.append(normalized)
    return result


def run_live_methodology_draft_pilot(paths: ProjectPaths, repo_root: Path, *, mode: str = "dry_run", limit: int = 1) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    root = paths.market_content_root / "05_draft_packs"
    brief_payload = read_json(root / "latest_methodology_content_briefs.json")
    outline_payload = read_json(root / "latest_methodology_content_outlines.json")
    draft_payload = read_json(root / "latest_methodology_content_drafts.json")
    review_payload = read_json(root / "latest_methodology_article_review.json")
    visual_payload = read_json(root / "latest_article_visual_plans.json")
    request_payload = read_json(root / "latest_image_asset_requests.json")
    drafts = list_payload(draft_payload, "drafts")[: max(1, limit)]
    briefs = by_id(list_payload(brief_payload, "briefs"), "brief_id")
    outlines = by_id(list_payload(outline_payload, "outlines"), "outline_id")
    selected = drafts[0] if drafts else {}
    selected_brief = briefs.get(str(selected.get("brief_id") or ""), {})
    selected_outline = outlines.get(str(selected.get("outline_id") or ""), {})
    outputs = output_paths(paths, run_date)
    response, provider_id, model, ready_status, ready_reason, cost_guard = run_pilot_llm(
        paths=paths,
        repo_root=repo_root,
        agent_name=AGENT_NAME,
        mode=mode,
        item_id=str(selected.get("draft_id") or "none"),
        metadata={"draft": selected, "brief": selected_brief, "outline": selected_outline},
        expected_output_schema={"drafts": "array"},
        system_prompt="You are the live methodology draft agent. Return strict JSON only; sidecar output, no overwrite, no publish.",
        user_prompt=f"""Write one stronger WeChat draft sidecar from this methodology package.

Brief:
{short_json(selected_brief)}

Outline:
{short_json(selected_outline)}

Rule draft:
{short_json(selected)}

Article review:
{short_json(review_payload)}

Visual plan:
{short_json(visual_payload)}

Image requests:
{short_json(request_payload)}

Return JSON with top-level `drafts` array.""",
        source_artifact="同行资本市场内容系统/05_draft_packs/latest_methodology_content_drafts.json",
        output_artifact="同行资本市场内容系统/05_draft_packs/latest_live_methodology_draft_pilot.json",
    )
    status = status_for_response(response, mode, ready_status)
    fallback = [rule_live_draft(draft, briefs.get(str(draft.get("brief_id") or ""), {}), outlines.get(str(draft.get("outline_id") or ""), {}), run_date) for draft in drafts] if status != "READY_CHECK_FAILED" else []
    live_drafts = normalize_live_drafts(response.output_json, fallback, run_date)[:limit]
    summary = {"draft_count": len(live_drafts), **live_summary(response, ready_status, ready_reason, cost_guard)}
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "agent_name": AGENT_NAME,
        "provider": provider_id,
        "model": model,
        "mode": mode,
        "status": status,
        "drafts": live_drafts,
        "summary": summary,
        "policy": {"sidecar_only": True, "do_not_overwrite_original": True, "do_not_publish": True, "do_not_generate_images": True},
    }
    write_pilot_payload(payload, render_markdown(payload), outputs, repo_root)
    return payload, outputs


def escape_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('live_draft_id')}` | `{item.get('source_draft_id')}` | `{item.get('status')}` | {escape_cell(item.get('selected_title') or '')} |"
        for item in list_payload(payload, "drafts")
    ) or "| - | - | - | No live draft sidecar |"
    return f"""# Live Methodology Draft Pilot

## Summary

- status: `{payload.get('status')}`
- mode: `{payload.get('mode')}`
- draft_count: `{summary.get('draft_count', 0)}`
- live_attempted: `{summary.get('live_attempted')}`
- live_succeeded: `{summary.get('live_succeeded')}`
- ready_check_status: `{summary.get('ready_check_status')}`

| Live Draft | Source Draft | Status | Title |
|---|---|---|---|
{rows}

{render_policy_section()}
"""

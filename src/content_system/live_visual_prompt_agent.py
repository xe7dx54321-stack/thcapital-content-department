"""Phase 16 live visual prompt pilot sidecar."""

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


AGENT_NAME = "live_visual_prompt_agent"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__live-visual-prompt-pilot.json",
        "dated_md": root / f"{run_date}__live-visual-prompt-pilot.md",
        "latest_json": root / "latest_live_visual_prompt_pilot.json",
        "latest_md": root / "latest_live_visual_prompt_pilot.md",
    }


def rule_live_prompt(request: dict[str, Any], run_date: str) -> dict[str, Any]:
    visual_type = str(request.get("visual_type") or "framework_diagram")
    strategy = str(request.get("source_strategy") or "manual_design_request")
    design_brief = str(request.get("design_brief") or "")
    prompt = str(request.get("image_prompt") or "")
    if not prompt:
        prompt = (
            "A premium restrained Chinese WeChat editorial information visual. "
            f"Visual type: {visual_type}. Design brief: {design_brief}. "
            "Use warm paper background, charcoal typography, deep green accents, clean hierarchy, mobile-readable layout, no generic AI robot."
        )
    return {
        "live_visual_prompt_id": make_id("lvprompt", run_date, request.get("request_id") or request.get("visual_id") or visual_type),
        "source_request_id": request.get("request_id") or "",
        "visual_type": visual_type,
        "source_strategy": strategy,
        "image_prompt": prompt,
        "negative_prompt": request.get("negative_prompt") or "generic robot, blue neon chip, sci-fi glow, clutter, unreadable text",
        "design_brief": design_brief or "人工确认信息层级、版权和移动端可读性后再生成。",
        "layout_guidance": "Use a clear title, 2-4 labeled blocks, restrained arrows, and enough whitespace for mobile reading.",
        "wechat_usage_note": "Use only after human visual review. Do not upload automatically.",
        "copyright_note": request.get("copyright_note") or "No unknown-copyright assets. Human source check required.",
        "recommended_tool": request.get("recommended_tool") or "manual_design",
        "do_not_auto_generate": True,
        "human_review_required": True,
        "status": "GENERATED",
    }


def normalize_live_prompts(response_json: dict[str, Any], fallback: list[dict[str, Any]], run_date: str) -> list[dict[str, Any]]:
    raw = response_json.get("visual_prompts")
    items = [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []
    if not items and isinstance(response_json.get("visual_prompt"), dict):
        items = [response_json["visual_prompt"]]
    if not items:
        return fallback
    result = []
    for index, item in enumerate(items):
        normalized = dict(item)
        normalized.setdefault("live_visual_prompt_id", make_id("lvprompt", run_date, normalized.get("source_request_id") or index))
        normalized.setdefault("do_not_auto_generate", True)
        normalized.setdefault("human_review_required", True)
        normalized.setdefault("status", "GENERATED")
        result.append(normalized)
    return result


def run_live_visual_prompt_pilot(paths: ProjectPaths, repo_root: Path, *, mode: str = "dry_run", limit: int = 3) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    root = paths.market_content_root / "05_draft_packs"
    methodology = read_json(repo_root / "config" / "article_visual_methodology.json")
    plan_payload = read_json(root / "latest_article_visual_plans.json")
    request_payload = read_json(root / "latest_image_asset_requests.json")
    draft_payload = read_json(root / "latest_methodology_content_drafts.json")
    final_payload = read_json(paths.market_content_root / "07_publishing" / "latest_final_article_candidates.json")
    requests = list_payload(request_payload, "requests")[: max(1, limit)]
    selected = requests[0] if requests else {}
    outputs = output_paths(paths, run_date)
    response, provider_id, model, ready_status, ready_reason, cost_guard = run_pilot_llm(
        paths=paths,
        repo_root=repo_root,
        agent_name=AGENT_NAME,
        mode=mode,
        item_id=str(selected.get("request_id") or "none"),
        metadata={"request": selected},
        expected_output_schema={"visual_prompts": "array"},
        system_prompt="You are the live visual prompt agent. Return strict JSON only. Do not generate images.",
        user_prompt=f"""Improve image prompts and design briefs for WeChat editorial visuals.

Visual methodology:
{short_json(methodology)}

Visual plans:
{short_json(plan_payload)}

Rule image asset requests:
{short_json({'requests': requests})}

Methodology drafts:
{short_json(draft_payload)}

Final candidates:
{short_json(final_payload)}

Return JSON with top-level `visual_prompts` array.""",
        source_artifact="同行资本市场内容系统/05_draft_packs/latest_image_asset_requests.json",
        output_artifact="同行资本市场内容系统/05_draft_packs/latest_live_visual_prompt_pilot.json",
    )
    status = status_for_response(response, mode, ready_status)
    fallback = [rule_live_prompt(item, run_date) for item in requests] if status != "READY_CHECK_FAILED" else []
    prompts = normalize_live_prompts(response.output_json, fallback, run_date)[:limit]
    summary = {
        "visual_prompt_count": len(prompts),
        "ready_for_human_review": sum(1 for item in prompts if item.get("human_review_required")),
        **live_summary(response, ready_status, ready_reason, cost_guard),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "agent_name": AGENT_NAME,
        "provider": provider_id,
        "model": model,
        "mode": mode,
        "status": status,
        "visual_prompts": prompts,
        "summary": summary,
        "policy": {"do_not_auto_generate": True, "do_not_call_image_model": True, "human_review_required": True},
    }
    write_pilot_payload(payload, render_markdown(payload), outputs, repo_root)
    return payload, outputs


def escape_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('live_visual_prompt_id')}` | `{item.get('source_request_id')}` | `{item.get('visual_type')}` | `{item.get('recommended_tool')}` | `{item.get('do_not_auto_generate')}` |"
        for item in list_payload(payload, "visual_prompts")
    ) or "| - | - | - | - | true |"
    return f"""# Live Visual Prompt Pilot

## Summary

- status: `{payload.get('status')}`
- mode: `{payload.get('mode')}`
- visual_prompt_count: `{summary.get('visual_prompt_count', 0)}`
- ready_for_human_review: `{summary.get('ready_for_human_review', 0)}`
- live_attempted: `{summary.get('live_attempted')}`
- live_succeeded: `{summary.get('live_succeeded')}`
- ready_check_status: `{summary.get('ready_check_status')}`

| Live Visual Prompt | Source Request | Type | Tool | Do Not Auto Generate |
|---|---|---|---|---|
{rows}

{render_policy_section()}
"""

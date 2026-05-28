"""Build image prompts and asset requests from visual plans."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__image-asset-requests.json",
        "dated_md": root / f"{run_date}__image-asset-requests.md",
        "latest_json": root / "latest_image_asset_requests.json",
        "latest_md": root / "latest_image_asset_requests.md",
    }


def make_id(prefix: str, run_date: str, *parts: object) -> str:
    digest = hashlib.sha1("|".join(str(part) for part in (run_date, *parts)).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{run_date}_{digest}"


def recommended_tool(strategy: str) -> str:
    return {
        "generated_concept_visual": "gpt-image-2",
        "manual_design_request": "manual_design",
        "evidence_snapshot": "screenshot",
        "internal_chart": "internal_chart",
    }.get(strategy, "manual_design")


def asset_status(strategy: str) -> str:
    if strategy == "generated_concept_visual":
        return "READY_FOR_GENERATION"
    if strategy in {"manual_design_request", "evidence_snapshot"}:
        return "NEEDS_HUMAN"
    if strategy == "internal_chart":
        return "REQUESTED"
    return "HOLD"


def prompt_for(visual: dict[str, Any], title: str) -> str:
    visual_type = str(visual.get("visual_type") or "framework_diagram")
    job = str(visual.get("information_job") or "")
    claim = str(visual.get("supports_claim") or title)
    return (
        "A calm premium Chinese editorial visual for a WeChat article. "
        f"Visual type: {visual_type}. Article title: {title}. "
        f"Information job: {job}. Core claim supported: {claim}. "
        "Use clear hierarchy, warm paper-like background, restrained deep green and charcoal accents, "
        "no generic robots, no sci-fi glow, no clutter, readable on mobile."
    )


def build_requests(paths: ProjectPaths) -> tuple[dict[str, Any], dict[str, Path]]:
    plan_payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_article_visual_plans.json")
    run_date = str(plan_payload.get("run_date") or today_token()).replace("-", "")[:8]
    requests = []
    for plan in list_payload(plan_payload, "visual_plans"):
        title = str(plan.get("title") or "")
        for visual in plan.get("visuals", []) if isinstance(plan.get("visuals"), list) else []:
            if not isinstance(visual, dict):
                continue
            strategy = str(visual.get("source_strategy") or "manual_design_request")
            requests.append(
                {
                    "request_id": make_id("imgreq", run_date, visual.get("visual_id"), plan.get("article_id")),
                    "visual_id": visual.get("visual_id") or "",
                    "article_id": plan.get("article_id") or "",
                    "visual_type": visual.get("visual_type") or "",
                    "source_strategy": strategy,
                    "asset_status": asset_status(strategy),
                    "image_prompt": prompt_for(visual, title) if strategy == "generated_concept_visual" else "",
                    "negative_prompt": "generic robot, blue neon chip, sci-fi glow, unreadable text, stock photo feel, clutter",
                    "design_brief": f"{visual.get('placement')}: {visual.get('information_job')} 支撑判断：{visual.get('supports_claim')}",
                    "copyright_note": "Do not use unknown-copyright images. Human review required before use.",
                    "recommended_tool": recommended_tool(strategy),
                    "do_not_auto_generate": True,
                    "human_review_required": True,
                }
            )
    summary = {
        "request_count": len(requests),
        "ready_for_generation": sum(1 for item in requests if item.get("asset_status") == "READY_FOR_GENERATION"),
        "needs_human": sum(1 for item in requests if item.get("asset_status") == "NEEDS_HUMAN"),
        "hold": sum(1 for item in requests if item.get("asset_status") == "HOLD"),
    }
    warnings = [] if requests else ["No visual plan requests found; run make article-visual-plans first."]
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "requests": requests, "summary": summary, "warnings": warnings, "policy": {"do_not_auto_generate": True, "human_review_required": True}}
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('request_id')}` | `{item.get('visual_type')}` | `{item.get('source_strategy')}` | `{item.get('asset_status')}` | `{item.get('recommended_tool')}` |"
        for item in list_payload(payload, "requests")
    ) or "| - | - | - | - | - |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Image Asset Requests

## Summary

- request_count: `{summary.get('request_count', 0)}`
- ready_for_generation: `{summary.get('ready_for_generation', 0)}`
- needs_human: `{summary.get('needs_human', 0)}`
- hold: `{summary.get('hold', 0)}`
- do_not_auto_generate: `true`

| Request | Visual Type | Strategy | Status | Tool |
|---|---|---|---|---|
{rows}
"""

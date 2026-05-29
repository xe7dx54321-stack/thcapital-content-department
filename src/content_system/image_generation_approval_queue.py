"""Manual approval queue for future image generation requests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__image-generation-approval-queue.json",
        "dated_md": root / f"{run_date}__image-generation-approval-queue.md",
        "latest_json": root / "latest_image_generation_approval_queue.json",
        "latest_md": root / "latest_image_generation_approval_queue.md",
    }


def summary_for(requests: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "request_count": len(requests),
        "pending": sum(1 for item in requests if item.get("approval_status") == "PENDING"),
        "approved": sum(1 for item in requests if item.get("approval_status") == "APPROVED"),
        "rejected": sum(1 for item in requests if item.get("approval_status") == "REJECTED"),
        "deferred": sum(1 for item in requests if item.get("approval_status") == "DEFERRED"),
    }


def build_queue(paths: ProjectPaths) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    draft_root = paths.market_content_root / "05_draft_packs"
    existing = read_json(draft_root / "latest_image_generation_approval_queue.json")
    existing_by_source = {str(item.get("source_request_id")): item for item in list_payload(existing, "requests") if item.get("source_request_id")}
    request_payload = read_json(draft_root / "latest_image_asset_requests.json")
    live_payload = read_json(draft_root / "latest_live_visual_prompt_pilot.json")
    live_by_request = {str(item.get("source_request_id")): item for item in list_payload(live_payload, "visual_prompts") if item.get("source_request_id")}
    requests: list[dict[str, Any]] = []
    for item in list_payload(request_payload, "requests"):
        source_id = str(item.get("request_id") or "")
        live = live_by_request.get(source_id, {})
        previous = existing_by_source.get(source_id, {})
        status = previous.get("approval_status") or "PENDING"
        requests.append(
            {
                "approval_id": previous.get("approval_id") or make_id("imgappr", run_date, source_id),
                "source_request_id": source_id,
                "source_live_visual_prompt_id": live.get("live_visual_prompt_id") or "",
                "article_id": item.get("article_id") or "",
                "visual_type": live.get("visual_type") or item.get("visual_type") or "",
                "image_prompt": live.get("image_prompt") or item.get("image_prompt") or "",
                "design_brief": live.get("design_brief") or item.get("design_brief") or "",
                "recommended_tool": live.get("recommended_tool") or item.get("recommended_tool") or "manual_design",
                "approval_status": status,
                "human_note": previous.get("human_note") or "",
                "do_not_auto_generate": True,
                "generation_allowed": status == "APPROVED",
                "created_at": previous.get("created_at") or utc_now(),
            }
        )
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "requests": requests,
        "summary": summary_for(requests),
        "policy": {"do_not_auto_generate": True, "approval_does_not_generate_images": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def update_approval(paths: ProjectPaths, approval_id: str, status: str, note: str) -> tuple[dict[str, Any], dict[str, Path]]:
    payload, _ = build_queue(paths)
    run_date = str(payload.get("run_date") or today_token())
    requests = list_payload(payload, "requests")
    for item in requests:
        if item.get("approval_id") == approval_id:
            item["approval_status"] = status
            item["human_note"] = note
            item["generation_allowed"] = status == "APPROVED"
            item["do_not_auto_generate"] = True
    payload["requests"] = requests
    payload["summary"] = summary_for(requests)
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('approval_id')}` | `{item.get('source_request_id')}` | `{item.get('visual_type')}` | `{item.get('approval_status')}` | `{item.get('generation_allowed')}` |"
        for item in list_payload(payload, "requests")
    ) or "| - | - | - | - | false |"
    return f"""# Image Generation Approval Queue

## Summary

- request_count: `{summary.get('request_count', 0)}`
- pending: `{summary.get('pending', 0)}`
- approved: `{summary.get('approved', 0)}`
- rejected: `{summary.get('rejected', 0)}`
- deferred: `{summary.get('deferred', 0)}`
- do_not_auto_generate: `true`

| Approval | Source Request | Visual Type | Status | Generation Allowed Later |
|---|---|---|---|---|
{rows}

Even APPROVED items do not generate images in Phase 16.
"""

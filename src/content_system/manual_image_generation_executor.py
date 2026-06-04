"""Convert approved image generation requests into manual generation tasks."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "08_assets"
    return {
        "dated_json": root / f"{run_date}__manual-image-generation-tasks.json",
        "dated_md": root / f"{run_date}__manual-image-generation-tasks.md",
        "latest_json": root / "latest_manual_image_generation_tasks.json",
        "latest_md": root / "latest_manual_image_generation_tasks.md",
    }


def slug(value: Any, fallback: str = "asset") -> str:
    text = re.sub(r"[^a-zA-Z0-9_\-\u4e00-\u9fff]+", "-", str(value or "")).strip("-")
    return text[:80] or fallback


def expected_path(paths: ProjectPaths, request: dict[str, Any], task_id: str) -> str:
    article = slug(request.get("article_id"), "article")
    visual = slug(request.get("visual_type"), "visual")
    return f"{paths.market_content_root.name}/08_assets/images/{article}__{visual}__{task_id}.png"


def build_manual_image_generation_tasks(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    draft_root = paths.market_content_root / "05_draft_packs"
    approval_payload = read_json(draft_root / "latest_image_generation_approval_queue.json")
    tasks: list[dict[str, Any]] = []
    skipped = 0
    for request in list_payload(approval_payload, "requests"):
        if request.get("approval_status") != "APPROVED":
            skipped += 1
            continue
        task_id = make_id("imgtask", run_date, request.get("approval_id"), request.get("source_request_id"))
        tool = request.get("recommended_tool") or "manual_design"
        status = "READY_FOR_MANUAL_GENERATION" if request.get("image_prompt") or request.get("design_brief") else "NEEDS_HUMAN_INPUT"
        task = {
            "task_id": task_id,
            "approval_id": request.get("approval_id") or "",
            "source_request_id": request.get("source_request_id") or "",
            "article_id": request.get("article_id") or "",
            "visual_type": request.get("visual_type") or "",
            "recommended_tool": tool,
            "image_prompt": request.get("image_prompt") or "",
            "negative_prompt": request.get("negative_prompt") or "",
            "design_brief": request.get("design_brief") or "",
            "generation_status": status,
            "manual_steps": manual_steps_for(tool),
            "expected_asset_path": expected_path(paths, request, task_id),
            "do_not_auto_generate": True,
            "created_at": utc_now(),
        }
        tasks.append(task)
    summary = {
        "task_count": len(tasks),
        "ready_for_manual_generation": sum(1 for item in tasks if item.get("generation_status") == "READY_FOR_MANUAL_GENERATION"),
        "needs_human_input": sum(1 for item in tasks if item.get("generation_status") == "NEEDS_HUMAN_INPUT"),
        "hold": sum(1 for item in tasks if item.get("generation_status") == "HOLD"),
        "skipped_unapproved": skipped,
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "tasks": tasks,
        "summary": summary,
        "policy": {"do_not_auto_generate": True, "no_image_model_called": True, "metadata_only": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def manual_steps_for(tool: str) -> list[str]:
    if tool == "gpt-image-2":
        return [
            "Human reviews the prompt and copyright note.",
            "Human explicitly approves future image generation outside this Phase 17 pipeline.",
            "Human places the generated file under 同行资本市场内容系统/08_assets/images/.",
            "Human registers the asset path with update_image_asset_library.py --mark-available.",
        ]
    if tool == "screenshot":
        return [
            "Human captures or prepares the source screenshot.",
            "Human confirms source attribution and copyright safety.",
            "Human places the asset under 同行资本市场内容系统/08_assets/images/.",
            "Human registers the asset path in the image asset library.",
        ]
    return [
        "Human or designer uses the design brief to prepare the asset.",
        "Human confirms it supports the article claim and is readable on mobile.",
        "Human places the asset under 同行资本市场内容系统/08_assets/images/.",
        "Human registers the asset path in the image asset library.",
    ]


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('task_id')}` | `{item.get('approval_id')}` | `{item.get('visual_type')}` | `{item.get('generation_status')}` | `{item.get('expected_asset_path')}` |"
        for item in list_payload(payload, "tasks")
    ) or "| - | - | - | - | No approved image generation requests |"
    return f"""# Manual Image Generation Tasks

## Summary

- task_count: `{summary.get('task_count', 0)}`
- ready_for_manual_generation: `{summary.get('ready_for_manual_generation', 0)}`
- needs_human_input: `{summary.get('needs_human_input', 0)}`
- hold: `{summary.get('hold', 0)}`
- no_image_model_called: `true`

| Task | Approval | Visual Type | Status | Expected Asset Path |
|---|---|---|---|---|
{rows}
"""

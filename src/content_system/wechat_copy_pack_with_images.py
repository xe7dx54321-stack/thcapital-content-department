"""Build manual WeChat copy packs with image slot markers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__wechat-copy-pack-with-images.json",
        "dated_md": root / f"{run_date}__wechat-copy-pack-with-images.md",
        "latest_json": root / "latest_wechat_copy_pack_with_images.json",
        "latest_md": root / "latest_wechat_copy_pack_with_images.md",
    }


def manual_copy_steps() -> list[str]:
    return [
        "打开微信公众号后台。",
        "新建图文消息。",
        "复制标题。",
        "复制正文。",
        "根据 [[IMAGE_SLOT_X]] 标记插入图片。",
        "删除 slot marker。",
        "检查手机预览。",
        "检查图片清晰度、版权说明、正文断点。",
        "人工决定是否发布。",
    ]


def visual_copy_steps(slots: list[dict[str, Any]]) -> list[str]:
    if not slots:
        return ["当前没有图片槽位；人工确认是否需要首图或框架图。"]
    return [
        f"{slot.get('slot_marker')}: {slot.get('copy_instruction')} 资产状态={slot.get('asset_status')}"
        for slot in slots
    ]


def first_paragraph_insert(body: str, slots: list[dict[str, Any]]) -> str:
    if not slots:
        return body
    markers = "\n\n".join(str(slot.get("slot_marker") or "") for slot in slots)
    if not body.strip():
        return markers
    paragraphs = body.split("\n\n")
    if len(paragraphs) == 1:
        return f"{paragraphs[0]}\n\n{markers}"
    return "\n\n".join([paragraphs[0], markers, *paragraphs[1:]])


def slot_instruction(slot: dict[str, Any], index: int) -> dict[str, Any]:
    marker = f"[[IMAGE_SLOT_{index}]]"
    visual_type = str(slot.get("visual_type") or "visual")
    placement = str(slot.get("placement") or "after_opening")
    asset_path = str(slot.get("asset_path") or "")
    return {
        "slot_marker": marker,
        "placement": placement,
        "visual_type": visual_type,
        "asset_path": asset_path,
        "asset_status": slot.get("asset_status") or "PLACEHOLDER",
        "copy_instruction": f"在 {placement} 插入 {visual_type}，用于说明：{slot.get('information_job') or slot.get('supports_claim') or '文章核心判断'}",
        "caption_suggestion": slot.get("supports_claim") or slot.get("information_job") or "",
        "alt_text": f"{visual_type}: {slot.get('supports_claim') or slot.get('information_job') or ''}".strip(),
        "copyright_note": slot.get("copyright_note") or "人工确认图片来源、版权和使用范围。",
        "manual_required": True,
    }


def pack_status(candidate: dict[str, Any], slots: list[dict[str, Any]]) -> str:
    if candidate.get("visual_status") == "BLOCKED" or any(slot.get("asset_status") == "REJECTED" for slot in slots):
        return "BLOCKED"
    if any(slot.get("asset_status") in {"", "PLACEHOLDER", "NEEDS_REVIEW"} or not slot.get("asset_path") for slot in slots):
        return "NEEDS_VISUAL_ASSET"
    if candidate.get("visual_status") in {"NEEDS_VISUAL_REVIEW", "HAS_PLACEHOLDERS"}:
        return "NEEDS_REVIEW"
    return "READY_FOR_MANUAL_COPY"


def build_wechat_copy_pack_with_images(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    publishing_root = paths.market_content_root / "07_publishing"
    candidate_payload = read_json(publishing_root / "latest_visual_approved_final_candidates.json")
    packs: list[dict[str, Any]] = []
    for candidate in list_payload(candidate_payload, "candidates"):
        slots = [slot_instruction(slot, index) for index, slot in enumerate(candidate.get("image_slots") or [], start=1) if isinstance(slot, dict)]
        body_markdown = str(candidate.get("body_markdown") or "")
        status = pack_status(candidate, slots)
        packs.append(
            {
                "copy_pack_id": make_id("wcp", run_date, candidate.get("visual_final_candidate_id"), candidate.get("article_id")),
                "visual_final_candidate_id": candidate.get("visual_final_candidate_id") or "",
                "title_to_copy": candidate.get("title") or "",
                "body_markdown_to_copy": body_markdown,
                "body_with_image_markers": first_paragraph_insert(body_markdown, slots),
                "image_slots": slots,
                "manual_copy_steps": manual_copy_steps(),
                "visual_copy_steps": visual_copy_steps(slots),
                "pack_status": status,
                "would_publish": False,
                "do_not_publish": True,
            }
        )
    summary = {
        "pack_count": len(packs),
        "ready_for_manual_copy": sum(1 for item in packs if item.get("pack_status") == "READY_FOR_MANUAL_COPY"),
        "needs_visual_asset": sum(1 for item in packs if item.get("pack_status") == "NEEDS_VISUAL_ASSET"),
        "needs_review": sum(1 for item in packs if item.get("pack_status") == "NEEDS_REVIEW"),
        "blocked": sum(1 for item in packs if item.get("pack_status") == "BLOCKED"),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "packs": packs,
        "summary": summary,
        "policy": {"manual_copy_only": True, "would_publish": False, "do_not_publish": True, "no_wechat_api": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('copy_pack_id')}` | `{item.get('visual_final_candidate_id')}` | {item.get('title_to_copy') or ''} | `{item.get('pack_status')}` | {len(item.get('image_slots') or [])} |"
        for item in list_payload(payload, "packs")
    ) or "| - | - | No WeChat copy packs | - | 0 |"
    return f"""# WeChat Copy Pack with Image Slots

## Summary

- pack_count: `{summary.get('pack_count', 0)}`
- ready_for_manual_copy: `{summary.get('ready_for_manual_copy', 0)}`
- needs_visual_asset: `{summary.get('needs_visual_asset', 0)}`
- needs_review: `{summary.get('needs_review', 0)}`
- blocked: `{summary.get('blocked', 0)}`
- manual_copy_only: `true`
- would_publish: `false`

| Copy Pack | Visual Candidate | Title | Status | Image Slots |
|---|---|---|---|---:|
{rows}
"""

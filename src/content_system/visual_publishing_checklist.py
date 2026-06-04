"""Build final manual publishing checklists that include visual assets."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


CHECK_LABELS = [
    ("title_cover_alignment", "标题是否和首图一致"),
    ("cover_core_judgment", "首图是否表达文章核心判断"),
    ("visual_supports_section", "每张图是否服务对应段落"),
    ("mobile_readability", "图片是否手机端可读"),
    ("copyright_source", "图片是否有版权/来源说明"),
    ("small_text", "图中文字是否过小"),
    ("decorative_noise", "图是否过度装饰、没有信息量"),
    ("text_visual_flow", "图文之间是否有断裂"),
    ("placement_reasonable", "图片插入位置是否合理"),
    ("slot_markers_removed", "是否删除所有 [[IMAGE_SLOT_X]] 标记"),
    ("wechat_preview_ok", "公众号预览是否正常"),
    ("no_auto_publish", "是否确认不自动发布"),
]


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__visual-publishing-checklist.json",
        "dated_md": root / f"{run_date}__visual-publishing-checklist.md",
        "latest_json": root / "latest_visual_publishing_checklist.json",
        "latest_md": root / "latest_visual_publishing_checklist.md",
    }


def status_for_check(check_id: str, pack: dict[str, Any], candidate: dict[str, Any]) -> tuple[str, str]:
    slots = pack.get("image_slots") if isinstance(pack.get("image_slots"), list) else []
    if check_id == "no_auto_publish":
        return "PASS", "System policy keeps publishing manual only."
    if check_id == "slot_markers_removed":
        return "WARN", "Manual operator must delete slot markers after inserting images."
    if not slots and check_id in {"cover_core_judgment", "visual_supports_section", "placement_reasonable"}:
        return "WARN", "No image slots are attached; confirm whether article needs visuals."
    if any(slot.get("asset_status") in {"PLACEHOLDER", "NEEDS_REVIEW", ""} for slot in slots):
        return "WARN", "Some image slots still need assets or review."
    if candidate.get("visual_status") == "BLOCKED" or pack.get("pack_status") == "BLOCKED":
        return "FAIL", "Visual workflow is blocked."
    if check_id == "copyright_source":
        return "WARN", "Human must confirm image rights before publishing."
    if check_id == "wechat_preview_ok":
        return "WARN", "Manual WeChat mobile preview is still required."
    return "PASS", ""


def checklist_status(checks: list[dict[str, Any]]) -> str:
    if any(item.get("status") == "FAIL" for item in checks):
        return "BLOCKED"
    if any(item.get("status") == "WARN" for item in checks):
        return "NEEDS_ATTENTION"
    return "READY"


def manual_steps(pack: dict[str, Any]) -> list[str]:
    steps = pack.get("manual_copy_steps") if isinstance(pack.get("manual_copy_steps"), list) else []
    return [str(item) for item in steps] or [
        "打开微信公众号后台。",
        "复制标题和正文。",
        "按图片槽位插入图片。",
        "人工预览并最终决定是否发布。",
    ]


def build_visual_publishing_checklist(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    root = paths.market_content_root / "07_publishing"
    pack_payload = read_json(root / "latest_wechat_copy_pack_with_images.json")
    candidate_payload = read_json(root / "latest_visual_approved_final_candidates.json")
    candidates = {str(item.get("visual_final_candidate_id") or ""): item for item in list_payload(candidate_payload, "candidates")}
    checklists: list[dict[str, Any]] = []
    for pack in list_payload(pack_payload, "packs"):
        candidate = candidates.get(str(pack.get("visual_final_candidate_id") or ""), {})
        checks = []
        for check_id, label in CHECK_LABELS:
            status, note = status_for_check(check_id, pack, candidate)
            checks.append({"check_id": check_id, "label": label, "status": status, "note": note})
        status = checklist_status(checks)
        checklists.append(
            {
                "visual_checklist_id": make_id("vpchk", run_date, pack.get("copy_pack_id"), pack.get("visual_final_candidate_id")),
                "copy_pack_id": pack.get("copy_pack_id") or "",
                "visual_final_candidate_id": pack.get("visual_final_candidate_id") or "",
                "status": status,
                "checks": checks,
                "manual_steps": manual_steps(pack),
                "would_publish": False,
                "final_human_confirmation_required": True,
            }
        )
    summary = {
        "checklist_count": len(checklists),
        "ready": sum(1 for item in checklists if item.get("status") == "READY"),
        "needs_attention": sum(1 for item in checklists if item.get("status") == "NEEDS_ATTENTION"),
        "blocked": sum(1 for item in checklists if item.get("status") == "BLOCKED"),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "checklists": checklists,
        "summary": summary,
        "policy": {"final_human_confirmation_required": True, "would_publish": False, "no_wechat_api": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('visual_checklist_id')}` | `{item.get('copy_pack_id')}` | `{item.get('status')}` | {sum(1 for check in item.get('checks', []) if isinstance(check, dict) and check.get('status') == 'WARN')} |"
        for item in list_payload(payload, "checklists")
    ) or "| - | - | - | 0 |"
    return f"""# Visual Publishing Checklist

## Summary

- checklist_count: `{summary.get('checklist_count', 0)}`
- ready: `{summary.get('ready', 0)}`
- needs_attention: `{summary.get('needs_attention', 0)}`
- blocked: `{summary.get('blocked', 0)}`
- final_human_confirmation_required: `true`
- would_publish: `false`

| Checklist | Copy Pack | Status | Warnings |
|---|---|---|---:|
{rows}
"""

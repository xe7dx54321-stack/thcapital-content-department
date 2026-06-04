"""Regression checks for manual publishing checklists and copy packs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


FORBIDDEN_KEYS = ("wechat_api", "draft_api", "auto_publish", "publish_api", "draftbox", "draft_box")


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__publishing-checklist-regression.json",
        "dated_md": paths.logs_root / f"{run_date}__publishing-checklist-regression.md",
        "latest_json": paths.logs_root / "latest_publishing_checklist_regression.json",
        "latest_md": paths.logs_root / "latest_publishing_checklist_regression.md",
    }


def check(check_id: str, ok: bool, message: str, warn: bool = False) -> dict[str, str]:
    status = "PASS" if ok else ("WARN" if warn else "FAIL")
    return {"check_id": check_id, "status": status, "message": message}


def contains_forbidden_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, inner in value.items():
            lowered = str(key).lower()
            if any(token in lowered for token in FORBIDDEN_KEYS):
                return True
            if contains_forbidden_key(inner):
                return True
    if isinstance(value, list):
        return any(contains_forbidden_key(item) for item in value)
    return False


def build_publishing_checklist_regression(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    publishing_root = paths.market_content_root / "07_publishing"
    final_checklist = read_json(publishing_root / "latest_final_publish_checklist.json")
    visual_checklist = read_json(publishing_root / "latest_visual_publishing_checklist.json")
    copy_pack = read_json(publishing_root / "latest_wechat_copy_pack_with_images.json")
    queue = read_json(publishing_root / "latest_content_queue_priority.json")
    final_items = list_payload(final_checklist, "items")
    visual_items = list_payload(visual_checklist, "checklists")
    packs = list_payload(copy_pack, "packs")
    queue_items = list_payload(queue, "items")
    checks: list[dict[str, str]] = []
    all_publish_flags = final_items + visual_items + packs
    checks.append(check("would_publish_false", all(item.get("would_publish") is False for item in all_publish_flags if "would_publish" in item), "All explicit would_publish flags must be false.", warn=not all_publish_flags))
    checks.append(check("do_not_publish_true", all(item.get("do_not_publish") is True for item in all_publish_flags if "do_not_publish" in item), "All explicit do_not_publish flags must be true.", warn=not all_publish_flags))
    checks.append(check("human_confirmation_required", all(item.get("final_human_confirmation_required") is True for item in final_items + visual_items if "final_human_confirmation_required" in item), "Final human confirmation is required where checklist exposes the field.", warn=not (final_items or visual_items)))
    labels = " ".join(str(check_item.get("label") or "") for item in visual_items for check_item in item.get("checks", []) if isinstance(check_item, dict))
    checks.append(check("visual_copyright_check", "版权" in labels or "来源" in labels, "Visual checklist must include copyright/source checks."))
    checks.append(check("visual_clarity_check", "清晰" in labels or "手机端" in labels, "Visual checklist must include clarity/mobile readability checks."))
    checks.append(check("visual_placement_check", "插入位置" in labels or "位置" in labels, "Visual checklist must include insertion placement checks."))
    checks.append(check("copy_pack_manual_steps", all(isinstance(pack.get("manual_copy_steps"), list) and pack.get("manual_copy_steps") for pack in packs), "Copy packs must include manual copy steps.", warn=not packs))
    checks.append(check("copy_pack_image_slots", all(isinstance(pack.get("image_slots"), list) and pack.get("image_slots") for pack in packs), "Copy packs must include image slot instructions.", warn=not packs))
    checks.append(check("no_api_fields", not contains_forbidden_key({"final": final_items, "visual": visual_items, "packs": packs}), "Publishing artifacts must not expose WeChat API / draftbox / auto publish fields."))
    missing_visual_items = [item for item in queue_items if item.get("readiness_status") == "NEEDS_VISUAL_ASSET"]
    pack_statuses = {str(pack.get("pack_status") or "") for pack in packs}
    visual_statuses = {str(item.get("status") or "") for item in visual_items}
    checks.append(check("missing_image_status_guard", not missing_visual_items or "NEEDS_VISUAL_ASSET" in pack_statuses or "NEEDS_ATTENTION" in visual_statuses or "BLOCKED" in visual_statuses, "Missing images must keep pack/checklist in NEEDS_VISUAL_ASSET or NEEDS_ATTENTION."))
    pass_count = sum(1 for item in checks if item["status"] == "PASS")
    warn_count = sum(1 for item in checks if item["status"] == "WARN")
    fail_count = sum(1 for item in checks if item["status"] == "FAIL")
    regression_status = "FAIL" if fail_count else ("WARN" if warn_count else "PASS")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "checks": checks,
        "summary": {"check_count": len(checks), "pass": pass_count, "warn": warn_count, "fail": fail_count, "regression_status": regression_status},
        "policy": {"regression_only": True, "no_auto_publish": True, "no_wechat_api": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [f"| `{item.get('status')}` | `{item.get('check_id')}` | {item.get('message')} |" for item in list_payload(payload, "checks")]
    return f"""# Publishing Checklist Regression

## Summary

- check_count: `{summary.get('check_count', 0)}`
- pass: `{summary.get('pass', 0)}`
- warn: `{summary.get('warn', 0)}`
- fail: `{summary.get('fail', 0)}`
- regression_status: `{summary.get('regression_status', 'WARN')}`

| Status | Check | Message |
|---|---|---|
{chr(10).join(rows)}
"""

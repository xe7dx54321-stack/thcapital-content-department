"""Manual post-publish visual performance records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


VALID_RATINGS = {"LOW", "MEDIUM", "HIGH", "EXCELLENT", "UNKNOWN"}
VALID_EFFECTS = {"HELPFUL", "NEUTRAL", "DISTRACTING", "UNKNOWN"}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    publishing_root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": publishing_root / f"{run_date}__post-publish-visual-performance.json",
        "dated_md": publishing_root / f"{run_date}__post-publish-visual-performance.md",
        "latest_json": publishing_root / "latest_post_publish_visual_performance.json",
        "latest_md": publishing_root / "latest_post_publish_visual_performance.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__post-publish-visual-performance-board.md",
        "board_latest_md": paths.frontstage_root / "latest_post_publish_visual_performance_board.md",
    }


def summary_for(records: list[dict[str, Any]]) -> dict[str, int]:
    visual_notes = [note for record in records for note in record.get("visual_notes", []) if isinstance(note, dict)]
    return {
        "record_count": len(records),
        "helpful_visuals": sum(1 for item in visual_notes if item.get("observed_effect") == "HELPFUL"),
        "distracting_visuals": sum(1 for item in visual_notes if item.get("observed_effect") == "DISTRACTING"),
        "high_or_excellent": sum(1 for item in records if item.get("overall_visual_rating") in {"HIGH", "EXCELLENT"}),
    }


def match_copy_pack(copy_packs: list[dict[str, Any]], final_candidate_id: str) -> dict[str, Any]:
    return next(
        (
            item
            for item in copy_packs
            if str(item.get("visual_final_candidate_id") or "") == final_candidate_id
            or str(item.get("copy_pack_id") or "") == final_candidate_id
        ),
        copy_packs[0] if copy_packs else {},
    )


def build_payload(paths: ProjectPaths) -> dict[str, Any]:
    run_date = today_token()
    root = paths.market_content_root / "07_publishing"
    existing = read_json(root / "latest_post_publish_visual_performance.json")
    records = list_payload(existing, "records")
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "records": records,
        "summary": summary_for(records),
        "policy": {"manual_input_only": True, "no_auto_metrics_fetch": True, "no_wechat_api": True},
    }


def write_payload(paths: ProjectPaths, repo_root: Path, payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Path]]:
    payload["summary"] = summary_for(list_payload(payload, "records"))
    outputs = output_paths(paths, str(payload.get("run_date") or today_token()))
    markdown = render_markdown(payload)
    write_json_and_markdown(payload, markdown, outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def build_post_publish_visual_performance_board(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    return write_payload(paths, repo_root, build_payload(paths))


def record_visual_performance(
    paths: ProjectPaths,
    repo_root: Path,
    *,
    session_id: str,
    rating: str = "UNKNOWN",
    note: str = "",
    asset_id: str = "",
    effect: str = "UNKNOWN",
    asset_note: str = "",
) -> tuple[dict[str, Any], dict[str, Path]]:
    rating = rating.upper()
    effect = effect.upper()
    if rating not in VALID_RATINGS:
        rating = "UNKNOWN"
    if effect not in VALID_EFFECTS:
        effect = "UNKNOWN"
    payload = build_payload(paths)
    records = list_payload(payload, "records")
    publishing_root = paths.market_content_root / "07_publishing"
    sessions_payload = read_json(publishing_root / "latest_manual_publish_sessions.json")
    copy_pack_payload = read_json(publishing_root / "latest_wechat_copy_pack_with_images.json")
    asset_payload = read_json(paths.market_content_root / "08_assets" / "image_asset_library.json")
    session = next((item for item in list_payload(sessions_payload, "sessions") if str(item.get("publish_session_id") or "") == session_id), {})
    pack = match_copy_pack(list_payload(copy_pack_payload, "packs"), str(session.get("final_candidate_id") or ""))
    assets = list_payload(asset_payload, "assets")
    visual_notes = []
    if asset_id:
        asset = next((item for item in assets if str(item.get("asset_id") or "") == asset_id), {})
        visual_notes.append(
            {
                "asset_id": asset_id,
                "visual_type": asset.get("visual_type") or "",
                "observed_effect": effect,
                "manual_note": asset_note or note,
            }
        )
    record_id = make_id("vperf", str(payload.get("run_date") or today_token()), session_id, asset_id or rating)
    existing = next((item for item in records if item.get("visual_performance_id") == record_id), None)
    record = existing or {
        "visual_performance_id": record_id,
        "publish_session_id": session_id,
        "copy_pack_id": pack.get("copy_pack_id") or "",
        "article_id": session.get("final_candidate_id") or "",
        "visual_notes": [],
        "overall_visual_rating": "UNKNOWN",
        "manual_note": "",
        "created_at": utc_now(),
    }
    if rating != "UNKNOWN":
        record["overall_visual_rating"] = rating
    if note:
        record["manual_note"] = note
    if visual_notes:
        existing_notes = [item for item in record.get("visual_notes", []) if isinstance(item, dict) and item.get("asset_id") != asset_id]
        record["visual_notes"] = [*existing_notes, *visual_notes]
    if existing is None:
        records.append(record)
    payload["records"] = records
    return write_payload(paths, repo_root, payload)


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('visual_performance_id')}` | `{item.get('publish_session_id')}` | `{item.get('copy_pack_id')}` | `{item.get('overall_visual_rating')}` | {item.get('manual_note') or ''} |"
        for item in list_payload(payload, "records")
    ) or "| - | - | - | UNKNOWN | No post-publish visual performance records |"
    return f"""# Post-publish Visual Performance

## Summary

- record_count: `{summary.get('record_count', 0)}`
- helpful_visuals: `{summary.get('helpful_visuals', 0)}`
- distracting_visuals: `{summary.get('distracting_visuals', 0)}`
- high_or_excellent: `{summary.get('high_or_excellent', 0)}`
- manual_input_only: `true`

| Record | Session | Copy Pack | Rating | Note |
|---|---|---|---|---|
{rows}
"""

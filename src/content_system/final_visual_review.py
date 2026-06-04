"""Human final visual review for image assets."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "08_assets"
    return {
        "dated_json": root / f"{run_date}__final-visual-review.json",
        "dated_md": root / f"{run_date}__final-visual-review.md",
        "latest_json": root / "latest_final_visual_review.json",
        "latest_md": root / "latest_final_visual_review.md",
    }


def default_scores(status: str) -> dict[str, int]:
    if status == "APPROVED":
        return {
            "relevance_to_core_judgment": 8,
            "clarity": 8,
            "information_density": 7,
            "wechat_readability": 8,
            "aesthetic_fit": 8,
            "copyright_safety": 7,
        }
    return {
        "relevance_to_core_judgment": 0,
        "clarity": 0,
        "information_density": 0,
        "wechat_readability": 0,
        "aesthetic_fit": 0,
        "copyright_safety": 0,
    }


def summary_for(reviews: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "review_count": len(reviews),
        "approved": sum(1 for item in reviews if item.get("review_status") == "APPROVED"),
        "rejected": sum(1 for item in reviews if item.get("review_status") == "REJECTED"),
        "needs_revision": sum(1 for item in reviews if item.get("review_status") == "NEEDS_REVISION"),
        "wechat_ready": sum(1 for item in reviews if item.get("wechat_ready")),
    }


def build_final_visual_review(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    assets_payload = read_json(paths.market_content_root / "08_assets" / "image_asset_library.json")
    existing = read_json(paths.market_content_root / "08_assets" / "latest_final_visual_review.json")
    existing_by_asset = {str(item.get("asset_id")): item for item in list_payload(existing, "reviews") if item.get("asset_id")}
    reviews: list[dict[str, Any]] = []
    for asset in list_payload(assets_payload, "assets"):
        asset_id = str(asset.get("asset_id") or "")
        previous = existing_by_asset.get(asset_id, {})
        status = previous.get("review_status") or "UNREVIEWED"
        reviews.append(
            {
                "review_id": previous.get("review_id") or make_id("vrev", run_date, asset_id),
                "asset_id": asset_id,
                "article_id": asset.get("article_id") or "",
                "visual_type": asset.get("visual_type") or "",
                "review_status": status,
                "scores": previous.get("scores") if isinstance(previous.get("scores"), dict) else default_scores(status),
                "human_note": previous.get("human_note") or "",
                "wechat_ready": bool(previous.get("wechat_ready")) if previous else False,
                "do_not_publish": True,
            }
        )
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "reviews": reviews,
        "summary": summary_for(reviews),
        "policy": {"manual_review_required": True, "do_not_publish": True, "no_auto_image_generation": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def update_review(paths: ProjectPaths, repo_root: Path, asset_id: str, status: str, note: str) -> tuple[dict[str, Any], dict[str, Path]]:
    payload, _ = build_final_visual_review(paths, repo_root)
    reviews = list_payload(payload, "reviews")
    matched = False
    for review in reviews:
        if review.get("asset_id") != asset_id:
            continue
        matched = True
        review["review_status"] = status
        review["human_note"] = note
        review["scores"] = default_scores(status)
        review["wechat_ready"] = status == "APPROVED"
        review["do_not_publish"] = True
    if not matched:
        run_date = str(payload.get("run_date") or today_token())
        reviews.append(
            {
                "review_id": make_id("vrev", run_date, asset_id),
                "asset_id": asset_id,
                "article_id": "",
                "visual_type": "",
                "review_status": status,
                "scores": default_scores(status),
                "human_note": note,
                "wechat_ready": status == "APPROVED",
                "do_not_publish": True,
            }
        )
    payload["reviews"] = reviews
    payload["summary"] = summary_for(reviews)
    outputs = output_paths(paths, str(payload.get("run_date") or today_token()))
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('review_id')}` | `{item.get('asset_id')}` | `{item.get('visual_type')}` | `{item.get('review_status')}` | `{item.get('wechat_ready')}` | {item.get('human_note') or ''} |"
        for item in list_payload(payload, "reviews")
    ) or "| - | - | - | - | false | No visual assets to review |"
    return f"""# Final Visual Review

## Summary

- review_count: `{summary.get('review_count', 0)}`
- approved: `{summary.get('approved', 0)}`
- rejected: `{summary.get('rejected', 0)}`
- needs_revision: `{summary.get('needs_revision', 0)}`
- wechat_ready: `{summary.get('wechat_ready', 0)}`
- do_not_publish: `true`

| Review | Asset | Visual Type | Status | WeChat Ready | Note |
|---|---|---|---|---|---|
{rows}
"""

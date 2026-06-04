"""Build final article candidates enriched with visual review state."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__visual-approved-final-candidates.json",
        "dated_md": root / f"{run_date}__visual-approved-final-candidates.md",
        "latest_json": root / "latest_visual_approved_final_candidates.json",
        "latest_md": root / "latest_visual_approved_final_candidates.md",
    }


def key_article_id(item: dict[str, Any]) -> str:
    return str(item.get("source_article_id") or item.get("article_id") or item.get("final_candidate_id") or "")


def plan_for_article(plans: list[dict[str, Any]], article_id: str) -> dict[str, Any]:
    return next((item for item in plans if str(item.get("article_id") or "") == article_id), plans[0] if plans else {})


def asset_for_visual(assets: list[dict[str, Any]], article_id: str, visual: dict[str, Any]) -> dict[str, Any]:
    visual_id = str(visual.get("visual_id") or "")
    visual_type = str(visual.get("visual_type") or "")
    return next(
        (
            item
            for item in assets
            if (str(item.get("article_id") or "") in {"", article_id})
            and (str(item.get("visual_id") or "") == visual_id or str(item.get("visual_type") or "") == visual_type)
        ),
        {},
    )


def review_for_asset(reviews: list[dict[str, Any]], asset_id: str) -> dict[str, Any]:
    return next((item for item in reviews if str(item.get("asset_id") or "") == asset_id), {})


def build_image_slots(candidate: dict[str, Any], plan: dict[str, Any], assets: list[dict[str, Any]], reviews: list[dict[str, Any]]) -> list[dict[str, Any]]:
    article_id = key_article_id(candidate)
    slots: list[dict[str, Any]] = []
    visuals = plan.get("visuals") if isinstance(plan.get("visuals"), list) else []
    for index, visual in enumerate([item for item in visuals if isinstance(item, dict)], start=1):
        asset = asset_for_visual(assets, article_id, visual)
        asset_id = str(asset.get("asset_id") or "")
        review = review_for_asset(reviews, asset_id)
        asset_status = str(asset.get("asset_status") or "PLACEHOLDER")
        review_status = str(review.get("review_status") or "UNREVIEWED")
        wechat_ready = bool(review.get("wechat_ready")) or bool(asset.get("wechat_ready"))
        slots.append(
            {
                "slot_id": make_id("slot", today_token(), candidate.get("final_candidate_id"), visual.get("visual_id"), index),
                "visual_id": visual.get("visual_id") or "",
                "asset_id": asset_id,
                "placement": visual.get("placement") or "",
                "visual_type": visual.get("visual_type") or "",
                "asset_status": asset_status,
                "asset_path": asset.get("asset_path") or "",
                "copyright_note": asset.get("copyright_note") or "",
                "visual_review_status": review_status,
                "wechat_ready": wechat_ready,
                "information_job": visual.get("information_job") or "",
                "supports_claim": visual.get("supports_claim") or "",
            }
        )
    return slots


def status_for_slots(slots: list[dict[str, Any]]) -> str:
    if any(item.get("visual_review_status") == "REJECTED" or item.get("asset_status") == "REJECTED" for item in slots):
        return "BLOCKED"
    if any(item.get("asset_status") in {"", "PLACEHOLDER"} or not item.get("asset_id") for item in slots):
        return "HAS_PLACEHOLDERS"
    if any(item.get("visual_review_status") not in {"APPROVED"} or not item.get("wechat_ready") for item in slots):
        return "NEEDS_VISUAL_REVIEW"
    return "VISUAL_READY"


def candidate_from_preview(paths: ProjectPaths) -> list[dict[str, Any]]:
    preview = read_json(paths.logs_root / "latest_article_with_images_preview.json")
    article = preview.get("article") if isinstance(preview.get("article"), dict) else {}
    if not article or not article.get("article_id"):
        return []
    return [
        {
            "final_candidate_id": article.get("article_id"),
            "source_article_id": article.get("article_id"),
            "title": article.get("title") or "",
            "wechat_title": article.get("title") or "",
            "body_markdown": article.get("body_markdown") or "",
            "wechat_body_markdown": article.get("body_markdown") or "",
        }
    ]


def build_visual_approved_final_candidates(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    publishing_root = paths.market_content_root / "07_publishing"
    assets_root = paths.market_content_root / "08_assets"
    drafts_root = paths.market_content_root / "05_draft_packs"
    final_payload = read_json(publishing_root / "latest_final_article_candidates.json")
    visual_review_payload = read_json(assets_root / "latest_final_visual_review.json")
    asset_payload = read_json(assets_root / "image_asset_library.json")
    visual_plan_payload = read_json(drafts_root / "latest_article_visual_plans.json")
    candidates = list_payload(final_payload, "candidates") or candidate_from_preview(paths)
    plans = list_payload(visual_plan_payload, "visual_plans")
    assets = list_payload(asset_payload, "assets")
    reviews = list_payload(visual_review_payload, "reviews")
    visual_candidates: list[dict[str, Any]] = []
    warnings = []
    if not candidates:
        warnings.append("No final article candidates or article-with-images preview found.")
    for candidate in candidates:
        article_id = key_article_id(candidate)
        slots = build_image_slots(candidate, plan_for_article(plans, article_id), assets, reviews)
        visual_status = status_for_slots(slots)
        remaining_risks = []
        if any(item.get("asset_status") in {"", "PLACEHOLDER"} for item in slots):
            remaining_risks.append("Some image slots still have placeholder assets.")
        if any(item.get("visual_review_status") in {"UNREVIEWED", "NEEDS_REVISION", "DEFERRED"} for item in slots):
            remaining_risks.append("Some visual assets still need human visual review.")
        if not slots:
            remaining_risks.append("No visual slots are attached to this final candidate.")
        visual_candidates.append(
            {
                "visual_final_candidate_id": make_id("vfinal", run_date, candidate.get("final_candidate_id"), article_id),
                "final_candidate_id": candidate.get("final_candidate_id") or "",
                "article_id": article_id,
                "title": candidate.get("wechat_title") or candidate.get("title") or "",
                "body_markdown": candidate.get("wechat_body_markdown") or candidate.get("body_markdown") or "",
                "visual_asset_count": len(slots),
                "approved_visual_count": sum(1 for item in slots if item.get("visual_review_status") == "APPROVED"),
                "placeholder_visual_count": sum(1 for item in slots if item.get("asset_status") in {"", "PLACEHOLDER"} or not item.get("asset_id")),
                "wechat_ready_visual_count": sum(1 for item in slots if item.get("wechat_ready")),
                "visual_status": visual_status,
                "image_slots": slots,
                "remaining_visual_risks": remaining_risks,
                "manual_review_required": True,
                "would_publish": False,
                "do_not_publish": True,
            }
        )
    summary = {
        "candidate_count": len(visual_candidates),
        "visual_ready": sum(1 for item in visual_candidates if item.get("visual_status") == "VISUAL_READY"),
        "needs_visual_review": sum(1 for item in visual_candidates if item.get("visual_status") == "NEEDS_VISUAL_REVIEW"),
        "has_placeholders": sum(1 for item in visual_candidates if item.get("visual_status") == "HAS_PLACEHOLDERS"),
        "blocked": sum(1 for item in visual_candidates if item.get("visual_status") == "BLOCKED"),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "candidates": visual_candidates,
        "summary": summary,
        "warnings": warnings,
        "policy": {"would_publish": False, "do_not_publish": True, "manual_review_required": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('visual_final_candidate_id')}` | `{item.get('final_candidate_id')}` | {item.get('title') or ''} | `{item.get('visual_status')}` | {item.get('visual_asset_count')} | {item.get('wechat_ready_visual_count')} |"
        for item in list_payload(payload, "candidates")
    ) or "| - | - | No visual-approved final candidates | - | 0 | 0 |"
    return f"""# Visual-approved Final Article Candidates

## Summary

- candidate_count: `{summary.get('candidate_count', 0)}`
- visual_ready: `{summary.get('visual_ready', 0)}`
- needs_visual_review: `{summary.get('needs_visual_review', 0)}`
- has_placeholders: `{summary.get('has_placeholders', 0)}`
- blocked: `{summary.get('blocked', 0)}`
- would_publish: `false`
- do_not_publish: `true`

| Visual Final Candidate | Final Candidate | Title | Visual Status | Visuals | WeChat Ready |
|---|---|---|---|---:|---:|
{rows}
"""

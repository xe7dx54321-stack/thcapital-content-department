"""Build data for the local WeChat content workbench."""

from __future__ import annotations

import os
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, safe_int, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class WechatWorkbenchDataReport:
    schema_version: str
    generated_at: str
    run_date: str
    summary: dict[str, Any]
    topics: tuple[dict[str, Any], ...]
    articles: tuple[dict[str, Any], ...]
    selected_article_id: str
    system_status: dict[str, Any]
    version_review: dict[str, Any]
    final_review: dict[str, Any]
    performance_panel: dict[str, Any]
    methodology_panel: dict[str, Any]
    generation_visual_panel: dict[str, Any]
    live_pilot_panel: dict[str, Any]
    image_asset_panel: dict[str, Any]
    publishing_pack_panel: dict[str, Any]
    content_ops_panel: dict[str, Any]
    content_hardening_panel: dict[str, Any]
    warnings: tuple[str, ...]


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.frontstage_root / f"{run_date}__wechat-workbench-data.json",
        "latest_json": paths.frontstage_root / "latest_wechat_workbench_data.json",
        "summary_dated_json": paths.logs_root / f"{run_date}__wechat-workbench-data-summary.json",
        "summary_latest_json": paths.logs_root / "latest_wechat_workbench_data_summary.json",
    }


def by_key(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(key)): item for item in items if item.get(key)}


def status_from(judge: dict[str, Any], candidate: dict[str, Any], package: dict[str, Any]) -> str:
    if candidate:
        return "ready"
    decision = str(judge.get("decision") or "")
    quality = str(package.get("quality_status") or "")
    publish_status = str(package.get("publish_status") or "")
    if decision == "APPROVED_FOR_QUEUE" or publish_status == "READY_FOR_HUMAN_REVIEW":
        if decision == "NEEDS_REVISION":
            return "needs_revision"
        return "ready"
    if decision == "HOLD" or publish_status == "HOLD":
        return "hold"
    if decision == "NEEDS_REVISION" or quality.startswith("NEEDS"):
        return "needs_revision"
    return "recommended"


def normalize_title(value: Any) -> str:
    text = str(value or "").lower()
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", text)


def build_topics(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    topics: list[dict[str, Any]] = []
    for item in candidates:
        topic_id = str(item.get("cluster_id") or item.get("candidate_id") or f"topic_{len(topics) + 1}")
        topics.append(
            {
                "topic_id": topic_id,
                "title": item.get("theme") or item.get("title") or "",
                "score": safe_float(item.get("total_score") or item.get("score")),
                "score_band": item.get("score_band") or "",
                "recommended_action": item.get("recommended_action") or "",
                "why_it_matters": item.get("why_it_matters") or "",
                "source_ids": item.get("source_ids") or [],
                "evidence_ids": [ev.get("evidence_id") for ev in item.get("key_evidence", []) if isinstance(ev, dict) and ev.get("evidence_id")],
                "evidence_count": len([ev for ev in item.get("key_evidence", []) if isinstance(ev, dict)]),
                "source_count": len(item.get("source_ids") or []),
                "status": "recommended",
            }
        )
    return topics


def find_topic_for_article(title: str, topics: list[dict[str, Any]], index: int) -> dict[str, Any]:
    normalized_title = normalize_title(title)
    for topic in topics:
        topic_title = normalize_title(topic.get("title"))
        if topic_title and (topic_title in normalized_title or normalized_title in topic_title):
            return topic
    if 0 <= index < len(topics):
        return topics[index]
    return {}


def next_step_for_status(status: str, judge_decision: str) -> str:
    if status == "ready":
        return "进入人工确认和发布 dry-run 检查。"
    if status == "needs_revision":
        return "优先处理 critic / revision 建议，再进入主编复核。"
    if status == "hold":
        return "暂不推进，等待更多证据或更明确的编辑判断。"
    if judge_decision:
        return f"根据 Judge 决策 {judge_decision} 做人工复核。"
    return "作为备选选题观察，必要时换角度或补证据。"


def latest_for_article(items: list[dict[str, Any]], article_id: str, article_ids: set[str]) -> dict[str, Any]:
    for item in reversed(items):
        if str(item.get("source_article_id") or "") in article_ids or str(item.get("source_article_id") or "") == article_id:
            return item
    return items[-1] if items else {}


def build_version_review(paths: ProjectPaths, selected_article_id: str) -> dict[str, Any]:
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    comparison_payload = read_json(versions_root / "latest_version_comparison_scores.json")
    decision_payload = read_json(versions_root / "latest_version_review_decisions.json")
    memory_payload = read_json(versions_root / "article_version_memory.json")
    analytics_payload = read_json(paths.logs_root / "latest_action_effectiveness_analytics.json")
    comparisons = list_payload(comparison_payload, "comparisons")
    decisions = list_payload(decision_payload, "decisions")
    memory_versions = list_payload(memory_payload, "versions")
    selected_ids = {selected_article_id}
    latest_comparison = latest_for_article(comparisons, selected_article_id, selected_ids)
    version_id = str(latest_comparison.get("version_id") or "")
    decision_by_version = {str(item.get("version_id")): item for item in decisions if item.get("version_id")}
    memory_by_version = {str(item.get("version_id")): item for item in memory_versions if item.get("version_id")}
    decision = decision_by_version.get(version_id, {})
    memory = memory_by_version.get(version_id, {})
    comp_summary = comparison_payload.get("summary") if isinstance(comparison_payload.get("summary"), dict) else {}
    analytics_summary = analytics_payload.get("summary") if isinstance(analytics_payload.get("summary"), dict) else {}
    return {
        "comparison_count": safe_int(comp_summary.get("comparison_count")),
        "accept_recommended": safe_int(comp_summary.get("accept_recommended")),
        "reject_recommended": safe_int(comp_summary.get("reject_recommended")),
        "revise_more_recommended": safe_int(comp_summary.get("revise_more_recommended")),
        "human_review_recommended": safe_int(comp_summary.get("human_review_recommended")),
        "latest_comparison": latest_comparison,
        "latest_decision": decision,
        "latest_memory": memory,
        "memory_summary": memory_payload.get("summary") if isinstance(memory_payload.get("summary"), dict) else {},
        "effectiveness_summary": analytics_summary,
        "versioned_preview_path": "同行资本市场内容系统/11_frontstage/latest_versioned_article_preview.html",
        "policy": {
            "do_not_publish": True,
            "do_not_overwrite_original": True,
            "quality_score_is_advisory": True,
        },
    }


def build_final_review(paths: ProjectPaths, selected_article_id: str) -> dict[str, Any]:
    publishing_root = paths.market_content_root / "07_publishing"
    final_payload = read_json(publishing_root / "latest_final_article_candidates.json")
    checklist_payload = read_json(publishing_root / "latest_final_publish_checklist.json")
    memory_payload = read_json(publishing_root / "final_candidate_memory.json")
    analytics_payload = read_json(paths.logs_root / "latest_multiday_version_analytics.json")
    candidates = list_payload(final_payload, "candidates")
    checklists = list_payload(checklist_payload, "items")
    checklist_by_candidate = {str(item.get("final_candidate_id")): item for item in checklists if item.get("final_candidate_id")}
    selected = {}
    for candidate in candidates:
        if candidate.get("source_article_id") == selected_article_id:
            selected = candidate
            break
    if not selected and candidates:
        selected = candidates[0]
    checklist = checklist_by_candidate.get(str(selected.get("final_candidate_id") or ""), {}) if selected else {}
    final_summary = final_payload.get("summary") if isinstance(final_payload.get("summary"), dict) else {}
    checklist_summary = checklist_payload.get("summary") if isinstance(checklist_payload.get("summary"), dict) else {}
    return {
        "candidate_count": safe_int(final_summary.get("candidate_count")),
        "ready_for_final_review": safe_int(final_summary.get("ready_for_final_review")),
        "needs_final_check": safe_int(final_summary.get("needs_final_check")),
        "hold": safe_int(final_summary.get("hold")),
        "selected_candidate": selected,
        "selected_checklist": checklist,
        "memory_summary": memory_payload.get("summary") if isinstance(memory_payload.get("summary"), dict) else {},
        "checklist_summary": checklist_summary,
        "multiday_summary": analytics_payload.get("summary") if isinstance(analytics_payload.get("summary"), dict) else {},
        "policy": {
            "would_publish": False,
            "do_not_publish": True,
            "manual_final_confirmation_required": True,
        },
    }


def build_performance_panel(paths: ProjectPaths, final_review: dict[str, Any]) -> dict[str, Any]:
    publishing_root = paths.market_content_root / "07_publishing"
    sessions_payload = read_json(publishing_root / "latest_manual_publish_sessions.json")
    metrics_payload = read_json(publishing_root / "latest_post_publish_metrics.json")
    memory_payload = read_json(publishing_root / "content_performance_memory.json")
    feedback_payload = read_json(paths.logs_root / "latest_performance_learning_feedback.json")
    selected_candidate = final_review.get("selected_candidate") if isinstance(final_review.get("selected_candidate"), dict) else {}
    final_candidate_id = str(selected_candidate.get("final_candidate_id") or "")
    sessions = list_payload(sessions_payload, "sessions")
    metrics = list_payload(metrics_payload, "metrics")
    records = list_payload(memory_payload, "records")
    selected_session = {}
    for session in reversed(sessions):
        if session.get("final_candidate_id") == final_candidate_id:
            selected_session = session
            break
    selected_metrics = {}
    session_id = str(selected_session.get("publish_session_id") or "")
    for metric in reversed(metrics):
        if metric.get("publish_session_id") == session_id or metric.get("final_candidate_id") == final_candidate_id:
            selected_metrics = metric
            break
    selected_record = {}
    for record in reversed(records):
        if record.get("final_candidate_id") == final_candidate_id:
            selected_record = record
            break
    session_summary = sessions_payload.get("summary") if isinstance(sessions_payload.get("summary"), dict) else {}
    metrics_summary = metrics_payload.get("summary") if isinstance(metrics_payload.get("summary"), dict) else {}
    memory_summary = memory_payload.get("summary") if isinstance(memory_payload.get("summary"), dict) else {}
    feedback_summary = feedback_payload.get("summary") if isinstance(feedback_payload.get("summary"), dict) else {}
    return {
        "session_summary": session_summary,
        "metrics_summary": metrics_summary,
        "performance_memory_summary": memory_summary,
        "learning_feedback_summary": feedback_summary,
        "selected_session": selected_session,
        "selected_metrics": selected_metrics,
        "selected_performance_record": selected_record,
        "recommendations": list_payload(feedback_payload, "recommendations")[:5],
        "policy": {
            "manual_publish_only": True,
            "manual_metrics_only": True,
            "no_wechat_api": True,
            "no_backend_scraping": True,
        },
    }


def build_methodology_panel(paths: ProjectPaths, selected_article_id: str, articles: list[dict[str, Any]]) -> dict[str, Any]:
    topic_payload = read_json(paths.market_content_root / "03_topic_candidates" / "latest_methodology_topic_scores.json")
    article_payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_methodology_article_review.json")
    context_payload = read_json(paths.logs_root / "latest_chief_editor_methodology_context.json")
    alignment_payload = read_json(paths.logs_root / "latest_methodology_performance_alignment.json")
    selected_article = next((item for item in articles if item.get("article_id") == selected_article_id), articles[0] if articles else {})
    topic_id = str(selected_article.get("topic_id") or "")
    topic_scores = list_payload(topic_payload, "topics")
    article_reviews = list_payload(article_payload, "articles")
    selected_topic_score = next((item for item in topic_scores if item.get("topic_id") == topic_id), topic_scores[0] if topic_scores else {})
    selected_article_review = next((item for item in article_reviews if item.get("article_id") == selected_article_id), article_reviews[0] if article_reviews else {})
    return {
        "topic_summary": topic_payload.get("summary") if isinstance(topic_payload.get("summary"), dict) else {},
        "article_summary": article_payload.get("summary") if isinstance(article_payload.get("summary"), dict) else {},
        "topic_scores": topic_scores,
        "article_reviews": article_reviews,
        "selected_topic_score": selected_topic_score,
        "selected_article_review": selected_article_review,
        "chief_editor_context_summary": {
            "selected_article_id": context_payload.get("selected_article_id"),
            "topic_dimension_count": ((context_payload.get("topic_methodology") or {}).get("dimension_count") if isinstance(context_payload.get("topic_methodology"), dict) else 0),
            "article_standard_count": ((context_payload.get("article_methodology") or {}).get("standard_count") if isinstance(context_payload.get("article_methodology"), dict) else 0),
        },
        "alignment_summary": alignment_payload.get("summary") if isinstance(alignment_payload.get("summary"), dict) else {},
        "dimension_insights": list_payload(alignment_payload, "dimension_insights")[:8],
        "recommendations": list_payload(alignment_payload, "recommendations")[:5],
        "policy": {
            "auto_apply": False,
            "do_not_change_config": True,
            "do_not_change_prompts": True,
            "do_not_change_rules": True,
        },
    }


def build_generation_visual_panel(paths: ProjectPaths, selected_article_id: str, articles: list[dict[str, Any]]) -> dict[str, Any]:
    draft_root = paths.market_content_root / "05_draft_packs"
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    briefs_payload = read_json(draft_root / "latest_methodology_content_briefs.json")
    outlines_payload = read_json(draft_root / "latest_methodology_content_outlines.json")
    drafts_payload = read_json(draft_root / "latest_methodology_content_drafts.json")
    rewrite_payload = read_json(versions_root / "latest_methodology_rewrite_versions.json")
    visual_payload = read_json(draft_root / "latest_article_visual_plans.json")
    request_payload = read_json(draft_root / "latest_image_asset_requests.json")
    selected_article = next((item for item in articles if item.get("article_id") == selected_article_id), articles[0] if articles else {})
    topic_id = str(selected_article.get("topic_id") or "")
    selected_brief = next((item for item in list_payload(briefs_payload, "briefs") if item.get("topic_id") == topic_id), list_payload(briefs_payload, "briefs")[0] if list_payload(briefs_payload, "briefs") else {})
    brief_id = str(selected_brief.get("brief_id") or selected_article.get("brief_id") or "")
    selected_outline = next((item for item in list_payload(outlines_payload, "outlines") if item.get("brief_id") == brief_id), list_payload(outlines_payload, "outlines")[0] if list_payload(outlines_payload, "outlines") else {})
    outline_id = str(selected_outline.get("outline_id") or "")
    selected_draft = next((item for item in list_payload(drafts_payload, "drafts") if item.get("outline_id") == outline_id), list_payload(drafts_payload, "drafts")[0] if list_payload(drafts_payload, "drafts") else {})
    draft_id = str(selected_draft.get("draft_id") or "")
    selected_plan = next((item for item in list_payload(visual_payload, "visual_plans") if item.get("article_id") == draft_id), list_payload(visual_payload, "visual_plans")[0] if list_payload(visual_payload, "visual_plans") else {})
    visual_ids = {str(item.get("visual_id")) for item in selected_plan.get("visuals", []) if isinstance(item, dict) and item.get("visual_id")}
    selected_requests = [item for item in list_payload(request_payload, "requests") if str(item.get("visual_id") or "") in visual_ids]
    selected_rewrite = next((item for item in list_payload(rewrite_payload, "versions") if item.get("source_article_id") == selected_article_id or item.get("source_article_id") == draft_id), list_payload(rewrite_payload, "versions")[0] if list_payload(rewrite_payload, "versions") else {})
    return {
        "brief_summary": briefs_payload.get("summary") if isinstance(briefs_payload.get("summary"), dict) else {},
        "outline_summary": outlines_payload.get("summary") if isinstance(outlines_payload.get("summary"), dict) else {},
        "draft_summary": drafts_payload.get("summary") if isinstance(drafts_payload.get("summary"), dict) else {},
        "rewrite_summary": rewrite_payload.get("summary") if isinstance(rewrite_payload.get("summary"), dict) else {},
        "visual_plan_summary": visual_payload.get("summary") if isinstance(visual_payload.get("summary"), dict) else {},
        "image_request_summary": request_payload.get("summary") if isinstance(request_payload.get("summary"), dict) else {},
        "selected_brief": selected_brief,
        "selected_outline": selected_outline,
        "selected_draft": selected_draft,
        "selected_methodology_rewrite": selected_rewrite,
        "selected_visual_plan": selected_plan,
        "selected_image_requests": selected_requests,
        "policy": {
            "do_not_auto_generate_images": True,
            "do_not_call_image_model": True,
            "do_not_publish": True,
            "human_review_required": True,
        },
    }


def build_live_pilot_panel(paths: ProjectPaths) -> dict[str, Any]:
    draft_root = paths.market_content_root / "05_draft_packs"
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    brief_payload = read_json(draft_root / "latest_live_methodology_brief_pilot.json")
    draft_payload = read_json(draft_root / "latest_live_methodology_draft_pilot.json")
    rewrite_payload = read_json(versions_root / "latest_live_methodology_rewrite_pilot.json")
    visual_payload = read_json(draft_root / "latest_live_visual_prompt_pilot.json")
    comparison_payload = read_json(paths.logs_root / "latest_live_output_quality_comparison.json")
    calibration_payload = read_json(paths.logs_root / "latest_live_calibration_feedback.json")
    approval_payload = read_json(draft_root / "latest_image_generation_approval_queue.json")
    phase16_payload = read_json(paths.logs_root / "latest_phase16_daily_live_pilot_pipeline.json")
    return {
        "brief_summary": brief_payload.get("summary") if isinstance(brief_payload.get("summary"), dict) else {},
        "draft_summary": draft_payload.get("summary") if isinstance(draft_payload.get("summary"), dict) else {},
        "rewrite_summary": rewrite_payload.get("summary") if isinstance(rewrite_payload.get("summary"), dict) else {},
        "visual_prompt_summary": visual_payload.get("summary") if isinstance(visual_payload.get("summary"), dict) else {},
        "comparison_summary": comparison_payload.get("summary") if isinstance(comparison_payload.get("summary"), dict) else {},
        "calibration_summary": calibration_payload.get("summary") if isinstance(calibration_payload.get("summary"), dict) else {},
        "image_approval_summary": approval_payload.get("summary") if isinstance(approval_payload.get("summary"), dict) else {},
        "phase16_summary": phase16_payload.get("summary") if isinstance(phase16_payload.get("summary"), dict) else {},
        "latest_brief": (list_payload(brief_payload, "briefs") or [{}])[0],
        "latest_draft": (list_payload(draft_payload, "drafts") or [{}])[0],
        "latest_rewrite": (list_payload(rewrite_payload, "rewrites") or [{}])[0],
        "latest_visual_prompt": (list_payload(visual_payload, "visual_prompts") or [{}])[0],
        "comparisons": list_payload(comparison_payload, "comparisons")[:6],
        "approval_requests": list_payload(approval_payload, "requests")[:6],
        "policy": {
            "dry_run_default": True,
            "live_requires_env_allowlist_key_cost_guard": True,
            "sidecar_only": True,
            "do_not_auto_generate_images": True,
            "do_not_auto_publish": True,
        },
    }


def build_image_asset_panel(paths: ProjectPaths) -> dict[str, Any]:
    draft_root = paths.market_content_root / "05_draft_packs"
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    assets_root = paths.market_content_root / "08_assets"
    live_content_payload = read_json(draft_root / "latest_promoted_live_content_candidates.json")
    live_rewrite_payload = read_json(versions_root / "latest_promoted_live_rewrite_versions.json")
    tasks_payload = read_json(assets_root / "latest_manual_image_generation_tasks.json")
    library_payload = read_json(assets_root / "image_asset_library.json")
    preview_payload = read_json(paths.logs_root / "latest_article_with_images_preview.json")
    visual_review_payload = read_json(assets_root / "latest_final_visual_review.json")
    tasks = list_payload(tasks_payload, "tasks")
    assets = list_payload(library_payload, "assets")
    reviews = list_payload(visual_review_payload, "reviews")
    return {
        "live_content_promotion_summary": live_content_payload.get("summary") if isinstance(live_content_payload.get("summary"), dict) else {},
        "live_rewrite_promotion_summary": live_rewrite_payload.get("summary") if isinstance(live_rewrite_payload.get("summary"), dict) else {},
        "manual_image_task_summary": tasks_payload.get("summary") if isinstance(tasks_payload.get("summary"), dict) else {},
        "image_asset_library_summary": library_payload.get("summary") if isinstance(library_payload.get("summary"), dict) else {},
        "article_with_images_summary": preview_payload.get("summary") if isinstance(preview_payload.get("summary"), dict) else {},
        "final_visual_review_summary": visual_review_payload.get("summary") if isinstance(visual_review_payload.get("summary"), dict) else {},
        "promoted_live_candidates": list_payload(live_content_payload, "promoted_candidates")[:6],
        "promoted_live_rewrites": list_payload(live_rewrite_payload, "versions")[:6],
        "manual_image_tasks": tasks[:8],
        "image_assets": assets[:8],
        "visual_reviews": reviews[:8],
        "article_with_images_preview_path": "同行资本市场内容系统/11_frontstage/latest_article_with_images_preview.html",
        "policy": {
            "manual_first": True,
            "approval_first": True,
            "no_auto_image_generation": True,
            "no_image_model_called": True,
            "no_auto_publish": True,
            "image_files_not_committed": True,
        },
    }


def build_publishing_pack_panel(paths: ProjectPaths) -> dict[str, Any]:
    publishing_root = paths.market_content_root / "07_publishing"
    visual_candidate_payload = read_json(publishing_root / "latest_visual_approved_final_candidates.json")
    copy_pack_payload = read_json(publishing_root / "latest_wechat_copy_pack_with_images.json")
    checklist_payload = read_json(publishing_root / "latest_visual_publishing_checklist.json")
    visual_performance_payload = read_json(publishing_root / "latest_post_publish_visual_performance.json")
    visual_feedback_payload = read_json(paths.logs_root / "latest_visual_strategy_learning_feedback.json")
    candidates = list_payload(visual_candidate_payload, "candidates")
    packs = list_payload(copy_pack_payload, "packs")
    checklists = list_payload(checklist_payload, "checklists")
    selected_pack = packs[0] if packs else {}
    selected_candidate = next(
        (item for item in candidates if item.get("visual_final_candidate_id") == selected_pack.get("visual_final_candidate_id")),
        candidates[0] if candidates else {},
    )
    selected_checklist = next(
        (item for item in checklists if item.get("copy_pack_id") == selected_pack.get("copy_pack_id")),
        checklists[0] if checklists else {},
    )
    return {
        "visual_candidate_summary": visual_candidate_payload.get("summary") if isinstance(visual_candidate_payload.get("summary"), dict) else {},
        "copy_pack_summary": copy_pack_payload.get("summary") if isinstance(copy_pack_payload.get("summary"), dict) else {},
        "visual_checklist_summary": checklist_payload.get("summary") if isinstance(checklist_payload.get("summary"), dict) else {},
        "visual_performance_summary": visual_performance_payload.get("summary") if isinstance(visual_performance_payload.get("summary"), dict) else {},
        "visual_strategy_feedback_summary": visual_feedback_payload.get("summary") if isinstance(visual_feedback_payload.get("summary"), dict) else {},
        "selected_visual_candidate": selected_candidate,
        "selected_copy_pack": selected_pack,
        "selected_visual_checklist": selected_checklist,
        "visual_performance_records": list_payload(visual_performance_payload, "records")[:6],
        "visual_strategy_recommendations": list_payload(visual_feedback_payload, "recommendations")[:6],
        "policy": {
            "manual_copy_only": True,
            "do_not_publish": True,
            "would_publish": False,
            "no_wechat_api": True,
            "no_auto_image_generation": True,
        },
    }


def build_content_ops_panel(paths: ProjectPaths) -> dict[str, Any]:
    publishing_root = paths.market_content_root / "07_publishing"
    calendar_payload = read_json(publishing_root / "latest_publishing_session_calendar.json")
    queue_payload = read_json(publishing_root / "latest_content_queue_priority.json")
    rhythm_payload = read_json(publishing_root / "latest_weekly_publishing_rhythm.json")
    archive_payload = read_json(publishing_root / "published_article_archive.json")
    metrics_review_payload = read_json(paths.logs_root / "latest_post_publish_metrics_review.json")
    closeout_payload = read_json(paths.logs_root / "latest_content_ops_closeout.json")
    queue_items = list_payload(queue_payload, "items")
    today_items = [item for item in queue_items if item.get("priority") == "TODAY"]
    this_week_items = [item for item in queue_items if item.get("priority") == "THIS_WEEK"]
    blockers = [item for item in queue_items if item.get("readiness_status") in {"NEEDS_VISUAL_ASSET", "NEEDS_EVIDENCE", "BLOCKED"}]
    return {
        "calendar_summary": calendar_payload.get("summary") if isinstance(calendar_payload.get("summary"), dict) else {},
        "queue_summary": queue_payload.get("summary") if isinstance(queue_payload.get("summary"), dict) else {},
        "rhythm_summary": rhythm_payload.get("summary") if isinstance(rhythm_payload.get("summary"), dict) else {},
        "archive_summary": archive_payload.get("summary") if isinstance(archive_payload.get("summary"), dict) else {},
        "metrics_review_summary": metrics_review_payload.get("summary") if isinstance(metrics_review_payload.get("summary"), dict) else {},
        "closeout_summary": closeout_payload.get("summary") if isinstance(closeout_payload.get("summary"), dict) else {},
        "calendar": list_payload(calendar_payload, "calendar")[:7],
        "today_recommendations": today_items[:5],
        "this_week_recommendations": this_week_items[:8],
        "blockers": blockers[:8],
        "weekly_rhythm": list_payload(rhythm_payload, "rhythm_plan"),
        "published_articles": list_payload(archive_payload, "articles")[:8],
        "metrics_insights": metrics_review_payload.get("insights") if isinstance(metrics_review_payload.get("insights"), list) else [],
        "operator_actions": closeout_payload.get("operator_actions") if isinstance(closeout_payload.get("operator_actions"), list) else [],
        "policy": {
            "manual_ops_only": True,
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_session_creation": True,
            "no_auto_metrics_input": True,
        },
    }


def build_content_hardening_panel(paths: ProjectPaths) -> dict[str, Any]:
    trial_payload = read_json(paths.logs_root / "latest_one_week_trial_run_protocol.json")
    failure_payload = read_json(paths.logs_root / "latest_content_ops_failure_handling.json")
    regression_payload = read_json(paths.logs_root / "latest_publishing_checklist_regression.json")
    runbook_payload = read_json(paths.logs_root / "latest_operator_runbook.json")
    closeout_payload = read_json(paths.logs_root / "latest_phase0_19_system_closeout.json")
    phase20_payload = read_json(paths.logs_root / "latest_phase20_daily_hardening_pipeline.json")
    failure_issues = list_payload(failure_payload, "issues")
    regression_checks = list_payload(regression_payload, "checks")
    runbook_sections = list_payload(runbook_payload, "sections")
    trial_routine = trial_payload.get("daily_routine") if isinstance(trial_payload.get("daily_routine"), list) else []
    trial_checklist = trial_payload.get("daily_checklist") if isinstance(trial_payload.get("daily_checklist"), list) else []
    closeout_readiness = closeout_payload.get("trial_readiness") if isinstance(closeout_payload.get("trial_readiness"), dict) else {}
    return {
        "trial_summary": {
            "days": ((trial_payload.get("trial_period") or {}).get("days") if isinstance(trial_payload.get("trial_period"), dict) else 0),
            "daily_checklist_count": len(trial_checklist),
            "success_criteria_count": len(trial_payload.get("success_criteria", [])) if isinstance(trial_payload.get("success_criteria"), list) else 0,
        },
        "failure_summary": failure_payload.get("summary") if isinstance(failure_payload.get("summary"), dict) else {},
        "regression_summary": regression_payload.get("summary") if isinstance(regression_payload.get("summary"), dict) else {},
        "runbook_status": runbook_payload.get("current_status") if isinstance(runbook_payload.get("current_status"), dict) else {},
        "system_closeout_readiness": closeout_readiness,
        "phase20_summary": phase20_payload.get("summary") if isinstance(phase20_payload.get("summary"), dict) else {},
        "daily_routine": [item for item in trial_routine if isinstance(item, dict)][:7],
        "daily_checklist": [str(item) for item in trial_checklist[:10]],
        "failure_issues": failure_issues[:8],
        "regression_checks": regression_checks[:10],
        "runbook_sections": runbook_sections[:8],
        "known_gaps": closeout_payload.get("known_gaps") if isinstance(closeout_payload.get("known_gaps"), list) else [],
        "policy": {
            "hardening_only": True,
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_metrics_input": True,
            "no_auto_image_generation": True,
            "no_config_prompt_rule_changes": True,
        },
    }


def critic_summary(critic: dict[str, Any]) -> str:
    concerns = critic.get("main_concerns")
    if isinstance(concerns, list) and concerns:
        return "; ".join(str(item) for item in concerns[:2])
    return str(critic.get("severity") or "")


def revision_summary(revision: dict[str, Any]) -> str:
    fixes = []
    for key in ("title_fixes", "opening_fixes", "logic_fixes", "evidence_fixes"):
        raw = revision.get(key)
        if isinstance(raw, list):
            fixes.extend(str(item) for item in raw[:1])
    return "; ".join(fixes[:3])


def build_wechat_workbench_data(paths: ProjectPaths) -> WechatWorkbenchDataReport:
    market = paths.market_content_root
    topic_root = market / "03_topic_candidates"
    draft_root = market / "05_draft_packs"
    review_root = market / "06_review_queue"
    publishing_root = market / "07_publishing"
    candidates_payload = read_json(topic_root / "latest_high_value_candidates.json")
    packages_payload = read_json(draft_root / "latest_platform_packages.json")
    quality_payload = read_json(draft_root / "latest_content_quality_review.json")
    reviews_payload = read_json(review_root / "latest_agent_review_queue.json")
    proponent_payload = read_json(review_root / "latest_proponent_reviews.json")
    critic_payload = read_json(review_root / "latest_critic_reviews.json")
    judge_payload = read_json(review_root / "latest_judge_gate.json")
    revision_payload = read_json(review_root / "latest_revision_instructions.json")
    publishing_payload = read_json(publishing_root / "latest_publishing_candidate_queue.json")
    runtime_summary = read_json(paths.logs_root / "latest_runtime_store_summary.json")
    phase8 = read_json(paths.logs_root / "latest_phase8_daily_production_pipeline.json")
    cost = read_json(paths.logs_root / "latest_cost_budget_guard.json")
    ab = read_json(paths.logs_root / "latest_llm_ab_comparison.json")
    run_date = str(packages_payload.get("run_date") or candidates_payload.get("run_date") or today_token()).replace("-", "")[:8]
    warnings: list[str] = []

    candidates = list_payload(candidates_payload, "candidates")
    packages = list_payload(packages_payload, "packages")
    review_items_by_package = by_key(list_payload(reviews_payload, "items"), "package_id")
    quality_by_package = by_key(list_payload(quality_payload, "reviews"), "package_id")
    proponent_by_review = by_key(list_payload(proponent_payload, "reviews"), "review_item_id")
    critic_by_review = by_key(list_payload(critic_payload, "reviews"), "review_item_id")
    judge_by_package = by_key(list_payload(judge_payload, "decisions"), "package_id")
    revision_by_package = by_key(list_payload(revision_payload, "instructions"), "package_id")
    publishing_by_package = by_key(list_payload(publishing_payload, "candidates"), "package_id")
    topics = build_topics(candidates)
    articles: list[dict[str, Any]] = []
    for index, package in enumerate(packages):
        package_id = str(package.get("package_id") or "")
        review = review_items_by_package.get(package_id, {})
        judge = judge_by_package.get(package_id, {})
        revision = revision_by_package.get(package_id, {})
        publishing_candidate = publishing_by_package.get(package_id, {})
        critic = critic_by_review.get(str(review.get("review_item_id") or ""), {})
        proponent = proponent_by_review.get(str(review.get("review_item_id") or ""), {})
        quality = quality_by_package.get(package_id, {})
        wechat = package.get("wechat") if isinstance(package.get("wechat"), dict) else {}
        article_title = str(wechat.get("title") or package.get("title") or review.get("title") or "")
        topic = find_topic_for_article(article_title, topics, index)
        source_ids = review.get("source_ids") or publishing_candidate.get("source_ids") or topic.get("source_ids") or []
        evidence_ids = review.get("evidence_ids") or publishing_candidate.get("evidence_ids") or topic.get("evidence_ids") or []
        status = status_from(judge, publishing_candidate, package)
        article_id = f"article_{package_id}" if package_id else f"article_{len(articles) + 1}"
        articles.append(
            {
                "article_id": article_id,
                "topic_id": topic.get("topic_id") or "",
                "brief_id": package.get("brief_id") or "",
                "draft_id": package.get("draft_id") or "",
                "package_id": package_id,
                "title": article_title,
                "wechat_title": wechat.get("title") or "",
                "wechat_body_markdown": wechat.get("body_markdown") or "",
                "status": status,
                "quality_score": safe_float(quality.get("quality_score") or review.get("quality_score")),
                "topic_score": safe_float(topic.get("score")),
                "score_band": topic.get("score_band") or "",
                "recommended_action": topic.get("recommended_action") or "",
                "why_it_matters": topic.get("why_it_matters") or "",
                "judge_decision": judge.get("decision") or "",
                "critic_summary": critic_summary(critic),
                "proponent_summary": proponent.get("publish_argument") or "",
                "revision_summary": revision_summary(revision),
                "publishing_candidate_id": publishing_candidate.get("publishing_candidate_id") or "",
                "source_ids": source_ids,
                "evidence_ids": evidence_ids,
                "source_count": len(source_ids) if isinstance(source_ids, list) else 0,
                "evidence_count": len(evidence_ids) if isinstance(evidence_ids, list) else 0,
                "next_step": next_step_for_status(status, str(judge.get("decision") or "")),
            }
        )
    topic_status_rank = {"ready": 4, "needs_revision": 3, "recommended": 2, "hold": 1}
    topic_status: dict[str, str] = {}
    for article in articles:
        topic_id = str(article.get("topic_id") or "")
        status = str(article.get("status") or "recommended")
        if topic_id and topic_status_rank.get(status, 0) > topic_status_rank.get(topic_status.get(topic_id, ""), 0):
            topic_status[topic_id] = status
    for topic in topics:
        topic_id = str(topic.get("topic_id") or "")
        if topic_id in topic_status:
            topic["status"] = topic_status[topic_id]
    if not articles:
        warnings.append("No platform packages found for WeChat article preview.")
    selected = next((item for item in articles if item.get("publishing_candidate_id")), None)
    if selected is None:
        selected = next((item for item in articles if item.get("status") == "ready"), None)
    if selected is None and articles:
        selected = sorted(articles, key=lambda item: safe_float(item.get("quality_score")), reverse=True)[0]
    selected_article_id = str(selected.get("article_id")) if selected else ""
    ready_count = sum(1 for item in articles if item.get("status") == "ready")
    needs_revision_count = sum(1 for item in articles if item.get("status") == "needs_revision")
    summary = {
        "topic_count": len(topics),
        "article_count": len(articles),
        "publishing_candidate_count": len(publishing_by_package),
        "needs_revision_count": needs_revision_count,
        "ready_count": ready_count,
        "llm_judge_conflict_count": safe_int((ab.get("summary") or {}).get("judge_decision_conflict_count")) if isinstance(ab.get("summary"), dict) else 0,
    }
    version_review = build_version_review(paths, selected_article_id)
    final_review = build_final_review(paths, selected_article_id)
    performance_panel = build_performance_panel(paths, final_review)
    methodology_panel = build_methodology_panel(paths, selected_article_id, articles)
    generation_visual_panel = build_generation_visual_panel(paths, selected_article_id, articles)
    live_pilot_panel = build_live_pilot_panel(paths)
    image_asset_panel = build_image_asset_panel(paths)
    publishing_pack_panel = build_publishing_pack_panel(paths)
    content_ops_panel = build_content_ops_panel(paths)
    content_hardening_panel = build_content_hardening_panel(paths)
    summary["version_comparison_count"] = version_review.get("comparison_count", 0)
    summary["version_accept_recommended"] = version_review.get("accept_recommended", 0)
    summary["final_candidate_count"] = final_review.get("candidate_count", 0)
    summary["final_ready_count"] = final_review.get("ready_for_final_review", 0)
    summary["manual_publish_session_count"] = safe_int((performance_panel.get("session_summary") or {}).get("session_count"))
    summary["post_publish_metrics_count"] = safe_int((performance_panel.get("metrics_summary") or {}).get("metrics_count"))
    summary["performance_record_count"] = safe_int((performance_panel.get("performance_memory_summary") or {}).get("record_count"))
    summary["methodology_topic_count"] = safe_int((methodology_panel.get("topic_summary") or {}).get("topic_count"))
    summary["methodology_article_count"] = safe_int((methodology_panel.get("article_summary") or {}).get("article_count"))
    summary["methodology_brief_count"] = safe_int((generation_visual_panel.get("brief_summary") or {}).get("brief_count"))
    summary["article_visual_plan_count"] = safe_int((generation_visual_panel.get("visual_plan_summary") or {}).get("plan_count"))
    summary["image_asset_request_count"] = safe_int((generation_visual_panel.get("image_request_summary") or {}).get("request_count"))
    summary["live_output_comparison_count"] = safe_int((live_pilot_panel.get("comparison_summary") or {}).get("comparison_count"))
    summary["image_generation_approval_count"] = safe_int((live_pilot_panel.get("image_approval_summary") or {}).get("request_count"))
    summary["live_pilot_attempted_count"] = safe_int((live_pilot_panel.get("phase16_summary") or {}).get("live_attempted_count"))
    summary["promoted_live_candidate_count"] = safe_int((image_asset_panel.get("live_content_promotion_summary") or {}).get("candidate_count"))
    summary["manual_image_task_count"] = safe_int((image_asset_panel.get("manual_image_task_summary") or {}).get("task_count"))
    summary["image_asset_count"] = safe_int((image_asset_panel.get("image_asset_library_summary") or {}).get("asset_count"))
    summary["visual_review_count"] = safe_int((image_asset_panel.get("final_visual_review_summary") or {}).get("review_count"))
    summary["visual_final_candidate_count"] = safe_int((publishing_pack_panel.get("visual_candidate_summary") or {}).get("candidate_count"))
    summary["wechat_copy_pack_count"] = safe_int((publishing_pack_panel.get("copy_pack_summary") or {}).get("pack_count"))
    summary["visual_publishing_checklist_count"] = safe_int((publishing_pack_panel.get("visual_checklist_summary") or {}).get("checklist_count"))
    summary["content_ops_queue_count"] = safe_int((content_ops_panel.get("queue_summary") or {}).get("item_count"))
    summary["publishing_calendar_slots"] = safe_int((content_ops_panel.get("calendar_summary") or {}).get("planned_slots"))
    summary["published_article_archive_count"] = safe_int((content_ops_panel.get("archive_summary") or {}).get("article_count"))
    summary["content_ops_failure_issue_count"] = safe_int((content_hardening_panel.get("failure_summary") or {}).get("issue_count"))
    summary["publishing_checklist_regression_status"] = (content_hardening_panel.get("regression_summary") or {}).get("regression_status", "UNKNOWN")
    summary["phase20_trial_readiness"] = (content_hardening_panel.get("system_closeout_readiness") or {}).get("status", "UNKNOWN")
    runtime_payload = runtime_summary.get("summary") if isinstance(runtime_summary.get("summary"), dict) else {}
    system_status = {
        "runtime_store": f"pipelines={runtime_payload.get('pipeline_runs', 0)}, artifacts={runtime_payload.get('content_artifacts', 0)}",
        "phase8_status": phase8.get("status") or "UNKNOWN",
        "cost_guard": cost.get("status") or "UNKNOWN",
        "live_mode": os.environ.get("THCAP_LLM_MODE", "dry_run"),
    }
    return WechatWorkbenchDataReport(
        SCHEMA_VERSION,
        utc_now(),
        run_date,
        summary,
        tuple(topics),
        tuple(articles),
        selected_article_id,
        system_status,
        version_review,
        final_review,
        performance_panel,
        methodology_panel,
        generation_visual_panel,
        live_pilot_panel,
        image_asset_panel,
        publishing_pack_panel,
        content_ops_panel,
        content_hardening_panel,
        tuple(warnings),
    )


def write_wechat_workbench_data(report: WechatWorkbenchDataReport, paths: ProjectPaths, repo_root: Path) -> dict[str, Path]:
    outputs = output_paths(paths, report.run_date)
    payload = asdict(report)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    summary_payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": report.generated_at,
        "run_date": report.run_date,
        "summary": report.summary,
        "selected_article_id": report.selected_article_id,
        "system_status": report.system_status,
        "version_review": report.version_review,
        "final_review": report.final_review,
        "performance_panel": report.performance_panel,
        "methodology_panel": report.methodology_panel,
        "generation_visual_panel": report.generation_visual_panel,
        "live_pilot_panel": report.live_pilot_panel,
        "image_asset_panel": report.image_asset_panel,
        "publishing_pack_panel": report.publishing_pack_panel,
        "content_ops_panel": report.content_ops_panel,
        "content_hardening_panel": report.content_hardening_panel,
        "warnings": report.warnings,
    }
    for key, path in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if key.startswith("summary"):
            path.write_text(json.dumps(summary_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return outputs


def report_to_dict(report: WechatWorkbenchDataReport) -> dict[str, Any]:
    return asdict(report)

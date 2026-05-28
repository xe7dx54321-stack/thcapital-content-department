"""Execute approved rewrite actions with methodology guidance."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"
REWRITE_ACTION_TYPES = {"rewrite_instruction", "rewrite_angle", "title_rewrite_request", "opening_rewrite_request"}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "09_workbench_actions" / "versions"
    return {
        "dated_json": root / f"{run_date}__methodology-rewrite-versions.json",
        "dated_md": root / f"{run_date}__methodology-rewrite-versions.md",
        "latest_json": root / "latest_methodology_rewrite_versions.json",
        "latest_md": root / "latest_methodology_rewrite_versions.md",
    }


def make_id(prefix: str, run_date: str, *parts: object) -> str:
    digest = hashlib.sha1("|".join(str(part) for part in (run_date, *parts)).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{run_date}_{digest}"


def approved_actions(paths: ProjectPaths) -> list[dict[str, Any]]:
    payload = read_json(paths.market_content_root / "09_workbench_actions" / "latest_approved_actions.json")
    return [
        action
        for action in list_payload(payload, "actions")
        if action.get("approval_status") == "APPROVED" and action.get("action_type") in REWRITE_ACTION_TYPES
    ]


def draft_by_article_id(paths: ProjectPaths) -> dict[str, dict[str, Any]]:
    payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_methodology_content_drafts.json")
    result: dict[str, dict[str, Any]] = {}
    for draft in list_payload(payload, "drafts"):
        for key in ("draft_id", "topic_id", "brief_id"):
            value = str(draft.get(key) or "")
            if value:
                result[value] = draft
    workbench = read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    for article in list_payload(workbench, "articles"):
        article_id = str(article.get("article_id") or "")
        if article_id:
            result.setdefault(
                article_id,
                {
                    "draft_id": article_id,
                    "selected_title": article.get("wechat_title") or article.get("title") or "",
                    "opening": "",
                    "body_markdown": article.get("wechat_body_markdown") or "",
                },
            )
    return result


def review_by_article_id(paths: ProjectPaths) -> dict[str, dict[str, Any]]:
    payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_methodology_article_review.json")
    return {str(item.get("article_id")): item for item in list_payload(payload, "articles") if item.get("article_id")}


def focus_from_review(review: dict[str, Any], action: dict[str, Any]) -> list[str]:
    focus: list[str] = []
    scores = review.get("scores") if isinstance(review.get("scores"), dict) else {}
    if scores.get("core_judgment", 10) < 7:
        focus.append("strengthen_core_judgment")
    if scores.get("judgment_density", 10) < 7 or review.get("generic_language_flags"):
        focus.append("increase_judgment_density")
    if scores.get("clear_question", 10) < 7:
        focus.append("improve_opening_tension")
    if scores.get("evidence_fit", 10) < 7:
        focus.append("align_evidence_to_claim")
    if scores.get("risk_balance", 10) < 7:
        focus.append("add_risk_balance")
    description = str(action.get("description") or "")
    if "标题" in description:
        focus.append("rewrite_title")
    if "开头" in description:
        focus.append("improve_opening_tension")
    return list(dict.fromkeys(focus)) or ["increase_judgment_density", "strengthen_core_judgment"]


def rewrite(draft: dict[str, Any], review: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
    title = str(draft.get("selected_title") or draft.get("title") or "未命名文章")
    body = str(draft.get("body_markdown") or "")
    focus = focus_from_review(review, action)
    focus_notes = "\n".join(f"- {item}" for item in focus)
    issue_notes = "\n".join(f"- {item}" for item in (review.get("weaknesses") or [])[:5]) or "- 方法论问题需人工继续确认。"
    new_title = title
    if "rewrite_title" in focus or action.get("action_type") == "title_rewrite_request":
        new_title = f"{title}：真正值得判断的变化是什么"
    new_opening = (
        f"这篇文章需要先回答一个更尖锐的问题：{title} 到底改变了什么判断？"
        "如果它只是普通新闻，就不值得写；如果它改变任务入口、产业链分工或投资预期，就必须把证据链讲清楚。"
    )
    body_without_title = "\n".join(line for line in body.splitlines() if not line.startswith("# ")).strip()
    new_body = f"""# {new_title}

{new_opening}

## 本次方法论改写重点

{focus_notes}

## 原稿主要问题

{issue_notes}

{body_without_title}

## 方法论补强后的结尾

这篇文章最终要留下的不是“值得关注”，而是一句可复述的判断：这条 AI/Agent 信号改变了谁的预期、影响哪条链路，以及下一步应该观察什么。
"""
    return {"focus": focus, "new_title": new_title, "new_opening": new_opening, "new_body_markdown": new_body}


def execute_methodology_rewrite_actions(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    approved_payload = read_json(paths.market_content_root / "09_workbench_actions" / "latest_approved_actions.json")
    draft_payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_methodology_content_drafts.json")
    run_date = str(draft_payload.get("run_date") or approved_payload.get("run_date") or today_token()).replace("-", "")[:8]
    drafts = draft_by_article_id(paths)
    reviews = review_by_article_id(paths)
    versions: list[dict[str, Any]] = []
    for action in approved_actions(paths):
        target = str(action.get("target_artifact_id") or "")
        draft = drafts.get(target) or next(iter(drafts.values()), {})
        review = reviews.get(target) or next(iter(reviews.values()), {})
        if not draft:
            versions.append(
                {
                    "version_id": make_id("mver", run_date, action.get("action_id"), "missing"),
                    "source_action_id": action.get("action_id"),
                    "source_article_id": target,
                    "rewrite_focus": [],
                    "methodology_issues_addressed": [],
                    "new_title": "",
                    "new_opening": "",
                    "new_body_markdown": "",
                    "change_summary": "No source draft found.",
                    "do_not_overwrite_original": True,
                    "status": "FAILED",
                }
            )
            continue
        result = rewrite(draft, review, action)
        versions.append(
            {
                "version_id": make_id("mver", run_date, action.get("action_id"), result["new_body_markdown"]),
                "source_action_id": action.get("action_id"),
                "source_article_id": target or draft.get("draft_id") or "",
                "rewrite_focus": result["focus"],
                "methodology_issues_addressed": review.get("weaknesses") or [],
                "new_title": result["new_title"],
                "new_opening": result["new_opening"],
                "new_body_markdown": result["new_body_markdown"],
                "change_summary": action.get("description") or "Methodology-aware rule-based rewrite.",
                "do_not_overwrite_original": True,
                "status": "GENERATED",
            }
        )
    summary = {"version_count": len(versions), "generated": sum(1 for item in versions if item.get("status") == "GENERATED"), "failed": sum(1 for item in versions if item.get("status") == "FAILED")}
    status = "SUCCESS" if versions else "SUCCESS_EMPTY"
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "status": status, "versions": versions, "summary": summary}
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('version_id')}` | `{item.get('source_action_id')}` | `{item.get('status')}` | {', '.join(item.get('rewrite_focus') or [])} |"
        for item in list_payload(payload, "versions")
    ) or "| - | - | SUCCESS_EMPTY | No approved methodology rewrite actions |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Methodology Rewrite Versions

## Summary

- status: `{payload.get('status')}`
- version_count: `{summary.get('version_count', 0)}`
- generated: `{summary.get('generated', 0)}`
- failed: `{summary.get('failed', 0)}`
- do_not_overwrite_original: `true`

| Version | Source Action | Status | Focus |
|---|---|---|---|
{rows}
"""

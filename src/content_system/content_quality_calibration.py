"""Calibrate content quality issues from stable trial records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


QUALITY_AREA_BY_SCORE = {
    "clear_question": "opening",
    "core_judgment": "core_judgment",
    "logic_progression": "logic",
    "evidence_fit": "evidence",
    "narrative_tension": "opening",
    "reader_relevance": "wechat_readability",
    "judgment_density": "core_judgment",
    "risk_balance": "risk_balance",
    "wechat_readability": "wechat_readability",
    "memorability": "core_judgment",
}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__content-quality-calibration.json",
        "dated_md": paths.logs_root / f"{run_date}__content-quality-calibration.md",
        "latest_json": paths.logs_root / "latest_content_quality_calibration.json",
        "latest_md": paths.logs_root / "latest_content_quality_calibration.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__content-quality-calibration-board.md",
        "board_latest_md": paths.frontstage_root / "latest_content_quality_calibration_board.md",
    }


def severity_for_score(score: float) -> str:
    if score < 5.5:
        return "HIGH"
    if score < 6.5:
        return "MEDIUM"
    return "LOW"


def issue_from_article(article: dict[str, Any], score_key: str, score: float) -> dict[str, Any]:
    area = QUALITY_AREA_BY_SCORE.get(score_key, "logic")
    severity = severity_for_score(score)
    blocks = severity == "HIGH" and area in {"core_judgment", "evidence", "logic", "wechat_readability"}
    return {
        "issue_id": make_id("quality_issue", article.get("article_id"), score_key),
        "article_id": article.get("article_id", ""),
        "area": area,
        "severity": severity,
        "blocks_publish": blocks,
        "description": f"{score_key} score is {score:.1f}, slowing publish readiness.",
        "recommended_fix": recommended_fix(area),
        "source": "methodology_review",
    }


def recommended_fix(area: str) -> str:
    mapping = {
        "title": "Rewrite title so it states the change and avoids vague promise language.",
        "opening": "Make the opening ask a concrete reader question and surface the expectation gap.",
        "core_judgment": "Strengthen one-sentence core judgment before adding more material.",
        "evidence": "Attach evidence to each claim; hold if no first-hand or credible source exists.",
        "logic": "Reorder sections so every paragraph advances the argument.",
        "visual": "Finish visual assets or explicitly keep image slots as blockers.",
        "wechat_readability": "Shorten dense paragraphs and improve mobile scan path.",
        "risk_balance": "Add counterargument and uncertainty before final checklist.",
    }
    return mapping.get(area, "Operator should review and decide whether this blocks publishing.")


def build_content_quality_calibration(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    publishing = paths.market_content_root / "07_publishing"
    days = [read_json(paths.logs_root / f"latest_stable_trial_day_{day}.json") for day in range(1, 4)]
    article_review = read_json(paths.market_content_root / "05_draft_packs" / "latest_methodology_article_review.json")
    drafts = read_json(paths.market_content_root / "05_draft_packs" / "latest_methodology_content_drafts.json")
    queue_repair = read_json(publishing / "latest_content_queue_readiness_repair.json")
    copy_pack = read_json(publishing / "latest_wechat_copy_pack_with_images.json")
    visual_checklist = read_json(publishing / "latest_visual_publishing_checklist.json")
    metrics_review = read_json(paths.logs_root / "latest_post_publish_metrics_review.json")
    warnings = []
    for index, day_payload in enumerate(days, start=1):
        if not day_payload:
            warnings.append(f"Missing stable trial day {index}.")

    quality_issues: list[dict[str, Any]] = []
    articles = list_payload(article_review, "articles")
    for article in articles:
        scores = article.get("scores") if isinstance(article.get("scores"), dict) else {}
        for score_key, raw_score in scores.items():
            try:
                score = float(raw_score)
            except (TypeError, ValueError):
                continue
            if score < 6.5:
                quality_issues.append(issue_from_article(article, score_key, score))
        for weakness in article.get("weaknesses") or []:
            text = str(weakness)
            area = "opening" if "开头" in text else "core_judgment" if "判断" in text else "logic"
            quality_issues.append(
                {
                    "issue_id": make_id("quality_issue", article.get("article_id"), text),
                    "article_id": article.get("article_id", ""),
                    "area": area,
                    "severity": "MEDIUM",
                    "blocks_publish": False,
                    "description": text,
                    "recommended_fix": recommended_fix(area),
                    "source": "methodology_review",
                }
            )
    for item in list_payload(queue_repair, "items"):
        if item.get("repaired_readiness_status") in {"NEEDS_EVIDENCE", "NEEDS_REWRITE"}:
            area = "evidence" if item.get("repaired_readiness_status") == "NEEDS_EVIDENCE" else "logic"
            quality_issues.append(
                {
                    "issue_id": make_id("quality_issue", item.get("queue_item_id"), area),
                    "article_id": item.get("queue_item_id", ""),
                    "area": area,
                    "severity": "HIGH",
                    "blocks_publish": True,
                    "description": f"Queue readiness remains {item.get('repaired_readiness_status')}: {item.get('title')}",
                    "recommended_fix": item.get("next_operator_action") or recommended_fix(area),
                    "source": "trial",
                }
            )
    for checklist in list_payload(visual_checklist, "checklists"):
        for check in checklist.get("checks") or []:
            if check.get("status") in {"WARN", "FAIL"}:
                quality_issues.append(
                    {
                        "issue_id": make_id("quality_issue", checklist.get("visual_checklist_id"), check.get("check_id")),
                        "article_id": checklist.get("visual_final_candidate_id", ""),
                        "area": "visual",
                        "severity": "HIGH" if check.get("status") == "FAIL" else "MEDIUM",
                        "blocks_publish": check.get("status") == "FAIL",
                        "description": f"{check.get('label')}: {check.get('note')}",
                        "recommended_fix": "Complete visual checklist and remove image slot blockers before manual publish.",
                        "source": "visual_checklist",
                    }
                )

    area_counts: dict[str, int] = {}
    blocking_counts: dict[str, int] = {}
    for issue in quality_issues:
        area = str(issue.get("area") or "logic")
        area_counts[area] = area_counts.get(area, 0) + 1
        if issue.get("blocks_publish"):
            blocking_counts[area] = blocking_counts.get(area, 0) + 1
    most_common_area = max(area_counts.items(), key=lambda item: item[1])[0] if area_counts else "none"
    recommendations = [
        {
            "recommendation_id": make_id("qcal", run_date, "review_weight", most_common_area),
            "target": "article_quality_methodology",
            "recommendation": f"Review whether `{most_common_area}` should be more prominent in methodology review and workbench warnings.",
            "reason": f"`{most_common_area}` appears in {area_counts.get(most_common_area, 0)} quality issue(s).",
            "auto_apply": False,
        },
        {
            "recommendation_id": make_id("qcal", run_date, "operator_runbook"),
            "target": "operator_runbook",
            "recommendation": "Add a daily calibration step: pick one READY_FOR_REVIEW item and resolve its top title/opening/evidence blocker.",
            "reason": "Stable trial is actionable but still lacks READY_TO_PUBLISH items.",
            "auto_apply": False,
        },
    ]
    if any(issue.get("area") == "visual" for issue in quality_issues):
        recommendations.append(
            {
                "recommendation_id": make_id("qcal", run_date, "visual_methodology"),
                "target": "visual_methodology",
                "recommendation": "Keep visual readiness as an explicit publish blocker until assets and mobile readability are reviewed.",
                "reason": "Visual checklist contains warnings and copy pack still needs visual assets.",
                "auto_apply": False,
            }
        )

    summary = {
        "article_count": len(articles) or len(list_payload(drafts, "drafts")),
        "quality_issue_count": len(quality_issues),
        "publish_blocking_quality_issues": sum(1 for issue in quality_issues if issue.get("blocks_publish")),
        "calibration_recommendation_count": len(recommendations),
        "copy_pack_count": len(list_payload(copy_pack, "packs")),
        "metrics_review_insights": len(metrics_review.get("insights", [])) if isinstance(metrics_review.get("insights"), list) else 0,
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "summary": summary,
        "quality_issues": quality_issues,
        "calibration_recommendations": recommendations,
        "warnings": warnings,
        "policy": {"auto_apply": False, "no_config_prompt_rule_changes": True, "sidecar_only": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        f"| `{item.get('severity')}` | `{item.get('area')}` | `{item.get('blocks_publish')}` | {item.get('article_id')} | {item.get('description')} |"
        for item in list_payload(payload, "quality_issues")[:30]
    ]
    recs = "\n".join(f"- {item.get('target')}: {item.get('recommendation')}" for item in list_payload(payload, "calibration_recommendations"))
    return f"""# Content Quality Calibration

## Summary

- article_count: `{summary.get('article_count', 0)}`
- quality_issue_count: `{summary.get('quality_issue_count', 0)}`
- publish_blocking_quality_issues: `{summary.get('publish_blocking_quality_issues', 0)}`
- calibration_recommendation_count: `{summary.get('calibration_recommendation_count', 0)}`

| Severity | Area | Blocks publish | Article | Description |
|---|---|---|---|---|
{chr(10).join(rows)}

## Recommendations

{recs}
"""

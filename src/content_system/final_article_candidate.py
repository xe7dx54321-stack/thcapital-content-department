"""Build final article candidates from promoted versions."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class FinalArticleCandidateResult:
    run_date: str
    candidate_count: int
    ready_for_final_review: int
    needs_final_check: int
    hold: int
    output_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__final-article-candidates.json",
        "dated_md": root / f"{run_date}__final-article-candidates.md",
        "latest_json": root / "latest_final_article_candidates.json",
        "latest_md": root / "latest_final_article_candidates.md",
    }


def by_key(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(key)): item for item in items if item.get(key)}


def final_candidate_id(run_date: str, promotion_id: str, version_id: str) -> str:
    digest = hashlib.sha1(f"{run_date}|{promotion_id}|{version_id}".encode("utf-8")).hexdigest()[:12]
    return f"final_{run_date}_{digest}"


def readiness_for(promotion: dict[str, Any], comparison: dict[str, Any], dry_run: dict[str, Any]) -> tuple[str, list[str], list[str]]:
    reasons: list[str] = []
    risks: list[str] = []
    title = str(promotion.get("new_title") or "")
    body = str(promotion.get("new_body_markdown") or "")
    human_score = safe_float(promotion.get("human_score"))
    score_delta = safe_float(promotion.get("score_delta"))
    regressions = comparison.get("regressions") if isinstance(comparison.get("regressions"), list) else []
    if title:
        reasons.append("Promoted version has a final candidate title.")
    else:
        risks.append("Missing title.")
    if len(body) > 500:
        reasons.append("Body is long enough for final review.")
    else:
        risks.append("Body is short or missing.")
    if human_score >= 8:
        reasons.append("Human score is at least 8.")
    else:
        risks.append("Human score below 8 or missing.")
    if score_delta >= 0:
        reasons.append("Version score delta is non-negative.")
    else:
        risks.append("Version score delta is negative.")
    risks.extend(str(item) for item in regressions[:4])
    dry_summary = dry_run.get("summary") if isinstance(dry_run.get("summary"), dict) else {}
    if safe_float(dry_summary.get("not_ready_count")) > 0:
        risks.append("Publishing dry-run has not-ready items; final review must re-check platform format.")
    if not title or not body:
        return "HOLD", reasons, risks
    if risks:
        return "NEEDS_FINAL_CHECK", reasons, risks
    return "READY_FOR_FINAL_REVIEW", reasons, risks


def build_final_article_candidates(paths: ProjectPaths, repo_root: Path) -> tuple[FinalArticleCandidateResult, dict[str, Any]]:
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    promoted_payload = read_json(versions_root / "latest_promoted_versions.json")
    comparisons = by_key(list_payload(read_json(versions_root / "latest_version_comparison_scores.json"), "comparisons"), "version_id")
    regression = read_json(paths.logs_root / "latest_prompt_rule_regression_dashboard.json")
    dry_run = read_json(paths.market_content_root / "07_publishing" / "latest_publishing_dry_run.json")
    run_date = str(promoted_payload.get("run_date") or today_token()).replace("-", "")[:8]
    candidates: list[dict[str, Any]] = []
    regression_suggestions = list_payload(regression, "suggestions")
    for promotion in list_payload(promoted_payload, "promoted_versions"):
        comparison = comparisons.get(str(promotion.get("version_id") or ""), {})
        status, reasons, risks = readiness_for(promotion, comparison, dry_run)
        if regression_suggestions:
            risks.append("Prompt/rule regression dashboard has suggestions; human should review before final publish.")
        candidates.append(
            {
                "final_candidate_id": final_candidate_id(run_date, str(promotion.get("promotion_id") or ""), str(promotion.get("version_id") or "")),
                "promotion_id": promotion.get("promotion_id") or "",
                "version_id": promotion.get("version_id") or "",
                "source_article_id": promotion.get("source_article_id") or "",
                "title": promotion.get("new_title") or "",
                "body_markdown": promotion.get("new_body_markdown") or "",
                "wechat_title": promotion.get("new_title") or "",
                "wechat_body_markdown": promotion.get("new_body_markdown") or "",
                "version_score_delta": safe_float(promotion.get("score_delta")),
                "human_score": promotion.get("human_score"),
                "quality_status": status,
                "readiness_reasons": reasons,
                "remaining_risks": risks,
                "final_review_required": True,
                "would_publish": False,
                "do_not_publish": True,
                "do_not_overwrite_original": True,
                "created_at": utc_now(),
            }
        )
    summary = {
        "candidate_count": len(candidates),
        "ready_for_final_review": sum(1 for item in candidates if item.get("quality_status") == "READY_FOR_FINAL_REVIEW"),
        "needs_final_check": sum(1 for item in candidates if item.get("quality_status") == "NEEDS_FINAL_CHECK"),
        "hold": sum(1 for item in candidates if item.get("quality_status") == "HOLD"),
    }
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "candidates": candidates, "summary": summary}
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return (
        FinalArticleCandidateResult(
            run_date,
            summary["candidate_count"],
            summary["ready_for_final_review"],
            summary["needs_final_check"],
            summary["hold"],
            repo_relative(outputs["latest_json"], repo_root),
        ),
        payload,
    )


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('final_candidate_id')}` | `{item.get('version_id')}` | `{item.get('quality_status')}` | `{item.get('would_publish')}` | {item.get('title') or ''} |"
        for item in list_payload(payload, "candidates")
    ) or "| - | - | SUCCESS_EMPTY | false | No promoted versions |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Final Article Candidates

## Summary

- Run date: `{payload.get('run_date')}`
- Candidates: `{summary.get('candidate_count', 0)}`
- Ready for final review: `{summary.get('ready_for_final_review', 0)}`
- Needs final check: `{summary.get('needs_final_check', 0)}`
- Hold: `{summary.get('hold', 0)}`
- Policy: `would_publish=false` for every candidate.

| Candidate | Version | Status | Would Publish | Title |
|---|---|---|---|---|
{rows}
"""

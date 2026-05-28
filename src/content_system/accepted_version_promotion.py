"""Promote human-accepted article versions into final-candidate inputs."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class AcceptedVersionPromotionResult:
    run_date: str
    accepted_version_count: int
    promoted_count: int
    skipped_count: int
    output_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "09_workbench_actions" / "versions"
    return {
        "dated_json": root / f"{run_date}__promoted-versions.json",
        "dated_md": root / f"{run_date}__promoted-versions.md",
        "latest_json": root / "latest_promoted_versions.json",
        "latest_md": root / "latest_promoted_versions.md",
    }


def by_key(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(key)): item for item in items if item.get(key)}


def promotion_id(run_date: str, version_id: str, source_article_id: str) -> str:
    digest = hashlib.sha1(f"{run_date}|{version_id}|{source_article_id}".encode("utf-8")).hexdigest()[:12]
    return f"promo_{run_date}_{digest}"


def article_by_id(workbench_data: dict[str, Any], article_id: str) -> dict[str, Any]:
    for article in list_payload(workbench_data, "articles"):
        article_keys = {
            article.get("article_id"),
            article.get("package_id"),
            article.get("draft_id"),
            f"article_{article.get('package_id')}" if article.get("package_id") else "",
        }
        if article_id in article_keys:
            return article
    return {}


def normalize_title(value: Any) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", str(value or "").lower())


def article_by_title(workbench_data: dict[str, Any], title: str) -> dict[str, Any]:
    needle = normalize_title(title)
    if not needle:
        return {}
    for article in list_payload(workbench_data, "articles"):
        haystacks = [article.get("wechat_title"), article.get("title")]
        if any(normalize_title(value) == needle for value in haystacks):
            return article
    return {}


def title_for_source_article(review_memory: dict[str, Any], source_article_id: str) -> str:
    package_id = source_article_id.removeprefix("article_")
    for record in list_payload(review_memory, "records"):
        if package_id and record.get("package_id") == package_id:
            return str(record.get("title") or "")
    return ""


def choose_best_accepted(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        grouped.setdefault(str(item.get("source_article_id") or item.get("version_id") or ""), []).append(item)
    selected: list[dict[str, Any]] = []
    for rows in grouped.values():
        rows.sort(
            key=lambda item: (
                safe_float(item.get("human_score")),
                safe_float(item.get("score_delta")),
                str(item.get("decided_at") or ""),
            ),
            reverse=True,
        )
        selected.append(rows[0])
    return selected


def build_accepted_version_promotions(paths: ProjectPaths, repo_root: Path) -> tuple[AcceptedVersionPromotionResult, dict[str, Any]]:
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    decisions_payload = read_json(versions_root / "latest_version_review_decisions.json")
    comparisons_payload = read_json(versions_root / "latest_version_comparison_scores.json")
    memory_payload = read_json(versions_root / "article_version_memory.json")
    rewrite_payload = read_json(versions_root / "latest_rewrite_versions.json")
    existing_promotions_payload = read_json(versions_root / "latest_promoted_versions.json")
    workbench_data = read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    review_memory = read_json(paths.market_content_root / "07_publishing" / "review_outcome_memory.json")
    final_candidate_memory = read_json(paths.market_content_root / "07_publishing" / "final_candidate_memory.json")
    run_date = str(decisions_payload.get("run_date") or comparisons_payload.get("run_date") or today_token()).replace("-", "")[:8]
    comparisons = by_key(list_payload(comparisons_payload, "comparisons"), "version_id")
    memories = by_key(list_payload(memory_payload, "versions"), "version_id")
    rewrites = by_key(list_payload(rewrite_payload, "versions"), "version_id")
    accepted: list[dict[str, Any]] = []
    accepted_version_ids: set[str] = set()
    for decision in list_payload(decisions_payload, "decisions"):
        if decision.get("decision") != "ACCEPT":
            continue
        version_id = str(decision.get("version_id") or "")
        comparison = comparisons.get(version_id, {})
        memory = memories.get(version_id, {})
        rewrite = rewrites.get(version_id, {})
        source_article_id = str(decision.get("source_article_id") or comparison.get("source_article_id") or memory.get("source_article_id") or rewrite.get("source_article_id") or "")
        article = article_by_id(workbench_data, source_article_id)
        if not article:
            article = article_by_title(workbench_data, title_for_source_article(review_memory, source_article_id))
        accepted.append(
            {
                "version_id": version_id,
                "source_article_id": source_article_id,
                "source_action_id": decision.get("source_action_id") or comparison.get("source_action_id") or memory.get("source_action_id") or rewrite.get("source_action_id") or "",
                "version_type": comparison.get("version_type") or memory.get("version_type") or rewrite.get("version_type") or "rewrite",
                "human_score": decision.get("human_score"),
                "human_notes": decision.get("human_notes") or "",
                "decided_at": decision.get("decided_at") or "",
                "score_delta": safe_float((comparison.get("scores") or {}).get("delta") or memory.get("score_delta")),
                "new_title": rewrite.get("new_title") or comparison.get("new_title") or article.get("wechat_title") or article.get("title") or "",
                "new_body_markdown": rewrite.get("new_body_markdown") or article.get("wechat_body_markdown") or "",
            }
        )
        accepted_version_ids.add(version_id)
    for final_candidate in list_payload(final_candidate_memory, "final_candidates"):
        version_id = str(final_candidate.get("version_id") or "")
        if not version_id or version_id in accepted_version_ids:
            continue
        if final_candidate.get("status") not in {"active", "reference"}:
            continue
        source_article_id = str(final_candidate.get("source_article_id") or "")
        article = article_by_id(workbench_data, source_article_id)
        if not article:
            article = article_by_title(workbench_data, final_candidate.get("title") or "")
        accepted.append(
            {
                "version_id": version_id,
                "source_article_id": source_article_id,
                "source_action_id": final_candidate.get("source_action_id") or "",
                "version_type": "rewrite",
                "human_score": final_candidate.get("human_score"),
                "human_notes": "Carried forward from final candidate memory.",
                "decided_at": "",
                "score_delta": safe_float(final_candidate.get("version_score_delta")),
                "new_title": article.get("wechat_title") or article.get("title") or final_candidate.get("title") or "",
                "new_body_markdown": article.get("wechat_body_markdown") or "",
            }
        )
        accepted_version_ids.add(version_id)
    for existing_promotion in list_payload(existing_promotions_payload, "promoted_versions"):
        version_id = str(existing_promotion.get("version_id") or "")
        if not version_id or version_id in accepted_version_ids:
            continue
        if existing_promotion.get("human_decision") != "ACCEPT":
            continue
        accepted.append(
            {
                "version_id": version_id,
                "source_article_id": existing_promotion.get("source_article_id") or "",
                "source_action_id": existing_promotion.get("source_action_id") or "",
                "version_type": existing_promotion.get("version_type") or "rewrite",
                "human_score": existing_promotion.get("human_score"),
                "human_notes": existing_promotion.get("human_notes") or "",
                "decided_at": existing_promotion.get("created_at") or "",
                "score_delta": safe_float(existing_promotion.get("score_delta")),
                "new_title": existing_promotion.get("new_title") or "",
                "new_body_markdown": existing_promotion.get("new_body_markdown") or "",
            }
        )
        accepted_version_ids.add(version_id)
    for memory in list_payload(memory_payload, "versions"):
        if memory.get("human_decision") != "ACCEPT":
            continue
        version_id = str(memory.get("version_id") or "")
        if version_id in accepted_version_ids:
            continue
        comparison = comparisons.get(version_id, {})
        rewrite = rewrites.get(version_id, {})
        source_article_id = str(memory.get("source_article_id") or comparison.get("source_article_id") or rewrite.get("source_article_id") or "")
        article = article_by_id(workbench_data, source_article_id)
        if not article:
            article = article_by_title(workbench_data, title_for_source_article(review_memory, source_article_id))
        accepted.append(
            {
                "version_id": version_id,
                "source_article_id": source_article_id,
                "source_action_id": memory.get("source_action_id") or comparison.get("source_action_id") or rewrite.get("source_action_id") or "",
                "version_type": memory.get("version_type") or comparison.get("version_type") or rewrite.get("version_type") or "rewrite",
                "human_score": memory.get("human_score"),
                "human_notes": memory.get("human_notes") or "",
                "decided_at": memory.get("updated_at") or memory.get("decided_at") or "",
                "score_delta": safe_float(memory.get("score_delta") or (comparison.get("scores") or {}).get("delta")),
                "new_title": rewrite.get("new_title") or comparison.get("new_title") or article.get("wechat_title") or article.get("title") or "",
                "new_body_markdown": rewrite.get("new_body_markdown") or article.get("wechat_body_markdown") or "",
            }
        )
        accepted_version_ids.add(version_id)
    selected = choose_best_accepted(accepted)
    promoted_versions = [
        {
            "promotion_id": promotion_id(run_date, str(item.get("version_id") or ""), str(item.get("source_article_id") or "")),
            "version_id": item.get("version_id") or "",
            "source_article_id": item.get("source_article_id") or "",
            "source_action_id": item.get("source_action_id") or "",
            "version_type": item.get("version_type") or "rewrite",
            "human_decision": "ACCEPT",
            "human_score": item.get("human_score"),
            "human_notes": item.get("human_notes") or "",
            "score_delta": item.get("score_delta") or 0,
            "new_title": item.get("new_title") or "",
            "new_body_markdown": item.get("new_body_markdown") or "",
            "promotion_status": "PROMOTED_TO_FINAL_CANDIDATE",
            "promotion_reason": "Human accepted this version; selected as the best accepted version for its source article.",
            "do_not_publish": True,
            "do_not_overwrite_original": True,
            "created_at": utc_now(),
        }
        for item in selected
    ]
    summary = {
        "accepted_version_count": len(accepted),
        "promoted_count": len(promoted_versions),
        "skipped_count": max(0, len(accepted) - len(promoted_versions)),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "promoted_versions": promoted_versions,
        "summary": summary,
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return (
        AcceptedVersionPromotionResult(
            run_date,
            summary["accepted_version_count"],
            summary["promoted_count"],
            summary["skipped_count"],
            repo_relative(outputs["latest_json"], repo_root),
        ),
        payload,
    )


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('promotion_id')}` | `{item.get('version_id')}` | `{item.get('human_score')}` | `{item.get('score_delta')}` | {item.get('new_title') or ''} |"
        for item in list_payload(payload, "promoted_versions")
    ) or "| - | - | - | 0 | No accepted versions to promote |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Promoted Versions

## Summary

- Run date: `{payload.get('run_date')}`
- Accepted versions: `{summary.get('accepted_version_count', 0)}`
- Promoted: `{summary.get('promoted_count', 0)}`
- Skipped: `{summary.get('skipped_count', 0)}`
- Policy: promotion is not publication and never overwrites original drafts.

| Promotion | Version | Human Score | Score Delta | Title |
|---|---|---:|---:|---|
{rows}
"""

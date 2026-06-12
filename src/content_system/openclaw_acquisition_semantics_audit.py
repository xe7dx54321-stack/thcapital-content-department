"""Audit OpenClaw cron jobs for acquisition playbook semantics."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from content_system.acquisition_playbook_common import SCHEMA_VERSION, basic_markdown, write_latest_report
from content_system.openclaw_source_inventory import OPENCLAW_JOBS_PATH, job_message, job_name, load_jobs, source_tokens
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, today_token, utc_now
from content_system.upstream_intelligence_common import compact_text, stable_id


ACQUISITION_AGENTS = {"signal-harvester", "market-scout", "knowledge-curator", "topic-planner", "content-analyst", "market-editor"}
BLOCKED_TERMS = ("草稿", "draft", "发布", "publish", "全文", "fulltext", "wechat deep")


def _cron(job: dict[str, Any]) -> str:
    schedule = job.get("schedule") if isinstance(job.get("schedule"), dict) else {}
    return str(schedule.get("expr") or schedule.get("cron") or job.get("cron") or "")


def _agent(job: dict[str, Any]) -> str:
    return str(job.get("agentId") or job.get("agent") or "unknown")


def infer_lane(text: str, source_ids: list[str]) -> str:
    haystack = f"{text} {' '.join(source_ids)}".lower()
    if "reddit" in haystack:
        return "reddit_llm_discussion"
    if any(token in haystack for token in ("yc", "techcrunch", "finsmes", "funding", "融资", "startup", "launches")):
        return "funding_startup"
    if any(token in haystack for token in ("product hunt", "trend hunt", "launch", "新产品")):
        return "product_launch"
    if any(token in haystack for token in ("openai", "anthropic", "deepmind", "google ai", "nvidia", "official", "官方")):
        return "official_ai_lab"
    if any(token in haystack for token in ("github", "huggingface", "open source", "开源")):
        return "open_source"
    if any(token in haystack for token in ("arxiv", "paper", "论文", "research")):
        return "paper_research"
    if any(token in haystack for token in ("latent", "interconnects", "simon", "batch", "newsletter", "builder", "学习池")):
        return "builder_research"
    if "wechat" in haystack or "微信" in haystack:
        return "wechat_metadata"
    if "youtube" in haystack:
        return "youtube_signal"
    if "x__" in haystack or "twitter" in haystack:
        return "x_signal"
    if any(token in haystack for token in ("hot", "trend", "热榜", "知乎", "百度", "bilibili")):
        return "trend_heat_validation"
    if any(token in haystack for token in ("keyword", "关键词", "discovery")):
        return "keyword_discovery"
    if any(token in haystack for token in ("candidate:", "semiconductor", "quantum", "policy", "trial", "垂直")):
        return "industry_deep_research"
    if "url" in haystack:
        return "manual_url_backfill"
    return "developer_community"


def infer_fetch_method(text: str, source_ids: list[str]) -> str:
    haystack = f"{text} {' '.join(source_ids)}".lower()
    if "rss" in haystack:
        return "rss"
    if "arxiv" in haystack:
        return "arxiv_query"
    if "github" in haystack:
        return "github_release"
    if "huggingface" in haystack:
        return "huggingface_feed"
    if "youtube" in haystack or "reddit" in haystack or "trend" in haystack:
        return "public_metadata"
    if "wechat" in haystack or "微信" in haystack:
        return "manual_only"
    if "url" in haystack:
        return "manual_url"
    return "public_metadata"


def infer_purpose(lane: str) -> str:
    return {
        "reddit_llm_discussion": "Detect repeated community discussion and early weak signals.",
        "funding_startup": "Detect AI startup, funding, launch, and investor movement metadata.",
        "product_launch": "Detect product launches and product-market adoption signals.",
        "official_ai_lab": "Capture first-party AI lab and official update metadata.",
        "open_source": "Capture GitHub/Hugging Face open-source release metadata.",
        "paper_research": "Capture paper and research metadata for evidence backfill.",
        "builder_research": "Capture builder newsletters and analysis for angles and supporting evidence.",
        "wechat_metadata": "Capture WeChat metadata only and route to manual confirmation.",
        "youtube_signal": "Capture video metadata as weak signal.",
        "x_signal": "Capture public X metadata only as weak signal.",
        "trend_heat_validation": "Validate heat around already observed topics.",
        "keyword_discovery": "Discover candidate query terms for operator approval.",
        "industry_deep_research": "Keep vertical trial lanes isolated from daily hot material pool.",
        "manual_url_backfill": "Route operator URL queues into backfill review.",
    }.get(lane, "Capture metadata for downstream triage.")


def infer_lookback(cron: str, lane: str) -> str:
    if lane in {"reddit_llm_discussion", "trend_heat_validation"}:
        return "8h"
    if lane in {"funding_startup", "product_launch", "china_ai_media", "youtube_signal", "x_signal"}:
        return "12h"
    if lane == "paper_research":
        return "48h"
    if lane == "industry_deep_research":
        return "72h"
    if "," in cron or "/" in cron:
        return "12-24h"
    return "24h"


def infer_fallback(lane: str) -> list[str]:
    if lane in {"reddit_llm_discussion", "youtube_signal", "x_signal", "trend_heat_validation"}:
        return ["second_source_required", "manual_review", "watch"]
    if lane in {"funding_startup", "product_launch", "global_ai_media"}:
        return ["company_official", "investor_official", "manual_url_backfill"]
    if lane == "wechat_metadata":
        return ["manual_review", "primary_source_search"]
    if lane == "paper_research":
        return ["author_page", "github_repo", "benchmark_reference"]
    return ["manual_url_backfill", "watch"]


def infer_downstream(lane: str) -> list[str]:
    if lane in {"reddit_llm_discussion", "youtube_signal", "x_signal", "trend_heat_validation"}:
        return ["weak_signal_pool", "confirmation_queue", "watch"]
    if lane == "wechat_metadata":
        return ["manual_review", "confirmation_queue"]
    if lane == "keyword_discovery":
        return ["manual_review", "watch"]
    if lane == "industry_deep_research":
        return ["industry_deep_research", "manual_review"]
    return ["normalized_upstream_items", "evidence_backfill", "topic_scoring"]


def migration_value(agent: str, lane: str, text: str) -> str:
    lower = text.lower()
    if any(term in lower for term in BLOCKED_TERMS):
        return "NONE"
    if agent in {"signal-harvester", "market-scout"} and lane not in {"developer_community"}:
        return "HIGH"
    if agent in ACQUISITION_AGENTS:
        return "MEDIUM"
    return "LOW"


def audit_job(job: dict[str, Any]) -> dict[str, Any]:
    name = job_name(job)
    message = job_message(job)
    text = f"{name}\n{message}"
    source_ids = source_tokens(text)
    lane = infer_lane(text, source_ids)
    agent = _agent(job)
    value = migration_value(agent, lane, text)
    confidence = "HIGH" if source_ids or lane != "developer_community" else "LOW"
    if not source_ids and agent not in ACQUISITION_AGENTS:
        confidence = "LOW"
    return {
        "job_id": str(job.get("id") or stable_id("openclaw_job", name, message[:120])),
        "agent": agent,
        "enabled": bool(job.get("enabled")),
        "cron": _cron(job),
        "source_ids": source_ids,
        "inferred_lane": lane,
        "inferred_purpose": infer_purpose(lane),
        "inferred_fetch_method": infer_fetch_method(text, source_ids),
        "inferred_cadence_reason": "Preserve early/midday/evening observation pattern when useful; compress duplicate jobs into lane batches.",
        "inferred_lookback": infer_lookback(_cron(job), lane),
        "inferred_fallback": infer_fallback(lane),
        "inferred_downstream": infer_downstream(lane),
        "confidence": confidence,
        "migration_value": value,
    }


def fallback_jobs(paths: ProjectPaths) -> list[dict[str, Any]]:
    inventory = read_json(paths.logs_root / "latest_openclaw_source_inventory.json")
    jobs = inventory.get("jobs") if isinstance(inventory.get("jobs"), list) else []
    output = []
    for item in jobs:
        if not isinstance(item, dict):
            continue
        output.append(
            {
                "id": item.get("job_id"),
                "enabled": item.get("enabled"),
                "agentId": item.get("agent"),
                "cron": item.get("cron"),
                "message": f"{item.get('description', '')} {' '.join(item.get('source_ids') or [])}",
            }
        )
    return output


def build_openclaw_acquisition_semantics_audit(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    jobs, warnings = load_jobs(OPENCLAW_JOBS_PATH)
    if not jobs:
        jobs = fallback_jobs(paths)
        warnings.append("Used Phase29 inventory fallback for acquisition semantics audit.")
    audited = [audit_job(job) for job in jobs if _agent(job) in ACQUISITION_AGENTS or source_tokens(f"{job_name(job)} {job_message(job)}")]
    summary = {
        "acquisition_job_count": len(audited),
        "high_value_playbook_jobs": sum(1 for item in audited if item["migration_value"] == "HIGH"),
        "medium_value_playbook_jobs": sum(1 for item in audited if item["migration_value"] == "MEDIUM"),
        "low_value_playbook_jobs": sum(1 for item in audited if item["migration_value"] == "LOW"),
        "do_not_migrate_jobs": sum(1 for item in audited if item["migration_value"] == "NONE"),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": today_token(),
        "jobs": audited,
        "summary": summary,
        "warnings": warnings,
        "policy": {"read_only_openclaw": True, "no_cron_migration": True, "no_full_text": True},
    }
    rows = [
        {
            "agent": item["agent"],
            "lane": item["inferred_lane"],
            "method": item["inferred_fetch_method"],
            "value": item["migration_value"],
            "job": compact_text(item["job_id"], 38),
        }
        for item in audited[:40]
    ]
    markdown = basic_markdown("OpenClaw Acquisition Semantics Audit", summary, rows, ("agent", "lane", "method", "value", "job"))
    outputs = write_latest_report(paths, repo_root, "openclaw_acquisition_semantics_audit", payload, markdown)
    return payload, outputs

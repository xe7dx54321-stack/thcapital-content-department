"""Import a read-only OpenClaw source inventory for Phase 29."""

from __future__ import annotations

import json
import plistlib
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table, stable_id


OPENCLAW_JOBS_PATH = Path("/Users/apple/.openclaw/cron/jobs.json")
OPENCLAW_GATEWAY_PLIST = Path("/Users/apple/Library/LaunchAgents/ai.openclaw.gateway.plist")
SOURCE_TOKEN_RE = re.compile(r"\b(?:web|wechat|trend|x|youtube)__[A-Za-z0-9_-]+|candidate:[A-Za-z0-9_:-]+")


FALLBACK_SOURCES: tuple[dict[str, str], ...] = (
    {"source_id": "trend__reddit_localllama_daily", "source_name": "Reddit LocalLLaMA", "source_type": "reddit", "lane_hint": "reddit_llm_discussion"},
    {"source_id": "trend__reddit_claude_daily", "source_name": "Reddit Claude", "source_type": "reddit", "lane_hint": "reddit_llm_discussion"},
    {"source_id": "trend__reddit_chatgpt_daily", "source_name": "Reddit ChatGPT", "source_type": "reddit", "lane_hint": "reddit_llm_discussion"},
    {"source_id": "trend__yc_launches_ai", "source_name": "YC Launches AI", "source_type": "yc", "lane_hint": "funding_startup"},
    {"source_id": "web__techcrunch_ai", "source_name": "TechCrunch AI", "source_type": "media", "lane_hint": "funding_startup"},
    {"source_id": "web__finsmes_ai_gnews", "source_name": "FinSMEs AI", "source_type": "media", "lane_hint": "funding_startup"},
    {"source_id": "trend__trend_hunt_ai_agents", "source_name": "Product Hunt / Trend Hunt AI Agents", "source_type": "trend_heat", "lane_hint": "trend_heat"},
    {"source_id": "web__deeplearning_ai_batch", "source_name": "DeepLearning.AI The Batch", "source_type": "newsletter", "lane_hint": "builder_research"},
    {"source_id": "web__latent_space", "source_name": "Latent Space", "source_type": "newsletter", "lane_hint": "builder_research"},
    {"source_id": "web__interconnects", "source_name": "Interconnects", "source_type": "newsletter", "lane_hint": "builder_research"},
    {"source_id": "web__simon_willison", "source_name": "Simon Willison", "source_type": "newsletter", "lane_hint": "builder_research"},
    {"source_id": "web__understanding_ai", "source_name": "Understanding AI", "source_type": "newsletter", "lane_hint": "builder_research"},
    {"source_id": "web__infoq_ai_ml", "source_name": "InfoQ AI / ML", "source_type": "media", "lane_hint": "builder_research"},
    {"source_id": "wechat__36kr", "source_name": "36Kr AI", "source_type": "wechat", "lane_hint": "wechat_metadata"},
    {"source_id": "wechat__geekpark", "source_name": "GeekPark", "source_type": "wechat", "lane_hint": "wechat_metadata"},
    {"source_id": "wechat__guixingren_pro", "source_name": "硅星人", "source_type": "wechat", "lane_hint": "wechat_metadata"},
    {"source_id": "youtube__openai", "source_name": "OpenAI YouTube", "source_type": "youtube", "lane_hint": "youtube_signal"},
    {"source_id": "youtube__ycombinator", "source_name": "Y Combinator YouTube", "source_type": "youtube", "lane_hint": "youtube_signal"},
    {"source_id": "youtube__googledeepmind", "source_name": "Google DeepMind YouTube", "source_type": "youtube", "lane_hint": "youtube_signal"},
    {"source_id": "x__openai", "source_name": "OpenAI X", "source_type": "x", "lane_hint": "x_signal"},
    {"source_id": "x__openai_developers", "source_name": "OpenAI Developers X", "source_type": "x", "lane_hint": "x_signal"},
    {"source_id": "x__anthropic", "source_name": "Anthropic X", "source_type": "x", "lane_hint": "x_signal"},
    {"source_id": "trend__baidu_realtime_ai", "source_name": "Baidu Realtime AI", "source_type": "trend_heat", "lane_hint": "trend_heat"},
    {"source_id": "trend__zhihu_hot_ai", "source_name": "Zhihu Hot AI", "source_type": "trend_heat", "lane_hint": "trend_heat"},
)


BLOCKED_CAPABILITY_SOURCES: tuple[dict[str, str], ...] = (
    {
        "source_id": "openclaw_capability__wechat_fulltext_deep_capture",
        "source_name": "OpenClaw WeChat full-text deep capture",
        "source_type": "unknown",
        "lane_hint": "wechat_metadata",
    },
    {
        "source_id": "openclaw_capability__wechat_draftbox_publish_flow",
        "source_name": "OpenClaw WeChat draftbox / publishing flow",
        "source_type": "unknown",
        "lane_hint": "wechat_metadata",
    },
)


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__openclaw-source-inventory.json",
        "dated_md": paths.logs_root / f"{run_date}__openclaw-source-inventory.md",
        "latest_json": paths.logs_root / "latest_openclaw_source_inventory.json",
        "latest_md": paths.logs_root / "latest_openclaw_source_inventory.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__openclaw-source-inventory-board.md",
        "board_latest_md": paths.frontstage_root / "latest_openclaw_source_inventory_board.md",
    }


def load_jobs(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    if not path.exists():
        return [], [f"Missing OpenClaw jobs file: {path}"]
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive local file parsing
        return [], [f"Failed to parse OpenClaw jobs file: {exc}"]
    jobs = raw.get("jobs") if isinstance(raw, dict) else raw
    if not isinstance(jobs, list):
        warnings.append("OpenClaw jobs payload did not contain a jobs list.")
        return [], warnings
    return [job for job in jobs if isinstance(job, dict)], warnings


def gateway_detected(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        payload = plistlib.loads(path.read_bytes())
    except Exception:
        text = path.read_text(encoding="utf-8", errors="ignore")
        return "openclaw" in text.lower() and "gateway" in text.lower()
    args = payload.get("ProgramArguments") if isinstance(payload, dict) else []
    return "openclaw" in " ".join(str(item) for item in args).lower() and "gateway" in " ".join(str(item) for item in args).lower()


def job_message(job: dict[str, Any]) -> str:
    payload = job.get("payload") if isinstance(job.get("payload"), dict) else {}
    return str(payload.get("message") or job.get("message") or "")


def job_name(job: dict[str, Any]) -> str:
    return str(job.get("name") or job.get("title") or job.get("id") or "")


def source_tokens(text: str) -> list[str]:
    return sorted(set(SOURCE_TOKEN_RE.findall(text)))


def source_prefix(source_id: str) -> str:
    if source_id.startswith("candidate:"):
        return "candidate"
    if "__" in source_id:
        return source_id.split("__", 1)[0]
    return source_id.split("_", 1)[0]


def infer_lane(text: str) -> str:
    haystack = text.lower()
    if "reddit" in haystack:
        return "reddit_llm_discussion"
    if any(token in haystack for token in ("finsmes", "financing", "funding", "融资", "yc", "launches", "techcrunch")):
        return "funding_startup"
    if any(token in haystack for token in ("openai", "anthropic", "deepmind", "google ai", "nvidia", "official")):
        return "official_ai"
    if any(token in haystack for token in ("newsletter", "latent", "interconnects", "simon", "batch", "builder", "研究扩散")):
        return "builder_research"
    if "wechat" in haystack or "微信" in haystack:
        return "wechat_metadata"
    if "youtube" in haystack:
        return "youtube_signal"
    if "x__" in haystack or " twitter" in haystack:
        return "x_signal"
    if any(token in haystack for token in ("trend", "hot", "热榜", "bilibili", "zhihu", "baidu")):
        return "trend_heat"
    if any(token in haystack for token in ("candidate:", "semiconductor", "photonics", "quantum", "policy", "careers", "trial")):
        return "industry_deep_research"
    return "unknown"


def infer_source_type(source_id: str, source_name: str) -> str:
    haystack = f"{source_id} {source_name}".lower()
    if "reddit" in haystack:
        return "reddit"
    if "yc" in haystack or "ycombinator" in haystack:
        return "yc"
    if any(token in haystack for token in ("techcrunch", "finsmes", "infoq", "36kr", "36氪", "media")):
        return "media"
    if any(token in haystack for token in ("batch", "latent", "interconnects", "newsletter", "simon", "understanding_ai")):
        return "newsletter"
    if source_id.startswith("wechat__"):
        return "wechat"
    if source_id.startswith("youtube__"):
        return "youtube"
    if source_id.startswith("x__"):
        return "x"
    if source_id.startswith("trend__"):
        return "trend_heat"
    if source_id.startswith("candidate:"):
        return "industry_trial"
    return "unknown"


def display_name(source_id: str) -> str:
    if source_id.startswith("candidate:"):
        raw = source_id.split(":", 1)[1]
    elif "__" in source_id:
        raw = source_id.split("__", 1)[1]
    else:
        raw = source_id
    return raw.replace("_", " ").replace("-", " ").title()


def job_record(job: dict[str, Any]) -> dict[str, Any]:
    name = job_name(job)
    message = job_message(job)
    tokens = source_tokens(f"{name}\n{message}")
    schedule = job.get("schedule") if isinstance(job.get("schedule"), dict) else {}
    text = f"{name} {message} {' '.join(tokens)}"
    return {
        "job_id": stable_id("openclaw_job", job.get("id") or name, message[:120]),
        "enabled": bool(job.get("enabled")),
        "agent": job.get("agentId") or job.get("agent") or "unknown",
        "cron": schedule.get("expr") or schedule.get("cron") or job.get("cron") or "",
        "source_ids": tokens,
        "lane_hint": infer_lane(text),
        "description": compact_text(name or message, 180),
    }


def add_blocked_capabilities(source_map: dict[str, dict[str, Any]], jobs: list[dict[str, Any]]) -> None:
    haystack = "\n".join(f"{job_name(job)} {job_message(job)}" for job in jobs).lower()
    if "全文深抓" in haystack or "deep" in haystack and "wechat" in haystack:
        source_map.setdefault("openclaw_capability__wechat_fulltext_deep_capture", dict(BLOCKED_CAPABILITY_SOURCES[0]))
    if any(token in haystack for token in ("草稿", "draft", "发布", "publish", "结果回流")):
        source_map.setdefault("openclaw_capability__wechat_draftbox_publish_flow", dict(BLOCKED_CAPABILITY_SOURCES[1]))


def build_sources(jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_jobs: dict[str, list[str]] = defaultdict(list)
    source_enabled: Counter[str] = Counter()
    for job in jobs:
        record = job_record(job)
        for token in record["source_ids"]:
            source_jobs[token].append(record["job_id"])
            if record["enabled"]:
                source_enabled[token] += 1
    source_map: dict[str, dict[str, Any]] = {}
    for token, detected_jobs in source_jobs.items():
        source_map[token] = {
            "source_id": token,
            "source_name": display_name(token),
            "source_prefix": source_prefix(token),
            "source_type": infer_source_type(token, token),
            "lane_hint": infer_lane(token),
            "detected_from_jobs": detected_jobs,
            "enabled_job_count": source_enabled[token],
        }
    for fallback in FALLBACK_SOURCES:
        source_id = fallback["source_id"]
        source_map.setdefault(
            source_id,
            {
                "source_id": source_id,
                "source_name": fallback["source_name"],
                "source_prefix": source_prefix(source_id),
                "source_type": fallback["source_type"],
                "lane_hint": fallback["lane_hint"],
                "detected_from_jobs": [],
                "enabled_job_count": 0,
            },
        )
    add_blocked_capabilities(source_map, jobs)
    for source_id, source in source_map.items():
        source.setdefault("source_prefix", source_prefix(source_id))
        source.setdefault("source_type", infer_source_type(source_id, source.get("source_name", "")))
        source.setdefault("lane_hint", infer_lane(f"{source_id} {source.get('source_name', '')}"))
        source.setdefault("detected_from_jobs", [])
        source.setdefault("enabled_job_count", 0)
    return sorted(source_map.values(), key=lambda item: (item.get("source_prefix", ""), item.get("source_id", "")))


def build_openclaw_source_inventory(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    jobs_raw, warnings = load_jobs(OPENCLAW_JOBS_PATH)
    jobs = [job_record(job) for job in jobs_raw]
    sources = build_sources(jobs_raw)
    prefix_counts = Counter(str(source.get("source_prefix") or "") for source in sources)
    summary = {
        "job_count": len(jobs),
        "enabled_job_count": sum(1 for job in jobs if job.get("enabled")),
        "source_count": len(sources),
        "web": prefix_counts.get("web", 0),
        "wechat": prefix_counts.get("wechat", 0),
        "trend": prefix_counts.get("trend", 0),
        "candidate": prefix_counts.get("candidate", 0),
        "x": prefix_counts.get("x", 0),
        "youtube": prefix_counts.get("youtube", 0),
    }
    if not jobs_raw:
        warnings.append("Using fallback source skeleton from user OpenClaw recap.")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "openclaw_available": OPENCLAW_JOBS_PATH.exists(),
        "gateway_detected": gateway_detected(OPENCLAW_GATEWAY_PLIST),
        "jobs": jobs,
        "sources": sources,
        "summary": summary,
        "warnings": warnings,
        "policy": {
            "read_only_inventory": True,
            "does_not_start_gateway": True,
            "does_not_migrate_cron": True,
            "does_not_fetch_full_text": True,
        },
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        {
            "type": item.get("source_type"),
            "lane": item.get("lane_hint"),
            "enabled": item.get("enabled_job_count"),
            "source": compact_text(item.get("source_name"), 56),
        }
        for item in payload.get("sources", [])[:40]
    ]
    warnings = "\n".join(f"- {item}" for item in payload.get("warnings", [])) or "- None."
    return f"""# OpenClaw Source Inventory

## Summary

- openclaw_available: `{payload.get('openclaw_available')}`
- gateway_detected: `{payload.get('gateway_detected')}`
- job_count: `{summary.get('job_count', 0)}`
- enabled_job_count: `{summary.get('enabled_job_count', 0)}`
- source_count: `{summary.get('source_count', 0)}`
- web/wechat/trend/candidate/x/youtube: `{summary.get('web', 0)}` / `{summary.get('wechat', 0)}` / `{summary.get('trend', 0)}` / `{summary.get('candidate', 0)}` / `{summary.get('x', 0)}` / `{summary.get('youtube', 0)}`

## Sources

{markdown_table(rows, ('type', 'lane', 'enabled', 'source'))}

## Warnings

{warnings}

## Boundary

This report reads OpenClaw files only. It does not start the gateway, migrate cron jobs, fetch full text, publish, or mutate the current project config.
"""

"""Shared helpers for Phase 26 upstream intelligence reports."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from content_system.phase7_report_utils import safe_float, safe_int


LANES: tuple[dict[str, str], ...] = (
    {"lane_id": "official_ai_lab", "label": "Official AI Lab"},
    {"lane_id": "model_release", "label": "Model Release"},
    {"lane_id": "agent_framework", "label": "Agent Framework"},
    {"lane_id": "open_source", "label": "Open Source"},
    {"lane_id": "paper_research", "label": "Paper Research"},
    {"lane_id": "ai_infra", "label": "AI Infra"},
    {"lane_id": "funding_startup", "label": "Funding / Startup"},
    {"lane_id": "developer_community", "label": "Developer Community"},
    {"lane_id": "china_ai_media", "label": "China AI Media"},
    {"lane_id": "global_ai_media", "label": "Global AI Media"},
    {"lane_id": "social_weak_signal", "label": "Social Weak Signal"},
)


P0_SOURCE_CANDIDATES: tuple[dict[str, Any], ...] = (
    {
        "source_name": "OpenAI News",
        "source_type": "official_blog",
        "category": "official_ai_lab",
        "priority": "P0",
        "reason": "Tier-A model, product, and agent platform updates.",
        "suggested_fetch_method": "rss",
        "requires_api_key": False,
        "estimated_reliability": "HIGH",
    },
    {
        "source_name": "Anthropic News",
        "source_type": "official_blog",
        "category": "official_ai_lab",
        "priority": "P0",
        "reason": "Tier-A frontier model and enterprise product updates.",
        "suggested_fetch_method": "html_index",
        "requires_api_key": False,
        "estimated_reliability": "HIGH",
    },
    {
        "source_name": "Google DeepMind Blog",
        "source_type": "official_blog",
        "category": "official_ai_lab",
        "priority": "P0",
        "reason": "Research, model, and product signals from a core AI lab.",
        "suggested_fetch_method": "rss",
        "requires_api_key": False,
        "estimated_reliability": "HIGH",
    },
    {
        "source_name": "Google AI Blog",
        "source_type": "official_blog",
        "category": "official_ai_lab",
        "priority": "P0",
        "reason": "Google product AI and platform updates.",
        "suggested_fetch_method": "html_index",
        "requires_api_key": False,
        "estimated_reliability": "HIGH",
    },
    {
        "source_name": "Meta AI Blog",
        "source_type": "official_blog",
        "category": "official_ai_lab",
        "priority": "P0",
        "reason": "Open model, agent, and research announcements.",
        "suggested_fetch_method": "html_index",
        "requires_api_key": False,
        "estimated_reliability": "HIGH",
    },
    {
        "source_name": "Microsoft AI Blog",
        "source_type": "official_blog",
        "category": "official_ai_lab",
        "priority": "P0",
        "reason": "Copilot, Azure AI, agent platform, and enterprise adoption updates.",
        "suggested_fetch_method": "rss",
        "requires_api_key": False,
        "estimated_reliability": "HIGH",
    },
    {
        "source_name": "NVIDIA AI Blog",
        "source_type": "official_blog",
        "category": "ai_infra",
        "priority": "P0",
        "reason": "AI infra, GPU, edge AI, agent deployment, and ecosystem updates.",
        "suggested_fetch_method": "rss",
        "requires_api_key": False,
        "estimated_reliability": "HIGH",
    },
    {
        "source_name": "Hugging Face Blog",
        "source_type": "huggingface",
        "category": "open_source",
        "priority": "P0",
        "reason": "Open-source model and developer ecosystem signals.",
        "suggested_fetch_method": "rss",
        "requires_api_key": False,
        "estimated_reliability": "HIGH",
    },
    {
        "source_name": "Hugging Face Papers",
        "source_type": "huggingface",
        "category": "paper",
        "priority": "P0",
        "reason": "Fast research trend discovery with developer attention proxy.",
        "suggested_fetch_method": "html_index",
        "requires_api_key": False,
        "estimated_reliability": "MEDIUM",
    },
    {
        "source_name": "LangChain Releases",
        "source_type": "github",
        "category": "agent_framework",
        "priority": "P0",
        "reason": "Agent framework releases reveal developer workflow changes.",
        "suggested_fetch_method": "github_release",
        "requires_api_key": False,
        "estimated_reliability": "HIGH",
    },
    {
        "source_name": "LlamaIndex Releases",
        "source_type": "github",
        "category": "agent_framework",
        "priority": "P0",
        "reason": "RAG and agent infrastructure release signals.",
        "suggested_fetch_method": "github_release",
        "requires_api_key": False,
        "estimated_reliability": "HIGH",
    },
    {
        "source_name": "AutoGen Releases",
        "source_type": "github",
        "category": "agent_framework",
        "priority": "P0",
        "reason": "Multi-agent framework signal from Microsoft ecosystem.",
        "suggested_fetch_method": "github_release",
        "requires_api_key": False,
        "estimated_reliability": "HIGH",
    },
    {
        "source_name": "CrewAI Releases",
        "source_type": "github",
        "category": "agent_framework",
        "priority": "P0",
        "reason": "Agent workflow tooling and startup ecosystem signal.",
        "suggested_fetch_method": "github_release",
        "requires_api_key": False,
        "estimated_reliability": "MEDIUM",
    },
    {
        "source_name": "arXiv AI / LLM / Agent queries",
        "source_type": "arxiv",
        "category": "paper",
        "priority": "P0",
        "reason": "Research frontier signal before media coverage.",
        "suggested_fetch_method": "search_query",
        "requires_api_key": False,
        "estimated_reliability": "MEDIUM",
    },
    {
        "source_name": "GitHub Trending AI / Agent",
        "source_type": "github",
        "category": "open_source",
        "priority": "P0",
        "reason": "Open-source momentum and developer adoption signal.",
        "suggested_fetch_method": "html_index",
        "requires_api_key": False,
        "estimated_reliability": "MEDIUM",
    },
)


P1_SOURCE_CANDIDATES: tuple[dict[str, Any], ...] = (
    {
        "source_name": "Product Hunt AI",
        "source_type": "community",
        "category": "developer_community",
        "priority": "P1",
        "reason": "Product launch and early adoption signal.",
        "suggested_fetch_method": "manual_url",
        "requires_api_key": False,
        "estimated_reliability": "MEDIUM",
    },
    {
        "source_name": "Hacker News AI",
        "source_type": "community",
        "category": "developer_community",
        "priority": "P1",
        "reason": "Developer attention and controversy signal.",
        "suggested_fetch_method": "search_query",
        "requires_api_key": False,
        "estimated_reliability": "MEDIUM",
    },
    {
        "source_name": "Papers with Code",
        "source_type": "papers",
        "category": "paper",
        "priority": "P1",
        "reason": "Benchmark and code-linked research signal.",
        "suggested_fetch_method": "html_index",
        "requires_api_key": False,
        "estimated_reliability": "MEDIUM",
    },
    {
        "source_name": "VentureBeat AI",
        "source_type": "media",
        "category": "global_media",
        "priority": "P1",
        "reason": "Global enterprise AI news and funding context.",
        "suggested_fetch_method": "rss",
        "requires_api_key": False,
        "estimated_reliability": "MEDIUM",
    },
    {
        "source_name": "The Decoder",
        "source_type": "media",
        "category": "global_media",
        "priority": "P1",
        "reason": "Focused AI product and model coverage.",
        "suggested_fetch_method": "rss",
        "requires_api_key": False,
        "estimated_reliability": "MEDIUM",
    },
    {
        "source_name": "SemiAnalysis public snippets",
        "source_type": "newsletter",
        "category": "ai_infra",
        "priority": "P1",
        "reason": "High-signal AI infra and semiconductor context when public.",
        "suggested_fetch_method": "manual_url",
        "requires_api_key": False,
        "estimated_reliability": "MEDIUM",
    },
    {
        "source_name": "The Information AI headlines",
        "source_type": "newsletter",
        "category": "global_media",
        "priority": "P1",
        "reason": "Business-side AI signal; only public headlines are suitable.",
        "suggested_fetch_method": "manual_url",
        "requires_api_key": False,
        "estimated_reliability": "LOW",
        "risk": ["paywall_or_login"],
    },
    {
        "source_name": "JiQiZhiXin AI",
        "source_type": "media",
        "category": "china_media",
        "priority": "P1",
        "reason": "Chinese AI research and industry coverage.",
        "suggested_fetch_method": "rss",
        "requires_api_key": False,
        "estimated_reliability": "MEDIUM",
    },
    {
        "source_name": "QbitAI",
        "source_type": "media",
        "category": "china_media",
        "priority": "P1",
        "reason": "Chinese AI media and product signal.",
        "suggested_fetch_method": "rss",
        "requires_api_key": False,
        "estimated_reliability": "MEDIUM",
    },
    {
        "source_name": "36Kr AI",
        "source_type": "media",
        "category": "china_media",
        "priority": "P1",
        "reason": "China startup and funding signal.",
        "suggested_fetch_method": "search_query",
        "requires_api_key": False,
        "estimated_reliability": "MEDIUM",
    },
)


def stable_id(prefix: str, *parts: Any) -> str:
    raw = "|".join(str(part) for part in parts if part is not None)
    return f"{prefix}_{hashlib.sha1(raw.encode('utf-8')).hexdigest()[:12]}"


def compact_text(value: Any, limit: int = 160) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "..."


def list_dicts(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def source_items_from_manifest(payload: dict[str, Any]) -> list[dict[str, Any]]:
    items = list_dicts(payload.get("sources"))
    if items:
        return items
    items = list_dicts(payload.get("records"))
    return items


def detect_lane(text: Any, source_id: Any = "") -> str:
    haystack = f"{text or ''} {source_id or ''}".lower()
    if any(token in haystack for token in ("openai", "anthropic", "deepmind", "google ai", "meta ai", "microsoft ai")):
        return "official_ai_lab"
    if any(token in haystack for token in ("gpt", "claude", "gemini", "llama", "model", "frontier")):
        return "model_release"
    if any(token in haystack for token in ("agent", "langchain", "llamaindex", "autogen", "crewai", "mcp")):
        return "agent_framework"
    if any(token in haystack for token in ("github", "open source", "repo", "hugging face", "huggingface")):
        return "open_source"
    if any(token in haystack for token in ("arxiv", "paper", "research", "benchmark", "papers with code")):
        return "paper_research"
    if any(token in haystack for token in ("nvidia", "gpu", "compute", "infra", "chip", "semiconductor", "光", "算力")):
        return "ai_infra"
    if any(token in haystack for token in ("funding", "startup", "series ", "venture", "融资")):
        return "funding_startup"
    if any(token in haystack for token in ("hacker news", "product hunt", "developer", "community")):
        return "developer_community"
    if any(token in haystack for token in ("机器之心", "量子位", "新智元", "智东西", "36kr", "36氪")):
        return "china_ai_media"
    if any(token in haystack for token in ("venturebeat", "decoder", "information", "media")):
        return "global_ai_media"
    if any(token in haystack for token in ("reddit", "x.com", "twitter", "social")):
        return "social_weak_signal"
    return "official_ai_lab" if "official" in haystack else "global_ai_media"


def detect_event_type(text: Any) -> str:
    haystack = str(text or "").lower()
    if any(token in haystack for token in ("release", "launch", "available", "announces", "model", "gpt", "claude", "gemini")):
        return "model_release"
    if "agent" in haystack or "workflow" in haystack:
        return "product_update"
    if any(token in haystack for token in ("paper", "arxiv", "benchmark", "research")):
        return "paper"
    if any(token in haystack for token in ("github", "open source", "repo", "hugging face")):
        return "open_source"
    if any(token in haystack for token in ("funding", "raises", "series", "融资")):
        return "funding"
    if any(token in haystack for token in ("nvidia", "gpu", "chip", "infra", "compute")):
        return "benchmark"
    return "unknown"


def freshness_from_run_date(run_date: Any, current_date: str) -> str:
    value = str(run_date or "").replace("-", "")[:8]
    if value == current_date:
        return "today"
    if value and value[:6] == current_date[:6]:
        return "this_week"
    return "unknown" if not value else "stale"


def normalize_summary(payload: dict[str, Any], key: str = "summary") -> dict[str, Any]:
    raw = payload.get(key)
    return raw if isinstance(raw, dict) else {}


def quality_score(hotness: Any, potential: Any, evidence_strength: str, freshness: str) -> int:
    score = int((safe_float(hotness) * 0.5) + (safe_float(potential) * 0.35))
    if evidence_strength == "HIGH":
        score += 12
    elif evidence_strength == "MEDIUM":
        score += 8
    elif evidence_strength == "LOW":
        score += 3
    if freshness == "today":
        score += 8
    elif freshness == "this_week":
        score += 4
    return max(0, min(100, score))


def markdown_table(rows: list[dict[str, Any]], columns: tuple[str, ...]) -> str:
    if not rows:
        return "_None._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in columns) + " |")
    return "\n".join([header, divider, *body])

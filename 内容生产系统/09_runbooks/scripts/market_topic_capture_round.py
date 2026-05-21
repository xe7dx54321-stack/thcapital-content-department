#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import difflib
import json
import re
import ssl
import subprocess
import sys
import tempfile
import textwrap
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, urlencode, urlparse
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

import yaml

from market_wechat_source_defs import WECHAT_SOURCE_TARGETS


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
PACKET_DIR = ROOT / "02_topic_radar" / "source_packets"
RAW_DIR = PACKET_DIR / "raw"
LOG_DIR = ROOT / "10_logs"
STATE_DIR = LOG_DIR / "runtime_state"
STATE_PATH = STATE_DIR / "market_topic_capture_state.json"
WEMP_BASE_URL = "http://localhost:8001"
WEMP_API_BASE = f"{WEMP_BASE_URL}/api/v1"
WEMP_LOGIN_URL = f"{WEMP_API_BASE}/wx/auth/login"
WEMP_MPS_URL = f"{WEMP_API_BASE}/wx/mps"

CN_TZ = ZoneInfo("Asia/Shanghai")
SSL_CONTEXT = ssl._create_unverified_context()
USER_AGENT = "Mozilla/5.0 THCapital/1.0"
ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}
WEMP_TOKEN_CACHE: str | None = None
WEMP_SUBSCRIPTIONS_CACHE: list[dict[str, Any]] | None = None
RAPIDOCR_ENGINE: Any | None = None


@dataclass(frozen=True)
class SourceConfig:
    source_id: str
    source_name: str
    source_url: str
    kind: str
    packet_prefix: str
    source_type: str = "trend_entrance"
    platform: str = "web"
    language: str = "en"
    region: str = "global"
    signal_quality: str = "medium"
    default_limit: int = 4
    metadata: dict[str, Any] = field(default_factory=dict)


SOURCE_CONFIGS: dict[str, SourceConfig] = {
    "trend__reddit_localllama_daily": SourceConfig(
        source_id="trend__reddit_localllama_daily",
        source_name="Reddit / LocalLLaMA Daily Top",
        source_url="https://old.reddit.com/r/LocalLLaMA/top/.rss?t=day",
        kind="reddit_rss",
        packet_prefix="reddit_localllama",
        source_type="community_discussion",
        signal_quality="medium",
        default_limit=4,
        metadata={
            "subreddit": "LocalLLaMA",
            "time": "day",
            "capture_method": "old.reddit rss / atom",
            "caveat": "官方 Reddit JSON 与 comments API 当前被 403 挡住；本轮切到 old.reddit RSS 作为稳定入口，但 score / comment_count 不再保证可见。",
        },
    ),
    "trend__reddit_claude_daily": SourceConfig(
        source_id="trend__reddit_claude_daily",
        source_name="Reddit / ClaudeAI Daily Top",
        source_url="https://old.reddit.com/r/ClaudeAI/top/.rss?t=day",
        kind="reddit_rss",
        packet_prefix="reddit_claude",
        source_type="community_discussion",
        signal_quality="medium",
        default_limit=4,
        metadata={
            "subreddit": "ClaudeAI",
            "time": "day",
            "capture_method": "old.reddit rss / atom",
            "caveat": "官方 Reddit JSON 与 comments API 当前被 403 挡住；本轮切到 old.reddit RSS 作为稳定入口，但 score / comment_count 不再保证可见。",
        },
    ),
    "trend__reddit_chatgpt_daily": SourceConfig(
        source_id="trend__reddit_chatgpt_daily",
        source_name="Reddit / ChatGPT Daily Top",
        source_url="https://old.reddit.com/r/ChatGPT/top/.rss?t=day",
        kind="reddit_rss",
        packet_prefix="reddit_chatgpt",
        source_type="community_discussion",
        signal_quality="medium",
        default_limit=3,
        metadata={
            "subreddit": "ChatGPT",
            "time": "day",
            "capture_method": "old.reddit rss / atom",
            "caveat": "官方 Reddit JSON 与 comments API 当前被 403 挡住；本轮切到 old.reddit RSS 作为稳定入口，但 score / comment_count 不再保证可见。",
        },
    ),
    "trend__trend_hunt_ai": SourceConfig(
        source_id="trend__trend_hunt_ai",
        source_name="Trend Hunt / Product Hunt Mirror / AI",
        source_url="https://trend-hunt.com/api/search?q=ai&locale=en&limit=10",
        kind="trend_hunt",
        packet_prefix="trend_hunt_ai",
        source_type="product_discovery_mirror",
        signal_quality="medium",
        default_limit=6,
        metadata={"query": "ai", "locale": "en"},
    ),
    "trend__trend_hunt_ai_agents": SourceConfig(
        source_id="trend__trend_hunt_ai_agents",
        source_name="Trend Hunt / Product Hunt Mirror / AI Agents",
        source_url="https://trend-hunt.com/api/search?q=ai+agents&locale=en&limit=10",
        kind="trend_hunt",
        packet_prefix="trend_hunt_ai_agents",
        source_type="product_discovery_mirror",
        signal_quality="medium",
        default_limit=6,
        metadata={"query": "ai agents", "locale": "en"},
    ),
    "trend__trend_hunt_automation": SourceConfig(
        source_id="trend__trend_hunt_automation",
        source_name="Trend Hunt / Product Hunt Mirror / Automation",
        source_url="https://trend-hunt.com/api/search?q=automation&locale=en&limit=10",
        kind="trend_hunt",
        packet_prefix="trend_hunt_automation",
        source_type="product_discovery_mirror",
        signal_quality="medium",
        default_limit=6,
        metadata={"query": "automation", "locale": "en", "category": "Productivity"},
    ),
    "trend__yc_launches_ai": SourceConfig(
        source_id="trend__yc_launches_ai",
        source_name="YC Launches / AI-Relevant",
        source_url="https://www.ycombinator.com/launches.json",
        kind="yc_launches_json",
        packet_prefix="yc_launches",
        source_type="official_listing",
        signal_quality="high",
        default_limit=6,
        metadata={
            "include_keywords": [
                "ai",
                "artificial intelligence",
                "agent",
                "agents",
                "llm",
                "language model",
                "robot",
                "robotics",
                "automation",
                "autonomous",
                "voice ai",
                "developer tools",
                "coding",
                "inference",
                "search",
                "video",
                "data layer",
            ],
        },
    ),
    "web__openai_news": SourceConfig(
        source_id="web__openai_news",
        source_name="OpenAI News",
        source_url="https://openai.com/news",
        kind="rss_feed",
        packet_prefix="openai_news",
        source_type="official_update",
        signal_quality="high",
        default_limit=6,
        metadata={
            "feed_url": "https://openai.com/news/rss.xml",
            "content_type": "official article",
            "capture_method": "official rss",
            "primary_source": "yes",
            "verification_status": "primary-source",
            "citation_reliability": "high",
            "why_source_matters": "OpenAI News 是模型、产品、API 与组织动作的官方一手口径。",
            "follow_up_hints": [
                "优先判断这次更新是不是能力边界、产品入口或商业模式变化",
                "继续回链单篇原文、产品页、帮助文档和开发者文档",
                "如果只是组织公告，也要判断对 agent 生态是否有结构性影响",
            ],
            "topic_tags": ["openai", "official-update", "model-platform"],
            "summary": "OpenAI News RSS 抓到新条目。它属于官方一手源，适合判断模型、产品、API 和平台战略的真实变化。",
            "heat_hint": "official update",
        },
    ),
    "web__google_blog_ai": SourceConfig(
        source_id="web__google_blog_ai",
        source_name="Google AI Blog",
        source_url="https://blog.google/innovation-and-ai/technology/ai/",
        kind="rss_feed",
        packet_prefix="google_blog_ai",
        source_type="official_update",
        signal_quality="high",
        default_limit=6,
        metadata={
            "feed_url": "https://blog.google/technology/ai/rss/",
            "content_type": "official article",
            "capture_method": "official rss",
            "primary_source": "yes",
            "verification_status": "primary-source",
            "citation_reliability": "high",
            "why_source_matters": "Google AI Blog 是 Gemini、Search、Workspace、Infra 与 AI 产品化动作的重要官方入口。",
            "follow_up_hints": [
                "优先判断是模型层更新、产品集成还是生态分发动作",
                "继续补单篇原文、Google 官方产品页和开发者文档",
                "若事件足够大，再去看中文媒体和社区是否已经跟进",
            ],
            "topic_tags": ["google", "official-update", "ai-platform"],
            "summary": "Google AI Blog RSS 抓到新条目。它属于官方一手源，适合判断 Google AI 平台层和产品层的真实变化。",
            "heat_hint": "official update",
        },
    ),
    "web__xai_news": SourceConfig(
        source_id="web__xai_news",
        source_name="xAI News",
        source_url="https://x.ai/news",
        kind="jina_markdown_snapshot",
        packet_prefix="xai_news",
        source_type="official_update",
        signal_quality="high",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://x.ai/news",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "snapshot_ignore_patterns": [r"^what's new$", r"^latest news$", r"^read$"],
            "link_domain_allowlist": ["x.ai"],
            "primary_source": "yes",
            "verification_status": "primary-source-snapshot",
            "citation_reliability": "high",
            "why_source_matters": "xAI News 是 Grok、API、组织动作与模型发布的一手官方入口。",
            "follow_up_hints": [
                "优先回链单篇 xAI 新闻页、API 文档和产品页",
                "判断是模型能力、产品入口还是组织并购动作",
                "如涉及重大更新，再去看 X、媒体和社区扩散",
            ],
            "topic_tags": ["xai", "official-update", "model-platform"],
            "heat_hint": "official update snapshot",
        },
    ),
    "web__nvidia_blog": SourceConfig(
        source_id="web__nvidia_blog",
        source_name="NVIDIA Blog",
        source_url="https://blogs.nvidia.com/",
        kind="jina_markdown_snapshot",
        packet_prefix="nvidia_blog",
        source_type="official_update",
        signal_quality="high",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://blogs.nvidia.com/",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "snapshot_ignore_patterns": [r"^featured$", r"^recent news$", r"^view all recent news$"],
            "link_domain_allowlist": ["blogs.nvidia.com"],
            "primary_source": "yes",
            "verification_status": "primary-source-snapshot",
            "citation_reliability": "high",
            "why_source_matters": "NVIDIA Blog 是 AI infra、agentic AI、机器人和数据中心变化的重要官方入口。",
            "follow_up_hints": [
                "优先回链单篇官方博客、产品页和 GTC 发布资料",
                "区分模型 infra、推理成本、机器人和行业解决方案",
            ],
            "topic_tags": ["nvidia", "official-update", "infra-hardware"],
            "heat_hint": "official update snapshot",
        },
    ),
    "web__anthropic_news": SourceConfig(
        source_id="web__anthropic_news",
        source_name="Anthropic News",
        source_url="https://www.anthropic.com/news",
        kind="jina_markdown_snapshot",
        packet_prefix="anthropic_newsroom",
        source_type="official_update",
        signal_quality="high",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.anthropic.com/news",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "snapshot_ignore_patterns": [
                r"^Newsroom Anthropic$",
                r"^Skip to main content.*",
                r"^Press inquires.*",
                r"^Non media inquiries.*",
                r"^Media assets.*",
                r"^Date Category Title$",
            ],
            "link_domain_allowlist": ["anthropic.com"],
            "primary_source": "yes",
            "verification_status": "primary-source-snapshot",
            "citation_reliability": "high",
            "why_source_matters": "Anthropic Newsroom 是 Claude、agents、computer use 与组织动作的重要官方一手入口。",
            "follow_up_hints": [
                "优先回链单篇官方新闻页和相关产品页",
                "判断是模型能力变化、组织动作还是生态分发动作",
                "如涉及重大模型更新，再去看多平台扩散情况",
            ],
            "topic_tags": ["anthropic", "official-update", "newsroom"],
            "heat_hint": "official update snapshot",
        },
    ),
    "web__deepmind_blog": SourceConfig(
        source_id="web__deepmind_blog",
        source_name="Google DeepMind Blog",
        source_url="https://deepmind.google/discover/blog/",
        kind="jina_markdown_snapshot",
        packet_prefix="deepmind_blog",
        source_type="official_update",
        signal_quality="high",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://deepmind.google/discover/blog/",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "link_domain_allowlist": ["deepmind.google"],
            "primary_source": "yes",
            "verification_status": "primary-source-snapshot",
            "citation_reliability": "high",
            "why_source_matters": "DeepMind Blog 能补模型、机器人和研究转产品的官方一手变化。",
            "follow_up_hints": [
                "优先判断是否和模型、robotics、world model、agent infra 有关",
                "继续回链单篇博客、论文页和 demo",
            ],
            "topic_tags": ["deepmind", "official-update", "research-product"],
            "heat_hint": "official update snapshot",
        },
    ),
    "web__simon_willison": SourceConfig(
        source_id="web__simon_willison",
        source_name="Simon Willison",
        source_url="https://simonwillison.net/",
        kind="jina_markdown_snapshot",
        packet_prefix="simon_willison",
        source_type="expert_site",
        signal_quality="high",
        default_limit=3,
        metadata={
            "capture_url": "https://r.jina.ai/http://simonwillison.net/",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "snapshot_prefer_line_entries": True,
            "link_domain_allowlist": ["simonwillison.net"],
            "section_anchor": "March",
            "snapshot_ignore_patterns": [
                r"^Simon Willison’s Weblog$",
                r"^Sponsored by:.*$",
                r"^On generative-ai .*",
                r"^EntriesLinksQuotesNotesGuidesElsewhere$",
            ],
            "snapshot_exclude_patterns": [
                r"^[Ii]['’]m\b.*$",
                r"^owners can edit.*$",
                r"^The file picker UI is now available.*$",
                r"^New from datasette files import .*",
                r"^\d{1,2}:\d{2}\s*[ap]m / .*",
            ],
            "primary_source": "partial",
            "verification_status": "expert-signal-snapshot",
            "citation_reliability": "medium",
            "why_source_matters": "Simon Willison 长期提供 LLM、agent、工具链和真实工程经验的高质量观察。",
            "follow_up_hints": [
                "优先回链原博客文章、repo 和 demo",
                "把它当观点 / 工程观察源，不要直接当最终事实源",
            ],
            "topic_tags": ["simon-willison", "expert-view", "agentic-coding"],
            "heat_hint": "expert viewpoint snapshot",
        },
    ),
    "web__latent_space": SourceConfig(
        source_id="web__latent_space",
        source_name="Latent Space",
        source_url="https://www.latent.space/",
        kind="jina_markdown_snapshot",
        packet_prefix="latent_space",
        source_type="expert_media_site",
        signal_quality="high",
        default_limit=3,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.latent.space/",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "link_domain_allowlist": ["latent.space"],
            "primary_source": "partial",
            "verification_status": "expert-media-snapshot",
            "citation_reliability": "medium",
            "why_source_matters": "Latent Space 擅长 builder、agent infra、workflow 与 AI 工程话题拆解。",
            "follow_up_hints": [
                "优先保留高密度方法论、访谈对象和关键链接",
                "继续回链播客、访谈对象主页和产品页",
            ],
            "topic_tags": ["latent-space", "builder-view", "agent-infra"],
            "heat_hint": "expert media snapshot",
        },
    ),
    "web__one_useful_thing": SourceConfig(
        source_id="web__one_useful_thing",
        source_name="One Useful Thing",
        source_url="https://www.oneusefulthing.org/",
        kind="jina_markdown_snapshot",
        packet_prefix="one_useful_thing",
        source_type="expert_site",
        signal_quality="high",
        default_limit=3,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.oneusefulthing.org/",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "link_domain_allowlist": ["oneusefulthing.org"],
            "primary_source": "partial",
            "verification_status": "expert-signal-snapshot",
            "citation_reliability": "medium",
            "why_source_matters": "One Useful Thing 适合补 AI 使用范式、用户行为和认知框架视角。",
            "follow_up_hints": [
                "优先提炼强框架、强问题意识和用户层洞察",
                "如要正式引用，回链原文与相关研究材料",
            ],
            "topic_tags": ["one-useful-thing", "ai-usage", "expert-view"],
            "heat_hint": "expert viewpoint snapshot",
        },
    ),
    "web__interconnects": SourceConfig(
        source_id="web__interconnects",
        source_name="Interconnects",
        source_url="https://www.interconnects.ai/",
        kind="jina_markdown_snapshot",
        packet_prefix="interconnects",
        source_type="expert_media_site",
        signal_quality="high",
        default_limit=3,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.interconnects.ai/",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "link_domain_allowlist": ["interconnects.ai"],
            "primary_source": "partial",
            "verification_status": "expert-media-snapshot",
            "citation_reliability": "medium",
            "why_source_matters": "Interconnects 对模型、硬件、推理与产业交界的解释力较强。",
            "follow_up_hints": [
                "优先保留结构性判断和产业链解释",
                "继续回链原文、论文和公司公告",
            ],
            "topic_tags": ["interconnects", "infra-view", "industry-analysis"],
            "heat_hint": "expert media snapshot",
        },
    ),
    "web__understanding_ai": SourceConfig(
        source_id="web__understanding_ai",
        source_name="Understanding AI",
        source_url="https://www.understandingai.org/",
        kind="jina_markdown_snapshot",
        packet_prefix="understanding_ai",
        source_type="expert_media_site",
        signal_quality="medium",
        default_limit=3,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.understandingai.org/",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "link_domain_allowlist": ["understandingai.org"],
            "snapshot_ignore_patterns": [
                r"^Understanding AI$",
                r"^Exploring how AI works and how it'?s changing our world\.$",
                r"^Over [\d,]+ subscribers$",
                r"^By subscribing, you agree.*$",
                r"^(Home|Podcast|Archive|About|Recommendations)$",
            ],
            "primary_source": "partial",
            "verification_status": "expert-media-snapshot",
            "citation_reliability": "medium",
            "why_source_matters": "Understanding AI 擅长把前沿 AI 议题做成相对易懂的解释型内容。",
            "follow_up_hints": [
                "优先提炼适合大众转译的解释框架",
                "继续回链原文与所引用的一手材料",
            ],
            "topic_tags": ["understanding-ai", "explainers", "ai-education"],
            "heat_hint": "expert media snapshot",
        },
    ),
    "web__deeplearningai_batch": SourceConfig(
        source_id="web__deeplearningai_batch",
        source_name="DeepLearning.AI The Batch",
        source_url="https://www.deeplearning.ai/the-batch/",
        kind="jina_markdown_snapshot",
        packet_prefix="deeplearningai_batch",
        source_type="expert_media_site",
        signal_quality="high",
        default_limit=3,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.deeplearning.ai/the-batch/",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "link_domain_allowlist": ["deeplearning.ai"],
            "snapshot_ignore_patterns": [
                r"^What Matters in AI Right Now$",
                r"^🗞️?\s*Stay updated with weekly AI News and Insights delivered to your inbox$",
                r"^Subscribe to The Batch$",
                r"^The Batch AI News and Insights:.*$",
                r"^About$",
            ],
            "primary_source": "partial",
            "verification_status": "expert-media-snapshot",
            "citation_reliability": "medium",
            "why_source_matters": "The Batch 适合快速回看 AI 大事件与周级整理。",
            "follow_up_hints": [
                "把它当事件归纳层，继续回链官方源和单篇深文",
            ],
            "topic_tags": ["deeplearning-ai", "the-batch", "weekly-roundup"],
            "heat_hint": "expert media snapshot",
        },
    ),
    "web__infoq_ai_ml": SourceConfig(
        source_id="web__infoq_ai_ml",
        source_name="InfoQ AI/ML",
        source_url="https://www.infoq.com/ai-ml-data-eng/",
        kind="jina_markdown_snapshot",
        packet_prefix="infoq_ai_ml",
        source_type="expert_media_site",
        signal_quality="medium",
        default_limit=3,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.infoq.com/ai-ml-data-eng/",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "link_domain_allowlist": ["infoq.com"],
            "primary_source": "partial",
            "verification_status": "expert-media-snapshot",
            "citation_reliability": "medium",
            "why_source_matters": "InfoQ AI/ML 更偏工程落地、架构实践和系统性经验。",
            "follow_up_hints": [
                "优先提炼工程实践、架构经验和企业落地案例",
                "继续回链原始项目页和技术文档",
            ],
            "topic_tags": ["infoq", "engineering-practice", "ai-ml"],
            "heat_hint": "expert media snapshot",
        },
    ),
    "web__semianalysis": SourceConfig(
        source_id="web__semianalysis",
        source_name="SemiAnalysis",
        source_url="https://www.semianalysis.com/",
        kind="jina_markdown_snapshot",
        packet_prefix="semianalysis",
        source_type="expert_media_site",
        signal_quality="high",
        default_limit=3,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.semianalysis.com/",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "link_domain_allowlist": ["semianalysis.com"],
            "primary_source": "partial",
            "verification_status": "expert-media-snapshot",
            "citation_reliability": "medium",
            "why_source_matters": "SemiAnalysis 对模型训练、推理、数据中心和 AI 硬件有强解释力。",
            "follow_up_hints": [
                "优先保留结构性产业判断和硬件 / infra 解释",
                "继续回链原始公司公告和数据来源",
            ],
            "topic_tags": ["semianalysis", "infra", "hardware"],
            "heat_hint": "expert media snapshot",
        },
    ),
    "web__huggingface_blog": SourceConfig(
        source_id="web__huggingface_blog",
        source_name="Hugging Face Blog",
        source_url="https://huggingface.co/blog",
        kind="hf_blog_repo",
        packet_prefix="huggingface_blog",
        source_type="official_update",
        signal_quality="high",
        default_limit=3,
        metadata={
            "capture_url": "https://api.github.com/repos/huggingface/blog/contents/_blog.yml?ref=main",
            "repo_owner": "huggingface",
            "repo_name": "blog",
            "repo_ref": "main",
            "primary_source": "yes",
            "verification_status": "primary-source-repo",
            "citation_reliability": "high",
            "why_source_matters": "Hugging Face Blog 是开源模型、工具、生态变化的重要官方入口。",
            "follow_up_hints": [
                "继续回链单篇博客、repo、模型页和 docs",
            ],
            "topic_tags": ["huggingface", "official-update", "open-source"],
            "heat_hint": "official update repo",
        },
    ),
    "web__itjuzi": SourceConfig(
        source_id="web__itjuzi",
        source_name="IT 桔子 / 中国人工智能融资报告",
        source_url="https://cdn.itjuzi.com/pdf/1a5ee188cfde75809136ad47f4077d3a.pdf",
        kind="jina_markdown_snapshot",
        packet_prefix="itjuzi_ai_report",
        source_type="cn_financing_database_report",
        platform="web",
        language="zh",
        region="cn",
        signal_quality="high",
        default_limit=1,
        metadata={
            "capture_url": "https://r.jina.ai/http://cdn.itjuzi.com/pdf/1a5ee188cfde75809136ad47f4077d3a.pdf",
            "page_title_override": "IT 桔子｜2024 中国人工智能行业融资报告",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": False,
            "snapshot_line_limit": 14,
            "snapshot_min_chars": 20,
            "content_type": "official financing report pdf",
            "primary_source": "yes",
            "verification_status": "official-report-snapshot",
            "citation_reliability": "high",
            "why_source_matters": "IT 桔子公开 AI 融资报告能稳定补国内融资规模、融资阶段、城市分布和细分赛道结构，是国内融资数据库线的公开兜底入口。",
            "follow_up_hints": [
                "优先保留融资规模、轮次结构、地域分布和子赛道分化结论",
                "继续回链具体公司页、融资公告、工商信息和媒体交叉验证",
                "注意这是公开报告层，不等于可实时查询的 live database",
            ],
            "topic_tags": ["itjuzi", "cn-financing", "ai-report"],
            "heat_hint": "official financing report",
        },
    ),
    "web__openclaw_docs": SourceConfig(
        source_id="web__openclaw_docs",
        source_name="OpenClaw / ClawHub Docs",
        source_url="https://docs.openclaw.ai/tools/clawhub",
        kind="jina_markdown_snapshot",
        packet_prefix="openclaw_docs",
        source_type="tool_builder_docs",
        signal_quality="high",
        default_limit=3,
        metadata={
            "capture_url": "https://r.jina.ai/http://docs.openclaw.ai/tools/clawhub",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "link_domain_allowlist": ["docs.openclaw.ai", "openclaw.ai"],
            "snapshot_ignore_patterns": [
                r"^OpenClaw home page$",
                r"^Search\.\.\.$",
                r"^Navigation$",
                r"^Skills$",
                r"^ClawHub$",
                r"^Get started.*$",
                r"^Install and Configure$",
                r"^Community Plugins$",
                r"^Plugin Bundles$",
                r"^Automation Overview$",
                r"^Automation Troubleshooting$",
                r"^BTW Side Questions$",
                r"^Tool loop detection$",
                r"^Agent coordination$",
            ],
            "snapshot_include_patterns": [
                r"\b(release|released|announc(?:e|ed|ement)|launch(?:ed)?|added|updated?|preview|beta|migration|breaking change|changelog|version|now available)\b",
            ],
            "snapshot_exclude_patterns": [
                r"^Download new skills$",
                r"^Update installed skills$",
                r"^Search for skills$",
                r"^Back up your skills.*$",
                r"^Install the ClawHub CLI$",
                r"^Quick start.*$",
                r"^How it works$",
                r"^What you can do$",
            ],
            "snapshot_disable_single_fallback": True,
            "primary_source": "yes",
            "verification_status": "primary-source-snapshot",
            "citation_reliability": "high",
            "why_source_matters": "OpenClaw / ClawHub 文档和 skill、tool、agent 主战场高度契合。",
            "follow_up_hints": [
                "优先保留新增能力、限制条件和工具变化",
                "继续回链具体文档页和 release 说明",
            ],
            "topic_tags": ["openclaw", "docs", "agent-tools"],
            "heat_hint": "tooling snapshot",
        },
    ),
    "web__sspai_ai": SourceConfig(
        source_id="web__sspai_ai",
        source_name="少数派 AI Tag",
        source_url="https://sspai.com/tag/AI",
        kind="jina_markdown_snapshot",
        packet_prefix="sspai_ai",
        source_type="cn_media_site",
        signal_quality="medium",
        default_limit=3,
        metadata={
            "capture_url": "https://r.jina.ai/http://sspai.com/tag/AI",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "link_domain_allowlist": ["sspai.com"],
            "primary_source": "partial",
            "verification_status": "cn-media-snapshot",
            "citation_reliability": "medium",
            "why_source_matters": "少数派 AI 标签页适合补中文应用型、体验型 AI 内容与用户语境。",
            "follow_up_hints": [
                "优先保留工具实测、真实体验和使用场景",
                "继续回链正文与相关产品页",
            ],
            "topic_tags": ["sspai", "cn-ai-media", "consumer-ai"],
            "heat_hint": "cn media snapshot",
        },
    ),
    "web__jiqizhixin_site": SourceConfig(
        source_id="web__jiqizhixin_site",
        source_name="机器之心官网",
        source_url="https://www.jiqizhixin.com/",
        kind="jina_markdown_snapshot",
        packet_prefix="jiqizhixin_site",
        source_type="cn_media_site",
        platform="web",
        language="zh",
        region="cn",
        signal_quality="high",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.jiqizhixin.com/",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "link_domain_allowlist": ["jiqizhixin.com"],
            "primary_source": "partial",
            "verification_status": "cn-media-snapshot",
            "citation_reliability": "medium",
            "why_source_matters": "机器之心官网适合补中文模型、研究、产品和产业化传播层。",
            "follow_up_hints": [
                "优先回链正文、相关产品页和一手研究材料",
                "把它当中文传播入口，不直接替代官方信源",
            ],
            "topic_tags": ["jiqizhixin", "cn-ai-media", "news-site"],
            "heat_hint": "cn media snapshot",
        },
    ),
    "web__qbitai_site": SourceConfig(
        source_id="web__qbitai_site",
        source_name="量子位官网",
        source_url="https://www.qbitai.com/",
        kind="jina_markdown_snapshot",
        packet_prefix="qbitai_site",
        source_type="cn_media_site",
        platform="web",
        language="zh",
        region="cn",
        signal_quality="high",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.qbitai.com/",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "link_domain_allowlist": ["qbitai.com"],
            "primary_source": "partial",
            "verification_status": "cn-media-snapshot",
            "citation_reliability": "medium",
            "why_source_matters": "量子位官网是中文 AI 热点、模型更新与 agent 传播的重要网站面入口。",
            "follow_up_hints": [
                "优先回链正文、项目页和原始事件",
                "适合补中文传播和话术变化，不代替官方事实链",
            ],
            "topic_tags": ["qbitai", "cn-ai-media", "news-site"],
            "heat_hint": "cn media snapshot",
        },
    ),
    "web__zhidx": SourceConfig(
        source_id="web__zhidx",
        source_name="智东西",
        source_url="https://zhidx.com/",
        kind="jina_markdown_snapshot",
        packet_prefix="zhidx_site",
        source_type="cn_media_site",
        platform="web",
        language="zh",
        region="cn",
        signal_quality="high",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://zhidx.com/",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "snapshot_ignore_patterns": [r"^扫码关注.*", r"^绑定手机号$", r"^获取验证码$", r"^确认绑定$", r"^欢迎来智东西$"],
            "link_domain_allowlist": ["zhidx.com"],
            "primary_source": "partial",
            "verification_status": "cn-media-snapshot",
            "citation_reliability": "medium",
            "why_source_matters": "智东西适合补具身、AI 硬件、产业化与大公司落地叙事。",
            "follow_up_hints": [
                "优先回链正文、相关公司页和一手活动资料",
                "把它当中文传播入口，不代替官方事实链",
            ],
            "topic_tags": ["zhidx", "cn-ai-media", "industry-site"],
            "heat_hint": "cn media snapshot",
        },
    ),
    "web__36kr_ai": SourceConfig(
        source_id="web__36kr_ai",
        source_name="36氪 AI",
        source_url="https://www.36kr.com/information/AI",
        kind="jina_markdown_snapshot",
        packet_prefix="36kr_ai",
        source_type="cn_media_site",
        platform="web",
        language="zh",
        region="cn",
        signal_quality="medium",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.36kr.com/information/AI",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "snapshot_ignore_patterns": [
                r"^36氪_让一部分人先看到未来$",
                r"^登录$",
                r"^搜索$",
                r"^我要入驻$",
                r"^寻求报道$",
                r"^媒体品牌$",
                r"^企业服务$",
                r"^政府服务$",
                r"^投资人服务$",
                r"^创业者服务$",
                r"^创投平台$",
                r"^AI测评网$",
            ],
            "link_domain_allowlist": ["36kr.com"],
            "primary_source": "partial",
            "verification_status": "cn-media-snapshot",
            "citation_reliability": "medium",
            "why_source_matters": "36氪 AI 页适合补创业、融资、产品化与商业化叙事。",
            "follow_up_hints": [
                "优先回链正文、公司官网和融资公告",
                "把它当商业化传播入口，不代替官方事实链",
            ],
            "topic_tags": ["36kr", "cn-ai-media", "commercialization"],
            "heat_hint": "cn media snapshot",
        },
    ),
    "web__ifanr_ai": SourceConfig(
        source_id="web__ifanr_ai",
        source_name="爱范儿 AIGC",
        source_url="https://www.ifanr.com/category/aigc",
        kind="jina_markdown_snapshot",
        packet_prefix="ifanr_aigc",
        source_type="cn_media_site",
        platform="web",
        language="zh",
        region="cn",
        signal_quality="medium",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.ifanr.com/category/aigc",
            "snapshot_mode": "generic",
            "snapshot_prefer_link_texts": True,
            "snapshot_ignore_patterns": [
                r"^AIGC \| 爱范儿$",
                r"^分类$",
                r"^热门搜索$",
                r"^为您查询到.*篇文章$",
                r"^媒体品牌.*",
                r"^关于我们.*",
                r"^粤ICP备.*",
                r"^版权所有.*",
            ],
            "link_domain_allowlist": ["ifanr.com"],
            "primary_source": "partial",
            "verification_status": "cn-media-snapshot",
            "citation_reliability": "medium",
            "why_source_matters": "爱范儿 AIGC 页适合补消费产品、AI 硬件和大众传播型叙事。",
            "follow_up_hints": [
                "优先回链正文、相关产品页和原始事件",
                "适合作为大众传播角度入口，不代替官方事实链",
            ],
            "topic_tags": ["ifanr", "cn-ai-media", "consumer-ai"],
            "heat_hint": "cn media snapshot",
        },
    ),
    "x__openai": SourceConfig(
        source_id="x__openai",
        source_name="OpenAI on X",
        source_url="https://x.com/OpenAI",
        kind="jina_markdown_snapshot",
        packet_prefix="x_openai",
        source_type="social_signal",
        platform="x",
        signal_quality="high",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://x.com/OpenAI",
            "snapshot_mode": "x_profile",
            "section_anchor": "posts",
            "snapshot_min_score": 0,
            "snapshot_ignore_patterns": [
                r"^Try new tools\..*credits in prizes\.?$",
                r"^Students: build something real in the Codex Creator Challenge.*$",
                r"^The more AI can do, the more we need to ask.*$",
                r"^More on our approach to the Model Spec:?$",
            ],
            "primary_source": "partial",
            "verification_status": "social-signal",
            "citation_reliability": "medium",
            "why_source_matters": "OpenAI 的 X 账号适合补官方社交快讯与传播语境，但事实仍需回链官网。",
            "follow_up_hints": [
                "事实类内容必须继续回链 OpenAI 官网或 docs",
                "观点类和 teaser 适合作为快信号层",
            ],
            "topic_tags": ["x", "openai", "social-signal"],
            "heat_hint": "social fast signal",
        },
    ),
    "x__openaidevs": SourceConfig(
        source_id="x__openaidevs",
        source_name="OpenAI Devs on X",
        source_url="https://x.com/OpenAIDevs",
        kind="jina_markdown_snapshot",
        packet_prefix="x_openaidevs",
        source_type="social_signal",
        platform="x",
        signal_quality="high",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://x.com/OpenAIDevs",
            "snapshot_mode": "x_profile",
            "section_anchor": "posts",
            "snapshot_min_score": 0,
            "snapshot_ignore_patterns": [
                r"^\d{2}:\d{2}\s+Introducing Codex.*$",
            ],
            "snapshot_include_patterns": [
                r"\b(codex|chatgpt|github|deep research|ide extension|vscode|vs code|xcode|terminal|iterm2|desktop|sdk|api|extension|repos?)\b",
            ],
            "primary_source": "partial",
            "verification_status": "social-signal",
            "citation_reliability": "medium",
            "why_source_matters": "OpenAI Devs 适合补 API、SDK、工具链与开发者更新快讯。",
            "follow_up_hints": [
                "优先回链 docs、SDK、API changelog",
            ],
            "topic_tags": ["x", "openai-devs", "dev-updates"],
            "heat_hint": "social fast signal",
        },
    ),
    "x__anthropic_ai": SourceConfig(
        source_id="x__anthropic_ai",
        source_name="Anthropic on X",
        source_url="https://x.com/AnthropicAI",
        kind="jina_markdown_snapshot",
        packet_prefix="x_anthropic",
        source_type="social_signal",
        platform="x",
        signal_quality="high",
        default_limit=3,
        metadata={
            "capture_url": "https://r.jina.ai/http://x.com/AnthropicAI",
            "snapshot_mode": "x_profile",
            "section_anchor": "posts",
            "primary_source": "partial",
            "verification_status": "social-signal",
            "citation_reliability": "medium",
            "why_source_matters": "Anthropic 的 X 账号适合补 Claude、MCP、政策与社交快讯。",
            "follow_up_hints": [
                "事实类内容继续回链 Anthropic 原站",
            ],
            "topic_tags": ["x", "anthropic", "social-signal"],
            "heat_hint": "social fast signal",
        },
    ),
    "x__karpathy": SourceConfig(
        source_id="x__karpathy",
        source_name="Andrej Karpathy on X",
        source_url="https://x.com/karpathy",
        kind="jina_markdown_snapshot",
        packet_prefix="x_karpathy",
        source_type="social_signal",
        platform="x",
        signal_quality="high",
        default_limit=3,
        metadata={
            "capture_url": "https://r.jina.ai/http://x.com/karpathy",
            "snapshot_mode": "x_profile",
            "section_anchor": "posts",
            "primary_source": "partial",
            "verification_status": "social-signal",
            "citation_reliability": "medium",
            "why_source_matters": "Karpathy 是方法论、产品判断和 AI 心智框架的重要观点源。",
            "follow_up_hints": [
                "把它当 framing / 观点线索源，不要单独承担事实证明",
            ],
            "topic_tags": ["x", "karpathy", "thought-leader"],
            "heat_hint": "expert viewpoint snapshot",
        },
    ),
    "x__swyx": SourceConfig(
        source_id="x__swyx",
        source_name="swyx on X",
        source_url="https://x.com/swyx",
        kind="jina_markdown_snapshot",
        packet_prefix="x_swyx",
        source_type="social_signal",
        platform="x",
        signal_quality="high",
        default_limit=3,
        metadata={
            "capture_url": "https://r.jina.ai/http://x.com/swyx",
            "snapshot_mode": "x_profile",
            "section_anchor": "posts",
            "primary_source": "partial",
            "verification_status": "social-signal",
            "citation_reliability": "medium",
            "why_source_matters": "swyx 对 agent infra、builder 社区与工具生态的桥梁作用很强。",
            "follow_up_hints": [
                "优先保留强观点、产品提及和外链对象",
            ],
            "topic_tags": ["x", "swyx", "agent-infra"],
            "heat_hint": "expert viewpoint snapshot",
        },
    ),
    "x__hwchase17": SourceConfig(
        source_id="x__hwchase17",
        source_name="Harrison Chase on X",
        source_url="https://x.com/hwchase17",
        kind="jina_markdown_snapshot",
        packet_prefix="x_hwchase17",
        source_type="social_signal",
        platform="x",
        signal_quality="high",
        default_limit=3,
        metadata={
            "capture_url": "https://r.jina.ai/http://x.com/hwchase17",
            "snapshot_mode": "x_profile",
            "section_anchor": "posts",
            "primary_source": "partial",
            "verification_status": "social-signal",
            "citation_reliability": "medium",
            "why_source_matters": "Harrison Chase 是 agent framework、开发者工作流和 builder 场景的重要线索源。",
            "follow_up_hints": [
                "优先回链 LangChain 官方文档、repo 和 demo",
            ],
            "topic_tags": ["x", "harrison-chase", "builder-workflow"],
            "heat_hint": "expert viewpoint snapshot",
        },
    ),
    "trend__hn_frontpage": SourceConfig(
        source_id="trend__hn_frontpage",
        source_name="Hacker News Frontpage",
        source_url="https://news.ycombinator.com/",
        kind="hn_frontpage_api",
        packet_prefix="hn_frontpage",
        source_type="trend_entrance",
        signal_quality="high",
        default_limit=6,
        metadata={
            "algolia_api_url": "https://hn.algolia.com/api/v1/search?tags=front_page",
            "firebase_topstories_url": "https://hacker-news.firebaseio.com/v0/topstories.json",
            "firebase_item_url_template": "https://hacker-news.firebaseio.com/v0/item/{item_id}.json",
            "firebase_scan_limit": 40,
            "include_keywords": [
                "ai",
                "agent",
                "agents",
                "llm",
                "model",
                "openai",
                "claude",
                "gemini",
                "deepseek",
                "copilot",
                "robot",
                "robotics",
                "coding agent",
                "computer use",
                "workflow",
                "automation",
                "benchmark",
                "reasoning",
            ],
            "content_type": "trend article",
            "capture_method": "hn algolia front_page api with firebase fallback",
            "primary_source": "partial",
            "verification_status": "trend-board-api",
            "citation_reliability": "medium",
            "why_source_matters": "HN 是 builder、开源、AI infra 与创业语境里最稳定的早期扩散层之一。",
            "follow_up_hints": [
                "优先判断是不是 agent / builder / workflow / infra 相关条目",
                "继续点回原文页、Show HN 项目页和评论区",
                "如果只是圈内自嗨，不要直接升级成正式选题",
            ],
            "topic_tags": ["hacker-news", "builder-signal", "trend-entrance"],
            "summary": "Hacker News RSS 抓到高热新条目。它适合作为 builder / startup / AI infra 话题的扩散入口，不是最终事实源。",
            "heat_hint": "builder breakout signal",
        },
    ),
    "trend__github_trending": SourceConfig(
        source_id="trend__github_trending",
        source_name="GitHub Trending",
        source_url="https://github.com/trending",
        kind="github_trending_jina",
        packet_prefix="github_trending",
        source_type="open_source_trend",
        signal_quality="high",
        default_limit=6,
        metadata={
            "capture_url": "https://r.jina.ai/http://github.com/trending",
            "include_keywords": [
                "ai",
                "agent",
                "agents",
                "llm",
                "model",
                "workflow",
                "automation",
                "reasoning",
                "mcp",
                "memory",
                "sandbox",
                "tool",
                "research",
                "robot",
                "computer use",
                "browser",
                "code",
                "voice",
                "video",
            ],
            "primary_source": "partial",
            "verification_status": "official-platform-listing",
            "citation_reliability": "medium",
            "why_source_matters": "GitHub Trending 最适合抓 agent、workflow、开发工具和开源 infra 的真实 traction。",
            "follow_up_hints": [
                "优先回链 README、demo、docs 和 release notes",
                "判断它是短期热榜项目，还是正在形成方法论 / 产品范式",
                "如果 repo 只是娱乐项目或纯模板，不升级成正式选题",
            ],
            "topic_tags": ["github-trending", "open-source", "builder-stack"],
            "heat_hint": "open-source traction",
        },
    ),
    "trend__huggingface_daily_papers": SourceConfig(
        source_id="trend__huggingface_daily_papers",
        source_name="Hugging Face Daily Papers / Takara Mirror",
        source_url="https://huggingface.co/papers",
        kind="hf_papers_takara_rss",
        packet_prefix="huggingface_daily_papers",
        source_type="research_trend",
        signal_quality="high",
        default_limit=6,
        metadata={
            "feed_url": "https://papers.takara.ai/api/feed?limit=5",
            "mirror_origin": "https://huggingface.co/papers",
            "capture_method": "takara rss mirror + arxiv id normalization",
            "primary_source": "no",
            "verification_status": "research-community-mirror",
            "citation_reliability": "medium",
            "why_source_matters": "HF Daily Papers 直连当前会被 reset / 451；Takara 的 daily papers feed 能稳定补研究扩散层，再回链 arXiv 原文。",
            "follow_up_hints": [
                "继续回链论文原文、项目页、数据集页和作者主页",
                "优先识别 agent、benchmark、computer use、robotics 和 multimodal 方向",
                "如果只是纯学术且离业务很远，只保留作背景材料",
            ],
            "topic_tags": ["huggingface", "daily-papers", "research-trend"],
            "heat_hint": "research diffusion",
            "caveat": "当前抓取来自 Takara 的社区镜像 feed，不是 Hugging Face 官方直连；正式研究仍需回链 arXiv / 项目页 / 作者主页。",
        },
    ),
    "trend__arxiv_cs_ai_recent": SourceConfig(
        source_id="trend__arxiv_cs_ai_recent",
        source_name="arXiv cs.AI recent",
        source_url="https://arxiv.org/list/cs.AI/recent",
        kind="rss_feed",
        packet_prefix="arxiv_cs_ai",
        source_type="research_feed",
        signal_quality="medium-high",
        default_limit=6,
        metadata={
            "feed_url": "https://export.arxiv.org/rss/cs.AI",
            "include_keywords": [
                "agent",
                "agents",
                "llm",
                "language model",
                "large language model",
                "robot",
                "robotics",
                "computer use",
                "gui",
                "browser",
                "world model",
                "video",
                "autonomous",
                "policy",
                "planning",
                "tool use",
                "coding agent",
                "code generation",
                "reasoning model",
                "embodied",
                "autonomous driving",
            ],
            "exclude_keywords": [
                "emotion recognition",
                "affective",
                "language of thought",
                "cognitive science",
                "ai ethics",
                "ethics",
                "pluralism",
                "multimodal emotion",
                "physical principles",
            ],
            "content_type": "research paper",
            "capture_method": "arxiv rss",
            "primary_source": "yes",
            "verification_status": "research-preprint",
            "citation_reliability": "high",
            "why_source_matters": "arXiv cs.AI 是方法创新和研究前沿的原始入口，能帮助补位 L2 研究扩散层。",
            "follow_up_hints": [
                "优先判断论文是否和 agent、computer use、robotics、workflow、multimodal 或推理有关",
                "继续回链 PDF、项目页、GitHub、作者主页和演示视频",
                "如果只是理论工作且与主战场距离较远，只保留为背景研究",
            ],
            "topic_tags": ["arxiv", "research-frontier", "cs-ai"],
            "summary": "arXiv cs.AI RSS 抓到最新论文条目。它是研究前沿的原始入口，适合作为方法和方向变化的早期信号层。",
            "heat_hint": "research frontier",
        },
    ),
    "trend__baidu_realtime": SourceConfig(
        source_id="trend__baidu_realtime",
        source_name="百度热搜",
        source_url="https://top.baidu.com/board?tab=realtime",
        kind="baidu_hot_jina",
        packet_prefix="baidu_realtime",
        source_type="heat_validation",
        platform="web",
        language="zh",
        region="cn",
        signal_quality="medium",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://top.baidu.com/board?tab=realtime",
            "include_keywords": [
                "ai",
                "人工智能",
                "智能体",
                "机器人",
                "机器狼",
                "大模型",
                "算力",
                "自动驾驶",
                "智驾",
                "openai",
                "deepseek",
                "豆包",
                "manus",
                "agent",
                "claude",
                "gemini",
                "chatgpt",
                "具身",
                "ai手机",
                "apple intelligence",
                "ai眼镜",
                "智能眼镜",
                "ai pc",
                "英伟达",
            ],
            "exclude_keywords": [
                "手机回收",
                "旧手机",
                "二手手机",
            ],
            "primary_source": "no",
            "verification_status": "heat-validation-signal",
            "citation_reliability": "low",
            "why_source_matters": "百度热搜适合判断 AI / agent / robotics 话题是否开始进入更大众的中文语境。",
            "follow_up_hints": [
                "优先判断话题是不是 AI 主战场或强相关相邻战场",
                "继续回链原始事件、官方源和多平台讨论",
                "热搜只能证明传播，不等于事实强度或商业价值",
            ],
            "topic_tags": ["baidu-hot", "heat-validation", "cn-breakout"],
            "heat_hint": "breakout validation",
        },
    ),
    "trend__zhihu_hotlist": SourceConfig(
        source_id="trend__zhihu_hotlist",
        source_name="知乎热榜",
        source_url="https://api.zhihu.com/topstory/hot-list?limit=20",
        kind="zhihu_hot_json",
        packet_prefix="zhihu_hot_ai",
        source_type="heat_validation",
        platform="zhihu",
        language="zh",
        region="cn",
        signal_quality="medium",
        default_limit=4,
        metadata={
            "include_keywords": [
                "ai",
                "人工智能",
                "智能体",
                "agent",
                "agents",
                "大模型",
                "模型",
                "openai",
                "chatgpt",
                "claude",
                "gemini",
                "deepseek",
                "sora",
                "manus",
                "机器人",
                "具身",
                "自动驾驶",
                "智驾",
                "ai眼镜",
                "智能眼镜",
                "ai手机",
                "ai硬件",
                "英伟达",
                "算力",
                "mcp",
            ],
            "exclude_keywords": [
                "盗版",
                "宿舍",
                "猝死",
                "足球",
                "酒店",
            ],
            "primary_source": "no",
            "verification_status": "heat-validation-signal",
            "citation_reliability": "low-medium",
            "why_source_matters": "知乎热榜适合验证 AI 话题是否已经进入问答讨论场域，并补用户视角的关注点、疑问和分歧。",
            "follow_up_hints": [
                "优先回链原始事件、官方源和对应产品页",
                "结合问题标题、摘要、回答数与热度文本判断是否值得展开",
                "知乎热榜体现的是讨论热度，不等于事实强度或商业价值",
            ],
            "topic_tags": ["zhihu-hot", "heat-validation", "cn-discussion"],
            "heat_hint": "qa breakout validation",
        },
    ),
    "trend__newrank_ai_media_rank": SourceConfig(
        source_id="trend__newrank_ai_media_rank",
        source_name="新榜 AI 新媒体影响力排行榜",
        source_url="https://www.newrank.cn/public/info/rank_detail.html?name=ai",
        kind="newrank_period_json",
        packet_prefix="newrank_ai_media_rank",
        source_type="heat_validation",
        platform="wechat",
        language="zh",
        region="cn",
        signal_quality="medium",
        default_limit=1,
        metadata={
            "api_url": "https://www.newrank.cn/xdnphb/weixinrank/period/searchByName",
            "rank_name": "ai",
            "primary_source": "no",
            "verification_status": "platform-ranking-signal",
            "citation_reliability": "low-medium",
            "why_source_matters": "新榜 AI 榜单可以补中文 AI 垂类账号势能、平台传播格局和竞品观察，不是日热点，但能提供月度平台验证层。",
            "follow_up_hints": [
                "把它当成平台秩序和账号势能观察层，不要当成日级热点判断",
                "优先结合 OCR 提取账号清单、微信深抓素材和内容复盘一起使用",
                "关键判断要继续回链公众号原文，不要只依赖榜单图片",
            ],
            "topic_tags": ["newrank", "ai-media-rank", "wechat-ecosystem"],
            "heat_hint": "platform benchmark validation",
        },
    ),
    "trend__feigua_bilibili": SourceConfig(
        source_id="trend__feigua_bilibili",
        source_name="飞瓜 B站科技热视频榜",
        source_url="https://bz.feigua.cn/ranking/DailyHotVideoV2/20260325/1/30.html",
        kind="feigua_bilibili_hot_html",
        packet_prefix="feigua_bilibili_hot_ai",
        source_type="heat_validation",
        platform="bilibili",
        language="zh",
        region="cn",
        signal_quality="medium",
        default_limit=4,
        metadata={
            "capture_url_template": "https://bz.feigua.cn/ranking/DailyHotVideoV2/{date}/1/30.html",
            "date_offset_days": 1,
            "include_keywords": [
                "ai",
                "人工智能",
                "智能体",
                "agent",
                "大模型",
                "模型",
                "openai",
                "chatgpt",
                "claude",
                "gemini",
                "deepseek",
                "sora",
                "manus",
                "机器人",
                "具身",
                "无人机",
                "自动驾驶",
                "智驾",
                "芯片",
                "英伟达",
                "眼镜",
                "ai眼镜",
                "智能眼镜",
                "ai手机",
                "ai硬件",
                "mcp",
                "langchain",
                "langgraph",
                "rag",
                "prompt",
            ],
            "exclude_keywords": [
                "搞笑",
                "躲猫猫",
                "影视杂谈",
                "音乐",
                "舞蹈",
                "鬼畜",
            ],
            "primary_source": "no",
            "verification_status": "video-ranking-signal",
            "citation_reliability": "low-medium",
            "why_source_matters": "飞瓜 B站热门视频榜能补中文视频场域的传播验证层，尤其适合看科技 / 数码 / AI 话题是否开始放大。",
            "follow_up_hints": [
                "优先用来验证传播，不要把榜单本身当最终事实",
                "继续回链原始事件、官方账号、产品页和视频评论",
                "如与 B 站官方热门 API 同时命中，可提高视频场域置信度",
            ],
            "topic_tags": ["feigua", "bilibili-hot-video", "cn-video"],
            "heat_hint": "video ranking validation",
        },
    ),
    "web__techcrunch_ai": SourceConfig(
        source_id="web__techcrunch_ai",
        source_name="TechCrunch AI",
        source_url="https://techcrunch.com/category/artificial-intelligence/feed/",
        kind="rss_feed",
        packet_prefix="techcrunch_ai",
        source_type="media_feed",
        signal_quality="medium-high",
        default_limit=6,
        metadata={
            "verification_status": "secondary-report",
            "primary_source": "no",
            "heat_hint": "media entrance",
        },
    ),
    "web__finsmes_ai_gnews": SourceConfig(
        source_id="web__finsmes_ai_gnews",
        source_name="FinSMEs AI Funding / Google News Fallback",
        source_url="https://news.google.com/rss/search?q=site:finsmes.com%20artificial%20intelligence%20funding&hl=en-US&gl=US&ceid=US:en",
        kind="rss_feed",
        packet_prefix="finsmes_ai_gnews",
        source_type="fallback_media_feed",
        signal_quality="low-medium",
        default_limit=6,
        metadata={
            "required_source": "FinSMEs",
            "include_title_patterns": [r"raises", r"funding", r"secures", r"closes", r"series [abc]", r"seed"],
            "exclude_title_patterns": [r"homepage", r"archives", r"category", r"tag archives"],
            "max_age_days": 120,
            "capture_method": "gnews-rss / site-filter fallback",
            "citation_reliability": "low",
            "why_source_matters": "FinSMEs 对融资事件和新公司快讯敏感；官方站点直连受阻时，可先用 Google News site-filter RSS 稳定拿回入口。",
            "caveat": "当前是 Google News site-filter fallback，不是 FinSMEs 官方直连；适合作为融资入口，不适合直接当最终事实证据。",
            "follow_up_hints": [
                "先把媒体快讯当入口，再继续补公司官网、融资公告、创始人账号与产品页",
                "若标题看起来像老归档页或泛页面，不进入正式 packet",
                "优先保留最近 90 天内、与 AI / agent / automation 相关的融资对象",
            ],
            "heat_hint": "financing entrance + blocked-source fallback",
            "topic_tags": ["finsmes", "gnews-fallback", "financing"],
            "verification_status": "fallback-entry",
        },
    ),
    "youtube__openai": SourceConfig(
        source_id="youtube__openai",
        source_name="OpenAI YouTube",
        source_url="https://www.youtube.com/@OpenAI/videos",
        kind="youtube_jina_channel",
        packet_prefix="youtube_openai",
        source_type="official_video_channel",
        platform="youtube",
        signal_quality="high",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.youtube.com/@OpenAI/videos",
            "primary_source": "yes",
            "verification_status": "official-video",
            "citation_reliability": "high",
            "why_source_matters": "官方发布会、demo、访谈和产品解释视频是一手素材，适合捕捉产品能力、定位和话术变化。",
            "follow_up_hints": [
                "优先回看视频里 demo、原始措辞和 feature boundary",
                "如话题升格，继续找官网博文、发布页与评论区反馈",
                "如果标题较大，务必核对视频正文与官方配套文档是否一致",
            ],
            "topic_tags": ["youtube", "official-video", "openai"],
        },
    ),
    "youtube__ycombinator": SourceConfig(
        source_id="youtube__ycombinator",
        source_name="Y Combinator YouTube",
        source_url="https://www.youtube.com/@YCombinator/videos",
        kind="youtube_jina_channel",
        packet_prefix="youtube_ycombinator",
        source_type="media_video_channel",
        platform="youtube",
        signal_quality="high",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.youtube.com/@YCombinator/videos",
            "primary_source": "partial",
            "verification_status": "channel-video",
            "citation_reliability": "medium-high",
            "why_source_matters": "YC 频道里的创始人访谈、产品 demo 与 build-in-public 内容适合发现业务思路和创业语境。",
            "follow_up_hints": [
                "先判断是 founder interview、product demo 还是行业观点",
                "继续回链公司官网、创始人账号、产品页和融资线",
                "如果只是泛访谈，不要直接升级成选题结论",
            ],
            "topic_tags": ["youtube", "founder-interview", "yc"],
        },
    ),
    "youtube__googledeepmind": SourceConfig(
        source_id="youtube__googledeepmind",
        source_name="Google DeepMind YouTube",
        source_url="https://www.youtube.com/@GoogleDeepMind/videos",
        kind="youtube_jina_channel",
        packet_prefix="youtube_googledeepmind",
        source_type="official_video_channel",
        platform="youtube",
        signal_quality="high",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.youtube.com/@GoogleDeepMind/videos",
            "primary_source": "yes",
            "verification_status": "official-video",
            "citation_reliability": "high",
            "why_source_matters": "DeepMind 视频覆盖模型、机器人、研究 demo 和产品化叙事，是重要一手视频源。",
            "follow_up_hints": [
                "优先核对视频中的研究对象、demo 条件和边界",
                "继续补官方博客、论文页、产品页与开发者文档",
            ],
            "topic_tags": ["youtube", "official-video", "deepmind"],
        },
    ),
    "youtube__aidotengineer": SourceConfig(
        source_id="youtube__aidotengineer",
        source_name="AI Engineer YouTube",
        source_url="https://www.youtube.com/@aiDotEngineer/videos",
        kind="youtube_jina_channel",
        packet_prefix="youtube_ai_dot_engineer",
        source_type="builder_video_channel",
        platform="youtube",
        signal_quality="high",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.youtube.com/@aiDotEngineer/videos",
            "primary_source": "partial",
            "verification_status": "channel-video",
            "citation_reliability": "medium",
            "why_source_matters": "Agent 实操、workflow、stack 教学密度高，适合抓 builder 社区的真实关心点。",
            "follow_up_hints": [
                "优先抠 workflow、stack、失败边界和工具组合",
                "如涉及具体产品，继续找 repo、docs 和社区讨论",
            ],
            "topic_tags": ["youtube", "builder-workflow", "agent"],
        },
    ),
    "youtube__latent_space_pod": SourceConfig(
        source_id="youtube__latent_space_pod",
        source_name="Latent Space Pod YouTube",
        source_url="https://www.youtube.com/@LatentSpacePod/videos",
        kind="youtube_jina_channel",
        packet_prefix="youtube_latent_space_pod",
        source_type="media_video_channel",
        platform="youtube",
        signal_quality="medium-high",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.youtube.com/@LatentSpacePod/videos",
            "primary_source": "partial",
            "verification_status": "channel-video",
            "citation_reliability": "medium",
            "why_source_matters": "长访谈和 builder 观点演化适合提炼高质量 discussion angle。",
            "follow_up_hints": [
                "优先保留强观点、强方法论和被反复强调的变量",
                "继续找访谈对象的原始产品页、个人账号和演讲资料",
            ],
            "topic_tags": ["youtube", "podcast", "builder-view"],
        },
    ),
    "youtube__langchain": SourceConfig(
        source_id="youtube__langchain",
        source_name="LangChain YouTube",
        source_url="https://www.youtube.com/@LangChain/videos",
        kind="youtube_jina_channel",
        packet_prefix="youtube_langchain",
        source_type="tool_builder_video_channel",
        platform="youtube",
        signal_quality="medium-high",
        default_limit=4,
        metadata={
            "capture_url": "https://r.jina.ai/http://www.youtube.com/@LangChain/videos",
            "primary_source": "partial",
            "verification_status": "tool-builder-video",
            "citation_reliability": "medium",
            "why_source_matters": "框架更新、agent builder 教学和案例演示适合补 workflow / skill / stack 线索。",
            "follow_up_hints": [
                "先判断是框架更新、教程还是客户 case",
                "继续补 docs、repo、release notes 和使用案例",
            ],
            "topic_tags": ["youtube", "langchain", "builder-workflow"],
        },
    ),
    "trend__bilibili_popular_all": SourceConfig(
        source_id="trend__bilibili_popular_all",
        source_name="Bilibili Popular All / AI-Relevant",
        source_url="https://api.bilibili.com/x/web-interface/popular?ps=30&pn=1",
        kind="bilibili_popular",
        packet_prefix="bilibili_popular_ai",
        source_type="video_ranking",
        platform="bilibili",
        language="zh",
        region="cn",
        signal_quality="medium",
        default_limit=6,
        metadata={
            "include_keywords": [
                "ai",
                "人工智能",
                "agent",
                "智能体",
                "大模型",
                "机器人",
                "具身",
                "数字人",
                "语音克隆",
                "声音克隆",
                "ai翻唱",
                "换脸",
                "视频生成",
                "图像生成",
                "音乐生成",
                "自动驾驶",
                "aigc",
                "openai",
                "claude",
                "gemini",
                "cursor",
                "manus",
                "workflow",
                "提示词",
                "sora",
                "midjourney",
                "runway",
                "luma",
                "suno",
                "可灵",
                "即梦",
                "豆包",
                "notebooklm",
            ],
            "why_source_matters": "B站热视频适合补中文大众语境里正在扩散的 AI 话题，包括工具、agent、AI 娱乐化应用和消费级玩法，但仍要避免纯泛娱乐噪音。",
            "follow_up_hints": [
                "优先保留 AI / agent / AI 娱乐化应用相关热视频，不做纯泛热视频搬运",
                "继续回链视频描述、评论区、作者主页和原始事件",
                "如只是娱乐化二创但缺少可讨论的原始事件、产品或方法论，不直接升级成正式选题",
            ],
            "topic_tags": ["bilibili", "video-ranking", "cn-video"],
        },
    ),
}

for target in WECHAT_SOURCE_TARGETS:
    source_id = str(target["source_id"])
    source_name = str(target["source_name"])
    packet_prefix = str(target["packet_prefix"])
    signal_quality = str(target["signal_quality"])
    citation_reliability = str(target["citation_reliability"])
    notes = str(target["notes"])
    SOURCE_CONFIGS[source_id] = SourceConfig(
        source_id=source_id,
        source_name=source_name,
        source_url=f"wechat://{source_name}",
        kind="wechat_feed",
        packet_prefix=packet_prefix,
        source_type="wechat_rss_feed",
        platform="wechat",
        language="zh",
        region="cn",
        signal_quality=signal_quality,
        default_limit=4,
        metadata={
            "mp_name": source_name,
            "aliases": [str(item) for item in target.get("aliases", [])],
            "include_keywords": [str(item) for item in target.get("include_keywords", []) if str(item).strip()],
            "exclude_keywords": [str(item) for item in target.get("exclude_keywords", []) if str(item).strip()],
            "capture_method": "wechat-rss / wemp",
            "content_type": "wechat article",
            "primary_source": "partial",
            "verification_status": "wechat-rss-entry",
            "citation_reliability": citation_reliability,
            "why_source_matters": f"{source_name} 是中文 AI / agent 语境里的高密度入口源。{notes}",
            "follow_up_hints": [
                "先判断是不是 AI / agent / workflow / builder 相关条目",
                "继续回链公众号正文、相关产品页、作者观点和跨平台讨论",
                "如果只是泛资讯或公关稿，不直接升级成最终选题",
            ],
            "topic_tags": ["wechat", "cn-ai-media", packet_prefix],
            "summary": f"{source_name} 微信 RSS 抓到新条目。它更适合作为中文热点、产品观察和玩法讨论的入口，不宜直接当最终事实结论。",
        },
    )


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_dt(dt: datetime | None) -> str:
    if dt is None:
        return "unknown"
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def fetch_text(url: str) -> str:
    if "r.jina.ai/" in url:
        return fetch_text_via_curl(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/plain, text/markdown;q=0.9, */*;q=0.8",
            },
            prefer_http1=False,
        )
    if "youtube.com/feeds/videos.xml" in url:
        return fetch_text_via_curl(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/xml,text/xml;q=0.9,*/*;q=0.8",
            },
        )
    if "youtube.com" in url:
        return fetch_text_via_curl(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )
    if "api.bilibili.com" in url:
        return fetch_text_via_curl(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Referer": "https://www.bilibili.com/",
                "Accept": "application/json,*/*;q=0.8",
            },
        )
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json,text/html,application/xml,text/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.reddit.com/",
    }
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=30, context=SSL_CONTEXT) as response:
            payload = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
        return payload.decode(charset, "replace")
    except Exception:
        return fetch_text_via_curl(url, headers=headers)


def fetch_text_via_curl(
    url: str,
    headers: dict[str, str] | None = None,
    *,
    prefer_http1: bool = True,
) -> str:
    def run_command(*, insecure: bool = False, force_http1: bool = False) -> str:
        command = ["curl", "-fsSL", "--max-time", "30", "--retry", "2", "--retry-delay", "1"]
        if force_http1:
            command.insert(1, "--http1.1")
        if insecure:
            command.append("-k")
        for key, value in (headers or {}).items():
            command.extend(["-H", f"{key}: {value}"])
        command.append(url)
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=40,
        )
        return result.stdout

    protocol_attempts = [True, False] if prefer_http1 else [False, True]
    last_error: subprocess.CalledProcessError | None = None
    for insecure in (False, True):
        for force_http1 in protocol_attempts:
            try:
                return run_command(insecure=insecure, force_http1=force_http1)
            except subprocess.CalledProcessError as exc:
                last_error = exc
                if exc.returncode != 35:
                    raise
    if last_error is not None:
        raise last_error
    raise RuntimeError(f"curl fetch failed without subprocess error for {url}")


def fetch_json_via_curl(url: str, headers: dict[str, str] | None = None) -> Any:
    return json.loads(fetch_text_via_curl(url, headers=headers))


def fetch_json(url: str) -> Any:
    return json.loads(fetch_text(url))


def fetch_form_json(url: str, data: dict[str, Any]) -> Any:
    encoded = urlencode({key: value for key, value in data.items()}).encode("utf-8")
    request = Request(
        url,
        data=encoded,
        headers={
            "User-Agent": USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json,text/plain,*/*",
            "Origin": "https://www.newrank.cn",
            "Referer": "https://www.newrank.cn/",
        },
        method="POST",
    )
    with urlopen(request, timeout=30, context=SSL_CONTEXT) as response:
        payload = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
    return json.loads(payload.decode(charset, "replace"))


def fetch_binary_via_curl(url: str, headers: dict[str, str] | None = None) -> bytes:
    command = ["curl", "-fsSL", "--max-time", "60", url]
    for key, value in (headers or {}).items():
        command.extend(["-H", f"{key}: {value}"])
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        timeout=70,
    )
    return result.stdout


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"sources": {}}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"sources": {}}


def save_state(state: dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state["last_updated_at"] = format_dt(now_cn())
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def resolve_fetch_url(config: SourceConfig, metadata_key: str) -> str:
    value = str(config.metadata.get(metadata_key) or "").strip()
    return value or config.source_url


def slugify(text: str, fallback: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    slug = re.sub(r"_+", "_", slug)
    return slug[:72] or fallback


def strip_html(text: str) -> str:
    text = re.sub(r"<br\\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</p\\s*>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def compact_snippet(text: str, limit: int = 220) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 1].rstrip() + "…"


def distill_text(*parts: str) -> str:
    blocks = [part.strip() for part in parts if part and part.strip()]
    if not blocks:
        return "_no distilled body_"
    return "\n\n".join(blocks)


def markdown_bullets(items: list[str], fallback: str = "- none") -> str:
    if not items:
        return fallback
    return "\n".join(f"  - `{compact_snippet(item, 140)}`" for item in items)


def extract_jina_markdown_body(raw_text: str) -> str:
    marker = "Markdown Content:"
    if marker in raw_text:
        return raw_text.split(marker, 1)[1].strip()
    return raw_text.strip()


def extract_json_object_after_marker(raw_text: str, marker: str) -> dict[str, Any]:
    marker_index = raw_text.find(marker)
    if marker_index < 0:
        raise RuntimeError(f"marker not found: {marker}")
    start_index = raw_text.find("{", marker_index)
    if start_index < 0:
        raise RuntimeError(f"json object start not found after marker: {marker}")
    depth = 0
    in_string = False
    escaped = False
    for pos in range(start_index, len(raw_text)):
        char = raw_text[pos]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
            continue
        if char == "{":
            depth += 1
            continue
        if char == "}":
            depth -= 1
            if depth == 0:
                return json.loads(raw_text[start_index : pos + 1])
    raise RuntimeError(f"unterminated json object after marker: {marker}")


def iter_nested_dict_values(node: Any, key: str) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict):
        value = node.get(key)
        if isinstance(value, dict):
            found.append(value)
        for child in node.values():
            found.extend(iter_nested_dict_values(child, key))
    elif isinstance(node, list):
        for child in node:
            found.extend(iter_nested_dict_values(child, key))
    return found


def extract_text_runs(value: Any) -> str:
    if isinstance(value, dict):
        simple_text = value.get("simpleText")
        if isinstance(simple_text, str):
            return clean_search_text(simple_text)
        runs = value.get("runs")
        if isinstance(runs, list):
            return clean_search_text("".join(str(item.get("text") or "") for item in runs if isinstance(item, dict)))
    return clean_search_text(str(value or ""))


def fetch_html_page(url: str, *, referer: str | None = None) -> str:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    if referer:
        headers["Referer"] = referer
    return fetch_text_via_curl(url, headers=headers)


def metadata_keywords(config: SourceConfig, key: str) -> list[str]:
    return [str(keyword).lower() for keyword in config.metadata.get(key, []) if str(keyword).strip()]


def passes_keyword_gate(
    config: SourceConfig,
    haystack: str,
    *,
    include_key: str = "include_keywords",
    exclude_key: str = "exclude_keywords",
) -> bool:
    include_keywords = metadata_keywords(config, include_key)
    if include_keywords and not any(contains_keyword(haystack, keyword) for keyword in include_keywords):
        return False
    exclude_keywords = metadata_keywords(config, exclude_key)
    if exclude_keywords and any(contains_keyword(haystack, keyword) for keyword in exclude_keywords):
        return False
    return True


def is_soft_fail(config: SourceConfig, exc: Exception) -> bool:
    haystack = f"{type(exc).__name__}: {exc}".lower()
    patterns = metadata_keywords(config, "soft_fail_patterns")
    if patterns and any(pattern in haystack for pattern in patterns):
        return True
    if config.kind == "jina_markdown_snapshot":
        default_soft_patterns = [
            "exit status 35",
            "connection reset by peer",
            "recv failure",
            "tls",
            "ssl",
        ]
        if any(pattern in haystack for pattern in default_soft_patterns):
            return True
    return False


def parse_pubdate(raw_value: str | None) -> datetime | None:
    if not raw_value:
        return None
    try:
        return parsedate_to_datetime(raw_value)
    except (TypeError, ValueError):
        return None


def parse_iso_datetime(raw_value: str | None) -> datetime | None:
    if not raw_value:
        return None
    try:
        return datetime.fromisoformat(raw_value.replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_unix_timestamp(raw_value: Any) -> datetime | None:
    try:
        timestamp = float(raw_value)
    except (TypeError, ValueError):
        return None
    if timestamp <= 0:
        return None
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def ensure_tz(dt: datetime | None, *, fallback_tz: timezone | ZoneInfo = timezone.utc) -> datetime | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=fallback_tz)
    return dt


def parse_relative_time(raw_value: str | None, captured_at: datetime) -> datetime | None:
    if not raw_value:
        return None
    cleaned = clean_search_text(raw_value).lower()
    cleaned = re.sub(r"^(streamed|premiered|live)\s+", "", cleaned).strip()
    match = re.search(r"(\d+)\s+(minute|hour|day|week|month|year)s?\s+ago", cleaned)
    if not match:
        return None
    amount = int(match.group(1))
    unit = match.group(2)
    delta_map = {
        "minute": timedelta(minutes=amount),
        "hour": timedelta(hours=amount),
        "day": timedelta(days=amount),
        "week": timedelta(weeks=amount),
        "month": timedelta(days=30 * amount),
        "year": timedelta(days=365 * amount),
    }
    delta = delta_map.get(unit)
    if delta is None:
        return None
    return captured_at - delta


def parse_hf_blog_date(raw_value: str | None) -> datetime | None:
    if not raw_value:
        return None
    parsed = ensure_tz(parse_pubdate(raw_value))
    if parsed is not None:
        return parsed
    stripped = clean_search_text(raw_value)
    for pattern in ("%B %d, %Y", "%b %d, %Y", "%B, %Y", "%b, %Y", "%B %Y", "%b %Y"):
        try:
            parsed_dt = datetime.strptime(stripped, pattern)
            if "%d" not in pattern:
                parsed_dt = parsed_dt.replace(day=1)
            return parsed_dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def parse_cn_datetime(raw_value: str | None) -> datetime | None:
    if not raw_value:
        return None
    raw_value = raw_value.strip()
    for pattern in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(raw_value, pattern).replace(tzinfo=CN_TZ)
        except ValueError:
            continue
    return None


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def matches_any_pattern(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.I) for pattern in patterns)


def normalize_text(value: str) -> str:
    return "".join(str(value or "").strip().lower().split())


def normalize_match_text(value: str) -> str:
    plain = clean_search_text(value)
    return re.sub(r"[^\w\u4e00-\u9fff]+", "", plain.lower())


def clean_search_text(value: str) -> str:
    plain = unescape(strip_html(str(value or "")))
    return re.sub(r"\s+", " ", plain).strip()


def clean_markdown_line(value: str) -> str:
    text = str(value or "").strip()
    text = re.sub(r"!\[[^\]]*\]\(([^)]+)\)", "", text)
    text = re.sub(r"!\[[^\]]*\]", "", text)
    text = re.sub(r"\[([^\]]*)\]\((https?://[^)\s]+)\)", r"\1", text)
    text = re.sub(r"^image\s+\d+\s*:?\s*", "", text, flags=re.I)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"[*_>#-]+", " ", text)
    text = text.replace("\\", " ")
    return clean_search_text(text)


def unique_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        cleaned = str(value or "").strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        ordered.append(cleaned)
    return ordered


def parse_jina_payload(raw_text: str) -> dict[str, str]:
    title_match = re.search(r"^Title:\s*(.+)$", raw_text, re.M)
    source_match = re.search(r"^URL Source:\s*(.+)$", raw_text, re.M)
    published_match = re.search(r"^Published Time:\s*(.+)$", raw_text, re.M)
    body = extract_jina_markdown_body(raw_text)
    return {
        "page_title": clean_search_text(title_match.group(1)) if title_match else "",
        "source_url": clean_search_text(source_match.group(1)) if source_match else "",
        "published_raw": clean_search_text(published_match.group(1)) if published_match else "",
        "body": body,
    }


def parse_jina_published_at(raw_value: str) -> datetime | None:
    parsed = parse_pubdate(raw_value)
    if parsed is not None:
        return parsed
    return parse_iso_datetime(raw_value)


def snapshot_ignore_patterns(config: SourceConfig) -> list[str]:
    patterns = [
        r"^(about|subscribe|tools|links|quotes|notes|guides|elsewhere|research|news|learn|commitments|search|try claude)$",
        r"^(pinned|quote|reposts?)$",
        r"^skip to main content.*$",
        r"^table of contents$",
        r"^@\w+$",
        r"^[A-Z][a-z]{2}\s+\d{1,2},\s+\d{4}$",
        r"^\d{1,2}(st|nd|rd|th)?\s+[A-Z][a-z]{2}\s+\d{4}",
        r"^\d{1,2}:\d{2}\s*(am|pm)$",
    ]
    patterns.extend(str(item) for item in config.metadata.get("snapshot_ignore_patterns", []) if str(item).strip())
    return patterns


def should_skip_snapshot_line(config: SourceConfig, line: str) -> bool:
    cleaned = clean_markdown_line(line)
    if not cleaned:
        return True
    if len(cleaned) < int(config.metadata.get("snapshot_min_chars") or 18):
        return True
    if cleaned.lower().startswith(("http://", "https://")):
        return True
    return any(re.search(pattern, cleaned, re.I) for pattern in snapshot_ignore_patterns(config))


def extract_snapshot_lines(config: SourceConfig, body: str, limit: int = 12) -> list[str]:
    mode = str(config.metadata.get("snapshot_mode") or "generic").strip()
    section_anchor = str(config.metadata.get("section_anchor") or "").strip().lower()
    started = not section_anchor
    items: list[str] = []
    for raw_line in body.splitlines():
        stripped = raw_line.strip()
        if not started and section_anchor and section_anchor in stripped.lower():
            started = True
            continue
        if not started:
            continue
        if should_skip_snapshot_line(config, stripped):
            continue
        cleaned = clean_markdown_line(stripped)
        if mode == "x_profile" and cleaned.startswith("Andrej Karpathy"):
            continue
        if cleaned in items:
            continue
        items.append(cleaned)
        if len(items) >= limit:
            break
    return items


def snapshot_link_deny_patterns(config: SourceConfig) -> list[str]:
    allow_domains = [str(item).strip().lower() for item in config.metadata.get("link_domain_allowlist", []) if str(item).strip()]
    deny_patterns = [
        r"/tags?/",
        r"/category",
        r"/search",
        r"#",
        r"mailto:",
        r"/press-kit",
        r"/photo/",
        r"_next/image",
        r"pbs\.twimg\.com",
        r"abs-0\.twimg\.com",
        r"\.(png|jpg|jpeg|gif|svg|webp)(\?|$)",
        r"[?&]format=(png|jpg|jpeg|gif|svg|webp)\b",
    ]
    deny_patterns.extend(str(item) for item in config.metadata.get("link_deny_patterns", []) if str(item).strip())
    return allow_domains, deny_patterns


def snapshot_link_allowed(candidate: str, allow_domains: list[str], deny_patterns: list[str]) -> bool:
    if allow_domains and not any(domain in candidate.lower() for domain in allow_domains):
        return False
    if any(re.search(pattern, candidate, re.I) for pattern in deny_patterns):
        return False
    return True


def snapshot_link_score(candidate: str) -> int:
    lower = candidate.lower().rstrip("/")
    score = 0
    if re.search(r"/\d{4}/\d{2}/", lower):
        score += 10
    if re.search(r"/issue-\d+\b", lower):
        score += 8
    if re.search(r"/blog/[^/]+", lower):
        score += 8
    if re.search(r"/news/[^/]+", lower):
        score += 8
    if re.search(r"/p/\d+", lower):
        score += 8
    if re.search(r"/status/\d+", lower):
        score += 6
    if re.search(r"/\d{6,}", lower):
        score += 6
    if re.search(r"/category/|/tag/|/topics?/|/search", lower):
        score -= 4
    if lower.endswith(("/news", "/blog", "/papers", "/information/ai", "/category/aigc")):
        score -= 6
    return score


def iter_markdown_links(body: str) -> list[tuple[str, str, str]]:
    body = re.sub(r"!\[[^\]]*\]\((https?://[^)\s]+)\)", "", body)
    pattern = re.compile(r"\[([^\]]*)\]\((https?://[^)\s]+)(?:\s+\"([^\"]+)\")?\)")
    return [(match.group(1), match.group(2), match.group(3) or "") for match in pattern.finditer(body)]


def extract_snapshot_links(config: SourceConfig, body: str, limit: int = 6) -> list[str]:
    allow_domains, deny_patterns = snapshot_link_deny_patterns(config)
    seen: set[str] = set()
    candidates: list[str] = []
    for _, url, _ in iter_markdown_links(body):
        candidate = url.replace("http://", "https://").strip()
        if candidate in seen:
            continue
        if not snapshot_link_allowed(candidate, allow_domains, deny_patterns):
            continue
        seen.add(candidate)
        candidates.append(candidate)
    ranked = sorted(candidates, key=lambda item: (-snapshot_link_score(item), candidates.index(item)))
    return ranked[:limit]


def extract_snapshot_link_texts(config: SourceConfig, body: str, limit: int = 12) -> list[str]:
    allow_domains, deny_patterns = snapshot_link_deny_patterns(config)
    best_text_by_url: dict[str, tuple[str, int]] = {}
    url_order: list[str] = []
    for raw_text, url, raw_title in iter_markdown_links(body):
        candidate_url = url.replace("http://", "https://").strip()
        if not snapshot_link_allowed(candidate_url, allow_domains, deny_patterns):
            continue
        cleaned = clean_markdown_line(raw_text)
        cleaned_title = clean_markdown_line(raw_title)
        if (not cleaned or cleaned.lower().startswith("image ")) and cleaned_title:
            cleaned = cleaned_title
        cleaned = normalize_snapshot_entry_text(cleaned)
        if not snapshot_entry_allowed(config, cleaned):
            continue
        text_score = snapshot_entry_text_score(config, cleaned)
        if candidate_url not in best_text_by_url:
            url_order.append(candidate_url)
            best_text_by_url[candidate_url] = (cleaned, text_score)
            continue
        _, existing_score = best_text_by_url[candidate_url]
        if text_score > existing_score:
            best_text_by_url[candidate_url] = (cleaned, text_score)
    items = unique_strings([best_text_by_url[url][0] for url in url_order if best_text_by_url.get(url)])
    return items[:limit]


def extract_snapshot_embedded_date(text: str) -> datetime | None:
    raw_text = clean_search_text(text)
    patterns = [
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{1,2},\s+\d{4}\b",
        r"\b\d{4}-\d{2}-\d{2}\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, raw_text, re.I)
        if not match:
            continue
        token = match.group(0)
        parsed = parse_hf_blog_date(token)
        if parsed is not None:
            return parsed
        try:
            return datetime.strptime(token, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def normalize_snapshot_entry_text(text: str) -> str:
    cleaned = clean_markdown_line(text)
    cleaned = re.sub(r"^(#+\s*)+", "", cleaned).strip()
    cleaned = re.sub(
        r"^(?:Products?|Announcements?|Policy|Research|News|Blog|Stories|Engineering|Insights?)\s+"
        r"(?=(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{1,2},\s+\d{4})",
        "",
        cleaned,
        flags=re.I,
    )
    cleaned = re.sub(
        r"^(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{1,2},\s+\d{4}\s+",
        "",
        cleaned,
        flags=re.I,
    )
    cleaned = re.sub(r"^\d{4}-\d{2}-\d{2}\s+", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return clean_search_text(cleaned)


def snapshot_entry_patterns(config: SourceConfig, key: str) -> list[str]:
    return [str(item) for item in config.metadata.get(key, []) if str(item).strip()]


def snapshot_entry_matches_patterns(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.I) for pattern in patterns)


def is_fragmentary_snapshot_text(text: str) -> bool:
    cleaned = clean_search_text(text)
    if not cleaned:
        return True
    if re.match(r"^[,.;:!?/&)\]-]", cleaned):
        return True
    return bool(re.match(r"^(this|that|these|those|here|there|and|or|but)\b", cleaned, re.I))


def is_dangling_x_snapshot_text(text: str) -> bool:
    cleaned = clean_search_text(text)
    if not cleaned:
        return True
    lowered = cleaned.lower().strip()
    if lowered.endswith(("…", "...", ",")):
        return True
    if re.search(
        r"(?:\b|^)(like|powered by|researcher|host|hosts|joins|join|and|or|but|with|without|for|from|to|of|in|on|at|by|via|into|onto|around|across|through|inside|outside|beneath|under|over|about|the chain)$",
        lowered,
    ):
        return True
    if lowered.endswith(":") and len(cleaned) < 72:
        return True
    return False


def snapshot_entry_text_score(config: SourceConfig, text: str) -> int:
    cleaned = normalize_snapshot_entry_text(text)
    if not cleaned:
        return -999
    score = 0
    text_len = len(cleaned)
    if 16 <= text_len <= 96:
        score += 6
    elif text_len <= 180:
        score += 4
    elif text_len <= 320:
        score += 1
    else:
        score -= 3
    if text_len < 14:
        score -= 4
    if re.match(r"^[a-z]", cleaned) and text_len > 15:
        score -= 3
    if re.match(r"^(?:I\b|I['’]m\b|We\b|Our\b|See\b|More on\b|By subscribing\b)", cleaned, re.I):
        score -= 4
    if cleaned.startswith("—"):
        score -= 6
    if cleaned.startswith(("“", '"', "‘", "'")):
        score -= 3
    if cleaned.endswith(".") and text_len > 40:
        score -= 2
    if cleaned.endswith("。") and text_len > 24:
        score -= 2
    cn_comma_count = cleaned.count("，") + cleaned.count("；")
    en_comma_count = cleaned.count(",") + cleaned.count(";")
    if cn_comma_count >= 2 and text_len > 50:
        score -= 4
    elif cn_comma_count >= 1 and text_len > 80:
        score -= 2
    if en_comma_count >= 5 and text_len > 120:
        score -= 1
    if snapshot_entry_matches_patterns(
        cleaned,
        [
            r"^the batch ai news and insights:.*$",
            r"^what matters in ai right now$",
            r"^openclaw home page$",
            r"^install and configure$",
            r"^automation overview$",
            r"^automation troubleshooting$",
            r"^understanding ai$",
            r"^exploring how ai works.*$",
            r"^by subscribing, you agree.*$",
            r"^over [\d,]+ subscribers$",
            r"^home page$",
            r"^(about|archive|recommendations|search|navigation)$",
        ],
    ):
        score -= 8
    if snapshot_entry_matches_patterns(
        cleaned,
        [
            r"\b(release|released|launch(?:ed)?|introduc(?:e|ing)|updated?|upgrade|breaking change|changelog|version|preview|beta|now available|gpt|chatgpt|codex|claude|gemini|openai|anthropic|agent|agents|plugin|plugins|model|models|融资|开源|发布|上线|推出|登场|ipo)\b",
        ],
    ):
        score += 1
    if str(config.metadata.get("snapshot_mode") or "").strip() == "x_profile" and is_dangling_x_snapshot_text(cleaned):
        score -= 8
    return score


def snapshot_entry_allowed(config: SourceConfig, text: str) -> bool:
    cleaned = normalize_snapshot_entry_text(text)
    if should_skip_snapshot_line(config, cleaned) or is_fragmentary_snapshot_text(cleaned):
        return False
    include_patterns = snapshot_entry_patterns(config, "snapshot_include_patterns")
    if include_patterns and not snapshot_entry_matches_patterns(cleaned, include_patterns):
        return False
    exclude_patterns = snapshot_entry_patterns(config, "snapshot_exclude_patterns")
    if exclude_patterns and snapshot_entry_matches_patterns(cleaned, exclude_patterns):
        return False
    if str(config.metadata.get("snapshot_mode") or "").strip() == "x_profile" and is_dangling_x_snapshot_text(cleaned):
        return False
    min_score_raw = config.metadata.get("snapshot_min_score")
    min_score = int(min_score_raw) if min_score_raw is not None else 2
    if snapshot_entry_text_score(config, cleaned) < min_score:
        return False
    return True


def extract_snapshot_status_links(body: str, limit: int = 8) -> list[str]:
    status_links: list[str] = []
    for _, url, _ in iter_markdown_links(body):
        candidate = url.replace("http://", "https://").strip()
        if "/status/" not in candidate or candidate in status_links:
            continue
        status_links.append(candidate)
        if len(status_links) >= limit:
            break
    return status_links


def extract_snapshot_heading_entries(config: SourceConfig, body: str, limit: int = 6) -> list[dict[str, Any]]:
    allow_domains, deny_patterns = snapshot_link_deny_patterns(config)
    lines = body.splitlines()
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    entries: list[dict[str, Any]] = []
    heading_pattern = re.compile(r"^\s{0,3}#{1,6}\s+(?P<title>.+?)\s*$")
    inline_link_pattern = re.compile(r"\[([^\]]*)\]\((https?://[^)\s]+)(?:\s+\"([^\"]+)\")?\)")
    for idx, raw_line in enumerate(lines):
        match = heading_pattern.match(raw_line)
        if not match:
            continue
        cleaned = normalize_snapshot_entry_text(match.group("title"))
        if not snapshot_entry_allowed(config, cleaned):
            continue
        nearby_urls: list[tuple[str, int, int]] = []
        for probe in range(max(0, idx - 4), idx + 1):
            for link_match in inline_link_pattern.finditer(lines[probe]):
                candidate_url = link_match.group(2).replace("http://", "https://").strip()
                if not snapshot_link_allowed(candidate_url, allow_domains, deny_patterns):
                    continue
                nearby_urls.append((candidate_url, snapshot_link_score(candidate_url), probe))
        if not nearby_urls:
            continue
        nearby_urls.sort(key=lambda item: (-item[1], item[2]))
        candidate_url = nearby_urls[0][0]
        title_key = normalize_match_text(cleaned)
        if candidate_url in seen_urls or title_key in seen_titles:
            continue
        seen_urls.add(candidate_url)
        seen_titles.add(title_key)
        entries.append(
            {
                "url": candidate_url,
                "text": cleaned,
                "title": cleaned,
                "order": idx,
                "entry_origin": "heading",
                "published_dt": extract_snapshot_embedded_date(cleaned),
                "text_score": snapshot_entry_text_score(config, cleaned),
            }
        )
        if len(entries) >= limit:
            break
    return entries


def extract_snapshot_link_entries(config: SourceConfig, body: str, limit: int = 6) -> list[dict[str, Any]]:
    allow_domains, deny_patterns = snapshot_link_deny_patterns(config)
    best_by_url: dict[str, dict[str, Any]] = {}
    url_order: list[str] = []
    for idx, (raw_text, url, raw_title) in enumerate(iter_markdown_links(body)):
        candidate_url = url.replace("http://", "https://").strip()
        if not snapshot_link_allowed(candidate_url, allow_domains, deny_patterns):
            continue
        cleaned = clean_markdown_line(raw_text)
        cleaned_title = clean_markdown_line(raw_title)
        if (not cleaned or cleaned.lower().startswith("image ")) and cleaned_title:
            cleaned = cleaned_title
        cleaned = normalize_snapshot_entry_text(cleaned)
        if not snapshot_entry_allowed(config, cleaned):
            continue
        text_score = snapshot_entry_text_score(config, cleaned)
        entry = {
            "url": candidate_url,
            "text": cleaned,
            "title": cleaned,
            "order": idx,
            "entry_origin": "link",
            "published_dt": extract_snapshot_embedded_date(cleaned),
            "text_score": text_score,
        }
        current = best_by_url.get(candidate_url)
        if current is None:
            best_by_url[candidate_url] = entry
            url_order.append(candidate_url)
            continue
        if text_score > int(current.get("text_score") or 0):
            best_by_url[candidate_url] = entry
    ranked = sorted(
        [best_by_url[url] for url in url_order],
        key=lambda item: (
            -int(item.get("text_score") or 0),
            -snapshot_link_score(str(item["url"])),
            int(item["order"]),
        ),
    )
    return ranked[:limit]


def extract_snapshot_line_entries(
    config: SourceConfig,
    body: str,
    *,
    limit: int = 6,
    candidate_urls: list[str] | None = None,
) -> list[dict[str, Any]]:
    lines = extract_snapshot_lines(config, body, limit=max(limit * 3, limit))
    urls = candidate_urls or []
    seen: set[str] = set()
    entries: list[dict[str, Any]] = []
    for idx, raw_line in enumerate(lines):
        cleaned = normalize_snapshot_entry_text(raw_line)
        key = normalize_match_text(cleaned)
        if not key or key in seen or not snapshot_entry_allowed(config, cleaned):
            continue
        seen.add(key)
        origin = "x-line" if str(config.metadata.get("snapshot_mode") or "").strip() == "x_profile" else "line"
        entries.append(
            {
                "url": urls[idx] if idx < len(urls) else config.source_url,
                "text": cleaned,
                "title": cleaned,
                "order": idx,
                "entry_origin": origin,
                "published_dt": extract_snapshot_embedded_date(cleaned),
                "text_score": snapshot_entry_text_score(config, cleaned),
            }
        )
        if len(entries) >= limit:
            break
    return entries


def build_jina_snapshot_entry_item(
    config: SourceConfig,
    payload: dict[str, str],
    entry: dict[str, Any],
    captured_at: datetime,
    *,
    capture_url: str,
    page_title: str,
    page_snapshot_lines: list[str],
) -> dict[str, Any]:
    entry_title = compact_snippet(str(entry.get("title") or entry.get("text") or page_title).strip(), 120)
    entry_text = clean_search_text(str(entry.get("text") or entry_title))
    canonical_url = str(entry.get("url") or config.source_url).strip() or config.source_url
    source_url = payload["source_url"] or config.source_url
    published_dt = entry.get("published_dt") or parse_jina_published_at(payload["published_raw"])
    entry_origin = str(entry.get("entry_origin") or "link")
    quote_candidates = unique_strings([entry_title, entry_text, *page_snapshot_lines[:2]])[:4]

    if entry_origin == "x-line":
        summary = (
            f"{config.source_name} 的 X profile 捕捉到近期帖文“{entry_title}”。"
            "它适合作为社交快信号和扩散入口，正式事实仍需回链官网、docs 或单帖原文。"
        )
        distilled_body = distill_text(
            f"账号：{config.source_name}",
            f"帖文片段：{entry_text}",
            f"单帖入口：{canonical_url}" if canonical_url != config.source_url else "",
            "同页其他高信号片段：\n" + "\n".join(f"- {line}" for line in page_snapshot_lines[:5]) if page_snapshot_lines else "",
        )
        content_type = "x post excerpt"
        capture_method = "jina-reader / x-profile line extraction"
        worth = canonical_url if canonical_url != config.source_url else "同主题官网 / docs / 单帖 / 讨论线程"
    else:
        summary = (
            f"{config.source_name} 当前页提取到近期条目“{entry_title}”。"
            "它适合作为官方更新、专家观察或中文传播层的单条入口，后续应回链原文继续核验。"
        )
        distilled_body = distill_text(
            f"来源页面：{page_title}",
            f"条目标题：{entry_title}",
            f"条目摘录：{entry_text}",
            f"原文入口：{canonical_url}" if canonical_url else "",
            "同页近期上下文：\n" + "\n".join(f"- {line}" for line in page_snapshot_lines[:5]) if page_snapshot_lines else "",
        )
        content_type = config.metadata.get("content_type", "web linked item")
        capture_method = "jina-reader / page link extraction" if entry_origin == "link" else "jina-reader / page line extraction"
        worth = canonical_url or "单篇原文 / 官方博客 / repo / docs"

    raw_body = (
        "# Raw Capture\n\n"
        f"- `source_id`: `{config.source_id}`\n"
        f"- `page_title`: `{page_title}`\n"
        f"- `source_url`: {source_url}\n"
        f"- `capture_url`: {capture_url}\n"
        f"- `entry_origin`: `{entry_origin}`\n"
        f"- `entry_url`: {canonical_url}\n"
        f"- `published_raw`: `{payload['published_raw'] or 'unknown'}`\n"
        f"- `published_at`: `{format_dt(published_dt)}`\n"
        f"- `captured_at`: `{format_dt(captured_at)}`\n\n"
        "## Entry Text\n\n"
        f"{entry_text or entry_title}\n\n"
        "## Page Snapshot Lines\n\n"
        + ("\n".join(f"- {line}" for line in page_snapshot_lines[:8]) if page_snapshot_lines else "- none")
        + "\n"
    )
    item_key = canonical_url if canonical_url and canonical_url != config.source_url else f"{config.source_id}:{normalize_match_text(entry_text) or slugify(entry_title, config.source_id)}"
    topic_tags = unique_strings([*config.metadata.get("topic_tags", ["jina-snapshot"]), "snapshot-entry"])
    return {
        "item_key": item_key,
        "packet_slug": f"{config.packet_prefix}_{slugify(entry_title, config.source_id)}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": source_url,
        "canonical_url": canonical_url,
        "title": entry_title,
        "author_or_channel": config.source_name,
        "published_at": format_dt(published_dt),
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": content_type,
        "capture_method": capture_method,
        "normalization_method": "markdown_normalized",
        "translation_needed": "yes" if config.language == "en" else "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": config.metadata.get("primary_source", "partial"),
        "verification_status": config.metadata.get("verification_status", "snapshot-signal"),
        "summary": summary,
        "topic_tags": topic_tags,
        "quote_candidates": quote_candidates,
        "distilled_body": distilled_body,
        "why_source_matters": config.metadata.get(
            "why_source_matters",
            "Jina snapshot 能把难直连的站点先转成可追踪的入口层快照。",
        ),
        "citation_reliability": config.metadata.get("citation_reliability", "medium"),
        "caveat": config.metadata.get(
            "caveat",
            "这是入口快照层，不等于最终事实结论；正式引用仍需回链单篇原文和一手对象。",
        ),
        "raw_body": raw_body,
        "normalized_excerpt": compact_snippet(entry_text or entry_title, 360),
        "worth_clustering_with": worth,
        "possible_topic_directions": config.metadata.get("follow_up_hints", []),
        "heat_hint": config.metadata.get("heat_hint", "snapshot signal"),
    }


def build_jina_snapshot_entry_items(
    config: SourceConfig,
    raw_text: str,
    captured_at: datetime,
    *,
    capture_url: str,
    limit: int,
) -> list[dict[str, Any]]:
    payload = parse_jina_payload(raw_text)
    body = payload["body"]
    page_title = clean_search_text(str(config.metadata.get("page_title_override") or "")) or payload["page_title"] or config.source_name
    page_snapshot_lines = extract_snapshot_lines(
        config,
        body,
        limit=int(config.metadata.get("snapshot_line_limit") or max(limit * 2, 8)),
    )
    mode = str(config.metadata.get("snapshot_mode") or "generic").strip()
    if mode == "x_profile":
        status_links = extract_snapshot_status_links(body, limit=max(limit * 2, 6))
        entries = extract_snapshot_line_entries(config, body, limit=limit, candidate_urls=status_links)
    else:
        prefer_line_entries = bool(config.metadata.get("snapshot_prefer_line_entries"))
        entries = extract_snapshot_line_entries(config, body, limit=limit) if prefer_line_entries else []
        if not entries:
            entries = extract_snapshot_link_entries(config, body, limit=limit)
        if not entries:
            entries = extract_snapshot_heading_entries(config, body, limit=limit)
        if not entries:
            fallback_urls = extract_snapshot_links(config, body, limit=max(limit * 2, 6))
            entries = extract_snapshot_line_entries(config, body, limit=limit, candidate_urls=fallback_urls)
    return [
        build_jina_snapshot_entry_item(
            config,
            payload,
            entry,
            captured_at,
            capture_url=capture_url,
            page_title=page_title,
            page_snapshot_lines=page_snapshot_lines,
        )
        for entry in entries
    ]


def contains_keyword(haystack: str, keyword: str) -> bool:
    normalized = str(keyword or "").strip().lower()
    if not normalized:
        return False
    if re.fullmatch(r"[a-z0-9.+_-]+", normalized):
        pattern = rf"(^|[^a-z0-9]){re.escape(normalized)}([^a-z0-9]|$)"
        return re.search(pattern, haystack) is not None
    return normalized in haystack


def iter_bilibili_video_candidates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    sections = data.get("result", []) if isinstance(data, dict) else []
    candidates: list[dict[str, Any]] = []
    for section in sections if isinstance(sections, list) else []:
        if not isinstance(section, dict) or section.get("result_type") != "video":
            continue
        for item in section.get("data", []) if isinstance(section.get("data"), list) else []:
            if not isinstance(item, dict):
                continue
            title = clean_search_text(item.get("title") or "")
            uploader = clean_search_text(item.get("author") or "")
            bvid = str(item.get("bvid") or "").strip()
            arcurl = str(item.get("arcurl") or "").strip()
            if not arcurl and bvid:
                arcurl = f"https://www.bilibili.com/video/{bvid}"
            if arcurl.startswith("http://"):
                arcurl = "https://" + arcurl.removeprefix("http://")
            pubdate = ""
            raw_pubdate = item.get("pubdate")
            if isinstance(raw_pubdate, (int, float)) and raw_pubdate > 0:
                pubdate = format_dt(datetime.fromtimestamp(float(raw_pubdate), tz=timezone.utc).astimezone(CN_TZ))
            candidates.append(
                {
                    "title": title,
                    "uploader": uploader,
                    "bvid": bvid,
                    "url": arcurl,
                    "typename": str(item.get("typename") or "").strip(),
                    "play": str(item.get("play") or "").strip(),
                    "pubdate": pubdate,
                    "description": clean_search_text(item.get("description") or ""),
                }
            )
    return candidates


def resolve_bilibili_video(title: str, uploader: str) -> dict[str, Any] | None:
    target_title = clean_search_text(title)
    target_uploader = clean_search_text(uploader)
    target_title_norm = normalize_match_text(target_title)
    target_uploader_norm = normalize_match_text(target_uploader)
    if not target_title_norm:
        return None
    queries = unique_strings(
        [
            target_title,
            f"{target_title} {target_uploader}" if target_uploader else "",
            target_title[:40] if len(target_title) > 40 else "",
        ]
    )
    best: dict[str, Any] | None = None
    for query in queries:
        search_url = f"https://api.bilibili.com/x/web-interface/search/all/v2?keyword={quote(query)}"
        try:
            payload = fetch_json(search_url)
        except Exception:
            continue
        for candidate in iter_bilibili_video_candidates(payload):
            candidate_title_norm = normalize_match_text(candidate["title"])
            candidate_uploader_norm = normalize_match_text(candidate["uploader"])
            title_ratio = (
                difflib.SequenceMatcher(None, target_title_norm, candidate_title_norm).ratio()
                if candidate_title_norm
                else 0.0
            )
            uploader_ratio = (
                difflib.SequenceMatcher(None, target_uploader_norm, candidate_uploader_norm).ratio()
                if target_uploader_norm and candidate_uploader_norm
                else 0.0
            )
            uploader_exact = bool(target_uploader_norm and target_uploader_norm == candidate_uploader_norm)
            substring_bonus = (
                0.08
                if target_title_norm
                and candidate_title_norm
                and (target_title_norm in candidate_title_norm or candidate_title_norm in target_title_norm)
                else 0.0
            )
            score = title_ratio + substring_bonus + (0.35 if uploader_exact else 0.15 * uploader_ratio)
            enriched = {
                **candidate,
                "query": query,
                "title_ratio": title_ratio,
                "uploader_ratio": uploader_ratio,
                "uploader_exact": uploader_exact,
                "score": score,
            }
            accepted = title_ratio >= 0.90 or (title_ratio >= 0.74 and uploader_exact) or score >= 1.18
            confidence = "high" if title_ratio >= 0.95 and uploader_exact else "medium" if accepted else "low"
            if accepted and (confidence == "high" or query == target_title):
                return {**enriched, "accepted": accepted, "confidence": confidence}
            if best is None or score > best["score"]:
                best = enriched
    if best is None:
        return None
    accepted = best["title_ratio"] >= 0.90 or (best["title_ratio"] >= 0.74 and best["uploader_exact"]) or best["score"] >= 1.18
    confidence = "high" if best["title_ratio"] >= 0.95 and best["uploader_exact"] else "medium" if accepted else "low"
    return {**best, "accepted": accepted, "confidence": confidence}


def guess_image_suffix(url: str) -> str:
    match = re.search(r"\.(png|jpe?g|webp)(?:[?#].*)?$", url, re.I)
    if match:
        return f".{match.group(1).lower()}"
    return ".img"


def get_rapidocr_engine() -> Any:
    global RAPIDOCR_ENGINE
    if RAPIDOCR_ENGINE is None:
        from rapidocr_onnxruntime import RapidOCR

        RAPIDOCR_ENGINE = RapidOCR()
    return RAPIDOCR_ENGINE


def ocr_image_from_url(image_url: str) -> dict[str, Any]:
    image_bytes = fetch_binary_via_curl(
        image_url,
        headers={
            "User-Agent": USER_AGENT,
            "Referer": "https://www.newrank.cn/",
        },
    )
    suffix = guess_image_suffix(image_url)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(prefix="newrank_ocr_", suffix=suffix, delete=False) as handle:
            handle.write(image_bytes)
            temp_path = Path(handle.name)
        engine = get_rapidocr_engine()
        result, _ = engine(str(temp_path))
        observations: list[dict[str, Any]] = []
        for row in result or []:
            if not isinstance(row, (list, tuple)) or len(row) < 3:
                continue
            box = row[0]
            text = clean_search_text(row[1] or "")
            if not text:
                continue
            try:
                score = float(row[2])
            except (TypeError, ValueError):
                score = 0.0
            xs: list[float] = []
            ys: list[float] = []
            for point in box if isinstance(box, (list, tuple)) else []:
                if not isinstance(point, (list, tuple)) or len(point) < 2:
                    continue
                try:
                    xs.append(float(point[0]))
                    ys.append(float(point[1]))
                except (TypeError, ValueError):
                    continue
            if not xs or not ys:
                continue
            observations.append(
                {
                    "text": text,
                    "score": score,
                    "x": sum(xs) / len(xs),
                    "y": sum(ys) / len(ys),
                }
            )
        observations.sort(key=lambda item: (item["y"], item["x"]))
        return {"image_url": image_url, "observations": observations}
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def select_ocr_text(
    items: list[dict[str, Any]],
    *,
    x_min: float,
    x_max: float,
    pattern: str | None = None,
    prefer_longest: bool = False,
) -> str:
    center = (x_min + x_max) / 2
    candidates = [item for item in items if x_min <= float(item.get("x") or 0) < x_max]
    if pattern:
        filtered = [item for item in candidates if re.search(pattern, str(item.get("text") or ""))]
        if filtered:
            candidates = filtered
    if not candidates:
        return ""
    candidates.sort(
        key=lambda item: (
            len(str(item.get("text") or "")) if prefer_longest else 0,
            float(item.get("score") or 0),
            -abs(float(item.get("x") or 0) - center),
        ),
        reverse=True,
    )
    return str(candidates[0].get("text") or "").strip()


def extract_newrank_rank_rows(observations: list[dict[str, Any]], limit: int = 15) -> list[dict[str, str]]:
    row_seed_items = [item for item in observations if float(item.get("y") or 0) >= 620 and float(item.get("score") or 0) >= 0.52]
    groups: list[list[dict[str, Any]]] = []
    current_group: list[dict[str, Any]] = []
    last_y: float | None = None
    for item in row_seed_items:
        current_y = float(item.get("y") or 0)
        if last_y is None or current_y - last_y <= 60:
            current_group.append(item)
        else:
            groups.append(current_group)
            current_group = [item]
        last_y = current_y
    if current_group:
        groups.append(current_group)

    rows: list[dict[str, str]] = []
    for group in groups:
        account_name = select_ocr_text(
            group,
            x_min=180,
            x_max=420,
            pattern=r"[A-Za-z\u4e00-\u9fff]",
            prefer_longest=True,
        )
        if not account_name:
            continue
        if account_name in {"公众号", "统计时间", "总阅读", "总点赞", "AI新榜指数", "平均", "最高"}:
            continue
        rank_text = select_ocr_text(group, x_min=0, x_max=120, pattern=r"^\d+$")
        rank_value = rank_text if rank_text.isdigit() else str(len(rows) + 1)
        rows.append(
            {
                "rank": rank_value,
                "account_name": account_name,
                "publish_count": select_ocr_text(group, x_min=420, x_max=520, pattern=r"\d"),
                "observed_total_read": select_ocr_text(group, x_min=595, x_max=635, pattern=r"\d|万|亿"),
                "observed_avg_read": select_ocr_text(group, x_min=520, x_max=595, pattern=r"\d|万|亿"),
                "observed_peak_read": select_ocr_text(group, x_min=635, x_max=720, pattern=r"\d|万|亿"),
                "observed_total_like": select_ocr_text(group, x_min=730, x_max=860, pattern=r"\d|万|亿"),
                "observed_ai_index": select_ocr_text(group, x_min=880, x_max=1000, pattern=r"\d"),
            }
        )
        if len(rows) >= limit:
            break
    return rows


def render_newrank_rank_rows(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "- none"
    lines: list[str] = []
    for row in rows:
        parts = [f"#{row['rank']} {row['account_name']}"]
        if row.get("publish_count"):
            parts.append(f"发布 {row['publish_count']}")
        if row.get("observed_total_read"):
            parts.append(f"总阅读 {row['observed_total_read']}")
        if row.get("observed_avg_read"):
            parts.append(f"平均阅读 {row['observed_avg_read']}")
        if row.get("observed_peak_read"):
            parts.append(f"最高阅读 {row['observed_peak_read']}")
        if row.get("observed_total_like"):
            parts.append(f"总点赞 {row['observed_total_like']}")
        if row.get("observed_ai_index"):
            parts.append(f"AI新榜指数 {row['observed_ai_index']}")
        lines.append("- " + "｜".join(parts))
    return "\n".join(lines)


def summarize_newrank_ocr(image_paths: list[str]) -> dict[str, Any]:
    errors: list[str] = []
    processed_images: list[dict[str, Any]] = []
    for image_url in image_paths:
        try:
            processed_images.append(ocr_image_from_url(image_url))
        except Exception as exc:
            errors.append(f"{image_url} → {type(exc).__name__}: {exc}")
    primary_observations = processed_images[0]["observations"] if processed_images else []
    excerpt_lines = unique_strings(
        [str(item.get("text") or "") for item in primary_observations if float(item.get("score") or 0) >= 0.55]
    )[:60]
    rows = extract_newrank_rank_rows(primary_observations, limit=15)
    return {
        "status": "ok" if processed_images else "failed",
        "engine": "rapidocr_onnxruntime" if processed_images else "unavailable",
        "processed_image_count": len(processed_images),
        "detected_text_blocks": sum(len(image["observations"]) for image in processed_images),
        "rows": rows,
        "text_excerpt_lines": excerpt_lines,
        "errors": errors,
    }


def request_wemp_json(
    url: str,
    *,
    method: str = "GET",
    data: dict[str, object] | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    payload = None
    headers: dict[str, str] = {}
    if data is not None:
        payload = urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, data=payload, headers=headers, method=method)
    with urlopen(request, timeout=30) as response:
        body = response.read().decode("utf-8", "ignore")
    if not body:
        return {}
    parsed = json.loads(body)
    return parsed if isinstance(parsed, dict) else {"data": parsed}


def wemp_login(username: str = "admin", password: str = "admin123") -> str:
    global WEMP_TOKEN_CACHE
    if WEMP_TOKEN_CACHE:
        return WEMP_TOKEN_CACHE
    payload = request_wemp_json(
        WEMP_LOGIN_URL,
        method="POST",
        data={"username": username, "password": password},
    )
    token = ((payload.get("data") or {}) if isinstance(payload.get("data"), dict) else {}).get("access_token")
    if not token:
        raise RuntimeError(f"WeMP login failed: {payload}")
    WEMP_TOKEN_CACHE = str(token)
    return WEMP_TOKEN_CACHE


def list_wemp_subscriptions(token: str) -> list[dict[str, Any]]:
    global WEMP_SUBSCRIPTIONS_CACHE
    if WEMP_SUBSCRIPTIONS_CACHE is not None:
        return WEMP_SUBSCRIPTIONS_CACHE
    items: list[dict[str, Any]] = []
    offset = 0
    page_size = 100
    while True:
        payload = request_wemp_json(f"{WEMP_MPS_URL}?limit={page_size}&offset={offset}", token=token)
        data = payload.get("data") or {}
        page = data.get("list") if isinstance(data, dict) else []
        if not isinstance(page, list) or not page:
            break
        items.extend(item for item in page if isinstance(item, dict))
        if len(page) < page_size:
            break
        offset += page_size
    WEMP_SUBSCRIPTIONS_CACHE = items
    return items


def resolve_wechat_feed_url(config: SourceConfig) -> str:
    target_name = str(config.metadata.get("mp_name") or config.source_name).strip()
    aliases = [target_name]
    aliases.extend(str(item).strip() for item in config.metadata.get("aliases", []) if str(item).strip())
    token = wemp_login()
    subscriptions = list_wemp_subscriptions(token)
    by_name = {
        normalize_text(str(item.get("mp_name") or "")): item
        for item in subscriptions
        if str(item.get("mp_name") or "").strip()
    }
    for alias in aliases:
        hit = by_name.get(normalize_text(alias))
        if hit is not None:
            feed_id = str(hit.get("id") or "").strip()
            if feed_id:
                return f"{WEMP_BASE_URL}/rss/{quote(feed_id, safe='')}"
    raise RuntimeError(f"WeChat subscription not found in WeMP-RSS: {target_name}")


def decode_escaped_url(raw_value: str) -> str:
    return (
        raw_value.replace("\\u0026", "&")
        .replace("\\u003d", "=")
        .replace("\\u002F", "/")
        .replace("\\/", "/")
    )


def resolve_youtube_feed_url(source_url: str) -> str:
    if "feeds/videos.xml" in source_url:
        return source_url
    html = fetch_text(source_url)
    direct_match = re.search(r"https://www\.youtube\.com/feeds/videos\.xml\?channel_id=[^\"'&<>\s]+", html)
    if direct_match:
        return direct_match.group(0)
    rss_match = re.search(r'"rssUrl":"(https:\\u002F\\u002Fwww\.youtube\.com\\u002Ffeeds\\u002Fvideos\.xml\\?channel_id=[^"]+)"', html)
    if rss_match:
        return decode_escaped_url(rss_match.group(1))
    channel_id_match = re.search(r'"externalId":"(UC[^"]+)"', html) or re.search(
        r'<meta itemprop="channelId" content="(UC[^"]+)">',
        html,
    )
    if channel_id_match:
        return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id_match.group(1)}"
    raise RuntimeError(f"Could not resolve YouTube feed URL from: {source_url}")


def fetch_reddit_rss_text(url: str) -> str:
    return fetch_text_via_curl(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/atom+xml,application/xml,text/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://old.reddit.com/",
        },
    )


def extract_reddit_content_lines(content_html: str, limit: int = 4) -> list[str]:
    content_text = strip_html(unescape(content_html or ""))
    lines = unique_strings(
        [
            clean_search_text(line)
            for line in re.split(r"\n+", content_text)
            if clean_search_text(line)
        ]
    )
    cleaned_lines: list[str] = []
    for line in lines:
        normalized = line.strip()
        if normalized in {"[link]", "[comments]"}:
            continue
        if normalized.startswith("/u/"):
            continue
        cleaned_lines.append(normalized)
        if len(cleaned_lines) >= limit:
            break
    return cleaned_lines


def extract_reddit_external_url(content_html: str) -> str:
    raw_html = unescape(content_html or "")
    href_matches = re.findall(r"""href=["']([^"']+)["']""", raw_html, re.I)
    text_matches = re.findall(r"https?://[^\s<>\"]+", raw_html)
    candidate_urls = unique_strings(
        [
            candidate.replace("&amp;", "&").strip().rstrip(").,;")
            for candidate in href_matches + text_matches
            if candidate.strip()
        ]
    )
    ignored_hosts = {
        "old.reddit.com",
        "www.reddit.com",
        "reddit.com",
        "redd.it",
        "preview.redd.it",
        "i.redd.it",
        "v.redd.it",
        "external-preview.redd.it",
        "redditmedia.com",
        "www.redditmedia.com",
    }
    for candidate in candidate_urls:
        host = urlparse(candidate).netloc.lower()
        if host.startswith("www."):
            host = host[4:]
        if host in ignored_hosts or not candidate.startswith("http"):
            continue
        return candidate
    return ""


def build_reddit_rss_item(
    config: SourceConfig,
    entry: ET.Element,
    captured_at: datetime,
    *,
    rank: int,
    capture_url: str,
) -> dict[str, Any]:
    title = clean_search_text(entry.findtext("atom:title", "", ATOM_NS) or "untitled reddit thread")
    permalink = str(entry.find("atom:link", ATOM_NS).attrib.get("href") if entry.find("atom:link", ATOM_NS) is not None else config.source_url).strip()
    item_key = clean_search_text(entry.findtext("atom:id", "", ATOM_NS) or permalink or title)
    published_at = parse_iso_datetime(entry.findtext("atom:published", "", ATOM_NS)) or parse_iso_datetime(
        entry.findtext("atom:updated", "", ATOM_NS)
    )
    author = clean_search_text(entry.findtext("atom:author/atom:name", "", ATOM_NS) or "unknown")
    subreddit = str(config.metadata.get("subreddit") or "reddit").strip()
    content_html = entry.findtext("atom:content", "", ATOM_NS) or ""
    content_lines = extract_reddit_content_lines(content_html, limit=5)
    external_url = extract_reddit_external_url(content_html)
    excerpt_base = " / ".join(content_lines[:3]) if content_lines else title
    raw_body = textwrap.dedent(
        f"""\
        # Raw Capture

        - `source_id`: `{config.source_id}`
        - `subreddit`: `r/{subreddit}`
        - `rank_in_feed`: `{rank}`
        - `title`: `{title}`
        - `permalink`: {permalink}
        - `external_url`: {external_url or 'unknown'}
        - `author`: `{author}`
        - `capture_url`: {capture_url}
        - `published_at`: `{format_dt(published_at)}`
        - `captured_at`: `{format_dt(captured_at)}`

        ## Feed Content

        {markdown_bullets(content_lines)}
        """
    ).strip() + "\n"
    distilled_body = distill_text(
        f"主题：{title}",
        "帖子正文摘录：\n" + "\n".join(f"- {line}" for line in content_lines[:4]) if content_lines else "",
        f"外部对象线索：{external_url}" if external_url else "",
        f"帖子链接：{permalink}",
    )
    summary = (
        f"Reddit / r/{subreddit} 的日榜 RSS 收录了“{title}”，当前位于本轮抓取顺序第 {rank} 位。"
        "它更适合判断真实用户问题、真实体验和外部对象入口，不适合直接当正式事实证据。"
    )
    directions = []
    if external_url:
        directions.append(f"优先回链外部对象：{external_url}")
    directions.append("结合帖子正文判断这是真实痛点、真实 workflow 还是纯情绪宣泄")
    directions.append("如果讨论命中产品 / 模型 / 硬件，再补官网、文档、创始人账号和社区二次验证")
    return {
        "item_key": item_key,
        "packet_slug": f"{config.packet_prefix}_{slugify(title, item_key)}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": capture_url,
        "canonical_url": permalink,
        "title": title,
        "author_or_channel": f"{author} in r/{subreddit}",
        "published_at": format_dt(published_at),
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": "reddit thread",
        "capture_method": config.metadata.get("capture_method", "old.reddit rss / atom"),
        "normalization_method": "markdown_normalized",
        "translation_needed": "yes" if config.language == "en" else "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": "no",
        "verification_status": "community-signal",
        "summary": summary,
        "topic_tags": [f"subreddit:{subreddit.lower()}", "reddit-discussion", "user-feedback", "daily-top-rss"],
        "quote_candidates": [title, *content_lines[:2]],
        "distilled_body": distilled_body,
        "why_source_matters": "高热帖子正文能帮助判断真实用户问题、真实体验和外部对象入口。",
        "citation_reliability": "low-medium",
        "caveat": config.metadata.get(
            "caveat",
            "社区帖主要用于热度与问题观察；正式结论需要继续回链官网、产品页或一手资料。",
        ),
        "raw_body": raw_body,
        "normalized_excerpt": compact_snippet(excerpt_base, 360),
        "worth_clustering_with": external_url or "同主题的官网 / 产品页 / 博客",
        "possible_topic_directions": directions,
        "heat_hint": f"daily top rss / rank {rank}",
    }


def build_reddit_item(config: SourceConfig, post: dict[str, Any], captured_at: datetime, thread: list[dict[str, Any]]) -> dict[str, Any]:
    title = post.get("title") or "untitled reddit thread"
    permalink = f"https://www.reddit.com{post.get('permalink', '')}"
    external_url = post.get("url_overridden_by_dest") or post.get("url") or permalink
    comments = [compact_snippet(comment.get("body", ""), 180) for comment in thread if comment.get("body")]
    selftext = (post.get("selftext") or "").strip()
    excerpt_base = selftext or ("\n".join(comments[:2]) if comments else title)
    score = post.get("score", 0)
    num_comments = post.get("num_comments", 0)
    author = post.get("author") or "unknown"
    subreddit = config.metadata.get("subreddit", "reddit")
    created = datetime.fromtimestamp(post.get("created_utc", 0), tz=timezone.utc)
    item_key = str(post.get("id") or permalink)
    slug = slugify(title, fallback=item_key)
    raw_body = textwrap.dedent(
        f"""\
        # Raw Capture

        - `source_id`: `{config.source_id}`
        - `subreddit`: `r/{subreddit}`
        - `title`: `{title}`
        - `permalink`: {permalink}
        - `external_url`: {external_url}
        - `author`: `u/{author}`
        - `score`: `{score}`
        - `num_comments`: `{num_comments}`
        - `published_at`: `{format_dt(created)}`
        - `captured_at`: `{format_dt(captured_at)}`

        ## Selftext

        {selftext if selftext else "_no selftext_"}

        ## Top Comments

        {markdown_bullets(comments)}
        """
    ).strip() + "\n"
    distilled_body = distill_text(
        f"主题：{title}",
        f"楼主正文：{selftext}" if selftext else "",
        "高赞评论：\n" + "\n".join(f"- {comment}" for comment in comments[:3]) if comments else "",
        f"外部对象线索：{external_url}" if external_url and "reddit.com" not in external_url else "",
    )
    summary = (
        f"Reddit / r/{subreddit} 当日高赞讨论集中在“{title}”。当前热度约 {score} 分、{num_comments} 条评论；"
        "更适合判断真实用户问题、情绪和使用反馈，不适合直接当正式事实证据。"
    )
    normalized_excerpt = compact_snippet(excerpt_base, 360)
    topic_tags = [f"subreddit:{subreddit.lower()}", "reddit-discussion", "user-feedback"]
    if post.get("link_flair_text"):
        topic_tags.append(f"flair:{slugify(post['link_flair_text'], 'flair')}")
    directions = []
    if external_url and "reddit.com" not in external_url:
        directions.append(f"回链外部对象：{external_url}")
    directions.append("结合高赞评论判断是否能延伸成‘真实痛点 / 真实 workflow / 真实吐槽’题")
    return {
        "item_key": item_key,
        "packet_slug": f"{config.packet_prefix}_{slug}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": config.source_url,
        "canonical_url": permalink,
        "title": title,
        "author_or_channel": f"u/{author} in r/{subreddit}",
        "published_at": format_dt(created),
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": "reddit thread",
        "capture_method": "reddit-readonly / public-json",
        "normalization_method": "markdown_normalized",
        "translation_needed": "yes" if config.language == "en" else "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": "no",
        "verification_status": "community-signal",
        "summary": summary,
        "topic_tags": topic_tags,
        "quote_candidates": [title, *comments[:2]],
        "distilled_body": distilled_body,
        "why_source_matters": "高赞帖子 + 高赞评论能帮助判断真实用户问题、真实体验和情绪方向。",
        "citation_reliability": "low-medium",
        "caveat": "社区帖主要用于热度与问题观察；正式结论需要继续回链官网、产品页或一手资料。",
        "raw_body": raw_body,
        "normalized_excerpt": normalized_excerpt,
        "worth_clustering_with": external_url if external_url and "reddit.com" not in external_url else "同主题的官网 / 产品页 / 博客",
        "possible_topic_directions": directions,
        "heat_hint": "high heat + user signal",
    }


def collect_reddit_rss_items(config: SourceConfig, captured_at: datetime, limit: int) -> list[dict[str, Any]]:
    capture_url = config.source_url
    xml_text = fetch_reddit_rss_text(capture_url)
    root = ET.fromstring(xml_text)
    built_items: list[dict[str, Any]] = []
    for rank, entry in enumerate(root.findall("atom:entry", ATOM_NS), start=1):
        built_items.append(build_reddit_rss_item(config, entry, captured_at, rank=rank, capture_url=capture_url))
        if len(built_items) >= limit:
            break
    return built_items


def build_trend_hunt_item(config: SourceConfig, product: dict[str, Any], captured_at: datetime) -> dict[str, Any]:
    name = product.get("name") or "unnamed product"
    item_key = product.get("slug") or slugify(name, "product")
    slug = slugify(name, fallback=item_key)
    ph_url = product.get("phUrl") or config.source_url
    website_url = product.get("websiteUrl") or ph_url
    description = ""
    translations = product.get("translations") or []
    if translations and isinstance(translations, list):
        description = translations[0].get("description") or translations[0].get("tagline") or ""
    description = description or product.get("tagline") or ""
    query = config.metadata.get("query", "ai")
    raw_body = textwrap.dedent(
        f"""\
        # Raw Capture

        - `source_id`: `{config.source_id}`
        - `query`: `{query}`
        - `name`: `{name}`
        - `tagline`: `{product.get('tagline', '')}`
        - `category`: `{product.get('category', '')}`
        - `upvotes`: `{product.get('upvotes', '')}`
        - `hypeScore`: `{product.get('hypeScore', '')}`
        - `utilityScore`: `{product.get('utilityScore', '')}`
        - `product_hunt_url`: {ph_url}
        - `website_url`: {website_url}
        - `captured_at`: `{format_dt(captured_at)}`

        ## Description

        {description if description else "_no description_"}
        """
    ).strip() + "\n"
    distilled_body = distill_text(
        f"产品：{name}",
        f"一句话描述：{product.get('tagline', '')}" if product.get("tagline") else "",
        f"详细描述：{description}" if description else "",
        f"平台热度：upvotes={product.get('upvotes', 0)} / hypeScore={product.get('hypeScore', 0)} / utilityScore={product.get('utilityScore', 0)}",
        f"产品官网候选：{website_url}" if website_url else "",
    )
    summary = (
        f"Trend Hunt 在 query “{query}” 下返回了 {name}。该对象当前显示 upvotes {product.get('upvotes', 0)}、"
        f"hypeScore {product.get('hypeScore', 0)}、utilityScore {product.get('utilityScore', 0)}；"
        "它更适合作为产品发现入口，后续必须回链 Product Hunt 页与官网做事实核验。"
    )
    directions = [
        f"先回链 Product Hunt：{ph_url}",
        f"再回链官网 / demo：{website_url}",
        "继续找创始人账号、演示视频、GitHub 或文档，看是否值得长期跟踪",
    ]
    return {
        "item_key": item_key,
        "packet_slug": f"{config.packet_prefix}_{slug}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": config.source_url,
        "canonical_url": website_url or ph_url,
        "title": name,
        "author_or_channel": config.source_name,
        "published_at": f"{captured_at.strftime('%Y-%m-%d')} (capture day)",
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": "product discovery listing",
        "capture_method": "find-products / trend-hunt api",
        "normalization_method": "markdown_normalized",
        "translation_needed": "yes" if config.language == "en" else "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": "no",
        "verification_status": "mirror-signal",
        "summary": summary,
        "topic_tags": ["product-discovery", "product-hunt-mirror", slugify(query, "query")],
        "quote_candidates": [name, product.get("tagline", ""), compact_snippet(description, 150)],
        "distilled_body": distilled_body,
        "why_source_matters": "官方 Product Hunt topic 页受限时，Trend Hunt 可以稳定提供产品发现入口。",
        "citation_reliability": "low",
        "caveat": "第三方 mirror 只适合发现线索；正式写作时必须回链 Product Hunt 页、官网或创始人原话。",
        "raw_body": raw_body,
        "normalized_excerpt": compact_snippet(f"{product.get('tagline', '')} {description}", 360),
        "worth_clustering_with": ph_url,
        "possible_topic_directions": directions,
        "heat_hint": "early signal + product discovery",
    }


def build_rss_item(
    config: SourceConfig,
    item: ET.Element,
    captured_at: datetime,
    *,
    resolved_source_url: str | None = None,
) -> dict[str, Any] | None:
    dc_creator_tag = "{http://purl.org/dc/elements/1.1/}creator"
    title = (item.findtext("title") or "untitled rss item").strip()
    source_label = (item.findtext("source") or "").strip()
    required_source = config.metadata.get("required_source")
    if required_source and source_label != required_source:
        return None
    exclude_title_patterns = config.metadata.get("exclude_title_patterns", [])
    if exclude_title_patterns and matches_any_pattern(title, exclude_title_patterns):
        return None
    include_title_patterns = config.metadata.get("include_title_patterns", [])
    if include_title_patterns and not matches_any_pattern(title, include_title_patterns):
        return None
    link = (item.findtext("link") or config.source_url).strip()
    guid = (item.findtext("guid") or link).strip()
    pub_dt = parse_pubdate(item.findtext("pubDate"))
    max_age_days = config.metadata.get("max_age_days")
    if max_age_days is not None and pub_dt is not None:
        age_days = (captured_at.astimezone(timezone.utc) - pub_dt.astimezone(timezone.utc)).days
        if age_days > int(max_age_days):
            return None
    creator = (item.findtext(dc_creator_tag) or source_label or config.metadata.get("author_or_channel") or config.source_name).strip()
    description = strip_html(item.findtext("description") or "")
    categories = [compact_snippet(category.text or "", 40) for category in item.findall("category") if (category.text or "").strip()]
    haystack = " ".join([title, description, " ".join(categories)]).lower()
    if not passes_keyword_gate(config, haystack):
        return None
    slug = slugify(title, fallback=slugify(guid, "rss"))
    effective_source_url = resolved_source_url or config.source_url
    raw_body = textwrap.dedent(
        f"""\
        # Raw Capture

        - `source_id`: `{config.source_id}`
        - `title`: `{title}`
        - `link`: {link}
        - `guid`: `{guid}`
        - `author`: `{creator}`
        - `published_at`: `{format_dt(pub_dt)}`
        - `captured_at`: `{format_dt(captured_at)}`
        - `categories`: `{', '.join(categories) if categories else 'none'}`

        ## Description

        {description if description else "_no description_"}
        """
    ).strip() + "\n"
    distilled_body = distill_text(
        f"标题：{title}",
        f"摘要：{description}" if description else "",
        f"分类：{', '.join(categories)}" if categories else "",
        f"原始入口：{link}",
    )
    summary = config.metadata.get(
        "summary",
        f"{config.source_name} RSS 抓到新条目“{title}”。这类媒体稿通常适合作为融资、新产品、新公司与产业变动的入口，后续需要继续回链公司官网、融资公告或创始人原话。",
    )
    directions = config.metadata.get(
        "follow_up_hints",
        [
            "优先判断是否涉及新融资 / 新产品 / 新公司",
            "如涉及具体公司，继续补官网、创始人账号、Demo、社区讨论",
            "如果只是媒体解读，不要直接升级成最终结论",
        ],
    )
    topic_tags = config.metadata.get("topic_tags") or ["rss", "media-article", *[slugify(category, "category") for category in categories[:3]]]
    excerpt_base = description if description and description != "点击查看>" else title
    return {
        "item_key": guid,
        "packet_slug": f"{config.packet_prefix}_{slug}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.metadata.get("region", config.region),
        "source_url": effective_source_url,
        "canonical_url": link,
        "title": title,
        "author_or_channel": creator,
        "published_at": format_dt(pub_dt),
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": config.metadata.get("content_type", "media article"),
        "capture_method": config.metadata.get("capture_method", "rss"),
        "normalization_method": "markdown_normalized",
        "translation_needed": "yes" if config.language == "en" else "no",
        "status": "normalized",
        "signal_quality": config.metadata.get("signal_quality", config.signal_quality),
        "primary_source": config.metadata.get("primary_source", "no"),
        "verification_status": config.metadata.get("verification_status", "secondary-report"),
        "summary": summary,
        "topic_tags": topic_tags,
        "quote_candidates": [title, compact_snippet(description, 150)],
        "distilled_body": distilled_body,
        "why_source_matters": config.metadata.get(
            "why_source_matters",
            "TechCrunch AI 对新融资、新公司、新产品和大厂动态比较敏感，适合作为 daily financing / newco 入口。",
        ),
        "citation_reliability": config.metadata.get("citation_reliability", "medium"),
        "caveat": config.metadata.get(
            "caveat",
            "媒体稿可以作为入口，但正式写作时仍要回链公司官网、融资公告或官方博客交叉验证。",
        ),
        "raw_body": raw_body,
        "normalized_excerpt": compact_snippet(excerpt_base, 360),
        "worth_clustering_with": config.metadata.get("worth_clustering_with", "同公司官网 / 融资公告 / 创始人账号"),
        "possible_topic_directions": directions,
        "heat_hint": config.metadata.get("heat_hint", "media entrance"),
    }


def normalize_hn_external_url(raw_url: str | None, fallback_url: str) -> str:
    value = str(raw_url or "").strip()
    if not value:
        return fallback_url
    if value.startswith("item?id="):
        return f"https://news.ycombinator.com/{value}"
    if value.startswith("/item?id="):
        return f"https://news.ycombinator.com{value}"
    if value.startswith("http://"):
        return "https://" + value.removeprefix("http://")
    return value


def build_hn_frontpage_item(
    config: SourceConfig,
    *,
    captured_at: datetime,
    item_id: str,
    title: str,
    author: str,
    link: str,
    discussion_url: str,
    published_dt: datetime | None,
    points: Any,
    comment_count: Any,
    text_excerpt: str,
    source_url: str,
    capture_method: str,
    verification_status: str,
    rank: int | None = None,
) -> dict[str, Any] | None:
    cleaned_title = clean_search_text(title) or f"HN item {item_id}"
    cleaned_author = clean_search_text(author) or "unknown"
    normalized_link = normalize_hn_external_url(link, discussion_url)
    excerpt = clean_search_text(text_excerpt)
    haystack = " ".join([cleaned_title, normalized_link, discussion_url, excerpt]).lower()
    if not passes_keyword_gate(config, haystack):
        return None

    points_text = str(points).strip() if points not in (None, "") else "unknown"
    comments_text = str(comment_count).strip() if comment_count not in (None, "") else "unknown"
    source_domain = urlparse(normalized_link).netloc or "news.ycombinator.com"
    slug = slugify(f"{item_id}_{cleaned_title}", fallback=f"hn_{item_id}")
    rank_text = str(rank) if rank is not None else "unknown"
    raw_body = textwrap.dedent(
        f"""\
        # Raw Capture

        - `source_id`: `{config.source_id}`
        - `hn_item_id`: `{item_id}`
        - `title`: `{cleaned_title}`
        - `link`: {normalized_link}
        - `discussion_url`: {discussion_url}
        - `author`: `{cleaned_author}`
        - `published_at`: `{format_dt(published_dt)}`
        - `captured_at`: `{format_dt(captured_at)}`
        - `rank`: `{rank_text}`
        - `points`: `{points_text}`
        - `comment_count`: `{comments_text}`
        - `source_domain`: `{source_domain}`

        ## HN Context

        {excerpt if excerpt else "_no text excerpt_"}
        """
    ).strip() + "\n"
    distilled_body = distill_text(
        f"标题：{cleaned_title}",
        f"HN 讨论：{discussion_url}",
        f"原文：{normalized_link}",
        f"热度：{points_text} points / {comments_text} comments / rank {rank_text}",
        f"补充：{excerpt}" if excerpt else "",
    )
    summary = config.metadata.get(
        "summary",
        f"Hacker News 前台抓到条目“{cleaned_title}”。它适合作为 builder / startup / AI infra 话题的扩散验证层，不是最终事实源。",
    )
    topic_tags = unique_strings(
        [
            *(config.metadata.get("topic_tags") or []),
            "hn-frontpage",
            slugify(source_domain, "hn-site"),
        ]
    )
    quote_candidates = unique_strings(
        [
            cleaned_title,
            f"{points_text} points / {comments_text} comments",
            excerpt,
        ]
    )
    excerpt_base = f"{cleaned_title} / {points_text} points / {comments_text} comments / {source_domain}"
    return {
        "item_key": f"hn_{item_id}",
        "packet_slug": f"{config.packet_prefix}_{slug}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.metadata.get("region", config.region),
        "source_url": source_url,
        "canonical_url": normalized_link,
        "title": cleaned_title,
        "author_or_channel": cleaned_author,
        "published_at": format_dt(published_dt),
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": config.metadata.get("content_type", "trend article"),
        "capture_method": capture_method,
        "normalization_method": "markdown_normalized",
        "translation_needed": "yes" if config.language == "en" else "no",
        "status": "normalized",
        "signal_quality": config.metadata.get("signal_quality", config.signal_quality),
        "primary_source": config.metadata.get("primary_source", "partial"),
        "verification_status": verification_status,
        "summary": summary,
        "topic_tags": topic_tags,
        "quote_candidates": quote_candidates,
        "distilled_body": distilled_body,
        "why_source_matters": config.metadata.get(
            "why_source_matters",
            "HN 是 builder、开源、AI infra 与创业语境里最稳定的早期扩散层之一。",
        ),
        "citation_reliability": config.metadata.get("citation_reliability", "medium"),
        "caveat": config.metadata.get(
            "caveat",
            "HN 适合作为扩散与讨论验证层，正式写作时仍要回链原始事件页、产品页或官方博客。",
        ),
        "raw_body": raw_body,
        "normalized_excerpt": compact_snippet(excerpt if excerpt else excerpt_base, 360),
        "worth_clustering_with": "原始文章 / HN 评论区 / 产品页 / 官方账号",
        "possible_topic_directions": config.metadata.get("follow_up_hints", []),
        "heat_hint": config.metadata.get("heat_hint", "builder breakout signal"),
    }


def build_hn_item_from_algolia(
    config: SourceConfig,
    hit: dict[str, Any],
    captured_at: datetime,
    *,
    source_url: str,
    rank: int,
) -> dict[str, Any] | None:
    item_id = str(hit.get("objectID") or hit.get("story_id") or "").strip()
    if not item_id:
        return None
    discussion_url = f"https://news.ycombinator.com/item?id={item_id}"
    return build_hn_frontpage_item(
        config,
        captured_at=captured_at,
        item_id=item_id,
        title=str(hit.get("title") or hit.get("story_title") or "").strip(),
        author=str(hit.get("author") or "").strip(),
        link=str(hit.get("url") or hit.get("story_url") or "").strip(),
        discussion_url=discussion_url,
        published_dt=parse_iso_datetime(str(hit.get("created_at") or "").strip()),
        points=hit.get("points"),
        comment_count=hit.get("num_comments"),
        text_excerpt=str(hit.get("story_text") or hit.get("comment_text") or "").strip(),
        source_url=source_url,
        capture_method="hn algolia front_page api",
        verification_status="trend-board-api",
        rank=rank,
    )


def build_hn_item_from_firebase(
    config: SourceConfig,
    payload: dict[str, Any],
    captured_at: datetime,
    *,
    source_url: str,
    rank: int,
) -> dict[str, Any] | None:
    item_id = str(payload.get("id") or "").strip()
    if not item_id:
        return None
    discussion_url = f"https://news.ycombinator.com/item?id={item_id}"
    text_excerpt = str(payload.get("text") or "").strip()
    return build_hn_frontpage_item(
        config,
        captured_at=captured_at,
        item_id=item_id,
        title=str(payload.get("title") or "").strip(),
        author=str(payload.get("by") or "").strip(),
        link=str(payload.get("url") or "").strip(),
        discussion_url=discussion_url,
        published_dt=parse_unix_timestamp(payload.get("time")),
        points=payload.get("score"),
        comment_count=payload.get("descendants"),
        text_excerpt=text_excerpt,
        source_url=source_url,
        capture_method="hn firebase topstories fallback",
        verification_status="trend-board-api-fallback",
        rank=rank,
    )


def build_yc_launch_item(config: SourceConfig, hit: dict[str, Any], captured_at: datetime) -> dict[str, Any] | None:
    company = hit.get("company") or {}
    title = (hit.get("title") or "").strip()
    tagline = (hit.get("tagline") or "").strip()
    tags = company.get("tags") or []
    batch = company.get("batch") or "unknown batch"
    industry = company.get("industry") or ""
    relevance_text = " ".join([title, tagline, batch, industry, *tags]).lower()
    keywords = config.metadata.get("include_keywords", [])
    if keywords and not any(keyword.lower() in relevance_text for keyword in keywords):
        return None
    company_name = company.get("name") or "unknown company"
    company_url = company.get("url") or hit.get("search_path") or config.source_url
    launch_url = hit.get("search_path") or config.source_url
    created_at = parse_iso_datetime(hit.get("created_at"))
    slug = slugify(company_name + "_" + title, fallback=str(hit.get("id", "yc")))
    raw_body = textwrap.dedent(
        f"""\
        # Raw Capture

        - `source_id`: `{config.source_id}`
        - `launch_title`: `{title}`
        - `company_name`: `{company_name}`
        - `company_url`: {company_url}
        - `launch_url`: {launch_url}
        - `batch`: `{batch}`
        - `industry`: `{industry}`
        - `tags`: `{', '.join(tags) if tags else 'none'}`
        - `vote_count`: `{hit.get('total_vote_count', 0)}`
        - `published_at`: `{format_dt(created_at)}`
        - `captured_at`: `{format_dt(captured_at)}`

        ## Tagline

        {tagline if tagline else "_no tagline_"}
        """
    ).strip() + "\n"
    distilled_body = distill_text(
        f"Launch 标题：{title}",
        f"公司：{company_name}",
        f"一句话：{tagline}" if tagline else "",
        f"Batch / 行业：{batch} / {industry}" if industry else f"Batch：{batch}",
        f"标签：{', '.join(tags)}" if tags else "",
        f"官网候选：{company_url}" if company_url else "",
    )
    summary = (
        f"YC Launches 抓到 {company_name} 的新 launch：{title}。当前 batch 为 {batch}，票数 {hit.get('total_vote_count', 0)}；"
        "它适合作为新项目 / 新业务 / 创始团队的发现入口，后续继续回链官网、创始人账号与 demo。"
    )
    directions = [
        f"继续看官网 / 产品页：{company_url}",
        f"继续看 launch 页面：{launch_url}",
        "补创始人账号、产品 demo、社区讨论，判断是否值得升格成正式选题对象",
    ]
    return {
        "item_key": str(hit.get("id") or hit.get("slug") or launch_url),
        "packet_slug": f"{config.packet_prefix}_{slug}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": config.source_url,
        "canonical_url": launch_url,
        "title": title,
        "author_or_channel": f"{company_name} / YC Launches",
        "published_at": format_dt(created_at),
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": "startup launch listing",
        "capture_method": "yc launches json",
        "normalization_method": "markdown_normalized",
        "translation_needed": "yes" if config.language == "en" else "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": "partial",
        "verification_status": "official-platform-listing",
        "summary": summary,
        "topic_tags": ["yc-launches", "startup-launch", *[slugify(tag, "tag") for tag in tags[:4]]],
        "quote_candidates": [title, tagline, company_name],
        "distilled_body": distilled_body,
        "why_source_matters": "YC Launches 能稳定暴露新项目、新产品与新商业模式，是融资 / newco 线的重要早期入口。",
        "citation_reliability": "medium",
        "caveat": "Launch 页证明的是‘YC 公开发射的新对象’，不等于融资事实或产品验证，需要继续回链官网与其他证据。",
        "raw_body": raw_body,
        "normalized_excerpt": compact_snippet(f"{title}. {tagline}. Batch: {batch}. Industry: {industry}. Tags: {', '.join(tags)}", 360),
        "worth_clustering_with": company_url,
        "possible_topic_directions": directions,
        "heat_hint": "newco + product launch entrance",
    }


def build_youtube_item(
    config: SourceConfig,
    entry: ET.Element,
    captured_at: datetime,
    *,
    resolved_source_url: str,
) -> dict[str, Any]:
    title = (entry.findtext("atom:title", "", ATOM_NS) or "untitled youtube video").strip()
    video_id = (entry.findtext("yt:videoId", "", ATOM_NS) or "").strip()
    channel_id = (entry.findtext("yt:channelId", "", ATOM_NS) or "").strip()
    author = (entry.findtext("atom:author/atom:name", "", ATOM_NS) or config.source_name).strip()
    link = ""
    for link_node in entry.findall("atom:link", ATOM_NS):
        href = str(link_node.attrib.get("href") or "").strip()
        rel = str(link_node.attrib.get("rel") or "alternate").strip()
        if href and rel in {"alternate", ""}:
            link = href
            break
    if not link and video_id:
        link = f"https://www.youtube.com/watch?v={video_id}"
    published_at = parse_iso_datetime(entry.findtext("atom:published", "", ATOM_NS))
    updated_at = parse_iso_datetime(entry.findtext("atom:updated", "", ATOM_NS))
    description = strip_html(entry.findtext("media:group/media:description", "", ATOM_NS) or "")
    raw_body = textwrap.dedent(
        f"""\
        # Raw Capture

        - `source_id`: `{config.source_id}`
        - `title`: `{title}`
        - `link`: {link}
        - `video_id`: `{video_id}`
        - `channel_id`: `{channel_id}`
        - `author_or_channel`: `{author}`
        - `published_at`: `{format_dt(published_at)}`
        - `updated_at`: `{format_dt(updated_at)}`
        - `captured_at`: `{format_dt(captured_at)}`

        ## Description

        {description if description else "_no description_"}
        """
    ).strip() + "\n"
    distilled_body = distill_text(
        f"视频：{title}",
        f"频道：{author}",
        f"描述：{description}" if description else "",
        f"视频地址：{link}" if link else "",
    )
    thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" if video_id else ""
    return {
        "item_key": video_id or link or title,
        "packet_slug": f"{config.packet_prefix}_{slugify(title, video_id or 'youtube')}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": resolved_source_url,
        "canonical_url": link or resolved_source_url,
        "title": title,
        "author_or_channel": author,
        "published_at": format_dt(published_at or updated_at),
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": "video",
        "capture_method": "youtube-feed / atom",
        "normalization_method": "markdown_normalized",
        "translation_needed": "yes" if config.language == "en" else "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": config.metadata.get("primary_source", "partial"),
        "verification_status": config.metadata.get("verification_status", "channel-video"),
        "summary": f"{config.source_name} 抓到新视频“{title}”。视频源适合保留原始 demo、产品解释和访谈措辞，后续要继续回链官网、文档或评论反馈。",
        "topic_tags": config.metadata.get("topic_tags", ["youtube", "video"]),
        "thumbnail_url": thumbnail_url,
        "quote_candidates": [title, compact_snippet(description, 180)],
        "distilled_body": distilled_body,
        "why_source_matters": config.metadata.get(
            "why_source_matters",
            "视频能保留演示过程、口头表述和视觉证据，适合作为产品 / workflow / 观点的原始入口。",
        ),
        "citation_reliability": config.metadata.get("citation_reliability", "medium"),
        "caveat": config.metadata.get(
            "caveat",
            "频道视频是高价值入口，但仍需区分官方发布、采访转述和个人解读，不能自动当成最终事实结论。",
        ),
        "raw_body": raw_body,
        "normalized_excerpt": compact_snippet(description or title, 360),
        "worth_clustering_with": "同主题官网 / 文档 / transcript / 评论区反馈",
        "possible_topic_directions": config.metadata.get(
            "follow_up_hints",
            [
                "继续找 transcript、产品页和配套文档",
                "如是访谈，补创始人账号和官网对象链",
            ],
        ),
        "heat_hint": config.metadata.get("heat_hint", "video signal"),
    }


def extract_youtube_video_id(video_url: str) -> str:
    parsed = urlparse(video_url)
    query_id = parse_qs(parsed.query).get("v", [])
    if query_id and query_id[0]:
        return query_id[0].strip()
    if parsed.path.startswith("/watch/"):
        return parsed.path.rsplit("/", 1)[-1].strip()
    return ""


def extract_youtube_stats(lines: list[str], start_index: int) -> tuple[str, datetime | None]:
    for line in lines[start_index : start_index + 8]:
        cleaned = clean_markdown_line(line)
        if not cleaned:
            continue
        if "views" in cleaned.lower() or "ago" in cleaned.lower():
            time_match = re.search(
                r"((?:streamed|premiered|live)?\s*\d+\s+(?:minute|hour|day|week|month|year)s?\s+ago)",
                cleaned,
                re.I,
            )
            relative_dt = parse_relative_time(time_match.group(1), now_cn()) if time_match else None
            return cleaned, relative_dt
    return "", None


def build_youtube_jina_item(
    config: SourceConfig,
    *,
    title: str,
    link: str,
    video_id: str,
    author: str,
    stats_line: str,
    published_at: datetime | None,
    captured_at: datetime,
    capture_url: str,
) -> dict[str, Any]:
    normalized_title = clean_search_text(title) or "untitled youtube video"
    normalized_link = link.replace("http://", "https://").strip()
    raw_body = textwrap.dedent(
        f"""\
        # Raw Capture

        - `source_id`: `{config.source_id}`
        - `title`: `{normalized_title}`
        - `link`: {normalized_link}
        - `video_id`: `{video_id or 'unknown'}`
        - `author_or_channel`: `{author}`
        - `capture_url`: {capture_url}
        - `stats_line`: `{stats_line or 'unknown'}`
        - `published_at`: `{format_dt(published_at)}`
        - `captured_at`: `{format_dt(captured_at)}`
        """
    ).strip() + "\n"
    distilled_body = distill_text(
        f"视频：{normalized_title}",
        f"频道：{author}",
        f"热度线索：{stats_line}" if stats_line else "",
        f"视频地址：{normalized_link}",
    )
    summary = (
        f"{config.source_name} 频道页抓到新视频“{normalized_title}”。"
        "Jina 频道快照现在可稳定保留标题、链接与相对发布时间，适合作为视频线索的硬成功入口。"
    )
    normalized_excerpt = compact_snippet(" / ".join(part for part in [normalized_title, stats_line] if part), 360)
    thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" if video_id else ""
    return {
        "item_key": video_id or normalized_link or normalized_title,
        "packet_slug": f"{config.packet_prefix}_{slugify(normalized_title, video_id or 'youtube')}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": config.source_url,
        "canonical_url": normalized_link or config.source_url,
        "title": normalized_title,
        "author_or_channel": author,
        "published_at": format_dt(published_at),
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": "video",
        "capture_method": "jina-reader / youtube channel page",
        "normalization_method": "markdown_normalized",
        "translation_needed": "yes" if config.language == "en" else "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": config.metadata.get("primary_source", "partial"),
        "verification_status": config.metadata.get("verification_status", "channel-video"),
        "summary": summary,
        "topic_tags": config.metadata.get("topic_tags", ["youtube", "video"]),
        "thumbnail_url": thumbnail_url,
        "quote_candidates": [normalized_title, stats_line],
        "distilled_body": distilled_body,
        "why_source_matters": config.metadata.get(
            "why_source_matters",
            "视频能保留演示过程、口头表述和视觉证据，适合作为产品 / workflow / 观点的原始入口。",
        ),
        "citation_reliability": config.metadata.get("citation_reliability", "medium"),
        "caveat": config.metadata.get(
            "caveat",
            "频道视频是高价值入口，但仍需区分官方发布、采访转述和个人解读，不能自动当成最终事实结论。",
        ),
        "raw_body": raw_body,
        "normalized_excerpt": normalized_excerpt or normalized_title,
        "worth_clustering_with": "同主题官网 / 文档 / transcript / 评论区反馈",
        "possible_topic_directions": config.metadata.get(
            "follow_up_hints",
            [
                "继续找 transcript、产品页和配套文档",
                "如是访谈，补创始人账号和官网对象链",
            ],
        ),
        "heat_hint": stats_line or config.metadata.get("heat_hint", "video signal"),
    }


def youtube_watch_url(video_renderer: dict[str, Any], video_id: str) -> str:
    navigation_endpoint = video_renderer.get("navigationEndpoint") or {}
    if isinstance(navigation_endpoint, dict):
        watch_endpoint = navigation_endpoint.get("watchEndpoint") or {}
        if isinstance(watch_endpoint, dict):
            candidate_video_id = clean_search_text(str(watch_endpoint.get("videoId") or "")).strip()
            if candidate_video_id:
                return f"https://www.youtube.com/watch?v={candidate_video_id}"
    if video_id:
        return f"https://www.youtube.com/watch?v={video_id}"
    return ""


def extract_youtube_channel_name(html: str, initial_data: dict[str, Any], fallback: str) -> str:
    metadata = initial_data.get("metadata") or {}
    if isinstance(metadata, dict):
        renderer = metadata.get("channelMetadataRenderer") or {}
        if isinstance(renderer, dict):
            title = clean_search_text(str(renderer.get("title") or "")).strip()
            if title:
                return title
    meta_match = re.search(r'<meta itemprop="name" content="([^"]+)">', html)
    if meta_match:
        title = clean_search_text(meta_match.group(1)).strip()
        if title:
            return title
    return fallback


def build_youtube_html_item(
    config: SourceConfig,
    video_renderer: dict[str, Any],
    captured_at: datetime,
    *,
    channel_name: str,
) -> dict[str, Any] | None:
    video_id = clean_search_text(str(video_renderer.get("videoId") or "")).strip()
    title = extract_text_runs(video_renderer.get("title"))
    if not title:
        return None
    link = youtube_watch_url(video_renderer, video_id)
    description = extract_text_runs(video_renderer.get("descriptionSnippet"))
    published_text = extract_text_runs(video_renderer.get("publishedTimeText"))
    view_count = extract_text_runs(video_renderer.get("viewCountText")) or extract_text_runs(video_renderer.get("shortViewCountText"))
    length_text = extract_text_runs(video_renderer.get("lengthText"))
    published_at = parse_relative_time(published_text, captured_at)
    stats_parts = [part for part in [published_text, view_count, length_text] if part]
    stats_line = " / ".join(stats_parts)
    raw_body = textwrap.dedent(
        f"""\
        # Raw Capture

        - `source_id`: `{config.source_id}`
        - `title`: `{title}`
        - `link`: {link or config.source_url}
        - `video_id`: `{video_id or 'unknown'}`
        - `channel`: `{channel_name}`
        - `published_text`: `{published_text or 'unknown'}`
        - `published_at`: `{format_dt(published_at)}`
        - `captured_at`: `{format_dt(captured_at)}`
        - `view_count`: `{view_count or 'unknown'}`
        - `duration`: `{length_text or 'unknown'}`

        ## Description

        {description if description else "_no description_"}
        """
    ).strip() + "\n"
    distilled_body = distill_text(
        f"视频：{title}",
        f"频道：{channel_name}",
        f"热度线索：{stats_line}" if stats_line else "",
        f"描述：{description}" if description else "",
        f"视频地址：{link}" if link else "",
    )
    summary = (
        f"{config.source_name} 频道页直连抓到新视频“{title}”。"
        "当前直接解析频道页内的 ytInitialData，避免 Jina 波动对视频 lane 造成整组失真。"
    )
    normalized_excerpt = compact_snippet(" / ".join(part for part in [title, stats_line, description] if part), 360)
    thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" if video_id else ""
    return {
        "item_key": video_id or link or title,
        "packet_slug": f"{config.packet_prefix}_{slugify(title, video_id or 'youtube')}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": config.source_url,
        "canonical_url": link or config.source_url,
        "title": title,
        "author_or_channel": channel_name,
        "published_at": format_dt(published_at),
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": "video",
        "capture_method": "direct youtube html / ytInitialData",
        "normalization_method": "html_json_normalized",
        "translation_needed": "yes" if config.language == "en" else "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": config.metadata.get("primary_source", "partial"),
        "verification_status": config.metadata.get("verification_status", "channel-video"),
        "summary": summary,
        "topic_tags": config.metadata.get("topic_tags", ["youtube", "video"]),
        "thumbnail_url": thumbnail_url,
        "quote_candidates": unique_strings([title, stats_line, compact_snippet(description, 180)]),
        "distilled_body": distilled_body,
        "why_source_matters": config.metadata.get(
            "why_source_matters",
            "视频能保留演示过程、口头表述和视觉证据，适合作为产品 / workflow / 观点的原始入口。",
        ),
        "citation_reliability": config.metadata.get("citation_reliability", "medium"),
        "caveat": config.metadata.get(
            "caveat",
            "频道视频是高价值入口，但仍需区分官方发布、采访转述和个人解读，不能自动当成最终事实结论。",
        ),
        "raw_body": raw_body,
        "normalized_excerpt": normalized_excerpt or title,
        "worth_clustering_with": "同主题官网 / 文档 / transcript / 评论区反馈",
        "possible_topic_directions": config.metadata.get(
            "follow_up_hints",
            [
                "继续找 transcript、产品页和配套文档",
                "如是访谈，补创始人账号和官网对象链",
            ],
        ),
        "heat_hint": stats_line or config.metadata.get("heat_hint", "video signal"),
    }


def collect_youtube_html_items(config: SourceConfig, captured_at: datetime, limit: int) -> list[dict[str, Any]]:
    html = fetch_html_page(config.source_url, referer="https://www.youtube.com/")
    initial_data = extract_json_object_after_marker(html, "var ytInitialData = ")
    channel_name = extract_youtube_channel_name(html, initial_data, config.source_name)
    built_items: list[dict[str, Any]] = []
    seen_video_ids: set[str] = set()
    for video_renderer in iter_nested_dict_values(initial_data, "videoRenderer"):
        video_id = clean_search_text(str(video_renderer.get("videoId") or "")).strip()
        if not video_id or video_id in seen_video_ids:
            continue
        built = build_youtube_html_item(
            config,
            video_renderer,
            captured_at,
            channel_name=channel_name,
        )
        if built is None:
            continue
        built_items.append(built)
        seen_video_ids.add(video_id)
        if len(built_items) >= limit:
            break
    if not built_items:
        raise RuntimeError(f"No videos extracted from YouTube channel HTML: {config.source_url}")
    return built_items


def collect_youtube_jina_items(config: SourceConfig, captured_at: datetime, limit: int) -> list[dict[str, Any]]:
    capture_url = resolve_fetch_url(config, "capture_url")
    raw_text = fetch_text(capture_url)
    payload = parse_jina_payload(raw_text)
    channel_name = payload["page_title"] or config.source_name
    body = payload["body"]
    lines = body.splitlines()
    built_items: list[dict[str, Any]] = []
    seen_video_ids: set[str] = set()
    pattern = re.compile(
        r"^###\s+\[([^\]]+)\]\((https?://www\.youtube\.com/watch\?v=[^)\s]+)(?:\s+\"([^\"]+)\")?\)",
        re.I,
    )
    for index, line in enumerate(lines):
        match = pattern.search(line.strip())
        if not match:
            continue
        raw_title = match.group(3) or match.group(1)
        title = clean_markdown_line(raw_title)
        link = match.group(2).replace("http://", "https://").strip()
        video_id = extract_youtube_video_id(link)
        if not title or not video_id or video_id in seen_video_ids:
            continue
        stats_line, relative_dt = extract_youtube_stats(lines, index + 1)
        built_items.append(
            build_youtube_jina_item(
                config,
                title=title,
                link=link,
                video_id=video_id,
                author=channel_name,
                stats_line=stats_line,
                published_at=relative_dt,
                captured_at=captured_at,
                capture_url=capture_url,
            )
        )
        seen_video_ids.add(video_id)
        if len(built_items) >= limit:
            break
    return built_items


def build_bilibili_video_item(config: SourceConfig, video: dict[str, Any], captured_at: datetime) -> dict[str, Any] | None:
    title = str(video.get("title") or "").strip()
    description = str(video.get("desc") or "").strip()
    owner = video.get("owner") or {}
    owner_name = str(owner.get("name") or "").strip()
    bvid = str(video.get("bvid") or "").strip()
    aid = str(video.get("aid") or "").strip()
    category = str(video.get("tname") or "").strip()
    rcmd_reason = video.get("rcmd_reason") or {}
    reason_text = str(rcmd_reason.get("content") or "").strip()
    haystack = " ".join([title, description, owner_name, category, reason_text]).lower()
    if not passes_keyword_gate(config, haystack):
        return None
    stats = video.get("stat") or {}
    thumbnail_url = str(video.get("pic") or "").strip()
    published_at = datetime.fromtimestamp(int(video.get("pubdate") or 0), tz=timezone.utc)
    link = f"https://www.bilibili.com/video/{bvid}" if bvid else config.source_url
    raw_body = textwrap.dedent(
        f"""\
        # Raw Capture

        - `source_id`: `{config.source_id}`
        - `title`: `{title}`
        - `link`: {link}
        - `bvid`: `{bvid}`
        - `aid`: `{aid}`
        - `uploader`: `{owner_name}`
        - `category`: `{category}`
        - `published_at`: `{format_dt(published_at)}`
        - `captured_at`: `{format_dt(captured_at)}`
        - `view`: `{stats.get('view', 0)}`
        - `like`: `{stats.get('like', 0)}`
        - `reply`: `{stats.get('reply', 0)}`
        - `share`: `{stats.get('share', 0)}`
        - `rank_reason`: `{reason_text}`

        ## Description

        {description if description else "_no description_"}
        """
    ).strip() + "\n"
    distilled_body = distill_text(
        f"视频：{title}",
        f"UP 主：{owner_name}" if owner_name else "",
        f"分类：{category}" if category else "",
        f"热度：播放 {stats.get('view', 0)} / 点赞 {stats.get('like', 0)} / 评论 {stats.get('reply', 0)} / 分享 {stats.get('share', 0)}",
        f"描述：{description}" if description else "",
        f"视频地址：{link}",
    )
    return {
        "item_key": bvid or aid or title,
        "packet_slug": f"{config.packet_prefix}_{slugify(title, bvid or 'bilibili')}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": config.source_url,
        "canonical_url": link,
        "title": title,
        "author_or_channel": owner_name or config.source_name,
        "published_at": format_dt(published_at),
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": "video",
        "capture_method": "bilibili popular api",
        "normalization_method": "markdown_normalized",
        "translation_needed": "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": "partial",
        "verification_status": "video-ranking-signal",
        "summary": f"B站热门榜抓到 AI 相关视频“{title}”。它适合作为中文视频热榜入口，帮助判断 AI 话题是否开始向大众用户扩散，并识别可被重构的话题切口。",
        "topic_tags": config.metadata.get("topic_tags", ["bilibili", "video-ranking"]),
        "thumbnail_url": thumbnail_url,
        "quote_candidates": [title, compact_snippet(description, 180), reason_text],
        "distilled_body": distilled_body,
        "why_source_matters": config.metadata.get(
            "why_source_matters",
            "B站热视频能补中文视频语境的传播型话题，但需要关键词过滤和后续事实回链。",
        ),
        "citation_reliability": config.metadata.get("citation_reliability", "low-medium"),
        "caveat": "热视频代表传播强度，不等于事实强度；正式写作仍需回链原始事件、产品页或官方口径。",
        "raw_body": raw_body,
        "normalized_excerpt": compact_snippet(description or title, 360),
        "worth_clustering_with": "视频描述 / 评论区 / 原始事件页 / 作者主页",
        "possible_topic_directions": config.metadata.get("follow_up_hints", []),
        "heat_hint": reason_text or "bilibili popular",
    }


def build_jina_snapshot_item(
    config: SourceConfig,
    raw_text: str,
    captured_at: datetime,
    *,
    capture_url: str,
) -> dict[str, Any] | None:
    payload = parse_jina_payload(raw_text)
    body = payload["body"]
    mode = str(config.metadata.get("snapshot_mode") or "generic").strip()
    line_limit = int(config.metadata.get("snapshot_line_limit") or 12)
    snapshot_lines = extract_snapshot_lines(config, body, limit=line_limit)
    if mode != "x_profile" and config.metadata.get("snapshot_prefer_link_texts"):
        link_text_limit = int(config.metadata.get("snapshot_link_text_limit") or max(line_limit, 8))
        snapshot_lines = unique_strings(extract_snapshot_link_texts(config, body, limit=link_text_limit) + snapshot_lines)[:line_limit]
    snapshot_links = extract_snapshot_links(config, body, limit=int(config.metadata.get("snapshot_link_limit") or 6))
    if not snapshot_lines:
        return None
    page_title = clean_search_text(str(config.metadata.get("page_title_override") or "")) or payload["page_title"] or config.source_name
    source_url = payload["source_url"] or config.source_url
    published_dt = parse_jina_published_at(payload["published_raw"])
    if mode == "x_profile":
        lead_line = snapshot_lines[0]
        author_name = config.source_name
        quote_candidates = unique_strings(snapshot_lines[:4])
        title = compact_snippet(f"{lead_line} recent X signal snapshot", 120)
        summary = (
            f"{config.source_name} 的 X profile 通过 Jina 抓到近期高信号片段。"
            "它适合作为观点、快讯和 builder 社区讨论的快信号层。"
        )
        distilled_body = distill_text(
            f"账号：{config.source_name}",
            "近期高信号片段：\n" + "\n".join(f"- {line}" for line in snapshot_lines[:6]),
            "可继续回链对象：\n" + "\n".join(f"- {link}" for link in snapshot_links[:4]) if snapshot_links else "",
        )
        normalized_excerpt = compact_snippet(" / ".join(snapshot_lines[:3]), 360)
        worth = " / ".join(snapshot_links[:3]) if snapshot_links else "帖子外链 / 官方博客 / repo / docs"
        content_type = "profile + post excerpts"
        capture_method = "jina-reader / x-profile snapshot"
    else:
        author_name = config.source_name
        quote_candidates = unique_strings(snapshot_lines[:3])
        title = compact_snippet(f"{page_title} snapshot", 120)
        summary = (
            f"{config.source_name} 当前页通过 Jina 抓到近期可读内容快照。"
            "它适合作为官方更新、专家观察或中文传播层的入口快照。"
        )
        distilled_body = distill_text(
            f"页面：{page_title}",
            "近期内容摘录：\n" + "\n".join(f"- {line}" for line in snapshot_lines[:6]),
            "可继续回链对象：\n" + "\n".join(f"- {link}" for link in snapshot_links[:4]) if snapshot_links else "",
        )
        normalized_excerpt = compact_snippet(" / ".join(snapshot_lines[:3]), 360)
        worth = " / ".join(snapshot_links[:3]) if snapshot_links else "单篇原文 / 官方博客 / repo / docs"
        content_type = config.metadata.get("content_type", "web page snapshot")
        capture_method = "jina-reader / page snapshot"
    raw_body = (
        "# Raw Capture\n\n"
        f"- `source_id`: `{config.source_id}`\n"
        f"- `page_title`: `{page_title}`\n"
        f"- `source_url`: {source_url}\n"
        f"- `capture_url`: {capture_url}\n"
        f"- `published_raw`: `{payload['published_raw'] or 'unknown'}`\n"
        f"- `published_at`: `{format_dt(published_dt)}`\n"
        f"- `captured_at`: `{format_dt(captured_at)}`\n\n"
        "## Snapshot Lines\n\n"
        + ("\n".join(f"- {line}" for line in snapshot_lines[:10]) if snapshot_lines else "- none")
        + "\n\n## Snapshot Links\n\n"
        + ("\n".join(f"- {link}" for link in snapshot_links) if snapshot_links else "- none")
        + "\n"
    )
    return {
        "item_key": f"{config.source_id}:{normalize_match_text(snapshot_lines[0]) or slugify(page_title, config.source_id)}",
        "packet_slug": f"{config.packet_prefix}_{slugify(page_title, config.source_id)}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": config.source_url,
        "canonical_url": config.source_url,
        "title": title,
        "author_or_channel": author_name,
        "published_at": format_dt(published_dt),
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": content_type,
        "capture_method": capture_method,
        "normalization_method": "markdown_normalized",
        "translation_needed": "yes" if config.language == "en" else "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": config.metadata.get("primary_source", "partial"),
        "verification_status": config.metadata.get("verification_status", "snapshot-signal"),
        "summary": summary,
        "topic_tags": config.metadata.get("topic_tags", ["jina-snapshot"]),
        "quote_candidates": quote_candidates,
        "distilled_body": distilled_body,
        "why_source_matters": config.metadata.get(
            "why_source_matters",
            "Jina snapshot 能把难直连的站点先转成可追踪的入口层快照。",
        ),
        "citation_reliability": config.metadata.get("citation_reliability", "medium"),
        "caveat": config.metadata.get(
            "caveat",
            "这是入口快照层，不等于最终事实结论；正式引用仍需回链单篇原文和一手对象。",
        ),
        "raw_body": raw_body,
        "normalized_excerpt": normalized_excerpt,
        "worth_clustering_with": worth,
        "possible_topic_directions": config.metadata.get("follow_up_hints", []),
        "heat_hint": config.metadata.get("heat_hint", "snapshot signal"),
    }


def collect_jina_snapshot_items(config: SourceConfig, captured_at: datetime, limit: int) -> list[dict[str, Any]]:
    capture_url = resolve_fetch_url(config, "capture_url")
    raw_text = fetch_text(capture_url)
    multi_items = build_jina_snapshot_entry_items(
        config,
        raw_text,
        captured_at,
        capture_url=capture_url,
        limit=limit,
    )
    if multi_items:
        return multi_items[:limit]
    if bool(config.metadata.get("snapshot_disable_single_fallback")):
        return []
    built = build_jina_snapshot_item(config, raw_text, captured_at, capture_url=capture_url)
    return [built] if built is not None else []


def parse_frontmatter_and_body(raw_text: str) -> tuple[dict[str, Any], str]:
    if raw_text.startswith("---\n"):
        parts = raw_text.split("\n---\n", 1)
        if len(parts) == 2:
            frontmatter_raw = parts[0].removeprefix("---\n")
            body = parts[1]
            try:
                frontmatter = yaml.safe_load(frontmatter_raw) or {}
            except Exception:
                frontmatter = {}
            return frontmatter if isinstance(frontmatter, dict) else {}, body.strip()
    return {}, raw_text.strip()


def extract_markdown_excerpt(body: str, limit: int = 4) -> list[str]:
    lines: list[str] = []
    for raw_line in body.splitlines():
        cleaned = clean_markdown_line(raw_line)
        if not cleaned:
            continue
        if cleaned.startswith(("Title:", "URL Source:", "Published Time:")):
            continue
        if cleaned.lower() in {"table of contents", "contents"}:
            continue
        if re.match(r"^(#|##|###)\s*", raw_line.strip()):
            continue
        if cleaned in lines:
            continue
        lines.append(cleaned)
        if len(lines) >= limit:
            break
    return lines


def github_api_headers() -> dict[str, str]:
    return {
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
    }


def fetch_github_contents_text(owner: str, repo: str, path: str, ref: str) -> tuple[str, str]:
    capture_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={ref}"
    payload = fetch_json_via_curl(capture_url, headers=github_api_headers())
    encoded_content = str(payload.get("content") or "").strip()
    if not encoded_content:
        raise RuntimeError(f"GitHub contents missing content: {capture_url}")
    raw_text = base64.b64decode(encoded_content).decode("utf-8", "replace")
    return raw_text, capture_url


def collect_hf_blog_repo_items(config: SourceConfig, captured_at: datetime, limit: int) -> list[dict[str, Any]]:
    capture_url = resolve_fetch_url(config, "capture_url")
    payload = fetch_json_via_curl(capture_url, headers=github_api_headers())
    encoded_content = str(payload.get("content") or "").strip()
    if not encoded_content:
        raise RuntimeError(f"Hugging Face blog registry missing content: {capture_url}")
    registry_raw = base64.b64decode(encoded_content).decode("utf-8", "replace")
    registry_items = yaml.safe_load(registry_raw)
    if not isinstance(registry_items, list):
        raise RuntimeError("Hugging Face blog registry is not a list")

    ranked_posts: list[tuple[datetime, dict[str, Any]]] = []
    for item in registry_items:
        if not isinstance(item, dict):
            continue
        slug = str(item.get("local") or "").strip()
        if not slug:
            continue
        published_dt = parse_hf_blog_date(str(item.get("date") or "").strip())
        if published_dt is None:
            continue
        ranked_posts.append((published_dt, item))
    ranked_posts.sort(key=lambda pair: pair[0], reverse=True)

    built_items: list[dict[str, Any]] = []
    repo_owner = str(config.metadata.get("repo_owner") or "huggingface").strip()
    repo_name = str(config.metadata.get("repo_name") or "blog").strip()
    repo_ref = str(config.metadata.get("repo_ref") or "main").strip()

    for published_dt, item in ranked_posts[:limit]:
        slug = str(item.get("local") or "").strip()
        raw_text = ""
        raw_capture_url = ""
        for candidate_path in (f"{slug}.md", f"{slug}.mdx"):
            try:
                raw_text, raw_capture_url = fetch_github_contents_text(repo_owner, repo_name, candidate_path, repo_ref)
                break
            except Exception:
                continue
        if not raw_text:
            raise RuntimeError(f"Hugging Face blog markdown not found for slug: {slug}")
        frontmatter, body = parse_frontmatter_and_body(raw_text)
        title = clean_search_text(str(frontmatter.get("title") or "").strip())
        if not title:
            heading_match = re.search(r"^#\s+(.+)$", body, re.M)
            title = clean_search_text(heading_match.group(1)) if heading_match else slug.replace("-", " ")
        excerpt_lines = extract_markdown_excerpt(body, limit=4)
        authors_raw = frontmatter.get("authors") or []
        authors: list[str] = []
        for author in authors_raw if isinstance(authors_raw, list) else []:
            if isinstance(author, dict):
                user = clean_search_text(str(author.get("user") or author.get("name") or "").strip())
                if user:
                    authors.append(user)
            else:
                value = clean_search_text(str(author).strip())
                if value:
                    authors.append(value)
        tags = [clean_search_text(str(tag)) for tag in (item.get("tags") or []) if clean_search_text(str(tag))]
        canonical_url = f"{config.source_url.rstrip('/')}/{slug}"
        raw_body = textwrap.dedent(
            f"""\
            # Raw Capture

            - `source_id`: `{config.source_id}`
            - `title`: `{title}`
            - `canonical_url`: {canonical_url}
            - `registry_capture_url`: {capture_url}
            - `raw_markdown_capture_url`: {raw_capture_url}
            - `published_at`: `{format_dt(published_dt)}`
            - `captured_at`: `{format_dt(captured_at)}`
            - `authors`: `{', '.join(authors) if authors else 'unknown'}`
            - `tags`: `{', '.join(tags) if tags else 'none'}`

            ## Excerpt

            {markdown_bullets(excerpt_lines)}
            """
        ).strip() + "\n"
        distilled_body = distill_text(
            f"文章：{title}",
            f"作者：{', '.join(authors)}" if authors else "",
            f"标签：{', '.join(tags)}" if tags else "",
            "摘要摘录：\n" + "\n".join(f"- {line}" for line in excerpt_lines[:3]) if excerpt_lines else "",
            f"原文：{canonical_url}",
        )
        built_items.append(
            {
                "item_key": canonical_url,
                "packet_slug": f"{config.packet_prefix}_{slugify(title, slug)}",
                "source_id": config.source_id,
                "source_name": config.source_name,
                "source_type": config.source_type,
                "platform": config.platform,
                "region": config.region,
                "source_url": config.source_url,
                "canonical_url": canonical_url,
                "title": title,
                "author_or_channel": ", ".join(authors) if authors else config.source_name,
                "published_at": format_dt(published_dt),
                "captured_at": format_dt(captured_at),
                "language": config.language,
                "content_type": "official blog post",
                "capture_method": "official github repo + raw markdown",
                "normalization_method": "markdown_normalized",
                "translation_needed": "yes" if config.language == "en" else "no",
                "status": "normalized",
                "signal_quality": config.signal_quality,
                "primary_source": config.metadata.get("primary_source", "yes"),
                "verification_status": config.metadata.get("verification_status", "primary-source-repo"),
                "summary": f"Hugging Face Blog 抓到官方新文章“{title}”。当前通过官方 GitHub repo 与原始 markdown 直连，已从匿名风控软失败切到可追踪的硬成功路径。",
                "topic_tags": unique_strings(config.metadata.get("topic_tags", ["huggingface", "official-update"]) + tags[:4]),
                "quote_candidates": [title, *excerpt_lines[:2]],
                "distilled_body": distilled_body,
                "why_source_matters": config.metadata.get(
                    "why_source_matters",
                    "Hugging Face Blog 是开源模型、工具、生态变化的重要官方入口。",
                ),
                "citation_reliability": config.metadata.get("citation_reliability", "high"),
                "caveat": config.metadata.get(
                    "caveat",
                    "官方博客适合做一手更新入口，但具体能力和发布日期仍建议继续回链 repo、docs、模型页和 release notes。",
                ),
                "raw_body": raw_body,
                "normalized_excerpt": compact_snippet(" / ".join(excerpt_lines[:3]) or title, 360),
                "worth_clustering_with": f"{canonical_url} / {raw_capture_url}",
                "possible_topic_directions": config.metadata.get("follow_up_hints", []),
                "heat_hint": config.metadata.get("heat_hint", "official update repo"),
            }
        )
    return built_items


def build_github_trending_item(
    config: SourceConfig,
    repo_full_name: str,
    repo_url: str,
    description: str,
    language: str,
    total_stars: str,
    forks: str,
    stars_today: str,
    captured_at: datetime,
    *,
    capture_url: str,
    capture_method: str = "jina-reader / github trending",
) -> dict[str, Any]:
    owner = repo_full_name.split("/", 1)[0].strip() if "/" in repo_full_name else config.source_name
    item_key = repo_url
    raw_body = textwrap.dedent(
        f"""\
        # Raw Capture

        - `source_id`: `{config.source_id}`
        - `repo`: `{repo_full_name}`
        - `repo_url`: {repo_url}
        - `capture_url`: {capture_url}
        - `language`: `{language or 'unknown'}`
        - `stars_total`: `{total_stars or 'unknown'}`
        - `forks`: `{forks or 'unknown'}`
        - `stars_today`: `{stars_today or 'unknown'}`
        - `captured_at`: `{format_dt(captured_at)}`

        ## Description

        {description if description else "_no description_"}
        """
    ).strip() + "\n"
    distilled_body = distill_text(
        f"Repo：{repo_full_name}",
        f"描述：{description}" if description else "",
        f"语言：{language}" if language else "",
        f"热度：总 stars {total_stars or 'unknown'} / forks {forks or 'unknown'} / 今日新增 {stars_today or 'unknown'}",
        f"仓库地址：{repo_url}",
    )
    summary = (
        f"GitHub Trending 抓到仓库 {repo_full_name}。当前总 stars {total_stars or 'unknown'}、"
        f"今日新增 {stars_today or 'unknown'}；它适合作为开源 agent / workflow / infra 真实 traction 的入口。"
    )
    return {
        "item_key": item_key,
        "packet_slug": f"{config.packet_prefix}_{slugify(repo_full_name, 'github_repo')}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": config.source_url,
        "canonical_url": repo_url,
        "title": repo_full_name,
        "author_or_channel": owner,
        "published_at": f"{captured_at.strftime('%Y-%m-%d')} (capture day)",
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": "open-source trending repo",
        "capture_method": capture_method,
        "normalization_method": "markdown_normalized",
        "translation_needed": "yes" if config.language == "en" else "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": config.metadata.get("primary_source", "partial"),
        "verification_status": config.metadata.get("verification_status", "official-platform-listing"),
        "summary": summary,
        "topic_tags": config.metadata.get("topic_tags", ["github-trending", "open-source"]),
        "quote_candidates": [repo_full_name, compact_snippet(description, 180), f"{stars_today or 'unknown'} stars today"],
        "distilled_body": distilled_body,
        "why_source_matters": config.metadata.get(
            "why_source_matters",
            "GitHub Trending 能判断开源项目是否真的开始获得开发者 traction。",
        ),
        "citation_reliability": config.metadata.get("citation_reliability", "medium"),
        "caveat": "Trending 说明热度，不说明长期价值；正式写作要继续看 README、docs、demo 和 release。",
        "raw_body": raw_body,
        "normalized_excerpt": compact_snippet(description or repo_full_name, 360),
        "worth_clustering_with": f"{repo_url} / README / demo / docs",
        "possible_topic_directions": config.metadata.get("follow_up_hints", []),
        "heat_hint": config.metadata.get("heat_hint", "open-source traction"),
    }


def collect_github_trending_html_items(config: SourceConfig, captured_at: datetime, limit: int) -> list[dict[str, Any]]:
    html = fetch_html_page(config.source_url, referer="https://github.com/")
    blocks = re.findall(r'<article class="Box-row">(.*?)</article>', html, re.S)
    built_items: list[dict[str, Any]] = []
    for block in blocks:
        repo_match = re.search(r'<h2[^>]*>.*?<a[^>]+href="/([^"#?]+/[^"#?]+)"', block, re.S)
        if not repo_match:
            continue
        repo_full_name = clean_search_text(repo_match.group(1)).replace(" ", "")
        repo_url = f"https://github.com/{repo_full_name}"
        description_match = re.search(r'<p class="[^"]*color-fg-muted[^"]*my-1[^"]*">(.*?)</p>', block, re.S)
        description = clean_search_text(description_match.group(1)) if description_match else ""
        haystack = " ".join([repo_full_name, description]).lower()
        if not passes_keyword_gate(config, haystack):
            continue
        language_match = re.search(r'<span itemprop="programmingLanguage">(.*?)</span>', block, re.S)
        stars_match = re.search(r'href="/[^"#?]+/[^"#?]+/stargazers"[^>]*>.*?</svg>\s*([\d,]+)</a>', block, re.S)
        forks_match = re.search(r'href="/[^"#?]+/[^"#?]+/forks"[^>]*>.*?</svg>\s*([\d,]+)</a>', block, re.S)
        stars_today_match = re.search(r'([\d,]+)\s+stars(?:\s+today|\s+this\s+\w+)', block, re.I)
        built_items.append(
            build_github_trending_item(
                config,
                repo_full_name,
                repo_url,
                description,
                clean_search_text(language_match.group(1)) if language_match else "",
                stars_match.group(1).strip() if stars_match else "",
                forks_match.group(1).strip() if forks_match else "",
                stars_today_match.group(1).strip() if stars_today_match else "",
                captured_at,
                capture_url=config.source_url,
                capture_method="direct html / github trending",
            )
        )
        if len(built_items) >= limit:
            break
    if not built_items:
        raise RuntimeError(f"No repositories extracted from GitHub Trending HTML: {config.source_url}")
    return built_items


def collect_github_trending_items(config: SourceConfig, captured_at: datetime, limit: int) -> list[dict[str, Any]]:
    try:
        return collect_github_trending_html_items(config, captured_at, limit)
    except Exception:
        pass
    capture_url = resolve_fetch_url(config, "capture_url")
    markdown = extract_jina_markdown_body(
        fetch_text_via_curl(
            capture_url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/plain, text/markdown;q=0.9, */*;q=0.8",
            },
        )
    )
    heading_pattern = re.compile(r"^## \[(?P<repo>[^\]]+)\]\((?P<url>https?://github\.com/[^)\s]+)\)$")
    stats_pattern = re.compile(
        r"^(?P<language>[^[]+?)\[(?P<stars>[\d,]+)\]\([^)]+\)\[(?P<forks>[\d,]+)\]\([^)]+\).*?(?P<today>[\d,]+) stars today",
        re.I,
    )
    lines = [line.rstrip() for line in markdown.splitlines()]
    built_items: list[dict[str, Any]] = []
    for index, line in enumerate(lines):
        match = heading_pattern.match(line.strip())
        if not match:
            continue
        repo_full_name = match.group("repo").replace(" ", "")
        repo_url = match.group("url").replace("http://", "https://")
        description = ""
        stats_line = ""
        for probe in range(index + 1, min(len(lines), index + 8)):
            candidate = lines[probe].strip()
            if not candidate:
                continue
            if candidate.startswith("## "):
                break
            if "Built by" in candidate and "stars today" in candidate:
                stats_line = candidate
                break
            if not description and not candidate.startswith("[Star]"):
                description = candidate
        haystack = " ".join([repo_full_name, description]).lower()
        if not passes_keyword_gate(config, haystack):
            continue
        language = ""
        total_stars = ""
        forks = ""
        stars_today = ""
        stats_match = stats_pattern.match(stats_line)
        if stats_match:
            language = stats_match.group("language").strip()
            total_stars = stats_match.group("stars").strip()
            forks = stats_match.group("forks").strip()
            stars_today = stats_match.group("today").strip()
        built_items.append(
            build_github_trending_item(
                config,
                repo_full_name,
                repo_url,
                description,
                language,
                total_stars,
                forks,
                stars_today,
                captured_at,
                capture_url=capture_url,
                capture_method="jina-reader / github trending",
            )
        )
        if len(built_items) >= limit:
            break
    return built_items


def build_hf_paper_item(
    config: SourceConfig,
    title: str,
    paper_url: str,
    submitter: str,
    vote_count: str,
    context_line: str,
    captured_at: datetime,
    *,
    published_at: datetime | None = None,
    capture_url: str,
) -> dict[str, Any]:
    item_key = paper_url
    raw_body = textwrap.dedent(
        f"""\
        # Raw Capture

        - `source_id`: `{config.source_id}`
        - `title`: `{title}`
        - `paper_url`: {paper_url}
        - `capture_url`: {capture_url}
        - `submitter`: `{submitter or 'unknown'}`
        - `vote_count`: `{vote_count or 'unknown'}`
        - `context`: `{context_line or 'unknown'}`
        - `published_at`: `{format_dt(published_at)}`
        - `captured_at`: `{format_dt(captured_at)}`
        """
    ).strip() + "\n"
    distilled_body = distill_text(
        f"论文：{title}",
        f"提交者：{submitter}" if submitter else "",
        f"社区线索：votes={vote_count}" if vote_count else "",
        f"附加信息：{context_line}" if context_line else "",
        f"论文入口：{paper_url}",
    )
    summary = (
        f"{config.source_name} 收录了“{title}”。它更适合作为研究社区扩散信号，"
        f"当前可见提交者 {submitter or 'unknown'}、社区票数 {vote_count or 'unknown'}。"
    )
    return {
        "item_key": item_key,
        "packet_slug": f"{config.packet_prefix}_{slugify(title, 'hf_paper')}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": config.source_url,
        "canonical_url": paper_url,
        "title": title,
        "author_or_channel": submitter or config.source_name,
        "published_at": format_dt(published_at) if published_at else f"{captured_at.strftime('%Y-%m-%d')} (capture day)",
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": "research trending paper",
        "capture_method": config.metadata.get("capture_method", "jina-reader / huggingface papers"),
        "normalization_method": "markdown_normalized",
        "translation_needed": "yes" if config.language == "en" else "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": config.metadata.get("primary_source", "partial"),
        "verification_status": config.metadata.get("verification_status", "research-community-signal"),
        "summary": summary,
        "topic_tags": config.metadata.get("topic_tags", ["huggingface", "daily-papers"]),
        "quote_candidates": [title, submitter, f"votes={vote_count or 'unknown'}"],
        "distilled_body": distilled_body,
        "why_source_matters": config.metadata.get(
            "why_source_matters",
            "HF Daily Papers 能帮助判断哪些研究对象正在研究社区里获得注意力。",
        ),
        "citation_reliability": config.metadata.get("citation_reliability", "medium"),
        "caveat": "HF Daily Papers 说明社区关注，不说明论文已经被产业验证；正式判断仍需回链 arXiv / 项目页。",
        "raw_body": raw_body,
        "normalized_excerpt": compact_snippet(" / ".join(part for part in [title, context_line, submitter] if part), 360),
        "worth_clustering_with": f"{paper_url} / arXiv / project page / authors",
        "possible_topic_directions": config.metadata.get("follow_up_hints", []),
        "heat_hint": config.metadata.get("heat_hint", "research diffusion"),
    }


def collect_hf_papers_items(config: SourceConfig, captured_at: datetime, limit: int) -> list[dict[str, Any]]:
    capture_url = resolve_fetch_url(config, "capture_url")
    markdown = extract_jina_markdown_body(fetch_text(capture_url))
    heading_pattern = re.compile(r"^### \[(?P<title>.+?)\]\((?P<url>https?://[^)\s]+)\)$")
    vote_pattern = re.compile(r"^\[- \[x\] (?P<votes>[\d-]+)\]\(")
    lines = [line.rstrip() for line in markdown.splitlines()]
    built_items: list[dict[str, Any]] = []
    for index, line in enumerate(lines):
        match = heading_pattern.match(line.strip())
        if not match:
            continue
        title = match.group("title").strip()
        paper_url = match.group("url").replace("http://", "https://")
        submitter = ""
        vote_count = ""
        context_line = ""
        for probe in range(max(0, index - 8), index):
            candidate = lines[probe].strip()
            vote_match = vote_pattern.match(candidate)
            if vote_match:
                vote_count = vote_match.group("votes").strip()
        for probe in range(index - 1, max(-1, index - 8), -1):
            if probe < 0:
                break
            candidate = lines[probe].strip()
            if not candidate:
                continue
            if candidate.startswith("![Image") or candidate.startswith("[- [x]") or candidate == "Submitted by" or candidate.startswith("[]("):
                continue
            submitter = candidate
            break
        for probe in range(index + 1, min(len(lines), index + 5)):
            candidate = lines[probe].strip()
            if not candidate:
                continue
            if candidate.startswith("[") and "#community" in candidate:
                continue
            if candidate.startswith("### "):
                break
            context_line = candidate
            break
        built_items.append(
            build_hf_paper_item(
                config,
                title,
                paper_url,
                submitter,
                vote_count,
                context_line,
                captured_at,
                published_at=None,
                capture_url=capture_url,
            )
        )
        if len(built_items) >= limit:
            break
    return built_items


def derive_arxiv_url(candidate_url: str) -> str:
    match = re.search(r"/p/(?P<arxiv_id>\d{4}\.\d{4,5}(?:v\d+)?)$", candidate_url.strip())
    if match:
        return f"https://arxiv.org/abs/{match.group('arxiv_id')}"
    return candidate_url


def collect_hf_papers_takara_items(config: SourceConfig, captured_at: datetime, limit: int) -> list[dict[str, Any]]:
    feed_url = resolve_fetch_url(config, "feed_url")
    xml_text = fetch_text(feed_url)
    root = ET.fromstring(xml_text)
    channel = root.find("channel")
    if channel is None:
        return []
    built_items: list[dict[str, Any]] = []
    for item in channel.findall("item"):
        title = clean_search_text(item.findtext("title") or "")
        takara_url = str(item.findtext("link") or "").strip()
        if not title or not takara_url:
            continue
        description = strip_html(item.findtext("description") or "")
        published_at = parse_pubdate(item.findtext("pubDate"))
        paper_url = derive_arxiv_url(takara_url)
        built = build_hf_paper_item(
            config,
            title,
            paper_url,
            "Takara mirror",
            "",
            description,
            captured_at,
            published_at=published_at,
            capture_url=feed_url,
        )
        built["worth_clustering_with"] = unique_strings([paper_url, takara_url])[0] if paper_url == takara_url else f"{paper_url} / {takara_url}"
        built["quote_candidates"] = unique_strings([title, compact_snippet(description, 180), "Takara mirror"])
        built["normalized_excerpt"] = compact_snippet(description or title, 360)
        built_items.append(built)
        if len(built_items) >= limit:
            break
    return built_items


def build_baidu_hot_item(
    config: SourceConfig,
    title: str,
    link: str,
    summary_text: str,
    heat_index: str,
    rank: int,
    captured_at: datetime,
    *,
    capture_url: str,
) -> dict[str, Any]:
    raw_body = textwrap.dedent(
        f"""\
        # Raw Capture

        - `source_id`: `{config.source_id}`
        - `rank`: `{rank}`
        - `title`: `{title}`
        - `link`: {link}
        - `heat_index`: `{heat_index or 'unknown'}`
        - `capture_url`: {capture_url}
        - `captured_at`: `{format_dt(captured_at)}`

        ## Summary

        {summary_text if summary_text else "_no summary_"}
        """
    ).strip() + "\n"
    distilled_body = distill_text(
        f"热搜题目：{title}",
        f"热搜指数：{heat_index}" if heat_index else "",
        f"摘要：{summary_text}" if summary_text else "",
        f"榜单链接：{link}",
    )
    summary = (
        f"百度热搜出现了与 AI / agent / robotics 相关的话题“{title}”。"
        f"当前热搜指数 {heat_index or 'unknown'}，它适合作为中文破圈验证信号，而不是事实源。"
    )
    return {
        "item_key": link,
        "packet_slug": f"{config.packet_prefix}_{slugify(title, 'baidu_hot')}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": config.source_url,
        "canonical_url": link,
        "title": title,
        "author_or_channel": config.source_name,
        "published_at": f"{captured_at.strftime('%Y-%m-%d')} (capture day)",
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": "heat ranking topic",
        "capture_method": "jina-reader / baidu hot",
        "normalization_method": "markdown_normalized",
        "translation_needed": "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": config.metadata.get("primary_source", "no"),
        "verification_status": config.metadata.get("verification_status", "heat-validation-signal"),
        "summary": summary,
        "topic_tags": config.metadata.get("topic_tags", ["baidu-hot", "heat-validation"]),
        "quote_candidates": [title, compact_snippet(summary_text, 150), f"heat_index={heat_index or 'unknown'}"],
        "distilled_body": distilled_body,
        "why_source_matters": config.metadata.get(
            "why_source_matters",
            "百度热搜适合作为大众传播层的破圈验证信号。",
        ),
        "citation_reliability": config.metadata.get("citation_reliability", "low"),
        "caveat": "热搜只能证明传播，不证明事实强度或商业价值；正式写作必须回链原始事件。",
        "raw_body": raw_body,
        "normalized_excerpt": compact_snippet(summary_text or title, 360),
        "worth_clustering_with": "原始事件页 / 官方源 / 多平台讨论",
        "possible_topic_directions": config.metadata.get("follow_up_hints", []),
        "heat_hint": config.metadata.get("heat_hint", "breakout validation"),
    }


def collect_baidu_hot_items(config: SourceConfig, captured_at: datetime, limit: int) -> list[dict[str, Any]]:
    capture_url = resolve_fetch_url(config, "capture_url")
    markdown = extract_jina_markdown_body(fetch_text(capture_url))
    lines = [line.rstrip() for line in markdown.splitlines()]
    title_pattern = re.compile(r"^\[(?P<title>[^\]]+)\]\((?P<link>https?://www\.baidu\.com/s\?[^)\s]+)\)$")
    rank_pattern = re.compile(r"^\[(?P<rank>\d+)\s+!\[Image")
    built_items: list[dict[str, Any]] = []
    seen_links: set[str] = set()
    sequential_rank = 0
    skip_titles = {"新闻", "hao123", "地图", "贴吧", "百度首页", "首页", "热搜", "小说", "电影", "电视剧", "查看更多>"}
    for index, line in enumerate(lines):
        candidate_line = line.strip()
        if candidate_line.startswith("[![Image"):
            continue
        match = title_pattern.match(candidate_line)
        if not match:
            continue
        title = match.group("title").strip()
        link = match.group("link").replace("http://", "https://")
        if title in skip_titles or "查看更多" in title or link in seen_links:
            continue
        summary_text = ""
        heat_index = ""
        explicit_rank = ""
        for probe in range(max(0, index - 6), index):
            candidate = lines[probe].strip()
            if candidate.isdigit() and len(candidate) >= 5:
                heat_index = candidate
            rank_match = rank_pattern.match(candidate)
            if rank_match:
                explicit_rank = rank_match.group("rank")
        for probe in range(index + 1, min(len(lines), index + 6)):
            candidate = lines[probe].strip()
            if not candidate:
                continue
            if candidate.startswith("[") or candidate.startswith("![Image"):
                continue
            summary_text = candidate.replace(" [查看更多>]", "").strip()
            break
        haystack = " ".join([title, summary_text]).lower()
        if not passes_keyword_gate(config, haystack):
            continue
        seen_links.add(link)
        sequential_rank += 1
        built_items.append(
            build_baidu_hot_item(
                config,
                title,
                link,
                summary_text,
                heat_index,
                int(explicit_rank or sequential_rank),
                captured_at,
                capture_url=capture_url,
            )
        )
        if len(built_items) >= limit:
            break
    return built_items


def build_zhihu_hot_item(
    config: SourceConfig,
    hot_item: dict[str, Any],
    captured_at: datetime,
    *,
    rank: int,
) -> dict[str, Any] | None:
    question = hot_item.get("question") or hot_item.get("target") or {}
    title = str(question.get("title") or "").strip()
    excerpt = str(question.get("excerpt") or "").strip()
    detail_text = str(hot_item.get("detail_text") or "").strip()
    reaction = hot_item.get("reaction") or {}
    topics = [str(topic.get("name") or "").strip() for topic in question.get("topics") or [] if str(topic.get("name") or "").strip()]
    question_id = str(question.get("id") or question.get("token") or "").strip()
    if not title:
        return None
    haystack = " ".join([title, excerpt, detail_text, " ".join(topics)]).lower()
    if not passes_keyword_gate(config, haystack):
        return None
    canonical_url = f"https://www.zhihu.com/question/{question_id}" if question_id else config.source_url
    created_at = question.get("created")
    published_dt = None
    if isinstance(created_at, int):
        published_dt = datetime.fromtimestamp(created_at, tz=timezone.utc)
    answer_count = question.get("answer_count") or 0
    follower_count = question.get("follower_count") or 0
    score = reaction.get("score")
    new_pv = reaction.get("new_pv")
    upvote_num = reaction.get("new_upvote_num") or reaction.get("upvote_num")
    raw_body = textwrap.dedent(
        f"""\
        # Raw Capture

        - `source_id`: `{config.source_id}`
        - `rank`: `{rank}`
        - `title`: `{title}`
        - `canonical_url`: {canonical_url}
        - `question_id`: `{question_id or 'unknown'}`
        - `topics`: `{', '.join(topics) if topics else 'unknown'}`
        - `detail_text`: `{detail_text or 'unknown'}`
        - `answer_count`: `{answer_count}`
        - `follower_count`: `{follower_count}`
        - `score`: `{score if score is not None else 'unknown'}`
        - `new_pv`: `{new_pv if new_pv is not None else 'unknown'}`
        - `new_upvote_num`: `{upvote_num if upvote_num is not None else 'unknown'}`
        - `published_at`: `{format_dt(published_dt)}`
        - `captured_at`: `{format_dt(captured_at)}`

        ## Excerpt

        {excerpt if excerpt else "_no excerpt_"}
        """
    ).strip() + "\n"
    distilled_body = distill_text(
        f"知乎热榜题目：{title}",
        f"热度：{detail_text}" if detail_text else "",
        f"话题：{' / '.join(topics)}" if topics else "",
        f"指标：回答 {answer_count} / 关注 {follower_count}" + (f" / score {score}" if score is not None else "") + (f" / new_pv {new_pv}" if new_pv is not None else ""),
        f"摘要：{excerpt}" if excerpt else "",
        f"问题链接：{canonical_url}",
    )
    summary = (
        f"知乎热榜出现了 AI 相关问题“{title}”。"
        f"{(' 当前热度 ' + detail_text + '。') if detail_text else ''}"
        "它适合作为中文问答场域的破圈验证和用户疑问观察层。"
    )
    return {
        "item_key": question_id or canonical_url or title,
        "packet_slug": f"{config.packet_prefix}_{slugify(title, 'zhihu_hot')}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": config.source_url,
        "canonical_url": canonical_url,
        "title": title,
        "author_or_channel": config.source_name,
        "published_at": format_dt(published_dt),
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": "heat ranking question",
        "capture_method": "zhihu public hot-list json",
        "normalization_method": "markdown_normalized",
        "translation_needed": "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": config.metadata.get("primary_source", "no"),
        "verification_status": config.metadata.get("verification_status", "heat-validation-signal"),
        "summary": summary,
        "topic_tags": config.metadata.get("topic_tags", ["zhihu-hot", "heat-validation"]),
        "quote_candidates": [title, detail_text, compact_snippet(excerpt, 160)],
        "distilled_body": distilled_body,
        "why_source_matters": config.metadata.get(
            "why_source_matters",
            "知乎热榜适合作为中文讨论场域的破圈验证层。",
        ),
        "citation_reliability": config.metadata.get("citation_reliability", "low-medium"),
        "caveat": "热榜问题说明讨论热度，不说明事实强度；正式写作仍需回链原始事件、官方源与产品页。",
        "raw_body": raw_body,
        "normalized_excerpt": compact_snippet(excerpt or title, 360),
        "worth_clustering_with": "原始事件页 / 官方源 / 题目讨论 / 高赞回答",
        "possible_topic_directions": config.metadata.get("follow_up_hints", []),
        "heat_hint": detail_text or config.metadata.get("heat_hint", "qa breakout validation"),
    }


def collect_zhihu_hot_items(config: SourceConfig, captured_at: datetime, limit: int) -> list[dict[str, Any]]:
    payload = fetch_json(config.source_url)
    data = payload.get("data", []) if isinstance(payload, dict) else []
    built_items: list[dict[str, Any]] = []
    for index, item in enumerate(data if isinstance(data, list) else [], start=1):
        if not isinstance(item, dict):
            continue
        built = build_zhihu_hot_item(config, item, captured_at, rank=index)
        if built is None:
            continue
        built_items.append(built)
        if len(built_items) >= limit:
            break
    return built_items


def build_newrank_period_item(
    config: SourceConfig,
    rank_meta: dict[str, Any],
    period_item: dict[str, Any],
    captured_at: datetime,
    *,
    detail_url: str,
    api_url: str,
) -> dict[str, Any]:
    display_name = str(rank_meta.get("display_name") or config.source_name).replace("</br>", " ").strip()
    period = str(period_item.get("period") or "unknown").strip()
    pub_time = str(period_item.get("pub_time") or "unknown").strip()
    image_paths = [path.strip() for path in str(period_item.get("img_path") or "").split(";") if path.strip()]
    item_id = str(period_item.get("id") or f"{config.source_id}_{period}").strip()
    ocr_summary = summarize_newrank_ocr(image_paths)
    rank_rows = ocr_summary["rows"]
    extracted_names = [row["account_name"] for row in rank_rows[:5]]
    ocr_structured_rows = render_newrank_rank_rows(rank_rows[:10])
    ocr_excerpt = markdown_bullets(ocr_summary["text_excerpt_lines"][:40])
    raw_body = (
        "# Raw Capture\n\n"
        f"- `source_id`: `{config.source_id}`\n"
        f"- `detail_url`: {detail_url}\n"
        f"- `api_url`: {api_url}\n"
        f"- `rank_name`: `{rank_meta.get('name') or config.metadata.get('rank_name') or 'unknown'}`\n"
        f"- `display_name`: `{display_name}`\n"
        f"- `period`: `{period}`\n"
        f"- `pub_time`: `{pub_time}`\n"
        f"- `latest_period`: `{rank_meta.get('last_period') or 'unknown'}`\n"
        f"- `latest_pub_time`: `{rank_meta.get('last_pub_time') or 'unknown'}`\n"
        f"- `captured_at`: `{format_dt(captured_at)}`\n\n"
        "## Image Paths\n\n"
        f"{chr(10).join(f'- {path}' for path in image_paths) if image_paths else '- none'}\n\n"
        "## OCR Enrichment\n\n"
        f"- `ocr_status`: `{ocr_summary['status']}`\n"
        f"- `ocr_engine`: `{ocr_summary['engine']}`\n"
        f"- `processed_image_count`: `{ocr_summary['processed_image_count']}`\n"
        f"- `detected_text_blocks`: `{ocr_summary['detected_text_blocks']}`\n"
        f"- `structured_rank_rows`: `{len(rank_rows)}`\n"
        "- `ocr_errors`:\n"
        f"{markdown_bullets(ocr_summary['errors'])}\n\n"
        "## OCR Structured Top Accounts\n\n"
        f"{ocr_structured_rows}\n\n"
        "## OCR Text Excerpt\n\n"
        f"{ocr_excerpt}\n"
    )
    distilled_body = distill_text(
        f"榜单：{display_name}",
        f"期数：第 {period} 期" if period else "",
        f"发布时间：{pub_time}" if pub_time else "",
        f"榜单详情：{detail_url}",
        f"榜单图片：{' / '.join(image_paths[:3])}" if image_paths else "",
        "OCR 提取 Top 10：\n" + ocr_structured_rows if rank_rows else "",
    )
    summary = (
        f"新榜返回了“{display_name}”的第 {period} 期记录，发布时间 {pub_time}。"
        "它更适合作为 AI 垂类账号势能与平台传播格局的月度验证层。"
    )
    if extracted_names:
        summary += f" 本轮 OCR 提取到的前列账号包括：{'、'.join(extracted_names)}。"
    quote_candidates = [display_name, f"第 {period} 期", pub_time, *extracted_names[:3]]
    caveat = (
        "公开接口原生只返回榜单图片；当前结构化明细来自本地 OCR 辅助提取。"
        "适合用于竞品观察与平台势能判断，但关键结论仍应结合公众号原文与账号复盘交叉验证。"
    )
    if ocr_summary["status"] != "ok":
        caveat = (
            "公开接口原生只返回榜单图片；本轮 OCR 未成功提取结构化明细。"
            "当前记录仍可用于月度平台验证，但需要后续补 OCR 或直接深抓公众号原文。"
        )
    return {
        "item_key": item_id or f"{config.source_id}_{period}",
        "packet_slug": f"{config.packet_prefix}_{slugify(display_name, 'newrank')}_{period}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": detail_url,
        "canonical_url": detail_url,
        "title": f"{display_name}｜第 {period} 期",
        "author_or_channel": config.source_name,
        "published_at": pub_time,
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": "platform periodic rank",
        "capture_method": "newrank public period json + local ocr",
        "normalization_method": "markdown_normalized",
        "translation_needed": "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": config.metadata.get("primary_source", "no"),
        "verification_status": config.metadata.get("verification_status", "platform-ranking-signal"),
        "summary": summary,
        "topic_tags": config.metadata.get("topic_tags", ["newrank", "platform-rank"]),
        "image_paths": image_paths,
        "quote_candidates": unique_strings(quote_candidates),
        "distilled_body": distilled_body,
        "why_source_matters": config.metadata.get(
            "why_source_matters",
            "新榜适合作为中文平台格局与账号势能观察层。",
        ),
        "citation_reliability": config.metadata.get("citation_reliability", "low-medium"),
        "caveat": caveat,
        "raw_body": raw_body,
        "normalized_excerpt": compact_snippet(
            f"{display_name} 第 {period} 期，发布时间 {pub_time}。"
            + (f" OCR 前列账号：{' / '.join(extracted_names[:5])}" if extracted_names else ""),
            240,
        ),
        "worth_clustering_with": "微信深抓全文 / 账号对象池 / 竞品复盘",
        "possible_topic_directions": config.metadata.get("follow_up_hints", []),
        "heat_hint": config.metadata.get("heat_hint", "platform benchmark validation"),
    }


def collect_newrank_period_items(config: SourceConfig, captured_at: datetime, limit: int) -> list[dict[str, Any]]:
    api_url = resolve_fetch_url(config, "api_url")
    rank_name = str(config.metadata.get("rank_name") or "").strip()
    payload = fetch_form_json(api_url, {"name": rank_name, "page": 0, "size": 0})
    value = payload.get("value", {}) if isinstance(payload, dict) else {}
    rank_meta = value.get("item", {}) if isinstance(value, dict) else {}
    data = value.get("datas", []) if isinstance(value, dict) else []
    detail_url = config.source_url
    built_items: list[dict[str, Any]] = []
    for item in data if isinstance(data, list) else []:
        if not isinstance(item, dict):
            continue
        built_items.append(build_newrank_period_item(config, rank_meta, item, captured_at, detail_url=detail_url, api_url=api_url))
        if len(built_items) >= limit:
            break
    return built_items


def build_feigua_hot_video_item(
    config: SourceConfig,
    block: str,
    captured_at: datetime,
    *,
    capture_url: str,
    rank_date: str,
) -> dict[str, Any] | None:
    rank_match = re.search(r'<span class="rank_index">(\d+)</span>', block)
    title_match = re.search(r'<a class="title[^"]*"[^>]*data-title="([^"]+)"', block)
    uploader_match = re.search(r'<span class="blogger-name">([^<]+)</span>', block)
    published_match = re.search(r'<span class="video-time">([^<]+)</span>', block)
    duration_match = re.search(r'<div class="during">([^<]+)</div>', block)
    category_match = re.search(r'<div class="home-tag">\s*([^<]+?)\s*</div>', block)
    metrics_match = re.search(
        r'<div class="col-item import_red"[^>]*>\s*([^<]+?)\s*</div>\s*'
        r'<div class="col-item"[^>]*>\s*([^<]+?)\s*</div>\s*'
        r'<div class="col-item"[^>]*>\s*([^<]+?)\s*</div>\s*'
        r'<div class="col-item"[^>]*>\s*([^<]+?)\s*</div>',
        block,
        re.S,
    )
    if not rank_match or not title_match:
        return None
    rank = int(rank_match.group(1))
    title = unescape(title_match.group(1)).strip()
    uploader = unescape(uploader_match.group(1)).strip() if uploader_match else ""
    published_raw = unescape(published_match.group(1)).strip() if published_match else ""
    duration = unescape(duration_match.group(1)).strip() if duration_match else ""
    category = unescape(category_match.group(1)).strip() if category_match else ""
    play_inc = like_inc = comment_inc = favorite_inc = ""
    if metrics_match:
        play_inc, like_inc, comment_inc, favorite_inc = [unescape(group).strip() for group in metrics_match.groups()]
    haystack = " ".join([title, uploader, category]).lower()
    if not passes_keyword_gate(config, haystack):
        return None
    published_dt = parse_cn_datetime(published_raw)
    backlink = resolve_bilibili_video(title, uploader)
    backlink_ok = bool(backlink and backlink.get("accepted") and backlink.get("url"))
    canonical_url = str(backlink.get("url")) if backlink_ok else f"{capture_url}#rank-{rank}"
    backlink_note = (
        textwrap.dedent(
            f"""\
            - `bilibili_query`: `{backlink.get('query') or title}`
            - `matched_title`: `{backlink.get('title') or 'unresolved'}`
            - `matched_uploader`: `{backlink.get('uploader') or 'unresolved'}`
            - `bvid`: `{backlink.get('bvid') or 'unresolved'}`
            - `bilibili_video_url`: `{backlink.get('url') or 'unresolved'}`
            - `match_confidence`: `{backlink.get('confidence') or 'unresolved'}`
            - `title_ratio`: `{f"{float(backlink.get('title_ratio') or 0):.3f}" if backlink else '0.000'}`
            - `uploader_exact`: `{str(bool(backlink.get('uploader_exact'))).lower() if backlink else 'false'}`
            """
        ).strip()
        if backlink
        else "- `bilibili_backlink`: `unresolved`"
    )
    raw_body = (
        "# Raw Capture\n\n"
        f"- `source_id`: `{config.source_id}`\n"
        f"- `rank`: `{rank}`\n"
        f"- `title`: `{title}`\n"
        f"- `uploader`: `{uploader or 'unknown'}`\n"
        f"- `category`: `{category or 'unknown'}`\n"
        f"- `duration`: `{duration or 'unknown'}`\n"
        f"- `published_at`: `{format_dt(published_dt)}`\n"
        f"- `rank_date`: `{rank_date}`\n"
        f"- `capture_url`: {capture_url}\n"
        f"- `新增播放`: `{play_inc or 'unknown'}`\n"
        f"- `新增点赞`: `{like_inc or 'unknown'}`\n"
        f"- `新增评论`: `{comment_inc or 'unknown'}`\n"
        f"- `新增收藏`: `{favorite_inc or 'unknown'}`\n"
        f"- `captured_at`: `{format_dt(captured_at)}`\n\n"
        "## Bilibili Backlink\n\n"
        f"{backlink_note}\n"
    )
    distilled_body = distill_text(
        f"飞瓜热视频榜：#{rank} {title}",
        f"UP 主：{uploader}" if uploader else "",
        f"分类：{category}" if category else "",
        f"时长：{duration}" if duration else "",
        f"数据：新增播放 {play_inc or 'unknown'} / 新增点赞 {like_inc or 'unknown'} / 新增评论 {comment_inc or 'unknown'} / 新增收藏 {favorite_inc or 'unknown'}",
        f"发布时间：{published_raw}" if published_raw else "",
        f"榜单地址：{capture_url}",
        f"B站原视频：{backlink['url']}" if backlink_ok else "B站原视频：未稳定回链成功，本轮仍保留飞瓜榜单锚点",
    )
    summary = (
        f"飞瓜 B站热门视频榜抓到 AI 相关视频“{title}”。"
        f"当前位于榜单第 {rank} 位，适合作为中文视频场域的传播验证层。"
    )
    if backlink_ok:
        summary += " 当前已自动回链到 B站原视频。"
    quote_candidates = [title, uploader, f"新增播放 {play_inc or 'unknown'}"]
    if backlink_ok and backlink:
        quote_candidates.append(str(backlink.get("bvid") or ""))
    caveat = "榜单代表传播热度，不代表事实强度；正式写作需要继续回链原始事件或官方源。"
    if backlink and not backlink_ok:
        caveat = (
            "榜单代表传播热度，不代表事实强度。当前 B站原视频未达到稳定回链阈值，"
            "正式写作时仍需手动复核原视频或继续回链原始事件。"
        )
    return {
        "item_key": f"{rank_date}:{rank}:{title}:{uploader}",
        "packet_slug": f"{config.packet_prefix}_{slugify(title, f'feigua_{rank}')}",
        "source_id": config.source_id,
        "source_name": config.source_name,
        "source_type": config.source_type,
        "platform": config.platform,
        "region": config.region,
        "source_url": capture_url,
        "canonical_url": canonical_url,
        "title": title,
        "author_or_channel": uploader or config.source_name,
        "published_at": format_dt(published_dt),
        "captured_at": format_dt(captured_at),
        "language": config.language,
        "content_type": "video ranking topic",
        "capture_method": "feigua hot video html + bilibili backlink search",
        "normalization_method": "markdown_normalized",
        "translation_needed": "no",
        "status": "normalized",
        "signal_quality": config.signal_quality,
        "primary_source": config.metadata.get("primary_source", "no"),
        "verification_status": config.metadata.get("verification_status", "video-ranking-signal"),
        "summary": summary,
        "topic_tags": config.metadata.get("topic_tags", ["feigua", "bilibili-hot-video"]),
        "quote_candidates": unique_strings(quote_candidates),
        "distilled_body": distilled_body,
        "why_source_matters": config.metadata.get(
            "why_source_matters",
            "飞瓜能补中文视频场域的传播验证层。",
        ),
        "citation_reliability": config.metadata.get("citation_reliability", "low-medium"),
        "caveat": caveat,
        "raw_body": raw_body,
        "normalized_excerpt": compact_snippet(
            f"{title} / {uploader} / {category} / 新增播放 {play_inc}"
            + (f" / 原视频 {backlink['url']}" if backlink_ok and backlink else ""),
            360,
        ),
        "worth_clustering_with": "B站原视频 / 原始事件页 / 官方账号 / 评论区",
        "possible_topic_directions": config.metadata.get("follow_up_hints", []),
        "heat_hint": config.metadata.get("heat_hint", "video ranking validation"),
    }


def collect_feigua_bilibili_items(config: SourceConfig, captured_at: datetime, limit: int) -> list[dict[str, Any]]:
    offset_days = int(config.metadata.get("date_offset_days") or 1)
    rank_date = (captured_at.astimezone(CN_TZ) - timedelta(days=offset_days)).strftime("%Y%m%d")
    capture_template = resolve_fetch_url(config, "capture_url_template")
    capture_url = capture_template.format(date=rank_date)
    html = fetch_text_via_curl(
        capture_url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://bz.feigua.cn/",
        },
    )
    built_items: list[dict[str, Any]] = []
    for block in re.split(r'<div class="list-row">', html)[1:]:
        built = build_feigua_hot_video_item(config, block, captured_at, capture_url=capture_url, rank_date=rank_date)
        if built is None:
            continue
        built_items.append(built)
        if len(built_items) >= limit:
            break
    return built_items


def collect_hn_frontpage_items(config: SourceConfig, captured_at: datetime, limit: int) -> list[dict[str, Any]]:
    algolia_url = str(config.metadata.get("algolia_api_url") or "").strip()
    if algolia_url:
        try:
            payload = fetch_json_via_curl(
                algolia_url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/json,text/plain,*/*",
                    "Referer": "https://news.ycombinator.com/",
                },
            )
            hits = payload.get("hits", []) if isinstance(payload, dict) else []
            built_items: list[dict[str, Any]] = []
            for rank, hit in enumerate(hits, start=1):
                if not isinstance(hit, dict):
                    continue
                built = build_hn_item_from_algolia(config, hit, captured_at, source_url=algolia_url, rank=rank)
                if built is None:
                    continue
                built_items.append(built)
                if len(built_items) >= limit:
                    break
            return built_items
        except Exception:
            pass

    topstories_url = str(config.metadata.get("firebase_topstories_url") or "").strip()
    item_url_template = str(config.metadata.get("firebase_item_url_template") or "").strip()
    scan_limit = int(config.metadata.get("firebase_scan_limit") or max(limit * 5, limit))
    story_ids = fetch_json_via_curl(
        topstories_url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json,text/plain,*/*",
            "Referer": "https://news.ycombinator.com/",
        },
    )
    if not isinstance(story_ids, list):
        return []
    built_items = []
    for rank, item_id in enumerate(story_ids[:scan_limit], start=1):
        url = item_url_template.format(item_id=item_id)
        try:
            payload = fetch_json_via_curl(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/json,text/plain,*/*",
                    "Referer": "https://news.ycombinator.com/",
                },
            )
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        built = build_hn_item_from_firebase(config, payload, captured_at, source_url=topstories_url, rank=rank)
        if built is None:
            continue
        built_items.append(built)
        if len(built_items) >= limit:
            break
    return built_items


def collect_from_source(config: SourceConfig, captured_at: datetime, limit_override: int | None = None) -> list[dict[str, Any]]:
    limit = limit_override or config.default_limit
    if config.kind == "reddit_rss":
        return collect_reddit_rss_items(config, captured_at, limit)

    if config.kind == "reddit_top":
        payload = fetch_json(config.source_url)
        children = payload.get("data", {}).get("children", [])
        items = []
        for child in children[:limit]:
            post = child.get("data", {})
            permalink = post.get("permalink")
            comment_limit = config.metadata.get("comment_limit", 3)
            thread_comments: list[dict[str, Any]] = []
            if permalink:
                thread_url = f"https://www.reddit.com{permalink}.json?{urlencode({'limit': comment_limit, 'depth': 2, 'sort': 'top', 'raw_json': 1})}"
                try:
                    thread_payload = fetch_json(thread_url)
                    thread_children = thread_payload[1]["data"]["children"]
                    for thread_child in thread_children:
                        if thread_child.get("kind") == "t1":
                            thread_comments.append(thread_child.get("data", {}))
                except Exception:
                    thread_comments = []
            items.append(build_reddit_item(config, post, captured_at, thread_comments))
        return items

    if config.kind == "trend_hunt":
        payload = fetch_json(config.source_url)
        products = payload.get("products", []) if isinstance(payload, dict) else []
        return [build_trend_hunt_item(config, product, captured_at) for product in products[:limit]]

    if config.kind == "rss_feed":
        feed_url = resolve_fetch_url(config, "feed_url")
        xml_text = fetch_text(feed_url)
        root = ET.fromstring(xml_text)
        channel = root.find("channel")
        if channel is None:
            return []
        built_items = []
        for item in channel.findall("item"):
            built = build_rss_item(config, item, captured_at, resolved_source_url=feed_url)
            if built is not None:
                built_items.append(built)
            if len(built_items) >= limit:
                break
        return built_items

    if config.kind == "hn_frontpage_api":
        return collect_hn_frontpage_items(config, captured_at, limit)

    if config.kind == "github_trending_jina":
        return collect_github_trending_items(config, captured_at, limit)

    if config.kind == "jina_markdown_snapshot":
        return collect_jina_snapshot_items(config, captured_at, limit)

    if config.kind == "hf_papers_jina":
        return collect_hf_papers_items(config, captured_at, limit)

    if config.kind == "hf_papers_takara_rss":
        return collect_hf_papers_takara_items(config, captured_at, limit)

    if config.kind == "hf_blog_repo":
        return collect_hf_blog_repo_items(config, captured_at, limit)

    if config.kind == "baidu_hot_jina":
        return collect_baidu_hot_items(config, captured_at, limit)

    if config.kind == "zhihu_hot_json":
        return collect_zhihu_hot_items(config, captured_at, limit)

    if config.kind == "newrank_period_json":
        return collect_newrank_period_items(config, captured_at, limit)

    if config.kind == "feigua_bilibili_hot_html":
        return collect_feigua_bilibili_items(config, captured_at, limit)

    if config.kind == "youtube_feed":
        feed_url = resolve_youtube_feed_url(config.source_url)
        xml_text = fetch_text(feed_url)
        root = ET.fromstring(xml_text)
        built_items = []
        for entry in root.findall("atom:entry", ATOM_NS):
            built_items.append(build_youtube_item(config, entry, captured_at, resolved_source_url=feed_url))
            if len(built_items) >= limit:
                break
        return built_items

    if config.kind == "youtube_jina_channel":
        try:
            return collect_youtube_html_items(config, captured_at, limit)
        except Exception:
            return collect_youtube_jina_items(config, captured_at, limit)

    if config.kind == "bilibili_popular":
        payload = fetch_json(config.source_url)
        videos = ((payload.get("data") or {}) if isinstance(payload.get("data"), dict) else {}).get("list", [])
        built_items = []
        for video in videos if isinstance(videos, list) else []:
            if not isinstance(video, dict):
                continue
            built = build_bilibili_video_item(config, video, captured_at)
            if built is not None:
                built_items.append(built)
            if len(built_items) >= limit:
                break
        return built_items

    if config.kind == "wechat_feed":
        feed_url = resolve_wechat_feed_url(config)
        xml_text = fetch_text(feed_url)
        root = ET.fromstring(xml_text)
        channel = root.find("channel")
        if channel is None:
            return []
        built_items = []
        for item in channel.findall("item"):
            built = build_rss_item(config, item, captured_at, resolved_source_url=feed_url)
            if built is not None:
                built_items.append(built)
            if len(built_items) >= limit:
                break
        return built_items

    if config.kind == "yc_launches_json":
        payload = fetch_json(config.source_url)
        hits = payload.get("hits", []) if isinstance(payload, dict) else []
        built_items = []
        for hit in hits:
            built = build_yc_launch_item(config, hit, captured_at)
            if built is not None:
                built_items.append(built)
            if len(built_items) >= limit:
                break
        return built_items

    raise ValueError(f"Unsupported source kind: {config.kind}")


def render_packet(packet_id: str, packet_key: str, item: dict[str, Any], raw_path: Path) -> str:
    topic_tags = ", ".join(f"`{tag}`" for tag in item["topic_tags"])
    quote_lines = "\n".join(f"  - `{compact_snippet(quote, 160)}`" for quote in item["quote_candidates"] if quote)
    direction_lines = "\n".join(f"  - {direction}" for direction in item["possible_topic_directions"])
    visual_section = render_visual_intelligence(item)
    return (
        "# Source Packet\n\n"
        "## Header\n\n"
        f"- `packet_id`: `{packet_id}`\n"
        f"- `packet_key`: `{packet_key}`\n"
        f"- `source_id`: `{item['source_id']}`\n"
        f"- `source_name`: `{item.get('source_name', item['source_id'])}`\n"
        f"- `source_type`: `{item.get('source_type', 'unknown')}`\n"
        f"- `platform`: `{item['platform']}`\n"
        f"- `region`: `{item.get('region', 'unknown')}`\n"
        f"- `source_url`: `{item['source_url']}`\n"
        f"- `canonical_url`: `{item['canonical_url']}`\n"
        f"- `title`: `{item['title']}`\n"
        f"- `author_or_channel`: `{item['author_or_channel']}`\n"
        f"- `published_at`: `{item['published_at']}`\n"
        f"- `captured_at`: `{item['captured_at']}`\n"
        f"- `language`: `{item['language']}`\n"
        f"- `content_type`: `{item['content_type']}`\n"
        f"- `capture_method`: `{item['capture_method']}`\n"
        f"- `normalization_method`: `{item['normalization_method']}`\n"
        f"- `translation_needed`: `{item['translation_needed']}`\n"
        f"- `status`: `{item['status']}`\n\n"
        "## Quick Summary\n\n"
        f"- `summary`: {item['summary']}\n"
        f"- `topic_tags`: {topic_tags}\n"
        "- `quote_candidates`:\n"
        f"{quote_lines if quote_lines else '  - `none`'}\n\n"
        "## Source Notes\n\n"
        f"- `signal_quality`: `{item.get('signal_quality', 'unknown')}`\n"
        f"- `primary_source`: `{item.get('primary_source', 'unknown')}`\n"
        f"- `verification_status`: `{item.get('verification_status', 'unknown')}`\n"
        f"- `citation_reliability`: `{item['citation_reliability']}`\n"
        f"- `why_source_matters`: {item['why_source_matters']}\n"
        f"- `caveat`: {item['caveat']}\n\n"
        "## Raw Capture Path\n\n"
        f"- `raw_capture_path`: `{raw_path}`\n"
        f"- `raw_text_path`: `{raw_path}`\n\n"
        f"{visual_section}"
        "## Distilled Body\n\n"
        f"{item.get('distilled_body', '_no distilled body_')}\n\n"
        "## Normalized Excerpt\n\n"
        f"> {item['normalized_excerpt']}\n\n"
        "## Follow-up Hints\n\n"
        f"- `worth_clustering_with`: {item['worth_clustering_with']}\n"
        "- Possible topic directions:\n"
        f"{direction_lines}\n"
        f"- `heat_hint`: `{item['heat_hint']}`\n"
    )


def infer_visual_inputs(item: dict[str, Any]) -> list[str]:
    candidates: list[str] = []
    explicit_keys = ["image_url", "thumbnail_url"]
    for key in explicit_keys:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            candidates.append(value.strip())
    for key in ["image_paths", "image_urls"]:
        value = item.get(key)
        if isinstance(value, list):
            for entry in value:
                if isinstance(entry, str) and entry.strip():
                    candidates.append(entry.strip())
    raw_body = str(item.get("raw_body") or "")
    candidates.extend(re.findall(r"https?://[^\s)>'\"`]+(?:png|jpg|jpeg|webp|gif)", raw_body, re.I))
    canonical_url = str(item.get("canonical_url") or "").strip()
    source_url = str(item.get("source_url") or "").strip()
    for page_url in [canonical_url, source_url]:
        if page_url and page_url not in candidates:
            candidates.append(page_url)
    deduped: list[str] = []
    for candidate in candidates:
        if candidate not in deduped:
            deduped.append(candidate)
    return deduped[:8]


def infer_layout_observations(item: dict[str, Any]) -> list[str]:
    content_type = str(item.get("content_type") or "").lower()
    source_url = str(item.get("canonical_url") or item.get("source_url") or "")
    observations: list[str] = []
    if "video" in content_type:
        observations.append("原始视频页面更适合作为对象识别和 demo 证据，不适合整页搬运。")
    elif source_url.lower().endswith(".pdf") or ".pdf?" in source_url.lower():
        observations.append("PDF 首页标题区最适合当作正文里的“原始发布证明”。")
    elif "x.com/" in source_url.lower() or "twitter.com/" in source_url.lower():
        observations.append("原始推文截图适合作为前段证据锚点，帮助用户快速进入事件。")
    elif "github.com/" in source_url.lower():
        observations.append("Repo header + README 首屏更适合承担对象识别与 traction 证明。")
    else:
        observations.append("优先截标题区 / hero 区 / 对象区，避免整页无重点。")
    observations.append("如果原图噪音过大，应补一张解释图，而不是完全放弃原始证据图。")
    return observations


def infer_reuse_suggestions(item: dict[str, Any]) -> list[str]:
    content_type = str(item.get("content_type") or "").lower()
    suggestions: list[str] = [
        "正文第一张图优先服务原始证据，而不是装饰封面。",
        "长文中段至少应保留 1 个解释型视觉停顿点。"
    ]
    if "video" in content_type:
        suggestions.append("如果能拿到官方缩略图或标题区截图，优先用于对象识别。")
    if "ranking" in content_type or "rank" in content_type:
        suggestions.append("榜单图适合做趋势验证，但不能单独支撑最终事实结论。")
    if "product discovery" in content_type or "startup launch" in content_type:
        suggestions.append("对象页截图适合放在背景讲清后，证明这不是二手复述。")
    return suggestions


def render_visual_intelligence(item: dict[str, Any]) -> str:
    visual_inputs = infer_visual_inputs(item)
    layout_notes = infer_layout_observations(item)
    reuse_suggestions = infer_reuse_suggestions(item)
    input_lines = "\n".join(f"  - `{compact_snippet(entry, 180)}`" for entry in visual_inputs) if visual_inputs else "  - `none`"
    layout_lines = "\n".join(f"  - {entry}" for entry in layout_notes) if layout_notes else "  - none"
    reuse_lines = "\n".join(f"  - {entry}" for entry in reuse_suggestions) if reuse_suggestions else "  - none"
    status = "visual-inputs-detected" if visual_inputs else "text-only"
    return (
        "## Visual Intelligence\n\n"
        f"- `visual_evidence_status`: `{status}`\n"
        "- `source_visual_inputs`:\n"
        f"{input_lines}\n"
        "- `layout_observations`:\n"
        f"{layout_lines}\n"
        "- `our_reuse_suggestions`:\n"
        f"{reuse_lines}\n\n"
    )


def logical_date_token(logical_date: str) -> str:
    return re.sub(r"[^0-9]", "", logical_date)[:8]


def persist_item(item: dict[str, Any], run_at: datetime, logical_date: str) -> tuple[Path, Path, str, str]:
    date_token = logical_date_token(logical_date)
    timestamp = f"{date_token}_{run_at.strftime('%H%M%S')}"
    packet_key = f"{date_token}__{item['packet_slug']}"
    packet_id = f"packet_{timestamp}_{slugify(item['item_key'], 'item')}"
    raw_path = RAW_DIR / f"{timestamp}__{item['packet_slug']}__raw.md"
    packet_path = PACKET_DIR / f"{timestamp}__{item['packet_slug']}__source-packet.md"
    write_text(raw_path, item["raw_body"])
    write_text(packet_path, render_packet(packet_id, packet_key, item, raw_path))
    return raw_path, packet_path, packet_id, packet_key


def render_summary_log(
    run_at: datetime,
    logical_date: str,
    write_mode: bool,
    processed_sources: list[str],
    new_packets: list[dict[str, str]],
    skipped_items: list[dict[str, str]],
    warnings: list[str],
    errors: list[str],
) -> str:
    new_packet_lines = "\n".join(
        f"- `{row['source_id']}` → `{row['title']}` → `{row['packet_path']}`" for row in new_packets
    )
    skipped_lines = "\n".join(
        f"- `{row['source_id']}` → `{row['title']}` (`{row['item_key']}`)" for row in skipped_items
    )
    warning_lines = "\n".join(f"- {warning}" for warning in warnings)
    error_lines = "\n".join(f"- {error}" for error in errors)
    return (
        "# 同行资本市场内容系统｜市场内容捕获轮\n\n"
        f"- `run_at`: `{format_dt(run_at)}`\n"
        f"- `logical_date`: `{logical_date}`\n"
        f"- `write_mode`: `{str(write_mode).lower()}`\n"
        f"- `sources`: `{', '.join(processed_sources)}`\n"
        f"- `new_packets`: `{len(new_packets)}`\n"
        f"- `skipped_existing`: `{len(skipped_items)}`\n"
        f"- `warnings`: `{len(warnings)}`\n"
        f"- `errors`: `{len(errors)}`\n\n"
        "## New Packets\n\n"
        f"{new_packet_lines if new_packet_lines else '- none'}\n\n"
        "## Skipped Existing\n\n"
        f"{skipped_lines if skipped_lines else '- none'}\n\n"
        "## Warnings\n\n"
        f"{warning_lines if warning_lines else '- none'}\n\n"
        "## Errors\n\n"
        f"{error_lines if error_lines else '- none'}\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture market-content source packets into TH Capital's market content system.")
    parser.add_argument("--date", help="Logical capture date in YYYY-MM-DD. Default: today in Asia/Shanghai.")
    parser.add_argument("--source-id", action="append", dest="source_ids", help="Source id to capture. Can repeat.")
    parser.add_argument("--limit", type=int, default=None, help="Override per-source item limit.")
    parser.add_argument("--write", action="store_true", help="Actually write raw files, packets, logs, and state.")
    parser.add_argument("--force", action="store_true", help="Ignore dedupe state and rewrite new packet files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dirs()
    run_at = now_cn()
    logical_date = args.date or run_at.strftime("%Y-%m-%d")

    selected_source_ids = args.source_ids or [
        "web__openai_news",
        "web__google_blog_ai",
        "web__anthropic_news",
        "web__deepmind_blog",
        "web__xai_news",
        "web__nvidia_blog",
        "x__openai",
        "x__openaidevs",
        "x__anthropic_ai",
        "x__karpathy",
        "x__swyx",
        "x__hwchase17",
        "trend__reddit_localllama_daily",
        "trend__reddit_claude_daily",
        "trend__reddit_chatgpt_daily",
        "trend__hn_frontpage",
        "trend__github_trending",
        "trend__trend_hunt_ai",
        "trend__trend_hunt_ai_agents",
        "trend__trend_hunt_automation",
        "trend__huggingface_daily_papers",
        "trend__arxiv_cs_ai_recent",
        "web__simon_willison",
        "web__latent_space",
        "web__one_useful_thing",
        "web__interconnects",
        "web__understanding_ai",
        "web__deeplearningai_batch",
        "web__infoq_ai_ml",
        "web__semianalysis",
        "web__huggingface_blog",
        "web__itjuzi",
        "web__openclaw_docs",
        "youtube__openai",
        "youtube__ycombinator",
        "youtube__googledeepmind",
        "youtube__aidotengineer",
        "youtube__latent_space_pod",
        "youtube__langchain",
        "trend__bilibili_popular_all",
        "trend__baidu_realtime",
        "trend__zhihu_hotlist",
        "trend__newrank_ai_media_rank",
        "trend__feigua_bilibili",
        "wechat__liangziwei",
        "wechat__xinzhiyuan",
        "wechat__jiqizhixin",
        "wechat__zhidx",
        "wechat__36kr",
        "wechat__ifanr",
        "wechat__geekpark",
        "wechat__founder_park",
        "wechat__appsso",
        "wechat__guiguang_ai_tools",
        "wechat__guixingren_pro",
        "web__jiqizhixin_site",
        "web__qbitai_site",
        "web__zhidx",
        "web__36kr_ai",
        "web__ifanr_ai",
        "web__sspai_ai",
        "trend__yc_launches_ai",
        "web__techcrunch_ai",
        "web__finsmes_ai_gnews",
    ]

    state = load_state()
    state.setdefault("sources", {})
    new_packets: list[dict[str, str]] = []
    skipped_items: list[dict[str, str]] = []
    warnings: list[str] = []
    errors: list[str] = []

    for source_id in selected_source_ids:
        config = SOURCE_CONFIGS.get(source_id)
        if config is None:
            errors.append(f"unknown source id: {source_id}")
            continue
        source_state = state["sources"].setdefault(source_id, {})
        try:
            items = collect_from_source(config, run_at, args.limit)
            for item in items:
                item_key = str(item["item_key"])
                if not args.force and item_key in source_state:
                    skipped_items.append(
                        {
                            "source_id": source_id,
                            "title": item["title"],
                            "item_key": item_key,
                        }
                    )
                    continue
                if args.write:
                    raw_path, packet_path, _, packet_key = persist_item(item, run_at, logical_date)
                    source_state[item_key] = {
                        "packet_key": packet_key,
                        "packet_path": str(packet_path),
                        "raw_path": str(raw_path),
                        "title": item["title"],
                        "captured_at": item["captured_at"],
                        "logical_date": logical_date,
                    }
                    new_packets.append(
                        {
                            "source_id": source_id,
                            "title": item["title"],
                            "packet_path": str(packet_path),
                        }
                    )
                else:
                    new_packets.append(
                        {
                            "source_id": source_id,
                            "title": item["title"],
                            "packet_path": f"(dry-run) {item['packet_slug']}",
                        }
                    )
        except Exception as exc:
            if is_soft_fail(config, exc):
                reason = str(config.metadata.get("soft_fail_reason") or "soft fail")
                warnings.append(f"{source_id}: {type(exc).__name__}: {exc} | {reason}")
            else:
                errors.append(f"{source_id}: {type(exc).__name__}: {exc}")

    summary_log = render_summary_log(run_at, logical_date, args.write, selected_source_ids, new_packets, skipped_items, warnings, errors)
    print(summary_log)

    if args.write:
        save_state(state)
        summary_path = LOG_DIR / f"{logical_date_token(logical_date)}_{run_at.strftime('%H%M%S')}__market-topic-capture-summary.md"
        write_text(summary_path, summary_log)
        print(f"\nSummary log written to: {summary_path}")
        print(f"State file updated: {STATE_PATH}")

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())

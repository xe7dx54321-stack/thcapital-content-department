#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

from market_business_day import BUSINESS_WINDOW_END, CN_TZ, business_window_status, day_token, format_cst, parse_cst
from market_recent_topic_guard import find_recent_conflicts
from market_topic_radar_brief_builder import parse_deep_article, parse_fields, parse_packet


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
TOPIC_DIR = ROOT / "03_topic_candidates"
LOG_DIR = ROOT / "10_logs"

MANIFEST_SOURCE_SECTION = "## Real Source Packets"
MANIFEST_DEEP_SECTION = "## Real Deep Articles"
MANIFEST_ASSET_SECTION = "## Real Asset Chains"
PATH_FIELD_RE = re.compile(r"`path`:\s*`([^`]+)`")
BACKTICK_PATH_RE = re.compile(r"`([^`]+)`")
TOKEN_RE = re.compile(r"[a-z0-9]{2,}|[\u4e00-\u9fff]{2,}")
NORMALIZE_TEXT_RE = re.compile(r"[^0-9a-z\u4e00-\u9fff]+")
GENERIC_TITLE_TOKENS = {
    "today",
    "daily",
    "breaking",
    "news",
    "update",
    "article",
    "story",
    "system",
    "market",
    "content",
    "capital",
}
FIT_KEYWORDS = (
    "ai",
    "agent",
    "agents",
    "model",
    "models",
    "llm",
    "claude",
    "openai",
    "anthropic",
    "gpt",
    "gemma",
    "deepseek",
    "robot",
    "robotics",
    "infra",
    "benchmark",
    "workflow",
    "coding",
    "一人公司",
    "模型",
    "智能体",
    "机器人",
    "算力",
    "推理",
    "端侧",
    "本地",
    "创业",
    "agent",
)
HEAT_KEYWORDS = (
    "launch hn",
    "show hn",
    "ipo",
    "benchmark",
    "leak",
    "issue",
    "debate",
    "controversy",
    "exposed",
    "breaking",
    "viral",
    "封杀",
    "曝光",
    "突发",
    "上线",
    "融资",
    "翻车",
    "打脸",
    "ipo",
)
CONTROVERSY_KEYWORDS = (
    "issue",
    "bug",
    "censored",
    "block",
    "blocked",
    "leak",
    "leaked",
    "unusable",
    "封杀",
    "曝光",
    "打脸",
    "翻车",
    "失守",
    "争议",
)
TECHNICAL_ONLY_KEYWORDS = (
    "arxiv",
    "cvpr",
    "neurips",
    "iclr",
    "embedding",
    "multimodal retrieval",
    "per-layer",
)
PROMO_OR_META_KEYWORDS = (
    "招聘",
    "作者招聘",
    "申报",
    "报名",
    "征集",
    "榜单",
    "议程",
    "大会",
    "论坛",
    "峰会",
    "开幕",
)
ROUNDUP_TITLE_KEYWORDS = (
    "早知道",
    "日报",
    "快讯",
    "速览",
    "合集",
)
RUMOR_KEYWORDS = (
    "rumor",
    "rumour",
    "据传",
    "传",
    "爆料",
    "偷跑",
)
HYPE_CLAIM_KEYWORDS = (
    "绝密",
    "首次反超",
    "曝光",
    "封杀",
    "暴涨",
    "打脸",
    "翻车",
    "年化收入",
)
WEAK_EVIDENCE_HINTS = (
    "不宜直接当最终事实结论",
    "不是最终事实源",
    "不适合直接当正式事实证据",
    "更适合作为",
    "真实用户问题",
    "玩法讨论的入口",
)
COMMUNITY_DOMAINS = {"news.ycombinator.com", "old.reddit.com", "reddit.com", "github.com"}
OFFICIAL_DOMAINS = {"openai.com", "anthropic.com", "huggingface.co", "blog.google", "deepmind.google", "googleblog.com"}
MAINSTREAM_MEDIA_DOMAINS = {
    "wired.com",
    "nytimes.com",
    "theverge.com",
    "techcrunch.com",
    "infoq.com",
    "36kr.com",
    "qbitai.com",
    "jiqizhixin.com",
    "geekpark.net",
    "sspai.com",
    "zhihu.com",
    "mp.weixin.qq.com",
}
CHINESE_MAINSTREAM_MARKERS = ("量子位", "机器之心", "智东西", "极客公园", "少数派", "36氪", "知乎", "微信")


@dataclass
class Candidate:
    packet_path: Path
    packet_title: str
    packet_key: str
    canonical_url: str
    source_id: str
    source_name: str
    platform: str
    primary_source: str
    verification_status: str
    citation_reliability: str
    heat_hint: str
    summary: str
    topic_tags: str
    published_at: str
    captured_at: str
    visual_status: str
    deep_article_paths: list[Path]
    asset_paths: list[Path]
    topic_key: str
    score_breakdown: dict[str, int]
    total_score: int
    mainstream_bias_score: int
    blended_priority_score: int
    why_in_top20: str
    risks: str
    visual_assets: str
    recent_duplicate_reason: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize a truthful baseline Top20 screening pack from the real manifest.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical date in YYYY-MM-DD.")
    parser.add_argument("--manifest-path", default="", help="Existing market-source-manifest path. Defaults to the canonical path for --date.")
    parser.add_argument("--output-path", default="", help="Top20 pack output path. Defaults to the canonical path for --date.")
    parser.add_argument("--runtime-log-path", default="", help="Runtime state output path. Defaults to the canonical path for --date.")
    parser.add_argument("--limit", type=int, default=20, help="Maximum number of candidates to materialize.")
    parser.add_argument("--lookback-hours", type=int, default=120, help="Recent-topic duplicate guard lookback window.")
    parser.add_argument("--write", action="store_true", help="Persist the generated pack and runtime log.")
    return parser.parse_args()


def clean(value: str, fallback: str = "n/a") -> str:
    text = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return text if text else fallback


def normalize_text(value: str) -> str:
    return NORMALIZE_TEXT_RE.sub("", clean(value, "").lower())


def tokenize(value: str) -> set[str]:
    return {
        token
        for token in TOKEN_RE.findall(clean(value, "").lower())
        if token and token not in GENERIC_TITLE_TOKENS
    }


def extract_paths_from_manifest(manifest_path: Path, section_header: str) -> list[Path]:
    current_section = ""
    paths: list[Path] = []
    for raw_line in manifest_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            current_section = line.strip()
            continue
        if current_section != section_header:
            continue
        path_match = PATH_FIELD_RE.search(line)
        if path_match:
            paths.append(Path(path_match.group(1)).expanduser())
            continue
        tick_match = BACKTICK_PATH_RE.search(line.strip())
        if tick_match:
            candidate = Path(tick_match.group(1)).expanduser()
            if candidate.is_absolute():
                paths.append(candidate)
    deduped: list[Path] = []
    for path in paths:
        if path.exists() and path not in deduped:
            deduped.append(path)
    return deduped


def manifest_counts(manifest_path: Path) -> dict[str, str]:
    fields = {}
    for raw_line in manifest_path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        match = re.match(r"^- `([^`]+)`: `?([^`]*)`?$", stripped)
        if match:
            fields[match.group(1)] = clean(match.group(2), "")
    return fields


def default_manifest_path(date_text: str) -> Path:
    return LOG_DIR / f"{day_token(date_text)}__market-source-manifest.md"


def default_output_path(date_text: str) -> Path:
    return TOPIC_DIR / f"{day_token(date_text)}__top20-screening-pack.md"


def default_runtime_log_path(date_text: str) -> Path:
    return LOG_DIR / f"{day_token(date_text)}__market-scout-runtime-state.md"


def candidate_topic_key(packet_key: str, token: str) -> str:
    base = clean(packet_key, "").lower()
    base = re.sub(r"^\d{8}__", "", base)
    base = re.sub(r"[^a-z0-9_]+", "_", base)
    base = re.sub(r"_+", "_", base).strip("_")
    if not base:
        base = f"top20_candidate_{token}"
    if not base.endswith(token):
        base = f"{base}_{token}"
    return base


def recency_score(raw_published_at: str, raw_captured_at: str, date_text: str) -> int:
    ts = parse_cst(raw_published_at) or parse_cst(raw_captured_at)
    if ts is None:
        return 1
    end_dt = datetime.combine(date.fromisoformat(date_text), datetime.strptime(BUSINESS_WINDOW_END, "%H:%M").time(), tzinfo=ts.tzinfo)
    age_hours = max((end_dt - ts).total_seconds() / 3600.0, 0.0)
    if age_hours <= 18:
        return 3
    if age_hours <= 48:
        return 2
    return 1


def published_age_hours(raw_published_at: str, raw_captured_at: str, date_text: str) -> float | None:
    ts = parse_cst(raw_published_at) or parse_cst(raw_captured_at)
    if ts is None:
        return None
    end_dt = datetime.combine(date.fromisoformat(date_text), datetime.strptime(BUSINESS_WINDOW_END, "%H:%M").time(), tzinfo=ts.tzinfo)
    return max((end_dt - ts).total_seconds() / 3600.0, 0.0)


def should_exclude_stale_nontrend(source_id: str, raw_published_at: str, raw_captured_at: str, date_text: str) -> bool:
    if source_id.startswith("trend__"):
        return False
    age_hours = published_age_hours(raw_published_at, raw_captured_at, date_text)
    if age_hours is None:
        return False
    return age_hours > 48


def propagation_score(source_id: str, deep_article_count: int, summary: str) -> int:
    lowered = f"{source_id} {summary}".lower()
    if source_id.startswith(("trend__hn", "trend__reddit", "trend__github", "trend__zhihu", "trend__weibo", "trend__feigua", "trend__newrank")):
        return 3
    if deep_article_count >= 1 and ("双平台" in summary or "多平台" in summary or "high heat" in lowered):
        return 3
    if source_id.startswith(("wechat__", "web__", "youtube__")) or deep_article_count >= 1:
        return 2
    return 1


def breakout_score(text: str, source_id: str) -> int:
    lowered = text.lower()
    if source_id.startswith(("trend__hn", "trend__reddit", "trend__zhihu", "trend__weibo", "trend__feigua")):
        return 3
    if any(keyword in lowered for keyword in HEAT_KEYWORDS):
        return 3
    if re.search(r"\b\d{2,}\b", lowered):
        return 2
    return 1


def track_fit_score(text: str) -> int:
    lowered = text.lower()
    hits = sum(1 for keyword in FIT_KEYWORDS if keyword in lowered)
    if hits >= 3:
        return 3
    if hits >= 1:
        return 2
    return 0


def extendability_score(summary: str, deep_article_count: int, source_id: str) -> int:
    if deep_article_count >= 1:
        return 3
    if len(summary) >= 70 or source_id.startswith(("trend__", "wechat__", "web__techcrunch", "web__infoq", "web__qbitai", "web__zhidx", "web__36kr")):
        return 2
    return 1


def hard_data_score(summary: str, canonical_url: str, primary_source: str, published_at: str) -> int:
    lowered = summary.lower()
    has_numbers = bool(re.search(r"\b\d+(?:\.\d+)?\b", lowered))
    has_link = canonical_url not in {"", "n/a", "unknown"}
    has_time = published_at not in {"", "n/a", "unknown"}
    if primary_source == "yes" and has_link and (has_numbers or has_time):
        return 3
    if has_link and (has_numbers or primary_source in {"yes", "partial"}):
        return 2
    return 1


def visual_score(visual_status: str, deep_article_count: int, asset_count: int) -> int:
    lowered = clean(visual_status, "").lower()
    if "detected" in lowered and (deep_article_count >= 1 or asset_count >= 1):
        return 3
    if "detected" in lowered:
        return 2
    return 1


def platform_adapt_score(title: str, summary: str) -> int:
    lowered = f"{title} {summary}".lower()
    if any(keyword in lowered for keyword in TECHNICAL_ONLY_KEYWORDS):
        return 1
    if any(keyword in lowered for keyword in CONTROVERSY_KEYWORDS) or re.search(r"\blaunch\b|\bipo\b|\bbenchmark\b", lowered):
        return 3
    return 2


def discussion_score(source_id: str, title: str, summary: str, deep_article_count: int) -> int:
    lowered = f"{title} {summary}".lower()
    if source_id.startswith(("trend__",)) or any(keyword in lowered for keyword in CONTROVERSY_KEYWORDS):
        return 3
    if deep_article_count >= 1 or "评论" in summary or "discussion" in lowered:
        return 2
    return 1


def primary_source_score(primary_source: str) -> int:
    mapping = {"yes": 3, "partial": 2, "no": 1}
    return mapping.get(clean(primary_source, "").lower(), 1)


def lowered_title_summary(title: str, summary: str) -> str:
    return f"{clean(title, '')} {clean(summary, '')}".lower()


def is_promotional_or_meta(title: str, summary: str) -> bool:
    lowered = lowered_title_summary(title, summary)
    return any(keyword in lowered for keyword in PROMO_OR_META_KEYWORDS)


def is_roundup_style(title: str) -> bool:
    lowered = clean(title, "").lower()
    separator_count = lowered.count("；") + lowered.count("|") + lowered.count("丨")
    return separator_count >= 1 or any(keyword in lowered for keyword in ROUNDUP_TITLE_KEYWORDS)


def is_rumor_like(title: str) -> bool:
    lowered = clean(title, "").lower()
    if lowered.startswith("传"):
        return True
    return any(keyword in lowered for keyword in RUMOR_KEYWORDS)


def has_claim_evidence_mismatch(title: str, summary: str, primary_source: str) -> bool:
    lowered = lowered_title_summary(title, summary)
    has_claim = any(keyword in lowered for keyword in HYPE_CLAIM_KEYWORDS)
    has_weak_hint = any(keyword in lowered for keyword in WEAK_EVIDENCE_HINTS)
    return has_claim and (has_weak_hint or primary_source != "yes")


def clamp_score(value: int) -> int:
    return max(0, min(value, 3))


def apply_quality_adjustments(
    breakdown: dict[str, int],
    *,
    title: str,
    summary: str,
    primary_source: str,
    deep_article_count: int,
) -> dict[str, int]:
    adjusted = dict(breakdown)
    if primary_source == "no" and deep_article_count == 0:
        adjusted["数据硬度"] = min(adjusted["数据硬度"], 1)
        adjusted["可延展性"] = min(adjusted["可延展性"], 2)

    if is_promotional_or_meta(title, summary):
        adjusted["可延展性"] -= 2
        adjusted["平台适配潜力"] -= 2
        adjusted["讨论度 / 争议度"] -= 2

    if is_roundup_style(title):
        adjusted["数据硬度"] -= 1
        adjusted["平台适配潜力"] -= 1
        adjusted["讨论度 / 争议度"] -= 1

    if is_rumor_like(title) and primary_source != "yes":
        adjusted["数据硬度"] -= 2
        adjusted["一手性"] -= 1

    if has_claim_evidence_mismatch(title, summary, primary_source):
        adjusted["数据硬度"] -= 2
        adjusted["平台适配潜力"] -= 1
        if deep_article_count == 0:
            adjusted["可延展性"] -= 1

    return {key: clamp_score(value) for key, value in adjusted.items()}


def diversity_group(source_id: str) -> str:
    lowered = clean(source_id, "").lower()
    if lowered.startswith("trend__hn"):
        return "hn"
    if lowered.startswith("trend__reddit"):
        return "reddit"
    if lowered.startswith("github_trending"):
        return "github"
    if lowered.startswith("wechat__"):
        return "wechat"
    if lowered.startswith("web__"):
        return "web"
    if lowered.startswith("youtube__"):
        return "youtube"
    if lowered.startswith("trend__"):
        return "trend_other"
    return lowered.split("__", 1)[0] or lowered


def rebalance_diversity(candidates: list[Candidate], limit: int) -> list[Candidate]:
    if len(candidates) <= 1:
        return candidates[:limit]

    first_band_limit = min(limit, 8)
    first_band_cap = 2
    selected: list[Candidate] = []
    selected_ids: set[int] = set()
    first_band_counts: dict[str, int] = {}

    for candidate in candidates:
        if len(selected) >= first_band_limit:
            break
        group = diversity_group(candidate.source_id)
        if first_band_counts.get(group, 0) >= first_band_cap:
            continue
        selected.append(candidate)
        selected_ids.add(id(candidate))
        first_band_counts[group] = first_band_counts.get(group, 0) + 1

    if len(selected) < first_band_limit:
        for candidate in candidates:
            if id(candidate) in selected_ids:
                continue
            selected.append(candidate)
            selected_ids.add(id(candidate))
            if len(selected) >= first_band_limit:
                break

    for candidate in candidates:
        if id(candidate) in selected_ids:
            continue
        selected.append(candidate)
        selected_ids.add(id(candidate))
        if len(selected) >= limit:
            break

    return selected[:limit]


def score_breakdown(packet, extra_fields: dict[str, str], deep_article_paths: list[Path], asset_paths: list[Path], date_text: str) -> dict[str, int]:
    published_at = clean(extra_fields.get("published_at", ""), "unknown")
    combined_text = " ".join(
        [
            packet.title,
            packet.summary,
            packet.topic_tags,
            packet.heat_hint,
            clean(extra_fields.get("source_name", ""), packet.source_id),
        ]
    )
    breakdown = {
        "一手性": primary_source_score(packet.primary_source),
        "传播性": propagation_score(packet.source_id, len(deep_article_paths), packet.summary),
        "破圈性": breakout_score(combined_text, packet.source_id),
        "赛道匹配": track_fit_score(combined_text),
        "可延展性": extendability_score(packet.summary, len(deep_article_paths), packet.source_id),
        "数据硬度": hard_data_score(packet.summary, packet.canonical_url, packet.primary_source, published_at),
        "视觉素材丰富度": visual_score(extra_fields.get("visual_evidence_status", ""), len(deep_article_paths), len(asset_paths)),
        "平台适配潜力": platform_adapt_score(packet.title, packet.summary),
        "时效窗口": recency_score(published_at, packet.captured_at, date_text),
        "讨论度 / 争议度": discussion_score(packet.source_id, packet.title, packet.summary, len(deep_article_paths)),
    }
    return apply_quality_adjustments(
        breakdown,
        title=packet.title,
        summary=packet.summary,
        primary_source=packet.primary_source,
        deep_article_count=len(deep_article_paths),
    )


def score_total(breakdown: dict[str, int]) -> int:
    return sum(max(value, 0) for value in breakdown.values())


def candidate_domains(canonical_url: str) -> set[str]:
    cleaned = clean(canonical_url, "")
    if "://" not in cleaned:
        return set()
    return {urlparse(cleaned).netloc.lower().lstrip("www.")}


def mainstream_bias_score(packet, extra_fields: dict[str, str], deep_article_paths: list[Path]) -> int:
    score = 0
    domains = candidate_domains(packet.canonical_url)
    source_name = clean(extra_fields.get("source_name", ""), "")
    title = clean(packet.title, "")
    lowered_title = title.lower()
    if any(domain in OFFICIAL_DOMAINS for domain in domains):
        score += 4
    if any(domain in MAINSTREAM_MEDIA_DOMAINS for domain in domains):
        score += 3
    if any(domain in COMMUNITY_DOMAINS for domain in domains):
        score -= 3
    if any(marker in source_name for marker in CHINESE_MAINSTREAM_MARKERS):
        score += 2
    if re.search(r"[\u4e00-\u9fff]", title):
        score += 1
    if deep_article_paths:
        score += 1
    if any(token in lowered_title for token in ("hn", "reddit", "show hn", "github")):
        score -= 2
    return score


def breakdown_text(breakdown: dict[str, int]) -> str:
    return " / ".join(f"{key}={value}" for key, value in breakdown.items())


def build_why(packet, deep_article_paths: list[Path], asset_paths: list[Path], breakdown: dict[str, int], bias_score: int) -> str:
    reasons: list[str] = []
    if packet.primary_source in {"yes", "partial"}:
        reasons.append(f"{packet.primary_source} source")
    if packet.source_id.startswith("trend__"):
        reasons.append("有明确扩散热度入口")
    if deep_article_paths:
        reasons.append(f"已存在 {len(deep_article_paths)} 篇 deep article")
    if asset_paths:
        reasons.append(f"已存在 {len(asset_paths)} 条 asset chain")
    if breakdown["时效窗口"] >= 3:
        reasons.append("仍处业务窗内高时效")
    if breakdown["讨论度 / 争议度"] >= 3:
        reasons.append("具备天然讨论空间")
    if breakdown["赛道匹配"] >= 3:
        reasons.append("与 AI / Agent / 一人公司主线高度一致")
    if bias_score >= 4:
        reasons.append("更接近官方 / 主流媒体共识")
    return "；".join(reasons) if reasons else "具备进入候选池所需的基础信号。"


def build_risks(packet, published_at: str, deep_article_paths: list[Path], breakdown: dict[str, int]) -> str:
    risks: list[str] = []
    if packet.primary_source != "yes":
        risks.append("正式引用前仍需补一手或原始上下文")
    if clean(published_at, "unknown") in {"unknown", "n/a"}:
        risks.append("发布时间不够硬")
    if not deep_article_paths:
        risks.append("缺全文深抓，角度延展需谨慎")
    if breakdown["平台适配潜力"] <= 1:
        risks.append("题目偏技术，泛流量平台适配有限")
    if breakdown["数据硬度"] <= 1:
        risks.append("硬数据偏少")
    return "；".join(risks) if risks else "主要风险可控。"


def build_visual_assets(packet, deep_article_paths: list[Path], asset_paths: list[Path], extra_fields: dict[str, str]) -> str:
    suggestions: list[str] = []
    if clean(extra_fields.get("visual_evidence_status", ""), "").lower().startswith("visual-inputs-detected"):
        suggestions.append("source packet 已探测原始视觉输入")
    if deep_article_paths:
        suggestions.append("deep article 首屏 / 标题区截图")
    if asset_paths:
        suggestions.append("asset chain 对应产品 / 官方页图")
    if not suggestions:
        suggestions.append("优先使用标题区或原始页面 hero 区截图")
    return " / ".join(suggestions)


def normalize_title_key(title: str) -> str:
    return normalize_text(title)


def filter_duplicates(candidates: Iterable[Candidate]) -> list[Candidate]:
    chosen_by_url: dict[str, Candidate] = {}
    chosen_by_title: dict[str, Candidate] = {}
    for candidate in candidates:
        keys = []
        if candidate.canonical_url not in {"n/a", "unknown", ""}:
            keys.append(("url", clean(candidate.canonical_url, "")))
        normalized_title = normalize_title_key(candidate.packet_title)
        if normalized_title:
            keys.append(("title", normalized_title))

        existing: Candidate | None = None
        for key_type, key in keys:
            existing = (chosen_by_url if key_type == "url" else chosen_by_title).get(key)
            if existing:
                break
        if existing and existing.total_score >= candidate.total_score:
            continue
        if existing:
            if existing.canonical_url not in {"n/a", "unknown", ""}:
                chosen_by_url.pop(clean(existing.canonical_url, ""), None)
            old_title_key = normalize_title_key(existing.packet_title)
            if old_title_key:
                chosen_by_title.pop(old_title_key, None)
        if candidate.canonical_url not in {"n/a", "unknown", ""}:
            chosen_by_url[clean(candidate.canonical_url, "")] = candidate
        if normalized_title:
            chosen_by_title[normalized_title] = candidate
    deduped = list({id(item): item for item in [*chosen_by_url.values(), *chosen_by_title.values()]}.values())
    deduped.sort(key=lambda item: (item.total_score, len(item.deep_article_paths), item.primary_source == "yes"), reverse=True)
    return deduped


def load_candidates(manifest_path: Path, date_text: str, lookback_hours: int) -> tuple[list[Candidate], list[str]]:
    token = day_token(date_text)
    source_paths = extract_paths_from_manifest(manifest_path, MANIFEST_SOURCE_SECTION)
    deep_paths = extract_paths_from_manifest(manifest_path, MANIFEST_DEEP_SECTION)
    asset_paths = extract_paths_from_manifest(manifest_path, MANIFEST_ASSET_SECTION)

    deep_by_packet: dict[str, list[Path]] = {}
    for path in deep_paths:
        article = parse_deep_article(path)
        packet_ref = clean(article.source_packet_path, "")
        if not packet_ref:
            continue
        deep_by_packet.setdefault(packet_ref, []).append(path)

    asset_by_packet: dict[str, list[Path]] = {}
    for path in asset_paths:
        fields = parse_fields(path)
        packet_ref = clean(fields.get("source_packet_path", ""), "")
        if packet_ref:
            asset_by_packet.setdefault(packet_ref, []).append(path)

    raw_candidates: list[Candidate] = []
    excluded_reasons: list[str] = []
    for path in source_paths:
        packet = parse_packet(path)
        extra_fields = parse_fields(path)
        combined_text = " ".join([packet.title, packet.summary, packet.topic_tags, packet.heat_hint])
        fit_score = track_fit_score(combined_text)
        if fit_score <= 0:
            excluded_reasons.append(f"skip:not_ai_enough:{packet.title}")
            continue
        deep_for_packet = deep_by_packet.get(str(path), [])
        asset_for_packet = asset_by_packet.get(str(path), [])
        published_at = clean(extra_fields.get("published_at", ""), "unknown")
        if should_exclude_stale_nontrend(packet.source_id, published_at, packet.captured_at, date_text):
            excluded_reasons.append(f"skip:stale_nontrend:{packet.title}:{published_at}")
            continue
        packet_key = clean(extra_fields.get("packet_key", ""), packet.packet_id)
        topic_key = candidate_topic_key(packet_key, token)
        conflicts = find_recent_conflicts(
            topic_key=topic_key,
            title=packet.title,
            approved_angle=packet.summary,
            lookback_hours=lookback_hours,
        )
        if conflicts:
            conflict = conflicts[0]
            excluded_reasons.append(f"skip:recent_duplicate:{packet.title}:{conflict.reason}:{conflict.record.topic_key}")
            continue
        breakdown = score_breakdown(packet, extra_fields, deep_for_packet, asset_for_packet, date_text)
        breakdown["赛道匹配"] = max(breakdown["赛道匹配"], fit_score)
        total = score_total(breakdown)
        bias_score = mainstream_bias_score(packet, extra_fields, deep_for_packet)
        raw_candidates.append(
            Candidate(
                packet_path=path,
                packet_title=packet.title,
                packet_key=packet_key,
                canonical_url=packet.canonical_url,
                source_id=packet.source_id,
                source_name=clean(extra_fields.get("source_name", ""), packet.source_id),
                platform=packet.platform,
                primary_source=packet.primary_source,
                verification_status=packet.verification_status,
                citation_reliability=packet.citation_reliability,
                heat_hint=packet.heat_hint,
                summary=packet.summary,
                topic_tags=packet.topic_tags,
                published_at=published_at,
                captured_at=packet.captured_at,
                visual_status=clean(extra_fields.get("visual_evidence_status", ""), "n/a"),
                deep_article_paths=deep_for_packet,
                asset_paths=asset_for_packet,
                topic_key=topic_key,
                score_breakdown=breakdown,
                total_score=total,
                mainstream_bias_score=bias_score,
                blended_priority_score=total + bias_score,
                why_in_top20=build_why(packet, deep_for_packet, asset_for_packet, breakdown, bias_score),
                risks=build_risks(packet, published_at, deep_for_packet, breakdown),
                visual_assets=build_visual_assets(packet, deep_for_packet, asset_for_packet, extra_fields),
                recent_duplicate_reason="",
            )
        )

    deduped = filter_duplicates(raw_candidates)
    deduped.sort(
        key=lambda item: (
            item.blended_priority_score,
            item.total_score,
            item.mainstream_bias_score,
            primary_source_score(item.primary_source),
            len(item.deep_article_paths),
            recency_score(item.published_at, item.captured_at, date_text),
        ),
        reverse=True,
    )
    return rebalance_diversity(deduped, 200), excluded_reasons


def render_pack(date_text: str, manifest_path: Path, output_path: Path, candidates: list[Candidate], excluded_reasons: list[str]) -> str:
    counts = manifest_counts(manifest_path)
    token = day_token(date_text)
    business_status = business_window_status(date_text)
    top_candidates = candidates[:20]
    top3 = top_candidates[:3]
    next3 = top_candidates[3:9]
    holdout = candidates[20:23]
    lines = [
        "# Top20 初筛包",
        "",
        f"- `date`: `{date_text}`",
        "- `owner`: `market-scout (signal-scout runtime)`",
        f"- `generated_at`: `{format_cst(datetime.now(CN_TZ))}`",
        "- `source_scope`: `T-1 17:00 ~ T 14:30`",
        f"- `total_candidates_seen`: `{counts.get('source_packets', '0')} source packets / {counts.get('deep_articles', '0')} deep articles / {counts.get('asset_chains', '0')} asset chains`",
        f"- `top20_count`: `{len(top_candidates)}`",
        "- `delivery_lane`: `day_mainline`",
        f"- `delivery_deadline`: `{date_text} 19:00 CST`",
        f"- `scorecard_path`: `{LOG_DIR / f'{token}__top20__stage-gate-scorecard.md'}`",
        f"- `manifest_path`: `{manifest_path}`",
        f"- `business_window_status`: `{business_status}`",
        f"- `builder_mode`: `script_materialized_baseline`",
        "",
        "## 使用说明",
        "",
        "- 这是 `signal-scout` 阶段正式交付包，基于 manifest 真实文件清单脚本化预物化。",
        "- 这份包的目标是保证 day_mainline 不会停留在模板壳；后续 agent 可以继续强化排序、补证和切角。",
        "- 若后续出现 `__reworked` 版本，应以更新版本为准。",
        "",
        "## 评分框架",
        "",
        "| 维度 | 说明 | 分值 |",
        "|---|---|---|",
        "| 一手性 | 是否来自官方 / 原始口径 / 可追溯原文 | 0-3 |",
        "| 传播性 | 是否已有开发者圈 / 媒体 / 社区扩散 | 0-3 |",
        "| 破圈性 | 是否有明显争议、反差或热度突破口 | 0-3 |",
        "| 赛道匹配 | 是否契合 AI / Agent / 一人公司 / 模型 / infra / 硬件主线 | 0-3 |",
        "| 可延展性 | 是否能继续深挖成观点稿、拆解稿或复盘稿 | 0-3 |",
        "| 数据硬度 | 是否有硬链接、时间锚点、数字或原始页面 | 0-3 |",
        "| 视觉素材丰富度 | 是否有原始截图 / 产品页 / 可解释图来源 | 0-3 |",
        "| 平台适配潜力 | 是否适合微信及多平台改写 | 0-3 |",
        "| 时效窗口 | 当前业务日写它是否仍然值钱 | 0-3 |",
        "| 讨论度 / 争议度 | 是否自带讨论空间 | 0-3 |",
        "",
        "---",
        "",
        "## Top20 候选",
        "",
    ]

    for index, candidate in enumerate(top_candidates, start=1):
        lines.extend(
            [
                f"### {index}. {candidate.packet_title}",
                f"- `topic_key`: `{candidate.topic_key}`",
                f"- `title`: `{candidate.packet_title}`",
                f"- `primary_platform`: `{clean(candidate.source_name or candidate.platform, candidate.platform)}`",
                f"- `published_at`: `{clean(candidate.published_at, candidate.captured_at)}`",
                f"- `original_link`: `{clean(candidate.canonical_url)}`",
                f"- `score_total`: `{candidate.total_score} / 30`",
                f"- `mainstream_bias_score`: `{candidate.mainstream_bias_score}`",
                f"- `blended_priority_score`: `{candidate.blended_priority_score}`",
                f"- `score_breakdown`: `{breakdown_text(candidate.score_breakdown)}`",
                f"- `signal_summary`: `{clean(candidate.summary)}`",
                f"- `why_in_top20`: `{candidate.why_in_top20}`",
                f"- `visual_assets`: `{candidate.visual_assets}`",
                f"- `risks`: `{candidate.risks}`",
                f"- `source_packet`: `{candidate.packet_path}`",
            ]
        )
        if candidate.deep_article_paths:
            lines.append(f"- `deep_article`: `{candidate.deep_article_paths[0]}`")
        if candidate.asset_paths:
            lines.append(f"- `asset_chain`: `{candidate.asset_paths[0]}`")
        lines.extend(["", "---", ""])

    lines.extend(["## 结论", ""])
    lines.append("### top3_must_watch")
    lines.append("")
    if top3:
        lines.extend(["| 排名 | topic_key | 理由 |", "|---|---|---|"])
        for index, candidate in enumerate(top3, start=1):
            reason = " / ".join(
                part
                for part in [
                    "高时效" if candidate.score_breakdown["时效窗口"] >= 3 else "",
                    "强扩散" if candidate.score_breakdown["传播性"] >= 3 else "",
                    "有 deep article" if candidate.deep_article_paths else "",
                    "主线高度匹配" if candidate.score_breakdown["赛道匹配"] >= 3 else "",
                ]
                if part
            ) or "基础信号完整"
            lines.append(f"| #{index} | `{candidate.topic_key}` | {reason} |")
    else:
        lines.append("- `none`")

    lines.extend(["", "### top6_strong_pool", ""])
    if next3:
        lines.extend(["| 排名 | topic_key | 理由 |", "|---|---|---|"])
        for index, candidate in enumerate(next3, start=4):
            lines.append(f"| #{index} | `{candidate.topic_key}` | {candidate.why_in_top20} |")
    else:
        lines.append("- `none`")

    lines.extend(["", "### holdout_watchlist", ""])
    if holdout:
        lines.extend(["| topic_key | holdout 原因 |", "|---|---|"])
        for candidate in holdout:
            lines.append(f"| `{candidate.topic_key}` | {candidate.risks} |")
    else:
        lines.append("- `none`")

    lines.extend(
        [
            "",
            "### supply_risk",
            "",
            f"- `kept_candidates`: `{len(top_candidates)}`",
            f"- `manifest_source_packets`: `{counts.get('source_packets', '0')}`",
            f"- `manifest_deep_articles`: `{counts.get('deep_articles', '0')}`",
            f"- `excluded_recent_duplicates`: `{sum(1 for item in excluded_reasons if item.startswith('skip:recent_duplicate'))}`",
            f"- `excluded_low_fit`: `{sum(1 for item in excluded_reasons if item.startswith('skip:not_ai_enough'))}`",
            f"- `notes`: `本包由脚本预物化生成，确保 day_mainline 不会停留在模板壳；若要冲 premium，需要后续岗位继续补证、重排、改角度。`",
            "",
            "## 本包交付约束",
            "",
            "- **不得自行放行**：本包为 `market-scout` 初筛交付，是否进入下一工序由 `market-editor` 最新 scorecard 决定。",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_runtime_log(date_text: str, manifest_path: Path, output_path: Path, candidates: list[Candidate], excluded_reasons: list[str]) -> str:
    top_titles = ", ".join(candidate.packet_title for candidate in candidates[:5]) or "none"
    duplicate_examples = [
        item for item in excluded_reasons if item.startswith("skip:recent_duplicate")
    ][:5]
    lines = [
        "# Market Scout Runtime State",
        "",
        f"- `date`: `{date_text}`",
        f"- `generated_at`: `{format_cst(datetime.now(CN_TZ))}`",
        f"- `manifest_path`: `{manifest_path}`",
        f"- `output_pack_path`: `{output_path}`",
        f"- `builder_status`: `materialized_baseline`",
        f"- `materialized_count`: `{min(len(candidates), 20)}`",
        f"- `raw_candidate_count_after_filters`: `{len(candidates)}`",
        f"- `excluded_count`: `{len(excluded_reasons)}`",
        f"- `top_titles`: `{top_titles}`",
        "",
        "## Exclusions",
        "",
    ]
    if excluded_reasons:
        for item in excluded_reasons[:20]:
            lines.append(f"- `{item}`")
    else:
        lines.append("- `none`")
    if duplicate_examples:
        lines.extend(["", "## Duplicate Guard Examples", ""])
        for item in duplicate_examples:
            lines.append(f"- `{item}`")
    return "\n".join(lines).rstrip() + "\n"


def resolve_path(raw: str, fallback: Path) -> Path:
    value = clean(raw, "")
    if not value:
        return fallback
    return Path(value).expanduser()


def main() -> None:
    args = parse_args()
    manifest_path = resolve_path(args.manifest_path, default_manifest_path(args.date))
    output_path = resolve_path(args.output_path, default_output_path(args.date))
    runtime_log_path = resolve_path(args.runtime_log_path, default_runtime_log_path(args.date))

    if not manifest_path.exists():
        raise SystemExit(f"MANIFEST_MISSING {manifest_path}")

    candidates, excluded_reasons = load_candidates(manifest_path, args.date, lookback_hours=args.lookback_hours)
    rendered_pack = render_pack(args.date, manifest_path, output_path, candidates, excluded_reasons)
    rendered_runtime = render_runtime_log(args.date, manifest_path, output_path, candidates, excluded_reasons)

    if args.write:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        runtime_log_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered_pack, encoding="utf-8")
        runtime_log_path.write_text(rendered_runtime, encoding="utf-8")

    print(f"PACK_PATH={output_path}")
    print(f"RUNTIME_LOG_PATH={runtime_log_path}")
    print(f"MATERIALIZED_COUNT={min(len(candidates), max(args.limit, 0))}")
    print(f"RAW_CANDIDATE_COUNT={len(candidates)}")
    print(f"EXCLUDED_COUNT={len(excluded_reasons)}")
    if candidates:
        print(f"TOP1={candidates[0].topic_key} | {candidates[0].packet_title}")


if __name__ == "__main__":
    main()

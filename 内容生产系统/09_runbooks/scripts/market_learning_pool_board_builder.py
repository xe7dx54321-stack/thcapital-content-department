#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime
from html import escape
from pathlib import Path
from statistics import median
from typing import Any
from zoneinfo import ZoneInfo

import market_learning_memo_builder as memo_builder
import market_learning_knowledge_builder as knowledge_builder
import market_ops_dashboard_builder as dashboard_builder


CN_TZ = ZoneInfo("Asia/Shanghai")
ROOT = dashboard_builder.ROOT.resolve()
FRONTSTAGE_DIR = ROOT / "11_frontstage"
LOG_ROOT = ROOT / "10_logs"
DRAFT_PACK_ROOT = ROOT / "05_draft_packs"
BRAND_ROOT = ROOT / "08_brand_assets"
TOPIC_CANDIDATE_DIR = dashboard_builder.TOPIC_CANDIDATE_DIR
SOURCE_PACKET_ROOT = ROOT / "02_topic_radar" / "source_packets"
CONSOLE_STATE_DIR = FRONTSTAGE_DIR / "_console_state"
OPTIMIZATION_STATE_PATH = CONSOLE_STATE_DIR / "learning_optimization_state.json"
LATEST_RULEBOOK_PATH = BRAND_ROOT / "latest__head-media-learning-rulebook-v1.md"
STRATEGIC_LEARNING_SOURCES = [
    "赛博禅心",
    "数字生命卡兹克",
    "饼干哥哥AGI",
    "袋鼠帝AI客栈",
]

PLATFORM_PRIORITY = ["wechat", "xiaohongshu", "zhihu", "bilibili", "toutiao", "baijiahao", "x"]
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
URL_RE = re.compile(r"https?://")
IMAGE_MD_RE = re.compile(r"!\[.*?\]\((.*?)\)")
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?(?:%|倍|亿元|亿|万|nm|卡|个|年|月|秒)")
JUDGMENT_RE = re.compile(r"真正该看|真正值得看|别只把|别只看|不只是|不是.+而是|我更想说|先给结论|这才是", re.S)
BACKGROUND_RE = re.compile(r"发生了什么|先补背景|先把背景|先说事实|背景|这次|原始事件")
PACKAGING_TOKENS = ("## 推荐包装", "## 标题候选", "## 封面包装", "## 引用来源", "## 参考来源")
STYLE_PLAYBOOK = [
    {
        "content_type": "事件科普 / 热点解释",
        "audience": "刚听说这件事、但上下文还不完整的泛 AI 读者",
        "style_rule": "先用白话把对象、变化、why now 讲清，再保留少量必要术语做精确表达。",
        "do": "判断先行，但前 10%-15% 内补齐背景和证据锚点。",
        "avoid": "一上来堆框架、堆术语，让读者半天不知道发生了什么。",
    },
    {
        "content_type": "产品推荐 / 工具体验",
        "audience": "想马上试、想知道值不值得用的实操型读者",
        "style_rule": "按场景、动作、收益来写；可以用体验叙述，但核心是降低试用门槛。",
        "do": "多放界面截图、流程卡、前后对比，用真实操作感替代空泛形容词。",
        "avoid": "只有“很好用 / 很惊艳”的感受，没有步骤、边界和证据。",
    },
    {
        "content_type": "产业判断 / 商业分析",
        "audience": "从业者、投资人、对商业含义敏感的高意图读者",
        "style_rule": "保持判断力度，但所有专业表达都要回到业务含义、商业变量和风险边界。",
        "do": "财务、竞争、分发、供给链等术语可以用，但要解释“这对谁有影响”。",
        "avoid": "把文章写成抽象行业评论，读者读完不知道能带走什么判断。",
    },
    {
        "content_type": "教程 / Builder 拆解",
        "audience": "开发者、产品经理、AI builder、人群更愿意为方法买单",
        "style_rule": "过程感优先，写清怎么判断、怎么验证、卡在哪、适用边界是什么。",
        "do": "多用步骤卡、结构图、变量表，给人“看完能照着做”的感觉。",
        "avoid": "只给结论不给路径，只晒结果不说前提。",
    },
    {
        "content_type": "观点 / 争议型题材",
        "audience": "已经感知到热度、想看更高层判断的人",
        "style_rule": "第一屏亮立场，但立刻补证据和边界，避免把“敢说”写成“乱说”。",
        "do": "把误判点、反直觉点和证据链一并前置。",
        "avoid": "只有态度没有证据，或者只用狠话制造情绪。",
    },
]
TOPIC_LANE_RULES = [
    {
        "label": "融资 / 商业化 / 资本信号",
        "tokens": (
            "融资",
            "估值",
            "ipo",
            "贷款",
            "loan",
            "revenue",
            "收入",
            "营收",
            "商业化",
            "funding",
            "valuation",
            "订单",
        ),
    },
    {
        "label": "机器人 / 硬件 / 具身智能",
        "tokens": (
            "机器人",
            "robot",
            "具身",
            "硬件",
            "芯片",
            "cpu",
            "gpu",
            "macbook",
            "factory",
            "工厂",
            "siri",
        ),
    },
    {
        "label": "安全 / 风险 / 漏洞",
        "tokens": (
            "安全",
            "漏洞",
            "vuln",
            "security",
            "bug",
            "风险",
            "风险提示",
            "挖穿",
        ),
    },
    {
        "label": "视频 / 多模态 / 语音",
        "tokens": (
            "sora",
            "视频",
            "video",
            "tts",
            "voice",
            "语音",
            "多模态",
            "cloning",
        ),
    },
    {
        "label": "开源 / Infra / 推理优化",
        "tokens": (
            "开源",
            "github",
            "repo",
            "pr #",
            "llama.cpp",
            "kv",
            "quant",
            "量化",
            "推理",
            "infra",
            "cache",
            "benchmark",
            "本地跑",
        ),
    },
    {
        "label": "模型 / 研究进展",
        "tokens": (
            "模型",
            "研究",
            "paper",
            "论文",
            "world model",
            "世界模型",
            "iclr",
            "agent",
            "deep research",
            "coder",
            "训练",
        ),
    },
    {
        "label": "行业落地 / 医疗 / 场景翻译",
        "tokens": (
            "医生",
            "医疗",
            "场景",
            "用户",
            "陪伴",
            "入口",
            "产品",
            "网站",
            "app",
        ),
    },
    {
        "label": "社会影响 / 就业伦理",
        "tokens": (
            "失业",
            "就业",
            "伦理",
            "human",
            "maher",
            "tristan harris",
            "公众",
            "反人类",
        ),
    },
]
LANE_REASON_PLAYBOOK = {
    "融资 / 商业化 / 资本信号": "这类题能直接回答“钱往哪流、商业上有没有成立”，更容易承接投资判断和行业观察。",
    "机器人 / 硬件 / 具身智能": "这类题自带强画面和具象对象，但如果没有用户 stakes，容易只剩酷炫而缺少转译。",
    "安全 / 风险 / 漏洞": "这类题兼具反常识、风险感和专业背书，既适合传播，也适合建立判断力。",
    "视频 / 多模态 / 语音": "这类题更容易被头部号选中，因为天然有产品感、演示感和大众入口。",
    "开源 / Infra / 推理优化": "这类题适合做专业壁垒和品牌判断，但首屏必须更早翻译成普通读者能感知的意义。",
    "模型 / 研究进展": "这类题能代表前沿，但需要快速翻译成“到底多了什么能力、对谁有影响”。",
    "行业落地 / 医疗 / 场景翻译": "这类题更容易让读者立刻感到 stakes，头部号常用它来拉宽受众。",
    "社会影响 / 就业伦理": "这类题带公共讨论张力，容易出圈，但需要更强的边界和多方视角。",
    "综合 / 其他": "这类题材目前还偏混合，说明系统需要继续积累更稳定的分类经验。",
}
OPTIMIZATION_OWNER_RULES = {
    "成品化清理不够彻底": {
        "owner": "content-writer / content-polish",
        "landing_layer": "skills + draft-pack final sweep",
        "landing_targets": [
            "09_runbooks/skills/th-draft-pack/SKILL.md",
            "09_runbooks/skills/th-content-polish/SKILL.md",
        ],
    },
    "背景桥接还要再早": {
        "owner": "topic-approval + draft-pack + content-polish",
        "landing_layer": "skills + approved-topic handoff",
        "landing_targets": [
            "09_runbooks/skills/th-topic-approval/SKILL.md",
            "09_runbooks/skills/th-draft-pack/SKILL.md",
            "09_runbooks/skills/th-content-polish/SKILL.md",
        ],
    },
    "证据锚点还不够前置": {
        "owner": "signal-scout + writer + visual-intelligence",
        "landing_layer": "skills + visual asset plan",
        "landing_targets": [
            "09_runbooks/skills/th-topic-radar/SKILL.md",
            "09_runbooks/skills/th-market-visual-intelligence/SKILL.md",
            "09_runbooks/skills/th-content-polish/SKILL.md",
        ],
    },
    "图证落地仍弱于头部号": {
        "owner": "visual-intelligence + writer",
        "landing_layer": "visual workflow + draft-pack assets",
        "landing_targets": [
            "09_runbooks/skills/th-market-visual-intelligence/SKILL.md",
            "09_runbooks/skills/th-draft-pack/SKILL.md",
        ],
    },
    "主要缺口已转入微调层": {
        "owner": "content-review / hook-title-cover",
        "landing_layer": "post-publish optimization",
        "landing_targets": [
            "09_runbooks/skills/th-content-review/SKILL.md",
            "09_runbooks/skills/th-market-postmortem-optimizer/SKILL.md",
        ],
    },
}


@dataclass
class LearningSample:
    source_name: str
    title: str
    published_at: str
    canonical_url: str
    char_count: int
    image_count: int
    first_image_after_text_paragraphs: int | None
    hook_excerpt: str
    learning_takeaway: str
    visual_takeaway: str
    path: str


@dataclass
class StrategicRotationItem:
    source_name: str
    status: str
    status_label: str
    title: str
    published_at: str
    canonical_url: str
    learning_takeaway: str
    visual_takeaway: str
    path: str
    note: str
    source_packet_count: int
    deep_article_count: int


@dataclass
class ReadyDraftLearningView:
    topic_key: str
    topic_title: str
    approved_angle: str
    platforms: list[str]
    representative_platform: str
    representative_platform_label: str
    representative_path: str
    pack_dir: str
    preview: str
    char_count: int
    section_count: int
    visual_asset_count: int
    strengths: list[str]
    gaps: list[str]
    gap_summary: str
    has_internal_packaging: bool
    has_early_background: bool
    has_early_judgment: bool
    has_early_evidence: bool


@dataclass
class SelectionTopicView:
    topic_key: str
    title: str
    status: str
    status_label: str
    score_total: str
    signal_summary: str
    why_selected: str
    lanes: list[str]
    path: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build head-media learning pool / benchmark board")
    parser.add_argument("--date", default=datetime.now(CN_TZ).date().isoformat())
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--window-start", default="17:00")
    parser.add_argument("--window-end", default="14:30")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--write-log", action="store_true")
    return parser.parse_args()


def now_cst() -> str:
    return datetime.now(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def clean(value: Any, fallback: str = "n/a") -> str:
    return dashboard_builder.clean(str(value), fallback=fallback)


def compact(text: str, limit: int = 120) -> str:
    text = clean(text, "")
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip("，。；：, ") + "…"


def token_for_date(date_text: str) -> str:
    return dashboard_builder.day_token(date_text)


def output_paths(date_text: str) -> dict[str, Path]:
    token = token_for_date(date_text)
    return {
        "markdown": FRONTSTAGE_DIR / f"{token}__head-media-learning-board.md",
        "html": FRONTSTAGE_DIR / f"{token}__head-media-learning-board.html",
        "json": FRONTSTAGE_DIR / f"{token}__head-media-learning-board.snapshot.json",
        "log": LOG_ROOT / f"{token}__head-media-learning-board-refresh.md",
    }


def rulebook_paths(date_text: str) -> dict[str, Path]:
    token = token_for_date(date_text)
    return {
        "dated": BRAND_ROOT / f"{token}__head-media-learning-rulebook-v1.md",
        "latest": LATEST_RULEBOOK_PATH,
    }


def load_optimization_state() -> dict[str, Any]:
    if not OPTIMIZATION_STATE_PATH.exists():
        return {"by_date": {}}
    try:
        data = json.loads(OPTIMIZATION_STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"by_date": {}}
    return data if isinstance(data, dict) else {"by_date": {}}


def write_optimization_state(state: dict[str, Any]) -> None:
    CONSOLE_STATE_DIR.mkdir(parents=True, exist_ok=True)
    OPTIMIZATION_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def record_optimization_action(
    date_text: str,
    item_id: str,
    action: str,
    *,
    actor: str = "system",
    note: str = "",
) -> dict[str, Any]:
    state = load_optimization_state()
    by_date = state.setdefault("by_date", {})
    bucket = by_date.setdefault(date_text, {"dismissed_ids": [], "events": []})
    dismissed_ids = set(bucket.get("dismissed_ids") or [])
    normalized_action = "restore" if action == "restore" else "dismiss"
    if normalized_action == "dismiss":
        dismissed_ids.add(item_id)
    else:
        dismissed_ids.discard(item_id)
    bucket["dismissed_ids"] = sorted(dismissed_ids)
    events = list(bucket.get("events") or [])
    events.append(
        {
            "item_id": item_id,
            "action": normalized_action,
            "actor": actor,
            "note": note,
            "recorded_at": now_cst(),
        }
    )
    bucket["events"] = events[-200:]
    write_optimization_state(state)
    return state


def optimization_action_log(date_text: str) -> list[dict[str, Any]]:
    state = load_optimization_state()
    bucket = (state.get("by_date") or {}).get(date_text, {})
    events = bucket.get("events") or []
    return [item for item in events if isinstance(item, dict)]


def extract_paragraphs(text: str) -> list[str]:
    paragraphs: list[str] = []
    for raw_block in re.split(r"\n\s*\n", text):
        lines: list[str] = []
        for raw_line in raw_block.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or line.startswith("![](") or line.startswith("!["):
                continue
            if line.startswith(">"):
                line = line[1:].strip()
            if line.startswith("- "):
                line = line[2:].strip()
            lines.append(line)
        paragraph = clean(" ".join(lines), "")
        if paragraph:
            paragraphs.append(paragraph)
    return paragraphs


def count_visual_assets(pack_dir: Path) -> int:
    visual_dir = pack_dir / "visual-assets"
    if not visual_dir.exists():
        return 0
    return sum(1 for path in visual_dir.rglob("*") if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS)


def pick_sample_takeaway(article: memo_builder.DeepArticle) -> tuple[str, str]:
    hook_excerpt = memo_builder.format_excerpt(article.opening_paragraphs, limit=2, max_chars=140)
    if article.first_image_after_text_paragraphs in {0, 1, 2}:
        visual_takeaway = "首屏或前两段就上图，先把事件锚住，再继续展开。"
    elif article.first_image_after_text_paragraphs is not None and article.first_image_after_text_paragraphs <= 6:
        visual_takeaway = "先给判断，再很快补一张证据图，图文切换节奏比较早。"
    else:
        visual_takeaway = "首图位置相对靠后，更像是在结构展开后用图片换气。"

    opening_text = " ".join(article.opening_paragraphs[:3])
    if NUMBER_RE.search(opening_text):
        learning_takeaway = "开头直接塞进数字或对象，让读者先感到“这事是真的，而且现在就值得看”。"
    elif JUDGMENT_RE.search(opening_text):
        learning_takeaway = "首屏先抛判断句，不先做百科式背景。"
    else:
        learning_takeaway = "开头更像“对象 + 事件 + why now”同步落地，读者不容易迷路。"
    return learning_takeaway, visual_takeaway


def build_learning_samples(
    count: int,
    *,
    date_text: str,
    window_start: str,
    window_end: str,
) -> list[LearningSample]:
    samples: list[LearningSample] = []
    for article in memo_builder.select_articles(
        count,
        date_text=date_text,
        window_start=window_start,
        window_end=window_end,
    ):
        learning_takeaway, visual_takeaway = pick_sample_takeaway(article)
        samples.append(
            LearningSample(
                source_name=article.source_name,
                title=article.title,
                published_at=article.published_at,
                canonical_url=article.canonical_url,
                char_count=article.normalized_char_count,
                image_count=article.image_count,
                first_image_after_text_paragraphs=article.first_image_after_text_paragraphs,
                hook_excerpt=memo_builder.format_excerpt(article.opening_paragraphs, limit=2, max_chars=170),
                learning_takeaway=learning_takeaway,
                visual_takeaway=visual_takeaway,
                path=str(article.path),
            )
        )
    return samples


def source_packet_count_for_source(source_name: str) -> int:
    count = 0
    for path in SOURCE_PACKET_ROOT.glob("*__source-packet.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if f"`source_name`: `{source_name}`" in text:
            count += 1
    return count


def build_strategic_rotation_items(
    date_text: str,
    samples: list[LearningSample],
    *,
    freshness_days: int = 14,
) -> list[StrategicRotationItem]:
    target_day = datetime.fromisoformat(f"{date_text}T00:00:00+08:00").date()
    primary_paths = {sample.path for sample in samples}
    articles_by_source: dict[str, list[memo_builder.DeepArticle]] = {name: [] for name in STRATEGIC_LEARNING_SOURCES}

    for path in sorted(memo_builder.DEEP_ARTICLE_ROOT.glob("*__deep-article.md"), reverse=True):
        article = memo_builder.load_article(path)
        if not article or article.source_name not in articles_by_source:
            continue
        if memo_builder.article_is_future(article, target_day):
            continue
        articles_by_source[article.source_name].append(article)

    items: list[StrategicRotationItem] = []
    for source_name in STRATEGIC_LEARNING_SOURCES:
        source_packet_count = source_packet_count_for_source(source_name)
        candidates = sorted(
            articles_by_source.get(source_name, []),
            key=memo_builder.article_recency,
            reverse=True,
        )
        deep_article_count = len(candidates)
        fresh_candidates = [
            article
            for article in candidates
            if (target_day - memo_builder.article_recency(article).date()).days <= freshness_days
        ]
        rotation_pool = fresh_candidates or candidates
        selected = next((article for article in rotation_pool if str(article.path) not in primary_paths), None)
        if selected is None and rotation_pool:
            selected = rotation_pool[0]

        if selected is None:
            items.append(
                StrategicRotationItem(
                    source_name=source_name,
                    status="blocked",
                    status_label="主链待补通",
                    title="暂无可学习 deep article",
                    published_at="n/a",
                    canonical_url="n/a",
                    learning_takeaway="RSS 已接入，但这个号还没真正进入 source packet / deep article 学习主链。",
                    visual_takeaway="先补通主链，再谈图文节奏学习。",
                    path="n/a",
                    note=(
                        f"当前记录为 source_packet={source_packet_count} / deep_article={deep_article_count}。"
                        "需要先补抓源或深抓，不然学习池无法持续吸收该号。"
                    ),
                    source_packet_count=source_packet_count,
                    deep_article_count=deep_article_count,
                )
            )
            continue

        learning_takeaway, visual_takeaway = pick_sample_takeaway(selected)
        in_primary_pool = str(selected.path) in primary_paths
        is_stale = (target_day - memo_builder.article_recency(selected).date()).days > freshness_days
        status = "primary" if in_primary_pool else ("archive" if is_stale else "rotation")
        status_label = {
            "primary": "主样本已覆盖",
            "rotation": "轮转补位",
            "archive": "历史回看",
        }[status]
        if in_primary_pool:
            note = "该号本轮已直接进入主学习池，无需额外补位。"
        elif is_stale:
            note = (
                f"该号近 {freshness_days} 天内暂无新 deep article，暂回看最近一篇高质量样本，"
                "避免战略学习断档。"
            )
        else:
            note = (
                f"主学习池仍按业务窗采样；该号本轮通过近 {freshness_days} 天轮转补位进入学习池，"
                "不污染当天主样本。"
            )
        items.append(
            StrategicRotationItem(
                source_name=source_name,
                status=status,
                status_label=status_label,
                title=selected.title,
                published_at=selected.published_at,
                canonical_url=selected.canonical_url,
                learning_takeaway=learning_takeaway,
                visual_takeaway=visual_takeaway,
                path=str(selected.path),
                note=note,
                source_packet_count=source_packet_count,
                deep_article_count=deep_article_count,
            )
        )
    return items


def representative_card(cards: list[dashboard_builder.DraftCard]) -> dashboard_builder.DraftCard | None:
    def sort_key(card: dashboard_builder.DraftCard) -> tuple[int, int]:
        try:
            order = PLATFORM_PRIORITY.index(card.platform)
        except ValueError:
            order = len(PLATFORM_PRIORITY)
        return (card.status == "missing", order)

    viable = [card for card in cards if card.file_path != "n/a" and Path(card.file_path).exists()]
    if viable:
        return sorted(viable, key=sort_key)[0]
    return sorted(cards, key=sort_key)[0] if cards else None


def analyse_draft_text(text: str) -> dict[str, Any]:
    paragraphs = extract_paragraphs(text)
    first_window = " ".join(paragraphs[:4])
    second_window = " ".join(paragraphs[:6])
    return {
        "paragraphs": paragraphs,
        "char_count": len(re.sub(r"\s+", "", text)),
        "section_count": len(re.findall(r"^##\s+", text, flags=re.M)),
        "image_markdown_count": len(IMAGE_MD_RE.findall(text)),
        "has_internal_packaging": any(token in text for token in PACKAGING_TOKENS),
        "has_early_judgment": bool(JUDGMENT_RE.search(first_window)),
        "has_early_background": bool(BACKGROUND_RE.search(second_window)),
        "has_early_evidence": bool(URL_RE.search(second_window) or NUMBER_RE.search(second_window) or IMAGE_MD_RE.search(text)),
    }


def fallback_ready_pack_cards(date_text: str) -> list[Path]:
    pack_cards: list[Path] = []
    for path in sorted(DRAFT_PACK_ROOT.glob("*/00_draft-pack-card.md")):
        fields = dashboard_builder.parse_fields(path)
        status = clean(fields.get("status", "n/a"))
        created_at = clean(fields.get("created_at", "n/a"))
        updated_at = clean(fields.get("updated_at", "n/a"))
        if status in {"ready", "waiting_human_publish", "queued", "published"} and (
            created_at.startswith(date_text) or updated_at.startswith(date_text)
        ):
            pack_cards.append(path)
    return pack_cards


def build_ready_drafts(date_text: str) -> list[ReadyDraftLearningView]:
    token = token_for_date(date_text)
    approved_topics, _ = dashboard_builder.load_approved_topics(token)
    approved_map = {item.topic_key: item for item in approved_topics}
    topic_ids = {item.topic_id for item in approved_topics}
    draft_cards, _pack_map = dashboard_builder.load_draft_cards(date_text, topic_ids)

    grouped: dict[str, list[dashboard_builder.DraftCard]] = {}
    for card in draft_cards:
        if card.pack_status not in {"ready", "waiting_human_publish", "queued", "published"}:
            continue
        grouped.setdefault(card.topic_key, []).append(card)

    if not grouped:
        for pack_card in fallback_ready_pack_cards(date_text):
            fields = dashboard_builder.parse_fields(pack_card)
            requested_platforms = dashboard_builder.parse_platform_list(fields.get("requested_platforms", ""))
            draft_key = clean(fields.get("draft_key", pack_card.parent.name))
            topic_id = clean(fields.get("topic_id", "n/a"))
            updated_at = clean(fields.get("updated_at", "n/a"))
            status = clean(fields.get("status", "n/a"))
            cards: list[dashboard_builder.DraftCard] = []
            for platform in requested_platforms:
                path_text = clean(fields.get(f"{platform}_path", "n/a"))
                if path_text != "n/a" and Path(path_text).exists():
                    text = dashboard_builder.read_text(path_text)
                    cards.append(
                        dashboard_builder.DraftCard(
                            topic_key=draft_key,
                            topic_id=topic_id,
                            platform=platform,
                            display_title=dashboard_builder.extract_first_heading(text),
                            preview=dashboard_builder.extract_preview(text),
                            status=status,
                            updated_at=updated_at,
                            pack_status=status,
                            pack_dir=str(pack_card.parent),
                            file_path=path_text,
                            note="草稿文件已落盘",
                        )
                    )
            if cards:
                grouped[draft_key] = cards

    views: list[ReadyDraftLearningView] = []
    for topic_key, cards in sorted(grouped.items()):
        representative = representative_card(cards)
        if not representative:
            continue
        pack_card_path = Path(representative.pack_dir) / "00_draft-pack-card.md"
        pack_fields = dashboard_builder.parse_fields(pack_card_path)
        approved = approved_map.get(topic_key)
        rep_text = dashboard_builder.read_text(representative.file_path) if representative.file_path != "n/a" else ""
        metrics = analyse_draft_text(rep_text)
        visual_asset_count = count_visual_assets(Path(representative.pack_dir))
        platforms = [
            dashboard_builder.PLATFORM_CONFIG.get(card.platform, {"label": card.platform})["label"]
            for card in sorted(cards, key=lambda card: PLATFORM_PRIORITY.index(card.platform) if card.platform in PLATFORM_PRIORITY else 999)
        ]

        strengths: list[str] = []
        if metrics["has_early_judgment"]:
            strengths.append("首屏已经有判断句，读者不至于一开始就掉线。")
        if metrics["has_early_background"]:
            strengths.append("前几段已经开始补对象 / 事件 / why now，不是完全悬空分析。")
        if metrics["has_early_evidence"]:
            strengths.append("正文早段已经有链接、数字或事实锚点，判断不是空转。")
        if visual_asset_count > 0:
            strengths.append(f"本地已落 `{visual_asset_count}` 张视觉素材，具备真实图文化基础。")
        if not strengths:
            strengths.append("已经有可复用 draft pack，骨架和平台槽位都在。")

        gaps: list[str] = []
        if metrics["has_internal_packaging"]:
            gaps.append("正文前仍残留内部包装 / 标题候选等工序痕迹，离一键发布还差“去工单味”。")
        if not metrics["has_early_background"]:
            gaps.append("冷启动读者的背景桥接还不够早，容易读到一半才知道这件事到底是什么。")
        if not metrics["has_early_evidence"]:
            gaps.append("首屏证据锚点偏弱，读者会先看到判断，后看到凭据。")
        if metrics["section_count"] < 3 and metrics["char_count"] > 1200:
            gaps.append("长文分层还不够，阅读节奏容易发闷。")
        if visual_asset_count == 0:
            gaps.append("图文能力还主要停留在规划层，真实可插入素材不足。")

        views.append(
            ReadyDraftLearningView(
                topic_key=topic_key,
                topic_title=clean(
                    approved.title if approved else dashboard_builder.extract_first_heading(rep_text),
                    fallback=clean(pack_fields.get("topic_title", topic_key)),
                ),
                approved_angle=clean(
                    approved.approved_angle if approved else pack_fields.get("approved_angle", "n/a")
                ),
                platforms=platforms,
                representative_platform=representative.platform,
                representative_platform_label=dashboard_builder.PLATFORM_CONFIG.get(
                    representative.platform, {"label": representative.platform}
                )["label"],
                representative_path=representative.file_path,
                pack_dir=str(Path(representative.pack_dir)),
                preview=representative.preview,
                char_count=metrics["char_count"],
                section_count=metrics["section_count"],
                visual_asset_count=visual_asset_count,
                strengths=strengths,
                gaps=gaps,
                gap_summary="；".join(gaps[:2]) if gaps else "当前主问题已经从结构层补到可发布精修层。",
                has_internal_packaging=metrics["has_internal_packaging"],
                has_early_background=metrics["has_early_background"],
                has_early_judgment=metrics["has_early_judgment"],
                has_early_evidence=metrics["has_early_evidence"],
            )
        )
    return views


def unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        cleaned = clean(value, "")
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        ordered.append(cleaned)
    return ordered


def detect_topic_lanes(*texts: str) -> list[str]:
    haystack = " ".join(clean(text, "") for text in texts if text)
    lowered = haystack.lower()
    lanes = [
        rule["label"]
        for rule in TOPIC_LANE_RULES
        if any(token.lower() in lowered for token in rule["tokens"])
    ]
    return unique_preserve_order(lanes)[:2] or ["综合 / 其他"]


def lane_reason(lane: str) -> str:
    return LANE_REASON_PLAYBOOK.get(lane, LANE_REASON_PLAYBOOK["综合 / 其他"])


def focus_rows_from_counter(counter: Counter[str], examples: dict[str, list[str]], limit: int = 4) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lane, count in counter.most_common(limit):
        rows.append(
            {
                "lane": lane,
                "count": count,
                "examples": unique_preserve_order(examples.get(lane, []))[:2],
                "why": lane_reason(lane),
            }
        )
    return rows


def find_top20_pack_path(date_text: str) -> Path | None:
    token = token_for_date(date_text)
    preferred = [
        TOPIC_CANDIDATE_DIR / f"{token}__top20-screening-pack__reworked.md",
        TOPIC_CANDIDATE_DIR / f"{token}__top20-screening-pack.md",
    ]
    for path in preferred:
        if path.exists():
            return path
    return None


def extract_active_task_sheet_topic_keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    keys: set[str] = set()
    in_platform_tasks = False
    in_task_block = False
    task_heading_re = re.compile(r"^#### Task \d+(?:[（(]([^）)]+)[）)])?$")
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## 六个主战场任务单"):
            in_platform_tasks = True
            in_task_block = False
            continue
        if in_platform_tasks and line.startswith("## ") and not line.startswith("## 六个主战场任务单"):
            break
        if not in_platform_tasks:
            continue
        if line.startswith("#### Task"):
            match = task_heading_re.match(line)
            label = clean(match.group(1), "") if match else ""
            in_task_block = not label or ("holdout" not in label.lower() and "不开启" not in label)
            continue
        if line.startswith("### "):
            in_task_block = False
            continue
        if in_task_block:
            match = re.search(r"`topic_key`:\s*`([^`]+)`", line)
            if match:
                keys.add(clean(match.group(1), ""))
    return keys


def build_selection_topics(date_text: str) -> list[SelectionTopicView]:
    pack_path = find_top20_pack_path(date_text)
    if pack_path is None:
        return []
    token = token_for_date(date_text)
    task_sheet_path = TOPIC_CANDIDATE_DIR / f"{token}__platform-task-sheet.md"
    active_keys = extract_active_task_sheet_topic_keys(task_sheet_path)

    items: list[SelectionTopicView] = []
    for candidate in dashboard_builder.parse_top20_pack(pack_path)[:6]:
        status = "active" if candidate.topic_key in active_keys else "pool"
        items.append(
            SelectionTopicView(
                topic_key=candidate.topic_key,
                title=clean(candidate.title, fallback=candidate.header_title),
                status=status,
                status_label="已下发" if status == "active" else "池内待捞回",
                score_total=clean(candidate.score_total, "n/a"),
                signal_summary=clean(candidate.signal_summary, "n/a"),
                why_selected=clean(candidate.why_in_top20, candidate.signal_summary),
                lanes=detect_topic_lanes(candidate.title, candidate.signal_summary, candidate.why_in_top20),
                path=candidate.path,
            )
        )
    return items


def describe_lane_mix(counter: Counter[str], limit: int = 2) -> str:
    if not counter:
        return "暂无稳定题材"
    return "、".join(f"{lane}×{count}" for lane, count in counter.most_common(limit))


def build_selection_review(
    date_text: str,
    samples: list[LearningSample],
    drafts: list[ReadyDraftLearningView],
) -> dict[str, Any]:
    selection_topics = build_selection_topics(date_text)
    active_topics = [item for item in selection_topics if item.status == "active"]

    head_counter: Counter[str] = Counter()
    head_examples: dict[str, list[str]] = {}
    for sample in samples:
        lanes = detect_topic_lanes(sample.title, sample.hook_excerpt, sample.learning_takeaway)
        for lane in lanes:
            head_counter[lane] += 1
            head_examples.setdefault(lane, []).append(sample.title)

    pool_counter: Counter[str] = Counter()
    pool_examples: dict[str, list[str]] = {}
    active_counter: Counter[str] = Counter()
    active_examples: dict[str, list[str]] = {}
    for topic in selection_topics:
        for lane in topic.lanes:
            pool_counter[lane] += 1
            pool_examples.setdefault(lane, []).append(topic.title)
            if topic.status == "active":
                active_counter[lane] += 1
                active_examples.setdefault(lane, []).append(topic.title)

    shared_lanes = unique_preserve_order([lane for lane in head_counter if lane in active_counter])
    head_media_only_lanes = unique_preserve_order([lane for lane in head_counter if lane not in pool_counter])
    our_only_lanes = unique_preserve_order([lane for lane in active_counter if lane not in head_counter])

    missed_lane_rows = [
        {
            "lane": lane,
            "examples": unique_preserve_order(head_examples.get(lane, []))[:2],
            "takeaway": f"头部号在 `{lane}` 连续给出样本，而我们的 Top6 主池还没覆盖，优先检查 seed / source lane 是否漏了，而不是先认定这题不值得做。",
        }
        for lane in head_media_only_lanes[:3]
    ]
    differentiated_rows = [
        {
            "lane": lane,
            "examples": unique_preserve_order(active_examples.get(lane, []))[:2],
            "takeaway": f"我们在 `{lane}` 上主动保留了更硬的一手题，但这类题一旦脱离大众语境，draft / hook / context 就必须更早补“普通人为什么该关心”。",
        }
        for lane in our_only_lanes[:3]
    ]

    ready_keys = {item.topic_key for item in drafts}
    active_keys = {item.topic_key for item in active_topics}
    ready_only = sorted(ready_keys - active_keys)

    verdicts = [
        f"头部号这轮更偏 `{describe_lane_mix(head_counter)}`，说明它们优先抓“普通读者能立刻感到 stakes”的题材。",
        f"我们当前已下发主池更偏 `{describe_lane_mix(active_counter)}`，说明系统这轮更偏一手性、可防守性和品牌判断力。",
        "裁判结论不是谁绝对更好，而是两边各赢一部分：头部号在传播势能和大众转译上更强，我们在可核验与可防守性上更稳。后续应保持“硬信号主池 + 大众 stakes 补位池”双轨，而不是二选一。",
    ]
    if ready_only:
        verdicts.append(
            f"当前 ready 库里还有 `{', '.join(ready_only[:3])}` 这类历史题，和今天 task sheet 已下发对象不完全同频，所以学习板后续必须同时对照“当日 task sheet + 当前 ready 稿”，不能只看现成库存。"
        )

    role_actions = [
        {
            "owner": "seed-refresh / source-scouting",
            "action": "若头部号连续两轮在某题材高频而我们的 Top6 没覆盖，下轮必须补至少 2 个对应来源或动态搜源规则。",
        },
        {
            "owner": "source-capture / citation",
            "action": "准备补位的题材必须先补一手原链、截图和中文工作摘要，再交给 radar，不允许只拿二手摘要就入池。",
        },
        {
            "owner": "topic-radar",
            "action": "筛 Top20 时同时看“确定性”和“普通读者 stakes”，避免候选池只剩硬核技术题。",
        },
        {
            "owner": "topic-approval",
            "action": "当最终锁的是和头部号不同的题，必须显式写明“我们为什么不跟”和“我们靠什么打赢”。",
        },
        {
            "owner": "draft-pack / hook / context / render",
            "action": "如果坚持更垂直的差异化题，首屏必须更早补背景、利益相关性和图证，不然再好的选题也会输在转译层。",
        },
    ]

    return {
        "selection_topics": [
            {
                "topic_key": item.topic_key,
                "title": item.title,
                "status": item.status,
                "status_label": item.status_label,
                "score_total": item.score_total,
                "signal_summary": item.signal_summary,
                "why_selected": item.why_selected,
                "lanes": item.lanes,
                "path": item.path,
            }
            for item in selection_topics
        ],
        "head_media_focus": focus_rows_from_counter(head_counter, head_examples),
        "our_pool_focus": focus_rows_from_counter(pool_counter, pool_examples),
        "our_active_focus": focus_rows_from_counter(active_counter, active_examples),
        "shared_lanes": shared_lanes,
        "head_media_only_lanes": missed_lane_rows,
        "our_only_lanes": differentiated_rows,
        "verdicts": verdicts,
        "role_actions": role_actions,
        "ready_only_topic_keys": ready_only,
    }


def build_gap_cards(samples: list[LearningSample], drafts: list[ReadyDraftLearningView]) -> list[dict[str, str]]:
    total = max(len(drafts), 1)
    median_first_image = median(
        [sample.first_image_after_text_paragraphs for sample in samples if sample.first_image_after_text_paragraphs is not None]
    ) if samples and any(sample.first_image_after_text_paragraphs is not None for sample in samples) else None

    packaging_gap = [item for item in drafts if item.has_internal_packaging]
    background_gap = [item for item in drafts if not item.has_early_background]
    evidence_gap = [item for item in drafts if not item.has_early_evidence]
    visual_gap = [item for item in drafts if item.visual_asset_count == 0]

    cards: list[dict[str, str]] = []
    if packaging_gap:
        cards.append(
            {
                "title": "成品化清理不够彻底",
                "severity": "high",
                "why": "头部样本的正文几乎不暴露“标题候选 / 包装说明 / 引用占位”，用户只会看到成品。",
                "current_gap": f"当前有 {len(packaging_gap)}/{total} 个 ready 主题还保留内部编辑结构，最典型的是 `{packaging_gap[0].topic_key}`。",
                "next_action": "写稿阶段最后一轮必须做“去工单味”清理：只保留读者该看到的标题、正文、图文与来源。",
            }
        )
    if background_gap:
        cards.append(
            {
                "title": "背景桥接还要再早",
                "severity": "high",
                "why": "学习样本普遍在前 2-4 段就把“发生了什么 / 对象是谁 / 为什么现在值得看”交代清楚。",
                "current_gap": f"当前有 {len(background_gap)}/{total} 个 ready 主题在首屏仍偏判断先行、背景偏晚。",
                "next_action": "优先补对象、事件、why now，不先换题；冷启动读者必须在前屏内知道你在说什么。",
            }
        )
    if evidence_gap:
        cards.append(
            {
                "title": "证据锚点还不够前置",
                "severity": "medium",
                "why": "头部样本喜欢很早给原话、数据、链接或关键截图，不让文章一直漂在抽象判断上。",
                "current_gap": f"当前有 {len(evidence_gap)}/{total} 个 ready 主题在前段还缺明确凭据。",
                "next_action": "补原始链接、关键数字或截图位；优先补证据，再谈换题。",
            }
        )
    if visual_gap:
        cards.append(
            {
                "title": "图证落地仍弱于头部号",
                "severity": "medium",
                "why": (
                    "学习样本的图片不是装饰。"
                    + (f"样本首图中位数约在前 `{median_first_image}` 个文字段落后。" if median_first_image is not None else "")
                ),
                "current_gap": f"当前有 {len(visual_gap)}/{total} 个 ready 主题还没落真实视觉素材，只停在 visual plan。",
                "next_action": "把“证据图 / 解释图 / 节奏图”分别落到素材资产，不要只停留在说明文档里。",
            }
        )
    if not cards:
        cards.append(
            {
                "title": "主要缺口已转入微调层",
                "severity": "low",
                "why": "学习样本与当前 ready 稿之间的大结构问题已基本补齐。",
                "current_gap": "当前主要差异已经从“结构错误”降到“标题 / 封面 / 节奏 A/B 测试”。",
                "next_action": "下一步重点做封面与标题实验，而不是大改正文骨架。",
            }
        )
    return cards


def build_next_actions(
    samples: list[LearningSample],
    drafts: list[ReadyDraftLearningView],
    gap_cards: list[dict[str, str]],
    strategic_rotation: list[StrategicRotationItem],
) -> list[str]:
    actions: list[str] = []
    if drafts:
        weakest = next((item for item in drafts if item.has_internal_packaging), drafts[0])
        actions.append(f"先把 `{weakest.topic_key}` 做一次“去工单味”清理，确保成品页只剩读者该看到的内容。")
    if any(not item.has_early_background for item in drafts):
        actions.append("把所有 ready 稿的背景桥接前移到首屏前 10%-15%，先补对象 / 事件 / why now。")
    if any(item.visual_asset_count == 0 for item in drafts):
        actions.append("按“证据图 / 解释图 / 节奏图”三类，给缺图稿件补一轮真实素材资产。")
    if samples:
        source_mix = Counter(sample.source_name for sample in samples).most_common(2)
        readable = "、".join(f"{name}×{count}" for name, count in source_mix)
        actions.append(f"明天继续从 `{readable}` 这类高密度样本增量学习，维持学习池稳定刷新。")
    blocked_sources = [item.source_name for item in strategic_rotation if item.status == "blocked"]
    if blocked_sources:
        actions.append(
            f"把 `{blocked_sources[0]}` 的 source packet / deep article 主链补通，避免已接入账号持续不进学习池。"
        )
    return actions[:4]


def optimization_item_id(card: dict[str, str]) -> str:
    digest = hashlib.md5(
        f"{card.get('title', '')}|{card.get('next_action', '')}|{card.get('current_gap', '')}".encode("utf-8")
    ).hexdigest()[:10]
    return f"opt_{digest}"


def build_optimization_items(
    date_text: str,
    samples: list[LearningSample],
    drafts: list[ReadyDraftLearningView],
    gap_cards: list[dict[str, str]],
) -> list[dict[str, Any]]:
    state = load_optimization_state()
    dismissed_ids = set(((state.get("by_date") or {}).get(date_text, {}) or {}).get("dismissed_ids") or [])
    source_mix = Counter(sample.source_name for sample in samples).most_common(3)
    source_basis = "、".join(f"{name}×{count}" for name, count in source_mix) if source_mix else "当前暂无稳定样本"

    items: list[dict[str, Any]] = []
    for card in gap_cards:
        rule = OPTIMIZATION_OWNER_RULES.get(card["title"], {})
        item_id = optimization_item_id(card)
        items.append(
            {
                "id": item_id,
                "title": card["title"],
                "severity": card["severity"],
                "owner": rule.get("owner", "content-analyst"),
                "landing_layer": rule.get("landing_layer", "learning follow-up"),
                "landing_targets": rule.get("landing_targets", []),
                "why": card["why"],
                "current_gap": card["current_gap"],
                "next_action": card["next_action"],
                "source_basis": source_basis,
                "status": "dismissed" if item_id in dismissed_ids else "active",
                "status_label": "已取消" if item_id in dismissed_ids else "待优化",
            }
        )

    style_item = {
        "title": "把题材 × 人群 × 文风匹配持续沉淀到岗位规则",
        "severity": "medium",
        "why": "头部号真正可复用的不是口头禅，而是不同题材会自动切换叙述密度、术语阈值和证据呈现方式。",
        "current_gap": "系统已有结构学习，但“事件科普 / 产品推荐 / 产业判断 / builder 拆解”对应的文风匹配规律还需要继续积累和显式沉淀。",
        "next_action": "继续把长期学习结果写进稳定规则手册，并让 topic-radar、draft-pack、content-polish、visual-intelligence 每次执行时显式加载。",
    }
    style_item_id = optimization_item_id(style_item)
    items.append(
        {
            "id": style_item_id,
            "title": style_item["title"],
            "severity": style_item["severity"],
            "owner": "content-analyst + core skills",
            "landing_layer": "skills + learning rulebook",
            "landing_targets": [
                "08_brand_assets/latest__head-media-learning-rulebook-v1.md",
                "09_runbooks/skills/th-topic-radar/SKILL.md",
                "09_runbooks/skills/th-draft-pack/SKILL.md",
                "09_runbooks/skills/th-content-polish/SKILL.md",
                "09_runbooks/skills/th-market-visual-intelligence/SKILL.md",
            ],
            "why": style_item["why"],
            "current_gap": style_item["current_gap"],
            "next_action": style_item["next_action"],
            "source_basis": source_basis,
            "status": "dismissed" if style_item_id in dismissed_ids else "active",
            "status_label": "已取消" if style_item_id in dismissed_ids else "待优化",
        }
    )

    selection_item = {
        "title": "把选题判断复盘前置到 seed / source / topic 三层",
        "severity": "high",
        "why": "头部号学习不能只反哺写法，还要让上游岗位知道今天什么题更值得做、我们为什么没做、是漏抓还是故意不跟。",
        "current_gap": "现有规则手册已有写法学习，但对“头部号今天在追什么 / 我们今天为什么押另一个题 / 哪边更优”的复盘还不够前置到上游岗位。",
        "next_action": "让 source-capture、seed-refresh、topic-radar、topic-approval 执行前显式读取规则手册中的选题复盘，并把共识题 / 漏题 / 差异化题写回下一轮动作。",
    }
    selection_item_id = optimization_item_id(selection_item)
    items.append(
        {
            "id": selection_item_id,
            "title": selection_item["title"],
            "severity": selection_item["severity"],
            "owner": "source-capture + seed-refresh + topic-radar + topic-approval",
            "landing_layer": "skills + learning rulebook + next-round source lanes",
            "landing_targets": [
                "08_brand_assets/latest__head-media-learning-rulebook-v1.md",
                "09_runbooks/skills/th-source-capture-and-citation/SKILL.md",
                "09_runbooks/skills/th-seed-refresh-and-source-scouting/SKILL.md",
                "09_runbooks/skills/th-topic-radar/SKILL.md",
                "09_runbooks/skills/th-topic-approval/SKILL.md",
            ],
            "why": selection_item["why"],
            "current_gap": selection_item["current_gap"],
            "next_action": selection_item["next_action"],
            "source_basis": source_basis,
            "status": "dismissed" if selection_item_id in dismissed_ids else "active",
            "status_label": "已取消" if selection_item_id in dismissed_ids else "待优化",
        }
    )
    return items


def render_style_matrix_markdown() -> str:
    rows = [
        "| 题材类型 | 目标人群 | 推荐表达 | 应该做什么 | 避免什么 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in STYLE_PLAYBOOK:
        rows.append(
            f"| {row['content_type']} | {row['audience']} | {row['style_rule']} | {row['do']} | {row['avoid']} |"
        )
    return "\n".join(rows)


def build_rulebook_markdown(snapshot: dict[str, Any]) -> str:
    overview = snapshot["overview"]
    selection_review = snapshot["selection_review"]
    strategic_rotation = snapshot["strategic_rotation"]
    sample_mix = "、".join(f"{name}×{count}" for name, count in overview["sample_source_mix"]) or "暂无稳定样本"
    optimization_blocks = "\n".join(
        f"- `{item['title']}`｜`{item['owner']}`｜`{item['status_label']}`｜{item['next_action']}"
        for item in snapshot["optimization_items"]
    ) or "- 当前没有待优化项。"
    selection_focus_rows = "\n".join(
        [
            "| 视角 | 题材带 | 样本数 | 代表对象 | 为什么会被选中 |",
            "| --- | --- | --- | --- | --- |",
            *[
                f"| 头部号样本 | {item['lane']} | {item['count']} | {compact('；'.join(item['examples']), 70)} | {item['why']} |"
                for item in selection_review["head_media_focus"]
            ],
            *[
                f"| 我们已下发主池 | {item['lane']} | {item['count']} | {compact('；'.join(item['examples']), 70)} | {item['why']} |"
                for item in selection_review["our_active_focus"]
            ],
        ]
    )
    selection_topic_rows = "\n".join(
        [
            "| 状态 | 主题 | 题材带 | 为什么保留 |",
            "| --- | --- | --- | --- |",
            *[
                f"| {item['status_label']} | {item['title']} | {' / '.join(item['lanes'])} | {compact(item['why_selected'], 100)} |"
                for item in selection_review["selection_topics"]
            ],
        ]
    ) if selection_review["selection_topics"] else "| 状态 | 主题 | 题材带 | 为什么保留 |\n| --- | --- | --- | --- |\n| n/a | n/a | n/a | n/a |"
    selection_role_rows = "\n".join(
        [
            "| Owner | 下轮必须落成什么动作 |",
            "| --- | --- |",
            *[
                f"| {item['owner']} | {item['action']} |"
                for item in selection_review["role_actions"]
            ],
        ]
    )
    selection_delta_blocks = "\n".join(
        [f"- {item}" for item in selection_review["verdicts"]]
        + [
            f"- 头部号漏斗外题材：`{row['lane']}`｜{compact('；'.join(row['examples']), 60)}｜{row['takeaway']}"
            for row in selection_review["head_media_only_lanes"]
        ]
        + [
            f"- 我们的差异化题材：`{row['lane']}`｜{compact('；'.join(row['examples']), 60)}｜{row['takeaway']}"
            for row in selection_review["our_only_lanes"]
        ]
    ) or "- 当前还没有足够样本做选题判断复盘。"
    strategic_rows = "\n".join(
        [
            "| 来源 | 状态 | 当前学习对象 / 阻塞 | 主链记录 | 说明 |",
            "| --- | --- | --- | --- | --- |",
            *[
                f"| {item['source_name']} | {item['status_label']} | {compact(item['title'], 70)} | source_packet={item['source_packet_count']} / deep_article={item['deep_article_count']} | {compact(item['note'], 100)} |"
                for item in strategic_rotation
            ],
        ]
    )
    landing_rows = "\n".join(
        [
            "| 岗位 / 能力 | 现在怎么接收学习结果 |",
            "| --- | --- |",
            "| source-capture / citation | 每轮执行前读取规则手册里的“漏题 / 共识题”，优先补原始链接、截图和中文工作摘要，不让二手摘要直接进候选池。 |",
            "| seed-refresh / source-scouting | 用规则手册里的“头部号今天在追什么”和“我们漏掉了什么”更新 watchlist 与动态搜源规则。 |",
            "| signal-scout / topic-radar | 每轮执行前读取规则手册，把“确定性 + 普通读者 stakes + 题材覆盖”一起带入 Top20 / Top5 筛选。 |",
            "| topic-approval / brand-context | 锁题时显式写清楚：为什么跟头部号同题，或为什么故意不跟；同时提醒平台束、背景桥接、证据抓手和图证计划。 |",
            "| hook / context / draft-pack / audience | 生成初稿前读取规则手册，把题材 × 人群 × 文风匹配，以及差异化题材的背景桥接要求写进平台初稿。 |",
            "| visual-intelligence / renderer / repurpose | 把头部号图文节奏、截图优先级和平台呈现方式转成具体视觉槽位和 handoff 资产。 |",
            "| content-polish / review / postmortem | 精修和复盘时对照规则手册，继续更新下一轮优化项，而不是把学习停在总结层。 |",
        ]
    )
    return f"""# 头部号学习规则手册 v1

- `generated_at`: `{snapshot['meta']['generated_at']}`
- `date`: `{snapshot['meta']['date']}`
- `sample_count`: `{overview['sample_count']}`
- `ready_topic_count`: `{overview['ready_topic_count']}`
- `sample_source_mix`: `{sample_mix}`
- `source_board`: `{snapshot['paths']['json']}`

## 一眼结论

{chr(10).join(f"- {item}" for item in overview["takeaways"])}

## 题材 × 人群 × 文风匹配表

{render_style_matrix_markdown()}

## 选题判断复盘

{selection_focus_rows}

## 今天我们的主池与差异化判断

{selection_topic_rows}

## 战略号轮转补位

{strategic_rows}

## 裁判结论

{selection_delta_blocks}

## 岗位落地表

{landing_rows}

## 选题复盘反哺动作

{selection_role_rows}

## 当前待优化项

{optimization_blocks}
"""


def build_snapshot(date_text: str, count: int = 8, window_start: str = "17:00", window_end: str = "14:30") -> dict[str, Any]:
    samples = build_learning_samples(
        count,
        date_text=date_text,
        window_start=window_start,
        window_end=window_end,
    )
    strategic_rotation = build_strategic_rotation_items(date_text, samples)
    drafts = build_ready_drafts(date_text)
    selection_review = build_selection_review(date_text, samples, drafts)
    gap_cards = build_gap_cards(samples, drafts)
    optimization_items = build_optimization_items(date_text, samples, drafts, gap_cards)
    outputs = output_paths(date_text)
    learning_rulebook_paths = rulebook_paths(date_text)

    sample_sources = Counter(sample.source_name for sample in samples)
    first_image_values = [sample.first_image_after_text_paragraphs for sample in samples if sample.first_image_after_text_paragraphs is not None]
    image_counts = [sample.image_count for sample in samples]
    next_actions = build_next_actions(samples, drafts, gap_cards, strategic_rotation)

    takeaways = [
        "先用判断或反差把人拉住，再在前 10%-15% 内补齐背景。",
        "证据要早，不要让读者一直听抽象判断。",
        "图片要承担证明、解释、换气三种职责，而不是只做装饰。",
        "写稿时优先补证、补背景、补图，而不是遇到问题就直接换题。",
        "学习不只反哺写稿岗，还要反哺 source / seed / topic 三层，持续校正“今天该追什么题”。",
    ]

    return {
        "meta": {
            "generated_at": now_cst(),
            "date": date_text,
            "window_rule": f"T-1 {window_start} → T {window_end}",
        },
        "paths": {
            **{key: str(path) for key, path in outputs.items() if key != "log"},
            "rulebook_markdown": str(learning_rulebook_paths["dated"]),
            "rulebook_latest": str(learning_rulebook_paths["latest"]),
            "optimization_state": str(OPTIMIZATION_STATE_PATH),
        },
        "overview": {
            "sample_count": len(samples),
            "ready_topic_count": len(drafts),
            "strategic_rotation_count": len(strategic_rotation),
            "strategic_rotation_blocked": sum(1 for item in strategic_rotation if item.status == "blocked"),
            "sample_source_mix": sample_sources.most_common(),
            "median_first_image_after_text_paragraphs": median(first_image_values) if first_image_values else None,
            "median_sample_image_count": median(image_counts) if image_counts else None,
            "takeaways": takeaways,
            "optimization_total": len(optimization_items),
            "optimization_active": sum(1 for item in optimization_items if item["status"] == "active"),
            "optimization_dismissed": sum(1 for item in optimization_items if item["status"] == "dismissed"),
        },
        "samples": [asdict(item) for item in samples],
        "strategic_rotation": [asdict(item) for item in strategic_rotation],
        "ready_drafts": [asdict(item) for item in drafts],
        "selection_review": selection_review,
        "gap_cards": gap_cards,
        "next_actions": next_actions,
        "optimization_items": optimization_items,
        "optimization_events": optimization_action_log(date_text),
    }


def render_markdown(snapshot: dict[str, Any]) -> str:
    overview = snapshot["overview"]
    selection_review = snapshot["selection_review"]
    sample_rows = "\n".join(
        f"| {sample['source_name']} | {sample['title']} | {sample['published_at']} | {sample['image_count']} | {sample['first_image_after_text_paragraphs'] if sample['first_image_after_text_paragraphs'] is not None else 'n/a'} | {sample['learning_takeaway']} | [原文]({sample['canonical_url']}) |"
        for sample in snapshot["samples"]
    ) or "| n/a | n/a | n/a | n/a | n/a | n/a | n/a |"

    ready_rows = "\n".join(
        f"| {item['topic_key']} | {' / '.join(item['platforms'])} | {compact(item['preview'], 70)} | {compact('；'.join(item['strengths']), 90)} | {compact(item['gap_summary'], 90)} | `{item['representative_path']}` |"
        for item in snapshot["ready_drafts"]
    ) or "| n/a | n/a | n/a | n/a | n/a | n/a |"

    gap_blocks = "\n".join(
        "\n".join(
            [
                f"### {card['title']}",
                f"- `severity`: `{card['severity']}`",
                f"- `why`: `{card['why']}`",
                f"- `current_gap`: `{card['current_gap']}`",
                f"- `next_action`: `{card['next_action']}`",
                "",
            ]
        )
        for card in snapshot["gap_cards"]
    )
    optimization_rows = "\n".join(
        f"| {item['title']} | {item['owner']} | {item['landing_layer']} | {compact(item['next_action'], 70)} | {item['status_label']} | {compact('；'.join(item['landing_targets']), 80)} |"
        for item in snapshot["optimization_items"]
    ) or "| n/a | n/a | n/a | n/a | n/a | n/a |"

    next_actions = "\n".join(f"- {item}" for item in snapshot["next_actions"]) or "- 当前没有新增动作。"
    takeaways = "\n".join(f"- {item}" for item in overview["takeaways"])
    selection_focus_rows = "\n".join(
        f"| 头部号样本 | {item['lane']} | {item['count']} | {compact('；'.join(item['examples']), 70)} | {item['why']} |"
        for item in selection_review["head_media_focus"]
    )
    selection_focus_rows += (
        ("\n" if selection_focus_rows else "")
        + "\n".join(
            f"| 我们已下发主池 | {item['lane']} | {item['count']} | {compact('；'.join(item['examples']), 70)} | {item['why']} |"
            for item in selection_review["our_active_focus"]
        )
    )
    selection_focus_rows = selection_focus_rows or "| n/a | n/a | n/a | n/a | n/a |"
    selection_topic_rows = "\n".join(
        f"| {item['status_label']} | {item['title']} | {' / '.join(item['lanes'])} | {compact(item['why_selected'], 90)} | `{item['topic_key']}` |"
        for item in selection_review["selection_topics"]
    ) or "| n/a | n/a | n/a | n/a | n/a |"
    selection_verdicts = "\n".join(f"- {item}" for item in selection_review["verdicts"]) or "- 当前还没有足够样本做选题判断复盘。"
    selection_role_rows = "\n".join(
        f"| {item['owner']} | {item['action']} |"
        for item in selection_review["role_actions"]
    ) or "| n/a | n/a |"
    missed_rows = "\n".join(
        f"- `头部号在做、我们没进主池`｜`{item['lane']}`｜{compact('；'.join(item['examples']), 60)}｜{item['takeaway']}"
        for item in selection_review["head_media_only_lanes"]
    )
    diff_rows = "\n".join(
        f"- `我们主动差异化`｜`{item['lane']}`｜{compact('；'.join(item['examples']), 60)}｜{item['takeaway']}"
        for item in selection_review["our_only_lanes"]
    )
    selection_deltas = "\n".join(filter(None, [missed_rows, diff_rows])) or "- 当前没有明显题材错位。"
    strategic_rows = "\n".join(
        f"| {item['source_name']} | {item['status_label']} | {item['title']} | {item['published_at']} | source_packet={item['source_packet_count']} / deep_article={item['deep_article_count']} | {compact(item['note'], 90)} | {'[原文](' + item['canonical_url'] + ')' if item['canonical_url'] != 'n/a' else 'n/a'} |"
        for item in snapshot["strategic_rotation"]
    ) or "| n/a | n/a | n/a | n/a | n/a | n/a | n/a |"

    return f"""# 头部号学习池 / 对标池

- `generated_at`: `{snapshot['meta']['generated_at']}`
- `date`: `{snapshot['meta']['date']}`
- `window_rule`: `{snapshot['meta']['window_rule']}`
- `sample_count`: `{overview['sample_count']}`
- `ready_topic_count`: `{overview['ready_topic_count']}`
- `strategic_rotation_count`: `{overview['strategic_rotation_count']}`

## 一眼结论

{takeaways}

## 学习样本池

| 来源 | 标题 | 发布时间 | 图片数 | 首图前文字段落数 | 值得学什么 | 原文 |
| --- | --- | --- | --- | --- | --- | --- |
{sample_rows}

## 战略号轮转补位

| 来源 | 状态 | 当前学习对象 | 发布时间 | 主链记录 | 说明 | 原文 |
| --- | --- | --- | --- | --- | --- | --- |
{strategic_rows}

## 当前 ready 稿对照

| 主题 | 平台 | 首屏预览 | 已有长处 | 当前差距 | 稿件 |
| --- | --- | --- | --- | --- | --- |
{ready_rows}

## 选题判断复盘

| 视角 | 题材带 | 样本数 | 代表对象 | 为什么会被选中 |
| --- | --- | --- | --- | --- |
{selection_focus_rows}

## 今天我们的主池

| 状态 | 主题 | 题材带 | 为什么保留 | topic_key |
| --- | --- | --- | --- | --- |
{selection_topic_rows}

## 裁判结论

{selection_verdicts}

## 题材错位与补位

{selection_deltas}

## 我们差在哪

{gap_blocks}

## 优化建议表

| 建议 | Owner | 落地层 | 下一步 | 状态 | 落点 |
| --- | --- | --- | --- | --- | --- |
{optimization_rows}

## 反哺到岗位的动作

| Owner | 下轮必须落成什么动作 |
| --- | --- |
{selection_role_rows}

## 下一步动作

{next_actions}
"""


def render_html(snapshot: dict[str, Any]) -> str:
    overview = snapshot["overview"]
    selection_review = snapshot["selection_review"]
    sample_mix = "".join(
        f'<span class="chip">{escape(name)} {count}</span>' for name, count in overview["sample_source_mix"]
    ) or '<span class="chip">暂无样本</span>'
    samples_html = "".join(
        (
            '<tr>'
            f"<td>{escape(sample['source_name'])}</td>"
            f"<td><div class=\"title\">{escape(sample['title'])}</div><div class=\"sub\">{escape(sample['hook_excerpt'])}</div></td>"
            f"<td>{escape(sample['published_at'])}</td>"
            f"<td>{sample['image_count']}</td>"
            f"<td>{sample['first_image_after_text_paragraphs'] if sample['first_image_after_text_paragraphs'] is not None else 'n/a'}</td>"
            f"<td>{escape(sample['learning_takeaway'])}<div class=\"sub\">{escape(sample['visual_takeaway'])}</div></td>"
            f"<td><a href=\"{escape(sample['canonical_url'])}\" target=\"_blank\" rel=\"noreferrer\">原文</a><br><a href=\"file://{escape(sample['path'])}\">deep article</a></td>"
            "</tr>"
        )
        for sample in snapshot["samples"]
    ) or '<tr><td colspan="7">当前还没有可用学习样本。</td></tr>'
    strategic_rows_html = "".join(
        (
            "<tr>"
            f"<td>{escape(item['source_name'])}</td>"
            f"<td>{escape(item['status_label'])}</td>"
            f"<td><div class=\"title\">{escape(item['title'])}</div><div class=\"sub\">source_packet={item['source_packet_count']} / deep_article={item['deep_article_count']}</div></td>"
            f"<td>{escape(item['published_at'])}</td>"
            f"<td>{escape(item['note'])}</td>"
            + ("<td>" + ("<a href=\"" + escape(item["canonical_url"]) + "\" target=\"_blank\" rel=\"noreferrer\">原文</a><br>" if item["canonical_url"] != "n/a" else "") + ("<a href=\"file://" + escape(item["path"]) + "\">deep article</a>" if item["path"] != "n/a" else "") + "</td>" if item.get("canonical_url") or item.get("path") else "<td></td>")
            + "</tr>"
        )
        for item in snapshot["strategic_rotation"]
    ) or '<tr><td colspan="6">当前还没有战略号补位样本。</td></tr>'

    drafts_html = "".join(
        (
            '<div class="draft-card">'
            f"<div class=\"draft-head\"><div><div class=\"title\">{escape(item['topic_title'])}</div><div class=\"sub\">{escape(item['topic_key'])} · {escape(' / '.join(item['platforms']))}</div></div><div class=\"badge\">{escape(item['representative_platform_label'])}</div></div>"
            f"<div class=\"block\"><strong>当前预览</strong><p>{escape(item['preview'])}</p></div>"
            f"<div class=\"block\"><strong>已有长处</strong><ul>{''.join(f'<li>{escape(point)}</li>' for point in item['strengths'])}</ul></div>"
            f"<div class=\"block\"><strong>当前差距</strong><ul>{''.join(f'<li>{escape(point)}</li>' for point in item['gaps'])}</ul></div>"
            f"<div class=\"draft-foot\"><span>视觉资产 {item['visual_asset_count']} 张 · section {item['section_count']}</span><span><a href=\"file://{escape(item['representative_path'])}\">稿件</a> · <a href=\"file://{escape(item['pack_dir'])}\">pack</a></span></div>"
            "</div>"
        )
        for item in snapshot["ready_drafts"]
    ) or '<div class="empty">当前没有 ready 稿件可对照。</div>'

    gap_cards_html = "".join(
        (
            '<div class="gap-card">'
            f"<div class=\"gap-head\"><strong>{escape(card['title'])}</strong><span class=\"severity severity-{escape(card['severity'])}\">{escape(card['severity'])}</span></div>"
            f"<p><strong>为什么要补：</strong>{escape(card['why'])}</p>"
            f"<p><strong>我们现在差在哪：</strong>{escape(card['current_gap'])}</p>"
            f"<p><strong>下一步：</strong>{escape(card['next_action'])}</p>"
            "</div>"
        )
        for card in snapshot["gap_cards"]
    )
    optimization_rows_html = "".join(
        (
            "<tr>"
            f"<td><div class=\"title\">{escape(item['title'])}</div><div class=\"sub\">{escape(item['why'])}</div></td>"
            f"<td>{escape(item['owner'])}</td>"
            f"<td>{escape(item['landing_layer'])}</td>"
            f"<td>{escape(item['status_label'])}</td>"
            f"<td>{escape(item['next_action'])}</td>"
            f"<td><div class=\"sub\">{escape('；'.join(item['landing_targets']))}</div></td>"
            "</tr>"
        )
        for item in snapshot["optimization_items"]
    ) or '<tr><td colspan="6">当前没有待优化项。</td></tr>'

    next_actions_html = "".join(f"<li>{escape(item)}</li>" for item in snapshot["next_actions"]) or "<li>当前没有新增动作。</li>"
    selection_focus_rows_html = "".join(
        (
            "<tr>"
            f"<td>{escape(view)}</td>"
            f"<td>{escape(item['lane'])}</td>"
            f"<td>{item['count']}</td>"
            f"<td><div class=\"title\">{escape('；'.join(item['examples']) or 'n/a')}</div></td>"
            f"<td>{escape(item['why'])}</td>"
            "</tr>"
        )
        for view, bucket in (
            ("头部号样本", selection_review["head_media_focus"]),
            ("我们已下发主池", selection_review["our_active_focus"]),
        )
        for item in bucket
    ) or '<tr><td colspan="5">当前还没有足够样本做选题判断复盘。</td></tr>'
    selection_topic_rows_html = "".join(
        (
            "<tr>"
            f"<td>{escape(item['status_label'])}</td>"
            f"<td><div class=\"title\">{escape(item['title'])}</div><div class=\"sub\">{escape(item['topic_key'])}</div></td>"
            f"<td>{escape(' / '.join(item['lanes']))}</td>"
            f"<td>{escape(item['why_selected'])}</td>"
            "</tr>"
        )
        for item in selection_review["selection_topics"]
    ) or '<tr><td colspan="4">今天还没有可对照的主池对象。</td></tr>'
    selection_verdicts_html = "".join(f"<li>{escape(item)}</li>" for item in selection_review["verdicts"]) or "<li>当前没有裁判结论。</li>"
    selection_role_rows_html = "".join(
        (
            "<tr>"
            f"<td>{escape(item['owner'])}</td>"
            f"<td>{escape(item['action'])}</td>"
            "</tr>"
        )
        for item in selection_review["role_actions"]
    ) or '<tr><td colspan="2">当前没有岗位动作。</td></tr>'
    selection_delta_cards_html = "".join(
        (
            '<div class="gap-card">'
            f"<div class=\"gap-head\"><strong>{escape(title)}</strong><span class=\"severity severity-medium\">delta</span></div>"
            f"<p><strong>题材带：</strong>{escape(item['lane'])}</p>"
            f"<p><strong>代表对象：</strong>{escape('；'.join(item['examples']) or 'n/a')}</p>"
            f"<p><strong>该怎么学：</strong>{escape(item['takeaway'])}</p>"
            "</div>"
        )
        for title, bucket in (
            ("头部号在做、我们没进主池", selection_review["head_media_only_lanes"]),
            ("我们主动差异化", selection_review["our_only_lanes"]),
        )
        for item in bucket
    ) or '<div class="empty">当前没有明显题材错位。</div>'

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>头部号学习池 / 对标池</title>
  <style>
    :root {{
      --bg: #f4f7fb;
      --panel: #ffffff;
      --line: #dbe5f3;
      --text: #132238;
      --muted: #5c708f;
      --accent: #2251cc;
      --good: #0d9b6b;
      --warn: #d38700;
      --high: #d13232;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: -apple-system,BlinkMacSystemFont,"SF Pro Display","PingFang SC",sans-serif; background: var(--bg); color: var(--text); }}
    .page {{ max-width: 1460px; margin: 0 auto; padding: 28px 24px 64px; }}
    .hero {{ background: linear-gradient(135deg, #132238, #1b3359); color: #fff; border-radius: 24px; padding: 28px; margin-bottom: 18px; }}
    .hero h1 {{ margin: 0 0 8px; font-size: 34px; }}
    .hero p {{ margin: 0; color: rgba(255,255,255,0.84); }}
    .meta {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 14px; }}
    .chip {{ display: inline-flex; align-items: center; padding: 6px 10px; background: rgba(255,255,255,0.12); border-radius: 999px; font-size: 12px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-bottom: 18px; }}
    .metric, .panel {{ background: var(--panel); border: 1px solid var(--line); border-radius: 18px; }}
    .metric {{ padding: 16px 18px; }}
    .metric .label {{ color: var(--muted); font-size: 13px; }}
    .metric .value {{ font-size: 28px; font-weight: 800; margin-top: 8px; }}
    .metric .sub {{ color: var(--muted); font-size: 12px; margin-top: 6px; }}
    .panel {{ padding: 20px; margin-bottom: 18px; }}
    .panel h2 {{ margin: 0 0 6px; font-size: 22px; }}
    .panel-sub {{ color: var(--muted); margin-bottom: 12px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ text-align: left; padding: 12px 10px; border-bottom: 1px solid var(--line); vertical-align: top; font-size: 14px; }}
    th {{ color: var(--muted); font-weight: 700; }}
    .title {{ font-weight: 800; line-height: 1.45; }}
    .sub {{ color: var(--muted); font-size: 12px; line-height: 1.6; margin-top: 4px; }}
    .takeaways {{ margin: 0; padding-left: 18px; }}
    .takeaways li + li {{ margin-top: 8px; }}
    .draft-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 12px; }}
    .draft-card, .gap-card {{ border: 1px solid var(--line); border-radius: 16px; padding: 16px; background: #fff; }}
    .draft-head, .gap-head {{ display: flex; justify-content: space-between; gap: 10px; align-items: flex-start; margin-bottom: 12px; }}
    .badge {{ background: #eef3ff; color: var(--accent); padding: 5px 10px; border-radius: 999px; font-size: 12px; }}
    .block + .block {{ margin-top: 12px; }}
    .block strong {{ display: block; margin-bottom: 6px; }}
    .block p {{ margin: 0; line-height: 1.7; }}
    .block ul {{ margin: 0; padding-left: 18px; }}
    .block li + li {{ margin-top: 6px; }}
    .draft-foot {{ display: flex; justify-content: space-between; gap: 10px; color: var(--muted); font-size: 12px; margin-top: 14px; }}
    .severity {{ padding: 4px 8px; border-radius: 999px; font-size: 12px; font-weight: 700; text-transform: uppercase; }}
    .severity-high {{ background: rgba(209,50,50,0.12); color: var(--high); }}
    .severity-medium {{ background: rgba(211,135,0,0.12); color: var(--warn); }}
    .severity-low {{ background: rgba(13,155,107,0.12); color: var(--good); }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .empty {{ color: var(--muted); }}
  </style>
</head>
<body>
  <div class="page">
    <section class="hero">
      <h1>头部号学习池 / 对标池</h1>
      <p>这张板只回答两个问题：别人是怎么拿结果的，我们现在还差在哪。</p>
      <div class="meta">
        <span class="chip">业务日 {escape(snapshot['meta']['date'])}</span>
        <span class="chip">窗口 {escape(snapshot['meta']['window_rule'])}</span>
        <span class="chip">生成 {escape(snapshot['meta']['generated_at'])}</span>
        {sample_mix}
      </div>
    </section>

    <section class="grid">
      <div class="metric"><div class="label">学习样本</div><div class="value">{overview['sample_count']}</div><div class="sub">深抓头部号样本</div></div>
      <div class="metric"><div class="label">战略号轮转</div><div class="value">{overview['strategic_rotation_count']}</div><div class="sub">其中阻塞 {overview['strategic_rotation_blocked']} 个</div></div>
      <div class="metric"><div class="label">当前 ready 主题</div><div class="value">{overview['ready_topic_count']}</div><div class="sub">进入对标池的当前稿件</div></div>
      <div class="metric"><div class="label">样本首图节奏</div><div class="value">{overview['median_first_image_after_text_paragraphs'] if overview['median_first_image_after_text_paragraphs'] is not None else 'n/a'}</div><div class="sub">首图前文字段落中位数</div></div>
      <div class="metric"><div class="label">样本图片密度</div><div class="value">{overview['median_sample_image_count'] if overview['median_sample_image_count'] is not None else 'n/a'}</div><div class="sub">单篇图片数中位数</div></div>
    </section>

    <section class="panel">
      <h2>一眼结论</h2>
      <div class="panel-sub">先把头部号稳定做对的事记牢，再看我们该补哪里。</div>
      <ul class="takeaways">{''.join(f'<li>{escape(item)}</li>' for item in overview['takeaways'])}</ul>
    </section>

    <section class="panel">
      <h2>学习样本池</h2>
      <div class="panel-sub">来自公众号深抓的真实样本，不只看标题，也看开头和图文节奏。</div>
      <table>
        <thead>
          <tr>
            <th>来源</th>
            <th>标题 / 开头</th>
            <th>发布时间</th>
            <th>图片数</th>
            <th>首图前文字段落</th>
            <th>值得学什么</th>
            <th>动作</th>
          </tr>
        </thead>
        <tbody>{samples_html}</tbody>
      </table>
    </section>

    <section class="panel">
      <h2>战略号轮转补位</h2>
      <div class="panel-sub">主学习池继续只看当天业务窗；这张表负责保证战略号不断学，同时把没跑通的主链直接暴露出来。</div>
      <table>
        <thead>
          <tr>
            <th>来源</th>
            <th>状态</th>
            <th>当前学习对象</th>
            <th>发布时间</th>
            <th>说明</th>
            <th>动作</th>
          </tr>
        </thead>
        <tbody>{strategic_rows_html}</tbody>
      </table>
    </section>

    <section class="panel">
      <h2>当前 ready 稿对照</h2>
      <div class="panel-sub">把今天已经 ready 的稿件拉进来，直接看“已有长处”和“还差哪一刀”。</div>
      <div class="draft-grid">{drafts_html}</div>
    </section>

    <section class="panel">
      <h2>选题判断复盘</h2>
      <div class="panel-sub">不只学怎么写，还要学“头部号今天为什么做这个题，我们为什么押另外一个题”。</div>
      <table>
        <thead>
          <tr>
            <th>视角</th>
            <th>题材带</th>
            <th>样本数</th>
            <th>代表对象</th>
            <th>为什么会被选中</th>
          </tr>
        </thead>
        <tbody>{selection_focus_rows_html}</tbody>
      </table>
    </section>

    <section class="panel">
      <h2>今天我们的主池</h2>
      <div class="panel-sub">把 task sheet / top6 主池也拉进来，避免学习只盯着旧库存 ready 稿。</div>
      <table>
        <thead>
          <tr>
            <th>状态</th>
            <th>主题</th>
            <th>题材带</th>
            <th>为什么保留</th>
          </tr>
        </thead>
        <tbody>{selection_topic_rows_html}</tbody>
      </table>
    </section>

    <section class="panel">
      <h2>裁判结论</h2>
      <div class="panel-sub">这里回答“哪边更优、为什么、下轮怎么改”。</div>
      <ul class="takeaways">{selection_verdicts_html}</ul>
    </section>

    <section class="panel">
      <h2>题材错位与补位</h2>
      <div class="panel-sub">把“别人做了我们没做”和“我们主动做差异化”的对象分开看。</div>
      <div class="draft-grid">{selection_delta_cards_html}</div>
    </section>

    <section class="panel">
      <h2>我们差在哪</h2>
      <div class="panel-sub">这里只放高杠杆差距，不做碎碎念。</div>
      <div class="draft-grid">{gap_cards_html}</div>
    </section>

    <section class="panel">
      <h2>优化建议表</h2>
      <div class="panel-sub">这层不是总结，而是把学习结果转成真正要落到岗位和能力层的动作。</div>
      <table>
        <thead>
          <tr>
            <th>建议</th>
            <th>Owner</th>
            <th>落地层</th>
            <th>状态</th>
            <th>下一步</th>
            <th>落点</th>
          </tr>
        </thead>
        <tbody>{optimization_rows_html}</tbody>
      </table>
    </section>

    <section class="panel">
      <h2>反哺到岗位的动作</h2>
      <div class="panel-sub">学习结果必须写回业务岗，而不是只停在总结和观后感。</div>
      <table>
        <thead>
          <tr>
            <th>Owner</th>
            <th>下轮必须落成什么动作</th>
          </tr>
        </thead>
        <tbody>{selection_role_rows_html}</tbody>
      </table>
    </section>

    <section class="panel">
      <h2>下一步动作</h2>
      <div class="panel-sub">这些动作直接对应当前的流程返修与明天的学习增量。</div>
      <ul class="takeaways">{next_actions_html}</ul>
    </section>
  </div>
</body>
</html>"""


def write_outputs(snapshot: dict[str, Any], write_log: bool = False) -> dict[str, Path]:
    paths = output_paths(snapshot["meta"]["date"])
    rulebook = rulebook_paths(snapshot["meta"]["date"])
    FRONTSTAGE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    BRAND_ROOT.mkdir(parents=True, exist_ok=True)
    paths["markdown"].write_text(render_markdown(snapshot), encoding="utf-8")
    paths["html"].write_text(render_html(snapshot), encoding="utf-8")
    paths["json"].write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    rulebook_md = build_rulebook_markdown(snapshot)
    rulebook["dated"].write_text(rulebook_md, encoding="utf-8")
    rulebook["latest"].write_text(rulebook_md, encoding="utf-8")
    knowledge_builder.build_assets_from_snapshot(snapshot)

    if write_log:
        lines = [
            "# Head Media Learning Board Refresh",
            "",
            f"- `generated_at`: `{snapshot['meta']['generated_at']}`",
            f"- `date`: `{snapshot['meta']['date']}`",
            f"- `sample_count`: `{snapshot['overview']['sample_count']}`",
            f"- `ready_topic_count`: `{snapshot['overview']['ready_topic_count']}`",
            "",
            "## Gap Cards",
            "",
        ]
        for card in snapshot["gap_cards"]:
            lines.append(f"- `{card['title']}`｜`{card['severity']}`｜{card['current_gap']}")
        lines.extend(
            [
                "",
                "## Optimization Items",
                "",
            ]
        )
        for item in snapshot["optimization_items"]:
            lines.append(f"- `{item['title']}`｜`{item['status_label']}`｜{item['next_action']}")
        paths["log"].write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return paths


def main() -> None:
    args = parse_args()
    snapshot = build_snapshot(args.date, count=args.count, window_start=args.window_start, window_end=args.window_end)
    if args.write:
        paths = write_outputs(snapshot, write_log=args.write_log)
        print(paths["html"])
        return
    print(json.dumps(snapshot, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

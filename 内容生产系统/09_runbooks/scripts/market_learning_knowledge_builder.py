#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from statistics import median
from typing import Any
from zoneinfo import ZoneInfo

_REPO_ROOT = None
for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "content_system" / "paths.py").exists():
        _REPO_ROOT = _parent
        sys.path.insert(0, str(_parent / "src"))
        break
if _REPO_ROOT is None:
    raise RuntimeError("Cannot locate repository root")
from content_system.paths import get_project_paths

import market_learning_memo_builder as memo_builder
from market_wechat_source_defs import target_by_source_name


CN_TZ = ZoneInfo("Asia/Shanghai")
ROOT = get_project_paths(_REPO_ROOT).legacy_content_root
FRONTSTAGE_DIR = ROOT / "11_frontstage"
BRAND_ROOT = ROOT / "08_brand_assets"
KNOWLEDGE_ROOT = BRAND_ROOT / "learning_knowledge_assets"
CREATOR_DIR = KNOWLEDGE_ROOT / "creator_dossiers"
CREATOR_PACK_DIR = KNOWLEDGE_ROOT / "creator_skill_packs"
CONTENT_TYPE_DIR = KNOWLEDGE_ROOT / "content_type_playbooks"
PACKAGING_DIR = KNOWLEDGE_ROOT / "packaging_playbooks"
VISUAL_DIR = KNOWLEDGE_ROOT / "visual_playbooks"
FAILURE_DIR = KNOWLEDGE_ROOT / "failure_patterns"
LATEST_INDEX_PATH = KNOWLEDGE_ROOT / "latest__learning-knowledge-index.md"
REGISTRY_PATH = KNOWLEDGE_ROOT / "latest__learning-knowledge-registry.json"
STYLE_ROUTER_PATH = KNOWLEDGE_ROOT / "latest__style-router.md"
PACKET_DIR = ROOT / "02_topic_radar" / "source_packets"
LOG_DIR = ROOT / "10_logs"
DEEP_CAPTURE_SCRIPT = ROOT / "09_runbooks" / "scripts" / "market_wechat_deep_capture_round.py"
RSS_BASE_URL = "http://localhost:8001/rss"

SOURCE_SLUG_OVERRIDES = {
    "数字生命卡兹克": "digitallife-khazix",
    "赛博禅心": "cyber-zenmind",
    "饼干哥哥AGI": "cookie-brother-agi",
    "袋鼠帝AI客栈": "kangaroo-ai-inn",
    "机器之心": "jiqizhixin",
    "量子位": "qbitai",
    "智东西": "zhidx",
}

OVERLAY_SKILL_NAMES = {
    "数字生命卡兹克": "th-style-overlay-digitallife-khazix",
    "赛博禅心": "th-style-overlay-cyber-zenmind",
    "饼干哥哥AGI": "th-style-overlay-cookie-brother-agi",
    "袋鼠帝AI客栈": "th-style-overlay-kangaroo-ai-inn",
    "量子位": "th-style-overlay-qbitai",
    "机器之心": "th-style-overlay-jiqizhixin",
    "智东西": "th-style-overlay-zhidx",
}

CREATOR_ORDER = [
    "数字生命卡兹克",
    "赛博禅心",
    "饼干哥哥AGI",
    "袋鼠帝AI客栈",
    "量子位",
    "机器之心",
    "智东西",
]

BACKFILL_REQUIRED_CREATORS = {
    "数字生命卡兹克",
    "赛博禅心",
    "饼干哥哥AGI",
    "袋鼠帝AI客栈",
}

CONTENT_TYPE_PLAYBOOKS = [
    {
        "slug": "event_explainer",
        "title": "事件科普 / 热点解释",
        "audience": "刚听说这件事、但上下文还不完整的泛 AI 读者",
        "opening": "先把对象、事件和 why now 说透，再给判断；不要让读者在抽象概念里迷路。",
        "evidence": "第一证据锚点尽量前置，可以是截图、原话、数字或结构图。",
        "visuals": "优先用证据图和解释图；不要全文都在抽象分析以后才突然给图。",
        "avoid": "先讲大框架，再慢慢告诉读者发生了什么。",
    },
    {
        "slug": "product_experience",
        "title": "产品推荐 / 工具体验",
        "audience": "想马上试、想知道值不值得用的实操型读者",
        "opening": "优先用‘少做哪几步 / 节省什么成本 / 解决什么卡点’开场。",
        "evidence": "用真实操作链路、界面截图、前后对比而不是抽象感受。",
        "visuals": "界面图、流程图、前后对比图优先于抽象解释卡。",
        "avoid": "只有‘好用 / 惊艳 / 太强了’这类感受，没有步骤和边界。",
    },
    {
        "slug": "industry_analysis",
        "title": "产业判断 / 商业分析",
        "audience": "从业者、投资人、对商业含义敏感的高意图读者",
        "opening": "先给结论，但必须尽快补业务含义、关键变量和风险边界。",
        "evidence": "财务口径、竞争格局、商业化变量、供给链等证据要尽早出现。",
        "visuals": "数字卡、竞争结构图、变量关系图比纯情绪型配图更重要。",
        "avoid": "把文章写成抽象行业评论，读者读完不知道能带走什么判断。",
    },
    {
        "slug": "builder_teardown",
        "title": "教程 / Builder 拆解",
        "audience": "开发者、产品经理、AI builder、人群更愿意为方法买单",
        "opening": "用过程感、误判点或关键路径切入，而不是只晒结论。",
        "evidence": "路径、步骤、变量、限制条件都应被显式写出。",
        "visuals": "步骤卡、结构图、变量表、流程图优先。",
        "avoid": "只给结论不给路径，只晒结果不说前提。",
    },
    {
        "slug": "opinionated_commentary",
        "title": "观点 / 争议型题材",
        "audience": "已经感知到热度、想看更高层判断的人",
        "opening": "第一屏可以亮立场，但必须立刻补证据和边界。",
        "evidence": "证据与反例都要前置，避免把‘敢说’写成‘乱说’。",
        "visuals": "解释卡和证据图的组合优先于纯装饰型头图。",
        "avoid": "只有态度没有证据，或者只靠狠话制造情绪。",
    },
]

SOURCE_STYLE_HINTS = {
    "数字生命卡兹克": {
        "positioning": "强活人感的 AI 长文创作者，擅长把观点、方法、情绪与判断揉在一起。",
        "best_for": ["趋势判断", "方法论文章", "需要明显作者人格的公众号长文"],
        "borrow": [
            "判断句先行，但很快补上下文，不让读者一直悬空。",
            "段落节奏强，长短句和独立成段更明显。",
            "像一个有见识的人在认真聊天，而不是信息播报器。",
        ],
        "avoid": [
            "直接照搬他的口头禅、情绪姿态和第一人称浓度。",
            "让 TH Capital 变成个人博主腔调，导致品牌人格漂移。",
        ],
    },
    "赛博禅心": {
        "positioning": "偏 workflow / skill / builder 的方法型创作者，更擅长把复杂方法翻译成可执行结构。",
        "best_for": ["workflow 拆解", "skill / agent / builder 方法论", "产品与流程级文章"],
        "borrow": [
            "对象、动作、收益同步落地。",
            "把复杂概念翻成用户能直接操作的流程。",
            "方法论和具体操作之间切换自然。",
        ],
        "avoid": [
            "把流程稿写成工具说明书，失去判断和品牌表达。",
            "只学术语与框架，不学转译能力。",
        ],
    },
    "饼干哥哥AGI": {
        "positioning": "偏实操收益导向，适合把‘值不值得用、怎么省钱、怎么起步’写清楚。",
        "best_for": ["成本 / 效率类题材", "实操体验稿", "对普通读者有明确即时收益的工具稿"],
        "borrow": [
            "收益点前置。",
            "少空话，多动作、多对比。",
            "更强的‘看完就能试’感。",
        ],
        "avoid": [
            "把所有题都写成省钱攻略。",
            "只剩结果导向，缺少证据和边界说明。",
        ],
    },
    "袋鼠帝AI客栈": {
        "positioning": "偏接地气和可玩性，更擅长把复杂本地 agent / 工具体验写得更好入口。",
        "best_for": ["本地 agent", "可玩性强的工具体验", "低门槛上手向内容"],
        "borrow": [
            "用更轻的门槛把读者拉进来。",
            "多写真实使用感和场景感。",
            "让工具类文章少一点说明书感。",
        ],
        "avoid": [
            "为了接地气而牺牲判断力。",
            "把复杂技术问题写得过于轻佻。",
        ],
    },
    "量子位": {
        "positioning": "头部快热点媒体，强在对象识别、事件抓手和大众传播转译。",
        "best_for": ["大热点快拆", "冷启动读者较多的事件解释", "需要强传播入口的标题和首屏"],
        "borrow": [
            "对象 + 事件 + why now 更早落地。",
            "大众 stakes 更早出现。",
            "首图和早段证据更积极。",
        ],
        "avoid": [
            "只学传播壳子，不保留 TH Capital 的判断密度。",
            "为了标题势能过度牺牲证据边界。",
        ],
    },
    "机器之心": {
        "positioning": "偏技术前沿与研究传播，强在把论文、模型和研究进展快速翻译成可传播的事件对象。",
        "best_for": ["模型 / 研究进展", "偏技术的新能力快拆", "需要先把研究对象讲明白的前沿题"],
        "borrow": [
            "对象识别更早，研究题也尽量先落到具体对象和变化。",
            "技术前沿题的首屏不要只讲框架，先讲这次到底多了什么。",
            "研究稿也要更早给图和证据，不让读者全程听抽象术语。",
        ],
        "avoid": [
            "把 TH Capital 写成纯技术媒体快讯。",
            "只学前沿感，不补商业含义和读者 stakes。",
        ],
    },
    "智东西": {
        "positioning": "偏产业、融资和硬信息的头部媒体，强在硬事实与行业变量的快速组织。",
        "best_for": ["融资 / 商业化 / 资本信号", "产业判断", "行业与公司层面的硬信息稿"],
        "borrow": [
            "更快把对象和硬信息钉住。",
            "让商业变量更早出现。",
            "首图和数字证据对齐正文判断。",
        ],
        "avoid": [
            "把 TH Capital 写成传统媒体快讯。",
            "只堆融资数字，不解释业务含义。",
        ],
    },
}

STYLE_ROUTE_RULES = [
    {
        "route": "方法论 / workflow / skill / agent 教程",
        "primary_overlay": "赛博禅心",
        "secondary_overlay": "数字生命卡兹克",
        "support_overlay": "饼干哥哥AGI",
        "apply_layers": "对象落地、步骤结构、背景桥接、活人感判断句、收益点前置",
        "visual_system": "原始证据图 + 约束分类图 + 分层架构图 + workflow 循环图",
        "avoid": "不要把 TH Capital 写成个人博主日记，也不要把流程稿写成工具说明书。",
    },
    {
        "route": "工具体验 / builder 拆解 / 产品推荐",
        "primary_overlay": "饼干哥哥AGI",
        "secondary_overlay": "袋鼠帝AI客栈",
        "support_overlay": "赛博禅心",
        "apply_layers": "收益点前置、步骤感、门槛转译、真实使用场景",
        "visual_system": "对象截图 + 前后对比 + 适合谁/不适合谁矩阵 + 风险提醒卡",
        "avoid": "不要只写感受，不要为了接地气牺牲判断边界。",
    },
    {
        "route": "大热点解释 / 冷启动用户较多的事件稿",
        "primary_overlay": "量子位",
        "secondary_overlay": "机器之心",
        "support_overlay": "数字生命卡兹克",
        "apply_layers": "对象识别、事件抓手、why now、大众 stakes、首屏证据",
        "visual_system": "首屏证据截图 + 对象解释卡 + 时间线/变量图 + 风险边界卡",
        "avoid": "不要只学热点媒体的壳子，必须保留 TH Capital 的判断密度。",
    },
    {
        "route": "产业判断 / 商业分析 / 融资与资本信号",
        "primary_overlay": "智东西",
        "secondary_overlay": "数字生命卡兹克",
        "support_overlay": "量子位",
        "apply_layers": "对象+硬信息前置、商业含义、变量拆解、风险边界",
        "visual_system": "原始证据图 + 数字/信号卡 + 竞争/链路关系图 + 风险边界卡",
        "avoid": "不要把文章写成传统媒体快讯，也不要只有融资数字没有判断。",
    },
    {
        "route": "技术前沿 / 模型进展 / 研究传播",
        "primary_overlay": "机器之心",
        "secondary_overlay": "量子位",
        "support_overlay": "数字生命卡兹克",
        "apply_layers": "对象识别、研究转译、首屏图证、能力变化表达",
        "visual_system": "论文/repo 证据图 + 能力变化卡 + 结构或 benchmark 图 + 实际意义卡",
        "avoid": "不要只剩技术前沿感，不补商业 / 用户意义。",
    },
]

JUDGMENT_TOKENS = ("不是", "真正", "本质", "核心", "关键", "问题", "其实", "很多人", "先说结论", "说白了")
QUESTION_TOKENS = ("为什么", "怎么", "如何", "到底", "是不是", "会不会", "吗", "呢")
SCENE_TOKENS = ("今天", "刚刚", "昨晚", "周末", "最近", "路上", "我", "我们")
EVENT_TOKENS = ("发布", "开源", "上线", "官宣", "签下", "回归", "收购", "融资", "突破", "发布了")
BENEFIT_TOKENS = ("值不值得", "怎么", "教程", "攻略", "省", "效率", "上手", "实测", "避坑", "必装", "手把手")
IMAGE_RE = re.compile(r"^!\[.*?\]\((https?://[^)]+)\)")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
NUMBER_RE = re.compile(r"\d")


def clean(value: Any, fallback: str = "n/a") -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip().strip("`")
    return text if text else fallback


def now_cst() -> str:
    return datetime.now(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def token_for_date(date_text: str) -> str:
    return date_text.replace("-", "")


def safe_slug(value: str) -> str:
    if value in SOURCE_SLUG_OVERRIDES:
        return SOURCE_SLUG_OVERRIDES[value]
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug or f"source-{abs(hash(value)) % 100000:05d}"


def ascii_slug(value: str, fallback: str = "item") -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    slug = re.sub(r"_+", "_", slug)
    return slug[:72] or fallback


def unique_lines(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        normalized = clean(value, "")
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return ordered


def median_or_none(values: list[int | float]) -> float | None:
    cleaned = [value for value in values if value is not None]
    if not cleaned:
        return None
    return float(median(cleaned))


def median_or_na(values: list[int | float]) -> str:
    result = median_or_none(values)
    if result is None:
        return "n/a"
    if abs(result - round(result)) < 1e-9:
        return str(int(round(result)))
    return f"{result:.2f}".rstrip("0").rstrip(".")


def percent(value: float) -> str:
    return f"{value * 100:.0f}%"


def snapshot_path(date_text: str) -> Path:
    return FRONTSTAGE_DIR / f"{token_for_date(date_text)}__head-media-learning-board.snapshot.json"


def load_snapshot(date_text: str) -> dict[str, Any]:
    path = snapshot_path(date_text)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_dirs() -> None:
    for path in [
        KNOWLEDGE_ROOT,
        CREATOR_DIR,
        CREATOR_PACK_DIR,
        CONTENT_TYPE_DIR,
        PACKAGING_DIR,
        VISUAL_DIR,
        FAILURE_DIR,
        LOG_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def read_raw_body(path: Path | None) -> str:
    if path is None or not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def parse_kv_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = KV_RE.match(raw_line.strip())
        if not match:
            continue
        key, value = match.groups()
        fields[clean(key)] = clean(value)
    return fields


def load_creator_article(path: Path) -> memo_builder.DeepArticle | None:
    strict = memo_builder.load_article(path)
    if strict is not None:
        return strict

    fields = parse_kv_fields(path)
    source_name = clean(fields.get("source_name", "n/a"))
    if source_name not in CREATOR_ORDER:
        return None
    status = clean(fields.get("status", "n/a"))
    if status != "full_text":
        return None

    title = clean(fields.get("title", "n/a"))
    try:
        image_count = int(clean(fields.get("image_count", "0"), "0"))
    except ValueError:
        image_count = 0
    try:
        normalized_char_count = int(clean(fields.get("normalized_char_count", "0"), "0"))
    except ValueError:
        normalized_char_count = 0
    raw_body_value = fields.get("raw_export_copy_path") or fields.get("x_reader_export_path") or "n/a"
    raw_body_path = Path(raw_body_value) if raw_body_value != "n/a" else None
    raw_text = read_raw_body(raw_body_path)
    paragraphs, first_image_after_text_paragraphs, image_break_count = memo_builder.extract_content_paragraphs(raw_text)
    if len(paragraphs) < 4 and normalized_char_count < 180:
        return None
    return memo_builder.DeepArticle(
        path=path,
        title=title,
        source_name=source_name,
        canonical_url=clean(fields.get("canonical_url", "n/a")),
        published_at=clean(fields.get("published_at", "n/a")),
        status=status,
        image_count=image_count,
        normalized_char_count=normalized_char_count,
        raw_body_path=raw_body_path,
        opening_paragraphs=paragraphs[:6],
        first_image_after_text_paragraphs=first_image_after_text_paragraphs,
        image_break_count=image_break_count,
        published_dt=memo_builder.parse_cst(fields.get("published_at", "")),
        artifact_dt=memo_builder.parse_artifact_dt(path),
        export_day=memo_builder.parse_export_day(raw_body_path),
    )


def creator_learning_recency(article: memo_builder.DeepArticle) -> datetime:
    if article.published_dt is not None:
        return article.published_dt
    if article.export_day is not None:
        return datetime.combine(article.export_day, datetime.min.time(), tzinfo=CN_TZ)
    if article.artifact_dt is not None:
        return article.artifact_dt
    return datetime(1970, 1, 1, tzinfo=CN_TZ)


def parse_packet_field(text: str, field: str) -> str | None:
    pattern = re.compile(rf"^- `{re.escape(field)}`: `(.*)`$", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def existing_packet_urls(source_name: str) -> set[str]:
    urls: set[str] = set()
    for path in PACKET_DIR.glob("*__source-packet.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if f"- `source_name`: `{source_name}`" not in text:
            continue
        canonical_url = parse_packet_field(text, "canonical_url")
        if canonical_url:
            urls.add(canonical_url)
    return urls


def load_distinct_creator_articles(date_text: str) -> dict[str, list[memo_builder.DeepArticle]]:
    target_day = datetime.fromisoformat(f"{date_text}T00:00:00+08:00").date()
    deduped: dict[tuple[str, str], memo_builder.DeepArticle] = {}
    for path in memo_builder.DEEP_ARTICLE_ROOT.glob("*__deep-article.md"):
        article = load_creator_article(path)
        if not article or article.source_name not in CREATOR_ORDER:
            continue
        if memo_builder.article_is_future(article, target_day):
            continue
        key = (article.source_name, clean(article.canonical_url, article.title))
        current = deduped.get(key)
        if current is None or memo_builder.article_recency(article) > memo_builder.article_recency(current):
            deduped[key] = article
    grouped: dict[str, list[memo_builder.DeepArticle]] = {source_name: [] for source_name in CREATOR_ORDER}
    for article in deduped.values():
        grouped.setdefault(article.source_name, []).append(article)
    for source_name in grouped:
        grouped[source_name].sort(key=creator_learning_recency, reverse=True)
    return grouped


def strip_html_fragment(text: str) -> str:
    text = unescape(text or "")
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</p\s*>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("\xa0", " ")
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def parse_rss_datetime(value: str | None) -> str:
    if not value:
        return "n/a"
    try:
        return parsedate_to_datetime(value).astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")
    except Exception:
        return clean(value)


def fetch_recent_rss_items(source_name: str, max_pages: int = 6) -> list[dict[str, str]]:
    target = target_by_source_name(source_name)
    if target is None:
        return []
    feed_id = clean(target.get("rss_feed_id", ""), "")
    if not feed_id:
        return []
    packet_prefix = clean(target.get("packet_prefix", safe_slug(source_name)), safe_slug(source_name))
    source_id = clean(target.get("source_id", ""), "")
    seen_urls: set[str] = set()
    items: list[dict[str, str]] = []
    for page_index in range(max_pages):
        offset = page_index * 10
        encoded_id = urllib.parse.quote(feed_id, safe="")
        url = f"{RSS_BASE_URL}/{encoded_id}?offset={offset}"
        with urllib.request.urlopen(url, timeout=30) as response:
            xml_text = response.read().decode("utf-8", "ignore")
        root = ET.fromstring(xml_text)
        page_items = root.findall("./channel/item")
        if not page_items:
            break
        new_items = 0
        for item in page_items:
            canonical_url = clean(item.findtext("guid") or item.findtext("link"), "")
            if not canonical_url or canonical_url in seen_urls:
                continue
            seen_urls.add(canonical_url)
            title = clean(item.findtext("title"), "untitled wechat item")
            summary = clean(strip_html_fragment(item.findtext("description") or ""), "")
            items.append(
                {
                    "source_id": source_id,
                    "source_name": source_name,
                    "packet_prefix": packet_prefix,
                    "feed_id": feed_id,
                    "source_url": f"{RSS_BASE_URL}/{feed_id}",
                    "canonical_url": canonical_url,
                    "title": title,
                    "summary": summary or title,
                    "published_at": parse_rss_datetime(item.findtext("pubDate")),
                }
            )
            new_items += 1
        if new_items == 0:
            break
    return items


def packet_slug_for_item(packet_prefix: str, title: str, canonical_url: str) -> str:
    fallback = ascii_slug(canonical_url, "wechat_article")
    title_slug = ascii_slug(title, fallback)
    return f"{packet_prefix}_{title_slug}"[:120]


def render_backfill_source_packet(item: dict[str, str], logical_date: str) -> str:
    timestamp = now_cst()
    packet_slug = item["packet_slug"]
    packet_key = f"{token_for_date(logical_date)}__{packet_slug}"
    packet_id = f"packet_{token_for_date(logical_date)}_{ascii_slug(item['canonical_url'], 'wechat')}"
    summary = clean(item.get("summary", ""), item["title"])
    return (
        "# Source Packet\n\n"
        "## Header\n\n"
        f"- `packet_id`: `{packet_id}`\n"
        f"- `packet_key`: `{packet_key}`\n"
        f"- `source_id`: `{item['source_id']}`\n"
        f"- `source_name`: `{item['source_name']}`\n"
        "- `source_type`: `wechat_rss_feed`\n"
        "- `platform`: `wechat`\n"
        "- `region`: `cn`\n"
        f"- `source_url`: `{item['source_url']}`\n"
        f"- `canonical_url`: `{item['canonical_url']}`\n"
        f"- `title`: `{item['title']}`\n"
        f"- `author_or_channel`: `{item['source_name']}`\n"
        f"- `published_at`: `{item['published_at']}`\n"
        f"- `captured_at`: `{timestamp}`\n"
        "- `language`: `zh`\n"
        "- `content_type`: `wechat article`\n"
        "- `capture_method`: `wechat-rss-offset-backfill`\n"
        "- `normalization_method`: `rss_entry`\n"
        "- `translation_needed`: `no`\n"
        "- `status`: `normalized`\n\n"
        "## Quick Summary\n\n"
        f"- `summary`: {summary}\n"
        f"- `topic_tags`: `wechat`, `creator-skill-backfill`, `{ascii_slug(item['source_name'], 'wechat_source')}`\n"
        "- `quote_candidates`:\n"
        f"  - `{item['title']}`\n"
        f"  - `{summary[:80]}`\n\n"
        "## Source Notes\n\n"
        "- `signal_quality`: `high`\n"
        "- `primary_source`: `partial`\n"
        "- `verification_status`: `wechat-rss-entry`\n"
        "- `citation_reliability`: `medium`\n"
        f"- `why_source_matters`: {item['source_name']} 是正在用于风格蒸馏的对标公众号，需要进入 creator skill pack 的 20 篇学习主链。\n"
        "- `caveat`: RSS 条目只用于补通学习主链；正式写作仍要回链一手证据和官方信息。\n"
    )


def create_backfill_packets(source_name: str, logical_date: str) -> list[Path]:
    existing_urls = existing_packet_urls(source_name)
    rss_items = fetch_recent_rss_items(source_name)
    written: list[Path] = []
    timestamp = now_cn().strftime("%Y%m%d_%H%M%S")
    for item in rss_items:
        if item["canonical_url"] in existing_urls:
            continue
        item = dict(item)
        item["packet_slug"] = packet_slug_for_item(item["packet_prefix"], item["title"], item["canonical_url"])
        packet_path = PACKET_DIR / f"{timestamp}__{item['packet_slug']}__source-packet.md"
        if packet_path.exists():
            continue
        packet_path.write_text(render_backfill_source_packet(item, logical_date), encoding="utf-8")
        written.append(packet_path)
    return written


def run_deep_capture(logical_date: str, packet_paths: list[Path]) -> dict[str, Any]:
    if not packet_paths:
        return {"returncode": 0, "stdout": "", "stderr": "", "packet_count": 0}
    command = [
        "python3",
        str(DEEP_CAPTURE_SCRIPT),
        "--date",
        logical_date,
        "--timeout-seconds",
        "180",
        "--write",
    ]
    for path in packet_paths:
        command.extend(["--packet-path", str(path)])
    completed = subprocess.run(command, capture_output=True, text=True)
    return {
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "packet_count": len(packet_paths),
    }


def backfill_missing_creator_samples(date_text: str, min_samples: int) -> dict[str, Any]:
    summary: dict[str, Any] = {"generated_at": now_cst(), "date": date_text, "sources": [], "deep_capture": {}}
    before = load_distinct_creator_articles(date_text)
    packet_paths: list[Path] = []
    for source_name in CREATOR_ORDER:
        current_count = len(before.get(source_name, []))
        row: dict[str, Any] = {
            "source_name": source_name,
            "before_count": current_count,
            "needs_backfill": source_name in BACKFILL_REQUIRED_CREATORS and current_count < min_samples,
            "packet_paths": [],
        }
        if row["needs_backfill"]:
            created = create_backfill_packets(source_name, date_text)
            row["packet_paths"] = [str(path) for path in created]
            packet_paths.extend(created)
        summary["sources"].append(row)
    summary["deep_capture"] = run_deep_capture(date_text, packet_paths)
    if summary["deep_capture"]["returncode"] != 0:
        raise SystemExit(
            "deep capture failed:\n"
            + clean(summary["deep_capture"]["stdout"], "")
            + ("\n" + clean(summary["deep_capture"]["stderr"], "") if clean(summary["deep_capture"]["stderr"], "") else "")
        )
    return summary


def persist_backfill_summary(summary: dict[str, Any]) -> Path:
    timestamp = now_cn().strftime("%Y%m%d_%H%M%S")
    path = LOG_DIR / f"{timestamp}__creator-skill-pack-backfill.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def opening_text(article: memo_builder.DeepArticle) -> str:
    return clean(" ".join(article.opening_paragraphs[:3]), "")


def classify_opening(text: str) -> str:
    snippet = clean(text, "").strip("。；：:，, ")
    if not snippet:
        return "对象/事件先落地"
    first_window = snippet[:80]
    if any(token in first_window for token in QUESTION_TOKENS) or "？" in first_window or "?" in first_window:
        return "问题/提问切入"
    if NUMBER_RE.search(first_window[:24]) and any(token in first_window for token in ["层", "步", "个", "类", "条"]):
        return "数字/清单切入"
    if any(token in first_window for token in JUDGMENT_TOKENS):
        return "判断句先行"
    if any(token in first_window for token in SCENE_TOKENS):
        return "场景/自述切入"
    if any(token in first_window for token in EVENT_TOKENS):
        return "事件/变化切入"
    return "对象/事件先落地"


def classify_title(title: str) -> str:
    normalized = clean(title, "")
    if any(token in normalized for token in BENEFIT_TOKENS):
        return "收益/教程型标题"
    if any(token in normalized for token in ("刚刚", "突然", "开源", "发布", "收购", "融资", "突破", "回归", "IPO")):
        return "快讯/变化型标题"
    if any(token in normalized for token in ("为什么", "聊聊", "到底", "真正", "会不会", "如何看待")):
        return "观点/判断型标题"
    if any(token in normalized for token in ("实测", "体验", "拆解", "复盘", "案例", "终于找到")):
        return "案例/体验型标题"
    return "对象直给型标题"


def article_detail(article: memo_builder.DeepArticle) -> dict[str, Any]:
    raw_text = read_raw_body(article.raw_body_path)
    paragraphs, _first_image, _image_break_count = memo_builder.extract_content_paragraphs(raw_text)
    paragraph_lengths = [len(re.sub(r"\s+", "", paragraph)) for paragraph in paragraphs]
    short_para_ratio = (
        sum(length <= 30 for length in paragraph_lengths) / len(paragraph_lengths) if paragraph_lengths else 0.0
    )
    opening = opening_text(article)
    image_density = (article.image_count * 1000 / article.normalized_char_count) if article.normalized_char_count else 0.0
    return {
        "article": article,
        "opening_text": opening,
        "opening_mode": classify_opening(opening),
        "title_mode": classify_title(article.title),
        "paragraph_count": len(paragraphs),
        "median_paragraph_chars": int(median(paragraph_lengths)) if paragraph_lengths else 0,
        "short_para_ratio": short_para_ratio,
        "image_density_per_1000_chars": round(image_density, 2),
        "first_person_opening": any(token in opening for token in ("我", "我们")),
        "reader_address_opening": any(token in opening for token in ("你", "大家", "读者")),
    }


def detail_note(detail: dict[str, Any]) -> str:
    article = detail["article"]
    notes: list[str] = [detail["opening_mode"]]
    if article.first_image_after_text_paragraphs is not None:
        if article.first_image_after_text_paragraphs <= 2:
            notes.append("很早上图")
        elif article.first_image_after_text_paragraphs <= 5:
            notes.append("判断后很快补图")
        else:
            notes.append("结构展开后再上图")
    if detail["short_para_ratio"] >= 0.35:
        notes.append("短段密度高")
    if article.image_count >= 6:
        notes.append("图文节奏偏密")
    return "；".join(unique_lines(notes)[:4])


def detail_record(detail: dict[str, Any]) -> dict[str, Any]:
    article = detail["article"]
    return {
        "title": article.title,
        "published_at": article.published_at,
        "canonical_url": article.canonical_url,
        "deep_article_path": str(article.path),
        "char_count": article.normalized_char_count,
        "image_count": article.image_count,
        "first_image_after_text_paragraphs": article.first_image_after_text_paragraphs,
        "opening_mode": detail["opening_mode"],
        "title_mode": detail["title_mode"],
        "short_para_ratio": round(detail["short_para_ratio"], 3),
        "opening_excerpt": clean(detail["opening_text"], ""),
        "note": detail_note(detail),
    }


def collect_examples(details: list[dict[str, Any]], key: str, value: str, limit: int = 3) -> list[str]:
    rows: list[str] = []
    for detail in details:
        if detail.get(key) != value:
            continue
        article = detail["article"]
        rows.append(f"`{article.title}`｜{clean(detail['opening_text'], '')[:72]}")
        if len(rows) >= limit:
            break
    return rows


def summarize_creator(source_name: str, articles: list[memo_builder.DeepArticle], min_samples: int) -> dict[str, Any]:
    hint = SOURCE_STYLE_HINTS[source_name]
    selected = sorted(articles, key=creator_learning_recency, reverse=True)[:min_samples]
    details = [article_detail(article) for article in selected]
    opening_counter = Counter(detail["opening_mode"] for detail in details)
    title_counter = Counter(detail["title_mode"] for detail in details)
    first_image_values = [
        detail["article"].first_image_after_text_paragraphs
        for detail in details
        if detail["article"].first_image_after_text_paragraphs is not None
    ]
    summary = {
        "source_name": source_name,
        "slug": safe_slug(source_name),
        "overlay_skill_name": OVERLAY_SKILL_NAMES[source_name],
        "sample_gate_passed": len(selected) >= min_samples,
        "sample_count": len(selected),
        "total_distinct_available": len(articles),
        "observed_window": {
            "latest": max((article.published_at for article in selected), default="n/a"),
            "oldest": min((article.published_at for article in selected), default="n/a"),
        },
        "median_char_count": int(median_or_none([detail["article"].normalized_char_count for detail in details]) or 0),
        "median_image_count": median_or_none([detail["article"].image_count for detail in details]),
        "median_first_image_after_text_paragraphs": median_or_none(first_image_values),
        "median_short_para_ratio": float(median_or_none([detail["short_para_ratio"] for detail in details]) or 0.0),
        "median_image_density_per_1000_chars": float(
            median_or_none([detail["image_density_per_1000_chars"] for detail in details]) or 0.0
        ),
        "early_image_share": (
            sum(
                detail["article"].first_image_after_text_paragraphs is not None
                and detail["article"].first_image_after_text_paragraphs <= 2
                for detail in details
            )
            / len(details)
            if details
            else 0.0
        ),
        "dense_visual_share": (
            sum(detail["article"].image_count >= 6 for detail in details) / len(details) if details else 0.0
        ),
        "first_person_opening_share": (
            sum(detail["first_person_opening"] for detail in details) / len(details) if details else 0.0
        ),
        "reader_address_opening_share": (
            sum(detail["reader_address_opening"] for detail in details) / len(details) if details else 0.0
        ),
        "opening_modes": dict(opening_counter),
        "title_modes": dict(title_counter),
        "details": details,
        "hint": hint,
    }
    return summary


def mode_lines(summary: dict[str, Any], key: str) -> list[str]:
    counter = Counter(summary[key])
    total = max(summary["sample_count"], 1)
    lines: list[str] = []
    for label, count in counter.most_common(3):
        examples = collect_examples(summary["details"], "opening_mode" if key == "opening_modes" else "title_mode", label, limit=2)
        example_text = "；".join(examples) if examples else "n/a"
        lines.append(f"- `{label}`：`{count}/{total}`，示例：{example_text}")
    return lines or ["- 暂无稳定分布。"]


def derived_text_moves(summary: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    top_mode = Counter(summary["opening_modes"]).most_common(1)[0][0] if summary["opening_modes"] else ""
    if top_mode == "判断句先行":
        lines.append("开头先抛判断，但必须在 1-2 段内把对象、变化和 stakes 补齐。")
    elif top_mode == "问题/提问切入":
        lines.append("开头可以用问题把读者拉住，但问题后面必须立刻兑现对象与结论。")
    elif top_mode == "场景/自述切入":
        lines.append("允许有限的场景或自述做入口，但不能让作者表演盖过事实。")
    else:
        lines.append("优先先把对象和变化钉住，再展开判断，不让读者在抽象段落里迷路。")
    if summary["median_short_para_ratio"] >= 0.32:
        lines.append("段落要明显偏短，关键判断句和风险句应独立成段。")
    elif summary["median_short_para_ratio"] >= 0.2:
        lines.append("长短段落要交替，不能整篇都用等长说明书段落。")
    if summary["first_person_opening_share"] >= 0.35:
        lines.append("可以借一点有限的一人称视角或即时观察，但只用来抬高可读性，不用来偷换论证。")
    if summary["reader_address_opening_share"] >= 0.3:
        lines.append("对读者的直接喊话要服务收益或风险提示，不能只是模板式‘你一定要看’。")
    return unique_lines(lines)


def derived_visual_moves(summary: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    first_image = summary["median_first_image_after_text_paragraphs"]
    if first_image is not None and first_image <= 2:
        lines.append("正文第一张图必须很早出现，承担对象锚定或原始证据职责。")
    elif first_image is not None and first_image <= 5:
        lines.append("先给判断，再很快补一张证据或解释图，不要把图拖到中后段。")
    else:
        lines.append("如果首图靠后，正文前段就要更强地承担对象识别与证据说明。")
    if summary["median_image_count"] is not None and summary["median_image_count"] >= 6:
        lines.append("图文节奏要偏密，不能用 1 张大图顶完整篇结构。")
    if summary["dense_visual_share"] >= 0.4:
        lines.append("适合多张小图或结构卡连续出现，帮助长文分段和换气。")
    if summary["early_image_share"] >= 0.5:
        lines.append("首屏图优先是证据图或对象图，不是抽象气氛图。")
    return unique_lines(lines)


def corpus_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at": now_cst(),
        "source_name": summary["source_name"],
        "slug": summary["slug"],
        "overlay_skill_name": summary["overlay_skill_name"],
        "sample_gate_passed": summary["sample_gate_passed"],
        "distinct_recent_articles_used": summary["sample_count"],
        "total_distinct_available": summary["total_distinct_available"],
        "observed_window": summary["observed_window"],
        "aggregate": {
            "median_char_count": summary["median_char_count"],
            "median_image_count": summary["median_image_count"],
            "median_first_image_after_text_paragraphs": summary["median_first_image_after_text_paragraphs"],
            "median_short_para_ratio": round(summary["median_short_para_ratio"], 3),
            "median_image_density_per_1000_chars": round(summary["median_image_density_per_1000_chars"], 3),
            "early_image_share": round(summary["early_image_share"], 3),
            "dense_visual_share": round(summary["dense_visual_share"], 3),
            "first_person_opening_share": round(summary["first_person_opening_share"], 3),
            "reader_address_opening_share": round(summary["reader_address_opening_share"], 3),
            "opening_modes": summary["opening_modes"],
            "title_modes": summary["title_modes"],
        },
        "articles": [detail_record(detail) for detail in summary["details"]],
    }


def sample_index_markdown(summary: dict[str, Any]) -> str:
    rows = []
    for index, detail in enumerate(summary["details"], start=1):
        article = detail["article"]
        rows.append(
            "| {index} | {title} | {published_at} | {chars} | {images} | {first_image} | {opening_mode} | {note} | [deep article]({path}) | [原文]({url}) |".format(
                index=index,
                title=clean(article.title),
                published_at=clean(article.published_at),
                chars=article.normalized_char_count,
                images=article.image_count,
                first_image=article.first_image_after_text_paragraphs if article.first_image_after_text_paragraphs is not None else "n/a",
                opening_mode=detail["opening_mode"],
                note=detail_note(detail),
                path=article.path,
                url=article.canonical_url,
            )
        )
    return f"""# 20 篇样本索引｜{summary['source_name']}

- `generated_at`: `{now_cst()}`
- `source_name`: `{summary['source_name']}`
- `distinct_recent_articles_used`: `{summary['sample_count']}`
- `overlay_skill_name`: `{summary['overlay_skill_name']}`

## Corpus Window

- `latest_sample`: `{summary['observed_window']['latest']}`
- `oldest_sample`: `{summary['observed_window']['oldest']}`

## Sample Table

| # | 标题 | 发布时间 | 字数 | 图片数 | 首图前文字段落 | 开头类型 | 这篇为什么值得学 | 稿件 | 原文 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
{chr(10).join(rows) if rows else "| n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |"}
"""


def text_patterns_markdown(summary: dict[str, Any]) -> str:
    hint = summary["hint"]
    return f"""# 文本模式｜{summary['source_name']}

- `generated_at`: `{now_cst()}`
- `sample_gate`: `passed ({summary['sample_count']}/20)`
- `median_char_count`: `{summary['median_char_count']}`
- `median_short_para_ratio`: `{summary['median_short_para_ratio']:.2f}`
- `first_person_opening_share`: `{summary['first_person_opening_share']:.2f}`
- `reader_address_opening_share`: `{summary['reader_address_opening_share']:.2f}`

## 开头模式分布

{chr(10).join(mode_lines(summary, "opening_modes"))}

## 标题模式分布

{chr(10).join(mode_lines(summary, "title_modes"))}

## 从 20 篇样本里稳定看到的文本动作

{chr(10).join(f"- {line}" for line in unique_lines(hint['borrow'] + derived_text_moves(summary)))}

## 适合借用的题型

{chr(10).join(f"- {line}" for line in hint['best_for'])}

## 对 TH Capital 的具体改写要求

- 先守品牌判断边界，再借这位作者的节奏和表达层。
- 如果要借作者感，只借“判断如何落地”和“段落如何呼吸”，不借外部人格壳。
- 如果一段话删掉作者名字后更像个人号而不是 TH Capital，就说明借过头了。
"""


def visual_patterns_markdown(summary: dict[str, Any]) -> str:
    sample_rows = []
    for detail in summary["details"][:8]:
        article = detail["article"]
        sample_rows.append(
            f"- `{article.title}`｜图片 `{article.image_count}` 张｜首图前文字段落 `{article.first_image_after_text_paragraphs if article.first_image_after_text_paragraphs is not None else 'n/a'}`｜{detail_note(detail)}"
        )
    return f"""# 视觉模式｜{summary['source_name']}

- `generated_at`: `{now_cst()}`
- `sample_gate`: `passed ({summary['sample_count']}/20)`
- `median_image_count`: `{median_or_na([detail['article'].image_count for detail in summary['details']])}`
- `median_first_image_after_text_paragraphs`: `{median_or_na([detail['article'].first_image_after_text_paragraphs for detail in summary['details'] if detail['article'].first_image_after_text_paragraphs is not None])}`
- `early_image_share`: `{percent(summary['early_image_share'])}`
- `dense_visual_share`: `{percent(summary['dense_visual_share'])}`
- `median_image_density_per_1000_chars`: `{summary['median_image_density_per_1000_chars']:.2f}`

## 从 20 篇样本里稳定看到的图文节奏

{chr(10).join(f"- {line}" for line in derived_visual_moves(summary))}

## 统一审美的落地要求

- 封面和正文图统一走 `proof-first editorial` 路线：纸白 / 浅灰底，深墨文字，只保留 1 个信号色，不做多色霓虹拼盘。
- 封面优先用 `对象截图 / 数字信号卡 / 结构图`，不再用浮夸 AI 人像、赛博脑回路、悬浮机器人、无对象光束图。
- 正文图固定优先级：`原始证据图 > 解释图 > 节奏换气图`；如果某张图既不能证明事实，也不能解释结构，就删掉。
- 解释图优先做 `四类信号卡 / 分层架构图 / workflow 循环图 / 对比矩阵` 这类结构化卡，而不是“看起来像图”的抽象海报。

## 样本里的代表性图文案例

{chr(10).join(sample_rows) if sample_rows else "- 暂无稳定案例。"}
"""


def style_audit_markdown(summary: dict[str, Any]) -> str:
    hint = summary["hint"]
    first_image = summary["median_first_image_after_text_paragraphs"]
    first_image_limit = 3 if first_image is None else max(1, min(4, int(round(first_image))))
    return f"""# 风格审计｜{summary['source_name']}

- `generated_at`: `{now_cst()}`
- `overlay_skill_name`: `{summary['overlay_skill_name']}`
- `sample_gate`: `passed ({summary['sample_count']}/20)`

## 这套 skill 必须出现什么

{chr(10).join(f"- {line}" for line in unique_lines(hint['borrow'] + derived_text_moves(summary)[:2] + derived_visual_moves(summary)[:2]))}

## 这套 skill 绝不能出现什么

{chr(10).join(f"- {line}" for line in hint['avoid'])}
- 不允许把第三方公众号的人格、口头禅或情绪姿态整包搬进 TH Capital。
- 不允许用抽象 AI 图代替原始证据或结构说明。

## 发布前检查单

- 开头是否兑现了这位作者最稳定的入口动作，而不是只贴了几个像他的词？
- 正文是否仍然保留 TH Capital 的判断边界、source refs 和 risk note？
- 长文平台里，第一张正文图是否不晚于前 `{first_image_limit}` 个文字段落？
- 封面、首图和正文主论点是否讲的是同一件事？
- 如果删掉所有风格化句子，这篇稿子还能成立吗？如果不能，说明风格压过了事实。
"""


def skill_card_markdown(summary: dict[str, Any]) -> str:
    hint = summary["hint"]
    pack_dir = CREATOR_PACK_DIR / summary["slug"]
    return f"""# Creator Skill Card｜{summary['source_name']}

- `generated_at`: `{now_cst()}`
- `source_name`: `{summary['source_name']}`
- `overlay_skill_name`: `{summary['overlay_skill_name']}`
- `sample_gate`: `passed ({summary['sample_count']}/20)`
- `latest_sample`: `{summary['observed_window']['latest']}`
- `oldest_sample`: `{summary['observed_window']['oldest']}`
- `median_char_count`: `{summary['median_char_count']}`
- `median_image_count`: `{median_or_na([detail['article'].image_count for detail in summary['details']])}`
- `median_first_image_after_text_paragraphs`: `{median_or_na([detail['article'].first_image_after_text_paragraphs for detail in summary['details'] if detail['article'].first_image_after_text_paragraphs is not None])}`

## 什么时候调用这套 skill

{chr(10).join(f"- {line}" for line in hint['best_for'])}

## 这位创作者最稳定的可借层

{chr(10).join(f"- {line}" for line in unique_lines(hint['borrow'] + derived_text_moves(summary)[:2] + derived_visual_moves(summary)[:2]))}

## 运行时加载顺序

1. 先读 [skill-card.md]({pack_dir / 'skill-card.md'})
2. 写正文前读 [text-patterns.md]({pack_dir / 'text-patterns.md'})
3. 做封面 / 正文图前读 [visual-patterns.md]({pack_dir / 'visual-patterns.md'})
4. 出稿前用 [style-audit.md]({pack_dir / 'style-audit.md'}) 做风格和品牌审计

## 永远不要复制

{chr(10).join(f"- {line}" for line in hint['avoid'])}
"""


def legacy_creator_summary_markdown(summary: dict[str, Any]) -> str:
    pack_dir = CREATOR_PACK_DIR / summary["slug"]
    return f"""# 创作者 skill pack 摘要｜{summary['source_name']}

- `generated_at`: `{now_cst()}`
- `source_name`: `{summary['source_name']}`
- `overlay_skill_name`: `{summary['overlay_skill_name']}`
- `sample_gate`: `passed ({summary['sample_count']}/20)`
- `total_distinct_available`: `{summary['total_distinct_available']}`

## 这是一个真正可调用的 style skill pack

- 这套资产不是“薄 dossier”，而是由最近 20 篇 distinct deep articles 蒸馏出来的 creator skill pack。
- 调用链已经约定：`style-router -> overlay skill -> skill-card / text-patterns / visual-patterns -> style-audit`。

## Pack Files

- [skill-card.md]({pack_dir / 'skill-card.md'})
- [text-patterns.md]({pack_dir / 'text-patterns.md'})
- [visual-patterns.md]({pack_dir / 'visual-patterns.md'})
- [style-audit.md]({pack_dir / 'style-audit.md'})
- [sample-index.md]({pack_dir / 'sample-index.md'})
- [corpus-manifest.json]({pack_dir / 'corpus-manifest.json'})
"""


def content_type_markdown(playbook: dict[str, str]) -> str:
    return f"""# 内容题材打法页｜{playbook['title']}

- `generated_at`: `{now_cst()}`
- `status`: `operational`

## 适合谁

- {playbook['audience']}

## 开头怎么抓

- {playbook['opening']}

## 证据怎么前置

- {playbook['evidence']}

## 图片怎么配

- {playbook['visuals']}

## 不要怎么写

- {playbook['avoid']}
"""


def packaging_playbook_markdown(snapshot: dict[str, Any]) -> str:
    takeaways = snapshot.get("overview", {}).get("takeaways", [])
    ready_drafts = snapshot.get("ready_drafts", [])
    gap_lines = []
    for item in ready_drafts[:5]:
        summary = clean(item.get("gap_summary", ""), "")
        if summary and summary != "当前主问题已经从结构层补到可发布精修层。":
            gap_lines.append(f"- `{clean(item.get('topic_title', ''), 'n/a')}`：{summary}")
    if not gap_lines:
        gap_lines.append("- 当前 ready 稿的主要缺口集中在包装一致性和证据兑现速度。")
    return f"""# TH Capital 包装打法页 v2

- `generated_at`: `{now_cst()}`
- `mode`: `production packaging`

## 包装层固定动作

- 标题必须回答：对象是什么、变化是什么、读者为什么该关心。
- 封面先给利益点或风险点，不要只写‘发生了什么’。
- 首屏前 10%-15% 内必须完成：对象、why now、最低限度背景桥接。
- 标题 / 封面 / 首图 / 正文第一屏必须承诺同一件事。

## 来自最近流程的提醒

{chr(10).join(f"- {line}" for line in takeaways[:4]) if takeaways else "- 学习池暂无额外提醒。"}

## 当前常见包装问题

{chr(10).join(gap_lines)}
"""


def failure_patterns_markdown(snapshot: dict[str, Any]) -> str:
    items = snapshot.get("optimization_items", [])
    rows = []
    for item in items:
        rows.append(
            "| {title} | {owner} | {why} | {next_action} |".format(
                title=clean(item.get("title", "")),
                owner=clean(item.get("owner", "")),
                why=clean(item.get("current_gap", "")),
                next_action=clean(item.get("next_action", "")),
            )
        )
    return f"""# 内容失败模式页 v2

- `generated_at`: `{now_cst()}`
- `mode`: `always-on review checklist`

## 当前系统最常见的失败模式

| 失败模式 | owner | 当前暴露方式 | 修复动作 |
| --- | --- | --- | --- |
{chr(10).join(rows) if rows else "| n/a | n/a | n/a | n/a |"}
"""


def visual_playbook_markdown(creator_summaries: list[dict[str, Any]]) -> str:
    first_image_values = [summary["median_first_image_after_text_paragraphs"] for summary in creator_summaries if summary["median_first_image_after_text_paragraphs"] is not None]
    image_count_values = [summary["median_image_count"] for summary in creator_summaries if summary["median_image_count"] is not None]
    return f"""# TH Capital 图文与封面统一审美 v2

- `generated_at`: `{now_cst()}`
- `mode`: `proof-first editorial`
- `creator_pack_count`: `{len(creator_summaries)}`
- `creator_pack_median_image_count`: `{median_or_na(image_count_values)}`
- `creator_pack_median_first_image_after_text_paragraphs`: `{median_or_na(first_image_values)}`

## 统一审美底座

- 背景用 `纸白 / 浅灰`，正文和图卡主文字用 `深墨`，整张图只保留 `1 个信号色`，不做多色霓虹拼盘。
- 封面优先 `对象截图 / 数字信号卡 / 结构图`，不要再默认生成“赛博人物 / 发光大脑 / 紫色抽象 AI 图”。
- 正文图固定按 `证明事实 -> 解释结构 -> 节奏换气` 排序；装饰优先级最低。
- 一张图只做一件事：证明、解释、提醒边界、或帮助传播；如果什么都没完成，就删掉。

## 封面系统

- `proof cover`：有强一手截图或对象页面时，直接用对象 + 主 claim。
- `signal cover`：有关键数字、对比或市场信号时，用数字卡或信号卡承接标题。
- `structure cover`：方法论 / tutorial / skill 题，用简洁结构图，不要假装成电影海报。

## 正文图系统

- `原始证据图`：repo、官网页、原帖、PDF 首页、产品界面。
- `信号分类图`：四类信号、四象限、适合谁 / 不适合谁、变量矩阵。
- `分层架构图`：五层 skill、系统结构、上下游链路。
- `workflow 图`：四步 / 五步循环、路径拆解、执行流程。
- `风险边界卡`：哪些条件成立才成立，哪些误判最常见。

## 明确禁区

- 不要用抽象 AI 图代替原始证据。
- 不要用看似高级、实则什么都没说的概念海报。
- 不要让封面承诺一件事，正文却在讲另一件事。
- 如果当前图出不来质量，宁可删掉该图位，也不要塞烂图凑数。
"""


def creator_pack_registry_entry(summary: dict[str, Any]) -> dict[str, Any]:
    pack_dir = CREATOR_PACK_DIR / summary["slug"]
    return {
        "source_name": summary["source_name"],
        "overlay_skill_name": summary["overlay_skill_name"],
        "sample_gate": f"{summary['sample_count']}/20",
        "skill_card": str(pack_dir / "skill-card.md"),
        "text_patterns": str(pack_dir / "text-patterns.md"),
        "visual_patterns": str(pack_dir / "visual-patterns.md"),
        "style_audit": str(pack_dir / "style-audit.md"),
        "sample_index": str(pack_dir / "sample-index.md"),
        "corpus_manifest": str(pack_dir / "corpus-manifest.json"),
        "legacy_summary": str(CREATOR_DIR / f"{summary['slug']}__style-dossier.md"),
    }


def index_markdown(
    date_text: str,
    creator_summaries: list[dict[str, Any]],
    content_type_files: list[Path],
    packaging_path: Path,
    visual_path: Path,
    failure_path: Path,
) -> str:
    creator_rows = []
    for summary in creator_summaries:
        pack_dir = CREATOR_PACK_DIR / summary["slug"]
        creator_rows.append(
            "| {name} | {samples}/20 | [{skill}]({skill_path}) | [{text}]({text_path}) | [{visual}]({visual_path}) | [{audit}]({audit_path}) |".format(
                name=summary["source_name"],
                samples=summary["sample_count"],
                skill="skill-card",
                skill_path=pack_dir / "skill-card.md",
                text="text-patterns",
                text_path=pack_dir / "text-patterns.md",
                visual="visual-patterns",
                visual_path=pack_dir / "visual-patterns.md",
                audit="style-audit",
                audit_path=pack_dir / "style-audit.md",
            )
        )
    content_type_links = "\n".join(f"- [{path.stem}]({path})" for path in content_type_files)
    return f"""# 学习知识资产索引 v2

- `generated_at`: `{now_cst()}`
- `date`: `{date_text}`
- `purpose`: `把对标公众号真正蒸馏成可调用的 style skill packs，并把统一封面/正文图审美接进写作生产链。`

## Creator Skill Packs

| 创作者 | 样本门槛 | Skill Card | Text Patterns | Visual Patterns | Style Audit |
| --- | --- | --- | --- | --- | --- |
{chr(10).join(creator_rows) if creator_rows else "| n/a | n/a | n/a | n/a | n/a | n/a |"}

## 运行时调用链

1. `topic-radar / topic-approval` 先选 `content_route`，明确 `primary overlay`。
2. `draft-pack` 按 route 加载对应 `overlay skill -> skill-card -> text-patterns -> visual-patterns`。
3. `hook-title-cover / visual-intelligence` 统一遵守 [图文与封面统一审美 v2]({visual_path})。
4. `content-polish` 出稿前必须过一遍对应创作者的 `style-audit.md`，防止品牌漂移和烂图混入。

## 题材打法页

{content_type_links if content_type_links else "- 暂无"}

## 通用打法页

- [包装打法页]({packaging_path})
- [图文与封面统一审美 v2]({visual_path})
- [失败模式页]({failure_path})
- [风格路由表]({STYLE_ROUTER_PATH})

## 当前硬规则

- 每个 creator skill pack 都必须基于最近 `20` 篇 distinct deep articles。
- 样本门槛没过，就不允许把该创作者当 `primary overlay`。
- 不允许让外部创作者人格覆盖 TH Capital 品牌人格。
- 不允许用抽象 AI 图替代原始证据或结构说明。
"""


def style_router_markdown(creator_summaries: list[dict[str, Any]]) -> str:
    creator_rows = []
    summary_map = {summary["source_name"]: summary for summary in creator_summaries}
    for source_name in CREATOR_ORDER:
        summary = summary_map[source_name]
        pack_dir = CREATOR_PACK_DIR / summary["slug"]
        creator_rows.append(
            "| {name} | `{skill}` | `{samples}/20` | [skill-card]({path}) |".format(
                name=source_name,
                skill=summary["overlay_skill_name"],
                samples=summary["sample_count"],
                path=pack_dir / "skill-card.md",
            )
        )
    route_rows = []
    for rule in STYLE_ROUTE_RULES:
        primary = summary_map[rule["primary_overlay"]]
        primary_pack = CREATOR_PACK_DIR / primary["slug"] / "skill-card.md"
        route_rows.append(
            "| {route} | `{primary_skill}` | [skill-card]({primary_path}) | `{secondary_skill}` | {layers} | {visuals} | {avoid} |".format(
                route=rule["route"],
                primary_skill=primary["overlay_skill_name"],
                primary_path=primary_pack,
                secondary_skill=summary_map[rule["secondary_overlay"]]["overlay_skill_name"],
                layers=rule["apply_layers"],
                visuals=rule["visual_system"],
                avoid=rule["avoid"],
            )
        )
    return f"""# TH Capital 风格路由表 v2

- `generated_at`: `{now_cst()}`
- `purpose`: `把每个公众号蒸馏成真 style skill，并明确不同题材该调用哪套 skill pack。`

## Creator Skill Roster

| 创作者 | Overlay Skill | 样本门槛 | Pack |
| --- | --- | --- | --- |
{chr(10).join(creator_rows)}

## Route Matrix

| 题材路由 | Primary Overlay Skill | Primary Pack | Secondary Overlay Skill | 重点借用层 | 推荐视觉系统 | 明确禁区 |
| --- | --- | --- | --- | --- | --- | --- |
{chr(10).join(route_rows)}

## Runtime Discipline

- 同一篇稿最多 `1 个 primary overlay + 1 个 secondary overlay`。
- `support overlay` 只能补一个局部动作，不得三家乱拼。
- route 一旦选定，`draft-pack / content-polish / hook-title-cover / visual-intelligence` 都要沿用同一套 creator skill pack。
- 如果成稿更像外部号而不是 TH Capital，优先收回品牌核心，而不是继续加风格。
"""


def write_creator_pack(summary: dict[str, Any]) -> dict[str, Any]:
    pack_dir = CREATOR_PACK_DIR / summary["slug"]
    pack_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = pack_dir / "corpus-manifest.json"
    sample_index_path = pack_dir / "sample-index.md"
    text_patterns_path = pack_dir / "text-patterns.md"
    visual_patterns_path = pack_dir / "visual-patterns.md"
    style_audit_path = pack_dir / "style-audit.md"
    skill_card_path = pack_dir / "skill-card.md"
    legacy_summary_path = CREATOR_DIR / f"{summary['slug']}__style-dossier.md"

    manifest_path.write_text(json.dumps(corpus_manifest(summary), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sample_index_path.write_text(sample_index_markdown(summary), encoding="utf-8")
    text_patterns_path.write_text(text_patterns_markdown(summary), encoding="utf-8")
    visual_patterns_path.write_text(visual_patterns_markdown(summary), encoding="utf-8")
    style_audit_path.write_text(style_audit_markdown(summary), encoding="utf-8")
    skill_card_path.write_text(skill_card_markdown(summary), encoding="utf-8")
    legacy_summary_path.write_text(legacy_creator_summary_markdown(summary), encoding="utf-8")
    return creator_pack_registry_entry(summary)


def build_assets(date_text: str, min_samples: int) -> dict[str, Any]:
    ensure_dirs()
    grouped = load_distinct_creator_articles(date_text)
    missing = {source_name: len(grouped.get(source_name, [])) for source_name in CREATOR_ORDER if len(grouped.get(source_name, [])) < min_samples}
    if missing:
        pretty = ", ".join(f"{source_name}={count}" for source_name, count in missing.items())
        raise SystemExit(f"creator skill pack sample gate failed: {pretty}")

    creator_summaries = [summarize_creator(source_name, grouped[source_name], min_samples) for source_name in CREATOR_ORDER]
    creator_registry = [write_creator_pack(summary) for summary in creator_summaries]

    content_type_files: list[Path] = []
    for playbook in CONTENT_TYPE_PLAYBOOKS:
        path = CONTENT_TYPE_DIR / f"{playbook['slug']}__playbook.md"
        path.write_text(content_type_markdown(playbook), encoding="utf-8")
        content_type_files.append(path)

    snapshot = load_snapshot(date_text)
    packaging_path = PACKAGING_DIR / "th_capital_packaging_playbook_v2.md"
    packaging_path.write_text(packaging_playbook_markdown(snapshot), encoding="utf-8")
    visual_path = VISUAL_DIR / "th_capital_visual_playbook_v2.md"
    visual_path.write_text(visual_playbook_markdown(creator_summaries), encoding="utf-8")
    failure_path = FAILURE_DIR / "content_failure_patterns_v2.md"
    failure_path.write_text(failure_patterns_markdown(snapshot), encoding="utf-8")

    STYLE_ROUTER_PATH.write_text(style_router_markdown(creator_summaries), encoding="utf-8")
    LATEST_INDEX_PATH.write_text(
        index_markdown(date_text, creator_summaries, content_type_files, packaging_path, visual_path, failure_path),
        encoding="utf-8",
    )

    registry = {
        "generated_at": now_cst(),
        "date": date_text,
        "creator_skill_packs": creator_registry,
        "creator_dossiers": [entry["legacy_summary"] for entry in creator_registry],
        "content_type_playbooks": [str(path) for path in content_type_files],
        "packaging_playbook": str(packaging_path),
        "visual_playbook": str(visual_path),
        "failure_patterns": str(failure_path),
        "style_router": str(STYLE_ROUTER_PATH),
        "index": str(LATEST_INDEX_PATH),
    }
    REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return registry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build creator skill packs and visual playbooks for TH Capital.")
    parser.add_argument("--date", default=datetime.now(CN_TZ).date().isoformat())
    parser.add_argument("--min-samples", type=int, default=20)
    parser.add_argument("--backfill-missing", action="store_true")
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.backfill_missing and not args.write:
        raise SystemExit("--backfill-missing requires --write so packet/deep-article artifacts can actually be created.")
    backfill_log_path = None
    if args.backfill_missing:
        summary = backfill_missing_creator_samples(args.date, args.min_samples)
        backfill_log_path = persist_backfill_summary(summary)
    registry = build_assets(args.date, args.min_samples)
    if backfill_log_path is not None:
        registry["backfill_log"] = str(backfill_log_path)
        REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.write:
        print(REGISTRY_PATH)
        return
    print(json.dumps(registry, ensure_ascii=False, indent=2))


def build_assets_from_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Thin wrapper so board builder can call build_assets with snapshot-derived params."""
    date_text = snapshot["meta"]["date"]
    # min_samples gate: use overview.sample_count or default 8
    min_samples = snapshot["overview"].get("sample_count", 8)
    return build_assets(date_text, min_samples)


if __name__ == "__main__":
    main()

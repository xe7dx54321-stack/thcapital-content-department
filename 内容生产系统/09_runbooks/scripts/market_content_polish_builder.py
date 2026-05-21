#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import math
import mimetypes
import os
import re
import ssl
import subprocess
from dataclasses import dataclass
from datetime import datetime
from html import unescape
from pathlib import Path
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

from market_morning_roundup_utils import sanitize_morning_roundup_markdown

CN_TZ = ZoneInfo("Asia/Shanghai")
ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
DEFAULT_LOG_ROOT = ROOT / "10_logs"
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
URL_RE = re.compile(r"https?://[^\s`<>\"'()（）】]+")
LONGFORM_PLATFORMS = {"wechat", "zhihu", "bilibili", "baijiahao", "toutiao"}
PLATFORM_LABELS = {
    "wechat": "WeChat",
    "xiaohongshu": "Xiaohongshu",
    "zhihu": "Zhihu",
    "x": "X",
    "bilibili": "Bilibili",
    "toutiao": "Toutiao",
    "baijiahao": "Baijiahao",
}
CARD_FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]
SCREENSHOT_ALLOWED_DOMAINS = {
    "x.com",
    "twitter.com",
    "github.com",
    "reddit.com",
    "old.reddit.com",
    "youtube.com",
    "youtu.be",
    "bilibili.com",
    "openai.com",
    "anthropic.com",
    "deepmind.google",
    "x.ai",
    "figure.ai",
    "huggingface.co",
    "arxiv.org",
    "kunlun.com",
    "zgcforum.com",
    "f-cn-static.arkgames.com",
    "kirinjin.com",
    "trump.kirinjin.com",
}
SCREENSHOT_BLOCKED_DOMAINS = {
    "mp.weixin.qq.com",
    "jiqizhixin.com",
    "www.jiqizhixin.com",
    "qbitai.com",
    "www.qbitai.com",
    "zhidx.com",
    "www.zhidx.com",
    "36kr.com",
    "www.36kr.com",
    "ifanr.com",
    "www.ifanr.com",
    "app.so",
    "appso.cn",
    "www.appso.cn",
    "techcrunch.com",
    "www.techcrunch.com",
    "venturebeat.com",
    "www.venturebeat.com",
    "theverge.com",
    "www.theverge.com",
    "reuters.com",
    "www.reuters.com",
    "bloomberg.com",
    "www.bloomberg.com",
}
METADATA_IMAGE_DOMAINS = {
    "youtube.com",
    "youtu.be",
    "bilibili.com",
    "openai.com",
    "anthropic.com",
    "deepmind.google",
    "x.ai",
    "figure.ai",
    "github.com",
    "huggingface.co",
    "arxiv.org",
    "kunlun.com",
    "zgcforum.com",
    "f-cn-static.arkgames.com",
    "kirinjin.com",
    "trump.kirinjin.com",
}
HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}
UNVERIFIED_SSL_CONTEXT = ssl._create_unverified_context()
ASSET_MANIFEST_NAME = "_asset-manifest.json"
ASSET_POLICY_VERSION = "2026-03-30-safe-visual-v3"
WIKIMEDIA_COMMONS_API = "https://commons.wikimedia.org/w/api.php"
MINIMAX_IMAGE_ENDPOINT = "https://api.minimaxi.com/v1/image_generation"
OPENAI_IMAGE_ENDPOINT = "https://api.openai.com/v1/images/generations"
OPENCLAW_AUTH_PROFILES_GLOB = ".openclaw/agents/*/agent/auth-profiles.json"
MINIMAX_IMAGE_MODEL_DEFAULT = "image-01"
MINIMAX_IMAGE_ASPECT_RATIO_DEFAULT = "16:9"
CARD_FILE_FIELDS = {
    "wechat_path": "wechat.md",
    "xiaohongshu_path": "xiaohongshu.md",
    "zhihu_path": "zhihu.md",
    "x_path": "x.md",
    "bilibili_path": "bilibili.md",
    "toutiao_path": "toutiao.md",
    "baijiahao_path": "baijiahao.md",
    "title_options_path": "title-options.md",
    "summary_options_path": "summary-options.md",
    "opening_hook_options_path": "opening-hook-options.md",
    "cta_mode_path": "cta-mode.md",
    "packaging_bundle_path": "packaging-bundle.md",
    "context_bridge_path": "context-bridge-notes.md",
    "audience_notes_path": "audience-notes.md",
    "render_plan_path": "platform-render-plan.md",
    "citation_block_path": "citation-block.md",
    "visual_notes_path": "visual-notes.md",
    "inline_visual_plan_path": "inline-visual-plan.md",
    "revision_notes_path": "revision-notes.md",
}
QUERY_TOKEN_STOPWORDS = {
    "ai",
    "aigc",
    "agi",
    "announcement",
    "article",
    "blog",
    "build",
    "com",
    "company",
    "forum",
    "github",
    "group",
    "home",
    "index",
    "info",
    "latest",
    "main",
    "market",
    "model",
    "models",
    "news",
    "one",
    "official",
    "page",
    "platform",
    "release",
    "repo",
    "signal",
    "site",
    "system",
    "tech",
    "three",
    "today",
    "top",
    "two",
    "update",
    "watch",
    "www",
}
PLATFORM_HEADING_ALIASES = {
    "wechat": {"wechat", "weixin", "公众号", "微信公众号"},
    "zhihu": {"zhihu", "知乎"},
    "xiaohongshu": {"xiaohongshu", "xhs", "小红书"},
    "x": {"x", "x / thread", "thread", "twitter", "推特"},
    "bilibili": {"bilibili", "b站", "b站专栏"},
    "toutiao": {"toutiao", "今日头条", "头条"},
    "baijiahao": {"baijiahao", "百家号"},
}
NON_SLOT_HEADING_KEYWORDS = {
    "visual strategy",
    "platform slots",
    "source candidates",
    "human qc",
    "visual placement",
    "planned visuals",
    "image sources",
    "image source guidance",
    "visual do",
    "visual don'ts",
    "visual don't",
    "no-go rules",
    "图文结构计划",
    "内嵌图片清单",
    "内嵌图策略原则",
    "图注与数据溯源规范",
    "优先级排序",
    "资产来源优先级",
    "无图区的设计意图",
    "基本信息",
    "图文结构",
    "inline visual slots",
    "principles",
    "visual do's",
    "visual don'ts",
}
SLOT_FIELD_ALIASES = {
    "position": {"位置", "position", "placement", "slot", "图位", "图位位置"},
    "job": {"任务", "job", "visual job"},
    "image_type": {"类型", "图片类型", "推荐类型", "asset type", "asset_type"},
    "preferred_asset": {"优先素材", "推荐素材", "preferred asset", "preferred_asset", "推荐类型"},
    "note": {"说明", "note", "reader note", "作用", "功能", "用途", "best use", "best_use"},
    "requirements": {
        "requirements",
        "制作要求",
        "内容要求",
        "建议内容",
        "建议",
        "建议配",
        "说明文字",
        "主标题",
        "副标题",
        "风格建议",
        "尺寸",
        "尺寸建议",
        "alt 文字",
        "alt文字",
        "来源标注要求",
    },
    "fallback": {"fallback", "替代方案", "备选", "如果无法截图", "ai 生成备选"},
    "priority": {"priority", "优先级", "优先级排序", "ai 生成可接受度", "ai生成可接受度"},
    "source_priority": {"source_priority", "资产来源优先级", "优先顺序", "preferred_asset_order"},
}
MULTILINE_SLOT_FIELDS = {"note", "requirements", "fallback", "source_priority"}
AUTO_VISUAL_PATH_RE = re.compile(r"^visual-assets/\d{2}__")
IMAGE_LINE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
MARKDOWN_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


@dataclass(frozen=True)
class SourcePolicy:
    source_class: str
    allow_screenshot: bool
    allow_metadata_image: bool
    reason: str


@dataclass
class DraftPack:
    pack_dir: Path
    card_path: Path
    draft_id: str
    draft_key: str
    topic_id: str
    topic_title: str
    approved_topic_path: str
    requested_platforms: list[str]
    status: str
    created_at: str
    updated_at: str
    core_judgment: str
    approved_angle: str
    risk_note: str
    paths: dict[str, str]


@dataclass(frozen=True)
class VisualSearchCandidate:
    provider: str
    query: str
    title: str
    image_url: str
    landing_url: str
    creator: str
    license_name: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build polish assets for TH Capital market content system")
    parser.add_argument("--draft-pack-dir", required=True, help="Draft pack directory path")
    parser.add_argument("--status", choices=["needs_revision", "ready"], default="needs_revision")
    parser.add_argument("--log-root", default=str(DEFAULT_LOG_ROOT))
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value).strip().strip("`")
    return value if value else fallback


def normalize_markdown_asset_path(raw: str) -> str:
    cleaned = raw.strip().strip("<>").strip().split(maxsplit=1)[0]
    return cleaned.replace("\\", "/")


def trim_text(text: str, max_chars: int) -> str:
    text = clean(text, "")
    if len(text) <= max_chars:
        return text
    shortened = text[: max_chars - 1].rstrip(" ，；：:。")
    return f"{shortened}…"


def split_platforms(raw: str) -> list[str]:
    if not raw or raw == "n/a":
        return []
    return [clean(item, "") for item in raw.split(",") if clean(item, "")]


def parse_card(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    fields: dict[str, str] = {}
    section = ""
    pack_paths: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        match = KV_RE.match(line.strip())
        if not match:
            continue
        key, value = match.groups()
        normalized = clean(value)
        if section == "Pack Paths":
            pack_paths[key] = normalized
        else:
            fields[key] = normalized
    return fields, pack_paths


def parse_simple_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    if not path.exists():
        return fields
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if not match:
            continue
        key, value = match.groups()
        fields[key] = clean(value)
    return fields


def parse_source_refs(path: Path) -> list[str]:
    if not path.exists():
        return []
    refs: list[str] = []
    in_refs = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line == "## Source Refs":
            in_refs = True
            continue
        if in_refs and line.startswith("## "):
            break
        if in_refs and line.startswith("- `") and line.endswith("`"):
            refs.append(clean(line[3:-1], ""))
    return [ref for ref in refs if ref and ref != "n/a"]


def resolve_doc_path(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path
    return ROOT / path


def hydrate_pack_paths(pack_dir: Path, pack_paths: dict[str, str]) -> dict[str, str]:
    hydrated = dict(pack_paths)
    for field_name, filename in CARD_FILE_FIELDS.items():
        candidate = pack_dir / filename
        if candidate.exists():
            hydrated[field_name] = str(candidate)
        else:
            hydrated.setdefault(field_name, "n/a")
    return hydrated


def extract_urls(text: str) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for match in URL_RE.finditer(text):
        url = match.group(0).rstrip(".,;:)]）】>")
        if (
            not url
            or "/rss/" in url
            or "localhost:8001" in url
            or url in seen
        ):
            continue
        seen.add(url)
        urls.append(url)
    return urls


def host_for(url: str) -> str:
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""


def domain_matches(host: str, candidates: set[str]) -> bool:
    return any(host == candidate or host.endswith(f".{candidate}") for candidate in candidates)


def is_pdf_url(url: str) -> bool:
    lowered = url.lower()
    return lowered.endswith(".pdf") or ".pdf?" in lowered


def is_direct_image_url(url: str) -> bool:
    lowered = url.lower()
    return any(lowered.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".gif"])


def source_policy(url: str) -> SourcePolicy:
    host = host_for(url)
    lowered = url.lower()
    if not lowered.startswith("http://") and not lowered.startswith("https://"):
        return SourcePolicy(
            source_class="local-analysis-ref",
            allow_screenshot=False,
            allow_metadata_image=False,
            reason="本地分析材料只作参考，不直接抓图。",
        )
    if is_pdf_url(url):
        return SourcePolicy(
            source_class="pdf-first-party",
            allow_screenshot=True,
            allow_metadata_image=False,
            reason="PDF 首页标题图可直接作为一手证据。",
        )
    if domain_matches(host, SCREENSHOT_BLOCKED_DOMAINS):
        return SourcePolicy(
            source_class="third-party-media",
            allow_screenshot=False,
            allow_metadata_image=False,
            reason="第三方媒体 / 公众号文章页默认禁止整页截图，避免把他人成稿搬进正文。",
        )
    if domain_matches(host, {"x.com", "twitter.com"}):
        return SourcePolicy(
            source_class="social-original",
            allow_screenshot=True,
            allow_metadata_image=False,
            reason="原始社交帖文可作为一手证据，优先截帖子主体而非整页。",
        )
    if domain_matches(host, {"reddit.com", "old.reddit.com"}):
        return SourcePolicy(
            source_class="community-original",
            allow_screenshot=True,
            allow_metadata_image=False,
            reason="社区原帖可作为原始讨论证据，但必须通过 blocked 检测。",
        )
    if domain_matches(host, {"github.com"}):
        return SourcePolicy(
            source_class="repo",
            allow_screenshot=True,
            allow_metadata_image=True,
            reason="Repo header / social preview 都可安全复用。",
        )
    if domain_matches(host, {"youtube.com", "youtu.be", "bilibili.com"}):
        return SourcePolicy(
            source_class="official-video-surface",
            allow_screenshot=True,
            allow_metadata_image=True,
            reason="视频标题区或官方缩略图可作为对象识别图。",
        )
    if domain_matches(host, SCREENSHOT_ALLOWED_DOMAINS):
        return SourcePolicy(
            source_class="official-or-primary",
            allow_screenshot=True,
            allow_metadata_image=True,
            reason="官方 / 一手页面可优先取 hero 图，再回退到标题区截图。",
        )
    return SourcePolicy(
        source_class="unknown-web",
        allow_screenshot=False,
        allow_metadata_image=False,
        reason="来源域名未进入安全抓图白名单，默认不自动抓取，改用解释图或人工补源。",
    )


def asset_extension(content_type: str, url: str) -> str:
    normalized = (content_type or "").split(";")[0].strip().lower()
    if normalized:
        guessed = mimetypes.guess_extension(normalized)
        if guessed in {".jpe"}:
            return ".jpg"
        if guessed:
            return guessed
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
        return ".jpg" if suffix == ".jpeg" else suffix
    return ".png"


def open_request(request: Request, timeout: int):
    try:
        return urlopen(request, timeout=timeout)
    except (ssl.SSLError, URLError):
        return urlopen(request, timeout=timeout, context=UNVERIFIED_SSL_CONTEXT)


def fetch_text(url: str) -> str:
    request = Request(url, headers=HTTP_HEADERS)
    with open_request(request, timeout=20) as response:
        payload = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
    return payload.decode(charset, errors="ignore")


def extract_meta_image_url(url: str) -> str:
    if is_direct_image_url(url):
        return url
    try:
        html = fetch_text(url)
    except Exception:
        return ""
    patterns = [
        r'<meta[^>]+property=["\']og:image(?::secure_url)?["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image(?::secure_url)?["\']',
        r'<meta[^>]+name=["\']twitter:image(?::src)?["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']twitter:image(?::src)?["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, html, flags=re.I)
        if match:
            candidate = unescape(match.group(1).strip())
            if candidate and candidate.startswith(("http://", "https://", "/")):
                return urljoin(url, candidate)
    return ""


def download_image(url: str, output_path: Path) -> Path:
    request = Request(url, headers=HTTP_HEADERS)
    with open_request(request, timeout=25) as response:
        content = response.read()
        content_type = response.headers.get("Content-Type", "")
    suffix = asset_extension(content_type, url)
    actual_path = output_path.with_suffix(suffix)
    actual_path.write_bytes(content)
    return actual_path


def clear_auto_generated_assets(asset_dir: Path) -> None:
    if not asset_dir.exists():
        return
    removable_paths: set[Path] = set()
    manifest_path = asset_dir / ASSET_MANIFEST_NAME
    if manifest_path.exists():
        try:
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            payload = {}
        for entry in payload.get("entries") or []:
            raw_path = clean(str((entry or {}).get("path", "")), "")
            if not raw_path or raw_path == "n/a":
                continue
            candidate = Path(raw_path).expanduser()
            try:
                candidate.relative_to(asset_dir)
            except ValueError:
                continue
            removable_paths.add(candidate)
    else:
        # Backward-compatible fallback: only clean the clearly auto-generated ranges,
        # so manually added evidence crops such as 10__/11__/20__ are preserved.
        for path in asset_dir.iterdir():
            if not path.is_file():
                continue
            if re.match(r"^(6\d|7\d|8\d|9\d)__", path.name):
                removable_paths.add(path)
    removable_paths.add(asset_dir / "_capture-log.md")
    removable_paths.add(asset_dir / ASSET_MANIFEST_NAME)
    for path in removable_paths:
        path.unlink(missing_ok=True)


def manifest_entry(
    *,
    path: Path | None,
    status: str,
    asset_kind: str,
    selection_reason: str,
    source_url: str = "",
    source_class: str = "",
    preview: bool = False,
    **extra: str | bool,
) -> dict[str, str | bool]:
    payload: dict[str, str | bool] = {
        "path": str(path) if path else "",
        "status": status,
        "asset_kind": asset_kind,
        "selection_reason": selection_reason,
        "source_url": source_url,
        "source_class": source_class,
        "preview": preview,
    }
    for key, value in extra.items():
        payload[key] = value
    return payload


def inspect_ai_image_quality(path: Path) -> tuple[bool, dict[str, float], list[str]]:
    try:
        grayscale = Image.open(path).convert("L")
    except Exception as error:
        return False, {}, [f"image unreadable: {clean(str(error), '')}"]

    histogram = grayscale.histogram()
    total_pixels = max(sum(histogram), 1)
    stat = ImageStat.Stat(grayscale)
    edges = grayscale.filter(ImageFilter.FIND_EDGES)
    edge_histogram = edges.histogram()
    edge_stat = ImageStat.Stat(edges)

    near_white_ratio = sum(histogram[245:]) / total_pixels
    grayscale_mean = stat.mean[0]
    grayscale_stddev = stat.stddev[0]
    edge_mean = edge_stat.mean[0]
    edge_active_ratio = sum(edge_histogram[28:]) / total_pixels

    metrics = {
        "grayscale_mean": round(grayscale_mean, 4),
        "grayscale_stddev": round(grayscale_stddev, 4),
        "near_white_ratio": round(near_white_ratio, 4),
        "edge_mean": round(edge_mean, 4),
        "edge_active_ratio": round(edge_active_ratio, 4),
    }
    failures: list[str] = []
    if near_white_ratio > 0.96:
        failures.append("near-white ratio too high")
    if near_white_ratio > 0.85 and grayscale_stddev < 12:
        failures.append("washed-out image with insufficient contrast")
    if grayscale_stddev < 12 and edge_active_ratio < 0.012:
        failures.append("contrast and structure too low")
    if edge_mean < 2.4 and edge_active_ratio < 0.01:
        failures.append("edge density too low")
    return not failures, metrics, failures


def screenshot_output_path(asset_dir: Path, index: int, url: str) -> Path:
    return asset_dir / f"{index:02d}__{slugify_url(url)}.png"


def remote_image_output_path(asset_dir: Path, index: int, url: str) -> Path:
    return asset_dir / f"{index:02d}__{slugify_url(url)}"


def source_ref_candidates(pack: DraftPack) -> list[str]:
    refs: list[str] = []
    citation_path = clean(pack.paths.get("citation_block_path", "n/a"))
    if citation_path != "n/a":
        refs.extend(parse_source_refs(resolve_doc_path(citation_path)))
    if pack.approved_topic_path != "n/a":
        refs.extend(parse_source_refs(resolve_doc_path(pack.approved_topic_path)))
    deduped: list[str] = []
    seen: set[str] = set()
    for ref in refs:
        normalized = clean(ref, "")
        if normalized and normalized not in seen:
            seen.add(normalized)
            deduped.append(normalized)
    return deduped


def maybe_local_doc_path(raw_ref: str) -> Path | None:
    normalized = clean(raw_ref, "")
    if not normalized or normalized.startswith(("http://", "https://")):
        return None
    candidate = Path(normalized).expanduser()
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate if candidate.exists() and candidate.is_file() else None


def extract_urls_from_doc(path: Path, *, depth: int = 1, seen: set[Path] | None = None) -> list[str]:
    if not path.exists():
        return []
    seen = seen or set()
    resolved = path.expanduser().resolve()
    if resolved in seen:
        return []
    seen.add(resolved)
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []
    urls = extract_urls(text)
    if depth <= 0:
        return dedupe_preserve_order(urls)
    nested_refs = parse_source_refs(path)
    for nested_ref in nested_refs:
        nested_path = maybe_local_doc_path(nested_ref)
        if nested_path is not None:
            urls.extend(extract_urls_from_doc(nested_path, depth=depth - 1, seen=seen))
        else:
            urls.extend(extract_urls(nested_ref))
    return dedupe_preserve_order(urls)


def dedupe_preserve_order(values: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = clean(value, "")
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(normalized)
    return deduped


def discover_source_urls(pack: DraftPack) -> list[str]:
    urls: list[str] = []
    direct_refs = source_ref_candidates(pack)
    for ref in direct_refs:
        urls.extend(extract_urls(ref))
        local_path = maybe_local_doc_path(ref)
        if local_path is not None:
            urls.extend(extract_urls_from_doc(local_path, depth=1))
    doc_candidates = [
        pack.approved_topic_path,
        pack.paths.get("citation_block_path", "n/a"),
        pack.paths.get("wechat_path", "n/a"),
        pack.paths.get("inline_visual_plan_path", "n/a"),
        pack.paths.get("packaging_bundle_path", "n/a"),
        pack.paths.get("render_plan_path", "n/a"),
    ]
    for raw_path in doc_candidates:
        normalized = clean(raw_path or "", "")
        if not normalized or normalized == "n/a":
            continue
        path = resolve_doc_path(normalized)
        urls.extend(extract_urls_from_doc(path, depth=1))
    return dedupe_preserve_order(urls)


def load_draft_pack(pack_dir: Path) -> DraftPack:
    card_path = pack_dir / "00_draft-pack-card.md"
    if not card_path.exists():
        raise SystemExit(f"Draft pack card not found: {card_path}")
    fields, pack_paths = parse_card(card_path)
    approved_topic_path = clean(fields.get("approved_topic_path", "n/a"))
    approved_topic_fields = (
        parse_simple_fields(resolve_doc_path(approved_topic_path))
        if approved_topic_path != "n/a"
        else {}
    )
    return DraftPack(
        pack_dir=pack_dir,
        card_path=card_path,
        draft_id=clean(fields.get("draft_id", f"draft__{pack_dir.name}")),
        draft_key=clean(fields.get("draft_key", pack_dir.name)),
        topic_id=clean(fields.get("topic_id", "n/a")),
        topic_title=clean(approved_topic_fields.get("title", pack_dir.name.replace("_", " "))),
        approved_topic_path=approved_topic_path,
        requested_platforms=split_platforms(fields.get("requested_platforms", "")),
        status=clean(fields.get("status", "drafting")),
        created_at=clean(fields.get("created_at", "n/a")),
        updated_at=clean(fields.get("updated_at", "n/a")),
        core_judgment=clean(fields.get("core_judgment", "n/a")),
        approved_angle=clean(fields.get("approved_angle", "n/a")),
        risk_note=clean(fields.get("risk_note", "n/a")),
        paths=hydrate_pack_paths(pack_dir, pack_paths),
    )


def platform_label(platform: str) -> str:
    return PLATFORM_LABELS.get(platform, platform)


def visual_asset_type(source_ref: str) -> str:
    ref = source_ref.lower()
    if not ref.startswith("http://") and not ref.startswith("https://"):
        return "分析素材引用（不建议直接截图）"
    if "mp.weixin.qq.com/" in ref:
        return "第三方公众号文章页（禁止整页截图，需回找原始源或替代图）"
    if "reddit.com/" in ref:
        return "社区原帖标题区截图"
    if "x.com/" in ref or "twitter.com/" in ref:
        return "原始推文 / thread 截图"
    if ref.endswith(".pdf") or ".pdf?" in ref:
        return "PDF 首页标题截图"
    if "youtube.com/" in ref or "youtu.be/" in ref:
        return "视频标题区截图或官方缩略图"
    if "bilibili.com/" in ref:
        return "视频标题区截图或封面图"
    if "github.com/" in ref:
        return "Repo header / README 首屏截图"
    if any(domain in ref for domain in ["openai.com", "anthropic.com", "deepmind.google", "x.ai", "figure.ai"]):
        return "官方公告 / 产品页标题区截图"
    return "网页标题区截图"


def visual_best_use(source_ref: str) -> str:
    ref = source_ref.lower()
    if not ref.startswith("http://") and not ref.startswith("https://"):
        return "作为分析链路参考，不作为正文原始证据图"
    if "mp.weixin.qq.com/" in ref:
        return "不直接入正文，优先回找原始源、官方资产或替代安全图"
    if "reddit.com/" in ref:
        return "正文前段作为原始事件证据锚点"
    if "x.com/" in ref or "twitter.com/" in ref:
        return "正文前段作为原始事件证据锚点"
    if ref.endswith(".pdf") or ".pdf?" in ref:
        return "正文背景段后，证明公告 / 招股书 / 白皮书确已发布"
    if "github.com/" in ref:
        return "变量段前，证明对象真实存在且具备 traction / release 语境"
    if "youtube.com/" in ref or "youtu.be/" in ref or "bilibili.com/" in ref:
        return "正文中段，补充 demo / 访谈 / workflow 的原始视觉证据"
    return "正文前中段，作为原始来源与对象说明图"


def capture_selector_hint(source_ref: str) -> str:
    ref = source_ref.lower()
    if not ref.startswith("http://") and not ref.startswith("https://"):
        return "`n/a`｜本地分析文档，不执行网页截图"
    if "mp.weixin.qq.com/" in ref:
        return "`blocked`｜第三方公众号文章页不自动截图，改找原始源 / 官方图 / 解释图"
    if "reddit.com/" in ref:
        return "标题区 / 首屏摘要区"
    if "github.com/" in ref:
        return "`article, main, [data-hpc]` 中的 repo header / README 首屏"
    if ref.endswith(".pdf") or ".pdf?" in ref:
        return "`full-page`，优先 PDF 首页标题区"
    if "youtube.com/" in ref or "youtu.be/" in ref or "bilibili.com/" in ref:
        return "标题区或播放器上方信息区"
    return "标题区 / hero 区 / 对象区"


def cover_job(platform: str) -> str:
    if platform == "wechat":
        return "帮助用户决定要不要点开，并在 3 秒内知道这不是普通资讯。"
    if platform == "xiaohongshu":
        return "让用户停下来，并立刻知道这件事和自己有什么关系。"
    if platform == "zhihu":
        return "让搜索读者先知道这篇在回答什么问题。"
    if platform == "x":
        return "让第一条像封面一样完成传播。"
    if platform == "bilibili":
        return "让 builder 一眼知道这是一篇可带走方法的拆解。"
    if platform == "toutiao":
        return "让泛读者快速知道这事为什么值得点开。"
    if platform == "baijiahao":
        return "让搜索用户迅速知道对象、问题和答案方向。"
    return "帮助用户更快决定要不要继续看。"


def cover_title_line(pack: DraftPack, platform: str) -> str:
    title = trim_text(pack.topic_title, 26)
    angle = trim_text(pack.approved_angle, 24)
    if platform == "wechat":
        return f"{title}：真正值得看的，是 {angle}"
    if platform == "xiaohongshu":
        return f"别把 {title} 当普通新闻"
    if platform == "zhihu":
        return f"如何看待“{title}”？"
    if platform == "x":
        return trim_text(pack.core_judgment, 36)
    if platform == "bilibili":
        return f"{title}：builder 真正该拆什么？"
    if platform == "toutiao":
        return f"{title} 为什么突然值得重看？"
    if platform == "baijiahao":
        return f"如何理解“{title}”？"
    return title


def cover_sub_line(pack: DraftPack, platform: str) -> str:
    if platform == "x":
        return "首条里就把背景 cash 掉，不靠封面图。"
    if platform == "xiaohongshu":
        return "这不是热闹，是你该看懂的变化。"
    return trim_text(pack.core_judgment, 34)


def background_cash_line(pack: DraftPack, platform: str) -> str:
    if platform == "x":
        return trim_text(pack.approved_angle, 40)
    return f"一句话背景：这件事值得看，不是因为 headline 本身，而是因为它暴露了 {trim_text(pack.approved_angle, 22)}。"


def visual_priority(platform: str) -> str:
    if platform == "wechat":
        return "对象截图 / logo + 结构变化副标题 + 1 个关键信息块"
    if platform == "xiaohongshu":
        return "封面卡 + 解释卡连续设计"
    if platform == "zhihu":
        return "问题 + 结论 + 对象解释图"
    if platform == "x":
        return "单句传播，不依赖配图"
    if platform == "bilibili":
        return "对象截图 + 过程标签 + 结论短句"
    if platform == "toutiao":
        return "强对比标题 + 结果感更强的首图"
    if platform == "baijiahao":
        return "解释型配图，服务搜索读者理解"
    return "突出对象和 stakes"


def section_job_map(platform: str) -> list[str]:
    if platform == "wechat":
        return [
            "首屏：对象 / why now / core claim",
            "中前段：第一个 proof anchor",
            "中段：关键变量",
            "后段：判断与边界",
            "结尾：观察点 / CTA",
        ]
    if platform == "zhihu":
        return [
            "开头：直接回答问题",
            "前段：讲清原始事件",
            "中段：变量与证据",
            "结尾：阶段性判断",
        ]
    if platform == "bilibili":
        return [
            "开头：告诉读者能带走什么",
            "前段：背景 + 案例",
            "中段：过程 / 卡点 / 变量",
            "结尾：builder takeaway",
        ]
    if platform == "toutiao":
        return [
            "前两段：结果和 stakes",
            "第三段：背景 cash",
            "中段：短块拆变量",
            "结尾：一句提醒",
        ]
    if platform == "baijiahao":
        return [
            "开头：answer-first",
            "前段：背景 + why now",
            "中段：定义 / 变量 / 风险 / 证据",
            "结尾：当前判断",
        ]
    return [
        "开头：promise",
        "中段：context + proof",
        "结尾：takeaway",
    ]


def proof_cadence(platform: str) -> str:
    if platform in LONGFORM_PLATFORMS:
        return "前 10-20% 给第一个 proof anchor，中后段再给一组补充证据。"
    if platform == "xiaohongshu":
        return "前 2 屏内至少出现 1 个可信锚点。"
    if platform == "x":
        return "第一条给判断，第二或第三条立刻给 context / proof。"
    return "尽早给一个可信锚点。"


def polish_checklist(pack: DraftPack, status: str) -> str:
    lines = [
        "# Polish Checklist",
        "",
        f"- `draft_pack_dir`: `{pack.pack_dir}`",
        f"- `current_target_status`: `{status}`",
        f"- `core_judgment`: `{pack.core_judgment}`",
        "",
        "## Sweep Checklist",
        "",
        "- [ ] Context bridge：冷启动用户能在早期知道对象 / stakes / why now",
        "- [ ] Clarity：结构清楚，主结论足够靠前",
        "- [ ] De-AI：无明显 AI 腔、无空话、无套话",
        "- [ ] Personality consistency：像 TH Capital 在说，不像 generic AI 媒体号",
        "- [ ] Judgment：观点更干净有力，不暧昧拖沓",
        "- [ ] Hook：标题 / 开头值得继续读",
        "- [ ] First screen：对象 / why now / core claim 在前 10-20% 可见",
        "- [ ] Promise-body match：标题承诺和正文兑现一致",
        "- [ ] Proof anchor：最关键 source ref 足够早出现",
        "- [ ] Citation：source refs 与风险提示都保留",
        "- [ ] Platform fit：各平台版本都没有变成简单裁切",
        "- [ ] CTA：收尾动作自然，不突兀、不硬转化",
        "",
        "## Platform Scope",
        "",
    ]
    if pack.requested_platforms:
        lines.extend(f"- `{platform}`" for platform in pack.requested_platforms)
    else:
        lines.append("- `n/a`")
    lines.extend(
        [
            "",
            "## Blockers",
            "",
            "- 若未通过，请明确写：哪个平台没过、为什么没过、下一步怎么改。",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def polish_notes(pack: DraftPack, status: str) -> str:
    lines = [
        "# Polish Notes",
        "",
        f"- `target_status`: `{status}`",
        f"- `approved_angle`: `{pack.approved_angle}`",
        f"- `risk_note`: `{pack.risk_note}`",
        "",
        "## Editing Principles",
        "",
        "- 不把判断磨平。",
        "- 不把信息密度磨掉。",
        "- 不为了更顺而删掉风险提示。",
        "- 不为了更像人类而加水话。",
        "- 不只做“去 AI 味”，而是做“人格一致性”。",
        "- 让首屏更清楚，但不把文章写成 bland 背景介绍。",
    ]
    return "\n".join(lines).rstrip() + "\n"


def publish_readiness(pack: DraftPack, status: str) -> str:
    lines = [
        "# Publish Readiness",
        "",
        f"- `draft_pack_status`: `{status}`",
        f"- `overall_readiness`: `{'可进入下一阶段' if status == 'ready' else '仍需返修'}`",
        f"- `first_screen_ready`: `{'yes' if status == 'ready' else 'no'}`",
        f"- `context_bridge_ready`: `{'yes' if status == 'ready' else 'no'}`",
        f"- `proof_anchor_ready`: `{'yes' if status == 'ready' else 'no'}`",
        f"- `cover_visual_ready`: `{'yes' if status == 'ready' else 'no'}`",
        f"- `longform_completeness_ready`: `{'yes' if status == 'ready' else 'no'}`",
        f"- `inline_visual_plan_ready`: `{'yes' if (pack.pack_dir / 'inline-visual-plan.md').exists() else 'no'}`",
        f"- `visual_sourcing_ready`: `{'yes' if status == 'ready' else 'no'}`",
        f"- `cta_ready`: `{'yes' if status == 'ready' else 'no'}`",
        f"- `personality_consistency_ready`: `{'yes' if status == 'ready' else 'no'}`",
        "",
        "## Platform Readiness",
        "",
    ]
    for platform in pack.requested_platforms:
        readiness = "ready" if status == "ready" else "needs_revision"
        if platform in LONGFORM_PLATFORMS:
            lines.append(f"- `{platform}`: `{readiness}`｜重点检查：首屏 / 背景 / proof anchor / section job map")
        else:
            lines.append(f"- `{platform}`: `{readiness}`")
    if not pack.requested_platforms:
        lines.append("- `n/a`")
    lines.extend(
        [
            "",
            "## Blockers",
            "",
            f"- `main_risk`: `{pack.risk_note}`",
            f"- `note`: `{'可继续进入下一阶段，但仍需人工把关。' if status == 'ready' else '请先完成多轮 polish，再进入下一阶段。'}`",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def voice_consistency_notes(pack: DraftPack) -> str:
    lines = [
        "# Voice Consistency Notes",
        "",
        f"- `core_judgment`: `{pack.core_judgment}`",
        f"- `approved_angle`: `{pack.approved_angle}`",
        "",
        "## What TH Capital should sound like",
        "",
        "- 先给判断，再补论证。",
        "- 有信息密度，但不端着。",
        "- 能讲清对象，也能拉出结构变化。",
        "- 承认风险和边界，不装确定性。",
        "",
        "## What to cut",
        "",
        "- “值得注意的是 / 在这个节点 / 某种程度上”这类空转话术。",
        "- 只会复述新闻、不落到判断的段落。",
        "- 为了口语化而加的废话。",
        "",
        "## What to strengthen",
        "",
        "- 核心判断更早。",
        "- why now 更具体。",
        "- 风险提示更像真人提醒，而不是免责声明。",
    ]
    return "\n".join(lines).rstrip() + "\n"


def platform_render_handoff(pack: DraftPack) -> str:
    lines = [
        "# Platform Render Handoff",
        "",
        f"- `draft_key`: `{pack.draft_key}`",
        "",
    ]
    for platform in pack.requested_platforms:
        lines.extend(
            [
                f"## `{platform_label(platform)}`",
                "",
                f"- `render_goal`: `让 {platform} 版本首屏更清楚、更像平台原生内容`",
                "- `first_screen_must_have`: `对象 / why now / core claim`",
                "- `proof_anchor_position`: `尽量在前 10-20% 出现第一个可信锚点`",
                f"- `section_job_map`: `{' / '.join(section_job_map(platform))}`",
                f"- `proof_cadence`: `{proof_cadence(platform)}`",
                f"- `visual_slots`: `{visual_priority(platform)}`",
                "- `risk_note_retention`: `必须保留，不得为了顺而删`",
                "- `cta_style`: `轻、自然、与平台节奏一致`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def cover_visual_brief(pack: DraftPack) -> str:
    lines = [
        "# Cover Visual Brief",
        "",
        f"- `draft_key`: `{pack.draft_key}`",
        f"- `topic_title`: `{pack.topic_title}`",
        f"- `approved_angle`: `{pack.approved_angle}`",
        f"- `core_judgment`: `{pack.core_judgment}`",
        f"- `risk_note`: `{pack.risk_note}`",
        "",
        "## Packaging Goal",
        "",
        "- 封面不是单纯“做漂亮”，而是帮助冷启动读者更快决定要不要点开、读下去。",
        "- 视觉表达要服务核心判断，而不是把对象做成泛 AI 海报。",
        "- 如果用户 3 秒内看不出对象和 stakes，这张图就还不够好。",
        "",
        "## 3-second Test",
        "",
        "- 用户能不能一眼知道对象是什么？",
        "- 用户能不能一眼知道为什么现在值得看？",
        "- 用户会不会被误导成另一条更热但不相关的话题？",
        "",
        "## Platform Briefs",
        "",
    ]
    for platform in pack.requested_platforms:
        lines.extend(
            [
                f"### `{platform_label(platform)}`",
                "",
                f"- `cover_job`: `{cover_job(platform)}`",
                f"- `main_title_line`: `{cover_title_line(pack, platform)}`",
                f"- `sub_line`: `{cover_sub_line(pack, platform)}`",
                f"- `background_cash_line`: `{background_cash_line(pack, platform)}`",
                f"- `visual_priority`: `{visual_priority(platform)}`",
                f"- `do_not_mislead`: `不要把它包装成与“{pack.approved_angle}”无关的泛 AI 热点。`",
                "",
            ]
        )
    lines.extend(
        [
            "## Visual Building Blocks",
            "",
            "- 优先考虑：产品界面截图、官方 logo、原始发布画面、结构图、流程箭头、关键变量卡片。",
            "- 如果没有强原图，再考虑做抽象辅助图；抽象图不能替代对象本身。",
            "- 微信 / 知乎优先横版头图，小红书优先封面卡 + 解释卡连续感。",
            "",
            "## Human QC",
            "",
            "- 看图的人 3 秒内能否知道对象是什么？",
            "- 看图的人能否知道为什么现在值得点开？",
            "- 图片有没有把风险、边界或真实对象遮掉？",
            "- 如果把标题拿掉，这张图会不会误导成另一个话题？",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def cover_asset_assist(pack: DraftPack) -> str:
    lines = [
        "# Cover Asset Assist",
        "",
        f"- `draft_key`: `{pack.draft_key}`",
        f"- `core_judgment`: `{pack.core_judgment}`",
        f"- `approved_angle`: `{pack.approved_angle}`",
        "",
        "## Asset Strategy",
        "",
        "- 目标不是一键产出终稿，而是给人工设计 / 编辑一个更像样的起点。",
        "- 每个平台都要先回答：这张图是为了让用户点开、看懂，还是为了收藏 / 转发？",
        "- 所有视觉都必须围绕同一核心判断，不允许标题和图片各讲各的。",
        "",
        "## Platform Assist",
        "",
    ]
    if "wechat" in pack.requested_platforms:
        lines.extend(
            [
                "### WeChat",
                "",
                "- 推荐结构：对象名 + stakes 文案 + 1 个结构变化副标题。",
                "- 头图优先横版，适合公众号首屏；不要塞太多字，主副标题合计尽量控制在两层。",
                f"- 可用文案方向 1：`{pack.approved_angle}`",
                f"- 可用文案方向 2：`{pack.core_judgment}`",
                "",
            ]
        )
    if "xiaohongshu" in pack.requested_platforms:
        lines.extend(
            [
                "### Xiaohongshu",
                "",
                "- 推荐做‘封面卡 + 解释卡’连续资产，而不是只有一张封面。",
                "- 封面卡只说一个最强承诺，第二张再补对象背景与 why now。",
                "- 收藏感强于正式感；优先突出‘3 个点看懂 / 现在为什么值得看’。",
                "",
            ]
        )
    if "zhihu" in pack.requested_platforms:
        lines.extend(
            [
                "### Zhihu",
                "",
                "- 头图以解释型为主，帮助用户快速理解对象和讨论问题。",
                "- 更适合‘对象 + 问题 + 结论’的解释图，而不是强营销封面。",
                "",
            ]
        )
    if "bilibili" in pack.requested_platforms:
        lines.extend(
            [
                "### Bilibili",
                "",
                "- 头图要更像 build log / case breakdown，而不是公众号封面搬运。",
                "- 适合用‘对象截图 + 过程拆解标签 + 结论短句’的组合。",
                "",
            ]
        )
    lines.extend(
        [
            "## Prompt Starters",
            "",
            f"- 结构图提示词：围绕“{pack.approved_angle}”生成一张信息架构草图，包含对象、变化、关键变量、风险点四块内容，风格克制、适合科技与商业内容。",
            f"- 头图提示词：围绕“{pack.core_judgment}”生成一张科技内容头图草案，突出对象和结构变化，不要做赛博蓝光污染，不要抽象到看不出主题。",
            "",
            "## Human QC",
            "",
            "- 看图的人 3 秒内能否知道对象是什么？",
            "- 看图的人能否知道为什么现在值得点开？",
            "- 图片有没有把风险、边界或真实对象遮掉？",
            "- 如果把标题拿掉，这张图会不会误导成另一个话题？",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def visual_asset_sourcing(pack: DraftPack) -> str:
    source_refs = source_ref_candidates(pack)
    web_refs = discover_source_urls(pack)
    local_refs = [ref for ref in source_refs if ref not in web_refs]
    asset_dir = pack.pack_dir / "visual-assets"
    capture_script = ROOT / "09_runbooks" / "scripts" / "market_visual_capture_helper.py"
    lines = [
        "# Visual Asset Sourcing",
        "",
        f"- `draft_key`: `{pack.draft_key}`",
        f"- `topic_title`: `{pack.topic_title}`",
        f"- `asset_dir`: `{asset_dir}`",
        f"- `capture_script`: `{capture_script}`",
        "",
        "## Sourcing Priority",
        "",
        "- `tier_1`: `原始截图`｜优先使用原推文、原公告、原 PDF、原产品页、原 repo 页。",
        "- `tier_2`: `官方资产`｜若原始截图不适合正文呈现，则优先用官方 hero image / thumbnail / logo。",
        "- `tier_3`: `解释图`｜结构图、流程图、变量卡，只负责解释，不负责证明事实。",
        "- `tier_4`: `外部补图`｜只有在前 3 层都不合适时才启用。",
        "- `tier_5`: `AI 生成图`｜仅限结构解释，不可冒充事实证据。",
        "- `hard_rule`: `禁止把第三方媒体 / 公众号文章页整页截图直接塞进正文。`",
        "- `fallback_rule`: `截图不安全或抓不到时，优先换原始源 / 官方资产，再退到解释图。`",
        "- `external_provider`: `当前默认启用 Wikimedia Commons 开放许可检索；命中后以 external-safe-image 进入成稿预览。`",
        "- `ai_provider`: `默认优先使用 OpenClaw / MiniMax Token Plan API Key 调用 MiniMax image-01；若无 MiniMax 可用凭证，再回退 OPENAI_API_KEY；都不可用时自动退回本地 structured explainer。`",
        "",
        "## Capture Targets",
        "",
    ]
    if web_refs:
        for index, ref in enumerate(web_refs[:6], start=1):
            policy = source_policy(ref)
            output_path = asset_dir / f"{index:02d}__source-capture.png"
            lines.extend(
                [
                    f"### `target_{index}`",
                    "",
                    f"- `source_ref`: `{ref}`",
                    f"- `source_policy`: `{policy.source_class}`",
                    f"- `policy_note`: `{policy.reason}`",
                    f"- `asset_type`: `{visual_asset_type(ref)}`",
                    f"- `best_use`: `{visual_best_use(ref)}`",
                    f"- `capture_focus`: `{capture_selector_hint(ref)}`",
                    f"- `suggested_output_path`: `{output_path}`",
                    (
                        f"- `capture_command`: `python3 {capture_script} --url \"{ref}\" --output \"{output_path}\" --hide-cookie-banners`"
                        if policy.allow_screenshot
                        else "- `capture_command`: `blocked`｜该 URL 不进入自动截图，改走官方资产 / 替代图 / 解释图"
                    ),
                    "",
                ]
            )
    else:
        lines.extend(
            [
                "- `target_1`: `当前 citation block 尚无可截图网页来源，请先补原始 URL 再执行抓图。`",
                "",
            ]
        )
    if local_refs:
        lines.extend(
            [
                "## Local Analysis Refs",
                "",
            ]
        )
        for index, ref in enumerate(local_refs[:6], start=1):
            lines.extend(
                [
                    f"- `analysis_ref_{index}`: `{ref}`",
                    "- `usage`: `可作为分析参考，但不直接执行网页截图。`",
                ]
            )
        lines.append("")
    lines.extend(
        [
            "## Inline Use Rule",
            "",
            "- 第一张正文图优先承担“原始证据锚点”角色。",
            "- 如果原图信息噪音太大，可先截图留证，再额外做一张解释图。",
            "- 不要让所有图片都挤在开头；长文中段必须至少有 1 个解释型视觉停顿点。",
            "",
            "## Human QC",
            "",
            "- 这张图是否在帮助读者更快理解，而不是只占版面？",
            "- 这张图是否保留了来源可信度线索？",
            "- 如果拿掉这张图，这一段是否明显更难读？",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def load_font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in CARD_FONT_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = list(text)
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current}{word}"
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
            continue
        if current:
            lines.append(current)
        current = word
    if current:
        lines.append(current)
    return lines or [text]


def create_text_card(output_path: Path, title: str, subtitle: str, bullets: list[str], accent: str) -> Path:
    width, height = 1440, 900
    image = Image.new("RGB", (width, height), color=(14, 18, 28))
    draw = ImageDraw.Draw(image)
    for y in range(height):
        blend = y / max(height - 1, 1)
        color = (
            int(14 + (38 - 14) * blend),
            int(18 + (28 - 18) * blend),
            int(28 + (56 - 28) * blend),
        )
        draw.line([(0, y), (width, y)], fill=color)
    draw.rounded_rectangle((64, 64, width - 64, height - 64), radius=28, outline=accent, width=4)
    title_font = load_font(52, bold=True)
    subtitle_font = load_font(28)
    bullet_font = load_font(34)
    kicker_font = load_font(22)
    draw.text((96, 96), "内容工厂自动生成｜解释卡", fill=(190, 200, 220), font=kicker_font)
    title_lines = wrap_text(draw, title, title_font, width - 192)
    cursor_y = 156
    for line in title_lines[:3]:
        draw.text((96, cursor_y), line, fill=(255, 255, 255), font=title_font)
        cursor_y += 72
    subtitle_lines = wrap_text(draw, subtitle, subtitle_font, width - 192)
    for line in subtitle_lines[:3]:
        draw.text((96, cursor_y + 10), line, fill=(181, 196, 214), font=subtitle_font)
        cursor_y += 42
    cursor_y += 24
    for bullet in bullets[:4]:
        bullet_lines = wrap_text(draw, bullet, bullet_font, width - 252)
        draw.ellipse((98, cursor_y + 16, 114, cursor_y + 32), fill=accent)
        line_y = cursor_y
        for idx, line in enumerate(bullet_lines[:3]):
            draw.text((136, line_y), line, fill=(238, 242, 247), font=bullet_font)
            line_y += 42
        cursor_y = line_y + 18
    image.save(output_path)
    return output_path


def slugify_text(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()
    return slug[:48] or "card"


def strip_html_tags(value: str) -> str:
    return clean(re.sub(r"<[^>]+>", " ", unescape(value or "")), "")


def fetch_json(url: str) -> dict:
    try:
        return json.loads(fetch_text(url))
    except Exception:
        return {}


def openclaw_auth_profile_files() -> list[Path]:
    home = Path.home()
    preferred = [
        home / ".openclaw" / "agents" / "main" / "agent" / "auth-profiles.json",
        home / ".openclaw" / "agents" / "market-scout" / "agent" / "auth-profiles.json",
    ]
    discovered = sorted(home.glob(OPENCLAW_AUTH_PROFILES_GLOB))
    ordered: list[Path] = []
    seen: set[Path] = set()
    for path in preferred + discovered:
        if not path.exists() or path in seen:
            continue
        seen.add(path)
        ordered.append(path)
    return ordered


def load_minimax_api_key() -> tuple[str, str]:
    for env_key in ("MINIMAX_API_KEY", "MINIMAX_CN_API_KEY", "MINIMAX_TOKEN_PLAN_API_KEY"):
        value = os.getenv(env_key, "").strip()
        if value:
            return value, f"env:{env_key}"
    for path in openclaw_auth_profile_files():
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        profiles = payload.get("profiles") or {}
        for profile_name in ("minimax-cn:default", "minimax:default"):
            profile = profiles.get(profile_name) or {}
            key = clean(str(profile.get("key", "")), "")
            if profile.get("type") == "api_key" and key and key != "n/a":
                return key, f"openclaw:{path.name}:{profile_name}"
    raise RuntimeError("MiniMax API key missing")


def preferred_visual_platform(pack: DraftPack) -> str:
    for candidate in ("wechat", "zhihu", "bilibili", "baijiahao", "toutiao", "xiaohongshu", "x"):
        if candidate in pack.requested_platforms:
            return candidate
    return pack.requested_platforms[0] if pack.requested_platforms else "wechat"


def normalize_plan_heading(text: str) -> str:
    normalized = re.sub(r"^#+\s*", "", text or "").strip()
    normalized = normalized.replace("`", "").strip()
    return re.sub(r"\s+", " ", normalized)


def canonical_platform_from_heading(text: str) -> str:
    normalized = normalize_plan_heading(text)
    lowered = normalized.lower()
    for platform, aliases in PLATFORM_HEADING_ALIASES.items():
        for alias in aliases:
            if alias in normalized or alias in lowered:
                return platform
    return ""


def is_non_slot_heading(text: str) -> bool:
    normalized = normalize_plan_heading(text)
    lowered = normalized.lower()
    if lowered in NON_SLOT_HEADING_KEYWORDS:
        return True
    return any(keyword in lowered for keyword in NON_SLOT_HEADING_KEYWORDS)


def detect_slot_heading(text: str) -> tuple[bool, dict[str, str]]:
    heading = normalize_plan_heading(text)
    lowered = heading.lower()
    if not heading or is_non_slot_heading(heading):
        return False, {}
    if any(token in lowered for token in ["## visual do", "## visual don't", "## image source", "## human qc"]):
        return False, {}
    required = ""
    if any(token in heading for token in ["必须", "必选", "必做"]):
        required = "required"
    elif any(token in heading for token in ["可选", "备用", "可做"]):
        required = "optional"
    slot_matchers = [
        r"^(?:图|图位)\s*\d+",
        r"^slot(?:[_\s-]*\d+)",
        r"^visual(?:[_\s-]*\d+)",
        r"^image\s*\d+",
        r"^\d+[.)]\s+",
        r"^(?:封面图|cover|hero|quote block|timeline|section divider|final cta area)",
    ]
    if any(re.match(pattern, lowered) for pattern in slot_matchers):
        slot_label = heading
        slot_number_match = re.search(r"(\d+)", heading)
        if slot_number_match:
            slot_label = f"slot_{slot_number_match.group(1)}"
        return True, {"slot": slot_label, "heading": heading, "priority": required}
    return False, {}


def canonical_slot_field(label: str) -> str:
    normalized = re.sub(r"[`*]", "", label or "").strip().strip("：:").lower()
    normalized = normalized.replace(" ", "")
    for canonical, aliases in SLOT_FIELD_ALIASES.items():
        for alias in aliases:
            alias_normalized = alias.lower().replace(" ", "")
            if normalized == alias_normalized:
                return canonical
    return ""


def start_slot(slot_meta: dict[str, str], current_platform: str) -> dict[str, str]:
    payload = {
        "slot": clean(slot_meta.get("slot", "visual_slot"), "visual_slot"),
        "heading": clean(slot_meta.get("heading", slot_meta.get("slot", "visual slot")), "visual slot"),
        "platform": clean(current_platform, ""),
    }
    if slot_meta.get("priority"):
        payload["priority"] = slot_meta["priority"]
    return payload


def append_slot_text(slot: dict[str, str], field_name: str, value: str) -> None:
    cleaned_value = clean(value, "")
    if not cleaned_value:
        return
    previous = clean(slot.get(field_name, ""), "")
    if not previous:
        slot[field_name] = cleaned_value
        return
    if cleaned_value in previous:
        return
    slot[field_name] = f"{previous} | {cleaned_value}"


def finalize_visual_slot(slot: dict[str, str] | None) -> dict[str, str] | None:
    if not slot:
        return None
    finalized = dict(slot)
    if not clean(finalized.get("job", ""), ""):
        text = " ".join(
            [
                finalized.get("heading", ""),
                finalized.get("image_type", ""),
                finalized.get("note", ""),
                finalized.get("requirements", ""),
            ]
        ).lower()
        if any(token in text for token in ["证据", "截图", "原始", "热榜", "repo", "readme", "产品页", "公告"]):
            finalized["job"] = "原始证据锚点"
        elif any(token in text for token in ["数据", "对比", "评分", "成本", "比值", "趋势", "柱状图", "表格"]):
            finalized["job"] = "数据对比"
        elif any(token in text for token in ["封面", "cover", "hero"]):
            finalized["job"] = "封面图"
        else:
            finalized["job"] = clean(finalized.get("heading", "结构解释"), "结构解释")
    if not clean(finalized.get("note", ""), ""):
        fallback_note = clean(finalized.get("requirements", ""), "") or clean(finalized.get("fallback", ""), "")
        if fallback_note:
            finalized["note"] = fallback_note
    if not clean(finalized.get("preferred_asset", ""), "") and clean(finalized.get("image_type", ""), ""):
        finalized["preferred_asset"] = finalized["image_type"]
    return finalized


def parse_visual_slots(pack: DraftPack) -> list[dict[str, str]]:
    path = pack.pack_dir / "inline-visual-plan.md"
    if not path.exists():
        return []
    target_platform = preferred_visual_platform(pack)
    slots: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    current_platform = ""
    active_field = ""
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            active_field = ""
            continue
        if line.startswith("#"):
            detected_platform = canonical_platform_from_heading(line)
            if detected_platform:
                finalized = finalize_visual_slot(current)
                if finalized:
                    slots.append(finalized)
                current = None
                current_platform = detected_platform
                active_field = ""
                continue
            if is_non_slot_heading(line):
                if current is not None and any(
                    token in normalize_plan_heading(line).lower() for token in ["source candidates", "human qc", "图文结构", "source candidate"]
                ):
                    finalized = finalize_visual_slot(current)
                    if finalized:
                        slots.append(finalized)
                    current = None
                active_field = ""
                continue
            is_slot, slot_meta = detect_slot_heading(line)
            if is_slot and (not current_platform or current_platform == target_platform):
                finalized = finalize_visual_slot(current)
                if finalized:
                    slots.append(finalized)
                current = start_slot(slot_meta, current_platform)
                active_field = ""
                continue
            active_field = ""
            continue
        if line.startswith("- `slot_"):
            match = KV_RE.match(line)
            if not match:
                continue
            finalized = finalize_visual_slot(current)
            if finalized:
                slots.append(finalized)
            current = start_slot({"slot": clean(match.group(1), "visual_slot"), "heading": clean(match.group(1), "visual slot")}, current_platform)
            raw_value = clean(match.group(2), "")
            if raw_value and raw_value not in {"n/a", current["slot"]}:
                current["position"] = raw_value
            active_field = ""
            continue
        if line.lower().startswith("### slot"):
            finalized = finalize_visual_slot(current)
            if finalized:
                slots.append(finalized)
            current = start_slot({"slot": clean(normalize_plan_heading(line), "visual_slot"), "heading": normalize_plan_heading(line)}, current_platform)
            active_field = ""
            continue
        if re.match(r"^- `visual[_-]?\d+", line):
            finalized = finalize_visual_slot(current)
            if finalized:
                slots.append(finalized)
            visual_match = re.match(r"^- `([^`]+)`: `([^`]+)`(?:｜用途：(.+?))?(?:｜位置：(.+))?$", line)
            if not visual_match:
                continue
            current = start_slot({"slot": clean(visual_match.group(1), "visual_slot"), "heading": clean(visual_match.group(1), "visual slot")}, current_platform)
            current["preferred_asset"] = clean(visual_match.group(2), "")
            if visual_match.group(3):
                current["job"] = "结构解释"
                current["note"] = clean(visual_match.group(3), "")
            if visual_match.group(4):
                current["position"] = clean(visual_match.group(4), "")
            active_field = ""
            continue
        if line.startswith("- `job`"):
            match = KV_RE.match(line)
            if match and current is not None:
                current["job"] = clean(match.group(2), "")
            continue
        if line.startswith("- `preferred_asset`"):
            match = KV_RE.match(line)
            if match and current is not None:
                current["preferred_asset"] = clean(match.group(2), "")
            continue
        if line.startswith("- `note`"):
            match = KV_RE.match(line)
            if match and current is not None:
                current["note"] = clean(match.group(2), "")
            continue
        if line.startswith("- **任务**：") and current is not None:
            current["job"] = clean(line.split("：", 1)[1], "")
            continue
        if line.startswith("- **推荐素材**：") and current is not None:
            current["preferred_asset"] = clean(line.split("：", 1)[1], "")
            continue
        if line.startswith("- **说明**：") and current is not None:
            current["note"] = clean(line.split("：", 1)[1], "")
            continue
        kv_match = KV_RE.match(line)
        if kv_match and current is not None:
            field_name = canonical_slot_field(kv_match.group(1))
            if field_name:
                current[field_name] = clean(kv_match.group(2), "")
                active_field = field_name if field_name in MULTILINE_SLOT_FIELDS else ""
                continue
        bold_field_match = re.match(r"^-?\s*\*\*(.+?)\*\*[:：]\s*(.*)$", line)
        if bold_field_match and current is not None:
            field_name = canonical_slot_field(bold_field_match.group(1))
            if field_name:
                current[field_name] = clean(bold_field_match.group(2), "")
                active_field = field_name if field_name in MULTILINE_SLOT_FIELDS else ""
                continue
        if current is not None and active_field:
            continuation = re.sub(r"^[-*]\s*", "", line).strip()
            append_slot_text(current, active_field, continuation)
            continue
    finalized = finalize_visual_slot(current)
    if finalized:
        slots.append(finalized)
    if slots:
        return slots
    return [
        {"slot": "slot_1", "job": "对象解释", "preferred_asset": "对象图 / 产品图", "note": "帮助读者知道对象是什么"},
        {"slot": "slot_2", "job": "结构解释", "preferred_asset": "结构图 / 变量卡", "note": "帮助读者知道判断为什么成立"},
        {"slot": "slot_3", "job": "风险提醒", "preferred_asset": "风险卡 / 对比图", "note": "帮助读者知道边界在哪里"},
    ]


def query_terms_from_text(text: str) -> list[str]:
    candidates: list[str] = []
    for token in re.findall(r"[A-Za-z][A-Za-z0-9+._/-]{1,}", text or ""):
        normalized = re.sub(r"[._/-]+", " ", token).strip()
        lowered = normalized.lower()
        if not normalized or lowered in QUERY_TOKEN_STOPWORDS:
            continue
        if len(lowered) <= 2:
            continue
        candidates.append(normalized)
    deduped: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        lowered = candidate.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        deduped.append(candidate)
    return deduped


def normalize_query_phrase(text: str) -> str:
    normalized = re.sub(r"[._/]+", " ", clean(text, ""))
    normalized = re.sub(r"[-–—]+", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip(" ，；：:。,.!?！？()[]{}<>“”\"'")
    return normalized


def tokenize_search_text(text: str) -> set[str]:
    tokens: set[str] = set()
    for candidate in query_terms_from_text(normalize_query_phrase(text)):
        for token in normalize_query_phrase(candidate).split():
            lowered = token.lower().strip()
            if not lowered or lowered in QUERY_TOKEN_STOPWORDS:
                continue
            if len(lowered) <= 2:
                continue
            tokens.add(lowered)
    return tokens


def english_phrase_candidates(text: str) -> list[str]:
    phrases: list[str] = []
    patterns = [
        r"(?:[A-Z][A-Za-z0-9+._/-]{1,}(?:\s+[A-Z][A-Za-z0-9+._/-]{1,}){0,3})",
        r"(?:[A-Z]{2,}[A-Za-z0-9+._/-]*(?:\s+[A-Z][A-Za-z0-9+._/-]{1,}){0,3})",
    ]
    for pattern in patterns:
        for raw in re.findall(pattern, text or ""):
            normalized = normalize_query_phrase(raw)
            if not normalized:
                continue
            tokens = normalized.split()
            if not tokens:
                continue
            if len(tokens) == 1:
                token = tokens[0]
                has_internal_case = any(char.isupper() for char in token[1:]) and any(char.islower() for char in token)
                has_signal_chars = any(char.isdigit() or char in {"+", "-"} for char in token)
                if not has_internal_case and not has_signal_chars:
                    continue
            if all(token.lower() in QUERY_TOKEN_STOPWORDS for token in tokens):
                continue
            phrases.append(normalized)
    deduped: list[str] = []
    seen: set[str] = set()
    for phrase in phrases:
        lowered = phrase.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        deduped.append(phrase)
    return deduped


def query_terms_from_urls(urls: list[str]) -> list[str]:
    terms: list[str] = []
    for url in urls:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        path_parts = [part for part in parsed.path.strip("/").split("/") if part]
        if "github.com" in host:
            for part in path_parts[:2]:
                human = re.sub(r"[_-]+", " ", part).strip()
                if human:
                    terms.append(human)
        else:
            host_parts = [part for part in host.split(".") if part and part not in {"www", "com", "cn", "ai", "co", "io", "org", "net"}]
            if host_parts:
                terms.append(host_parts[0])
            if path_parts:
                tail = re.sub(r"[_-]+", " ", Path(path_parts[-1]).stem).strip()
                if tail.lower() not in QUERY_TOKEN_STOPWORDS:
                    terms.append(tail)
    return query_terms_from_text(" ".join(terms))


def query_phrases_from_urls(urls: list[str]) -> list[str]:
    phrases: list[str] = []
    for url in urls:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        path_parts = [part for part in parsed.path.strip("/").split("/") if part]
        if "github.com" in host and len(path_parts) >= 2:
            owner = normalize_query_phrase(path_parts[0])
            repo = normalize_query_phrase(Path(path_parts[1]).stem)
            if owner:
                phrases.append(owner)
            if repo:
                phrases.append(repo)
            combo = normalize_query_phrase(f"{owner} {repo}")
            if combo:
                phrases.append(combo)
            continue
        if path_parts:
            tail = normalize_query_phrase(Path(path_parts[-1]).stem)
            if tail and len(tail.split()) <= 5 and tail.lower() not in QUERY_TOKEN_STOPWORDS:
                phrases.append(tail)
        host_parts = [part for part in parsed.netloc.split(".") if part and part not in {"www", "com", "cn", "ai", "co", "io", "org", "net"}]
        if host_parts:
            phrases.append(normalize_query_phrase(host_parts[0]))
    deduped: list[str] = []
    seen: set[str] = set()
    for phrase in phrases:
        lowered = phrase.lower()
        if not phrase or lowered in seen:
            continue
        seen.add(lowered)
        deduped.append(phrase)
    return deduped


def infer_concept_queries(pack: DraftPack, slots: list[dict[str, str]]) -> list[str]:
    text = " ".join(
        [
            pack.topic_title,
            pack.approved_angle,
            pack.core_judgment,
            " ".join(slot.get("job", "") for slot in slots),
            " ".join(slot.get("preferred_asset", "") for slot in slots),
        ]
    ).lower()
    concepts: list[str] = []
    if any(token in text for token in ["robot", "robotics", "具身", "机械", "hardware", "硬件"]):
        concepts.extend(["robotics", "robotics concept"])
    if any(token in text for token in ["finance", "ipo", "融资", "资本", "投资", "估值"]):
        concepts.extend(["finance", "technology finance"])
    if any(token in text for token in ["video", "视频", "film", "movie"]):
        concepts.extend(["video technology", "digital media"])
    if any(token in text for token in ["music", "音频", "音乐"]):
        concepts.extend(["music technology"])
    if any(token in text for token in ["chip", "gpu", "cpu", "macbook", "算力", "芯片"]):
        concepts.extend(["computer hardware", "semiconductor"])
    if any(token in text for token in ["model", "agent", "智能体", "模型", "aigc", "agi", "llm", "bench", "benchmark"]):
        concepts.extend(["artificial intelligence", "machine learning diagram"])
    if not concepts:
        concepts.append("artificial intelligence")
    deduped: list[str] = []
    seen: set[str] = set()
    for concept in concepts:
        lowered = concept.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        deduped.append(concept)
    return deduped


def build_external_search_queries(pack: DraftPack, slots: list[dict[str, str]]) -> list[str]:
    urls = discover_source_urls(pack)
    phrase_terms = []
    phrase_terms.extend(query_phrases_from_urls(urls))
    phrase_terms.extend(english_phrase_candidates(pack.topic_title))
    phrase_terms.extend(english_phrase_candidates(pack.approved_angle))
    phrase_terms.extend(english_phrase_candidates(pack.core_judgment))
    deduped_phrases: list[str] = []
    seen_phrases: set[str] = set()
    for phrase in phrase_terms:
        normalized = normalize_query_phrase(phrase)
        lowered = normalized.lower()
        if not normalized or lowered in seen_phrases:
            continue
        seen_phrases.add(lowered)
        deduped_phrases.append(normalized)

    entity_terms = query_terms_from_text(" ".join([pack.topic_title, pack.approved_angle, pack.core_judgment]))
    entity_terms.extend(query_terms_from_urls(urls))
    entity_terms = [
        term
        for term in query_terms_from_text(" ".join(entity_terms))
        if len(term) >= 4 and term.lower() not in QUERY_TOKEN_STOPWORDS
    ]
    concept_terms = infer_concept_queries(pack, slots)
    queries: list[str] = []
    for phrase in deduped_phrases[:6]:
        queries.append(phrase)
    for term in entity_terms[:4]:
        queries.append(term)
    for phrase in deduped_phrases[:2]:
        for concept in concept_terms[:1]:
            combo = f"{phrase} {concept}".strip()
            if combo:
                queries.append(combo)
    for term in entity_terms[:2]:
        for concept in concept_terms[:1]:
            combo = f"{term} {concept}".strip()
            if combo:
                queries.append(combo)
    for concept in concept_terms[:3]:
        queries.append(concept)
        queries.append(f"{concept} diagram")
    deduped: list[str] = []
    seen: set[str] = set()
    for query in queries:
        normalized = clean(query, "")
        lowered = normalized.lower()
        if not normalized or lowered in seen:
            continue
        seen.add(lowered)
        deduped.append(normalized)
    return deduped[:10]


def license_allows_safe_reuse(license_text: str) -> bool:
    lowered = clean(strip_html_tags(license_text), "").lower()
    if not lowered:
        return False
    if any(token in lowered for token in ["noncommercial", "by-nc", "nc", "no derivatives", "by-nd", "nd"]):
        return False
    return any(token in lowered for token in ["cc by", "cc-by", "cc0", "public domain", "pdm", "cc by-sa", "cc-by-sa"])


def wikimedia_commons_candidates(query: str, limit: int = 4) -> list[VisualSearchCandidate]:
    api_url = (
        f"{WIKIMEDIA_COMMONS_API}"
        f"?action=query&generator=search&gsrsearch={quote(query)}&gsrnamespace=6&gsrlimit={max(limit, 1)}"
        "&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=1280&format=json"
    )
    payload = fetch_json(api_url)
    pages = (payload.get("query") or {}).get("pages") or {}
    candidates: list[VisualSearchCandidate] = []
    for page in pages.values():
        image_info = (page.get("imageinfo") or [{}])[0]
        ext = image_info.get("extmetadata") or {}
        license_name = strip_html_tags(((ext.get("LicenseShortName") or {}).get("value")) or ((ext.get("UsageTerms") or {}).get("value")) or "")
        if not license_allows_safe_reuse(license_name):
            continue
        title = clean(str(page.get("title", "")), "")
        lowered_title = title.lower()
        if any(token in lowered_title for token in [".pdf", "icon", "logo"]):
            continue
        image_url = clean(str(image_info.get("thumburl") or image_info.get("url") or ""), "")
        if not image_url:
            continue
        candidates.append(
            VisualSearchCandidate(
                provider="wikimedia-commons",
                query=query,
                title=title,
                image_url=image_url,
                landing_url=clean(str(image_info.get("descriptionurl") or image_info.get("descriptionshorturl") or ""), ""),
                creator=strip_html_tags(((ext.get("Artist") or {}).get("value")) or ""),
                license_name=license_name,
            )
        )
        if len(candidates) >= limit:
            break
    return candidates


def pack_entity_signals(pack: DraftPack, slots: list[dict[str, str]]) -> tuple[list[str], set[str], set[str]]:
    urls = discover_source_urls(pack)
    phrases: list[str] = []
    phrases.extend(query_phrases_from_urls(urls))
    phrases.extend(english_phrase_candidates(pack.topic_title))
    phrases.extend(english_phrase_candidates(pack.approved_angle))
    phrases.extend(english_phrase_candidates(pack.core_judgment))
    deduped_phrases: list[str] = []
    seen_phrases: set[str] = set()
    for phrase in phrases:
        normalized = normalize_query_phrase(phrase)
        lowered = normalized.lower()
        if not normalized or lowered in seen_phrases:
            continue
        seen_phrases.add(lowered)
        deduped_phrases.append(normalized)
    entity_tokens = tokenize_search_text(
        " ".join(
            deduped_phrases
            + query_terms_from_urls(urls)
            + query_terms_from_text(" ".join([pack.topic_title, pack.approved_angle, pack.core_judgment]))
        )
    )
    concept_tokens = tokenize_search_text(" ".join(infer_concept_queries(pack, slots)))
    return deduped_phrases, entity_tokens, concept_tokens


def candidate_relevance_score(
    candidate: VisualSearchCandidate,
    query: str,
    entity_phrases: list[str],
    entity_tokens: set[str],
) -> tuple[int, set[str], set[str]]:
    candidate_text = normalize_query_phrase(" ".join([candidate.title, candidate.landing_url, candidate.image_url])).lower()
    candidate_tokens = tokenize_search_text(candidate_text)
    query_normalized = normalize_query_phrase(query).lower()
    query_tokens = tokenize_search_text(query)
    score = 0
    if query_normalized and len(query_normalized) >= 4 and query_normalized in candidate_text:
        score += 4
    phrase_hits = {
        phrase.lower()
        for phrase in entity_phrases
        if len(phrase) >= 4 and phrase.lower() in candidate_text
    }
    score += min(len(phrase_hits) * 2, 4)
    entity_overlap = candidate_tokens & entity_tokens
    query_overlap = candidate_tokens & query_tokens
    score += min(len(entity_overlap), 3)
    score += min(len(query_overlap), 2)
    return score, entity_overlap, query_overlap


def external_candidate_allowed(
    pack: DraftPack,
    candidate: VisualSearchCandidate,
    query: str,
    entity_phrases: list[str],
    entity_tokens: set[str],
    concept_tokens: set[str],
    *,
    has_primary_visuals: bool,
) -> bool:
    score, entity_overlap, query_overlap = candidate_relevance_score(candidate, query, entity_phrases, entity_tokens)
    candidate_text = normalize_query_phrase(" ".join([candidate.title, candidate.landing_url, candidate.image_url])).lower()
    primary_entity_tokens = tokenize_search_text(" ".join(entity_phrases[:2])) or (entity_tokens - concept_tokens)
    query_tokens = tokenize_search_text(query)
    query_is_concept = bool(query_tokens) and query_tokens.issubset(concept_tokens)
    has_specific_entity = bool(entity_phrases or entity_tokens - concept_tokens)
    phrase_hit = any(len(phrase) >= 4 and phrase.lower() in candidate_text for phrase in entity_phrases[:3])
    if has_primary_visuals and primary_entity_tokens:
        candidate_tokens = tokenize_search_text(" ".join([candidate.title, candidate.landing_url, candidate.image_url]))
        primary_overlap = candidate_tokens & primary_entity_tokens
        if not primary_overlap:
            return False
        return score >= 3
    if has_specific_entity and not query_is_concept and not (entity_overlap or phrase_hit):
        return False
    if query_is_concept and has_specific_entity:
        if not entity_overlap:
            return False
        return score >= (3 if has_primary_visuals else 2)
    if query_is_concept:
        return score >= (3 if has_primary_visuals else 2)
    if entity_overlap or query_overlap:
        return score >= 2
    return score >= 4


def slot_is_evidence_like(slot: dict[str, str]) -> bool:
    text = " ".join(
        [
            slot.get("heading", ""),
            slot.get("job", ""),
            slot.get("preferred_asset", ""),
            slot.get("note", ""),
            slot.get("requirements", ""),
            slot.get("image_type", ""),
        ]
    ).lower()
    return any(
        token in text
        for token in [
            "证据",
            "原始",
            "截图",
            "公告",
            "repo",
            "readme",
            "pdf",
            "锚点",
            "原帖",
            "热榜",
            "trending",
            "问题截图",
            "官方",
            "产品页",
        ]
    )


def slot_is_data_like(slot: dict[str, str]) -> bool:
    text = " ".join(
        [
            slot.get("heading", ""),
            slot.get("job", ""),
            slot.get("image_type", ""),
            slot.get("note", ""),
            slot.get("requirements", ""),
        ]
    ).lower()
    return any(
        token in text
        for token in [
            "数据",
            "评分",
            "成本",
            "比值",
            "估值",
            "数字",
            "benchmark",
            "bar",
            "chart",
            "柱状图",
            "条形图",
            "表格",
            "可视化",
            "对比图",
            "对照图",
        ]
    )


def slot_is_cover_like(slot: dict[str, str]) -> bool:
    text = " ".join([slot.get("heading", ""), slot.get("job", ""), slot.get("image_type", "")]).lower()
    return any(token in text for token in ["封面", "cover", "hero", "headline", "首图"])


def slot_is_framework_like(slot: dict[str, str]) -> bool:
    text = " ".join(
        [
            slot.get("heading", ""),
            slot.get("job", ""),
            slot.get("image_type", ""),
            slot.get("note", ""),
            slot.get("requirements", ""),
            slot.get("preferred_asset", ""),
            slot.get("position", ""),
        ]
    ).lower()
    return any(
        token in text
        for token in [
            "结构",
            "框架",
            "流程",
            "阶段",
            "架构",
            "分类",
            "四象限",
            "工作流",
            "workflow",
            "signal",
            "skill",
            "step",
            "时间线",
            "timeline",
            "roadmap",
            "变量",
            "三层",
            "四层",
            "五层",
            "地图",
            "关系",
            "分层",
            "收束",
            "quote",
            "引语",
        ]
    )


def slot_prefers_primary_asset(slot: dict[str, str]) -> bool:
    text = " ".join(
        [
            slot.get("heading", ""),
            slot.get("job", ""),
            slot.get("preferred_asset", ""),
            slot.get("requirements", ""),
        ]
    ).lower()
    return slot_is_evidence_like(slot) or any(
        token in text
        for token in ["原始截图", "官方", "公告", "repo", "readme", "产品页", "热榜", "github", "知乎", "截图"]
    )


def slot_is_explainer_like(slot: dict[str, str]) -> bool:
    return slot_is_framework_like(slot) or any(
        token in " ".join([slot.get("job", ""), slot.get("preferred_asset", ""), slot.get("note", "")]).lower()
        for token in ["对比", "风险", "解释", "结论", "提醒"]
    )


def create_structured_slot_card(output_path: Path, pack: DraftPack, slot: dict[str, str], accent: str) -> Path:
    width, height = 1600, 900
    image = Image.new("RGB", (width, height), color=(247, 249, 253))
    draw = ImageDraw.Draw(image)
    for y in range(height):
        blend = y / max(height - 1, 1)
        color = (
            int(247 - 10 * blend),
            int(249 - 6 * blend),
            int(253 - 2 * blend),
        )
        draw.line([(0, y), (width, y)], fill=color)
    draw.rounded_rectangle((56, 48, width - 56, height - 48), radius=30, outline=accent, width=5)
    title_font = load_font(56, bold=True)
    kicker_font = load_font(22)
    subtitle_font = load_font(28)
    body_font = load_font(30)
    label_font = load_font(22, bold=True)

    kicker = f"结构解释卡｜{slot.get('slot', 'visual slot')}"
    draw.text((92, 86), kicker, fill=(92, 106, 130), font=kicker_font)
    title = slot.get("job", "结构解释")
    title_lines = wrap_text(draw, title, title_font, width - 184)
    cursor_y = 126
    for line in title_lines[:2]:
        draw.text((92, cursor_y), line, fill=(17, 24, 39), font=title_font)
        cursor_y += 72
    subtitle = trim_text(pack.approved_angle, 58)
    for line in wrap_text(draw, subtitle, subtitle_font, width - 184)[:2]:
        draw.text((92, cursor_y), line, fill=(85, 99, 122), font=subtitle_font)
        cursor_y += 42

    blocks = [
        ("What Changed", trim_text(pack.approved_angle, 60)),
        ("Core View", trim_text(pack.core_judgment, 60)),
        ("Watch Next", trim_text(pack.risk_note, 60)),
    ]
    block_y = 338
    block_width = 430
    gap = 40
    for index, (label, content) in enumerate(blocks):
        left = 92 + index * (block_width + gap)
        right = left + block_width
        draw.rounded_rectangle((left, block_y, right, 760), radius=22, fill=(255, 255, 255), outline=(220, 229, 240), width=2)
        draw.text((left + 28, block_y + 24), label, fill=accent, font=label_font)
        text_y = block_y + 70
        for line in wrap_text(draw, content, body_font, block_width - 56)[:6]:
            draw.text((left + 28, text_y), line, fill=(31, 41, 55), font=body_font)
            text_y += 38
    footer = "说明：这是一张解释型图卡，不用于充当原始事实证据。"
    draw.text((92, 804), footer, fill=(107, 114, 128), font=kicker_font)
    image.save(output_path)
    return output_path


def hex_to_rgb(value: str, fallback: tuple[int, int, int] = (59, 130, 246)) -> tuple[int, int, int]:
    cleaned = clean(value, "").lstrip("#")
    if len(cleaned) != 6:
        return fallback
    try:
        return tuple(int(cleaned[index : index + 2], 16) for index in (0, 2, 4))
    except ValueError:
        return fallback


def split_slot_points(text: str) -> list[str]:
    seed = clean(text, "")
    if not seed:
        return []
    lines: list[str] = []
    for chunk in re.split(r"[\n|]+", seed):
        chunk = chunk.strip()
        if not chunk:
            continue
        for piece in re.split(r"(?:→|->|；|;)", chunk):
            cleaned_piece = re.sub(r"^[\-\*\d.\s]+", "", piece).strip(" ：:，,。")
            if cleaned_piece:
                lines.append(cleaned_piece)
    deduped: list[str] = []
    seen: set[str] = set()
    for item in lines:
        normalized = item.lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(item)
    return deduped


def strip_markdown_inline(text: str) -> str:
    normalized = text or ""
    normalized = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", normalized)
    normalized = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", normalized)
    normalized = re.sub(r"[*_`>#]+", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def is_visual_meta_phrase(text: str) -> bool:
    lowered = strip_markdown_inline(text).lower()
    if not lowered:
        return True
    return any(
        token in lowered
        for token in [
            "px",
            "alt",
            "版权",
            "尺寸",
            "宽度",
            "高度",
            "占位符",
            "来源标注",
            "图注",
            "slot_",
            "正文第",
            "章节之后",
            "小节之后",
            "位置",
            "可合理使用",
            "输出路径",
            "数据来源：",
            "recommended",
            "purpose",
            "position",
            "placeholder",
            "copyright",
            "best use",
        ]
    )


def normalize_visual_phrase(text: str, max_chars: int = 0) -> str:
    normalized = strip_markdown_inline(text)
    normalized = normalized.replace('"', "").replace("“", "").replace("”", "").replace("「", "").replace("」", "")
    normalized = re.sub(r"^[一二三四五六七八九十百]+\s*[、.．]\s*", "", normalized)
    normalized = re.sub(r"^\d+\s*[、.．]\s*", "", normalized)
    normalized = re.sub(r"^(?:图|图位)\s*\d+\s*[：:、.\-]?\s*", "", normalized, flags=re.I)
    normalized = re.sub(r"^(?:slot|visual|image)\s*[_-]?\d+\s*[：:、.\-]?\s*", "", normalized, flags=re.I)
    normalized = re.sub(r"^正文第\s*\d+\s*段\s*", "", normalized)
    normalized = re.sub(
        r"[（(][^）)]*(?:必须|可选|备用|尺寸|版权|alt|来源标注|位置|占位符|视制作资源决定|若有优质素材则加)[^）)]*[）)]",
        "",
        normalized,
        flags=re.I,
    )
    normalized = re.sub(r"\bOR\b", "/", normalized, flags=re.I)
    normalized = re.sub(r"^(?:建议|优先|若无原图|若无|如果|可选|备用|视制作资源决定|若有优质素材则加)[：:，,\s]*", "", normalized)
    normalized = normalized.replace("截图", "").replace("示意图", "").replace("图卡", "")
    normalized = re.sub(r"\s+", " ", normalized).strip(" ，；：:。,.!?！？/|-")
    if max_chars and len(normalized) > max_chars:
        return trim_text(normalized, max_chars)
    return normalized


def searchable_visual_text(text: str) -> str:
    normalized = normalize_visual_phrase(text)
    normalized = re.sub(r"\s+", "", normalized).lower()
    return normalized


def primary_markdown_path(pack: DraftPack) -> Path | None:
    preferred = preferred_visual_platform(pack)
    field_candidates = [
        f"{preferred}_path",
        "wechat_path",
        "zhihu_path",
        "bilibili_path",
        "toutiao_path",
        "baijiahao_path",
        "xiaohongshu_path",
        "x_path",
    ]
    for field_name in field_candidates:
        raw_path = clean(pack.paths.get(field_name, "n/a"), "")
        if not raw_path or raw_path == "n/a":
            continue
        resolved = resolve_doc_path(raw_path)
        if resolved.exists():
            return resolved
    return None


def primary_markdown_title(pack: DraftPack) -> str:
    markdown_path = primary_markdown_path(pack)
    if markdown_path is None:
        return trim_text(pack.topic_title, 28)
    for raw in markdown_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("# "):
            title = normalize_visual_phrase(line[2:])
            title = re.sub(r"^[^｜|]{1,10}稿[｜|]\s*", "", title)
            return title
    return trim_text(pack.topic_title, 28)


def primary_markdown_lead(pack: DraftPack) -> str:
    markdown_path = primary_markdown_path(pack)
    if markdown_path is None:
        return trim_text(pack.core_judgment, 48)
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    body_started = False
    for raw in lines:
        line = raw.strip()
        if line.startswith("# "):
            body_started = True
            continue
        if not body_started or not line or line.startswith("![") or line.startswith("---"):
            continue
        if any(
            token in line
            for token in [
                "封面图建议",
                "副标题",
                "开篇一句话",
                "信息来源",
                "参考来源",
                "同行资本 TH Capital",
            ]
        ):
            continue
        if line.startswith(">"):
            line = line.lstrip(">").strip()
        cleaned_line = normalize_visual_phrase(line, 52)
        if cleaned_line and len(cleaned_line) >= 10:
            return cleaned_line
    return trim_text(pack.core_judgment, 48)


def packaging_bundle_fields(pack: DraftPack) -> dict[str, str]:
    raw_path = clean(pack.paths.get("packaging_bundle_path", "n/a"), "")
    if not raw_path or raw_path == "n/a":
        return {}
    resolved = resolve_doc_path(raw_path)
    if not resolved.exists():
        return {}
    return parse_simple_fields(resolved)


def is_morning_roundup_pack(pack: DraftPack) -> bool:
    title = clean(pack.topic_title, "").strip()
    draft_key = clean(pack.draft_key, "").strip().lower()
    return draft_key.startswith("ai_morning_brief_") or title.startswith("AI早报｜")


def morning_roundup_event_count(pack: DraftPack) -> str:
    text = " ".join([pack.topic_title, pack.approved_angle, pack.core_judgment])
    match = re.search(r"(\d+)\s*个", text)
    if match:
        return match.group(1)
    return "9"


def morning_roundup_title_lines(pack: DraftPack) -> list[str]:
    title = clean(pack.topic_title, "AI早报").strip()
    if "｜" in title:
        left, right = [part.strip() for part in title.split("｜", 1)]
        if left and right:
            return [left, right]
    return [title]


def extract_ratio_signal(text: str) -> str:
    normalized = normalize_visual_phrase(text, 36)
    if not normalized:
        return ""
    ratio_match = re.search(r"(\d+\s*/\s*\d+)", normalized)
    if ratio_match and "成本" in normalized:
        return f"{ratio_match.group(1).replace(' ', '')} 成本"
    if ratio_match:
        return ratio_match.group(1).replace(" ", "")
    return ""


def compact_cover_signal(candidate: str) -> str:
    normalized = normalize_visual_phrase(candidate, 24)
    if not normalized:
        return ""
    lowered = normalized.lower()
    if any(token in normalized for token in ["封面图建议", "一句话背景", "内容封面"]):
        return ""
    if any(
        token in lowered
        for token in [
            "headline",
            "background",
            "cash line",
            "why_this_package",
            "让用户愿意点开",
            "普通资讯稿",
            "值得沿着",
            "包装",
            "hook",
        ]
    ):
        return ""
    replacements = [
        ("AI圈复古命令行风潮", "CLI 复兴"),
        ("Karpathy推文影响", "Karpathy 点火"),
        ("大厂案例", "大厂跟进"),
        ("为什么现在爆发", "时点成熟"),
        ("YC-Bench 长程任务验证", "长程验证"),
        ("一手硬数据", "一手硬数据"),
        ("核心数据对比", "核心数据"),
        ("GitHub 上的具体信号", "GitHub 信号"),
        ("大厂也在复古", "大厂跟进"),
    ]
    for old, new in replacements:
        normalized = normalized.replace(old, new)
    normalized = re.sub(r"^(第一|第二|第三|第四)[，,、]\s*", "", normalized)
    normalized = re.sub(r"^(第一|第二|第三|第四)\s*", "", normalized)
    normalized = normalized.replace("这不是官方 benchmark", "非官方 benchmark")
    if normalized.endswith("是什么"):
        normalized = normalized[:-3].strip()
    ratio_signal = extract_ratio_signal(normalized)
    if ratio_signal:
        return ratio_signal
    multiple_match = re.search(r"(\d+\s*(?:[-~]|—|–)\s*\d+\s*倍)", normalized)
    if multiple_match:
        return multiple_match.group(1).replace(" ", "")
    if any(token in lowered for token in ["yc-bench", "yc bench"]):
        return "YC-Bench"
    if "ceo" in lowered and any(token in lowered for token in ["模拟", "创业公司", "一年"]):
        return "CEO 模拟"
    if "长程" in normalized and any(token in normalized for token in ["验证", "决策"]):
        return "长程验证"
    if "openai" in lowered and any(token in normalized for token in ["回归", "重返", "回到"]):
        return "重返 OpenAI"
    if "karpathy" in lowered and any(token in normalized for token in ["推文", "站台", "带火", "强推"]):
        return "Karpathy 点火"
    if "github" in lowered and any(token in normalized for token in ["信号", "趋势", "trending"]):
        return "GitHub 信号"
    if "benchmark" in lowered and "不是" in normalized:
        return ""
    if "cost" in lowered and re.search(r"\d", lowered):
        return trim_text(normalized, 12)
    if "命令行" in normalized:
        return "CLI 复兴" if any(token in normalized for token in ["复古", "复兴", "回潮", "押注"]) else "命令行"
    if "cli" in lowered:
        return "CLI 复兴"
    if "大厂" in normalized and any(token in normalized for token in ["跟进", "押注", "回归", "复古"]):
        return "大厂跟进"
    if "缓存" in normalized:
        return "缓存风险"
    if "漏洞" in normalized:
        return "安全风险"
    if "源码" in normalized:
        return "源码能力"
    if "验证" in normalized and len(normalized) <= 10:
        return normalized
    if "数据" in normalized and len(normalized) <= 10:
        return normalized
    if len(normalized) > 12 and not re.search(r"\d", normalized):
        return ""
    return normalized if len(normalized) <= 12 else ""


def split_cover_claims(text: str) -> list[str]:
    pieces: list[str] = []
    for chunk in re.split(r"[；;]", text or ""):
        chunk = normalize_visual_phrase(chunk, 28)
        if not chunk:
            continue
        sub_parts = re.split(r"[：:、，,]", chunk)
        if len(sub_parts) <= 2:
            pieces.append(chunk)
            continue
        for sub in sub_parts:
            normalized = normalize_visual_phrase(sub, 22)
            if normalized:
                pieces.append(normalized)
    deduped: list[str] = []
    seen: set[str] = set()
    for piece in pieces:
        compact = compact_cover_signal(piece)
        lowered = compact.lower()
        if not compact or lowered in seen:
            continue
        seen.add(lowered)
        deduped.append(compact)
    return deduped


def cover_signal_pills(pack: DraftPack, limit: int = 3) -> list[str]:
    if is_morning_roundup_pack(pack):
        return ["官方更新", "Builder 信号", "中文观察"][:limit]
    pills: list[str] = []
    bundle = packaging_bundle_fields(pack)
    title_keywords = {searchable_visual_text(line) for line in cover_title_lines(pack)}
    for key in ("core_claim", "angle_short", "angle_full"):
        pills.extend(split_cover_claims(bundle.get(key, "")))
    markdown_path = primary_markdown_path(pack)
    if markdown_path is not None:
        markdown = markdown_path.read_text(encoding="utf-8")
        lead_ratio = extract_ratio_signal(markdown[:1200])
        if lead_ratio:
            pills.append(lead_ratio)
        for match in re.findall(r"(\d+\s*(?:[-~]|—|–)\s*\d+\s*倍)", markdown[:1600]):
            pills.append(match.replace(" ", ""))
        for section in extract_markdown_sections(markdown)[:5]:
            compact = compact_cover_signal(section.get("title", ""))
            if compact:
                pills.append(compact)
    cleaned: list[str] = []
    seen: set[str] = set()
    for pill in pills:
        lowered = pill.lower()
        if not pill or lowered in seen:
            continue
        if searchable_visual_text(pill) in title_keywords:
            continue
        if lowered in {"背景原因", "投资视角", "边界和风险提示", "结论", "时点成熟", "为什么是现在", "值不值得关注"}:
            continue
        if any(token in pill for token in ["封面图建议", "一句话背景"]):
            continue
        if any(token in lowered for token in ["值得看", "headline", "背景", "普通资讯稿", "包装"]):
            continue
        if len(pill) > 12 and not re.search(r"\d", pill):
            continue
        seen.add(lowered)
        cleaned.append(pill)
        if len(cleaned) >= limit:
            break
    return cleaned[:limit]


def clean_cover_framework_point(text: str, max_chars: int = 14) -> str:
    normalized = normalize_visual_phrase(text, max_chars * 2)
    normalized = re.sub(r"^第\s*\d+\s*层[：:]\s*", "", normalized)
    normalized = re.sub(r"^step\s*\d+\s*[：:]\s*", "", normalized, flags=re.I)
    normalized = re.sub(r"^最小可用\s*workflow[：:]\s*", "", normalized, flags=re.I)
    normalized = re.sub(r"^微信稿[｜|]\s*", "", normalized)
    normalized = normalized.strip(" ：:，,。")
    return trim_text(normalized, max_chars) if normalized else ""


def cover_framework_points(pack: DraftPack, limit: int = 4) -> list[str]:
    if is_morning_roundup_pack(pack):
        return ["太长不看", "逐条展开", "继续追踪"][:limit]
    points: list[str] = []
    markdown_path = primary_markdown_path(pack)
    if markdown_path is not None and markdown_path.exists():
        seen: set[str] = set()
        for section in extract_markdown_sections(markdown_path.read_text(encoding="utf-8")):
            level = int(section.get("level", "0") or 0)
            if level < 3:
                continue
            point = clean_cover_framework_point(section.get("title", ""))
            if not point or is_visual_meta_phrase(point):
                continue
            lowered = point.lower()
            if lowered in seen:
                continue
            seen.add(lowered)
            points.append(point)
            if len(points) >= limit:
                return points
    pills = cover_signal_pills(pack, limit=limit)
    for pill in pills:
        lowered = pill.lower()
        if lowered in {item.lower() for item in points}:
            continue
        points.append(pill)
        if len(points) >= limit:
            break
    return points[:limit]


def compress_cover_title_fragment(text: str, max_chars: int = 18) -> str:
    normalized = normalize_visual_phrase(text)
    if not normalized:
        return ""
    replacements = [
        ("在长程决策测试里站到了全球头部", "站到全球头部"),
        ("在长程决策测试里站到全球头部", "站到全球头部"),
        ("在长程决策测试里", "长程决策"),
        ("长程决策测试里", "长程决策"),
        ("长程决策测试", "长程决策"),
        ("悄悄放大", "放大"),
    ]
    for old, new in replacements:
        normalized = normalized.replace(old, new)
    if len(normalized) > max_chars and "站到全球头部" in normalized:
        model_match = re.search(r"([A-Za-z0-9.+-]+)", normalized)
        if model_match:
            normalized = f"{model_match.group(1)} 站到全球头部"
        else:
            normalized = "站到全球头部"
    return trim_text(normalized, max_chars) if len(normalized) > max_chars else normalized


def split_cover_title_lines(text: str, max_lines: int = 3) -> list[str]:
    normalized = normalize_visual_phrase(text)
    if not normalized:
        return ["TH Capital"]
    sentence_parts: list[str] = []
    buffer = ""
    for char in normalized:
        buffer += char
        if char in "？?!！：:":
            sentence_parts.append(buffer.strip())
            buffer = ""
    if buffer.strip():
        sentence_parts.append(buffer.strip())
    compact_sentence_parts = [compress_cover_title_fragment(part, 22) for part in sentence_parts if compress_cover_title_fragment(part, 22)]
    if len(compact_sentence_parts) >= 2 and all(len(part) <= 22 for part in compact_sentence_parts[:max_lines]):
        return compact_sentence_parts[:max_lines]
    parts = [compress_cover_title_fragment(part, 20) for part in re.split(r"[：:，,、]|——| - ", normalized) if compress_cover_title_fragment(part, 20)]
    if len(parts) >= 2:
        return parts[:max_lines]
    if len(normalized) <= 18:
        return [normalized]
    max_chars = 20 if len(normalized) <= 34 else 16
    lines: list[str] = []
    remaining = normalized
    while remaining and len(lines) < max_lines - 1:
        if len(remaining) <= max_chars:
            break
        window = remaining[: max_chars + 6]
        split_idx = 0
        for candidate in range(len(window) - 1, max(max_chars - 6, 1), -1):
            if window[candidate] in "？?!！：:，,、 的了与和让把将从向在":
                split_idx = candidate + 1
                break
        if split_idx <= 0:
            split_idx = max_chars
        line = compress_cover_title_fragment(remaining[:split_idx].strip(), max_chars + 2)
        if line:
            lines.append(line)
        remaining = remaining[split_idx:].strip()
    if remaining:
        lines.append(compress_cover_title_fragment(remaining, max_chars + 2))
    result = [line for line in lines if line]
    if not result:
        return [trim_text(normalized, 20)]
    if len(result) > max_lines:
        head = result[: max_lines - 1]
        tail = "".join(result[max_lines - 1 :]).strip()
        result = head + [compress_cover_title_fragment(tail, max_chars + 2)]
    return result[:max_lines]


def cover_title_candidate_strength(candidate: str) -> int:
    normalized = normalize_visual_phrase(candidate, 38)
    if not normalized or is_visual_meta_phrase(normalized):
        return -99
    lowered = normalized.lower()
    if any(
        token in lowered
        for token in [
            "headline",
            "background",
            "cash line",
            "why_this_package",
            "让用户愿意点开",
            "普通资讯稿",
            "为什么值得",
            "包装",
        ]
    ):
        return -99
    score = 0
    length = len(normalized)
    if 10 <= length <= 28:
        score += 6
    elif 6 <= length <= 36:
        score += 3
    else:
        score -= 2
    if re.search(r"\d", normalized):
        score += 2
    if any(
        token in lowered
        for token in [
            "karpathy",
            "openai",
            "claude",
            "glm",
            "grok",
            "qwen",
            "anthropic",
            "xai",
            "agent",
            "cli",
            "benchmark",
            "ipo",
            "命令行",
            "成本",
            "源码",
            "缓存",
            "漏洞",
            "回归",
            "ceo",
        ]
    ):
        score += 2
    if length < 8 and not re.search(r"\d", normalized):
        score -= 4
    if normalized.endswith(("强推", "值得看")) and length < 10:
        score -= 4
    return score


def cover_title_lines(pack: DraftPack) -> list[str]:
    if is_morning_roundup_pack(pack):
        return morning_roundup_title_lines(pack)
    bundle = packaging_bundle_fields(pack)
    title_candidates = [
        primary_markdown_title(pack),
        pack.topic_title,
        bundle.get("recommended_title", ""),
        bundle.get("core_claim", ""),
    ]
    best_lines: list[str] = []
    best_score = -999
    for candidate in title_candidates:
        lines = split_cover_title_lines(candidate, max_lines=3)
        joined = "".join(lines).strip()
        score = cover_title_candidate_strength(joined)
        if score > best_score and lines:
            best_lines = lines
            best_score = score
    if best_lines:
        return best_lines
    return [trim_text(pack.topic_title, 18)]


def cover_subtitle_fragment_candidates(text: str) -> list[str]:
    raw = strip_markdown_inline(text or "")
    if not raw:
        return []
    fragments: list[str] = []
    for sentence in re.split(r"[。！？!?；;]", raw):
        sentence = sentence.strip()
        if not sentence:
            continue
        for piece in re.split(r"[：:]", sentence):
            for sub_piece in re.split(r"[，,]", piece):
                normalized = normalize_visual_phrase(sub_piece, 42)
                if normalized and normalized not in {"一句话背景", "背景", "为什么是现在", "值不值得关注"}:
                    fragments.append(normalized)
    deduped: list[str] = []
    seen: set[str] = set()
    for fragment in fragments:
        lowered = fragment.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        deduped.append(fragment)
    return deduped


def cover_subtitle_score(candidate: str, title_keywords: set[str]) -> int:
    normalized = normalize_visual_phrase(candidate, 42)
    if not normalized or is_visual_meta_phrase(normalized):
        return -99
    lowered = normalized.lower()
    score = 0
    length = len(normalized)
    if 10 <= length <= 30:
        score += 6
    elif length <= 38:
        score += 3
    else:
        score -= 2
    if re.search(r"\d", normalized):
        score += 3
    if any(
        token in lowered
        for token in [
            "成本",
            "回归",
            "命令行",
            "cli",
            "agent",
            "benchmark",
            "ceo",
            "源码",
            "漏洞",
            "缓存",
            "openai",
            "karpathy",
            "glm",
            "anthropic",
            "opus",
        ]
    ):
        score += 2
    if any(token in normalized for token in ["看命令行", "你还是看命令行", "重返 OpenAI"]):
        score += 5
    if any(token in normalized for token in ["持续更新", "判断系统", "判断链", "不是猜", "而是", "TACO"]):
        score += 4
    if any(lowered.startswith(prefix) for prefix in ["最近有一个", "很多人会把", "今早", "简单说", "如果你", "读者可能"]):
        score -= 4
    if any(token in lowered for token in ["如何做一个", "agent / skill", "agent/skill", "如何做 agent", "如何做 skill"]):
        score -= 8
    if any(token in lowered for token in ["值得看", "普通资讯稿", "headline", "包装", "风潮", "背景原因", "为什么现在"]):
        score -= 6
    if searchable_visual_text(normalized) in title_keywords:
        score -= 2
    return score


def cover_subtitle_line(pack: DraftPack) -> str:
    if is_morning_roundup_pack(pack):
        return f"隔夜 {morning_roundup_event_count(pack)} 条 AI 热点，一次看完"
    bundle = packaging_bundle_fields(pack)
    title_keywords = {searchable_visual_text(line) for line in cover_title_lines(pack)}
    candidates = [bundle.get("core_claim", ""), primary_markdown_lead(pack), pack.core_judgment, pack.approved_angle]
    best_fragment = ""
    best_score = -999
    for candidate in candidates:
        for fragment in cover_subtitle_fragment_candidates(candidate):
            score = cover_subtitle_score(fragment, title_keywords)
            if score > best_score:
                best_fragment = fragment
                best_score = score
    return trim_text(best_fragment or pack.topic_title, 40)


def cover_summary_line(pack: DraftPack) -> str:
    if is_morning_roundup_pack(pack):
        return "先抓主线，再决定白天重点追哪一条"
    bundle = packaging_bundle_fields(pack)
    title_keywords = {searchable_visual_text(line) for line in cover_title_lines(pack)}
    best_fragment = ""
    best_score = -999
    candidates = [
        bundle.get("core_claim", ""),
        bundle.get("background_cash_line", ""),
        bundle.get("cold_start_gap", ""),
        bundle.get("why_this_package_wins", ""),
        pack.core_judgment,
        pack.approved_angle,
    ]
    for candidate in candidates:
        for fragment in cover_subtitle_fragment_candidates(candidate):
            if len(fragment) > 24:
                continue
            score = cover_subtitle_score(fragment, title_keywords)
            if score > best_score:
                best_fragment = fragment
                best_score = score
    return trim_text(best_fragment, 22) if best_fragment else ""


def cover_contrast_lines(pack: DraftPack) -> tuple[str, str]:
    candidates = [pack.core_judgment, pack.approved_angle, primary_markdown_lead(pack)]
    for candidate in candidates:
        text = strip_markdown_inline(candidate or "")
        match = re.search(r"不是(.{4,28}?)(?:，|,)?而是(.{4,40}?)(?:。|$)", text)
        if not match:
            continue
        left = normalize_visual_phrase(match.group(1), 28)
        right = normalize_visual_phrase(match.group(2), 40)
        left_line = f"不是{left}" if left else ""
        right_line = f"而是{right}" if right else ""
        if left_line or right_line:
            return trim_text(left_line, 22), trim_text(right_line, 26)
    return "", ""


def cover_takeaway_line(pack: DraftPack) -> str:
    if is_morning_roundup_pack(pack):
        return "先抓主线，不被碎片热点带跑"
    markdown_path = primary_markdown_path(pack)
    candidates: list[str] = []
    if markdown_path is not None and markdown_path.exists():
        markdown = markdown_path.read_text(encoding="utf-8")
        candidates.extend(re.findall(r"\*\*([^*]{8,48})\*\*", markdown))
    candidates.extend([pack.core_judgment, pack.approved_angle, primary_markdown_lead(pack)])
    contrast_left, contrast_right = cover_contrast_lines(pack)

    def score(candidate: str) -> int:
        normalized = normalize_visual_phrase(candidate, 38)
        if not normalized or normalized in {contrast_left, contrast_right}:
            return -99
        value = normalized.lower()
        points = 0
        length = len(normalized)
        if 10 <= length <= 26:
            points += 8
        elif length <= 34:
            points += 3
        else:
            points -= 4
        if any(token in normalized for token in ["判断", "约束", "退路", "成本", "顶不顶得住", "不是看", "而是盯"]):
            points += 6
        if any(token in value for token in ["headline", "skill", "agent / skill", "agent/skill"]):
            points -= 4
        return points

    best = ""
    best_score = -999
    for candidate in candidates:
        normalized = normalize_visual_phrase(candidate, 38)
        current_score = score(normalized)
        if current_score > best_score:
            best = normalized
            best_score = current_score
    return trim_text(best, 30) if best and best_score > 0 else ""


def cover_kicker_label(pack: DraftPack) -> str:
    text = " ".join([pack.topic_title, pack.core_judgment, pack.approved_angle]).lower()
    if any(token in text for token in ["bug", "漏洞", "缓存", "风险", "安全", "隐患"]):
        return "工程风险预警"
    if any(token in text for token in ["源码", "source", "repo", "代码泄漏", "开源"]):
        return "源码学习笔记"
    if any(token in text for token in ["融资", "ipo", "估值", "revenue", "deal", "funding", "资本"]):
        return "资本信号"
    if any(token in text for token in ["一人公司", "solo", "个人生产力"]):
        return "一人公司观察"
    return "AI 产业观察"


def cover_theme_colors(pack: DraftPack) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
    text = " ".join([pack.topic_title, pack.core_judgment, pack.approved_angle]).lower()
    if any(token in text for token in ["ipo", "融资", "估值", "资本", "vc", "投资"]):
        return (8, 26, 37), (14, 53, 69), (32, 201, 151), (224, 252, 244)
    if any(token in text for token in ["chip", "芯片", "hardware", "semiconductor"]):
        return (16, 28, 51), (24, 66, 95), (72, 193, 255), (229, 247, 255)
    if any(token in text for token in ["karpathy", "人才", "回归", "openai"]):
        return (8, 31, 66), (21, 63, 122), (38, 214, 96), (241, 249, 255)
    return (9, 26, 54), (18, 47, 102), (43, 204, 72), (240, 248, 255)


def extract_markdown_sections(markdown: str) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []
    current_title = ""
    current_level = 0
    current_lines: list[str] = []
    for raw in markdown.splitlines():
        match = MARKDOWN_HEADING_RE.match(raw.strip())
        if match:
            if current_title:
                sections.append(
                    {
                        "title": current_title,
                        "level": str(current_level),
                        "content": "\n".join(current_lines).strip(),
                    }
                )
            current_level = len(match.group(1))
            current_title = normalize_visual_phrase(match.group(2))
            current_lines = []
            continue
        if current_title:
            current_lines.append(raw.rstrip())
    if current_title:
        sections.append({"title": current_title, "level": str(current_level), "content": "\n".join(current_lines).strip()})
    return sections


def quoted_section_hints(text: str) -> list[str]:
    hints: list[str] = []
    for pattern in [
        r'"([^"]{2,40})"',
        r"“([^”]{2,40})”",
        r"「([^」]{2,40})」",
        r"'([^']{2,40})'",
    ]:
        for candidate in re.findall(pattern, text or ""):
            normalized = normalize_visual_phrase(candidate, 28)
            if normalized:
                hints.append(normalized)
    deduped: list[str] = []
    seen: set[str] = set()
    for hint in hints:
        lowered = hint.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        deduped.append(hint)
    return deduped


def plain_section_hints(text: str) -> list[str]:
    seed = normalize_visual_phrase(text, 32)
    if not seed:
        return []
    hints = [seed]
    trimmed = re.sub(r"(?:段后|节后|章后|部分后|之后|后|前)$", "", seed).strip(" ：:，,。")
    if trimmed and trimmed != seed:
        hints.append(trimmed)
    for piece in re.split(r"[|/｜]+", trimmed or seed):
        normalized_piece = normalize_visual_phrase(piece, 24)
        if not normalized_piece:
            continue
        normalized_piece = re.sub(r"(?:首屏后|正文前中段|正文前段|正文中段|正文后段)$", "", normalized_piece).strip(" ：:，,。")
        if normalized_piece:
            hints.append(normalized_piece)
    deduped: list[str] = []
    seen: set[str] = set()
    for hint in hints:
        lowered = hint.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        deduped.append(hint)
    return deduped


def section_hints_from_slot(slot: dict[str, str]) -> list[str]:
    hints: list[str] = []
    for field_name in ("position", "heading", "note", "requirements", "job"):
        hints.extend(quoted_section_hints(slot.get(field_name, "")))
        hints.extend(plain_section_hints(slot.get(field_name, "")))
    heading = normalize_visual_phrase(slot.get("heading", ""))
    if "：" in heading:
        hints.append(normalize_visual_phrase(heading.split("：", 1)[1], 28))
    elif ":" in heading:
        hints.append(normalize_visual_phrase(heading.split(":", 1)[1], 28))
    if not hints:
        hints.extend(
            [
                normalize_visual_phrase(slot.get("job", ""), 24),
                normalize_visual_phrase(slot.get("note", ""), 24),
            ]
        )
    deduped: list[str] = []
    seen: set[str] = set()
    for hint in hints:
        if not hint or is_visual_meta_phrase(hint):
            continue
        lowered = hint.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        deduped.append(hint)
    return deduped


def best_section_for_slot(slot: dict[str, str], pack: DraftPack) -> dict[str, str] | None:
    markdown_path = primary_markdown_path(pack)
    if markdown_path is None:
        return None
    markdown = markdown_path.read_text(encoding="utf-8")
    sections = extract_markdown_sections(markdown)
    if not sections:
        return None
    hints = section_hints_from_slot(slot)
    best_section: dict[str, str] | None = None
    best_score = -1
    slot_text = " ".join(
        [
            slot.get("position", ""),
            slot.get("heading", ""),
            slot.get("job", ""),
            slot.get("note", ""),
            slot.get("requirements", ""),
            slot.get("preferred_asset", ""),
        ]
    ).lower()
    for section in sections:
        title = clean(section.get("title", ""), "")
        lowered_title = searchable_visual_text(title)
        content = section.get("content", "")
        score = 0
        for hint in hints:
            lowered_hint = searchable_visual_text(hint)
            if lowered_hint == lowered_title:
                score += 8
            elif lowered_hint and lowered_hint in lowered_title:
                score += 5
            elif lowered_hint and lowered_title in lowered_hint:
                score += 3
        if slot_is_data_like(slot) and extract_markdown_tables(content):
            score += 5
        if slot_is_framework_like(slot) and any(token in lowered_title for token in ["什么", "框架", "结构", "流程", "阶段", "why", "为何", "背景"]):
            score += 2
        if slot_is_evidence_like(slot) and any(token in lowered_title for token in ["信号", "数据", "热度", "来源", "证据", "github"]):
            score += 2
        if any(token in slot_text for token in ["约束识别", "关键信号", "四类", "四象限"]) and any(
            token in lowered_title for token in ["约束识别", "关键信号", "信号"]
        ):
            score += 6
        if any(token in slot_text for token in ["五层", "5层", "skill", "架构"]) and any(
            token in lowered_title for token in ["五层", "5层", "skill", "结构", "架构"]
        ):
            score += 6
        if any(token in slot_text for token in ["workflow", "工作流", "四步", "4步", "step"]) and any(
            token in lowered_title for token in ["workflow", "工作流", "循环", "step", "4步", "四步"]
        ):
            score += 6
        if score > best_score:
            best_score = score
            best_section = section
    if best_score > 0:
        return best_section
    if slot_is_data_like(slot):
        for section in sections:
            if extract_markdown_tables(section.get("content", "")):
                return section
    return sections[0] if sections else None


def clean_story_label(label: str) -> str:
    normalized = normalize_visual_phrase(label, 16)
    normalized = re.sub(r"^(?:第[一二三四五六七八九十]+|[一二三四五六七八九十]+)[、，]\s*", "", normalized)
    return normalized


def clean_story_desc(desc: str) -> str:
    normalized = normalize_visual_phrase(desc, 42)
    normalized = re.sub(r"^(?:展示|说明|指出|意味着)[：:\s]*", "", normalized)
    return normalized


def compact_editorial_desc(desc: str, max_chars: int = 40) -> str:
    normalized = clean_story_desc(desc)
    normalized = re.sub(r"^(?:这层只回答三件事|一句话|正确顺序是|比如|每天固定抓这几类输入|不要只输出一个百分比)[：:\s]*", "", normalized)
    normalized = normalized.replace("特朗普有一个很典型的特征：", "")
    normalized = normalized.replace("你要让系统去追的，不是更多情绪，而是更多约束。至少盯这四类：", "")
    if " / " in normalized:
        parts = [trim_text(clean_story_desc(part), 14) for part in normalized.split(" / ") if clean_story_desc(part)]
        if len(parts) >= 2:
            return " / ".join(parts[:3])
    if "→" in normalized:
        parts = [trim_text(clean_story_desc(part), 12) for part in normalized.split("→") if clean_story_desc(part)]
        if len(parts) >= 2:
            return " → ".join(parts[:3])
    return trim_text(normalized, max_chars)


def add_story_item(items: list[tuple[str, str]], label: str, desc: str, limit: int = 4) -> None:
    label_clean = clean_story_label(label)
    desc_clean = clean_story_desc(desc)
    if not label_clean and not desc_clean:
        return
    if is_visual_meta_phrase(label_clean) or is_visual_meta_phrase(desc_clean):
        return
    if not label_clean:
        label_clean = f"要点 {len(items) + 1}"
    signature = f"{label_clean.lower()}::{desc_clean.lower()}"
    existing = {f"{left.lower()}::{right.lower()}" for left, right in items}
    if signature in existing:
        return
    items.append((label_clean, desc_clean))
    if len(items) > limit:
        del items[limit:]


def extract_story_items_from_text(section: dict[str, str], limit: int = 4) -> list[tuple[str, str]]:
    content = section.get("content", "")
    items: list[tuple[str, str]] = []
    tables = extract_markdown_tables(content)
    for table in tables:
        headers = list(table.get("headers") or [])
        rows = list(table.get("rows") or [])
        if len(headers) == 2 and rows:
            for row in rows[:limit]:
                add_story_item(items, row[0], row[1], limit=limit)
            if items:
                return items[:limit]

    for raw in content.splitlines():
        line = raw.strip()
        if not line or line.startswith("!["):
            continue
        bullet_match = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.*)$", line)
        if bullet_match:
            body = strip_markdown_inline(bullet_match.group(1))
            bold_match = re.match(r"^\*\*(.+?)\*\*[:：，,\s]*(.*)$", bullet_match.group(1))
            if bold_match:
                add_story_item(items, bold_match.group(1), bold_match.group(2), limit=limit)
                continue
            phased = re.match(r"^(第一阶段|第二阶段|第三阶段|第四阶段|中期|后期|前期|阶段\s*\d+|Step\s*\d+|20\d{2})[:：]\s*(.+)$", body, flags=re.I)
            if phased:
                add_story_item(items, phased.group(1), phased.group(2), limit=limit)
                continue
            if "：" in body:
                left, right = body.split("：", 1)
                add_story_item(items, left, right, limit=limit)
                continue
            if ":" in body:
                left, right = body.split(":", 1)
                add_story_item(items, left, right, limit=limit)
                continue
            add_story_item(items, f"要点 {len(items) + 1}", body, limit=limit)
            continue
        bold_line_match = re.match(r"^\s*\*\*(.+?)\*\*[:：，,\s]*(.*)$", line)
        if bold_line_match:
            add_story_item(items, bold_line_match.group(1), bold_line_match.group(2), limit=limit)
            continue
        inline_bold_match = re.match(r"^(第一|第二|第三|第四)[，,](.+)$", strip_markdown_inline(line))
        if inline_bold_match:
            add_story_item(items, inline_bold_match.group(1), inline_bold_match.group(2), limit=limit)
            continue
    if items:
        return items[:limit]

    stage_hits = re.findall(
        r"(第一阶段|第二阶段|第三阶段|第四阶段|中期|后期|前期|阶段\s*\d+|Step\s*\d+|20\d{2})\s*[:：]\s*([^\n。]+)",
        strip_markdown_inline(content),
        flags=re.I,
    )
    for label, desc in stage_hits[:limit]:
        add_story_item(items, label, desc, limit=limit)
    if items:
        return items[:limit]

    plain = strip_markdown_inline(content)
    for sentence in re.split(r"[。；;!?！？]", plain):
        cleaned_sentence = clean_story_desc(sentence)
        if len(cleaned_sentence) < 10 or is_visual_meta_phrase(cleaned_sentence):
            continue
        add_story_item(items, f"要点 {len(items) + 1}", cleaned_sentence, limit=limit)
        if len(items) >= limit:
            break
    return items[:limit]


def extract_slot_points_from_plan(slot: dict[str, str], pack: DraftPack, limit: int = 3) -> list[str]:
    def normalize_point(candidate: str) -> str:
        cleaned_candidate = clean(candidate, "")
        cleaned_candidate = re.sub(r"^[若如可请建议推荐优先使用生成制作截图配上截一张]+", "", cleaned_candidate)
        cleaned_candidate = re.sub(r"^(展示|说明|建议内容|制作要求|推荐素材|优先素材)[:：]\s*", "", cleaned_candidate)
        cleaned_candidate = cleaned_candidate.replace("截图", "").replace("可合理使用", "").replace("仅用于解释结构", "")
        cleaned_candidate = cleaned_candidate.strip(" ，；：:。,.")
        return trim_text(cleaned_candidate, 32)

    def is_meta_point(candidate: str) -> bool:
        lowered = clean(candidate, "").lower()
        return any(
            token in lowered
            for token in [
                "px",
                "宽度",
                "高度",
                "尺寸",
                "alt",
                "版权",
                "可选",
                "备用",
                "正文第",
                "位置",
                "slot_",
                "图 ",
                "图位",
                "来源标注",
            ]
        )

    candidates: list[str] = []
    for key in ("requirements", "note", "fallback", "preferred_asset", "image_type"):
        candidates.extend(split_slot_points(slot.get(key, "")))
    arrow_source = " ".join([slot.get("requirements", ""), slot.get("note", ""), slot.get("preferred_asset", "")])
    for arrow_piece in re.split(r"(?:→|->)", arrow_source):
        normalized_piece = normalize_point(arrow_piece)
        if normalized_piece and not is_meta_point(normalized_piece):
            candidates.insert(0, normalized_piece)
    if not candidates:
        candidates.extend(split_slot_points(pack.approved_angle))
    if len(candidates) < limit:
        candidates.extend(split_slot_points(pack.core_judgment))
    compact: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        trimmed = normalize_point(candidate)
        if not trimmed:
            continue
        if is_meta_point(trimmed) and len(compact) >= 1:
            continue
        lowered = trimmed.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        compact.append(trimmed)
        if len(compact) >= limit:
            break
    if compact:
        return compact
    return [
        trim_text(pack.approved_angle, 30),
        trim_text(pack.core_judgment, 30),
        trim_text(pack.risk_note, 30),
    ][:limit]


def extract_slot_points(slot: dict[str, str], pack: DraftPack, limit: int = 3) -> list[str]:
    section = best_section_for_slot(slot, pack)
    if section is not None:
        items = extract_story_items_from_text(section, limit=limit)
        if items:
            points = [desc or label for label, desc in items]
            compact = [trim_text(point, 36) for point in points if point]
            if compact:
                return compact[:limit]
    return extract_slot_points_from_plan(slot, pack, limit)


def slot_kind_label(slot: dict[str, str]) -> str:
    if slot_is_cover_like(slot):
        return "封面卡"
    if slot_is_data_like(slot):
        return "数据图"
    if slot_is_evidence_like(slot):
        return "证据图"
    if slot_is_framework_like(slot):
        return "结构图"
    return "解释图"


def derive_slot_title(slot: dict[str, str], pack: DraftPack) -> str:
    generic_jobs = {"原始证据锚点", "结构解释", "对象解释", "数据对比", "封面图"}
    heading = clean(slot.get("heading", ""), "")
    if "：" in heading:
        heading = heading.split("：", 1)[1]
    elif ":" in heading:
        heading = heading.split(":", 1)[1]
    if "｜" in heading:
        heading = heading.split("｜", 1)[-1]
    elif "|" in heading:
        heading = heading.split("|", 1)[-1]
    heading = normalize_visual_phrase(heading, 28)
    section = best_section_for_slot(slot, pack)
    title_candidates = []
    job = clean(slot.get("job", ""), "")
    if slot_is_evidence_like(slot):
        title_candidates.extend([heading, job])
    if section is not None:
        title_candidates.append(section.get("title", ""))
    if job and job not in generic_jobs:
        title_candidates.append(job)
    if heading and not re.fullmatch(r"(?:图|slot|visual)\s*\d+.*", heading.lower()):
        title_candidates.append(heading)
    title_candidates.extend([slot.get("image_type", ""), slot.get("note", ""), job, pack.topic_title])
    for candidate in title_candidates:
        normalized = clean(candidate, "")
        if not normalized:
            continue
        if re.fullmatch(r"slot_\d+", normalized.lower()):
            continue
        return trim_text(normalized, 28)
    return trim_text(pack.topic_title, 28)


def derive_slot_subtitle(slot: dict[str, str], pack: DraftPack) -> str:
    section = best_section_for_slot(slot, pack)
    subtitle_candidates = []
    if section is not None and section.get("title"):
        subtitle_candidates.append(f"把正文“{section.get('title', '')}”这一节压成一张图")
    subtitle_candidates.extend([slot.get("note", ""), slot.get("requirements", ""), pack.approved_angle])
    for candidate in subtitle_candidates:
        normalized = normalize_visual_phrase(candidate, 44)
        if normalized:
            return trim_text(normalized, 44)
    return trim_text(pack.core_judgment, 44)


def create_headline_cover_card(output_path: Path, pack: DraftPack, slot: dict[str, str], accent: str) -> Path:
    if is_morning_roundup_pack(pack):
        return create_morning_roundup_cover_card(output_path, pack)
    width, height = 1600, 900
    base_rgb, panel_rgb, accent_rgb, soft_rgb = cover_theme_colors(pack)
    bg_rgb = tuple(min(255, max(244, soft_rgb[index] + 2)) for index in range(3))
    panel_fill = (252, 253, 255)
    ink_rgb = (18, 31, 53)
    muted_rgb = (91, 104, 126)

    image = Image.new("RGB", (width, height), color=bg_rgb)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        blend = y / max(height - 1, 1)
        color = (
            int(bg_rgb[0] + (255 - bg_rgb[0]) * blend * 0.14),
            int(bg_rgb[1] + (255 - bg_rgb[1]) * blend * 0.1),
            int(bg_rgb[2] + (255 - bg_rgb[2]) * blend * 0.08),
        )
        draw.line([(0, y), (width, y)], fill=color)
    grid_rgb = tuple(min(252, max(220, channel + 8)) for channel in soft_rgb)
    for x in range(0, width, 68):
        draw.line([(x, 0), (x, height)], fill=grid_rgb, width=1)
    for y in range(0, height, 68):
        draw.line([(0, y), (width, y)], fill=grid_rgb, width=1)

    shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((64, 56, width - 64, height - 56), radius=42, fill=(12, 25, 48, 18))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    image = Image.alpha_composite(image.convert("RGBA"), shadow).convert("RGB")
    draw = ImageDraw.Draw(image)

    outer = (58, 50, width - 58, height - 50)
    draw.rounded_rectangle(outer, radius=40, fill=panel_fill, outline=(214, 224, 238), width=2)
    draw.rounded_rectangle((86, 84, 186, 92), radius=4, fill=accent_rgb)

    right_panel = (980, 118, width - 96, height - 118)
    draw.rounded_rectangle(right_panel, radius=34, fill=(247, 250, 255), outline=(214, 224, 238), width=2)
    draw.rounded_rectangle((right_panel[0] + 30, right_panel[1] + 28, right_panel[0] + 154, right_panel[1] + 66), radius=19, fill=accent_rgb)

    accent_wash = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    accent_draw = ImageDraw.Draw(accent_wash)
    accent_draw.ellipse((width - 450, 180, width - 120, 470), fill=(*accent_rgb, 26))
    accent_draw.ellipse((width - 320, 480, width - 40, 800), fill=(*panel_rgb, 18))
    accent_wash = accent_wash.filter(ImageFilter.GaussianBlur(34))
    image = Image.alpha_composite(image.convert("RGBA"), accent_wash).convert("RGB")
    draw = ImageDraw.Draw(image)

    brand_font = load_font(26, bold=False)
    title_lines = cover_title_lines(pack)
    longest_line = max((len(line) for line in title_lines), default=0)
    title_font_size = 98 if longest_line <= 12 else 88 if longest_line <= 18 else 76
    title_font = load_font(title_font_size, bold=True)
    subtitle_font = load_font(30)
    pill_font = load_font(21, bold=True)
    footer_font = load_font(21, bold=False)
    panel_title_font = load_font(28, bold=True)
    panel_item_font = load_font(28, bold=True)
    panel_note_font = load_font(23)
    panel_tag_font = load_font(18, bold=True)

    kicker = cover_kicker_label(pack)
    draw.text((88, 104), f"TH Capital | {kicker}", fill=muted_rgb, font=brand_font)

    title_x = 88
    title_y = 168
    max_title_width = 804
    line_gap = 98 if title_font_size >= 92 else 88 if title_font_size >= 84 else 78
    for line in title_lines[:3]:
        wrapped = wrap_text(draw, line, title_font, max_title_width)
        current_line = wrapped[0] if wrapped else line
        draw.text((title_x, title_y), current_line, fill=ink_rgb, font=title_font)
        title_y += line_gap

    contrast_left, contrast_right = cover_contrast_lines(pack)
    subtitle = contrast_left or cover_subtitle_line(pack)
    subtitle_y = title_y + 12
    for line in wrap_text(draw, subtitle, subtitle_font, max_title_width)[:2]:
        draw.text((title_x, subtitle_y), line, fill=muted_rgb, font=subtitle_font)
        subtitle_y += 42

    summary = contrast_right or cover_summary_line(pack)
    if not summary or summary == subtitle:
        summary = compact_editorial_desc(pack.core_judgment or pack.approved_angle, 30)
    if summary:
        summary_y = subtitle_y + 24
        draw.rounded_rectangle((title_x, summary_y, title_x + 760, summary_y + 74), radius=24, fill=(243, 248, 253), outline=(223, 231, 241), width=2)
        draw.text((title_x + 22, summary_y + 12), trim_text(summary, 34), fill=ink_rgb, font=subtitle_font)
    else:
        summary_y = subtitle_y

    pills = cover_signal_pills(pack, limit=3)
    chip_x = title_x
    chip_y = summary_y + 104
    for pill in pills:
        text_width = int(draw.textlength(pill, font=pill_font))
        chip_width = max(126, text_width + 42)
        draw.rounded_rectangle((chip_x, chip_y, chip_x + chip_width, chip_y + 46), radius=23, fill=(245, 251, 248), outline=accent_rgb, width=2)
        draw.text((chip_x + 20, chip_y + 11), pill, fill=accent_rgb, font=pill_font)
        chip_x += chip_width + 14
        if chip_x > 860:
            chip_x = title_x
            chip_y += 58

    draw.text((right_panel[0] + 58, right_panel[1] + 36), "方法框架", fill=(255, 255, 255), font=panel_tag_font)
    draw.text((right_panel[0] + 34, right_panel[1] + 94), "把判断变成可复用结构", fill=ink_rgb, font=panel_title_font)
    panel_points = cover_framework_points(pack, limit=3)
    panel_y = right_panel[1] + 150
    point_gap = 18
    for index, point in enumerate(panel_points[:4], start=1):
        item_top = panel_y + (index - 1) * (92 + point_gap)
        item_box = (right_panel[0] + 28, item_top, right_panel[2] - 28, item_top + 92)
        draw.rounded_rectangle(item_box, radius=24, fill=(255, 255, 255), outline=(223, 231, 241), width=2)
        chip_box = (item_box[0] + 20, item_box[1] + 22, item_box[0] + 82, item_box[1] + 54)
        draw.rounded_rectangle(chip_box, radius=16, fill=accent_rgb)
        draw.text((chip_box[0] + 22, chip_box[1] + 7), f"{index:02d}", fill=(255, 255, 255), font=panel_tag_font)
        draw.text((item_box[0] + 102, item_box[1] + 23), trim_text(point, 16), fill=ink_rgb, font=panel_item_font)

    panel_note = cover_takeaway_line(pack) or compact_editorial_desc(pack.core_judgment or pack.approved_angle, 32)
    note_box = (right_panel[0] + 28, right_panel[3] - 148, right_panel[2] - 28, right_panel[3] - 30)
    draw.rounded_rectangle(note_box, radius=28, fill=(243, 248, 253), outline=(223, 231, 241), width=2)
    draw.text((note_box[0] + 26, note_box[1] + 20), "读完要带走的判断", fill=accent_rgb, font=panel_tag_font)
    note_y = note_box[1] + 48
    for line in wrap_text(draw, panel_note, panel_note_font, note_box[2] - note_box[0] - 52)[:3]:
        draw.text((note_box[0] + 26, note_y), line, fill=muted_rgb, font=panel_note_font)
        note_y += 30

    footer_y = height - 118
    draw.text((88, footer_y), "同行资本内容工厂出品 | proof-first editorial cover", fill=(118, 129, 146), font=footer_font)
    draw.text((width - 278, footer_y), "同行资本 TH Capital", fill=(72, 87, 110), font=load_font(26, bold=True))
    image.save(output_path)
    return output_path


def create_morning_roundup_cover_card(output_path: Path, pack: DraftPack) -> Path:
    width, height = 1600, 900
    bg_rgb = (245, 241, 233)
    navy_rgb = (12, 31, 58)
    navy_soft = (28, 56, 95)
    cream_rgb = (252, 248, 242)
    orange_rgb = (239, 134, 52)
    line_rgb = (220, 210, 194)
    ink_rgb = (23, 36, 54)
    muted_rgb = (88, 98, 114)
    pale_blue = (230, 239, 247)

    image = Image.new("RGB", (width, height), color=bg_rgb)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        blend = y / max(height - 1, 1)
        color = (
            int(bg_rgb[0] + (255 - bg_rgb[0]) * blend * 0.08),
            int(bg_rgb[1] + (250 - bg_rgb[1]) * blend * 0.05),
            int(bg_rgb[2] + (248 - bg_rgb[2]) * blend * 0.04),
        )
        draw.line([(0, y), (width, y)], fill=color)
    for x in range(70, width - 70, 84):
        draw.line([(x, 70), (x, height - 70)], fill=line_rgb, width=1)
    for y in range(70, height - 70, 84):
        draw.line([(70, y), (width - 70, y)], fill=line_rgb, width=1)

    outer = (48, 46, width - 48, height - 46)
    draw.rounded_rectangle(outer, radius=42, fill=cream_rgb, outline=(214, 202, 184), width=2)

    left_panel = (84, 82, 808, height - 82)
    right_panel = (846, 82, width - 84, height - 82)
    draw.rounded_rectangle(left_panel, radius=36, fill=navy_rgb)
    draw.rounded_rectangle(right_panel, radius=36, fill=(248, 245, 239), outline=(224, 216, 203), width=2)
    draw.rounded_rectangle((left_panel[0] + 34, left_panel[1] + 34, left_panel[0] + 174, left_panel[1] + 74), radius=20, fill=orange_rgb)
    draw.rounded_rectangle((right_panel[0] + 34, right_panel[1] + 34, right_panel[0] + 178, right_panel[1] + 74), radius=20, fill=navy_rgb)

    accent_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    accent_draw = ImageDraw.Draw(accent_overlay)
    accent_draw.ellipse((left_panel[0] + 420, left_panel[1] + 360, left_panel[0] + 760, left_panel[1] + 720), fill=(*orange_rgb, 42))
    accent_draw.ellipse((right_panel[0] + 180, right_panel[1] + 70, right_panel[0] + 620, right_panel[1] + 440), fill=(*pale_blue, 118))
    accent_overlay = accent_overlay.filter(ImageFilter.GaussianBlur(36))
    image = Image.alpha_composite(image.convert("RGBA"), accent_overlay).convert("RGB")
    draw = ImageDraw.Draw(image)

    label_font = load_font(23, bold=True)
    overline_font = load_font(28, bold=False)
    series_font = load_font(122, bold=True)
    subtitle_font = load_font(30)
    chip_font = load_font(20, bold=True)
    number_font = load_font(20, bold=True)
    right_title_font = load_font(46, bold=True)
    right_copy_font = load_font(25)
    item_font = load_font(30, bold=True)
    note_font = load_font(24)
    footer_font = load_font(20, bold=False)
    brand_font = load_font(24, bold=True)

    title_lines = cover_title_lines(pack)
    series_line = title_lines[0] if title_lines else "AI早报"
    date_line = title_lines[1] if len(title_lines) > 1 else ""
    subtitle = cover_subtitle_line(pack)
    summary = cover_takeaway_line(pack) or "隔夜变量太多，先抓主线再开工。"
    pills = cover_signal_pills(pack, limit=3)
    panel_points = cover_framework_points(pack, limit=3)
    event_count = morning_roundup_event_count(pack)

    draw.text((left_panel[0] + 52, left_panel[1] + 44), "TH Capital | Morning Brief", fill=(255, 255, 255), font=label_font)
    draw.text((left_panel[0] + 52, left_panel[1] + 114), "栏目固定封面", fill=(161, 178, 202), font=overline_font)
    draw.text((left_panel[0] + 52, left_panel[1] + 188), series_line, fill=(248, 245, 239), font=series_font)

    date_box = (left_panel[0] + 52, left_panel[1] + 356, left_panel[0] + 328, left_panel[1] + 426)
    draw.rounded_rectangle(date_box, radius=28, fill=orange_rgb)
    draw.text((date_box[0] + 28, date_box[1] + 14), date_line or "今日刊", fill=(255, 255, 255), font=load_font(40, bold=True))
    draw.text((left_panel[0] + 52, left_panel[1] + 454), f"隔夜 {event_count} 条 AI 热点，先看结构，再看波动。", fill=(216, 225, 238), font=subtitle_font)

    summary_box = (left_panel[0] + 52, left_panel[1] + 530, left_panel[0] + 618, left_panel[1] + 682)
    draw.rounded_rectangle(summary_box, radius=30, fill=navy_soft, outline=(74, 104, 146), width=2)
    draw.text((summary_box[0] + 26, summary_box[1] + 22), "今天先拿住什么", fill=(255, 214, 179), font=chip_font)
    summary_y = summary_box[1] + 60
    for line in wrap_text(draw, summary, note_font, summary_box[2] - summary_box[0] - 52)[:3]:
        draw.text((summary_box[0] + 26, summary_y), line, fill=(245, 247, 251), font=note_font)
        summary_y += 32

    chip_y = left_panel[3] - 108
    chip_x = left_panel[0] + 52
    for pill in pills:
        chip_width = int(draw.textlength(pill, font=chip_font)) + 42
        draw.rounded_rectangle((chip_x, chip_y, chip_x + chip_width, chip_y + 42), radius=21, fill=(245, 247, 251))
        draw.text((chip_x + 20, chip_y + 10), pill, fill=navy_rgb, font=chip_font)
        chip_x += chip_width + 14

    draw.text((right_panel[0] + 52, right_panel[1] + 44), "隔夜主线", fill=(255, 255, 255), font=label_font)
    draw.text((right_panel[0] + 52, right_panel[1] + 108), "不是拼热点数量，而是先把今天的主线排出来。", fill=ink_rgb, font=right_copy_font)
    draw.text((right_panel[0] + 52, right_panel[1] + 168), subtitle, fill=ink_rgb, font=right_title_font)

    band_top = right_panel[1] + 254
    draw.rounded_rectangle((right_panel[0] + 52, band_top, right_panel[2] - 52, band_top + 88), radius=26, fill=(255, 255, 255), outline=(222, 214, 202), width=2)
    draw.text((right_panel[0] + 80, band_top + 28), "AI 早报固定阅读顺序", fill=muted_rgb, font=chip_font)

    item_top = band_top + 126
    for index, point in enumerate(panel_points, start=1):
        box_top = item_top + (index - 1) * 126
        box = (right_panel[0] + 52, box_top, right_panel[2] - 52, box_top + 104)
        draw.rounded_rectangle(box, radius=28, fill=(255, 255, 255), outline=(222, 214, 202), width=2)
        num_box = (box[0] + 22, box[1] + 22, box[0] + 90, box[1] + 56)
        draw.rounded_rectangle(num_box, radius=17, fill=orange_rgb)
        draw.text((num_box[0] + 21, num_box[1] + 7), f"{index:02d}", fill=(255, 255, 255), font=number_font)
        draw.text((box[0] + 116, box[1] + 28), point, fill=ink_rgb, font=item_font)
        helper = (
            "先看 8-10 条热点，快速建立全局感。"
            if index == 1
            else "把重点条目拆开看，抓事实、影响和判断。"
            if index == 2
            else "把白天还要继续盯的线索提前标出来。"
        )
        draw.text((box[0] + 116, box[1] + 62), helper, fill=muted_rgb, font=note_font)

    footer_line = height - 132
    draw.text((84, footer_line), "固定系列封面 | 日期与重点会更新，视觉骨架不再每天重做", fill=(113, 108, 102), font=footer_font)
    draw.text((width - 360, footer_line), "同行资本 TH Capital", fill=navy_rgb, font=brand_font)
    image.save(output_path)
    return output_path


def story_style_from_items(slot: dict[str, str], section: dict[str, str] | None, items: list[tuple[str, str]]) -> str:
    joined = " ".join([section.get("title", "") if section else "", slot.get("heading", ""), slot.get("job", ""), slot.get("note", "")]).lower()
    labels = " ".join(label for label, _ in items).lower()
    if any(token in joined for token in ["时间线", "timeline", "路径", "履历", "career", "阶段", "框架", "流程", "结构"]):
        return "stage-flow"
    if any(re.search(pattern, labels, flags=re.I) for pattern in [r"20\d{2}", r"第一阶段", r"第二阶段", r"第三阶段", r"中期", r"后期", r"step\s*\d+"]):
        return "stage-flow"
    if len(items) >= 3:
        return "signal-grid"
    return "step-stack"


def create_stage_flow_card(
    output_path: Path,
    title: str,
    subtitle: str,
    items: list[tuple[str, str]],
    accent: str,
) -> Path:
    width, height = 1440, 900
    image = Image.new("RGB", (width, height), color=(247, 249, 253))
    draw = ImageDraw.Draw(image)
    accent_rgb = hex_to_rgb(accent, (59, 130, 246))
    for y in range(height):
        blend = y / max(height - 1, 1)
        color = (
            int(247 + (255 - 247) * blend),
            int(249 + (252 - 249) * blend),
            int(253 + (255 - 253) * blend),
        )
        draw.line([(0, y), (width, y)], fill=color)
    draw.rounded_rectangle((42, 34, width - 42, height - 34), radius=30, outline=(203, 216, 235), width=3)

    kicker_font = load_font(24, bold=True)
    title_font = load_font(52, bold=True)
    subtitle_font = load_font(26)
    label_font = load_font(24, bold=True)
    body_font = load_font(24)
    title_y = 78
    draw.text((84, title_y), "结构图｜关键路径", fill=accent_rgb, font=kicker_font)
    title_y += 42
    for line in wrap_text(draw, title, title_font, width - 168)[:2]:
        draw.text((84, title_y), line, fill=(26, 37, 54), font=title_font)
        title_y += 64
    for line in wrap_text(draw, subtitle, subtitle_font, width - 168)[:2]:
        draw.text((84, title_y + 4), line, fill=(92, 106, 130), font=subtitle_font)
        title_y += 36

    cards = items[:4]
    count = max(len(cards), 1)
    line_y = 420
    start_x = 170
    end_x = width - 170
    step = (end_x - start_x) / max(count - 1, 1)
    draw.line([(start_x, line_y), (end_x, line_y)], fill=(180, 197, 221), width=6)
    for index, (label, desc) in enumerate(cards):
        center_x = int(start_x + index * step)
        draw.ellipse((center_x - 18, line_y - 18, center_x + 18, line_y + 18), fill=accent_rgb)
        card_top = 482
        card_left = max(72, min(width - 72 - 250, center_x - 125))
        card_right = card_left + 250
        card_bottom = 770
        draw.rounded_rectangle((card_left, card_top, card_right, card_bottom), radius=24, fill=(255, 255, 255), outline=(212, 223, 239), width=2)
        chip_width = max(94, int(draw.textlength(label, font=label_font) + 34))
        draw.rounded_rectangle((card_left + 20, card_top + 18, card_left + 20 + chip_width, card_top + 58), radius=18, fill=(235, 243, 255))
        draw.text((card_left + 36, card_top + 27), label, fill=accent_rgb, font=label_font)
        body_y = card_top + 82
        for line in wrap_text(draw, desc or label, body_font, 210)[:6]:
            draw.text((card_left + 24, body_y), line, fill=(37, 48, 65), font=body_font)
            body_y += 34
    draw.text((84, 826), "根据正文对应章节信息自动整理", fill=(111, 122, 145), font=kicker_font)
    image.save(output_path)
    return output_path


def create_signal_grid_card(
    output_path: Path,
    title: str,
    subtitle: str,
    items: list[tuple[str, str]],
    accent: str,
) -> Path:
    width, height = 1440, 920
    image = Image.new("RGB", (width, height), color=(11, 27, 62))
    draw = ImageDraw.Draw(image)
    accent_rgb = hex_to_rgb(accent, (67, 184, 122))
    for y in range(height):
        blend = y / max(height - 1, 1)
        color = (
            int(11 + (18 - 11) * blend),
            int(27 + (39 - 27) * blend),
            int(62 + (86 - 62) * blend),
        )
        draw.line([(0, y), (width, y)], fill=color)
    title_font = load_font(52, bold=True)
    subtitle_font = load_font(28)
    label_font = load_font(30, bold=True)
    body_font = load_font(24)
    brand_font = load_font(24, bold=True)
    draw.text((84, 66), "同行资本 TH Capital", fill=(196, 209, 235), font=brand_font)
    current_y = 116
    for line in wrap_text(draw, title, title_font, width - 168)[:2]:
        draw.text((84, current_y), line, fill=(255, 255, 255), font=title_font)
        current_y += 64
    for line in wrap_text(draw, subtitle, subtitle_font, width - 168)[:2]:
        draw.text((84, current_y + 4), line, fill=(201, 214, 236), font=subtitle_font)
        current_y += 36

    cards = items[:4]
    columns = min(len(cards), 3) if cards else 1
    rows = 1 if len(cards) <= 3 else 2
    gap_x = 28
    gap_y = 28
    available_width = width - 168 - gap_x * (columns - 1)
    card_width = available_width // max(columns, 1)
    card_height = 220 if rows == 1 else 188
    start_y = 300
    for index, (label, desc) in enumerate(cards):
        row = index // columns
        col = index % columns
        left = 84 + col * (card_width + gap_x)
        top = start_y + row * (card_height + gap_y)
        right = left + card_width
        bottom = top + card_height
        draw.rounded_rectangle((left, top, right, bottom), radius=26, fill=(20, 40, 84), outline=(58, 87, 145), width=2)
        draw.rounded_rectangle((left + 24, top + 22, right - 24, top + 26), radius=2, fill=accent_rgb)
        text_y = top + 46
        for line in wrap_text(draw, label, label_font, card_width - 48)[:2]:
            draw.text((left + 24, text_y), line, fill=(255, 255, 255), font=label_font)
            text_y += 36
        text_y += 8
        for line in wrap_text(draw, desc or label, body_font, card_width - 48)[:4]:
            draw.text((left + 24, text_y), line, fill=(206, 218, 238), font=body_font)
            text_y += 30
    draw.rounded_rectangle((84, height - 112, width - 84, height - 58), radius=24, outline=(72, 103, 165), width=2)
    draw.text((112, height - 96), "根据正文关键信号自动整理，不替代原始事实截图", fill=(211, 220, 238), font=subtitle_font)
    image.save(output_path)
    return output_path


def slot_generation_text(slot: dict[str, str]) -> str:
    return " ".join(
        [
            slot.get("position", ""),
            slot.get("heading", ""),
            slot.get("job", ""),
            slot.get("note", ""),
            slot.get("requirements", ""),
            slot.get("preferred_asset", ""),
        ]
    ).lower()


def slot_is_signal_grid_like(slot: dict[str, str]) -> bool:
    text = slot_generation_text(slot)
    if slot_is_evidence_like(slot):
        return False
    if any(token in text for token in ["五层", "5层", "skill", "架构", "工作流", "workflow", "四步", "4步", "step"]):
        return False
    return any(token in text for token in ["约束识别", "关键信号", "四类", "四象限", "分类卡", "分类总结"])


def slot_is_layer_architecture_like(slot: dict[str, str]) -> bool:
    text = slot_generation_text(slot)
    if any(token in text for token in ["约束识别", "四类", "四象限", "分类卡", "分类总结"]):
        return False
    return any(token in text for token in ["五层", "5层", "架构", "层级"]) or (
        "skill" in text and any(token in text for token in ["结构", "分层", "链路"])
    )


def slot_is_workflow_cycle_like(slot: dict[str, str]) -> bool:
    text = slot_generation_text(slot)
    return any(token in text for token in ["workflow", "工作流", "循环", "四步", "4步", "step"])


def deterministic_slot_asset_kind(slot: dict[str, str]) -> str:
    if slot_is_signal_grid_like(slot):
        return "constraint-signal-card"
    if slot_is_layer_architecture_like(slot):
        return "layer-architecture-card"
    if slot_is_workflow_cycle_like(slot):
        return "workflow-cycle-card"
    return "slot-story-card"


def deterministic_slot_selection_reason(slot: dict[str, str]) -> str:
    asset_kind = deterministic_slot_asset_kind(slot)
    if asset_kind == "constraint-signal-card":
        return "根据正文约束识别段直接生成四类信号卡，替代容易出乱码的 AI 说明图。"
    if asset_kind == "layer-architecture-card":
        return "根据正文分层结构直接生成五层架构图，避免结构图退化成模板故事卡。"
    if asset_kind == "workflow-cycle-card":
        return "根据正文 workflow 段直接生成四步循环图，避免流程图挂错段或退化成摘要卡。"
    return "根据 slot 的位置、功能和制作要求自动生成结构图卡，服务正文理解。"


def summarize_heading_block(block_lines: list[str], max_chars: int = 34) -> str:
    plain_lines: list[str] = []
    list_items: list[str] = []
    for raw in block_lines:
        line = raw.strip()
        if not line or line.startswith("!["):
            continue
        bullet_match = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.*)$", line)
        if bullet_match:
            body = strip_markdown_inline(bullet_match.group(1))
            body = re.sub(r"^`([^`]+)`[:：]\s*", r"\1 ", body)
            body = body.replace("有没有", "").replace("会不会", "")
            if "：" in body:
                left, right = body.split("：", 1)
                body = left if len(left) <= 18 else f"{left} {right}"
            elif ":" in body:
                left, right = body.split(":", 1)
                body = left if len(left) <= 18 else f"{left} {right}"
            body = trim_text(clean_story_desc(body), 18)
            if body:
                list_items.append(body)
            continue
        plain = strip_markdown_inline(line)
        if plain:
            plain_lines.append(plain)
    joined_plain = " ".join(plain_lines)
    if list_items and any(token in joined_plain for token in ["只回答", "至少输出", "打 5 组分", "盯这四类", "比如"]):
        return " / ".join(list_items[:4])
    skip_fragments = ["这是最关键的一层", "这里要给系统明确的", "这些不是语言修辞", "最后才是概率", "比如"]
    for line in plain_lines:
        cleaned_line = clean_story_desc(line)
        if len(cleaned_line) < 10:
            continue
        if any(fragment in cleaned_line for fragment in skip_fragments):
            continue
        return trim_text(cleaned_line, max_chars)
    if list_items:
        return " / ".join(list_items[:4])
    return trim_text(strip_markdown_inline(joined_plain), max_chars)


def extract_heading_sequence(
    pack: DraftPack,
    pattern: re.Pattern[str],
    limit: int,
) -> list[tuple[str, str, str]]:
    markdown_path = primary_markdown_path(pack)
    if markdown_path is None or not markdown_path.exists():
        return []
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    items: list[tuple[str, str, str]] = []
    current_tag = ""
    current_title = ""
    block_lines: list[str] = []

    def flush() -> None:
        if not current_title:
            return
        summary = summarize_heading_block(block_lines)
        items.append((current_tag, current_title, summary or current_title))

    for raw in lines:
        heading_match = pattern.match(raw.strip())
        if heading_match:
            flush()
            current_tag = clean(heading_match.group(1), "")
            current_title = clean(heading_match.group(2), "")
            block_lines = []
            continue
        if current_title and MARKDOWN_HEADING_RE.match(raw.strip()):
            flush()
            current_tag = ""
            current_title = ""
            block_lines = []
            continue
        if current_title:
            block_lines.append(raw)
    flush()
    return items[:limit]


def draw_arrow_segment(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    *,
    fill: tuple[int, int, int],
    width: int = 6,
    arrow_size: int = 16,
) -> None:
    draw.line([start, end], fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (
        end[0] - arrow_size * math.cos(angle) + arrow_size * 0.55 * math.sin(angle),
        end[1] - arrow_size * math.sin(angle) - arrow_size * 0.55 * math.cos(angle),
    )
    right = (
        end[0] - arrow_size * math.cos(angle) - arrow_size * 0.55 * math.sin(angle),
        end[1] - arrow_size * math.sin(angle) + arrow_size * 0.55 * math.cos(angle),
    )
    draw.polygon([end, left, right], fill=fill)


def create_constraint_signal_card(output_path: Path, pack: DraftPack, slot: dict[str, str], accent: str) -> Path:
    section = best_section_for_slot(slot, pack)
    items = extract_story_items_from_text(section, limit=4) if section is not None else []
    if not items:
        fallback_points = extract_slot_points_from_plan(slot, pack, limit=4)
        items = [(f"要点 {index}", point) for index, point in enumerate(fallback_points, start=1)]

    width, height = 1600, 980
    image = Image.new("RGB", (width, height), color=(245, 248, 252))
    draw = ImageDraw.Draw(image)
    for y in range(height):
        blend = y / max(height - 1, 1)
        color = (
            int(245 + (255 - 245) * blend),
            int(248 + (252 - 248) * blend),
            int(252 + (255 - 252) * blend),
        )
        draw.line([(0, y), (width, y)], fill=color)
    for x in range(0, width, 72):
        draw.line([(x, 0), (x, height)], fill=(236, 241, 247), width=1)
    for y in range(0, height, 72):
        draw.line([(0, y), (width, y)], fill=(236, 241, 247), width=1)

    accent_rgb = hex_to_rgb(accent, (26, 173, 25))
    title_font = load_font(58, bold=True)
    subtitle_font = load_font(28)
    label_font = load_font(34, bold=True)
    body_font = load_font(24)
    chip_font = load_font(22, bold=True)
    kicker_font = load_font(24, bold=True)

    title = "约束识别：四类关键信号"
    subtitle = "不是盯特朗普今天有多凶，而是盯哪些现实约束开始把他往回推。"
    draw.text((88, 72), "TACO 方法图｜约束层", fill=accent_rgb, font=kicker_font)
    cursor_y = 118
    for line in wrap_text(draw, title, title_font, width - 176)[:2]:
        draw.text((88, cursor_y), line, fill=(18, 31, 53), font=title_font)
        cursor_y += 68
    for line in wrap_text(draw, subtitle, subtitle_font, width - 176)[:2]:
        draw.text((88, cursor_y), line, fill=(90, 105, 128), font=subtitle_font)
        cursor_y += 38

    card_colors = [
        ((235, 243, 255), (61, 103, 198)),
        ((232, 246, 241), (59, 180, 141)),
        ((255, 244, 228), (239, 161, 62)),
        ((252, 236, 241), (233, 99, 122)),
    ]
    columns = 2
    rows = 2
    gap_x = 30
    gap_y = 30
    card_width = (width - 176 - gap_x) // columns
    card_height = 250
    start_y = 298
    for index, (label, desc) in enumerate(items[:4]):
        row = index // columns
        col = index % columns
        left = 88 + col * (card_width + gap_x)
        top = start_y + row * (card_height + gap_y)
        right = left + card_width
        bottom = top + card_height
        fill_color, line_color = card_colors[index % len(card_colors)]
        draw.rounded_rectangle((left, top, right, bottom), radius=30, fill=fill_color, outline=line_color, width=3)
        chip_width = 58
        draw.rounded_rectangle((left + 24, top + 22, left + 24 + chip_width, top + 62), radius=18, fill=line_color)
        draw.text((left + 40, top + 31), f"{index + 1:02d}", fill=(255, 255, 255), font=chip_font)
        title_y = top + 84
        cleaned_label = trim_text(clean_story_label(label), 14)
        for line in wrap_text(draw, cleaned_label, label_font, card_width - 48)[:2]:
            draw.text((left + 24, title_y), line, fill=(19, 32, 54), font=label_font)
            title_y += 40
        desc_text = compact_editorial_desc(desc or label, 34)
        body_y = title_y + 8
        for line in wrap_text(draw, desc_text, body_font, card_width - 48)[:4]:
            draw.text((left + 24, body_y), line, fill=(86, 101, 125), font=body_font)
            body_y += 30

    footer = "判断 TACO，不是看语气，而是看成本曲线有没有开始逼出让步。"
    draw.rounded_rectangle((88, height - 124, width - 88, height - 70), radius=26, fill=(243, 248, 253), outline=(214, 224, 238), width=2)
    draw.text((116, height - 108), footer, fill=(73, 90, 115), font=subtitle_font)
    image.save(output_path)
    return output_path


def create_layer_architecture_card(output_path: Path, pack: DraftPack, accent: str) -> Path:
    items = extract_heading_sequence(pack, re.compile(r"^###\s*第\s*(\d+)\s*层[：:]\s*(.+?)\s*$"), limit=5)
    if not items:
        items = [
            ("1", "事件识别层", "先归并事件对象，再分清口头表态和真实动作"),
            ("2", "约束识别层", "盯市场反噬、内部松动、口风软化、核心利益受损"),
            ("3", "让步触发器层", "捕捉从强硬话术切向缓和口风的转折"),
            ("4", "叙事一致性层", "判断他有没有体面退场的叙事出口"),
            ("5", "概率输出层", "最后才给 TACO 概率和明日观察点"),
        ]

    width, height = 1600, 1080
    image = Image.new("RGB", (width, height), color=(244, 248, 253))
    draw = ImageDraw.Draw(image)
    for y in range(height):
        blend = y / max(height - 1, 1)
        color = (
            int(244 + (255 - 244) * blend),
            int(248 + (252 - 248) * blend),
            int(253 + (255 - 253) * blend),
        )
        draw.line([(0, y), (width, y)], fill=color)
    accent_rgb = hex_to_rgb(accent, (15, 76, 129))
    draw.rounded_rectangle((56, 42, width - 56, height - 42), radius=34, outline=(200, 216, 236), width=3)

    kicker_font = load_font(24, bold=True)
    title_font = load_font(58, bold=True)
    subtitle_font = load_font(28)
    chip_font = load_font(22, bold=True)
    label_font = load_font(32, bold=True)
    body_font = load_font(23)

    draw.text((92, 72), "TACO 方法图｜五层架构", fill=accent_rgb, font=kicker_font)
    cursor_y = 116
    title = "TACO 预测 skill 五层架构"
    subtitle = "先识别事件，再识别约束、触发器和叙事出口，最后才给概率。"
    for line in wrap_text(draw, title, title_font, width - 184)[:2]:
        draw.text((92, cursor_y), line, fill=(18, 31, 53), font=title_font)
        cursor_y += 70
    for line in wrap_text(draw, subtitle, subtitle_font, width - 184)[:2]:
        draw.text((92, cursor_y), line, fill=(82, 98, 122), font=subtitle_font)
        cursor_y += 40

    layer_colors = [
        ((230, 240, 255), (56, 99, 187)),
        ((223, 244, 240), (37, 128, 105)),
        ((255, 239, 217), (214, 126, 40)),
        ((248, 229, 237), (185, 85, 116)),
        ((232, 236, 248), (81, 96, 155)),
    ]
    base_left = 168
    box_width = width - 336
    box_height = 118
    gap = 22
    start_y = 262
    for index, (tag, layer_title, layer_desc) in enumerate(items[:5]):
        top = start_y + index * (box_height + gap)
        left = base_left + (4 - min(index, 4)) * 28
        right = left + box_width - (4 - min(index, 4)) * 56
        bottom = top + box_height
        fill_color, border_color = layer_colors[index % len(layer_colors)]
        draw.rounded_rectangle((left, top, right, bottom), radius=28, fill=fill_color, outline=border_color, width=3)
        chip_label = f"L{tag}"
        chip_width = int(draw.textlength(chip_label, font=chip_font) + 42)
        draw.rounded_rectangle((left + 24, top + 20, left + 24 + chip_width, top + 58), radius=18, fill=border_color)
        draw.text((left + 44, top + 29), chip_label, fill=(255, 255, 255), font=chip_font)
        draw.text((left + 24, top + 70), trim_text(layer_title, 18), fill=(19, 32, 54), font=label_font)
        desc_x = left + 360
        wrapped_desc = wrap_text(draw, compact_editorial_desc(layer_desc, 42), body_font, right - desc_x - 28)[:2]
        for line_index, line in enumerate(wrapped_desc):
            draw.text((desc_x, top + 38 + line_index * 30), line, fill=(66, 82, 107), font=body_font)
        if index < min(len(items), 5) - 1:
            center_x = width // 2
            draw_arrow_segment(draw, (center_x, bottom + 6), (center_x, bottom + gap - 4), fill=border_color, width=5, arrow_size=14)

    footer = "不是先问今天几成，而是先问：事件、约束、trigger、叙事出口，哪一层变了。"
    draw.text((92, height - 96), footer, fill=(92, 106, 130), font=kicker_font)
    image.save(output_path)
    return output_path


def create_workflow_cycle_card(output_path: Path, pack: DraftPack, accent: str) -> Path:
    items = extract_heading_sequence(pack, re.compile(r"^###\s*Step\s*(\d+)\s*[：:]\s*(.+?)\s*$", re.I), limit=4)
    if not items:
        items = [
            ("1", "抓原始输入", "抓特朗普表态、白宫口风、市场反馈和外部压力"),
            ("2", "做事件归并", "把一天噪音归并成同一个 Trump 风险事件"),
            ("3", "跑 TACO 评分", "评估口头强硬、真实动作、市场痛感、退路和约束"),
            ("4", "输出结论", "写清概率变化原因、两个新 trigger 和明日观察点"),
        ]
    normalized_items: list[tuple[str, str, str]] = []
    for tag, step_title, step_desc in items[:4]:
        cleaned_desc = step_desc
        lowered_title = step_title.lower()
        if "评分" in step_title:
            cleaned_desc = "给每个事件打 5 组分，再合成 TACO 概率。"
        elif "输出" in step_title:
            cleaned_desc = "输出核心事件、变化原因、新 trigger 和明日观察点。"
        elif "归并" in step_title:
            cleaned_desc = "把一天噪音收束成同一个 Trump 风险事件。"
        elif "输入" in step_title or "抓" in lowered_title:
            cleaned_desc = "抓表态、口风、市场反馈和外部压力四类输入。"
        normalized_items.append((tag, step_title, cleaned_desc))
    items = normalized_items

    width, height = 1600, 980
    image = Image.new("RGB", (width, height), color=(246, 249, 253))
    draw = ImageDraw.Draw(image)
    for y in range(height):
        blend = y / max(height - 1, 1)
        color = (
            int(246 + (255 - 246) * blend),
            int(249 + (252 - 249) * blend),
            int(253 + (255 - 253) * blend),
        )
        draw.line([(0, y), (width, y)], fill=color)
    accent_rgb = hex_to_rgb(accent, (15, 76, 129))
    draw.rounded_rectangle((56, 42, width - 56, height - 42), radius=34, outline=(200, 216, 236), width=3)

    kicker_font = load_font(24, bold=True)
    title_font = load_font(56, bold=True)
    subtitle_font = load_font(28)
    chip_font = load_font(22, bold=True)
    label_font = load_font(32, bold=True)
    body_font = load_font(24)
    center_font = load_font(26, bold=True)

    draw.text((92, 72), "TACO 方法图｜每日循环", fill=accent_rgb, font=kicker_font)
    cursor_y = 116
    title = "TACO 预测 4 步 workflow"
    subtitle = "每天循环刷新一次，让判断从情绪反应变成稳定流程。"
    for line in wrap_text(draw, title, title_font, width - 184)[:2]:
        draw.text((92, cursor_y), line, fill=(18, 31, 53), font=title_font)
        cursor_y += 68
    for line in wrap_text(draw, subtitle, subtitle_font, width - 184)[:2]:
        draw.text((92, cursor_y), line, fill=(82, 98, 122), font=subtitle_font)
        cursor_y += 40

    positions = [
        (150, 296, 650, 496),
        (950, 296, 1450, 496),
        (950, 624, 1450, 824),
        (150, 624, 650, 824),
    ]
    card_colors = [
        ((229, 239, 255), (56, 99, 187)),
        ((223, 244, 240), (37, 128, 105)),
        ((255, 239, 217), (214, 126, 40)),
        ((248, 229, 237), (185, 85, 116)),
    ]
    centers = []
    for index, (tag, step_title, step_desc) in enumerate(items[:4]):
        left, top, right, bottom = positions[index]
        fill_color, border_color = card_colors[index]
        draw.rounded_rectangle((left, top, right, bottom), radius=30, fill=fill_color, outline=border_color, width=3)
        chip_label = f"STEP {tag}"
        chip_width = int(draw.textlength(chip_label, font=chip_font) + 42)
        draw.rounded_rectangle((left + 24, top + 20, left + 24 + chip_width, top + 58), radius=18, fill=border_color)
        draw.text((left + 42, top + 29), chip_label, fill=(255, 255, 255), font=chip_font)
        text_y = top + 78
        for line in wrap_text(draw, trim_text(step_title, 18), label_font, right - left - 48)[:2]:
            draw.text((left + 24, text_y), line, fill=(18, 31, 53), font=label_font)
            text_y += 40
        for line in wrap_text(draw, trim_text(step_desc, 40), body_font, right - left - 48)[:3]:
            draw.text((left + 24, text_y + 6), line, fill=(68, 84, 107), font=body_font)
            text_y += 32
        centers.append(((left + right) // 2, (top + bottom) // 2))

    center_x, center_y = width // 2, 560
    draw.ellipse((center_x - 98, center_y - 98, center_x + 98, center_y + 98), fill=(18, 42, 88), outline=(67, 111, 196), width=4)
    draw.text((center_x - 52, center_y - 18), "每日", fill=(255, 255, 255), font=center_font)
    draw.text((center_x - 52, center_y + 18), "刷新", fill=(255, 255, 255), font=center_font)

    arrow_points = [
        ((650, 396), (950, 396)),
        ((1200, 496), (1200, 624)),
        ((950, 724), (650, 724)),
        ((400, 624), (400, 496)),
    ]
    for start, end in arrow_points:
        draw_arrow_segment(draw, start, end, fill=accent_rgb, width=6, arrow_size=16)

    footer = "把输入、归并、评分、结论四步跑顺，你每天看到的就不再只是 headline。"
    draw.text((92, height - 96), footer, fill=(92, 106, 130), font=kicker_font)
    image.save(output_path)
    return output_path


def create_slot_story_card(output_path: Path, pack: DraftPack, slot: dict[str, str], accent: str) -> Path:
    if slot_is_layer_architecture_like(slot):
        return create_layer_architecture_card(output_path, pack, accent)
    if slot_is_workflow_cycle_like(slot):
        return create_workflow_cycle_card(output_path, pack, accent)
    if slot_is_signal_grid_like(slot):
        return create_constraint_signal_card(output_path, pack, slot, accent)

    width, height = 1440, 960
    section = best_section_for_slot(slot, pack)
    story_items = extract_story_items_from_text(section, limit=4) if section is not None else []
    if not story_items:
        fallback_points = extract_slot_points_from_plan(slot, pack, limit=3)
        story_items = [(f"要点 {index}", point) for index, point in enumerate(fallback_points, start=1)]
    title = derive_slot_title(slot, pack)
    style = story_style_from_items(slot, section, story_items)
    section_title = normalize_visual_phrase(section.get("title", ""), 28) if section is not None else ""
    if style == "stage-flow":
        subtitle = trim_text(f"{section_title or title} 这一节的关键结构，一张图看懂", 34)
    elif style == "signal-grid":
        subtitle = trim_text(f"{section_title or title}里最值得记住的 {len(story_items[:4])} 个信号", 34)
    else:
        subtitle = derive_slot_subtitle(slot, pack)
    if style == "stage-flow":
        return create_stage_flow_card(output_path, title, subtitle, story_items, accent)
    if style == "signal-grid":
        return create_signal_grid_card(output_path, title, subtitle, story_items, accent)

    image = Image.new("RGB", (width, height), color=(241, 246, 252))
    draw = ImageDraw.Draw(image)
    accent_rgb = hex_to_rgb(accent, (59, 130, 246))
    for y in range(height):
        blend = y / max(height - 1, 1)
        color = (
            int(241 + (252 - 241) * blend),
            int(246 + (250 - 246) * blend),
            int(252 + (255 - 252) * blend),
        )
        draw.line([(0, y), (width, y)], fill=color)
    draw.rounded_rectangle((44, 34, width - 44, height - 34), radius=32, outline=(200, 216, 236), width=3)
    kicker_font = load_font(24, bold=True)
    title_font = load_font(56, bold=True)
    subtitle_font = load_font(28)
    step_font = load_font(22, bold=True)
    body_font = load_font(30)

    draw.text((84, 74), f"{slot_kind_label(slot)}｜核心脉络", fill=accent_rgb, font=kicker_font)
    cursor_y = 116
    for line in wrap_text(draw, title, title_font, width - 168)[:2]:
        draw.text((84, cursor_y), line, fill=(24, 35, 52), font=title_font)
        cursor_y += 70
    for line in wrap_text(draw, subtitle, subtitle_font, width - 168)[:2]:
        draw.text((84, cursor_y + 8), line, fill=(88, 104, 128), font=subtitle_font)
        cursor_y += 40

    block_top = 306
    block_height = 170
    while len(story_items) < 3:
        story_items.append((f"要点 {len(story_items) + 1}", trim_text(pack.core_judgment, 32)))
    for index, (label, desc) in enumerate(story_items[:3], start=1):
        top = block_top + (index - 1) * 208
        box = (84, top, width - 84, top + block_height)
        fill = (255, 255, 255) if index < 3 else (254, 247, 236)
        draw.rounded_rectangle(box, radius=26, fill=fill, outline=(205, 220, 238), width=2)
        chip_color = accent_rgb if index < 3 else (46, 134, 115)
        draw.rounded_rectangle((112, top + 26, 302, top + 72), radius=23, fill=chip_color)
        draw.text((136, top + 36), clean_story_label(label) or f"要点 {index}", fill=(255, 255, 255), font=step_font)
        text_y = top + 92
        for line in wrap_text(draw, desc or label, body_font, width - 220)[:3]:
            draw.text((112, text_y), line, fill=(32, 43, 60), font=body_font)
            text_y += 38
        if index < 3:
            arrow_y = top + block_height + 8
            center_x = width // 2
            draw.line([(center_x, arrow_y), (center_x, arrow_y + 28)], fill=accent_rgb, width=6)
            draw.polygon(
                [(center_x, arrow_y + 40), (center_x - 16, arrow_y + 18), (center_x + 16, arrow_y + 18)],
                fill=accent_rgb,
            )
    draw.text((84, 902), "根据正文对应章节信息自动整理", fill=(103, 116, 141), font=kicker_font)
    image.save(output_path)
    return output_path


def split_markdown_table_row(line: str) -> list[str]:
    raw = line.strip().strip("|")
    return [clean(re.sub(r"[*_`]+", "", cell.strip()), "") for cell in raw.split("|")]


def extract_markdown_tables(markdown: str) -> list[dict[str, list[list[str]] | list[str]]]:
    lines = markdown.splitlines()
    tables: list[dict[str, list[list[str]] | list[str]]] = []
    index = 0
    while index + 1 < len(lines):
        header_line = lines[index].strip()
        separator_line = lines[index + 1].strip()
        if "|" not in header_line or "|" not in separator_line:
            index += 1
            continue
        if not re.match(r"^\|?(?:\s*:?-{3,}:?\s*\|)+\s*:?-{3,}:?\s*\|?$", separator_line):
            index += 1
            continue
        headers = split_markdown_table_row(header_line)
        rows: list[list[str]] = []
        cursor = index + 2
        while cursor < len(lines):
            row_line = lines[cursor].strip()
            if "|" not in row_line or row_line.startswith("!["):
                break
            row = split_markdown_table_row(row_line)
            if len(row) == len(headers):
                rows.append(row)
            cursor += 1
        if headers and rows:
            tables.append({"headers": headers, "rows": rows})
        index = cursor
    return tables


def parse_numeric_value(value: str) -> float | None:
    raw = clean(value, "")
    if not raw:
        return None
    if re.fullmatch(r"\d+\s*/\s*\d+", raw):
        numerator, denominator = [int(part.strip()) for part in raw.split("/", 1)]
        return round(numerator / max(denominator, 1), 6)
    numeric_with_units = re.fullmatch(
        r"[$￥€]?\s*-?\d[\d,]*(?:\.\d+)?\s*(?:%|USD|usd|万美元|亿美元|百万|亿|万|倍|x|X)?",
        raw,
    )
    if re.search(r"[A-Za-z\u4e00-\u9fff]", raw) and not numeric_with_units:
        return None
    candidate = raw.replace(",", "").replace("$", "").replace("USD", "").replace("%", "").strip()
    match = re.search(r"-?\d+(?:\.\d+)?", candidate)
    if not match:
        return None
    try:
        return float(match.group(0))
    except ValueError:
        return None


def choose_best_table_for_slot(slot: dict[str, str], markdown: str) -> dict[str, list[list[str]] | list[str]] | None:
    slot_text = " ".join([slot.get("heading", ""), slot.get("job", ""), slot.get("note", ""), slot.get("requirements", "")]).lower()
    best_table: dict[str, list[list[str]] | list[str]] | None = None
    best_score = -1
    for table in extract_markdown_tables(markdown):
        headers = table.get("headers") or []
        rows = table.get("rows") or []
        numeric_headers = [header for index, header in enumerate(headers) if any(parse_numeric_value(row[index]) is not None for row in rows)]
        if len(rows) < 2 or not numeric_headers:
            continue
        score = len(numeric_headers) * 3 + min(len(rows), 8)
        lowered_headers = " ".join(headers).lower()
        if "成本" in slot_text and "成本" in lowered_headers:
            score += 4
        if any(token in slot_text for token in ["评分", "benchmark", "得分"]) and any(token in lowered_headers for token in ["评分", "score"]):
            score += 4
        if any(token in slot_text for token in ["比值", "ratio"]) and any(token in lowered_headers for token in ["比", "ratio"]):
            score += 5
        if score > best_score:
            best_score = score
            best_table = table
    return best_table


def choose_chart_headers(slot: dict[str, str], headers: list[str], rows: list[list[str]]) -> tuple[int, list[int]]:
    numeric_indices = [index for index, _ in enumerate(headers) if any(parse_numeric_value(row[index]) is not None for row in rows)]
    label_index = 0
    for index in range(len(headers)):
        if index not in numeric_indices:
            label_index = index
            break
    slot_text = " ".join([slot.get("heading", ""), slot.get("job", ""), slot.get("requirements", "")]).lower()
    preferred: list[int] = []
    for keyword in ("评分/成本比", "评分成本比", "ratio"):
        for index, header in enumerate(headers):
            if keyword in header.lower():
                preferred.append(index)
    if any(token in slot_text for token in ["成本", "score", "评分", "benchmark"]):
        for keyword in ("评分", "score", "cost", "成本"):
            for index, header in enumerate(headers):
                if keyword in header.lower() and index in numeric_indices and index not in preferred:
                    preferred.append(index)
    for index in numeric_indices:
        if index not in preferred:
            preferred.append(index)
    return label_index, preferred[:2] or numeric_indices[:1]


def highlight_label_from_pack(pack: DraftPack, labels: list[str]) -> str:
    signals = " ".join([pack.topic_title, pack.approved_angle, pack.core_judgment]).lower()
    for label in labels:
        normalized = clean(label, "").lower()
        if normalized and normalized in signals:
            return label
    return labels[0] if labels else ""


def create_data_comparison_card(output_path: Path, pack: DraftPack, slot: dict[str, str], accent: str) -> Path | None:
    wechat_path = clean(pack.paths.get("wechat_path", "n/a"), "")
    if not wechat_path or wechat_path == "n/a":
        return None
    markdown_path = resolve_doc_path(wechat_path)
    if not markdown_path.exists():
        return None
    markdown = markdown_path.read_text(encoding="utf-8")
    table = choose_best_table_for_slot(slot, markdown)
    if table is None:
        return None
    headers = list(table.get("headers") or [])
    rows = list(table.get("rows") or [])
    label_index, metric_indices = choose_chart_headers(slot, headers, rows)
    if not metric_indices:
        return None

    width, height = 1600, 980
    image = Image.new("RGB", (width, height), color=(245, 248, 253))
    draw = ImageDraw.Draw(image)
    accent_rgb = hex_to_rgb(accent, (34, 197, 94))
    for y in range(height):
        blend = y / max(height - 1, 1)
        color = (
            int(245 + (255 - 245) * blend),
            int(248 + (252 - 248) * blend),
            int(253 + (255 - 253) * blend),
        )
        draw.line([(0, y), (width, y)], fill=color)
    draw.rounded_rectangle((48, 40, width - 48, height - 40), radius=30, outline=(203, 216, 235), width=3)

    kicker_font = load_font(24, bold=True)
    title_font = load_font(52, bold=True)
    subtitle_font = load_font(26)
    label_font = load_font(24, bold=True)
    value_font = load_font(20, bold=True)
    row_font = load_font(24)

    draw.text((92, 82), "数据图｜正文表格自动转图", fill=accent_rgb, font=kicker_font)
    highlight_label = highlight_label_from_pack(pack, [row[label_index] for row in rows])
    metric_names = [headers[index] for index in metric_indices]
    section = best_section_for_slot(slot, pack)
    section_title = normalize_visual_phrase(section.get("title", ""), 24) if section is not None else ""
    if section_title:
        metric_label = " / ".join(metric_names[:2]) if metric_names else "关键指标"
        title = trim_text(f"{section_title}：{metric_label}", 30)
    elif len(metric_names) >= 2:
        title = trim_text(f"{highlight_label} 与主流模型的 {metric_names[0]} / {metric_names[1]} 对比", 32)
    elif metric_names:
        title = trim_text(f"{highlight_label} 与主流模型的 {metric_names[0]} 对比", 32)
    else:
        title = derive_slot_title(slot, pack)
    subtitle = section_title
    if not subtitle:
        subtitle = derive_slot_subtitle(slot, pack)
    cursor_y = 118
    for line in wrap_text(draw, title, title_font, width - 184)[:2]:
        draw.text((92, cursor_y), line, fill=(20, 32, 49), font=title_font)
        cursor_y += 68
    for line in wrap_text(draw, subtitle, subtitle_font, width - 184)[:2]:
        draw.text((92, cursor_y), line, fill=(92, 107, 129), font=subtitle_font)
        cursor_y += 38

    labels = [row[label_index] for row in rows]
    panel_gap = 42
    panel_width = (width - 92 * 2 - panel_gap * max(len(metric_indices) - 1, 0)) // max(len(metric_indices), 1)
    chart_top = 286
    chart_height = 550
    for panel_idx, metric_index in enumerate(metric_indices):
        left = 92 + panel_idx * (panel_width + panel_gap)
        right = left + panel_width
        draw.rounded_rectangle((left, chart_top, right, chart_top + chart_height), radius=24, fill=(255, 255, 255), outline=(214, 224, 239), width=2)
        header = headers[metric_index]
        draw.text((left + 26, chart_top + 24), trim_text(header, 20), fill=accent_rgb, font=label_font)
        numeric_rows: list[tuple[str, str, float]] = []
        for row in rows[:8]:
            value = parse_numeric_value(row[metric_index])
            if value is None:
                continue
            numeric_rows.append((row[label_index], row[metric_index], value))
        if not numeric_rows:
            continue
        max_value = max(item[2] for item in numeric_rows) or 1.0
        row_gap = 60
        start_y = chart_top + 82
        max_label_width = max(draw.textlength(trim_text(label, 14), font=row_font) for label, _, _ in numeric_rows)
        bar_left = int(left + 28 + max_label_width + 28)
        bar_right = right - 28
        for row_index, (label, raw_value, value) in enumerate(numeric_rows):
            y = start_y + row_index * row_gap
            is_highlight = clean(label, "").lower() == clean(highlight_label, "").lower()
            draw.text((left + 26, y), trim_text(label, 14), fill=(23, 34, 49), font=row_font)
            draw.rounded_rectangle((bar_left, y + 10, bar_right, y + 34), radius=12, fill=(231, 237, 245))
            fill_right = bar_left + int((bar_right - bar_left) * (value / max_value))
            fill_color = accent_rgb if is_highlight else (91, 124, 173)
            draw.rounded_rectangle((bar_left, y + 10, max(fill_right, bar_left + 12), y + 34), radius=12, fill=fill_color)
            value_x = min(max(fill_right + 10, bar_left + 8), bar_right - 90)
            draw.text((value_x, y + 38), raw_value, fill=fill_color, font=value_font)
    footer = "图表由正文表格自动生成，请以文中原表及来源说明为准。"
    draw.text((92, 900), footer, fill=(102, 116, 141), font=kicker_font)
    image.save(output_path)
    return output_path


def ai_image_prompt(pack: DraftPack, slot: dict[str, str]) -> str:
    return (
        "Create a clean editorial explainer image for a Chinese technology and capital-markets article. "
        "This image is only for structural explanation, not for factual proof. "
        "Do not imitate screenshots, do not include fake UIs, do not include brand logos or watermarks, "
        "do not pretend to be a real press photo. "
        f"Topic: {pack.topic_title}. "
        f"Approved angle: {pack.approved_angle}. "
        f"Visual job: {slot.get('job', 'structure explanation')}. "
        f"Reader note: {slot.get('note', '')}. "
        "Style: modern editorial infographic, light background with strong mid-to-dark contrast, clearly visible geometry, "
        "clearly visible arrows / blocks / labels area, centered composition, generous whitespace, high readability. "
        "Avoid washed-out pastel elements, avoid almost-white strokes, avoid empty abstract wallpaper. "
        "Use visible slate / teal / blue-gray accents so the graphic remains legible inside a longform article preview. "
        "Suitable for WeChat/Zhihu/Baijiahao longform articles."
    )


def generate_minimax_image(output_path: Path, prompt: str) -> tuple[Path, str]:
    api_key, auth_source = load_minimax_api_key()
    payload = {
        "model": os.getenv("TH_MARKET_MINIMAX_IMAGE_MODEL", MINIMAX_IMAGE_MODEL_DEFAULT),
        "prompt": prompt,
        "aspect_ratio": os.getenv("TH_MARKET_MINIMAX_IMAGE_ASPECT_RATIO", MINIMAX_IMAGE_ASPECT_RATIO_DEFAULT),
        "response_format": "base64",
        "prompt_optimizer": os.getenv("TH_MARKET_MINIMAX_PROMPT_OPTIMIZER", "false").lower() == "true",
        "aigc_watermark": False,
    }
    request = Request(
        MINIMAX_IMAGE_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            **HTTP_HEADERS,
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with open_request(request, timeout=180) as response:
        body = json.loads(response.read().decode("utf-8", "ignore"))
    images = (((body or {}).get("data") or {}).get("image_base64") or [])
    if not images:
        raise RuntimeError(f"MiniMax image response missing image_base64 ｜ {clean(json.dumps(body, ensure_ascii=False), '')}")
    output_path.write_bytes(base64.b64decode(images[0]))
    return output_path, auth_source


def generate_openai_image(output_path: Path, prompt: str) -> Path:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY missing")
    payload = {
        "model": os.getenv("TH_MARKET_AI_IMAGE_MODEL", "gpt-image-1"),
        "prompt": prompt,
        "size": os.getenv("TH_MARKET_AI_IMAGE_SIZE", "1536x1024"),
        "quality": os.getenv("TH_MARKET_AI_IMAGE_QUALITY", "low"),
    }
    request = Request(
        OPENAI_IMAGE_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            **HTTP_HEADERS,
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with open_request(request, timeout=90) as response:
        body = json.loads(response.read().decode("utf-8", "ignore"))
    first = (body.get("data") or [{}])[0]
    b64_payload = first.get("b64_json")
    if b64_payload:
        output_path.write_bytes(base64.b64decode(b64_payload))
        return output_path
    image_url = clean(str(first.get("url", "")), "")
    if image_url:
        return download_image(image_url, output_path)
    raise RuntimeError("OpenAI image response missing b64_json/url")


def generate_ai_image(output_path: Path, prompt: str) -> tuple[Path, str, str]:
    minimax_error = ""
    try:
        image_path, auth_source = generate_minimax_image(output_path, prompt)
        return image_path, "minimax-image-01", auth_source
    except Exception as error:
        minimax_error = clean(str(error), "")
    try:
        image_path = generate_openai_image(output_path, prompt)
        return image_path, "openai-gpt-image-1", "env:OPENAI_API_KEY"
    except Exception as error:
        openai_error = clean(str(error), "")
    raise RuntimeError(
        f"MiniMax unavailable: {minimax_error or 'unknown'}; OpenAI unavailable: {openai_error or 'unknown'}"
    )


def materialize_external_safe_assets(
    pack: DraftPack,
    asset_dir: Path,
    remaining: int,
    used_urls: set[str],
    has_primary_visuals: bool,
) -> tuple[list[Path], list[dict[str, str | bool]], list[str]]:
    if remaining <= 0:
        return [], [], []
    max_external = 0 if has_primary_visuals else min(1, remaining)
    if max_external <= 0:
        return [], [], []
    slots = parse_visual_slots(pack)
    queries = build_external_search_queries(pack, slots)
    entity_phrases, entity_tokens, concept_tokens = pack_entity_signals(pack, slots)
    assets: list[Path] = []
    entries: list[dict[str, str | bool]] = []
    failures: list[str] = []
    used_image_urls: set[str] = set()
    slot_text = " ".join(slot.get("job", "") for slot in slots)
    for query in queries:
        if len(assets) >= max_external:
            break
        try:
            candidates = wikimedia_commons_candidates(query, limit=4)
        except Exception as error:
            failures.append(f"external search failed for {query} ｜ {clean(str(error), '')}")
            continue
        if not candidates:
            continue
        for candidate in candidates:
            if len(assets) >= max_external:
                break
            if candidate.image_url in used_image_urls or candidate.image_url in used_urls or candidate.landing_url in used_urls:
                continue
            if not external_candidate_allowed(
                pack,
                candidate,
                query,
                entity_phrases,
                entity_tokens,
                concept_tokens,
                has_primary_visuals=has_primary_visuals,
            ):
                failures.append(
                    f"{query} ｜ filtered low-relevance candidate ｜ {candidate.title} ｜ {candidate.landing_url or candidate.image_url}"
                )
                continue
            output_base = asset_dir / f"{60 + len(assets):02d}__external_{slugify_text(candidate.title)}"
            try:
                downloaded_path = download_image(candidate.image_url, output_base)
            except Exception as error:
                failures.append(f"{candidate.query} ｜ {candidate.image_url} ｜ {clean(str(error), '')}")
                continue
            used_image_urls.add(candidate.image_url)
            assets.append(downloaded_path)
            selection_reason = (
                f"Wikimedia Commons 开放许可补图（query={candidate.query}；license={candidate.license_name}"
                f"{f'；creator={candidate.creator}' if candidate.creator else ''}）。"
            )
            entries.append(
                manifest_entry(
                    path=downloaded_path,
                    status="approved",
                    asset_kind="external-safe-image",
                    selection_reason=selection_reason,
                    source_url=candidate.landing_url or candidate.image_url,
                    source_class="external-open-license",
                    preview=True,
                    source_title=candidate.title,
                    search_query=candidate.query,
                    creator=candidate.creator,
                    license=candidate.license_name,
                    slot_hint=slot_text,
                )
            )
    return assets, entries, failures


def materialize_ai_explainer_assets(
    pack: DraftPack,
    asset_dir: Path,
    remaining: int,
    accent: str,
    primary_assets: list[Path] | None = None,
    primary_asset_kinds: dict[str, str] | None = None,
) -> tuple[list[Path], list[dict[str, str | bool]], list[str], list[dict[str, str]]]:
    slots = parse_visual_slots(pack)
    assets: list[Path] = []
    entries: list[dict[str, str | bool]] = []
    failures: list[str] = []
    slot_map: list[dict[str, str]] = []
    reusable_primary = list(primary_assets or [])
    primary_kind_map = primary_asset_kinds or {}
    allow_ai_fallback = os.getenv("TH_MARKET_ENABLE_AI_VISUAL_FALLBACK", "false").lower() == "true"
    seen_slot_signatures: set[str] = set()

    has_cover_slot = any(slot_is_cover_like(slot) for slot in slots)
    if not has_cover_slot:
        synthetic_cover_slot = {
            "slot": "cover_auto",
            "heading": "封面图",
            "job": "封面图",
            "platform": preferred_visual_platform(pack),
        }
        cover_path = asset_dir / "00__cover.png"
        created_cover = create_headline_cover_card(cover_path, pack, synthetic_cover_slot, accent)
        assets.append(created_cover)
        entries.append(
            manifest_entry(
                path=created_cover,
                status="approved",
                asset_kind="headline-cover",
                selection_reason="即使 plan 未显式声明封面图位，也自动生成标准封面，避免交付链出现无头图状态。",
                source_url="local://headline-cover",
                source_class="local-generated",
                preview=True,
                slot_hint="封面图",
                slot_index="0",
                slot_title=primary_markdown_title(pack),
            )
        )

    if not slots:
        return assets, entries, failures, slot_map
    slot_budget = min(max(len(slots), max(remaining, 0)), 4)
    chosen_slots = slots[:slot_budget]

    for slot_index, slot in enumerate(chosen_slots, start=1):
        slot_title = derive_slot_title(slot, pack)
        slot_signature = f"{slot_kind_label(slot)}::{searchable_visual_text(slot_title)}"
        if slot_signature in seen_slot_signatures and clean(slot.get("priority", ""), "") == "optional":
            continue
        is_cover_slot = slot_is_cover_like(slot)
        if slot_prefers_primary_asset(slot) and reusable_primary and not slot_is_data_like(slot) and not is_cover_slot:
            assigned = reusable_primary.pop(0)
            assigned_kind = primary_kind_map.get(str(assigned), "official-asset")
            entries.append(
                manifest_entry(
                    path=assigned,
                    status="approved",
                    asset_kind=assigned_kind,
                    selection_reason="按配图计划优先复用已抓到的一手图 / 官方图，避免正文继续退化成通用解释卡。",
                    source_url="local://slot-primary-assignment",
                    source_class="primary-assigned",
                    preview=True,
                    slot_hint=slot.get("job", ""),
                    slot_index=str(slot_index),
                    slot_title=slot_title,
                )
            )
            slot_map.append(
                {
                    "slot_index": str(slot_index),
                    "slot_title": slot_title,
                    "asset_kind": assigned_kind,
                    "markdown_path": f"visual-assets/{assigned.name}",
                    "heading": slot.get("heading", ""),
                    "position": slot.get("position", ""),
                    "note": slot.get("note", ""),
                }
            )
            continue

        output_path = asset_dir / ("00__cover.png" if is_cover_slot else f"{79 + slot_index:02d}__slot_{slot_index}.png")
        asset_kind = "story-card"
        selection_reason = "根据 slot 需求自动生成稳定信息卡，优先保证可发布性与图文一致性。"
        created_path: Path | None = None

        if is_cover_slot:
            created_path = create_headline_cover_card(output_path, pack, slot, accent)
            asset_kind = "headline-cover"
            selection_reason = "根据标题与 approved angle 自动生成封面卡，替代泛化 AI 封面。"
        elif slot_is_data_like(slot):
            created_path = create_data_comparison_card(output_path, pack, slot, accent)
            if created_path is not None:
                asset_kind = "data-comparison-chart"
                selection_reason = "根据正文现成表格自动生成数据图，避免数据图退化成无关解释卡。"
        if created_path is None and (slot_is_framework_like(slot) or slot_is_explainer_like(slot) or slot_is_evidence_like(slot)):
            created_path = create_slot_story_card(output_path, pack, slot, accent)
            asset_kind = deterministic_slot_asset_kind(slot)
            selection_reason = deterministic_slot_selection_reason(slot)
        if created_path is None and allow_ai_fallback:
            ai_output = asset_dir / f"{69 + slot_index:02d}__ai_slot_{slot_index}.png"
            prompt = ai_image_prompt(pack, slot)
            try:
                ai_path, provider, auth_source = generate_ai_image(ai_output, prompt)
                provider_label = "MiniMax" if provider.startswith("minimax") else "OpenAI"
                quality_ok, quality_metrics, quality_failures = inspect_ai_image_quality(ai_path)
                if quality_ok:
                    created_path = ai_path
                    asset_kind = "ai-explainer"
                    selection_reason = f"{provider_label} 生成解释图，当前 slot 无法从正文表格或稳定模板直接生成。"
                    entries.append(
                        manifest_entry(
                            path=ai_path,
                            status="approved",
                            asset_kind=asset_kind,
                            selection_reason=selection_reason,
                            source_url=f"ai://{provider}",
                            source_class="generated-ai",
                            preview=True,
                            prompt=prompt,
                            slot_hint=slot.get("job", ""),
                            slot_index=str(slot_index),
                            slot_title=slot_title,
                            provider=provider,
                            auth_source=auth_source,
                            quality_gate="passed",
                            quality_metrics=json.dumps(quality_metrics, ensure_ascii=False),
                        )
                    )
                else:
                    ai_path.unlink(missing_ok=True)
                    failures.append(
                        f"{slot.get('job', 'explainer')} ｜ AI 解释图闸门拒收：{', '.join(quality_failures)} ｜ metrics={json.dumps(quality_metrics, ensure_ascii=False)}"
                    )
            except Exception as error:
                failures.append(f"ai generation unavailable for {slot.get('job', 'explainer')} ｜ {clean(str(error), '')}")
        if created_path is None:
            created_path = create_slot_story_card(output_path, pack, slot, accent)
            asset_kind = deterministic_slot_asset_kind(slot)
            selection_reason = deterministic_slot_selection_reason(slot)
        assets.append(created_path)
        entries.append(
            manifest_entry(
                path=created_path,
                status="approved",
                asset_kind=asset_kind,
                selection_reason=selection_reason,
                source_url=f"local://{asset_kind}",
                source_class="local-generated",
                preview=True,
                slot_hint=slot.get("job", ""),
                slot_index=str(slot_index),
                slot_title=slot_title,
            )
        )
        if not is_cover_slot:
            seen_slot_signatures.add(slot_signature)
            slot_map.append(
                {
                    "slot_index": str(slot_index),
                    "slot_title": slot_title,
                    "asset_kind": asset_kind,
                    "markdown_path": f"visual-assets/{created_path.name}",
                    "heading": slot.get("heading", ""),
                    "position": slot.get("position", ""),
                    "note": slot.get("note", ""),
                }
            )
        else:
            seen_slot_signatures.add(slot_signature)
    return assets, entries, failures, slot_map


def should_replace_markdown_asset(pack_dir: Path, markdown_path: str) -> bool:
    normalized = normalize_markdown_asset_path(markdown_path)
    if not normalized.startswith("visual-assets/"):
        return False
    plan_path = pack_dir / "inline-visual-plan.md"
    explicit_plan_assets = set(re.findall(r"visual-assets/[^\s`)<]+", plan_path.read_text(encoding="utf-8"))) if plan_path.exists() else set()
    if normalized in explicit_plan_assets:
        return False
    if AUTO_VISUAL_PATH_RE.match(normalized):
        return True
    return True


def refresh_markdown_auto_visuals(markdown: str, pack_dir: Path, slot_map: list[dict[str, str]]) -> str:
    if not markdown or not slot_map:
        return markdown

    kept_lines: list[str] = []
    for raw in markdown.splitlines():
        match = IMAGE_LINE_RE.match(raw.strip())
        if match:
            current_path = normalize_markdown_asset_path(match.group(2))
            if AUTO_VISUAL_PATH_RE.match(current_path):
                continue
        kept_lines.append(raw)
    refreshed = "\n".join(kept_lines)
    lines = refreshed.splitlines()
    for slot_index, slot in enumerate(slot_map, start=1):
        markdown_path = clean(slot.get("markdown_path", ""), "")
        if not markdown_path or markdown_path in "\n".join(lines):
            continue
        hints = section_hints_from_slot(
            {
                "heading": slot.get("heading", ""),
                "position": slot.get("position", ""),
                "note": slot.get("note", ""),
                "job": slot.get("slot_title", ""),
            }
        )
        insert_at: int | None = None
        for index, raw in enumerate(lines):
            match = MARKDOWN_HEADING_RE.match(raw.strip())
            if not match:
                continue
            title = searchable_visual_text(match.group(2))
            if any(hint and (searchable_visual_text(hint) in title or title in searchable_visual_text(hint)) for hint in hints):
                next_heading_index = len(lines)
                for cursor in range(index + 1, len(lines)):
                    if MARKDOWN_HEADING_RE.match(lines[cursor].strip()):
                        next_heading_index = cursor
                        break
                insert_at = next_heading_index
                break
        if insert_at is None:
            if slot_index == 1:
                insert_at = min(len(lines), 8)
            else:
                insert_at = len(lines)
        alt_text = clean(slot.get("slot_title", "正文配图"), "正文配图")
        snippet = [f"![{alt_text}]({markdown_path})", ""]
        if insert_at > 0 and lines[insert_at - 1].strip():
            snippet.insert(0, "")
        lines[insert_at:insert_at] = snippet
    return "\n".join(lines)


def refresh_platform_visual_references(pack: DraftPack, slot_map: list[dict[str, str]]) -> list[Path]:
    updated_paths: list[Path] = []
    if not slot_map:
        return updated_paths
    for field_name in (
        "wechat_path",
        "zhihu_path",
        "bilibili_path",
        "toutiao_path",
        "baijiahao_path",
        "xiaohongshu_path",
        "x_path",
    ):
        raw_path = clean(pack.paths.get(field_name, "n/a"), "")
        if not raw_path or raw_path == "n/a":
            continue
        resolved = resolve_doc_path(raw_path)
        if not resolved.exists():
            continue
        original = resolved.read_text(encoding="utf-8")
        refreshed = refresh_markdown_auto_visuals(original, pack.pack_dir, slot_map)
        if refreshed != original:
            resolved.write_text(refreshed, encoding="utf-8")
            updated_paths.append(resolved)
    return updated_paths


def source_capture_targets(pack: DraftPack, limit: int = 4) -> list[tuple[str, str]]:
    targets: list[tuple[str, str]] = []
    seen: set[str] = set()
    for url in discover_source_urls(pack):
        if url in seen:
            continue
        seen.add(url)
        targets.append((url, url))
        if len(targets) >= limit:
            return targets
    return targets


def slugify_url(url: str) -> str:
    slug = re.sub(r"^https?://", "", url)
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", slug).strip("_").lower()
    return slug[:48] or "source"


def should_full_page_capture(url: str) -> bool:
    return any(token in url for token in [".pdf", "old.reddit.com"])


def materialize_visual_assets(pack: DraftPack, target_total: int = 4) -> tuple[list[Path], Path, list[dict[str, str]]]:
    asset_dir = pack.pack_dir / "visual-assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    clear_auto_generated_assets(asset_dir)
    capture_script = ROOT / "09_runbooks" / "scripts" / "market_visual_capture_helper.py"
    source_assets: list[Path] = []
    preview_assets: list[Path] = []
    failures: list[str] = []
    manifest_entries: list[dict[str, str | bool]] = []
    used_source_urls: set[str] = set()
    primary_asset_kinds: dict[str, str] = {}
    accent_map = {
        "wechat": "#1aad19",
        "zhihu": "#1677ff",
        "xiaohongshu": "#ff2442",
        "x": "#111111",
        "bilibili": "#00a1d6",
        "toutiao": "#ff4d4f",
        "baijiahao": "#3b82f6",
    }
    accent = accent_map.get(pack.requested_platforms[0], "#4f8cff") if pack.requested_platforms else "#4f8cff"

    if is_morning_roundup_pack(pack):
        for stale in asset_dir.iterdir():
            if stale.name in {ASSET_MANIFEST_NAME, "_capture-log.md"}:
                continue
            if stale.name == "00__cover.png":
                continue
            if stale.is_file():
                stale.unlink(missing_ok=True)
        cover_path = asset_dir / "00__cover.png"
        synthetic_cover_slot = {
            "slot": "cover_auto",
            "heading": "AI早报封面",
            "job": "固定系列封面",
            "platform": preferred_visual_platform(pack),
        }
        create_headline_cover_card(cover_path, pack, synthetic_cover_slot, accent)
        manifest_entries.append(
            manifest_entry(
                path=cover_path,
                status="approved",
                asset_kind="headline-cover",
                selection_reason="晨间聚合早报默认只自动生成固定系列封面，正文图保持可选，避免误抓无关素材。",
                source_url="local://morning-roundup-cover",
                source_class="local-generated",
                preview=True,
                slot_hint="封面图",
                slot_index="0",
                slot_title=primary_markdown_title(pack),
            )
        )
        log_path = asset_dir / "_capture-log.md"
        manifest_path = asset_dir / ASSET_MANIFEST_NAME
        log_lines = [
            "# Visual Asset Capture Log",
            "",
            f"- `draft_key`: `{pack.draft_key}`",
            "- `source_asset_count`: `0`",
            "- `slot_asset_count`: `1`",
            "- `external_safe_count`: `0`",
            "- `ai_or_structured_count`: `0`",
            "- `generated_explainer_count`: `0`",
            f"- `policy_version`: `{ASSET_POLICY_VERSION}`",
            "",
            "## Source Assets",
            "",
            "- `none`",
            "",
            "## Slot Assets",
            "",
            f"- `{cover_path}`",
            "",
            "## External Safe Assets",
            "",
            "- `none`",
            "",
            "## Generated Explainers",
            "",
            "- `none`",
            "",
            "## Capture Failures",
            "",
            "- `none`",
        ]
        log_path.write_text("\n".join(log_lines).rstrip() + "\n", encoding="utf-8")
        manifest_payload = {
            "draft_key": pack.draft_key,
            "generated_at": format_ts(now_cn()),
            "policy_version": ASSET_POLICY_VERSION,
            "entries": manifest_entries,
        }
        manifest_path.write_text(json.dumps(manifest_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return [cover_path], log_path, []

    for index, (raw_ref, url) in enumerate(source_capture_targets(pack, limit=max(target_total * 3, 8)), start=1):
        if len(source_assets) >= target_total:
            break
        policy = source_policy(url)
        if not policy.allow_screenshot and not policy.allow_metadata_image:
            failures.append(f"{url} ｜ {policy.reason}")
            manifest_entries.append(
                manifest_entry(
                    path=None,
                    status="skipped",
                    asset_kind="blocked-source",
                    selection_reason=policy.reason,
                    source_url=url,
                    source_class=policy.source_class,
                    preview=False,
                )
            )
            continue

        if policy.allow_metadata_image and domain_matches(host_for(url), METADATA_IMAGE_DOMAINS):
            meta_image_url = extract_meta_image_url(url)
            if meta_image_url:
                try:
                    output_base = remote_image_output_path(asset_dir, index, url)
                    downloaded_path = download_image(meta_image_url, output_base)
                    source_assets.append(downloaded_path)
                    preview_assets.append(downloaded_path)
                    primary_asset_kinds[str(downloaded_path)] = "official-asset"
                    used_source_urls.add(meta_image_url)
                    manifest_entries.append(
                        manifest_entry(
                            path=downloaded_path,
                            status="approved",
                            asset_kind="official-asset",
                            selection_reason="优先使用页面自带官方预览图 / 缩略图。",
                            source_url=url,
                            source_class=policy.source_class,
                            preview=True,
                        )
                    )
                    continue
                except Exception as error:
                    failures.append(f"{url} ｜ metadata image fallback failed: {clean(str(error), '')}")

        if policy.allow_screenshot:
            output_path = screenshot_output_path(asset_dir, index, url)
            if output_path.exists():
                output_path.unlink()
            command = [
                "python3",
                str(capture_script),
                "--url",
                url,
                "--output",
                str(output_path),
                "--hide-cookie-banners",
            ]
            if should_full_page_capture(url):
                command.append("--full-page")
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0 and output_path.exists():
                source_assets.append(output_path)
                preview_assets.append(output_path)
                primary_asset_kinds[str(output_path)] = "source-screenshot"
                used_source_urls.add(url)
                manifest_entries.append(
                    manifest_entry(
                        path=output_path,
                        status="approved",
                        asset_kind="source-screenshot",
                        selection_reason="安全白名单内来源，保留对象识别与证据线索。",
                        source_url=url,
                        source_class=policy.source_class,
                        preview=True,
                    )
                )
                continue
            if output_path.exists():
                output_path.unlink()
            stderr = clean(result.stderr or result.stdout or "capture failed", "")
            failures.append(f"{url} ｜ {stderr or raw_ref}")
            manifest_entries.append(
                manifest_entry(
                    path=None,
                    status="failed",
                    asset_kind="source-screenshot",
                    selection_reason=stderr or raw_ref,
                    source_url=url,
                    source_class=policy.source_class,
                    preview=False,
                )
            )

    remaining = max(0, target_total - len(preview_assets))
    ai_assets, ai_entries, ai_failures, slot_map = materialize_ai_explainer_assets(
        pack,
        asset_dir,
        remaining=remaining,
        accent=accent,
        primary_assets=source_assets,
        primary_asset_kinds=primary_asset_kinds,
    )
    preview_assets.extend(ai_assets)
    manifest_entries.extend(ai_entries)
    failures.extend(ai_failures)

    remaining = max(0, target_total - len(preview_assets))
    external_assets, external_entries, external_failures = materialize_external_safe_assets(
        pack,
        asset_dir,
        remaining=remaining,
        used_urls=used_source_urls,
        has_primary_visuals=bool(preview_assets),
    )
    preview_assets.extend(external_assets)
    manifest_entries.extend(external_entries)
    failures.extend(external_failures)

    fallback_specs = [
        (
            asset_dir / "90__core-judgment-card.png",
            "这件事真正值得看的点",
            pack.topic_title,
            [pack.approved_angle, pack.core_judgment],
        ),
        (
            asset_dir / "91__why-now-card.png",
            "为什么现在值得看",
            "不是普通资讯，而是值得继续追的信号",
            [
                f"核心判断：{pack.approved_angle}",
                "图像任务：优先证明事实，再解释结构，最后控制阅读节奏。",
            ],
        ),
        (
            asset_dir / "92__risk-boundary-card.png",
            "风险与边界",
            "别把热度直接当结论",
            [pack.risk_note],
        ),
    ]
    generated_cards: list[Path] = []
    for output_path, title, subtitle, bullets in fallback_specs:
        if len(preview_assets) + len(generated_cards) >= target_total:
            break
        created = create_text_card(output_path, title, subtitle, bullets, accent)
        generated_cards.append(created)
        manifest_entries.append(
            manifest_entry(
                path=created,
                status="approved",
                asset_kind="generated-explainer",
                selection_reason="未找到足够安全原图，退回解释型图卡保证成稿不断图。",
                source_url="",
                source_class="generated",
                preview=False,
            )
        )

    log_path = asset_dir / "_capture-log.md"
    manifest_path = asset_dir / ASSET_MANIFEST_NAME
    log_lines = [
        "# Visual Asset Capture Log",
        "",
        f"- `draft_key`: `{pack.draft_key}`",
        f"- `source_asset_count`: `{len(source_assets)}`",
        f"- `slot_asset_count`: `{len(ai_assets)}`",
        f"- `external_safe_count`: `{len(external_assets)}`",
        f"- `ai_or_structured_count`: `{len([entry for entry in ai_entries if str(entry.get('asset_kind', '')).startswith('ai-')])}`",
        f"- `generated_explainer_count`: `{len(generated_cards)}`",
        f"- `policy_version`: `{ASSET_POLICY_VERSION}`",
        "",
        "## Source Assets",
        "",
    ]
    if source_assets:
        log_lines.extend(f"- `{path}`" for path in source_assets)
    else:
        log_lines.append("- `none`")
    log_lines.extend(["", "## Slot Assets", ""])
    if ai_assets:
        log_lines.extend(f"- `{path}`" for path in ai_assets)
    else:
        log_lines.append("- `none`")
    log_lines.extend(["", "## External Safe Assets", ""])
    if external_assets:
        log_lines.extend(f"- `{path}`" for path in external_assets)
    else:
        log_lines.append("- `none`")
    log_lines.extend(["", "## Generated Explainers", ""])
    if generated_cards:
        log_lines.extend(f"- `{path}`" for path in generated_cards)
    else:
        log_lines.append("- `none`")
    log_lines.extend(["", "## Capture Failures", ""])
    if failures:
        log_lines.extend(f"- {failure}" for failure in failures)
    else:
        log_lines.append("- `none`")
    log_path.write_text("\n".join(log_lines).rstrip() + "\n", encoding="utf-8")
    manifest_payload = {
        "draft_key": pack.draft_key,
        "generated_at": format_ts(now_cn()),
        "policy_version": ASSET_POLICY_VERSION,
        "entries": manifest_entries,
    }
    manifest_path.write_text(json.dumps(manifest_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return preview_assets + generated_cards, log_path, slot_map


def longform_completeness_notes(pack: DraftPack) -> str:
    lines = [
        "# Longform Completeness Notes",
        "",
        f"- `draft_key`: `{pack.draft_key}`",
        f"- `topic_title`: `{pack.topic_title}`",
        "",
    ]
    targets = [platform for platform in pack.requested_platforms if platform in LONGFORM_PLATFORMS]
    if not targets:
        lines.extend(
            [
                "## Coverage",
                "",
                "- `none`｜当前 pack 不含长文平台。",
            ]
        )
        return "\n".join(lines).rstrip() + "\n"
    lines.extend(
        [
            "## Universal Contract",
            "",
            "- 首屏前段必须回答：这是什么事、为什么现在值得看、我们的判断是什么。",
            "- 第一证据锚点不能太晚，不然文章会先抽象、后证明。",
            "- 每个 section 必须有明确 job，不能每段都在重复 headline。",
            "",
        ]
    )
    for platform in targets:
        lines.extend(
            [
                f"## `{platform_label(platform)}`",
                "",
                "- `first_screen_contract`: `对象 / why now / core claim`",
                "- `background_deadline`: `前 10-20% 内必须把原始事件讲清楚`",
                f"- `proof_cadence`: `{proof_cadence(platform)}`",
                f"- `section_job_map`: `{' / '.join(section_job_map(platform))}`",
                "- `fatigue_cut`: `长段压字、重复抽象判断、先讲框架后讲事件`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def wechat_html_handoff(pack: DraftPack) -> str:
    wechat_path = pack.paths.get("wechat_path", "n/a")
    lines = [
        "# WeChat HTML Handoff",
        "",
        f"- `source_markdown`: `{wechat_path}`",
        f"- `core_judgment`: `{pack.core_judgment}`",
        "",
        "## Formatting Guidance",
        "",
        "- 标题下固定带品牌签名块：`同行资本 TH Capital` + 一句话 slogan + 一句定位说明。",
        "- 第一屏必须完成：对象是什么、为什么现在值得看、核心判断是什么。",
        "- 导语后固定插入一张“关注我们”提示卡，动作要轻，不要像硬广。",
        "- 保留标题、导语、一级 / 二级小标题结构。",
        "- 一级小标题要有明确设计感；不要只靠“字号变大”去区分层级。",
        "- 二级小标题适合做成更轻的标签 / chip 样式，帮助读者扫读。",
        "- 开头 2-4 段要突出“为什么值得看”。",
        "- 背景桥接要在前 3 屏内落地，不要一直藏对象。",
        "- 适合加强调或引用框的位置，优先放在核心判断和关键变量附近。",
        f"- 风险提示不能丢：{pack.risk_note}",
        "",
        "## Note",
        "",
        "- 本文件只提供 handoff，不代表 HTML 已完成。",
    ]
    return "\n".join(lines).rstrip() + "\n"


def xiaohongshu_card_brief(pack: DraftPack) -> str:
    xhs_path = pack.paths.get("xiaohongshu_path", "n/a")
    lines = [
        "# Xiaohongshu Card Brief",
        "",
        f"- `source_draft`: `{xhs_path}`",
        f"- `approved_angle`: `{pack.approved_angle}`",
        "",
        "## Card Structure",
        "",
        "- 卡 1：一句话结论",
        "- 卡 2：一句话背景桥接",
        "- 卡 3：为什么现在值得看",
        "- 卡 4：真正要看的变量",
        "- 卡 5：容易被忽视的风险",
        "- 卡 6：互动 / 导流",
        "",
        "## Discipline",
        "",
        "- 每张卡都要短、直、信息密度高。",
        "- 不能把长段公众号文案直接塞进图卡。",
        "- 第 1-2 张卡就要让用户知道这是啥、和自己有什么关系。",
    ]
    return "\n".join(lines).rstrip() + "\n"


def update_card_field(text: str, field_name: str, value: str) -> str:
    return re.sub(
        rf"^(- `{re.escape(field_name)}`: `)([^`]+)(`)\s*$",
        lambda match: f"{match.group(1)}{value}{match.group(3)}",
        text,
        count=1,
        flags=re.M,
    )


def refresh_card_paths(text: str, pack_dir: Path) -> str:
    updated = text
    for field_name, filename in CARD_FILE_FIELDS.items():
        candidate = pack_dir / filename
        value = str(candidate) if candidate.exists() else "n/a"
        updated = update_card_field(updated, field_name, value)
    return updated


def update_card_status(text: str, target_status: str, pack_dir: Path) -> str:
    text = re.sub(
        r"^(- `status`: `)([^`]+)(`)\s*$",
        lambda match: f"{match.group(1)}{target_status}{match.group(3)}",
        text,
        count=1,
        flags=re.M,
    )
    text = refresh_card_paths(text, pack_dir)
    updated = format_ts(now_cn())
    text = re.sub(
        r"^(- `updated_at`: `)([^`]+)(`)\s*$",
        lambda match: f"{match.group(1)}{updated}{match.group(3)}",
        text,
        count=1,
        flags=re.M,
    )
    return text


def sanitize_roundup_copy(pack: DraftPack) -> list[Path]:
    if not is_morning_roundup_pack(pack):
        return []
    wechat_path_raw = pack.paths.get("wechat_path", "n/a")
    if not wechat_path_raw or wechat_path_raw == "n/a":
        return []
    wechat_path = Path(wechat_path_raw)
    if not wechat_path.exists():
        return []
    original = wechat_path.read_text(encoding="utf-8")
    sanitized = sanitize_morning_roundup_markdown(original)
    title_line = f"# {clean(pack.topic_title, 'AI早报')}"
    if sanitized.lstrip().startswith("# "):
        sanitized = re.sub(r"^#\s+.*$", title_line, sanitized, count=1, flags=re.M)
    else:
        sanitized = f"{title_line}\n\n{sanitized.lstrip()}"
    if sanitized == original:
        return []
    wechat_path.write_text(sanitized, encoding="utf-8")
    return [wechat_path]


def execution_log(pack: DraftPack, status: str, generated_files: list[Path]) -> str:
    lines = [
        "# 同行资本市场内容系统｜Content Polish Execution",
        "",
        f"- `draft_pack_dir`: `{pack.pack_dir}`",
        f"- `draft_key`: `{pack.draft_key}`",
        f"- `target_status`: `{status}`",
        f"- `approved_topic_path`: `{pack.approved_topic_path}`",
        "",
        "## Generated Files",
        "",
    ]
    lines.extend(f"- `{path}`" for path in generated_files)
    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- 已为 `{pack.draft_key}` 生成打磨层支撑文件。",
            f"- 当前建议状态：`{status}`。",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    pack_dir = Path(args.draft_pack_dir)
    pack = load_draft_pack(pack_dir)
    log_root = Path(args.log_root)
    sanitized_markdowns: list[Path] = []

    if args.write:
        sanitized_markdowns = sanitize_roundup_copy(pack)
        if sanitized_markdowns:
            pack = load_draft_pack(pack_dir)

    generated: list[tuple[Path, str]] = [
        (pack_dir / "polish-checklist.md", polish_checklist(pack, args.status)),
        (pack_dir / "polish-notes.md", polish_notes(pack, args.status)),
        (pack_dir / "publish-readiness.md", publish_readiness(pack, args.status)),
        (pack_dir / "voice-consistency-notes.md", voice_consistency_notes(pack)),
        (pack_dir / "platform-render-handoff.md", platform_render_handoff(pack)),
        (pack_dir / "longform-completeness-notes.md", longform_completeness_notes(pack)),
        (pack_dir / "cover-visual-brief.md", cover_visual_brief(pack)),
        (pack_dir / "cover-asset-assist.md", cover_asset_assist(pack)),
        (pack_dir / "visual-asset-sourcing.md", visual_asset_sourcing(pack)),
    ]

    if pack.paths.get("wechat_path") and pack.paths.get("wechat_path") != "n/a":
        generated.append((pack_dir / "wechat-html-handoff.md", wechat_html_handoff(pack)))
    if pack.paths.get("xiaohongshu_path") and pack.paths.get("xiaohongshu_path") != "n/a":
        generated.append((pack_dir / "xiaohongshu-card-brief.md", xiaohongshu_card_brief(pack)))

    if args.write:
        pack_dir.mkdir(parents=True, exist_ok=True)
        for path, content in generated:
            path.write_text(content, encoding="utf-8")
        visual_assets, capture_log_path, slot_map = materialize_visual_assets(pack)
        refreshed_markdowns = refresh_platform_visual_references(pack, slot_map)
        updated_card = update_card_status(pack.card_path.read_text(encoding="utf-8"), args.status, pack_dir)
        pack.card_path.write_text(updated_card, encoding="utf-8")
        log_root.mkdir(parents=True, exist_ok=True)
        log_path = log_root / f"{now_cn().strftime('%Y%m%d_%H%M%S')}__{pack.draft_key}__content-polish-execution.md"
        log_text = execution_log(
            pack,
            args.status,
            sanitized_markdowns + [path for path, _ in generated] + refreshed_markdowns + visual_assets + [capture_log_path],
        )
        log_path.write_text(log_text, encoding="utf-8")
        print(pack.card_path)
        print(log_path)
        return

    log_path = log_root / f"{now_cn().strftime('%Y%m%d_%H%M%S')}__{pack.draft_key}__content-polish-execution.md"
    log_text = execution_log(pack, args.status, [path for path, _ in generated])
    for path, content in generated:
        print(f"# Preview File: {path.name}")
        print(content)
        print("---")
    print(log_text)


if __name__ == "__main__":
    main()

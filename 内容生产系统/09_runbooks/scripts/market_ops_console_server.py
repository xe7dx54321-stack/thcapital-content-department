#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import threading
import time
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, unquote, urlparse
from zoneinfo import ZoneInfo

import market_ops_dashboard_builder as builder
import market_learning_pool_board_builder as learning_builder


CN_TZ = ZoneInfo("Asia/Shanghai")
ROOT = builder.ROOT.resolve()
STATE_DIR = ROOT / "11_frontstage" / "_console_state"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8780
CACHE_TTL_SECONDS = 12
DEFAULT_ENTRY_PATH = "/today"
SAFE_FALLBACK_IMAGE_MARKERS = (
    "github_com",
    "openai_com",
    "anthropic_com",
    "deepmind_google",
    "x_ai",
    "figure_ai",
    "youtube_com",
    "youtu_be",
    "bilibili_com",
    "twitter_com",
    "x_com",
    "reddit_com",
    "old_reddit_com",
    "arxiv_org",
    "huggingface_co",
)
PREVIEWABLE_ASSET_KINDS = {
    "source-screenshot",
    "official-asset",
    "external-safe-image",
    "official-thumbnail",
    "pdf-title-capture",
    "ai-explainer",
    "structured-explainer",
}
ASSET_KIND_PRIORITY = {
    "source-screenshot": 0,
    "official-asset": 1,
    "official-thumbnail": 2,
    "external-safe-image": 3,
    "pdf-title-capture": 4,
    "structured-explainer": 5,
    "ai-explainer": 9,
}

_SNAPSHOT_CACHE: dict[tuple[str, str, str], tuple[float, dict[str, Any]]] = {}
_LEARNING_CACHE: dict[str, tuple[float, dict[str, Any]]] = {}
_CACHE_LOCK = threading.Lock()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve multi-page localhost console for market ops dashboard")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--date", default=datetime.now(CN_TZ).date().isoformat())
    parser.add_argument("--window-start", default="17:00")
    parser.add_argument("--window-end", default="14:30")
    return parser.parse_args()


def now_cst() -> str:
    return datetime.now(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def today_cn() -> str:
    return datetime.now(CN_TZ).date().isoformat()


def current_console_base_url() -> str:
    state_path = STATE_DIR / "market-ops-console.json"
    if state_path.exists():
        try:
            payload = json.loads(state_path.read_text(encoding="utf-8"))
            base_url = clean_text(payload.get("base_url", ""), fallback="")
            if base_url:
                return base_url
        except Exception:
            pass
    return f"http://{DEFAULT_HOST}:{DEFAULT_PORT}"


def read_snapshot(date_text: str, window_start: str, window_end: str, force: bool = False) -> dict[str, Any]:
    cache_key = (date_text, window_start, window_end)
    with _CACHE_LOCK:
        cached = _SNAPSHOT_CACHE.get(cache_key)
        if cached and not force and time.time() - cached[0] < CACHE_TTL_SECONDS:
            return cached[1]

    args = argparse.Namespace(date=date_text, window_start=window_start, window_end=window_end, write=True)
    snapshot = builder.build_snapshot(args)

    token = builder.day_token(date_text)
    html_path = builder.FRONTSTAGE_DIR / f"{token}__market-ops-dashboard.html"
    json_path = builder.FRONTSTAGE_DIR / f"{token}__market-ops-dashboard.snapshot.json"
    html_path.write_text(builder.render_html(snapshot), encoding="utf-8")
    json_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")

    with _CACHE_LOCK:
        _SNAPSHOT_CACHE[cache_key] = (time.time(), snapshot)
    return snapshot


def read_learning_snapshot(date_text: str, force: bool = False) -> dict[str, Any]:
    with _CACHE_LOCK:
        cached = _LEARNING_CACHE.get(date_text)
        if cached and not force and time.time() - cached[0] < CACHE_TTL_SECONDS:
            return cached[1]

    snapshot = learning_builder.build_snapshot(date_text)
    learning_builder.write_outputs(snapshot, write_log=False)

    with _CACHE_LOCK:
        _LEARNING_CACHE[date_text] = (time.time(), snapshot)
    return snapshot


def normalize_path(path_text: str) -> Path | None:
    if not path_text:
        return None
    try:
        resolved = Path(path_text).expanduser().resolve()
    except Exception:
        return None
    if ROOT in resolved.parents or resolved == ROOT:
        return resolved
    return None


def html_escape(text: Any) -> str:
    return builder.escape(str(text))


def clean_text(value: Any, fallback: str = "n/a") -> str:
    return builder.clean(str(value), fallback=fallback)


def nav_link(page: str, label: str, active_page: str, date_text: str) -> str:
    active_cls = "nav-link active" if page == active_page else "nav-link"
    return f'<a class="{active_cls}" href="/{page}?date={quote(date_text)}">{html_escape(label)}</a>'


def chip(text: str, tone: str = "neutral") -> str:
    return f'<span class="chip chip-{html_escape(tone)}">{html_escape(text)}</span>'


def button_link(label: str, href: str, kind: str = "ghost", new_tab: bool = False) -> str:
    extra = ' target="_blank" rel="noreferrer"' if new_tab else ""
    return f'<a class="btn btn-{html_escape(kind)}" href="{html_escape(href)}"{extra}>{html_escape(label)}</a>'


def button_form(label: str, action: str, *, item_id: str, date_text: str, kind: str = "ghost") -> str:
    return (
        f'<form class="inline-form" method="POST" action="/learning/optimization">'
        f'<input type="hidden" name="item_id" value="{html_escape(item_id)}">'
        f'<input type="hidden" name="action" value="{html_escape(action)}">'
        f'<input type="hidden" name="date" value="{html_escape(date_text)}">'
        f'<button type="submit" class="btn btn-{html_escape(kind)} compact">{html_escape(label)}</button>'
        "</form>"
    )


def artifact_link(path_text: str, label: str = "查看文件") -> str:
    resolved = normalize_path(path_text)
    if not resolved:
        return '<span class="btn btn-disabled">文件缺失</span>'
    return f'<a class="btn compact" href="/artifact?path={quote(str(resolved))}">{html_escape(label)}</a>'


def external_link(url: str, label: str = "原文") -> str:
    if not url or url == "n/a" or not re.match(r"^https?://", url):
        return '<span class="btn btn-disabled">无原文</span>'
    return f'<a class="btn btn-primary compact" href="{html_escape(url)}" target="_blank" rel="noreferrer">{html_escape(label)}</a>'


def format_title(title: str, sub: str | None = None) -> str:
    if not sub:
        return f'<div class="title-main">{html_escape(title)}</div>'
    return f'<div class="title-main">{html_escape(title)}</div><div class="title-sub">{html_escape(sub)}</div>'


def list_html(items: list[str], cls: str = "bullet-list") -> str:
    if not items:
        return '<div class="empty-inline">当前没有补充项。</div>'
    return f'<ul class="{cls}">' + "".join(f"<li>{html_escape(item)}</li>" for item in items) + "</ul>"


INLINE_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)|\*\*(.+?)\*\*|`([^`]+)`")
KV_LINE_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
INTERNAL_PATH_RE = re.compile(r"(/Users/|\\Users\\|^evidence_hint::|证据提示：)")

HIDDEN_SECTION_HEADINGS = {
    "开头",
    "正文",
    "互动",
    "轻 CTA",
    "先给结论",
    "推荐包装",
    "标题候选",
    "封面包装",
    "配图建议",
    "引用来源",
    "参考来源",
}
SECTION_HEADING_MAP = {
    "如果你还没跟这件事，先把背景说清楚": "先把背景讲清楚",
    "先看一眼证据锚点": "关键证据",
    "先看案例 / 证据锚点": "关键证据",
    "TH Capital 的判断": "我们的判断",
    "下一步观察": "接下来关注什么",
    "为什么这个角度值得看": "为什么值得看",
}


def read_utf8(path: Path | None) -> str:
    if not path or not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def extract_heading_title(text: str) -> str:
    title = builder.extract_first_heading(text)
    return clean_text(title)


def split_markdown_sections(text: str) -> tuple[str, list[dict[str, Any]]]:
    title = extract_heading_title(text)
    sections: list[dict[str, Any]] = []
    current: dict[str, Any] = {"heading": "", "lines": []}
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped.startswith("# "):
            continue
        if stripped.startswith("## "):
            if current["heading"] or current["lines"]:
                sections.append(current)
            current = {"heading": clean_text(stripped[3:]), "lines": []}
            continue
        current["lines"].append(line)
    if current["heading"] or current["lines"]:
        sections.append(current)
    return title, sections


def normalize_content_line(line: str) -> str:
    text = line.strip()
    text = re.sub(r"evidence_hint::[^:]+::", "证据提示：", text)
    return text


def is_internal_reference_line(text: str) -> bool:
    value = text.strip()
    if not value:
        return False
    if INTERNAL_PATH_RE.search(value):
        return True
    if value.endswith(".md") and ("/" in value or "\\" in value):
        return True
    if "__top20-screening-pack" in value or "__platform-task-sheet" in value:
        return True
    if "source_packets/" in value or "draft_packs/" in value or "approved_topics/" in value:
        return True
    return False


def sanitize_section_heading(heading: str) -> str | None:
    normalized = clean_text(heading, fallback="").strip()
    if not normalized or normalized in HIDDEN_SECTION_HEADINGS:
        return None
    for raw, target in SECTION_HEADING_MAP.items():
        if normalized == raw:
            return target
    return normalized


def clean_packaging_text(text: str) -> str:
    value = clean_text(text, fallback="")
    if not value:
        return ""
    replacements = [
        "封面主文案：",
        "封面文案：",
        "主标题：",
        "副标题：",
        "副文案：",
        "一句话背景：",
        "首屏钩子：",
        "背景桥接：",
        "封面：",
    ]
    for token in replacements:
        value = value.replace(token, "")
    value = re.sub(r"\s{2,}", " ", value).strip(" /")
    return value


def render_inline(text: str) -> str:
    output: list[str] = []
    cursor = 0
    for match in INLINE_RE.finditer(text):
        output.append(html_escape(text[cursor : match.start()]))
        if match.group(1) and match.group(2):
            output.append(
                f'<a class="inline-link" href="{html_escape(match.group(2))}" target="_blank" rel="noreferrer">{html_escape(match.group(1))}</a>'
            )
        elif match.group(3):
            output.append(f"<strong>{html_escape(match.group(3))}</strong>")
        elif match.group(4):
            output.append(f"<code>{html_escape(match.group(4))}</code>")
        cursor = match.end()
    output.append(html_escape(text[cursor:]))
    return "".join(output)


def parse_kv_section(lines: list[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw in lines:
        line = raw.strip()
        if not line.startswith("- "):
            continue
        match = KV_LINE_RE.match(line)
        if match:
            fields[clean_text(match.group(1))] = clean_text(match.group(2))
            continue
        body = line[2:]
        if "：" in body:
            key, value = body.split("：", 1)
        elif ":" in body:
            key, value = body.split(":", 1)
        else:
            continue
        key = clean_text(re.sub(r"^\*\*(.*?)\*\*$", r"\1", key.strip()))
        fields[key] = clean_text(value)
    return fields


def extract_list_items(lines: list[str]) -> list[str]:
    items: list[str] = []
    for raw in lines:
        stripped = normalize_content_line(raw)
        if stripped.startswith("- "):
            items.append(clean_text(stripped[2:]))
        elif re.match(r"^\d+[.)/]\s+", stripped):
            items.append(clean_text(re.sub(r"^\d+[.)/]\s+", "", stripped)))
    return items


def extract_hash_tags(lines: list[str]) -> list[str]:
    tags: list[str] = []
    for raw in lines:
        stripped = normalize_content_line(raw)
        if not stripped:
            continue
        tags.extend(re.findall(r"#\S+", stripped))
    return tags


def find_section(sections: list[dict[str, Any]], keywords: list[str]) -> dict[str, Any] | None:
    for section in sections:
        heading = str(section.get("heading", ""))
        if any(keyword in heading for keyword in keywords):
            return section
    return None


def keep_body_section(platform: str, heading: str) -> bool:
    skip = {"推荐包装", "标题候选", "封面包装"}
    if any(token in heading for token in skip):
        return False
    if "引用来源" in heading or "参考来源" in heading:
        return False
    if platform == "xiaohongshu":
        return heading in {"正文", "互动", "图卡文案", "配文"} or heading == ""
    return True


def find_visual_assets(pack_dir: Path | None) -> list[Path]:
    if not pack_dir or not pack_dir.exists():
        return []
    result: list[Path] = []
    visual_root = pack_dir / "visual-assets"
    manifest_path = visual_root / "_asset-manifest.json"
    if manifest_path.exists():
        try:
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            ranked: list[tuple[int, int, str, Path]] = []
            for entry in payload.get("entries", []):
                if not entry.get("preview") or entry.get("status") != "approved":
                    continue
                asset_kind = clean_text(str(entry.get("asset_kind", "")), fallback="")
                if asset_kind not in PREVIEWABLE_ASSET_KINDS:
                    continue
                path_text = clean_text(str(entry.get("path", "")), fallback="")
                if not path_text:
                    continue
                path = Path(path_text)
                if path.exists() and path.suffix.lower() in IMAGE_SUFFIXES:
                    ranked.append(
                        (
                            ASSET_KIND_PRIORITY.get(asset_kind, 99),
                            1 if asset_kind == "ai-explainer" else 0,
                            path.name,
                            path,
                        )
                    )
            if ranked:
                ranked.sort(key=lambda item: (item[0], item[1], item[2]))
                ordered = [item[3] for item in ranked]
                non_ai = [path for _, is_ai, _, path in ranked if is_ai == 0]
                if non_ai:
                    return non_ai[:6]
                return ordered[:6]
        except Exception:
            result = []
    roots = [visual_root] if visual_root.exists() else [pack_dir]
    for root in roots:
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
                if "mp_weixin_qq_com" in path.name:
                    continue
                lowered = path.name.lower()
                if not any(marker in lowered for marker in SAFE_FALLBACK_IMAGE_MARKERS):
                    continue
                result.append(path)
    return result[:6]


def image_data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(str(path))[0] or "image/png"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def visual_heading_names(platform: str) -> set[str]:
    names = {
        "wechat": {"微信公众号", "微信"},
        "xiaohongshu": {"小红书"},
        "zhihu": {"知乎"},
        "x": {"X / Thread", "X"},
        "bilibili": {"B站", "B站专栏"},
        "toutiao": {"今日头条"},
        "baijiahao": {"百家号"},
    }
    return names.get(platform, {platform})


def parse_visual_slots(pack_dir: Path | None, platform: str) -> list[dict[str, str]]:
    if not pack_dir:
        return []
    path = pack_dir / "inline-visual-plan.md"
    text = read_utf8(path)
    if not text:
        return []
    inside = False
    current: dict[str, str] = {}
    slots: list[dict[str, str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("### "):
            if inside and current:
                slots.append(current)
                current = {}
            title = clean_text(line[4:]).strip("`")
            inside = title in visual_heading_names(platform)
            continue
        if not inside:
            continue
        match = KV_LINE_RE.match(line)
        if not match:
            continue
        key = clean_text(match.group(1))
        value = clean_text(match.group(2))
        if key.startswith("slot_"):
            if current:
                slots.append(current)
            current = {"slot": value}
        else:
            current[key] = value
    if inside and current:
        slots.append(current)
    return slots


def compute_slot_positions(section_count: int, slot_count: int) -> list[int]:
    if section_count <= 0 or slot_count <= 0:
        return []
    positions: list[int] = []
    for index in range(slot_count):
        position = round(((index + 1) * section_count) / (slot_count + 1)) - 1
        positions.append(max(0, min(section_count - 1, position)))
    return positions


def render_visual_slot(slot: dict[str, str], image_path: Path | None = None) -> str:
    label = slot.get("job", slot.get("slot", "配图位"))
    if image_path and image_path.exists():
        src = image_data_uri(image_path)
        return (
            '<figure class="visual-card actual">'
            f'<img src="{src}" alt="{html_escape(label)}">'
            "</figure>"
        )
    return ""


def render_visual_strip(pack_dir: Path | None, platform: str, limit: int = 4) -> str:
    slots = parse_visual_slots(pack_dir, platform)[:limit]
    images = find_visual_assets(pack_dir)[:limit]
    cards: list[str] = []
    max_len = min(len(images), max(len(slots), len(images)))
    for index in range(max_len):
        slot = slots[index] if index < len(slots) else {"slot": f"图 {index + 1}", "job": "配图", "preferred_asset": "正文图片"}
        image_path = images[index] if index < len(images) else None
        rendered = render_visual_slot(slot, image_path)
        if rendered:
            cards.append(rendered)
    return f'<div class="visual-strip">{"".join(cards)}</div>' if cards else ""


def render_markdown_lines(lines: list[str]) -> str:
    blocks: list[str] = []
    index = 0
    while index < len(lines):
        stripped = normalize_content_line(lines[index])
        if not stripped or stripped == "---":
            index += 1
            continue
        if is_internal_reference_line(stripped):
            index += 1
            continue
        if stripped.startswith("### "):
            blocks.append(f'<h4 class="article-inline-heading">{render_inline(stripped[4:])}</h4>')
            index += 1
            continue
        if stripped.startswith("#### "):
            blocks.append(f'<h4 class="article-inline-heading">{render_inline(stripped[5:])}</h4>')
            index += 1
            continue
        if stripped.startswith("> "):
            quote_lines: list[str] = []
            while index < len(lines):
                current = normalize_content_line(lines[index])
                if not current.startswith("> "):
                    break
                if not is_internal_reference_line(current[2:]):
                    quote_lines.append(render_inline(current[2:]))
                index += 1
            if quote_lines:
                blocks.append('<blockquote class="article-quote">' + "<br>".join(quote_lines) + "</blockquote>")
            continue
        if stripped.startswith("- "):
            bullets: list[str] = []
            while index < len(lines):
                current = normalize_content_line(lines[index])
                if not current.startswith("- "):
                    break
                bullet_text = current[2:]
                if not is_internal_reference_line(bullet_text):
                    bullets.append(f"<li>{render_inline(bullet_text)}</li>")
                index += 1
            if bullets:
                blocks.append('<ul class="article-list">' + "".join(bullets) + "</ul>")
            continue
        if re.match(r"^\d+[.)/]\s+", stripped):
            items: list[str] = []
            while index < len(lines):
                current = normalize_content_line(lines[index])
                if not re.match(r"^\d+[.)/]\s+", current):
                    break
                item_text = re.sub(r'^\d+[.)/]\s+', '', current)
                if not is_internal_reference_line(item_text):
                    items.append(f"<li>{render_inline(item_text)}</li>")
                index += 1
            if items:
                blocks.append('<ol class="article-olist">' + "".join(items) + "</ol>")
            continue
        if stripped.startswith("**【") and stripped.endswith("】**"):
            blocks.append(f'<h4 class="article-inline-heading">{render_inline(stripped[2:-2].strip("【】"))}</h4>')
            index += 1
            continue
        paragraph: list[str] = [stripped]
        index += 1
        while index < len(lines):
            current = normalize_content_line(lines[index])
            if not current or current == "---" or current.startswith("> ") or current.startswith("- ") or re.match(r"^\d+[.)/]\s+", current):
                break
            if current.startswith("**【") and current.endswith("】**"):
                break
            if not is_internal_reference_line(current):
                paragraph.append(current)
            index += 1
        if paragraph:
            blocks.append(f'<p class="article-paragraph">{render_inline(" ".join(paragraph))}</p>')
    return "".join(blocks)


def render_longform_sections(sections: list[dict[str, Any]], pack_dir: Path | None, platform: str) -> str:
    body_sections = [section for section in sections if keep_body_section(platform, str(section.get("heading", "")))]
    slots = parse_visual_slots(pack_dir, platform)
    images = find_visual_assets(pack_dir)
    positions = compute_slot_positions(len(body_sections), min(len(slots), len(images), 4))
    slot_cursor = 0
    body_parts: list[str] = []
    for index, section in enumerate(body_sections):
        heading = str(section.get("heading", ""))
        display_heading = sanitize_section_heading(heading)
        rendered_block = render_markdown_lines(list(section.get("lines", [])))
        if not rendered_block:
            continue
        if display_heading:
            body_parts.append(f'<h3 class="article-section-title">{html_escape(display_heading)}</h3>')
        body_parts.append(rendered_block)
        while slot_cursor < len(positions) and positions[slot_cursor] == index:
            image_path = images[slot_cursor] if slot_cursor < len(images) else None
            rendered_slot = render_visual_slot(slots[slot_cursor], image_path)
            if rendered_slot:
                body_parts.append(rendered_slot)
            slot_cursor += 1
    return "".join(body_parts)


def extract_references(sections: list[dict[str, Any]]) -> list[str]:
    references: list[str] = []
    for section in sections:
        heading = str(section.get("heading", ""))
        if "引用来源" not in heading and "参考来源" not in heading:
            continue
        references.extend(extract_list_items(list(section.get("lines", []))))
    return references


def build_draft_context(item: dict[str, Any]) -> dict[str, Any]:
    file_path = normalize_path(str(item.get("file_path", "")))
    pack_dir = normalize_path(str(item.get("pack_dir", "")))
    text = read_utf8(file_path)
    title, sections = split_markdown_sections(text)
    packaging_section = find_section(sections, ["推荐包装", "封面包装", "封面建议"]) if sections else None
    title_section = find_section(sections, ["标题候选", "标题备选"]) if sections else None
    tag_section = find_section(sections, ["标签"]) if sections else None
    packaging = parse_kv_section(list(packaging_section.get("lines", []))) if packaging_section else {}
    title_candidates = extract_list_items(list(title_section.get("lines", []))) if title_section else []
    references = extract_references(sections)
    tags = extract_hash_tags(list(tag_section.get("lines", []))) if tag_section else []
    return {
        "file_path": file_path,
        "pack_dir": pack_dir,
        "text": text,
        "title": title or clean_text(item.get("display_title", "待生成草稿")),
        "sections": sections,
        "packaging": packaging,
        "title_candidates": title_candidates,
        "references": references,
        "tags": tags,
        "images": find_visual_assets(pack_dir),
        "visual_slots": parse_visual_slots(pack_dir, str(item.get("platform", ""))),
    }


def author_badge(platform: str) -> str:
    labels = {
        "wechat": "同行资本市场部",
        "xiaohongshu": "同行资本内容工厂",
        "zhihu": "同行资本研究与内容",
        "x": "TH Capital",
        "bilibili": "同行资本观察室",
        "toutiao": "同行资本头条号",
        "baijiahao": "同行资本百家号",
    }
    return labels.get(platform, "同行资本")


def render_reference_block(references: list[str]) -> str:
    public_refs = [ref for ref in references if not is_internal_reference_line(ref)]
    if not public_refs:
        return ""
    items = "".join(f"<li>{render_inline(ref)}</li>" for ref in public_refs[:8])
    return '<section class="article-reference"><div class="article-reference-title">引用与来源</div><ul>' + items + "</ul></section>"


def render_wechat_mock(item: dict[str, Any], ctx: dict[str, Any], accent: str) -> str:
    body = render_longform_sections(ctx["sections"], ctx["pack_dir"], "wechat")
    return (
        f'<div class="platform-shell wechat" style="--platform-accent:{html_escape(accent)}">'
        '<div class="platform-chrome">微信公众号 · 发布预览</div>'
        '<article class="mock-article wechat-article">'
        f'<h1 class="mock-title">{html_escape(ctx["title"])}</h1>'
        f'<div class="mock-meta">{html_escape(author_badge("wechat"))} · {html_escape(item["updated_at"])} · 未发布</div>'
        + body
        + render_reference_block(ctx["references"])
        + "</article></div>"
    )


def render_xiaohongshu_mock(item: dict[str, Any], ctx: dict[str, Any], accent: str) -> str:
    cover = clean_packaging_text(
        ctx["packaging"].get("封面") or ctx["packaging"].get("封面主文案") or ctx["packaging"].get("封面文案", "")
    )
    if not cover:
        cover = clean_packaging_text(ctx["packaging"].get("主标题", ""))
    subtitle = clean_packaging_text(ctx["packaging"].get("副文案") or ctx["packaging"].get("一句话背景") or "")
    if not subtitle:
        subtitle = clean_packaging_text(ctx["packaging"].get("副标题", ""))
    body = render_longform_sections(ctx["sections"], ctx["pack_dir"], "xiaohongshu")
    visuals = render_visual_strip(ctx["pack_dir"], "xiaohongshu", limit=5)
    title = ctx["title_candidates"][0] if ctx["title_candidates"] else ctx["title"]
    tags = ctx.get("tags") or ["#AI", "#Agent", "#内容工厂"]
    return (
        f'<div class="platform-shell xiaohongshu" style="--platform-accent:{html_escape(accent)}">'
        '<div class="platform-chrome">小红书 · 发布预览</div>'
        '<article class="mock-phone xhs-note">'
        f'<div class="mock-meta userline"><span class="avatar-dot"></span>{html_escape(author_badge("xiaohongshu"))}<span class="dot-sep">·</span>刚刚生成</div>'
        f'<div class="xhs-cover-card"><div class="cover-title">{html_escape(cover or title)}</div>'
        + (f'<div class="cover-sub">{html_escape(subtitle)}</div>' if subtitle else "")
        + "</div>"
        + visuals
        + f'<h2 class="mock-title">{html_escape(title)}</h2>'
        + body
        + '<div class="mock-tags">' + "".join(f"<span>{html_escape(tag)}</span>" for tag in tags[:8]) + "</div>"
        + "</article></div>"
    )


def render_zhihu_mock(item: dict[str, Any], ctx: dict[str, Any], accent: str) -> str:
    body = render_longform_sections(ctx["sections"], ctx["pack_dir"], "zhihu")
    return (
        f'<div class="platform-shell zhihu" style="--platform-accent:{html_escape(accent)}">'
        '<div class="platform-chrome">知乎 · 发布预览</div>'
        '<article class="mock-article zhihu-answer">'
        f'<div class="question-chip">问题 · {html_escape(ctx["title"])}</div>'
        f'<h1 class="mock-title">{html_escape(ctx["title"])}</h1>'
        f'<div class="mock-meta">{html_escape(author_badge("zhihu"))} · 默认盐选风格排版</div>'
        + body
        + render_reference_block(ctx["references"])
        + "</article></div>"
    )


def render_x_mock(item: dict[str, Any], ctx: dict[str, Any], accent: str) -> str:
    posts: list[str] = []
    for raw in ctx["text"].splitlines():
        stripped = normalize_content_line(raw)
        if re.match(r"^\d+/\s+", stripped):
            posts.append(re.sub(r"^\d+/\s+", "", stripped))
    if not posts:
        posts = [ctx["title"]]
    image_path = ctx["images"][0] if ctx["images"] else None
    image_html = (
        f'<div class="tweet-image"><img src="{image_data_uri(image_path)}" alt="{html_escape(ctx["title"])}"></div>'
        if image_path and image_path.exists()
        else ""
    )
    tweet_cards = []
    for index, post in enumerate(posts, start=1):
        media = image_html if index == 2 and image_html else ""
        tweet_cards.append(
            '<div class="tweet-card">'
            f'<div class="mock-meta userline"><span class="avatar-dot dark"></span>{html_escape(author_badge("x"))}<span class="dot-sep">·</span>@thcapital</div>'
            f'<div class="tweet-body">{render_inline(post)}</div>'
            + media
            + f'<div class="tweet-footer">{index}/{len(posts)} · 草稿线程</div>'
            + "</div>"
        )
    return (
        f'<div class="platform-shell x-thread" style="--platform-accent:{html_escape(accent)}">'
        '<div class="platform-chrome dark">X / Thread · 发布预览</div>'
        f'<div class="tweet-stack">{"".join(tweet_cards)}</div>'
        "</div>"
    )


def render_editorial_mock(item: dict[str, Any], ctx: dict[str, Any], platform: str, accent: str) -> str:
    labels = {
        "bilibili": "B站专栏 · 发布预览",
        "toutiao": "今日头条 · 发布预览",
        "baijiahao": "百家号 · 发布预览",
    }
    body = render_longform_sections(ctx["sections"], ctx["pack_dir"], platform)
    title = ctx["title"]
    visual_strip = render_visual_strip(ctx["pack_dir"], platform, limit=3)
    return (
        f'<div class="platform-shell {html_escape(platform)}" style="--platform-accent:{html_escape(accent)}">'
        f'<div class="platform-chrome">{html_escape(labels.get(platform, "发布预览"))}</div>'
        '<article class="mock-article editorial-article">'
        f'<h1 class="mock-title">{html_escape(title)}</h1>'
        f'<div class="mock-meta">{html_escape(author_badge(platform))} · {html_escape(item["updated_at"])} · 待发布</div>'
        + visual_strip
        + body
        + render_reference_block(ctx["references"])
        + "</article></div>"
    )


def render_platform_preview(item: dict[str, Any]) -> str:
    platform = str(item.get("platform", ""))
    config = builder.PLATFORM_CONFIG.get(platform, {"label": platform, "accent": "#1f6fff"})
    accent = str(config.get("accent", "#1f6fff"))
    ctx = build_draft_context(item)
    title = ctx["title"]
    anchor = f'{platform}-{item["topic_key"]}'.replace("_", "-")
    toolbar = (
        '<div class="preview-toolbar">'
        f'<div class="preview-titleline"><div class="preview-platform">{html_escape(config["label"])}</div><div class="preview-topic">{html_escape(title)}</div></div>'
        f'<div class="chips">{chip(str(item["status"]), tone_for_status(str(item["status"])))}{chip(str(item["topic_key"]), "neutral")}</div>'
        f'<div class="cell-actions">{artifact_link(str(item.get("file_path", "")), "原稿 MD")}{artifact_link(str(item.get("pack_dir", "")), "Draft Pack")}</div>'
        "</div>"
    )
    if platform == "wechat":
        shell = render_wechat_mock(item, ctx, accent)
    elif platform == "xiaohongshu":
        shell = render_xiaohongshu_mock(item, ctx, accent)
    elif platform == "zhihu":
        shell = render_zhihu_mock(item, ctx, accent)
    elif platform == "x":
        shell = render_x_mock(item, ctx, accent)
    elif platform in {"bilibili", "toutiao", "baijiahao"}:
        shell = render_editorial_mock(item, ctx, platform, accent)
    else:
        shell = render_editorial_mock(item, ctx, platform, accent)
    return f'<section id="{html_escape(anchor)}" class="draft-preview-panel">{toolbar}{shell}</section>'


def page_shell(
    *,
    title: str,
    subtitle: str,
    body: str,
    active_page: str,
    snapshot: dict[str, Any],
    date_text: str,
) -> str:
    counts = snapshot["counts"]
    meta = snapshot["meta"]
    refresh_href = f"/{active_page}?date={quote(date_text)}&refresh=1"
    draft_value = counts.get("draft_cards", 0)
    inventory_value = counts.get("publishable_inventory_cards")
    draft_sub = (
        f"主线 {draft_value} / 库存 {inventory_value}"
        if inventory_value is not None
        else "平台稿件卡片数量"
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html_escape(title)}｜市场内容控制台</title>
  <style>
    :root {{
      --bg: #f6f8fc;
      --card: #ffffff;
      --card-soft: #f9fbff;
      --line: #e6ebf3;
      --line-strong: #d6deea;
      --text: #152034;
      --muted: #61708b;
      --blue: #1f6fff;
      --blue-soft: #eef4ff;
      --green: #13ae6f;
      --green-soft: #ebfff6;
      --orange: #f59e0b;
      --orange-soft: #fff7e7;
      --red: #e5484d;
      --red-soft: #fff1f2;
      --shadow: 0 14px 40px rgba(24, 39, 75, 0.08);
      --radius: 18px;
      --radius-sm: 14px;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
      background: linear-gradient(180deg, #f7f9fd 0%, #f4f7fb 100%);
      color: var(--text);
      line-height: 1.55;
    }}
    a {{ color: inherit; text-decoration: none; }}
    .app {{
      max-width: 1520px;
      margin: 0 auto;
      padding: 20px 24px 40px;
    }}
    .topbar {{
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(246,248,252,0.88);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(214, 222, 234, 0.7);
    }}
    .topbar-inner {{
      max-width: 1520px;
      margin: 0 auto;
      padding: 14px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }}
    .brand {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .brand-title {{ font-size: 18px; font-weight: 800; }}
    .brand-sub {{ color: var(--muted); font-size: 12px; }}
    .top-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .nav {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin: 16px 0 22px;
    }}
    .nav-link {{
      padding: 10px 14px;
      border-radius: 999px;
      border: 1px solid var(--line-strong);
      background: var(--card);
      color: var(--muted);
      font-size: 14px;
      font-weight: 600;
      box-shadow: 0 2px 10px rgba(24,39,75,0.04);
    }}
    .nav-link.active {{
      background: var(--blue);
      border-color: var(--blue);
      color: #fff;
      box-shadow: 0 8px 20px rgba(31,111,255,0.20);
    }}
    .hero {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 24px;
      box-shadow: var(--shadow);
      padding: 24px;
      margin-bottom: 18px;
    }}
    .hero-head {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 18px;
      margin-bottom: 18px;
    }}
    .hero h1 {{
      margin: 0;
      font-size: 30px;
      line-height: 1.18;
    }}
    .hero-sub {{
      color: var(--muted);
      font-size: 14px;
      margin-top: 8px;
      max-width: 860px;
    }}
    .hero-meta {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
    }}
    .meta-card {{
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--card-soft);
      padding: 14px 16px;
    }}
    .meta-label {{ color: var(--muted); font-size: 12px; margin-bottom: 6px; }}
    .meta-value {{ font-size: 16px; font-weight: 700; }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }}
    .metric {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 16px 18px;
      box-shadow: var(--shadow);
    }}
    .metric-label {{ color: var(--muted); font-size: 12px; margin-bottom: 6px; }}
    .metric-value {{ font-size: 28px; font-weight: 800; }}
    .metric-sub {{ color: var(--muted); font-size: 12px; margin-top: 6px; }}
    .panel {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 22px;
      box-shadow: var(--shadow);
      padding: 20px;
      margin-bottom: 18px;
    }}
    .panel-head {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 18px;
      margin-bottom: 14px;
    }}
    .panel-title {{
      font-size: 22px;
      line-height: 1.25;
      font-weight: 800;
      margin: 0;
    }}
    .panel-sub {{
      color: var(--muted);
      font-size: 14px;
      margin-top: 6px;
      max-width: 900px;
    }}
    .chips {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }}
    .chip {{
      display: inline-flex;
      align-items: center;
      padding: 5px 10px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      border: 1px solid transparent;
    }}
    .chip-neutral {{ background: #f1f4fa; color: #4f5f7a; border-color: #e2e9f3; }}
    .chip-good {{ background: var(--green-soft); color: #0f8e5a; border-color: #d5f5e7; }}
    .chip-warn {{ background: var(--orange-soft); color: #b66e00; border-color: #fde6b6; }}
    .chip-bad {{ background: var(--red-soft); color: #c03036; border-color: #f7d8da; }}
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 10px 14px;
      border-radius: 12px;
      border: 1px solid var(--line-strong);
      font-size: 13px;
      font-weight: 700;
      background: #fff;
      color: var(--text);
      cursor: pointer;
    }}
    .btn.compact {{
      padding: 7px 9px;
      border-radius: 10px;
      font-size: 12px;
      line-height: 1.15;
      min-height: 30px;
    }}
    .btn:hover {{ border-color: #bfd0ea; background: #f9fbff; }}
    .inline-form {{
      display: inline-flex;
      margin: 0;
    }}
    .inline-form + .inline-form {{
      margin-left: 6px;
    }}
    .btn-primary {{
      background: var(--blue);
      border-color: var(--blue);
      color: #fff;
    }}
    .btn-primary:hover {{ background: #155de0; border-color: #155de0; }}
    .btn-disabled {{
      pointer-events: none;
      background: #f3f6fb;
      border-color: var(--line);
      color: #99a6be;
    }}
    .alert {{
      border-radius: var(--radius);
      padding: 14px 16px;
      border: 1px solid transparent;
      margin-bottom: 16px;
    }}
    .alert-danger {{
      background: var(--red-soft);
      border-color: #f7d8da;
      color: #8e2430;
    }}
    .alert-success {{
      background: var(--green-soft);
      border-color: #d5f5e7;
      color: #0f8e5a;
    }}
    .alert ul {{ margin: 0; padding-left: 18px; }}
    .alert li + li {{ margin-top: 6px; }}
    .table-wrap {{
      width: 100%;
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 18px;
      background: #fff;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 1360px;
      table-layout: auto;
    }}
    th, td {{
      border-bottom: 1px solid var(--line);
      padding: 14px 14px;
      vertical-align: top;
      text-align: left;
      font-size: 14px;
      white-space: normal;
      word-break: break-word;
    }}
    th {{
      background: #f7f9fc;
      color: var(--muted);
      font-size: 12px;
      letter-spacing: .02em;
      font-weight: 800;
    }}
    tr:hover td {{ background: #fbfcfe; }}
    .title-main {{
      font-weight: 800;
      line-height: 1.4;
      margin-bottom: 4px;
    }}
    .title-sub {{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
    }}
    .timeline {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 12px;
    }}
    .clamp-1, .clamp-2, .clamp-3 {{
      display: -webkit-box;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .clamp-1 {{ -webkit-line-clamp: 1; }}
    .clamp-2 {{ -webkit-line-clamp: 2; }}
    .clamp-3 {{ -webkit-line-clamp: 3; }}
    .cell-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: flex-start;
    }}
    .fulltext {{
      line-height: 1.6;
      white-space: normal;
      word-break: break-word;
    }}
    .center-cell {{
      text-align: center;
      white-space: nowrap;
    }}
    .timeline-card {{
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 14px 16px;
      background: #fff;
      box-shadow: 0 4px 16px rgba(24,39,75,0.04);
    }}
    .timeline-meta {{ color: var(--muted); font-size: 12px; margin-bottom: 6px; }}
    .timeline-headline {{ font-size: 15px; font-weight: 800; line-height: 1.4; margin-bottom: 8px; }}
    .timeline-actions {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }}
    .bullet-list {{ margin: 0; padding-left: 18px; color: var(--muted); }}
    .bullet-list li + li {{ margin-top: 6px; }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }}
    .summary-card {{
      background: var(--card-soft);
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 14px 16px;
    }}
    .summary-card strong {{ display: block; margin-bottom: 6px; }}
    .filter-bar {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 14px;
    }}
    .search-input, .date-input {{
      padding: 11px 13px;
      border-radius: 12px;
      border: 1px solid var(--line-strong);
      background: #fff;
      font-size: 14px;
      min-width: 240px;
      color: var(--text);
    }}
    .platform-board {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 14px;
    }}
    .preview-nav {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 18px;
    }}
    .preview-nav-link {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 9px 12px;
      border-radius: 999px;
      border: 1px solid var(--line-strong);
      background: #fff;
      color: var(--text);
      font-size: 13px;
      font-weight: 700;
      box-shadow: 0 4px 12px rgba(24,39,75,0.05);
    }}
    .preview-nav-link span {{
      color: var(--muted);
      font-weight: 600;
    }}
    .preview-wall {{
      display: grid;
      gap: 18px;
    }}
    .draft-preview-panel {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 22px;
      box-shadow: var(--shadow);
      padding: 18px;
    }}
    .preview-toolbar {{
      display: grid;
      grid-template-columns: 1fr auto auto;
      gap: 14px;
      align-items: center;
      margin-bottom: 16px;
    }}
    .preview-titleline {{
      min-width: 0;
    }}
    .preview-platform {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      margin-bottom: 4px;
    }}
    .preview-topic {{
      font-size: 18px;
      font-weight: 800;
      line-height: 1.4;
    }}
    .platform-shell {{
      background: linear-gradient(180deg, rgba(18,24,38,0.03) 0%, rgba(18,24,38,0.01) 100%);
      border: 1px solid var(--line);
      border-radius: 20px;
      padding: 14px;
    }}
    .platform-chrome {{
      display: inline-flex;
      align-items: center;
      min-height: 34px;
      padding: 0 12px;
      border-radius: 999px;
      background: color-mix(in srgb, var(--platform-accent) 12%, white);
      color: #1f2a44;
      border: 1px solid color-mix(in srgb, var(--platform-accent) 22%, #d6deea);
      font-size: 12px;
      font-weight: 800;
      margin-bottom: 12px;
    }}
    .platform-chrome.dark {{
      background: #0f172a;
      border-color: #0f172a;
      color: #f8fafc;
    }}
    .mock-article {{
      background: #fff;
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 20px;
      box-shadow: 0 8px 20px rgba(24,39,75,0.05);
    }}
    .mock-phone {{
      width: min(420px, 100%);
      margin: 0 auto;
      background: #fff;
      border: 1px solid var(--line);
      border-radius: 26px;
      padding: 16px;
      box-shadow: 0 14px 28px rgba(24,39,75,0.08);
    }}
    .mock-title {{
      font-size: 28px;
      line-height: 1.28;
      margin: 0 0 12px;
      font-weight: 850;
      letter-spacing: -0.01em;
    }}
    .mock-meta {{
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 14px;
    }}
    .userline {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .avatar-dot {{
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: var(--platform-accent);
      display: inline-block;
      flex: 0 0 auto;
    }}
    .avatar-dot.dark {{ background: #111827; }}
    .dot-sep {{ color: #b0bacb; }}
    .wechat-cover, .editorial-hero, .xhs-cover-card {{
      border-radius: 18px;
      padding: 18px;
      background: linear-gradient(135deg, color-mix(in srgb, var(--platform-accent) 16%, white), color-mix(in srgb, var(--platform-accent) 8%, white));
      border: 1px solid color-mix(in srgb, var(--platform-accent) 18%, #d6deea);
      margin-bottom: 16px;
    }}
    .cover-kicker, .hero-label {{
      font-size: 12px;
      font-weight: 800;
      color: var(--muted);
      margin-bottom: 8px;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}
    .cover-title, .hero-title {{
      font-size: 24px;
      line-height: 1.35;
      font-weight: 850;
      color: #14213a;
    }}
    .cover-sub, .hero-sub {{
      margin-top: 10px;
      color: #30425f;
      font-size: 14px;
      line-height: 1.6;
    }}
    .hook-box {{
      padding: 14px 16px;
      border-radius: 14px;
      background: #f7fbff;
      border-left: 4px solid var(--platform-accent);
      margin-bottom: 18px;
      color: #243a5d;
      font-size: 14px;
    }}
    .article-section-title {{
      font-size: 20px;
      line-height: 1.35;
      margin: 24px 0 12px;
      font-weight: 850;
    }}
    .article-inline-heading {{
      font-size: 16px;
      line-height: 1.4;
      margin: 20px 0 10px;
      font-weight: 850;
      color: #22314d;
    }}
    .article-paragraph {{
      margin: 0 0 14px;
      font-size: 16px;
      line-height: 1.9;
      color: #1d293d;
    }}
    .article-list, .article-olist {{
      margin: 0 0 16px 0;
      padding-left: 22px;
      color: #1d293d;
      line-height: 1.8;
      font-size: 15px;
    }}
    .article-quote {{
      margin: 0 0 16px;
      padding: 12px 14px;
      border-left: 4px solid var(--platform-accent);
      background: #f8fbff;
      border-radius: 0 14px 14px 0;
      color: #274064;
      line-height: 1.8;
    }}
    .inline-link {{
      color: #1967d2;
      text-decoration: underline;
      text-underline-offset: 2px;
    }}
    .visual-strip {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
      margin: 14px 0 18px;
    }}
    .visual-card {{
      overflow: hidden;
      border-radius: 16px;
      border: 1px solid var(--line);
      background: #fff;
      box-shadow: 0 6px 14px rgba(24,39,75,0.05);
    }}
    .visual-card.actual img {{
      display: block;
      width: 100%;
      height: auto;
      background: #f5f7fb;
    }}
    .visual-card figcaption, .visual-card.placeholder {{
      padding: 12px 13px;
    }}
    .visual-kicker {{
      color: var(--muted);
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .04em;
      margin-bottom: 6px;
    }}
    .visual-title {{
      font-size: 15px;
      line-height: 1.45;
      font-weight: 800;
      margin-bottom: 6px;
      color: #17253c;
    }}
    .visual-note {{
      color: #334764;
      font-size: 13px;
      line-height: 1.6;
    }}
    .visual-note.muted {{
      margin-top: 6px;
      color: var(--muted);
    }}
    .article-reference {{
      margin-top: 22px;
      border-top: 1px solid var(--line);
      padding-top: 16px;
    }}
    .article-reference-title {{
      font-size: 13px;
      font-weight: 800;
      color: var(--muted);
      margin-bottom: 8px;
    }}
    .article-reference ul {{
      margin: 0;
      padding-left: 18px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.7;
    }}
    .tweet-stack {{
      display: grid;
      gap: 12px;
      max-width: 620px;
      margin: 0 auto;
    }}
    .tweet-card {{
      background: #fff;
      border: 1px solid #d9e0eb;
      border-radius: 18px;
      padding: 16px;
      box-shadow: 0 10px 22px rgba(24,39,75,0.05);
    }}
    .tweet-body {{
      font-size: 16px;
      line-height: 1.75;
      color: #0f172a;
      margin-bottom: 12px;
    }}
    .tweet-image {{
      overflow: hidden;
      border-radius: 16px;
      background: #f6f8fc;
      margin-bottom: 12px;
    }}
    .tweet-image img {{
      display: block;
      width: 100%;
      height: auto;
    }}
    .tweet-footer {{
      color: var(--muted);
      font-size: 12px;
    }}
    .question-chip {{
      display: inline-flex;
      align-items: center;
      padding: 6px 10px;
      border-radius: 999px;
      background: #eef5ff;
      color: #2762c1;
      font-size: 12px;
      font-weight: 800;
      margin-bottom: 12px;
    }}
    .mock-tags {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 16px;
    }}
    .mock-tags span {{
      padding: 6px 10px;
      border-radius: 999px;
      background: #fff2f4;
      color: #d83a56;
      font-size: 12px;
      font-weight: 700;
    }}
    .lane {{
      border: 1px solid var(--line);
      border-radius: 18px;
      background: #fff;
      overflow: hidden;
      box-shadow: 0 6px 18px rgba(24,39,75,0.05);
    }}
    .lane-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 16px;
      border-bottom: 1px solid var(--line);
      font-weight: 800;
      font-size: 15px;
      background: var(--lane-bg);
    }}
    .lane-body {{
      padding: 12px;
      display: grid;
      gap: 10px;
    }}
    .draft-card {{
      display: block;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: #fff;
      padding: 12px;
      color: inherit;
      transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease;
    }}
    .draft-card:hover {{
      transform: translateY(-1px);
      border-color: #c8d8ef;
      box-shadow: 0 10px 18px rgba(24,39,75,0.08);
    }}
    .draft-card.missing {{
      background: #fbfcfe;
      border-style: dashed;
    }}
    .draft-meta {{ font-size: 12px; color: var(--muted); margin-bottom: 8px; }}
    .draft-title {{ font-size: 15px; font-weight: 800; line-height: 1.4; margin-bottom: 6px; }}
    .draft-topic {{ font-size: 12px; color: #4b6cae; margin-bottom: 8px; }}
    .draft-preview {{ font-size: 13px; color: var(--muted); line-height: 1.6; min-height: 64px; }}
    .draft-footer {{ display: flex; justify-content: space-between; gap: 8px; font-size: 12px; color: var(--muted); margin-top: 8px; }}
    .digest-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 12px;
    }}
    .digest-card {{
      border: 1px solid var(--line);
      border-radius: 16px;
      background: #fff;
      padding: 14px 16px;
      box-shadow: 0 4px 16px rgba(24,39,75,0.04);
    }}
    .digest-head {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: flex-start;
      margin-bottom: 10px;
    }}
    .digest-title {{
      font-size: 15px;
      font-weight: 800;
      line-height: 1.4;
    }}
    .digest-sub {{
      color: var(--muted);
      font-size: 12px;
      margin-top: 4px;
    }}
    .digest-block + .digest-block {{
      margin-top: 10px;
      padding-top: 10px;
      border-top: 1px solid var(--line);
    }}
    .digest-label {{
      font-size: 12px;
      font-weight: 800;
      color: var(--muted);
      margin-bottom: 6px;
    }}
    .code-view {{
      background: #0f172a;
      color: #e8eefc;
      border-radius: 16px;
      padding: 18px;
      overflow: auto;
      border: 1px solid #15213a;
      font-size: 13px;
      line-height: 1.6;
      white-space: pre-wrap;
      word-break: break-word;
    }}
    .artifact-meta {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 14px;
      color: var(--muted);
      font-size: 13px;
    }}
    .empty-inline {{
      color: var(--muted);
      font-size: 13px;
    }}
    .footer {{
      color: var(--muted);
      font-size: 12px;
      margin-top: 18px;
      text-align: right;
    }}
    @media (max-width: 1080px) {{
      .metrics {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .hero-head, .panel-head, .topbar-inner {{ flex-direction: column; align-items: flex-start; }}
      .preview-toolbar {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 720px) {{
      .app {{ padding: 16px; }}
      .metrics {{ grid-template-columns: 1fr; }}
      .hero h1 {{ font-size: 24px; }}
      .panel-title {{ font-size: 20px; }}
      .mock-title {{ font-size: 22px; }}
      .cover-title, .hero-title {{ font-size: 20px; }}
    }}
  </style>
</head>
<body>
  <div class="topbar">
    <div class="topbar-inner">
      <div class="brand">
        <div class="brand-title">内容工厂本地控制台</div>
        <div class="brand-sub">localhost 多页前台 · 所有页面都直接连真实产物</div>
      </div>
      <div class="top-actions">
        {button_link("刷新当前页", refresh_href, kind="primary")}
        {button_link("查看 JSON 快照", f"/api/snapshot?date={quote(date_text)}", kind="ghost", new_tab=True)}
      </div>
    </div>
  </div>
  <main class="app">
    <div class="nav">
      {nav_link("intake", "① 信息 Intake", active_page, date_text)}
      {nav_link("top20", "② Top20", active_page, date_text)}
      {nav_link("selection", "③ 最终锁题", active_page, date_text)}
      {nav_link("drafts", "④ 稿件池", active_page, date_text)}
      {nav_link("learning", "⑤ 学习池", active_page, date_text)}
    </div>
    <section class="hero">
      <div class="hero-head">
        <div>
          <h1>{html_escape(title)}</h1>
          <div class="hero-sub">{html_escape(subtitle)}</div>
        </div>
        <div class="chips">
          {chip(str(meta.get("intake_scope_label", f"业务日 {date_text}")), "neutral")}
          {chip(f"流程时窗 {meta['business_window_label']}", "neutral")}
          {chip(f"生成 {meta['generated_at']}", "neutral")}
        </div>
      </div>
      <div class="metrics">
        <div class="metric"><div class="metric-label">信息 intake</div><div class="metric-value">{counts["source_packets"]}</div><div class="metric-sub">按业务窗统计的真实 intake，不按自然日</div></div>
        <div class="metric"><div class="metric-label">Top20</div><div class="metric-value">{counts["top20"]}</div><div class="metric-sub">signal-scout 收束对象</div></div>
        <div class="metric"><div class="metric-label">最终锁题</div><div class="metric-value">{counts["final_topics"]}</div><div class="metric-sub">approved topic 真实数量</div></div>
        <div class="metric"><div class="metric-label">草稿卡</div><div class="metric-value">{draft_value}</div><div class="metric-sub">{html_escape(draft_sub)}</div></div>
      </div>
    </section>
    {body}
    <div class="footer">控制台后端：{html_escape(current_console_base_url())} · 更新时间 {html_escape(now_cst())}</div>
  </main>
</body>
</html>"""


def warning_panel(warnings: list[str]) -> str:
    if not warnings:
        return '<div class="alert alert-success">当前页面没发现新的流程穿透问题。</div>'
    return '<div class="alert alert-danger"><ul>' + "".join(f"<li>{html_escape(item)}</li>" for item in warnings) + "</ul></div>"


def render_intake_page(snapshot: dict[str, Any], date_text: str) -> str:
    items = snapshot["sources"]["items"]
    platform_counts = snapshot["sources"]["platform_counts"]
    chips = "".join(
        chip(f"{builder.PLATFORM_CONFIG.get(platform, {}).get('label', platform)} {count}", "neutral")
        for platform, count in platform_counts
    )

    rows: list[str] = []
    for item in items:
        rows.append(
            "<tr>"
            f'<td style="width:57%"><div class="title-main" title="{html_escape(item["summary"])}">{html_escape(item["summary"])}</div><div class="title-sub" title="{html_escape(item["title"])}">{html_escape(item["title"])}</div></td>'
            f'<td style="width:5%" class="center-cell">{html_escape(builder.PLATFORM_CONFIG.get(item["platform"], {}).get("label", item["platform"]))}</td>'
            f'<td style="width:8%"><div title="{html_escape(item["source_name"])}">{html_escape(item["source_name"])}</div></td>'
            f'<td style="width:8%"><div title="{html_escape(item["heat_hint"])}">{html_escape(item["heat_hint"])}</div></td>'
            f'<td style="width:4%" class="center-cell">{html_escape(builder.label_for_primary_source(item["primary_source"]))}</td>'
            f'<td style="width:4%" class="center-cell">{html_escape(builder.label_for_quality(item["signal_quality"]))}</td>'
            f'<td style="width:4%" class="center-cell">{html_escape(builder.label_for_visual(item["visual_evidence_status"]))}</td>'
            f'<td style="width:6%"><div title="{html_escape(item["captured_at"])}">{html_escape(item["captured_at"])}</div></td>'
            f'<td style="width:4%"><div class="cell-actions">{external_link(item["canonical_url"], "原文")}{artifact_link(item["path"], "包文件")}</div></td>'
            "</tr>"
        )

    body = f"""
    <section class="panel">
      <div class="panel-head">
        <div>
          <h2 class="panel-title">今天到底拿回来了什么</h2>
          <div class="panel-sub">这里只展示最新业务日真实归档的信息；第一列是中文一句话概述，方便你快速扫一遍供给池。</div>
        </div>
        <div class="chips">{chips}</div>
      </div>
      <div class="summary-grid">
        <div class="summary-card"><strong>热度字段</strong>优先显示各源自己带回来的 `heat_hint`，不乱造伪统一分。</div>
        <div class="summary-card"><strong>点击逻辑</strong>`原文` 直跳外链，`包文件` 进入本地 artifact 查看页。</div>
        <div class="summary-card"><strong>展示重点</strong>描述列尽量完整展示，指标列只保留最必要的对比信息。</div>
      </div>
      <div class="filter-bar">
        <input id="intakeSearch" class="search-input" type="search" placeholder="筛关键词 / 平台 / 来源 / 热度">
      </div>
      <div class="table-wrap">
        <table id="intakeTable">
          <thead>
            <tr>
              <th>一句话概述</th>
              <th>平台</th>
              <th>来源</th>
              <th>热度线索</th>
              <th>一手性</th>
              <th>信号质量</th>
              <th>图像可用性</th>
              <th>抓取时间</th>
              <th>动作</th>
            </tr>
          </thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
      </div>
    </section>
    <script>
      const input = document.getElementById('intakeSearch');
      const table = document.getElementById('intakeTable');
      if (input && table) {{
        input.addEventListener('input', () => {{
          const keyword = input.value.trim().toLowerCase();
          table.querySelectorAll('tbody tr').forEach((row) => {{
            row.style.display = !keyword || row.innerText.toLowerCase().includes(keyword) ? '' : 'none';
          }});
        }});
      }}
    </script>
    """
    return page_shell(
        title="① 今日信息 Intake",
        subtitle="第一屏只回答一个问题：今天这套系统到底抓回来了哪些有用线索。",
        body=body,
        active_page="intake",
        snapshot=snapshot,
        date_text=date_text,
    )


def render_timeline_cards(logs: list[dict[str, Any]]) -> str:
    if not logs:
        return '<div class="alert alert-success">这一步当前还没有新的攻防记录。</div>'
    cards: list[str] = []
    for item in logs:
        cards.append(
            '<div class="timeline-card">'
            f'<div class="timeline-meta">{html_escape(item.get("ts", "n/a"))} · {html_escape(item.get("role", "n/a"))}</div>'
            f'<div class="timeline-headline">{html_escape(item.get("headline", "n/a"))}</div>'
            f'{chip(str(item.get("status", "n/a")), tone_for_status(str(item.get("status", "n/a"))))}'
            + list_html(list(item.get("highlights") or []))
            + f'<div class="timeline-actions">{artifact_link(str(item.get("source_path", "")), "查看记录")}</div>'
            + "</div>"
        )
    return '<div class="timeline">' + "".join(cards) + "</div>"


def tone_for_status(status: str) -> str:
    value = clean_text(status).lower()
    if "pass" in value or "ready" in value or "ok" in value or "waiting_human_publish" in value or value == "published":
        return "good"
    if "recommend" in value or "rebuild" in value or "warn" in value:
        return "warn"
    if "rework" in value or "missing" in value or "blocked" in value:
        return "bad"
    return "neutral"


def is_publish_ready_status(status: Any) -> bool:
    value = clean_text(status).lower()
    return value in {"draft_ready", "ready", "waiting_human_publish", "queued", "published"}


def render_top20_page(snapshot: dict[str, Any], date_text: str) -> str:
    top20 = snapshot["top20"]
    rows: list[str] = []
    for item in top20["candidates"]:
        breakdown = builder.parse_score_breakdown(item["score_breakdown"])
        rows.append(
            "<tr>"
            f'<td style="width:6%" class="center-cell">{item["rank"]}</td>'
            f'<td style="width:45%"><div class="title-main" title="{html_escape(item["header_title"])}">{html_escape(item["header_title"])}</div><div class="title-sub" title="{html_escape(item["signal_summary"])}">{html_escape(item["signal_summary"])}</div></td>'
            f'<td style="width:6%" class="center-cell">{html_escape(item["primary_platform"])}</td>'
            f'<td style="width:4%" class="center-cell">{html_escape(breakdown.get("一手性", "n/a"))}</td>'
            f'<td style="width:4%" class="center-cell">{html_escape(breakdown.get("传播性", "n/a"))}</td>'
            f'<td style="width:4%" class="center-cell">{html_escape(breakdown.get("破圈性", "n/a"))}</td>'
            f'<td style="width:6%" class="center-cell">{html_escape(item["score_total"])}</td>'
            f'<td style="width:18%"><div class="fulltext" title="{html_escape(item["why_in_top20"])}">{html_escape(item["why_in_top20"])}</div></td>'
            f'<td style="width:7%"><div class="cell-actions">{external_link(item["original_link"], "原文")}{artifact_link(top20["pack_path"], "Top20 包")}</div></td>'
            "</tr>"
        )

    body = f"""
    <section class="panel">
      <div class="panel-head">
        <div>
          <h2 class="panel-title">Top20 列表</h2>
          <div class="panel-sub">这一屏把候选池本身和攻防记录放在同一页，方便你判断：到底是供给问题、排序问题，还是流程前后不一致。</div>
        </div>
        <div class="chips">
          {chip(f'候选 {len(top20["candidates"])}', 'good')}
          {chip(f'修订 {top20["revision_note"]}', 'warn' if top20["revision_note"] != 'n/a' else 'neutral')}
        </div>
      </div>
      {warning_panel(top20["warnings"])}
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>入选信息</th>
              <th>主平台</th>
              <th>一手性</th>
              <th>传播性</th>
              <th>破圈性</th>
              <th>总分</th>
              <th>入选原因</th>
              <th>动作</th>
            </tr>
          </thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
      </div>
    </section>
    <section class="panel">
      <div class="panel-head">
        <div>
          <h2 class="panel-title">Top20 攻防记录</h2>
          <div class="panel-sub">这里只保留简洁的过程摘要：谁在什么时候提了什么问题、为什么打回、下一步该怎么修。</div>
        </div>
      </div>
      {render_timeline_cards(top20["logs"])}
    </section>
    """
    return page_shell(
        title="② Top20 候选池",
        subtitle="第二屏专门看 signal-scout 的候选池质量和这一步的 stage-gate 攻防。",
        body=body,
        active_page="top20",
        snapshot=snapshot,
        date_text=date_text,
    )


def render_selection_page(snapshot: dict[str, Any], date_text: str) -> str:
    selection = snapshot["selection"]
    rows: list[str] = []
    for item in selection["items"]:
        rows.append(
            "<tr>"
            f'<td style="width:7%" class="center-cell">{html_escape(item["selected_rank"])}</td>'
            f'<td style="width:36%"><div class="title-main" title="{html_escape(item["title"])}">{html_escape(item["title"])}</div><div class="title-sub" title="{html_escape(item["one_line_judgment"])}">{html_escape(item["one_line_judgment"])}</div></td>'
            f'<td style="width:10%"><div title="{html_escape(item["requested_platforms"])}">{html_escape(item["requested_platforms"])}</div></td>'
            f'<td style="width:18%"><div title="{html_escape(item["approved_angle"])}">{html_escape(item["approved_angle"])}</div></td>'
            f'<td style="width:16%"><div title="{html_escape(item["recommended_reason"])}">{html_escape(item["recommended_reason"])}</div></td>'
            f'<td style="width:8%" class="center-cell">{html_escape(item["status"])}</td>'
            f'<td style="width:5%"><div class="cell-actions">{artifact_link(item["path"], "题卡")}</div></td>'
            "</tr>"
        )
    if not rows:
        rows.append('<tr><td colspan="7">当前还没有锁题结果；这一页现在为 0，说明本轮还没有任何真正穿透到 `approved topic` 的对象。</td></tr>')
    body = f"""
    <section class="panel">
      <div class="panel-head">
        <div>
          <h2 class="panel-title">20 进几，最后留下了谁</h2>
          <div class="panel-sub">这一步用真实 `approved topic` 说话，而不是只看 markdown 计划稿，所以你能直接看见哪些对象已经真正穿透到了下游。</div>
        </div>
        <div class="chips">
          {chip(f'20 → {len(selection["items"])}', 'good')}
          {chip('approved topic = 真锁题对象', 'neutral')}
        </div>
      </div>
      {warning_panel(selection["warnings"])}
      <div class="summary-grid">
        <div class="summary-card"><strong>Top5 推荐板</strong>{artifact_link(selection["top5_board_path"], "查看 Top5 板")}</div>
        <div class="summary-card"><strong>平台任务单</strong>{artifact_link(selection["platform_task_sheet_path"], "查看任务单")}</div>
        <div class="summary-card"><strong>当前重点</strong>如果这里的锁题对象和裁判结果不一致，就说明流程已经穿透了。</div>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>原序号</th>
              <th>最终留下的题</th>
              <th>平台</th>
              <th>锁题角度</th>
              <th>入选原因</th>
              <th>状态</th>
              <th>动作</th>
            </tr>
          </thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
      </div>
    </section>
    <section class="panel">
      <div class="panel-head">
        <div>
          <h2 class="panel-title">锁题攻防记录</h2>
          <div class="panel-sub">方便你追问：为什么是这几个题，不是另外几个题。</div>
        </div>
      </div>
      {render_timeline_cards(selection["logs"])}
    </section>
    """
    return page_shell(
        title="③ 最终锁题",
        subtitle="第三屏只看从候选池到正式锁题的收束过程，以及这一步的流程一致性。",
        body=body,
        active_page="selection",
        snapshot=snapshot,
        date_text=date_text,
    )


def render_drafts_page(snapshot: dict[str, Any], date_text: str) -> str:
    drafts = snapshot["drafts"]
    items = sorted(
        drafts["items"],
        key=lambda row: (
            builder.PLATFORM_ORDER.index(row["platform"]) if row["platform"] in builder.PLATFORM_ORDER else 99,
            row["status"] == "missing",
            row["topic_key"],
        ),
    )
    inventory_items = sorted(
        drafts.get("inventory_items", []),
        key=lambda row: (
            builder.PLATFORM_ORDER.index(row["platform"]) if row["platform"] in builder.PLATFORM_ORDER else 99,
            row["topic_key"],
        ),
    )
    current_final_items = [item for item in items if is_publish_ready_status(item.get("status", ""))]
    current_keys = {(str(item.get("topic_key", "")), str(item.get("platform", ""))) for item in current_final_items}
    inventory_final_items = [
        item
        for item in inventory_items
        if is_publish_ready_status(item.get("status", ""))
        and (str(item.get("topic_key", "")), str(item.get("platform", ""))) not in current_keys
    ]

    current_nav_links: list[str] = []
    current_previews: list[str] = []
    for item in current_final_items:
        platform = str(item["platform"])
        config = builder.PLATFORM_CONFIG.get(platform, {"label": platform})
        anchor = f'{platform}-{item["topic_key"]}'.replace("_", "-")
        current_nav_links.append(
            f'<a class="preview-nav-link" href="#{html_escape(anchor)}">{html_escape(config["label"])}<span>{html_escape(item["topic_key"])}</span></a>'
        )
        current_previews.append(render_platform_preview(item))

    inventory_nav_links: list[str] = []
    inventory_previews: list[str] = []
    for item in inventory_final_items:
        platform = str(item["platform"])
        config = builder.PLATFORM_CONFIG.get(platform, {"label": platform})
        anchor = f'{platform}-{item["topic_key"]}'.replace("_", "-")
        inventory_nav_links.append(
            f'<a class="preview-nav-link" href="#{html_escape(anchor)}">{html_escape(config["label"])}<span>{html_escape(item["topic_key"])}</span></a>'
        )
        inventory_previews.append(render_platform_preview(item))

    if current_final_items:
        current_preview_nav_html = f'<div class="preview-nav">{"".join(current_nav_links)}</div>'
        current_preview_wall_html = f'<div class="preview-wall">{"".join(current_previews)}</div>'
    else:
        current_preview_nav_html = ""
        current_preview_wall_html = (
            '<div class="empty-note">今天 task sheet 主线还没真正长成可预发布成稿。'
            '这不代表系统没有稿件，下方继续展示当前库存中的可预发布 / 可发布稿。</div>'
        )

    if inventory_final_items:
        inventory_preview_nav_html = f'<div class="preview-nav">{"".join(inventory_nav_links)}</div>'
        inventory_preview_wall_html = f'<div class="preview-wall">{"".join(inventory_previews)}</div>'
    else:
        inventory_preview_nav_html = ""
        inventory_preview_wall_html = '<div class="empty-note">当前库存里也没有可预发布 / 可发布稿件。</div>'

    body = f"""
    <section class="panel">
      <div class="panel-head">
        <div>
          <h2 class="panel-title">平台发布仿真池</h2>
          <div class="panel-sub">这一屏把“今天主线成稿”和“当前可发布库存”拆开显示，避免旧题冒充今日主线，也避免稿件池被修空。</div>
        </div>
      </div>
      {warning_panel(drafts["warnings"])}
      <div class="summary-grid">
        <div class="summary-card"><strong>今日主线成稿</strong>当前命中 {len(current_final_items)} 个，严格对齐今天 task sheet / 锁题链路。</div>
        <div class="summary-card"><strong>库存可预发布稿</strong>当前命中 {len(inventory_final_items)} 个，用于展示系统手里已经可拿出来的真实稿件库存。</div>
        <div class="summary-card"><strong>当前展示逻辑</strong>展示 `draft_ready / ready / waiting_human_publish / queued / published`，但主线与库存分开看。</div>
        <div class="summary-card"><strong>图文策略</strong>优先展示真实截图与图卡；没有原图时，展示解释型配图，但不再把内部图位说明暴露到成品页。</div>
        <div class="summary-card"><strong>点击动作</strong>每篇右上角仍可打开原始 markdown 与 draft pack，便于继续精修。</div>
      </div>
      <div class="digest-block">
        <div class="digest-label">A. 今天主线成稿</div>
        {current_preview_nav_html}
        {current_preview_wall_html}
      </div>
      <div class="digest-block">
        <div class="digest-label">B. 当前可发布库存</div>
        {inventory_preview_nav_html}
        {inventory_preview_wall_html}
      </div>
    </section>
    """
    return page_shell(
        title="④ 稿件池 / 平台仿真",
        subtitle="第四屏直接回答一个问题：这些稿子如果现在发到各平台，用户看到的会是什么样子。",
        body=body,
        active_page="drafts",
        snapshot=snapshot,
        date_text=date_text,
    )


def render_learning_page(snapshot: dict[str, Any], learning_snapshot: dict[str, Any], date_text: str) -> str:
    overview = learning_snapshot["overview"]
    paths = learning_snapshot["paths"]
    samples = learning_snapshot["samples"]
    strategic_rotation = learning_snapshot.get("strategic_rotation", [])
    ready_drafts = learning_snapshot["ready_drafts"]
    gap_cards = learning_snapshot["gap_cards"]
    next_actions = learning_snapshot["next_actions"]
    optimization_items = sorted(
        learning_snapshot.get("optimization_items", []),
        key=lambda item: (item.get("status") == "dismissed", item.get("severity") != "high", item.get("title", "")),
    )
    optimization_events = list(reversed(learning_snapshot.get("optimization_events", [])[-10:]))

    source_mix = "".join(
        chip(f"{source} {count}", "neutral") for source, count in overview.get("sample_source_mix", [])
    ) or chip("暂无样本", "neutral")

    sample_rows: list[str] = []
    for sample in samples:
        sample_rows.append(
            "<tr>"
            f'<td style="width:8%">{html_escape(sample["source_name"])}</td>'
            f'<td style="width:30%"><div class="title-main" title="{html_escape(sample["title"])}">{html_escape(sample["title"])}</div><div class="title-sub fulltext">{html_escape(sample["hook_excerpt"])}</div></td>'
            f'<td style="width:11%">{html_escape(sample["published_at"])}</td>'
            f'<td style="width:5%" class="center-cell">{html_escape(sample["image_count"])}</td>'
            f'<td style="width:6%" class="center-cell">{html_escape(sample["first_image_after_text_paragraphs"] if sample["first_image_after_text_paragraphs"] is not None else "n/a")}</td>'
            f'<td style="width:24%"><div class="fulltext">{html_escape(sample["learning_takeaway"])}</div><div class="title-sub fulltext">{html_escape(sample["visual_takeaway"])}</div></td>'
            f'<td style="width:16%"><div class="cell-actions">{external_link(sample["canonical_url"], "原文")}{artifact_link(sample["path"], "deep article")}</div></td>'
            "</tr>"
        )

    strategic_rows: list[str] = []
    for item in strategic_rotation:
        strategic_rows.append(
            "<tr>"
            f'<td style="width:10%">{html_escape(item["source_name"])}</td>'
            f'<td style="width:10%">{chip(item["status_label"], "warn" if item.get("status") == "blocked" else "neutral")}</td>'
            f'<td style="width:28%"><div class="title-main" title="{html_escape(item["title"])}">{html_escape(item["title"])}</div><div class="title-sub fulltext">source_packet={html_escape(item["source_packet_count"])} / deep_article={html_escape(item["deep_article_count"])}</div></td>'
            f'<td style="width:12%">{html_escape(item["published_at"])}</td>'
            f'<td style="width:22%"><div class="fulltext">{html_escape(item["note"])}</div></td>'
            f'<td style="width:18%"><div class="cell-actions">{external_link(item["canonical_url"], "原文") if item.get("canonical_url") not in {"", "n/a"} else ""}{artifact_link(item["path"], "deep article") if item.get("path") not in {"", "n/a"} else ""}</div></td>'
            "</tr>"
        )

    draft_cards: list[str] = []
    for item in ready_drafts:
        strengths_html = list_html(list(item.get("strengths") or []))
        gaps_html = list_html(list(item.get("gaps") or []))
        draft_cards.append(
            '<div class="digest-card">'
            '<div class="digest-head">'
            f'<div><div class="digest-title">{html_escape(item["topic_title"])}</div><div class="digest-sub">{html_escape(item["topic_key"])} · {html_escape(" / ".join(item["platforms"]))}</div></div>'
            f'<div>{chip(item["representative_platform_label"], "good")}</div>'
            "</div>"
            f'<div class="digest-block"><div class="digest-label">当前预览</div><div class="fulltext">{html_escape(item["preview"])}</div></div>'
            f'<div class="digest-block"><div class="digest-label">已有长处</div>{strengths_html}</div>'
            f'<div class="digest-block"><div class="digest-label">当前差距</div>{gaps_html}</div>'
            '<div class="digest-block">'
            f'<div class="digest-label">动作</div><div class="cell-actions">{artifact_link(item["representative_path"], "稿件")}{artifact_link(item["pack_dir"], "draft pack")}</div>'
            f'<div class="digest-sub">视觉资产 {html_escape(item["visual_asset_count"])} 张 · section {html_escape(item["section_count"])}</div>'
            "</div>"
            "</div>"
        )

    gap_html = "".join(
        '<div class="digest-card">'
        '<div class="digest-head">'
        f'<div><div class="digest-title">{html_escape(card["title"])}</div><div class="digest-sub">{html_escape(card["why"])}</div></div>'
        f'<div>{chip(card["severity"], "bad" if card["severity"] == "high" else "warn" if card["severity"] == "medium" else "good")}</div>'
        "</div>"
        f'<div class="digest-block"><div class="digest-label">我们现在差在哪</div><div class="fulltext">{html_escape(card["current_gap"])}</div></div>'
        f'<div class="digest-block"><div class="digest-label">下一步</div><div class="fulltext">{html_escape(card["next_action"])}</div></div>'
        "</div>"
        for card in gap_cards
    )

    optimization_rows: list[str] = []
    for item in optimization_items:
        tone = "bad" if item.get("severity") == "high" else "warn" if item.get("severity") == "medium" else "good"
        targets = list(item.get("landing_targets") or [])
        actions = (
            button_form("恢复", "restore", item_id=str(item["id"]), date_text=date_text, kind="ghost")
            if item.get("status") == "dismissed"
            else button_form("取消优化", "dismiss", item_id=str(item["id"]), date_text=date_text, kind="ghost")
        )
        optimization_rows.append(
            "<tr>"
            f'<td style="width:20%"><div class="title-main">{html_escape(item["title"])}</div><div class="title-sub fulltext">{html_escape(item["why"])}</div></td>'
            f'<td style="width:12%">{html_escape(item["owner"])}</td>'
            f'<td style="width:12%">{html_escape(item["landing_layer"])}</td>'
            f'<td style="width:12%">{chip(item["status_label"], tone if item.get("status") == "active" else "neutral")}</td>'
            f'<td style="width:18%"><div class="fulltext">{html_escape(item["current_gap"])}</div></td>'
            f'<td style="width:18%"><div class="fulltext">{html_escape(item["next_action"])}</div><div class="title-sub fulltext">{html_escape("；".join(targets))}</div></td>'
            f'<td style="width:8%"><div class="cell-actions">{actions}</div></td>'
            "</tr>"
        )

    optimization_event_html = list_html(
        [
            f'{item.get("recorded_at", "n/a")}｜{item.get("actor", "system")}｜{item.get("item_id", "n/a")}｜{item.get("action", "n/a")}'
            for item in optimization_events
        ]
    )

    board_actions = (
        artifact_link(paths.get("markdown", ""), "学习池 md")
        + artifact_link(paths.get("json", ""), "学习池 JSON")
        + artifact_link(paths.get("rulebook_markdown", ""), "规则手册")
    )

    body = f"""
    <section class="panel">
      <div class="panel-head">
        <div>
          <h2 class="panel-title">头部号学习池 / 对标池</h2>
          <div class="panel-sub">这一屏只回答两个问题：别人怎么写，我们现在还差哪几刀。</div>
        </div>
        <div class="chips">{source_mix}</div>
      </div>
      <div class="summary-grid">
        <div class="summary-card"><strong>学习样本</strong>{overview["sample_count"]} 条深抓样本，持续从头部号里抽结构、开头和图文节奏。</div>
        <div class="summary-card"><strong>战略号轮转</strong>{overview.get("strategic_rotation_count", len(strategic_rotation))} 个账号进入补位视图，其中阻塞 {overview.get("strategic_rotation_blocked", 0)} 个。</div>
        <div class="summary-card"><strong>当前 ready 主题</strong>{overview["ready_topic_count"]} 个 topic 已进入对标池，直接跟样本做差异比对。</div>
        <div class="summary-card"><strong>样本首图节奏</strong>首图前文字段落中位数：`{html_escape(overview["median_first_image_after_text_paragraphs"] if overview["median_first_image_after_text_paragraphs"] is not None else "n/a")}`。</div>
        <div class="summary-card"><strong>板面产物</strong><div class="cell-actions">{board_actions}</div></div>
      </div>
      <div class="summary-grid">
        {"".join(f'<div class="summary-card"><strong>学习结论</strong>{html_escape(item)}</div>' for item in overview.get("takeaways", []))}
      </div>
    </section>
    <section class="panel">
      <div class="panel-head">
        <div>
          <h2 class="panel-title">学习样本池</h2>
          <div class="panel-sub">这里看真实深抓样本，不只看标题，也看开头和图证节奏。</div>
        </div>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>来源</th>
              <th>标题 / 开头</th>
              <th>发布时间</th>
              <th>图片数</th>
              <th>首图前文字</th>
              <th>值得学什么</th>
              <th>动作</th>
            </tr>
          </thead>
          <tbody>{"".join(sample_rows)}</tbody>
        </table>
      </div>
    </section>
    <section class="panel">
      <div class="panel-head">
        <div>
          <h2 class="panel-title">战略号轮转补位</h2>
          <div class="panel-sub">主学习池仍然只看当天业务窗；这里专门显示战略账号的轮转学习状态，以及还没跑通的主链阻塞。</div>
        </div>
      </div>
      <div class="table-wrap">
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
          <tbody>{"".join(strategic_rows) if strategic_rows else '<tr><td colspan="6">当前没有战略号补位样本。</td></tr>'}</tbody>
        </table>
      </div>
    </section>
    <section class="panel">
      <div class="panel-head">
        <div>
          <h2 class="panel-title">当前 ready 稿对照</h2>
          <div class="panel-sub">把今天已经 ready 的稿件直接拉进来，看“已有长处”和“当前差距”。</div>
        </div>
      </div>
      <div class="digest-grid">{"".join(draft_cards) if draft_cards else '<div class="summary-card">当前没有 ready 稿件可对照。</div>'}</div>
    </section>
    <section class="panel">
      <div class="panel-head">
        <div>
          <h2 class="panel-title">我们差在哪</h2>
          <div class="panel-sub">这里只保留高杠杆问题，不做碎碎念。</div>
        </div>
      </div>
      <div class="digest-grid">{gap_html}</div>
      <div class="digest-block">
        <div class="digest-label">下一步动作</div>
        {list_html(next_actions)}
      </div>
    </section>
    <section class="panel">
      <div class="panel-head">
        <div>
          <h2 class="panel-title">优化建议表</h2>
          <div class="panel-sub">这层是学习结果的真实落地队列。你可以手动取消某条优化，系统会把状态记下来。</div>
        </div>
      </div>
      <div class="summary-grid">
        <div class="summary-card"><strong>待优化</strong>{overview.get("optimization_active", 0)} 条仍在队列中。</div>
        <div class="summary-card"><strong>已取消</strong>{overview.get("optimization_dismissed", 0)} 条被人工取消。</div>
        <div class="summary-card"><strong>规则手册</strong>核心岗位 skill 现在可读取稳定规则文件。</div>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>建议</th>
              <th>Owner</th>
              <th>落地层</th>
              <th>状态</th>
              <th>当前差距</th>
              <th>下一步 / 落点</th>
              <th>动作</th>
            </tr>
          </thead>
          <tbody>{"".join(optimization_rows) if optimization_rows else '<tr><td colspan="7">当前没有优化建议。</td></tr>'}</tbody>
        </table>
      </div>
      <div class="digest-block">
        <div class="digest-label">最近状态变更</div>
        {optimization_event_html}
      </div>
    </section>
    """
    return page_shell(
        title="⑤ 学习池 / 对标池",
        subtitle="第五屏把头部号学习结果和当前 ready 稿放在一起，直接看“别人怎么写、我们差在哪”。",
        body=body,
        active_page="learning",
        snapshot=snapshot,
        date_text=date_text,
    )


def render_artifact_page(path_text: str, date_text: str) -> tuple[int, str]:
    resolved = normalize_path(path_text)
    if not resolved or not resolved.exists():
        html = page_shell(
            title="Artifact 不存在",
            subtitle="这个点击动作已经连到后端了，但路径不存在或不在允许范围内。",
            body='<section class="panel"><div class="alert alert-danger">找不到对应文件，请回到控制台刷新后再试。</div></section>',
            active_page="intake",
            snapshot={"counts": {"source_packets": 0, "top20": 0, "final_topics": 0, "draft_cards": 0}, "meta": {"business_window_label": "-", "generated_at": now_cst()}, "anomalies": []},
            date_text=date_text,
        )
        return HTTPStatus.NOT_FOUND, html

    meta = f'<div class="artifact-meta"><span>路径：{html_escape(str(resolved))}</span><span>大小：{resolved.stat().st_size} bytes</span><span>更新时间：{datetime.fromtimestamp(resolved.stat().st_mtime, tz=CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")}</span></div>'
    actions = f'<div class="timeline-actions">{button_link("返回 Intake", f"/intake?date={quote(date_text)}")}{artifact_link(str(resolved.parent), "查看上级路径")}</div>'
    if resolved.is_dir():
        entries = []
        for child in sorted(resolved.iterdir())[:200]:
            label = f"{child.name}/" if child.is_dir() else child.name
            entries.append(f'<li><a href="/artifact?path={quote(str(child))}">{html_escape(label)}</a></li>')
        body = f"""
        <section class="panel">
          <div class="panel-head">
            <div>
              <h2 class="panel-title">{html_escape(resolved.name or str(resolved))}</h2>
              <div class="panel-sub">这是目录视图。点击下方任一条目即可继续打开。</div>
            </div>
          </div>
          {meta}
          {actions}
          <div class="panel"><ul class="bullet-list">{''.join(entries) if entries else '<li>空目录</li>'}</ul></div>
        </section>
        """
        html = page_shell(
            title="Artifact Viewer",
            subtitle="点击动作已绑定到后端 artifact 查看逻辑。",
            body=body,
            active_page="intake",
            snapshot={"counts": {"source_packets": 0, "top20": 0, "final_topics": 0, "draft_cards": 0}, "meta": {"business_window_label": "-", "generated_at": now_cst()}, "anomalies": []},
            date_text=date_text,
        )
        return HTTPStatus.OK, html

    text = resolved.read_text(encoding="utf-8", errors="replace")
    body = f"""
    <section class="panel">
      <div class="panel-head">
        <div>
          <h2 class="panel-title">{html_escape(resolved.name)}</h2>
          <div class="panel-sub">这是本地 artifact 查看页。所有“查看文件 / 题卡 / 包文件 / 查看记录”都会落到这里，而不是空点。</div>
        </div>
      </div>
      {meta}
      {actions}
      <pre class="code-view">{html_escape(text)}</pre>
    </section>
    """
    html = page_shell(
        title="Artifact Viewer",
        subtitle="点击动作已绑定到后端 artifact 查看逻辑。",
        body=body,
        active_page="intake",
        snapshot={"counts": {"source_packets": 0, "top20": 0, "final_topics": 0, "draft_cards": 0}, "meta": {"business_window_label": "-", "generated_at": now_cst()}, "anomalies": []},
        date_text=date_text,
    )
    return HTTPStatus.OK, html


class MarketConsoleHandler(BaseHTTPRequestHandler):
    server_version = "MarketOpsConsole/0.1"

    def log_message(self, format: str, *args: Any) -> None:
        log_path = STATE_DIR / "console-access.log"
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        line = "%s - - [%s] %s\n" % (self.client_address[0], self.log_date_time_string(), format % args)
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(line)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        date_text = query.get("date", [today_cn()])[0]
        force = query.get("refresh", ["0"])[0] == "1"

        if parsed.path == "/health":
            self.send_text(HTTPStatus.OK, "ok")
            return

        if parsed.path == "/api/snapshot":
            snapshot = read_snapshot(date_text, self.server.window_start, self.server.window_end, force=force)
            self.send_json(snapshot)
            return

        if parsed.path == "/artifact":
            path_text = unquote(query.get("path", [""])[0])
            status, html = render_artifact_page(path_text, date_text)
            self.send_html(status, html)
            return

        if parsed.path in {"/today", "/latest"}:
            self.redirect(f"/intake?date={quote(today_cn())}&refresh=1")
            return

        snapshot = read_snapshot(date_text, self.server.window_start, self.server.window_end, force=force)

        if parsed.path in {"", "/"}:
            self.redirect(DEFAULT_ENTRY_PATH)
            return
        if parsed.path == "/intake":
            self.send_html(HTTPStatus.OK, render_intake_page(snapshot, date_text))
            return
        if parsed.path == "/top20":
            self.send_html(HTTPStatus.OK, render_top20_page(snapshot, date_text))
            return
        if parsed.path in {"/selection", "/finals"}:
            self.send_html(HTTPStatus.OK, render_selection_page(snapshot, date_text))
            return
        if parsed.path == "/drafts":
            self.send_html(HTTPStatus.OK, render_drafts_page(snapshot, date_text))
            return
        if parsed.path == "/learning":
            learning_snapshot = read_learning_snapshot(date_text, force=force)
            self.send_html(HTTPStatus.OK, render_learning_page(snapshot, learning_snapshot, date_text))
            return

        self.send_html(HTTPStatus.NOT_FOUND, "<h1>404</h1>")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length > 0 else b""
        form = parse_qs(raw.decode("utf-8", "ignore"))
        date_text = form.get("date", [today_cn()])[0]

        if parsed.path == "/learning/optimization":
            item_id = form.get("item_id", [""])[0].strip()
            action = form.get("action", ["dismiss"])[0].strip() or "dismiss"
            if not item_id:
                self.send_text(HTTPStatus.BAD_REQUEST, "missing item_id")
                return
            learning_builder.record_optimization_action(date_text, item_id, action, actor="dashboard")
            with _CACHE_LOCK:
                _LEARNING_CACHE.pop(date_text, None)
            self.redirect(f"/learning?date={quote(date_text)}&refresh=1")
            return

        self.send_text(HTTPStatus.NOT_FOUND, "not found")

    def do_HEAD(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", "2")
            self.end_headers()
            return
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

    def redirect(self, location: str) -> None:
        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", location)
        self.end_headers()

    def send_html(self, status: int, body: str) -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def send_text(self, status: int, body: str) -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def send_json(self, payload: dict[str, Any]) -> None:
        raw = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


class MarketConsoleHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def make_server(host: str, port: int, default_date: str, window_start: str, window_end: str) -> ThreadingHTTPServer:
    httpd = MarketConsoleHTTPServer((host, port), MarketConsoleHandler)
    httpd.default_date = default_date
    httpd.window_start = window_start
    httpd.window_end = window_end
    return httpd


def write_state_file(host: str, port: int, default_date: str) -> Path:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_path = STATE_DIR / "market-ops-console.json"
    state_path.write_text(
        json.dumps(
            {
                "host": host,
                "port": port,
                "default_date": default_date,
                "started_at": now_cst(),
                "base_url": f"http://{host}:{port}",
                "entry_path": DEFAULT_ENTRY_PATH,
                "entry_url": f"http://{host}:{port}{DEFAULT_ENTRY_PATH}",
                "today_url": f"http://{host}:{port}/today",
                "pid": os.getpid(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return state_path


def main() -> None:
    args = parse_args()
    server = make_server(args.host, args.port, args.date, args.window_start, args.window_end)
    write_state_file(args.host, args.port, args.date)
    print(f"http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import mimetypes
import os
import platform
import re
import ssl
import sys
import tempfile
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from wechat_bridge_official_metrics_sync import sync_official_metrics

try:
    import certifi  # type: ignore

    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except Exception:
    SSL_CONTEXT = ssl.create_default_context()


TITLE_RE = re.compile(r"^- 标题：(.+?)\s*$")
TOP_HEADING_RE = re.compile(r"^#\s+(.+?)\s*$")
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
H3_RE = re.compile(r"^###\s+(.+?)\s*$")
IMAGE_LINE_RE = re.compile(r"^!\[(.*?)\]\((.+?)\)\s*$")
URL_RE = re.compile(r"https?://[^\s)]+")
QUEUE_KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
HORIZONTAL_RULE_RE = re.compile(r"^([*\-_])\1{2,}$")
BRAND_SECTION = "品牌签名"
FOLLOW_SECTION = "关注我们"
SKIP_SECTIONS = {"推荐包装", "标题候选"}
HIDDEN_HEADING_SECTIONS = {"开头", "轻 CTA", BRAND_SECTION, FOLLOW_SECTION}
DEFAULT_BRAND_NAME = "同行资本 TH Capital"
DEFAULT_BRAND_SLOGAN = "研究 AI、Agent 与一人公司的真实变化。"
DEFAULT_BRAND_DESCRIPTION = "看热点，也看热点背后的结构变化。"
DEFAULT_FOLLOW_PROMPT = "如果这篇内容对你有帮助，欢迎在微信里搜索「同行资本 TH Capital」关注我们。"
DEFAULT_FOLLOW_DESCRIPTION = "这里会持续更新 AI、Agent 与一人公司的真实案例、流程拆解与业务判断。"
DEFAULT_FOLLOW_ACTION = "微信搜索：同行资本 TH Capital"
CONSUMER_VERSION = "2026-04-01-wechat-layout-system-v1"
CN_TZ = ZoneInfo("Asia/Shanghai")
MORNING_FLASH_EXPIRE_GRACE = timedelta(hours=2)
DAY_MAINLINE_EXPIRE_GRACE = timedelta(hours=2, minutes=30)
GENERIC_REQUEST_EXPIRE_GRACE = timedelta(hours=24)

if os.name == "nt":
    import ctypes

    ERROR_ALREADY_EXISTS = 183
    INVALID_HANDLE_VALUE = 0
else:
    ctypes = None
    ERROR_ALREADY_EXISTS = 183
    INVALID_HANDLE_VALUE = 0


def now_iso() -> str:
    return datetime.now().astimezone().isoformat()


class WindowsSingleInstanceGuard:
    def __init__(self, name: str):
        self.name = name
        self.handle = None
        self.acquired = False

    def acquire(self) -> bool:
        if os.name != "nt" or ctypes is None:
            self.acquired = True
            return True
        kernel32 = ctypes.windll.kernel32
        kernel32.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_wchar_p]
        kernel32.CreateMutexW.restype = ctypes.c_void_p
        kernel32.GetLastError.restype = ctypes.c_uint32
        handle = kernel32.CreateMutexW(None, True, self.name)
        if not handle or handle == INVALID_HANDLE_VALUE:
            raise RuntimeError("CreateMutexW failed")
        self.handle = handle
        last_error = kernel32.GetLastError()
        if last_error == ERROR_ALREADY_EXISTS:
            return False
        self.acquired = True
        return True

    def release(self) -> None:
        if os.name != "nt" or ctypes is None or not self.handle:
            return
        kernel32 = ctypes.windll.kernel32
        if self.acquired:
            try:
                kernel32.ReleaseMutex(self.handle)
            except Exception:
                pass
        try:
            kernel32.CloseHandle(self.handle)
        except Exception:
            pass
        self.handle = None


def watch_mutex_name(root_dir: Path) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "_", str(root_dir).lower()).strip("_")
    suffix = normalized[-40:] if normalized else "default"
    return f"Local\\THCapital-WeChat-Bridge-{suffix}"


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return value if value else fallback


def default_layout_config() -> dict:
    return {
        "brand": {
            "badge": "TH Capital",
            "name": DEFAULT_BRAND_NAME,
            "slogan": "把 AI、Agent 与一人公司的变化讲明白。",
            "description": "看热点，也看热点背后的结构变化。",
            "accent": "#0f4c81",
            "secondary": "#1d4ed8",
            "surface": "#f5f9ff",
            "border": "#dbe7ff",
            "title_color": "#0f172a",
            "body_color": "#475569",
        },
        "follow": {
            "label": "继续关注",
            "prompt": DEFAULT_FOLLOW_PROMPT,
            "description": DEFAULT_FOLLOW_DESCRIPTION,
            "action": DEFAULT_FOLLOW_ACTION,
            "profile_url": "",
            "surface": "#f8fafc",
            "border": "#e2e8f0",
            "accent": "#0f4c81",
            "pill_surface": "#e9f2ff",
            "pill_text": "#1d4ed8",
            "label_color": "#64748b",
            "title_color": "#0f172a",
            "body_color": "#475569",
        },
        "heading": {
            "h2_text": "#0f172a",
            "h2_accent": "#1f6feb",
            "h2_rule": "#bfdbfe",
            "h3_surface": "#edf5ff",
            "h3_border": "#cfe0ff",
            "h3_text": "#1d4ed8",
        },
    }


def deep_merge(base: dict, overrides: dict) -> dict:
    merged = dict(base)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_layout_config(root_dir: Path) -> dict:
    config = default_layout_config()
    config_path = root_dir / "brand_layout_config.json"
    if not config_path.exists():
        return config
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        return config
    if isinstance(payload, dict):
        return deep_merge(config, payload)
    return config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Windows WeChat draft-box bridge consumer.")
    parser.add_argument("--root-dir", default=str(Path(__file__).resolve().parents[1]), help="Bridge outbox root directory")
    parser.add_argument("--appid", default="", help="Override WeChat AppID")
    parser.add_argument("--secret", default="", help="Override WeChat AppSecret")
    parser.add_argument("--watch", action="store_true", help="Watch for new requests continuously")
    parser.add_argument("--interval", type=int, default=20, help="Watch polling interval seconds")
    return parser.parse_args()


def credentials_path() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
        return base / "THCapital" / "wechat-bridge" / "credentials.json"
    return Path.home() / ".config" / "thcapital" / "wechat-bridge" / "credentials.json"


def credential_candidates() -> list[Path]:
    candidates = [credentials_path()]
    if os.name != "nt":
        candidates.extend(
            [
                Path.home() / ".config" / "THCapital" / "wechat-bridge" / "credentials.json",
                Path.home() / "Library" / "Application Support" / "THCapital" / "wechat-bridge" / "credentials.json",
            ]
        )
    return candidates


def load_credentials(appid_override: str, secret_override: str) -> tuple[str, str]:
    appid = (appid_override or os.environ.get("TH_WECHAT_APPID", "")).strip()
    secret = (secret_override or os.environ.get("TH_WECHAT_APPSECRET", "")).strip()
    if appid and secret:
        return appid, secret
    for path in credential_candidates():
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        appid = appid or str(payload.get("appid", "")).strip()
        secret = secret or str(payload.get("secret", "")).strip()
        if appid and secret:
            break
    if not appid or not secret:
        raise RuntimeError(
            "WeChat credentials missing. Set TH_WECHAT_APPID / TH_WECHAT_APPSECRET "
            f"or create one of: {', '.join(str(path) for path in credential_candidates())}"
        )
    return appid, secret


def request_dirs(root_dir: Path) -> list[Path]:
    requests_dir = root_dir / "requests"
    if not requests_dir.exists():
        return []
    return sorted([path for path in requests_dir.iterdir() if path.is_dir()])


def request_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def result_needs_refresh(result_path: Path, request_path: Path, inline_image_count: int) -> bool:
    if not result_path.exists():
        return True
    try:
        payload = request_json(result_path)
    except Exception:
        return True
    status = clean(str(payload.get("status", "")), "")
    if status in {"skipped_expired", "skipped_queue_closed"}:
        try:
            return request_path.stat().st_mtime_ns > result_path.stat().st_mtime_ns
        except FileNotFoundError:
            return True
    if status != "success":
        return True
    # If the request was rewritten after the result was produced, rebuild it.
    try:
        if request_path.stat().st_mtime_ns > result_path.stat().st_mtime_ns:
            return True
    except FileNotFoundError:
        return True
    # Older consumer versions succeeded but did not upload/record inline images.
    if inline_image_count > 0 and "inline_image_count" not in payload:
        return True
    if inline_image_count > 0 and int(payload.get("inline_image_count") or 0) < inline_image_count:
        return True
    # A consumer code/layout upgrade should not silently republish old successful drafts.
    # Historical requests should refresh only when the request package changes or when
    # the recorded success payload is incomplete/corrupted.
    return False


def write_debug_html(request_dir: Path, content_html: str) -> Path:
    debug_path = request_dir / "rendered_content.html"
    debug_path.write_text(content_html, encoding="utf-8")
    return debug_path


def result_is_done(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        payload = request_json(path)
    except Exception:
        return False
    return payload.get("status") == "success"


def parse_queue_item_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    if not path.exists():
        return fields
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = QUEUE_KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def parse_cn_dt(value: str) -> datetime | None:
    normalized = clean(value, "")
    if not normalized or normalized == "n/a":
        return None
    stripped = normalized.replace(" CST", "").strip()
    try:
        return datetime.strptime(stripped, "%Y-%m-%d %H:%M:%S").replace(tzinfo=CN_TZ)
    except ValueError:
        pass
    try:
        parsed = datetime.fromisoformat(stripped)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=CN_TZ)
    return parsed.astimezone(CN_TZ)


def request_expiry_reason(request: dict) -> str:
    queue_item_path_raw = clean(str(((request.get("paths") or {}).get("queue_item_path") or "")), "")
    if not queue_item_path_raw or queue_item_path_raw == "n/a":
        return ""
    queue_item_path = Path(queue_item_path_raw).expanduser()
    if not queue_item_path.exists():
        return ""
    fields = parse_queue_item_fields(queue_item_path)
    queue_status = clean(fields.get("status", ""), "")
    if queue_status in {"published", "cancelled"}:
        return f"queue_{queue_status}"
    delivery_lane = clean(fields.get("delivery_lane", ""), "")
    delivery_deadline = parse_cn_dt(fields.get("delivery_deadline", ""))
    planned_publish_at = parse_cn_dt(fields.get("planned_publish_at", ""))
    anchor_dt = delivery_deadline or planned_publish_at or parse_cn_dt(str(request.get("created_at", "")))
    if anchor_dt is None:
        return ""
    if delivery_lane == "morning_flash":
        expire_at = anchor_dt + MORNING_FLASH_EXPIRE_GRACE
    elif delivery_lane == "day_mainline":
        expire_at = anchor_dt + DAY_MAINLINE_EXPIRE_GRACE
    else:
        expire_at = anchor_dt + GENERIC_REQUEST_EXPIRE_GRACE
    if datetime.now(CN_TZ) > expire_at:
        return f"expired_{delivery_lane or 'request'}"
    return ""


def escape_text(value: str) -> str:
    return html.escape(value, quote=False)


def escape_attr(value: str) -> str:
    return html.escape(value, quote=True)


def truncate_utf8_bytes(value: str, max_bytes: int) -> str:
    raw = (value or "").strip()
    if len(raw.encode("utf-8")) <= max_bytes:
        return raw
    buffer: list[str] = []
    used = 0
    for char in raw:
        size = len(char.encode("utf-8"))
        if used + size > max_bytes:
            break
        buffer.append(char)
        used += size
    return "".join(buffer).strip()


def format_inline(value: str) -> str:
    escaped = escape_text(value)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*(.+?)\*", r"<em>\1</em>", escaped)
    return escaped


def normalize_markdown_asset_path(raw: str) -> str:
    return raw.strip().strip("<>").strip().split(maxsplit=1)[0].replace("\\", "/")


def section_paragraphs(lines: list[str]) -> list[str]:
    paragraphs: list[str] = []
    buffer: list[str] = []
    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            if buffer:
                paragraphs.append(" ".join(buffer).strip())
                buffer = []
            continue
        if stripped.startswith(("- ", "* ")):
            stripped = stripped[2:].strip()
        buffer.append(stripped)
    if buffer:
        paragraphs.append(" ".join(buffer).strip())
    return paragraphs


def first_url(*values: str) -> str:
    for value in values:
        match = URL_RE.search(value or "")
        if match:
            return match.group(0)
    return ""


def render_brand_card(lines: list[str], layout_config: dict) -> tuple[str, list[str]]:
    brand = layout_config.get("brand", {})
    paragraphs = section_paragraphs(lines)
    default_badge = clean(str(brand.get("badge", "TH Capital")), "TH Capital")
    default_name = clean(str(brand.get("name", DEFAULT_BRAND_NAME)), DEFAULT_BRAND_NAME)
    default_slogan = clean(str(brand.get("slogan", DEFAULT_BRAND_SLOGAN)), DEFAULT_BRAND_SLOGAN)
    default_description = clean(str(brand.get("description", DEFAULT_BRAND_DESCRIPTION)), DEFAULT_BRAND_DESCRIPTION)
    if len(paragraphs) >= 4:
        badge, name, slogan, description = paragraphs[0], paragraphs[1], paragraphs[2], paragraphs[3]
    elif len(paragraphs) == 3:
        badge, name, slogan, description = default_badge, paragraphs[0], paragraphs[1], paragraphs[2]
    else:
        badge = paragraphs[0] if paragraphs else default_badge
        name = paragraphs[1] if len(paragraphs) > 1 else default_name
        slogan = paragraphs[2] if len(paragraphs) > 2 else default_slogan
        description = paragraphs[3] if len(paragraphs) > 3 else default_description
    accent = clean(str(brand.get("accent", "#0f4c81")), "#0f4c81")
    secondary = clean(str(brand.get("secondary", "#1d4ed8")), "#1d4ed8")
    surface = clean(str(brand.get("surface", "#f5f9ff")), "#f5f9ff")
    border = clean(str(brand.get("border", "#dbe7ff")), "#dbe7ff")
    title_color = clean(str(brand.get("title_color", "#0f172a")), "#0f172a")
    body_color = clean(str(brand.get("body_color", "#475569")), "#475569")
    html_block = (
        '<section style="margin:10px 0 22px;padding:18px 18px 16px;border-radius:20px;'
        f'background-color:{surface};border:1px solid {border};">'
        '<p style="margin:0 0 10px;">'
        '<span style="display:inline-block;padding:4px 10px;border-radius:999px;'
        f'background-color:{accent};color:#ffffff;font-size:12px;font-weight:700;">'
        f"{escape_text(badge)}"
        "</span>"
        "</p>"
        f'<p style="margin:0;font-size:22px;line-height:1.38;font-weight:700;color:{title_color};">{format_inline(name)}</p>'
        f'<p style="margin:10px 0 0;font-size:16px;line-height:1.8;color:{secondary};font-weight:600;">{format_inline(slogan)}</p>'
        f'<div style="width:68px;height:3px;border-radius:999px;background:{secondary};opacity:0.18;margin-top:10px;"></div>'
        f'<p style="margin:10px 0 0;font-size:14px;line-height:1.8;color:{body_color};">{format_inline(description)}</p>'
        "</section>"
    )
    plain = [badge, name, slogan, description]
    return html_block, plain


def render_follow_card(lines: list[str], layout_config: dict) -> tuple[str, list[str]]:
    follow = layout_config.get("follow", {})
    paragraphs = section_paragraphs(lines)
    label = clean(str(follow.get("label", "继续关注")), "继续关注")
    prompt = paragraphs[0] if paragraphs else clean(str(follow.get("prompt", DEFAULT_FOLLOW_PROMPT)), DEFAULT_FOLLOW_PROMPT)
    description = paragraphs[1] if len(paragraphs) > 1 else clean(str(follow.get("description", DEFAULT_FOLLOW_DESCRIPTION)), DEFAULT_FOLLOW_DESCRIPTION)
    action = paragraphs[2] if len(paragraphs) > 2 else clean(str(follow.get("action", DEFAULT_FOLLOW_ACTION)), DEFAULT_FOLLOW_ACTION)
    profile_url = first_url(prompt, description, action, clean(str(follow.get("profile_url", "")), ""))
    surface = clean(str(follow.get("surface", "#f8fafc")), "#f8fafc")
    border = clean(str(follow.get("border", "#e2e8f0")), "#e2e8f0")
    accent = clean(str(follow.get("accent", "#0f4c81")), "#0f4c81")
    pill_surface = clean(str(follow.get("pill_surface", "#e9f2ff")), "#e9f2ff")
    pill_text = clean(str(follow.get("pill_text", "#1d4ed8")), "#1d4ed8")
    label_color = clean(str(follow.get("label_color", "#64748b")), "#64748b")
    title_color = clean(str(follow.get("title_color", "#0f172a")), "#0f172a")
    body_color = clean(str(follow.get("body_color", "#475569")), "#475569")
    if profile_url:
        action_html = (
            f'<a href="{escape_attr(profile_url)}" '
            'style="display:inline-block;margin-top:10px;padding:7px 12px;border-radius:999px;'
            f'background-color:{accent};color:#ffffff;font-size:13px;font-weight:700;text-decoration:none;">'
            f"{escape_text(action.replace(profile_url, '').strip('：: ') or '查看公众号主页')}"
            "</a>"
        )
    else:
        action_html = (
            '<p style="margin:10px 0 0;">'
            '<span style="display:inline-block;padding:7px 12px;border-radius:999px;'
            f'background-color:{pill_surface};color:{pill_text};font-size:13px;font-weight:700;">'
            f"{format_inline(action)}"
            "</span>"
            "</p>"
        )
    html_block = (
        '<section style="margin:24px 0;padding:16px 18px;border-radius:18px;'
        f'background-color:{surface};border:1px solid {border};">'
        '<p style="margin:0 0 8px;font-size:12px;line-height:1.5;letter-spacing:0.2px;'
        f'text-transform:uppercase;color:{label_color};font-weight:700;">{escape_text(label)}</p>'
        f'<p style="margin:0;font-size:16px;line-height:1.8;color:{title_color};font-weight:600;">{format_inline(prompt)}</p>'
        f'<p style="margin:8px 0 0;font-size:14px;line-height:1.8;color:{body_color};">{format_inline(description)}</p>'
        f"{action_html}"
        "</section>"
    )
    plain = [prompt, description, action]
    return html_block, plain


def render_h2_heading(title: str, layout_config: dict) -> str:
    heading = layout_config.get("heading", {})
    h2_text = clean(str(heading.get("h2_text", "#0f172a")), "#0f172a")
    h2_accent = clean(str(heading.get("h2_accent", "#1f6feb")), "#1f6feb")
    h2_rule = clean(str(heading.get("h2_rule", "#bfdbfe")), "#bfdbfe")
    return (
        '<section style="margin:30px 0 14px;padding-left:14px;'
        f'border-left:4px solid {h2_accent};">'
        f'<p style="margin:0;font-size:22px;line-height:1.55;font-weight:700;color:{h2_text};">{escape_text(title)}</p>'
        f'<div style="width:78px;height:2px;border-radius:999px;background:{h2_rule};margin-top:10px;"></div>'
        "</section>"
    )


def render_h3_heading(title: str, layout_config: dict) -> str:
    heading = layout_config.get("heading", {})
    h3_surface = clean(str(heading.get("h3_surface", "#edf5ff")), "#edf5ff")
    h3_border = clean(str(heading.get("h3_border", "#cfe0ff")), "#cfe0ff")
    h3_text = clean(str(heading.get("h3_text", "#1d4ed8")), "#1d4ed8")
    return (
        '<section style="margin:20px 0 8px;">'
        '<span style="display:inline-block;max-width:100%;padding:5px 10px;border-radius:999px;'
        f'background-color:{h3_surface};color:{h3_text};font-size:15px;line-height:1.5;font-weight:700;'
        f'border:1px solid {h3_border};">'
        f"{escape_text(title)}"
        "</span>"
        "</section>"
    )


def extract_title(markdown: str, fallback: str) -> str:
    for raw in markdown.splitlines():
        match = TITLE_RE.match(raw.strip())
        if match:
            return match.group(1).strip()
    for raw in markdown.splitlines():
        match = TOP_HEADING_RE.match(raw.strip())
        if match:
            heading = match.group(1).replace("微信稿｜", "").replace("微信稿|", "").strip()
            if heading:
                return heading
    return fallback


def split_sections(markdown: str) -> list[tuple[str | None, list[str]]]:
    sections: list[tuple[str | None, list[str]]] = []
    current_heading: str | None = None
    current_lines: list[str] = []
    started = False
    for raw in markdown.splitlines():
        top = TOP_HEADING_RE.match(raw.strip())
        if top and not started:
            started = True
            continue
        h2 = H2_RE.match(raw.strip())
        if h2:
            if current_heading is not None or current_lines:
                sections.append((current_heading, current_lines))
            current_heading = h2.group(1).strip()
            current_lines = []
            started = True
            continue
        current_lines.append(raw.rstrip("\n"))
    if current_heading is not None or current_lines:
        sections.append((current_heading, current_lines))
    return sections


def render_body(
    markdown: str,
    inline_image_urls: dict[str, str] | None = None,
    layout_config: dict | None = None,
) -> tuple[str, str]:
    sections = split_sections(markdown)
    html_parts: list[str] = []
    plain_parts: list[str] = []
    inline_image_urls = inline_image_urls or {}
    layout_config = layout_config or default_layout_config()
    has_explicit_brand = any((heading or "").strip() == BRAND_SECTION for heading, _ in sections)
    has_explicit_follow = any((heading or "").strip() == FOLLOW_SECTION for heading, _ in sections)
    brand_rendered = False
    follow_rendered = False

    def flush_paragraph(buffer: list[str]) -> None:
        text = " ".join(item.strip() for item in buffer if item.strip()).strip()
        if not text:
            return
        plain_parts.append(text)
        html_parts.append(
            f'<p style="font-size:16px;line-height:1.85;color:#1f2329;margin:14px 0;">{format_inline(text)}</p>'
        )

    def flush_list(buffer: list[str]) -> None:
        items = [item.strip()[2:].strip() for item in buffer if item.strip().startswith(("- ", "* "))]
        if not items:
            return
        plain_parts.extend(items)
        html_parts.append('<ul style="margin:12px 0 16px 22px;padding:0;color:#1f2329;">')
        for item in items:
            html_parts.append(
                f'<li style="margin:8px 0;font-size:16px;line-height:1.75;">{format_inline(item)}</li>'
            )
        html_parts.append("</ul>")

    for heading, lines in sections:
        section_heading = heading or ""
        if section_heading in SKIP_SECTIONS:
            continue
        if not brand_rendered and not has_explicit_brand:
            brand_html, brand_plain = render_brand_card([], layout_config)
            html_parts.append(brand_html)
            plain_parts.extend(brand_plain)
            brand_rendered = True
        if section_heading == BRAND_SECTION:
            brand_html, brand_plain = render_brand_card(lines, layout_config)
            html_parts.append(brand_html)
            plain_parts.extend(brand_plain)
            brand_rendered = True
            continue
        if section_heading == FOLLOW_SECTION:
            follow_html, follow_plain = render_follow_card(lines, layout_config)
            html_parts.append(follow_html)
            plain_parts.extend(follow_plain)
            follow_rendered = True
            continue
        if section_heading and section_heading not in HIDDEN_HEADING_SECTIONS:
            html_parts.append(render_h2_heading(section_heading, layout_config))
            plain_parts.append(section_heading)
        paragraph_buffer: list[str] = []
        list_buffer: list[str] = []
        for raw in lines:
            stripped = raw.strip()
            h3 = H3_RE.match(stripped)
            if h3:
                flush_paragraph(paragraph_buffer)
                paragraph_buffer = []
                flush_list(list_buffer)
                list_buffer = []
                subheading = h3.group(1).strip()
                html_parts.append(render_h3_heading(subheading, layout_config))
                plain_parts.append(subheading)
                continue
            if HORIZONTAL_RULE_RE.match(stripped):
                flush_paragraph(paragraph_buffer)
                paragraph_buffer = []
                flush_list(list_buffer)
                list_buffer = []
                continue
            image_match = IMAGE_LINE_RE.match(stripped)
            if image_match:
                flush_paragraph(paragraph_buffer)
                paragraph_buffer = []
                flush_list(list_buffer)
                list_buffer = []
                alt_text = image_match.group(1).strip()
                image_key = normalize_markdown_asset_path(image_match.group(2))
                image_url = inline_image_urls.get(image_key, "")
                if image_url:
                    html_parts.append(
                        '<figure style="margin:18px 0 20px;">'
                        f'<img src="{escape_text(image_url)}" alt="{escape_text(alt_text)}" '
                        'style="width:100%;height:auto;border-radius:10px;display:block;" />'
                        + (
                            f'<figcaption style="margin-top:8px;font-size:13px;line-height:1.6;color:#6b7280;">{escape_text(alt_text)}</figcaption>'
                            if alt_text
                            else ""
                        )
                        + "</figure>"
                    )
                    if alt_text:
                        plain_parts.append(alt_text)
                continue
            if not stripped:
                flush_paragraph(paragraph_buffer)
                paragraph_buffer = []
                flush_list(list_buffer)
                list_buffer = []
                continue
            if stripped.startswith(("- ", "* ")):
                flush_paragraph(paragraph_buffer)
                paragraph_buffer = []
                list_buffer.append(stripped)
                continue
            flush_list(list_buffer)
            list_buffer = []
            paragraph_buffer.append(stripped)
        flush_paragraph(paragraph_buffer)
        flush_list(list_buffer)
        if not follow_rendered and not has_explicit_follow and (section_heading == "开头" or not section_heading):
            follow_html, follow_plain = render_follow_card([], layout_config)
            html_parts.append(follow_html)
            plain_parts.extend(follow_plain)
            follow_rendered = True
    if not follow_rendered:
        follow_html, follow_plain = render_follow_card([], layout_config)
        html_parts.append(follow_html)
        plain_parts.extend(follow_plain)
    plain_text = " ".join(part.strip() for part in plain_parts if part.strip())
    return "\n".join(html_parts), plain_text


def create_fallback_cover() -> Path:
    width, height = 900, 500
    row_size = (width * 3 + 3) & ~3
    image_size = row_size * height
    file_size = 54 + image_size

    def bmp_header() -> bytes:
        return bytes(
            [
                0x42,
                0x4D,
                file_size & 0xFF,
                (file_size >> 8) & 0xFF,
                (file_size >> 16) & 0xFF,
                (file_size >> 24) & 0xFF,
                0x00,
                0x00,
                0x00,
                0x00,
                0x36,
                0x00,
                0x00,
                0x00,
                0x28,
                0x00,
                0x00,
                0x00,
                width & 0xFF,
                (width >> 8) & 0xFF,
                (width >> 16) & 0xFF,
                (width >> 24) & 0xFF,
                height & 0xFF,
                (height >> 8) & 0xFF,
                (height >> 16) & 0xFF,
                (height >> 24) & 0xFF,
                0x01,
                0x00,
                0x18,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                image_size & 0xFF,
                (image_size >> 8) & 0xFF,
                (image_size >> 16) & 0xFF,
                (image_size >> 24) & 0xFF,
                0x13,
                0x0B,
                0x00,
                0x00,
                0x13,
                0x0B,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ]
        )

    tmp = Path(tempfile.gettempdir()) / f"th_wechat_cover_{uuid.uuid4().hex}.bmp"
    blue_pixel = bytes([0x80, 0x40, 0x20])
    padding = bytes([0x00] * (row_size - width * 3))
    row = blue_pixel * width + padding
    with tmp.open("wb") as handle:
        handle.write(bmp_header())
        for _ in range(height):
            handle.write(row)
    return tmp


def request_json_call(url: str, payload: dict | None = None, method: str = "GET", timeout: int = 60) -> dict:
    data = None
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(url, data=data, method=method, headers=headers)
    try:
        with urlopen(request, timeout=timeout, context=SSL_CONTEXT) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", "ignore")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error: {exc}") from exc


def multipart_upload(url: str, file_path: Path, field_name: str = "media", timeout: int = 120) -> dict:
    boundary = f"----THCapitalBoundary{uuid.uuid4().hex}"
    file_name = file_path.name
    content = file_path.read_bytes()
    content_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"
    body = bytearray()
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(
        f'Content-Disposition: form-data; name="{field_name}"; filename="{file_name}"\r\n'.encode("utf-8")
    )
    body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
    body.extend(content)
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))
    request = Request(
        url,
        data=bytes(body),
        method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urlopen(request, timeout=timeout, context=SSL_CONTEXT) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", "ignore")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error: {exc}") from exc


class WeChatDraftPublisher:
    def __init__(self, appid: str, secret: str):
        self.appid = appid
        self.secret = secret
        self.access_token = ""

    def ensure_access_token(self, force_refresh: bool = False) -> str:
        if self.access_token and not force_refresh:
            return self.access_token
        qs = urlencode({"grant_type": "client_credential", "appid": self.appid, "secret": self.secret})
        payload = request_json_call(f"https://api.weixin.qq.com/cgi-bin/token?{qs}")
        token = str(payload.get("access_token", "")).strip()
        if not token:
            raise RuntimeError(f"access_token failed: {payload}")
        self.access_token = token
        return token

    def invalidate_access_token(self) -> None:
        self.access_token = ""

    def _should_retry_with_fresh_token(self, message: str) -> bool:
        lowered = message.lower()
        if "invalid credential" in lowered:
            return True
        if "access_token is invalid or not latest" in lowered:
            return True
        if "access_token expired" in lowered:
            return True
        if re.search(r"['\"]errcode['\"]\s*:\s*(40001|42001|40014)", message):
            return True
        return False

    def _with_token_retry(self, action):
        try:
            return action()
        except Exception as exc:
            message = str(exc)
            if not self._should_retry_with_fresh_token(message):
                raise
            self.invalidate_access_token()
            return action()

    def upload_cover(self, image_path: Path) -> str:
        def action() -> str:
            token = self.ensure_access_token()
            payload = multipart_upload(
                f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image",
                image_path,
            )
            media_id = str(payload.get("media_id", "")).strip()
            if not media_id:
                raise RuntimeError(f"cover upload failed: {payload}")
            return media_id
        return self._with_token_retry(action)

    def upload_inline_image(self, image_path: Path) -> str:
        def action() -> str:
            token = self.ensure_access_token()
            payload = multipart_upload(
                f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}",
                image_path,
            )
            url = str(payload.get("url", "")).strip()
            if not url:
                raise RuntimeError(f"inline image upload failed: {payload}")
            return url
        return self._with_token_retry(action)

    def create_draft(self, title: str, author: str, digest: str, content_html: str, thumb_media_id: str) -> str:
        def action() -> str:
            token = self.ensure_access_token()
            payload = {
                "articles": [
                    {
                        "title": title[:64],
                        "author": author,
                        "digest": digest[:120],
                        "content": content_html,
                        "content_source_url": "",
                        "thumb_media_id": thumb_media_id,
                        "show_cover_pic": 1,
                        "need_open_comment": 0,
                        "only_fans_can_comment": 0,
                    }
                ]
            }
            result = request_json_call(
                f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}",
                payload=payload,
                method="POST",
            )
            media_id = str(result.get("media_id", "")).strip()
            if not media_id:
                raise RuntimeError(f"draft add failed: {result}")
            return media_id
        return self._with_token_retry(action)

    def freepublish_batchget(self, offset: int, count: int, no_content: int = 0) -> dict:
        token = self.ensure_access_token()
        return request_json_call(
            f"https://api.weixin.qq.com/cgi-bin/freepublish/batchget?access_token={token}",
            payload={"offset": offset, "count": count, "no_content": no_content},
            method="POST",
        )

    def article_total_detail(self, publish_date: str) -> dict:
        token = self.ensure_access_token()
        return request_json_call(
            f"https://api.weixin.qq.com/datacube/getarticletotaldetail?access_token={token}",
            payload={"begin_date": publish_date, "end_date": publish_date},
            method="POST",
        )

    def user_summary(self, begin_date: str, end_date: str) -> dict:
        token = self.ensure_access_token()
        return request_json_call(
            f"https://api.weixin.qq.com/datacube/getusersummary?access_token={token}",
            payload={"begin_date": begin_date, "end_date": end_date},
            method="POST",
        )

    def user_cumulate(self, begin_date: str, end_date: str) -> dict:
        token = self.ensure_access_token()
        return request_json_call(
            f"https://api.weixin.qq.com/datacube/getusercumulate?access_token={token}",
            payload={"begin_date": begin_date, "end_date": end_date},
            method="POST",
        )


def write_result(result_path: Path, payload: dict) -> None:
    result_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_consumer_heartbeat(root_dir: Path, outputs: list[str]) -> None:
    pending_request_ids = []
    for request_dir in request_dirs(root_dir):
        request_path = request_dir / "request.json"
        result_path = request_dir / "result.json"
        if request_path.exists() and not result_path.exists():
            pending_request_ids.append(request_dir.name)
    heartbeat = {
        "last_seen_at": now_iso(),
        "consumer_version": CONSUMER_VERSION,
        "host": platform.node() or "unknown-host",
        "python": sys.version.split()[0],
        "pending_request_count": len(pending_request_ids),
        "pending_request_ids": pending_request_ids[:20],
        "last_outputs": outputs[-10:],
    }
    (root_dir / "consumer-heartbeat.json").write_text(
        json.dumps(heartbeat, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def process_request_dir(request_dir: Path, publisher: WeChatDraftPublisher, layout_config: dict) -> str:
    request_path = request_dir / "request.json"
    result_path = request_dir / "result.json"
    request = request_json(request_path)
    inline_image_total = len(request.get("inline_images") or [])
    expiry_reason = request_expiry_reason(request)
    if expiry_reason:
        if not result_needs_refresh(result_path, request_path, inline_image_total):
            return f"SKIP {request_dir.name} already_recorded_{expiry_reason}"
        result = {
            "status": "skipped_expired" if expiry_reason.startswith("expired_") else "skipped_queue_closed",
            "completed_at": now_iso(),
            "consumer_version": CONSUMER_VERSION,
            "reason": expiry_reason,
            "title": str((request.get("article") or {}).get("title", "")).strip() or request.get("draft_key", request_dir.name),
        }
        write_result(result_path, result)
        return f"SKIP {request_dir.name} {expiry_reason}"
    if not result_needs_refresh(result_path, request_path, inline_image_total):
        return f"SKIP {request_dir.name} already_success"
    article_meta = request.get("article") or {}
    markdown_file = request_dir / str((request.get("files") or {}).get("wechat_markdown", "wechat.md"))
    markdown_text = markdown_file.read_text(encoding="utf-8")
    title = str(article_meta.get("title", "")).strip() or extract_title(markdown_text, request.get("draft_key", "TH Capital"))
    inline_image_urls: dict[str, str] = {}
    author = str(article_meta.get("author", "")).strip() or "TH Capital"
    author = truncate_utf8_bytes(author, 20) or "TH Capital"
    cover_name = str((request.get("files") or {}).get("cover_image", "n/a"))
    temp_cover: Path | None = None
    cover_path = request_dir / cover_name if cover_name != "n/a" else None
    if cover_path is None or not cover_path.exists():
        temp_cover = create_fallback_cover()
        cover_path = temp_cover
    try:
        for image_meta in request.get("inline_images") or []:
            markdown_path = normalize_markdown_asset_path(str(image_meta.get("markdown_path", "")))
            request_image_path = normalize_markdown_asset_path(
                str(image_meta.get("request_path", "") or markdown_path)
            )
            if not markdown_path or not request_image_path:
                continue
            image_path = (request_dir / request_image_path).resolve()
            if image_path.exists() and image_path.is_file():
                inline_image_urls[markdown_path] = publisher.upload_inline_image(image_path)
        content_html, plain_text = render_body(markdown_text, inline_image_urls=inline_image_urls, layout_config=layout_config)
        debug_html_path = write_debug_html(request_dir, content_html)
        digest = str(article_meta.get("digest", "")).strip() or plain_text[:120]
        thumb_media_id = publisher.upload_cover(cover_path)
        media_id = publisher.create_draft(title, author, digest, content_html, thumb_media_id)
        result = {
            "status": "success",
            "completed_at": now_iso(),
            "consumer_version": CONSUMER_VERSION,
            "media_id": media_id,
            "thumb_media_id": thumb_media_id,
            "inline_image_count": len(inline_image_urls),
            "inline_image_keys": sorted(inline_image_urls.keys()),
            "rendered_html_path": str(debug_html_path),
            "rendered_html_img_count": content_html.count("<img "),
            "title": title,
            "author": author,
            "digest": digest,
        }
        write_result(result_path, result)
        return f"SUCCESS {request_dir.name} media_id={media_id}"
    except Exception as exc:
        result = {
            "status": "failed",
            "completed_at": now_iso(),
            "error_message": str(exc),
            "title": title,
        }
        write_result(result_path, result)
        return f"FAILED {request_dir.name} {exc}"
    finally:
        if temp_cover and temp_cover.exists():
            temp_cover.unlink(missing_ok=True)


def run_once(root_dir: Path, publisher: WeChatDraftPublisher) -> list[str]:
    outputs: list[str] = []
    layout_config = load_layout_config(root_dir)
    for request_dir in request_dirs(root_dir):
        if not (request_dir / "request.json").exists():
            continue
        outputs.append(process_request_dir(request_dir, publisher, layout_config))
    outputs.extend(sync_official_metrics(root_dir, publisher))
    if not outputs:
        outputs.append("NO_PENDING_REQUESTS")
    write_consumer_heartbeat(root_dir, outputs)
    return outputs


def maybe_restart_for_code_change(watched_mtime_ns: int) -> int:
    script_path = Path(__file__).resolve()
    current_mtime_ns = script_path.stat().st_mtime_ns
    if current_mtime_ns == watched_mtime_ns:
        return watched_mtime_ns
    print(f"{now_iso()} CODE_CHANGE_DETECTED restarting consumer version={CONSUMER_VERSION}")
    os.execv(sys.executable, [sys.executable, str(script_path), *sys.argv[1:]])
    return current_mtime_ns


def main() -> None:
    args = parse_args()
    root_dir = Path(args.root_dir).expanduser().resolve()
    appid, secret = load_credentials(args.appid, args.secret)
    publisher = WeChatDraftPublisher(appid, secret)
    instance_guard: WindowsSingleInstanceGuard | None = None
    if args.watch:
        instance_guard = WindowsSingleInstanceGuard(watch_mutex_name(root_dir))
        if not instance_guard.acquire():
            print(f"{now_iso()} WATCHER_ALREADY_RUNNING {instance_guard.name}")
            return
    if not args.watch:
        for line in run_once(root_dir, publisher):
            print(line)
        return
    watched_mtime_ns = Path(__file__).resolve().stat().st_mtime_ns
    try:
        while True:
            watched_mtime_ns = maybe_restart_for_code_change(watched_mtime_ns)
            for line in run_once(root_dir, publisher):
                print(f"{now_iso()} {line}")
            time.sleep(max(args.interval, 5))
    finally:
        if instance_guard is not None:
            instance_guard.release()


if __name__ == "__main__":
    main()

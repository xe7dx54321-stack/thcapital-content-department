"""Shared lightweight connector helpers for Phase 27.

The helpers intentionally fetch and store metadata only: title, URL, date,
summary snippet, and tags. They do not download full articles or PDFs.
"""

from __future__ import annotations

import html
import re
import socket
import ssl
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from typing import Any

from content_system.phase7_report_utils import safe_int
from content_system.upstream_intelligence_common import compact_text, detect_event_type, detect_lane, stable_id


DEFAULT_TIMEOUT = 12
USER_AGENT = "THCapitalContentFactory/1.0 metadata-only; contact=operator"


def https_context() -> ssl.SSLContext | None:
    try:
        import certifi  # type: ignore[import-not-found]
    except Exception:  # noqa: BLE001 - optional CA bundle fallback.
        return None
    return ssl.create_default_context(cafile=certifi.where())


class LinkTitleParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.page_title = ""
        self.meta_description = ""
        self.links: list[dict[str, str]] = []
        self._in_title = False
        self._current_href = ""
        self._current_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "title":
            self._in_title = True
        if tag.lower() == "meta":
            name = (attr.get("name") or attr.get("property") or "").lower()
            if name in {"description", "og:description"} and attr.get("content"):
                self.meta_description = compact_text(html.unescape(attr["content"]), 280)
        if tag.lower() == "a" and attr.get("href"):
            self._current_href = urllib.parse.urljoin(self.base_url, attr["href"])
            self._current_text = []

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False
        if tag.lower() == "a" and self._current_href:
            text = compact_text(html.unescape(" ".join(self._current_text)), 160)
            if text and self._current_href.startswith(("http://", "https://")):
                self.links.append({"title": text, "url": self._current_href})
            self._current_href = ""
            self._current_text = []

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.page_title += data
        if self._current_href:
            self._current_text.append(data)


def fetch_url(url: str, timeout: int = DEFAULT_TIMEOUT) -> tuple[str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/atom+xml, text/html;q=0.9, */*;q=0.1"})
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=https_context()) as response:
            content_type = response.headers.get("content-type", "")
            raw = response.read(1_200_000)
    except (urllib.error.URLError, socket.timeout, TimeoutError) as exc:
        raise RuntimeError(str(exc)) from exc
    return raw.decode("utf-8", errors="replace"), content_type


def strip_tags(text: str) -> str:
    return compact_text(re.sub(r"<[^>]+>", " ", html.unescape(text or "")), 260)


def xml_text(element: ET.Element, *names: str) -> str:
    for name in names:
        found = element.find(name)
        if found is not None and found.text:
            return strip_tags(found.text)
    for child in element.iter():
        tag = child.tag.split("}", 1)[-1].lower()
        if tag in {name.lower().split("}", 1)[-1] for name in names} and child.text:
            return strip_tags(child.text)
    return ""


def xml_link(element: ET.Element) -> str:
    for child in element.iter():
        tag = child.tag.split("}", 1)[-1].lower()
        if tag == "link":
            href = child.attrib.get("href")
            if href:
                return href
            if child.text and child.text.strip().startswith("http"):
                return child.text.strip()
    return ""


def parse_feed_items(text: str, source_name: str, source_type: str, limit: int = 20) -> list[dict[str, Any]]:
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return []
    entries = [item for item in root.iter() if item.tag.split("}", 1)[-1].lower() in {"item", "entry"}]
    items: list[dict[str, Any]] = []
    for entry in entries[:limit]:
        title = xml_text(entry, "title")
        url = xml_link(entry)
        if not title or not url:
            continue
        published = xml_text(entry, "published", "updated", "pubDate")
        summary = xml_text(entry, "summary", "description", "content")
        lane_id = detect_lane(title, source_name)
        items.append(
            normalized_connector_item(
                prefix="srcitem" if source_type == "rss_official_blog" else "researchitem",
                title=title,
                url=url,
                source_name=source_name,
                source_type=source_type,
                lane_id=lane_id,
                published_at=published,
                summary=summary,
                tags=[lane_id, detect_event_type(title)],
            )
        )
    return items


def parse_html_index_items(text: str, url: str, source_name: str, source_type: str, limit: int = 15) -> list[dict[str, Any]]:
    parser = LinkTitleParser(url)
    parser.feed(text)
    seen: set[str] = set()
    items: list[dict[str, Any]] = []
    candidates = parser.links
    if parser.page_title.strip():
        candidates = [{"title": parser.page_title.strip(), "url": url}, *candidates]
    for link in candidates:
        href = link.get("url", "")
        title = compact_text(link.get("title", ""), 180)
        if not href or not title or href in seen:
            continue
        if any(skip in href.lower() for skip in ("login", "signup", "privacy", "terms", "mailto:", "#")):
            continue
        seen.add(href)
        lane_id = detect_lane(title, source_name)
        items.append(
            normalized_connector_item(
                prefix="srcitem" if source_type == "rss_official_blog" else "researchitem",
                title=title,
                url=href,
                source_name=source_name,
                source_type=source_type,
                lane_id=lane_id,
                published_at="",
                summary=parser.meta_description if href == url else "",
                tags=[lane_id, detect_event_type(title)],
            )
        )
        if len(items) >= limit:
            break
    return items


def normalized_connector_item(
    *,
    prefix: str,
    title: str,
    url: str,
    source_name: str,
    source_type: str,
    lane_id: str,
    published_at: str,
    summary: str,
    tags: list[str] | None = None,
) -> dict[str, Any]:
    safe_title = compact_text(title, 220)
    safe_url = url.strip()
    return {
        "item_id": stable_id(prefix, source_type, source_name, safe_title, safe_url),
        "title": safe_title,
        "url": safe_url,
        "source_name": source_name,
        "published_at": published_at or "",
        "fetched_at": "",
        "summary": compact_text(summary, 300),
        "tags": tags or [],
        "metadata_only": True,
        "copyright_safe": True,
    }


def source_status(item_count: int, error: str = "") -> str:
    if error:
        return "FAILED"
    if item_count:
        return "SUCCESS"
    return "EMPTY"


def count_by_status(rows: list[dict[str, Any]], status: str) -> int:
    return sum(1 for item in rows if item.get("status") == status)


def item_count_from_rows(rows: list[dict[str, Any]]) -> int:
    return sum(safe_int(item.get("item_count")) for item in rows)

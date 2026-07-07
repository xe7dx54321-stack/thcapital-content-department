"""WeChat RSS Ingestion v1.

Fetches RSS feeds without additional web page scraping. Supports dry-run mode
where no actual HTTP requests are made.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from content_system.wechat_rss_source_registry import WechatRssSource, resolve_env_variables


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class RssEntry:
    schema_version: str
    entry_id: str
    source_id: str
    source_label: str
    is_official: bool
    title: str
    link: str
    published_at: str
    excerpt: str
    captured_at: str
    do_not_copy_text: bool = True


@dataclass(frozen=True)
class RssIngestionReport:
    schema_version: str
    generated_at: str
    run_date: str
    dry_run: bool
    source_count: int
    entry_count: int
    entries: tuple[RssEntry, ...]
    warnings: tuple[str, ...]
    errors: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def normalize_date(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return today_token()
    return text.replace("-", "")[:8]


def safe_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    text = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def make_entry_id(source_id: str, title: str, link: str) -> str:
    digest = hashlib.sha1(f"{source_id}|{title}|{link}".encode("utf-8")).hexdigest()[:12]
    safe_source = re.sub(r"[^a-z0-9_]+", "_", source_id.lower()).strip("_") or "source"
    return f"entry_{safe_source}_{digest}"


def extract_excerpt(text: str, max_length: int = 300) -> str:
    cleaned = safe_text(text)
    if len(cleaned) <= max_length:
        return cleaned
    return cleaned[: max_length - 1].rstrip() + "..."


def mock_rss_entries(source: WechatRssSource) -> tuple[RssEntry, ...]:
    return (
        RssEntry(
            schema_version=SCHEMA_VERSION,
            entry_id=make_entry_id(source.source_id, "Mock Article 1", "https://example.com/mock1"),
            source_id=source.source_id,
            source_label=source.label,
            is_official=source.is_official,
            title=f"[MOCK] Sample article from {source.label}",
            link="https://example.com/mock-article",
            published_at=today_token(),
            excerpt=f"[MOCK] This is a sample excerpt from {source.label}. In dry-run mode, no actual RSS fetching occurs.",
            captured_at=utc_now(),
            do_not_copy_text=True,
        ),
    )


def parse_rss_feed(xml_content: str, source: WechatRssSource) -> tuple[RssEntry, ...]:
    entries: list[RssEntry] = []

    item_pattern = re.compile(r"<item>(.*?)</item>", re.DOTALL | re.IGNORECASE)
    for item_match in item_pattern.finditer(xml_content):
        item_content = item_match.group(1)

        title_match = re.search(r"<title>(.*?)</title>", item_content, re.DOTALL | re.IGNORECASE)
        title = safe_text(title_match.group(1)) if title_match else ""

        link_match = re.search(r"<link>(.*?)</link>", item_content, re.DOTALL | re.IGNORECASE)
        link = safe_text(link_match.group(1)) if link_match else ""

        pub_date_match = re.search(r"<pubDate>(.*?)</pubDate>", item_content, re.DOTALL | re.IGNORECASE)
        pub_date = normalize_date(pub_date_match.group(1)) if pub_date_match else today_token()

        description_match = re.search(r"<description>(.*?)</description>", item_content, re.DOTALL | re.IGNORECASE)
        excerpt = extract_excerpt(description_match.group(1)) if description_match else ""

        if not title or not link:
            continue

        entries.append(
            RssEntry(
                schema_version=SCHEMA_VERSION,
                entry_id=make_entry_id(source.source_id, title, link),
                source_id=source.source_id,
                source_label=source.label,
                is_official=source.is_official,
                title=title,
                link=link,
                published_at=pub_date,
                excerpt=excerpt,
                captured_at=utc_now(),
                do_not_copy_text=True,
            )
        )

    return tuple(entries)


def fetch_rss_content(url: str, timeout: int = 10) -> str | None:
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def ingest_source(source: WechatRssSource, dry_run: bool) -> tuple[tuple[RssEntry, ...], list[str], list[str]]:
    entries: tuple[RssEntry, ...] = ()
    warnings: list[str] = []
    errors: list[str] = []

    resolved_url = resolve_env_variables(source.rss_url)

    if dry_run:
        entries = mock_rss_entries(source)
        warnings.append(f"dry-run: mocked {len(entries)} entries for {source.source_id}")
        return entries, warnings, errors

    content = fetch_rss_content(resolved_url)
    if content is None:
        errors.append(f"Failed to fetch RSS from {source.source_id}")
        return entries, warnings, errors

    entries = parse_rss_feed(content, source)
    if not entries:
        warnings.append(f"No entries found in RSS feed for {source.source_id}")

    return entries, warnings, errors


def ingest_all_sources(sources: tuple[WechatRssSource, ...], dry_run: bool, run_date: str | None = None) -> RssIngestionReport:
    all_entries: list[RssEntry] = []
    all_warnings: list[str] = []
    all_errors: list[str] = []

    final_run_date = normalize_date(run_date)

    for source in sources:
        if not source.enabled:
            all_warnings.append(f"Source {source.source_id} is disabled, skipping")
            continue

        entries, warnings, errors = ingest_source(source, dry_run)
        all_entries.extend(entries)
        all_warnings.extend(warnings)
        all_errors.extend(errors)

    return RssIngestionReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        dry_run=dry_run,
        source_count=len(sources),
        entry_count=len(all_entries),
        entries=tuple(all_entries),
        warnings=tuple(all_warnings),
        errors=tuple(all_errors),
    )


def report_to_dict(report: RssIngestionReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: RssIngestionReport) -> str:
    rows = []
    for index, entry in enumerate(report.entries, start=1):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    entry.source_id,
                    "official" if entry.is_official else "media",
                    entry.published_at,
                    entry.title[:60] + "..." if len(entry.title) > 60 else entry.title,
                    entry.link,
                ]
            )
            + " |"
        )

    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    errors = "\n".join(f"- {item}" for item in report.errors) if report.errors else "- None"

    return f"""# WeChat RSS Ingestion Report
    - Generated at: `{report.generated_at}`
    - Run date: `{report.run_date}`
    - Dry run: `{report.dry_run}`
    - Sources processed: `{report.source_count}`
    - Entries ingested: `{report.entry_count}`

## Entries

| # | Source | Type | Date | Title | URL |
|---:|---|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | - | None | - |'}

## Warnings

{warnings}

## Errors

{errors}

## Notes

- Only RSS feed content is fetched; no additional web page scraping.
- Excerpts only (no full text).
- do_not_copy_text=True for all entries.
"""


def write_report(report: RssIngestionReport, output_path: str) -> None:
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = output_path + ".json"
    md_path = output_path + ".md"

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(payload + "\n")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)


def load_report(json_path: str) -> RssIngestionReport | None:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return RssIngestionReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            dry_run=bool(data.get("dry_run", False)),
            source_count=int(data.get("source_count", 0)),
            entry_count=int(data.get("entry_count", 0)),
            entries=tuple(
                RssEntry(
                    schema_version=e.get("schema_version", SCHEMA_VERSION),
                    entry_id=e.get("entry_id", ""),
                    source_id=e.get("source_id", ""),
                    source_label=e.get("source_label", ""),
                    is_official=bool(e.get("is_official", False)),
                    title=e.get("title", ""),
                    link=e.get("link", ""),
                    published_at=e.get("published_at", ""),
                    excerpt=e.get("excerpt", ""),
                    captured_at=e.get("captured_at", ""),
                    do_not_copy_text=bool(e.get("do_not_copy_text", True)),
                )
                for e in data.get("entries", [])
            ),
            warnings=tuple(data.get("warnings", [])),
            errors=tuple(data.get("errors", [])),
        )
    except Exception:
        return None
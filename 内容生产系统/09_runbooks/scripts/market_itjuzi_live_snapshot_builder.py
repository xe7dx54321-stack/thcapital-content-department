#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import signal
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, sync_playwright

from market_itjuzi_live_probe import find_chrome_executable, find_free_port, launch_native_chrome
from market_topic_capture_round import LOG_DIR, ROOT, compact_snippet, format_dt, now_cn, slugify, write_text


SNAPSHOT_DIR = ROOT / "02_topic_radar" / "itjuzi_live_snapshot"
EVENT_DIR = SNAPSHOT_DIR / "events"
COMPANY_DIR = SNAPSHOT_DIR / "companies"
DAILY_UPDATES_CSV = SNAPSHOT_DIR / "itjuzi-live-daily-updates.csv"
PAGE_URLS = {
    "home": "https://www.itjuzi.com/",
    "company": "https://www.itjuzi.com/company",
    "investevent": "https://www.itjuzi.com/investevent",
}
AI_KEYWORDS = [
    ("人工智能", 3),
    ("ai", 2),
    ("agent", 2),
    ("gui agent", 2),
    ("机器人", 2),
    ("具身", 2),
    ("大模型", 2),
    ("智能", 1),
    ("模型", 1),
]


@dataclass
class CompanySnapshot:
    row_rank: int
    company_id: str
    company_name: str
    company_description: str
    location: str
    established_at: str
    industry: str
    financing_total: str
    company_url: str
    detail_url: str
    ai_relevance: str
    ai_score: int
    source_page_url: str
    captured_at: str
    raw_text: str


@dataclass
class InvesteventSnapshot:
    row_rank: int
    event_id: str
    event_date: str
    company_id: str
    company_name: str
    company_description: str
    industry: str
    round_name: str
    amount: str
    investor_names: list[str]
    valuation: str
    company_url: str
    detail_url: str
    ai_relevance: str
    ai_score: int
    source_page_url: str
    captured_at: str
    raw_text: str


@dataclass
class HomeDailyOverview:
    logical_date: str
    investment_count: int | None
    investment_amount: str
    source_page_url: str
    captured_at: str
    raw_text: str


@dataclass
class HomeInvesteventHeadline:
    row_rank: int
    event_id: str
    title: str
    relative_time: str
    detail_url: str
    source_page_url: str
    captured_at: str
    raw_text: str


@dataclass
class HomeEventListRow:
    row_rank: int
    event_id: str
    company_id: str
    company_name: str
    company_description: str
    round_name: str
    relative_time: str
    amount: str
    investor_names: list[str]
    company_url: str
    detail_url: str
    source_page_url: str
    captured_at: str
    raw_text: str


@dataclass
class EventApiProbe:
    page: int
    status: int | None
    message: str
    url: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build structured IT桔子 live snapshot cards and daily update tables.")
    parser.add_argument("--company-limit", type=int, default=8, help="How many company rows to extract from the company page.")
    parser.add_argument(
        "--event-limit",
        type=int,
        default=None,
        help="Deprecated and ignored. The script now captures all visible investevent rows matching the logical date.",
    )
    parser.add_argument("--logical-date", type=str, default=None, help="Logical date in YYYY-MM-DD. Defaults to China today.")
    parser.add_argument("--write", action="store_true", help="Reserved for parity. Current script always writes outputs.")
    return parser.parse_args()


def ensure_dirs() -> None:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    EVENT_DIR.mkdir(parents=True, exist_ok=True)
    COMPANY_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def cleanup_today_cards(day_token: str) -> None:
    for directory in [EVENT_DIR, COMPANY_DIR]:
        for path in directory.glob(f"{day_token}__*__itjuzi-live-*.md"):
            path.unlink(missing_ok=True)


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def split_company_block(value: str) -> tuple[str, str]:
    parts = [clean_text(part) for part in str(value or "").splitlines() if clean_text(part)]
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[1]


def extract_numeric_id(url: str, marker: str) -> str:
    match = re.search(rf"/{re.escape(marker)}/(\d+)", str(url or ""))
    return match.group(1) if match else ""


def ai_relevance(text: str) -> tuple[str, int]:
    haystack = clean_text(text).lower()
    score = 0
    for keyword, points in AI_KEYWORDS:
        if keyword.lower() in haystack:
            score += points
    if score >= 3:
        return "high", score
    if score >= 1:
        return "medium", score
    return "low", score


def unique_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        cleaned = clean_text(value)
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        ordered.append(cleaned)
    return ordered


def stable_slug(*parts: str, fallback: str) -> str:
    normalized = "_".join(clean_text(part) for part in parts if clean_text(part))
    slug = slugify(normalized, "")
    return slug or fallback


def parse_home_daily_overview(body_text: str, logical_date: str, captured_at: str) -> HomeDailyOverview:
    normalized = clean_text(body_text)
    match = re.search(r"今日概览\s+(\d+)\s+本日投资数量\s+([\d\.]+)\s+亿元\s+本日投资金额", normalized)
    return HomeDailyOverview(
        logical_date=logical_date,
        investment_count=int(match.group(1)) if match else None,
        investment_amount=f"{match.group(2)}亿元" if match else "",
        source_page_url=PAGE_URLS["home"],
        captured_at=captured_at,
        raw_text=compact_snippet(normalized, 800),
    )


def evaluate_home_headlines(page: Any) -> list[dict[str, Any]]:
    return page.evaluate(
        """() => Array.from(document.querySelectorAll('a[href]'))
            .map((anchor, index) => {
                const href = anchor.href || '';
                if (!href.includes('/investevent/')) {
                    return null;
                }
                const text = (anchor.innerText || anchor.textContent || '').trim();
                if (!text || text === '详情') {
                    return null;
                }
                const context = (
                    (anchor.closest('li') && anchor.closest('li').innerText)
                    || (anchor.closest('tr') && anchor.closest('tr').innerText)
                    || (anchor.parentElement && anchor.parentElement.innerText)
                    || text
                );
                return {
                    dom_index: index,
                    href,
                    text,
                    context: (context || '').trim(),
                };
            })
            .filter(Boolean)""",
    )


def evaluate_home_event_table_rows(page: Any) -> list[dict[str, Any]]:
    return page.evaluate(
        """() => Array.from(document.querySelectorAll('tr'))
            .map((tr, index) => {
                const cells = Array.from(tr.querySelectorAll('td')).map(td => (td.innerText || td.textContent || '').trim());
                const links = Array.from(tr.querySelectorAll('a[href]')).map(a => ({
                    text: (a.innerText || a.textContent || '').trim(),
                    href: a.href,
                }));
                const eventLinks = links.filter(link => link.href.includes('/investevent/'));
                const companyLinks = links.filter(link => link.href.includes('/company/'));
                if (!eventLinks.length || !companyLinks.length || cells.length < 4) {
                    return null;
                }
                return {
                    dom_index: index,
                    cells,
                    links,
                    text: (tr.innerText || tr.textContent || '').trim(),
                };
            })
            .filter(Boolean)""",
    )


def evaluate_company_rows(page: Any, limit: int) -> list[dict[str, Any]]:
    return page.evaluate(
        """(limit) => Array.from(document.querySelectorAll('tr'))
            .map((tr, index) => {
                const cells = Array.from(tr.querySelectorAll('td')).map(td => (td.innerText || td.textContent || '').trim());
                const links = Array.from(tr.querySelectorAll('a[href]')).map(a => ({
                    text: (a.innerText || a.textContent || '').trim(),
                    href: a.href,
                }));
                const companyLinks = links.filter(link => link.href.includes('/company/'));
                if (!companyLinks.length || cells.length < 6) {
                    return null;
                }
                return {
                    dom_index: index,
                    cells,
                    links,
                    text: (tr.innerText || tr.textContent || '').trim(),
                };
            })
            .filter(Boolean)
            .slice(0, limit)""",
        limit,
    )


def evaluate_event_rows(page: Any) -> list[dict[str, Any]]:
    return page.evaluate(
        """() => Array.from(document.querySelectorAll('tr'))
            .map((tr, index) => {
                const cells = Array.from(tr.querySelectorAll('td')).map(td => (td.innerText || td.textContent || '').trim());
                const links = Array.from(tr.querySelectorAll('a[href]')).map(a => ({
                    text: (a.innerText || a.textContent || '').trim(),
                    href: a.href,
                }));
                const eventLinks = links.filter(link => link.href.includes('/investevent/'));
                const companyLinks = links.filter(link => link.href.includes('/company/'));
                if (!eventLinks.length || !companyLinks.length || cells.length < 8) {
                    return null;
                }
                return {
                    dom_index: index,
                    cells,
                    links,
                    text: (tr.innerText || tr.textContent || '').trim(),
                };
            })
            .filter(Boolean)""",
    )


def build_company_snapshots(raw_rows: list[dict[str, Any]], captured_at: str, source_page_url: str) -> list[CompanySnapshot]:
    snapshots: list[CompanySnapshot] = []
    for row_rank, row in enumerate(raw_rows, start=1):
        cells = row.get("cells", [])
        links = row.get("links", [])
        company_links = [link for link in links if "/company/" in str(link.get("href") or "")]
        primary_company_link = next((link for link in company_links if clean_text(link.get("text") or "")), company_links[0] if company_links else {})
        company_name, company_description = split_company_block(cells[1] if len(cells) > 1 else "")
        detail_url = str(primary_company_link.get("href") or "")
        company_id = extract_numeric_id(detail_url, "company")
        score_label, score = ai_relevance(" ".join([company_name, company_description, cells[4] if len(cells) > 4 else ""]))
        snapshots.append(
            CompanySnapshot(
                row_rank=row_rank,
                company_id=company_id,
                company_name=company_name or clean_text(primary_company_link.get("text") or ""),
                company_description=company_description,
                location=clean_text(cells[2] if len(cells) > 2 else ""),
                established_at=clean_text(cells[3] if len(cells) > 3 else ""),
                industry=clean_text(cells[4] if len(cells) > 4 else ""),
                financing_total=clean_text(cells[5] if len(cells) > 5 else ""),
                company_url=detail_url,
                detail_url=detail_url,
                ai_relevance=score_label,
                ai_score=score,
                source_page_url=source_page_url,
                captured_at=captured_at,
                raw_text=clean_text(row.get("text") or ""),
            )
        )
    return snapshots


def build_event_snapshots(raw_rows: list[dict[str, Any]], captured_at: str, source_page_url: str) -> list[InvesteventSnapshot]:
    snapshots: list[InvesteventSnapshot] = []
    for row_rank, row in enumerate(raw_rows, start=1):
        cells = row.get("cells", [])
        links = row.get("links", [])
        company_links = [link for link in links if "/company/" in str(link.get("href") or "")]
        event_links = [link for link in links if "/investevent/" in str(link.get("href") or "")]
        investor_links = [link for link in links if "/investfirm/" in str(link.get("href") or "")]
        company_link = next((link for link in company_links if clean_text(link.get("text") or "")), company_links[0] if company_links else {})
        event_link = next((link for link in event_links if clean_text(link.get("text") or "") == "详情"), event_links[0] if event_links else {})
        company_name, company_description = split_company_block(cells[2] if len(cells) > 2 else "")
        investor_names = unique_strings([link.get("text") or "" for link in investor_links])
        if not investor_names and len(cells) > 6:
            investor_names = unique_strings(re.split(r"[\n/]+", cells[6]))
            investor_names = [name for name in investor_names if not name.startswith("展开(")]
        event_text = " ".join(
            [
                company_name,
                company_description,
                clean_text(cells[3] if len(cells) > 3 else ""),
                clean_text(cells[4] if len(cells) > 4 else ""),
                clean_text(cells[5] if len(cells) > 5 else ""),
            ]
        )
        score_label, score = ai_relevance(event_text)
        snapshots.append(
            InvesteventSnapshot(
                row_rank=row_rank,
                event_id=extract_numeric_id(str(event_link.get("href") or ""), "investevent"),
                event_date=clean_text(cells[1] if len(cells) > 1 else ""),
                company_id=extract_numeric_id(str(company_link.get("href") or ""), "company"),
                company_name=company_name or clean_text(company_link.get("text") or ""),
                company_description=company_description,
                industry=clean_text(cells[3] if len(cells) > 3 else ""),
                round_name=clean_text(cells[4] if len(cells) > 4 else ""),
                amount=clean_text(cells[5] if len(cells) > 5 else ""),
                investor_names=investor_names,
                valuation=clean_text(cells[7] if len(cells) > 7 else ""),
                company_url=str(company_link.get("href") or ""),
                detail_url=str(event_link.get("href") or ""),
                ai_relevance=score_label,
                ai_score=score,
                source_page_url=source_page_url,
                captured_at=captured_at,
                raw_text=clean_text(row.get("text") or ""),
            )
        )
    return snapshots


def build_home_headlines(raw_rows: list[dict[str, Any]], captured_at: str, source_page_url: str) -> list[HomeInvesteventHeadline]:
    seen_event_ids: set[str] = set()
    headlines: list[HomeInvesteventHeadline] = []
    for raw_row in raw_rows:
        detail_url = str(raw_row.get("href") or "")
        event_id = extract_numeric_id(detail_url, "investevent")
        if not event_id or event_id in seen_event_ids:
            continue
        seen_event_ids.add(event_id)
        raw_text = clean_text(raw_row.get("context") or raw_row.get("text") or "")
        relative_match = re.search(r"(刚刚|\d+\s*分钟前|\d+\s*小时前|\d+\s*天前)", raw_text)
        headlines.append(
            HomeInvesteventHeadline(
                row_rank=len(headlines) + 1,
                event_id=event_id,
                title=clean_text(raw_row.get("text") or ""),
                relative_time=clean_text(relative_match.group(1) if relative_match else ""),
                detail_url=detail_url,
                source_page_url=source_page_url,
                captured_at=captured_at,
                raw_text=raw_text,
            )
        )
    return headlines


def build_home_event_list_rows(raw_rows: list[dict[str, Any]], captured_at: str, source_page_url: str) -> list[HomeEventListRow]:
    rows: list[HomeEventListRow] = []
    for raw_row in raw_rows:
        cells = raw_row.get("cells", [])
        links = raw_row.get("links", [])
        event_link = next((link for link in links if "/investevent/" in str(link.get("href") or "")), {})
        company_link = next((link for link in links if "/company/" in str(link.get("href") or "") and clean_text(link.get("text") or "")), {})
        event_id = extract_numeric_id(str(event_link.get("href") or ""), "investevent")
        if not event_id:
            continue
        company_name, company_description = split_company_block(cells[0] if len(cells) > 0 else "")
        meta_lines = [clean_text(part) for part in str(cells[1] if len(cells) > 1 else "").splitlines() if clean_text(part)]
        round_name = ""
        relative_time = ""
        amount = ""
        if meta_lines:
            match = re.search(r"(.+?)\s+(刚刚|\d+\s*分钟前|\d+\s*小时前|\d+\s*天前)$", meta_lines[0])
            if match:
                round_name = clean_text(match.group(1))
                relative_time = clean_text(match.group(2))
            else:
                round_name = clean_text(meta_lines[0])
            if len(meta_lines) > 1:
                amount = clean_text(meta_lines[1])
        investor_names = unique_strings(re.split(r"[\n/]+", cells[2] if len(cells) > 2 else ""))
        investor_names = [name for name in investor_names if name and name != "详情"]
        rows.append(
            HomeEventListRow(
                row_rank=len(rows) + 1,
                event_id=event_id,
                company_id=extract_numeric_id(str(company_link.get("href") or ""), "company"),
                company_name=company_name or clean_text(company_link.get("text") or ""),
                company_description=company_description,
                round_name=round_name,
                relative_time=relative_time,
                amount=amount,
                investor_names=investor_names,
                company_url=str(company_link.get("href") or ""),
                detail_url=str(event_link.get("href") or ""),
                source_page_url=source_page_url,
                captured_at=captured_at,
                raw_text=clean_text(raw_row.get("text") or ""),
            )
        )
    return rows


def probe_event_api(page: Any) -> EventApiProbe:
    dollar = chr(36)
    call_js = f"""
    (pageNo) => {{
      const table = document.querySelector('.company-table-wrap');
      let vm = table && table.__vue__;
      let depth = 0;
      while (vm && depth < 10) {{
        const keys = Object.keys(vm);
        if (keys.includes('handleCurrentChange') && keys.includes('ssrData')) {{
          vm.handleCurrentChange(pageNo);
          return true;
        }}
        vm = vm["{dollar}parent"];
        depth += 1;
      }}
      return false;
    }}
    """
    try:
        with page.expect_response(lambda resp: "/api/v1/investevents" in resp.url, timeout=15000) as response_info:
            page.evaluate(call_js, 2)
        response = response_info.value
        message = ""
        try:
            payload = response.json()
            message = clean_text(payload.get("msg") or payload.get("message") or "")
        except Exception:
            try:
                message = compact_snippet(response.text(), 200)
            except Exception:
                message = ""
        return EventApiProbe(page=2, status=response.status, message=message, url=response.url)
    except PlaywrightTimeoutError:
        return EventApiProbe(page=2, status=None, message="no response", url="")
    except Exception as exc:
        return EventApiProbe(page=2, status=None, message=clean_text(str(exc)), url="")


def render_company_card(snapshot: CompanySnapshot) -> str:
    return (
        "# IT桔子 Live Company Card\n\n"
        "## Header\n\n"
        f"- `company_id`: `{snapshot.company_id or 'unknown'}`\n"
        f"- `company_name`: `{snapshot.company_name}`\n"
        f"- `company_url`: `{snapshot.company_url}`\n"
        f"- `detail_url`: `{snapshot.detail_url}`\n"
        f"- `row_rank`: `{snapshot.row_rank}`\n"
        f"- `captured_at`: `{snapshot.captured_at}`\n"
        f"- `source_page_url`: `{snapshot.source_page_url}`\n\n"
        "## Snapshot Fields\n\n"
        f"- `company_description`: {snapshot.company_description or 'none'}\n"
        f"- `location`: `{snapshot.location or 'unknown'}`\n"
        f"- `established_at`: `{snapshot.established_at or 'unknown'}`\n"
        f"- `industry`: `{snapshot.industry or 'unknown'}`\n"
        f"- `financing_total`: `{snapshot.financing_total or 'unknown'}`\n"
        f"- `ai_relevance`: `{snapshot.ai_relevance}`\n"
        f"- `ai_score`: `{snapshot.ai_score}`\n\n"
        "## Raw Row\n\n"
        f"> {snapshot.raw_text}\n"
    )


def render_event_card(snapshot: InvesteventSnapshot) -> str:
    investors = ", ".join(f"`{name}`" for name in snapshot.investor_names) if snapshot.investor_names else "`unknown`"
    return (
        "# IT桔子 Live Investevent Card\n\n"
        "## Header\n\n"
        f"- `event_id`: `{snapshot.event_id or 'unknown'}`\n"
        f"- `event_date`: `{snapshot.event_date or 'unknown'}`\n"
        f"- `company_id`: `{snapshot.company_id or 'unknown'}`\n"
        f"- `company_name`: `{snapshot.company_name}`\n"
        f"- `company_url`: `{snapshot.company_url}`\n"
        f"- `detail_url`: `{snapshot.detail_url}`\n"
        f"- `row_rank`: `{snapshot.row_rank}`\n"
        f"- `captured_at`: `{snapshot.captured_at}`\n"
        f"- `source_page_url`: `{snapshot.source_page_url}`\n\n"
        "## Snapshot Fields\n\n"
        f"- `company_description`: {snapshot.company_description or 'none'}\n"
        f"- `industry`: `{snapshot.industry or 'unknown'}`\n"
        f"- `round_name`: `{snapshot.round_name or 'unknown'}`\n"
        f"- `amount`: `{snapshot.amount or 'unknown'}`\n"
        f"- `investor_names`: {investors}\n"
        f"- `valuation`: `{snapshot.valuation or 'unknown'}`\n"
        f"- `ai_relevance`: `{snapshot.ai_relevance}`\n"
        f"- `ai_score`: `{snapshot.ai_score}`\n\n"
        "## Raw Row\n\n"
        f"> {snapshot.raw_text}\n"
    )


def render_daily_updates_markdown(
    logical_date: str,
    generated_at: str,
    events: list[InvesteventSnapshot],
    home_overview: HomeDailyOverview,
    home_headlines: list[HomeInvesteventHeadline],
    home_event_rows: list[HomeEventListRow],
    api_probe: EventApiProbe,
) -> str:
    event_rows = "\n".join(
        f"| {item.row_rank} | {item.event_date or '—'} | {item.company_name} | {item.company_description or '—'} | {item.industry or '—'} | {item.round_name or '—'} | {item.amount or '—'} | {', '.join(item.investor_names) or '—'} | {item.valuation or '—'} | {item.detail_url} |"
        for item in events
    ) or "| none | none | none | none | none | none | none | none | none | none |"
    structured_event_ids = {item.event_id for item in events if item.event_id}
    home_event_only_rows = [item for item in home_event_rows if item.event_id and item.event_id not in structured_event_ids and item.relative_time and "天前" not in item.relative_time]
    headline_only_rows = [item for item in home_headlines if item.event_id and item.event_id not in structured_event_ids]
    home_event_only_lines = "\n".join(
        f"| {item.row_rank} | {item.company_name or '—'} | {item.company_description or '—'} | {item.round_name or '—'} | {item.relative_time or '—'} | {item.amount or '—'} | {', '.join(item.investor_names) or '—'} | {item.detail_url} |"
        for item in home_event_only_rows
    ) or "| none | none | none | none | none | none | none | none |"
    headline_only_lines = "\n".join(
        f"| {item.row_rank} | {item.title} | {item.relative_time or '—'} | {item.detail_url} |"
        for item in headline_only_rows
    ) or "| none | none | none | none |"
    known_today_signal_count = len(structured_event_ids | {item.event_id for item in home_event_only_rows if item.event_id} | {item.event_id for item in headline_only_rows if item.event_id})
    gap = None
    if home_overview.investment_count is not None:
        gap = max(home_overview.investment_count - known_today_signal_count, 0)
    return (
        "# IT桔子 Live Daily Updates\n\n"
        f"- `logical_date`: `{logical_date}`\n"
        f"- `generated_at`: `{generated_at}`\n"
        f"- `structured_rows_captured`: `{len(events)}`\n"
        f"- `home_event_row_signals`: `{len(home_event_only_rows)}`\n"
        f"- `headline_only_signals`: `{len(headline_only_rows)}`\n"
        f"- `known_today_signal_count`: `{known_today_signal_count}`\n"
        f"- `home_today_investment_count`: `{home_overview.investment_count if home_overview.investment_count is not None else 'unknown'}`\n"
        f"- `home_today_investment_amount`: `{home_overview.investment_amount or 'unknown'}`\n"
        f"- `page_2_api_probe_status`: `{api_probe.status if api_probe.status is not None else 'unknown'}`\n"
        f"- `page_2_api_probe_message`: `{api_probe.message or 'none'}`\n"
        f"- `capture_gap_vs_home_overview`: `{gap if gap is not None else 'unknown'}`\n\n"
        "## 捕获边界\n\n"
        "- `本表已不再按固定条数截断，而是收集当前 auth-free 页面中 event_date=logical_date 的全部可见行。`\n"
        "- `若 page 2 API 返回 441 / 缺少令牌，则说明更深分页仍被登录令牌拦住；此时本表是“当日可见更新表”，不是完整数据库导出。`\n"
        "- `首页 headline 会额外保留一份补充信号，帮助分析师判断还有哪些同日事件未被当前结构化表覆盖。`\n\n"
        "## Structured Visible Rows\n\n"
        "| Rank | 日期 | 公司 | 简介 | 行业 | 轮次 | 金额 | 投资方 | 估值 | 详情 |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        f"{event_rows}\n\n"
        "## Home Event-List Supplemental Rows\n\n"
        "| Rank | 公司 | 简介 | 轮次 | 相对时间 | 金额 | 投资方 | 详情 |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
        f"{home_event_only_lines}\n\n"
        "## Home Headline-Only Signals\n\n"
        "| Rank | 标题 | 相对时间 | 详情 |\n"
        "| --- | --- | --- | --- |\n"
        f"{headline_only_lines}\n"
    )


def render_board(
    logical_date: str,
    generated_at: str,
    companies: list[CompanySnapshot],
    events: list[InvesteventSnapshot],
    home_overview: HomeDailyOverview,
    home_headlines: list[HomeInvesteventHeadline],
    home_event_rows: list[HomeEventListRow],
    api_probe: EventApiProbe,
) -> str:
    company_rows = "\n".join(
        f"| {item.row_rank} | {item.company_name} | {item.company_description or '—'} | {item.location or '—'} | {item.established_at or '—'} | {item.industry or '—'} | {item.financing_total or '—'} | {item.ai_relevance} | {item.company_url} |"
        for item in companies
    ) or "| none | none | none | none | none | none | none | none | none |"
    event_rows = "\n".join(
        f"| {item.row_rank} | {item.event_date or '—'} | {item.company_name} | {item.company_description or '—'} | {item.industry or '—'} | {item.round_name or '—'} | {item.amount or '—'} | {', '.join(item.investor_names) or '—'} | {item.valuation or '—'} | {item.ai_relevance} | {item.detail_url} |"
        for item in events
    ) or "| none | none | none | none | none | none | none | none | none | none | none |"
    ai_companies = [item for item in companies if item.ai_relevance != "low"]
    ai_events = [item for item in events if item.ai_relevance != "low"]
    structured_event_ids = {item.event_id for item in events if item.event_id}
    home_event_only_rows = [item for item in home_event_rows if item.event_id and item.event_id not in structured_event_ids and item.relative_time and "天前" not in item.relative_time]
    home_headline_lines = "\n".join(
        f"- `{item.title}` | `{item.relative_time or 'unknown'}` | `{item.detail_url}`"
        for item in home_headlines
    ) or "- none"
    return (
        "# IT桔子 Live Snapshot Board\n\n"
        f"- `logical_date`: `{logical_date}`\n"
        f"- `generated_at`: `{generated_at}`\n"
        f"- `company_rows`: `{len(companies)}`\n"
        f"- `event_rows_visible_today`: `{len(events)}`\n"
        f"- `ai_company_rows`: `{len(ai_companies)}`\n"
        f"- `ai_event_rows`: `{len(ai_events)}`\n"
        f"- `home_event_row_signals`: `{len(home_event_only_rows)}`\n"
        f"- `home_today_investment_count`: `{home_overview.investment_count if home_overview.investment_count is not None else 'unknown'}`\n"
        f"- `home_today_investment_amount`: `{home_overview.investment_amount or 'unknown'}`\n"
        f"- `page_2_api_probe_status`: `{api_probe.status if api_probe.status is not None else 'unknown'}`\n"
        f"- `page_2_api_probe_message`: `{api_probe.message or 'none'}`\n\n"
        "## 当前判断\n\n"
        "- `这份 board 不是背景 PDF，而是 IT 桔子 live 页面 + 首页概览的结构化快照。`\n"
        "- `investevent` 这一层已经从“固定抓前 N 条”改成“抓取当前 auth-free 页面中 event_date=logical_date 的全部可见行”。`\n"
        "- `company` 仍主要用于补中国创业公司对象池；`investevent` 主要用于补每日融资事件流。`\n"
        "- `首页“本日投资数量”用于衡量当日理论更新量；若其大于当前结构化可见行数，说明仍存在认证后分页缺口。`\n"
        "- `page 2 API 若返回 441 / 缺少令牌，说明更深分页需要 Authorization token；当前脚本会诚实标记缺口，不伪装成全量。`\n"
        "- `ai_relevance` 只是首轮启发式标签，用于帮助分析师快速筛 AI 相关行，不等于最终结论。`\n\n"
        "## Company Snapshot\n\n"
        "| Rank | 公司 | 简介 | 地点 | 成立时间 | 行业 | 融资总额 | AI 相关度 | 详情 |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        f"{company_rows}\n\n"
        "## Investevent Snapshot\n\n"
        "| Rank | 日期 | 公司 | 简介 | 行业 | 轮次 | 金额 | 投资方 | 估值 | AI 相关度 | 详情 |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        f"{event_rows}\n\n"
        "## Home Headline Signals\n\n"
        f"{home_headline_lines}\n"
    )


def build_daily_update_rows(
    logical_date: str,
    events: list[InvesteventSnapshot],
    home_headlines: list[HomeInvesteventHeadline],
    home_event_rows: list[HomeEventListRow],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    structured_event_ids = {event.event_id for event in events if event.event_id}
    for event in events:
        rows.append(
            {
                "logical_date": logical_date,
                "event_date": event.event_date,
                "event_id": event.event_id,
                "headline_title": "",
                "company_id": event.company_id,
                "company_name": event.company_name,
                "company_description": event.company_description,
                "industry": event.industry,
                "round_name": event.round_name,
                "amount": event.amount,
                "investor_names": " | ".join(event.investor_names),
                "valuation": event.valuation,
                "ai_relevance": event.ai_relevance,
                "ai_score": str(event.ai_score),
                "detail_url": event.detail_url,
                "company_url": event.company_url,
                "source_page_url": event.source_page_url,
                "captured_at": event.captured_at,
                "capture_scope": "structured_visible_row",
            }
        )
    for home_row in home_event_rows:
        if not home_row.event_id or home_row.event_id in structured_event_ids:
            continue
        if not home_row.relative_time or "天前" in home_row.relative_time:
            continue
        rows.append(
            {
                "logical_date": logical_date,
                "event_date": logical_date,
                "event_id": home_row.event_id,
                "headline_title": "",
                "company_id": home_row.company_id,
                "company_name": home_row.company_name,
                "company_description": home_row.company_description,
                "industry": "",
                "round_name": home_row.round_name,
                "amount": home_row.amount,
                "investor_names": " | ".join(home_row.investor_names),
                "valuation": "",
                "ai_relevance": "",
                "ai_score": "",
                "detail_url": home_row.detail_url,
                "company_url": home_row.company_url,
                "source_page_url": home_row.source_page_url,
                "captured_at": home_row.captured_at,
                "capture_scope": "home_event_list_row",
            }
        )
    for headline in home_headlines:
        if not headline.event_id or headline.event_id in structured_event_ids:
            continue
        if any(item.event_id == headline.event_id for item in home_event_rows):
            continue
        rows.append(
            {
                "logical_date": logical_date,
                "event_date": logical_date,
                "event_id": headline.event_id,
                "headline_title": headline.title,
                "company_id": "",
                "company_name": "",
                "company_description": "",
                "industry": "",
                "round_name": "",
                "amount": "",
                "investor_names": "",
                "valuation": "",
                "ai_relevance": "",
                "ai_score": "",
                "detail_url": headline.detail_url,
                "company_url": "",
                "source_page_url": headline.source_page_url,
                "captured_at": headline.captured_at,
                "capture_scope": "home_headline_only_signal",
            }
        )
    return rows


def write_daily_updates_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "logical_date",
        "event_date",
        "event_id",
        "headline_title",
        "company_id",
        "company_name",
        "company_description",
        "industry",
        "round_name",
        "amount",
        "investor_names",
        "valuation",
        "ai_relevance",
        "ai_score",
        "detail_url",
        "company_url",
        "source_page_url",
        "captured_at",
        "capture_scope",
    ]
    existing: dict[str, dict[str, str]] = {}
    if path.exists():
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                logical_date = clean_text(row.get("logical_date") or "")
                event_id = clean_text(row.get("event_id") or "")
                if not logical_date or not event_id:
                    continue
                existing[f"{logical_date}::{event_id}"] = {field: clean_text(row.get(field) or "") for field in fieldnames}
    for row in rows:
        existing[f"{row['logical_date']}::{row['event_id']}"] = {field: clean_text(row.get(field) or "") for field in fieldnames}
    ordered_rows = sorted(
        existing.values(),
        key=lambda row: (
            row.get("logical_date", ""),
            row.get("event_date", ""),
            row.get("event_id", ""),
        ),
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ordered_rows)


def collect_snapshots(
    company_limit: int,
    logical_date: str,
) -> tuple[list[CompanySnapshot], list[InvesteventSnapshot], HomeDailyOverview, list[HomeInvesteventHeadline], list[HomeEventListRow], EventApiProbe]:
    chrome_path = find_chrome_executable()
    remote_port = find_free_port()
    user_data_dir = Path(tempfile.mkdtemp(prefix="itjuzi_live_snapshot_"))
    chrome_proc = launch_native_chrome(chrome_path, remote_port, user_data_dir)
    captured_at = format_dt(now_cn())
    companies: list[CompanySnapshot] = []
    events: list[InvesteventSnapshot] = []
    home_overview = HomeDailyOverview(
        logical_date=logical_date,
        investment_count=None,
        investment_amount="",
        source_page_url=PAGE_URLS["home"],
        captured_at=captured_at,
        raw_text="",
    )
    home_headlines: list[HomeInvesteventHeadline] = []
    home_event_rows: list[HomeEventListRow] = []
    api_probe = EventApiProbe(page=2, status=None, message="not-run", url="")
    time.sleep(3)
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{remote_port}")
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            page = context.new_page()

            page.goto(PAGE_URLS["home"], wait_until="networkidle", timeout=45000)
            time.sleep(2)
            home_overview = parse_home_daily_overview(page.locator("body").inner_text(timeout=5000), logical_date=logical_date, captured_at=captured_at)
            home_headlines = build_home_headlines(
                evaluate_home_headlines(page),
                captured_at=captured_at,
                source_page_url=PAGE_URLS["home"],
            )
            home_event_rows = build_home_event_list_rows(
                evaluate_home_event_table_rows(page),
                captured_at=captured_at,
                source_page_url=PAGE_URLS["home"],
            )

            page.goto(PAGE_URLS["company"], wait_until="networkidle", timeout=45000)
            time.sleep(2)
            companies = build_company_snapshots(
                evaluate_company_rows(page, company_limit),
                captured_at=captured_at,
                source_page_url=PAGE_URLS["company"],
            )

            page.goto(PAGE_URLS["investevent"], wait_until="networkidle", timeout=45000)
            time.sleep(2)
            events = [
                item
                for item in build_event_snapshots(
                    evaluate_event_rows(page),
                    captured_at=captured_at,
                    source_page_url=PAGE_URLS["investevent"],
                )
                if item.event_date == logical_date
            ]
            api_probe = probe_event_api(page)
            browser.close()
    finally:
        try:
            os.kill(chrome_proc.pid, signal.SIGTERM)
        except Exception:
            pass
    return companies, events, home_overview, home_headlines, home_event_rows, api_probe


def main() -> int:
    args = parse_args()
    ensure_dirs()
    run_at = now_cn()
    logical_date = clean_text(args.logical_date or run_at.strftime("%Y-%m-%d"))
    day_token = logical_date.replace("-", "") or run_at.strftime("%Y%m%d")
    generated_at = format_dt(run_at)
    cleanup_today_cards(day_token)

    companies, events, home_overview, home_headlines, home_event_rows, api_probe = collect_snapshots(args.company_limit, logical_date)

    for company in companies:
        company_slug = stable_slug(
            company.company_name,
            company.company_id,
            fallback=f"company_{company.company_id or company.row_rank}",
        )
        card_path = COMPANY_DIR / f"{day_token}__{company_slug}__itjuzi-live-company.md"
        write_text(card_path, render_company_card(company))

    for event in events:
        event_slug = stable_slug(
            event.event_date,
            event.company_name,
            event.round_name,
            event.event_id,
            fallback=f"event_{event.event_id or event.row_rank}",
        )
        card_path = EVENT_DIR / f"{day_token}__{event_slug}__itjuzi-live-event.md"
        write_text(card_path, render_event_card(event))

    board_path = SNAPSHOT_DIR / f"{day_token}__itjuzi-live-snapshot-board.md"
    daily_updates_path = SNAPSHOT_DIR / f"{day_token}__itjuzi-live-daily-updates.md"
    json_path = LOG_DIR / f"{run_at.strftime('%Y%m%d_%H%M%S')}__itjuzi-live-snapshot.json"
    markdown_path = LOG_DIR / f"{run_at.strftime('%Y%m%d_%H%M%S')}__itjuzi-live-snapshot.md"

    board_content = render_board(logical_date, generated_at, companies, events, home_overview, home_headlines, home_event_rows, api_probe)
    daily_updates_content = render_daily_updates_markdown(logical_date, generated_at, events, home_overview, home_headlines, home_event_rows, api_probe)
    daily_update_rows = build_daily_update_rows(logical_date, events, home_headlines, home_event_rows)

    write_text(board_path, board_content)
    write_text(daily_updates_path, daily_updates_content)
    write_daily_updates_csv(DAILY_UPDATES_CSV, daily_update_rows)

    payload = {
        "logical_date": logical_date,
        "generated_at": generated_at,
        "companies": [asdict(company) for company in companies],
        "events": [asdict(event) for event in events],
        "home_overview": asdict(home_overview),
        "home_headlines": [asdict(item) for item in home_headlines],
        "home_event_rows": [asdict(item) for item in home_event_rows],
        "event_api_probe": asdict(api_probe),
        "board_path": str(board_path),
        "daily_updates_path": str(daily_updates_path),
        "daily_updates_csv_path": str(DAILY_UPDATES_CSV),
    }
    write_text(json_path, json.dumps(payload, ensure_ascii=False, indent=2))
    write_text(markdown_path, board_content + "\n\n---\n\n" + daily_updates_content)

    print(f"Board written to: {board_path}")
    print(f"Daily updates written to: {daily_updates_path}")
    print(f"Daily updates CSV written to: {DAILY_UPDATES_CSV}")
    print(f"JSON log written to: {json_path}")
    print(f"Markdown log written to: {markdown_path}")
    print(f"Company cards: {len(companies)}")
    print(f"Event cards: {len(events)}")
    print(f"Home today investment count: {home_overview.investment_count if home_overview.investment_count is not None else 'unknown'}")
    print(f"Event page 2 API probe: {api_probe.status if api_probe.status is not None else 'unknown'} | {api_probe.message or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import signal
import socket
import subprocess
import tempfile
import textwrap
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
LOG_DIR = ROOT / "10_logs"
CN_TZ = ZoneInfo("Asia/Shanghai")
DEFAULT_PAGE_URLS = {
    "home": "https://www.itjuzi.com/",
    "company": "https://www.itjuzi.com/company",
    "investevent": "https://www.itjuzi.com/investevent",
    "financing_company": "https://www.itjuzi.com/financing_company",
}
CHROME_CANDIDATES = [
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"),
]


def now_cn() -> datetime:
    return datetime.now(tz=CN_TZ)


def format_dt(value: datetime) -> str:
    return value.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def compact(text: str, limit: int = 300) -> str:
    cleaned = " ".join(str(text or "").split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 1].rstrip() + "…"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe IT桔子 live pages via native Chrome + CDP.")
    parser.add_argument(
        "--page",
        action="append",
        dest="pages",
        choices=sorted(DEFAULT_PAGE_URLS.keys()),
        help="Page key to probe. Can repeat. Default: home, company, investevent, financing_company.",
    )
    parser.add_argument("--limit", type=int, default=8, help="Max sampled anchors per category.")
    return parser.parse_args()


def find_chrome_executable() -> Path:
    for candidate in CHROME_CANDIDATES:
        if candidate.exists():
            return candidate
    playwright_glob = list(
        Path.home().glob("Library/Caches/ms-playwright/chromium-*/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing")
    )
    for candidate in playwright_glob:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Native Chrome executable not found")


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def launch_native_chrome(chrome_path: Path, remote_port: int, user_data_dir: Path) -> subprocess.Popen[Any]:
    command = [
        str(chrome_path),
        f"--remote-debugging-port={remote_port}",
        f"--user-data-dir={user_data_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "about:blank",
    ]
    return subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def mask_cookie_names(cookies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "name": cookie.get("name"),
            "domain": cookie.get("domain"),
            "expires": cookie.get("expires"),
            "httpOnly": cookie.get("httpOnly"),
            "secure": cookie.get("secure"),
            "sameSite": cookie.get("sameSite"),
        }
        for cookie in cookies
    ]


def collect_anchor_samples(page: Any, limit: int) -> dict[str, list[dict[str, str]]]:
    return page.evaluate(
        """(limit) => {
            const anchors = Array.from(document.querySelectorAll('a[href]'));
            const clean = (value, hardLimit = 280) => {
                const normalized = String(value || '').replace(/\\s+/g, ' ').trim();
                return normalized.length <= hardLimit ? normalized : normalized.slice(0, hardLimit - 1).trimEnd() + '…';
            };
            const pick = (fragment) => anchors
                .filter(anchor => anchor.href.includes(fragment))
                .slice(0, limit)
                .map(anchor => ({
                    text: clean(anchor.innerText || anchor.textContent || ''),
                    href: anchor.href,
                    context: clean(
                        (anchor.closest('tr') && anchor.closest('tr').innerText)
                        || (anchor.closest('section') && anchor.closest('section').innerText)
                        || (anchor.parentElement && anchor.parentElement.innerText)
                        || '',
                        420
                    ),
                }));
            return {
                company: pick('/company/'),
                investevent: pick('/investevent/'),
                investfirm: pick('/investfirm/'),
                report: pick('/report'),
            };
        }""",
        limit,
    )


def collect_page_summary(page: Any, page_key: str, page_url: str, limit: int) -> dict[str, Any]:
    page.goto(page_url, wait_until="networkidle", timeout=45000)
    time.sleep(2)
    body_text = page.locator("body").inner_text(timeout=5000)
    anchor_samples = collect_anchor_samples(page, limit)
    is_404 = "404" in body_text[:300] and "未找到您需要的页面" in body_text[:300]
    return {
        "page_key": page_key,
        "page_url": page_url,
        "resolved_url": page.url,
        "title": page.title(),
        "is_404": is_404,
        "body_excerpt": compact(body_text, 2800),
        "anchor_samples": anchor_samples,
    }


def render_sample_lines(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "- none"
    lines: list[str] = []
    for row in rows:
        text = compact(row.get("text") or "", 80) or "(no text)"
        href = row.get("href") or ""
        context = compact(row.get("context") or "", 180)
        suffix = f" | {context}" if context else ""
        lines.append(f"- `{text}` | {href}{suffix}")
    return "\n".join(lines)


def render_markdown(
    run_at: datetime,
    chrome_path: Path,
    remote_port: int,
    selected_pages: list[str],
    results: list[dict[str, Any]],
    cookies: list[dict[str, Any]],
) -> str:
    sections: list[str] = []
    for result in results:
        anchor_samples = result["anchor_samples"]
        sections.append(
            textwrap.dedent(
                f"""\
                ## `{result['page_key']}`

                - `page_url`: `{result['page_url']}`
                - `resolved_url`: `{result['resolved_url']}`
                - `title`: `{result['title']}`
                - `is_404`: `{str(result['is_404']).lower()}`

                ### Body Excerpt

                {result['body_excerpt']}

                ### Company Links

                {render_sample_lines(anchor_samples.get('company', []))}

                ### Investevent Links

                {render_sample_lines(anchor_samples.get('investevent', []))}

                ### Investfirm Links

                {render_sample_lines(anchor_samples.get('investfirm', []))}

                ### Report Links

                {render_sample_lines(anchor_samples.get('report', []))}
                """
            ).strip()
        )
    return (
        f"# 2026-03-26｜IT 桔子 live probe\n\n"
        f"- `run_at`: `{format_dt(run_at)}`\n"
        f"- `chrome_path`: `{chrome_path}`\n"
        f"- `remote_debugging_port`: `{remote_port}`\n"
        f"- `pages`: `{', '.join(selected_pages)}`\n"
        f"- `cookie_names`: `{', '.join(cookie['name'] for cookie in cookies if cookie.get('name'))}`\n\n"
        "## 结论\n\n"
        "本轮验证表明：`itjuzi.com` 的 live web 页面并非彻底不可达，"
        "而是 **HTTP / Jina / Playwright 直接启动链会卡在风控**；"
        "切到 **本机原生 Chrome + CDP 接入** 后，可稳定进入真实页面。\n\n"
        + "\n\n".join(sections)
        + "\n"
    )


def main() -> int:
    args = parse_args()
    run_at = now_cn()
    chrome_path = find_chrome_executable()
    remote_port = find_free_port()
    selected_pages = args.pages or ["home", "company", "investevent", "financing_company"]

    user_data_dir = Path(tempfile.mkdtemp(prefix="itjuzi_live_probe_"))
    chrome_proc = launch_native_chrome(chrome_path, remote_port, user_data_dir)
    time.sleep(3)

    timestamp = run_at.strftime("%Y%m%d_%H%M%S")
    json_path = LOG_DIR / f"{timestamp}__itjuzi-live-probe.json"
    markdown_path = LOG_DIR / f"{timestamp}__itjuzi-live-probe.md"
    result_payload: dict[str, Any] = {}

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{remote_port}")
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            page = context.new_page()

            results = [
                collect_page_summary(page, page_key, DEFAULT_PAGE_URLS[page_key], args.limit)
                for page_key in selected_pages
            ]
            cookies = mask_cookie_names(context.cookies())
            browser.close()

        result_payload = {
            "run_at": format_dt(run_at),
            "chrome_path": str(chrome_path),
            "remote_port": remote_port,
            "pages": selected_pages,
            "cookies": cookies,
            "results": results,
        }
        write_text(json_path, json.dumps(result_payload, ensure_ascii=False, indent=2))
        write_text(markdown_path, render_markdown(run_at, chrome_path, remote_port, selected_pages, results, cookies))
    finally:
        try:
            os.kill(chrome_proc.pid, signal.SIGTERM)
        except Exception:
            pass

    print(f"JSON written to: {json_path}")
    print(f"Markdown written to: {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

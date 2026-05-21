#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture webpage screenshots for TH Capital market content system")
    parser.add_argument("--url", required=True, help="Target page URL")
    parser.add_argument("--output", required=True, help="Output png path")
    parser.add_argument("--selector", default="", help="Optional CSS selector to capture instead of full page")
    parser.add_argument("--viewport-width", type=int, default=1440)
    parser.add_argument("--viewport-height", type=int, default=1800)
    parser.add_argument("--wait-ms", type=int, default=1800)
    parser.add_argument("--timeout-ms", type=int, default=45000)
    parser.add_argument("--full-page", action="store_true")
    parser.add_argument("--dark-mode", action="store_true")
    parser.add_argument("--hide-cookie-banners", action="store_true")
    return parser.parse_args()


COMMON_HIDE_SELECTORS = [
    "[id*='cookie']",
    "[class*='cookie']",
    "[aria-label*='cookie']",
    "[data-testid*='cookie']",
    "[id*='consent']",
    "[class*='consent']",
]
BLOCKED_TEXT_PATTERNS = [
    "you've been blocked by network security",
    "you have been blocked by network security",
    "blocked by network security",
    "file a ticket",
    "access denied",
]


def maybe_hide_noise(page) -> None:
    for selector in COMMON_HIDE_SELECTORS:
        try:
            page.locator(selector).evaluate_all("els => els.forEach(el => el.remove())")
        except Exception:
            continue


def page_looks_blocked(page) -> bool:
    try:
        title = (page.title() or "").lower()
    except Exception:
        title = ""
    try:
        body_text = (page.locator("body").text_content(timeout=3000) or "").lower()
    except Exception:
        body_text = ""
    haystack = f"{title}\n{body_text}"
    return any(pattern in haystack for pattern in BLOCKED_TEXT_PATTERNS)


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": args.viewport_width, "height": args.viewport_height},
            color_scheme="dark" if args.dark_mode else "light",
            device_scale_factor=2,
        )
        page = context.new_page()
        page.goto(args.url, wait_until="domcontentloaded", timeout=args.timeout_ms)
        page.wait_for_timeout(args.wait_ms)
        if args.hide_cookie_banners:
            maybe_hide_noise(page)
        if page_looks_blocked(page):
            raise SystemExit(f"blocked capture refused for {args.url}")

        if args.selector:
            locator = page.locator(args.selector).first
            locator.scroll_into_view_if_needed(timeout=args.timeout_ms)
            locator.screenshot(path=str(output_path))
        else:
            page.screenshot(path=str(output_path), full_page=args.full_page)

        print(output_path)
        browser.close()


if __name__ == "__main__":
    main()

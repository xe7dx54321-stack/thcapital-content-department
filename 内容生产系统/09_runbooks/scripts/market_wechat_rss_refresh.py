#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from market_wechat_source_defs import WECHAT_SOURCE_TARGETS, aliases_for_target, normalize_wechat_name


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
LOG_ROOT = ROOT / "10_logs"
CN_TZ = ZoneInfo("Asia/Shanghai")
BASE_URL = "http://localhost:8001/api/v1"
LOGIN_URL = f"{BASE_URL}/wx/auth/login"
MPS_URL = f"{BASE_URL}/wx/mps"
RSS_REFRESH_URL = f"{BASE_URL}/rss"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh half of TH Capital market-content WeChat RSS subscriptions.")
    parser.add_argument("--batch", choices=("a", "b"), required=True)
    parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="admin123")
    parser.add_argument("--sleep-seconds", type=float, default=1.5)
    parser.add_argument("--jitter-seconds", type=float, default=0.4)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write-log", action="store_true")
    return parser.parse_args()


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def request_json(
    url: str,
    *,
    method: str = "GET",
    data: dict[str, object] | None = None,
    token: str | None = None,
) -> dict[str, object]:
    payload = None
    headers: dict[str, str] = {}
    if data is not None:
        payload = urllib.parse.urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=payload, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read().decode("utf-8", "ignore")
    if not body:
        return {}
    parsed = json.loads(body)
    return parsed if isinstance(parsed, dict) else {"data": parsed}


def unwrap_success(payload: dict[str, object]) -> dict[str, object]:
    if payload.get("code") != 0:
        raise RuntimeError(f"WeMP request failed: {payload}")
    data = payload.get("data")
    return data if isinstance(data, dict) else {}


def login(username: str, password: str) -> str:
    payload = request_json(
        LOGIN_URL,
        method="POST",
        data={"username": username, "password": password},
    )
    token = ((payload.get("data") or {}) if isinstance(payload.get("data"), dict) else {}).get("access_token")
    if not token:
        raise RuntimeError(f"WeMP login failed: {payload}")
    return str(token)


def list_current_subscriptions(token: str) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    offset = 0
    page_size = 100
    while True:
        payload = request_json(f"{MPS_URL}?limit={page_size}&offset={offset}", token=token)
        data = unwrap_success(payload)
        page = data.get("list")
        if not isinstance(page, list) or not page:
            break
        items.extend(item for item in page if isinstance(item, dict))
        if len(page) < page_size:
            break
        offset += page_size
    return items


def refresh_feed(feed_id: str) -> None:
    encoded = urllib.parse.quote(feed_id, safe="")
    request = urllib.request.Request(f"{RSS_REFRESH_URL}/{encoded}/fresh", method="GET")
    with urllib.request.urlopen(request, timeout=30):
        return


def target_subscription_rows(subscriptions: list[dict[str, object]]) -> list[dict[str, str]]:
    name_map = {
        normalize_wechat_name(str(item.get("mp_name") or "")): item
        for item in subscriptions
        if str(item.get("mp_name") or "").strip()
    }
    rows: list[dict[str, str]] = []
    for target in WECHAT_SOURCE_TARGETS:
        matched = None
        for alias in aliases_for_target(target):
            matched = name_map.get(normalize_wechat_name(alias))
            if matched is not None:
                break
        rows.append(
            {
                "source_id": str(target["source_id"]),
                "source_name": str(target["source_name"]),
                "feed_id": str((matched or {}).get("id") or "").strip(),
                "mp_name": str((matched or {}).get("mp_name") or "").strip(),
            }
        )
    return rows


def select_batch(rows: list[dict[str, str]], batch: str) -> list[dict[str, str]]:
    ordered = sorted(rows, key=lambda row: row["source_id"])
    parity = 0 if batch == "a" else 1
    return [row for idx, row in enumerate(ordered) if idx % 2 == parity]


def render_markdown(summary: dict[str, object]) -> str:
    lines = [
        f"# 市场内容系统｜微信公众号 RSS 半批刷新 {str(summary['batch']).upper()}",
        "",
        f"- `generated_at`: `{summary['generated_at']}`",
        f"- `dry_run`: `{str(summary['dry_run']).lower()}`",
        f"- `planned_count`: `{summary['planned_count']}`",
        f"- `refreshed_count`: `{summary['refreshed_count']}`",
        f"- `missing_subscription_count`: `{summary['missing_subscription_count']}`",
        f"- `failed_count`: `{summary['failed_count']}`",
        "",
        "## Refreshed",
        "",
    ]
    if summary["refreshed"]:
        for row in summary["refreshed"]:
            lines.append(f"- `{row['source_id']}` | `{row['feed_id']}` | {row['mp_name']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Missing subscriptions", ""])
    if summary["missing"]:
        for row in summary["missing"]:
            lines.append(f"- `{row['source_id']}` | {row['source_name']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Failures", ""])
    if summary["failures"]:
        for row in summary["failures"]:
            lines.append(f"- `{row['source_id']}` | `{row['feed_id']}` | {row['message']}")
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def persist_summary(summary: dict[str, object]) -> tuple[Path, Path]:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    timestamp = now_cn().strftime("%Y%m%d_%H%M%S")
    md_path = LOG_ROOT / f"{timestamp}__market-wechat-rss-refresh-batch-{summary['batch']}.md"
    json_path = LOG_ROOT / f"{timestamp}__market-wechat-rss-refresh-batch-{summary['batch']}.json"
    md_path.write_text(render_markdown(summary), encoding="utf-8")
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return md_path, json_path


def main() -> int:
    args = parse_args()
    token = login(args.username, args.password)
    subscriptions = list_current_subscriptions(token)
    rows = target_subscription_rows(subscriptions)
    selected = select_batch(rows, args.batch)

    refreshed: list[dict[str, str]] = []
    missing: list[dict[str, str]] = []
    failures: list[dict[str, str]] = []

    for index, row in enumerate(selected, start=1):
        if not row["feed_id"]:
            missing.append({"source_id": row["source_id"], "source_name": row["source_name"]})
            continue
        try:
            if not args.dry_run:
                refresh_feed(row["feed_id"])
            refreshed.append(row)
        except Exception as exc:
            failures.append(
                {
                    "source_id": row["source_id"],
                    "feed_id": row["feed_id"],
                    "message": str(exc),
                }
            )
        if not args.dry_run and index < len(selected):
            delay = max(0.0, args.sleep_seconds + random.uniform(-args.jitter_seconds, args.jitter_seconds))
            time.sleep(delay)

    summary = {
        "generated_at": now_cn().strftime("%Y-%m-%d %H:%M:%S CST"),
        "batch": args.batch,
        "dry_run": args.dry_run,
        "planned_count": len(selected),
        "refreshed_count": len(refreshed),
        "missing_subscription_count": len(missing),
        "failed_count": len(failures),
        "refreshed": refreshed,
        "missing": missing,
        "failures": failures,
    }
    if args.write_log:
        md_path, json_path = persist_summary(summary)
        print(md_path)
        print(json_path)
    else:
        print(render_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

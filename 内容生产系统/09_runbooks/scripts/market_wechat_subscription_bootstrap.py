#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from market_wechat_source_defs import (
    WECHAT_SOURCE_TARGETS,
    aliases_for_target,
    normalize_wechat_name,
)


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
LOG_ROOT = ROOT / "10_logs"
CN_TZ = ZoneInfo("Asia/Shanghai")
BASE_URL = "http://localhost:8001/api/v1"
LOGIN_URL = f"{BASE_URL}/wx/auth/login"
MPS_URL = f"{BASE_URL}/wx/mps"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap TH Capital market-content WeChat subscriptions in WeMP-RSS.")
    parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="admin123")
    parser.add_argument("--write-log", action="store_true")
    parser.add_argument("--apply", action="store_true", help="Actually add missing subscriptions.")
    return parser.parse_args()


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def request_json(
    url: str,
    *,
    method: str = "GET",
    data: dict[str, object] | None = None,
    token: str | None = None,
    json_body: bool = False,
) -> dict[str, object]:
    payload = None
    headers: dict[str, str] = {}
    if data is not None:
        if json_body:
            payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        else:
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


def search_mp(token: str, query: str) -> list[dict[str, object]]:
    encoded = urllib.parse.quote(query)
    payload = request_json(f"{MPS_URL}/search/{encoded}", token=token)
    data = unwrap_success(payload)
    items = data.get("list")
    return [item for item in items if isinstance(item, dict)] if isinstance(items, list) else []


def candidate_name(item: dict[str, object]) -> str:
    return str(item.get("nickname") or item.get("mp_name") or item.get("name") or "").strip()


def candidate_id(item: dict[str, object]) -> str:
    return str(item.get("mp_id") or item.get("id") or item.get("fakeid") or "").strip()


def candidate_avatar(item: dict[str, object]) -> str:
    return str(item.get("avatar") or item.get("mp_cover") or item.get("round_head_img") or "").strip()


def choose_match(target: dict[str, object], items: list[dict[str, object]]) -> dict[str, object] | None:
    if not items:
        return None
    alias_keys = [normalize_wechat_name(alias) for alias in aliases_for_target(target) if alias]
    best_score = -1
    best_item: dict[str, object] | None = None
    for item in items:
        name = candidate_name(item)
        name_key = normalize_wechat_name(name)
        score = 0
        if name_key in alias_keys:
            score += 100
        for alias_key in alias_keys:
            if alias_key and alias_key in name_key:
                score += 40
        if candidate_id(item):
            score += 5
        if candidate_avatar(item):
            score += 5
        if item.get("verify_status") in {1, 2}:
            score += 5
        if score > best_score:
            best_score = score
            best_item = item
    return best_item if best_score > 0 else None


def add_subscription(token: str, item: dict[str, object]) -> dict[str, object]:
    payload = {
        "mp_name": candidate_name(item),
        "mp_cover": candidate_avatar(item),
        "avatar": candidate_avatar(item),
        "mp_id": candidate_id(item),
        "mp_intro": str(item.get("signature") or item.get("mp_intro") or item.get("intro") or "").strip(),
    }
    if not payload["mp_name"] or not payload["mp_id"]:
        raise RuntimeError(f"search result missing required fields: {item}")
    response = request_json(MPS_URL, method="POST", data=payload, token=token, json_body=True)
    return unwrap_success(response)


def render_markdown(summary: dict[str, object]) -> str:
    lines = [
        "# 市场内容系统｜微信公众号订阅补齐",
        "",
        f"- `generated_at`: `{summary['generated_at']}`",
        f"- `apply`: `{str(summary['apply']).lower()}`",
        f"- `subscription_total`: `{summary['subscription_total']}`",
        f"- `added_count`: `{summary['added_count']}`",
        f"- `already_exists_count`: `{summary['already_exists_count']}`",
        f"- `missing_count`: `{summary['missing_count']}`",
        f"- `failed_count`: `{summary['failed_count']}`",
        "",
        "## Results",
        "",
        "| source_id | source_name | status | query | matched_name | matched_id | message |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in summary["results"]:
        lines.append(
            f"| `{row['source_id']}` | {row['source_name']} | `{row['status']}` | "
            f"{row['query']} | {row['matched_name'] or '-'} | `{row['matched_id'] or '-'}` | {row['message']} |"
        )
    lines.append("")
    return "\n".join(lines)


def persist_summary(summary: dict[str, object]) -> tuple[Path, Path]:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    timestamp = now_cn().strftime("%Y%m%d_%H%M%S")
    md_path = LOG_ROOT / f"{timestamp}__market-wechat-subscription-bootstrap.md"
    json_path = LOG_ROOT / f"{timestamp}__market-wechat-subscription-bootstrap.json"
    md_path.write_text(render_markdown(summary), encoding="utf-8")
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return md_path, json_path


def main() -> int:
    args = parse_args()
    token = login(args.username, args.password)
    current = list_current_subscriptions(token)
    current_name_map = {
        normalize_wechat_name(str(item.get("mp_name") or "")): item for item in current if str(item.get("mp_name") or "").strip()
    }

    results: list[dict[str, str]] = []
    added_count = 0
    already_exists_count = 0
    missing_count = 0
    failed_count = 0

    for target in WECHAT_SOURCE_TARGETS:
        alias_keys = [normalize_wechat_name(alias) for alias in aliases_for_target(target)]
        existing = next((current_name_map[key] for key in alias_keys if key in current_name_map), None)
        if existing is not None:
            already_exists_count += 1
            results.append(
                {
                    "source_id": str(target["source_id"]),
                    "source_name": str(target["source_name"]),
                    "status": "already_exists",
                    "query": str(target["query"]),
                    "matched_name": str(existing.get("mp_name") or ""),
                    "matched_id": str(existing.get("id") or ""),
                    "message": "订阅已存在，无需重复添加。",
                }
            )
            continue

        try:
            items = search_mp(token, str(target["query"]))
            matched = choose_match(target, items)
            if matched is None:
                missing_count += 1
                results.append(
                    {
                        "source_id": str(target["source_id"]),
                        "source_name": str(target["source_name"]),
                        "status": "not_found",
                        "query": str(target["query"]),
                        "matched_name": "",
                        "matched_id": "",
                        "message": "搜索未找到足够可信的公众号结果。",
                    }
                )
                continue

            matched_name = candidate_name(matched)
            matched_id = candidate_id(matched)
            if args.apply:
                add_subscription(token, matched)
                added_count += 1
                status = "added"
                message = "已补订阅到 WeMP-RSS。"
            else:
                status = "ready_to_add"
                message = "已找到候选，可在 apply 模式下自动补订阅。"
            results.append(
                {
                    "source_id": str(target["source_id"]),
                    "source_name": str(target["source_name"]),
                    "status": status,
                    "query": str(target["query"]),
                    "matched_name": matched_name,
                    "matched_id": matched_id,
                    "message": message,
                }
            )
        except urllib.error.HTTPError as exc:
            failed_count += 1
            results.append(
                {
                    "source_id": str(target["source_id"]),
                    "source_name": str(target["source_name"]),
                    "status": "failed",
                    "query": str(target["query"]),
                    "matched_name": "",
                    "matched_id": "",
                    "message": f"HTTP {exc.code}",
                }
            )
        except Exception as exc:
            failed_count += 1
            results.append(
                {
                    "source_id": str(target["source_id"]),
                    "source_name": str(target["source_name"]),
                    "status": "failed",
                    "query": str(target["query"]),
                    "matched_name": "",
                    "matched_id": "",
                    "message": str(exc),
                }
            )

    summary = {
        "generated_at": now_cn().strftime("%Y-%m-%d %H:%M:%S CST"),
        "apply": args.apply,
        "subscription_total": len(current),
        "added_count": added_count,
        "already_exists_count": already_exists_count,
        "missing_count": missing_count,
        "failed_count": failed_count,
        "results": results,
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

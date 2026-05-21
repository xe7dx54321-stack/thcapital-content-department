#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def china_tz() -> timezone | ZoneInfo:
    try:
        return ZoneInfo("Asia/Shanghai")
    except ZoneInfoNotFoundError:
        return timezone(timedelta(hours=8), name="CST")


CN_TZ = china_tz()
URL_RE = re.compile(r"https?://[^\s)]+")
WINDOW_DAYS = 7
FOLLOWER_CONTEXT_DAYS = 3


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def now_iso() -> str:
    return now_cn().isoformat()


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return value if value else fallback


def normalize_title(value: str) -> str:
    return re.sub(r"[^\w]+", "", value or "").lower()


def parse_iso_dt(raw: str) -> datetime | None:
    raw = clean(raw, "")
    if not raw or raw == "n/a":
        return None
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=CN_TZ)
    return dt.astimezone(CN_TZ)


def parse_publish_dt(raw: str) -> datetime | None:
    parsed = parse_iso_dt(raw)
    if parsed is not None:
        return parsed
    raw = clean(raw, "")
    if not raw or raw == "n/a":
        return None
    for fmt in (
        "%Y-%m-%d %H:%M:%S CST",
        "%Y-%m-%d %H:%M CST",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
    ):
        try:
            return datetime.strptime(raw, fmt).replace(tzinfo=CN_TZ)
        except ValueError:
            continue
    return None


def request_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def request_dirs(root_dir: Path) -> list[Path]:
    requests_dir = root_dir / "requests"
    if not requests_dir.exists():
        return []
    return sorted([path for path in requests_dir.iterdir() if path.is_dir()])


def publish_confirmation_path(request_dir: Path) -> Path:
    return request_dir / "publish_confirmation.json"


def load_publish_confirmation(request_dir: Path) -> dict[str, Any]:
    path = publish_confirmation_path(request_dir)
    if not path.exists():
        return {}
    try:
        return request_json(path)
    except Exception:
        return {}


def is_official_metrics_ready(publish_dt: datetime, now_dt: datetime) -> tuple[bool, datetime]:
    ready_at = datetime.combine(publish_dt.date() + timedelta(days=1), time(hour=8, minute=0), tzinfo=CN_TZ)
    return now_dt >= ready_at, ready_at


def latest_scene_breakdown(detail: dict[str, Any]) -> str:
    parts: list[str] = []
    for row in (detail.get("read_user_source") or [])[:6]:
        scene = clean(str(row.get("scene_desc", "")), "")
        count = clean(str(row.get("user_count", "")), "")
        if scene and count:
            parts.append(f"{scene}={count}")
    return " | ".join(parts) if parts else "n/a"


def latest_jump_breakdown(detail: dict[str, Any]) -> str:
    parts: list[str] = []
    for row in (detail.get("read_jump_position") or []):
        position = clean(str(row.get("position", "")), "")
        rate = clean(str(row.get("rate", "")), "")
        if position and rate:
            parts.append(f"{position}={rate}")
    return " | ".join(parts) if parts else "n/a"


def format_follower_summary(context: dict[str, Any]) -> str:
    if clean(str(context.get("status", "n/a")), "n/a") != "ready":
        return clean(str(context.get("message", "n/a")), "n/a")
    parts: list[str] = []
    for row in (context.get("rows") or [])[: FOLLOWER_CONTEXT_DAYS + 1]:
        ref_date = clean(str(row.get("ref_date", "")), "n/a")
        net_user = clean(str(row.get("net_user", "n/a")), "n/a")
        cumulate_user = clean(str(row.get("cumulate_user", "n/a")), "n/a")
        parts.append(f"{ref_date}: net={net_user}, cumulate={cumulate_user}")
    return " | ".join(parts + [f"window_net_total={clean(str(context.get('net_total', 'n/a')), 'n/a')}"])


def build_follower_context(publisher: Any, publish_date: date, now_dt: datetime) -> dict[str, Any]:
    end_day = min(now_dt.date() - timedelta(days=1), publish_date + timedelta(days=FOLLOWER_CONTEXT_DAYS))
    if end_day < publish_date:
        return {"status": "waiting_t_plus_one", "message": "followers summary is also T+1"}
    begin_text = publish_date.isoformat()
    end_text = end_day.isoformat()
    try:
        summary_payload = publisher.user_summary(begin_text, end_text)
        cumulate_payload = publisher.user_cumulate(begin_text, end_text)
    except Exception as exc:
        return {"status": "official_api_error", "message": str(exc)}
    summary_rows = summary_payload.get("list") or []
    daily: dict[str, dict[str, int]] = {}
    for row in summary_rows:
        ref_date = clean(str(row.get("ref_date", "")), "")
        if not ref_date:
            continue
        bucket = daily.setdefault(ref_date, {"new_user": 0, "cancel_user": 0, "net_user": 0})
        bucket["new_user"] += int(row.get("new_user") or 0)
        bucket["cancel_user"] += int(row.get("cancel_user") or 0)
    for ref_date, bucket in daily.items():
        bucket["net_user"] = bucket["new_user"] - bucket["cancel_user"]
    cumulate_rows = {
        clean(str(row.get("ref_date", "")), ""): int(row.get("cumulate_user") or 0)
        for row in (cumulate_payload.get("list") or [])
        if clean(str(row.get("ref_date", "")), "")
    }
    ordered_dates = sorted(daily.keys())
    rows: list[dict[str, Any]] = []
    net_total = 0
    for ref_date in ordered_dates:
        bucket = daily[ref_date]
        net_total += bucket["net_user"]
        rows.append(
            {
                "ref_date": ref_date,
                "new_user": bucket["new_user"],
                "cancel_user": bucket["cancel_user"],
                "net_user": bucket["net_user"],
                "cumulate_user": cumulate_rows.get(ref_date, "n/a"),
            }
        )
    return {
        "status": "ready" if rows else "empty",
        "message": "ok" if rows else "no follower summary rows yet",
        "begin_date": begin_text,
        "end_date": end_text,
        "rows": rows,
        "net_total": net_total,
    }


def fetch_recent_published(publisher: Any, page_size: int = 20, max_pages: int = 5) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    offset = 0
    for _ in range(max(1, max_pages)):
        payload = publisher.freepublish_batchget(offset=offset, count=page_size, no_content=0)
        raw_items = payload.get("item") or []
        total_count = int(payload.get("total_count") or 0)
        if not raw_items:
            break
        for raw_item in raw_items:
            article_id = clean(str(raw_item.get("article_id", "")), "")
            publish_id = clean(str(raw_item.get("publish_id", article_id)), article_id or "n/a")
            update_time = int(raw_item.get("update_time") or 0)
            update_dt = datetime.fromtimestamp(update_time, CN_TZ) if update_time > 0 else None
            for idx, news_item in enumerate(((raw_item.get("content") or {}).get("news_item") or []), start=1):
                results.append(
                    {
                        "article_id": article_id,
                        "publish_id": publish_id,
                        "idx": idx,
                        "title": clean(str(news_item.get("title", "")), ""),
                        "url": clean(str(news_item.get("url", "")), ""),
                        "update_time": update_time,
                        "update_dt": update_dt,
                    }
                )
        offset += len(raw_items)
        if total_count and offset >= total_count:
            break
    results.sort(key=lambda item: item.get("update_time") or 0, reverse=True)
    return results


def candidate_publish_dates(
    request_payload: dict,
    result_payload: dict,
    now_dt: datetime,
    anchor_publish_dt: datetime | None = None,
) -> list[date]:
    anchors = [
        anchor_publish_dt,
        parse_iso_dt(str(result_payload.get("completed_at", ""))),
        parse_iso_dt(str(request_payload.get("created_at", ""))),
    ]
    anchor_dt = next((dt for dt in anchors if dt is not None), now_dt)
    begin_day = anchor_dt.date()
    end_day = min(now_dt.date() - timedelta(days=1), begin_day + timedelta(days=WINDOW_DAYS))
    if end_day < begin_day:
        return [begin_day]
    days: list[date] = []
    cursor = begin_day
    while cursor <= end_day:
        days.append(cursor)
        cursor += timedelta(days=1)
    return days


def build_official_metrics(request_dir: Path, publisher: Any, published_articles: list[dict[str, Any]], detail_cache: dict[str, dict[str, Any]]) -> dict[str, Any]:
    request_payload = request_json(request_dir / "request.json")
    result_payload = request_json(request_dir / "result.json")
    publish_confirmation = load_publish_confirmation(request_dir)
    title = clean(str((request_payload.get("article") or {}).get("title", "")), request_dir.name)
    now_dt = now_cn()
    request_dt = parse_iso_dt(str(result_payload.get("completed_at", ""))) or parse_iso_dt(str(request_payload.get("created_at", ""))) or now_dt
    confirmed_publish_dt = (
        parse_publish_dt(str(publish_confirmation.get("published_at_iso", "")))
        or parse_publish_dt(str(publish_confirmation.get("published_at", "")))
    )
    confirmation_publish_url = clean(str(publish_confirmation.get("publish_url", "")), "n/a")
    confirmation_present = (
        clean(str(publish_confirmation.get("status", "")), "") == "published"
        or confirmed_publish_dt is not None
        or confirmation_publish_url != "n/a"
    )
    state: dict[str, Any] = {
        "status": "waiting_publish",
        "message": "draft exists but manual publish is not confirmed yet",
        "captured_at": now_iso(),
        "metric_source": "windows bridge wechat official api",
        "title": title,
        "publish_url": "n/a",
        "article_id": "n/a",
        "published_at": "n/a",
        "publish_date": "n/a",
        "publish_time_source": "n/a",
        "official_ready_at": "n/a",
        "latest_stat_date": "n/a",
        "latest": {},
        "detail_list": [],
        "read_source_breakdown": "n/a",
        "jump_breakdown": "n/a",
        "follower_context": {},
        "follower_summary": "n/a",
        "bridge_consumer_version": "2026-04-02-official-metrics-sync-v1",
    }
    if clean(str(result_payload.get("status", "")), "") != "success":
        return state

    normalized_title = normalize_title(title)
    published_match = next((row for row in published_articles if normalize_title(str(row.get("title", ""))) == normalized_title), None)
    if published_match:
        state["publish_url"] = clean(str(published_match.get("url", "")), "n/a")
        state["article_id"] = clean(str(published_match.get("article_id", "")), "n/a")
        publish_dt = published_match.get("update_dt")
        if publish_dt is not None:
            state["published_at"] = publish_dt.strftime("%Y-%m-%d %H:%M:%S CST")
            state["publish_date"] = publish_dt.date().isoformat()
            state["publish_time_source"] = "freepublish_batchget"
            ready, ready_at = is_official_metrics_ready(publish_dt, now_dt)
            state["official_ready_at"] = ready_at.isoformat()
    elif confirmation_present:
        if confirmation_publish_url != "n/a":
            state["publish_url"] = confirmation_publish_url
        if confirmed_publish_dt is not None:
            state["published_at"] = confirmed_publish_dt.strftime("%Y-%m-%d %H:%M:%S CST")
            state["publish_date"] = confirmed_publish_dt.date().isoformat()
            state["publish_time_source"] = clean(str(publish_confirmation.get("publish_time_source", "")), "publish_confirmation")
            ready, ready_at = is_official_metrics_ready(confirmed_publish_dt, now_dt)
            state["official_ready_at"] = ready_at.isoformat()
        else:
            state["publish_time_source"] = clean(str(publish_confirmation.get("publish_time_source", "")), "publish_confirmation")
            state["message"] = "manual publish confirmed, but publish timestamp is still pending"

    effective_publish_dt = published_match.get("update_dt") if published_match is not None else confirmed_publish_dt
    if published_match is None and not confirmation_present:
        return state
    if effective_publish_dt is None:
        state["status"] = "published_time_pending"
        state["message"] = "manual publish confirmed, but publish timestamp is still pending"
        return state

    if not ready:
        state["status"] = "waiting_t_plus_one"
        state["message"] = "official WeChat metrics are T+1 and available after next-day 08:00 CST"
        state["follower_context"] = build_follower_context(publisher, effective_publish_dt.date(), now_dt)
        state["follower_summary"] = format_follower_summary(state["follower_context"])
        return state

    matched_row = None
    matched_day = None
    for publish_day in candidate_publish_dates(request_payload, result_payload, now_dt, effective_publish_dt):
        publish_day_text = publish_day.isoformat()
        if publish_day_text not in detail_cache:
            try:
                detail_cache[publish_day_text] = publisher.article_total_detail(publish_day_text)
            except Exception as exc:
                state["status"] = "official_api_error"
                state["message"] = str(exc)
                return state
        payload = detail_cache[publish_day_text]
        for row in (payload.get("list") or []):
            row_title = clean(str(row.get("title", "")), "")
            if normalize_title(row_title) == normalized_title:
                matched_row = row
                matched_day = publish_day_text
                state["is_delay"] = clean(str(payload.get("is_delay", "n/a")), "n/a")
                break
        if matched_row is not None:
            break

    if matched_row is None:
        state["status"] = "article_not_found"
        state["message"] = "published article not found in official datacube list yet"
        state["follower_context"] = build_follower_context(publisher, effective_publish_dt.date(), now_dt)
        state["follower_summary"] = format_follower_summary(state["follower_context"])
        return state

    detail_list = matched_row.get("detail_list") or []
    latest_detail = detail_list[-1] if detail_list else {}
    state["status"] = "ready"
    state["message"] = "ok"
    state["publish_date"] = matched_day or state["publish_date"]
    state["publish_url"] = clean(str(matched_row.get("content_url", "")), state["publish_url"])
    state["latest_stat_date"] = clean(str(latest_detail.get("stat_date", "")), "n/a")
    state["latest"] = latest_detail
    state["detail_list"] = detail_list
    state["read_source_breakdown"] = latest_scene_breakdown(latest_detail)
    state["jump_breakdown"] = latest_jump_breakdown(latest_detail)
    state["follower_context"] = build_follower_context(publisher, effective_publish_dt.date(), now_dt)
    state["follower_summary"] = format_follower_summary(state["follower_context"])
    return state


def sync_official_metrics(root_dir: Path, publisher: Any) -> list[str]:
    outputs: list[str] = []
    detail_cache: dict[str, dict[str, Any]] = {}
    try:
        published_articles = fetch_recent_published(publisher)
    except Exception as exc:
        published_articles = []
        outputs.append(f"METRICS_SYNC_SKIPPED freepublish fetch failed: {exc}")
    for request_dir in request_dirs(root_dir):
        request_path = request_dir / "request.json"
        result_path = request_dir / "result.json"
        if not request_path.exists() or not result_path.exists():
            continue
        try:
            request_payload = request_json(request_path)
            result_payload = request_json(result_path)
        except Exception as exc:
            outputs.append(f"METRICS_SYNC_FAILED {request_dir.name} {exc}")
            continue
        if clean(str(result_payload.get("status", "")), "") != "success":
            continue
        metrics_payload = build_official_metrics(request_dir, publisher, published_articles, detail_cache)
        metrics_path = request_dir / "official_metrics.json"
        metrics_path.write_text(json.dumps(metrics_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        outputs.append(f"METRICS_SYNCED {request_dir.name} status={metrics_payload.get('status', 'n/a')}")
    if not outputs:
        outputs.append("METRICS_SYNC_NOOP")
    return outputs

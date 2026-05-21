from __future__ import annotations

import re
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


CN_TZ = ZoneInfo("Asia/Shanghai")
DAY_MAINLINE_LANE = "day_mainline"
MORNING_FLASH_LANE = "morning_flash"
PUBLISH_MODE_DRAFT_ONLY = "draft_only"
PUBLISH_MODE_AUTO_API = "auto_api"

BUSINESS_WINDOW_START = "17:00"
BUSINESS_WINDOW_END = "14:30"
MORNING_FLASH_WINDOW_START = BUSINESS_WINDOW_START
MORNING_FLASH_WINDOW_END = "05:00"
DAY_MAINLINE_DELIVERY_DEADLINE = "19:00"
MORNING_FLASH_DELIVERY_DEADLINE = "06:50"
_CST_FORMATS = (
    "%Y-%m-%d %H:%M:%S CST",
    "%Y-%m-%d %H:%M CST",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
)


def clean_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().strip("`")


def day_token(date_text: str) -> str:
    return date.fromisoformat(date_text).strftime("%Y%m%d")


def parse_cst(raw: str | None) -> datetime | None:
    text = clean_text(raw)
    if not text or text.lower() in {"n/a", "none", "unknown", "not_found"}:
        return None
    for fmt in _CST_FORMATS:
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=CN_TZ)
        except ValueError:
            continue
    return None


def parse_hm(raw: str) -> time:
    hour, minute = [int(part) for part in raw.split(":", 1)]
    return time(hour=hour, minute=minute)


def format_cst(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def lane_window_bounds(lane: str) -> tuple[str, str]:
    normalized = clean_text(lane).lower()
    if normalized == MORNING_FLASH_LANE:
        return MORNING_FLASH_WINDOW_START, MORNING_FLASH_WINDOW_END
    return BUSINESS_WINDOW_START, BUSINESS_WINDOW_END


def lane_publish_mode_default(lane: str) -> str:
    normalized = clean_text(lane).lower()
    if normalized == MORNING_FLASH_LANE:
        return PUBLISH_MODE_AUTO_API
    return PUBLISH_MODE_DRAFT_ONLY


def lane_selection_scope_default(lane: str) -> str:
    normalized = clean_text(lane).lower()
    if normalized == MORNING_FLASH_LANE:
        return "previous_day_17_to_today_05_roundup_window"
    return "previous_day_17_to_today_1430_full_window_excluding_morning_flash"


def lane_delivery_deadline_hm(lane: str) -> str:
    normalized = clean_text(lane).lower()
    if normalized == MORNING_FLASH_LANE:
        return MORNING_FLASH_DELIVERY_DEADLINE
    return DAY_MAINLINE_DELIVERY_DEADLINE


def lane_delivery_deadline(date_text: str, lane: str) -> datetime:
    target_day = date.fromisoformat(date_text)
    deadline_hm = lane_delivery_deadline_hm(lane)
    return datetime.combine(target_day, parse_hm(deadline_hm), tzinfo=CN_TZ)


def business_window(
    date_text: str,
    start_hm: str = BUSINESS_WINDOW_START,
    end_hm: str = BUSINESS_WINDOW_END,
) -> tuple[datetime, datetime]:
    target_day = date.fromisoformat(date_text)
    start_day = target_day - timedelta(days=1)
    return (
        datetime.combine(start_day, parse_hm(start_hm), tzinfo=CN_TZ),
        datetime.combine(target_day, parse_hm(end_hm), tzinfo=CN_TZ),
    )


def business_window_status(date_text: str, now_dt: datetime | None = None) -> str:
    _, end_dt = business_window(date_text)
    current = (now_dt or datetime.now(CN_TZ)).astimezone(CN_TZ)
    return "open" if current < end_dt else "closed"


def timestamp_from_name(path_value: str | Path | None) -> datetime | None:
    if not path_value:
        return None
    name = Path(path_value).name
    try:
        return datetime.strptime(name[:15], "%Y%m%d_%H%M%S").replace(tzinfo=CN_TZ)
    except ValueError:
        return None


def timestamp_in_business_window(
    ts: datetime | None,
    date_text: str,
    start_hm: str = BUSINESS_WINDOW_START,
    end_hm: str = BUSINESS_WINDOW_END,
) -> bool:
    if ts is None:
        return False
    start_dt, end_dt = business_window(date_text, start_hm=start_hm, end_hm=end_hm)
    return start_dt <= ts <= end_dt


def text_timestamp_in_business_window(
    raw: str | None,
    date_text: str,
    start_hm: str = BUSINESS_WINDOW_START,
    end_hm: str = BUSINESS_WINDOW_END,
) -> bool:
    return timestamp_in_business_window(parse_cst(raw), date_text, start_hm=start_hm, end_hm=end_hm)


def path_in_business_window(
    path_value: str | Path | None,
    date_text: str,
    start_hm: str = BUSINESS_WINDOW_START,
    end_hm: str = BUSINESS_WINDOW_END,
) -> bool:
    return timestamp_in_business_window(timestamp_from_name(path_value), date_text, start_hm=start_hm, end_hm=end_hm)


def window_file_tokens(paths: list[Path]) -> list[str]:
    tokens = {
        path.name[:8]
        for path in paths
        if len(path.name) >= 8 and path.name[:8].isdigit()
    }
    return sorted(tokens)

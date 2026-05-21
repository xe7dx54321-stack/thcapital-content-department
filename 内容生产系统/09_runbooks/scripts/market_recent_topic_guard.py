#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
QUEUE_ROOT = ROOT / "06_publish_queue"
LOG_ROOT = ROOT / "10_logs"
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
HEADING_RE = re.compile(r"^#\s+(.+)$", re.M)
TOKEN_RE = re.compile(r"[a-z0-9]+")
DATE_SUFFIX_RE = re.compile(r"(?:^|_)(20\d{6}|20\d{2})(?:$|_)")
ROUNDUP_DATE_RE = re.compile(r"(20\d{2}[-/年]\d{1,2}(?:[-/月]\d{1,2}日?)?|\d{1,2}月\d{1,2}日)")
ROUNDUP_KEYWORDS_EN = ("roundup", "brief", "digest", "snapshot", "bulletin")
ROUNDUP_KEYWORDS_CN = ("早报", "早知道", "热点新闻", "新闻早知道", "快讯", "日报", "速览")
GENERIC_TOKENS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "into",
    "today",
    "yesterday",
    "morning",
    "flash",
    "daily",
    "hot",
    "topic",
    "capital",
    "content",
    "system",
    "market",
    "wechat",
    "article",
    "post",
    "story",
}
BLOCKING_STATUSES = {"waiting_human_publish", "published", "reviewed"}
DEFAULT_LOOKBACK_HOURS = 120


@dataclass(frozen=True)
class TopicRecord:
    queue_key: str
    topic_key: str
    title: str
    angle: str
    status: str
    delivery_lane: str
    platform: str
    happened_at: datetime
    path: Path

    @property
    def fingerprint_text(self) -> str:
        return " ".join(part for part in [self.topic_key, self.title, self.angle] if part)


@dataclass(frozen=True)
class TopicConflict:
    record: TopicRecord
    reason: str
    similarity: float
    shared_tokens: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Guard morning topic selection against recent duplicate topics.")
    parser.add_argument("--topic-key", required=True, help="Candidate topic key")
    parser.add_argument("--title", required=True, help="Candidate title")
    parser.add_argument("--approved-angle", default="", help="Candidate approved angle / one-line judgment")
    parser.add_argument("--delivery-lane", default="morning_flash")
    parser.add_argument("--lookback-hours", type=int, default=DEFAULT_LOOKBACK_HOURS)
    parser.add_argument("--exclude-queue-key", action="append", default=[], help="Queue key(s) to exclude")
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def clean(value: str, fallback: str = "") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return value if value else fallback


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def parse_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def parse_dt(raw: str) -> datetime | None:
    value = clean(raw)
    if not value or value == "n/a":
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S CST", "%Y-%m-%d %H:%M CST", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=CN_TZ)
        except ValueError:
            continue
    return None


def path_timestamp(path: Path) -> datetime:
    match = re.match(r"(\d{8})_(\d{6})__", path.name)
    if match:
        return datetime.strptime("".join(match.groups()), "%Y%m%d%H%M%S").replace(tzinfo=CN_TZ)
    return datetime.fromtimestamp(path.stat().st_mtime, tz=CN_TZ)


def first_heading(path: Path) -> str:
    if not path.exists():
        return ""
    match = HEADING_RE.search(path.read_text(encoding="utf-8"))
    return clean(match.group(1), "") if match else ""


def approved_topic_title(fields: dict[str, str]) -> str:
    approved_path = clean(fields.get("approved_topic_path", ""), "")
    if approved_path and approved_path != "n/a":
        path = Path(approved_path).expanduser()
        if path.exists():
            approved_fields = parse_fields(path)
            return clean(approved_fields.get("title", ""), "")
    return ""


def approved_topic_angle(fields: dict[str, str]) -> str:
    approved_path = clean(fields.get("approved_topic_path", ""), "")
    if approved_path and approved_path != "n/a":
        path = Path(approved_path).expanduser()
        if path.exists():
            approved_fields = parse_fields(path)
            return clean(approved_fields.get("approved_angle", ""), "")
    return ""


def record_from_queue_item(path: Path) -> TopicRecord | None:
    fields = parse_fields(path)
    queue_key = clean(fields.get("queue_key", ""), "")
    topic_key = clean(queue_key.rsplit("__", 1)[0], "")
    if not topic_key:
        topic_key = clean(fields.get("topic_id", path.stem), "")
    status = clean(fields.get("status", ""), "")
    if status not in BLOCKING_STATUSES:
        return None
    title = approved_topic_title(fields)
    if not title:
        content_path = clean(fields.get("content_path", ""), "")
        if content_path and content_path != "n/a":
            title = first_heading(Path(content_path).expanduser())
    angle = approved_topic_angle(fields)
    if not angle:
        angle = title
    happened_at = (
        parse_dt(fields.get("actual_publish_at", ""))
        or parse_dt(fields.get("planned_publish_at", ""))
        or path_timestamp(path)
    )
    return TopicRecord(
        queue_key=queue_key or path.stem,
        topic_key=topic_key,
        title=title,
        angle=angle,
        status=status,
        delivery_lane=clean(fields.get("delivery_lane", ""), ""),
        platform=clean(fields.get("platform", ""), ""),
        happened_at=happened_at,
        path=path,
    )


def normalize_topic_key(topic_key: str) -> str:
    value = clean(topic_key, "").lower()
    value = DATE_SUFFIX_RE.sub("_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def tokenize(text: str) -> set[str]:
    normalized = clean(text, "").lower()
    normalized = normalized.replace("源码泄露", " source leak ")
    normalized = normalized.replace("源代码泄露", " source leak ")
    normalized = normalized.replace("源码", " sourcecode ")
    normalized = normalized.replace("泄露", " leak ")
    normalized = normalized.replace("缓存", " cache ")
    normalized = normalized.replace("故障", " bug ")
    normalized = normalized.replace("问题", " issue ")
    normalized = DATE_SUFFIX_RE.sub(" ", normalized)
    tokens = {
        token
        for token in TOKEN_RE.findall(normalized)
        if token and not token.isdigit() and token not in GENERIC_TOKENS and len(token) >= 2
    }
    return tokens


def similarity(candidate_tokens: set[str], record_tokens: set[str]) -> tuple[float, tuple[str, ...]]:
    shared = tuple(sorted(candidate_tokens & record_tokens))
    if not candidate_tokens or not record_tokens:
        return 0.0, shared
    score = len(shared) / len(candidate_tokens | record_tokens)
    return score, shared


def conflict_reason(candidate_key: str, record: TopicRecord, shared: tuple[str, ...], score: float) -> str | None:
    normalized_candidate = normalize_topic_key(candidate_key)
    normalized_record = normalize_topic_key(record.topic_key)
    if normalized_candidate and normalized_candidate == normalized_record:
        return "same_topic_key"
    if len(shared) >= 3 and (
        score >= 0.50
        or set(tokenize(normalized_candidate)).issubset(set(shared))
        or set(tokenize(normalized_record)).issubset(set(shared))
    ):
        return "high_overlap_recent_topic"
    if len(shared) >= 4 and score >= 0.40:
        return "broad_overlap_recent_topic"
    return None


def is_recurring_roundup(topic_key: str, title: str, angle: str) -> bool:
    raw_text = " ".join([clean(topic_key, ""), clean(title, ""), clean(angle, "")])
    lowered = raw_text.lower()
    has_date = bool(DATE_SUFFIX_RE.search(topic_key) or ROUNDUP_DATE_RE.search(raw_text))
    has_series_hint = any(keyword in lowered for keyword in ROUNDUP_KEYWORDS_EN) or any(
        keyword in raw_text for keyword in ROUNDUP_KEYWORDS_CN
    )
    return has_date and has_series_hint


def recent_topic_records(
    lookback_hours: int = DEFAULT_LOOKBACK_HOURS,
    exclude_queue_keys: set[str] | None = None,
) -> list[TopicRecord]:
    exclude_queue_keys = exclude_queue_keys or set()
    cutoff = now_cn() - timedelta(hours=max(lookback_hours, 1))
    records: list[TopicRecord] = []
    for path in sorted(QUEUE_ROOT.glob("*__publish-queue-item.md")):
        record = record_from_queue_item(path)
        if not record:
            continue
        if record.queue_key in exclude_queue_keys:
            continue
        if record.happened_at < cutoff:
            continue
        records.append(record)
    return sorted(records, key=lambda item: item.happened_at, reverse=True)


def find_recent_conflicts(
    topic_key: str,
    title: str,
    approved_angle: str = "",
    lookback_hours: int = DEFAULT_LOOKBACK_HOURS,
    exclude_queue_keys: set[str] | None = None,
) -> list[TopicConflict]:
    candidate_tokens = tokenize(" ".join([normalize_topic_key(topic_key), title, approved_angle]))
    conflicts: list[TopicConflict] = []
    for record in recent_topic_records(lookback_hours=lookback_hours, exclude_queue_keys=exclude_queue_keys):
        if is_recurring_roundup(topic_key, title, approved_angle) and is_recurring_roundup(
            record.topic_key, record.title, record.angle
        ):
            if record.happened_at.date() != now_cn().date():
                continue
        score, shared = similarity(candidate_tokens, tokenize(record.fingerprint_text))
        reason = conflict_reason(topic_key, record, shared, score)
        if reason:
            conflicts.append(
                TopicConflict(
                    record=record,
                    reason=reason,
                    similarity=round(score, 3),
                    shared_tokens=shared,
                )
            )
    return conflicts


def render_report(
    topic_key: str,
    title: str,
    approved_angle: str,
    delivery_lane: str,
    lookback_hours: int,
    conflicts: list[TopicConflict],
) -> str:
    lines = [
        "# Recent Topic Guard",
        "",
        f"- `generated_at`: `{format_ts(now_cn())}`",
        f"- `candidate_topic_key`: `{clean(topic_key)}`",
        f"- `candidate_title`: `{clean(title)}`",
        f"- `candidate_angle`: `{clean(approved_angle, 'n/a')}`",
        f"- `delivery_lane`: `{clean(delivery_lane, 'n/a')}`",
        f"- `lookback_hours`: `{lookback_hours}`",
        f"- `recent_duplicate_status`: `{'fail' if conflicts else 'pass'}`",
        f"- `conflict_count`: `{len(conflicts)}`",
        "",
        "## Conflicts",
        "",
    ]
    if conflicts:
        for item in conflicts:
            lines.append(
                "- "
                + "｜".join(
                    [
                        f"`{item.record.topic_key}`",
                        f"reason=`{item.reason}`",
                        f"similarity=`{item.similarity}`",
                        f"shared=`{', '.join(item.shared_tokens) or 'n/a'}`",
                        f"status=`{item.record.status}`",
                        f"lane=`{item.record.delivery_lane or 'n/a'}`",
                        f"time=`{format_ts(item.record.happened_at)}`",
                        f"path=`{item.record.path}`",
                    ]
                )
            )
    else:
        lines.append("- `none`")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    conflicts = find_recent_conflicts(
        topic_key=args.topic_key,
        title=args.title,
        approved_angle=args.approved_angle,
        lookback_hours=args.lookback_hours,
        exclude_queue_keys={clean(item, "") for item in args.exclude_queue_key if clean(item, "")},
    )
    report_text = render_report(
        topic_key=args.topic_key,
        title=args.title,
        approved_angle=args.approved_angle,
        delivery_lane=args.delivery_lane,
        lookback_hours=args.lookback_hours,
        conflicts=conflicts,
    )
    if args.write:
        LOG_ROOT.mkdir(parents=True, exist_ok=True)
        log_path = LOG_ROOT / f"{now_cn().strftime('%Y%m%d_%H%M%S')}__recent-topic-guard.md"
        log_path.write_text(report_text, encoding="utf-8")
        print(log_path)
    print(report_text)


if __name__ == "__main__":
    main()

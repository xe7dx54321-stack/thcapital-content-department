#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
QUEUE_ROOT = ROOT / "06_publish_queue"
REVIEW_ROOT = ROOT / "07_performance_reviews"
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
CN_TZ = ZoneInfo("Asia/Shanghai")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record manual post-publish qualitative feedback and lead signals.")
    parser.add_argument("--queue-item", default="", help="Absolute queue item path")
    parser.add_argument("--queue-key", default="", help="queue_key under publish queue root")
    parser.add_argument("--queue-root", default=str(QUEUE_ROOT))
    parser.add_argument("--review-root", default=str(REVIEW_ROOT))
    parser.add_argument("--private-message-count", type=int, default=-1)
    parser.add_argument("--project-lead-count", type=int, default=-1)
    parser.add_argument("--business-lead-count", type=int, default=-1)
    parser.add_argument("--notable-comment", action="append", default=[])
    parser.add_argument("--manual-tag", action="append", default=[])
    parser.add_argument("--founder-summary", default="")
    parser.add_argument("--title-feedback", default="")
    parser.add_argument("--packaging-feedback", default="")
    parser.add_argument("--next-topic-hint", default="")
    parser.add_argument("--note", default="")
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return value if value else fallback


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def parse_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def resolve_queue_item_path(queue_root: Path, queue_item: str, queue_key: str) -> Path:
    if clean(queue_item, ""):
        path = Path(queue_item).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"queue item not found: {path}")
        return path
    if not clean(queue_key, ""):
        raise SystemExit("provide either --queue-item or --queue-key")
    matches = sorted(queue_root.glob(f"*__{queue_key}__publish-queue-item.md"))
    if not matches:
        raise SystemExit(f"queue_key not found under {queue_root}: {queue_key}")
    if len(matches) > 1:
        raise SystemExit(f"queue_key matched multiple items, please use --queue-item: {queue_key}")
    return matches[0]


def feedback_path(review_root: Path, queue_key: str) -> Path:
    return review_root / "_manual_feedback" / f"{queue_key}.json"


def load_existing(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def merge_int(existing: dict, key: str, value: int) -> int:
    if value >= 0:
        return value
    return int(existing.get(key) or 0)


def merge_list(existing: dict, key: str, values: list[str]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for raw in [*(existing.get(key) or []), *values]:
        item = clean(str(raw), "")
        if not item or item in seen:
            continue
        merged.append(item)
        seen.add(item)
    return merged


def merge_text(existing: dict, key: str, value: str) -> str:
    new_value = clean(value, "")
    if new_value:
        return new_value
    return clean(str(existing.get(key, "n/a")), "n/a")


def main() -> None:
    args = parse_args()
    queue_root = Path(args.queue_root).expanduser().resolve()
    review_root = Path(args.review_root).expanduser().resolve()
    queue_item_path = resolve_queue_item_path(queue_root, args.queue_item, args.queue_key)
    fields = parse_fields(queue_item_path)
    queue_key = clean(fields.get("queue_key", queue_item_path.stem))
    path = feedback_path(review_root, queue_key)
    existing = load_existing(path)
    payload = {
        "queue_key": queue_key,
        "queue_id": clean(fields.get("queue_id", "n/a")),
        "topic_id": clean(fields.get("topic_id", "n/a")),
        "platform": clean(fields.get("platform", "n/a")),
        "updated_at": now_cn().isoformat(),
        "private_message_count": merge_int(existing, "private_message_count", args.private_message_count),
        "project_lead_count": merge_int(existing, "project_lead_count", args.project_lead_count),
        "business_lead_count": merge_int(existing, "business_lead_count", args.business_lead_count),
        "notable_comments": merge_list(existing, "notable_comments", args.notable_comment),
        "manual_tags": merge_list(existing, "manual_tags", args.manual_tag),
        "founder_summary": merge_text(existing, "founder_summary", args.founder_summary),
        "title_feedback": merge_text(existing, "title_feedback", args.title_feedback),
        "packaging_feedback": merge_text(existing, "packaging_feedback", args.packaging_feedback),
        "next_topic_hint": merge_text(existing, "next_topic_hint", args.next_topic_hint),
        "note": merge_text(existing, "note", args.note),
    }
    if args.write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path)
    if not args.write:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

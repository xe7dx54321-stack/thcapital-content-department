#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
DEFAULT_REVIEW_ROOT = ROOT / "07_performance_reviews"
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")


@dataclass
class QueueItem:
    path: Path
    queue_id: str
    topic_id: str
    approved_topic_path: str
    platform: str
    publish_owner: str
    actual_publish_at: str
    publish_url: str
    manual_gate: str
    human_action_required: str
    frontstage_summary: str
    status: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build performance review for TH Capital market content system")
    parser.add_argument("--queue-item", action="append", required=True, help="Queue item path, repeatable")
    parser.add_argument("--review-window", default="24h")
    parser.add_argument("--status", choices=["scheduled", "collecting", "ready", "closed"], required=True)
    parser.add_argument("--review-root", default=str(DEFAULT_REVIEW_ROOT))
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value).strip().strip("`")
    return value if value else fallback


def resolve_doc_path(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path
    return ROOT / raw_path


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def parse_queue_item(path: Path) -> QueueItem:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return QueueItem(
        path=path,
        queue_id=clean(fields.get("queue_id", path.stem)),
        topic_id=clean(fields.get("topic_id", "n/a")),
        approved_topic_path=clean(fields.get("approved_topic_path", "n/a")),
        platform=clean(fields.get("platform", "n/a")),
        publish_owner=clean(fields.get("publish_owner", "n/a")),
        actual_publish_at=clean(fields.get("actual_publish_at", "n/a")),
        publish_url=clean(fields.get("publish_url", "n/a")),
        manual_gate=clean(fields.get("manual_gate", "n/a")),
        human_action_required=clean(fields.get("human_action_required", "n/a")),
        frontstage_summary=clean(fields.get("frontstage_summary", "n/a")),
        status=clean(fields.get("status", "n/a")),
    )


def require_real_publish(items: list[QueueItem], target_status: str) -> None:
    if target_status not in {"ready", "closed"}:
        return
    published = [item for item in items if item.status == "published" and item.publish_url != "n/a"]
    if not published:
        raise SystemExit("Review status ready/closed requires at least one published queue item with publish_url")


def review_text(items: list[QueueItem], review_window: str, status: str) -> str:
    topic_id = items[0].topic_id
    topic_key = topic_id.split("__")[-1] if "__" in topic_id else topic_id
    review_id = f"review__{now_cn().strftime('%Y%m%d_%H%M%S')}__{topic_key}__{review_window}"
    queue_ids = ", ".join(item.queue_id for item in items)
    lines = [
        "# Performance Review",
        "",
        f"- `review_id`: `{review_id}`",
        f"- `review_key`: `{topic_key}__{review_window}`",
        f"- `topic_id`: `{topic_id}`",
        f"- `queue_ids`: `{queue_ids}`",
        f"- `review_window`: `{review_window}`",
        f"- `status`: `{status}`",
        "",
        "## Publish Evidence",
        "",
    ]
    for item in items:
        lines.append(
            f"- `{item.platform}`｜owner=`{item.publish_owner}`｜published_at=`{item.actual_publish_at}`｜url=`{item.publish_url}`"
        )
    lines.extend(
        [
            "",
            "## Platform Metrics",
            "",
        ]
    )
    for item in items:
        metric_hint = item.publish_url if item.publish_url != "n/a" else "n/a"
        lines.append(f"- `{item.platform}`: `{metric_hint}`")
    lines.extend(
        [
            "",
            "## Current Gaps",
            "",
            "- `metrics_backfill_gap`: `n/a`",
            "- `distribution_context_gap`: `n/a`",
            "- `comment_or_feedback_gap`: `n/a`",
            "",
            "## Frontstage Brief",
            "",
            *[f"- `{item.platform}`: {item.frontstage_summary}" for item in items],
            "",
            "## Learnings",
            "",
            "- `adoption_result`: `n/a`",
            "- `title_learnings`: `n/a`",
            "- `platform_fit_learnings`: `n/a`",
            "- `source_learnings`: `n/a`",
            "- `next_actions`: `n/a`",
            "",
            "## Workflow Feedback",
            "",
            "- `workflow_gap`: `n/a`",
            "- `skill_update_hint`: `n/a`",
            "- `ops_owner_next_action`: `n/a`",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def update_approved_topic_status(text: str, review_status: str) -> str:
    if review_status != "closed":
        return text
    pattern = re.compile(r"^(- `status`: `)([^`]+)(`)\s*$", re.M)
    return pattern.sub(lambda m: f"{m.group(1)}reviewed{m.group(3)}", text, count=1)


def main() -> None:
    args = parse_args()
    items = [parse_queue_item(Path(path)) for path in args.queue_item]
    if not items:
        raise SystemExit("No queue items provided")
    topic_ids = {item.topic_id for item in items}
    if len(topic_ids) != 1:
        raise SystemExit("All queue items in one review must belong to the same topic_id")

    require_real_publish(items, args.status)

    topic_key = items[0].topic_id.split("__")[-1] if "__" in items[0].topic_id else items[0].topic_id
    review_root = Path(args.review_root)
    review_path = review_root / f"{now_cn().strftime('%Y%m%d')}__{topic_key}__{args.review_window}-review.md"
    content = review_text(items, args.review_window, args.status)

    if args.write:
        review_root.mkdir(parents=True, exist_ok=True)
        review_path.write_text(content, encoding="utf-8")
        approved_paths = {item.approved_topic_path for item in items if item.approved_topic_path != "n/a"}
        if args.status == "closed":
            for approved_path in approved_paths:
                path = resolve_doc_path(approved_path)
                if path.exists():
                    updated = update_approved_topic_status(path.read_text(encoding="utf-8"), args.status)
                    path.write_text(updated, encoding="utf-8")
        print(review_path)
        return

    print(review_path)
    print(content)


if __name__ == "__main__":
    main()

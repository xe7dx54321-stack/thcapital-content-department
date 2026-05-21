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
OUTBOX_ROOT = ROOT / "07_wechat_bridge_outbox"
CN_TZ = ZoneInfo("Asia/Shanghai")
FIELD_RE_TEMPLATE = r"^(- `{field}`: `)([^`]*)((?:`)\s*)$"
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record a founder-confirmed manual publish into the publish queue.")
    parser.add_argument("--queue-item", default="", help="Absolute queue item path")
    parser.add_argument("--queue-key", default="", help="queue_key under publish queue root")
    parser.add_argument("--queue-root", default=str(QUEUE_ROOT))
    parser.add_argument("--publish-url", default="", help="Optional final publish URL")
    parser.add_argument("--actual-publish-at", default="", help="Optional publish timestamp in local CST text")
    parser.add_argument("--confirmed-by", default="founder", help="Who confirmed the manual publish")
    parser.add_argument("--note", default="", help="Optional extra note")
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return value if value else fallback


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def parse_publish_dt(raw: str) -> datetime | None:
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


def update_field(text: str, field: str, value: str) -> str:
    pattern = re.compile(FIELD_RE_TEMPLATE.format(field=re.escape(field)), re.M)
    if pattern.search(text):
        return pattern.sub(lambda match: f"{match.group(1)}{value}{match.group(3)}", text, count=1)
    return text


def parse_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def merge_notes(existing: str, extras: dict[str, str]) -> str:
    chunks = [item.strip() for item in existing.split("|") if item.strip() and item.strip() != "n/a"]
    filtered = [chunk for chunk in chunks if not any(chunk.startswith(f"{key}=") for key in extras)]
    for key, value in extras.items():
        filtered.append(f"{key}={value}")
    return " | ".join(filtered) if filtered else "n/a"


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


def refresh_card_paths(text: str, pack_dir: Path) -> str:
    mapping = {
        "wechat_path": "wechat.md",
        "xiaohongshu_path": "xiaohongshu.md",
        "zhihu_path": "zhihu.md",
        "x_path": "x.md",
        "bilibili_path": "bilibili.md",
        "toutiao_path": "toutiao.md",
        "baijiahao_path": "baijiahao.md",
        "title_options_path": "title-options.md",
        "summary_options_path": "summary-options.md",
        "opening_hook_options_path": "opening-hook-options.md",
        "cta_mode_path": "cta-mode.md",
        "packaging_bundle_path": "packaging-bundle.md",
        "context_bridge_path": "context-bridge-notes.md",
        "audience_notes_path": "audience-notes.md",
        "render_plan_path": "platform-render-plan.md",
        "citation_block_path": "citation-block.md",
        "visual_notes_path": "visual-notes.md",
        "inline_visual_plan_path": "inline-visual-plan.md",
        "revision_notes_path": "revision-notes.md",
    }
    updated = text
    for field_name, filename in mapping.items():
        candidate = pack_dir / filename
        updated = update_field(updated, field_name, str(candidate) if candidate.exists() else "n/a")
    return updated


def update_approved_topic_status(text: str) -> str:
    updated = update_field(text, "status", "published")
    updated = update_field(updated, "next_step", "published -> performance_review")
    return updated


def update_draft_pack_card(text: str) -> str:
    updated = update_field(text, "status", "published")
    updated = update_field(updated, "next_step", "published -> performance_review")
    updated = update_field(updated, "publish_gate", "completed")
    updated = update_field(updated, "updated_at", format_ts(now_cn()))
    return updated


def rebuild_queue_board(queue_root: Path) -> Path:
    rows = [parse_fields(path) for path in sorted(queue_root.glob("*__publish-queue-item.md"))]
    status_counts: dict[str, int] = {}
    lane_counts: dict[str, int] = {}
    for row in rows:
        status = row.get("status", "n/a")
        lane = row.get("delivery_lane", "n/a")
        status_counts[status] = status_counts.get(status, 0) + 1
        lane_counts[lane] = lane_counts.get(lane, 0) + 1
    lines = [
        "# Publish Queue Board",
        "",
        f"- `generated_at`: `{format_ts(now_cn())}`",
        f"- `total_items`: `{len(rows)}`",
        f"- `queued_items`: `{status_counts.get('queued', 0)}`",
        f"- `waiting_human_publish_items`: `{status_counts.get('waiting_human_publish', 0)}`",
        f"- `published_items`: `{status_counts.get('published', 0)}`",
        f"- `deferred_items`: `{status_counts.get('deferred', 0)}`",
        f"- `cancelled_items`: `{status_counts.get('cancelled', 0)}`",
        f"- `morning_flash_items`: `{lane_counts.get('morning_flash', 0)}`",
        f"- `day_mainline_items`: `{lane_counts.get('day_mainline', 0)}`",
        "",
        "## Queue Table",
        "",
        "| queue_id | topic_key | lane | publish_mode | platform | status | manual_gate | publish_owner | planned_publish_at | actual_publish_at | publish_url |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        queue_key = row.get("queue_key", "n/a")
        topic_key = queue_key.rsplit("__", 1)[0] if "__" in queue_key else row.get("topic_id", "n/a")
        lines.append(
            f"| `{row.get('queue_id', 'n/a')}` | `{topic_key}` | `{row.get('delivery_lane', 'n/a')}` | `{row.get('publish_mode', 'n/a')}` | `{row.get('platform', 'n/a')}` | `{row.get('status', 'n/a')}` | `{row.get('manual_gate', 'n/a')}` | `{row.get('publish_owner', 'n/a')}` | `{row.get('planned_publish_at', 'n/a')}` | `{row.get('actual_publish_at', 'n/a')}` | `{row.get('publish_url', 'n/a')}` |"
        )
    board_path = queue_root / f"{now_cn().strftime('%Y%m%d')}__publish-queue-board.md"
    board_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return board_path


def queue_topic_key(queue_key: str) -> str:
    return queue_key.rsplit("__", 1)[0] if "__" in queue_key else queue_key


def bridge_publish_confirmation_path(queue_key: str) -> Path:
    request_id = f"wechat_bridge__{queue_topic_key(queue_key)}"
    return OUTBOX_ROOT / "requests" / request_id / "publish_confirmation.json"


def main() -> None:
    args = parse_args()
    queue_root = Path(args.queue_root).expanduser().resolve()
    queue_item_path = resolve_queue_item_path(queue_root, args.queue_item, args.queue_key)
    fields = parse_fields(queue_item_path)
    queue_key = clean(fields.get("queue_key", queue_item_path.stem))
    original = queue_item_path.read_text(encoding="utf-8")
    actual_publish_at = clean(args.actual_publish_at, "")
    publish_dt = parse_publish_dt(actual_publish_at) if actual_publish_at else now_cn()
    if not actual_publish_at:
        actual_publish_at = format_ts(publish_dt)
    publish_url = clean(args.publish_url, clean(fields.get("publish_url", "n/a")))
    publish_url_backfill = "done" if publish_url != "n/a" else "required"
    updated = original
    updated = update_field(updated, "status", "published")
    updated = update_field(updated, "manual_gate", "human_publish_completed")
    updated = update_field(updated, "actual_publish_at", actual_publish_at)
    updated = update_field(updated, "publish_url", publish_url)
    if publish_url_backfill == "required":
        human_action = "人工发布已确认；下一步补 publish_url，随后进入 24h / 72h review"
        frontstage = "稿件已人工发布，等待 URL 回填后进入正式复盘。"
    else:
        human_action = "人工发布已确认，下一步自动进入 24h / 72h review"
        frontstage = "稿件已人工发布，结果回流与复盘链路已启动。"
    updated = update_field(updated, "human_action_required", human_action)
    updated = update_field(updated, "frontstage_summary", frontstage)
    notes = merge_notes(
        clean(fields.get("notes", "n/a")),
        {
            "human_publish_confirmed_by_founder": "yes" if clean(args.confirmed_by, "").lower() in {"founder", "老板"} else "no",
            "human_publish_confirmed_by": clean(args.confirmed_by),
            "human_publish_confirmed_recorded_at": now_cn().isoformat(),
            "human_publish_url_backfill": publish_url_backfill,
            "human_publish_extra_note": clean(args.note) if clean(args.note, "") else "n/a",
        },
    )
    updated = update_field(updated, "notes", notes)

    if args.write and updated != original:
        queue_item_path.write_text(updated, encoding="utf-8")
        refreshed_fields = parse_fields(queue_item_path)
        confirmation_path = bridge_publish_confirmation_path(queue_key)
        confirmation_path.parent.mkdir(parents=True, exist_ok=True)
        confirmation_path.write_text(
            json.dumps(
                {
                    "status": "published",
                    "queue_key": queue_key,
                    "queue_id": clean(fields.get("queue_id", "n/a")),
                    "topic_id": clean(fields.get("topic_id", "n/a")),
                    "confirmed_by": clean(args.confirmed_by),
                    "confirmed_at": now_cn().isoformat(),
                    "published_at": actual_publish_at,
                    "published_at_iso": publish_dt.isoformat(),
                    "publish_url": publish_url,
                    "publish_time_source": "market_human_publish_record",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        approved_topic_path = Path(clean(refreshed_fields.get("approved_topic_path", "n/a")))
        if approved_topic_path.exists():
            approved_topic_path.write_text(
                update_approved_topic_status(approved_topic_path.read_text(encoding="utf-8")),
                encoding="utf-8",
            )
        content_path = Path(clean(refreshed_fields.get("content_path", "n/a")))
        card_path = content_path.parent / "00_draft-pack-card.md"
        if card_path.exists():
            refreshed = refresh_card_paths(card_path.read_text(encoding="utf-8"), content_path.parent)
            card_path.write_text(update_draft_pack_card(refreshed), encoding="utf-8")
        board_path = rebuild_queue_board(queue_root)
        print(f"QUEUE_UPDATED {queue_item_path}")
        print(f"PUBLISH_CONFIRMATION_SYNCED {confirmation_path}")
        print(f"QUEUE_BOARD_REBUILT {board_path}")
    print(queue_item_path)


if __name__ == "__main__":
    main()

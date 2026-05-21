#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from market_morning_flash_gate_recovery import recover_morning_flash_gate

DEFAULT_OUTBOX_DIR = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统/07_wechat_bridge_outbox")
DEFAULT_QUEUE_ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue")
FIELD_RE_TEMPLATE = r"^(- `{field}`: `)([^`]*)((?:`)\s*)$"
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
CN_TZ = ZoneInfo("Asia/Shanghai")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reconcile Windows WeChat bridge results back into publish queue items.")
    parser.add_argument("--outbox-dir", default=str(DEFAULT_OUTBOX_DIR), help="Synced WeChat bridge outbox directory")
    parser.add_argument("--queue-root", default=str(DEFAULT_QUEUE_ROOT), help="Publish queue root directory")
    parser.add_argument("--request-id", action="append", default=[], help="Only reconcile the specified request_id(s)")
    parser.add_argument("--write", action="store_true", help="Write queue item updates")
    return parser.parse_args()


def update_field(text: str, field: str, value: str) -> str:
    pattern = re.compile(FIELD_RE_TEMPLATE.format(field=re.escape(field)), re.M)
    if pattern.search(text):
        return pattern.sub(lambda match: f"{match.group(1)}{value}{match.group(3)}", text, count=1)
    return text


def merge_notes(existing: str, extras: dict[str, str]) -> str:
    chunks = [item.strip() for item in existing.split("|") if item.strip() and item.strip() != "n/a"]
    filtered = [chunk for chunk in chunks if not any(chunk.startswith(f"{key}=") for key in extras)]
    for key, value in extras.items():
        filtered.append(f"{key}={value}")
    return " | ".join(filtered) if filtered else "n/a"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def request_dirs(outbox_dir: Path) -> list[Path]:
    requests_dir = outbox_dir / "requests"
    if not requests_dir.exists():
        return []
    return sorted([path for path in requests_dir.iterdir() if path.is_dir()])


def selected_request_dirs(outbox_dir: Path, request_ids: list[str]) -> list[Path]:
    if not request_ids:
        return request_dirs(outbox_dir)
    requests_dir = outbox_dir / "requests"
    return [requests_dir / request_id for request_id in request_ids if (requests_dir / request_id).is_dir()]


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value).strip().strip("`")
    return value if value else fallback


def parse_item_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def rebuild_board(queue_root: Path, board_path: Path) -> None:
    rows: list[dict[str, str]] = []
    for path in sorted(queue_root.glob("*__publish-queue-item.md")):
        rows.append(parse_item_fields(path))
    status_counts: dict[str, int] = {}
    lane_counts: dict[str, int] = {}
    for row in rows:
        status = row.get("status", "n/a")
        status_counts[status] = status_counts.get(status, 0) + 1
        lane = row.get("delivery_lane", "n/a")
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
    lines.extend(["", "## Human Action Queue", ""])
    action_rows = [row for row in rows if row.get("status") in {"queued", "waiting_human_publish", "deferred"}]
    if action_rows:
        for row in action_rows:
            lines.append(
                f"- `{row.get('queue_key', 'n/a')}`｜{row.get('human_action_required', 'n/a')}｜前台摘要：{row.get('frontstage_summary', 'n/a')}"
            )
    else:
        lines.append("- `none`")

    lines.extend(["", "## Published / Review Follow-up", ""])
    published_rows = [row for row in rows if row.get("status") == "published"]
    if published_rows:
        for row in published_rows:
            lines.append(
                f"- `{row.get('queue_key', 'n/a')}`｜URL：`{row.get('publish_url', 'n/a')}`｜下一步：{row.get('human_action_required', 'n/a')}"
            )
    else:
        lines.append("- `none`")
    board_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def reconcile_request(request_dir: Path, write: bool) -> tuple[str, bool]:
    request_path = request_dir / "request.json"
    result_path = request_dir / "result.json"
    if not request_path.exists() and not result_path.exists():
        return f"SKIP {request_dir.name} missing request and result", False
    if not request_path.exists():
        return f"SKIP {request_dir.name} missing request.json", False
    if not result_path.exists():
        return f"SKIP {request_dir.name} result pending (request.json present, result.json missing)", False
    request = load_json(request_path)
    result = load_json(result_path)
    queue_item_path = Path(((request.get("paths") or {}).get("queue_item_path") or "")).expanduser()
    if not queue_item_path.exists():
        return f"SKIP {request_dir.name} queue item missing", False
    original = queue_item_path.read_text(encoding="utf-8")
    updated = original
    if result.get("status") == "success":
        media_id = str(result.get("media_id", "")).strip() or "n/a"
        inline_image_count = clean(str(result.get("inline_image_count", "0")), "0")
        rendered_html_img_count = clean(str(result.get("rendered_html_img_count", "0")), "0")
        queue_fields = parse_item_fields(queue_item_path)
        publish_mode = clean(queue_fields.get("publish_mode", "draft_only"))
        updated = update_field(updated, "publish_url", f"wechat-draft://{media_id}")
        if publish_mode == "auto_api":
            updated = update_field(
                updated,
                "human_action_required",
                "等待晨间自动发布闸门：technical_preflight=pass、reviewer_checklist=pass、leader_checklist=pass 后调用 freepublish/submit",
            )
            updated = update_field(updated, "frontstage_summary", "wechat 草稿已自动入箱，等待晨间自动发布闸门。")
        else:
            updated = update_field(updated, "human_action_required", f"去公众号草稿箱审核并发送（media_id={media_id}）")
            updated = update_field(updated, "frontstage_summary", "wechat 草稿已自动入箱，待人工审核发送。")
        notes_value = merge_notes(
            re.search(FIELD_RE_TEMPLATE.format(field="notes"), updated, re.M).group(2) if re.search(FIELD_RE_TEMPLATE.format(field="notes"), updated, re.M) else "n/a",
            {
                "wechat_bridge_status": "success",
                "wechat_draft_media_id": media_id,
                "wechat_draft_synced_at": str(result.get("completed_at", "")),
                "wechat_inline_image_count": inline_image_count,
                "wechat_rendered_html_img_count": rendered_html_img_count,
                "wechat_bridge_consumer_version": clean(str(result.get("consumer_version", "")), "n/a"),
            },
        )
        updated = update_field(updated, "notes", notes_value)
    elif result.get("status") in {"skipped_expired", "skipped_queue_closed"}:
        skip_reason = clean(str(result.get("reason", "")), "unknown")
        notes_value = merge_notes(
            re.search(FIELD_RE_TEMPLATE.format(field="notes"), updated, re.M).group(2) if re.search(FIELD_RE_TEMPLATE.format(field="notes"), updated, re.M) else "n/a",
            {
                "wechat_bridge_status": "skipped",
                "wechat_bridge_skip_reason": skip_reason,
            },
        )
        updated = update_field(updated, "notes", notes_value)
        updated = update_field(
            updated,
            "frontstage_summary",
            f"wechat bridge 已跳过历史请求（{skip_reason}），不会再把过期稿件回补进草稿箱。",
        )
        updated = update_field(
            updated,
            "human_action_required",
            "如该稿件仍需交付，请先重建当前发布队列，再生成新的 bridge request。",
        )
    else:
        error_message = str(result.get("error_message", "")).strip().replace("`", "'") or "unknown"
        notes_value = merge_notes(
            re.search(FIELD_RE_TEMPLATE.format(field="notes"), updated, re.M).group(2) if re.search(FIELD_RE_TEMPLATE.format(field="notes"), updated, re.M) else "n/a",
            {
                "wechat_bridge_status": "failed",
                "wechat_bridge_error": error_message,
            },
        )
        updated = update_field(updated, "notes", notes_value)
    changed = updated != original
    if write and changed:
        queue_item_path.write_text(updated, encoding="utf-8")
    recovery_messages: list[str] = []
    recovery_changed = False
    if result.get("status") == "success":
        recovery_changed, recovery_messages = recover_morning_flash_gate(queue_item_path, write=write)
        changed = changed or recovery_changed
    prefix = "RECONCILED" if changed else "UNCHANGED"
    suffix = f" | {' ; '.join(recovery_messages)}" if recovery_messages else ""
    return f"{prefix} {request_dir.name} -> {queue_item_path}{suffix}", changed


def main() -> None:
    args = parse_args()
    outbox_dir = Path(args.outbox_dir).expanduser().resolve()
    queue_root = Path(args.queue_root).expanduser().resolve()
    changed_any = False
    for request_dir in selected_request_dirs(outbox_dir, args.request_id):
        message, changed = reconcile_request(request_dir, args.write)
        print(message)
        changed_any = changed_any or changed
    if args.write and changed_any:
        board_path = queue_root / f"{now_cn().strftime('%Y%m%d')}__publish-queue-board.md"
        rebuild_board(queue_root, board_path)
        print(f"BOARD_REBUILT {board_path}")


if __name__ == "__main__":
    main()

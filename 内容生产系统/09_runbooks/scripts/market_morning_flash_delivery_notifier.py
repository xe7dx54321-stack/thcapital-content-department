#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import market_frontstage_board_builder as board_builder


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
FRONTSTAGE_DIR = ROOT / "11_frontstage"
NOTIFICATION_STATE_PATH = FRONTSTAGE_DIR / "_notification_state" / "morning_flash_delivery_notifier_state.json"
QUEUE_DIR = ROOT / "06_publish_queue"
LOG_DIR = ROOT / "10_logs"
FEISHU_DOC_DELIVERY_SCRIPT = ROOT / "09_runbooks" / "scripts" / "market_feishu_doc_delivery.py"
FIELD_RE_TEMPLATE = r"^(- `{field}`: `)([^`]*)((?:`)\s*)$"
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
CN_TZ = ZoneInfo("Asia/Shanghai")
DEFAULT_ACCOUNT = "market"
DEFAULT_TARGET = f"chat:{board_builder.FRONTSTAGE_GROUP_ID}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Notify the founder once the morning_flash article has a synced Feishu doc.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical date in YYYY-MM-DD.")
    parser.add_argument("--account", default=DEFAULT_ACCOUNT, help="OpenClaw Feishu account id.")
    parser.add_argument("--target", default=DEFAULT_TARGET, help="OpenClaw Feishu target.")
    parser.add_argument("--state-path", default=str(NOTIFICATION_STATE_PATH), help="Notification dedupe state path.")
    parser.add_argument("--dry-run", action="store_true", help="Build and print the message, but skip real delivery.")
    return parser.parse_args()


def clean(value: object, fallback: str = "") -> str:
    normalized = re.sub(r"\s+", " ", str(value or "")).strip().strip("`")
    return normalized or fallback


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def parse_queue_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    if not path.exists():
        return fields
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def note_value(notes: str, key: str) -> str:
    for chunk in clean(notes, "").split("|"):
        stripped = chunk.strip()
        if stripped.startswith(f"{key}="):
            return clean(stripped.split("=", 1)[1], "")
    return ""


def queue_item_sort_key(path: Path) -> tuple[str, int, str]:
    fields = parse_queue_fields(path)
    queue_id = clean(fields.get("queue_id", ""), "")
    for candidate in (queue_id, path.name):
        match = re.search(r"(\d{8}_\d{6})", candidate)
        if match:
            return (match.group(1), 1, path.name)
    try:
        return (f"{path.stat().st_mtime_ns:020d}", 0, path.name)
    except FileNotFoundError:
        return ("", 0, path.name)


def latest_same_day_morning_queue_item(date_text: str) -> Path | None:
    candidates: list[Path] = []
    for path in sorted(QUEUE_DIR.glob("*__wechat__publish-queue-item.md"), key=queue_item_sort_key):
        fields = parse_queue_fields(path)
        if clean(fields.get("delivery_lane", ""), "") != "morning_flash":
            continue
        planned = clean(fields.get("planned_publish_at", ""), "")
        deadline = clean(fields.get("delivery_deadline", ""), "")
        if planned.startswith(date_text) or deadline.startswith(date_text):
            candidates.append(path)
    return candidates[-1] if candidates else None


def pack_dir_from_queue_item(queue_item_path: Path | None) -> Path | None:
    if queue_item_path is None or not queue_item_path.exists():
        return None
    fields = parse_queue_fields(queue_item_path)
    pack_dir = clean(fields.get("draft_pack_dir", ""), "")
    if pack_dir and pack_dir != "n/a":
        resolved = Path(pack_dir).expanduser().resolve()
        if resolved.exists():
            return resolved
    content_path = clean(fields.get("content_path", ""), "")
    if content_path and content_path != "n/a":
        resolved = Path(content_path).expanduser().resolve().parent
        if resolved.exists():
            return resolved
    return None


def extract_title(markdown: str, fallback: str) -> str:
    for raw in markdown.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", raw.strip())
        if match:
            heading = clean(match.group(1), fallback)
            return heading.replace("微信稿｜", "").replace("微信稿|", "").strip() or fallback
    return fallback


def ensure_feishu_doc(pack_dir: Path) -> dict:
    sidecar_path = pack_dir / "feishu-doc-delivery.json"
    sidecar = load_json(sidecar_path)
    if clean(sidecar.get("status"), "") == "success" and clean(sidecar.get("url"), ""):
        return sidecar
    if not FEISHU_DOC_DELIVERY_SCRIPT.exists():
        return sidecar
    command = [
        "python3",
        str(FEISHU_DOC_DELIVERY_SCRIPT),
        "--draft-pack-dir",
        str(pack_dir),
        "--write",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return {
            "status": "blocked",
            "error": clean(completed.stderr or completed.stdout, "feishu_doc_delivery_failed"),
        }
    return load_json(sidecar_path)


def send_group_message(account: str, target: str, message: str, dry_run: bool) -> dict:
    command = [
        "openclaw",
        "message",
        "send",
        "--channel",
        "feishu",
        "--account",
        account,
        "--target",
        target,
        "--message",
        message,
        "--json",
    ]
    if dry_run:
        command.append("--dry-run")
    result = subprocess.run(command, capture_output=True, text=True, timeout=60, check=False)
    if result.returncode != 0:
        raise RuntimeError(clean(result.stderr or result.stdout, "unknown delivery error"))
    raw = clean(result.stdout or result.stderr, "")
    if not raw:
        return {"ok": True, "raw": ""}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"ok": True, "raw": raw}


def build_message(date_text: str, title: str, doc_url: str, publish_state: str, publish_url: str, queue_item_path: Path) -> str:
    publish_line = f"- 微信状态：{publish_state}"
    if publish_url and publish_url != "n/a":
        publish_line += f"\n- 文章链接：{publish_url}"
    return (
        f"【同行资本｜晨间线成品交付｜{date_text}】\n"
        f"- 题目：{title}\n"
        f"{publish_line}\n"
        f"- 飞书云文档：{doc_url}\n"
        f"- 发布队列：`{queue_item_path}`\n"
    )


def write_log(path: Path, payload: dict[str, object]) -> None:
    lines = [
        "# Market Morning Flash Delivery Notifier",
        "",
        f"- `timestamp`: `{payload.get('timestamp', '')}`",
        f"- `status`: `{payload.get('status', '')}`",
        f"- `date`: `{payload.get('date', '')}`",
        f"- `title`: `{payload.get('title', '')}`",
        f"- `queue_item_path`: `{payload.get('queue_item_path', '')}`",
        f"- `draft_pack_dir`: `{payload.get('draft_pack_dir', '')}`",
        f"- `feishu_doc_url`: `{payload.get('feishu_doc_url', '')}`",
        f"- `publish_state`: `{payload.get('publish_state', '')}`",
        f"- `publish_url`: `{payload.get('publish_url', '')}`",
        f"- `dry_run`: `{'true' if payload.get('dry_run') else 'false'}`",
    ]
    if payload.get("reason"):
        lines.append(f"- `reason`: `{payload.get('reason')}`")
    if payload.get("message"):
        lines.extend(["", "## Message", "", "```text", str(payload["message"]).rstrip(), "```"])
    if payload.get("delivery_result") is not None:
        lines.extend(["", "## Delivery Result", "", "```json", json.dumps(payload["delivery_result"], ensure_ascii=False, indent=2), "```"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    queue_item_path = latest_same_day_morning_queue_item(args.date)
    if queue_item_path is None:
        print("NO_MORNING_QUEUE_ITEM")
        return
    queue_fields = parse_queue_fields(queue_item_path)
    pack_dir = pack_dir_from_queue_item(queue_item_path)
    if pack_dir is None:
        print("WAITING draft_pack_missing")
        return

    title = extract_title(read_text(pack_dir / "wechat.md"), pack_dir.name.replace("-", " "))
    feishu_meta = ensure_feishu_doc(pack_dir)
    notes = clean(queue_fields.get("notes", ""), "")
    doc_url = clean(feishu_meta.get("url"), note_value(notes, "feishu_doc_url"))
    if not doc_url:
        print("WAITING feishu_doc_missing")
        return

    publish_url = clean(queue_fields.get("publish_url", ""), "")
    queue_status = clean(queue_fields.get("status", ""), "")
    bridge_success = note_value(notes, "wechat_bridge_status") == "success"
    if queue_status == "published" and publish_url and not publish_url.startswith("wechat-draft://"):
        publish_state = "已自动发布"
    elif bridge_success or publish_url.startswith("wechat-draft://"):
        publish_state = "已入微信草稿箱 / 待自动发布"
    else:
        publish_state = "飞书云文档已就位 / 微信自动发布待恢复"

    notify_state_path = Path(args.state_path).expanduser().resolve()
    notify_state = load_json(notify_state_path)
    deliveries = notify_state.setdefault("deliveries", {})
    event_key = f"{args.date}::{pack_dir.name}"
    if deliveries.get(event_key, {}).get("notified_at"):
        print("SKIP already_notified")
        return

    message = build_message(args.date, title, doc_url, publish_state, publish_url if queue_status == "published" else "", queue_item_path)
    delivery_result = send_group_message(args.account, args.target, message, dry_run=args.dry_run)
    log_path = LOG_DIR / f"{now_cn().strftime('%Y%m%d_%H%M%S')}__{pack_dir.name}__morning-flash-delivery-notifier.md"
    write_log(
        log_path,
        {
            "timestamp": format_ts(now_cn()),
            "status": "dry_run_sent" if args.dry_run else "sent",
            "date": args.date,
            "title": title,
            "queue_item_path": str(queue_item_path),
            "draft_pack_dir": str(pack_dir),
            "feishu_doc_url": doc_url,
            "publish_state": publish_state,
            "publish_url": publish_url,
            "dry_run": args.dry_run,
            "message": message,
            "delivery_result": delivery_result,
        },
    )
    if not args.dry_run:
        deliveries[event_key] = {
            "notified_at": format_ts(now_cn()),
            "queue_item_path": str(queue_item_path),
            "draft_pack_dir": str(pack_dir),
            "feishu_doc_url": doc_url,
            "publish_state": publish_state,
            "publish_url": publish_url,
        }
        save_json(notify_state_path, notify_state)
    print(f"SENT log={log_path}")


if __name__ == "__main__":
    main()

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
SELECTION_STATE_DIR = FRONTSTAGE_DIR / "_selection_state"
NOTIFICATION_STATE_PATH = FRONTSTAGE_DIR / "_notification_state" / "day_mainline_delivery_notifier_state.json"
OUTBOX_DIR = ROOT / "07_wechat_bridge_outbox"
QUEUE_DIR = ROOT / "06_publish_queue"
LOG_DIR = ROOT / "10_logs"
FEISHU_DOC_DELIVERY_SCRIPT = ROOT / "09_runbooks" / "scripts" / "market_feishu_doc_delivery.py"
TITLE_RE = re.compile(r"^- 标题：(.+?)\s*$")
TOP_HEADING_RE = re.compile(r"^#\s+(.+?)\s*$")
FIELD_RE_TEMPLATE = r"^(- `{field}`: `)([^`]*)((?:`)\s*)$"
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
CN_TZ = ZoneInfo("Asia/Shanghai")
DEFAULT_ACCOUNT = "market"
DEFAULT_TARGET = f"chat:{board_builder.FRONTSTAGE_GROUP_ID}"
DAY_MAINLINE_DRAFTBOX_DEADLINE_HM = "19:00"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Notify the founder once day_mainline delivery is complete in both WeChat draftbox and Feishu doc.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical date in YYYY-MM-DD.")
    parser.add_argument("--account", default=DEFAULT_ACCOUNT, help="OpenClaw Feishu account id.")
    parser.add_argument("--target", default=DEFAULT_TARGET, help="OpenClaw Feishu target.")
    parser.add_argument("--state-path", default=str(NOTIFICATION_STATE_PATH), help="Notification dedupe state path.")
    parser.add_argument("--dry-run", action="store_true", help="Build and print the message, but skip real delivery.")
    return parser.parse_args()


def clean(value: object, fallback: str = "") -> str:
    normalized = re.sub(r"\s+", " ", str(value or "")).strip().strip("`")
    return normalized or fallback


def compact(text: object, limit: int = 160) -> str:
    normalized = " ".join(str(text or "").split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "…"


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def parse_hm(raw: str) -> tuple[int, int]:
    hour, minute = [int(part) for part in raw.split(":", 1)]
    return hour, minute


def lane_dt(date_text: str, hm: str) -> datetime:
    target_day = date.fromisoformat(date_text)
    hour, minute = parse_hm(hm)
    return datetime(target_day.year, target_day.month, target_day.day, hour, minute, tzinfo=CN_TZ)


def day_token(date_text: str) -> str:
    return date.fromisoformat(date_text).strftime("%Y%m%d")


def selection_state_path(date_text: str) -> Path:
    return SELECTION_STATE_DIR / f"{day_token(date_text)}__day-mainline-founder-pick-state.json"


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


def extract_title(markdown: str, fallback: str) -> str:
    for raw in markdown.splitlines():
        match = TITLE_RE.match(raw.strip())
        if match:
            return clean(match.group(1), fallback)
    for raw in markdown.splitlines():
        match = TOP_HEADING_RE.match(raw.strip())
        if match:
            heading = clean(match.group(1), fallback)
            heading = heading.replace("微信稿｜", "").replace("微信稿|", "").strip()
            return heading or fallback
    return fallback


def parse_prefixed_fields(lines: list[str], prefix: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in lines:
        if not line.startswith(prefix) or "=" not in line:
            continue
        key, value = line.split("=", 1)
        parsed[key] = value.strip()
    return parsed


def extract_field(text: str, field: str) -> str:
    match = re.search(FIELD_RE_TEMPLATE.format(field=re.escape(field)), text, re.M)
    if not match:
        return "n/a"
    return match.group(2).strip() or "n/a"


def extract_markdown_field(path_text: str, field: str) -> str:
    path = Path(clean(path_text, "")).expanduser().resolve() if clean(path_text, "") else None
    if path is None or not path.exists():
        return ""
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(rf"^- `{re.escape(field)}`: ?`?(.*?)`?$", raw_line.strip())
        if match:
            return clean(match.group(1), "")
    return ""


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
    text = read_text(path)
    queue_id = extract_field(text, "queue_id")
    for candidate in (queue_id, path.name):
        match = re.search(r"(\d{8}_\d{6})", candidate)
        if match:
            return (match.group(1), 1, path.name)
    try:
        return (f"{path.stat().st_mtime_ns:020d}", 0, path.name)
    except FileNotFoundError:
        return ("", 0, path.name)


def find_wechat_queue_item(draft_key: str) -> Path | None:
    pattern = f"*__{draft_key}__wechat__publish-queue-item.md"
    candidates = sorted(QUEUE_DIR.glob(pattern), key=queue_item_sort_key)
    if candidates:
        return candidates[-1]
    archive_candidates = sorted(
        QUEUE_DIR.glob(f"archive/**/*__{draft_key}__wechat__publish-queue-item.md"),
        key=queue_item_sort_key,
    )
    return archive_candidates[-1] if archive_candidates else None


def latest_same_day_day_mainline_queue_item(date_text: str) -> Path | None:
    target_prefix = date_text
    candidates: list[Path] = []
    for path in sorted(QUEUE_DIR.glob("*__wechat__publish-queue-item.md"), key=queue_item_sort_key):
        fields = parse_queue_fields(path)
        if clean(fields.get("delivery_lane", ""), "") != "day_mainline":
            continue
        planned = clean(fields.get("planned_publish_at", ""), "")
        deadline = clean(fields.get("delivery_deadline", ""), "")
        if planned.startswith(target_prefix) or deadline.startswith(target_prefix):
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


def queue_item_feishu_meta(queue_item_path: Path | None) -> dict:
    if queue_item_path is None or not queue_item_path.exists():
        return {}
    fields = parse_queue_fields(queue_item_path)
    notes = clean(fields.get("notes", ""), "")
    return {
        "status": note_value(notes, "feishu_doc_status"),
        "url": note_value(notes, "feishu_doc_url"),
        "document_id": note_value(notes, "feishu_doc_token"),
        "source_fingerprint": note_value(notes, "feishu_doc_source_fingerprint"),
    }


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
    lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    sidecar = load_json(sidecar_path)
    if clean(sidecar.get("status"), "") == "success" and clean(sidecar.get("url"), ""):
        return sidecar
    meta = parse_prefixed_fields(lines, "FEISHU_DOC_")
    if meta:
        return {
            "status": clean(meta.get("FEISHU_DOC_STATUS"), "unknown"),
            "mode": clean(meta.get("FEISHU_DOC_MODE"), "n/a"),
            "title": clean(meta.get("FEISHU_DOC_TITLE"), "n/a"),
            "document_id": clean(meta.get("FEISHU_DOC_TOKEN"), ""),
            "url": clean(meta.get("FEISHU_DOC_URL"), ""),
            "source_fingerprint": clean(meta.get("FEISHU_DOC_SOURCE_FINGERPRINT"), ""),
        }
    if completed.returncode != 0:
        return {
            "status": "blocked",
            "error": clean(completed.stderr or completed.stdout, "feishu_doc_delivery_failed"),
        }
    return sidecar


def bridge_result_for_request(request_id: str) -> dict:
    request_dir = OUTBOX_DIR / "requests" / request_id
    result_path = request_dir / "result.json"
    if not result_path.exists():
        return {}
    try:
        return json.loads(result_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def queue_item_bridge_success(queue_item_path: Path | None) -> tuple[bool, str, str]:
    if queue_item_path is None or not queue_item_path.exists():
        return False, "", ""
    fields = parse_queue_fields(queue_item_path)
    publish_url = clean(fields.get("publish_url"), "")
    notes = clean(fields.get("notes"), "")
    media_id = ""
    bridge_status = ""
    for chunk in notes.split("|"):
        stripped = chunk.strip()
        if stripped.startswith("wechat_bridge_status="):
            bridge_status = clean(stripped.split("=", 1)[1], "")
        if stripped.startswith("wechat_draft_media_id="):
            media_id = clean(stripped.split("=", 1)[1], "")
    if publish_url.startswith("wechat-draft://"):
        media_id = media_id or publish_url.split("://", 1)[1]
        return True, media_id, publish_url
    if bridge_status == "success":
        return True, media_id, publish_url
    return False, media_id, publish_url


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


def build_message(date_text: str, title: str, doc_url: str, media_id: str, queue_item_path: Path | None) -> str:
    queue_suffix = f"\n- 发布队列：`{queue_item_path}`" if queue_item_path else ""
    media_suffix = f"（media_id={media_id}）" if media_id else ""
    draft_line = f"- 微信草稿箱：已入箱{media_suffix}" if media_id else "- 微信草稿箱：暂未确认入箱，先发飞书云文档兜底"
    return (
        f"【同行资本｜白天线成品交付｜{date_text}】\n"
        f"- 题目：{title}\n"
        f"{draft_line}\n"
        f"- 飞书云文档：{doc_url}\n"
        "- 兜底说明：如果今晚外出或 Windows 桥接不在身边，可直接打开飞书云文档复制到公众号草稿箱后发布。"
        f"{queue_suffix}\n"
    )


def write_log(path: Path, payload: dict[str, object]) -> None:
    lines = [
        "# Market Day Mainline Delivery Notifier",
        "",
        f"- `timestamp`: `{payload.get('timestamp', '')}`",
        f"- `status`: `{payload.get('status', '')}`",
        f"- `date`: `{payload.get('date', '')}`",
        f"- `title`: `{payload.get('title', '')}`",
        f"- `request_id`: `{payload.get('request_id', '')}`",
        f"- `draft_pack_dir`: `{payload.get('draft_pack_dir', '')}`",
        f"- `queue_item_path`: `{payload.get('queue_item_path', '')}`",
        f"- `feishu_doc_url`: `{payload.get('feishu_doc_url', '')}`",
        f"- `media_id`: `{payload.get('media_id', '')}`",
        f"- `dry_run`: `{'true' if payload.get('dry_run') else 'false'}`",
    ]
    if payload.get("reason"):
        lines.append(f"- `reason`: `{payload.get('reason')}`")
    if payload.get("error"):
        lines.append(f"- `error`: `{payload.get('error')}`")
    if payload.get("message"):
        lines.extend(["", "## Message", "", "```text", str(payload["message"]).rstrip(), "```"])
    if payload.get("delivery_result") is not None:
        lines.extend(["", "## Delivery Result", "", "```json", json.dumps(payload["delivery_result"], ensure_ascii=False, indent=2), "```"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    now = now_cn()
    if now < lane_dt(args.date, DAY_MAINLINE_DRAFTBOX_DEADLINE_HM):
        print("WAITING deadline_not_reached")
        return

    state_path = selection_state_path(args.date)
    selection_state = load_json(state_path)

    draft_pack_dir_text = clean(selection_state.get("draft_pack_dir"), "")
    if not draft_pack_dir_text:
        draft_pack_dir_text = extract_markdown_field(clean(selection_state.get("approved_topic_path"), ""), "draft_pack_target_dir")
    selected_candidate_key = clean(selection_state.get("selected_candidate_key"), "")
    queue_item_path = None
    if selected_candidate_key and draft_pack_dir_text:
        pack_dir = Path(draft_pack_dir_text).expanduser().resolve()
        queue_item_path = find_wechat_queue_item(pack_dir.name)
    else:
        queue_item_path = latest_same_day_day_mainline_queue_item(args.date)
        pack_dir = pack_dir_from_queue_item(queue_item_path) if queue_item_path else None
    if pack_dir is None:
        print("WAITING selection_not_materialized")
        return
    if not pack_dir.exists():
        print("WAITING draft_pack_missing")
        return

    title = extract_title(read_text(pack_dir / "wechat.md"), pack_dir.name.replace("-", " "))
    feishu_meta = ensure_feishu_doc(pack_dir)
    if not clean(feishu_meta.get("url"), ""):
        feishu_meta = {**queue_item_feishu_meta(queue_item_path), **feishu_meta}
    doc_url = clean(feishu_meta.get("url"), clean(selection_state.get("feishu_doc_url"), ""))
    if not doc_url:
        print("WAITING feishu_doc_missing")
        return

    request_id = clean(selection_state.get("bridge_request_id"), f"wechat_bridge__{pack_dir.name}")
    bridge_result = bridge_result_for_request(request_id)
    if queue_item_path is None:
        queue_item_path = find_wechat_queue_item(pack_dir.name)
    queue_success, queue_media_id, _ = queue_item_bridge_success(queue_item_path)

    bridge_success = clean(bridge_result.get("status"), "") == "success"
    media_id = clean(bridge_result.get("media_id"), queue_media_id)

    notify_state_path = Path(args.state_path).expanduser().resolve()
    notify_state = load_json(notify_state_path)
    deliveries = notify_state.setdefault("deliveries", {})
    event_key = f"{args.date}::{pack_dir.name}"
    if deliveries.get(event_key, {}).get("notified_at"):
        print("SKIP already_notified")
        return

    message = build_message(args.date, title, doc_url, media_id, queue_item_path)
    timestamp_token = now.strftime("%Y%m%d_%H%M%S")
    delivery_result = send_group_message(args.account, args.target, message, dry_run=args.dry_run)
    log_path = LOG_DIR / f"{timestamp_token}__{pack_dir.name}__day-mainline-delivery-notifier.md"
    write_log(
        log_path,
        {
            "timestamp": format_ts(now),
            "status": "dry_run_sent" if args.dry_run else "sent",
            "date": args.date,
            "title": title,
            "request_id": request_id,
            "draft_pack_dir": str(pack_dir),
            "queue_item_path": str(queue_item_path) if queue_item_path else "n/a",
            "feishu_doc_url": doc_url,
            "media_id": media_id,
            "dry_run": args.dry_run,
            "message": message,
            "delivery_result": delivery_result,
        },
    )

    if not args.dry_run:
        deliveries[event_key] = {
            "notified_at": format_ts(now_cn()),
            "request_id": request_id,
            "draft_pack_dir": str(pack_dir),
            "feishu_doc_url": doc_url,
            "media_id": media_id,
        }
        notify_state["last_checked_at"] = format_ts(now_cn())
        save_json(notify_state_path, notify_state)

    print(f"SENT log={log_path}")


if __name__ == "__main__":
    main()

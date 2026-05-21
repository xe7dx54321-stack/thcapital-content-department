#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
QUEUE_ROOT = ROOT / "06_publish_queue"
OUTBOX_ROOT = ROOT / "07_wechat_bridge_outbox"
QUEUE_BUILDER_SCRIPT = ROOT / "09_runbooks" / "scripts" / "market_publish_queue_builder.py"
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")


@dataclass(frozen=True)
class RetryCandidate:
    queue_item_path: Path
    queue_key: str
    draft_pack_dir: str
    publish_owner: str
    planned_publish_at: str
    reason: str
    request_id: str
    request_exists: bool
    result_exists: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retry same-day day_mainline WeChat draft-box delivery when the bridge missed the primary deadline.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical date in YYYY-MM-DD.")
    parser.add_argument("--queue-root", default=str(QUEUE_ROOT), help="Publish queue root directory.")
    parser.add_argument("--outbox-dir", default=str(OUTBOX_ROOT), help="WeChat bridge outbox root directory.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum queue items to retry in one run.")
    parser.add_argument("--write", action="store_true", help="Actually rewrite queue item bridge requests.")
    return parser.parse_args()


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return value if value else fallback


def parse_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    if not path.exists():
        return fields
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def extract_note_value(notes: str, key: str) -> str:
    for chunk in notes.split("|"):
        stripped = chunk.strip()
        if stripped.startswith(f"{key}="):
            return clean(stripped.split("=", 1)[1], "")
    return ""


def queue_items_for_date(queue_root: Path, date_text: str) -> list[Path]:
    token = date.fromisoformat(date_text).strftime("%Y%m%d")
    items: list[Path] = []
    for path in sorted(queue_root.glob("*__publish-queue-item.md")):
        fields = parse_fields(path)
        if clean(fields.get("planned_publish_at", ""), "").startswith(date_text):
            items.append(path)
            continue
        if clean(fields.get("delivery_deadline", ""), "").startswith(date_text):
            items.append(path)
            continue
        if path.name.startswith(f"{token}_"):
            items.append(path)
    deduped: list[Path] = []
    for item in items:
        if item not in deduped:
            deduped.append(item)
    return deduped


def candidate_for(path: Path, outbox_dir: Path) -> RetryCandidate | None:
    fields = parse_fields(path)
    if clean(fields.get("delivery_lane", "")) != "day_mainline":
        return None
    if clean(fields.get("platform", "")) != "wechat":
        return None
    if clean(fields.get("status", "")) != "waiting_human_publish":
        return None
    publish_url = clean(fields.get("publish_url", ""), "")
    if publish_url and publish_url != "n/a":
        return None

    notes = clean(fields.get("notes", ""), "")
    bridge_status = extract_note_value(notes, "wechat_bridge_status") or "n/a"
    media_id = extract_note_value(notes, "wechat_draft_media_id")
    if bridge_status == "success" or media_id:
        return None

    queue_key = clean(fields.get("queue_key", path.stem))
    draft_key = queue_key.rsplit("__", 1)[0]
    request_id = f"wechat_bridge__{draft_key}"
    request_dir = outbox_dir / "requests" / request_id
    request_exists = (request_dir / "request.json").exists()
    result_exists = (request_dir / "result.json").exists()

    if bridge_status == "failed":
        reason = "bridge_failed"
    elif not request_exists:
        reason = "request_missing"
    elif not result_exists:
        reason = "result_missing"
    else:
        reason = f"bridge_status={bridge_status}"

    draft_pack_dir = clean(fields.get("draft_pack_dir", ""), "")
    if not draft_pack_dir or draft_pack_dir == "n/a":
        return None

    return RetryCandidate(
        queue_item_path=path,
        queue_key=queue_key,
        draft_pack_dir=draft_pack_dir,
        publish_owner=clean(fields.get("publish_owner", "老板")),
        planned_publish_at=clean(fields.get("planned_publish_at", f"{date.today().isoformat()} 19:00:00 CST")),
        reason=reason,
        request_id=request_id,
        request_exists=request_exists,
        result_exists=result_exists,
    )


def run_retry(candidate: RetryCandidate, write: bool) -> str:
    if not QUEUE_BUILDER_SCRIPT.exists():
        raise SystemExit(f"Publish queue builder missing: {QUEUE_BUILDER_SCRIPT}")
    command = [
        "python3",
        str(QUEUE_BUILDER_SCRIPT),
        "--draft-pack-dir",
        candidate.draft_pack_dir,
        "--status",
        "waiting_human_publish",
        "--platform",
        "wechat",
        "--publish-owner",
        candidate.publish_owner,
        "--planned-publish-at",
        candidate.planned_publish_at,
    ]
    if write:
        command.append("--write")
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    summary = " | ".join(lines[:3]) if lines else "QUEUE_REBUILT"
    return summary


def main() -> None:
    args = parse_args()
    queue_root = Path(args.queue_root).expanduser().resolve()
    outbox_dir = Path(args.outbox_dir).expanduser().resolve()
    all_candidates = [
        candidate
        for path in queue_items_for_date(queue_root, args.date)
        if (candidate := candidate_for(path, outbox_dir)) is not None
    ]
    selected = all_candidates[: max(args.limit, 0)]

    print(f"DAY_MAINLINE_RETRY date={args.date} generated_at={format_ts(now_cn())} candidate_count={len(selected)}")
    if not selected:
        print("NO_RETRY_CANDIDATES")
        return

    for candidate in selected:
        base = (
            f"queue_key={candidate.queue_key} reason={candidate.reason} "
            f"request_exists={'yes' if candidate.request_exists else 'no'} "
            f"result_exists={'yes' if candidate.result_exists else 'no'}"
        )
        if not args.write:
            print(f"RETRY_CANDIDATE {base}")
            continue
        try:
            output = run_retry(candidate, write=True)
            print(f"RETRIED {base} output={output}")
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").strip().replace("\n", " | ")
            print(f"RETRY_FAILED {base} error={stderr or exc}")


if __name__ == "__main__":
    main()

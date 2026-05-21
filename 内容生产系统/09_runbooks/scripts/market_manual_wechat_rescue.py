#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
QUEUE_ROOT = ROOT / "06_publish_queue"
DRAFT_PACK_ROOT = ROOT / "05_draft_packs"
QUEUE_BUILDER_SCRIPT = ROOT / "09_runbooks" / "scripts" / "market_publish_queue_builder.py"
BRIDGE_RECONCILE_SCRIPT = ROOT / "09_runbooks" / "scripts" / "market_wechat_bridge_reconcile.py"
PIPELINE_RECONCILE_SCRIPT = ROOT / "09_runbooks" / "scripts" / "market_pipeline_reconcile.py"
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manual rescue for a WeChat draft: reconcile, requeue, and resend to draft box.")
    parser.add_argument("--topic-key", default="", help="Draft/topic key, e.g. why_we_are_th_capital_20260401")
    parser.add_argument("--draft-pack-dir", default="", help="Absolute draft pack directory path")
    parser.add_argument("--queue-item", default="", help="Absolute publish queue item path")
    parser.add_argument("--queue-key", default="", help="Queue key ending with __wechat")
    parser.add_argument("--publish-owner", default="", help="Optional publish owner override")
    parser.add_argument("--planned-publish-at", default="", help="Optional planned publish time override")
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical date in YYYY-MM-DD")
    parser.add_argument("--write", action="store_true", help="Actually requeue and resend")
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


def run_command(command: list[str], write: bool) -> list[str]:
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    if write:
        for line in lines:
            print(line)
    return lines


def latest_queue_item_for_topic(topic_key: str) -> Path | None:
    matches = sorted(QUEUE_ROOT.glob(f"*__{topic_key}__wechat__publish-queue-item.md"))
    return matches[-1] if matches else None


def resolve_queue_item(args: argparse.Namespace) -> Path | None:
    if clean(args.queue_item, ""):
        path = Path(args.queue_item).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"queue item not found: {path}")
        return path
    if clean(args.queue_key, ""):
        matches = sorted(QUEUE_ROOT.glob(f"*__{args.queue_key}__publish-queue-item.md"))
        if not matches:
            raise SystemExit(f"queue key not found: {args.queue_key}")
        return matches[-1]
    if clean(args.topic_key, ""):
        return latest_queue_item_for_topic(clean(args.topic_key, ""))
    return None


def resolve_draft_pack_dir(args: argparse.Namespace, queue_item_path: Path | None) -> Path:
    if clean(args.draft_pack_dir, ""):
        path = Path(args.draft_pack_dir).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"draft pack dir not found: {path}")
        return path
    if queue_item_path is not None:
        fields = parse_fields(queue_item_path)
        draft_pack_dir = clean(fields.get("draft_pack_dir", ""), "")
        if draft_pack_dir:
            path = Path(draft_pack_dir).expanduser().resolve()
            if path.exists():
                return path
    if clean(args.topic_key, ""):
        path = (DRAFT_PACK_ROOT / clean(args.topic_key, "")).resolve()
        if path.exists():
            return path
    raise SystemExit("unable to resolve draft pack dir; provide --topic-key or --draft-pack-dir")


def queue_context(queue_item_path: Path | None, draft_pack_dir: Path, args: argparse.Namespace) -> tuple[str, str]:
    publish_owner = clean(args.publish_owner, "")
    planned_publish_at = clean(args.planned_publish_at, "")
    if queue_item_path is not None and queue_item_path.exists():
        fields = parse_fields(queue_item_path)
        if not publish_owner:
            publish_owner = clean(fields.get("publish_owner", ""), "")
        if not planned_publish_at:
            planned_publish_at = clean(fields.get("planned_publish_at", ""), "")
    if not publish_owner:
        publish_owner = "老板"
    if not planned_publish_at:
        planned_publish_at = f"{args.date} 19:00:00 CST"
    return publish_owner, planned_publish_at


def main() -> None:
    args = parse_args()
    queue_item_path = resolve_queue_item(args)
    draft_pack_dir = resolve_draft_pack_dir(args, queue_item_path)
    publish_owner, planned_publish_at = queue_context(queue_item_path, draft_pack_dir, args)

    print(f"MANUAL_WECHAT_RESCUE generated_at={format_ts(now_cn())}")
    print(f"DRAFT_PACK_DIR {draft_pack_dir}")
    print(f"QUEUE_ITEM {queue_item_path or 'n/a'}")
    print(f"PUBLISH_OWNER {publish_owner}")
    print(f"PLANNED_PUBLISH_AT {planned_publish_at}")

    if not args.write:
        return

    if BRIDGE_RECONCILE_SCRIPT.exists():
        run_command(["python3", str(BRIDGE_RECONCILE_SCRIPT), "--write"], write=True)
    if PIPELINE_RECONCILE_SCRIPT.exists():
        run_command(["python3", str(PIPELINE_RECONCILE_SCRIPT), "--date", args.date, "--write"], write=True)
    if not QUEUE_BUILDER_SCRIPT.exists():
        raise SystemExit(f"publish queue builder missing: {QUEUE_BUILDER_SCRIPT}")

    builder_cmd = [
        "python3",
        str(QUEUE_BUILDER_SCRIPT),
        "--draft-pack-dir",
        str(draft_pack_dir),
        "--status",
        "waiting_human_publish",
        "--platform",
        "wechat",
        "--publish-owner",
        publish_owner,
        "--planned-publish-at",
        planned_publish_at,
        "--write",
    ]
    run_command(builder_cmd, write=True)
    if BRIDGE_RECONCILE_SCRIPT.exists():
        run_command(["python3", str(BRIDGE_RECONCILE_SCRIPT), "--write"], write=True)
    print("MANUAL_WECHAT_RESCUE_DONE")


if __name__ == "__main__":
    main()

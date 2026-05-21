#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from market_content_hygiene_guard import inspect_content_hygiene
from market_content_pack_truth import latest_content_pack_verdict
from market_publish_queue_builder import rebuild_board


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
DRAFT_PACK_ROOT = ROOT / "05_draft_packs"
QUEUE_DIR = ROOT / "06_publish_queue"
LOG_DIR = ROOT / "10_logs"
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
PUBLISH_PATH_STATUSES = {"ready", "queued", "waiting_human_publish"}
ACTIVE_QUEUE_STATUSES = {"queued", "waiting_human_publish"}
CONFIRMED_PUBLISH_MANUAL_GATES = {"human_publish_completed", "auto_publish_completed"}


@dataclass(frozen=True)
class ReconcileChange:
    kind: str
    topic_key: str
    source_path: str
    from_status: str
    to_status: str
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reconcile stale draft-pack / publish-queue states against latest content-pack truth.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical date in YYYY-MM-DD.")
    parser.add_argument("--write", action="store_true", help="Apply the reconciliation instead of printing planned changes only.")
    return parser.parse_args()


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def day_token(date_text: str) -> str:
    return date.fromisoformat(date_text).strftime("%Y%m%d")


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


def update_field(text: str, field_name: str, value: str) -> str:
    pattern = re.compile(rf"^(- `{re.escape(field_name)}`: `)([^`]*)(`)\s*$", re.M)
    if pattern.search(text):
        return pattern.sub(lambda match: f"{match.group(1)}{value}{match.group(3)}", text, count=1)
    return text


def merge_note(existing: str, addition: str) -> str:
    existing_clean = clean(existing, "")
    addition_clean = clean(addition, "")
    if not existing_clean:
        return addition_clean
    if addition_clean in existing_clean:
        return existing_clean
    return f"{existing_clean} | {addition_clean}"


def topic_key_from_queue(fields: dict[str, str], path: Path) -> str:
    queue_key = clean(fields.get("queue_key", path.stem), "")
    if "__" in queue_key:
        return clean(queue_key.rsplit("__", 1)[0], path.stem)
    return clean(fields.get("topic_id", path.stem), path.stem)


def draft_pack_dir_from_queue(fields: dict[str, str]) -> Path | None:
    explicit = clean(fields.get("draft_pack_dir", ""), "")
    if explicit and explicit != "n/a":
        return Path(explicit).expanduser()
    content_path = clean(fields.get("content_path", ""), "")
    if content_path and content_path != "n/a":
        return Path(content_path).expanduser().parent
    return None


def queue_item_fields_for_topic(topic_key: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for path in sorted(QUEUE_DIR.glob("*__publish-queue-item.md")):
        fields = parse_fields(path)
        if topic_key_from_queue(fields, path) == topic_key:
            items.append(fields)
    return items


def topic_has_confirmed_publish(topic_key: str) -> bool:
    for fields in queue_item_fields_for_topic(topic_key):
        status = clean(fields.get("status", "n/a"))
        manual_gate = clean(fields.get("manual_gate", "n/a"))
        actual_publish_at = clean(fields.get("actual_publish_at", "n/a"))
        publish_url = clean(fields.get("publish_url", "n/a"))
        if status == "published":
            return True
        if manual_gate in CONFIRMED_PUBLISH_MANUAL_GATES:
            return True
        if actual_publish_at != "n/a":
            return True
        if publish_url not in {"n/a", ""} and not publish_url.startswith("wechat-draft://"):
            return True
    return False


def pack_card_needs_live_reconcile(topic_key: str, current_status: str) -> bool:
    if current_status in PUBLISH_PATH_STATUSES:
        return True
    if current_status != "published":
        return False
    return not topic_has_confirmed_publish(topic_key)


def reconcile_pack_card(path: Path) -> tuple[ReconcileChange | None, str | None]:
    fields = parse_fields(path)
    topic_key = clean(fields.get("draft_key", path.parent.name))
    current_status = clean(fields.get("status", "n/a"))
    verdict = latest_content_pack_verdict(topic_key)
    live_reconcile = pack_card_needs_live_reconcile(topic_key, current_status)

    if verdict and verdict.requires_rework and live_reconcile:
        updated = path.read_text(encoding="utf-8")
        updated = update_field(updated, "status", "needs_revision")
        updated = update_field(updated, "next_step", "needs_revision -> revise current object")
        updated = update_field(updated, "publish_gate", "blocked_by_rework")
        updated = update_field(updated, "updated_at", format_ts(now_cn()))
        change = ReconcileChange(
            kind="pack_status_conflicts_with_rework",
            topic_key=topic_key,
            source_path=str(path),
            from_status=current_status,
            to_status="needs_revision",
            detail=f"最新 content-pack verdict 为 rework（{verdict.score_text or 'n/a'}），草稿状态回收为 needs_revision。",
        )
        return change, updated

    if verdict is None and current_status == "ready":
        updated = path.read_text(encoding="utf-8")
        updated = update_field(updated, "status", "draft_ready")
        updated = update_field(updated, "next_step", "draft_ready -> content-pack stage gate review")
        updated = update_field(updated, "publish_gate", "awaiting_scorecard")
        updated = update_field(updated, "updated_at", format_ts(now_cn()))
        change = ReconcileChange(
            kind="ready_without_scorecard",
            topic_key=topic_key,
            source_path=str(path),
            from_status=current_status,
            to_status="draft_ready",
            detail="draft pack 已落到 ready，但缺 content-pack scorecard，回收为 draft_ready 等待裁判。",
        )
        return change, updated

    platform = "wechat"
    content_path = path.parent / "wechat.md"
    if content_path.exists() and live_reconcile:
        hygiene = inspect_content_hygiene(path.parent, platform, content_path=content_path)
        if hygiene.blocking_issues:
            updated = path.read_text(encoding="utf-8")
            updated = update_field(updated, "status", "needs_revision")
            updated = update_field(updated, "next_step", "needs_revision -> fix content hygiene blockers")
            updated = update_field(updated, "publish_gate", "blocked_by_content_hygiene")
            updated = update_field(updated, "updated_at", format_ts(now_cn()))
            change = ReconcileChange(
                kind="pack_status_conflicts_with_hygiene",
                topic_key=topic_key,
                source_path=str(path),
                from_status=current_status,
                to_status="needs_revision",
                detail=f"draft pack 存在成品卫生阻断：{','.join(hygiene.blocking_issues)}。",
            )
            return change, updated

    return None, None


def reconcile_queue_item(path: Path) -> tuple[ReconcileChange | None, str | None]:
    fields = parse_fields(path)
    current_status = clean(fields.get("status", "n/a"))
    if current_status not in ACTIVE_QUEUE_STATUSES:
        return None, None

    topic_key = topic_key_from_queue(fields, path)
    platform = clean(fields.get("platform", "n/a"))
    verdict = latest_content_pack_verdict(topic_key)

    if verdict and not verdict.allows_publish_queue_for(platform):
        note = merge_note(
            fields.get("notes", "n/a"),
            f"reconciled_on={date.today().isoformat()} latest_verdict=rework score={verdict.score_text or 'n/a'}",
        )
        updated = path.read_text(encoding="utf-8")
        updated = update_field(updated, "status", "deferred")
        updated = update_field(updated, "manual_gate", "blocked_by_rework")
        updated = update_field(updated, "human_action_required", f"暂停 {platform} 发布，先修当前对象并重新通过 content-pack 裁判。")
        updated = update_field(updated, "frontstage_summary", f"{platform} 已从发布队列暂缓，原因是最新 content-pack verdict 回退为 rework。")
        updated = update_field(updated, "notes", note)
        change = ReconcileChange(
            kind="queue_item_conflicts_with_verdict",
            topic_key=topic_key,
            source_path=str(path),
            from_status=current_status,
            to_status="deferred",
            detail=f"最新 content-pack verdict 不允许发布，{platform} queue item 暂缓。",
        )
        return change, updated

    if verdict is None:
        note = merge_note(fields.get("notes", "n/a"), f"reconciled_on={date.today().isoformat()} latest_verdict=missing")
        updated = path.read_text(encoding="utf-8")
        updated = update_field(updated, "status", "deferred")
        updated = update_field(updated, "manual_gate", "awaiting_scorecard")
        updated = update_field(updated, "human_action_required", f"暂停 {platform} 发布，先补 content-pack 裁判评分卡。")
        updated = update_field(updated, "frontstage_summary", f"{platform} 已从发布队列暂缓，等待 content-pack scorecard。")
        updated = update_field(updated, "notes", note)
        change = ReconcileChange(
            kind="queue_item_missing_scorecard",
            topic_key=topic_key,
            source_path=str(path),
            from_status=current_status,
            to_status="deferred",
            detail=f"{platform} queue item 缺少对应的 content-pack scorecard，已暂缓。",
        )
        return change, updated

    pack_dir = draft_pack_dir_from_queue(fields)
    if pack_dir is not None:
        content_path = Path(clean(fields.get("content_path", ""), ""))
        if content_path.exists():
            hygiene = inspect_content_hygiene(pack_dir, platform, content_path=content_path)
            if hygiene.blocking_issues:
                note = merge_note(
                    fields.get("notes", "n/a"),
                    f"reconciled_on={date.today().isoformat()} content_hygiene_blockers={','.join(hygiene.blocking_issues)}",
                )
                updated = path.read_text(encoding="utf-8")
                updated = update_field(updated, "status", "deferred")
                updated = update_field(updated, "manual_gate", "blocked_by_content_hygiene")
                updated = update_field(updated, "human_action_required", f"暂停 {platform} 发布，先修复 content hygiene：{','.join(hygiene.blocking_issues)}。")
                updated = update_field(updated, "frontstage_summary", f"{platform} 已从发布队列暂缓，原因是 content hygiene 未达标。")
                updated = update_field(updated, "notes", note)
                change = ReconcileChange(
                    kind="queue_item_conflicts_with_hygiene",
                    topic_key=topic_key,
                    source_path=str(path),
                    from_status=current_status,
                    to_status="deferred",
                    detail=f"{platform} queue item 存在成品卫生阻断：{','.join(hygiene.blocking_issues)}。",
                )
                return change, updated

    return None, None


def render_report(date_text: str, changes: list[ReconcileChange]) -> str:
    lines = [
        "# Market Pipeline Reconciliation",
        "",
        f"- `date`: `{date_text}`",
        f"- `generated_at`: `{format_ts(now_cn())}`",
        f"- `change_count`: `{len(changes)}`",
        "",
        "## Changes",
        "",
    ]
    if not changes:
        lines.append("- `none`")
        return "\n".join(lines).rstrip() + "\n"

    for idx, change in enumerate(changes, start=1):
        lines.extend(
            [
                f"### {idx}. `{change.topic_key}`",
                f"- `kind`: `{change.kind}`",
                f"- `source_path`: `{change.source_path}`",
                f"- `from_status`: `{change.from_status}`",
                f"- `to_status`: `{change.to_status}`",
                f"- `detail`: `{change.detail}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    changes: list[ReconcileChange] = []
    pending_writes: list[tuple[Path, str]] = []

    for path in sorted(DRAFT_PACK_ROOT.glob("*/00_draft-pack-card.md")):
        change, updated = reconcile_pack_card(path)
        if change and updated:
            changes.append(change)
            pending_writes.append((path, updated))

    for path in sorted(QUEUE_DIR.glob("*__publish-queue-item.md")):
        change, updated = reconcile_queue_item(path)
        if change and updated:
            changes.append(change)
            pending_writes.append((path, updated))

    changes.sort(key=lambda item: (item.kind, item.topic_key, item.source_path))
    rendered = render_report(args.date, changes)
    print(rendered)

    report_path = LOG_DIR / f"{day_token(args.date)}__market-pipeline-reconciliation.md"
    if args.write:
        for path, updated in pending_writes:
            path.write_text(updated, encoding="utf-8")
        report_path.write_text(rendered, encoding="utf-8")
        board_path = QUEUE_DIR / f"{day_token(args.date)}__publish-queue-board.md"
        rebuild_board(QUEUE_DIR, board_path)
        print(f"REPORT_PATH={report_path}")


if __name__ == "__main__":
    main()

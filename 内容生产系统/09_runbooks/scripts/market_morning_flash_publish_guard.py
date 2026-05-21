#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from market_morning_flash_autosign import autosign as autosign_morning_flash
from market_morning_flash_gate_recovery import recover_morning_flash_gate
from market_publish_queue_builder import rebuild_board


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
QUEUE_ROOT = ROOT / "06_publish_queue"
LOG_ROOT = ROOT / "10_logs"
WECHAT_SUBMIT_SCRIPT = ROOT / "09_runbooks" / "scripts" / "market_wechat_publish_submit.py"
MORNING_PREFLIGHT_SCRIPT = ROOT / "09_runbooks" / "scripts" / "market_morning_flash_preflight.py"
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
CHECK_RE = re.compile(r"^- `([^`]+)`: `([^`]+)`")
TIMESTAMP_TOKEN_RE = re.compile(r"(\d{8}_\d{6})")
STRUCTURAL_PREFLIGHT_BLOCKERS = {
    "recent_topic_duplicate_guard",
    "public_copy_no_internal_scaffolding",
}


@dataclass(frozen=True)
class GuardDecision:
    queue_item_path: Path
    queue_key: str
    eligible: bool
    reason: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Auto-publish only morning_flash WeChat items that passed all guardrails.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical day in YYYY-MM-DD")
    parser.add_argument("--queue-item", default="", help="Absolute queue item path")
    parser.add_argument("--queue-key", default="", help="queue_key under publish queue root")
    parser.add_argument("--queue-root", default=str(QUEUE_ROOT))
    parser.add_argument("--limit", type=int, default=2, help="Maximum items to auto-publish in one run")
    parser.add_argument("--write", action="store_true", help="Actually call freepublish submit")
    return parser.parse_args()


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return value if value else fallback


def parse_dt(raw: str | None) -> datetime | None:
    value = clean(raw or "", "")
    if not value or value.lower() in {"n/a", "none", "unknown", "not_found"}:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S CST", "%Y-%m-%d %H:%M CST", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=CN_TZ)
        except ValueError:
            continue
    return None


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
    if not addition_clean or addition_clean in existing_clean:
        return existing_clean
    return f"{existing_clean} | {addition_clean}"


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


def queue_items_for_date(queue_root: Path, date_text: str) -> list[Path]:
    token = date.fromisoformat(date_text).strftime("%Y%m%d")
    items: list[Path] = []
    for path in sorted(queue_root.glob("*__publish-queue-item.md")):
        fields = parse_fields(path)
        if clean(fields.get("delivery_deadline", ""), "").startswith(date_text):
            items.append(path)
            continue
        if clean(fields.get("planned_publish_at", ""), "").startswith(date_text):
            items.append(path)
            continue
        if path.name.startswith(f"{token}_"):
            items.append(path)
    deduped: list[Path] = []
    for item in items:
        if item not in deduped:
            deduped.append(item)
    latest_by_queue_key: dict[str, Path] = {}
    passthrough: list[Path] = []
    for item in deduped:
        fields = parse_fields(item)
        queue_key = clean(fields.get("queue_key", ""), "")
        if not queue_key:
            passthrough.append(item)
            continue
        current = latest_by_queue_key.get(queue_key)
        if current is None or queue_item_sort_key(item) > queue_item_sort_key(current):
            latest_by_queue_key[queue_key] = item
    merged = list(latest_by_queue_key.values()) + passthrough
    return sorted(merged, key=queue_item_sort_key)


def queue_item_sort_key(path: Path) -> tuple[str, int, str]:
    fields = parse_fields(path)
    queue_id = clean(fields.get("queue_id", ""), "")
    for candidate in (queue_id, path.name):
        match = TIMESTAMP_TOKEN_RE.search(candidate)
        if match:
            return (match.group(1), 1, path.name)
    try:
        return (f"{path.stat().st_mtime_ns:020d}", 0, path.name)
    except FileNotFoundError:
        return ("", 0, path.name)


def checklist_fields(path: Path) -> dict[str, str]:
    return parse_fields(path) if path.exists() else {}


def checklist_passed(path: Path) -> bool:
    fields = checklist_fields(path)
    decision = clean(fields.get("decision", ""), "").lower()
    checklist_status = clean(fields.get("checklist_status", ""), "").lower()
    return decision == "pass" or checklist_status == "pass"


def already_published(fields: dict[str, str]) -> bool:
    if clean(fields.get("status", ""), "") == "published":
        return True
    notes = clean(fields.get("notes", ""), "")
    return "wechat_publish_route=freepublish_submit" in notes


def draft_pack_dir(fields: dict[str, str]) -> Path:
    explicit = clean(fields.get("draft_pack_dir", ""), "")
    if explicit:
        return Path(explicit).expanduser()
    content_path = clean(fields.get("content_path", ""), "")
    if content_path:
        return Path(content_path).expanduser().parent
    raise SystemExit("queue item missing draft_pack_dir and content_path")


def refresh_preflight(queue_item_path: Path) -> None:
    if not MORNING_PREFLIGHT_SCRIPT.exists():
        raise SystemExit(f"morning flash preflight script missing: {MORNING_PREFLIGHT_SCRIPT}")
    subprocess.run(
        ["python3", str(MORNING_PREFLIGHT_SCRIPT), "--queue-item", str(queue_item_path), "--write"],
        check=True,
        capture_output=True,
        text=True,
    )


def checklist_check_statuses(path: Path) -> dict[str, str]:
    statuses: dict[str, str] = {}
    if not path.exists():
        return statuses
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = CHECK_RE.match(raw_line.strip())
        if match:
            code, status = match.groups()
            statuses[clean(code, "")] = clean(status, "")
    return statuses


def structural_preflight_blockers(queue_item_path: Path) -> list[str]:
    fields = parse_fields(queue_item_path)
    pack_dir = draft_pack_dir(fields)
    preflight_path = pack_dir / "morning-flash-preflight.md"
    statuses = checklist_check_statuses(preflight_path)
    blockers = [code for code in STRUCTURAL_PREFLIGHT_BLOCKERS if statuses.get(code) == "fail"]
    return blockers


def downgrade_pack_card(queue_item_path: Path, blockers: list[str]) -> bool:
    fields = parse_fields(queue_item_path)
    pack_dir = draft_pack_dir(fields)
    card_path = pack_dir / "00_draft-pack-card.md"
    if not card_path.exists():
        return False
    updated = card_path.read_text(encoding="utf-8")
    updated = update_field(updated, "status", "needs_revision")
    updated = update_field(updated, "next_step", "needs_revision -> fix morning_flash blockers and re-run guard")
    updated = update_field(updated, "publish_gate", "blocked_by_morning_guard")
    updated = update_field(updated, "updated_at", format_ts(now_cn()))
    card_path.write_text(updated, encoding="utf-8")
    return True


def downgrade_queue_item(queue_item_path: Path, blockers: list[str]) -> bool:
    if not blockers:
        return False
    fields = parse_fields(queue_item_path)
    current_status = clean(fields.get("status", ""), "")
    if current_status != "waiting_human_publish":
        return False
    blocker_text = ",".join(blockers)
    updated = queue_item_path.read_text(encoding="utf-8")
    updated = update_field(updated, "status", "deferred")
    updated = update_field(updated, "manual_gate", "blocked_by_morning_guard")
    updated = update_field(
        updated,
        "human_action_required",
        f"晨间自动发布已拦截，先修复 {blocker_text}，通过 preflight / reviewer / leader 后再决定是否重入发布队列。",
    )
    updated = update_field(
        updated,
        "frontstage_summary",
        f"晨间快反稿已从自动发布队列暂缓，原因：{blocker_text}。",
    )
    note = merge_note(
        fields.get("notes", "n/a"),
        f"morning_guard_blocked_at={now_cn().isoformat()} morning_guard_blockers={blocker_text}",
    )
    updated = update_field(updated, "notes", note)
    queue_item_path.write_text(updated, encoding="utf-8")
    downgrade_pack_card(queue_item_path, blockers)
    return True


def guard_decision(queue_item_path: Path) -> GuardDecision:
    fields = parse_fields(queue_item_path)
    queue_key = clean(fields.get("queue_key", queue_item_path.stem))
    if clean(fields.get("platform", "")) != "wechat":
        return GuardDecision(queue_item_path, queue_key, False, "platform is not wechat")
    if clean(fields.get("delivery_lane", "")) != "morning_flash":
        return GuardDecision(queue_item_path, queue_key, False, "delivery_lane is not morning_flash")
    if clean(fields.get("publish_mode", "")) != "auto_api":
        return GuardDecision(queue_item_path, queue_key, False, "publish_mode is not auto_api")
    if already_published(fields):
        return GuardDecision(queue_item_path, queue_key, False, "already published")
    if clean(fields.get("status", "")) != "waiting_human_publish":
        return GuardDecision(queue_item_path, queue_key, False, f"status={clean(fields.get('status', 'n/a'))}")
    planned_publish_at = parse_dt(fields.get("planned_publish_at", "")) or parse_dt(fields.get("delivery_deadline", ""))
    if planned_publish_at and now_cn() < planned_publish_at:
        return GuardDecision(
            queue_item_path,
            queue_key,
            False,
            f"planned_publish_at_not_reached({format_ts(planned_publish_at)})",
        )

    pack_dir = draft_pack_dir(fields)
    preflight_path = pack_dir / "morning-flash-preflight.md"
    reviewer_path = pack_dir / "morning-flash-reviewer-checklist.md"
    leader_path = pack_dir / "morning-flash-leader-checklist.md"
    if not preflight_path.exists():
        return GuardDecision(queue_item_path, queue_key, False, "preflight report missing")
    preflight_fields = parse_fields(preflight_path)
    if clean(preflight_fields.get("technical_preflight_status", "")) != "pass":
        return GuardDecision(
            queue_item_path,
            queue_key,
            False,
            f"technical_preflight_status={clean(preflight_fields.get('technical_preflight_status', 'n/a'))}",
        )
    if not checklist_passed(reviewer_path):
        return GuardDecision(queue_item_path, queue_key, False, "reviewer checklist not passed")
    if not checklist_passed(leader_path):
        return GuardDecision(queue_item_path, queue_key, False, "leader checklist not passed")
    return GuardDecision(queue_item_path, queue_key, True, "all three gates passed")


def run_submit(queue_item_path: Path) -> str:
    if not WECHAT_SUBMIT_SCRIPT.exists():
        raise SystemExit(f"wechat publish submit script missing: {WECHAT_SUBMIT_SCRIPT}")
    completed = subprocess.run(
        ["python3", str(WECHAT_SUBMIT_SCRIPT), "--queue-item", str(queue_item_path), "--write"],
        check=True,
        capture_output=True,
        text=True,
    )
    output = "\n".join(line.strip() for line in completed.stdout.splitlines() if line.strip())
    return output or "PUBLISH_SUCCESS"


def render_log(
    date_text: str,
    decisions: list[GuardDecision],
    published: list[tuple[GuardDecision, str]],
    deferred_items: list[tuple[GuardDecision, list[str]]],
) -> str:
    lines = [
        "# Morning Flash Publish Guard",
        "",
        f"- `date`: `{date_text}`",
        f"- `generated_at`: `{format_ts(now_cn())}`",
        f"- `candidate_count`: `{len(decisions)}`",
        f"- `eligible_count`: `{len([item for item in decisions if item.eligible])}`",
        f"- `published_count`: `{len(published)}`",
        f"- `deferred_count`: `{len(deferred_items)}`",
        "",
        "## Decisions",
        "",
    ]
    if decisions:
        for item in decisions:
            lines.append(
                f"- `{item.queue_key}`｜eligible=`{'yes' if item.eligible else 'no'}`｜reason=`{item.reason}`｜path=`{item.queue_item_path}`"
            )
    else:
        lines.append("- `none`")
    lines.extend(["", "## Publish Actions", ""])
    if published:
        for item, output in published:
            lines.append(f"- `{item.queue_key}`｜{output}")
    else:
        lines.append("- `none`")
    lines.extend(["", "## Deferred Actions", ""])
    if deferred_items:
        for item, blockers in deferred_items:
            lines.append(f"- `{item.queue_key}`｜blockers=`{', '.join(blockers)}`｜action=`deferred`")
    else:
        lines.append("- `none`")
    lines.append("")
    return "\n".join(lines)


def _recover_deferred_items(
    candidates: list[Path], date_text: str, queue_root: Path
) -> list[Path]:
    """Re-include deferred morning_flash items whose three gates now pass."""
    token = date.fromisoformat(date_text).strftime("%Y%m%d")
    recovered: list[Path] = []
    for path in sorted(queue_root.glob("*__publish-queue-item.md")):
        fields = parse_fields(path)
        if clean(fields.get("delivery_lane", "")) != "morning_flash":
            continue
        if clean(fields.get("status", "")) != "deferred":
            continue
        if path in candidates:
            continue
        pack_dir = draft_pack_dir(fields)
        preflight_path = pack_dir / "morning-flash-preflight.md"
        reviewer_path = pack_dir / "morning-flash-reviewer-checklist.md"
        leader_path = pack_dir / "morning-flash-leader-checklist.md"
        if not preflight_path.exists():
            continue
        pf = parse_fields(preflight_path)
        if clean(pf.get("technical_preflight_status", "")) != "pass":
            continue
        if not checklist_passed(reviewer_path):
            continue
        if not checklist_passed(leader_path):
            continue
        blockers = structural_preflight_blockers(path)
        if blockers:
            continue
        updated = path.read_text(encoding="utf-8")
        updated = update_field(updated, "status", "waiting_human_publish")
        updated = update_field(updated, "manual_gate", "auto_recovered_from_deferred")
        note = merge_note(
            fields.get("notes", "n/a"),
            f"auto_recovered_at={now_cn().isoformat()} reason=three_gates_passed_after_deferred",
        )
        updated = update_field(updated, "notes", note)
        path.write_text(updated, encoding="utf-8")
        card_path = pack_dir / "00_draft-pack-card.md"
        if card_path.exists():
            card_text = card_path.read_text(encoding="utf-8")
            card_text = update_field(card_text, "status", "ready")
            card_text = update_field(card_text, "publish_gate", "auto_recovered")
            card_path.write_text(card_text, encoding="utf-8")
        recovered.append(path)
    if recovered:
        print(f"[recovery] {len(recovered)} deferred item(s) auto-recovered: {[p.name for p in recovered]}")
    return candidates + recovered


def main() -> None:
    args = parse_args()
    queue_root = Path(args.queue_root).expanduser().resolve()
    if clean(args.queue_item, "") or clean(args.queue_key, ""):
        candidates = [resolve_queue_item_path(queue_root, args.queue_item, args.queue_key)]
    else:
        candidates = queue_items_for_date(queue_root, args.date)

    if args.write:
        for candidate in candidates:
            refresh_preflight(candidate)
            autosign_morning_flash(candidate, write=True)
            recover_morning_flash_gate(candidate, write=True)
        candidates = _recover_deferred_items(candidates, args.date, queue_root)

    decisions = [guard_decision(path) for path in candidates]
    deferred_items: list[tuple[GuardDecision, list[str]]] = []
    if args.write:
        for item in decisions:
            if item.eligible:
                continue
            blockers = structural_preflight_blockers(item.queue_item_path)
            if downgrade_queue_item(item.queue_item_path, blockers):
                deferred_items.append((item, blockers))
    eligible = [item for item in decisions if item.eligible][: max(args.limit, 0)]
    published: list[tuple[GuardDecision, str]] = []
    if args.write:
        for item in eligible:
            output = run_submit(item.queue_item_path)
            published.append((item, output))

    log_text = render_log(args.date, decisions, published, deferred_items)
    if args.write:
        LOG_ROOT.mkdir(parents=True, exist_ok=True)
        log_path = LOG_ROOT / f"{now_cn().strftime('%Y%m%d_%H%M%S')}__morning-flash-publish-guard.md"
        log_path.write_text(log_text, encoding="utf-8")
        if deferred_items:
            board_path = queue_root / f"{date.fromisoformat(args.date).strftime('%Y%m%d')}__publish-queue-board.md"
            rebuild_board(queue_root, board_path)
        print(log_path)
    print(log_text)


if __name__ == "__main__":
    main()

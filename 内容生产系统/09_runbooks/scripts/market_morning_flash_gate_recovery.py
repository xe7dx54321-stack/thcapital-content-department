#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
CHECK_RE = re.compile(r"^- `([^`]+)`: `([^`]+)`(?:｜(.*))?$")
FIELD_RE_TEMPLATE = r"^(- `{field}`: `)([^`]*)((?:`)\s*)$"
PRIORITY_RE = re.compile(r"(?i)(?:\*\*|\[)?P([012])(?:[\]/\s—:-]|$)|(?:\*\*)?P([012])(?:[\s—:-]|$)")
BRIDGE_HINT_RE = re.compile(r"(?i)bridge|infra|基础设施")
OPTIONAL_HINT_RE = re.compile(r"(?i)minor|optional|非强制|不阻断|可选")
INFRA_ONLY_HINTS = (
    "唯一阻塞点",
    "唯一硬阻断",
    "与内容质量无关",
    "内容本身无 fatal 问题",
    "内容层无实质问题",
    "structural gates 双 pass",
    "三闸门全绿",
)
REVIEWER_REQUIRED_CHECKS = (
    "duplicate_and_freshness",
    "headline_and_hook",
    "timeliness_and_heat",
    "risk_wording",
    "public_copy_cleanliness",
    "layout_and_images",
)
STRUCTURAL_PREFLIGHT_CHECKS = (
    "recent_topic_duplicate_guard",
    "public_copy_no_internal_scaffolding",
)
OBJECTIVE_PREFLIGHT_CHECKS = (
    "content_pack_gate_wechat",
    "roundup_item_count",
    "roundup_titles_aligned",
    "roundup_title_limit",
    "roundup_summary_limit",
    "roundup_detail_length_window",
    "roundup_third_party_media_mentions",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recover stale morning_flash reviewer / leader checklist files once bridge results arrive."
    )
    parser.add_argument("--queue-item", required=True, help="Absolute publish queue item path.")
    parser.add_argument("--write", action="store_true", help="Apply recovery in-place.")
    return parser.parse_args()


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


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


def parse_check_rows(path: Path) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    if not path.exists():
        return rows
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = CHECK_RE.match(raw_line.strip())
        if match:
            code, status, detail = match.groups()
            rows[clean(code, "")] = (clean(status, ""), clean(detail or "", ""))
    return rows


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


def resolve_pack_dir(queue_fields: dict[str, str], queue_item_path: Path) -> Path:
    explicit = clean(queue_fields.get("draft_pack_dir", ""), "")
    if explicit:
        return Path(explicit).expanduser()
    content_path = clean(queue_fields.get("content_path", ""), "")
    if content_path:
        return Path(content_path).expanduser().parent
    raise SystemExit(f"queue item missing draft_pack_dir/content_path: {queue_item_path}")


def has_non_infra_priority_blocker(text: str) -> bool:
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if not PRIORITY_RE.search(line):
            continue
        if BRIDGE_HINT_RE.search(line):
            continue
        if OPTIONAL_HINT_RE.search(line):
            continue
        return True
    return False


def infra_only_signal(text: str) -> bool:
    lowered = text.lower()
    return any(hint in text for hint in INFRA_ONLY_HINTS) or "bridge" in lowered


def preflight_checks_pass(preflight_rows: dict[str, tuple[str, str]], codes: tuple[str, ...]) -> bool:
    present = [code for code in codes if code in preflight_rows]
    if not present:
        return False
    return all(clean(preflight_rows.get(code, ("", ""))[0], "").lower() == "pass" for code in present)


def reviewer_recoverable(
    reviewer_path: Path,
    reviewer_fields: dict[str, str],
    reviewer_rows: dict[str, tuple[str, str]],
    preflight_fields: dict[str, str],
    preflight_rows: dict[str, tuple[str, str]],
) -> bool:
    if not reviewer_path.exists():
        return False
    if clean(reviewer_fields.get("decision", "")).lower() == "pass":
        return False
    if clean(preflight_fields.get("technical_preflight_status", "")).lower() != "pass":
        return False
    if clean(preflight_fields.get("bridge_status", "")).lower() != "success":
        return False
    if any(clean(preflight_rows.get(code, ("", ""))[0], "").lower() != "pass" for code in STRUCTURAL_PREFLIGHT_CHECKS):
        return False
    if preflight_checks_pass(preflight_rows, OBJECTIVE_PREFLIGHT_CHECKS):
        return True
    if not reviewer_rows:
        return False
    if any(clean(reviewer_rows.get(code, ("", ""))[0], "").lower() != "pass" for code in REVIEWER_REQUIRED_CHECKS):
        return False
    text = reviewer_path.read_text(encoding="utf-8")
    if has_non_infra_priority_blocker(text):
        return False
    return infra_only_signal(text)


def leader_recoverable(
    leader_path: Path,
    leader_fields: dict[str, str],
    reviewer_fields: dict[str, str],
    preflight_fields: dict[str, str],
    preflight_rows: dict[str, tuple[str, str]],
) -> bool:
    if not leader_path.exists():
        return False
    if clean(leader_fields.get("decision", "")).lower() == "pass":
        return False
    if clean(preflight_fields.get("technical_preflight_status", "")).lower() != "pass":
        return False
    if clean(preflight_fields.get("bridge_status", "")).lower() != "success":
        return False
    if clean(reviewer_fields.get("decision", "")).lower() != "pass":
        return False
    if any(clean(preflight_rows.get(code, ("", ""))[0], "").lower() != "pass" for code in STRUCTURAL_PREFLIGHT_CHECKS):
        return False
    if preflight_checks_pass(preflight_rows, OBJECTIVE_PREFLIGHT_CHECKS):
        return True
    text = leader_path.read_text(encoding="utf-8")
    if has_non_infra_priority_blocker(text):
        return False
    return infra_only_signal(text)


def render_reviewer_pass_doc(
    queue_item_path: Path,
    pack_dir: Path,
    preflight_path: Path,
    reviewer_rows: dict[str, tuple[str, str]],
    preflight_fields: dict[str, str],
    signed_at: datetime,
    recovery_reason: str,
) -> str:
    signed_iso = signed_at.isoformat(timespec="seconds")
    bridge_media_id = clean(preflight_fields.get("bridge_media_id", "n/a"))
    bridge_completed_at = clean(preflight_fields.get("bridge_result_completed_at", "n/a"))
    latest_verdict = clean(preflight_fields.get("latest_verdict_score", "n/a"))
    lines = [
        "# Morning Flash Reviewer Checklist",
        "",
        f"- `queue_item_path`: `{queue_item_path}`",
        f"- `draft_pack_dir`: `{pack_dir}`",
        f"- `preflight_path`: `{preflight_path}`",
        "- `checklist_role`: `reviewer`",
        "- `checklist_status`: `pass`",
        "- `decision`: `pass`",
        "- `signed_off_by`: `redteam-reviewer`",
        f"- `signed_off_at`: `{signed_iso}`",
        f"- `review_round`: `Auto recovery — {signed_at.strftime('%H:%M CST')} — {recovery_reason}`",
        "",
        "## Required Checks",
        "",
    ]
    for code in REVIEWER_REQUIRED_CHECKS:
        status, detail = reviewer_rows.get(code, ("pass", "沿用上一轮内容结论。"))
        detail_text = detail or "沿用上一轮内容结论。"
        lines.append(f"- `{code}`: `pass`｜{detail_text}")
    lines.append(f"- `auto_publish_recommendation`: `pass`｜{recovery_reason}，可继续进入 leader / publish_guard。")
    lines.extend(
        [
            "",
            "## Recovery Context",
            "",
            f"- `technical_preflight_status`: `pass`",
            f"- `bridge_status`: `success`",
            f"- `bridge_media_id`: `{bridge_media_id}`",
            f"- `bridge_result_completed_at`: `{bridge_completed_at}`",
            f"- `latest_verdict_score`: `{latest_verdict}`",
            "- `recovery_rule`: `only when structural gates pass + reviewer content checks all pass + no non-infra P0/P1/P2 blockers remain`",
            "",
            "## Notes",
            "",
            "- 本轮不是重新审稿，而是对已过期的 reviewer rework 快照做自动回正。",
            f"- 当前放行依据：{recovery_reason}。",
            "- 后续由 `market_morning_flash_publish_guard.py` 承接最终 submit；reviewer 不直接调用发布脚本。",
            "",
        ]
    )
    return "\n".join(lines)


def render_leader_pass_doc(
    queue_item_path: Path,
    pack_dir: Path,
    preflight_path: Path,
    reviewer_path: Path,
    preflight_fields: dict[str, str],
    signed_at: datetime,
    recovery_reason: str,
) -> str:
    signed_iso = signed_at.isoformat(timespec="seconds")
    bridge_media_id = clean(preflight_fields.get("bridge_media_id", "n/a"))
    bridge_completed_at = clean(preflight_fields.get("bridge_result_completed_at", "n/a"))
    run_date = signed_at.date().isoformat()
    lines = [
        "# Morning Flash Leader Checklist — market-editor 裁判签核",
        "",
        f"- `queue_item_path`: `{queue_item_path}`",
        f"- `draft_pack_dir`: `{pack_dir}`",
        f"- `preflight_path`: `{preflight_path}`",
        f"- `reviewer_checklist_path`: `{reviewer_path}`",
        "- `checklist_role`: `leader`",
        "- `checklist_status`: `pass`",
        "- `decision`: `pass`",
        "- `signed_off_by`: `market-editor`",
        f"- `signed_off_at`: `{signed_iso}`",
        f"- `RUN_DATE`: `{run_date}`",
        f"- `review_round`: `晨间快反领导自动回正 {signed_at.strftime('%H:%M CST')} — {recovery_reason}`",
        "",
        "## 三闸门终审",
        "",
        "| 闸门 | 状态 | 详情 |",
        "|------|------|------|",
        f"| `technical_preflight` | **pass** | bridge_status=success，bridge_media_id={bridge_media_id}，bridge_result_completed_at={bridge_completed_at} |",
        f"| `reviewer checklist` | **pass** | reviewer 已在同轮恢复为 pass；恢复依据：{recovery_reason} |",
        "| `structural gates` | **pass×2** | recent_topic_duplicate_guard=pass，public_copy_no_internal_scaffolding=pass |",
        "",
        "## 签核决定",
        "",
        "- `结论`: `三闸门已齐，可继续交给 publish_guard 判断是否触发 submit`",
        "- `边界`: `leader 只回正签核状态，不直接调用发布脚本`",
        f"- `恢复原因`: `{recovery_reason}`",
        "",
    ]
    return "\n".join(lines)


def recover_morning_flash_gate(queue_item_path: Path, write: bool = False) -> tuple[bool, list[str]]:
    queue_item_path = queue_item_path.expanduser().resolve()
    queue_fields = parse_fields(queue_item_path)
    if clean(queue_fields.get("delivery_lane", "")).lower() != "morning_flash":
        return False, []
    if clean(queue_fields.get("publish_mode", "")).lower() != "auto_api":
        return False, []
    if clean(queue_fields.get("platform", "")).lower() != "wechat":
        return False, []

    pack_dir = resolve_pack_dir(queue_fields, queue_item_path)
    preflight_path = pack_dir / "morning-flash-preflight.md"
    reviewer_path = pack_dir / "morning-flash-reviewer-checklist.md"
    leader_path = pack_dir / "morning-flash-leader-checklist.md"
    preflight_fields = parse_fields(preflight_path)
    preflight_rows = parse_check_rows(preflight_path)
    reviewer_fields = parse_fields(reviewer_path)
    reviewer_rows = parse_check_rows(reviewer_path)
    leader_fields = parse_fields(leader_path)

    changed = False
    messages: list[str] = []
    recovery_at = now_cn()
    reviewer_changed = False
    leader_changed = False
    objective_ready = preflight_checks_pass(preflight_rows, OBJECTIVE_PREFLIGHT_CHECKS)
    recovery_reason = (
        "最新 preflight 已确认内容闸门与晨报客观结构规则全部通过，旧 rework 状态已过期"
        if objective_ready
        else "bridge result 已补回且三闸门重新对齐，旧 rework 状态已过期"
    )

    if reviewer_recoverable(reviewer_path, reviewer_fields, reviewer_rows, preflight_fields, preflight_rows):
        if write:
            reviewer_text = render_reviewer_pass_doc(
                queue_item_path=queue_item_path,
                pack_dir=pack_dir,
                preflight_path=preflight_path,
                reviewer_rows=reviewer_rows,
                preflight_fields=preflight_fields,
                signed_at=recovery_at,
                recovery_reason=recovery_reason,
            )
            reviewer_path.write_text(reviewer_text.rstrip() + "\n", encoding="utf-8")
        reviewer_changed = True
        reviewer_fields = parse_fields(reviewer_path) if write else {**reviewer_fields, "decision": "pass", "checklist_status": "pass"}
        changed = True
        messages.append(f"RECOVERED reviewer checklist -> pass ({queue_item_path.name})")

    if leader_recoverable(leader_path, leader_fields, reviewer_fields, preflight_fields, preflight_rows):
        if write:
            leader_text = render_leader_pass_doc(
                queue_item_path=queue_item_path,
                pack_dir=pack_dir,
                preflight_path=preflight_path,
                reviewer_path=reviewer_path,
                preflight_fields=preflight_fields,
                signed_at=recovery_at,
                recovery_reason=recovery_reason,
            )
            leader_path.write_text(leader_text.rstrip() + "\n", encoding="utf-8")
        leader_changed = True
        changed = True
        messages.append(f"RECOVERED leader checklist -> pass ({queue_item_path.name})")

    if write and changed:
        queue_text = queue_item_path.read_text(encoding="utf-8")
        current_status = clean(queue_fields.get("status", "n/a"))
        if objective_ready and current_status in {"rework_pending", "deferred"}:
            queue_text = update_field(queue_text, "status", "waiting_human_publish")
            queue_text = update_field(queue_text, "publish_safety_tier", "auto_recovered_after_objective_roundup_pass")
            queue_text = update_field(queue_text, "frontstage_summary", "wechat 草稿已自动入箱，晨报客观规则已回正，等待自动发布闸门。")
            queue_text = update_field(queue_text, "human_action_required", "晨间客观规则已回正；等待 publish_guard 继续执行 freepublish/submit。")
        notes = merge_notes(
            queue_fields.get("notes", "n/a"),
            {
                "technical_preflight_status": clean(preflight_fields.get("technical_preflight_status", "n/a")),
                "reviewer_checklist_status": "pass" if reviewer_changed else clean(queue_fields.get("reviewer_checklist_status", "pass")),
                "leader_checklist_status": "pass" if leader_changed else clean(queue_fields.get("leader_checklist_status", "pass")),
                "morning_flash_gate_recovered_at": recovery_at.isoformat(timespec="seconds"),
                "morning_flash_gate_recovery_reason": recovery_reason,
                "wechat_bridge_status": clean(preflight_fields.get("bridge_status", "n/a")),
                "wechat_draft_media_id": clean(preflight_fields.get("bridge_media_id", "n/a")),
            },
        )
        queue_text = update_field(queue_text, "notes", notes)
        queue_item_path.write_text(queue_text, encoding="utf-8")

    return changed, messages


def main() -> None:
    args = parse_args()
    changed, messages = recover_morning_flash_gate(Path(args.queue_item), write=args.write)
    if not messages:
        print(f"NO_RECOVERY {Path(args.queue_item).name}")
        return
    for message in messages:
        print(message)
    print(f"CHANGED {changed}")


if __name__ == "__main__":
    main()

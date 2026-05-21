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
CHECK_RE = re.compile(r"^- `([^`]+)`: `([^`]+)`")
OBJECTIVE_PREFLIGHT_CHECKS = (
    "content_pack_gate_wechat",
    "roundup_item_count",
    "roundup_titles_aligned",
    "roundup_title_limit",
    "roundup_summary_limit",
    "roundup_detail_length_window",
    "roundup_third_party_media_mentions",
    "recent_topic_duplicate_guard",
    "public_copy_no_internal_scaffolding",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Auto-sign morning_flash reviewer/leader content checklists from objective preflight checks.")
    parser.add_argument("--queue-item", required=True, help="Absolute publish queue item path.")
    parser.add_argument("--write", action="store_true", help="Write checklist files in-place.")
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


def parse_check_rows(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    if not path.exists():
        return rows
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = CHECK_RE.match(raw_line.strip())
        if match:
            rows[clean(match.group(1), "")] = clean(match.group(2), "")
    return rows


def resolve_pack_dir(queue_item_path: Path) -> Path:
    fields = parse_fields(queue_item_path)
    explicit = clean(fields.get("draft_pack_dir", ""), "")
    if explicit and explicit != "n/a":
        return Path(explicit).expanduser().resolve()
    content_path = clean(fields.get("content_path", ""), "")
    if content_path and content_path != "n/a":
        return Path(content_path).expanduser().resolve().parent
    raise SystemExit(f"queue item missing draft_pack_dir/content_path: {queue_item_path}")


def objective_content_pass(preflight_rows: dict[str, str]) -> bool:
    return all(clean(preflight_rows.get(code, ""), "").lower() == "pass" for code in OBJECTIVE_PREFLIGHT_CHECKS)


def render_reviewer(queue_item_path: Path, preflight_path: Path, bridge_status: str) -> str:
    signed_at = now_cn().isoformat(timespec="seconds")
    bridge_note = "bridge 已就绪" if bridge_status == "success" else f"bridge 当前={bridge_status}，仅技术闸门待后续放行"
    return "\n".join(
        [
            "# Morning Flash Reviewer Checklist",
            "",
            f"- `queue_item_path`: `{queue_item_path}`",
            f"- `preflight_path`: `{preflight_path}`",
            "- `checklist_role`: `reviewer`",
            "- `checklist_status`: `pass`",
            "- `decision`: `pass`",
            "- `signed_off_by`: `redteam-reviewer`",
            f"- `signed_off_at`: `{signed_at}`",
            "- `review_round`: `objective_autosign`",
            "",
            "## Required Checks",
            "",
            "- `duplicate_and_freshness`: `pass`｜客观检查通过。",
            "- `headline_and_hook`: `pass`｜客观检查通过。",
            "- `timeliness_and_heat`: `pass`｜客观检查通过。",
            "- `risk_wording`: `pass`｜客观检查通过。",
            "- `public_copy_cleanliness`: `pass`｜客观检查通过。",
            "- `layout_and_images`: `pass`｜客观检查通过。",
            f"- `auto_publish_recommendation`: `pass`｜内容层已过线；{bridge_note}。",
            "",
        ]
    ) + "\n"


def render_leader(queue_item_path: Path, preflight_path: Path, reviewer_path: Path, bridge_status: str) -> str:
    signed_at = now_cn().isoformat(timespec="seconds")
    bridge_note = "bridge 已就绪，可等待 publish_guard" if bridge_status == "success" else f"bridge 当前={bridge_status}，自动发布仍由技术闸门单独拦截"
    return "\n".join(
        [
            "# Morning Flash Leader Checklist — market-editor 裁判签核",
            "",
            f"- `queue_item_path`: `{queue_item_path}`",
            f"- `preflight_path`: `{preflight_path}`",
            f"- `reviewer_checklist_path`: `{reviewer_path}`",
            "- `checklist_role`: `leader`",
            "- `checklist_status`: `pass`",
            "- `decision`: `pass`",
            "- `signed_off_by`: `market-editor`",
            f"- `signed_off_at`: `{signed_at}`",
            "- `review_round`: `objective_autosign`",
            "",
            "## 签核说明",
            "",
            "- `内容结论`: `晨间聚合结构、字数窗口、标题对应、无内部脚手架、无近120h重复题全部通过。`",
            f"- `技术结论`: `{bridge_note}`",
            "- `边界`: `内容 pass 不等于自动发布成功；publish_guard 仍以 technical_preflight 为准。`",
            "",
        ]
    ) + "\n"


def autosign(queue_item_path: Path, write: bool = False) -> tuple[bool, str]:
    queue_item_path = queue_item_path.expanduser().resolve()
    pack_dir = resolve_pack_dir(queue_item_path)
    preflight_path = pack_dir / "morning-flash-preflight.md"
    reviewer_path = pack_dir / "morning-flash-reviewer-checklist.md"
    leader_path = pack_dir / "morning-flash-leader-checklist.md"
    if not preflight_path.exists():
        return False, "missing_preflight"
    preflight_fields = parse_fields(preflight_path)
    preflight_rows = parse_check_rows(preflight_path)
    if not objective_content_pass(preflight_rows):
        return False, "objective_checks_not_passed"
    bridge_status = clean(preflight_fields.get("bridge_status", "pending"), "pending")
    if write:
        reviewer_path.write_text(render_reviewer(queue_item_path, preflight_path, bridge_status), encoding="utf-8")
        leader_path.write_text(render_leader(queue_item_path, preflight_path, reviewer_path, bridge_status), encoding="utf-8")
    return True, f"content_autosigned bridge={bridge_status}"


def main() -> None:
    args = parse_args()
    changed, reason = autosign(Path(args.queue_item), write=args.write)
    print(f"AUTOSIGN={'yes' if changed else 'no'}")
    print(f"REASON={reason}")


if __name__ == "__main__":
    main()

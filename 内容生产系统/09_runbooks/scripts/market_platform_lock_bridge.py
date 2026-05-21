#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import date, datetime
from pathlib import Path

from market_platform_task_sheet_to_approved import (
    TZ,
    existing_card_for,
    materialize_task_sheet,
    parse_task_sheet,
    persist_outputs,
    top5_board_path_for_sheet,
    top5_board_status_for_sheet,
)


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
TOPIC_DIR = ROOT / "03_topic_candidates"
SCORECARD_DIR = ROOT / "10_logs"
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
BOLD_KV_RE = re.compile(r"^- \*\*([^*]+)\*\*: ?`?(.*?)`?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bridge platform-task-sheet active slots into approved topics when downstream is allowed.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical date in YYYY-MM-DD.")
    parser.add_argument("--approved-by", default="market-editor")
    parser.add_argument(
        "--allow-day-mainline-auto-lock",
        action="store_true",
        help="Override the default founder-pick contract and allow day_mainline task-sheet slots to auto-materialize.",
    )
    parser.add_argument(
        "--allow-missing-top5-recovery",
        action="store_true",
        help="When continuity_only limited task sheet is valid, allow truthful same-day fallback materialization even if Top5 board is missing.",
    )
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def day_token(date_text: str) -> str:
    return date.fromisoformat(date_text).strftime("%Y%m%d")


def logical_approved_at(date_text: str) -> datetime:
    current_cn = datetime.now(TZ)
    logical_day = date.fromisoformat(date_text)
    return datetime(
        logical_day.year,
        logical_day.month,
        logical_day.day,
        current_cn.hour,
        current_cn.minute,
        current_cn.second,
        tzinfo=TZ,
    )


def clean(value: str, fallback: str = "") -> str:
    text = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return text if text else fallback


def parse_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        match = KV_RE.match(stripped) or BOLD_KV_RE.match(stripped)
        if match:
            fields[clean(match.group(1))] = clean(match.group(2))
    return fields


def normalize_gate_label(value: str) -> str:
    label = clean(value).lower()
    if "continuity_only" in label:
        return "continuity_only"
    if "stop_for_truth" in label:
        return "stop_for_truth"
    if label == "pass" or "premium_only" in label or "premium_pass" in label:
        return "premium_only"
    if label == "rework":
        return "rework"
    return label


def bridge_mode(scorecard_fields: dict[str, str]) -> tuple[str | None, str]:
    status = normalize_gate_label(scorecard_fields.get("status", ""))
    continuity_decision = normalize_gate_label(scorecard_fields.get("continuity_decision", ""))
    continuity_output = normalize_gate_label(scorecard_fields.get("continuity_output", ""))

    if continuity_decision == "stop_for_truth":
        return None, "platform scorecard stop_for_truth blocks downstream"
    if continuity_decision == "continuity_only" and continuity_output == "limited_task_sheet":
        return "continuity_active_only", "continuity_only limited task sheet may materialize active slots"
    if status == "pass" or continuity_decision == "premium_only":
        return "premium_all", "platform scorecard pass/premium_only allows full approved-topic materialization"
    return None, "platform scorecard has not opened any downstream lane yet"


def main() -> None:
    args = parse_args()
    token = day_token(args.date)
    task_sheet_path = TOPIC_DIR / f"{token}__platform-task-sheet.md"
    scorecard_path = SCORECARD_DIR / f"{token}__platform-task-sheet__stage-gate-scorecard.md"

    if not args.allow_day_mainline_auto_lock:
        print("BRIDGE_STATUS=blocked")
        print("REASON=day_mainline_now_requires_founder_pick_briefing; use market_day_mainline_briefing_builder.py + market_day_mainline_selection_apply.py")
        return

    if not task_sheet_path.exists():
        print("BRIDGE_STATUS=noop")
        print(f"MISSING_PATH={task_sheet_path}")
        return
    if not scorecard_path.exists():
        print("BRIDGE_STATUS=noop")
        print(f"MISSING_PATH={scorecard_path}")
        return

    sheet = parse_task_sheet(task_sheet_path)
    scorecard_fields = parse_fields(scorecard_path)
    selected_mode, reason = bridge_mode(scorecard_fields)
    if selected_mode is None:
        print("BRIDGE_STATUS=blocked")
        print(f"REASON={reason}")
        return

    top5_status = top5_board_status_for_sheet(sheet)
    allow_missing_top5_recovery = (
        args.allow_missing_top5_recovery
        and top5_status != "ready"
        and selected_mode == "continuity_active_only"
    )
    if top5_status != "ready" and not allow_missing_top5_recovery:
        print("BRIDGE_STATUS=blocked")
        print(f"REASON=top5_board_missing_or_unusable:{top5_board_path_for_sheet(sheet)}")
        return

    active_topic_keys = sorted(sheet.tasks_by_topic.keys())
    if not active_topic_keys:
        print("BRIDGE_STATUS=noop")
        print("REASON=no active task slots in platform task sheet")
        return

    existing_topic_keys = [topic_key for topic_key in active_topic_keys if existing_card_for(topic_key, sheet.date_token)]
    missing_topic_keys = [topic_key for topic_key in active_topic_keys if topic_key not in existing_topic_keys]

    print(f"ACTIVE_TOPIC_KEYS={','.join(active_topic_keys)}")
    print(f"EXISTING_APPROVED_TOPIC_KEYS={','.join(existing_topic_keys) if existing_topic_keys else 'none'}")
    print(f"MISSING_APPROVED_TOPIC_KEYS={','.join(missing_topic_keys) if missing_topic_keys else 'none'}")

    if not missing_topic_keys:
        print("BRIDGE_STATUS=noop")
        print("REASON=all active slots already materialized")
        return

    outputs, resolved_mode, _ = materialize_task_sheet(
        task_sheet_path=task_sheet_path,
        approved_by=args.approved_by,
        approved_at=logical_approved_at(args.date),
        materialization_mode=selected_mode,
        write=args.write,
        requested_topic_keys=missing_topic_keys,
        allow_missing_top5_recovery=allow_missing_top5_recovery,
    )

    if args.write:
        outputs, _, _ = persist_outputs(
            outputs=outputs,
            sheet=sheet,
            approved_by=args.approved_by,
            approved_at=logical_approved_at(args.date),
            task_sheet_path=task_sheet_path,
            materialization_mode=resolved_mode,
        )

    if allow_missing_top5_recovery:
        print("BRIDGE_RECOVERY_MODE=top5_missing_continuity_task_sheet")
    print("BRIDGE_STATUS=materialized" if args.write else "BRIDGE_STATUS=dry_run")
    print(f"MATERIALIZATION_MODE={resolved_mode}")
    print(f"REASON={reason}")
    print(f"APPROVED_TOPIC_COUNT={len(outputs)}")
    for _, path, _ in outputs:
        print(path)


if __name__ == "__main__":
    main()

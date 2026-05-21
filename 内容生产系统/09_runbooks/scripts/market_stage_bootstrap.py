#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
TEMPLATE_DIR = ROOT / "09_runbooks" / "templates"
TOPIC_DIR = ROOT / "03_topic_candidates"
LOG_DIR = ROOT / "10_logs"
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_LINE_RE = re.compile(r"^(\s*-\s*`([^`]+)`:)(.*)$")


@dataclass
class BootstrapTarget:
    path: Path
    template: Path
    fields: dict[str, str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap missing stage output files from market runbook templates.")
    parser.add_argument(
        "--stage",
        required=True,
        choices=[
            "top20_pack",
            "top20_redteam",
            "top20_score",
            "platform_task",
            "platform_redteam",
            "platform_score",
        ],
    )
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical date in YYYY-MM-DD.")
    parser.add_argument("--write", action="store_true", help="Create missing files in place.")
    return parser.parse_args()


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def day_token(date_text: str) -> str:
    return date.fromisoformat(date_text).strftime("%Y%m%d")


def render_template(template_text: str, fields: dict[str, str]) -> str:
    lines: list[str] = []
    for raw_line in template_text.splitlines():
        match = KV_LINE_RE.match(raw_line)
        if not match:
            lines.append(raw_line)
            continue
        prefix, key, _ = match.groups()
        if key not in fields:
            lines.append(raw_line)
            continue
        value = fields[key]
        if value:
            lines.append(f"{prefix} `{value}`")
        else:
            lines.append(f"{prefix}")
    return "\n".join(lines).rstrip() + "\n"


def targets_for(stage: str, requested_date: str) -> list[BootstrapTarget]:
    token = day_token(requested_date)
    generated_at = format_ts(now_cn())
    top20_pack = TOPIC_DIR / f"{token}__top20-screening-pack.md"
    top20_redteam = LOG_DIR / f"{token}__top20__redteam-review.md"
    top20_score = LOG_DIR / f"{token}__top20__stage-gate-scorecard.md"
    top20_score_mirror = TOPIC_DIR / f"{token}__top20-screening-pack__stage-gate-scorecard.md"
    platform_task = TOPIC_DIR / f"{token}__platform-task-sheet.md"
    platform_redteam = LOG_DIR / f"{token}__platform-task-sheet__redteam-review.md"
    platform_score = LOG_DIR / f"{token}__platform-task-sheet__stage-gate-scorecard.md"

    top20_pack_fields = {
        "date": requested_date,
        "generated_at": generated_at,
        "source_scope": "T-1 17:00 ~ T 14:30",
    }
    top20_redteam_fields = {
        "date": requested_date,
        "stage": "top20",
        "generated_at": generated_at,
        "review_target": str(top20_pack),
    }
    top20_score_fields = {
        "date": requested_date,
        "stage": "top20",
        "generated_at": generated_at,
        "delivery_pack": str(top20_pack),
        "redteam_review": str(top20_redteam),
    }
    platform_task_fields = {
        "date": requested_date,
        "generated_at": generated_at,
        "input_pack": str(top20_pack),
        "stage_gate_status": "drafting",
    }
    platform_redteam_fields = {
        "date": requested_date,
        "stage": "platform-task-sheet",
        "generated_at": generated_at,
        "review_target": str(platform_task),
    }
    platform_score_fields = {
        "date": requested_date,
        "stage": "platform-task-sheet",
        "generated_at": generated_at,
        "delivery_pack": str(platform_task),
        "redteam_review": str(platform_redteam),
    }

    mapping: dict[str, list[BootstrapTarget]] = {
        "top20_pack": [
            BootstrapTarget(
                path=top20_pack,
                template=TEMPLATE_DIR / "market_top20_screening_pack_template.md",
                fields=top20_pack_fields,
            )
        ],
        "top20_redteam": [
            BootstrapTarget(
                path=top20_redteam,
                template=TEMPLATE_DIR / "market_redteam_review_template.md",
                fields=top20_redteam_fields,
            )
        ],
        "top20_score": [
            BootstrapTarget(
                path=top20_score,
                template=TEMPLATE_DIR / "market_stage_gate_scorecard_template.md",
                fields=top20_score_fields,
            ),
            BootstrapTarget(
                path=top20_score_mirror,
                template=TEMPLATE_DIR / "market_stage_gate_scorecard_template.md",
                fields=top20_score_fields,
            ),
        ],
        "platform_task": [
            BootstrapTarget(
                path=platform_task,
                template=TEMPLATE_DIR / "market_platform_task_sheet_template.md",
                fields=platform_task_fields,
            )
        ],
        "platform_redteam": [
            BootstrapTarget(
                path=platform_redteam,
                template=TEMPLATE_DIR / "market_redteam_review_template.md",
                fields=platform_redteam_fields,
            )
        ],
        "platform_score": [
            BootstrapTarget(
                path=platform_score,
                template=TEMPLATE_DIR / "market_stage_gate_scorecard_template.md",
                fields=platform_score_fields,
            )
        ],
    }
    return mapping[stage]


def main() -> None:
    args = parse_args()
    targets = targets_for(args.stage, args.date)

    created = 0
    for target in targets:
        if target.path.exists():
            print(f"EXISTS\t{target.path}")
            continue
        rendered = render_template(target.template.read_text(encoding="utf-8"), target.fields)
        print(f"MISSING\t{target.path}")
        if not args.write:
            continue
        target.path.parent.mkdir(parents=True, exist_ok=True)
        target.path.write_text(rendered, encoding="utf-8")
        created += 1
        print(f"CREATED\t{target.path}")
    print(f"CREATED_COUNT={created}")


if __name__ == "__main__":
    main()

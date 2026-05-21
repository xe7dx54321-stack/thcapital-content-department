#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
BOARD_DIR = ROOT / "03_topic_candidates"
LOG_DIR = ROOT / "10_logs"


@dataclass
class RankedItem:
    rank: str
    candidate_key: str
    title: str
    note_a: str
    note_b: str


BRIEF_FIELD_RE = re.compile(r"^- `([^`]+)`: `([^`]*)`$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build topic radar execution log for TH Capital market content system")
    parser.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD")
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def day_token(date_text: str) -> str:
    return date.fromisoformat(date_text).strftime("%Y%m%d")


def parse_brief_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    if not path.exists():
        return fields
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = BRIEF_FIELD_RE.match(raw_line.strip())
        if not match:
            continue
        key, value = match.groups()
        fields[key] = value
    return fields


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_table_rows(lines: list[str], header: str) -> list[list[str]]:
    rows: list[list[str]] = []
    in_table = False
    for index, raw_line in enumerate(lines):
        line = raw_line.rstrip()
        if line.startswith(header):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.strip():
            if rows:
                break
            continue
        if not line.lstrip().startswith("|"):
            if rows:
                break
            continue
        row = split_row(line)
        if index > 0 and set("".join(row).replace("-", "").replace(" ", "")) == set():
            continue
        rows.append(row)
    if len(rows) >= 2:
        return rows[1:]
    return []


def parse_ranked_items(board_path: Path) -> tuple[list[RankedItem], list[RankedItem]]:
    if not board_path.exists():
        return [], []
    try:
        from market_approved_topic_builder import load_candidates

        candidates = load_candidates(board_path)
    except Exception:
        candidates = {}
    if candidates:
        top_items = [
            RankedItem(
                rank=str(candidate.rank),
                candidate_key=candidate.candidate_key,
                title=candidate.title,
                note_a=candidate.brand_fit_judgment,
                note_b=candidate.recommended_reason,
            )
            for _, candidate in sorted(candidates.items())
            if candidate.selection_bucket == "top5"
        ]
        holdout_items = [
            RankedItem(
                rank=str(candidate.rank),
                candidate_key=candidate.candidate_key,
                title=candidate.title,
                note_a=candidate.why_not_top5,
                note_b=candidate.why_it_made_top8,
            )
            for _, candidate in sorted(candidates.items())
            if candidate.selection_bucket == "holdout"
        ]
        return top_items, holdout_items
    lines = board_path.read_text(encoding="utf-8").splitlines()
    top_rows = parse_table_rows(lines, "## Top 5 Recommended")
    holdout_rows = parse_table_rows(lines, "## Holdout 3")

    top_items = [
        RankedItem(
            rank=row[0],
            candidate_key=row[1],
            title=row[2],
            note_a=row[4],
            note_b=row[5],
        )
        for row in top_rows
        if len(row) >= 6
    ]
    holdout_items = [
        RankedItem(
            rank=row[0],
            candidate_key=row[1],
            title=row[2],
            note_a=row[4],
            note_b=row[3],
        )
        for row in holdout_rows
        if len(row) >= 5
    ]
    return top_items, holdout_items


def build_founder_brief(top_items: list[RankedItem], holdout_items: list[RankedItem], board_path: Path, exec_log_path: Path) -> list[str]:
    lines = ["## Founder Brief Draft", ""]
    if top_items:
        top_preview = top_items[:2]
        lines.append("- 建议先拍板：")
        for item in top_preview:
            lines.append(f"  - Top {item.rank}｜{item.title} —— {item.note_b}")
    else:
        lines.append("- 今日强候选不足，建议先补源再拍板。")

    if holdout_items:
        holdout_titles = " / ".join(item.title for item in holdout_items[:3])
        lines.append(f"- 今日压下的 3 个：{holdout_titles}")
    else:
        lines.append("- 今日没有额外 holdout 候选。")

    lines.extend(
        [
            f"- 板子：`{board_path}`",
            f"- 执行日志：`{exec_log_path}`",
        ]
    )
    return lines


def build_execution_log(date_text: str) -> str:
    token = day_token(date_text)
    brief_path = LOG_DIR / f"{token}__market-topic-radar-brief.md"
    board_path = BOARD_DIR / f"{token}__daily-top8-to-top5.md"
    exec_log_path = LOG_DIR / f"{token}__market-topic-radar-execution.md"

    brief_fields = parse_brief_fields(brief_path)
    top_items, holdout_items = parse_ranked_items(board_path)
    supply_status = "full" if len(top_items) + len(holdout_items) >= 8 else "insufficient"

    lines = [
        "# 同行资本市场内容系统｜Topic Radar 执行日志",
        "",
        f"- `date`: `{date_text}`",
        f"- `brief_path`: `{brief_path}`",
        f"- `board_path`: `{board_path}`",
        f"- `source_packet_count`: `{brief_fields.get('source_packet_count', 'n/a')}`",
        f"- `asset_chain_count`: `{brief_fields.get('asset_chain_count', 'n/a')}`",
        f"- `topic_cluster_count`: `{brief_fields.get('topic_cluster_count', 'n/a')}`",
        f"- `top5_count`: `{len(top_items)}`",
        f"- `holdout_count`: `{len(holdout_items)}`",
        f"- `supply_status`: `{supply_status}`",
        "",
        "## Top 5 Snapshot",
    ]

    if top_items:
        for item in top_items:
            lines.append(
                f"- `Top {item.rank}` `{item.title}` | `brand_fit`: `{item.note_a}` | `why_now`: {item.note_b}"
            )
    else:
        lines.append("- `none`")

    lines.extend(["", "## Holdout Snapshot"])
    if holdout_items:
        for item in holdout_items:
            lines.append(
                f"- `Holdout {item.rank}` `{item.title}` | `why_not_top5`: {item.note_a} | `why_made_top8`: {item.note_b}"
            )
    else:
        lines.append("- `none`")

    lines.extend(
        [
            "",
            "## Founder Delivery Checklist",
            "",
            "- 对外只用简洁 plain text 汇报，不把内部侦察过程倒给老板",
            "- 默认只突出最值得先拍板的 1-2 个方向",
            "- 被压下的 3 个必须继续露出，便于老板手动捞回",
            "- 对外回报必须同时附板子路径与执行日志路径",
            "",
        ]
    )
    lines.extend(build_founder_brief(top_items, holdout_items, board_path, exec_log_path))
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    content = build_execution_log(args.date)
    if args.write:
        out_path = LOG_DIR / f"{day_token(args.date)}__market-topic-radar-execution.md"
        out_path.write_text(content, encoding="utf-8")
        print(out_path)
        return
    print(content, end="")


if __name__ == "__main__":
    main()

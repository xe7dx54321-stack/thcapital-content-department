#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
INTAKE_ROOT = ROOT / "12_public_intake_requests"
FRONTSTAGE_ROOT = ROOT / "11_frontstage"
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the public intake request board.")
    parser.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD")
    parser.add_argument("--intake-root", default=str(INTAKE_ROOT))
    parser.add_argument("--frontstage-root", default=str(FRONTSTAGE_ROOT))
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def clean(value: str, fallback: str = "") -> str:
    text = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return text if text else fallback


def compact(value: str, limit: int = 64) -> str:
    text = clean(value)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def parse_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def load_requests(intake_root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not intake_root.exists():
        return rows
    for path in sorted(intake_root.glob("*.md"), reverse=True):
        if path.name.lower() == "readme.md":
            continue
        fields = parse_fields(path)
        rows.append(
            {
                "request_id": clean(fields.get("request_id", path.stem)),
                "created_at": clean(fields.get("created_at", "")),
                "source_platform": clean(fields.get("source_platform", "unknown")),
                "source_channel": clean(fields.get("source_channel", "unknown")),
                "source_article_queue_key": clean(fields.get("source_article_queue_key", "n/a")),
                "requester_handle": clean(fields.get("requester_handle", "anonymous")),
                "normalized_request_type": clean(fields.get("normalized_request_type", "unknown_request")),
                "routed_department": clean(fields.get("routed_department", "founder_triage")),
                "classification_confidence": clean(fields.get("classification_confidence", "low")),
                "status": clean(fields.get("status", "pending_triage")),
                "priority_hint": clean(fields.get("priority_hint", "normal")),
                "normalized_brief": clean(fields.get("normalized_brief", path.stem)),
                "next_action": clean(fields.get("next_action", "manual follow-up")),
                "file": str(path),
            }
        )
    return rows


def render_markdown(rows: list[dict[str, str]], target_date: str) -> str:
    type_counter = Counter(row["normalized_request_type"] for row in rows)
    route_counter = Counter(row["routed_department"] for row in rows)
    status_counter = Counter(row["status"] for row in rows)
    now = datetime.now(CN_TZ).isoformat(timespec="seconds")

    lines = [
        "# market public intake board",
        "",
        f"- date: {target_date}",
        f"- updated_at: {now}",
        "- purpose: 把公众号留言 / 私信等外部输入先落成正式对象，形成后续内容、研究、项目、合作的统一入口。",
        "- mode: 第一阶段仅支持人工 / 半自动录入，不直接承诺实时自动抓取微信真实留言。",
        f"- total_requests: {len(rows)}",
        f"- pending_triage: {status_counter.get('pending_triage', 0)}",
        f"- queued_or_routed: {status_counter.get('queued', 0) + status_counter.get('routed', 0)}",
        f"- content_request: {type_counter.get('content_request', 0)}",
        f"- research_request: {type_counter.get('research_request', 0)}",
        f"- project_review_request: {type_counter.get('project_review_request', 0)}",
        f"- cooperation_request: {type_counter.get('cooperation_request', 0)}",
        "",
        "## By route",
        "",
    ]

    if route_counter:
        for route, count in sorted(route_counter.items()):
            lines.append(f"- `{route}`: `{count}`")
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Latest requests",
            "",
            "| request_id | type | route | status | priority | requester | source_article | brief | next_action | file |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )

    if rows:
        for row in rows[:20]:
            lines.append(
                f"| `{row['request_id']}` | `{row['normalized_request_type']}` | `{row['routed_department']}` | "
                f"`{row['status']}` | `{row['priority_hint']}` | `{compact(row['requester_handle'], 18)}` | "
                f"`{compact(row['source_article_queue_key'], 22)}` | `{compact(row['normalized_brief'], 48)}` | "
                f"`{compact(row['next_action'], 34)}` | `{row['file']}` |"
            )
    else:
        lines.append("| `-` | `-` | `-` | `-` | `-` | `-` | `-` | `none` | `-` | `-` |")

    lines.extend(
        [
            "",
            "## Rule",
            "",
            "- 这块当前是正式对象入口，不是自动客服系统；系统先保证“接得住”，再谈“自动吃得下”。",
            "- `content_request / research_request / project_review_request / cooperation_request` 是当前唯一正式分类，超出边界的输入先回 `founder_triage`。",
            "- 留言如果同时包含多个意图，第一阶段优先按主意图落一个对象，不追求一次性拆成多个工单。",
            "- 没有真实流量也照样保留这套对象，因为它是后续自动抓微信留言、接 bot、接网页抓取的统一契约。",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def snapshot(rows: list[dict[str, str]], target_date: str) -> dict[str, object]:
    return {
        "date": target_date,
        "updated_at": datetime.now(CN_TZ).isoformat(timespec="seconds"),
        "requests": rows[:50],
    }


def main() -> None:
    args = parse_args()
    intake_root = Path(args.intake_root).expanduser().resolve()
    frontstage_root = Path(args.frontstage_root).expanduser().resolve()
    rows = load_requests(intake_root)
    markdown = render_markdown(rows, args.date)
    payload = snapshot(rows, args.date)

    date_token = args.date.replace("-", "")
    board_path = frontstage_root / f"{date_token}__market-public-intake-board.md"
    snapshot_path = frontstage_root / f"{date_token}__market-public-intake-board.snapshot.json"

    if args.write:
        board_path.write_text(markdown, encoding="utf-8")
        snapshot_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(board_path)
    if not args.write:
        print(markdown)


if __name__ == "__main__":
    main()

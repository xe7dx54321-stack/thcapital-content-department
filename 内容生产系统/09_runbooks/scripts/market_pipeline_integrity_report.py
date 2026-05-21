#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from market_content_pack_truth import latest_content_pack_verdict


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
DRAFT_PACK_ROOT = ROOT / "05_draft_packs"
QUEUE_DIR = ROOT / "06_publish_queue"
LOG_DIR = ROOT / "10_logs"
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
ACTIVE_QUEUE_STATUSES = {"queued", "waiting_human_publish", "published"}


@dataclass(frozen=True)
class IntegrityIssue:
    kind: str
    topic_key: str
    current_status: str
    verdict_status: str
    verdict_score: str
    source_path: str
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report state drift between draft packs, publish queue items, and latest content-pack verdicts.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical date in YYYY-MM-DD.")
    parser.add_argument("--write", action="store_true", help="Write report into 10_logs.")
    return parser.parse_args()


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


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def day_token(date_text: str) -> str:
    return date.fromisoformat(date_text).strftime("%Y%m%d")


def topic_key_from_queue(fields: dict[str, str], path: Path) -> str:
    queue_key = clean(fields.get("queue_key", path.stem), "")
    if "__" in queue_key:
        return clean(queue_key.rsplit("__", 1)[0], path.stem)
    return clean(fields.get("topic_id", path.stem), path.stem)


def verdict_labels(topic_key: str) -> tuple[str, str]:
    verdict = latest_content_pack_verdict(topic_key)
    if verdict is None:
        return "missing", "n/a"
    return verdict.normalized_status, verdict.score_text or "n/a"


def draft_pack_issues() -> list[IntegrityIssue]:
    issues: list[IntegrityIssue] = []
    for path in sorted(DRAFT_PACK_ROOT.glob("*/00_draft-pack-card.md")):
        fields = parse_fields(path)
        topic_key = clean(fields.get("draft_key", path.parent.name))
        current_status = clean(fields.get("status", "n/a"))
        verdict = latest_content_pack_verdict(topic_key)
        verdict_status = verdict.normalized_status if verdict else "missing"
        verdict_score = verdict.score_text if verdict and verdict.score_text else "n/a"
        if current_status == "ready" and verdict is None:
            issues.append(
                IntegrityIssue(
                    kind="ready_without_scorecard",
                    topic_key=topic_key,
                    current_status=current_status,
                    verdict_status=verdict_status,
                    verdict_score=verdict_score,
                    source_path=str(path),
                    detail="draft pack 已是 ready，但还没有 content-pack stage-gate scorecard。",
                )
            )
        if current_status in {"ready", "queued", "waiting_human_publish", "published"} and verdict and verdict.requires_rework:
            issues.append(
                IntegrityIssue(
                    kind="pack_status_conflicts_with_rework",
                    topic_key=topic_key,
                    current_status=current_status,
                    verdict_status=verdict_status,
                    verdict_score=verdict_score,
                    source_path=str(path),
                    detail="draft pack 状态仍显示可发布路径，但最新 content-pack verdict 已是 rework。",
                )
            )
    return issues


def queue_issues() -> list[IntegrityIssue]:
    issues: list[IntegrityIssue] = []
    for path in sorted(QUEUE_DIR.glob("*__publish-queue-item.md")):
        fields = parse_fields(path)
        current_status = clean(fields.get("status", "n/a"))
        if current_status not in ACTIVE_QUEUE_STATUSES:
            continue
        topic_key = topic_key_from_queue(fields, path)
        platform = clean(fields.get("platform", "n/a"))
        verdict = latest_content_pack_verdict(topic_key)
        verdict_status = verdict.normalized_status if verdict else "missing"
        verdict_score = verdict.score_text if verdict and verdict.score_text else "n/a"
        if verdict and not verdict.allows_publish_queue_for(platform):
            if verdict.publish_ready_platforms:
                detail = (
                    f"publish queue item 仍处于活跃发布状态，但最新 content-pack verdict 不允许 `{platform}` 入队；"
                    f"当前允许平台：{','.join(verdict.publish_ready_platforms)}。"
                )
            else:
                detail = f"publish queue item 仍处于活跃发布状态，但最新 content-pack verdict 不允许 `{platform}` 入队。"
            issues.append(
                IntegrityIssue(
                    kind="queue_item_conflicts_with_verdict",
                    topic_key=topic_key,
                    current_status=current_status,
                    verdict_status=verdict_status,
                    verdict_score=verdict_score,
                    source_path=str(path),
                    detail=detail,
                )
            )
        if verdict is None and current_status in {"queued", "waiting_human_publish"}:
            issues.append(
                IntegrityIssue(
                    kind="queue_item_missing_scorecard",
                    topic_key=topic_key,
                    current_status=current_status,
                    verdict_status=verdict_status,
                    verdict_score=verdict_score,
                    source_path=str(path),
                    detail="publish queue item 已进入待发布状态，但找不到对应 content-pack scorecard。",
                )
            )
    return issues


def render_report(date_text: str, issues: list[IntegrityIssue]) -> str:
    lines = [
        "# Market Pipeline Integrity Report",
        "",
        f"- `date`: `{date_text}`",
        f"- `generated_at`: `{format_ts(now_cn())}`",
        f"- `issue_count`: `{len(issues)}`",
        "",
        "## Issues",
        "",
    ]
    if not issues:
        lines.append("- `none`")
        return "\n".join(lines).rstrip() + "\n"
    for idx, issue in enumerate(issues, start=1):
        lines.extend(
            [
                f"### {idx}. `{issue.topic_key}`",
                f"- `kind`: `{issue.kind}`",
                f"- `current_status`: `{issue.current_status}`",
                f"- `latest_verdict_status`: `{issue.verdict_status}`",
                f"- `latest_verdict_score`: `{issue.verdict_score}`",
                f"- `source_path`: `{issue.source_path}`",
                f"- `detail`: `{issue.detail}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    issues = draft_pack_issues() + queue_issues()
    issues.sort(key=lambda item: (item.kind, item.topic_key, item.source_path))
    rendered = render_report(args.date, issues)
    print(rendered)
    if args.write:
        path = LOG_DIR / f"{day_token(args.date)}__market-pipeline-integrity-report.md"
        path.write_text(rendered, encoding="utf-8")
        print(f"REPORT_PATH={path}")


if __name__ == "__main__":
    main()

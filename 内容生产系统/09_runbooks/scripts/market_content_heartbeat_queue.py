#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from market_content_pack_truth import ContentPackVerdict, latest_content_pack_verdict


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
APPROVED_DIR = ROOT / "04_approved_topics"
DRAFT_ROOT = ROOT / "05_draft_packs"
TOPIC_CANDIDATE_DIR = ROOT / "03_topic_candidates"
LOG_DIR = ROOT / "10_logs"
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
DONE_STATUSES = {"waiting_human_publish", "published", "reviewed"}
POLISH_SUPPORT_FILES = ["publish-readiness.md", "cover-visual-brief.md", "inline-visual-plan.md"]
TASK_SHEET_SECTION_HEADERS = {
    "## 六个主战场任务单",
    "## 三个最重要平台任务单",
}
STATUS_PRIORITY = {
    "needs_revision": 5,
    "drafting": 4,
    "draft_ready": 3,
    "ready": 2,
    "missing": 1,
}
HARD_DISABLE_DAY_MAINLINE_BACKLOG = True


@dataclass
class ApprovedTopic:
    path: Path
    topic_key: str
    requested_platforms: list[str]
    delivery_lane: str
    publish_mode: str
    delivery_deadline: str
    market_potential: str
    selected_rank: str
    approved_at: str
    status: str


@dataclass
class QueueItem:
    approved_topic_path: Path
    topic_key: str
    draft_pack_dir: Path
    selection_lane: str
    selection_reason: str
    current_status: str
    requested_platforms: list[str]
    missing_platforms: list[str]
    missing_support_files: list[str]
    suggested_actions: list[str]
    priority_score: int
    why_now: str
    approved_at: str
    delivery_lane: str
    publish_mode: str
    delivery_deadline: str
    verdict_status: str
    verdict_score: str
    verdict_lane: str
    score_gap_to_premium: str
    verdict_path: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Select a bounded work queue for content heartbeat runs.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical date in YYYY-MM-DD.")
    parser.add_argument("--limit", type=int, default=2, help="Maximum number of topics to queue.")
    parser.add_argument(
        "--allow-backlog",
        action="store_true",
        help="Explicitly allow historical backlog to fill unused capacity. By default this queue is same-day only.",
    )
    parser.add_argument("--write", action="store_true", help="Write queue snapshot into 10_logs.")
    return parser.parse_args()


def day_token(date_text: str) -> str:
    return date.fromisoformat(date_text).strftime("%Y%m%d")


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return value if value else fallback


def parse_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if not match:
            continue
        key, value = match.groups()
        fields[key] = clean(value)
    return fields


def split_platforms(raw: str) -> list[str]:
    if not raw or raw == "n/a":
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def extract_active_task_sheet_topic_keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    keys: set[str] = set()
    in_platform_tasks = False
    in_task_block = False
    task_heading_re = re.compile(r"^#### Task \d+(?:\s*(?:[（(]([^）)]+)[）)]|[—-]\s*(.+)))?$")
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line in TASK_SHEET_SECTION_HEADERS:
            in_platform_tasks = True
            in_task_block = False
            continue
        if in_platform_tasks and line.startswith("## ") and not line.startswith("## 六个主战场任务单"):
            break
        if not in_platform_tasks:
            continue
        if line.startswith("#### Task"):
            match = task_heading_re.match(line)
            label = clean((match.group(1) or match.group(2)), "") if match else ""
            in_task_block = not label or ("holdout" not in label.lower() and "不开启" not in label)
            continue
        if line.startswith("### "):
            in_task_block = False
            continue
        if not in_task_block:
            continue
        match = re.search(r"`topic_key`:\s*`([^`]+)`", line)
        if match:
            keys.add(clean(match.group(1), ""))
    return {key for key in keys if key}


def load_approved_topics(token: str) -> list[ApprovedTopic]:
    topics: list[ApprovedTopic] = []
    for path in sorted(APPROVED_DIR.glob("*__approved-topic.md")):
        fields = parse_fields(path)
        topics.append(
            ApprovedTopic(
                path=path,
                topic_key=clean(fields.get("topic_key", path.stem)),
                requested_platforms=split_platforms(fields.get("requested_platforms", "")),
                delivery_lane=clean(fields.get("delivery_lane", "day_mainline")),
                publish_mode=clean(fields.get("publish_mode", "draft_only")),
                delivery_deadline=clean(fields.get("delivery_deadline", "n/a")),
                market_potential=clean(fields.get("market_potential", "中")),
                selected_rank=clean(fields.get("selected_rank", "n/a")),
                approved_at=clean(fields.get("approved_at", "n/a")),
                status=clean(fields.get("status", "approved")),
            )
        )
    topics.sort(
        key=lambda item: (
            1 if item.path.name.startswith(f"{token}_") else 0,
            item.approved_at,
            item.topic_key,
        ),
        reverse=True,
    )
    return topics


def platform_file_expected(pack_dir: Path, platform: str) -> Path:
    return pack_dir / f"{platform}.md"


def card_status(card_fields: dict[str, str]) -> str:
    return clean(card_fields.get("status", "missing"))


def is_real_content(path: Path) -> bool:
    if not path.exists():
        return False
    content = path.read_text(encoding="utf-8").strip()
    return len(content) >= 80 and "TBD" not in content and "n/a" not in content


def market_potential_score(raw: str) -> int:
    value = clean(raw, "中")
    if "高" in value:
        return 20
    if "中" in value:
        return 10
    return 0


def selected_rank_boost(raw: str) -> int:
    value = clean(raw, "n/a")
    if not value.isdigit():
        return 0
    rank = int(value)
    if rank <= 1:
        return 35
    if rank == 2:
        return 25
    if rank == 3:
        return 18
    if rank <= 5:
        return 10
    return 0


def recency_boost(approved_at: str, requested_date: str) -> int:
    raw = clean(approved_at, "")
    if not raw:
        return 0
    try:
        approved_day = date.fromisoformat(raw[:10])
        target_day = date.fromisoformat(requested_date)
    except ValueError:
        return 0
    age = (target_day - approved_day).days
    if age <= 0:
        return 80
    if age == 1:
        return 50
    if age == 2:
        return 20
    return 0


def is_same_business_day_topic(topic: ApprovedTopic, token: str, requested_date: str) -> bool:
    if topic.path.name.startswith(f"{token}_"):
        return True
    return clean(topic.approved_at, "").startswith(requested_date)


def selection_lane_for(
    topic: ApprovedTopic,
    requested_date: str,
    token: str,
    active_task_topic_keys: set[str],
) -> tuple[str, str]:
    if active_task_topic_keys:
        if topic.topic_key in active_task_topic_keys:
            return ("today_mainline", "present in today's platform-task-sheet")
        if HARD_DISABLE_DAY_MAINLINE_BACKLOG:
            return ("historical_blocked", "excluded: not in today's platform-task-sheet")
        return ("inventory_backlog_fill", "historical inventory; not in today's platform-task-sheet")
    if is_same_business_day_topic(topic, token, requested_date):
        return ("today_mainline", "approved on the requested business day")
    if HARD_DISABLE_DAY_MAINLINE_BACKLOG:
        return ("historical_blocked", "excluded: outside requested business day")
    return (
        "inventory_backlog_fill",
        "historical inventory fallback because today's task sheet has no active approved topic",
    )


def verdict_status_label(verdict: ContentPackVerdict | None) -> str:
    if verdict is None:
        return "missing"
    return verdict.normalized_status


def verdict_score_label(verdict: ContentPackVerdict | None) -> str:
    if verdict is None:
        return "n/a"
    return verdict.score_text or "n/a"


def verdict_lane_label(verdict: ContentPackVerdict | None) -> str:
    if verdict is None:
        return "missing"
    return verdict.continuity_lane


def verdict_gap_label(verdict: ContentPackVerdict | None) -> str:
    if verdict is None or verdict.score_gap_to_premium is None:
        return "n/a"
    return f"{verdict.score_gap_to_premium:g}"


def verdict_path_label(verdict: ContentPackVerdict | None) -> str:
    if verdict is None:
        return "n/a"
    return str(verdict.path)


def queue_item_for(
    topic: ApprovedTopic,
    requested_date: str,
    selection_lane: str,
    selection_reason: str,
) -> QueueItem | None:
    pack_dir = DRAFT_ROOT / topic.topic_key
    card_path = pack_dir / "00_draft-pack-card.md"
    verdict = latest_content_pack_verdict(topic.topic_key)
    verdict_status = verdict_status_label(verdict)
    verdict_score = verdict_score_label(verdict)
    verdict_lane = verdict_lane_label(verdict)
    verdict_gap = verdict_gap_label(verdict)
    verdict_path = verdict_path_label(verdict)

    if not card_path.exists():
        actions = ["build_draft_pack", "write_requested_platform_drafts", "build_polish_assets"]
        score = (
            100
            + len(topic.requested_platforms) * 5
            + market_potential_score(topic.market_potential)
            + selected_rank_boost(topic.selected_rank)
            + recency_boost(topic.approved_at, requested_date)
        )
        return QueueItem(
            approved_topic_path=topic.path,
            topic_key=topic.topic_key,
            draft_pack_dir=pack_dir,
            selection_lane=selection_lane,
            selection_reason=selection_reason,
            current_status="missing",
            requested_platforms=topic.requested_platforms,
            missing_platforms=topic.requested_platforms[:],
            missing_support_files=POLISH_SUPPORT_FILES[:],
            suggested_actions=actions,
            priority_score=score,
            why_now="draft_pack card missing",
            approved_at=topic.approved_at,
            delivery_lane=topic.delivery_lane,
            publish_mode=topic.publish_mode,
            delivery_deadline=topic.delivery_deadline,
            verdict_status=verdict_status,
            verdict_score=verdict_score,
            verdict_lane=verdict_lane,
            score_gap_to_premium=verdict_gap,
            verdict_path=verdict_path,
        )

    card_fields = parse_fields(card_path)
    current_status = card_status(card_fields)
    if verdict and verdict.requires_rework:
        current_status = "needs_revision"
    if current_status in DONE_STATUSES and not (verdict and verdict.requires_rework):
        return None

    missing_platforms = [
        platform
        for platform in topic.requested_platforms
        if not is_real_content(platform_file_expected(pack_dir, platform))
    ]
    missing_support_files = [name for name in POLISH_SUPPORT_FILES if not (pack_dir / name).exists()]

    suggested_actions: list[str] = []
    score = (
        market_potential_score(topic.market_potential)
        + len(topic.requested_platforms) * 5
        + selected_rank_boost(topic.selected_rank)
        + recency_boost(topic.approved_at, requested_date)
    )
    why_parts: list[str] = []

    if verdict and verdict.requires_rework:
        score += 70 + verdict.revision_priority_boost
        suggested_actions.append("polish_and_revise")
        why_parts.append(f"latest_verdict=rework(score={verdict_score}, lane={verdict_lane})")
    elif verdict and verdict.allows_publish_queue:
        if current_status in {"queued", "waiting_human_publish", "published", "reviewed"}:
            return None
        if current_status == "ready" and not missing_platforms and not missing_support_files:
            return None
    elif verdict is None and current_status == "ready" and not missing_platforms and not missing_support_files:
        suggested_actions.append("request_stage_gate_review")
        score += 65
        why_parts.append("ready_without_content_pack_scorecard")
    elif verdict:
        score += verdict.revision_priority_boost
        why_parts.append(f"latest_verdict_lane={verdict_lane}")

    if current_status in {"drafting", "needs_revision", "draft_ready", "ready"}:
        score += {"needs_revision": 90, "drafting": 80, "draft_ready": 70, "ready": 40}.get(current_status, 30)
        why_parts.append(f"status={current_status}")

    if missing_platforms:
        suggested_actions.append("write_requested_platform_drafts")
        score += 25 + len(missing_platforms) * 4
        why_parts.append(f"missing_platforms={','.join(missing_platforms)}")

    if missing_support_files:
        suggested_actions.append("build_polish_assets")
        score += 20
        why_parts.append(f"missing_support={','.join(missing_support_files)}")

    if current_status in {"drafting", "needs_revision", "draft_ready"}:
        suggested_actions.append("polish_and_revise")

    if current_status == "ready" and not missing_platforms and not missing_support_files and verdict and verdict.allows_publish_queue:
        return None

    deduped_actions: list[str] = []
    for action in suggested_actions:
        if action not in deduped_actions:
            deduped_actions.append(action)

    if not deduped_actions:
        deduped_actions = ["inspect_manually"]
        why_parts.append("non-terminal status without clear missing files")

    return QueueItem(
        approved_topic_path=topic.path,
        topic_key=topic.topic_key,
        draft_pack_dir=pack_dir,
        selection_lane=selection_lane,
        selection_reason=selection_reason,
        current_status=current_status,
        requested_platforms=topic.requested_platforms,
        missing_platforms=missing_platforms,
        missing_support_files=missing_support_files,
        suggested_actions=deduped_actions,
        priority_score=score,
        why_now="; ".join(why_parts) if why_parts else "needs advancement",
        approved_at=topic.approved_at,
        delivery_lane=topic.delivery_lane,
        publish_mode=topic.publish_mode,
        delivery_deadline=topic.delivery_deadline,
        verdict_status=verdict_status,
        verdict_score=verdict_score,
        verdict_lane=verdict_lane,
        score_gap_to_premium=verdict_gap,
        verdict_path=verdict_path,
    )


def render_queue_section(title: str, items: list[QueueItem]) -> list[str]:
    lines = [f"### {title}", ""]
    if not items:
        lines.append("- none")
        lines.append("")
        return lines

    for idx, item in enumerate(items, start=1):
        lines.extend(
            [
                f"#### {idx}. `{item.topic_key}`",
                f"- `approved_topic_path`: `{item.approved_topic_path}`",
                f"- `draft_pack_dir`: `{item.draft_pack_dir}`",
                f"- `selection_lane`: `{item.selection_lane}`",
                f"- `selection_reason`: `{item.selection_reason}`",
                f"- `current_status`: `{item.current_status}`",
                f"- `approved_at`: `{item.approved_at}`",
                f"- `delivery_lane`: `{item.delivery_lane}`",
                f"- `publish_mode`: `{item.publish_mode}`",
                f"- `delivery_deadline`: `{item.delivery_deadline}`",
                f"- `requested_platforms`: `{', '.join(item.requested_platforms) if item.requested_platforms else 'n/a'}`",
                f"- `latest_verdict_status`: `{item.verdict_status}`",
                f"- `latest_verdict_score`: `{item.verdict_score}`",
                f"- `latest_verdict_lane`: `{item.verdict_lane}`",
                f"- `score_gap_to_premium`: `{item.score_gap_to_premium}`",
                f"- `latest_verdict_path`: `{item.verdict_path}`",
                f"- `missing_platforms`: `{', '.join(item.missing_platforms) if item.missing_platforms else 'none'}`",
                f"- `missing_support_files`: `{', '.join(item.missing_support_files) if item.missing_support_files else 'none'}`",
                f"- `suggested_actions`: `{', '.join(item.suggested_actions)}`",
                f"- `priority_score`: `{item.priority_score}`",
                f"- `why_now`: `{item.why_now}`",
                "",
            ]
        )
    return lines


def render_queue(
    requested_date: str,
    limit: int,
    allow_backlog: bool,
    task_sheet_path: Path,
    active_task_topic_keys: list[str],
    covered_active_keys: list[str],
    missing_active_keys: list[str],
    mainline_candidates: list[QueueItem],
    backlog_candidates: list[QueueItem],
    selected_mainline: list[QueueItem],
    selected_backlog: list[QueueItem],
) -> str:
    generated_at = format_ts(now_cn())
    lines = [
        "# Content Heartbeat Queue",
        "",
        f"- `date`: `{requested_date}`",
        f"- `generated_at`: `{generated_at}`",
        f"- `limit`: `{limit}`",
        f"- `target_count`: `{len(selected_mainline) + len(selected_backlog)}`",
        f"- `queue_policy`: `{'today_mainline first; backlog may fill unused capacity' if allow_backlog else 'today_mainline strict only; historical backlog hard-disabled'}`",
        "- `selection_guard`: `finish in-progress same-day items before opening new skeletons`",
        f"- `task_sheet_path`: `{task_sheet_path}`",
        f"- `active_task_topic_keys`: `{', '.join(active_task_topic_keys) if active_task_topic_keys else 'none'}`",
        f"- `active_task_keys_with_approved_topic`: `{', '.join(covered_active_keys) if covered_active_keys else 'none'}`",
        f"- `active_task_keys_missing_approved_topic`: `{', '.join(missing_active_keys) if missing_active_keys else 'none'}`",
        f"- `today_mainline_candidate_count`: `{len(mainline_candidates)}`",
        f"- `inventory_backlog_candidate_count`: `{len(backlog_candidates)}`",
        f"- `selected_today_mainline`: `{len(selected_mainline)}`",
        f"- `selected_backlog_fill`: `{len(selected_backlog)}`",
        "",
        "## Targets",
        "",
    ]
    if not selected_mainline and not selected_backlog:
        lines.append("- none")
        return "\n".join(lines).rstrip() + "\n"

    lines.extend(render_queue_section("Today Mainline", selected_mainline))
    lines.extend(render_queue_section("Backlog Continuity Fill", selected_backlog))
    return "\n".join(lines).rstrip() + "\n"


def status_priority(item: QueueItem) -> int:
    return STATUS_PRIORITY.get(item.current_status, 0)


def select_today_mainline(candidates: list[QueueItem], limit: int) -> list[QueueItem]:
    if limit <= 0:
        return []
    in_progress = [item for item in candidates if item.current_status != "missing"]
    if in_progress:
        return in_progress[:limit]
    return candidates[:limit]


def main() -> None:
    args = parse_args()
    effective_allow_backlog = False if HARD_DISABLE_DAY_MAINLINE_BACKLOG else args.allow_backlog
    token = day_token(args.date)
    task_sheet_path = TOPIC_CANDIDATE_DIR / f"{token}__platform-task-sheet.md"
    active_task_topic_keys = extract_active_task_sheet_topic_keys(task_sheet_path)
    topics = load_approved_topics(token)
    approved_topic_keys = {topic.topic_key for topic in topics}
    covered_active_keys = sorted(active_task_topic_keys & approved_topic_keys)
    missing_active_keys = sorted(active_task_topic_keys - approved_topic_keys)
    mainline_candidates: list[QueueItem] = []
    backlog_candidates: list[QueueItem] = []

    for topic in topics:
        if topic.delivery_lane != "day_mainline":
            continue
        selection_lane, selection_reason = selection_lane_for(topic, args.date, token, active_task_topic_keys)
        item = queue_item_for(topic, args.date, selection_lane, selection_reason)
        if item is None:
            continue
        if selection_lane == "today_mainline":
            mainline_candidates.append(item)
        elif selection_lane == "inventory_backlog_fill":
            backlog_candidates.append(item)

    mainline_candidates.sort(
        key=lambda item: (status_priority(item), item.priority_score, item.approved_at, item.topic_key),
        reverse=True,
    )
    backlog_candidates.sort(key=lambda item: (item.priority_score, item.approved_at, item.topic_key), reverse=True)

    selected_mainline = select_today_mainline(mainline_candidates, max(args.limit, 0))
    remaining_capacity = max(args.limit - len(selected_mainline), 0)
    selected_backlog = backlog_candidates[:remaining_capacity] if effective_allow_backlog else []
    rendered = render_queue(
        args.date,
        args.limit,
        effective_allow_backlog,
        task_sheet_path,
        sorted(active_task_topic_keys),
        covered_active_keys,
        missing_active_keys,
        mainline_candidates,
        backlog_candidates,
        selected_mainline,
        selected_backlog,
    )
    print(rendered)
    if args.write:
        path = LOG_DIR / f"{token}__content-heartbeat-queue.md"
        path.write_text(rendered, encoding="utf-8")
        print(f"QUEUE_PATH={path}")


if __name__ == "__main__":
    main()

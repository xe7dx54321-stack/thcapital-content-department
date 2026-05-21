#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from market_content_pack_truth import latest_content_pack_verdict
from market_top5_board_utils import top5_board_is_ready

ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
SOURCE_PACKET_DIR = ROOT / "02_topic_radar" / "source_packets"
ASSET_CHAIN_DIR = ROOT / "02_topic_radar" / "asset_chains"
TOPIC_CLUSTER_DIR = ROOT / "02_topic_radar" / "topic_clusters"
BOARD_DIR = ROOT / "03_topic_candidates"
APPROVED_DIR = ROOT / "04_approved_topics"
DRAFT_PACK_ROOT = ROOT / "05_draft_packs"
QUEUE_DIR = ROOT / "06_publish_queue"
REVIEW_DIR = ROOT / "07_performance_reviews"
LOG_DIR = ROOT / "10_logs"
FRONTSTAGE_DIR = ROOT / "11_frontstage"
ROLE_MATRIX_PATH = ROOT / "00_planning" / "20260326_内容工厂多Agent责任矩阵.md"

CN_TZ = ZoneInfo("Asia/Shanghai")
FRONTSTAGE_GROUP_ID = "oc_8e290d3f3b5215cab938fef7d0e4a860"
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
BUSINESS_WINDOW_START = "17:00"
BUSINESS_WINDOW_END = "14:30"


@dataclass
class ApprovedTopic:
    path: Path
    topic_id: str
    topic_key: str
    title: str
    requested_platforms: str
    status: str
    approved_angle: str
    approved_at: str
    selected_rank: str
    selection_bucket: str
    recommended_reason: str
    delivery_lane: str
    publish_mode: str
    source_board_path: str
    source_top5_board_path: str
    source_top5_board_status: str
    lock_truth: str
    selection_instruction: str


@dataclass
class CandidateDecision:
    bucket: str
    rank: str
    key: str
    title: str
    primary_reason: str
    note: str


@dataclass
class DraftPack:
    path: Path
    draft_key: str
    topic_id: str
    requested_platforms: str
    status: str
    created_at: str
    updated_at: str


@dataclass
class QueueItem:
    path: Path
    queue_id: str
    topic_id: str
    platform: str
    status: str
    publish_owner: str
    planned_publish_at: str
    actual_publish_at: str
    publish_url: str


@dataclass
class TopicTruth:
    topic: ApprovedTopic
    top5_backing_status: str
    lock_truth: str
    final_gate_status: str
    final_gate_note: str
    verdict_score: str


@dataclass
class TimelineEvent:
    ts: datetime
    label: str
    path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build frontstage board for TH Capital market content system")
    parser.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD")
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def format_hm(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%H:%M")


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


def list_daily_files(folder: Path, prefix: str, suffix: str) -> list[Path]:
    if not folder.exists():
        return []
    return sorted(
        [
            path
            for path in folder.iterdir()
            if path.is_file()
            and path.name.startswith(prefix)
            and path.name.endswith(suffix)
            and "template" not in path.name
        ]
    )


def parse_cst(raw: str) -> datetime | None:
    raw = clean(raw, "")
    if not raw:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S CST", "%Y-%m-%d %H:%M CST", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(raw, fmt).replace(tzinfo=CN_TZ)
        except ValueError:
            continue
    return None


def parse_hm(raw: str) -> time:
    hour, minute = [int(part) for part in raw.split(":", 1)]
    return time(hour=hour, minute=minute)


def business_window(date_text: str, start_hm: str = BUSINESS_WINDOW_START, end_hm: str = BUSINESS_WINDOW_END) -> tuple[datetime, datetime]:
    target_day = date.fromisoformat(date_text)
    start_day = target_day - timedelta(days=1)
    return (
        datetime.combine(start_day, parse_hm(start_hm), tzinfo=CN_TZ),
        datetime.combine(target_day, parse_hm(end_hm), tzinfo=CN_TZ),
    )


def packet_ts_from_name(path: Path) -> datetime | None:
    try:
        return datetime.strptime(path.name[:15], "%Y%m%d_%H%M%S").replace(tzinfo=CN_TZ)
    except ValueError:
        return None


def source_packet_ts(path: Path) -> datetime | None:
    fields = parse_fields(path)
    return parse_cst(fields.get("captured_at", "n/a")) or packet_ts_from_name(path)


def list_source_packets_in_business_window(date_text: str) -> list[Path]:
    if not SOURCE_PACKET_DIR.exists():
        return []
    start_dt, end_dt = business_window(date_text)
    items: list[Path] = []
    for path in SOURCE_PACKET_DIR.glob("*__source-packet.md"):
        ts = source_packet_ts(path)
        if ts and start_dt <= ts <= end_dt:
            items.append(path)
    return sorted(items)


def same_day(raw: str, date_text: str) -> bool:
    return clean(raw, "").startswith(date_text)


def load_approved_topics(token: str) -> list[ApprovedTopic]:
    topics: list[ApprovedTopic] = []
    for path in sorted(APPROVED_DIR.glob(f"{token}_*__approved-topic.md")):
        fields = parse_fields(path)
        topics.append(
            ApprovedTopic(
                path=path,
                topic_id=clean(fields.get("topic_id", path.stem)),
                topic_key=clean(fields.get("topic_key", path.stem)),
                title=clean(fields.get("title", path.stem)),
                requested_platforms=clean(fields.get("requested_platforms", "n/a")),
                status=clean(fields.get("status", "n/a")),
                approved_angle=clean(fields.get("approved_angle", "n/a")),
                approved_at=clean(fields.get("approved_at", "n/a")),
                selected_rank=clean(fields.get("selected_rank", "n/a")),
                selection_bucket=clean(fields.get("selection_bucket", "n/a")),
                recommended_reason=clean(fields.get("recommended_reason", "n/a")),
                delivery_lane=clean(fields.get("delivery_lane", "n/a")),
                publish_mode=clean(fields.get("publish_mode", "n/a")),
                source_board_path=clean(fields.get("source_board_path", "n/a")),
                source_top5_board_path=clean(fields.get("source_top5_board_path", "n/a")),
                source_top5_board_status=clean(fields.get("source_top5_board_status", "n/a")),
                lock_truth=clean(fields.get("lock_truth", "n/a")),
                selection_instruction=clean(fields.get("selection_instruction", "n/a")),
            )
        )
    return topics


def day_mainline_requires_top5(topic: ApprovedTopic) -> bool:
    return topic.delivery_lane in {"n/a", "day_mainline"}


def infer_top5_backing_status(topic: ApprovedTopic, token: str) -> str:
    explicit = clean(topic.source_top5_board_status, "")
    if explicit in {"ready", "missing", "not_required"}:
        return explicit
    if not day_mainline_requires_top5(topic):
        return "not_required"
    default_top5_path = BOARD_DIR / f"{token}__daily-top8-to-top5.md"
    source_top5_path = Path(topic.source_top5_board_path) if topic.source_top5_board_path != "n/a" else default_top5_path
    source_board_name = source_top5_path.name
    if source_board_name.endswith("__daily-top8-to-top5.md"):
        return "ready" if top5_board_is_ready(source_top5_path) else "missing"
    return "ready" if top5_board_is_ready(default_top5_path) else "missing"


def infer_lock_truth(topic: ApprovedTopic, token: str) -> str:
    explicit = clean(topic.lock_truth, "")
    if explicit and explicit != "n/a":
        return explicit
    top5_status = infer_top5_backing_status(topic, token)
    if not day_mainline_requires_top5(topic):
        return "explicit_lane_lock"
    if "continuity" in topic.selection_bucket:
        return "fallback_top5_backed" if top5_status == "ready" else "fallback_task_sheet_only"
    source_board_name = Path(topic.source_board_path).name if topic.source_board_path != "n/a" else ""
    if source_board_name.endswith("__daily-top8-to-top5.md"):
        return "manual_top5_lock"
    return "premium_top5_backed" if top5_status == "ready" else "task_sheet_only_without_top5"


def build_queue_items_by_topic_id(queue_items: list[QueueItem]) -> dict[str, list[QueueItem]]:
    grouped: dict[str, list[QueueItem]] = {}
    for item in queue_items:
        grouped.setdefault(item.topic_id, []).append(item)
    return grouped


def infer_final_gate_status(topic: ApprovedTopic, topic_queue_items: list[QueueItem]) -> tuple[str, str, str]:
    verdict = latest_content_pack_verdict(topic.topic_key)
    published = any(
        item.status == "published"
        or (item.publish_url not in {"n/a", ""} and not item.publish_url.startswith("wechat-draft://"))
        or item.actual_publish_at not in {"n/a", ""}
        for item in topic_queue_items
    )
    if published:
        return "published", "已发布或已回填真实 publish 信息。", verdict.score_text if verdict else "n/a"
    if verdict is None:
        if any(item.status in {"queued", "waiting_human_publish"} for item in topic_queue_items):
            return "queue_active_without_final_gate", "已进入发布队列，但前台缺少可核验的 content-pack 最终门信息。", "n/a"
        return "not_at_final_gate", "尚未进入 content-pack 最终放行门。", "n/a"
    if verdict.allows_publish_queue:
        return "premium_publish_ready", "已通过 content-pack publish-ready 终门。", verdict.score_text or "n/a"
    if verdict.publish_ready_platforms:
        platforms = ", ".join(verdict.publish_ready_platforms)
        return "platform_partial_publishable", f"仅部分平台达到可发布状态：{platforms}。", verdict.score_text or "n/a"
    if verdict.requires_rework:
        return "blocked_final_gate", "最新 content-pack verdict 为 rework，仍被最终放行门阻断。", verdict.score_text or "n/a"
    return "reviewed_not_publish_ready", "已有 content-pack 评分，但尚未达到 publish-ready。", verdict.score_text or "n/a"


def build_topic_truths(approved_topics: list[ApprovedTopic], queue_items_all: list[QueueItem], token: str) -> list[TopicTruth]:
    queue_by_topic_id = build_queue_items_by_topic_id(queue_items_all)
    truths: list[TopicTruth] = []
    for topic in approved_topics:
        final_gate_status, final_gate_note, verdict_score = infer_final_gate_status(
            topic,
            queue_by_topic_id.get(topic.topic_id, []),
        )
        truths.append(
            TopicTruth(
                topic=topic,
                top5_backing_status=infer_top5_backing_status(topic, token),
                lock_truth=infer_lock_truth(topic, token),
                final_gate_status=final_gate_status,
                final_gate_note=final_gate_note,
                verdict_score=verdict_score,
            )
        )
    return truths


def extract_active_task_sheet_topic_keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    keys: set[str] = set()
    in_platform_tasks = False
    in_task_block = False
    task_heading_re = re.compile(r"^#### Task \d+(?:[（(]([^）)]+)[）)])?$")
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## 六个主战场任务单"):
            in_platform_tasks = True
            in_task_block = False
            continue
        if in_platform_tasks and line.startswith("## ") and not line.startswith("## 六个主战场任务单"):
            break
        if not in_platform_tasks:
            continue
        if line.startswith("#### Task"):
            match = task_heading_re.match(line)
            label = clean(match.group(1), "") if match else ""
            in_task_block = not label or ("holdout" not in label.lower() and "不开启" not in label)
            continue
        if line.startswith("### "):
            in_task_block = False
            continue
        if in_task_block:
            match = re.search(r"`topic_key`:\s*`([^`]+)`", line)
            if match:
                keys.add(clean(match.group(1), ""))
    return {clean(key, "") for key in keys if clean(key, "")}


def load_draft_packs(
    date_text: str,
    today_topic_ids: set[str],
    active_topic_keys: set[str] | None = None,
) -> tuple[list[DraftPack], list[DraftPack]]:
    today_items: list[DraftPack] = []
    active_items: list[DraftPack] = []
    if not DRAFT_PACK_ROOT.exists():
        return today_items, active_items

    tracked_topic_ids = {clean(topic_id, "") for topic_id in today_topic_ids if clean(topic_id, "")}
    tracked_topic_keys = {clean(topic_key, "") for topic_key in (active_topic_keys or set()) if clean(topic_key, "")}
    tracked = bool(tracked_topic_ids or tracked_topic_keys)

    for path in sorted(DRAFT_PACK_ROOT.glob("*/00_draft-pack-card.md")):
        fields = parse_fields(path)
        item = DraftPack(
            path=path,
            draft_key=clean(fields.get("draft_key", path.parent.name)),
            topic_id=clean(fields.get("topic_id", "n/a")),
            requested_platforms=clean(fields.get("requested_platforms", "n/a")),
            status=clean(fields.get("status", "n/a")),
            created_at=clean(fields.get("created_at", "n/a")),
            updated_at=clean(fields.get("updated_at", "n/a")),
        )
        is_current_topic = item.topic_id in tracked_topic_ids or item.draft_key in tracked_topic_keys
        if item.status not in {"published", "cancelled"} and (not tracked or is_current_topic):
            active_items.append(item)
        if tracked:
            if is_current_topic:
                today_items.append(item)
        elif same_day(item.created_at, date_text) or same_day(item.updated_at, date_text) or item.topic_id in tracked_topic_ids:
            today_items.append(item)

    return today_items, active_items


def load_queue_items(token: str | None = None) -> list[QueueItem]:
    items: list[QueueItem] = []
    pattern = f"{token}_*__publish-queue-item.md" if token else "*__publish-queue-item.md"
    for path in sorted(QUEUE_DIR.glob(pattern)):
        fields = parse_fields(path)
        items.append(
            QueueItem(
                path=path,
                queue_id=clean(fields.get("queue_id", path.stem)),
                topic_id=clean(fields.get("topic_id", "n/a")),
                platform=clean(fields.get("platform", "n/a")),
                status=clean(fields.get("status", "n/a")),
                publish_owner=clean(fields.get("publish_owner", "n/a")),
                planned_publish_at=clean(fields.get("planned_publish_at", "n/a")),
                actual_publish_at=clean(fields.get("actual_publish_at", "n/a")),
                publish_url=clean(fields.get("publish_url", "n/a")),
            )
        )
    return items


def parse_table_rows(lines: list[str], header: str) -> list[list[str]]:
    rows: list[list[str]] = []
    in_table = False
    for raw_line in lines:
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
        row = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if set("".join(row).replace("-", "").replace(" ", "")) == set():
            continue
        rows.append(row)
    if len(rows) >= 2:
        return rows[1:]
    return []


def parse_top_titles(board_path: Path) -> list[str]:
    if not board_path.exists():
        return []
    try:
        from market_approved_topic_builder import load_candidates

        candidates = load_candidates(board_path)
    except Exception:
        candidates = {}
    if candidates:
        return [
            clean(candidate.title, "n/a")
            for _, candidate in sorted(candidates.items())
            if candidate.selection_bucket == "top5"
        ]
    lines = board_path.read_text(encoding="utf-8").splitlines()
    rows = parse_table_rows(lines, "## Top 5 Recommended")
    if not rows:
        rows = parse_table_rows(lines, "## Top 5 推荐")
    titles: list[str] = []
    for row in rows:
        if len(row) >= 3:
            titles.append(clean(row[2], "n/a"))
    return titles


def load_candidate_decisions(board_path: Path) -> tuple[list[CandidateDecision], list[CandidateDecision]]:
    if not board_path.exists():
        return [], []
    try:
        from market_approved_topic_builder import load_candidates

        candidates = load_candidates(board_path)
    except Exception:
        candidates = {}
    if candidates:
        top_decisions = [
            CandidateDecision(
                bucket="top5",
                rank=str(candidate.rank),
                key=clean(candidate.candidate_key, "n/a"),
                title=clean(candidate.title, "n/a"),
                primary_reason=clean(candidate.recommended_reason, "n/a"),
                note=clean(candidate.owner_note, "n/a"),
            )
            for _, candidate in sorted(candidates.items())
            if candidate.selection_bucket == "top5"
        ]
        holdout_decisions = [
            CandidateDecision(
                bucket="holdout",
                rank=str(candidate.rank),
                key=clean(candidate.candidate_key, "n/a"),
                title=clean(candidate.title, "n/a"),
                primary_reason=clean(candidate.why_not_top5, "n/a"),
                note=clean(candidate.why_it_made_top8, "n/a"),
            )
            for _, candidate in sorted(candidates.items())
            if candidate.selection_bucket == "holdout"
        ]
        return top_decisions, holdout_decisions
    lines = board_path.read_text(encoding="utf-8").splitlines()
    top_rows = parse_table_rows(lines, "## Top 5 推荐") or parse_table_rows(lines, "## Top 5 Recommended")
    holdout_rows = parse_table_rows(lines, "## Holdout 3")

    top_decisions: list[CandidateDecision] = []
    for row in top_rows:
        if len(row) < 7:
            continue
        top_decisions.append(
            CandidateDecision(
                bucket="top5",
                rank=clean(row[0], "n/a"),
                key=clean(row[1], "n/a"),
                title=clean(row[2], "n/a"),
                primary_reason=clean(row[5], "n/a"),
                note=clean(row[6], "n/a"),
            )
        )

    holdout_decisions: list[CandidateDecision] = []
    for row in holdout_rows:
        if len(row) < 7:
            continue
        holdout_decisions.append(
            CandidateDecision(
                bucket="holdout",
                rank=clean(row[0], "n/a"),
                key=clean(row[1], "n/a"),
                title=clean(row[2], "n/a"),
                primary_reason=clean(row[4], "n/a"),
                note=clean(row[6], "n/a"),
            )
        )

    return top_decisions, holdout_decisions


def topic_display(topic_id: str, topic_lookup: dict[str, str]) -> str:
    return topic_lookup.get(topic_id, topic_id)


def queue_item_is_dirty(item: QueueItem) -> bool:
    dirty_tokens = {"n/a", "", "none"}
    return (
        clean(item.topic_id, "").lower() in dirty_tokens
        or clean(item.queue_id, "").lower() in dirty_tokens
    )


def day_mainline_unbacked_truths(topic_truths: list[TopicTruth]) -> list[TopicTruth]:
    return [
        truth
        for truth in topic_truths
        if day_mainline_requires_top5(truth.topic) and truth.top5_backing_status != "ready"
    ]


def premium_ready_truths(topic_truths: list[TopicTruth]) -> list[TopicTruth]:
    return [truth for truth in topic_truths if truth.final_gate_status in {"published", "premium_publish_ready"}]


def blocked_final_gate_truths(topic_truths: list[TopicTruth]) -> list[TopicTruth]:
    return [
        truth
        for truth in topic_truths
        if truth.final_gate_status in {"blocked_final_gate", "platform_partial_publishable", "queue_active_without_final_gate"}
    ]


def infer_formal_tasks(
    source_packet_count: int,
    board_exists: bool,
    approved_topics: list[ApprovedTopic],
    topic_truths: list[TopicTruth],
    active_draft_packs: list[DraftPack],
    waiting_publish_items: list[QueueItem],
    topic_lookup: dict[str, str],
    active_task_topic_keys: list[str],
) -> list[str]:
    tasks: list[str] = []
    unbacked_truths = day_mainline_unbacked_truths(topic_truths)
    blocked_truths = blocked_final_gate_truths(topic_truths)
    premium_truths = premium_ready_truths(topic_truths)

    if unbacked_truths:
        preview = ", ".join(truth.topic.topic_key for truth in unbacked_truths[:3])
        tasks.append(f"补齐今日 `Top 8 -> Top 5` 正式建议板；当前 `{preview}` 属于间接锁题，不应视为自治闭环。")

    if approved_topics and not premium_truths:
        blocked_preview = ", ".join(truth.topic.topic_key for truth in blocked_truths[:3]) if blocked_truths else "当前已拍板对象"
        tasks.append(f"优先把 `{blocked_preview}` 推过 content-pack 最终放行门，而不是继续新增对象。")

    if active_task_topic_keys and not approved_topics and not active_draft_packs:
        preview = ", ".join(active_task_topic_keys[:3])
        tasks.append(f"把今日 task sheet 已下发主线 `{preview}` 推进成正式 Draft Pack。")
    elif not board_exists:
        if source_packet_count > 0:
            tasks.append("把今日 radar 输入收束成正式 `Top 8 -> Top 5` 建议单。")
        else:
            tasks.append("补齐今日内容源供给，避免内容工厂空转。")

    for topic in approved_topics:
        if topic.status in {"drafting", "approved"}:
            tasks.append(f"把 `{topic.topic_key}` 从已拍板题推进到可编辑 Draft Pack。")

    for pack in active_draft_packs:
        if pack.status == "drafting":
            tasks.append(f"完成 `{pack.draft_key}` 的 Draft Pack 起草。")
        elif pack.status == "needs_revision":
            tasks.append(f"继续打磨 `{pack.draft_key}`，把它推进到 `ready`。")
        elif pack.status == "ready":
            tasks.append(f"把 `{pack.draft_key}` 推进到 publish queue。")

    if waiting_publish_items:
        grouped: dict[str, list[str]] = {}
        for item in waiting_publish_items:
            grouped.setdefault(item.topic_id, []).append(item.platform)
        for topic_id, platforms in grouped.items():
            tasks.append(f"`{topic_display(topic_id, topic_lookup)}` 已进入待人工发布，待处理平台：{', '.join(sorted(platforms))}。")

    if not tasks:
        tasks.append("当前主链路已跑通，继续保持补源、选题与待发布状态可见。")
    return dedupe(tasks)


def infer_current_focus(
    board_exists: bool,
    top_titles: list[str],
    approved_topics: list[ApprovedTopic],
    topic_truths: list[TopicTruth],
    active_draft_packs: list[DraftPack],
    waiting_publish_items: list[QueueItem],
    source_packet_count: int,
    topic_lookup: dict[str, str],
    active_task_topic_keys: list[str],
) -> list[str]:
    unbacked_truths = day_mainline_unbacked_truths(topic_truths)
    blocked_truths = blocked_final_gate_truths(topic_truths)
    if unbacked_truths:
        lines = []
        for truth in unbacked_truths[:3]:
            lines.append(
                f"当前实际在修复 `{truth.topic.topic_key}` 的锁题真相：{truth.lock_truth}，缺少 Top5 正式背书。"
            )
        return lines
    if blocked_truths:
        lines = []
        for truth in blocked_truths[:3]:
            lines.append(
                f"当前实际在把 `{truth.topic.topic_key}` 推过最终放行门：{truth.final_gate_note}"
            )
        return lines

    if active_task_topic_keys:
        ready_packs = [pack for pack in active_draft_packs if pack.status in {"ready", "needs_revision", "drafting"}]
        if ready_packs:
            lines = []
            for pack in ready_packs[:3]:
                lines.append(f"当前实际在推进 `{pack.draft_key}`，状态 `{pack.status}`。")
            return lines
        preview = "、".join(active_task_topic_keys[:3])
        return [f"当前实际主线仍是今日 task sheet 已下发对象：`{preview}`。"]

    if waiting_publish_items:
        grouped: dict[str, list[str]] = {}
        for item in waiting_publish_items:
            grouped.setdefault(item.topic_id, []).append(item.platform)
        lines = []
        for topic_id, platforms in sorted(grouped.items()):
            lines.append(f"当前实际在盯 `{topic_display(topic_id, topic_lookup)}` 的人工发布闭环，平台：{', '.join(sorted(platforms))}。")
        return lines

    ready_packs = [pack for pack in active_draft_packs if pack.status in {"ready", "needs_revision", "drafting"}]
    if ready_packs:
        lines = []
        for pack in ready_packs[:3]:
            lines.append(f"当前实际在推进 `{pack.draft_key}`，状态 `{pack.status}`。")
        return lines

    if approved_topics:
        return [f"当前实际在把已拍板题推进成正式稿件，最新题目是 `{approved_topics[-1].topic_key}`。"]

    if board_exists and top_titles:
        return [f"当前实际在等待老板从今日 Top 候选中拍板，最值得优先看的方向是：{top_titles[0]}。"]

    if source_packet_count > 0:
        return ["当前实际在收束今日素材供给，为正式 Top 5 建议单做准备。"]

    return ["当前没有足够有效供给，实际工作重点转为补源与校正 watchlist。"]


def build_stage_results(
    source_packet_count: int,
    asset_chain_count: int,
    topic_cluster_count: int,
    board_exists: bool,
    board_path: Path,
    top_titles: list[str],
    approved_topics: list[ApprovedTopic],
    topic_truths: list[TopicTruth],
    today_draft_packs: list[DraftPack],
    queue_items: list[QueueItem],
    dirty_waiting_publish_count: int,
    active_task_topic_keys: list[str],
) -> list[str]:
    unbacked_truths = day_mainline_unbacked_truths(topic_truths)
    premium_truths = premium_ready_truths(topic_truths)
    blocked_truths = blocked_final_gate_truths(topic_truths)
    lines = [
        f"今日新增 `source packet` {source_packet_count} 份、`asset chain` {asset_chain_count} 份、`topic cluster` {topic_cluster_count} 份。"
    ]
    if board_exists:
        preview = " / ".join(top_titles[:2]) if top_titles else "候选已收束"
        lines.append(f"今日选题建议板已形成：`{board_path}`；优先关注：{preview}。")
    else:
        lines.append("今日正式 `Top 8 -> Top 5` 建议板尚未形成。")
    if active_task_topic_keys and not approved_topics:
        lines.append(f"今日 task sheet 已下发主线 {len(active_task_topic_keys)} 个：{', '.join(active_task_topic_keys[:3])}。")

    if approved_topics:
        lines.append(f"今日新增 `approved_topic` {len(approved_topics)} 个：{', '.join(topic.topic_key for topic in approved_topics[:4])}。")
        if unbacked_truths:
            lines.append(f"其中 `day_mainline` 对象有 {len(unbacked_truths)} 个缺少 Top5 正式背书。")
        if premium_truths:
            lines.append(f"当前已有 {len(premium_truths)} 个对象通过最终 publish-ready 放行门。")
        else:
            lines.append("当前仍无任何对象通过最终 publish-ready 放行门。")
        if blocked_truths:
            lines.append(f"当前有 {len(blocked_truths)} 个对象被最终放行门阻断或仅部分平台可发。")
    if today_draft_packs:
        lines.append(f"今日推进中的 Draft Pack {len(today_draft_packs)} 个：{', '.join(pack.draft_key for pack in today_draft_packs[:4])}。")
    waiting = [item for item in queue_items if item.status == 'waiting_human_publish']
    if waiting:
        lines.append(f"当前已有 {len(waiting)} 个发布队列项进入 `waiting_human_publish`。")
    if dirty_waiting_publish_count:
        lines.append(f"发布队列中另有 {dirty_waiting_publish_count} 个脏对象待清理，不应计入正常待发布任务。")
    return lines


def build_role_boundary_lines() -> list[str]:
    return [
        "对外只保留 `market-editor` 这一个前台 bot；老板不直接和后台 agent 交互。",
        "后台正式角色为 `market-scout`（按 `signal-scout` 语义运行）、`topic-planner`、`content-writer`、`redteam-reviewer`、`publish-ops`、`content-analyst`；全部独立 workspace / session 运行，且不允许越级回报。",
        f"正式角色职责矩阵见：`{ROLE_MATRIX_PATH}`。",
    ]


def build_decision_digest(
    top_decisions: list[CandidateDecision],
    holdout_decisions: list[CandidateDecision],
    topic_truths: list[TopicTruth],
) -> list[str]:
    lines: list[str] = []

    for item in top_decisions[:3]:
        lines.append(f"入围 `{item.key}`：{item.title}｜原因：{item.primary_reason}。")

    for item in holdout_decisions[:2]:
        lines.append(f"暂放 `{item.key}`：{item.title}｜原因：{item.primary_reason}；捞回条件：{item.note}。")

    for truth in topic_truths[:3]:
        item = truth.topic
        if truth.top5_backing_status == "missing" and day_mainline_requires_top5(item):
            lines.append(
                f"已锁 `{item.topic_key}`：当前来自间接锁题（{truth.lock_truth}），当日 Top5 正式建议板仍缺失，不应视为自治完成。"
            )
        elif item.selection_bucket == "holdout":
            lines.append(
                f"已拍板 `{item.topic_key}`：这是一次 holdout 捞回（原序号 `{item.selected_rank}`），当前归一角度为“{item.approved_angle}”。"
            )
        else:
            lines.append(
                f"已拍板 `{item.topic_key}`：来自 Top 候选序号 `{item.selected_rank}`，推荐原因是：{item.recommended_reason}。"
            )

    return dedupe(lines) or ["今日还没有形成可解释的选题决策。"]


def build_light_approval_summary(
    board_exists: bool,
    approved_topics: list[ApprovedTopic],
    topic_truths: list[TopicTruth],
    waiting_publish_items: list[QueueItem],
    published_items: list[QueueItem],
    review_count_today: int,
    dirty_waiting_publish_count: int,
    topic_lookup: dict[str, str],
) -> list[str]:
    lines: list[str] = []
    unbacked_truths = day_mainline_unbacked_truths(topic_truths)
    blocked_truths = blocked_final_gate_truths(topic_truths)
    premium_truths = premium_ready_truths(topic_truths)

    if board_exists and not approved_topics:
        lines.append("待拍板：今日 `Top 8 -> Top 5` 已形成，下一步只需要确认题号 / 角度 / 平台。")

    if unbacked_truths:
        for truth in unbacked_truths[:3]:
            lines.append(f"锁题真相待补：`{truth.topic.topic_key}` 缺少 Top5 正式背书，当前为 `{truth.lock_truth}`。")

    if approved_topics:
        drafting_like = [item for item in approved_topics if item.status in {"approved", "drafting", "draft_ready"}]
        for item in drafting_like[:3]:
            lines.append(f"已拍板待推进：`{item.topic_key}`，下一步应进入 Draft Pack / polish。")
    if blocked_truths:
        for truth in blocked_truths[:3]:
            lines.append(
                f"最终放行受阻：`{truth.topic.topic_key}`｜{truth.final_gate_note}｜score={truth.verdict_score}。"
            )
    elif approved_topics and not premium_truths:
        lines.append("注意：今日已有 approved-topic，但仍无任何对象通过最终 publish-ready 放行门。")

    if waiting_publish_items:
        grouped: dict[str, list[str]] = {}
        for item in waiting_publish_items:
            grouped.setdefault(item.topic_id, []).append(item.platform)
        for topic_id, platforms in sorted(grouped.items()):
            lines.append(
                f"待人工发布：`{topic_display(topic_id, topic_lookup)}`，平台 `{', '.join(sorted(platforms))}`。"
            )
    if dirty_waiting_publish_count:
        lines.append(f"队列清洁：当前有 {dirty_waiting_publish_count} 个 `n/a` 脏发布对象，需从发布主板剥离。")

    if published_items and review_count_today == 0:
        lines.append("待复盘：已有内容发布，但今日尚未生成 review skeleton。")

    if not lines:
        lines.append("当前没有新的拍板 / 发布提醒堆积。")
    return dedupe(lines)


def build_automation_boundary_lines() -> list[str]:
    return [
        "自动化负责：抓源、补查、收束候选、起稿、打磨、排版 handoff、排队提醒。",
        "人工负责：选题确认、最终发布、真实链接回填、效果数据回填。",
        "浏览器自动化只允许做无 API 平台的兜底发稿 / 截图验收，不允许成为主链决策中心。",
    ]


def build_active_pool(
    topic_truths: list[TopicTruth],
    active_draft_packs: list[DraftPack],
    queue_items: list[QueueItem],
) -> list[str]:
    lines: list[str] = []
    for truth in topic_truths:
        topic = truth.topic
        lines.append(
            f"`{topic.topic_key}` | `approved_topic` | `{topic.status}` | `lock={truth.lock_truth}` | `final_gate={truth.final_gate_status}` | `{topic.path}`"
        )
    for pack in active_draft_packs[:8]:
        lines.append(f"`{pack.draft_key}` | `draft_pack` | `{pack.status}` | `{pack.path}`")
    for item in queue_items:
        if item.status in {"queued", "waiting_human_publish", "published"}:
            lines.append(f"`{item.queue_id}` | `publish_queue` | `{item.status}` | `{item.path}`")
    return dedupe(lines) or ["`none`"]


def build_next_actions(
    board_exists: bool,
    approved_topics: list[ApprovedTopic],
    topic_truths: list[TopicTruth],
    active_draft_packs: list[DraftPack],
    waiting_publish_items: list[QueueItem],
    active_task_topic_keys: list[str],
) -> list[str]:
    plans: list[str] = []
    if day_mainline_unbacked_truths(topic_truths):
        plans.append("先补齐今日 Top5 正式建议板，避免 approved-topic 继续脱离正式锁题链。")
    if approved_topics and not premium_ready_truths(topic_truths):
        plans.append("先把已拍板对象推进到 content-pack 最终放行门，再谈今晚交付。")
    if active_task_topic_keys and not active_draft_packs:
        plans.append("先把 task sheet 已下发主线推进成 Draft Pack，再进入 polish。")
    elif not board_exists:
        plans.append("先把今日建议单补齐，再进入选题拍板。")
    if approved_topics and not active_draft_packs:
        plans.append("把已拍板题推进成 Draft Pack。")
    if any(pack.status == "drafting" for pack in active_draft_packs):
        plans.append("完成起草中的平台稿，把状态推进到 `ready`。")
    if any(pack.status == "needs_revision" for pack in active_draft_packs):
        plans.append("继续打磨 `needs_revision` 稿件，补强 hook、背景桥接与平台适配。")
    if waiting_publish_items:
        plans.append("等人工发布后，补 publish URL，并开始 24h review。")
    if not plans:
        plans.append("继续维持补源 -> 选题 -> 起稿 -> 待发布 的主链稳定运行。")
    return dedupe(plans)


def build_human_assist(
    waiting_publish_items: list[QueueItem],
    board_exists: bool,
    approved_topics: list[ApprovedTopic],
    topic_truths: list[TopicTruth],
    dirty_waiting_publish_count: int,
    supply_status: str,
    topic_lookup: dict[str, str],
) -> list[str]:
    needs: list[str] = []
    if not board_exists and not approved_topics:
        needs.append("若要继续推进成稿，需先拍板今日选题。")
    elif day_mainline_unbacked_truths(topic_truths):
        needs.append("今日 Top5 正式建议板缺失；当前 approved-topic 仍含间接锁题对象，需先补齐锁题真相。")
    if approved_topics and not premium_ready_truths(topic_truths):
        needs.append("今日虽已有 approved-topic，但仍无对象通过最终 publish-ready 放行门，不应按已交付理解。")
    if dirty_waiting_publish_count:
        needs.append(f"发布队列里存在 {dirty_waiting_publish_count} 个 `n/a` 脏对象，需清理后再作为正式运营看板使用。")
    if supply_status == "insufficient":
        needs.append("今日强候选供给不足，建议补充更强热点源或允许从 holdout 手动捞回。")
    if waiting_publish_items:
        grouped: dict[str, list[str]] = {}
        for item in waiting_publish_items:
            grouped.setdefault(item.topic_id, []).append(item.platform)
        for topic_id, platforms in sorted(grouped.items()):
            needs.append(f"`{topic_display(topic_id, topic_lookup)}` 等待人工发布，平台：{', '.join(sorted(platforms))}。")
    if not needs:
        needs.append("暂时无。")
    return needs


def describe_event(path: Path) -> str:
    name = path.name
    if name.endswith("__market-frontstage-sync-execution.md"):
        return "同步前台群关键节点"
    if name.endswith("__market-topic-capture-summary.md"):
        return "完成一轮 source capture"
    if name.endswith("__market-asset-derivation-summary.md"):
        return "完成一轮对象一跳派生"
    if name.endswith("__market-asset-query-resolution-summary.md"):
        return "完成一轮弱链补查"
    if name.endswith("__market-topic-radar-brief.md"):
        return "更新 Topic Radar brief"
    if name.endswith("__market-topic-radar-execution.md"):
        return "更新 Topic Radar execution"
    if name.endswith("__daily-top8-to-top5.md"):
        return "形成今日 Top 8 -> Top 5 建议板"
    if name.endswith("__approved-topic.md"):
        return "新增 approved topic"
    if name.endswith("__draft-pack-execution.md"):
        return "推进 Draft Pack"
    if name.endswith("__content-polish-execution.md"):
        return "推进内容打磨"
    if name.endswith("__publish-queue-execution.md"):
        return "推进发布队列"
    if name.endswith("__performance-review-execution.md"):
        return "推进内容复盘"
    return "更新内容工厂对象"


def build_timeline(date_text: str, token: str, board_path: Path) -> list[TimelineEvent]:
    candidates: list[Path] = []
    for suffix in [
        "__market-frontstage-sync-execution.md",
        "__market-topic-capture-summary.md",
        "__market-asset-derivation-summary.md",
        "__market-asset-query-resolution-summary.md",
        "__market-topic-radar-brief.md",
        "__market-topic-radar-execution.md",
        "__topic-approval-execution.md",
        "__draft-pack-execution.md",
        "__content-polish-execution.md",
        "__publish-queue-execution.md",
        "__performance-review-execution.md",
    ]:
        candidates.extend(list(LOG_DIR.glob(f"{token}*{suffix}")))
    candidates.extend(list(APPROVED_DIR.glob(f"{token}_*__approved-topic.md")))
    if board_path.exists():
        candidates.append(board_path)

    events: list[TimelineEvent] = []
    for path in candidates:
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=CN_TZ)
        if mtime.strftime("%Y-%m-%d") != date_text:
            continue
        events.append(TimelineEvent(ts=mtime, label=describe_event(path), path=path))
    events.sort(key=lambda item: item.ts, reverse=True)
    return events[:18]


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def build_group_sync_draft(
    formal_tasks: list[str],
    current_focus: list[str],
    decision_digest: list[str],
    stage_results: list[str],
    approval_summary: list[str],
    next_actions: list[str],
    human_assist: list[str],
    board_path: Path,
) -> list[str]:
    lines = [
        "内容工厂状态已更新。",
        "",
        "当前正式任务：",
    ]
    for index, task in enumerate(formal_tasks[:4], start=1):
        lines.append(f"{index}. {task}")

    lines.extend(["", "当前实际在做："])
    for item in current_focus[:3]:
        lines.append(f"- {item}")

    lines.extend(["", "关键决策："])
    for item in decision_digest[:3]:
        lines.append(f"- {item}")

    lines.extend(["", "阶段性成果："])
    for item in stage_results[:4]:
        lines.append(f"- {item}")

    lines.extend(["", "轻审批提醒："])
    for item in approval_summary[:3]:
        lines.append(f"- {item}")

    lines.extend(["", "下一阶段计划："])
    for item in next_actions[:3]:
        lines.append(f"- {item}")

    lines.extend(["", "需要人类协助："])
    for item in human_assist[:3]:
        lines.append(f"- {item}")

    lines.extend(["", f"状态板：`{board_path}`"])
    return lines


def build_board(date_text: str) -> str:
    token = day_token(date_text)
    board_path = FRONTSTAGE_DIR / f"{token}__market-frontstage-board.md"
    radar_board_path = BOARD_DIR / f"{token}__daily-top8-to-top5.md"
    radar_exec_path = LOG_DIR / f"{token}__market-topic-radar-execution.md"
    start_dt, end_dt = business_window(date_text)

    source_packets = list_source_packets_in_business_window(date_text)
    asset_chains = list_daily_files(ASSET_CHAIN_DIR, token, "__asset-chain.md")
    topic_clusters = list_daily_files(TOPIC_CLUSTER_DIR, token, "__topic-cluster.md")
    approved_topics = load_approved_topics(token)
    today_topic_ids = {topic.topic_id for topic in approved_topics}
    topic_lookup = {topic.topic_id: topic.topic_key for topic in approved_topics}
    platform_task_sheet_path = BOARD_DIR / f"{token}__platform-task-sheet.md"
    active_task_topic_keys = sorted(extract_active_task_sheet_topic_keys(platform_task_sheet_path))
    today_draft_packs, active_draft_packs = load_draft_packs(date_text, today_topic_ids, set(active_task_topic_keys))
    queue_items_today = load_queue_items(token)
    queue_items_all = load_queue_items()
    topic_truths = build_topic_truths(approved_topics, queue_items_all, token)
    waiting_publish_items_all = [item for item in queue_items_all if item.status == "waiting_human_publish"]
    dirty_waiting_publish_items = [item for item in waiting_publish_items_all if queue_item_is_dirty(item)]
    waiting_publish_items = [item for item in waiting_publish_items_all if not queue_item_is_dirty(item)]
    published_items = [item for item in queue_items_today if item.status == "published"]
    review_files = list_daily_files(REVIEW_DIR, token, "-review.md")
    top_titles = parse_top_titles(radar_board_path)
    top_decisions, holdout_decisions = load_candidate_decisions(radar_board_path)
    board_exists = top5_board_is_ready(radar_board_path)
    radar_exec_fields = parse_fields(radar_exec_path)
    supply_status = clean(radar_exec_fields.get("supply_status", "n/a"))

    formal_tasks = infer_formal_tasks(
        len(source_packets),
        board_exists,
        approved_topics,
        topic_truths,
        active_draft_packs,
        waiting_publish_items,
        topic_lookup,
        active_task_topic_keys,
    )
    current_focus = infer_current_focus(
        board_exists,
        top_titles,
        approved_topics,
        topic_truths,
        active_draft_packs,
        waiting_publish_items,
        len(source_packets),
        topic_lookup,
        active_task_topic_keys,
    )
    stage_results = build_stage_results(
        len(source_packets),
        len(asset_chains),
        len(topic_clusters),
        board_exists,
        radar_board_path,
        top_titles,
        approved_topics,
        topic_truths,
        today_draft_packs,
        waiting_publish_items,
        len(dirty_waiting_publish_items),
        active_task_topic_keys,
    )
    role_boundary = build_role_boundary_lines()
    decision_digest = build_decision_digest(top_decisions, holdout_decisions, topic_truths)
    active_pool = build_active_pool(topic_truths, active_draft_packs, queue_items_today)
    approval_summary = build_light_approval_summary(
        board_exists,
        approved_topics,
        topic_truths,
        waiting_publish_items,
        published_items,
        len(review_files),
        len(dirty_waiting_publish_items),
        topic_lookup,
    )
    next_actions = build_next_actions(
        board_exists,
        approved_topics,
        topic_truths,
        active_draft_packs,
        waiting_publish_items,
        active_task_topic_keys,
    )
    automation_boundary = build_automation_boundary_lines()
    human_assist = build_human_assist(
        waiting_publish_items,
        board_exists,
        approved_topics,
        topic_truths,
        len(dirty_waiting_publish_items),
        supply_status,
        topic_lookup,
    )
    day_mainline_unbacked_count = len(day_mainline_unbacked_truths(topic_truths))
    premium_ready_count = len(premium_ready_truths(topic_truths))
    blocked_final_gate_count = len(blocked_final_gate_truths(topic_truths))
    timeline = build_timeline(date_text, token, radar_board_path)
    group_sync_draft = build_group_sync_draft(
        formal_tasks,
        current_focus,
        decision_digest,
        stage_results,
        approval_summary,
        next_actions,
        human_assist,
        board_path,
    )

    lines = [
        "# Market Frontstage Board",
        "",
        f"- `date`: `{date_text}`",
        f"- `generated_at`: `{format_ts(now_cn())}`",
        f"- `frontstage_group_id`: `{FRONTSTAGE_GROUP_ID}`",
        f"- `board_path`: `{board_path}`",
        "",
        "## Snapshot",
        "",
        f"- `source_packets_business_day`: `{len(source_packets)}`",
        f"- `source_packet_window`: `{start_dt.strftime('%Y-%m-%d %H:%M')} → {end_dt.strftime('%Y-%m-%d %H:%M')} CST`",
        f"- `asset_chains_today`: `{len(asset_chains)}`",
        f"- `topic_clusters_today`: `{len(topic_clusters)}`",
        f"- `top5_board_status`: `{'ready' if board_exists else 'missing'}`",
        f"- `approved_topics_today`: `{len(approved_topics)}`",
        f"- `day_mainline_approved_topics_without_top5_backing`: `{day_mainline_unbacked_count}`",
        f"- `active_draft_packs`: `{len(active_draft_packs)}`",
        f"- `premium_publish_ready_topics_today`: `{premium_ready_count}`",
        f"- `blocked_final_gate_topics_today`: `{blocked_final_gate_count}`",
        f"- `waiting_human_publish_items`: `{len(waiting_publish_items)}`",
        f"- `dirty_waiting_publish_items`: `{len(dirty_waiting_publish_items)}`",
        f"- `published_items_today`: `{len(published_items)}`",
        "",
        "## 当前正式任务",
        "",
    ]

    for item in formal_tasks:
        lines.append(f"- {item}")

    lines.extend(["", "## 当前实际在做", ""])
    for item in current_focus:
        lines.append(f"- {item}")

    lines.extend(["", "## 组织边界", ""])
    for item in role_boundary:
        lines.append(f"- {item}")

    lines.extend(["", "## 关键决策与原因", ""])
    for item in decision_digest:
        lines.append(f"- {item}")

    lines.extend(["", "## 今日阶段性成果", ""])
    for item in stage_results:
        lines.append(f"- {item}")

    lines.extend(["", "## 当前活跃对象池", ""])
    for item in active_pool:
        lines.append(f"- {item}")

    lines.extend(["", "## 轻审批与提醒", ""])
    for item in approval_summary:
        lines.append(f"- {item}")

    lines.extend(["", "## 下一阶段计划", ""])
    for item in next_actions:
        lines.append(f"- {item}")

    lines.extend(["", "## 自动化边界", ""])
    for item in automation_boundary:
        lines.append(f"- {item}")

    lines.extend(["", "## 人类协助", ""])
    for item in human_assist:
        lines.append(f"- {item}")

    lines.extend(["", "## 今日日志时间线", ""])
    if timeline:
        for event in timeline:
            lines.append(f"- `{format_hm(event.ts)}` {event.label} | `{event.path}`")
    else:
        lines.append("- `none`")

    lines.extend(["", "## 群同步草稿", ""])
    lines.extend(group_sync_draft)

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    content = build_board(args.date)
    if args.write:
        out_path = FRONTSTAGE_DIR / f"{day_token(args.date)}__market-frontstage-board.md"
        out_path.write_text(content, encoding="utf-8")
        print(out_path)
        return
    print(content, end="")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from market_content_pack_truth import latest_content_pack_verdict
from market_content_hygiene_guard import inspect_content_hygiene


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
DEFAULT_QUEUE_ROOT = ROOT / "06_publish_queue"
DEFAULT_WECHAT_BRIDGE_OUTBOX = ROOT / "07_wechat_bridge_outbox"
WECHAT_BRIDGE_ENQUEUE_SCRIPT = ROOT / "09_runbooks" / "scripts" / "market_wechat_bridge_enqueue.py"
WECHAT_BRIDGE_RECONCILE_SCRIPT = ROOT / "09_runbooks" / "scripts" / "market_wechat_bridge_reconcile.py"
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
TIMESTAMP_TOKEN_RE = re.compile(r"(\d{8}_\d{6})")
DEFAULT_WECHAT_BRIDGE_WAIT_SECONDS = 180
WECHAT_BRIDGE_POLL_SECONDS = 3
CARD_FILE_FIELDS = {
    "wechat_path": "wechat.md",
    "xiaohongshu_path": "xiaohongshu.md",
    "zhihu_path": "zhihu.md",
    "x_path": "x.md",
    "bilibili_path": "bilibili.md",
    "toutiao_path": "toutiao.md",
    "baijiahao_path": "baijiahao.md",
    "title_options_path": "title-options.md",
    "summary_options_path": "summary-options.md",
    "opening_hook_options_path": "opening-hook-options.md",
    "cta_mode_path": "cta-mode.md",
    "packaging_bundle_path": "packaging-bundle.md",
    "context_bridge_path": "context-bridge-notes.md",
    "audience_notes_path": "audience-notes.md",
    "render_plan_path": "platform-render-plan.md",
    "citation_block_path": "citation-block.md",
    "visual_notes_path": "visual-notes.md",
    "inline_visual_plan_path": "inline-visual-plan.md",
    "revision_notes_path": "revision-notes.md",
}


@dataclass
class DraftPack:
    pack_dir: Path
    card_path: Path
    draft_id: str
    draft_key: str
    topic_id: str
    approved_topic_path: str
    requested_platforms: list[str]
    delivery_lane: str
    publish_mode: str
    delivery_deadline: str
    selection_scope: str
    business_window_start: str
    business_window_end: str
    status: str
    paths: dict[str, str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build publish queue items for TH Capital market content system")
    parser.add_argument("--draft-pack-dir", required=True, help="Draft pack directory path")
    parser.add_argument("--status", choices=["queued", "waiting_human_publish", "published", "deferred", "cancelled"], required=True)
    parser.add_argument("--platform", action="append", default=[], help="Target platform(s)")
    parser.add_argument("--publish-owner", default="老板")
    parser.add_argument(
        "--publish-safety-tier",
        choices=["premium_publish_ready", "fallback_publish_safe", "n/a"],
        default="n/a",
        help="Truthful publish safety tier written into queue item; defaults to inferred verdict truth.",
    )
    parser.add_argument("--planned-publish-at", default="")
    parser.add_argument("--actual-publish-at", default="")
    parser.add_argument("--publish-url", default="")
    parser.add_argument("--notes", default="")
    parser.add_argument("--queue-root", default=str(DEFAULT_QUEUE_ROOT))
    parser.add_argument("--wechat-bridge-wait-seconds", type=int, default=DEFAULT_WECHAT_BRIDGE_WAIT_SECONDS)
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value).strip().strip("`")
    return value if value else fallback


def split_platforms(raw: str) -> list[str]:
    if not raw or raw == "n/a":
        return []
    return [clean(item, "") for item in raw.split(",") if clean(item, "")]


def resolve_doc_path(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path
    return ROOT / raw_path


def hydrate_pack_paths(pack_dir: Path, pack_paths: dict[str, str]) -> dict[str, str]:
    hydrated = dict(pack_paths)
    for field_name, filename in CARD_FILE_FIELDS.items():
        candidate = pack_dir / filename
        if candidate.exists():
            hydrated[field_name] = str(candidate)
        else:
            hydrated.setdefault(field_name, "n/a")
    return hydrated


def parse_card(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    fields: dict[str, str] = {}
    section = ""
    pack_paths: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        match = KV_RE.match(line.strip())
        if not match:
            continue
        key, value = match.groups()
        normalized = clean(value)
        if section == "Pack Paths":
            pack_paths[key] = normalized
        else:
            fields[key] = normalized
    return fields, pack_paths


def load_draft_pack(pack_dir: Path) -> DraftPack:
    card_path = pack_dir / "00_draft-pack-card.md"
    if not card_path.exists():
        raise SystemExit(f"Draft pack card not found: {card_path}")
    fields, pack_paths = parse_card(card_path)
    return DraftPack(
        pack_dir=pack_dir,
        card_path=card_path,
        draft_id=clean(fields.get("draft_id", f"draft__{pack_dir.name}")),
        draft_key=clean(fields.get("draft_key", pack_dir.name)),
        topic_id=clean(fields.get("topic_id", "n/a")),
        approved_topic_path=clean(fields.get("approved_topic_path", "n/a")),
        requested_platforms=split_platforms(fields.get("requested_platforms", "")),
        delivery_lane=clean(fields.get("delivery_lane", "day_mainline")),
        publish_mode=clean(fields.get("publish_mode", "draft_only")),
        delivery_deadline=clean(fields.get("delivery_deadline", "n/a")),
        selection_scope=clean(fields.get("selection_scope", "n/a")),
        business_window_start=clean(fields.get("business_window_start", "n/a")),
        business_window_end=clean(fields.get("business_window_end", "n/a")),
        status=clean(fields.get("status", "drafting")),
        paths=hydrate_pack_paths(pack_dir, pack_paths),
    )


def resolve_platforms(pack: DraftPack, requested: list[str]) -> list[str]:
    platforms = requested or pack.requested_platforms
    filtered: list[str] = []
    for platform in platforms:
        key = f"{platform}_path"
        if pack.paths.get(key, "n/a") != "n/a":
            filtered.append(platform)
    return filtered


def parse_cst(raw: str) -> str:
    return raw.strip() or format_ts(now_cn())


def maybe_path(path: Path) -> str:
    return str(path) if path.exists() else "n/a"


def resolve_publish_safety_tier(requested_tier: str, verdict, selected_platforms: list[str], draft_key: str) -> str:
    requested = clean(requested_tier, "n/a")
    inferred = "n/a"
    if verdict is not None:
        if verdict.allows_publish_queue:
            inferred = "premium_publish_ready"
        elif any(verdict.allows_publish_queue_for(platform) for platform in selected_platforms):
            inferred = "fallback_publish_safe"
    if requested == "n/a":
        return inferred
    if inferred != "n/a" and requested != inferred:
        raise SystemExit(
            "Requested publish_safety_tier conflicts with latest content-pack truth. "
            f"draft_key={draft_key} requested={requested} inferred={inferred} scorecard={verdict.path if verdict else 'n/a'}"
        )
    return requested


def platform_handoff_paths(pack: DraftPack, platform: str, content_path: str) -> tuple[str, list[str]]:
    shared_candidates = [
        pack.pack_dir / "publish-readiness.md",
        pack.pack_dir / "platform-render-handoff.md",
        pack.pack_dir / "cover-visual-brief.md",
        pack.pack_dir / "cover-asset-assist.md",
        pack.pack_dir / "inline-visual-plan.md",
        pack.pack_dir / "visual-asset-sourcing.md",
        pack.pack_dir / "citation-block.md",
    ]
    if platform in {"wechat", "zhihu", "bilibili", "baijiahao", "toutiao"}:
        shared_candidates.append(pack.pack_dir / "longform-completeness-notes.md")
    platform_specific = {
        "wechat": pack.pack_dir / "wechat-html-handoff.md",
        "xiaohongshu": pack.pack_dir / "xiaohongshu-card-brief.md",
    }

    primary_path = platform_specific.get(platform)
    primary = maybe_path(primary_path) if primary_path else content_path
    if primary == "n/a":
        primary = content_path

    supporting: list[str] = []
    if content_path != "n/a" and content_path != primary:
        supporting.append(content_path)
    for candidate in shared_candidates:
        rendered = maybe_path(candidate)
        if rendered != "n/a" and rendered not in supporting:
            supporting.append(rendered)
    return primary, supporting


def manual_gate(status: str, publish_mode: str) -> str:
    if publish_mode == "auto_api":
        mapping = {
            "queued": "auto_schedule_required",
            "waiting_human_publish": "auto_publish_guard_required",
            "published": "published_recorded",
            "deferred": "auto_reschedule_required",
            "cancelled": "closed",
        }
        return mapping.get(status, "n/a")
    mapping = {
        "queued": "human_schedule_required",
        "waiting_human_publish": "human_publish_required",
        "published": "human_publish_completed",
        "deferred": "human_reschedule_required",
        "cancelled": "closed",
    }
    return mapping.get(status, "n/a")


def human_action_required(
    status: str,
    platform: str,
    planned_publish_at: str,
    primary_handoff_path: str,
    publish_mode: str,
    delivery_lane: str,
) -> str:
    if publish_mode == "auto_api" and platform == "wechat":
        if status == "queued":
            return (
                f"{delivery_lane} 已进入自动发布链路，先确保桥接入箱；随后必须通过 "
                "technical_preflight + reviewer checklist + leader checklist"
            )
        if status == "waiting_human_publish":
            return (
                "等待晨间自动发布闸门：technical_preflight=pass、reviewer_checklist=pass、"
                "leader_checklist=pass 后调用 freepublish/submit"
            )
        if status == "published":
            return "wechat 已由自动发布链路完成，下一步自动进入 24h / 72h review"
        if status == "deferred":
            return f"{delivery_lane} 自动发布已延期，等待重新排期"
        if status == "cancelled":
            return f"{delivery_lane} 自动发布已关闭"
    if status == "queued":
        return f"确认 {platform} 的发布时间与发布 owner；主交接文件：{primary_handoff_path}"
    if status == "waiting_human_publish":
        return f"按 {primary_handoff_path} 完成 {platform} 人工发布，发完回填 publish_url"
    if status == "published":
        return f"{platform} 已发，下一步回填平台数据并进入 24h review"
    if status == "deferred":
        return f"{platform} 延期，等待重新定时"
    if status == "cancelled":
        return f"{platform} 已取消，无需继续动作"
    return "n/a"


def frontstage_summary(status: str, platform: str, publish_owner: str, planned_publish_at: str, publish_mode: str, delivery_lane: str) -> str:
    if publish_mode == "auto_api" and platform == "wechat":
        if status == "queued":
            return f"{delivery_lane} 已入自动发布队列，计划最晚 {planned_publish_at} 完成自动发稿。"
        if status == "waiting_human_publish":
            return "wechat 草稿已自动入箱，等待晨间自动发布闸门。"
        if status == "published":
            return "wechat 已通过自动发布链路发布，结果回流与复盘链路已启动。"
        if status == "deferred":
            return f"{delivery_lane} 自动发布已延期。"
        if status == "cancelled":
            return f"{delivery_lane} 自动发布已取消。"
    if status == "queued":
        return f"{platform} 已入发布队列，owner={publish_owner}，待确认发布时间。"
    if status == "waiting_human_publish":
        return f"{platform} 已待人工发布，owner={publish_owner}，计划时间 {planned_publish_at}。"
    if status == "published":
        return f"{platform} 已发布，下一步应进入 review。"
    if status == "deferred":
        return f"{platform} 已延期，等待重新排期。"
    if status == "cancelled":
        return f"{platform} 已取消。"
    return "n/a"


def update_status_field(text: str, field_name: str, value: str) -> str:
    pattern = re.compile(rf"^(- `{re.escape(field_name)}`: `)([^`]+)(`)\s*$", re.M)
    if pattern.search(text):
        return pattern.sub(lambda m: f"{m.group(1)}{value}{m.group(3)}", text, count=1)
    return text


def refresh_card_paths(text: str, pack_dir: Path) -> str:
    updated = text
    for field_name, filename in CARD_FILE_FIELDS.items():
        candidate = pack_dir / filename
        updated = update_status_field(updated, field_name, str(candidate) if candidate.exists() else "n/a")
    return updated


def update_approved_topic_status(path_text: str, queue_status: str) -> str:
    mapping = {
        "queued": {
            "status": "queued",
            "next_step": "queued -> waiting_human_publish / published",
        },
        "waiting_human_publish": {
            "status": "waiting_human_publish",
            "next_step": "waiting_human_publish -> human publish / publish_url backfill",
        },
        "published": {
            "status": "published",
            "next_step": "published -> performance_review",
        },
        "deferred": {
            "status": "deferred",
            "next_step": "deferred -> repick publish timing",
        },
        "cancelled": {
            "status": "cancelled",
            "next_step": "cancelled",
        },
    }
    target = mapping.get(queue_status)
    if not target:
        return path_text
    updated = update_status_field(path_text, "status", target["status"])
    updated = update_status_field(updated, "next_step", target["next_step"])
    return updated


def update_draft_pack_card(text: str, queue_status: str) -> str:
    mapping = {
        "queued": {
            "status": "queued",
            "next_step": "queued -> waiting_human_publish / published",
            "publish_gate": "allowed",
        },
        "waiting_human_publish": {
            "status": "waiting_human_publish",
            "next_step": "waiting_human_publish -> human publish",
            "publish_gate": "allowed",
        },
        "published": {
            "status": "published",
            "next_step": "published -> performance_review",
            "publish_gate": "completed",
        },
        "deferred": {
            "status": "deferred",
            "next_step": "deferred -> repick publish timing",
            "publish_gate": "deferred",
        },
        "cancelled": {
            "status": "cancelled",
            "next_step": "cancelled",
            "publish_gate": "closed",
        },
    }
    target = mapping.get(queue_status)
    if not target:
        return text
    updated = update_status_field(text, "status", target["status"])
    updated = update_status_field(updated, "next_step", target["next_step"])
    updated = update_status_field(updated, "publish_gate", target["publish_gate"])
    updated = update_status_field(updated, "updated_at", format_ts(now_cn()))
    return updated


def update_partial_publish_card(text: str) -> str:
    updated = update_status_field(text, "status", "needs_revision")
    updated = update_status_field(updated, "next_step", "needs_revision -> revise remaining platforms / partial publish active")
    updated = update_status_field(updated, "publish_gate", "platform_partial_allowed")
    updated = update_status_field(updated, "updated_at", format_ts(now_cn()))
    return updated


def queue_item_text(
    queue_id: str,
    queue_key: str,
    pack: DraftPack,
    platform: str,
    publish_safety_tier: str,
    content_path: str,
    publish_owner: str,
    planned_publish_at: str,
    actual_publish_at: str,
    publish_url: str,
    primary_handoff_path: str,
    supporting_asset_paths: list[str],
    manual_gate_value: str,
    human_action: str,
    frontstage_line: str,
    status: str,
    notes: str,
) -> str:
    return "\n".join(
        [
            "# Publish Queue Item",
            "",
            f"- `queue_id`: `{queue_id}`",
            f"- `queue_key`: `{queue_key}`",
            f"- `topic_id`: `{pack.topic_id}`",
            f"- `draft_id`: `{pack.draft_id}`",
            f"- `approved_topic_path`: `{pack.approved_topic_path}`",
            f"- `draft_pack_dir`: `{pack.pack_dir}`",
            f"- `delivery_lane`: `{pack.delivery_lane}`",
            f"- `publish_mode`: `{pack.publish_mode}`",
            f"- `delivery_deadline`: `{pack.delivery_deadline}`",
            f"- `selection_scope`: `{pack.selection_scope}`",
            f"- `business_window_start`: `{pack.business_window_start}`",
            f"- `business_window_end`: `{pack.business_window_end}`",
            f"- `platform`: `{platform}`",
            f"- `publish_safety_tier`: `{publish_safety_tier}`",
            f"- `content_path`: `{content_path}`",
            f"- `publish_owner`: `{publish_owner}`",
            f"- `planned_publish_at`: `{planned_publish_at}`",
            f"- `actual_publish_at`: `{actual_publish_at}`",
            f"- `publish_url`: `{publish_url}`",
            f"- `primary_handoff_path`: `{primary_handoff_path}`",
            f"- `supporting_asset_paths`: `{', '.join(supporting_asset_paths) if supporting_asset_paths else 'n/a'}`",
            f"- `manual_gate`: `{manual_gate_value}`",
            f"- `human_action_required`: `{human_action}`",
            f"- `frontstage_summary`: `{frontstage_line}`",
            f"- `status`: `{status}`",
            f"- `notes`: `{notes}`",
        ]
    ).rstrip() + "\n"


def parse_item_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def queue_item_sort_key(path: Path) -> tuple[str, int, str]:
    try:
        fields = parse_item_fields(path)
    except Exception:
        fields = {}
    queue_id = clean(fields.get("queue_id", ""), "")
    for candidate in (queue_id, path.name):
        match = TIMESTAMP_TOKEN_RE.search(candidate)
        if match:
            return (match.group(1), 1, path.name)
    try:
        return (f"{path.stat().st_mtime_ns:020d}", 0, path.name)
    except FileNotFoundError:
        return ("", 0, path.name)


def latest_queue_item_path(paths: list[Path]) -> Path:
    if not paths:
        raise SystemExit("latest_queue_item_path called with empty paths")
    return sorted(paths, key=queue_item_sort_key)[-1]


def rebuild_board(queue_root: Path, board_path: Path) -> None:
    rows: list[dict[str, str]] = []
    for path in sorted(queue_root.glob("*__publish-queue-item.md")):
        rows.append(parse_item_fields(path))
    status_counts: dict[str, int] = {}
    lane_counts: dict[str, int] = {}
    tier_counts: dict[str, int] = {}
    for row in rows:
        status = row.get("status", "n/a")
        status_counts[status] = status_counts.get(status, 0) + 1
        lane = row.get("delivery_lane", "n/a")
        lane_counts[lane] = lane_counts.get(lane, 0) + 1
        tier = row.get("publish_safety_tier", "n/a")
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
    lines = [
        "# Publish Queue Board",
        "",
        f"- `generated_at`: `{format_ts(now_cn())}`",
        f"- `total_items`: `{len(rows)}`",
        f"- `queued_items`: `{status_counts.get('queued', 0)}`",
        f"- `waiting_human_publish_items`: `{status_counts.get('waiting_human_publish', 0)}`",
        f"- `published_items`: `{status_counts.get('published', 0)}`",
        f"- `deferred_items`: `{status_counts.get('deferred', 0)}`",
        f"- `cancelled_items`: `{status_counts.get('cancelled', 0)}`",
        f"- `morning_flash_items`: `{lane_counts.get('morning_flash', 0)}`",
        f"- `day_mainline_items`: `{lane_counts.get('day_mainline', 0)}`",
        f"- `premium_publish_ready_items`: `{tier_counts.get('premium_publish_ready', 0)}`",
        f"- `fallback_publish_safe_items`: `{tier_counts.get('fallback_publish_safe', 0)}`",
        "",
        "## Queue Table",
        "",
        "| queue_id | topic_key | lane | publish_mode | publish_safety_tier | platform | status | manual_gate | publish_owner | planned_publish_at | actual_publish_at | publish_url |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        queue_key = row.get("queue_key", "n/a")
        topic_key = queue_key.rsplit("__", 1)[0] if "__" in queue_key else row.get("topic_id", "n/a")
        lines.append(
            f"| `{row.get('queue_id', 'n/a')}` | `{topic_key}` | `{row.get('delivery_lane', 'n/a')}` | `{row.get('publish_mode', 'n/a')}` | `{row.get('publish_safety_tier', 'n/a')}` | `{row.get('platform', 'n/a')}` | `{row.get('status', 'n/a')}` | `{row.get('manual_gate', 'n/a')}` | `{row.get('publish_owner', 'n/a')}` | `{row.get('planned_publish_at', 'n/a')}` | `{row.get('actual_publish_at', 'n/a')}` | `{row.get('publish_url', 'n/a')}` |"
        )
    lines.extend(["", "## Human Action Queue", ""])
    action_rows = [row for row in rows if row.get("status") in {"queued", "waiting_human_publish", "deferred"}]
    if action_rows:
        for row in action_rows:
            lines.append(
                f"- `{row.get('queue_key', 'n/a')}`｜{row.get('human_action_required', 'n/a')}｜前台摘要：{row.get('frontstage_summary', 'n/a')}"
            )
    else:
        lines.append("- `none`")

    lines.extend(["", "## Published / Review Follow-up", ""])
    published_rows = [row for row in rows if row.get("status") == "published"]
    if published_rows:
        for row in published_rows:
            lines.append(
                f"- `{row.get('queue_key', 'n/a')}`｜URL：`{row.get('publish_url', 'n/a')}`｜下一步：{row.get('human_action_required', 'n/a')}"
            )
    else:
        lines.append("- `none`")
    board_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def require_publish_gate(pack: DraftPack, target_status: str, selected_platforms: list[str]) -> None:
    if target_status in {"deferred", "cancelled"}:
        return
    verdict = latest_content_pack_verdict(pack.draft_key)
    if verdict is None:
        raise SystemExit(
            f"Draft pack cannot enter publish queue without a content-pack stage-gate scorecard. draft_key={pack.draft_key}"
        )
    blocked_platforms = [platform for platform in selected_platforms if not verdict.allows_publish_queue_for(platform)]
    if blocked_platforms:
        if verdict.publish_ready_platforms:
            allowed_text = ",".join(verdict.publish_ready_platforms)
            gate_hint = f"allowed_platforms={allowed_text}"
        else:
            gate_hint = "allowed_platforms=none"
        if not verdict.allows_publish_queue:
            raise SystemExit(
                "Draft pack failed latest content-pack gate; refusing publish queue transition. "
                f"draft_key={pack.draft_key} verdict={verdict.normalized_status or 'unknown'} "
                f"score={verdict.score_text or 'n/a'} blocked_platforms={','.join(blocked_platforms)} "
                f"{gate_hint} scorecard={verdict.path}"
            )
    hygiene_failures: list[str] = []
    for platform in selected_platforms:
        content_path = pack.paths.get(f"{platform}_path", "n/a")
        resolved_path = Path(content_path).expanduser() if content_path != "n/a" else None
        result = inspect_content_hygiene(pack.pack_dir, platform, content_path=resolved_path)
        if result.blocking_issues:
            hygiene_failures.append(f"{platform}:{','.join(result.blocking_issues)}")
    if hygiene_failures:
        raise SystemExit(
            "Draft pack failed content hygiene gate; refusing publish queue transition. "
            f"draft_key={pack.draft_key} hygiene_failures={';'.join(hygiene_failures)}"
        )


def run_bridge_command(command: list[str]) -> list[str]:
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    for line in lines:
        print(line)
    return lines


def reconcile_wechat_bridge(request_id: str | None, write: bool) -> None:
    if not WECHAT_BRIDGE_RECONCILE_SCRIPT.exists():
        raise SystemExit(f"WeChat bridge reconcile script missing: {WECHAT_BRIDGE_RECONCILE_SCRIPT}")
    command = ["python3", str(WECHAT_BRIDGE_RECONCILE_SCRIPT)]
    if request_id:
        command.extend(["--request-id", request_id])
    if write:
        command.append("--write")
    run_bridge_command(command)


def wait_for_wechat_bridge_result(request_id: str, wait_seconds: int) -> bool:
    if wait_seconds <= 0:
        return False
    result_path = DEFAULT_WECHAT_BRIDGE_OUTBOX / "requests" / request_id / "result.json"
    deadline = time.monotonic() + wait_seconds
    while time.monotonic() < deadline:
        if result_path.exists():
            return True
        time.sleep(WECHAT_BRIDGE_POLL_SECONDS)
    return result_path.exists()


def maybe_enqueue_wechat_bridge(
    pack: DraftPack,
    platform: str,
    status: str,
    item_path: Path,
    wait_seconds: int,
    write: bool,
) -> None:
    if platform != "wechat" or status != "waiting_human_publish":
        return
    if not WECHAT_BRIDGE_ENQUEUE_SCRIPT.exists():
        raise SystemExit(f"WeChat bridge enqueue script missing: {WECHAT_BRIDGE_ENQUEUE_SCRIPT}")
    command = [
        "python3",
        str(WECHAT_BRIDGE_ENQUEUE_SCRIPT),
        "--draft-pack-dir",
        str(pack.pack_dir),
        "--queue-item-path",
        str(item_path),
        "--write",
    ]
    run_bridge_command(command)
    request_id = f"wechat_bridge__{pack.draft_key}"
    if wait_for_wechat_bridge_result(request_id, wait_seconds):
        reconcile_wechat_bridge(request_id=request_id, write=write)
    else:
        print(f"WECHAT_BRIDGE_PENDING {request_id}")


def main() -> None:
    args = parse_args()
    pack_dir = Path(args.draft_pack_dir)
    queue_root = Path(args.queue_root)
    queue_root.mkdir(parents=True, exist_ok=True)
    pack = load_draft_pack(pack_dir)
    allowed_pack_statuses = {"draft_ready", "ready", "needs_revision", "queued", "waiting_human_publish", "published", "deferred", "cancelled"}
    if pack.status not in allowed_pack_statuses:
        raise SystemExit(f"Draft pack must be ready/queueable before queueing. Current status: {pack.status}")
    selected_platforms = resolve_platforms(pack, args.platform)
    if not selected_platforms:
        raise SystemExit("No valid platform drafts found to queue")
    require_publish_gate(pack, args.status, selected_platforms)
    verdict = latest_content_pack_verdict(pack.draft_key)
    partial_platform_queue = bool(
        verdict
        and not verdict.allows_publish_queue
        and any(verdict.allows_publish_queue_for(platform) for platform in selected_platforms)
    )
    publish_safety_tier = resolve_publish_safety_tier(
        args.publish_safety_tier,
        verdict,
        selected_platforms,
        pack.draft_key,
    )
    if args.write and WECHAT_BRIDGE_RECONCILE_SCRIPT.exists():
        reconcile_wechat_bridge(request_id=None, write=True)

    now = now_cn()
    written_paths: list[Path] = []
    for platform in selected_platforms:
        queue_key = f"{pack.draft_key}__{platform}"
        existing = sorted(queue_root.glob(f"*__{queue_key}__publish-queue-item.md"))
        if existing:
            item_path = latest_queue_item_path(existing)
            existing_fields = parse_item_fields(item_path)
            queue_id = existing_fields.get("queue_id", f"queue__{now.strftime('%Y%m%d_%H%M%S')}__{queue_key}")
        else:
            item_path = queue_root / f"{now.strftime('%Y%m%d_%H%M%S')}__{queue_key}__publish-queue-item.md"
            queue_id = f"queue__{now.strftime('%Y%m%d_%H%M%S')}__{queue_key}"
            existing_fields = {}

        content_path = pack.paths.get(f"{platform}_path", "n/a")
        planned_publish_at = parse_cst(args.planned_publish_at) if args.planned_publish_at.strip() else existing_fields.get("planned_publish_at", format_ts(now_cn()))
        if args.status == "published":
            fallback_actual_publish_at = existing_fields.get("actual_publish_at", "n/a")
            if fallback_actual_publish_at == "n/a":
                fallback_actual_publish_at = format_ts(now_cn())
            actual_publish_at = clean(args.actual_publish_at, fallback_actual_publish_at)
            publish_url = clean(args.publish_url, existing_fields.get("publish_url", "n/a"))
            if publish_url == "n/a":
                raise SystemExit("Published status requires --publish-url")
        else:
            actual_publish_at = existing_fields.get("actual_publish_at", "n/a") if existing_fields.get("status") == "published" else "n/a"
            publish_url = existing_fields.get("publish_url", "n/a") if existing_fields.get("status") == "published" else "n/a"
        notes = clean(args.notes, existing_fields.get("notes", "n/a"))
        primary_handoff_path, supporting_asset_paths = platform_handoff_paths(pack, platform, content_path)
        manual_gate_value = manual_gate(args.status, pack.publish_mode)
        human_action = human_action_required(
            args.status,
            platform,
            planned_publish_at,
            primary_handoff_path,
            pack.publish_mode,
            pack.delivery_lane,
        )
        frontstage_line = frontstage_summary(
            args.status,
            platform,
            clean(args.publish_owner),
            planned_publish_at,
            pack.publish_mode,
            pack.delivery_lane,
        )
        item_text = queue_item_text(
            queue_id=queue_id,
            queue_key=queue_key,
            pack=pack,
            platform=platform,
            publish_safety_tier=publish_safety_tier,
            content_path=content_path,
            publish_owner=clean(args.publish_owner),
            planned_publish_at=planned_publish_at,
            actual_publish_at=actual_publish_at,
            publish_url=publish_url,
            primary_handoff_path=primary_handoff_path,
            supporting_asset_paths=supporting_asset_paths,
            manual_gate_value=manual_gate_value,
            human_action=human_action,
            frontstage_line=frontstage_line,
            status=args.status,
            notes=notes,
        )
        if args.write:
            item_path.write_text(item_text, encoding="utf-8")
            maybe_enqueue_wechat_bridge(
                pack=pack,
                platform=platform,
                status=args.status,
                item_path=item_path,
                wait_seconds=max(0, args.wechat_bridge_wait_seconds),
                write=True,
            )
        written_paths.append(item_path)

    board_path = queue_root / f"{now.strftime('%Y%m%d')}__publish-queue-board.md"
    if args.write:
        rebuild_board(queue_root, board_path)
        if pack.approved_topic_path != "n/a" and not partial_platform_queue:
            approved_path = resolve_doc_path(pack.approved_topic_path)
            if approved_path.exists():
                updated = update_approved_topic_status(approved_path.read_text(encoding="utf-8"), args.status)
                approved_path.write_text(updated, encoding="utf-8")
        if pack.card_path.exists():
            current_card = refresh_card_paths(pack.card_path.read_text(encoding="utf-8"), pack.pack_dir)
            if partial_platform_queue:
                updated_card = update_partial_publish_card(current_card)
            else:
                updated_card = update_draft_pack_card(current_card, args.status)
            pack.card_path.write_text(updated_card, encoding="utf-8")
        print(board_path)
        for path in written_paths:
            print(path)
        return

    print(board_path)
    for path in written_paths:
        print(path)


if __name__ == "__main__":
    main()

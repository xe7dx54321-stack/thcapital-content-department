#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from market_business_day import MORNING_FLASH_WINDOW_END, MORNING_FLASH_WINDOW_START, business_window, parse_cst, timestamp_from_name
from market_content_pack_truth import latest_content_pack_verdict
from market_morning_roundup_utils import inspect_morning_roundup_markdown
from market_recent_topic_guard import find_recent_conflicts


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
QUEUE_ROOT = ROOT / "06_publish_queue"
WECHAT_OUTBOX_ROOT = ROOT / "07_wechat_bridge_outbox"
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
TIMESTAMP_TOKEN_RE = re.compile(r"(\d{8}_\d{6})")
PLACEHOLDER_TOKENS = ("TBD", "TODO", "[待补", "待补", "n/a", "占位", "lorem ipsum")
INTERNAL_SCAFFOLD_PATTERNS = {
    "confirmed_vs_unverified_heading": ("当前能确认的事实", "仍需验证"),
    "confirmed_and_unverified_labels": ("已确认：", "仍需验证"),
    "writer_speed_disclaimer": ("本文撰写时距离事件发生不足 24 小时",),
    "verification_status_heading": ("Verification Status",),
    "pending_questions_heading": ("待确认问题清单",),
}


@dataclass(frozen=True)
class CheckResult:
    code: str
    status: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run technical preflight for morning_flash WeChat auto-publish.")
    parser.add_argument("--queue-item", default="", help="Absolute queue item path")
    parser.add_argument("--queue-key", default="", help="queue_key under publish queue root")
    parser.add_argument("--queue-root", default=str(QUEUE_ROOT))
    parser.add_argument("--write", action="store_true", help="Write report and checklist files")
    return parser.parse_args()


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return value if value else fallback


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def parse_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def publish_readiness_value(path: Path, platform: str) -> str:
    if not path.exists():
        return "n/a"
    pattern = re.compile(rf"^- `{re.escape(platform)}`: `([^`]+)`", re.M)
    match = pattern.search(path.read_text(encoding="utf-8"))
    return clean(match.group(1)) if match else "n/a"


def section_list_items(path: Path, heading: str) -> list[str]:
    if not path.exists():
        return []
    items: list[str] = []
    in_section = False
    marker = f"## {heading}"
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line == marker:
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section:
            continue
        match = re.match(r"^- `([^`]+)`$", line)
        if not match:
            continue
        value = clean(match.group(1), "")
        if value and value != "n/a":
            items.append(value)
    return items


def resolve_queue_item_path(queue_root: Path, queue_item: str, queue_key: str) -> Path:
    if clean(queue_item, ""):
        path = Path(queue_item).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"queue item not found: {path}")
        return path
    if not clean(queue_key, ""):
        raise SystemExit("provide either --queue-item or --queue-key")
    matches = sorted(queue_root.glob(f"*__{queue_key}__publish-queue-item.md"))
    if not matches:
        raise SystemExit(f"queue_key not found under {queue_root}: {queue_key}")
    return sorted(matches, key=queue_item_sort_key)[-1]


def extract_note_value(notes: str, key: str) -> str:
    for chunk in notes.split("|"):
        stripped = chunk.strip()
        if stripped.startswith(f"{key}="):
            return clean(stripped.split("=", 1)[1], "")
    return ""


def draft_pack_dir(fields: dict[str, str]) -> Path:
    explicit = clean(fields.get("draft_pack_dir", ""), "")
    if explicit:
        return Path(explicit).expanduser()
    content_path = clean(fields.get("content_path", ""), "")
    if content_path:
        return Path(content_path).expanduser().parent
    raise SystemExit("queue item is missing both draft_pack_dir and content_path")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def bridge_request_dir(topic_key: str) -> Path:
    return WECHAT_OUTBOX_ROOT / "requests" / f"wechat_bridge__{topic_key}"


def queue_item_sort_key(path: Path) -> tuple[str, int, str]:
    fields = parse_fields(path)
    queue_id = clean(fields.get("queue_id", ""), "")
    for candidate in (queue_id, path.name):
        match = TIMESTAMP_TOKEN_RE.search(candidate)
        if match:
            return (match.group(1), 1, path.name)
    try:
        return (f"{path.stat().st_mtime_ns:020d}", 0, path.name)
    except FileNotFoundError:
        return ("", 0, path.name)


def validate_source_packet_ref(path: Path, start_dt: datetime, end_dt: datetime) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing:{path}"
    fields = parse_fields(path)
    published_raw = clean(fields.get("published_at", "n/a"))
    captured_raw = clean(fields.get("captured_at", "n/a"))
    published_dt = parse_cst(published_raw)
    captured_dt = parse_cst(captured_raw) or timestamp_from_name(path)
    if published_dt is None:
        return False, f"{path.name}:published_at_unparseable:{published_raw}"
    if not (start_dt <= published_dt <= end_dt):
        return False, f"{path.name}:published_at_outside_window:{published_raw}"
    if captured_dt is None:
        return False, f"{path.name}:captured_at_missing"
    if not (start_dt <= captured_dt <= end_dt):
        return False, f"{path.name}:captured_at_outside_window:{format_ts(captured_dt)}"
    return True, f"{path.name}:published_at={published_raw}"


def logical_date_for_topic(topic_key: str) -> str:
    match = re.search(r"(\d{8})$", clean(topic_key, ""))
    if match:
        token = match.group(1)
        return f"{token[:4]}-{token[4:6]}-{token[6:8]}"
    return now_cn().date().isoformat()


def bridge_request_metadata(topic_key: str, metadata: dict[str, str]) -> None:
    request_dir = bridge_request_dir(topic_key)
    request_path = request_dir / "request.json"
    result_path = request_dir / "result.json"
    heartbeat_path = WECHAT_OUTBOX_ROOT / "consumer-heartbeat.json"
    metadata["bridge_request_dir"] = str(request_dir)
    metadata["bridge_request_present"] = "pass" if request_path.exists() else "fail"
    metadata["bridge_result_present"] = "pass" if result_path.exists() else "fail"
    metadata["bridge_request_created_at"] = "n/a"
    metadata["bridge_result_completed_at"] = "n/a"
    metadata["bridge_request_status"] = "missing"
    metadata["bridge_result_status"] = "missing"
    metadata["bridge_error_message"] = "n/a"
    metadata["bridge_consumer_heartbeat"] = "missing"
    metadata["bridge_consumer_last_seen_at"] = "n/a"
    metadata["bridge_consumer_pending_request_count"] = "n/a"
    if request_path.exists():
        request_payload = load_json(request_path)
        request_status = clean(str(request_payload.get("status", "")), "pending")
        metadata["bridge_request_status"] = request_status
        metadata["bridge_request_created_at"] = clean(str(request_payload.get("created_at", "")))
        if metadata.get("bridge_status", "n/a") == "n/a":
            metadata["bridge_status"] = "pending" if request_status == "pending" else request_status
    if result_path.exists():
        result_payload = load_json(result_path)
        result_status = clean(str(result_payload.get("status", "")), "unknown")
        metadata["bridge_result_status"] = result_status
        metadata["bridge_result_completed_at"] = clean(str(result_payload.get("completed_at", "")))
        metadata["bridge_error_message"] = clean(str(result_payload.get("error_message", "")), "n/a")
        if metadata.get("bridge_status", "n/a") == "n/a" or metadata["bridge_status"] == "pending":
            metadata["bridge_status"] = result_status
        if metadata.get("bridge_media_id", "n/a") == "n/a":
            metadata["bridge_media_id"] = clean(str(result_payload.get("media_id", "")), "n/a")
        if metadata.get("inline_image_count", "0") == "0":
            metadata["inline_image_count"] = clean(str(result_payload.get("inline_image_count", "")), "0")
        if metadata.get("rendered_html_img_count", "0") == "0":
            metadata["rendered_html_img_count"] = clean(str(result_payload.get("rendered_html_img_count", "")), "0")
    if heartbeat_path.exists():
        heartbeat_payload = load_json(heartbeat_path)
        metadata["bridge_consumer_last_seen_at"] = clean(str(heartbeat_payload.get("last_seen_at", "")))
        metadata["bridge_consumer_pending_request_count"] = clean(
            str(heartbeat_payload.get("pending_request_count", "")),
            "0",
        )
        last_seen_at = heartbeat_payload.get("last_seen_at")
        if isinstance(last_seen_at, str) and last_seen_at.strip():
            try:
                delta_seconds = max(
                    0,
                    int((now_cn() - datetime.fromisoformat(last_seen_at)).total_seconds()),
                )
            except ValueError:
                metadata["bridge_consumer_heartbeat"] = "invalid"
            else:
                if delta_seconds <= 180:
                    metadata["bridge_consumer_heartbeat"] = "healthy"
                elif delta_seconds <= 900:
                    metadata["bridge_consumer_heartbeat"] = "stale"
                else:
                    metadata["bridge_consumer_heartbeat"] = "offline"
        else:
            metadata["bridge_consumer_heartbeat"] = "invalid"


def check_placeholders(text: str) -> list[str]:
    lowered = text.lower()
    hits: list[str] = []
    for token in PLACEHOLDER_TOKENS:
        if token.lower() in lowered:
            hits.append(token)
    return hits


def count_markdown_images(markdown: str) -> int:
    return len(IMAGE_RE.findall(markdown))


def internal_scaffolding_hits(text: str) -> list[str]:
    hits: list[str] = []
    normalized = clean(text, "").replace("**", "")
    for label, needles in INTERNAL_SCAFFOLD_PATTERNS.items():
        if all(needle in normalized for needle in needles):
            hits.append(label)
    return hits


def top_heading(path: Path) -> str:
    if not path.exists():
        return ""
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("# "):
            return clean(stripped[2:], "")
    return ""


def approved_topic_fields(fields: dict[str, str]) -> dict[str, str]:
    approved_path = clean(fields.get("approved_topic_path", ""), "")
    if not approved_path or approved_path == "n/a":
        return {}
    path = Path(approved_path).expanduser()
    if not path.exists():
        return {}
    return parse_fields(path)


def checklist_path(pack_dir: Path, role: str) -> Path:
    return pack_dir / f"morning-flash-{role}-checklist.md"


def render_checklist(role: str, queue_item_path: Path, preflight_path: Path) -> str:
    return "\n".join(
        [
            f"# Morning Flash {role.title()} Checklist",
            "",
            f"- `queue_item_path`: `{queue_item_path}`",
            f"- `preflight_path`: `{preflight_path}`",
            f"- `checklist_role`: `{role}`",
            "- `checklist_status`: `pending`",
            "- `decision`: `pending`",
            "- `signed_off_by`: `n/a`",
            "- `signed_off_at`: `n/a`",
            "- `notes`: `n/a`",
            "",
            "## Required Checks",
            "",
            "- `duplicate_and_freshness`: `pending`",
            "- `headline_and_hook`: `pending`",
            "- `timeliness_and_heat`: `pending`",
            "- `risk_wording`: `pending`",
            "- `public_copy_cleanliness`: `pending`",
            "- `layout_and_images`: `pending`",
            "- `auto_publish_recommendation`: `pending`",
            "",
        ]
    )


def run_checks(queue_item_path: Path, fields: dict[str, str], pack_dir: Path) -> tuple[list[CheckResult], dict[str, str]]:
    notes = clean(fields.get("notes", "n/a"))
    topic_key = clean(fields.get("queue_key", pack_dir.name)).rsplit("__", 1)[0]
    markdown_path = Path(clean(fields.get("content_path", "n/a"))).expanduser()
    handoff_path = pack_dir / "wechat-html-handoff.md"
    publish_readiness_path = pack_dir / "publish-readiness.md"
    approved_fields = approved_topic_fields(fields)
    checks: list[CheckResult] = []
    queue_status = clean(fields.get("status", ""))
    roundup_ready = False
    metadata: dict[str, str] = {
        "topic_key": topic_key,
        "bridge_media_id": extract_note_value(notes, "wechat_draft_media_id") or "n/a",
        "bridge_status": extract_note_value(notes, "wechat_bridge_status") or "n/a",
        "inline_image_count": extract_note_value(notes, "wechat_inline_image_count") or "0",
        "rendered_html_img_count": extract_note_value(notes, "wechat_rendered_html_img_count") or "0",
    }
    bridge_request_metadata(topic_key, metadata)

    platform = clean(fields.get("platform", "n/a"))
    checks.append(
        CheckResult(
            "platform_is_wechat",
            "pass" if platform == "wechat" else "fail",
            f"platform={platform}",
        )
    )
    checks.append(
        CheckResult(
            "lane_is_morning_flash",
            "pass" if clean(fields.get("delivery_lane", "")) == "morning_flash" else "fail",
            f"delivery_lane={clean(fields.get('delivery_lane', 'n/a'))}",
        )
    )
    checks.append(
        CheckResult(
            "publish_mode_auto_api",
            "pass" if clean(fields.get("publish_mode", "")) == "auto_api" else "fail",
            f"publish_mode={clean(fields.get('publish_mode', 'n/a'))}",
        )
    )

    checks.append(
        CheckResult(
            "draft_pack_dir_exists",
            "pass" if pack_dir.exists() else "fail",
            f"pack_dir={pack_dir}",
        )
    )
    markdown_text = read_text(markdown_path)
    checks.append(
        CheckResult(
            "wechat_markdown_exists",
            "pass" if markdown_path.exists() else "fail",
            f"content_path={markdown_path}",
        )
    )
    checks.append(
        CheckResult(
            "wechat_handoff_exists",
            "pass" if handoff_path.exists() else "fail",
            f"handoff_path={handoff_path}",
        )
    )
    checks.append(
        CheckResult(
            "publish_readiness_exists",
            "pass" if publish_readiness_path.exists() else "fail",
            f"publish_readiness_path={publish_readiness_path}",
        )
    )
    citation_block_path = pack_dir / "citation-block.md"
    source_refs = section_list_items(citation_block_path, "Source Refs")
    source_packet_refs = [
        Path(ref).expanduser()
        for ref in source_refs
        if ref.startswith("/Users/") and ref.endswith("__source-packet.md")
    ]
    metadata["citation_source_ref_count"] = str(len(source_refs))
    metadata["citation_source_packet_ref_count"] = str(len(source_packet_refs))
    checks.append(
        CheckResult(
            "citation_block_has_source_refs",
            "pass" if source_packet_refs else "fail",
            (
                f"source_packet_refs={len(source_packet_refs)}"
                if source_packet_refs
                else f"citation_block_path={citation_block_path} refs=0"
            ),
        )
    )
    window_start_hm = clean(approved_fields.get("business_window_start", MORNING_FLASH_WINDOW_START), MORNING_FLASH_WINDOW_START)
    window_end_hm = clean(approved_fields.get("business_window_end", MORNING_FLASH_WINDOW_END), MORNING_FLASH_WINDOW_END)
    source_window_start, source_window_end = business_window(
        logical_date_for_topic(topic_key),
        start_hm=window_start_hm,
        end_hm=window_end_hm,
    )
    invalid_source_refs: list[str] = []
    for ref_path in source_packet_refs:
        valid, reason = validate_source_packet_ref(ref_path, source_window_start, source_window_end)
        if not valid:
            invalid_source_refs.append(reason)
    metadata["invalid_source_refs"] = " ; ".join(invalid_source_refs[:8]) if invalid_source_refs else "n/a"
    checks.append(
        CheckResult(
            "morning_source_refs_fresh",
            "pass" if source_packet_refs and not invalid_source_refs else "fail",
            (
                f"all_refs_within_window={len(source_packet_refs)}"
                if source_packet_refs and not invalid_source_refs
                else metadata["invalid_source_refs"]
            ),
        )
    )
    if markdown_text:
        title = clean(approved_fields.get("title", ""), "") or top_heading(markdown_path)
        approved_angle = clean(approved_fields.get("approved_angle", ""), "")
        conflicts = find_recent_conflicts(
            topic_key=topic_key,
            title=title or topic_key,
            approved_angle=approved_angle,
            exclude_queue_keys={clean(fields.get("queue_key", ""), "")},
        )
        metadata["recent_topic_conflict_count"] = str(len(conflicts))
        metadata["recent_topic_conflicts"] = " ; ".join(
            f"{item.record.topic_key}:{item.reason}:{','.join(item.shared_tokens) or 'n/a'}"
            for item in conflicts[:3]
        ) or "n/a"
        checks.append(
            CheckResult(
                "recent_topic_duplicate_guard",
                "pass" if not conflicts else "fail",
                "no blocking recent duplicate found"
                if not conflicts
                else f"conflicts={metadata['recent_topic_conflicts']}",
            )
        )
        checks.append(
            CheckResult(
                "markdown_length_ok",
                "pass" if len(markdown_text) >= 1200 else "fail",
                f"chars={len(markdown_text)}",
            )
        )
        placeholder_hits = check_placeholders(markdown_text)
        checks.append(
            CheckResult(
                "markdown_no_placeholders",
                "pass" if not placeholder_hits else "fail",
                "no placeholder tokens found" if not placeholder_hits else f"hits={', '.join(placeholder_hits[:6])}",
            )
        )
        checks.append(
            CheckResult(
                "markdown_has_heading",
                "pass" if markdown_text.lstrip().startswith("# ") else "fail",
                "top heading present" if markdown_text.lstrip().startswith("# ") else "missing top heading",
            )
        )
        scaffolding_hits = internal_scaffolding_hits(markdown_text)
        metadata["public_copy_scaffolding_hits"] = ", ".join(scaffolding_hits) if scaffolding_hits else "n/a"
        checks.append(
            CheckResult(
                "public_copy_no_internal_scaffolding",
                "pass" if not scaffolding_hits else "fail",
                "no internal evidence / verification scaffolding found"
                if not scaffolding_hits
                else f"hits={metadata['public_copy_scaffolding_hits']}",
            )
        )
        image_count = count_markdown_images(markdown_text)
        metadata["markdown_image_count"] = str(image_count)
        checks.append(
            CheckResult(
                "markdown_image_count",
                "pass" if image_count >= 1 else "warn",
                f"markdown_images={image_count}",
            )
        )
        roundup = inspect_morning_roundup_markdown(markdown_text)
        if roundup.is_roundup:
            metadata["roundup_tldr_count"] = str(roundup.tldr_count)
            metadata["roundup_detail_count"] = str(roundup.detail_count)
            metadata["roundup_title_max_length"] = str(roundup.title_max_length)
            metadata["roundup_summary_max_length"] = str(roundup.summary_max_length)
            metadata["roundup_detail_min_length"] = str(roundup.detail_min_length)
            metadata["roundup_detail_max_length"] = str(roundup.detail_max_length)
            metadata["roundup_third_party_media_mentions"] = str(roundup.third_party_media_mentions)
            metadata["roundup_mismatched_markers"] = ", ".join(roundup.mismatched_markers) if roundup.mismatched_markers else "n/a"
            checks.append(
                CheckResult(
                    "roundup_item_count",
                    "pass" if 8 <= roundup.tldr_count <= 10 and roundup.tldr_count == roundup.detail_count else "fail",
                    f"tldr={roundup.tldr_count} detail={roundup.detail_count}",
                )
            )
            checks.append(
                CheckResult(
                    "roundup_titles_aligned",
                    "pass" if roundup.titles_aligned else "fail",
                    "all titles aligned"
                    if roundup.titles_aligned
                    else f"mismatches={metadata['roundup_mismatched_markers']}",
                )
            )
            checks.append(
                CheckResult(
                    "roundup_title_limit",
                    "pass" if roundup.title_max_length <= 20 else "fail",
                    f"max_title_chars={roundup.title_max_length}",
                )
            )
            checks.append(
                CheckResult(
                    "roundup_summary_limit",
                    "pass" if roundup.summary_max_length <= 50 else "fail",
                    f"max_summary_chars={roundup.summary_max_length}",
                )
            )
            checks.append(
                CheckResult(
                    "roundup_detail_length_window",
                    "pass" if 260 <= roundup.detail_min_length and roundup.detail_max_length <= 420 else "fail",
                    f"detail_min={roundup.detail_min_length} detail_max={roundup.detail_max_length}",
                )
            )
            checks.append(
                CheckResult(
                    "roundup_third_party_media_mentions",
                    "pass" if roundup.third_party_media_mentions <= 1 else "fail",
                    f"mentions={roundup.third_party_media_mentions}",
                )
            )
            checks.append(
                CheckResult(
                    "roundup_source_ref_count",
                    "pass" if len(source_packet_refs) >= roundup.tldr_count else "fail",
                    f"source_packet_refs={len(source_packet_refs)} roundup_items={roundup.tldr_count}",
                )
            )
            roundup_ready = (
                8 <= roundup.tldr_count <= 10
                and roundup.tldr_count == roundup.detail_count
                and roundup.titles_aligned
                and roundup.title_max_length <= 20
                and roundup.summary_max_length <= 50
                and 260 <= roundup.detail_min_length
                and roundup.detail_max_length <= 420
                and roundup.third_party_media_mentions <= 1
                and len(source_packet_refs) >= roundup.tldr_count
                and not invalid_source_refs
            )

    publish_fields = parse_fields(publish_readiness_path) if publish_readiness_path.exists() else {}
    wechat_readiness = publish_readiness_value(publish_readiness_path, "wechat")
    checks.append(
        CheckResult(
            "wechat_publish_readiness",
            "pass" if wechat_readiness.startswith("ready") else ("warn" if publish_fields else "fail"),
            f"wechat={wechat_readiness}",
        )
    )
    overall_readiness = clean(publish_fields.get("overall_readiness", "n/a"))
    checks.append(
        CheckResult(
            "overall_readiness_ok",
            "pass" if overall_readiness not in {"n/a", "blocked"} else "warn",
            f"overall_readiness={overall_readiness}",
        )
    )

    verdict = latest_content_pack_verdict(topic_key)
    metadata["verdict_path"] = str(verdict.path) if verdict else "n/a"
    metadata["verdict_score"] = verdict.score_text if verdict and verdict.score_text else "n/a"
    objective_roundup_override = bool(
        verdict
        and roundup_ready
        and verdict.score_value is not None
        and verdict.score_value >= 8.0
        and verdict.continuity_lane == "near_pass_rework"
    )
    metadata["objective_roundup_override"] = "yes" if objective_roundup_override else "no"
    checks.append(
        CheckResult(
            "status_waiting_publish",
            "pass" if queue_status == "waiting_human_publish" or (objective_roundup_override and queue_status in {"rework_pending", "deferred"}) else "fail",
            (
                f"status={queue_status}"
                if queue_status == "waiting_human_publish" or not objective_roundup_override
                else f"status={queue_status} objective_roundup_override=ready_for_requeue"
            ),
        )
    )
    checks.append(
        CheckResult(
            "content_pack_gate_wechat",
            "pass" if verdict and (verdict.allows_publish_queue_for("wechat") or objective_roundup_override) else "fail",
            (
                "wechat publish gate passed"
                if verdict and verdict.allows_publish_queue_for("wechat")
                else "objective_roundup_override=pass"
                if objective_roundup_override
                else f"verdict={metadata['verdict_score']} lane={(verdict.continuity_lane if verdict else 'missing')}"
            ),
        )
    )

    bridge_status = metadata["bridge_status"]
    bridge_media_id = metadata["bridge_media_id"]
    checks.append(
        CheckResult(
            "bridge_success",
            "pass" if bridge_status == "success" else "fail",
            f"wechat_bridge_status={bridge_status}",
        )
    )
    checks.append(
        CheckResult(
            "bridge_media_id_present",
            "pass" if bridge_media_id and bridge_media_id != "n/a" else "fail",
            f"wechat_draft_media_id={bridge_media_id or 'n/a'}",
        )
    )
    rendered_image_count = int(metadata["rendered_html_img_count"]) if metadata["rendered_html_img_count"].isdigit() else 0
    checks.append(
        CheckResult(
            "rendered_image_count",
            "pass" if rendered_image_count >= 1 else "warn",
            f"rendered_html_images={rendered_image_count}",
        )
    )
    return checks, metadata


def render_report(queue_item_path: Path, pack_dir: Path, checks: list[CheckResult], metadata: dict[str, str]) -> str:
    fail_count = len([item for item in checks if item.status == "fail"])
    warn_count = len([item for item in checks if item.status == "warn"])
    overall = "pass" if fail_count == 0 else "fail"
    lines = [
        "# Morning Flash Technical Preflight",
        "",
        f"- `generated_at`: `{format_ts(now_cn())}`",
        f"- `queue_item_path`: `{queue_item_path}`",
        f"- `draft_pack_dir`: `{pack_dir}`",
        f"- `topic_key`: `{metadata.get('topic_key', 'n/a')}`",
        f"- `technical_preflight_status`: `{overall}`",
        f"- `fail_count`: `{fail_count}`",
        f"- `warn_count`: `{warn_count}`",
        f"- `bridge_status`: `{metadata.get('bridge_status', 'n/a')}`",
        f"- `bridge_media_id`: `{metadata.get('bridge_media_id', 'n/a')}`",
        f"- `bridge_request_status`: `{metadata.get('bridge_request_status', 'n/a')}`",
        f"- `bridge_request_created_at`: `{metadata.get('bridge_request_created_at', 'n/a')}`",
        f"- `bridge_result_status`: `{metadata.get('bridge_result_status', 'n/a')}`",
        f"- `bridge_result_completed_at`: `{metadata.get('bridge_result_completed_at', 'n/a')}`",
        f"- `bridge_consumer_heartbeat`: `{metadata.get('bridge_consumer_heartbeat', 'missing')}`",
        f"- `bridge_consumer_last_seen_at`: `{metadata.get('bridge_consumer_last_seen_at', 'n/a')}`",
        f"- `bridge_consumer_pending_request_count`: `{metadata.get('bridge_consumer_pending_request_count', 'n/a')}`",
        f"- `markdown_image_count`: `{metadata.get('markdown_image_count', '0')}`",
        f"- `rendered_html_img_count`: `{metadata.get('rendered_html_img_count', '0')}`",
        f"- `recent_topic_conflict_count`: `{metadata.get('recent_topic_conflict_count', '0')}`",
        f"- `recent_topic_conflicts`: `{metadata.get('recent_topic_conflicts', 'n/a')}`",
        f"- `public_copy_scaffolding_hits`: `{metadata.get('public_copy_scaffolding_hits', 'n/a')}`",
        f"- `roundup_tldr_count`: `{metadata.get('roundup_tldr_count', 'n/a')}`",
        f"- `roundup_detail_count`: `{metadata.get('roundup_detail_count', 'n/a')}`",
        f"- `roundup_title_max_length`: `{metadata.get('roundup_title_max_length', 'n/a')}`",
        f"- `roundup_summary_max_length`: `{metadata.get('roundup_summary_max_length', 'n/a')}`",
        f"- `roundup_detail_min_length`: `{metadata.get('roundup_detail_min_length', 'n/a')}`",
        f"- `roundup_detail_max_length`: `{metadata.get('roundup_detail_max_length', 'n/a')}`",
        f"- `roundup_third_party_media_mentions`: `{metadata.get('roundup_third_party_media_mentions', 'n/a')}`",
        f"- `roundup_mismatched_markers`: `{metadata.get('roundup_mismatched_markers', 'n/a')}`",
        f"- `objective_roundup_override`: `{metadata.get('objective_roundup_override', 'no')}`",
        f"- `latest_verdict_score`: `{metadata.get('verdict_score', 'n/a')}`",
        f"- `latest_verdict_path`: `{metadata.get('verdict_path', 'n/a')}`",
        "",
        "## Checks",
        "",
    ]
    for item in checks:
        lines.append(f"- `{item.code}`: `{item.status}`｜{item.message}")
    lines.extend(
        [
            "",
            "## Auto-Publish Rule",
            "",
            "- `technical_preflight_status=pass` 只是第一闸门。",
            "- 只要命中 `recent_topic_duplicate_guard=fail` 或 `public_copy_no_internal_scaffolding=fail`，晨间自动发布必须拦截。",
            "- 仍需 `morning-flash-reviewer-checklist.md` 与 `morning-flash-leader-checklist.md` 两张清单都显式签成 `pass`。",
            "- 三闸门全部通过后，`market_morning_flash_publish_guard.py` 才允许调用 `market_wechat_publish_submit.py`。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    queue_root = Path(args.queue_root).expanduser().resolve()
    queue_item_path = resolve_queue_item_path(queue_root, args.queue_item, args.queue_key)
    fields = parse_fields(queue_item_path)
    pack_dir = draft_pack_dir(fields)
    preflight_path = pack_dir / "morning-flash-preflight.md"
    reviewer_path = checklist_path(pack_dir, "reviewer")
    leader_path = checklist_path(pack_dir, "leader")
    checks, metadata = run_checks(queue_item_path, fields, pack_dir)
    report_text = render_report(queue_item_path, pack_dir, checks, metadata)

    if args.write:
        pack_dir.mkdir(parents=True, exist_ok=True)
        preflight_path.write_text(report_text, encoding="utf-8")
        if not reviewer_path.exists():
            reviewer_path.write_text(render_checklist("reviewer", queue_item_path, preflight_path), encoding="utf-8")
        if not leader_path.exists():
            leader_path.write_text(render_checklist("leader", queue_item_path, preflight_path), encoding="utf-8")
        print(preflight_path)
        print(reviewer_path)
        print(leader_path)
        return

    print(report_text)


if __name__ == "__main__":
    main()

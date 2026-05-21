#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from market_business_day import (
    BUSINESS_WINDOW_END,
    BUSINESS_WINDOW_START,
    DAY_MAINLINE_LANE,
    MORNING_FLASH_LANE,
    PUBLISH_MODE_DRAFT_ONLY,
    format_cst,
    lane_delivery_deadline,
    lane_publish_mode_default,
    lane_selection_scope_default,
    lane_window_bounds,
)


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
APPROVED_DIR = ROOT / "04_approved_topics"
LOG_DIR = ROOT / "10_logs"
CN_TZ = ZoneInfo("Asia/Shanghai")
PLATFORM_ORDER = ["wechat", "xiaohongshu", "zhihu", "x", "bilibili", "toutiao", "baijiahao"]


@dataclass(frozen=True)
class DeliveryContract:
    delivery_lane: str
    publish_mode: str
    delivery_deadline: str
    selection_scope: str
    business_window_start: str
    business_window_end: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build an approved-topic card directly for a delivery lane.")
    parser.add_argument("--topic-key", required=True, help="Stable topic key")
    parser.add_argument("--title", required=True, help="Article title / working title")
    parser.add_argument("--approved-angle", required=True, help="Approved writing angle")
    parser.add_argument("--platform", action="append", default=[], help="Requested platform(s), repeatable")
    parser.add_argument("--special-instructions", default="", help="Extra delivery instructions")
    parser.add_argument("--approved-by", default="market-editor")
    parser.add_argument("--approved-at", default="", help="Approved timestamp in local time, YYYY-MM-DD HH:MM:SS")
    parser.add_argument("--delivery-lane", default=MORNING_FLASH_LANE, help="Delivery lane, e.g. morning_flash or day_mainline")
    parser.add_argument("--publish-mode", default="", help="Override publish mode")
    parser.add_argument("--delivery-deadline", default="", help="Override delivery deadline CST text")
    parser.add_argument("--selection-scope", default="", help="Human-readable selection scope / business window label")
    parser.add_argument("--business-window-start", default="", help="Override business window start HH:MM")
    parser.add_argument("--business-window-end", default="", help="Override business window end HH:MM")
    parser.add_argument("--selection-bucket", default="lane_explicit_lock", help="Selection bucket label")
    parser.add_argument("--selected-rank", default="1", help="Optional selected rank label")
    parser.add_argument("--source-board-path", default="n/a", help="Optional upstream board / planning path")
    parser.add_argument("--selection-instruction", default="按显式交付车道直接锁题", help="Selection instruction text")
    parser.add_argument("--market-potential", default="高")
    parser.add_argument("--brand-fit-judgment", default="")
    parser.add_argument("--recommended-reason", default="")
    parser.add_argument("--one-line-judgment", default="")
    parser.add_argument("--why-now", default="")
    parser.add_argument("--platform-hint", default="")
    parser.add_argument("--risk-note", default="")
    parser.add_argument("--source-ref", action="append", default=[], help="Freeform source ref / URL, repeatable")
    parser.add_argument("--source-path", action="append", default=[], help="Local path source ref, repeatable")
    parser.add_argument("--source-bundle-path", default="", help="Optional bundle file with a `## Source Refs` section")
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return value if value else fallback


def compact(value: str) -> str:
    return clean(value, "")


def bundle_source_refs(bundle_path: str) -> list[str]:
    bundle = compact(bundle_path)
    if not bundle:
        return []
    path = Path(bundle).expanduser()
    if not path.exists():
        raise SystemExit(f"source bundle not found: {path}")
    refs: list[str] = []
    in_source_refs = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line == "## Source Refs":
            in_source_refs = True
            continue
        if in_source_refs and line.startswith("## "):
            break
        if not in_source_refs:
            continue
        match = re.match(r"^- `([^`]+)`$", line)
        if not match:
            continue
        ref = clean(match.group(1), "")
        if ref and ref != "n/a":
            refs.append(ref)
    return refs


def normalize_platforms(platforms: list[str]) -> list[str]:
    requested = {clean(item, "").lower() for item in platforms if clean(item, "")}
    return [platform for platform in PLATFORM_ORDER if platform in requested]


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    slug = re.sub(r"_+", "_", slug)
    return slug or "topic"


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def parse_approved_at(raw_value: str) -> datetime:
    value = compact(raw_value)
    if value:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").replace(tzinfo=CN_TZ)
    return now_cn()


def normalize_lane(raw_value: str) -> str:
    value = compact(raw_value).lower()
    return value or MORNING_FLASH_LANE


def resolve_delivery_contract(args: argparse.Namespace, approved_at: datetime) -> DeliveryContract:
    delivery_lane = normalize_lane(args.delivery_lane)
    default_window_start, default_window_end = lane_window_bounds(delivery_lane)
    publish_mode = compact(args.publish_mode) or lane_publish_mode_default(delivery_lane)
    if compact(args.delivery_deadline):
        delivery_deadline = compact(args.delivery_deadline)
    else:
        delivery_deadline = format_cst(lane_delivery_deadline(approved_at.date().isoformat(), delivery_lane))
    return DeliveryContract(
        delivery_lane=delivery_lane,
        publish_mode=publish_mode or PUBLISH_MODE_DRAFT_ONLY,
        delivery_deadline=delivery_deadline,
        selection_scope=compact(args.selection_scope) or lane_selection_scope_default(delivery_lane),
        business_window_start=compact(args.business_window_start) or default_window_start or BUSINESS_WINDOW_START,
        business_window_end=compact(args.business_window_end) or default_window_end or BUSINESS_WINDOW_END,
    )


def build_paths(topic_key: str, approved_at: datetime) -> tuple[Path, Path, str]:
    ts_token = approved_at.astimezone(CN_TZ).strftime("%Y%m%d_%H%M%S")
    approved_path = APPROVED_DIR / f"{ts_token}__{topic_key}__approved-topic.md"
    log_path = LOG_DIR / f"{ts_token}__{topic_key}__lane-approval-execution.md"
    topic_id = f"topic__{ts_token}__{topic_key}"
    return approved_path, log_path, topic_id


def carried_brand_fit(args: argparse.Namespace, delivery_lane: str) -> str:
    if compact(args.brand_fit_judgment):
        return compact(args.brand_fit_judgment)
    if delivery_lane == MORNING_FLASH_LANE:
        return "晨间聚合早报锁题"
    if delivery_lane == DAY_MAINLINE_LANE:
        return "日间主线锁题"
    return f"{delivery_lane} 显式锁题"


def carried_recommended_reason(args: argparse.Namespace, delivery_lane: str) -> str:
    if compact(args.recommended_reason):
        return compact(args.recommended_reason)
    if delivery_lane == MORNING_FLASH_LANE:
        return "该题作为晨间聚合早报主题壳，用于承载今日 8-10 个热点事件，并在 06:50 自动发布。"
    return "该题被显式指定进入当前交付车道，作为正式生产对象推进。"


def source_refs(args: argparse.Namespace) -> list[str]:
    refs: list[str] = []
    refs.extend(bundle_source_refs(args.source_bundle_path))
    refs.extend(clean(item, "") for item in args.source_ref if clean(item, ""))
    refs.extend(str(Path(item).expanduser()) for item in args.source_path if clean(item, ""))
    deduped: list[str] = []
    for ref in refs:
        if ref and ref not in deduped:
            deduped.append(ref)
    return deduped


def effective_source_board_path(args: argparse.Namespace) -> str:
    explicit = clean(args.source_board_path, "")
    if explicit:
        return explicit
    bundle = compact(args.source_bundle_path)
    if bundle:
        return str(Path(bundle).expanduser())
    return "n/a"


def build_card_text(
    args: argparse.Namespace,
    topic_key: str,
    topic_id: str,
    approved_at: datetime,
    platforms: list[str],
    delivery_contract: DeliveryContract,
) -> str:
    draft_pack_target_dir = ROOT / "05_draft_packs" / topic_key
    one_line_judgment = compact(args.one_line_judgment) or compact(args.approved_angle)
    why_now = compact(args.why_now) or compact(args.approved_angle)
    platform_hint = compact(args.platform_hint) or ", ".join(platforms) or "n/a"
    lines = [
        "# Approved Topic Card",
        "",
        f"- `topic_id`: `{topic_id}`",
        f"- `topic_key`: `{topic_key}`",
        f"- `candidate_id`: `cand__{topic_key}`",
        f"- `title`: `{clean(args.title)}`",
        f"- `approved_angle`: `{clean(args.approved_angle)}`",
        f"- `requested_platforms`: `{', '.join(platforms) if platforms else 'wechat'}`",
        f"- `special_instructions`: `{clean(args.special_instructions)}`",
        f"- `approved_by`: `{clean(args.approved_by)}`",
        f"- `approved_at`: `{format_cst(approved_at)}`",
        "- `status`: `approved`",
        f"- `delivery_lane`: `{delivery_contract.delivery_lane}`",
        f"- `publish_mode`: `{delivery_contract.publish_mode}`",
        f"- `delivery_deadline`: `{delivery_contract.delivery_deadline}`",
        f"- `selection_scope`: `{delivery_contract.selection_scope}`",
        f"- `business_window_start`: `{delivery_contract.business_window_start}`",
        f"- `business_window_end`: `{delivery_contract.business_window_end}`",
        "",
        "## Selection Context",
        "",
        f"- `source_board_path`: `{effective_source_board_path(args)}`",
        "- `source_top5_board_path`: `n/a`",
        "- `source_top5_board_status`: `not_required`",
        f"- `selected_rank`: `{clean(args.selected_rank)}`",
        f"- `selection_bucket`: `{clean(args.selection_bucket)}`",
        f"- `selection_instruction`: `{clean(args.selection_instruction)}`",
        "- `lock_truth`: `explicit_lane_lock`",
        "- `restored_from_holdout`: `no`",
        "",
        "## Platform Decision",
        "",
        "- `platform_selection_mode`: `explicit_lane_lock`",
        "- `platform_bundle`: `explicit_lane_platforms`",
        f"- `platform_selection_reason`: `该题被显式指定进入 {delivery_contract.delivery_lane} 车道，并按 {delivery_contract.publish_mode} 模式交付。`",
        "",
        "## Carried Judgment",
        "",
        f"- `market_potential`: `{clean(args.market_potential)}`",
        f"- `brand_fit_judgment`: `{carried_brand_fit(args, delivery_contract.delivery_lane)}`",
        f"- `recommended_reason`: `{carried_recommended_reason(args, delivery_contract.delivery_lane)}`",
        f"- `one_line_judgment`: `{one_line_judgment}`",
        f"- `why_now`: `{why_now}`",
        f"- `platform_hint`: `{platform_hint}`",
        f"- `risk_note`: `{clean(args.risk_note)}`",
        "",
        "## Source Refs",
        "",
    ]
    refs = source_refs(args)
    if refs:
        lines.extend(f"- `{ref}`" for ref in refs)
    else:
        lines.append("- `n/a`")
    lines.extend(
        [
            "",
            "## Next Handoff",
            "",
            f"- `draft_pack_target_dir`: `{draft_pack_target_dir}`",
            "- `next_step`: `approved -> drafting`",
            f"- `draft_scope`: `基于 {clean(args.approved_angle)} 生成 {', '.join(platforms) if platforms else 'wechat'} 对应平台成稿，并按 {delivery_contract.delivery_lane} 的 deadline 交付。`",
            "",
        ]
    )
    return "\n".join(lines)


def build_log_text(
    args: argparse.Namespace,
    approved_path: Path,
    topic_key: str,
    approved_at: datetime,
    platforms: list[str],
    delivery_contract: DeliveryContract,
) -> str:
    return "\n".join(
        [
            "# Lane Approval Execution",
            "",
            f"- `approved_at`: `{format_cst(approved_at)}`",
            f"- `topic_key`: `{topic_key}`",
            f"- `title`: `{clean(args.title)}`",
            f"- `requested_platforms`: `{', '.join(platforms) if platforms else 'wechat'}`",
            f"- `delivery_lane`: `{delivery_contract.delivery_lane}`",
            f"- `publish_mode`: `{delivery_contract.publish_mode}`",
            f"- `delivery_deadline`: `{delivery_contract.delivery_deadline}`",
            f"- `selection_scope`: `{delivery_contract.selection_scope}`",
            f"- `approved_topic_path`: `{approved_path}`",
            "",
            "## Summary",
            "",
            f"- 已将 `{topic_key}` 显式锁进 `{delivery_contract.delivery_lane}` 车道。",
            f"- 交付方式：`{delivery_contract.publish_mode}`。",
            f"- deadline：`{delivery_contract.delivery_deadline}`。",
            "",
        ]
    )


def main() -> None:
    args = parse_args()
    approved_at = parse_approved_at(args.approved_at)
    topic_key = slugify(clean(args.topic_key, "topic"))
    platforms = normalize_platforms(args.platform or ["wechat"])
    approved_path, log_path, topic_id = build_paths(topic_key, approved_at)
    delivery_contract = resolve_delivery_contract(args, approved_at)
    card_text = build_card_text(args, topic_key, topic_id, approved_at, platforms, delivery_contract)
    log_text = build_log_text(args, approved_path, topic_key, approved_at, platforms, delivery_contract)

    if args.write:
        APPROVED_DIR.mkdir(parents=True, exist_ok=True)
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        approved_path.write_text(card_text, encoding="utf-8")
        log_path.write_text(log_text, encoding="utf-8")
        print(approved_path)
        print(log_path)
        return

    print(card_text)
    print("---")
    print(log_text)


if __name__ == "__main__":
    main()

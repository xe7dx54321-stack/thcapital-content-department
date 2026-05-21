#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

from market_business_day import (
    BUSINESS_WINDOW_END,
    BUSINESS_WINDOW_START,
    DAY_MAINLINE_LANE,
    PUBLISH_MODE_DRAFT_ONLY,
    format_cst,
    lane_delivery_deadline,
    lane_publish_mode_default,
    lane_selection_scope_default,
    lane_window_bounds,
)
from market_top5_board_utils import top5_board_is_ready


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
BOARD_DIR = ROOT / "03_topic_candidates"
APPROVED_DIR = ROOT / "04_approved_topics"
LOG_DIR = ROOT / "10_logs"
CN_TZ = ZoneInfo("Asia/Shanghai")
DEFAULT_REQUESTED_PLATFORMS = ["wechat", "xiaohongshu", "zhihu", "x"]
PLATFORM_ORDER = ["wechat", "xiaohongshu", "zhihu", "bilibili", "toutiao", "baijiahao", "x"]
BUNDLE_DEFINITIONS: dict[str, list[str]] = {
    "deep_research_bundle": ["wechat", "zhihu", "baijiahao"],
    "breaking_signal_bundle": ["x", "wechat", "xiaohongshu"],
    "builder_community_bundle": ["wechat", "bilibili", "zhihu"],
    "mass_distribution_bundle": ["xiaohongshu", "toutiao", "wechat"],
    "search_compound_bundle": ["zhihu", "baijiahao", "wechat"],
}
BUNDLE_LABELS = {
    "deep_research_bundle": "深度认知束",
    "breaking_signal_bundle": "全信号快反束",
    "builder_community_bundle": "Builder 社区束",
    "mass_distribution_bundle": "破圈传播束",
    "search_compound_bundle": "搜索沉淀束",
}
BUNDLE_DESCRIPTIONS = {
    "deep_research_bundle": "更适合趋势解释、中深度判断和系统拆解",
    "breaking_signal_bundle": "更适合官方发布、社区热议和快反型观点分发",
    "builder_community_bundle": "更适合 agent tooling、workflow、skill、framework 这类 builder 社区深拆题",
    "mass_distribution_bundle": "更适合大众表达、增长测试、快拆和传播钩子",
    "search_compound_bundle": "更适合问答、解释、对比和 SEO 长尾沉淀",
}


@dataclass
class PlatformDecision:
    platforms: list[str]
    mode: str
    bundle: str
    reason: str
    notes: list[str] = field(default_factory=list)


@dataclass
class Candidate:
    rank: int
    candidate_key: str
    title: str
    market_potential: str = "n/a"
    brand_fit_judgment: str = "n/a"
    recommended_reason: str = "n/a"
    owner_note: str = "n/a"
    why_it_made_top8: str = "n/a"
    why_not_top5: str = "n/a"
    selection_bucket: str = "top5"
    detail_fields: dict[str, str] = field(default_factory=dict)
    detail_lists: dict[str, list[str]] = field(default_factory=dict)


@dataclass(frozen=True)
class DeliveryContract:
    delivery_lane: str
    publish_mode: str
    delivery_deadline: str
    selection_scope: str
    business_window_start: str
    business_window_end: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build approved topic card for TH Capital market content system")
    parser.add_argument("--board-path", help="Path to daily top8-top5 board")
    parser.add_argument("--date", help="Board date in YYYY-MM-DD or YYYYMMDD when board path is omitted")
    parser.add_argument("--rank", type=int, help="Selected rank from Top5 or Holdout")
    parser.add_argument("--candidate-key", default="", help="Select by candidate key instead of rank")
    parser.add_argument("--approved-angle", default="", help="Final approved angle")
    parser.add_argument("--platform", action="append", default=[], help="Requested platform, repeatable")
    parser.add_argument("--special-instructions", default="", help="Extra founder instructions")
    parser.add_argument("--selection-instruction", default="", help="Original founder instruction")
    parser.add_argument("--approved-by", default="老板", help="Approver name")
    parser.add_argument("--approved-at", default="", help="Approved timestamp in local time")
    parser.add_argument("--title-override", default="", help="Override final title if needed")
    parser.add_argument("--delivery-lane", default=DAY_MAINLINE_LANE, help="Delivery lane, e.g. day_mainline or morning_flash")
    parser.add_argument("--publish-mode", default="", help="Publish mode override, e.g. draft_only or auto_api")
    parser.add_argument("--delivery-deadline", default="", help="Delivery deadline timestamp in local CST text")
    parser.add_argument("--selection-scope", default="", help="Human-readable selection scope / business window label")
    parser.add_argument("--business-window-start", default="", help="Override business window start HH:MM")
    parser.add_argument("--business-window-end", default="", help="Override business window end HH:MM")
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def compact(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def strip_ticks(value: str) -> str:
    return value.strip().strip("`").strip()


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    slug = re.sub(r"_+", "_", slug)
    return slug or "topic"


def resolve_board_path(args: argparse.Namespace) -> Path:
    if args.board_path:
        return Path(args.board_path)
    token = (args.date or now_cn().strftime("%Y%m%d")).replace("-", "")
    path = BOARD_DIR / f"{token}__daily-top8-to-top5.md"
    return path


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_markdown_table(lines: list[str], section_header: str) -> list[list[str]]:
    rows: list[list[str]] = []
    in_section = False
    table_started = False
    for line in lines:
        if line.startswith(section_header):
            in_section = True
            continue
        if not in_section:
            continue
        if line.startswith("## ") and not line.startswith(section_header):
            break
        if not line.strip():
            continue
        if line.lstrip().startswith("|"):
            table_started = True
            row = split_row(line)
            if table_started:
                rows.append(row)
            continue
        if table_started:
            break
    if len(rows) >= 2:
        cleaned: list[list[str]] = []
        for row in rows[1:]:
            joined = "".join(cell.replace("-", "").replace(" ", "") for cell in row)
            if not joined:
                continue
            cleaned.append(row)
        return cleaned
    return []


def parse_markdown_table_multi(lines: list[str], section_headers: list[str]) -> list[list[str]]:
    for header in section_headers:
        rows = parse_markdown_table(lines, header)
        if rows:
            return rows
    return []


DETAIL_HEADER_RE = re.compile(r"^###\s+(?:.+?\s+)?(Top|Holdout)\s+(\d+)\s*(?:｜|—|-)\s*(.+)$")
DETAIL_ITEM_RE = re.compile(r"^- (?:\*\*)?([^:*：]+?)(?:\*\*)?\s*[:：]\s*(.*)$")
SUB_BULLET_RE = re.compile(r"^\s*-\s+(.*)$")
BOLD_ITEM_RE = re.compile(r"^\*\*([^*]+)\*\*(?:：(.*))?$")


def parse_detail_sections(lines: list[str]) -> dict[tuple[str, int], tuple[dict[str, str], dict[str, list[str]]]]:
    sections: dict[tuple[str, int], tuple[dict[str, str], dict[str, list[str]]]] = {}
    current_rank: int | None = None
    current_bucket = "top"
    current_key: str | None = None
    current_fields: dict[str, str] = {}
    current_lists: dict[str, list[str]] = {}

    def append_field_text(key: str, value: str) -> None:
        normalized = compact(value)
        if not normalized:
            return
        existing = current_fields.get(key, "")
        current_fields[key] = f"{existing} {normalized}".strip() if existing else normalized

    def flush() -> None:
        nonlocal current_rank, current_fields, current_lists, current_key, current_bucket
        if current_rank is not None:
            sections[(current_bucket, current_rank)] = (current_fields, current_lists)
        current_rank = None
        current_bucket = "top"
        current_key = None
        current_fields = {}
        current_lists = {}

    for raw_line in lines:
        line = raw_line.rstrip()
        header_match = DETAIL_HEADER_RE.match(line)
        if header_match:
            flush()
            current_bucket = compact(header_match.group(1)).lower()
            current_rank = int(header_match.group(2))
            current_fields["__detail_title__"] = compact(header_match.group(3))
            continue
        if current_rank is None:
            continue
        if re.match(r"^##+\s+", line):
            flush()
            continue
        match = DETAIL_ITEM_RE.match(line)
        if match:
            current_key = compact(match.group(1))
            value = compact(match.group(2))
            if value:
                current_fields[current_key] = value
            else:
                current_fields.setdefault(current_key, "")
                current_lists.setdefault(current_key, [])
            continue
        bold_match = BOLD_ITEM_RE.match(line.strip())
        if bold_match:
            current_key = compact(bold_match.group(1))
            value = compact(bold_match.group(2) or "")
            if value:
                current_fields[current_key] = value
            else:
                current_fields.setdefault(current_key, "")
                current_lists.setdefault(current_key, [])
            continue
        if current_key and line.strip().startswith("- "):
            current_lists.setdefault(current_key, []).append(strip_ticks(line.strip()[2:]))
            continue
        if current_key:
            stripped = line.strip()
            sub_match = SUB_BULLET_RE.match(stripped)
            if sub_match:
                current_lists.setdefault(current_key, []).append(strip_ticks(sub_match.group(1)))
                continue
            if stripped and not stripped.startswith("---"):
                append_field_text(current_key, stripped)
    flush()
    return sections


def first_present(detail_fields: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = compact(detail_fields.get(key, ""))
        if value:
            return value
    return "n/a"


def load_candidates(board_path: Path) -> dict[int, Candidate]:
    lines = board_path.read_text(encoding="utf-8").splitlines()
    top_rows = parse_markdown_table_multi(lines, ["## Top 5 Recommended", "## Top 5 推荐"])
    holdout_rows = parse_markdown_table_multi(lines, ["## Holdout 3", "## Holdout 3（未进 Top 5，但保留观察）"])
    detail_sections = parse_detail_sections(lines)

    candidates: dict[int, Candidate] = {}

    for row in top_rows:
        rank = int(row[0])
        detail_fields, detail_lists = detail_sections.get(("top", rank), ({}, {}))
        if len(row) >= 7:
            title = strip_ticks(row[2])
            market_potential = strip_ticks(row[3])
            brand_fit_judgment = strip_ticks(row[4])
            recommended_reason = strip_ticks(row[5])
            owner_note = strip_ticks(row[6])
        elif len(row) >= 5:
            title = first_present(detail_fields, "__detail_title__")
            market_potential = first_present(detail_fields, "市场潜力")
            brand_fit_judgment = first_present(detail_fields, "品牌贴合度", "品牌贴合度判断")
            recommended_reason = first_present(
                detail_fields,
                "为什么该我们写",
                "为什么值得做",
                "建议切入角度",
                "Heat Signal（热度信号）",
                "Heat Signal",
            )
            owner_note = first_present(
                detail_fields,
                "风险提示",
                "平台发酵预判",
                "适合平台",
                "Evidence Signal（证据信号）",
                "Evidence Signal",
            )
        else:
            continue
        candidate = Candidate(
            rank=rank,
            candidate_key=strip_ticks(row[1]),
            title=title,
            market_potential=market_potential,
            brand_fit_judgment=brand_fit_judgment,
            recommended_reason=recommended_reason,
            owner_note=owner_note,
            selection_bucket="top5",
        )
        if ("top", rank) in detail_sections:
            candidate.detail_fields, candidate.detail_lists = detail_fields, detail_lists
        candidates[rank] = candidate

    for index, row in enumerate(holdout_rows, start=1):
        if len(row) < 5:
            continue
        raw_rank = strip_ticks(row[0])
        rank_match = re.search(r"(\d+)", raw_rank)
        rank_suffix = int(rank_match.group(1)) if rank_match else index
        rank = int(raw_rank) if raw_rank.isdigit() else len(top_rows) + rank_suffix
        detail_fields, detail_lists = detail_sections.get(("holdout", index), detail_sections.get(("holdout", rank), ({}, {})))
        title = strip_ticks(row[2]) if len(row) >= 7 else first_present(detail_fields, "__detail_title__")
        why_it_made_top8 = (
            strip_ticks(row[3])
            if len(row) >= 7
            else first_present(detail_fields, "为何进入 Top 8 候选", "为何能进 Top 8 候选", "恢复角度")
        )
        why_not_top5 = (
            strip_ticks(row[4])
            if len(row) >= 7
            else first_present(detail_fields, "为何被放下", "Holdout Reason", "恢复条件")
        )
        candidate = Candidate(
            rank=rank,
            candidate_key=strip_ticks(row[1]),
            title=title,
            why_it_made_top8=why_it_made_top8,
            why_not_top5=why_not_top5,
            selection_bucket="holdout",
        )
        if ("holdout", index) in detail_sections or ("holdout", rank) in detail_sections:
            candidate.detail_fields, candidate.detail_lists = detail_fields, detail_lists
        candidates[rank] = candidate

    return candidates


def find_candidate(candidates: dict[int, Candidate], rank: int | None, candidate_key: str) -> Candidate:
    normalized_key = strip_ticks(candidate_key)
    if rank is not None:
        if rank not in candidates:
            raise SystemExit(f"Rank {rank} not found in board")
        return candidates[rank]
    if normalized_key:
        for candidate in candidates.values():
            if candidate.candidate_key == normalized_key:
                return candidate
        raise SystemExit(f"Candidate key not found in board: {normalized_key}")
    raise SystemExit("Either --rank or --candidate-key is required")


def extract_platform_mentions(texts: Iterable[str]) -> list[str]:
    joined = " ".join(texts)
    mapping = [
        ("wechat", ["微信", "wechat"]),
        ("xiaohongshu", ["小红书", "xiaohongshu"]),
        ("zhihu", ["知乎", "zhihu"]),
        ("x", [" x ", "X/", "X ", "X（", "X(", "Twitter", "twitter", "X/小红书", "X 线程"]),
        ("bilibili", ["B站", "bilibili"]),
        ("toutiao", ["头条", "今日头条", "toutiao"]),
        ("baijiahao", ["百家号", "baijiahao"]),
        ("douyin", ["抖音", "douyin"]),
        ("youtube", ["YouTube", "youtube"]),
    ]
    normalized = joined.lower()
    platforms: list[str] = []
    for name, hints in mapping:
        if any(hint.lower() in normalized for hint in hints):
            platforms.append(name)
    return normalize_platforms(platforms)


def detect_platforms(texts: Iterable[str]) -> list[str]:
    platforms = extract_platform_mentions(texts)
    if not platforms:
        return DEFAULT_REQUESTED_PLATFORMS[:]
    return platforms


def normalize_platforms(platforms: Iterable[str]) -> list[str]:
    seen = {platform for platform in platforms if platform in PLATFORM_ORDER}
    return [platform for platform in PLATFORM_ORDER if platform in seen]


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    normalized = text.lower()
    return any(keyword.lower() in normalized for keyword in keywords)


def joined_candidate_text(candidate: Candidate, approved_angle: str) -> str:
    parts = [
        candidate.title,
        candidate.market_potential,
        candidate.brand_fit_judgment,
        candidate.recommended_reason,
        candidate.owner_note,
        candidate.why_it_made_top8,
        candidate.why_not_top5,
        approved_angle,
    ]
    parts.extend(candidate.detail_fields.values())
    for values in candidate.detail_lists.values():
        parts.extend(values)
    return "\n".join(part for part in parts if part)


def recommend_platform_bundle(candidate: Candidate, approved_angle: str) -> PlatformDecision:
    combined_text = joined_candidate_text(candidate, approved_angle)
    platform_hint = candidate.detail_fields.get("建议输出形式 / 平台", "")
    source_refs = build_source_refs(candidate)
    score = {platform: 0 for platform in PLATFORM_ORDER}
    bundle_score = {bundle: 0 for bundle in BUNDLE_DEFINITIONS}
    notes: list[str] = []

    builder_keywords = [
        "agent", "workflow", "skill", "tool", "tooling", "framework", "infra", "harness",
        "stack", "developer", "开发者", "技术创始人", "教程", "实操", "coding", "code",
        "automation", "编排", "多 agent", "multi-agent", "多智能体",
    ]
    hot_signal_keywords = [
        "快拆", "快讯", "热点", "刷屏", "发酵", "热度", "官宣", "发布", "上新", "高热",
        "讨论", "热议", "trending", "launch", "product hunt", "reddit", "hackernews", "hacker news",
    ]
    search_keywords = [
        "解释", "怎么看", "如何看", "什么是", "why", "how", "对比", "框架", "问题回答",
        "答疑", "概念", "路线", "回答", "横评",
    ]
    mass_keywords = [
        "普通人", "消费者", "体验", "种草", "小白", "机会清单", "误区", "3 个点", "看懂",
        "使用体验", "creator", "内容工厂", "内容生产", "公域", "传播",
    ]
    deep_keywords = [
        "深度", "解读", "分析", "趋势", "判断", "专题", "复盘", "研究", "关键变量",
        "商业闭环", "技术反思", "系统性",
    ]

    if contains_any(combined_text, builder_keywords):
        score["bilibili"] += 4
        score["zhihu"] += 2
        score["wechat"] += 2
        bundle_score["builder_community_bundle"] += 4
        notes.append("识别到 builder / workflow / tooling / framework 信号，适合社区深拆。")

    if contains_any(combined_text, hot_signal_keywords):
        score["x"] += 3
        score["xiaohongshu"] += 2
        score["toutiao"] += 2
        score["wechat"] += 1
        bundle_score["breaking_signal_bundle"] += 4
        notes.append("识别到热点 / 官宣 / 社区热议信号，适合快反与分发。")

    if contains_any(combined_text, search_keywords):
        score["zhihu"] += 3
        score["baijiahao"] += 3
        score["wechat"] += 1
        bundle_score["search_compound_bundle"] += 4
        notes.append("识别到解释 / 对比 / 问答信号，适合搜索承接与长尾沉淀。")

    if contains_any(combined_text, mass_keywords):
        score["xiaohongshu"] += 3
        score["toutiao"] += 2
        score["wechat"] += 1
        bundle_score["mass_distribution_bundle"] += 4
        notes.append("识别到大众表达 / 使用体验 / 传播性信号，适合破圈传播。")

    if contains_any(combined_text, deep_keywords):
        score["wechat"] += 3
        score["zhihu"] += 2
        score["baijiahao"] += 1
        score["bilibili"] += 1
        bundle_score["deep_research_bundle"] += 4
        notes.append("识别到深度解读 / 趋势判断信号，适合公众号主稿承载。")

    hinted_platforms = extract_platform_mentions([platform_hint]) if platform_hint and platform_hint != "n/a" else []
    if hinted_platforms:
        for platform in hinted_platforms:
            score[platform] += 3
        notes.append(f"上游 board 的平台提示提到了：{', '.join(hinted_platforms)}。")

    source_ref_text = " ".join(source_refs).lower()
    if any(domain in source_ref_text for domain in ["github.com", "producthunt.com", "ycombinator.com"]):
        score["bilibili"] += 1
        score["zhihu"] += 1
        score["wechat"] += 1
        bundle_score["builder_community_bundle"] += 1
        notes.append("source refs 含 GitHub / Product Hunt / YC，说明开发者社区属性较强。")

    if any(domain in source_ref_text for domain in ["reddit.com", "news.ycombinator.com", "x.com", "twitter.com"]):
        score["x"] += 1
        score["xiaohongshu"] += 1
        score["toutiao"] += 1
        bundle_score["breaking_signal_bundle"] += 1
        notes.append("source refs 含 Reddit / HN / X，说明外部讨论热度可用于快反。")

    if any(domain in source_ref_text for domain in ["openai.com", "anthropic.com", "claude.com"]):
        score["wechat"] += 1
        score["zhihu"] += 1
        notes.append("source refs 含官方产品页 / 博客，适合做判断型与解释型主稿。")

    bundle_priority = [
        "builder_community_bundle",
        "breaking_signal_bundle",
        "deep_research_bundle",
        "mass_distribution_bundle",
        "search_compound_bundle",
    ]
    selected_bundle = max(bundle_priority, key=lambda name: (bundle_score[name], -bundle_priority.index(name)))
    platforms = list(BUNDLE_DEFINITIONS[selected_bundle])

    extras = [platform for platform, platform_score in sorted(score.items(), key=lambda item: (-item[1], PLATFORM_ORDER.index(item[0]))) if platform_score >= 4 and platform not in platforms]
    for platform in extras:
        if len(platforms) >= 4:
            break
        platforms.append(platform)

    platforms = normalize_platforms(platforms)

    extra_note = ""
    added = [platform for platform in platforms if platform not in BUNDLE_DEFINITIONS[selected_bundle]]
    if added:
        extra_note = f"；同时补充 {', '.join(added)} 作为增强分发或搜索补位"

    reason = (
        f"自动判定为 {selected_bundle}（{BUNDLE_LABELS[selected_bundle]}）："
        f"{BUNDLE_DESCRIPTIONS[selected_bundle]}{extra_note}。"
    )

    return PlatformDecision(
        platforms=platforms,
        mode="heuristic_bundle",
        bundle=selected_bundle,
        reason=reason,
        notes=notes,
    )


def default_angle(candidate: Candidate) -> str:
    if candidate.selection_bucket == "holdout":
        return candidate.detail_fields.get("如果捞回，最佳改写角度", candidate.owner_note) or candidate.owner_note or "沿原候选核心角度推进"
    return candidate.detail_fields.get("建议切入角度", candidate.owner_note) or candidate.owner_note or "沿原候选推荐角度推进"


def preferred_title(candidate: Candidate, title_override: str) -> str:
    return compact(title_override) if compact(title_override) else candidate.title


def build_topic_key(candidate: Candidate) -> str:
    raw = candidate.candidate_key or candidate.title
    raw = strip_ticks(raw)
    if raw.startswith("cand__"):
        raw = raw[len("cand__") :]
    return slugify(raw)


def format_timestamp(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def build_paths(topic_key: str, approved_at: datetime) -> tuple[Path, Path, str, str]:
    ts_token = approved_at.astimezone(CN_TZ).strftime("%Y%m%d_%H%M%S")
    topic_id = f"topic__{ts_token}__{topic_key}"
    approved_path = APPROVED_DIR / f"{ts_token}__{topic_key}__approved-topic.md"
    log_path = LOG_DIR / f"{ts_token}__{topic_key}__topic-approval-execution.md"
    return approved_path, log_path, topic_id, ts_token


def build_source_refs(candidate: Candidate) -> list[str]:
    refs = []
    refs.extend(candidate.detail_lists.get("原始链接 / source packet", []))
    refs.extend(candidate.detail_lists.get("原始链接 / Source Packet", []))
    return refs


def parse_approved_at(raw_value: str) -> datetime:
    if raw_value.strip():
        return datetime.strptime(raw_value.strip(), "%Y-%m-%d %H:%M:%S").replace(tzinfo=CN_TZ)
    return now_cn()


def normalize_lane(raw_value: str) -> str:
    value = compact(raw_value).lower()
    return value or DAY_MAINLINE_LANE


def resolve_delivery_contract(args: argparse.Namespace, approved_at: datetime) -> DeliveryContract:
    delivery_lane = normalize_lane(args.delivery_lane)
    default_window_start, default_window_end = lane_window_bounds(delivery_lane)
    window_start = compact(args.business_window_start) or default_window_start or BUSINESS_WINDOW_START
    window_end = compact(args.business_window_end) or default_window_end or BUSINESS_WINDOW_END
    publish_mode = compact(args.publish_mode) or lane_publish_mode_default(delivery_lane) or PUBLISH_MODE_DRAFT_ONLY
    if compact(args.delivery_deadline):
        delivery_deadline = compact(args.delivery_deadline)
    else:
        delivery_deadline = format_cst(lane_delivery_deadline(approved_at.date().isoformat(), delivery_lane))
    selection_scope = compact(args.selection_scope) or lane_selection_scope_default(delivery_lane)
    return DeliveryContract(
        delivery_lane=delivery_lane,
        publish_mode=publish_mode,
        delivery_deadline=delivery_deadline,
        selection_scope=selection_scope,
        business_window_start=window_start,
        business_window_end=window_end,
    )


def build_card_text(
    candidate: Candidate,
    board_path: Path,
    approved_at: datetime,
    topic_id: str,
    approved_angle: str,
    platform_decision: PlatformDecision,
    special_instructions: str,
    selection_instruction: str,
    approved_by: str,
    title: str,
    draft_pack_target_dir: Path,
    delivery_contract: DeliveryContract,
) -> str:
    source_refs = build_source_refs(candidate)
    lines = [
        "# Approved Topic Card",
        "",
        f"- `topic_id`: `{topic_id}`",
        f"- `topic_key`: `{build_topic_key(candidate)}`",
        f"- `candidate_id`: `{candidate.candidate_key}`",
        f"- `title`: `{title}`",
        f"- `approved_angle`: `{approved_angle}`",
        f"- `requested_platforms`: `{', '.join(platform_decision.platforms)}`",
        f"- `special_instructions`: `{special_instructions or 'n/a'}`",
        f"- `approved_by`: `{approved_by}`",
        f"- `approved_at`: `{format_timestamp(approved_at)}`",
        f"- `status`: `approved`",
        f"- `delivery_lane`: `{delivery_contract.delivery_lane}`",
        f"- `publish_mode`: `{delivery_contract.publish_mode}`",
        f"- `delivery_deadline`: `{delivery_contract.delivery_deadline}`",
        f"- `selection_scope`: `{delivery_contract.selection_scope}`",
        f"- `business_window_start`: `{delivery_contract.business_window_start}`",
        f"- `business_window_end`: `{delivery_contract.business_window_end}`",
        "",
        "## Selection Context",
        "",
        f"- `source_board_path`: `{board_path}`",
        f"- `source_top5_board_path`: `{board_path}`",
        "- `source_top5_board_status`: `ready`",
        f"- `selected_rank`: `{candidate.rank}`",
        f"- `selection_bucket`: `{candidate.selection_bucket}`",
        f"- `selection_instruction`: `{selection_instruction or 'n/a'}`",
        f"- `lock_truth`: `{'manual_holdout_top5_lock' if candidate.selection_bucket == 'holdout' else 'manual_top5_lock'}`",
        f"- `restored_from_holdout`: `{'yes' if candidate.selection_bucket == 'holdout' else 'no'}`",
        "",
        "## Platform Decision",
        "",
        f"- `platform_selection_mode`: `{platform_decision.mode}`",
        f"- `platform_bundle`: `{platform_decision.bundle}`",
        f"- `platform_selection_reason`: `{platform_decision.reason}`",
        "",
        "## Platform Decision Notes",
        "",
    ]
    if platform_decision.notes:
        lines.extend(f"- `{note}`" for note in platform_decision.notes)
    else:
        lines.append("- `n/a`")

    lines.extend(
        [
            "",
            "## Carried Judgment",
            "",
            f"- `market_potential`: `{candidate.market_potential}`",
            f"- `brand_fit_judgment`: `{candidate.brand_fit_judgment}`",
            f"- `recommended_reason`: `{candidate.recommended_reason}`",
            f"- `one_line_judgment`: `{candidate.detail_fields.get('一句话判断', 'n/a')}`",
            f"- `why_now`: `{candidate.detail_fields.get('为什么值得做', candidate.why_it_made_top8) or 'n/a'}`",
            f"- `platform_hint`: `{candidate.detail_fields.get('建议输出形式 / 平台', 'n/a')}`",
            f"- `risk_note`: `{candidate.detail_fields.get('风险提示', candidate.why_not_top5) or 'n/a'}`",
            "",
            "## Source Refs",
            "",
        ]
    )
    if source_refs:
        lines.extend(f"- `{ref}`" for ref in source_refs)
    else:
        lines.append("- `n/a`")

    lines.extend(
        [
            "",
            "## Next Handoff",
            "",
            f"- `draft_pack_target_dir`: `{draft_pack_target_dir}`",
            "- `next_step`: `approved -> drafting`",
            f"- `draft_scope`: `基于 {approved_angle} 生成 {', '.join(platform_decision.platforms)} 对应的多平台草稿，并保留 source refs 与 risk note`",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def build_log_text(
    candidate: Candidate,
    board_path: Path,
    approved_topic_path: Path,
    approved_at: datetime,
    approved_angle: str,
    platform_decision: PlatformDecision,
    selection_instruction: str,
    delivery_contract: DeliveryContract,
) -> str:
    lines = [
        "# 同行资本市场内容系统｜Topic Approval Execution",
        "",
        f"- `approved_at`: `{format_timestamp(approved_at)}`",
        f"- `board_path`: `{board_path}`",
        f"- `selected_rank`: `{candidate.rank}`",
        f"- `selection_bucket`: `{candidate.selection_bucket}`",
        f"- `candidate_id`: `{candidate.candidate_key}`",
        f"- `title`: `{candidate.title}`",
        f"- `selection_instruction`: `{selection_instruction or 'n/a'}`",
        f"- `approved_angle`: `{approved_angle}`",
        f"- `requested_platforms`: `{', '.join(platform_decision.platforms)}`",
        f"- `platform_selection_mode`: `{platform_decision.mode}`",
        f"- `platform_bundle`: `{platform_decision.bundle}`",
        f"- `delivery_lane`: `{delivery_contract.delivery_lane}`",
        f"- `publish_mode`: `{delivery_contract.publish_mode}`",
        f"- `delivery_deadline`: `{delivery_contract.delivery_deadline}`",
        f"- `selection_scope`: `{delivery_contract.selection_scope}`",
        f"- `approved_topic_path`: `{approved_topic_path}`",
        "",
        "## Summary",
        "",
        f"- 已将 `Top {candidate.rank}` 固化为 `approved_topic`。",
        f"- 下游应按 `{', '.join(platform_decision.platforms)}` 先产出 Draft Pack。",
        f"- 角度已归一为：`{approved_angle}`。",
        f"- 平台决策说明：`{platform_decision.reason}`。",
        f"- 交付车道：`{delivery_contract.delivery_lane}`；交付方式：`{delivery_contract.publish_mode}`；deadline：`{delivery_contract.delivery_deadline}`。",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    board_path = resolve_board_path(args)
    if not board_path.exists():
        raise SystemExit(f"Board not found: {board_path}")
    if not top5_board_is_ready(board_path):
        raise SystemExit(f"Board exists but has no usable Top5/Holdout candidates: {board_path}")

    candidates = load_candidates(board_path)
    candidate = find_candidate(candidates, args.rank, args.candidate_key)
    approved_at = parse_approved_at(args.approved_at)
    delivery_contract = resolve_delivery_contract(args, approved_at)
    approved_angle = compact(args.approved_angle) or compact(default_angle(candidate))
    special_instructions = compact(args.special_instructions)
    selection_instruction = compact(args.selection_instruction)
    founder_platforms = normalize_platforms(args.platform) if args.platform else extract_platform_mentions([special_instructions, selection_instruction])
    if args.platform:
        platform_decision = PlatformDecision(
            platforms=normalize_platforms(args.platform),
            mode="manual_override",
            bundle="custom_manual_bundle",
            reason="创始人显式通过命令参数指定了平台范围，系统按人工指定执行。",
            notes=["人工指定平台优先级，跳过自动平台束推荐。"],
        )
    elif founder_platforms and any(token in (special_instructions + " " + selection_instruction) for token in ["微信", "小红书", "知乎", "X", "x", "B站", "头条", "百家号", "wechat", "xiaohongshu", "zhihu", "bilibili", "toutiao", "baijiahao"]):
        platform_decision = PlatformDecision(
            platforms=founder_platforms,
            mode="founder_instruction_parse",
            bundle="custom_founder_instruction_bundle",
            reason="创始人在确认语句或附加说明中已经明确给出平台范围，系统按该范围执行。",
            notes=["平台范围来自创始人自然语言确认，不使用自动推荐结果覆盖。"],
        )
    else:
        platform_decision = recommend_platform_bundle(candidate, approved_angle)

    title = preferred_title(candidate, args.title_override)
    topic_key = build_topic_key(candidate)
    approved_path, log_path, topic_id, _ = build_paths(topic_key, approved_at)
    draft_pack_target_dir = ROOT / "05_draft_packs" / topic_key

    card_text = build_card_text(
        candidate=candidate,
        board_path=board_path,
        approved_at=approved_at,
        topic_id=topic_id,
        approved_angle=approved_angle,
        platform_decision=platform_decision,
        special_instructions=special_instructions,
        selection_instruction=selection_instruction,
        approved_by=args.approved_by,
        title=title,
        draft_pack_target_dir=draft_pack_target_dir,
        delivery_contract=delivery_contract,
    )
    log_text = build_log_text(
        candidate=candidate,
        board_path=board_path,
        approved_topic_path=approved_path,
        approved_at=approved_at,
        approved_angle=approved_angle,
        platform_decision=platform_decision,
        selection_instruction=selection_instruction,
        delivery_contract=delivery_contract,
    )

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

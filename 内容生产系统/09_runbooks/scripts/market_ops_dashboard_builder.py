#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from html import escape
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

_REPO_ROOT = None
for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "content_system" / "paths.py").exists():
        _REPO_ROOT = _parent
        sys.path.insert(0, str(_parent / "src"))
        break
if _REPO_ROOT is None:
    raise RuntimeError("Cannot locate repository root")
from content_system.paths import get_project_paths

from market_content_pack_truth import latest_content_pack_verdict
from market_stage_artifact_status import best_artifact_in_family, inspect_artifact, state_satisfies
from market_top5_board_utils import top5_board_is_ready
from market_topic_key_registry import extract_top20_topic_keys, legacy_top20_topic_key


ROOT = get_project_paths(_REPO_ROOT).legacy_content_root
SOURCE_PACKET_DIR = ROOT / "02_topic_radar" / "source_packets"
TOPIC_CANDIDATE_DIR = ROOT / "03_topic_candidates"
APPROVED_TOPIC_DIR = ROOT / "04_approved_topics"
DRAFT_PACK_ROOT = ROOT / "05_draft_packs"
LOG_DIR = ROOT / "10_logs"
FRONTSTAGE_DIR = ROOT / "11_frontstage"
FILE_SCHEME = "file"

CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
TOP20_HEADING_RE = re.compile(r"^###\s+(\d+)\.\s+(.+)$")
MD_HEADING_RE = re.compile(r"^#+\s+(.+)$")
TOPIC_KEY_INLINE_RE = re.compile(r"topic_key`:\s*`([^`]+)`")

PLATFORM_CONFIG = {
    "wechat": {"label": "微信公众号", "accent": "#07c160", "slug": "wechat"},
    "xiaohongshu": {"label": "小红书", "accent": "#ff2442", "slug": "xiaohongshu"},
    "zhihu": {"label": "知乎", "accent": "#1677ff", "slug": "zhihu"},
    "x": {"label": "X", "accent": "#111111", "slug": "x"},
    "bilibili": {"label": "B站", "accent": "#00a1d6", "slug": "bilibili"},
    "toutiao": {"label": "今日头条", "accent": "#ff4d4f", "slug": "toutiao"},
    "baijiahao": {"label": "百家号", "accent": "#376bff", "slug": "baijiahao"},
}
PLATFORM_ORDER = list(PLATFORM_CONFIG.keys())
GENERIC_ISSUE_HEADINGS = {
    "做得好的地方",
    "扣分点",
    "为什么是这个分数",
    "Top 5 Detail Blocks",
}


@dataclass
class SourcePacketView:
    packet_key: str
    title: str
    summary: str
    platform: str
    source_name: str
    source_type: str
    captured_at: str
    published_at: str
    canonical_url: str
    primary_source: str
    signal_quality: str
    citation_reliability: str
    visual_evidence_status: str
    heat_hint: str
    verification_status: str
    path: str


@dataclass
class Top20Candidate:
    rank: int
    header_title: str
    title: str
    topic_key: str
    primary_platform: str
    published_at: str
    original_link: str
    score_total: str
    score_breakdown: str
    signal_summary: str
    why_in_top20: str
    visual_assets: str
    risks: str
    path: str


@dataclass
class ApprovedTopicView:
    topic_id: str
    topic_key: str
    title: str
    requested_platforms: str
    approved_angle: str
    approved_at: str
    status: str
    selected_rank: str
    selection_bucket: str
    recommended_reason: str
    one_line_judgment: str
    risk_note: str
    source_board_path: str
    path: str


@dataclass
class DraftCard:
    topic_key: str
    topic_id: str
    platform: str
    display_title: str
    preview: str
    status: str
    updated_at: str
    pack_status: str
    pack_dir: str
    file_path: str
    note: str


@dataclass
class ReviewDigest:
    topic_key: str
    platforms: str
    pack_status: str
    last_event_at: str
    redteam_summary: str
    judge_score: str
    judge_status: str
    main_failures: list[str]
    next_fixes: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build HTML ops dashboard for TH Capital market content system")
    parser.add_argument("--date", default=datetime.now(CN_TZ).date().isoformat(), help="Business date in YYYY-MM-DD")
    parser.add_argument("--window-start", default="17:00", help="Previous-day business window start, HH:MM")
    parser.add_argument("--window-end", default="14:30", help="Current-day business window end, HH:MM")
    parser.add_argument("--write", action="store_true", help="Write HTML and JSON snapshots")
    return parser.parse_args()


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\*\*(.*?)\*\*", r"\1", value or "")
    value = re.sub(r"\s+", " ", value).strip().strip("`").strip("*")
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


def parse_fields_from_lines(lines: list[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in lines:
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def parse_cst(raw: str) -> datetime | None:
    raw = clean(raw, "")
    if not raw or raw == "n/a":
        return None
    for fmt in (
        "%Y-%m-%d %H:%M:%S CST",
        "%Y-%m-%d %H:%M CST",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
    ):
        try:
            return datetime.strptime(raw, fmt).replace(tzinfo=CN_TZ)
        except ValueError:
            continue
    return None


def parse_hm(raw: str) -> time:
    hour, minute = [int(part) for part in raw.split(":", 1)]
    return time(hour=hour, minute=minute)


def file_href(path: str) -> str:
    if not path or path == "n/a":
        return "#"
    return f"{FILE_SCHEME}://{quote(path)}"


def within_business_window(ts: datetime | None, start_dt: datetime, end_dt: datetime) -> bool:
    return bool(ts and start_dt <= ts <= end_dt)


def day_token(date_text: str) -> str:
    return date.fromisoformat(date_text).strftime("%Y%m%d")


def business_window(date_text: str, start_hm: str, end_hm: str) -> tuple[datetime, datetime]:
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


def source_packet_ts(path: Path, fields: dict[str, str]) -> datetime | None:
    return parse_cst(fields.get("captured_at", "n/a")) or packet_ts_from_name(path)


def label_for_primary_source(value: str) -> str:
    value = clean(value, "n/a").lower()
    mapping = {"yes": "3 / 一手", "partial": "2 / 半一手", "no": "1 / 二手", "n/a": "n/a"}
    return mapping.get(value, value)


def label_for_quality(value: str) -> str:
    value = clean(value, "n/a").lower()
    mapping = {"high": "高", "medium": "中", "low": "低", "low-medium": "偏低", "medium-high": "偏高", "n/a": "n/a"}
    return mapping.get(value, value)


def label_for_visual(value: str) -> str:
    value = clean(value, "n/a")
    mapping = {
        "visual-inputs-detected": "已探测",
        "visual-inputs-missing": "缺素材",
        "n/a": "n/a",
    }
    return mapping.get(value, value)


def load_source_packets(start_dt: datetime, end_dt: datetime) -> list[SourcePacketView]:
    items: list[SourcePacketView] = []
    if not SOURCE_PACKET_DIR.exists():
        return items

    for path in sorted(SOURCE_PACKET_DIR.glob("*__source-packet.md")):
        fields = parse_fields(path)
        if not within_business_window(source_packet_ts(path, fields), start_dt, end_dt):
            continue
        items.append(
            SourcePacketView(
                packet_key=clean(fields.get("packet_key", path.stem)),
                title=clean(fields.get("title", path.stem)),
                summary=clean(fields.get("summary", fields.get("title", path.stem))),
                platform=clean(fields.get("platform", "n/a")),
                source_name=clean(fields.get("source_name", "n/a")),
                source_type=clean(fields.get("source_type", "n/a")),
                captured_at=clean(fields.get("captured_at", "n/a")),
                published_at=clean(fields.get("published_at", "n/a")),
                canonical_url=clean(fields.get("canonical_url", "n/a")),
                primary_source=clean(fields.get("primary_source", "n/a")),
                signal_quality=clean(fields.get("signal_quality", "n/a")),
                citation_reliability=clean(fields.get("citation_reliability", "n/a")),
                visual_evidence_status=clean(fields.get("visual_evidence_status", "n/a")),
                heat_hint=clean(fields.get("heat_hint", "n/a")),
                verification_status=clean(fields.get("verification_status", "n/a")),
                path=str(path),
            )
        )

    items.sort(key=lambda item: parse_cst(item.captured_at) or datetime.min.replace(tzinfo=CN_TZ), reverse=True)
    return items


def parse_score_breakdown(raw: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for part in [chunk.strip() for chunk in clean(raw, "").split("|") if chunk.strip()]:
        match = re.match(r"(.+?)\s+(\d+)$", part)
        if match:
            mapping[clean(match.group(1), "")] = match.group(2)
    return mapping


def parse_top20_pack(path: Path) -> list[Top20Candidate]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    items: list[Top20Candidate] = []
    token = path.name.split("__", 1)[0]
    index = 0
    while index < len(lines):
        match = TOP20_HEADING_RE.match(lines[index].strip())
        if not match:
            index += 1
            continue
        rank = int(match.group(1))
        header_title = clean(match.group(2))
        index += 1
        block: list[str] = []
        while index < len(lines) and not lines[index].startswith("### "):
            block.append(lines[index])
            index += 1
        fields = parse_fields_from_lines(block)
        items.append(
            Top20Candidate(
                rank=rank,
                header_title=header_title,
                title=clean(fields.get("title", header_title)),
                topic_key=clean(fields.get("topic_key", legacy_top20_topic_key(token, rank) or "n/a")),
                primary_platform=clean(fields.get("primary_platform", "n/a")),
                published_at=clean(fields.get("published_at", "n/a")),
                original_link=clean(fields.get("original_link", "n/a")),
                score_total=clean(fields.get("score_total", "n/a")),
                score_breakdown=clean(fields.get("score_breakdown", "n/a")),
                signal_summary=clean(fields.get("signal_summary", "n/a")),
                why_in_top20=clean(fields.get("why_in_top20", fields.get(f"why_top{rank}", "n/a"))),
                visual_assets=clean(fields.get("visual_assets", "n/a")),
                risks=clean(fields.get("risks", "n/a")),
                path=str(path),
            )
        )
    return items


def safe_resolve(path_text: str) -> Path | None:
    value = clean(path_text, "")
    if not value:
        return None
    try:
        return Path(value).expanduser().resolve()
    except Exception:
        return None


def extract_task_sheet_topic_keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    keys: set[str] = set()
    text = path.read_text(encoding="utf-8")
    keys.update(match.group(1).strip() for match in TOPIC_KEY_INLINE_RE.finditer(text))
    in_top6 = False
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("## 全局主池 Top6"):
            in_top6 = True
            continue
        if in_top6 and line.startswith("## ") and not line.startswith("## 全局主池 Top6"):
            in_top6 = False
        if not in_top6:
            continue
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 2 and clean(cells[0], "") != "rank":
            key = clean(cells[1], "")
            if key:
                keys.add(key)
    return {clean(key, "") for key in keys if clean(key, "")}


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


def task_sheet_has_real_content(path: Path) -> bool:
    return bool(extract_task_sheet_topic_keys(path))


def load_approved_topics(
    token: str,
    allowed_source_paths: set[Path] | None = None,
    allowed_topic_keys: set[str] | None = None,
) -> tuple[list[ApprovedTopicView], list[ApprovedTopicView]]:
    items: list[ApprovedTopicView] = []
    mismatched: list[ApprovedTopicView] = []
    allowed = {path.resolve() for path in (allowed_source_paths or set()) if path.exists()}
    allowed_keys = {clean(key, "") for key in (allowed_topic_keys or set()) if clean(key, "")}
    for path in sorted(APPROVED_TOPIC_DIR.glob(f"{token}_*__approved-topic.md")):
        fields = parse_fields(path)
        item = ApprovedTopicView(
            topic_id=clean(fields.get("topic_id", path.stem)),
            topic_key=clean(fields.get("topic_key", path.stem)),
            title=clean(fields.get("title", path.stem)),
            requested_platforms=clean(fields.get("requested_platforms", "n/a")),
            approved_angle=clean(fields.get("approved_angle", "n/a")),
            approved_at=clean(fields.get("approved_at", "n/a")),
            status=clean(fields.get("status", "n/a")),
            selected_rank=clean(fields.get("selected_rank", "n/a")),
            selection_bucket=clean(fields.get("selection_bucket", "n/a")),
            recommended_reason=clean(fields.get("recommended_reason", "n/a")),
            one_line_judgment=clean(fields.get("one_line_judgment", fields.get("approved_angle", "n/a"))),
            risk_note=clean(fields.get("risk_note", "n/a")),
            source_board_path=clean(fields.get("source_board_path", "n/a")),
            path=str(path),
        )
        if allowed:
            source_board = safe_resolve(item.source_board_path)
            if source_board not in allowed:
                mismatched.append(item)
                continue
        if allowed_keys and item.topic_key not in allowed_keys:
            mismatched.append(item)
            continue
        items.append(item)
    items.sort(key=lambda item: parse_cst(item.approved_at) or datetime.min.replace(tzinfo=CN_TZ))
    mismatched.sort(key=lambda item: parse_cst(item.approved_at) or datetime.min.replace(tzinfo=CN_TZ))
    return items, mismatched


def parse_platform_list(raw: str) -> list[str]:
    if not raw or raw == "n/a":
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def read_text(path_text: str) -> str:
    path = Path(path_text)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def extract_first_heading(text: str) -> str:
    for line in text.splitlines():
        match = MD_HEADING_RE.match(line.strip())
        if match:
            title = clean(match.group(1), "n/a")
            if "｜" in title:
                return clean(title.split("｜", 1)[1])
            return title
    return "n/a"


def extract_preview(text: str) -> str:
    lines = text.splitlines()
    capture = False
    for raw_line in lines:
        line = raw_line.strip()
        if line.startswith("## 开头") or line.startswith("## Opening"):
            capture = True
            continue
        if capture:
            if not line or line.startswith("#") or line.startswith("- "):
                continue
            return clean(line, "n/a")
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("- ") or line.startswith(">"):
            continue
        return clean(line, "n/a")
    return "n/a"


def load_draft_cards(date_text: str, topic_ids: set[str], topic_keys: set[str] | None = None) -> tuple[list[DraftCard], dict[str, dict[str, str]]]:
    cards: list[DraftCard] = []
    pack_map: dict[str, dict[str, str]] = {}
    allowed_topic_ids = {clean(topic_id, "") for topic_id in topic_ids if clean(topic_id, "")}
    allowed_topic_keys = {clean(topic_key, "") for topic_key in (topic_keys or set()) if clean(topic_key, "")}
    for pack_card in sorted(DRAFT_PACK_ROOT.glob("*/00_draft-pack-card.md")):
        fields = parse_fields(pack_card)
        topic_id = clean(fields.get("topic_id", "n/a"))
        draft_key = clean(fields.get("draft_key", pack_card.parent.name))
        created_at = clean(fields.get("created_at", "n/a"))
        updated_at = clean(fields.get("updated_at", "n/a"))
        if allowed_topic_ids or allowed_topic_keys:
            if topic_id not in allowed_topic_ids and draft_key not in allowed_topic_keys:
                continue
        elif not created_at.startswith(date_text) and not updated_at.startswith(date_text):
            continue
        pack_status = clean(fields.get("status", "n/a"))
        requested_platforms = parse_platform_list(fields.get("requested_platforms", ""))
        pack_map[draft_key] = {
            "topic_id": topic_id,
            "status": pack_status,
            "updated_at": updated_at,
            "pack_dir": str(pack_card.parent),
            "requested_platforms": ", ".join(requested_platforms),
        }
        for platform in requested_platforms:
            path_key = f"{platform}_path"
            article_path = clean(fields.get(path_key, "n/a"))
            if article_path != "n/a" and Path(article_path).exists():
                text = read_text(article_path)
                cards.append(
                    DraftCard(
                        topic_key=draft_key,
                        topic_id=topic_id,
                        platform=platform,
                        display_title=extract_first_heading(text),
                        preview=extract_preview(text),
                        status=pack_status,
                        updated_at=updated_at,
                        pack_status=pack_status,
                        pack_dir=str(pack_card.parent),
                        file_path=article_path,
                        note="草稿文件已落盘",
                    )
                )
            else:
                cards.append(
                    DraftCard(
                        topic_key=draft_key,
                        topic_id=topic_id,
                        platform=platform,
                        display_title="待生成草稿",
                        preview="该平台槽位已锁题，但对应草稿文件尚未落盘。",
                        status="missing",
                        updated_at=updated_at,
                        pack_status=pack_status,
                        pack_dir=str(pack_card.parent),
                        file_path="n/a",
                        note="平台槽位存在，但稿件缺失",
                    )
                )
    return cards, pack_map


def load_publishable_inventory_cards() -> tuple[list[DraftCard], dict[str, dict[str, str]]]:
    cards: list[DraftCard] = []
    pack_map: dict[str, dict[str, str]] = {}
    publishable_statuses = {"draft_ready", "ready", "waiting_human_publish", "queued", "published"}
    for pack_card in sorted(DRAFT_PACK_ROOT.glob("*/00_draft-pack-card.md")):
        fields = parse_fields(pack_card)
        pack_status = clean(fields.get("status", "n/a"))
        if pack_status not in publishable_statuses:
            continue
        topic_id = clean(fields.get("topic_id", "n/a"))
        draft_key = clean(fields.get("draft_key", pack_card.parent.name))
        updated_at = clean(fields.get("updated_at", "n/a"))
        requested_platforms = parse_platform_list(fields.get("requested_platforms", ""))
        pack_map[draft_key] = {
            "topic_id": topic_id,
            "status": pack_status,
            "updated_at": updated_at,
            "pack_dir": str(pack_card.parent),
            "requested_platforms": ", ".join(requested_platforms),
        }
        for platform in requested_platforms:
            article_path = clean(fields.get(f"{platform}_path", "n/a"))
            if article_path != "n/a" and Path(article_path).exists():
                text = read_text(article_path)
                cards.append(
                    DraftCard(
                        topic_key=draft_key,
                        topic_id=topic_id,
                        platform=platform,
                        display_title=extract_first_heading(text),
                        preview=extract_preview(text),
                        status=pack_status,
                        updated_at=updated_at,
                        pack_status=pack_status,
                        pack_dir=str(pack_card.parent),
                        file_path=article_path,
                        note="库存中存在可预发布稿件",
                    )
                )
    cards.sort(key=lambda item: parse_cst(item.updated_at) or datetime.min.replace(tzinfo=CN_TZ), reverse=True)
    return cards, pack_map


def extract_section(lines: list[str], heading_prefix: str) -> list[str]:
    collected: list[str] = []
    inside = False
    for line in lines:
        if line.startswith(heading_prefix):
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside:
            collected.append(line)
    return collected


def extract_issue_titles(text: str) -> list[str]:
    titles: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("### "):
            continue
        title = clean(line[4:], "")
        title = re.sub(r"^(?:[PM]\d+(?:（.*?）)?|Round\s*\d+|Top\s*\d+)\s*[—\-｜:：]\s*", "", title)
        if not title or title in GENERIC_ISSUE_HEADINGS:
            continue
        titles.append(title)
    return titles


def extract_numbered_actions(text: str) -> list[str]:
    actions: list[str] = []
    lines = text.splitlines()
    inside = False
    for raw_line in lines:
        line = raw_line.rstrip()
        if line.startswith("## 若打回") or line.startswith("## 返工指令"):
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if not inside:
            continue
        stripped = line.strip()
        if re.match(r"^\d+\.\s+", stripped):
            action = re.sub(r"^\d+\.\s+", "", stripped)
            action = re.sub(r"\*\*(.*?)\*\*", r"\1", action)
            actions.append(clean(action))
    return actions


def extract_conclusion(text: str) -> str:
    fields = parse_fields_from_lines(text.splitlines())
    if "结论" in fields:
        return clean(fields["结论"])
    if "status" in fields:
        return clean(fields["status"])
    return "n/a"


def extract_score(text: str) -> str:
    fields = parse_fields_from_lines(text.splitlines())
    return clean(fields.get("score", "n/a"))


def latest_existing(paths: list[Path]) -> Path | None:
    existing = [path for path in paths if path.exists()]
    if not existing:
        return None
    existing.sort(key=lambda item: item.stat().st_mtime)
    return existing[-1]


def resolved_stage_artifact(path: Path, kind: str, accept_state: str = "materialized") -> Path | None:
    report = best_artifact_in_family(path, kind)
    if not state_satisfies(report["state"], accept_state):
        return None
    return Path(report["path"])


def latest_valid_artifact(paths: list[Path], kind: str, accept_state: str = "materialized") -> Path | None:
    valid: list[Path] = []
    for path in paths:
        report = inspect_artifact(path, kind)
        if state_satisfies(report["state"], accept_state):
            valid.append(path)
    if not valid:
        return None
    valid.sort(key=lambda item: item.stat().st_mtime)
    return valid[-1]


def load_scorecard_verdict(path: Path | None) -> dict[str, str]:
    empty = {
        "score": "n/a",
        "raw_status": "n/a",
        "normalized_status": "n/a",
        "continuity_decision": "",
        "continuity_output": "",
    }
    if not path or not path.exists():
        return empty
    report = inspect_artifact(path, "scorecard")
    fields = parse_fields(path)
    verdict = empty.copy()
    verdict["score"] = clean(str(report.get("score", "")), extract_score(path.read_text(encoding="utf-8")))
    verdict["raw_status"] = clean(fields.get("status", "n/a"))
    verdict["normalized_status"] = clean(str(report.get("normalized_status", "")), verdict["raw_status"])
    verdict["continuity_decision"] = clean(str(report.get("continuity_decision", "")), "")
    verdict["continuity_output"] = clean(str(report.get("continuity_output", "")), "")
    return verdict


def scorecard_status_badge(verdict: dict[str, str]) -> str:
    continuity = clean(verdict.get("continuity_decision", ""), "")
    normalized = clean(verdict.get("normalized_status", "n/a"))
    if continuity == "premium_only":
        return "premium_pass"
    if continuity == "continuity_only":
        output = clean(verdict.get("continuity_output", ""), "")
        return f"continuity_only / {output}" if output else "continuity_only"
    if continuity == "stop_for_truth" or normalized == "truth_stop":
        return "stop_for_truth"
    return normalized


def platform_task_log_highlights(fields: dict[str, str]) -> list[str]:
    stage_gate_status = clean(fields.get("stage_gate_status", "")).lower()
    stage_gate_rule = clean(fields.get("stage_gate_rule", ""))
    if "continuity_only" in stage_gate_status:
        return [stage_gate_rule or "continuity_only limited task sheet：3 平台 × 每平台 1 槽位，其余平台进入 holdout"]
    return ["六个主战场 × 每个平台 2 个槽位"]


def build_top20_logs(token: str, top20_pack: Path, platform_task_sheet: Path) -> tuple[list[dict[str, object]], list[str]]:
    logs: list[dict[str, object]] = []
    warnings: list[str] = []

    early_scorecard = TOPIC_CANDIDATE_DIR / f"{token}__top20-screening-pack__stage-gate-scorecard.md"
    top20_redteam = resolved_stage_artifact(LOG_DIR / f"{token}__top20__redteam-review.md", "redteam", "final")
    top20_scorecard = resolved_stage_artifact(LOG_DIR / f"{token}__top20__stage-gate-scorecard.md", "scorecard", "materialized")

    if early_scorecard.exists() and state_satisfies(inspect_artifact(early_scorecard, "scorecard")["state"], "materialized"):
        text = early_scorecard.read_text(encoding="utf-8")
        fields = parse_fields(early_scorecard)
        logs.append(
            {
                "ts": clean(fields.get("generated_at", early_scorecard.name)),
                "role": "market-editor",
                "status": clean(fields.get("status", "rework")),
                "headline": "前置检查：没有 redteam review，裁判暂缓放行",
                "highlights": ["stage-gate 缺少 redteam 前置工序"],
                "source_path": str(early_scorecard),
            }
        )

    if top20_redteam and top20_redteam.exists():
        text = top20_redteam.read_text(encoding="utf-8")
        fields = parse_fields(top20_redteam)
        logs.append(
            {
                "ts": clean(fields.get("generated_at", top20_redteam.name)),
                "role": "redteam-reviewer",
                "status": "rework",
                "headline": clean(fields.get("结论", "红队指出 Top20 存在高优先级问题")),
                "highlights": extract_issue_titles(text)[:3],
                "source_path": str(top20_redteam),
            }
        )

    if top20_scorecard and top20_scorecard.exists():
        text = top20_scorecard.read_text(encoding="utf-8")
        fields = parse_fields(top20_scorecard)
        verdict = load_scorecard_verdict(top20_scorecard)
        status_badge = scorecard_status_badge(verdict)
        logs.append(
            {
                "ts": clean(fields.get("generated_at", top20_scorecard.name)),
                "role": "market-editor",
                "status": status_badge,
                "headline": f"裁判打分 {verdict['score']}，结论 {status_badge}",
                "highlights": extract_numbered_actions(text)[:3] or extract_issue_titles(text)[:3],
                "source_path": str(top20_scorecard),
            }
        )

    if top20_pack.exists():
        fields = parse_fields(top20_pack)
        revision_note = clean(fields.get("revision_note", "n/a"))
        if revision_note != "n/a":
            logs.append(
                {
                    "ts": clean(fields.get("generated_at", top20_pack.name)),
                    "role": "market-scout",
                    "status": "rebuild",
                    "headline": f"返工说明：{revision_note}",
                    "highlights": [],
                    "source_path": str(top20_pack),
                }
            )

    if platform_task_sheet.exists() and task_sheet_has_real_content(platform_task_sheet):
        task_sheet_fields = parse_fields(platform_task_sheet)
        claimed_status = clean(task_sheet_fields.get("stage_gate_status", "n/a"))
        top20_verdict = load_scorecard_verdict(top20_scorecard)
        scorecard_status = top20_verdict["normalized_status"].lower()
        continuity_decision = top20_verdict["continuity_decision"].lower()
        input_pack_path = safe_resolve(task_sheet_fields.get("input_pack", ""))
        input_pack_generated_at = None
        if input_pack_path and input_pack_path.exists():
            input_pack_generated_at = parse_cst(parse_fields(input_pack_path).get("generated_at", ""))
        scorecard_generated_at = None
        if top20_scorecard and top20_scorecard.exists():
            scorecard_generated_at = parse_cst(parse_fields(top20_scorecard).get("generated_at", ""))
        claimed_status_lower = claimed_status.lower()
        if "premium_pass" in claimed_status_lower or (claimed_status_lower == "pass"):
            if scorecard_status != "pass":
                warnings.append(
                    f"平台任务单自称 `{claimed_status}`，但当前能找到的 Top20 最新裁判稿结论仍是 `{scorecard_status or 'n/a'}`。"
                )
        elif "continuity_only" in claimed_status_lower:
            if scorecard_status == "truth_stop" or continuity_decision not in {"continuity_only", ""}:
                warnings.append(
                    "平台任务单已经进入 `continuity_only`，但上游 Top20 最新裁判稿并未给出合法 continuity 放行，请复核 Top20 scorecard。"
                )
        if (
            input_pack_path
            and input_pack_path.name.endswith("__reworked.md")
            and input_pack_generated_at
            and scorecard_generated_at
            and scorecard_generated_at < input_pack_generated_at
        ):
            warnings.append("平台任务单引用了较新的 `__reworked` Top20 包，但尚未看到晚于该包的 Top20 重评分卡，存在绕过裁判稿继续下游的风险。")
    elif platform_task_sheet.exists():
        warnings.append("平台任务单文件已存在，但当前仍是 bootstrap / drafting 占位模板，尚未形成真实锁题结果。")

    logs.sort(key=lambda item: parse_cst(str(item["ts"])) or datetime.min.replace(tzinfo=CN_TZ))
    return logs, warnings


def build_selection_logs(
    token: str,
    approved_topics: list[ApprovedTopicView],
    mismatched_topics: list[ApprovedTopicView],
    platform_task_sheet: Path,
    top5_board: Path,
) -> tuple[list[dict[str, object]], list[str]]:
    logs: list[dict[str, object]] = []
    warnings: list[str] = []

    if top5_board_is_ready(top5_board):
        fields = parse_fields(top5_board)
        logs.append(
            {
                "ts": clean(fields.get("generated_at", top5_board.name)),
                "role": "market-editor",
                "status": "recommend",
                "headline": "先从候选池收束出 Top5 推荐单",
                "highlights": ["本轮用于从 Top20 收缩到更少的优先方向"],
                "source_path": str(top5_board),
            }
        )

    if platform_task_sheet.exists() and task_sheet_has_real_content(platform_task_sheet):
        fields = parse_fields(platform_task_sheet)
        input_pack_path = safe_resolve(fields.get("input_pack", ""))
        logs.append(
            {
                "ts": clean(fields.get("generated_at", platform_task_sheet.name)),
                "role": "topic-planner",
                "status": clean(fields.get("stage_gate_status", "draft")),
                "headline": "生成平台任务单并准备锁题",
                "highlights": platform_task_log_highlights(fields),
                "source_path": str(platform_task_sheet),
            }
        )
        if mismatched_topics:
            mismatched_names = ", ".join(topic.topic_key for topic in mismatched_topics[:6])
            warnings.append(
                f"发现 `{len(mismatched_topics)}` 个同日 approved topic 来自其他轮次任务单，已从本页隐藏：{mismatched_names}"
                + ("…" if len(mismatched_topics) > 6 else "")
            )
    elif platform_task_sheet.exists():
        warnings.append("平台任务单文件已存在，但仍是空模板 / drafting 占位，说明本轮尚未真正产出锁题结果。")

    redteam_path = resolved_stage_artifact(LOG_DIR / f"{token}__platform-task-sheet__redteam-review.md", "redteam", "final")
    scorecard_path = resolved_stage_artifact(LOG_DIR / f"{token}__platform-task-sheet__stage-gate-scorecard.md", "scorecard", "materialized")
    if redteam_path and redteam_path.exists():
        text = redteam_path.read_text(encoding="utf-8")
        fields = parse_fields(redteam_path)
        logs.append(
            {
                "ts": clean(fields.get("generated_at", redteam_path.name)),
                "role": "redteam-reviewer",
                "status": "rework",
                "headline": clean(fields.get("结论", "红队对平台任务单发起攻防")),
                "highlights": extract_issue_titles(text)[:3],
                "source_path": str(redteam_path),
            }
        )

    if scorecard_path and scorecard_path.exists():
        text = scorecard_path.read_text(encoding="utf-8")
        fields = parse_fields(scorecard_path)
        verdict = load_scorecard_verdict(scorecard_path)
        status_badge = scorecard_status_badge(verdict)
        logs.append(
            {
                "ts": clean(fields.get("generated_at", scorecard_path.name)),
                "role": "market-editor",
                "status": status_badge,
                "headline": f"裁判打分 {verdict['score']}，平台任务单结论 {status_badge}",
                "highlights": extract_numbered_actions(text)[:3] or extract_issue_titles(text)[:3],
                "source_path": str(scorecard_path),
            }
        )
        scorecard_status = verdict["normalized_status"].lower()
        continuity_decision = verdict["continuity_decision"].lower()
        continuity_output = verdict["continuity_output"].lower()
        approved_materialization_allowed = (
            scorecard_status == "pass"
            or (continuity_decision == "continuity_only" and continuity_output == "limited_task_sheet")
        )
        if not approved_materialization_allowed and approved_topics:
            warnings.append(f"平台任务单最新裁判状态是 `{scorecard_status}`，但已经物化出 `{len(approved_topics)}` 个 approved topic。")
        scorecard_dt = parse_cst(fields.get("generated_at", ""))
        if scorecard_dt and not approved_materialization_allowed:
            early_approved = [
                topic.topic_key
                for topic in approved_topics
                if topic.path.exists() and datetime.fromtimestamp(topic.path.stat().st_mtime, CN_TZ) < scorecard_dt
            ]
            if early_approved:
                warnings.append(
                    "这些 approved topic 早于平台任务单裁判稿生成："
                    + ", ".join(early_approved[:6])
                    + ("…" if len(early_approved) > 6 else "")
                )

    logs.sort(key=lambda item: parse_cst(str(item["ts"])) or datetime.min.replace(tzinfo=CN_TZ))
    return logs, warnings


def load_review_digest(topic_key: str, requested_platforms: str, pack_status: str) -> ReviewDigest:
    redteam_path = latest_valid_artifact(
        sorted(LOG_DIR.glob(f"*__{topic_key}__content-pack__redteam-review.md")),
        "redteam",
        "final",
    )
    verdict = latest_content_pack_verdict(topic_key)
    scorecard_path = latest_valid_artifact(
        sorted(LOG_DIR.glob(f"*__{topic_key}__content-pack__stage-gate-scorecard.md")),
        "scorecard",
        "materialized",
    )
    if verdict and verdict.path.exists():
        scorecard_path = verdict.path

    redteam_text = redteam_path.read_text(encoding="utf-8") if redteam_path else ""
    scorecard_text = scorecard_path.read_text(encoding="utf-8") if scorecard_path else ""
    redteam_fields = parse_fields(redteam_path) if redteam_path else {}
    scorecard_fields = parse_fields(scorecard_path) if scorecard_path else {}

    last_event_candidates = [
        clean(redteam_fields.get("generated_at", ""), ""),
        clean(scorecard_fields.get("generated_at", ""), ""),
    ]
    last_event_candidates = [value for value in last_event_candidates if value]
    last_event = max(last_event_candidates, key=lambda value: parse_cst(value) or datetime.min.replace(tzinfo=CN_TZ)) if last_event_candidates else "n/a"

    main_failures = extract_issue_titles(redteam_text)[:3] if redteam_text else []
    next_fixes = extract_numbered_actions(scorecard_text)[:3] if scorecard_text else []
    redteam_summary = extract_conclusion(redteam_text) if redteam_text else "尚未进入 content-pack 红队"
    judge_score = verdict.score_text if verdict and verdict.score_text else (extract_score(scorecard_text) if scorecard_text else "n/a")
    judge_status = verdict.normalized_status if verdict else (clean(scorecard_fields.get("status", "n/a")) if scorecard_path else "n/a")

    return ReviewDigest(
        topic_key=topic_key,
        platforms=requested_platforms,
        pack_status=pack_status,
        last_event_at=last_event,
        redteam_summary=redteam_summary,
        judge_score=judge_score,
        judge_status=judge_status,
        main_failures=main_failures,
        next_fixes=next_fixes,
    )


def build_draft_review_digests(cards: list[DraftCard], pack_map: dict[str, dict[str, str]]) -> tuple[list[ReviewDigest], list[str]]:
    topic_keys = sorted(set(card.topic_key for card in cards))
    digests: list[ReviewDigest] = []
    warnings: list[str] = []
    for topic_key in topic_keys:
        pack_info = pack_map.get(topic_key, {})
        digest = load_review_digest(
            topic_key=topic_key,
            requested_platforms=pack_info.get("requested_platforms", "n/a"),
            pack_status=pack_info.get("status", "n/a"),
        )
        digests.append(digest)
        if pack_info.get("status") == "ready" and digest.judge_status == "n/a":
            warnings.append(f"`{topic_key}` 已是 ready，但还没找到 content-pack 红队 / 裁判记录。")
    digests.sort(key=lambda item: item.topic_key)
    return digests, warnings


def metric_counts_by_platform(items: list[SourcePacketView]) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item.platform] = counts.get(item.platform, 0) + 1
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))


def serialise_dataclass_list(items: list[object]) -> list[dict[str, object]]:
    payload: list[dict[str, object]] = []
    for item in items:
        payload.append(item.__dict__)
    return payload


def render_chip(text: str, tone: str = "neutral") -> str:
    return f'<span class="chip chip-{escape(tone)}">{escape(text)}</span>'


def render_metric_card(label: str, value: str, sub: str = "") -> str:
    sub_html = f'<div class="metric-sub">{escape(sub)}</div>' if sub else ""
    return f'<div class="metric-card"><div class="metric-label">{escape(label)}</div><div class="metric-value">{escape(value)}</div>{sub_html}</div>'


def render_warning_list(warnings: list[str]) -> str:
    if not warnings:
        return '<div class="empty-note good-note">当前没发现新的流程穿透问题。</div>'
    items = "".join(f"<li>{escape(item)}</li>" for item in warnings)
    return f'<ul class="warning-list">{items}</ul>'


def render_source_rows(items: list[SourcePacketView]) -> str:
    rows: list[str] = []
    for item in items:
        original_link = (
            f'<a href="{escape(item.canonical_url)}" target="_blank" rel="noreferrer">原文</a>'
            if item.canonical_url != "n/a"
            else "n/a"
        )
        rows.append(
            "<tr>"
            f'<td class="summary-cell"><div class="row-title">{escape(item.summary)}</div><div class="row-sub">{escape(item.title)}</div></td>'
            f"<td>{escape(PLATFORM_CONFIG.get(item.platform, {}).get('label', item.platform))}</td>"
            f"<td>{escape(item.source_name)}</td>"
            f"<td>{escape(item.heat_hint)}</td>"
            f"<td>{escape(label_for_primary_source(item.primary_source))}</td>"
            f"<td>{escape(label_for_quality(item.signal_quality))}</td>"
            f"<td>{escape(label_for_quality(item.citation_reliability))}</td>"
            f"<td>{escape(label_for_visual(item.visual_evidence_status))}</td>"
            f"<td>{escape(item.captured_at)}</td>"
            f"<td>{original_link}</td>"
            "</tr>"
        )
    return "".join(rows)


def render_top20_rows(items: list[Top20Candidate]) -> str:
    rows: list[str] = []
    for item in items:
        breakdown = parse_score_breakdown(item.score_breakdown)
        original_link = (
            f'<a href="{escape(item.original_link)}" target="_blank" rel="noreferrer">原文</a>'
            if item.original_link != "n/a" and item.original_link.startswith("http")
            else escape(item.original_link)
        )
        rows.append(
            "<tr>"
            f"<td>{item.rank}</td>"
            f'<td class="summary-cell"><div class="row-title">{escape(item.header_title)}</div><div class="row-sub">{escape(item.signal_summary)}</div></td>'
            f"<td>{escape(item.primary_platform)}</td>"
            f"<td>{escape(breakdown.get('一手性', 'n/a'))}</td>"
            f"<td>{escape(breakdown.get('传播性', 'n/a'))}</td>"
            f"<td>{escape(breakdown.get('破圈性', 'n/a'))}</td>"
            f"<td>{escape(item.score_total)}</td>"
            f"<td>{escape(item.why_in_top20)}</td>"
            f"<td>{original_link}</td>"
            "</tr>"
        )
    return "".join(rows)


def render_selection_rows(items: list[ApprovedTopicView]) -> str:
    if not items:
        return '<tr><td colspan="8">当前还没有锁题结果；如果这里应当有题，但 Top20 / 任务单 / approved topic 不一致，说明流程存在穿透或 provenance 错配。</td></tr>'
    rows: list[str] = []
    for item in items:
        rows.append(
            "<tr>"
            f"<td>{escape(item.selected_rank)}</td>"
            f'<td class="summary-cell"><div class="row-title">{escape(item.title)}</div><div class="row-sub">{escape(item.one_line_judgment)}</div></td>'
            f"<td>{escape(item.requested_platforms)}</td>"
            f"<td>{escape(item.approved_angle)}</td>"
            f"<td>{escape(item.recommended_reason)}</td>"
            f"<td>{escape(item.status)}</td>"
            f"<td>{escape(item.approved_at)}</td>"
            f'<td><a href="{escape(file_href(item.path))}">任务卡</a></td>'
            "</tr>"
        )
    return "".join(rows)


def render_timeline(logs: list[dict[str, object]]) -> str:
    if not logs:
        return '<div class="empty-note">当前还没有拿到这一环节的攻防记录。</div>'
    cards: list[str] = []
    for item in logs:
        highlights = item.get("highlights") or []
        highlight_html = "".join(f"<li>{escape(str(point))}</li>" for point in highlights)
        cards.append(
            '<div class="timeline-card">'
            f'<div class="timeline-meta">{escape(str(item.get("ts", "n/a")))} · {escape(str(item.get("role", "n/a")))}</div>'
            f'<div class="timeline-headline">{escape(str(item.get("headline", "n/a")))}</div>'
            f'<div class="timeline-status">{render_chip(str(item.get("status", "n/a")), tone_for_status(str(item.get("status", "n/a"))))}</div>'
            + (f"<ul class=\"timeline-points\">{highlight_html}</ul>" if highlight_html else "")
            + f'<div class="timeline-link"><a href="{escape(file_href(str(item.get("source_path", "n/a"))))}">查看文件</a></div>'
            + "</div>"
        )
    return "".join(cards)


def tone_for_status(status: str) -> str:
    status = clean(status, "neutral").lower()
    if any(token in status for token in ("pass", "ready", "ok", "premium_only")):
        return "good"
    if any(token in status for token in ("warn", "recommend", "rebuild", "continuity_only", "drafting")):
        return "warn"
    if any(token in status for token in ("rework", "blocked", "missing", "n/a", "truth_stop", "stop_for_truth")):
        return "bad"
    return "neutral"


def render_platform_lanes(cards: list[DraftCard]) -> str:
    grouped: dict[str, list[DraftCard]] = {platform: [] for platform in PLATFORM_ORDER}
    for card in cards:
        grouped.setdefault(card.platform, []).append(card)

    lane_html: list[str] = []
    for platform in PLATFORM_ORDER:
        config = PLATFORM_CONFIG[platform]
        platform_cards = sorted(grouped.get(platform, []), key=lambda item: (item.status != "ready", item.topic_key))
        if not platform_cards:
            cards_html = '<div class="draft-empty">今日这个平台还没有落到草稿箱的稿件。</div>'
        else:
            card_bits: list[str] = []
            for card in platform_cards:
                file_link = (
                    f'<a href="{escape(file_href(card.file_path))}">打开稿件</a>'
                    if card.file_path != "n/a"
                    else "稿件待生成"
                )
                card_bits.append(
                    f'<div class="draft-card status-{escape(card.status)}">'
                    f'<div class="draft-card-meta">{render_chip(card.status, tone_for_status(card.status))} · {escape(card.updated_at)}</div>'
                    f'<div class="draft-card-title">{escape(card.display_title)}</div>'
                    f'<div class="draft-card-topic">{escape(card.topic_key)}</div>'
                    f'<div class="draft-card-preview">{escape(card.preview)}</div>'
                    f'<div class="draft-card-footer"><span>{escape(card.note)}</span><span>{file_link}</span></div>'
                    "</div>"
                )
            cards_html = "".join(card_bits)
        lane_html.append(
            f'<div class="platform-lane" style="--lane-accent:{escape(config["accent"])}">'
            f'<div class="platform-lane-head"><span>{escape(config["label"])}</span><span>{len(platform_cards)}</span></div>'
            f'<div class="platform-lane-body">{cards_html}</div>'
            "</div>"
        )
    return "".join(lane_html)


def render_review_digest_rows(items: list[ReviewDigest]) -> str:
    rows: list[str] = []
    for item in items:
        failures = "；".join(item.main_failures) if item.main_failures else "尚未进入正式攻防"
        fixes = "；".join(item.next_fixes) if item.next_fixes else "等 redteam / judge 产出整改指令"
        judge = item.judge_score if item.judge_score != "n/a" else item.judge_status
        rows.append(
            "<tr>"
            f"<td>{escape(item.topic_key)}</td>"
            f"<td>{escape(item.platforms)}</td>"
            f"<td>{escape(item.pack_status)}</td>"
            f"<td>{escape(item.last_event_at)}</td>"
            f"<td>{escape(judge)}</td>"
            f"<td>{escape(failures)}</td>"
            f"<td>{escape(fixes)}</td>"
            "</tr>"
        )
    return "".join(rows)


def build_snapshot(args: argparse.Namespace) -> dict[str, object]:
    date_text = args.date
    token = day_token(date_text)
    start_dt, end_dt = business_window(date_text, args.window_start, args.window_end)

    source_packets = load_source_packets(start_dt, end_dt)
    top20_pack_path = TOPIC_CANDIDATE_DIR / f"{token}__top20-screening-pack.md"
    top20_pack_fields = parse_fields(top20_pack_path)
    top20_candidates = parse_top20_pack(top20_pack_path)
    top5_board_path = TOPIC_CANDIDATE_DIR / f"{token}__daily-top8-to-top5.md"
    platform_task_sheet_path = TOPIC_CANDIDATE_DIR / f"{token}__platform-task-sheet.md"
    platform_task_sheet_fields = parse_fields(platform_task_sheet_path)
    selection_source_pack_path = top20_pack_path
    if task_sheet_has_real_content(platform_task_sheet_path):
        task_sheet_input_pack = safe_resolve(platform_task_sheet_fields.get("input_pack", ""))
        if task_sheet_input_pack and task_sheet_input_pack.exists():
            selection_source_pack_path = task_sheet_input_pack
    allowed_source_paths = {
        path
        for path in [top20_pack_path, selection_source_pack_path, platform_task_sheet_path]
        if path.exists()
    }
    if top5_board_is_ready(top5_board_path):
        allowed_source_paths.add(top5_board_path)
    task_sheet_topic_keys = extract_task_sheet_topic_keys(platform_task_sheet_path)
    active_task_sheet_topic_keys = extract_active_task_sheet_topic_keys(platform_task_sheet_path)
    top20_topic_keys, top20_keys_explicit = extract_top20_topic_keys(selection_source_pack_path)
    selection_integrity_warnings: list[str] = []
    selection_integrity: dict[str, object] = {
        "top20_source_path": str(selection_source_pack_path),
        "top20_topic_key_count": len(top20_topic_keys),
        "task_sheet_topic_key_count": len(task_sheet_topic_keys),
        "active_task_sheet_topic_key_count": len(active_task_sheet_topic_keys),
        "top20_keys_explicit": top20_keys_explicit,
        "task_sheet_keys_outside_top20": [],
    }
    allowed_topic_keys = task_sheet_topic_keys
    integrity_target_keys = task_sheet_topic_keys
    stage_gate_status_lower = clean(platform_task_sheet_fields.get("stage_gate_status", "")).lower()
    if "continuity_only" in stage_gate_status_lower and active_task_sheet_topic_keys:
        integrity_target_keys = active_task_sheet_topic_keys
    if top20_topic_keys:
        out_of_pool = sorted(integrity_target_keys - top20_topic_keys)
        selection_integrity["task_sheet_keys_outside_top20"] = out_of_pool
        if out_of_pool:
            selection_integrity_warnings.append(
                ("平台任务单 active slots 包含 Top20 之外的 topic_key：" if integrity_target_keys == active_task_sheet_topic_keys else "平台任务单包含 Top20 之外的 topic_key：")
                + ", ".join(out_of_pool[:8])
                + ("…" if len(out_of_pool) > 8 else "")
            )
        if task_sheet_topic_keys:
            allowed_topic_keys = task_sheet_topic_keys & top20_topic_keys
        else:
            allowed_topic_keys = top20_topic_keys
    elif task_sheet_topic_keys:
        selection_integrity_warnings.append(
            "当前 Top20 包缺少可校验的 topic_key，暂无法核对平台任务单是否完全来自 Top20。"
        )
    approved_topics, mismatched_approved_topics = load_approved_topics(token, allowed_source_paths, allowed_topic_keys)
    draft_filter_topic_keys = {item.topic_key for item in approved_topics}
    if not draft_filter_topic_keys and active_task_sheet_topic_keys:
        draft_filter_topic_keys = set(active_task_sheet_topic_keys)
    elif not draft_filter_topic_keys and allowed_topic_keys:
        draft_filter_topic_keys = set(allowed_topic_keys)
    draft_cards, pack_map = load_draft_cards(
        date_text,
        {item.topic_id for item in approved_topics},
        draft_filter_topic_keys,
    )
    draft_digests, draft_warnings = build_draft_review_digests(draft_cards, pack_map)
    inventory_cards, inventory_pack_map = load_publishable_inventory_cards()

    top20_logs, top20_warnings = build_top20_logs(token, top20_pack_path, platform_task_sheet_path)
    selection_logs, selection_warnings = build_selection_logs(
        token,
        approved_topics,
        mismatched_approved_topics,
        platform_task_sheet_path,
        top5_board_path,
    )

    selection_warnings = selection_integrity_warnings + selection_warnings
    anomalies = top20_warnings + selection_warnings + draft_warnings

    return {
        "meta": {
            "generated_at": datetime.now(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST"),
            "business_date": date_text,
            "intake_scope_label": f"{date_text}（按最新业务窗统计）",
            "business_window_label": f"{start_dt.strftime('%Y-%m-%d %H:%M')} → {end_dt.strftime('%Y-%m-%d %H:%M')} CST",
            "window_start": start_dt.isoformat(),
            "window_end": end_dt.isoformat(),
            "window_rule": (
                f"intake 只统计 captured_at 落在业务窗内的 source packet；"
                f"不是自然日，也不是按文件 token {token} 计数"
            ),
        },
        "counts": {
            "source_packets": len(source_packets),
            "top20": len(top20_candidates),
            "final_topics": len(approved_topics),
            "draft_cards": len(draft_cards),
            "publishable_inventory_cards": len(inventory_cards),
            "anomalies": len(anomalies),
        },
        "sources": {
            "items": serialise_dataclass_list(source_packets),
            "platform_counts": metric_counts_by_platform(source_packets),
        },
        "top20": {
            "pack_path": str(top20_pack_path),
            "generated_at": clean(top20_pack_fields.get("generated_at", "n/a")),
            "revision_note": clean(top20_pack_fields.get("revision_note", "n/a")),
            "candidates": serialise_dataclass_list(top20_candidates),
            "logs": top20_logs,
            "warnings": top20_warnings,
        },
        "selection": {
            "top5_board_path": str(top5_board_path),
            "platform_task_sheet_path": str(platform_task_sheet_path),
            "items": serialise_dataclass_list(approved_topics),
            "hidden_mismatched_items": serialise_dataclass_list(mismatched_approved_topics),
            "integrity": selection_integrity,
            "logs": selection_logs,
            "warnings": selection_warnings,
        },
        "drafts": {
            "items": serialise_dataclass_list(draft_cards),
            "pack_map": pack_map,
            "review_digests": serialise_dataclass_list(draft_digests),
            "inventory_items": serialise_dataclass_list(inventory_cards),
            "inventory_pack_map": inventory_pack_map,
            "warnings": draft_warnings,
        },
        "anomalies": anomalies,
    }


def render_html(snapshot: dict[str, object]) -> str:
    meta = snapshot["meta"]
    counts = snapshot["counts"]
    sources = snapshot["sources"]
    top20 = snapshot["top20"]
    selection = snapshot["selection"]
    drafts = snapshot["drafts"]
    anomalies = snapshot["anomalies"]

    source_items = [SourcePacketView(**item) for item in sources["items"]]
    top20_candidates = [Top20Candidate(**item) for item in top20["candidates"]]
    approved_topics = [ApprovedTopicView(**item) for item in selection["items"]]
    draft_cards = [DraftCard(**item) for item in drafts["items"]]
    review_digests = [ReviewDigest(**item) for item in drafts["review_digests"]]

    platform_count_chips = "".join(
        render_chip(f"{PLATFORM_CONFIG.get(platform, {}).get('label', platform)} {count}", "neutral")
        for platform, count in sources["platform_counts"]
    )
    selection_count_label = f"20 → {len(approved_topics)}"

    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>同行资本市场内容系统｜业务看板</title>
  <style>
    :root {{
      --bg: #0b1020;
      --panel: #11182d;
      --panel-2: #151f39;
      --line: rgba(255,255,255,0.08);
      --text: #edf2ff;
      --muted: #9eb0d9;
      --good: #1ec98f;
      --warn: #f59e0b;
      --bad: #ff5d73;
      --chip: rgba(255,255,255,0.08);
      --shadow: 0 14px 40px rgba(0,0,0,0.28);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Helvetica Neue", sans-serif;
      background:
        radial-gradient(circle at top right, rgba(0,168,255,0.10), transparent 25%),
        radial-gradient(circle at top left, rgba(7,193,96,0.10), transparent 30%),
        var(--bg);
      color: var(--text);
      line-height: 1.55;
    }}
    a {{ color: #8ec5ff; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .page {{
      max-width: 1600px;
      margin: 0 auto;
      padding: 28px 24px 72px;
    }}
    .hero {{
      background: linear-gradient(135deg, rgba(18,28,52,0.94), rgba(22,34,60,0.96));
      border: 1px solid var(--line);
      border-radius: 24px;
      padding: 28px;
      box-shadow: var(--shadow);
      margin-bottom: 20px;
    }}
    .hero h1 {{
      margin: 0 0 10px;
      font-size: 34px;
      line-height: 1.2;
    }}
    .hero-meta {{
      color: var(--muted);
      margin-bottom: 18px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px 18px;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }}
    .metric-card {{
      background: rgba(255,255,255,0.03);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 16px 18px;
    }}
    .metric-label {{ color: var(--muted); font-size: 13px; margin-bottom: 8px; }}
    .metric-value {{ font-size: 28px; font-weight: 700; }}
    .metric-sub {{ color: var(--muted); font-size: 12px; margin-top: 6px; }}
    .warning-panel {{
      background: rgba(255,93,115,0.08);
      border: 1px solid rgba(255,93,115,0.24);
      border-radius: 18px;
      padding: 16px 18px;
    }}
    .warning-panel h3 {{ margin: 0 0 10px; font-size: 16px; }}
    .warning-list {{ margin: 0; padding-left: 18px; color: #ffd5db; }}
    .warning-list li + li {{ margin-top: 8px; }}
    .good-note {{
      color: #d4ffef;
      background: rgba(30,201,143,0.10);
      border: 1px solid rgba(30,201,143,0.22);
      border-radius: 14px;
      padding: 12px 14px;
    }}
    .jump-nav {{
      position: sticky;
      top: 0;
      z-index: 30;
      backdrop-filter: blur(16px);
      background: rgba(11, 16, 32, 0.82);
      border-bottom: 1px solid rgba(255,255,255,0.05);
      padding: 12px 0 14px;
      margin: 0 0 22px;
    }}
    .jump-nav-inner {{
      max-width: 1600px;
      margin: 0 auto;
      padding: 0 24px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .jump-nav a {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(255,255,255,0.05);
      border: 1px solid var(--line);
      color: var(--text);
      font-size: 14px;
    }}
    .section {{
      background: linear-gradient(180deg, rgba(18,24,41,0.96), rgba(15,21,36,0.98));
      border: 1px solid var(--line);
      border-radius: 22px;
      padding: 24px;
      box-shadow: var(--shadow);
      margin-bottom: 22px;
    }}
    .section-head {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 14px;
      margin-bottom: 14px;
    }}
    .section h2 {{
      margin: 0;
      font-size: 24px;
      line-height: 1.25;
    }}
    .section-sub {{
      color: var(--muted);
      margin-top: 6px;
      font-size: 14px;
    }}
    .chips {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }}
    .chip {{
      display: inline-flex;
      align-items: center;
      padding: 5px 10px;
      border-radius: 999px;
      font-size: 12px;
      background: var(--chip);
      border: 1px solid var(--line);
      color: var(--text);
    }}
    .chip-good {{ background: rgba(30,201,143,0.10); color: #cbffef; border-color: rgba(30,201,143,0.26); }}
    .chip-warn {{ background: rgba(245,158,11,0.12); color: #ffe2a7; border-color: rgba(245,158,11,0.28); }}
    .chip-bad {{ background: rgba(255,93,115,0.12); color: #ffd5db; border-color: rgba(255,93,115,0.28); }}
    .chip-neutral {{ background: rgba(255,255,255,0.06); }}
    .stage-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }}
    .status-card {{
      background: rgba(255,255,255,0.03);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 14px 16px;
    }}
    .status-card strong {{ display: block; font-size: 15px; margin-bottom: 6px; }}
    .table-wrap {{
      width: 100%;
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 18px;
      background: rgba(8,12,24,0.45);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 1080px;
    }}
    th, td {{
      padding: 12px 14px;
      vertical-align: top;
      border-bottom: 1px solid var(--line);
      font-size: 14px;
    }}
    th {{
      position: sticky;
      top: 0;
      background: rgba(14,21,38,0.98);
      text-align: left;
      color: var(--muted);
      z-index: 1;
    }}
    tr:hover td {{ background: rgba(255,255,255,0.02); }}
    .summary-cell {{ min-width: 320px; }}
    .row-title {{ font-weight: 700; margin-bottom: 4px; }}
    .row-sub {{ color: var(--muted); font-size: 13px; }}
    .timeline {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 12px;
      margin-top: 14px;
    }}
    .timeline-card {{
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.03);
      border-radius: 18px;
      padding: 14px 16px;
    }}
    .timeline-meta {{ color: var(--muted); font-size: 12px; margin-bottom: 8px; }}
    .timeline-headline {{ font-weight: 700; margin-bottom: 8px; }}
    .timeline-status {{ margin-bottom: 10px; }}
    .timeline-points {{ margin: 0; padding-left: 18px; color: var(--muted); }}
    .timeline-points li + li {{ margin-top: 6px; }}
    .timeline-link {{ margin-top: 12px; font-size: 13px; }}
    .platform-board {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 14px;
    }}
    .platform-lane {{
      background: rgba(255,255,255,0.03);
      border: 1px solid var(--line);
      border-radius: 18px;
      overflow: hidden;
      min-height: 220px;
    }}
    .platform-lane-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 14px;
      font-weight: 700;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(90deg, color-mix(in srgb, var(--lane-accent) 24%, transparent), rgba(255,255,255,0.02));
    }}
    .platform-lane-body {{
      padding: 12px;
      display: grid;
      gap: 10px;
    }}
    .draft-card {{
      background: rgba(8,12,24,0.66);
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 12px;
      display: grid;
      gap: 8px;
    }}
    .draft-card.status-missing {{
      border-style: dashed;
      background: rgba(255,93,115,0.05);
    }}
    .draft-card-meta {{
      color: var(--muted);
      font-size: 12px;
    }}
    .draft-card-title {{
      font-weight: 700;
      font-size: 15px;
      line-height: 1.4;
    }}
    .draft-card-topic {{
      color: #91a9df;
      font-size: 12px;
      word-break: break-all;
    }}
    .draft-card-preview {{
      color: var(--muted);
      font-size: 13px;
      min-height: 44px;
    }}
    .draft-card-footer {{
      display: flex;
      justify-content: space-between;
      gap: 10px;
      font-size: 12px;
      color: var(--muted);
    }}
    .draft-empty {{
      padding: 16px;
      border: 1px dashed var(--line);
      border-radius: 14px;
      color: var(--muted);
      text-align: center;
    }}
    .empty-note {{
      color: var(--muted);
      background: rgba(255,255,255,0.03);
      border: 1px dashed var(--line);
      border-radius: 14px;
      padding: 12px 14px;
    }}
    .search-box {{
      width: min(420px, 100%);
      margin: 0 0 14px;
      padding: 12px 14px;
      border-radius: 14px;
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--line);
      color: var(--text);
      outline: none;
    }}
    .footnote {{
      color: var(--muted);
      font-size: 13px;
      margin-top: 12px;
    }}
    @media (max-width: 900px) {{
      .page {{ padding: 20px 14px 56px; }}
      .hero h1 {{ font-size: 28px; }}
      .section {{ padding: 18px; }}
      .section-head {{ flex-direction: column; }}
      .chips {{ justify-content: flex-start; }}
    }}
  </style>
</head>
<body>
  <div class="jump-nav">
    <div class="jump-nav-inner">
      <a href="#intake">① 信息 Intake</a>
      <a href="#top20">② Top20</a>
      <a href="#selection">③ 最终锁题</a>
      <a href="#drafts">④ 稿件池</a>
    </div>
  </div>
  <main class="page">
    <section class="hero">
      <h1>同行资本市场内容系统｜业务可视化看板</h1>
      <div class="hero-meta">
        <span>业务日：{escape(str(meta["business_date"]))}</span>
        <span>Intake 口径：{escape(str(meta["intake_scope_label"]))}</span>
        <span>流程时窗：{escape(str(meta["business_window_label"]))}</span>
        <span>规则：{escape(str(meta["window_rule"]))}</span>
        <span>生成时间：{escape(str(meta["generated_at"]))}</span>
      </div>
      <div class="metrics">
        {render_metric_card("今日获取的信息", str(counts["source_packets"]), "按业务窗统计，不按自然日")}
        {render_metric_card("Top20 候选", str(counts["top20"]), "signal-scout 收束后的正式候选")}
        {render_metric_card("最终锁题", str(counts["final_topics"]), "approved topic 唯一 topic 数")}
        {render_metric_card("平台稿件卡", str(counts["draft_cards"]), "真实草稿文件 + 待生成槽位")}
        {render_metric_card("流程异常", str(counts["anomalies"]), "用于暴露当前链路穿透与断点")}
      </div>
      <div class="warning-panel">
        <h3>当前最该盯的异常</h3>
        {render_warning_list(list(anomalies))}
      </div>
    </section>

    <section id="intake" class="section">
      <div class="section-head">
        <div>
          <h2>① 今日获取的信息</h2>
          <div class="section-sub">先看最新业务日真实归档了什么，再决定后面的筛选是不是站得住。</div>
        </div>
        <div class="chips">
          {render_chip(f"共 {len(source_items)} 条", "good")}
          {platform_count_chips}
        </div>
      </div>
      <div class="stage-grid">
        <div class="status-card"><strong>业务日归档</strong>{escape(str(meta["intake_scope_label"]))}</div>
        <div class="status-card"><strong>流程时窗</strong>{escape(str(meta["business_window_label"]))}</div>
        <div class="status-card"><strong>一手性字段</strong>用 `primary_source` 显示官方 / 半一手 / 二手</div>
        <div class="status-card"><strong>热度字段</strong>优先展示 `heat_hint`，不强行伪造统一分数</div>
        <div class="status-card"><strong>可视素材</strong>直接展示 `visual_evidence_status`，方便看图文能力缺口</div>
      </div>
      <input class="search-box" id="sourceSearch" type="search" placeholder="筛今天拿到的线索：输入关键词 / 平台 / 来源名">
      <div class="table-wrap">
        <table id="sourceTable">
          <thead>
            <tr>
              <th>一句话概述</th>
              <th>平台</th>
              <th>来源</th>
              <th>热度线索</th>
              <th>一手性</th>
              <th>信号质量</th>
              <th>引用可靠度</th>
              <th>图片可用性</th>
              <th>抓取时间</th>
              <th>原文链接</th>
            </tr>
          </thead>
          <tbody>
            {render_source_rows(source_items)}
          </tbody>
        </table>
      </div>
      <div class="footnote">这块刻意不直接用“覆盖度”打分，因为 stage 1 的职责是把真实输入拿回来；覆盖度与破圈验证在后续 Top20 / 锁题阶段再算更合理。</div>
    </section>

    <section id="top20" class="section">
      <div class="section-head">
        <div>
          <h2>② 今日入选 Top20</h2>
          <div class="section-sub">看 signal-scout 把什么送进了候选池，以及这一轮攻防到底把哪些问题打出来了。</div>
        </div>
        <div class="chips">
          {render_chip(f"Top20 {len(top20_candidates)} 条", "good")}
          {render_chip(f"revision: {str(top20['revision_note'])}", "warn" if str(top20["revision_note"]) != "n/a" else "neutral")}
          {render_chip("看板会主动标记文件不一致", "bad" if top20["warnings"] else "good")}
        </div>
      </div>
      <div class="stage-grid">
        <div class="status-card"><strong>当前包</strong><a href="{escape(file_href(str(top20["pack_path"])))}">{escape(Path(str(top20["pack_path"])).name)}</a></div>
        <div class="status-card"><strong>包生成时间</strong>{escape(str(top20["generated_at"]))}</div>
        <div class="status-card"><strong>流程告警</strong>{escape(top20["warnings"][0] if top20["warnings"] else "当前未发现额外告警")}</div>
      </div>
      {render_warning_list(list(top20["warnings"]))}
      <div class="table-wrap" style="margin-top:14px;">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>入选信息</th>
              <th>主平台</th>
              <th>一手性</th>
              <th>传播性</th>
              <th>破圈性</th>
              <th>总分</th>
              <th>入选原因</th>
              <th>原文链接</th>
            </tr>
          </thead>
          <tbody>
            {render_top20_rows(top20_candidates)}
          </tbody>
        </table>
      </div>
      <h3 style="margin:18px 0 10px;">Top20 攻防记录</h3>
      <div class="timeline">
        {render_timeline(list(top20["logs"]))}
      </div>
    </section>

    <section id="selection" class="section">
      <div class="section-head">
        <div>
          <h2>③ 20 进几，最后留下了谁</h2>
          <div class="section-sub">这里按真实 downstream 对象展示：当前已经物化成 approved topic 的唯一题目集合。</div>
        </div>
        <div class="chips">
          {render_chip(selection_count_label, "good")}
          {render_chip("approved topic = 真正往下游走的对象", "neutral")}
        </div>
      </div>
      <div class="stage-grid">
        <div class="status-card"><strong>Top5 推荐板</strong><a href="{escape(file_href(str(selection["top5_board_path"])))}">{escape(Path(str(selection["top5_board_path"])).name)}</a></div>
        <div class="status-card"><strong>平台任务单</strong><a href="{escape(file_href(str(selection["platform_task_sheet_path"])))}">{escape(Path(str(selection["platform_task_sheet_path"])).name)}</a></div>
        <div class="status-card"><strong>当前流程风险</strong>{escape(selection["warnings"][0] if selection["warnings"] else "没有发现平台锁题穿透")}</div>
      </div>
      {render_warning_list(list(selection["warnings"]))}
      <div class="table-wrap" style="margin-top:14px;">
        <table>
          <thead>
            <tr>
              <th>原序号</th>
              <th>最终留下的题</th>
              <th>目标平台</th>
              <th>锁题角度</th>
              <th>入选原因</th>
              <th>状态</th>
              <th>锁题时间</th>
              <th>任务卡</th>
            </tr>
          </thead>
          <tbody>
            {render_selection_rows(approved_topics)}
          </tbody>
        </table>
      </div>
      <h3 style="margin:18px 0 10px;">锁题攻防记录</h3>
      <div class="timeline">
        {render_timeline(list(selection["logs"]))}
      </div>
    </section>

    <section id="drafts" class="section">
      <div class="section-head">
        <div>
          <h2>④ 稿件池 / 平台草稿箱</h2>
          <div class="section-sub">这块先做成虚拟草稿箱，但全部基于真实 draft pack 和平台稿文件渲染，不贴历史大版本，只展示当前成品与攻防要点。</div>
        </div>
        <div class="chips">
          {render_chip(f"草稿卡 {len(draft_cards)} 张", "good")}
          {render_chip(f"攻防摘要 {len(review_digests)} 条", "neutral")}
        </div>
      </div>
      {render_warning_list(list(drafts["warnings"]))}
      <div class="platform-board" style="margin-top:14px;">
        {render_platform_lanes(draft_cards)}
      </div>
      <h3 style="margin:22px 0 10px;">成品攻防摘要</h3>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>topic</th>
              <th>平台</th>
              <th>pack 状态</th>
              <th>最后动作</th>
              <th>裁判分 / 状态</th>
              <th>本轮主要不合格</th>
              <th>下一步该改什么</th>
            </tr>
          </thead>
          <tbody>
            {render_review_digest_rows(review_digests)}
          </tbody>
        </table>
      </div>
      <div class="footnote">如果你想看某一篇的全过程，这里会给你当前最新 redteam / scorecard 的摘要；不会把历史整稿直接贴满页面。</div>
    </section>
  </main>
  <script>
    const searchInput = document.getElementById('sourceSearch');
    const sourceTable = document.getElementById('sourceTable');
    if (searchInput && sourceTable) {{
      searchInput.addEventListener('input', (event) => {{
        const keyword = event.target.value.trim().toLowerCase();
        const rows = sourceTable.querySelectorAll('tbody tr');
        rows.forEach((row) => {{
          const text = row.innerText.toLowerCase();
          row.style.display = !keyword || text.includes(keyword) ? '' : 'none';
        }});
      }});
    }}
  </script>
</body>
</html>
"""
    return html


def main() -> None:
    args = parse_args()
    snapshot = build_snapshot(args)
    html = render_html(snapshot)

    if args.write:
        FRONTSTAGE_DIR.mkdir(parents=True, exist_ok=True)
        token = day_token(args.date)
        html_path = FRONTSTAGE_DIR / f"{token}__market-ops-dashboard.html"
        json_path = FRONTSTAGE_DIR / f"{token}__market-ops-dashboard.snapshot.json"
        html_path.write_text(html, encoding="utf-8")
        json_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
        print(str(html_path))
        print(str(json_path))
        return

    print(html)


if __name__ == "__main__":
    main()

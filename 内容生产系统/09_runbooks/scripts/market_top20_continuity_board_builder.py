#!/usr/bin/env python3
from __future__ import annotations

import argparse
from difflib import SequenceMatcher
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
TOPIC_DIR = ROOT / "03_topic_candidates"
LOG_DIR = ROOT / "10_logs"
CN_TZ = ZoneInfo("Asia/Shanghai")
FIELD_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
TOP20_HEADING_RE = re.compile(r"^###\s+(\d+)\.\s+(.+)$")
MINISLATE_HEADER_RE = re.compile(r"^##\s+top20_mini_slate", re.I)
RANK_REF_RE = re.compile(r"#(\d+)")
MINISLATE_RANK_RE = re.compile(r"^#?(\d+)$")
MINISLATE_RANK_WITH_TITLE_RE = re.compile(r"^#?(\d+)\s+(.+)$")
INLINE_KV_RE = re.compile(r"`?([0-9A-Za-z_\-\u4e00-\u9fff]+)`?\s*=\s*`?([^`、|]+)`?")
MINISLATE_PRIORITY_HEADER_RE = re.compile(r"^###\s+(P\d+)\b", re.I)
TRUTH_STOP_TOKENS = (
    "truth_stop",
    "stop_for_truth",
    "truth failure",
    "事实失真",
    "方向严重偏离",
    "不可继续",
)
COMMUNITY_DOMAINS = {"news.ycombinator.com", "old.reddit.com", "reddit.com", "github.com"}
OFFICIAL_DOMAINS = {"openai.com", "anthropic.com", "huggingface.co", "blog.google", "deepmind.google", "googleblog.com"}
MAINSTREAM_DOMAINS = {
    "wired.com",
    "nytimes.com",
    "theverge.com",
    "techcrunch.com",
    "infoq.com",
    "36kr.com",
    "qbitai.com",
    "jiqizhixin.com",
    "geekpark.net",
    "sspai.com",
    "zhihu.com",
    "mp.weixin.qq.com",
}
TABLE_FIELD_HEADER_KEYS = {"字段", "值", "项目", "说明", "维度", "评估", "问题项", "类型", "严重度", "后果", "候选", "顺位"}


@dataclass(frozen=True)
class PackCandidate:
    rank: int
    topic_key: str
    title: str
    primary_platform: str
    published_at: str
    original_link: str
    score_total: str
    why_in_top20: str
    signal_summary: str
    risks: str
    source_packet: str
    deep_article: str
    asset_chain: str


@dataclass(frozen=True)
class SlateCandidate:
    priority: str
    topic_key: str
    note: str
    enter_condition: str
    source_mode: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a continuity-safe Top5/Holdout board when Top20 is in truthful rework."
    )
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical date in YYYY-MM-DD.")
    parser.add_argument("--top-count", type=int, default=5, help="How many active slots to keep in Top5.")
    parser.add_argument("--holdout-count", type=int, default=3, help="How many reserve slots to keep as Holdout.")
    parser.add_argument(
        "--allow-inferred-recovery",
        action="store_true",
        help="When scorecard did not explicitly emit top20_mini_slate, infer a truthful continuity board from the pack plus scorecard hard blocks.",
    )
    parser.add_argument(
        "--min-score-for-inference",
        type=float,
        default=6.0,
        help="Minimum Top20 score required before inferred continuity recovery is allowed.",
    )
    parser.add_argument("--write", action="store_true", help="Write the board to 03_topic_candidates.")
    return parser.parse_args()


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`").strip()
    return value if value else fallback


def day_token(date_text: str) -> str:
    return date.fromisoformat(date_text).strftime("%Y%m%d")


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def parse_fields_from_lines(lines: list[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in lines:
        stripped = raw_line.strip()
        match = FIELD_RE.match(stripped)
        if match:
            key, value = match.groups()
            fields[clean(key, "")] = clean(value, "")
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [clean(cell, "") for cell in stripped.strip("|").split("|")]
            if len(cells) >= 2:
                key = clean(cells[0], "")
                value = clean(cells[1], "")
                if key and key not in TABLE_FIELD_HEADER_KEYS and not re.fullmatch(r"[-: ]+", key):
                    fields[key] = value
            continue
        if stripped.startswith(">"):
            for key, value in INLINE_KV_RE.findall(stripped):
                normalized_key = clean(key, "")
                normalized_value = clean(value, "")
                if normalized_key and normalized_value:
                    fields[normalized_key] = normalized_value
    return fields


def parse_fields(path: Path) -> dict[str, str]:
    return parse_fields_from_lines(path.read_text(encoding="utf-8").splitlines()) if path.exists() else {}


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_table_rows(lines: list[str], header_matcher: re.Pattern[str]) -> list[list[str]]:
    rows: list[list[str]] = []
    in_section = False
    table_started = False
    for raw_line in lines:
        line = raw_line.rstrip()
        if header_matcher.match(line):
            in_section = True
            continue
        if not in_section:
            continue
        if line.startswith("## ") and not header_matcher.match(line):
            break
        if not line.strip():
            if table_started:
                break
            continue
        if line.lstrip().startswith("|"):
            table_started = True
            rows.append(split_row(line))
            continue
        if table_started:
            break
    if len(rows) < 2:
        return []
    cleaned: list[list[str]] = []
    for row in rows[1:]:
        joined = "".join(cell.replace("-", "").replace(" ", "") for cell in row)
        if not joined:
            continue
        cleaned.append(row)
    return cleaned


def parse_table_rows_all(lines: list[str], header_matcher: re.Pattern[str]) -> list[list[str]]:
    rows: list[list[str]] = []
    in_section = False
    current_table: list[list[str]] = []

    def flush_current() -> None:
        nonlocal current_table
        if len(current_table) >= 2:
            for row in current_table[1:]:
                joined = "".join(cell.replace("-", "").replace(" ", "") for cell in row)
                if not joined:
                    continue
                rows.append(row)
        current_table = []

    for raw_line in lines:
        line = raw_line.rstrip()
        if header_matcher.match(line):
            in_section = True
            current_table = []
            continue
        if not in_section:
            continue
        if line.startswith("## ") and not header_matcher.match(line):
            break
        if line.lstrip().startswith("|"):
            current_table.append(split_row(line))
            continue
        if current_table:
            flush_current()
    flush_current()
    return rows


def normalize_header_cell(cell: str) -> str:
    normalized = clean(cell, "").lower().replace(" ", "").replace("-", "_")
    return normalized.replace("`", "")


def parse_score_value(raw: str) -> float | None:
    text = clean(raw, "")
    if not text:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)", text)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def extract_total_score(scorecard_text: str, fields: dict[str, str]) -> float | None:
    direct = parse_score_value(fields.get("score", ""))
    if direct is not None:
        return direct
    for raw_line in scorecard_text.splitlines():
        if "综合得分" not in raw_line and "综合评分" not in raw_line:
            continue
        parsed = parse_score_value(raw_line)
        if parsed is not None:
            return parsed
    return None


def parse_published_day(raw: str) -> date | None:
    value = clean(raw, "")
    if not value or value in {"unknown", "n/a"}:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S CST", "%Y-%m-%d %H:%M CST", "%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    match = re.search(r"(\d{4})-(\d{2})-(\d{2})", value)
    if match:
        return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return None


def normalize_continuity_decision(raw: str) -> str:
    text = clean(raw, "").lower()
    if not text:
        return ""
    if any(token in text for token in ("premium_only", "premium pass", "premium_pass")):
        return "premium_only"
    if any(token in text for token in ("continuity_only", "mini_slate", "limited_task_sheet")):
        return "continuity_only"
    if any(token in text for token in TRUTH_STOP_TOKENS):
        return "stop_for_truth"
    return text


def normalize_continuity_output(raw: str) -> str:
    text = clean(raw, "").lower()
    if not text:
        return ""
    if "top20_mini_slate" in text or "mini slate" in text:
        return "top20_mini_slate"
    if "limited_task_sheet" in text or "limited task sheet" in text:
        return "limited_task_sheet"
    if "backlog_publish" in text:
        return "backlog_publish"
    if "carry_rework_backlog" in text:
        return "carry_rework_backlog"
    if "none" == text:
        return "none"
    return text


def parse_pack(path: Path) -> list[PackCandidate]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    items: list[PackCandidate] = []
    index = 0
    while index < len(lines):
        match = TOP20_HEADING_RE.match(lines[index].strip())
        if not match:
            index += 1
            continue
        rank = int(match.group(1))
        heading_title = clean(match.group(2))
        index += 1
        block: list[str] = []
        while index < len(lines) and not TOP20_HEADING_RE.match(lines[index].strip()):
            block.append(lines[index])
            index += 1
        fields = parse_fields_from_lines(block)
        topic_key = clean(fields.get("topic_key", ""), "")
        if not topic_key:
            continue
        items.append(
            PackCandidate(
                rank=rank,
                topic_key=topic_key,
                title=clean(fields.get("title", heading_title)),
                primary_platform=clean(fields.get("primary_platform", "n/a")),
                published_at=clean(fields.get("published_at", "n/a")),
                original_link=clean(fields.get("original_link", "n/a")),
                score_total=clean(fields.get("score_total", "n/a")),
                why_in_top20=clean(fields.get("why_in_top20", "n/a")),
                signal_summary=clean(fields.get("signal_summary", "n/a")),
                risks=clean(fields.get("risks", "n/a")),
                source_packet=clean(fields.get("source_packet", "n/a")),
                deep_article=clean(fields.get("deep_article", "n/a")),
                asset_chain=clean(fields.get("asset_chain", "n/a")),
            )
        )
    return items


def pack_map(items: list[PackCandidate]) -> dict[str, PackCandidate]:
    return {item.topic_key: item for item in items}


def normalize_lookup_text(raw: str) -> str:
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", clean(raw, "").lower())


def merge_pack_items(*groups: list[PackCandidate]) -> list[PackCandidate]:
    merged: dict[str, PackCandidate] = {}
    for group in groups:
        for item in group:
            merged[item.topic_key] = item
    return list(merged.values())


def titles_look_aligned(left: str, right: str) -> bool:
    normalized_left = normalize_lookup_text(left)
    normalized_right = normalize_lookup_text(right)
    if not normalized_left or not normalized_right:
        return False
    if normalized_left in normalized_right or normalized_right in normalized_left:
        return True
    return SequenceMatcher(None, normalized_left, normalized_right).find_longest_match().size >= 4


def parse_mini_slate(scorecard_text: str, pack_items: list[PackCandidate]) -> list[SlateCandidate]:
    pack_by_rank = {item.rank: item for item in pack_items}
    pack_by_title = {normalize_lookup_text(item.title): item for item in pack_items}
    parsed: list[SlateCandidate] = []
    in_section = False
    current_priority = ""
    current_table: list[list[str]] = []

    def process_table(table_rows: list[list[str]], section_priority: str) -> None:
        if len(table_rows) < 2:
            return
        header_row = table_rows[0]
        header_index = {
            normalize_header_cell(header): index
            for index, header in enumerate(header_row)
            if normalize_header_cell(header)
        }

        def cell(row: list[str], *header_options: str) -> str:
            for option in header_options:
                index = header_index.get(option)
                if index is not None and index < len(row):
                    return clean(row[index], "")
            return ""

        for row in table_rows[1:]:
            joined = "".join(cell_value.replace("-", "").replace(" ", "") for cell_value in row)
            if not joined:
                continue

            priority = section_priority or cell(row, "优先级", "priority")
            rank_value = cell(row, "#", "顺位", "rank")
            title = cell(row, "候选", "题目", "title", "candidate")
            topic_key = cell(row, "topic_key", "candidate_key")
            enter_condition = cell(row, "进入条件", "enter_condition", "truth_verdict", "score")
            note = title

            item = None
            rank_match = MINISLATE_RANK_RE.fullmatch(rank_value)
            rank_with_title_match = MINISLATE_RANK_WITH_TITLE_RE.fullmatch(rank_value)

            if topic_key:
                if rank_match:
                    item = pack_by_rank.get(int(rank_match.group(1)))
                title_item = pack_by_title.get(normalize_lookup_text(title)) if title else None
                if title_item is not None:
                    item = title_item
                if not note and item is not None:
                    note = item.title
            elif rank_match and title:
                rank = int(rank_match.group(1))
                item = pack_by_rank.get(rank)
                title_item = pack_by_title.get(normalize_lookup_text(title)) if title else None
                if title_item is not None:
                    item = title_item
                elif item is not None and not titles_look_aligned(title, item.title):
                    item = None
                if item is not None:
                    topic_key = item.topic_key
                    note = title or item.title
            elif rank_with_title_match:
                rank = int(rank_with_title_match.group(1))
                embedded_title = clean(rank_with_title_match.group(2), "")
                item = pack_by_rank.get(rank)
                title_item = pack_by_title.get(normalize_lookup_text(embedded_title)) if embedded_title else None
                if title_item is not None:
                    item = title_item
                elif item is not None and embedded_title and not titles_look_aligned(embedded_title, item.title):
                    item = None
                if item is not None:
                    topic_key = item.topic_key
                note = embedded_title or (item.title if item is not None else "")

            if not topic_key or topic_key.lower() in {"topic_key", "candidate_key"}:
                continue
            parsed.append(
                SlateCandidate(
                    priority=priority,
                    topic_key=topic_key,
                    note=note,
                    enter_condition=enter_condition,
                    source_mode="explicit_top20_mini_slate",
                )
            )

    for raw_line in scorecard_text.splitlines():
        line = raw_line.rstrip()
        if MINISLATE_HEADER_RE.match(line):
            in_section = True
            current_priority = ""
            current_table = []
            continue
        if not in_section:
            continue
        if line.startswith("## ") and not MINISLATE_HEADER_RE.match(line):
            break
        priority_match = MINISLATE_PRIORITY_HEADER_RE.match(line.strip())
        if priority_match:
            if current_table:
                process_table(current_table, current_priority)
                current_table = []
            current_priority = clean(priority_match.group(1), "").upper()
            continue
        if line.lstrip().startswith("|"):
            current_table.append(split_row(line))
            continue
        if current_table:
            process_table(current_table, current_priority)
            current_table = []

    if current_table:
        process_table(current_table, current_priority)
    return parsed


def is_truth_stop(fields: dict[str, str]) -> bool:
    decisive_fields = [
        clean(fields.get("status", ""), ""),
        clean(fields.get("continuity_decision", ""), ""),
        clean(fields.get("continuity_output", ""), ""),
        clean(fields.get("status_rule", ""), ""),
    ]
    combined = " | ".join(decisive_fields).lower()
    if not combined.strip():
        return False
    if "非 truth failure" in combined or "not truth failure" in combined:
        return False
    return any(token in combined for token in TRUTH_STOP_TOKENS)


def hard_block_ranks_from_scorecard(scorecard_text: str) -> set[int]:
    blocked: set[int] = set()
    for raw_line in scorecard_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lowered = line.lower()
        hard_block = any(
            token in lowered
            for token in (
                "必须从 top20 移出",
                "必须移出",
                "永久降格",
                "不得进入任何 lane",
                "fatal replace_topic",
                "时效过期",
                "移出或降权",
            )
        )
        if not hard_block:
            continue
        for match in RANK_REF_RE.finditer(line):
            blocked.add(int(match.group(1)))
    return blocked


def infer_from_pack(
    items: list[PackCandidate],
    scorecard_text: str,
    score_value: float | None,
    min_score_for_inference: float,
    requested_day: date,
) -> list[SlateCandidate]:
    if score_value is None or score_value < min_score_for_inference:
        return []
    blocked_ranks = hard_block_ranks_from_scorecard(scorecard_text)
    filtered_items = [item for item in items if candidate_fresh_enough(item, requested_day)]
    inferred: list[SlateCandidate] = []
    for item in sorted(filtered_items, key=lambda current: inferred_priority_score(current, requested_day), reverse=True):
        if item.rank in blocked_ranks:
            continue
        inferred.append(
            SlateCandidate(
                priority="P0" if item.rank <= 3 else "P1" if item.rank <= 6 else "P2",
                topic_key=item.topic_key,
                note=f"从 Top20 rework 包逆推出的 continuity 候选，保留原排序 rank #{item.rank}",
                enter_condition="✅ 可进入 continuity 保底锁题，但写稿前必须补关键一手证据",
                source_mode="inferred_rework_recovery",
            )
        )
    return inferred


def candidate_domains(item: PackCandidate) -> set[str]:
    refs = [item.original_link, item.source_packet, item.deep_article, item.asset_chain]
    domains: set[str] = set()
    for ref in refs:
        cleaned = clean(ref, "")
        if "://" not in cleaned:
            continue
        domains.add(urlparse(cleaned).netloc.lower().lstrip("www."))
    return domains


def candidate_fresh_enough(item: PackCandidate, requested_day: date) -> bool:
    published_day = parse_published_day(item.published_at)
    if published_day is None:
        return True
    age = (requested_day - published_day).days
    return age <= 1


def inferred_priority_score(item: PackCandidate, requested_day: date) -> int:
    score = max(0, 160 - item.rank * 10)
    domains = candidate_domains(item)
    title = clean(item.title, "")
    lowered = title.lower()
    if re.search(r"[\u4e00-\u9fff]", title):
        score += 36
    if any(domain in OFFICIAL_DOMAINS for domain in domains):
        score += 42
    if any(domain in MAINSTREAM_DOMAINS for domain in domains):
        score += 24
    if any(domain in COMMUNITY_DOMAINS for domain in domains):
        score -= 28
    if "/" in title:
        score -= 18
    if any(token in lowered for token in ("reddit", "show hn", "hn frontpage", "github trending")):
        score -= 18
    if any(token in lowered for token in ("openai", "anthropic", "google", "claude")):
        score += 10
    published_day = parse_published_day(item.published_at)
    if published_day is not None:
        age = (requested_day - published_day).days
        score -= max(0, age - 0) * 20
    return score


def is_active_candidate(candidate: SlateCandidate) -> bool:
    topic_key = clean(candidate.topic_key, "")
    if not topic_key or topic_key.startswith("#"):
        return False
    lowered_priority = clean(candidate.priority, "").lower()
    lowered_condition = clean(candidate.enter_condition, "").lower()
    if "⛔" in candidate.priority or "不得进入" in lowered_condition:
        return False
    if lowered_condition.startswith("✅"):
        return True
    if "可进入" in lowered_condition and "待" not in lowered_condition:
        return True
    if lowered_priority in {"p0", "p1", "p2"} and "pending" not in lowered_priority:
        return True
    return False


def label_market_potential(priority: str) -> str:
    mapping = {
        "p0": "高",
        "p1": "中高",
        "p2": "中",
        "p3": "观察",
    }
    return mapping.get(clean(priority, "").lower(), "中")


def label_brand_fit(item: PackCandidate) -> str:
    lowered = f"{item.title} {item.primary_platform} {item.signal_summary}".lower()
    if any(token in lowered for token in ("agent", "code", "benchmark", "github", "workflow", "sandbox", "infra", "developer", "claude")):
        return "高"
    if any(token in lowered for token in ("wechat", "obsidian", "估值", "融资", "创业", "builder")):
        return "中高"
    return "中"


def suggested_angle(item: PackCandidate) -> str:
    lowered = f"{item.title} {item.signal_summary}".lower()
    if any(token in lowered for token in ("issue", "unusable", "bug", "benchmark", "claude code")):
        return "不要复述抱怨，直接回答这个工程痛点为什么会被放大，以及它会怎样改变 agent / coding workflow 的真实使用方式。"
    if any(token in lowered for token in ("launch hn", "show hn", "github", "sandbox", "freestyle", "ghost pepper")):
        return "从产品取舍和开发者真实需求切入，说明它解决了什么旧痛点，以及为什么现在会形成扩散。"
    if any(token in lowered for token in ("估值", "obsidian", "融资", "小而美")):
        return "不要停留在故事包装，重点判断这种小团队经营方式成立的前提条件、边界和可复制性。"
    if any(token in lowered for token in ("ai singer", "itunes")):
        return "别只写猎奇，重点拆平台规则、注意力结构和内容生产链会因此发生什么变化。"
    return "以事件本身为入口，但正文要继续深挖一层：这个信号为什么现在值得看，以及它对我们关注的 agent / builder / 一人公司主线意味着什么。"


def suggested_platforms(item: PackCandidate) -> str:
    lowered = f"{item.title} {item.primary_platform} {item.signal_summary}".lower()
    if any(token in lowered for token in ("issue", "benchmark", "github", "hn", "claude", "developer", "code")):
        return "微信 / 知乎 / X"
    if any(token in lowered for token in ("itunes", "singer", "consumer", "obsidian", "wechat")):
        return "微信 / 小红书 / X"
    return "微信 / 知乎 / 小红书"


def platform_fermentation(item: PackCandidate) -> list[str]:
    suggested = suggested_platforms(item)
    if "知乎" in suggested:
        return [
            "微信：做主稿，承担完整叙事、证据和判断。",
            "知乎：承接解释 / 对比 / 问答式需求，适合把论证展开。",
            "X：做快讯 / 观点钩子，放大首轮传播。",
        ]
    return [
        "微信：做主稿，承担完整叙事和判断。",
        "小红书：提炼为易传播的切片观点或案例卡。",
        "X：做快讯 / 观点钩子，抢第一轮讨论。",
    ]


def one_line_judgment(priority: str, item: PackCandidate, slate_note: str, source_mode: str) -> str:
    if source_mode == "explicit_top20_mini_slate":
        return f"{priority} continuity 槽位：{clean(slate_note, item.why_in_top20)}"
    return f"{priority} 推进保底对象：当前来自 Top20 rework 包逆推，不等同 premium pass，但可避免当日直接挂 0。"


def source_refs(item: PackCandidate) -> list[str]:
    refs = [item.original_link, item.source_packet, item.deep_article, item.asset_chain]
    return [ref for ref in refs if clean(ref, "") and clean(ref, "") != "n/a"]


def render_detail_block(
    rank: int,
    block_kind: str,
    slate: SlateCandidate,
    item: PackCandidate,
    reason: str,
    owner_note: str,
) -> list[str]:
    lines = [
        f"### {block_kind} {rank}｜{item.title}",
        "",
        f"- 一句话判断：{one_line_judgment(slate.priority, item, slate.note, slate.source_mode)}",
        f"- 为什么值得做：{clean(item.why_in_top20, reason)}",
        f"- 市场潜力：{label_market_potential(slate.priority)}",
        f"- 品牌贴合度判断：{label_brand_fit(item)}",
        "- 平台发酵：",
    ]
    for point in platform_fermentation(item):
        lines.append(f"  - {point}")
    lines.extend(
        [
            "- 原始链接 / Source Packet：",
        ]
    )
    refs = source_refs(item)
    if refs:
        for ref in refs:
            lines.append(f"  - `{ref}`")
    else:
        lines.append("  - `n/a`")
    lines.extend(
        [
            f"- 建议切入角度：{suggested_angle(item)}",
            f"- 建议输出形式 / 平台：{suggested_platforms(item)}",
            f"- 风险提示：{clean(item.risks, owner_note)}",
            "",
        ]
    )
    return lines


def render_board(
    date_text: str,
    top_candidates: list[tuple[SlateCandidate, PackCandidate]],
    holdout_candidates: list[tuple[SlateCandidate, PackCandidate]],
    pack_path: Path,
    scorecard_path: Path,
    source_scope: str,
    board_mode: str,
    reason: str,
) -> str:
    generated_at = format_ts(now_cn())
    lines = [
        f"# {day_token(date_text)} Top 8 -> Top 5 选题板",
        "",
        f"- `date`: `{date_text}`",
        f"- `generated_at`: `{generated_at}`",
        f"- `source_scope`: `{source_scope}`",
        f"- `top20_pack_path`: `{pack_path}`",
        f"- `top20_scorecard_path`: `{scorecard_path}`",
        f"- `board_status`: `continuity_only`",
        f"- `board_mode`: `{board_mode}`",
        f"- `board_truth`: `该板来自 Top20 rework 场景下的 continuity recovery，只用于 day_mainline 不挂 0 保底锁题，不等同 premium Top5。`",
        f"- `candidate_count`: `{len(top_candidates) + len(holdout_candidates)}`",
        f"- `continuity_reason`: `{reason}`",
        "",
        "## Continuity Rule",
        "",
        "- `该板不是 premium pass`：后续平台任务单、approved-topic、draft-pack 必须沿 continuity_only 路径运行。",
        "- `可以继续生产，但不能假装已经过线`：写稿时必须优先补官方 / 原始来源，不得把补证脚手架直接带进正文。",
        "- `若强候选不足 8 个，就写实 supply gap`：宁缺毋滥，不为凑数硬塞弱题。",
        "",
        "## Top 5 Recommended",
        "",
        "| rank | candidate_key | 题目 | 市场潜力 | 品牌贴合 | 推荐理由 | 执行备注 |",
        "|------|---------------|------|----------|----------|----------|----------|",
    ]

    for index, (slate, item) in enumerate(top_candidates, start=1):
        recommended_reason = clean(item.why_in_top20, slate.note)
        owner_note = (
            "continuity 保底锁题；正文必须先补关键一手/原始证据，再展开判断。"
            if slate.source_mode == "inferred_rework_recovery"
            else "来自明确的 top20_mini_slate；正文仍需遵守补证纪律。"
        )
        lines.append(
            "| {rank} | {key} | {title} | {market} | {fit} | {reason} | {note} |".format(
                rank=index,
                key=item.topic_key,
                title=item.title,
                market=label_market_potential(slate.priority),
                fit=label_brand_fit(item),
                reason=recommended_reason,
                note=owner_note,
            )
        )

    lines.extend(
        [
            "",
            "## Holdout 3",
            "",
            "| holdout_rank | candidate_key | 题目 | 为什么能进 Top 8 | 为什么被放下 | 能否捞回 | 捞回条件 |",
            "|--------------|---------------|------|------------------|------------|----------|----------|",
        ]
    )

    holdout_rank_start = len(top_candidates) + 1
    for offset, (slate, item) in enumerate(holdout_candidates, start=0):
        index = holdout_rank_start + offset
        why_in = clean(item.why_in_top20, slate.note)
        why_not = "当前优先级低于 Top5 主槽位，保留为当日 continuity 备选。"
        rescue = "可以"
        rescue_condition = "若 Top5 主槽位后续补证失败、锁题撞车或内容展开明显不足，可按原题接力。"
        lines.append(
            "| {rank} | {key} | {title} | {why_in} | {why_not} | {rescue} | {cond} |".format(
                rank=index,
                key=item.topic_key,
                title=item.title,
                why_in=why_in,
                why_not=why_not,
                rescue=rescue,
                cond=rescue_condition,
            )
        )

    lines.extend(["", "## Top 5 Detail Blocks", ""])
    for index, (slate, item) in enumerate(top_candidates, start=1):
        recommended_reason = clean(item.why_in_top20, slate.note)
        owner_note = (
            "continuity 保底锁题；写稿前必须补关键一手证据。"
            if slate.source_mode == "inferred_rework_recovery"
            else "top20_mini_slate 明确保留对象；写稿前仍需补关键一手证据。"
        )
        lines.extend(
            render_detail_block(
                rank=index,
                block_kind="Top",
                slate=slate,
                item=item,
                reason=recommended_reason,
                owner_note=owner_note,
            )
        )

    if holdout_candidates:
        lines.extend(["---", "", "## Holdout Detail Blocks", ""])
        for offset, (slate, item) in enumerate(holdout_candidates, start=0):
            index = holdout_rank_start + offset
            lines.extend(
                render_detail_block(
                    rank=index,
                    block_kind="Holdout",
                    slate=slate,
                    item=item,
                    reason=clean(item.why_in_top20, slate.note),
                    owner_note="保留观察；若前位候选失效可接力。",
                )
            )

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    token = day_token(args.date)
    scorecard_path = LOG_DIR / f"{token}__top20__stage-gate-scorecard.md"
    pack_path = TOPIC_DIR / f"{token}__top20-screening-pack.md"

    if not scorecard_path.exists():
        print("CONTINUITY_BOARD_STATUS=blocked")
        print(f"REASON=missing_scorecard:{scorecard_path}")
        return
    if not pack_path.exists():
        print("CONTINUITY_BOARD_STATUS=blocked")
        print(f"REASON=missing_pack:{pack_path}")
        return
    reworked_pack_path = pack_path.with_name(f"{pack_path.stem}__reworked{pack_path.suffix}")

    scorecard_text = scorecard_path.read_text(encoding="utf-8")
    scorecard_fields = parse_fields(scorecard_path)
    pack_fields = parse_fields(pack_path)
    score_value = extract_total_score(scorecard_text, scorecard_fields)
    continuity_decision = normalize_continuity_decision(scorecard_fields.get("continuity_decision", ""))
    continuity_output = normalize_continuity_output(scorecard_fields.get("continuity_output", ""))

    if is_truth_stop(scorecard_fields):
        print("CONTINUITY_BOARD_STATUS=blocked")
        print("REASON=truth_stop")
        return

    canonical_pack_items = parse_pack(pack_path)
    if not canonical_pack_items:
        print("CONTINUITY_BOARD_STATUS=blocked")
        print("REASON=pack_has_no_candidates")
        return
    reworked_pack_items = parse_pack(reworked_pack_path) if reworked_pack_path.exists() else []
    pack_items = merge_pack_items(canonical_pack_items, reworked_pack_items)
    pack_by_key = pack_map(pack_items)
    source_pack_path = reworked_pack_path if reworked_pack_items else pack_path

    board_mode = ""
    continuity_reason = ""
    slate_candidates: list[SlateCandidate] = []

    if continuity_decision == "continuity_only" and continuity_output == "top20_mini_slate":
        explicit = [candidate for candidate in parse_mini_slate(scorecard_text, pack_items) if is_active_candidate(candidate)]
        explicit = [candidate for candidate in explicit if candidate.topic_key in pack_by_key]
        if len(explicit) >= max(3, args.top_count):
            slate_candidates = explicit
            board_mode = "explicit_top20_mini_slate"
            continuity_reason = "Top20 scorecard 已显式给出 continuity_only + top20_mini_slate，直接按裁判明确保留对象生成板子。"

    if not slate_candidates and args.allow_inferred_recovery:
        inferred = infer_from_pack(
            items=pack_items,
            scorecard_text=scorecard_text,
            score_value=score_value,
            min_score_for_inference=args.min_score_for_inference,
            requested_day=date.fromisoformat(args.date),
        )
        if inferred:
            slate_candidates = inferred
            board_mode = "inferred_rework_recovery"
            continuity_reason = (
                "Top20 scorecard 为 rework，且未给出可用 mini_slate；按 scorecard 硬阻断条目剔除后，从 Top20 原排序逆推 continuity recovery 板。"
            )

    if not slate_candidates:
        print("CONTINUITY_BOARD_STATUS=blocked")
        print("REASON=no_recoverable_candidates")
        print(f"CONTINUITY_DECISION={continuity_decision or 'n/a'}")
        print(f"CONTINUITY_OUTPUT={continuity_output or 'n/a'}")
        print(f"SCORE={scorecard_fields.get('score', 'n/a')}")
        return

    active_pairs = [
        (candidate, pack_by_key[candidate.topic_key])
        for candidate in slate_candidates
        if candidate.topic_key in pack_by_key and candidate_fresh_enough(pack_by_key[candidate.topic_key], date.fromisoformat(args.date))
    ]
    top_pairs = active_pairs[: max(args.top_count, 0)]
    holdout_pairs = active_pairs[max(args.top_count, 0) : max(args.top_count + args.holdout_count, 0)]

    if not top_pairs:
        print("CONTINUITY_BOARD_STATUS=blocked")
        print("REASON=top_pairs_empty_after_filter")
        return

    board_text = render_board(
        date_text=args.date,
        top_candidates=top_pairs,
        holdout_candidates=holdout_pairs,
        pack_path=source_pack_path,
        scorecard_path=scorecard_path,
        source_scope=clean(pack_fields.get("source_scope", "n/a")),
        board_mode=board_mode,
        reason=continuity_reason,
    )

    output_path = TOPIC_DIR / f"{token}__daily-top8-to-top5.md"
    if args.write:
        output_path.write_text(board_text, encoding="utf-8")
    print(f"CONTINUITY_BOARD_STATUS={'materialized' if args.write else 'dry_run'}")
    print(f"BOARD_MODE={board_mode}")
    print(f"REASON={continuity_reason}")
    print(f"OUTPUT_PATH={output_path}")
    print(f"TOP_COUNT={len(top_pairs)}")
    print(f"HOLDOUT_COUNT={len(holdout_pairs)}")


if __name__ == "__main__":
    main()

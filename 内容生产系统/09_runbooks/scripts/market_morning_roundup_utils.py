from __future__ import annotations

import re
from dataclasses import dataclass


THIRD_PARTY_MEDIA_NAMES = (
    "量子位",
    "机器之心",
    "智东西",
    "36氪",
    "极客公园",
    "GeekPark",
    "InfoQ",
    "爱范儿",
    "虎嗅",
    "TechCrunch",
    "The Verge",
    "VentureBeat",
    "Bloomberg",
    "Reuters",
    "CNBC",
    "彭博",
    "路透",
)
ROUNDUP_SECTION_TLDR = "太长不看"
ROUNDUP_SECTION_DETAIL = "详细阐述版"

_MEDIA_GROUP = "|".join(sorted((re.escape(name) for name in THIRD_PARTY_MEDIA_NAMES), key=len, reverse=True))
_MEDIA_RE = re.compile(_MEDIA_GROUP, re.I)
_SECTION_RE = re.compile(r"^##\s+(.*)$")
_DETAIL_RE = re.compile(r"^###\s+(.*)$")
_BOLD_RE = re.compile(r"^\*\*(.+?)\*\*$")
_MARKER_RE = re.compile(r"^([①②③④⑤⑥⑦⑧⑨⑩]|\d{1,2}[、.．]?)\s*(.*)$")
_DATE_RE = re.compile(r"\d{1,2}\s*月\s*\d{1,2}\s*日")
_ATTR_VERB_RE = re.compile(r"(报道|发文|写道|称|指出|提到|确认|跟进|披露|专访|重点报道|广泛跟进)")
_SPACE_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class MorningRoundupInspection:
    is_roundup: bool
    tldr_count: int
    detail_count: int
    titles_aligned: bool
    title_max_length: int
    summary_max_length: int
    detail_min_length: int
    detail_max_length: int
    third_party_media_mentions: int
    mismatched_markers: tuple[str, ...]


def _clean(text: str) -> str:
    return _SPACE_RE.sub(" ", (text or "")).strip()


def _strip_markdown(text: str) -> str:
    cleaned = _clean(text)
    cleaned = cleaned.replace("**", "").replace("`", "")
    cleaned = cleaned.replace("“", "").replace("”", "")
    return cleaned.strip()


def _split_marker(text: str) -> tuple[str, str]:
    cleaned = _strip_markdown(text)
    match = _MARKER_RE.match(cleaned)
    if not match:
        return "", cleaned
    return match.group(1).strip(), match.group(2).strip()


def count_third_party_media_mentions(text: str) -> int:
    return len(_MEDIA_RE.findall(text or ""))


def strip_third_party_attribution(text: str) -> str:
    cleaned = _clean(text)
    if not cleaned:
        return ""
    cleaned = re.sub(
        rf"^(?:据)?(?:{_MEDIA_GROUP})(?:、(?:{_MEDIA_GROUP}))*"
        rf"(?:等(?:媒体|平台))?(?:[^，。；;]{{0,18}})?{_ATTR_VERB_RE.pattern}[：:，, ]*",
        "",
        cleaned,
        flags=re.I,
    )
    cleaned = re.sub(
        rf"^[^，。；;]*?(?:{_MEDIA_GROUP})(?:、(?:{_MEDIA_GROUP}))*"
        rf"(?:等(?:媒体|平台))?(?:[^，。；;]{{0,18}})?{_ATTR_VERB_RE.pattern}[：:，, ]*",
        "",
        cleaned,
        flags=re.I,
    )
    cleaned = re.sub(
        rf"[，,](?:据)?(?:{_MEDIA_GROUP})(?:、(?:{_MEDIA_GROUP}))*"
        rf"(?:等(?:媒体|平台))?(?:[^，。；;]{{0,18}})?{_ATTR_VERB_RE.pattern}[：:，, ]*",
        "，",
        cleaned,
        flags=re.I,
    )
    cleaned = re.sub(
        rf"(?:{_MEDIA_GROUP})(?:、(?:{_MEDIA_GROUP}))*等(?:媒体|平台)",
        "多方公开信息",
        cleaned,
        flags=re.I,
    )
    cleaned = re.sub(
        rf"(?:{_MEDIA_GROUP})(?:、(?:{_MEDIA_GROUP}))*",
        "",
        cleaned,
        flags=re.I,
    )
    cleaned = re.sub(r"(?:等平台|等媒体)", "", cleaned)
    cleaned = re.sub(r"^(?:核心信息|的核心信息|报道内容|内容提要)[：:]\s*", "", cleaned)
    cleaned = re.sub(r"[，,][。.!?]", "。", cleaned)
    cleaned = re.sub(r"[。.!?]{2,}", "。", cleaned)
    cleaned = re.sub(r"[，,]{2,}", "，", cleaned)
    cleaned = re.sub(r"^[，,：:；;。.!? ]+", "", cleaned)
    cleaned = re.sub(r"[，,：:；;。.!? ]+$", "", cleaned)
    return _clean(cleaned)


def _trim_to_boundary(text: str, limit: int) -> str:
    cleaned = _clean(text).strip("，,：:；;。.!? ")
    if len(cleaned) <= limit:
        return cleaned
    best = -1
    for token in ("。", "；", "：", "，", "、", " "):
        idx = cleaned.rfind(token, 0, limit + 1)
        if idx > best:
            best = idx
    if best >= max(8, int(limit * 0.55)):
        return cleaned[:best].strip("，,：:；;。.!? ")
    return cleaned[:limit].strip("，,：:；;。.!? ")


def normalize_roundup_heading(text: str, max_chars: int = 20) -> str:
    marker, cleaned = _split_marker(text)
    cleaned = strip_third_party_attribution(cleaned)
    cleaned = re.sub(
        rf"[，,].*?(?:{_MEDIA_GROUP}|{_ATTR_VERB_RE.pattern}|官方博客|官网|官方)[^，。；;]*$",
        "",
        cleaned,
        flags=re.I,
    )
    cleaned = re.sub(r"[（(].*?[）)]", "", cleaned)
    cleaned = cleaned.strip("，,：:；;。.!? ")
    replacements = [
        (r"Managed\s+Agents", "托管 Agent"),
        (r"Embedding\s*(?:&|与)\s*Reranker", "检索"),
        (r"正式支持", "支持"),
        (r"正式接入", "接入"),
        (r"创始人表示", "创始人谈"),
        (r"罕见受访", "受访"),
        (r"完成超千万美元 A 轮融资", "完成超千万美元融资"),
        (r"Anthropic CEO .*奥特曼", "Anthropic CEO 受访"),
        (r"DeepMind 创始人.*AGI", "DeepMind 创始人谈 AGI"),
    ]
    for pattern, replacement in replacements:
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.I)
    if "，" in cleaned and len(cleaned) > max_chars:
        cleaned = cleaned.split("，", 1)[0].strip()
    if "：" in cleaned and len(cleaned) > max_chars:
        left, right = [part.strip() for part in cleaned.split("：", 1)]
        if left and right:
            candidate = f"{left}：{right}"
            cleaned = candidate if len(candidate) <= max_chars else left
    cleaned = cleaned.replace(" 正式", " ").replace("  正式", " ")
    cleaned = cleaned.replace(" & Reranker", "")
    cleaned = cleaned.replace(" Embedding", " Embedding")
    cleaned = _clean(cleaned)
    cleaned = _trim_to_boundary(cleaned, max_chars)
    return f"{marker} {cleaned}".strip() if marker else cleaned


def compress_roundup_summary(text: str, max_chars: int = 50) -> str:
    cleaned = strip_third_party_attribution(_strip_markdown(text))
    if not cleaned:
        return ""
    cleaned = re.sub(r"^(这件事|这一动作|这条信号|这个更新)(在于|意味着)", "", cleaned)
    sentence = re.split(r"[。！？!?]", cleaned)[0].strip()
    sentence = re.sub(r"(?:，|,)?(?:Reddit|Hacker News|HN).*$", "", sentence, flags=re.I)
    sentence = re.sub(r"(?:；|;)?引述专访内容$", "", sentence)
    sentence = sentence.replace("，；", "，").replace("；，", "，")
    sentence = re.sub(r"[，,；;]{2,}", "，", sentence)
    sentence = sentence.strip("，,；; ")
    if len(sentence) > max_chars and re.search(r"[，,；;、]", sentence):
        sentence = re.split(r"[，,；;、]", sentence)[0].strip()
    if len(sentence) <= max_chars:
        return sentence
    parts = [part.strip() for part in re.split(r"[，,；;、]", sentence) if part.strip()]
    kept: list[str] = []
    current = ""
    for part in parts:
        candidate = f"{current}，{part}" if current else part
        if len(candidate) > max_chars:
            break
        current = candidate
        kept.append(part)
    if current:
        return current
    return _trim_to_boundary(sentence, max_chars)


def _split_h2_sections(markdown: str) -> tuple[list[str], list[tuple[str, list[str]]]]:
    preamble: list[str] = []
    sections: list[tuple[str, list[str]]] = []
    current_heading = ""
    current_lines: list[str] = []
    seen_section = False
    for raw in markdown.splitlines():
        match = _SECTION_RE.match(raw.strip())
        if not match:
            if seen_section:
                current_lines.append(raw)
            else:
                preamble.append(raw)
            continue
        if seen_section:
            sections.append((current_heading, current_lines))
        current_heading = match.group(1).strip()
        current_lines = []
        seen_section = True
    if seen_section:
        sections.append((current_heading, current_lines))
    return preamble, sections


def _sanitize_freeform_lines(lines: list[str]) -> list[str]:
    output: list[str] = []
    for raw in lines:
        stripped = raw.strip()
        if not stripped or stripped.startswith("![") or stripped.startswith("#") or stripped == "---":
            output.append(raw)
            continue
        output.append(strip_third_party_attribution(raw))
    return output


def _parse_tldr_items(lines: list[str]) -> list[tuple[str, list[str]]]:
    items: list[tuple[str, list[str]]] = []
    current_heading = ""
    current_lines: list[str] = []
    for raw in lines:
        match = _BOLD_RE.match(raw.strip())
        if match:
            if current_heading:
                items.append((current_heading, current_lines))
            current_heading = match.group(1).strip()
            current_lines = []
            continue
        if current_heading:
            current_lines.append(raw)
    if current_heading:
        items.append((current_heading, current_lines))
    return items


def _parse_detail_items(lines: list[str]) -> list[tuple[str, list[str]]]:
    items: list[tuple[str, list[str]]] = []
    current_heading = ""
    current_lines: list[str] = []
    for raw in lines:
        match = _DETAIL_RE.match(raw.strip())
        if match:
            if current_heading:
                items.append((current_heading, current_lines))
            current_heading = match.group(1).strip()
            current_lines = []
            continue
        if current_heading:
            current_lines.append(raw)
    if current_heading:
        items.append((current_heading, current_lines))
    return items


def _visible_text_length(lines: list[str]) -> int:
    joined = "\n".join(raw for raw in lines if not raw.strip().startswith("!["))
    joined = _strip_markdown(joined)
    return len(joined.replace("\n", ""))


def _sanitize_detail_block(lines: list[str], max_chars: int = 400) -> list[str]:
    paragraphs: list[str] = []
    buffer: list[str] = []
    preserved_images: list[str] = []
    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            if buffer:
                paragraphs.append(strip_third_party_attribution(" ".join(buffer)))
                buffer = []
            continue
        if stripped.startswith("!["):
            if buffer:
                paragraphs.append(strip_third_party_attribution(" ".join(buffer)))
                buffer = []
            preserved_images.append(raw)
            continue
        buffer.append(stripped)
    if buffer:
        paragraphs.append(strip_third_party_attribution(" ".join(buffer)))
    paragraphs = [paragraph for paragraph in paragraphs if paragraph]
    while len(paragraphs) > 1 and len("".join(paragraphs)) > max_chars:
        paragraphs.pop()
    if paragraphs and len("".join(paragraphs)) > max_chars:
        paragraphs[-1] = _trim_to_boundary(paragraphs[-1], max_chars)
    output: list[str] = []
    for paragraph in paragraphs:
        if output:
            output.append("")
        output.append(paragraph)
    if preserved_images:
        if output:
            output.append("")
        output.extend(preserved_images)
    return output


def sanitize_morning_roundup_markdown(markdown: str) -> str:
    if ROUNDUP_SECTION_TLDR not in markdown or ROUNDUP_SECTION_DETAIL not in markdown:
        return markdown
    preamble, sections = _split_h2_sections(markdown)
    title_map: dict[str, str] = {}
    rendered: list[str] = _sanitize_freeform_lines(preamble)
    for heading, lines in sections:
        if rendered and rendered[-1] != "":
            rendered.append("")
        rendered.append(f"## {heading}")
        rendered.append("")
        if heading == ROUNDUP_SECTION_TLDR:
            items = _parse_tldr_items(lines)
            for index, (raw_heading, body_lines) in enumerate(items, start=1):
                marker, _ = _split_marker(raw_heading)
                normalized = normalize_roundup_heading(raw_heading)
                key = marker or str(index)
                title_map[key] = normalized
                rendered.append(f"**{normalized}**")
                summary = compress_roundup_summary(" ".join(line.strip() for line in body_lines if line.strip()))
                if summary:
                    rendered.append(summary)
                rendered.append("")
            continue
        if heading == ROUNDUP_SECTION_DETAIL:
            items = _parse_detail_items(lines)
            for index, (raw_heading, body_lines) in enumerate(items, start=1):
                marker, _ = _split_marker(raw_heading)
                key = marker or str(index)
                normalized = title_map.get(key) or normalize_roundup_heading(raw_heading)
                rendered.append(f"### {normalized}")
                sanitized_lines = _sanitize_detail_block(body_lines)
                rendered.extend(sanitized_lines)
                rendered.append("")
            continue
        rendered.extend(_sanitize_freeform_lines(lines))
        rendered.append("")
    while rendered and rendered[-1] == "":
        rendered.pop()
    return "\n".join(rendered) + "\n"


def inspect_morning_roundup_markdown(markdown: str) -> MorningRoundupInspection:
    if ROUNDUP_SECTION_TLDR not in markdown or ROUNDUP_SECTION_DETAIL not in markdown:
        return MorningRoundupInspection(
            is_roundup=False,
            tldr_count=0,
            detail_count=0,
            titles_aligned=False,
            title_max_length=0,
            summary_max_length=0,
            detail_min_length=0,
            detail_max_length=0,
            third_party_media_mentions=count_third_party_media_mentions(markdown),
            mismatched_markers=(),
        )
    _, sections = _split_h2_sections(markdown)
    tldr_lines = next((lines for heading, lines in sections if heading == ROUNDUP_SECTION_TLDR), [])
    detail_lines = next((lines for heading, lines in sections if heading == ROUNDUP_SECTION_DETAIL), [])
    tldr_items = _parse_tldr_items(tldr_lines)
    detail_items = _parse_detail_items(detail_lines)
    tldr_by_key: dict[str, tuple[str, int]] = {}
    detail_by_key: dict[str, tuple[str, int]] = {}
    max_title_length = 0
    max_summary_length = 0
    detail_lengths: list[int] = []
    for index, (heading, body_lines) in enumerate(tldr_items, start=1):
        marker, title = _split_marker(heading)
        key = marker or str(index)
        summary = " ".join(line.strip() for line in body_lines if line.strip())
        title_len = len(title)
        summary_len = len(_strip_markdown(summary))
        tldr_by_key[key] = (title, summary_len)
        max_title_length = max(max_title_length, title_len)
        max_summary_length = max(max_summary_length, summary_len)
    for index, (heading, body_lines) in enumerate(detail_items, start=1):
        marker, title = _split_marker(heading)
        key = marker or str(index)
        detail_len = _visible_text_length(body_lines)
        detail_by_key[key] = (title, detail_len)
        max_title_length = max(max_title_length, len(title))
        detail_lengths.append(detail_len)
    mismatches: list[str] = []
    for key, (title, _) in tldr_by_key.items():
        detail_title = detail_by_key.get(key, ("", 0))[0]
        if title != detail_title:
            mismatches.append(key)
    return MorningRoundupInspection(
        is_roundup=True,
        tldr_count=len(tldr_items),
        detail_count=len(detail_items),
        titles_aligned=not mismatches and len(tldr_items) == len(detail_items),
        title_max_length=max_title_length,
        summary_max_length=max_summary_length,
        detail_min_length=min(detail_lengths) if detail_lengths else 0,
        detail_max_length=max(detail_lengths) if detail_lengths else 0,
        third_party_media_mentions=count_third_party_media_mentions(markdown),
        mismatched_markers=tuple(mismatches),
    )

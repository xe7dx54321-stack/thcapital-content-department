#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
DEFAULT_DRAFT_ROOT = ROOT / "05_draft_packs"
DEFAULT_LOG_ROOT = ROOT / "10_logs"
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
DEFAULT_REQUESTED_PLATFORMS = ["wechat", "xiaohongshu", "zhihu", "x"]
PLATFORM_PREVIEW_ORDER = ["wechat", "xiaohongshu", "zhihu", "bilibili", "toutiao", "baijiahao", "x"]
PLATFORM_DISPLAY = {
    "wechat": "微信公众号",
    "xiaohongshu": "小红书",
    "zhihu": "知乎",
    "x": "X / Thread",
    "bilibili": "B站专栏",
    "toutiao": "今日头条",
    "baijiahao": "百家号",
}
PLATFORM_AUDIENCE = {
    "wechat": "layer_b / layer_c hybrid：懂一点 AI、愿意看中深度判断的人",
    "xiaohongshu": "layer_a：AI 感兴趣、想用 agent 提升自己的人",
    "zhihu": "layer_b / layer_c：带问题进来、希望得到结构化回答的人",
    "x": "layer_b：想快速获取高信号判断的 builder / operator",
    "bilibili": "layer_b：builder、创作者、workflow 玩家",
    "toutiao": "layer_a：更泛的大众读者，需要更低门槛翻译",
    "baijiahao": "layer_b / layer_c：搜索驱动、想快速建立基本认知的人",
}
PLATFORM_READER_QUESTION = {
    "wechat": "这件事到底为什么值得我认真看，而不是刷过就算？",
    "xiaohongshu": "这件事跟我有什么关系，我该从哪 3 个点理解？",
    "zhihu": "如何看待这件事，它真正说明了什么？",
    "x": "So what? 这件事真正改变了什么？",
    "bilibili": "这条线对真实 workflow / builder 有什么启发？",
    "toutiao": "这事为什么突然值得看，普通人该关心什么？",
    "baijiahao": "如何快速理解这件事，以及它为什么重要？",
}
PLATFORM_CONTEXT_DEPTH = {
    "wechat": "short-to-medium",
    "xiaohongshu": "micro-to-short",
    "zhihu": "short",
    "x": "micro",
    "bilibili": "medium",
    "toutiao": "short",
    "baijiahao": "short",
}
PLATFORM_HOOK_FAMILY = {
    "wechat": "structural-shift",
    "xiaohongshu": "user-stake",
    "zhihu": "answer-first",
    "x": "result-first",
    "bilibili": "builder-takeaway",
    "toutiao": "opportunity-window",
    "baijiahao": "search-answer",
}
PLATFORM_CTA = {
    "wechat": "给一个轻交流口子，不要硬转化",
    "xiaohongshu": "引导收藏 / 评论 / 说出你最关心的变量",
    "zhihu": "收束成当前阶段判断，不强求互动",
    "x": "用 follow-up angle 或问题收尾",
    "bilibili": "引导读者补充自己的 workflow / case",
    "toutiao": "收束成一个大众读者也能回答的问题",
    "baijiahao": "以“后续观察点”结束，保持搜索友好",
}
STATUS_ORDER = {
    "approved": 0,
    "drafting": 1,
    "needs_revision": 2,
    "draft_ready": 2,
    "ready": 2,
    "queued": 3,
    "waiting_human_publish": 4,
    "published": 5,
    "reviewed": 6,
}
PLATFORM_RENDER_HINT = {
    "wechat": "首屏要完成 hook + context + core judgment，前 3 屏内出现 1 个 proof anchor。",
    "xiaohongshu": "按图卡节奏写，每屏只做一件事，至少有 1 屏是可收藏信息块。",
    "zhihu": "问题式标题 + 答案先行 + 结构化论证，别像公众号导语。",
    "x": "第一行要能单独截图传播，第二行立刻补 context。",
    "bilibili": "更像 build log / case breakdown，要给过程、变量和边界。",
    "toutiao": "更快给结果、更强 why-you-should-care，但不能写歪。",
    "baijiahao": "问题标题 + answer-first opening + 搜索友好小标题。",
}
WECHAT_BRAND_NAME = "同行资本 TH Capital"
WECHAT_BRAND_SLOGAN = "研究 AI、Agent 与一人公司的真实变化。"
WECHAT_BRAND_DESCRIPTION = "看热点，也看热点背后的结构变化。"
WECHAT_FOLLOW_PROMPT = "如果这篇内容对你有帮助，欢迎在微信里搜索「同行资本 TH Capital」关注我们。"
WECHAT_FOLLOW_DESCRIPTION = "这里会持续更新 AI、Agent 与一人公司的真实案例、流程拆解与业务判断。"
SPECIAL_INSTRUCTION_KEYS = (
    "目标读者",
    "切入角度",
    "核心论点",
    "证据抓手",
    "视觉建议",
    "为什么适合",
    "为什么适合该平台",
)
SPECIFIC_SIGNAL_TOKENS = (
    "Claude",
    "Code",
    "API",
    "Bug",
    "bug",
    "缓存",
    "账单",
    "Anthropic",
    "GitHub",
    "Issue",
    "issue",
    "workaround",
    "Agent",
    "agent",
    "agents",
    "commit",
    "commits",
    "项目",
    "管理",
    "workflow",
    "OpenAI",
    "Qwen",
    "llama.cpp",
    "TurboQuant",
    "机器人",
    "SpaceX",
    "xAI",
)
GENERIC_FRAGMENT_PATTERNS = (
    r"直接受影响",
    r"值得(继续|持续)?跟踪",
    r"技术细节极强",
    r"具体数字硬",
    r"社区验证高",
    r"叙事强反转",
    r"易破圈",
    r"结果先行警报体",
    r"技术深度分析",
    r"工程教训",
    r"社区响应",
    r"技术警示",
    r"成本风险",
    r"修复方案三层",
    r"效率陷阱.*自述",
    r"反鸡娃",
    r"反内卷",
)
INTERNAL_COPY_SCAFFOLD_RE = re.compile(r"^P\d+\s*continuity\s*槽位\s*[:：]\s*", re.I)


@dataclass
class ApprovedTopic:
    path: Path
    topic_id: str
    topic_key: str
    candidate_id: str
    title: str
    approved_angle: str
    approved_angle_short: str
    approved_angle_medium: str
    requested_platforms: list[str]
    delivery_lane: str
    publish_mode: str
    delivery_deadline: str
    selection_scope: str
    business_window_start: str
    business_window_end: str
    special_instructions: str
    approved_by: str
    approved_at: str
    status: str
    market_potential: str
    brand_fit_judgment: str
    recommended_reason: str
    core_judgment: str
    why_now: str
    platform_hint: str
    risk_note: str
    source_refs: list[str]
    platform_task_notes: dict[str, dict[str, str]]
    special_instruction_map: dict[str, dict[str, str]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build draft pack for TH Capital market content system")
    parser.add_argument("--approved-topic-path", required=True, help="Path to approved topic card")
    parser.add_argument("--status", choices=["drafting", "ready"], default="drafting")
    parser.add_argument("--draft-root", default=str(DEFAULT_DRAFT_ROOT))
    parser.add_argument("--log-root", default=str(DEFAULT_LOG_ROOT))
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--force-platform-overwrite", action="store_true")
    return parser.parse_args()


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    slug = re.sub(r"_+", "_", slug)
    return slug or "draft"


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value).strip().strip("`")
    return value if value else fallback


def trim_text(text: str, max_chars: int) -> str:
    text = clean(text, "")
    if len(text) <= max_chars:
        return text
    shortened = text[: max_chars - 1].rstrip(" ，；：:。")
    return f"{shortened}…"


def normalize_angle(angle: str) -> str:
    text = clean(angle, "")
    replacements = [
        (r"^从\s*", ""),
        (r"\b20\d{2}\s*年", ""),
        (r"产品标配体验视角", "标配体验"),
        (r"标配体验视角", "标配体验"),
        (r"产品标配", "标配"),
        (r"视角", ""),
        (r"为什么值得持续跟踪", "为何值得跟"),
        (r"为什么值得跟踪", "为何值得跟"),
        (r"为什么值得关注", "为何值得看"),
        (r"工作流重构", "工作流变化"),
        (r"权限管理、自动执行与开发工作流变化", "授权边界、自动执行与工作流变化"),
        (r"权限管理、自动执行与", ""),
        (r"解释", ""),
        (r"说明", ""),
    ]
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)
    text = re.sub(r"\s+", " ", text).strip(" ，；：:。")
    return text


def strip_internal_copy_scaffolding(text: str) -> str:
    value = clean(text, "")
    if not value:
        return ""
    stripped = INTERNAL_COPY_SCAFFOLD_RE.sub("", value).strip(" ，；：:。")
    return clean(stripped, value)


def compact_angle(angle: str, max_chars: int, fallback: str) -> str:
    normalized = normalize_angle(angle)
    candidates: list[str] = []
    if normalized:
        candidates.append(normalized)
        for sep in ["：", "，", "；", "。"]:
            if sep in normalized:
                parts = [item.strip(" ，；：:。") for item in normalized.split(sep) if item.strip(" ，；：:。")]
                if parts:
                    candidates.append(parts[0])
                    candidates.append(parts[-1])
                    if len(parts) > 1:
                        candidates.append(f"{parts[0]}：{parts[1]}")
    deduped: list[str] = []
    for candidate in candidates:
        candidate = clean(candidate, "")
        candidate = re.sub(r"^是否会成为", "会不会成为", candidate)
        candidate = re.sub(r"(.+?)是否会成为", r"\1会不会成为", candidate)
        candidate = re.sub(r"\s+", " ", candidate).strip(" ，；：:。")
        if candidate and candidate not in deduped:
            deduped.append(candidate)
    return specific_fragment(deduped, max_chars, fallback)


def split_platforms(raw: str) -> list[str]:
    if not raw or raw == "n/a":
        return DEFAULT_REQUESTED_PLATFORMS[:]
    items = [clean(item, "") for item in raw.split(",")]
    return [item for item in items if item]


def status_rank(status: str) -> int:
    return STATUS_ORDER.get(status, -1)


def preserve_advanced_status(current_status: str, target_status: str) -> str:
    current = clean(current_status, "")
    target = clean(target_status, "")
    if status_rank(current) > status_rank(target):
        return current
    return target or current or "drafting"


def parse_sections(path: Path) -> tuple[dict[str, str], dict[str, list[str]]]:
    fields: dict[str, str] = {}
    lists: dict[str, list[str]] = {}
    current_section: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        match = KV_RE.match(line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
            continue
        if line.startswith("## "):
            current_section = line[3:].strip()
            lists.setdefault(current_section, [])
            continue
        if current_section and line.strip().startswith("- "):
            item = line.strip()[2:].strip().strip("`")
            if item:
                lists.setdefault(current_section, []).append(item)
    return fields, lists


def extract_section_lines(path: Path, heading: str) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    target = f"## {heading}"
    inside = False
    items: list[str] = []
    for raw_line in lines:
        line = raw_line.rstrip()
        if line == target:
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside and line.strip().startswith("- "):
            items.append(line.strip()[2:].strip())
    return items


def split_semicolon_items(raw: str) -> list[str]:
    value = clean(raw, "")
    if not value:
        return []
    return [clean(item, "") for item in re.split(r"[；;]\s*", value) if clean(item, "")]


def clean_publish_evidence_item(raw: str) -> str:
    value = clean(raw, "")
    if not value or value == "n/a":
        return ""
    if value.startswith("可补") or value.startswith("可回链") or value.startswith("补充："):
        return ""
    value = re.sub(r"[（(]可补[^）)]*[）)]", "", value)
    value = re.sub(r"[；;，,]\s*可补.*$", "", value)
    value = re.sub(r"[；;，,]\s*可回链.*$", "", value)
    value = re.sub(r"[；;，,]\s*补充[:：].*$", "", value)
    return clean(value, "")


def parse_platform_task_notes(path: Path) -> dict[str, dict[str, str]]:
    notes: dict[str, dict[str, str]] = {}
    for raw in extract_section_lines(path, "Platform Task Notes"):
        text = clean(raw, "")
        if not text:
            continue
        parts = [part.strip() for part in text.split("｜") if part.strip()]
        if not parts:
            continue
        platform = clean(parts[0].replace("`", ""), "").lower()
        if not platform:
            continue
        payload: dict[str, str] = {}
        for part in parts[1:]:
            if "：" in part:
                key, value = part.split("：", 1)
            elif ":" in part:
                key, value = part.split(":", 1)
            else:
                continue
            payload[clean(key, "")] = clean(value, "")
        notes[platform] = payload
    return notes


def parse_special_instructions(raw: str) -> dict[str, dict[str, str]]:
    value = clean(raw, "")
    if not value or value == "n/a":
        return {}
    result: dict[str, dict[str, str]] = {}
    for chunk in re.split(r"\s+\|\s+", value):
        if ":" not in chunk:
            continue
        platform, rest = chunk.split(":", 1)
        platform_key = clean(platform, "").lower()
        if not platform_key:
            continue
        payload: dict[str, str] = {}
        key_pattern = re.compile(rf"({'|'.join(re.escape(key) for key in SPECIAL_INSTRUCTION_KEYS)})\s*[=:：]")
        matches = list(key_pattern.finditer(rest))
        if matches:
            for index, match in enumerate(matches):
                key = clean(match.group(1), "")
                start = match.end()
                end = matches[index + 1].start() if index + 1 < len(matches) else len(rest)
                payload[key] = clean(rest[start:end].strip("；; "), "")
        else:
            for part in re.split(r"[；;]\s*", rest):
                if "=" in part:
                    key, item_value = part.split("=", 1)
                elif "：" in part:
                    key, item_value = part.split("：", 1)
                elif ":" in part:
                    key, item_value = part.split(":", 1)
                else:
                    continue
                payload[clean(key, "")] = clean(item_value, "")
        result[platform_key] = payload
    return result


def parse_simple_fields(path: Path) -> dict[str, str]:
    fields, _ = parse_sections(path)
    return fields


def load_approved_topic(path: Path) -> ApprovedTopic:
    fields, lists = parse_sections(path)
    approved_angle = clean(fields.get("approved_angle", "沿已确认角度推进"))
    core_judgment = strip_internal_copy_scaffolding(clean(fields.get("one_line_judgment", "n/a")))
    platform_task_notes = parse_platform_task_notes(path)
    special_instruction_map = parse_special_instructions(fields.get("special_instructions", "n/a"))
    focus_sources = [approved_angle, core_judgment, clean(fields.get("why_now", "n/a"))]
    for platform in ["wechat", "zhihu", "xiaohongshu", "x", "bilibili", "toutiao", "baijiahao"]:
        note = platform_task_notes.get(platform, {})
        for key in ("核心论点", "切入角度"):
            value = strip_internal_copy_scaffolding(clean(note.get(key, ""), ""))
            if value and value != "n/a":
                focus_sources.append(value)
    return ApprovedTopic(
        path=path,
        topic_id=clean(fields.get("topic_id", path.stem)),
        topic_key=clean(fields.get("topic_key", slugify(path.stem))),
        candidate_id=clean(fields.get("candidate_id", "n/a")),
        title=clean(fields.get("title", path.stem)),
        approved_angle=approved_angle,
        approved_angle_short=specific_fragment(focus_sources, 26, core_judgment or approved_angle),
        approved_angle_medium=specific_fragment(focus_sources, 40, core_judgment or approved_angle),
        requested_platforms=split_platforms(fields.get("requested_platforms", "")),
        delivery_lane=clean(fields.get("delivery_lane", "day_mainline")),
        publish_mode=clean(fields.get("publish_mode", "draft_only")),
        delivery_deadline=clean(fields.get("delivery_deadline", "n/a")),
        selection_scope=clean(fields.get("selection_scope", "n/a")),
        business_window_start=clean(fields.get("business_window_start", "n/a")),
        business_window_end=clean(fields.get("business_window_end", "n/a")),
        special_instructions=clean(fields.get("special_instructions", "n/a")),
        approved_by=clean(fields.get("approved_by", "老板")),
        approved_at=clean(fields.get("approved_at", "n/a")),
        status=clean(fields.get("status", "approved")),
        market_potential=clean(fields.get("market_potential", "n/a")),
        brand_fit_judgment=clean(fields.get("brand_fit_judgment", "n/a")),
        recommended_reason=clean(fields.get("recommended_reason", "n/a")),
        core_judgment=core_judgment,
        why_now=clean(fields.get("why_now", "n/a")),
        platform_hint=clean(fields.get("platform_hint", "n/a")),
        risk_note=clean(fields.get("risk_note", "n/a")),
        source_refs=lists.get("Source Refs", []),
        platform_task_notes=platform_task_notes,
        special_instruction_map=special_instruction_map,
    )


def platform_field(topic: ApprovedTopic, platform: str, *keys: str, default: str = "n/a") -> str:
    platform_key = clean(platform, "").lower()
    sources = [
        topic.platform_task_notes.get(platform_key, {}),
        topic.special_instruction_map.get(platform_key, {}),
    ]
    for source in sources:
        for key in keys:
            value = clean(source.get(key, ""), "")
            if value and value != "n/a":
                return value
    return default


def readable_ref(source_ref: str, platform: str | None = None) -> tuple[str | None, str]:
    ref = clean(source_ref, "")
    if not ref:
        return None, ""
    if ref.startswith("evidence_hint::"):
        parts = ref.split("::", 2)
        if len(parts) == 3:
            ref_platform = clean(parts[1], "").lower()
            if platform and ref_platform and ref_platform != clean(platform, "").lower():
                return ref_platform, ""
            return ref_platform, clean(parts[2], "")
    if ref.startswith("http://") or ref.startswith("https://"):
        return "all", ref
    if ref.startswith("/Users/") or ref.startswith(str(ROOT)):
        return "internal", ""
    return "all", ref


def source_packet_preview(ref: str) -> dict[str, str] | None:
    raw = clean(ref, "")
    if not raw:
        return None
    path = Path(raw).expanduser()
    if not path.exists() or not path.name.endswith("__source-packet.md"):
        return None
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return {
        "title": clean(fields.get("title", path.stem)),
        "published_at": clean(fields.get("published_at", "n/a")),
        "source_name": clean(fields.get("source_name", fields.get("source_id", "n/a"))),
        "path": str(path),
    }


def platform_evidence_lines(topic: ApprovedTopic, platform: str, max_items: int = 4) -> list[str]:
    lines: list[str] = []
    direct = split_semicolon_items(platform_field(topic, platform, "证据抓手", default=""))
    if direct:
        lines.extend(clean_publish_evidence_item(item) for item in direct)
    for ref in topic.source_refs:
        _, text = readable_ref(ref, platform=platform)
        if text:
            lines.extend(clean_publish_evidence_item(item) for item in split_semicolon_items(text))
    deduped: list[str] = []
    for item in lines:
        if item and item not in deduped:
            deduped.append(item)
    return deduped[:max_items]


def platform_visual_lines(topic: ApprovedTopic, platform: str, max_items: int = 4) -> list[str]:
    direct = [clean_publish_evidence_item(item) for item in split_semicolon_items(platform_field(topic, platform, "视觉建议", default=""))]
    direct = [item for item in direct if item]
    if direct:
        return direct[:max_items]
    return [
        "原始截图做证据锚点",
        "一张解释型结构图梳理变量",
        "一张数据或对比图突出核心结论",
    ][:max_items]


def title_angle_fragment(angle: str) -> str:
    value = clean(angle, "")
    value = re.sub(r"^是\s*", "", value)
    return value or "结构性变化"


def why_now_text(topic: ApprovedTopic, platform: str) -> str:
    claim = clean(claim_text(topic, platform), "")
    evidence = platform_evidence_lines(topic, platform, max_items=1)
    generated = ""
    if claim and claim != "n/a":
        claim_bits = [clean(part, "") for part in re.split(r"[；;]", claim) if clean(part, "")]
        claim_head = "；".join(claim_bits[:2]) if claim_bits else claim
        generated = trim_text(claim_head, 72).rstrip("。.!！")
        if evidence:
            generated = f"{generated}，而且公开证据已经给到：{publish_evidence_phrase(evidence[0])}"
    candidates = [
        generated,
        topic.why_now,
        topic.recommended_reason,
        claim,
        f"它把“{topic.approved_angle_medium}”从一个可讨论的话题，推进到了可以被读者验证和判断的阶段。",
    ]
    for item in candidates:
        value = clean(item, "")
        if value and value != "n/a":
            return value
    return f"它把“{topic.approved_angle_medium}”从抽象讨论推进到了可验证阶段。"


def audience_text(topic: ApprovedTopic, platform: str) -> str:
    return platform_field(topic, platform, "目标读者", default=PLATFORM_AUDIENCE.get(platform, "n/a"))


def angle_text(topic: ApprovedTopic, platform: str) -> str:
    return platform_field(topic, platform, "切入角度", default=topic.title)


def claim_text(topic: ApprovedTopic, platform: str) -> str:
    return platform_field(topic, platform, "核心论点", default=topic.core_judgment)


def fit_text(topic: ApprovedTopic, platform: str) -> str:
    return platform_field(
        topic,
        platform,
        "为什么适合",
        default=f"因为这个话题天然适合沿着“{topic.approved_angle_medium}”做平台化展开。",
    )


def compact_title_seed(text: str) -> str:
    value = clean(text, "")
    if not value:
        return ""
    quoted = extract_quoted_fragments(value)
    if quoted:
        return specific_fragment(quoted, 40, quoted[0])
    value = re.sub(r"^[^———]*[———]+", "", value)
    value = re.sub(r"^[^：:]*[：:]\s*", "", value)
    value = re.split(r"[；;]", value, maxsplit=1)[0]
    value = clean(value, "")
    return value


def compact_meaning_seed(text: str) -> str:
    value = clean(text, "")
    if not value:
        return ""
    replacements = [
        ("产品矩阵 + 路线叙事 + 战略节奏", "矩阵战"),
        ("产品矩阵+路线叙事+战略节奏", "矩阵战"),
        ("AI 普惠硬件门槛降至消费级", "消费级硬件也能跑大模型"),
        ("Unsloth Studio 重大更新", "这波更新不只是加功能"),
        ("Agent 正开始吃掉部分建模工作流", "Agent 开始接管建模工作流"),
        ("SoftBank $40B 贷款是 OpenAI IPO 的强信号", "它像 OpenAI IPO 的前哨战"),
        ("llama.cpp 实现 KV Dequant 压缩", "开源推理效率进入深水区"),
    ]
    for source, target in replacements:
        value = value.replace(source, target)
    if "说明" in value:
        left, right = value.split("说明", 1)
        right = re.split(r"[，。；;]", right, maxsplit=1)[0]
        value = f"{clean(left, '')}，{clean(right, '')}"
    if "意味着" in value:
        left, right = value.split("意味着", 1)
        right = re.split(r"[，。；;]", right, maxsplit=1)[0]
        value = f"{clean(left, '')}，{clean(right, '')}"
    if "转向" in value:
        prefix = re.split(r"[，。；;]", value, maxsplit=1)[0]
        value = prefix
    value = value.strip("，。；;：: ")
    return clean(value, "")


def claim_event_seed(text: str) -> str:
    value = clean(text, "")
    if not value:
        return ""
    for marker in ["说明", "意味着", "让", "开始", "正在", "是"]:
        if marker in value:
            left = clean(value.split(marker, 1)[0], "")
            if 6 <= len(left) <= 40 and not re.search(r"[把让是将与和在于向]$", left):
                return left
    return clean(re.split(r"[，。；;]", value, maxsplit=1)[0], "")


def claim_meaning_seed(text: str) -> str:
    value = clean(text, "")
    if not value:
        return ""
    if "说明" in value:
        value = value.split("说明", 1)[1]
    elif "意味着" in value:
        value = value.split("意味着", 1)[1]
    elif "转向" in value:
        value = "开始转向" + value.split("转向", 1)[1]
    value = compact_meaning_seed(value)
    value = value.replace("正在从单点能力比拼", "开始告别单点能力比拼")
    value = value.replace("开始转向“矩阵战", "开始打矩阵战")
    value = value.replace("开始转向矩阵战", "开始打矩阵战")
    return clean(value, "")


def dedupe_preserve(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        value = clean(item, "")
        if value and value not in result:
            result.append(value)
    return result


def extract_quoted_fragments(text: str) -> list[str]:
    value = clean(text, "")
    if not value:
        return []
    patterns = [
        r"「([^」]{4,160})」",
        r"“([^”]{4,160})”",
        r"\"([^\"]{4,160})\"",
    ]
    matches: list[str] = []
    for pattern in patterns:
        matches.extend(clean(item, "") for item in re.findall(pattern, value) if clean(item, ""))
    return dedupe_preserve(matches)


def generic_fragment_penalty(text: str) -> int:
    value = clean(text, "")
    penalty = 0
    for pattern in GENERIC_FRAGMENT_PATTERNS:
        if re.search(pattern, value, re.I):
            penalty += 8
    if value in {"n/a", "值得看", "值得重看", "开发者直接受影响"}:
        penalty += 12
    return penalty


def fragment_candidates(text: str) -> list[str]:
    value = clean(text, "")
    if not value:
        return []
    quoted = extract_quoted_fragments(value)
    if quoted:
        candidates: list[str] = []
        for item in quoted:
            candidates.append(item)
            for sep in ["——", "—", "：", "；", "，", "。", " / "]:
                if sep in item:
                    candidates.extend(clean(part, "") for part in item.split(sep) if clean(part, ""))
        return dedupe_preserve(candidates)
    candidates: list[str] = []
    candidates.append(value)
    for sep in ["——", "—", "：", "；", "，", "。", " / "]:
        if sep in value:
            candidates.extend(clean(part, "") for part in value.split(sep) if clean(part, ""))
    return dedupe_preserve(candidates)


def specific_fragment(texts: list[str], max_chars: int, fallback: str) -> str:
    candidates: list[str] = []
    for text in texts:
        candidates.extend(fragment_candidates(text))
    candidates = dedupe_preserve(candidates)
    if not candidates:
        return trim_text(fallback, max_chars)

    def score(item: str) -> tuple[int, int]:
        value = clean(item, "")
        length = len(value)
        points = 0
        if 8 <= length <= max_chars:
            points += 12
        elif 8 <= length <= max_chars + 12:
            points += 6
        else:
            points -= abs(length - max_chars)
        if re.search(r"\d", value):
            points += 3
        if re.search(r"[A-Z]", value):
            points += 2
        if any(token in value for token in SPECIFIC_SIGNAL_TOKENS):
            points += 6
        if any(token in value for token in ["导致", "暴增", "失效", "更累", "管理", "缓存", "账单", "commits", "projects"]):
            points += 4
        if re.match(r"^\d+[）\)]", value):
            points -= 10
        points -= generic_fragment_penalty(value)
        return points, -length

    chosen = max(candidates, key=score)
    return trim_text(chosen, max_chars) if chosen else trim_text(fallback, max_chars)


def normalize_title_phrase(text: str) -> str:
    value = clean(text, "")
    if not value:
        return ""
    value = value.replace("“", "").replace("”", "").replace("「", "").replace("」", "").replace('"', "")
    value = re.sub(r"[（(][^）)]{1,24}[）)]", "", value)
    replacements = [
        (r"在中关村论坛", ""),
        (r"一口气发布", "连发"),
        (r"一次性", ""),
        (r"同时摆上桌", "摆上桌"),
        (r"亮出 2026 AGI 战略", "亮出 2026 AGI 计划"),
        (r"亮出 2026 AGI 时间表", "亮出 2026 AGI 时间表"),
        (r"拿到 OpenAI MLE-Bench 榜单第一", "拿下 MLE-Bench 第一"),
        (r"拿到 MLE-Bench 榜单第一", "拿下 MLE-Bench 第一"),
        (r"推进到可 benchmark 的层级", ""),
        (r"自然语言描述任务 → 自动构建 AI 模型", "AI 自动搭模型"),
        (r"AIBuildAI 把AI 自动搭模型", "AIBuildAI 自动搭模型"),
        (r"AIBuildAI 把[^，。；;]*", "AIBuildAI 自动搭模型"),
        (r"本地跑通", "跑通"),
        (r"在普通\s*", ""),
        (r"在[^，。；;]*?上跑通", "跑通"),
        (r"Google TurboQuant 量化算法让 ", ""),
        (r"TurboQuant 量化算法让 ", ""),
        (r"TurboQuant 量化算法 patch 进 llama.cpp", "llama.cpp 接入 TurboQuant"),
        (r"SoftBank \$40B 贷款的结构与时机", "软银这笔 400 亿美元贷款"),
        (r"SoftBank \$40B 贷款", "软银这笔 400 亿美元贷款"),
        (r"Unsloth Studio Beta 一周内重大更新", "Unsloth Studio 一周更了 50+ 功能"),
        (r"OpenAI IPO 的强信号", "OpenAI 上市前哨战"),
        (r"\s+", " "),
    ]
    for pattern, repl in replacements:
        value = re.sub(pattern, repl, value)
    return clean(value.strip(" ，；;：:。"), "")


def choose_title_candidate(candidates: list[str], max_chars: int, min_chars: int = 6) -> str:
    normalized = dedupe_preserve(candidates)
    if not normalized:
        return ""
    generic_prefixes = [
        "真正值得看的不是",
        "真正值得看",
        "为什么",
        "如何看待",
        "技术深拆",
        "产业深度分析",
        "实用教程",
        "新工具发现",
    ]
    generic_exact = {
        "TurboQuant",
        "50+ 新功能",
        "50+ 功能",
        "新功能",
        "SoftBank $40B 贷款的结构与时机",
    }
    entity_markers = [
        "OpenAI",
        "SoftBank",
        "软银",
        "昆仑",
        "TurboQuant",
        "Qwen",
        "Unsloth",
        "AIBuildAI",
        "Siri",
        "Arm",
        "Claude",
        "DeerFlow",
        "Minicor",
        "MacBook",
        "llama.cpp",
    ]
    action_markers = ["发布", "连发", "更新", "借出", "上市", "跑", "接入", "拿下", "更了", "亮出"]

    def score(item: str) -> tuple[int, int]:
        value = clean(item, "")
        length = len(value)
        points = 0
        if min_chars <= length <= max_chars:
            points += 8
        elif min_chars <= length <= max_chars + 6:
            points += 4
        else:
            points -= abs(length - max_chars)
        if re.search(r"[\u4e00-\u9fff]", value):
            points += 2
        if re.search(r"[A-Za-z]", value) and re.search(r"[\u4e00-\u9fff]", value):
            points += 1
        if re.search(r"\d", value):
            points += 1
        if any(marker in value for marker in entity_markers):
            points += 4
        if any(marker in value for marker in action_markers):
            points += 2
        if any(value.startswith(prefix) for prefix in generic_prefixes):
            points -= 6
        if value in generic_exact:
            points -= 8
        if "…" in value:
            points -= 12
        if value.endswith("功能") and "Unsloth" not in value:
            points -= 5
        if value.startswith("AI 普惠") and "MacBook" not in value:
            points -= 4
        if re.fullmatch(r"[A-Za-z0-9 .+_/-]{1,20}", value):
            points -= 4
        if "不是又发了" in value:
            points -= 3
        return points, -length

    return max(normalized, key=score)


def event_title_seed(topic: ApprovedTopic, platform: str, max_chars: int = 24) -> str:
    candidates: list[str] = []
    for source in [
        angle_text(topic, platform),
        topic.title,
        claim_event_seed(claim_text(topic, platform)),
        compact_title_seed(angle_text(topic, platform)),
        claim_event_seed(topic.core_judgment),
        compact_title_seed(topic.title),
        topic.approved_angle_short,
    ]:
        value = normalize_title_phrase(source)
        if not value:
            continue
        candidates.append(value)
        for sep in ["；", "，", "："]:
            if sep in value:
                candidates.extend(normalize_title_phrase(part) for part in value.split(sep))
        if "并" in value:
            candidates.append(normalize_title_phrase(value.split("并", 1)[0]))
    return choose_title_candidate(candidates, max_chars) or clean(topic.title)


def normalize_meaning_phrase(text: str) -> str:
    value = normalize_title_phrase(text)
    replacements = [
        ("国产大模型竞争进入矩阵战 + 路线战的强信号", "大厂模型竞争开始换打法"),
        ("国产大模型竞争进入矩阵战+路线战的强信号", "大厂模型竞争开始换打法"),
        ("产品矩阵 + 路线叙事 + 战略节奏", "矩阵战"),
        ("产品矩阵+路线叙事+战略节奏", "矩阵战"),
        ("AI 普惠硬件门槛降至消费级", "消费级硬件开始能跑大模型"),
        ("Agent 正开始吃掉部分建模工作流", "Agent 开始接管一部分建模"),
        ("Agent 开始吃掉部分建模工作流", "Agent 开始接管一部分建模"),
        ("OpenAI 上市前哨战", "OpenAI 上市前哨战"),
        ("Unsloth Studio 重大更新", "训练工作台继续一体化"),
        ("开源推理效率进入深水区", "开源推理开始卷效率"),
    ]
    for source, target in replacements:
        value = value.replace(source, target)
    return clean(value, "")


def meaning_title_seed(topic: ApprovedTopic, platform: str, max_chars: int = 14) -> str:
    candidates = [
        normalize_meaning_phrase(claim_meaning_seed(claim_text(topic, platform))),
        normalize_meaning_phrase(compact_meaning_seed(topic.approved_angle_short)),
        normalize_meaning_phrase(title_angle_fragment(topic.approved_angle_short)),
    ]
    chosen = choose_title_candidate(candidates, max_chars) or ""
    if "…" in chosen:
        if ("SoftBank" in chosen or "软银" in chosen) and "OpenAI" in chosen:
            return "OpenAI 上市前哨战"
        return ""
    return chosen


def question_title_base(text: str) -> str:
    value = clean(text, "")
    value = re.sub(r"^如何看待[“\"]?", "", value)
    value = re.sub(r"[”\"]?[？?]$", "", value)
    return clean(value.strip("“”\" "), "")


def publish_evidence_phrase(raw: str) -> str:
    value = clean(raw, "")
    if not value:
        return ""
    replacements = [
        (r"(.+?)原文中的\s*(.+?)信息", r"\1对\2的梳理"),
        (r"(.+?)原文中的\s*(.+)", r"\1对\2的梳理"),
        (r"(.+?)原文里\s*(.+?)信息", r"\1对\2的梳理"),
        (r"(.+?)场景$", r"\1现场"),
        (r"(.+?)规格$", r"\1配置"),
        (r"帖子实操结果", "实操结果"),
        (r"benchmark 数据", "benchmark 结果"),
        (r"对3 模型", "对 3 个模型"),
    ]
    for pattern, repl in replacements:
        value = re.sub(pattern, repl, value)
    return clean(value, "")


def publish_title(topic: ApprovedTopic, platform: str) -> str:
    event_seed = event_title_seed(topic, platform)
    meaning_seed = meaning_title_seed(topic, platform)
    if platform == "wechat":
        base_title = clean(topic.title, "")
        if base_title and len(base_title) <= 30:
            return base_title
        if meaning_seed and meaning_seed not in event_seed and len(event_seed) + len(meaning_seed) + 1 <= 30:
            return clean(f"{event_seed}，{meaning_seed}", topic.title)
        return clean(event_seed, topic.title)
    if platform == "toutiao":
        base_title = clean(topic.title, "")
        if base_title and len(base_title) <= 30:
            return base_title
        if meaning_seed and meaning_seed not in event_seed and len(event_seed) + len(meaning_seed) + 1 <= 30:
            return clean(f"{event_seed}，{meaning_seed}", topic.title)
        return clean(event_seed, topic.title)
    if platform == "zhihu":
        return f"如何看待{question_title_base(event_seed)}？"
    if platform == "xiaohongshu":
        preferred = []
        angle_seed = normalize_title_phrase(compact_title_seed(angle_text(topic, platform)))
        if angle_seed and any(token in angle_seed for token in ["你", "MacBook", "iPhone", "Siri", "机器人"]) and len(angle_seed) <= 36:
            return clean(angle_seed, topic.title)
        if angle_seed and 8 <= len(angle_seed) <= 24:
            return clean(angle_seed, topic.title)
        if angle_seed:
            preferred.append(angle_seed)
            preferred.extend(normalize_title_phrase(part) for part in re.split(r"[，；:：]", angle_seed))
        preferred.append(event_seed)
        title = choose_title_candidate(preferred, 24) or event_seed or meaning_seed
        return clean(title, topic.title)
    if platform == "bilibili":
        if len(event_seed) <= 18:
            return clean(f"{event_seed}，这波值不值得跟？", topic.title)
        return clean(event_seed, topic.title)
    if platform == "x":
        quoted_hook = extract_quoted_fragments(angle_text(topic, platform))
        if quoted_hook:
            return clean(quoted_hook[0], quoted_hook[0])
        hook_seed = specific_fragment([angle_text(topic, platform), topic.title, event_seed], 88, claim_text(topic, platform))
        return clean(hook_seed or meaning_seed or event_seed or claim_text(topic, platform), claim_text(topic, platform))
    if platform == "baijiahao":
        return f"如何理解{question_title_base(event_seed)}？"
    return clean(event_seed or topic.title, topic.title)


def evidence_paragraphs(topic: ApprovedTopic, platform: str) -> list[str]:
    evidence = platform_evidence_lines(topic, platform, max_items=3)
    if not evidence:
        return []
    paragraphs: list[str] = []
    first = publish_evidence_phrase(evidence[0])
    paragraphs.append(
        f"先看已经公开的第一层信号：{first}。至少从这一步看，这不是靠情绪和转述撑起来的话题，而是已经有明确对象、明确动作和明确场景支撑的事件。"
    )
    if len(evidence) >= 2:
        second = publish_evidence_phrase(evidence[1])
        paragraphs.append(
            f"再把 {second} 放进来一起看，事件的意义就不只是一条 headline，而是能被放回更完整的行业语境里理解。"
        )
    if len(evidence) >= 3:
        third = publish_evidence_phrase(evidence[2])
        paragraphs.append(
            f"第三个值得继续盯的信号是 {third}。它决定这条判断后面能不能从“值得讨论”，继续升级成“值得长期跟”。"
        )
    return paragraphs


def variable_answer_paragraphs(topic: ApprovedTopic, platform: str) -> list[str]:
    audience = audience_text(topic, platform)
    claim = claim_text(topic, platform)
    return [
        f"先看事件层：{claim}。这意味着相关参与方已经不只是做一个单点动作，而是在主动把更大的路线图推到台前。",
        f"再看行业层：{topic.approved_angle_medium} 这条线，已经从“可以讨论”变成了“必须持续跟踪”的变量。",
        f"最后看决策层：对 {audience} 来说，现在最重要的不是急着站队，而是尽快判断这条变化最终会把机会、注意力和资源往哪里重新聚拢。",
    ]


def risk_boundary_paragraph(topic: ApprovedTopic, platform: str) -> str:
    return (
        f"当然，现在下强结论还太早。当前最大的风险点仍然是：{topic.risk_note}。"
        "更稳的做法，不是把它写成已经兑现完毕的终局答案，而是把它视为已经显形、但仍要继续补证的一条主线。"
    )


def platform_name(platform: str) -> str:
    return PLATFORM_DISPLAY.get(platform, platform)


def cold_start_gap(topic: ApprovedTopic, platform: str) -> str:
    if platform == "x":
        return f"如果一上来只看到“{topic.title}”，用户很可能只把它当成快讯，看不到 {topic.approved_angle_medium} 这一层。"
    if platform == "xiaohongshu":
        return f"冷启动用户不知道对象是谁，也不知道这件事为什么和自己有关，必须在 1-2 屏内把 stakes 讲清楚。"
    return f"读者可能知道“{topic.title}”发生了，但不知道这件事为什么值得沿着“{topic.approved_angle_medium}”继续看。"


def minimum_event_kernel(topic: ApprovedTopic) -> list[str]:
    return [
        f"对象：{topic.title}",
        f"变化：{topic.why_now}",
        f"判断：{topic.core_judgment}",
        f"切口：{topic.approved_angle_medium}",
        f"完整角度：{topic.approved_angle}",
    ]


def source_ref_lines(topic: ApprovedTopic, numbered: bool = False, max_refs: int = 4) -> list[str]:
    refs = [text for _, text in (readable_ref(ref) for ref in topic.source_refs) if text][:max_refs]
    if not refs:
        return ["- `n/a`"]
    if numbered:
        return [f"- `[{index}]` {ref}" for index, ref in enumerate(refs, start=1)]
    return [f"- `{ref}`" for ref in refs]


def primary_ref(topic: ApprovedTopic) -> str:
    for ref in topic.source_refs:
        _, text = readable_ref(ref)
        if text:
            return text
    return "n/a"


def background_snapshot_lines(topic: ApprovedTopic, platform: str = "wechat") -> list[str]:
    return [
        f"发生了什么：{topic.title}",
        f"为什么现在值得看：{why_now_text(topic, platform)}",
        f"真正要拆的不是 headline，而是：{topic.approved_angle_medium}",
        f"当前判断：{claim_text(topic, platform)}",
    ]


def cover_job(platform: str) -> str:
    if platform == "wechat":
        return "让用户愿意点开，同时在 3 秒内知道这不是普通资讯稿。"
    if platform == "xiaohongshu":
        return "让用户停下来，并立刻知道这件事和自己 / 自己的机会有什么关系。"
    if platform == "zhihu":
        return "让搜索读者先知道这篇回答的问题是什么，再决定继续读。"
    if platform == "x":
        return "让首条单独截图传播也能成立。"
    if platform == "bilibili":
        return "让 builder 社区知道这不是泛资讯，而是值得拆过程的案例。"
    if platform == "toutiao":
        return "让泛读者快速知道这事为什么值得看，而不是把它刷过去。"
    if platform == "baijiahao":
        return "让搜索流量用户一眼知道对象、问题和答案方向。"
    return "帮助用户更快决定要不要点开。"


def background_cash_line(topic: ApprovedTopic, platform: str) -> str:
    if platform == "x":
        return f"{topic.title} 表面像产品动态，但真正改变的是 {topic.approved_angle_short}。"
    if platform == "xiaohongshu":
        return f"一句话背景：这不是普通新闻，它和 {topic.approved_angle_medium} 直接相关。"
    return f"一句话背景：{topic.title} 值得看，不是因为 headline 本身，而是因为它暴露了 {topic.approved_angle_medium}。"


def section_job_map(platform: str) -> list[str]:
    if platform == "wechat":
        return [
            "首屏：hook + 对象 + why now + core judgment",
            "中前段：先给第一证据锚点，防止全文变抽象",
            "中段：拆关键变量与链路变化",
            "后段：给 TH Capital 判断与边界",
            "结尾：给下一步观察点与轻 CTA",
        ]
    if platform == "zhihu":
        return [
            "开头：直接回答问题",
            "前段：把原始事件和 why now 讲清楚",
            "中段：按变量/分歧/证据组织论证",
            "后段：收束为当前阶段判断",
        ]
    if platform == "bilibili":
        return [
            "开头：告诉读者能带走什么",
            "前段：先把背景和案例说清楚",
            "中段：拆过程、坑点、变量",
            "后段：给 builder takeaway 和边界",
        ]
    if platform == "toutiao":
        return [
            "前两段：先给结果和 stakes",
            "第三段：补背景，避免用户云里雾里",
            "中段：短块拆变量",
            "结尾：给一句明确提醒",
        ]
    if platform == "baijiahao":
        return [
            "开头：answer-first",
            "前段：背景 + why now",
            "中段：定义 / 变量 / 风险 / 证据",
            "结尾：给当前判断和观察点",
        ]
    return [
        "开头：先完成 promise",
        "中段：补上下文和证据",
        "结尾：给下一步动作",
    ]


def proof_cadence(platform: str) -> str:
    if platform in {"wechat", "zhihu", "bilibili", "baijiahao", "toutiao"}:
        return "前 10-20% 出现第一个 proof anchor，中后段再给一组补充证据。"
    if platform == "xiaohongshu":
        return "前 2 屏内至少出现 1 个可信锚点。"
    if platform == "x":
        return "第一条给判断，第二条或第三条立刻给 context / proof。"
    return "尽早给一个可信锚点。"


def platform_title_options(topic: ApprovedTopic, platform: str) -> list[str]:
    title = publish_title(topic, platform)
    event = event_title_seed(topic, platform)
    meaning = meaning_title_seed(topic, platform)
    question = question_title_base(event)
    if platform == "wechat":
        return dedupe_preserve(
            [
                title,
                f"{event}，为什么值得重看",
                f"{event}，它想抢的不是一轮热度",
            ]
        )[:3]
    if platform == "xiaohongshu":
        return dedupe_preserve(
            [
                title,
                f"{event}，这次真的不只是热闹",
                f"3 个点看懂：{event}",
            ]
        )[:3]
    if platform == "zhihu":
        return dedupe_preserve(
            [
                f"如何看待{question}？",
                f"{question}说明了什么？",
                f"{question}为什么值得持续关注？",
            ]
        )[:3]
    if platform == "x":
        x_title = publish_title(topic, platform)
        return dedupe_preserve(
            [
                x_title,
                f"{event} is less about the feature, more about the shift.",
                f"The real signal behind {event}: {meaning or 'the boundary is moving'}.",
            ]
        )[:3]
    if platform == "bilibili":
        return dedupe_preserve(
            [
                title,
                f"{event}，这波到底值不值得跟？",
                f"{event}，对 builder 真正重要的是什么？",
            ]
        )[:3]
    if platform == "toutiao":
        return dedupe_preserve(
            [
                title,
                f"{event}，这次不只是一个新消息",
                f"{event}，普通人到底该关心什么？",
            ]
        )[:3]
    if platform == "baijiahao":
        return dedupe_preserve(
            [
                title,
                f"{question}说明了什么？",
                f"{question}为什么值得关注？",
            ]
        )[:3]
    return title_options(topic)[:3]


def platform_cover_options(topic: ApprovedTopic, platform: str) -> list[str]:
    short_title = publish_title(topic, platform)
    meaning = meaning_title_seed(topic, platform)
    if platform == "wechat":
        return [
            f"主标题：{short_title} / 副标题：{meaning or title_angle_fragment(topic.approved_angle_short)}",
            f"主标题：{short_title} / 副标题：别只看热闹，要看背后的变量",
        ]
    if platform == "xiaohongshu":
        return [
            f"封面主文案：{short_title}\n副文案：{meaning or '这次不是噱头，是门槛真的在下移'}",
            f"封面主文案：{short_title}\n副文案：别只看热闹，要看真正变了什么",
        ]
    if platform == "x":
        return [
            "首条必须像截图也能看懂的结论句。",
            "不要封面感，要单句传播感。",
        ]
    return [
        f"核心视觉文案：{short_title}",
        f"辅助文案：{meaning or title_angle_fragment(topic.approved_angle_short)}",
    ]


def platform_opening_options(topic: ApprovedTopic, platform: str) -> list[str]:
    event = event_title_seed(topic, platform)
    if platform == "wechat":
        return [
            f"很多人会把“{event}”当成一条快讯，但如果把它放回今天的行业竞争里看，真正重要的不是发布本身，而是 {topic.approved_angle_medium}。",
            f"如果只把“{event}”当新闻看，你会错过真正重要的那层：{topic.approved_angle_medium}。",
        ]
    if platform == "xiaohongshu":
        return [
            f"先给一句最直接的结论：{claim_text(topic, platform)}。",
            f"如果你最近刷到“{event}”，先别急着划走，这事真正影响的是 {topic.approved_angle_medium}。",
        ]
    if platform == "zhihu":
        return [
            f"先说结论：{claim_text(topic, platform)}。",
            f"这件事真正值得看的，不是 headline，而是 {topic.approved_angle_medium}。",
        ]
    if platform == "x":
        return [
            topic.core_judgment,
            f"Most people will read this as product news. The real shift is {topic.approved_angle_short}.",
        ]
    if platform == "bilibili":
        return [
            f"先说结论：{claim_text(topic, platform)}。",
            f"别把“{event}”只当成热闹，builder 更该看的是 {topic.approved_angle_medium}。",
        ]
    if platform == "toutiao":
        return [
            f"先给结论：{claim_text(topic, platform)}。",
            f"如果你今天只看一条 AI 相关变化，我建议别把“{event}”当普通新闻刷过去。",
        ]
    if platform == "baijiahao":
        return [
            f"先说结论：{claim_text(topic, platform)}。",
            f"“{event}”表面像一条行业动态，但真正值得看的，是 {topic.approved_angle_medium}。",
        ]
    return [topic.core_judgment]


def context_bridge_block(topic: ApprovedTopic, platform: str) -> str:
    if platform == "x":
        return f"{topic.title} 这件事表面像功能/产品变化，但真正值得看的，是它会不会改写 {topic.approved_angle_medium}。"
    if platform == "xiaohongshu":
        return f"一句话背景：这不是单一新闻点，而是一条和 {topic.approved_angle_medium} 直接相关的变化。"
    if platform == "wechat":
        return (
            f"先补背景：{topic.title} 并不是孤立事件。真正值得读下去的原因是，"
            f"它把“{topic.approved_angle_medium}”这层变量提前暴露出来了。"
        )
    if platform == "zhihu":
        return f"背景补充：这件事之所以值得回答，不是因为 headline 本身，而是它说明了 {topic.approved_angle_medium}。"
    if platform == "bilibili":
        return f"背景桥接：如果只看事件本身，它像一条更新；但拉到 builder 视角，它其实在提示 {topic.approved_angle_medium}。"
    if platform == "toutiao":
        return f"背景很简单：这事不是单点新闻，它真正影响的是 {topic.approved_angle_medium}。"
    if platform == "baijiahao":
        return f"背景补充：把这件事放到 {topic.approved_angle_medium} 的框架里看，才更容易理解它为什么重要。"
    return f"背景桥接：{topic.approved_angle_medium}"


def user_payoff(topic: ApprovedTopic, platform: str) -> str:
    if platform in {"wechat", "zhihu", "baijiahao"}:
        return "帮读者快速建立一个可复用的判断框架，而不是只看完一条资讯。"
    if platform == "xiaohongshu":
        return "让用户快速明白：这件事跟自己、自己的机会和自己的 workflow 有什么关系。"
    if platform == "x":
        return "给读者一个能立刻转述的高信号判断。"
    if platform == "bilibili":
        return "让 builder 拿到能回到自己业务 / workflow 里验证的启发。"
    if platform == "toutiao":
        return "让泛读者快速判断：这事是不是值得继续跟。"
    return "让读者更快看懂这件事。"


def packaging_bundle(topic: ApprovedTopic) -> str:
    lines = [
        "# Packaging Bundle",
        "",
        f"- `topic_title`: `{topic.title}`",
        f"- `core_claim`: `{topic.core_judgment}`",
        f"- `angle_short`: `{topic.approved_angle_short}`",
        f"- `angle_full`: `{topic.approved_angle}`",
        "",
    ]
    for platform in topic.requested_platforms:
        lines.extend(
            [
                f"## {platform_name(platform)}",
                "",
                f"- `target_audience`: `{PLATFORM_AUDIENCE.get(platform, 'n/a')}`",
                f"- `hook_family`: `{PLATFORM_HOOK_FAMILY.get(platform, 'n/a')}`",
                f"- `cold_start_gap`: {cold_start_gap(topic, platform)}",
                f"- `cover_job`: {cover_job(platform)}",
                f"- `background_cash_line`: {background_cash_line(topic, platform)}",
                f"- `recommended_title`: {platform_title_options(topic, platform)[0]}",
                f"- `recommended_cover_or_packaging`: {platform_cover_options(topic, platform)[0]}",
                f"- `recommended_opening_hook`: {platform_opening_options(topic, platform)[0]}",
                f"- `why_this_package_wins`: 这组包装能更快把读者从 headline 拉到“{topic.approved_angle_medium}”这一层。",
                f"- `what_to_avoid`: 不要把 {topic.title} 写成单一功能快讯，也不要把对象藏太久。",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def context_bridge_notes(topic: ApprovedTopic) -> str:
    lines = [
        "# Context Bridge Notes",
        "",
        "## Minimum Event Kernel",
        "",
        *[f"- {item}" for item in minimum_event_kernel(topic)],
        "",
    ]
    if topic.delivery_lane == "morning_flash" and topic.source_refs:
        previews = [preview for preview in (source_packet_preview(ref) for ref in topic.source_refs) if preview]
        lines.extend(
            [
                "## Morning Roundup Guardrails",
                "",
                f"- `freshness_window`: `T-1 {topic.business_window_start} -> T {topic.business_window_end}`",
                f"- `selected_source_refs`: `{len(previews)}`",
                "- 只允许写下列 source refs 覆盖的事件，不得额外增写历史旧题、旧草稿或包外对象。",
                "- 若某条 source 只是二手媒体或社区讨论，正文只能把它写成“昨夜出现的信号 / 讨论”，不得编造成官方一手事实。",
                "",
                "## Selected Morning Source Packets",
                "",
            ]
        )
        if previews:
            lines.extend(
                f"- `{index}` `{preview['title']}` | `source_name`: `{preview['source_name']}` | `published_at`: `{preview['published_at']}` | `source_path`: `{preview['path']}`"
                for index, preview in enumerate(previews[:10], start=1)
            )
        else:
            lines.append("- `n/a`")
        lines.append("")
    for platform in topic.requested_platforms:
        lines.extend(
            [
                f"## {platform_name(platform)}",
                "",
                f"- `recommended_context_depth`: `{PLATFORM_CONTEXT_DEPTH.get(platform, 'short')}`",
                f"- `recommended_placement`: `hook 之后、抽象分析之前`",
                f"- `cold_start_gap`: {cold_start_gap(topic, platform)}",
                f"- `best_context_block`: {context_bridge_block(topic, platform)}",
                f"- `handoff_line`: 也正因为如此，真正值得拆的不是新闻本身，而是 {topic.approved_angle}。",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def audience_notes(topic: ApprovedTopic) -> str:
    lines = [
        "# Audience Translation Notes",
        "",
        f"- `core_claim`: `{topic.core_judgment}`",
        f"- `angle_short`: `{topic.approved_angle_short}`",
        "",
    ]
    for platform in topic.requested_platforms:
        lines.extend(
            [
                f"## {platform_name(platform)}",
                "",
                f"- `target_layer`: `{PLATFORM_AUDIENCE.get(platform, 'n/a')}`",
                f"- `reader_primary_question`: {PLATFORM_READER_QUESTION.get(platform, 'n/a')}",
                f"- `user_payoff_frame`: {user_payoff(topic, platform)}",
                f"- `what_must_not_change`: approved angle / core judgment / risk note / source refs",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def platform_render_plan(topic: ApprovedTopic) -> str:
    lines = [
        "# Platform Render Plan",
        "",
        f"- `topic_title`: `{topic.title}`",
        "",
    ]
    for platform in topic.requested_platforms:
        lines.extend(
            [
                f"## {platform_name(platform)}",
                "",
                f"- `render_goal`: 让 {platform_name(platform)} 版本第一屏就完成对象、stakes、why now 的交代。",
                f"- `first_screen_plan`: {platform_opening_options(topic, platform)[0]} + {context_bridge_block(topic, platform)}",
                f"- `emphasis_map`: 核心判断 / why now / 风险提示 / 1 个 proof anchor",
                f"- `section_job_map`: {' / '.join(section_job_map(platform))}",
                f"- `proof_cadence`: {proof_cadence(platform)}",
                f"- `cta_plan`: {PLATFORM_CTA.get(platform, '轻 CTA')}",
                f"- `render_hint`: {PLATFORM_RENDER_HINT.get(platform, '保持平台原生节奏。')}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def title_options(topic: ApprovedTopic) -> list[str]:
    base = topic.title
    angle = title_angle_fragment(topic.approved_angle_short)
    return [
        f"{base}：这件事真正值得看的，是 {angle}",
        f"别把 {base} 看小了，它可能意味着新的分发入口正在形成",
        f"{base} 背后，真正该看的变量是什么？",
        f"为什么 {base} 值得机构视角重新看一遍？",
        f"如果沿着 {angle} 去看，{base} 可能比表面更重要",
        f"3 个点看懂：{base} 到底改变了什么",
    ]


def summary_options(topic: ApprovedTopic) -> list[str]:
    return [
        f"先给结论：{topic.core_judgment} 这不是一条普通资讯，而是值得沿着“{topic.approved_angle_medium}”继续展开的题。",
        f"{topic.title} 表面看像一条新动态，但真正值得写的是：{why_now_text(topic, topic.requested_platforms[0] if topic.requested_platforms else 'wechat')}",
        f"如果只把 {topic.title} 当新闻看，很容易错过它更大的含义；更值得看的，是它会如何影响 {topic.approved_angle_medium}。",
    ]


def opening_hook_options(topic: ApprovedTopic) -> str:
    lines = [
        "# Opening Hook Options",
        "",
        f"- `topic_title`: `{topic.title}`",
        f"- `core_claim`: `{topic.core_judgment}`",
        "",
    ]
    for platform in topic.requested_platforms:
        hooks = platform_opening_options(topic, platform)
        lines.extend(
            [
                f"## {platform_name(platform)}",
                "",
                f"- `hook_version_1`: {hooks[0] if hooks else topic.core_judgment}",
                f"- `hook_version_2`: {hooks[1] if len(hooks) > 1 else (hooks[0] if hooks else topic.core_judgment)}",
                f"- `recommended_use`: 先用 `{platform_name(platform)}` 第一屏完成对象、stakes、why now，再决定是否下沉背景。",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def cta_mode(topic: ApprovedTopic) -> str:
    lines = [
        "# CTA Mode",
        "",
        f"- `topic_title`: `{topic.title}`",
        f"- `core_claim`: `{topic.core_judgment}`",
        "",
    ]
    for platform in topic.requested_platforms:
        lines.extend(
            [
                f"## {platform_name(platform)}",
                "",
                f"- `primary_cta_mode`: `{PLATFORM_CTA.get(platform, '轻 CTA')}`",
                f"- `cta_goal`: `{PLATFORM_READER_QUESTION.get(platform, '让读者继续互动或关注')}`",
                f"- `cta_rule`: `全篇只保留 1 个主 CTA，不要把关注、留言、私聊、转发全部堆在一起。`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def wechat_draft(topic: ApprovedTopic) -> str:
    platform = "wechat"
    titles = platform_title_options(topic, platform)
    cover = platform_cover_options(topic, platform)[0]
    opening = platform_opening_options(topic, platform)[0]
    bridge = context_bridge_block(topic, platform)
    audience = audience_text(topic, platform)
    claim = claim_text(topic, platform)
    why_now = why_now_text(topic, platform)
    why_fit = fit_text(topic, platform)
    evidence = evidence_paragraphs(topic, platform)
    return "\n".join(
        [
            f"# 微信稿｜{titles[0]}",
            "",
            "## 推荐包装",
            f"- 标题：{titles[0]}",
            f"- 封面文案：{cover}",
            f"- 首屏钩子：{opening}",
            f"- 背景桥接：{bridge}",
            f"- 主要受众：{audience}",
            "",
            "## 标题候选",
            *[f"- {item}" for item in titles],
            "",
            "## 品牌签名",
            WECHAT_BRAND_NAME,
            "",
            WECHAT_BRAND_SLOGAN,
            "",
            WECHAT_BRAND_DESCRIPTION,
            "",
            "## 开头",
            opening,
            "",
            bridge,
            "",
            f"我会把这件事概括成一句话：{claim}。",
            f"对 {audience} 来说，这条线的价值不在于追一条热搜，而在于提早判断 {topic.approved_angle_medium} 会不会真的开始成形。",
            "",
            "## 关注我们",
            WECHAT_FOLLOW_PROMPT,
            "",
            WECHAT_FOLLOW_DESCRIPTION,
            "",
            "## 为什么它不只是一次产品发布",
            f"表面上看，{topic.title} 只是一个当天很容易被转发的新闻点；但把它放进更长的行业时间轴里，这件事之所以值得写，是因为 {why_now}。",
            "这说明相关玩家已经不满足于只争一轮注意力，而是开始把能力、节奏、路线甚至平台位置一起往前推。真正要看的，不是“今天有没有新消息”，而是谁在借这次动作重新定义下一阶段的叙事。",
            f"这也是它适合在微信展开的原因：{why_fit}。",
            "",
            "## 目前能确认的信号",
            *evidence,
            "",
            "## 我的判断",
            *variable_answer_paragraphs(topic, platform),
            "",
            "## 边界和下一步",
            risk_boundary_paragraph(topic, platform),
            "- 接下来重点看：是否出现更完整的官方材料、更多可验证数据，以及用户和生态是否真的开始跟着变化。",
            "- 如果这些信号继续加密，这条题就不只是一篇快评，而有机会升级成一条值得连续跟踪的主线。",
            "",
            "## 轻 CTA",
            "- 如果你最近也在看这个方向，欢迎把你看到的一手信息和不同判断发给我。",
        ]
    ) + "\n"


def xiaohongshu_draft(topic: ApprovedTopic) -> str:
    platform = "xiaohongshu"
    titles = platform_title_options(topic, platform)
    cover = platform_cover_options(topic, platform)[0]
    opening = platform_opening_options(topic, platform)[0]
    bridge = context_bridge_block(topic, platform)
    audience = audience_text(topic, platform)
    claim = claim_text(topic, platform)
    why_now = why_now_text(topic, platform)
    evidence = platform_evidence_lines(topic, platform, max_items=3)
    return "\n".join(
        [
            f"# 小红书稿｜{titles[0]}",
            "",
            "## 推荐包装",
            f"- 封面：{cover}",
            f"- 首屏钩子：{opening}",
            f"- 一句话背景：{bridge}",
            "",
            "## 标题候选",
            *[f"- {item}" for item in titles],
            "",
            "## 正文",
            opening,
            "",
            f"今天这条最有意思的点，不是又多了一个 demo，而是 {topic.approved_angle_medium} 这件事，开始从“听起来很远”变成“普通用户也可能摸得到”。",
            f"如果你是 {audience}，最直接的影响不是要不要立刻换设备，而是你会开始重新判断手里的设备、工具和 workflow 还有没有被重写的可能。",
            "",
            f"事情本身并不复杂：{topic.title}。",
            f"但它今天值得看，不只是因为热度高，而是因为 {why_now}。",
            f"更直白一点说，真正重要的不是“又有一个新功能”，而是 {claim}。",
            "",
            "## 图卡文案",
            f"1. {titles[0]}",
            f"2. 真正值得看的是：{topic.approved_angle_medium}",
            f"3. 公开信号已经给到：{publish_evidence_phrase(evidence[0]) if evidence else '优先放官方或实测截图'}",
            f"4. 对你更实际的意义：{claim}",
            f"5. 先别过度兴奋：{topic.risk_note}",
            "",
            "## 配文",
            f"我会把这条题理解成一个很典型的“表面是新闻，实质是门槛变化”的案例。对 {audience} 来说，它最大的意义不是看完觉得厉害，而是你会更清楚接下来该把注意力放在哪里。",
            f"如果你准备继续跟，我最建议先看的公开信号是：{'；'.join(publish_evidence_phrase(item) for item in evidence) if evidence else '官方公告、实操截图、GitHub / 产品页更新'}。",
            f"一句话总结：{bridge}",
            "",
            "## 互动",
            "- 如果你也在看这个方向，欢迎留言说说你最关心哪个变量。",
            "- 这条建议先收藏，因为真正要看的不是热闹，而是后续会不会继续落地。",
            "",
            "## 标签",
            "#AI #Agent #开源工具 #内容工厂",
        ]
    ) + "\n"


def zhihu_draft(topic: ApprovedTopic) -> str:
    platform = "zhihu"
    titles = platform_title_options(topic, platform)
    opening = platform_opening_options(topic, platform)[0]
    bridge = context_bridge_block(topic, platform)
    audience = audience_text(topic, platform)
    claim = claim_text(topic, platform)
    why_now = why_now_text(topic, platform)
    evidence = evidence_paragraphs(topic, platform)
    return "\n".join(
        [
            f"# 知乎稿｜{titles[0]}",
            "",
            "## 先说结论",
            opening,
            "",
            f"如果只回答一句，我的判断是：{claim}。",
            "",
            "## 为什么这件事值得单独回答",
            f"很多类似话题之所以讨论几天就过去，是因为它们只提供了一个 headline，却没有提供足够强的结构变化。这个题不一样，它之所以值得单独回答，是因为 {why_now}。",
            f"换句话说，真正该讨论的，不是这条消息今天有没有热度，而是 {topic.approved_angle_medium} 会不会因此提前进入加速段。",
            "",
            "## 先把背景补齐",
            f"事情本身是：{topic.title}。",
            bridge,
            "",
            "## 先给证据锚点",
            *evidence,
            "",
            "## 这个问题真正该怎么看",
            f"如果沿着“{topic.approved_angle_medium}”这个框架去看，会发现它真正重要的不是表面事件，而是它可能对入口、分发、商业化或工作流边界带来的影响。",
            f"对 {audience} 来说，这个题最有价值的地方，不是重复一遍新闻，而是借这条新闻，尽快看清楚相关参与方到底在往哪个方向下注。",
            "",
            "## 我的判断",
            *variable_answer_paragraphs(topic, platform),
            "",
            "## 最后一句",
            risk_boundary_paragraph(topic, platform),
            f"所以我会把它视为值得继续跟踪的有效线索，但不会把它写成已经盖棺定论的结果。更值得做的，是沿着“{topic.approved_angle_medium}”继续看下去。",
        ]
    ) + "\n"


def x_thread(topic: ApprovedTopic) -> str:
    platform = "x"
    claim = claim_text(topic, platform)
    why_now = why_now_text(topic, platform)
    evidence = platform_evidence_lines(topic, platform, max_items=2)
    return "\n".join(
        [
            f"# X Thread｜{platform_title_options(topic, platform)[0]}",
            "",
            f"1/ {claim}",
            f"2/ Most people will read this as product news. The real shift is {topic.approved_angle_medium}.",
            f"3/ Why now: {why_now}",
            f"4/ What is already public: {publish_evidence_phrase(evidence[0]) if evidence else 'need stronger official / repo / benchmark proof'}",
            f"5/ Another useful signal: {publish_evidence_phrase(evidence[1]) if len(evidence) >= 2 else 'watch for follow-up proof from official sources'}",
            f"6/ Biggest risk: {topic.risk_note}",
            "7/ My read: worth tracking as a real line, but not a closed case yet.",
        ]
    ) + "\n"


def bilibili_draft(topic: ApprovedTopic) -> str:
    platform = "bilibili"
    titles = platform_title_options(topic, platform)
    opening = platform_opening_options(topic, platform)[0]
    bridge = context_bridge_block(topic, platform)
    audience = audience_text(topic, platform)
    claim = claim_text(topic, platform)
    why_now = why_now_text(topic, platform)
    evidence = evidence_paragraphs(topic, platform)
    return "\n".join(
        [
            f"# B站专栏稿｜{titles[0]}",
            "",
            "## 先给结论",
            opening,
            "",
            f"如果你是 {audience}，最值得带走的一句话就是：{claim}。",
            "",
            "## 这次真正变的不是热闹，而是门槛",
            f"表面上看，{topic.title} 像是一条很适合做演示和截图传播的消息；但如果你真在搭 workflow、跑本地模型或者做工具内容，这条线真正重要的地方在于 {why_now}。",
            f"也就是说，大家表面上在看一条案例，实际上更该看的，是 {topic.approved_angle_medium} 会不会因此提前落地。",
            "",
            "## 现在能确认到什么程度",
            *evidence,
            "",
            "## 对 builder 最重要的三个结论",
            *variable_answer_paragraphs(topic, platform),
            "",
            "## 最后一句",
            risk_boundary_paragraph(topic, platform),
            "如果后面还有更多实测、更多 repo 更新或者更多用户反馈，这条线就非常适合再做第二轮拆解，因为它已经不只是个 demo 话题了。",
        ]
    ) + "\n"


def toutiao_draft(topic: ApprovedTopic) -> str:
    platform = "toutiao"
    titles = platform_title_options(topic, platform)
    opening = platform_opening_options(topic, platform)[0]
    bridge = context_bridge_block(topic, platform)
    claim = claim_text(topic, platform)
    why_now = why_now_text(topic, platform)
    evidence = evidence_paragraphs(topic, platform)
    return "\n".join(
        [
            f"# 今日头条稿｜{titles[0]}",
            "",
            "## 标题候选",
            *[f"- {item}" for item in titles],
            "",
            "## 正文",
            opening,
            "",
            bridge,
            "",
            f"事情本身并不复杂：{topic.title}。",
            f"但这件事今天之所以值得看，不是因为它能刷到热榜，而是因为 {why_now}。",
            "",
            "## 先看一个可信锚点",
            *(evidence[:1] if evidence else [f"先看基础证据：{primary_ref(topic)}。"]),
            "",
            f"如果继续往下看，这条消息真正影响的，不只是表面的新闻热度，而是：{claim}。",
            f"所以普通读者最值得关心的，不是记住几个名词，而是记住这条变化会不会继续往 {topic.approved_angle_medium} 的方向发展。",
            f"当然也别忽视最大的风险点：{topic.risk_note}。",
            "",
            "如果后面这个方向继续发酵，最值得补看的不会是更多情绪，而是更多真实案例和验证信号。",
        ]
    ) + "\n"


def baijiahao_draft(topic: ApprovedTopic) -> str:
    platform = "baijiahao"
    titles = platform_title_options(topic, platform)
    opening = platform_opening_options(topic, platform)[0]
    bridge = context_bridge_block(topic, platform)
    claim = claim_text(topic, platform)
    why_now = why_now_text(topic, platform)
    evidence = evidence_paragraphs(topic, platform)
    return "\n".join(
        [
            f"# 百家号稿｜{titles[0]}",
            "",
            "## 开头结论",
            opening,
            "",
            f"如果只看一句判断，那就是：{claim}。",
            "",
            "## 这件事到底是什么",
            f"{topic.title} 本身是一个可以被快速转述的行业动态，但真正值得展开的地方，不在 headline，而在 {topic.approved_angle_medium}。",
            bridge,
            "",
            "## 为什么现在值得关注",
            f"{why_now}",
            "",
            "## 证据锚点",
            *evidence,
            "",
            "## 真正该怎么理解",
            *variable_answer_paragraphs(topic, platform),
            "",
            "## 当前阶段判断",
            risk_boundary_paragraph(topic, platform),
            f"所以 TH Capital 当前更倾向于把这个题放在“{topic.approved_angle_medium}”的框架里继续看，而不是把它当成一条已经兑现的确定性结论。",
        ]
    ) + "\n"


def citation_block(topic: ApprovedTopic) -> str:
    lines = [
        "# Citation Block",
        "",
        f"- `topic_title`: `{topic.title}`",
        f"- `approved_angle`: `{topic.approved_angle}`",
        f"- `approved_angle_short`: `{topic.approved_angle_short}`",
        f"- `risk_note`: `{topic.risk_note}`",
        "",
        "## Source Refs",
        "",
    ]
    if topic.source_refs:
        lines.extend(f"- `{ref}`" for ref in topic.source_refs)
    else:
        lines.append("- `n/a`")
    return "\n".join(lines).rstrip() + "\n"


def visual_asset_type(source_ref: str) -> str:
    ref = source_ref.lower()
    if not ref.startswith("http://") and not ref.startswith("https://"):
        return "分析素材引用（不建议直接截图）"
    if "x.com/" in ref or "twitter.com/" in ref:
        return "原始推文 / thread 截图"
    if ref.endswith(".pdf") or ".pdf?" in ref:
        return "PDF 首页标题截图"
    if "youtube.com/" in ref or "youtu.be/" in ref:
        return "视频标题区截图或官方缩略图"
    if "bilibili.com/" in ref:
        return "视频标题区截图或封面图"
    if "github.com/" in ref:
        return "Repo header / README 首屏截图"
    if any(domain in ref for domain in ["openai.com", "anthropic.com", "deepmind.google", "x.ai", "figure.ai"]):
        return "官方公告 / 产品页标题区截图"
    return "网页标题区截图"


def visual_best_use(source_ref: str) -> str:
    ref = source_ref.lower()
    if not ref.startswith("http://") and not ref.startswith("https://"):
        return "作为分析链路参考，不作为正文原始证据图"
    if "x.com/" in ref or "twitter.com/" in ref:
        return "正文前段作为原始事件证据锚点"
    if ref.endswith(".pdf") or ".pdf?" in ref:
        return "正文背景段后，证明公告 / 招股书 / 白皮书确已发布"
    if "github.com/" in ref:
        return "变量段前，证明对象真实存在且具备 traction / release 语境"
    if "youtube.com/" in ref or "youtu.be/" in ref or "bilibili.com/" in ref:
        return "正文中段，补充 demo / 访谈 / workflow 的原始视觉证据"
    return "正文前中段，作为原始来源与对象说明图"


STYLE_ROUTE_HINTS = [
    ("方法论 / workflow / skill / agent 教程", ("workflow", "skill", "agent", "教程", "手把手", "怎么做", "工作流", "拆解", "builder", "方法论")),
    ("产业判断 / 商业分析 / 融资与资本信号", ("融资", "收入", "估值", "资本", "商业", "产业", "公司", "市场", "deal", "ipo", "revenue", "利润")),
    ("技术前沿 / 模型进展 / 研究传播", ("模型", "研究", "论文", "benchmark", "基准", "架构", "训练", "推理", "开源模型")),
    ("工具体验 / builder 拆解 / 产品推荐", ("体验", "工具", "插件", "产品", "上手", "实测", "本地", "cli", "应用")),
]

STYLE_ROUTE_ALIASES = {
    re.sub(r"\s*/\s*", "/", route).strip().lower(): route for route, _ in STYLE_ROUTE_HINTS
}

VISUAL_ROUTE_BLUEPRINTS = {
    "方法论 / workflow / skill / agent 教程": {
        "theme": "proof-first tutorial",
        "aesthetic": "纸白底 + 深墨字 + 单一信号色；优先截图、结构图、workflow 图，禁止抽象 AI 海报。",
        "cover": "封面优先‘对象 + 方法收益’，必要时配 repo / 产品 / 结构卡，而不是幻想插画。",
        "platforms": {
            "wechat": [
                {
                    "slot": "slot_1",
                    "heading": "原始证据锚点",
                    "position": "首屏后 / why-now 段后",
                    "job": "先证明对象、发布和当前热度是真实存在的",
                    "preferred_asset": "repo / 官网 / 原帖截图",
                    "note": "第一张图必须把对象钉住，不要让读者先看抽象判断。",
                    "requirements": "只截标题区、hero 区或 README 首屏；至少保留对象名 + 发布主体 + 1 个有效信号。",
                    "fallback": "如果拿不到安全截图，就做‘对象卡 + 来源条’，但正文必须保留原始链接。",
                    "priority": "required",
                    "source_priority": "原始截图 > 官方资产 > 结构化解释卡",
                },
                {
                    "slot": "slot_2",
                    "heading": "约束 / 变量分类图",
                    "position": "背景讲清后",
                    "job": "把读者接下来要盯的几类输入、信号或约束一口气讲明白",
                    "preferred_asset": "四类信号卡 / 四象限图",
                    "note": "适合‘盯这几类 / 只回答这几个问题 / 方法分层输入’这类段落。",
                    "requirements": "明确写出 3-4 类，每类都要有名称 + 1 个具体信号示例，不许只有抽象标签。",
                    "fallback": "如果正文没有明显分类结构，就改成‘适合谁 / 不适合谁 / 什么时候别用’矩阵。",
                    "priority": "required",
                    "source_priority": "结构化解释卡 > 对比表 > AI 生成图",
                },
                {
                    "slot": "slot_3",
                    "heading": "分层架构图",
                    "position": "核心方法段前",
                    "job": "把 skill / agent / system 拆成可理解的分层结构",
                    "preferred_asset": "五层架构图 / 链路图",
                    "note": "适合‘五层 / 分层 / 上下游 / 输入输出链路’这类段落。",
                    "requirements": "每层都写清名称、核心问题和与上下层的关系；不要只做装饰性金字塔。",
                    "fallback": "如果分层不明显，就改成‘输入 -> 处理 -> 输出 -> 风险’链路图。",
                    "priority": "required",
                    "source_priority": "结构化解释卡 > 自绘图 > AI 生成图",
                },
                {
                    "slot": "slot_4",
                    "heading": "workflow 循环图",
                    "position": "执行步骤段前",
                    "job": "把方法真正落成每天可执行的 4 步或 5 步循环",
                    "preferred_asset": "workflow 图 / step card",
                    "note": "适合‘每天怎么跑 / 如何更新 / 如何迭代’这类段落。",
                    "requirements": "每一步都要有动作词和产出，不许只写名词；箭头关系必须能读懂。",
                    "fallback": "如果流程不闭环，就改成顺序步骤卡而不是圆环。",
                    "priority": "required",
                    "source_priority": "结构化解释卡 > 自绘图 > AI 生成图",
                },
            ],
            "zhihu": [
                {
                    "slot": "slot_1",
                    "heading": "对象与来源锚点",
                    "position": "answer-first 后",
                    "job": "先把对象和来源锚住",
                    "preferred_asset": "repo / 官网 / 原帖截图",
                    "note": "知乎用户更愿意接受先答后证，但证据要跟上。",
                    "requirements": "截图要能直接回答‘这到底是什么’。",
                    "fallback": "改成对象卡 + 简短来源条。",
                    "priority": "required",
                    "source_priority": "原始截图 > 官方资产 > 结构化解释卡",
                },
                {
                    "slot": "slot_2",
                    "heading": "方法分层图",
                    "position": "论证段前",
                    "job": "把方法拆成分层结构",
                    "preferred_asset": "分层架构图",
                    "note": "知乎版允许更硬核，但不能只剩抽象框架。",
                    "requirements": "层级要清楚写出输入、处理、判断和输出。",
                    "fallback": "退成 4 步步骤图。",
                    "priority": "required",
                    "source_priority": "结构化解释卡 > 自绘图 > AI 生成图",
                },
                {
                    "slot": "slot_3",
                    "heading": "执行 workflow 图",
                    "position": "结论前",
                    "job": "告诉读者方法如何真正跑起来",
                    "preferred_asset": "workflow 图",
                    "note": "结论前补执行路径，增强可操作性。",
                    "requirements": "至少 3 步，且每步对应正文动作。",
                    "fallback": "改成 checklist 卡。",
                    "priority": "optional",
                    "source_priority": "结构化解释卡 > 自绘图 > AI 生成图",
                },
            ],
            "xiaohongshu": [
                {
                    "slot": "slot_1",
                    "heading": "封面主结论卡",
                    "position": "封面卡",
                    "job": "让用户一眼知道这套方法能解决什么问题",
                    "preferred_asset": "结论卡 / 数字卡",
                    "note": "封面只保留一个主 claim，不要塞满副标题。",
                    "requirements": "主标题短、对象明确、副标题只补收益或风险。",
                    "fallback": "改成‘别再怎么做 / 现在该怎么做’对比卡。",
                    "priority": "required",
                    "source_priority": "结构化结论卡 > 官方资产",
                },
                {
                    "slot": "slot_2",
                    "heading": "对象截图",
                    "position": "第 2 张",
                    "job": "把对象和来源讲明白",
                    "preferred_asset": "repo / 官网截图",
                    "note": "第二张必须让用户知道这不是空口方法论。",
                    "requirements": "优先截对象名、核心界面或 repo header。",
                    "fallback": "对象卡 + 来源条。",
                    "priority": "required",
                    "source_priority": "原始截图 > 官方资产 > 结构化解释卡",
                },
                {
                    "slot": "slot_3",
                    "heading": "分类 / workflow 卡",
                    "position": "第 3-4 张",
                    "job": "把核心方法拆清楚",
                    "preferred_asset": "分类卡 / workflow 图",
                    "note": "小红书更适合每张卡只讲一个动作。",
                    "requirements": "一张卡不要超过 4 个点；每个点要能读完就懂。",
                    "fallback": "拆成两张卡，不要硬塞。",
                    "priority": "required",
                    "source_priority": "结构化解释卡 > 自绘图 > AI 生成图",
                },
            ],
            "x": [
                {
                    "slot": "slot_1",
                    "heading": "原始对象截图",
                    "position": "thread 第 2-3 条",
                    "job": "快速补一手证据",
                    "preferred_asset": "原始截图",
                    "note": "X 里第一张图要帮 thread 站住脚。",
                    "requirements": "一张图就说清对象是谁、信号是什么。",
                    "fallback": "短对象卡。",
                    "priority": "required",
                    "source_priority": "原始截图 > 官方资产",
                },
                {
                    "slot": "slot_2",
                    "heading": "workflow 摘要卡",
                    "position": "thread 中段",
                    "job": "把方法压缩成可转发的结构图",
                    "preferred_asset": "step card",
                    "note": "X 版只留最能截图传播的那张结构卡。",
                    "requirements": "最多 4 步，每步一行动词。",
                    "fallback": "改成 3 个 bullet 卡。",
                    "priority": "optional",
                    "source_priority": "结构化解释卡 > 自绘图",
                },
            ],
        },
    },
    "工具体验 / builder 拆解 / 产品推荐": {
        "theme": "editorial product teardown",
        "aesthetic": "真实产品界面 + 对比卡 + 适配矩阵，不要用抽象 AI 人物图代替产品。",
        "cover": "封面优先‘对象 + 收益 + 适合谁’，最好带真实界面或功能模块图。",
        "platforms": {
            "wechat": [
                {
                    "slot": "slot_1",
                    "heading": "对象与界面截图",
                    "position": "首屏后",
                    "job": "先证明产品真实存在、长什么样",
                    "preferred_asset": "产品页 / 操作界面截图",
                    "note": "第一张图必须是产品本体，不要先做抽象海报。",
                    "requirements": "截功能区、核心按钮或关键结果，不截整页无重点。",
                    "fallback": "对象卡 + 功能摘要。",
                    "priority": "required",
                    "source_priority": "原始截图 > 官方资产 > 结构化解释卡",
                },
                {
                    "slot": "slot_2",
                    "heading": "前后对比图",
                    "position": "收益点段前",
                    "job": "把‘值不值得用’讲成可见变化",
                    "preferred_asset": "前后对比卡 / 流程对比图",
                    "note": "适合省步骤、省时间、少踩坑的收益段。",
                    "requirements": "明确写出使用前、使用后和最直观差异。",
                    "fallback": "改成‘多做什么 / 少做什么’双栏卡。",
                    "priority": "required",
                    "source_priority": "结构化解释卡 > 自绘图 > AI 生成图",
                },
                {
                    "slot": "slot_3",
                    "heading": "适合谁 / 不适合谁矩阵",
                    "position": "边界段前",
                    "job": "帮助读者快速判断自己是否该试",
                    "preferred_asset": "四象限图 / 用户矩阵",
                    "note": "不要把所有产品都写成人人都该上。",
                    "requirements": "至少列出 2 类适合人群和 2 类不适合人群。",
                    "fallback": "改成风险提醒卡。",
                    "priority": "required",
                    "source_priority": "结构化解释卡 > 自绘图 > AI 生成图",
                },
            ],
        },
    },
    "大热点解释 / 冷启动用户较多的事件稿": {
        "theme": "cold-start event explainer",
        "aesthetic": "首屏证据图 + 对象解释卡 + 时间线或变量卡，先让冷启动读者不迷路。",
        "cover": "封面优先‘对象 + 为什么跟你有关’，别只做空洞情绪封面。",
        "platforms": {
            "wechat": [
                {
                    "slot": "slot_1",
                    "heading": "事件原始证据图",
                    "position": "首屏后",
                    "job": "证明事件真的发生了",
                    "preferred_asset": "公告 / 原帖 / 官方页面截图",
                    "note": "第一张图要像证据，不要像气氛图。",
                    "requirements": "保留对象、时间或发布主体中的至少两个信号。",
                    "fallback": "对象卡 + 来源条。",
                    "priority": "required",
                    "source_priority": "原始截图 > 官方资产 > 结构化解释卡",
                },
                {
                    "slot": "slot_2",
                    "heading": "对象解释卡",
                    "position": "背景 bridge 段后",
                    "job": "让冷启动读者快速知道对象是谁、变化是什么",
                    "preferred_asset": "对象解释卡 / 产品页截图",
                    "note": "这一张负责回答‘这到底是什么事’。",
                    "requirements": "对象、变化、stakes 至少写清两项。",
                    "fallback": "时间线卡。",
                    "priority": "required",
                    "source_priority": "对象卡 > 官方资产 > 自绘图",
                },
                {
                    "slot": "slot_3",
                    "heading": "变量 / 时间线图",
                    "position": "核心论证段前",
                    "job": "把事情为什么重要讲成结构变化",
                    "preferred_asset": "时间线图 / 变量图",
                    "note": "适合 why now、影响链和变量变化段。",
                    "requirements": "时间线不要只列日期，要列转折点；变量图要写变量间关系。",
                    "fallback": "改成三段式解释卡。",
                    "priority": "required",
                    "source_priority": "结构化解释卡 > 自绘图 > AI 生成图",
                },
                {
                    "slot": "slot_4",
                    "heading": "风险边界卡",
                    "position": "风险段前",
                    "job": "提醒读者哪些结论还不能下死",
                    "preferred_asset": "风险卡 / 对比图",
                    "note": "防止热点稿写成情绪稿。",
                    "requirements": "至少写清 2 个仍待观察变量。",
                    "fallback": "改成‘别急着下结论’清单卡。",
                    "priority": "optional",
                    "source_priority": "结构化解释卡 > 自绘图",
                },
            ],
        },
    },
    "产业判断 / 商业分析 / 融资与资本信号": {
        "theme": "editorial capital analysis",
        "aesthetic": "原始证据图 + 数字信号卡 + 变量关系图，少做情绪型海报。",
        "cover": "封面优先用数字、公司名和核心变化，不要只写抽象行业判断。",
        "platforms": {
            "wechat": [
                {
                    "slot": "slot_1",
                    "heading": "硬信息证据图",
                    "position": "首屏后",
                    "job": "先把对象、金额、交易或核心变化钉死",
                    "preferred_asset": "公告 / 数据 / 新闻源截图",
                    "note": "第一张图就是证据图，不要拿抽象图替代融资或收入事实。",
                    "requirements": "保留公司名、数字、主体和发布时间中的关键元素。",
                    "fallback": "数字卡 + 来源条。",
                    "priority": "required",
                    "source_priority": "原始截图 > 官方资产 > 数字卡",
                },
                {
                    "slot": "slot_2",
                    "heading": "关键信号卡",
                    "position": "变量段前",
                    "job": "把 3-4 个最关键商业变量讲清楚",
                    "preferred_asset": "信号卡 / 四类变量图",
                    "note": "适合收入、算力、供给链、竞争压力这类变量。",
                    "requirements": "每个信号必须写明‘是什么 + 为什么重要’。",
                    "fallback": "改成双栏对比卡。",
                    "priority": "required",
                    "source_priority": "结构化解释卡 > 自绘图 > AI 生成图",
                },
                {
                    "slot": "slot_3",
                    "heading": "关系 / 链路图",
                    "position": "深度分析段前",
                    "job": "把公司、供应链或竞争关系画清楚",
                    "preferred_asset": "关系图 / 链路图",
                    "note": "不要让读者只看到数字，看不到背后结构。",
                    "requirements": "至少标出 3 个节点和它们的关系方向。",
                    "fallback": "改成竞争格局卡。",
                    "priority": "required",
                    "source_priority": "结构化解释卡 > 自绘图 > AI 生成图",
                },
            ],
        },
    },
    "技术前沿 / 模型进展 / 研究传播": {
        "theme": "research-to-stakes explainer",
        "aesthetic": "论文 / repo 证据图 + 能力变化卡 + benchmark/结构图，避免技术题只剩大词和废图。",
        "cover": "封面优先‘对象 + 多了什么能力 + 为什么值得看’，不要只塞模型名。",
        "platforms": {
            "wechat": [
                {
                    "slot": "slot_1",
                    "heading": "论文 / repo 证据图",
                    "position": "首屏后",
                    "job": "证明研究对象真实存在、确实发布了",
                    "preferred_asset": "PDF 首页 / repo header / 官方页截图",
                    "note": "技术前沿题先把对象钉住，再讲概念。",
                    "requirements": "保留标题、作者 / 机构或 repo 核心信号。",
                    "fallback": "对象卡 + 来源条。",
                    "priority": "required",
                    "source_priority": "原始截图 > 官方资产 > 结构化解释卡",
                },
                {
                    "slot": "slot_2",
                    "heading": "能力变化卡",
                    "position": "对象讲清后",
                    "job": "回答‘这次到底多了什么能力’",
                    "preferred_asset": "能力变化卡 / 对比图",
                    "note": "适合新能力、性能变化或体验变化段。",
                    "requirements": "至少写清旧状态、新状态和对用户的含义。",
                    "fallback": "改成‘以前 vs 现在’双栏卡。",
                    "priority": "required",
                    "source_priority": "结构化解释卡 > 自绘图 > AI 生成图",
                },
                {
                    "slot": "slot_3",
                    "heading": "benchmark / 结构图",
                    "position": "核心论证段前",
                    "job": "把性能、架构或系统关系讲明白",
                    "preferred_asset": "benchmark 图 / 结构图",
                    "note": "如果正文重点是结构而不是分数，就优先结构图。",
                    "requirements": "图里只保留对结论真正有用的指标或层级。",
                    "fallback": "改成三点总结卡。",
                    "priority": "required",
                    "source_priority": "结构化解释卡 > 官方图 > 自绘图",
                },
            ],
        },
    },
}


def extract_style_route_hint(text: str) -> str:
    match = re.search(r"style_route=([^;]+)", clean(text, ""))
    return clean(match.group(1), "") if match else ""


def normalize_style_route(route: str) -> str:
    value = clean(route, "")
    if not value:
        return ""
    alias_key = re.sub(r"\s*/\s*", "/", value).strip().lower()
    return STYLE_ROUTE_ALIASES.get(alias_key, value)


def infer_content_route(topic: ApprovedTopic) -> str:
    explicit = extract_style_route_hint(topic.special_instructions)
    if explicit:
        normalized = normalize_style_route(explicit)
        if normalized in VISUAL_ROUTE_BLUEPRINTS:
            return normalized
    haystack = " ".join(
        [
            clean(topic.title, ""),
            clean(topic.approved_angle, ""),
            clean(topic.approved_angle_short, ""),
            clean(topic.special_instructions, ""),
            clean(topic.delivery_lane, ""),
        ]
    ).lower()
    for route, keywords in STYLE_ROUTE_HINTS:
        if any(keyword in haystack for keyword in keywords):
            return normalize_style_route(route)
    return "大热点解释 / 冷启动用户较多的事件稿"


def inline_visual_slots(topic: ApprovedTopic, platform: str) -> list[dict[str, str]]:
    route = infer_content_route(topic)
    blueprint = VISUAL_ROUTE_BLUEPRINTS.get(route, VISUAL_ROUTE_BLUEPRINTS["大热点解释 / 冷启动用户较多的事件稿"])
    return blueprint["platforms"].get(platform) or blueprint["platforms"].get("wechat") or []


def inline_visual_plan(topic: ApprovedTopic) -> str:
    route = infer_content_route(topic)
    blueprint = VISUAL_ROUTE_BLUEPRINTS.get(route, VISUAL_ROUTE_BLUEPRINTS["大热点解释 / 冷启动用户较多的事件稿"])
    lines = [
        "# Inline Visual Plan",
        "",
        f"- `draft_key`: `{topic.topic_key}`",
        f"- `topic_title`: `{topic.title}`",
        f"- `approved_angle`: `{topic.approved_angle}`",
        "",
        "## Visual Strategy",
        "",
        f"- `content_route`: `{route}`",
        f"- `core_visual_goal`: `用图片同时完成原始证据、对象解释和阅读节奏控制，服务“{topic.approved_angle_short}”。`",
        f"- `visual_theme`: `{blueprint['theme']}`",
        f"- `aesthetic_system`: `{blueprint['aesthetic']}`",
        "- `preferred_asset_order`: `原始截图 > 官方资产 > 结构化解释卡 > 安全外部图 > AI 生成图`",
        "- `hard_rule`: `AI 生成图只能解释结构，不能证明事实。`",
        "- `hard_ban`: `抽象 AI 人像、赛博脑回路、无对象光束图、看起来像封面却什么都没解释的海报`",
        "",
        "## Platform Slots",
        "",
    ]
    for platform in topic.requested_platforms:
        lines.extend([f"### `{PLATFORM_DISPLAY.get(platform, platform)}`", ""])
        for slot in inline_visual_slots(topic, platform):
            lines.extend(
                [
                    f"#### `{slot['slot']}`｜{slot['heading']}",
                    "",
                    f"- `position`: `{slot['position']}`",
                    f"- `job`: `{slot['job']}`",
                    f"- `preferred_asset`: `{slot['preferred_asset']}`",
                    f"- `note`: `{slot['note']} 这张图优先服务“{PLATFORM_READER_QUESTION.get(platform, '理解主题')}”。`",
                    f"- `requirements`: `{slot['requirements']}`",
                    f"- `fallback`: `{slot['fallback']}`",
                    f"- `priority`: `{slot['priority']}`",
                    f"- `source_priority`: `{slot['source_priority']}`",
                    "",
                ]
            )
    lines.extend(["## Source Candidates", ""])
    if topic.source_refs:
        for index, ref in enumerate(topic.source_refs[:6], start=1):
            lines.extend(
                [
                    f"- `candidate_{index}`: `{ref}`",
                    f"- `asset_type`: `{visual_asset_type(ref)}`",
                    f"- `best_use`: `{visual_best_use(ref)}`",
                    "",
                ]
            )
    else:
        lines.append("- `candidate_1`: `n/a`")
        lines.append("- `asset_type`: `待补原始 source ref 后生成`")
        lines.append("- `best_use`: `优先补原始证据图`")
        lines.append("")
    lines.extend(
        [
            "## Human QC",
            "",
            "- 这张图是在证明事实、解释结构，还是只是在装饰？",
            "- 第一张正文图能不能当作原始证据锚点？",
            "- 有没有哪一段本应放图，但现在读起来一片纯文字？",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def visual_notes(topic: ApprovedTopic) -> str:
    route = infer_content_route(topic)
    blueprint = VISUAL_ROUTE_BLUEPRINTS.get(route, VISUAL_ROUTE_BLUEPRINTS["大热点解释 / 冷启动用户较多的事件稿"])
    lines = [
        "# Visual Notes",
        "",
        f"- `main_message`: `{topic.approved_angle_short}`",
        f"- `angle_full`: `{topic.approved_angle}`",
        f"- `content_route`: `{route}`",
        f"- `cover_direction`: `{blueprint['cover']}`",
        f"- `aesthetic_system`: `{blueprint['aesthetic']}`",
        "",
        "## Unified Aesthetic",
        "",
        "- 背景优先纸白 / 浅灰，文字用深墨，只保留 1 个信号色，不做多色霓虹。",
        "- 封面和正文图优先用对象截图、数字信号卡、结构图，不再默认上抽象 AI 图。",
        "- 一张图只做一件事：证明事实、解释结构、提醒边界，或者帮助传播。",
        "- 如果某个图位当前只能出烂图，宁可删掉，也不要为了‘有图’硬塞废图。",
        "",
        "## Recommended visuals",
        "",
        f"- 封面图优先服务“{topic.title}”，主标题只留一个强 claim，副标题只补收益或风险。",
        f"- 微信 / 知乎正文第一张图必须是对象或证据图，不要先上抽象海报。",
        f"- 结构解释图优先做‘四类信号卡 / 分层架构图 / workflow 图 / 适合谁矩阵’这些真正能帮助理解的卡片。",
        f"- 如果走 X / thread，只留最能截图传播的那一张结构卡，不要把长文里的所有图位硬搬过去。",
    ]
    if "bilibili" in topic.requested_platforms:
        lines.append(f"- 一张适合 B站专栏头图的横版封面：突出“{topic.title}”与“实操 / 拆解 / 复盘”语义。")
    if "toutiao" in topic.requested_platforms:
        lines.append(f"- 头条版建议配 1 张强对比封面图，主文案突出“为什么值得看”。")
    if "baijiahao" in topic.requested_platforms:
        lines.append(f"- 百家号版建议保留 1 张解释型配图，服务搜索用户快速理解主题。")
    return "\n".join(lines).rstrip() + "\n"


def revision_notes(topic: ApprovedTopic, status: str) -> str:
    lines = [
        "# Revision Notes",
        "",
        f"- `current_status`: `{status}`",
        f"- `special_instructions`: `{topic.special_instructions}`",
        f"- `platform_hint_from_topic`: `{topic.platform_hint}`",
        "",
        "## Editing discipline",
        "",
        "- 所有平台都要保留同一套核心判断，但表达方式必须重算。",
        "- 不得丢掉 citation 与 risk note。",
        "- 不得把公众号长文直接压缩成其他平台版本。",
    ]
    return "\n".join(lines).rstrip() + "\n"


def pack_card(
    topic: ApprovedTopic,
    status: str,
    pack_dir: Path,
    file_map: dict[str, Path | None],
    created_at: datetime,
    updated_at: datetime,
    draft_id_override: str | None = None,
) -> str:
    draft_id = draft_id_override or f"draft__{created_at.strftime('%Y%m%d_%H%M%S')}__{topic.topic_key}"
    def fmt_path(key: str) -> str:
        path = file_map.get(key)
        return str(path) if path else "n/a"
    next_step = "drafting -> ready"
    if status == "draft_ready":
        next_step = "draft_ready -> content-pack stage gate review"
    elif status == "needs_revision":
        next_step = "needs_revision -> revise current object"
    if status == "ready":
        next_step = "ready -> publish_queue (not started yet)"
    elif status in {"queued", "waiting_human_publish"}:
        next_step = "waiting_human_publish -> human publish / publish_url backfill"
    elif status == "published":
        next_step = "published -> review"
    elif status == "reviewed":
        next_step = "review closed"
    lines = [
        "# Draft Pack Card",
        "",
        f"- `draft_id`: `{draft_id}`",
        f"- `draft_key`: `{topic.topic_key}`",
        f"- `topic_id`: `{topic.topic_id}`",
        f"- `approved_topic_path`: `{topic.path}`",
        f"- `requested_platforms`: `{', '.join(topic.requested_platforms)}`",
        f"- `delivery_lane`: `{topic.delivery_lane}`",
        f"- `publish_mode`: `{topic.publish_mode}`",
        f"- `delivery_deadline`: `{topic.delivery_deadline}`",
        f"- `selection_scope`: `{topic.selection_scope}`",
        f"- `business_window_start`: `{topic.business_window_start}`",
        f"- `business_window_end`: `{topic.business_window_end}`",
        f"- `status`: `{status}`",
        f"- `created_at`: `{format_ts(created_at)}`",
        f"- `updated_at`: `{format_ts(updated_at)}`",
        "",
        "## Pack Paths",
        "",
        f"- `wechat_path`: `{fmt_path('wechat')}`",
        f"- `xiaohongshu_path`: `{fmt_path('xiaohongshu')}`",
        f"- `zhihu_path`: `{fmt_path('zhihu')}`",
        f"- `x_path`: `{fmt_path('x')}`",
        f"- `bilibili_path`: `{fmt_path('bilibili')}`",
        f"- `toutiao_path`: `{fmt_path('toutiao')}`",
        f"- `baijiahao_path`: `{fmt_path('baijiahao')}`",
        f"- `title_options_path`: `{fmt_path('title_options')}`",
        f"- `summary_options_path`: `{fmt_path('summary_options')}`",
        f"- `opening_hook_options_path`: `{fmt_path('opening_hook_options')}`",
        f"- `cta_mode_path`: `{fmt_path('cta_mode')}`",
        f"- `packaging_bundle_path`: `{fmt_path('packaging_bundle')}`",
        f"- `context_bridge_path`: `{fmt_path('context_bridge')}`",
        f"- `audience_notes_path`: `{fmt_path('audience_notes')}`",
        f"- `render_plan_path`: `{fmt_path('render_plan')}`",
        f"- `citation_block_path`: `{fmt_path('citation_block')}`",
        f"- `visual_notes_path`: `{fmt_path('visual_notes')}`",
        f"- `inline_visual_plan_path`: `{fmt_path('inline_visual_plan')}`",
        f"- `revision_notes_path`: `{fmt_path('revision_notes')}`",
        "",
        "## Carried Core",
        "",
        f"- `core_judgment`: `{topic.core_judgment}`",
        f"- `approved_angle`: `{topic.approved_angle}`",
        f"- `approved_angle_short`: `{topic.approved_angle_short}`",
        f"- `risk_note`: `{topic.risk_note}`",
        "",
        "## Next Step",
        "",
        f"- `next_step`: `{next_step}`",
        "- `publish_gate`: `not allowed yet`",
        f"- `pack_dir`: `{pack_dir}`",
    ]
    return "\n".join(lines).rstrip() + "\n"


def execution_log(topic: ApprovedTopic, status: str, pack_dir: Path, pack_card_path: Path) -> str:
    lines = [
        "# 同行资本市场内容系统｜Draft Pack Execution",
        "",
        f"- `topic_id`: `{topic.topic_id}`",
        f"- `topic_key`: `{topic.topic_key}`",
        f"- `approved_topic_path`: `{topic.path}`",
        f"- `requested_platforms`: `{', '.join(topic.requested_platforms)}`",
        f"- `delivery_lane`: `{topic.delivery_lane}`",
        f"- `publish_mode`: `{topic.publish_mode}`",
        f"- `delivery_deadline`: `{topic.delivery_deadline}`",
        f"- `pack_dir`: `{pack_dir}`",
        f"- `draft_pack_card_path`: `{pack_card_path}`",
        f"- `status`: `{status}`",
        "",
        "## Summary",
        "",
        f"- 已为 `{topic.title}` 生成 / 更新 Draft Pack。",
        f"- 当前平台范围：`{', '.join(topic.requested_platforms)}`。",
        f"- 当前状态：`{status}`。",
    ]
    return "\n".join(lines).rstrip() + "\n"


def update_approved_topic_status(text: str, target_status: str) -> str:
    current_match = re.search(r"^(- `status`: `)([^`]+)(`)\s*$", text, re.M)
    current = current_match.group(2) if current_match else ""
    mapped = "drafting" if target_status == "drafting" else "draft_ready"
    mapped = preserve_advanced_status(current, mapped)
    pattern = re.compile(r"^(- `status`: `)([^`]+)(`)\s*$", re.M)
    return pattern.sub(lambda match: f"{match.group(1)}{mapped}{match.group(3)}", text, count=1)


def safe_write(path: Path, content: str, overwrite: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return
    path.write_text(content, encoding="utf-8")


def build_files(topic: ApprovedTopic, pack_dir: Path) -> dict[str, tuple[Path, str, bool]]:
    files: dict[str, tuple[Path, str, bool]] = {}
    files["title_options"] = (
        pack_dir / "title-options.md",
        "# Title Options\n\n" + "\n".join(f"- {item}" for item in title_options(topic)) + "\n",
        True,
    )
    files["summary_options"] = (
        pack_dir / "summary-options.md",
        "# Summary Options\n\n" + "\n".join(f"- {item}" for item in summary_options(topic)) + "\n",
        True,
    )
    files["opening_hook_options"] = (pack_dir / "opening-hook-options.md", opening_hook_options(topic), True)
    files["cta_mode"] = (pack_dir / "cta-mode.md", cta_mode(topic), True)
    files["packaging_bundle"] = (pack_dir / "packaging-bundle.md", packaging_bundle(topic), True)
    files["context_bridge"] = (pack_dir / "context-bridge-notes.md", context_bridge_notes(topic), True)
    files["audience_notes"] = (pack_dir / "audience-notes.md", audience_notes(topic), True)
    files["render_plan"] = (pack_dir / "platform-render-plan.md", platform_render_plan(topic), True)
    files["citation_block"] = (pack_dir / "citation-block.md", citation_block(topic), True)
    files["visual_notes"] = (pack_dir / "visual-notes.md", visual_notes(topic), True)
    files["inline_visual_plan"] = (pack_dir / "inline-visual-plan.md", inline_visual_plan(topic), True)
    files["revision_notes"] = (pack_dir / "revision-notes.md", revision_notes(topic, "drafting"), True)

    generators = {
        "wechat": wechat_draft,
        "xiaohongshu": xiaohongshu_draft,
        "zhihu": zhihu_draft,
        "x": x_thread,
        "bilibili": bilibili_draft,
        "toutiao": toutiao_draft,
        "baijiahao": baijiahao_draft,
    }
    for platform in topic.requested_platforms:
        if platform in generators:
            filename = "x.md" if platform == "x" else f"{platform}.md"
            files[platform] = (pack_dir / filename, generators[platform](topic), False)
    return files


def main() -> None:
    args = parse_args()
    approved_topic_path = Path(args.approved_topic_path)
    if not approved_topic_path.exists():
        raise SystemExit(f"Approved topic not found: {approved_topic_path}")

    topic = load_approved_topic(approved_topic_path)
    draft_root = Path(args.draft_root)
    log_root = Path(args.log_root)
    pack_dir = draft_root / topic.topic_key
    current_time = now_cn()
    created_at = current_time
    updated_at = current_time
    files = build_files(topic, pack_dir)

    file_map: dict[str, Path | None] = {
        "wechat": files.get("wechat", (None, "", False))[0] if "wechat" in files else None,
        "xiaohongshu": files.get("xiaohongshu", (None, "", False))[0] if "xiaohongshu" in files else None,
        "zhihu": files.get("zhihu", (None, "", False))[0] if "zhihu" in files else None,
        "x": files.get("x", (None, "", False))[0] if "x" in files else None,
        "bilibili": files.get("bilibili", (None, "", False))[0] if "bilibili" in files else None,
        "toutiao": files.get("toutiao", (None, "", False))[0] if "toutiao" in files else None,
        "baijiahao": files.get("baijiahao", (None, "", False))[0] if "baijiahao" in files else None,
        "title_options": files["title_options"][0],
        "summary_options": files["summary_options"][0],
        "opening_hook_options": files["opening_hook_options"][0],
        "cta_mode": files["cta_mode"][0],
        "packaging_bundle": files["packaging_bundle"][0],
        "context_bridge": files["context_bridge"][0],
        "audience_notes": files["audience_notes"][0],
        "render_plan": files["render_plan"][0],
        "citation_block": files["citation_block"][0],
        "visual_notes": files["visual_notes"][0],
        "inline_visual_plan": files["inline_visual_plan"][0],
        "revision_notes": files["revision_notes"][0],
    }

    pack_card_path = pack_dir / "00_draft-pack-card.md"
    existing_draft_id: str | None = None
    effective_status = preserve_advanced_status(topic.status, args.status)
    if pack_card_path.exists():
        existing_fields = parse_simple_fields(pack_card_path)
        existing_draft_id = existing_fields.get("draft_id")
        effective_status = preserve_advanced_status(existing_fields.get("status", ""), args.status)
        effective_status = preserve_advanced_status(topic.status, effective_status)
        existing_created_at = existing_fields.get("created_at")
        if existing_created_at and existing_created_at != "n/a":
            try:
                created_at = datetime.strptime(existing_created_at, "%Y-%m-%d %H:%M:%S CST").replace(tzinfo=CN_TZ)
            except ValueError:
                created_at = current_time
    pack_card_text = pack_card(topic, effective_status, pack_dir, file_map, created_at, updated_at, existing_draft_id)
    log_path = log_root / f"{created_at.strftime('%Y%m%d_%H%M%S')}__{topic.topic_key}__draft-pack-execution.md"
    log_text = execution_log(topic, effective_status, pack_dir, pack_card_path)

    if args.write:
        pack_dir.mkdir(parents=True, exist_ok=True)
        safe_write(pack_card_path, pack_card_text, True)
        for key, (path, content, always_overwrite) in files.items():
            overwrite = always_overwrite or args.force_platform_overwrite
            if key == "revision_notes":
                content = revision_notes(topic, effective_status)
            safe_write(path, content, overwrite)
        log_root.mkdir(parents=True, exist_ok=True)
        log_path.write_text(log_text, encoding="utf-8")
        approved_text = approved_topic_path.read_text(encoding="utf-8")
        approved_topic_path.write_text(update_approved_topic_status(approved_text, effective_status), encoding="utf-8")
        print(pack_dir)
        print(pack_card_path)
        print(log_path)
        return

    print(pack_card_text)
    print("---")
    for key in PLATFORM_PREVIEW_ORDER + ["title_options", "summary_options", "packaging_bundle", "context_bridge", "audience_notes", "render_plan", "citation_block", "visual_notes", "inline_visual_plan", "revision_notes"]:
        if key not in files:
            continue
        path, content, _ = files[key]
        print(f"# Preview File: {path.name}")
        print(content)
        print("---")
    print(log_text)


if __name__ == "__main__":
    main()

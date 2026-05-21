#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import date, datetime
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import market_draft_pack_builder as draft_builder
from market_approved_topic_builder import Candidate, load_candidates
from market_frontstage_board_builder import FRONTSTAGE_GROUP_ID
from market_top5_board_utils import top5_board_is_ready


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
BOARD_DIR = ROOT / "03_topic_candidates"
FRONTSTAGE_DIR = ROOT / "11_frontstage"
BRIEFING_CARD_DIR = FRONTSTAGE_DIR / "day_mainline_briefing_cards"
SELECTION_STATE_DIR = FRONTSTAGE_DIR / "_selection_state"
CONTINUITY_BOARD_BUILDER = ROOT / "09_runbooks" / "scripts" / "market_top20_continuity_board_builder.py"
CN_TZ = ZoneInfo("Asia/Shanghai")
DEFAULT_ACCOUNT = "market"
DEFAULT_TARGET = f"chat:{FRONTSTAGE_GROUP_ID}"
DAY_MAINLINE_BRIEFING_HM = "17:40"
DAY_MAINLINE_DEFAULT_PICK_HM = "18:00"
DAY_MAINLINE_DRAFTBOX_DEADLINE_HM = "19:00"
BRIEFING_SEND_WINDOW_START_HM = "17:35"
BRIEFING_SEND_WINDOW_END_HM = "17:59"
COMMUNITY_DOMAINS = {"news.ycombinator.com", "old.reddit.com", "reddit.com", "github.com"}
OFFICIAL_DOMAINS = {
    "openai.com",
    "anthropic.com",
    "huggingface.co",
    "blog.google",
    "ai.google.dev",
    "deepmind.google",
    "googleblog.com",
    "colab.google",
}
MAINSTREAM_MEDIA_DOMAINS = {
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
PLACEHOLDER_TOPIC_PATTERNS = (
    re.compile(r"^P\d+\s*(?:推进|continuity|锚点|保底对象|槽位)", re.I),
    re.compile(r"^围绕「.+」这个新信号", re.I),
)
TITLE_LOCALIZATION_RULES = (
    (re.compile(r"OpenAI backs .*Illinois bill", re.I), "OpenAI 为伊州 AI 责任法案背书"),
    (re.compile(r"Molotov cocktail.*Sam Altman", re.I), "有人向 Sam Altman 家投掷燃烧弹"),
    (re.compile(r"Cirrus Labs.*OpenAI", re.I), "Cirrus Labs 团队确认加入 OpenAI"),
    (re.compile(r"Google Brings MCP Support to Colab", re.I), "Google 把 MCP 接进 Colab"),
    (re.compile(r"Agent Experience", re.I), "Agent Experience 工具体验"),
    (re.compile(r"Claude Mythos", re.I), "Claude Mythos bug 事件"),
    (re.compile(r"Working with files in ChatGPT", re.I), "ChatGPT 文件处理能力升级"),
    (re.compile(r"Anthropic.*18", re.I), "Anthropic 禁止 18 岁以下使用"),
    (re.compile(r"GLM 5\.1", re.I), "GLM 5.1 登顶开源代码竞技场"),
)

STYLE_ROUTE_SKILLS = {
    "方法论 / workflow / skill / agent 教程": {
        "primary_creator": "赛博禅心",
        "primary_skill": "th-style-overlay-cyber-zenmind",
        "secondary_creator": "数字生命卡兹克",
        "secondary_skill": "th-style-overlay-digitallife-khazix",
        "support_creator": "饼干哥哥AGI",
        "support_skill": "th-style-overlay-cookie-brother-agi",
        "borrowed_layers": "对象落地 / 步骤结构 / 背景桥接 / 判断句先行 / 收益点前置",
    },
    "工具体验 / builder 拆解 / 产品推荐": {
        "primary_creator": "饼干哥哥AGI",
        "primary_skill": "th-style-overlay-cookie-brother-agi",
        "secondary_creator": "袋鼠帝AI客栈",
        "secondary_skill": "th-style-overlay-kangaroo-ai-inn",
        "support_creator": "",
        "support_skill": "",
        "borrowed_layers": "收益点前置 / 步骤感 / 门槛转译 / 场景感",
    },
    "大热点解释 / 冷启动用户较多的事件稿": {
        "primary_creator": "量子位",
        "primary_skill": "th-style-overlay-qbitai",
        "secondary_creator": "机器之心",
        "secondary_skill": "th-style-overlay-jiqizhixin",
        "support_creator": "",
        "support_skill": "",
        "borrowed_layers": "对象识别 / 首屏证据 / why now / stakes / 大众转译",
    },
    "产业判断 / 商业分析 / 融资与资本信号": {
        "primary_creator": "智东西",
        "primary_skill": "th-style-overlay-zhidx",
        "secondary_creator": "数字生命卡兹克",
        "secondary_skill": "th-style-overlay-digitallife-khazix",
        "support_creator": "",
        "support_skill": "",
        "borrowed_layers": "硬信息前置 / 商业变量 / 风险边界 / 判断句力度",
    },
    "技术前沿 / 模型进展 / 研究传播": {
        "primary_creator": "机器之心",
        "primary_skill": "th-style-overlay-jiqizhixin",
        "secondary_creator": "量子位",
        "secondary_skill": "th-style-overlay-qbitai",
        "support_creator": "",
        "support_skill": "",
        "borrowed_layers": "对象识别 / 技术转译 / 首屏图证 / 变化表达",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build day_mainline founder-pick briefing cards from the daily Top5 board.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical day in YYYY-MM-DD.")
    parser.add_argument("--board-path", default="", help="Override Top5 board path.")
    parser.add_argument("--recommended-limit", type=int, default=2, help="How many recommended cards to prepare.")
    parser.add_argument("--holdout-limit", type=int, default=1, help="How many recallable holdout cards to prepare.")
    parser.add_argument("--write", action="store_true", help="Persist cards and selection state.")
    parser.add_argument("--send", action="store_true", help="Send each card as an individual Feishu message.")
    parser.add_argument("--dry-run", action="store_true", help="Build/send payloads without real delivery.")
    parser.add_argument("--account", default=DEFAULT_ACCOUNT, help="OpenClaw Feishu account id.")
    parser.add_argument("--target", default=DEFAULT_TARGET, help="OpenClaw Feishu target.")
    return parser.parse_args()


def clean(value: str | None, fallback: str = "") -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().strip("`") or fallback


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def parse_hm(raw: str) -> tuple[int, int]:
    hour, minute = [int(part) for part in raw.split(":", 1)]
    return hour, minute


def day_token(date_text: str) -> str:
    return date.fromisoformat(date_text).strftime("%Y%m%d")


def board_path_for(date_text: str, override: str) -> Path:
    if clean(override):
        return Path(override).expanduser().resolve()
    return BOARD_DIR / f"{day_token(date_text)}__daily-top8-to-top5.md"


def lane_dt(date_text: str, hm: str) -> datetime:
    target_day = date.fromisoformat(date_text)
    hour, minute = parse_hm(hm)
    return datetime(target_day.year, target_day.month, target_day.day, hour, minute, tzinfo=CN_TZ)


def now_in_window(date_text: str, start_hm: str, end_hm: str) -> bool:
    now = datetime.now(CN_TZ)
    return lane_dt(date_text, start_hm) <= now <= lane_dt(date_text, end_hm)


def board_signature(board_path: Path) -> str:
    if not board_path.exists():
        return "missing"
    payload = f"{board_path}|{board_path.stat().st_mtime_ns}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def ensure_board_ready(date_text: str, board_path: Path) -> Path:
    if top5_board_is_ready(board_path):
        return board_path
    if not CONTINUITY_BOARD_BUILDER.exists():
        return board_path
    command = [
        "python3",
        str(CONTINUITY_BOARD_BUILDER),
        "--date",
        date_text,
        "--allow-inferred-recovery",
        "--write",
    ]
    subprocess.run(command, capture_output=True, text=True, check=False)
    return board_path


def chinese_topic_line(candidate: Candidate) -> str:
    one_line = clean(candidate.detail_fields.get("一句话判断", ""), "")
    if one_line:
        one_line = re.sub(r"^P\d+\s*continuity\s*槽位[:：]\s*", "", one_line, flags=re.I)
        one_line = re.sub(r"^P\d+\s*槽位[:：]\s*", "", one_line, flags=re.I)
    if one_line and re.search(r"[\u4e00-\u9fff]", one_line) and not any(pattern.search(one_line) for pattern in PLACEHOLDER_TOPIC_PATTERNS):
        return one_line
    localized = localized_title(candidate)
    if localized and re.search(r"[\u4e00-\u9fff]", localized):
        return trim_text(localized, 60)
    angle = clean(candidate.detail_fields.get("建议切入角度", ""), "")
    if angle and re.search(r"[\u4e00-\u9fff]", angle):
        angle = re.sub(r"^以\s*", "", angle)
        angle = re.sub(r"\s*为入口.*$", "", angle)
        if angle and re.search(r"[\u4e00-\u9fff]", angle):
            return trim_text(angle, 60)
    title = clean(candidate.title, "")
    short_title = re.split(r"[–—-]|/|\\|:", title)[0].strip() or title
    if re.search(r"[\u4e00-\u9fff]", title):
        return trim_text(title, 60)
    return trim_text(f"围绕「{short_title}」这个新信号，讲清它为什么今天值得看。", 60)


def localized_title(candidate: Candidate) -> str:
    title = clean(candidate.title, "")
    if not title:
        return ""
    if re.search(r"[\u4e00-\u9fff]", title):
        return title
    for pattern, replacement in TITLE_LOCALIZATION_RULES:
        if pattern.search(title):
            return replacement
    candidate_key = clean(candidate.candidate_key, "").lower()
    if "/" in title:
        repo = title.split("/", 1)[-1].split("—", 1)[0].strip()
        if "github" in candidate_key or any(token in candidate_key for token in ("repo", "project")):
            return f"{repo}：开发者工具新项目"
    if "openai" in title.lower():
        return trim_text(f"OpenAI 相关新信号：{title}", 26)
    if "claude" in title.lower():
        return trim_text(f"Claude 新动态：{title}", 26)
    if "google" in title.lower():
        return trim_text(f"Google 新动态：{title}", 26)
    return trim_text(title, 36)


def route_for(candidate: Candidate) -> str:
    title = clean(candidate.title, "").lower()
    candidate_key = clean(candidate.candidate_key, "").lower()
    if any(token in candidate_key for token in ["github_", "githubtrending", "github_trending", "repo", "workflow", "agent", "cli"]):
        return "工具体验 / builder 拆解 / 产品推荐"
    if "/" in clean(candidate.title, "") and any(token in title for token in ["agent", "fund", "tool", "cli", "repo"]):
        return "工具体验 / builder 拆解 / 产品推荐"
    angle = clean(candidate.detail_fields.get("建议切入角度", ""), "") or clean(candidate.title, "")
    topic = SimpleNamespace(
        title=clean(candidate.title, ""),
        approved_angle=angle,
        approved_angle_short=trim_text(angle, 18),
        special_instructions="",
        delivery_lane="day_mainline",
    )
    return draft_builder.infer_content_route(topic)


def outline_for(candidate: Candidate, route: str) -> str:
    angle = clean(candidate.detail_fields.get("建议切入角度", ""), "")
    why_write = clean(candidate.detail_fields.get("为什么值得做", ""), "") or clean(candidate.recommended_reason, "")
    route_templates = {
        "方法论 / workflow / skill / agent 教程": "先交代读者为什么总会判断失真，再拆方法结构、关键步骤、怎么每天执行，最后补边界与风险。",
        "工具体验 / builder 拆解 / 产品推荐": "先讲旧痛点和新方案，再拆它怎么工作、谁最适合用、真实收益和不该高估的地方。",
        "大热点解释 / 冷启动用户较多的事件稿": "先把对象和原始信号说清，再解释 why now、普通人 stakes、深层变化，以及现在还不能下死结论的边界。",
        "产业判断 / 商业分析 / 融资与资本信号": "先交代硬事实和关键数字，再拆商业变量、行业含义、谁会受影响，以及最该继续盯的风险边界。",
        "技术前沿 / 模型进展 / 研究传播": "先说明这次技术变化具体多了什么，再翻译成真实能力变化、落地意义和仍需谨慎的限制。",
    }
    preferred = route_templates.get(route, route_templates["大热点解释 / 冷启动用户较多的事件稿"])
    if angle and re.search(r"[\u4e00-\u9fff]", angle):
        return trim_text(f"{preferred} 具体展开时围绕：{angle}", 150)
    if why_write:
        return trim_text(f"{preferred} 这题优先成立的原因是：{why_write}", 150)
    return trim_text(preferred, 150)


def trim_text(text: str, max_chars: int) -> str:
    normalized = clean(text, "")
    if len(normalized) <= max_chars:
        return normalized
    return normalized[: max_chars - 1].rstrip(" ，；：:。") + "…"


def approved_angle_for(candidate: Candidate, route: str) -> str:
    angle = clean(candidate.detail_fields.get("建议切入角度", ""), "")
    if angle:
        return angle
    if route == "大热点解释 / 冷启动用户较多的事件稿":
        return f"以 {candidate.title} 为入口，讲清对象、why now、影响链和当前阶段判断。"
    if route == "方法论 / workflow / skill / agent 教程":
        return f"围绕 {candidate.title}，把问题从热点描述改写成可复用的方法与执行路径。"
    if route == "工具体验 / builder 拆解 / 产品推荐":
        return f"围绕 {candidate.title}，讲清真实痛点、具体收益、适合人群和边界。"
    if route == "产业判断 / 商业分析 / 融资与资本信号":
        return f"围绕 {candidate.title}，优先交代硬事实和商业变量，再给行业判断。"
    return f"围绕 {candidate.title}，讲清这次变化本身、能力边界和实际意义。"


def cover_description(candidate: Candidate, route: str) -> str:
    if route == "方法论 / workflow / skill / agent 教程":
        return "封面：主标题做成判断句，右侧用 3 层方法框架或核心步骤提示这是一篇可执行教程。"
    if route == "工具体验 / builder 拆解 / 产品推荐":
        return "封面：对象名 + 旧痛点/新收益对照，别做抽象海报。"
    if route == "产业判断 / 商业分析 / 融资与资本信号":
        return "封面：对象 + 关键数字/信号卡，先把商业 stakes 钉住。"
    if route == "技术前沿 / 模型进展 / 研究传播":
        return "封面：模型/研究对象 + 这次具体多了什么，避免空泛技术感。"
    return "封面：对象 + why now 的一句判断，优先让冷启动读者知道这件事是什么。"


def image_outline(candidate: Candidate, route: str) -> list[str]:
    angle = approved_angle_for(candidate, route)
    topic = SimpleNamespace(
        title=clean(candidate.title, ""),
        approved_angle=angle,
        approved_angle_short=trim_text(angle, 18),
        special_instructions=f"style_route={route}",
        delivery_lane="day_mainline",
        requested_platforms=["wechat"],
    )
    outlines = [cover_description(candidate, route)]
    for slot in draft_builder.inline_visual_slots(topic, "wechat"):
        heading = clean(slot.get("heading", ""), "正文图")
        note = clean(slot.get("note", ""), "")
        position = clean(slot.get("position", ""), "")
        if position:
            outlines.append(f"正文图：{heading}，放在{position}，核心作用是{note or slot.get('job', '')}。")
        else:
            outlines.append(f"正文图：{heading}，核心作用是{note or slot.get('job', '')}。")
    return outlines


def style_profile_for(route: str) -> dict[str, str]:
    return STYLE_ROUTE_SKILLS.get(route, STYLE_ROUTE_SKILLS["大热点解释 / 冷启动用户较多的事件稿"])


def special_instructions_for(route: str, style: dict[str, str]) -> str:
    parts = [
        f"style_route={route}",
        f"primary_overlay={style['primary_creator']}",
        f"secondary_overlay={style['secondary_creator']}",
        f"borrowed_layers={style['borrowed_layers']}",
        "必须保留 TH Capital 判断边界",
        "正文必须服务微信公众号成稿与草稿箱交付",
    ]
    if style.get("support_creator"):
        parts.insert(3, f"support_overlay={style['support_creator']}")
    return "; ".join(parts)


def card_kind_label(card_role: str) -> str:
    if card_role == "holdout":
        return "候补"
    return "推荐"


def card_markdown(card: dict) -> str:
    image_lines = [f"- 图 {index + 1}：{item}" for index, item in enumerate(card["image_outline"])]
    return "\n".join(
        [
            f"# 白天线{card_kind_label(card['card_role'])}卡｜{card['card_label']}｜{card['display_title']}",
            "",
            f"- `date`: `{card['date']}`",
            f"- `candidate_rank`: `{card['rank']}`",
            f"- `candidate_key`: `{card['candidate_key']}`",
            f"- `default_if_no_reply_by_1800`: `{'yes' if card.get('default_pick') else 'no'}`",
            f"- `draftbox_deadline`: `{card['draftbox_deadline']}`",
            "",
            "## 中文题目",
            "",
            f"- {card['display_title']}",
            "",
            "## 1）话题",
            "",
            f"- {card['topic_line']}",
            "",
            "## 2）内容展开",
            "",
            f"- {card['outline']}",
            "",
            "## 3）写作风格 Skill",
            "",
            f"- 主 Skill：{card['style_profile']['primary_creator']}（`{card['style_profile']['primary_skill']}`）",
            f"- 辅 Skill：{card['style_profile']['secondary_creator']}（`{card['style_profile']['secondary_skill']}`）",
            *(
                [f"- 补位 Skill：{card['style_profile']['support_creator']}（`{card['style_profile']['support_skill']}`）"]
                if card["style_profile"].get("support_creator")
                else []
            ),
            f"- 路由：`{card['style_route']}`",
            "",
            "## 4）图片大纲",
            "",
            f"- 共 `{len(card['image_outline'])}` 张：封面 1 张，正文图 {max(len(card['image_outline']) - 1, 0)} 张。",
            *image_lines,
            "",
        ]
    ).rstrip() + "\n"


def send_feishu_message(account: str, target: str, message: str, dry_run: bool) -> dict:
    command = [
        "openclaw",
        "message",
        "send",
        "--channel",
        "feishu",
        "--account",
        account,
        "--target",
        target,
        "--message",
        message,
        "--json",
    ]
    if dry_run:
        command.append("--dry-run")
    result = subprocess.run(command, capture_output=True, text=True, timeout=60, check=False)
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "unknown delivery error").strip())
    raw = (result.stdout or result.stderr or "").strip()
    if not raw:
        return {"ok": True, "raw": ""}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"ok": True, "raw": raw}


def build_card_payload(date_text: str, candidate: Candidate, card_role: str, card_label: str, default_pick: bool) -> dict:
    route = route_for(candidate)
    style_profile = style_profile_for(route)
    outline = outline_for(candidate, route)
    image_plan = image_outline(candidate, route)
    return {
        "date": date_text,
        "card_role": card_role,
        "card_label": card_label,
        "rank": candidate.rank,
        "candidate_key": candidate.candidate_key,
        "title": clean(candidate.title, ""),
        "display_title": trim_text(localized_title(candidate), 32),
        "topic_line": chinese_topic_line(candidate),
        "outline": outline,
        "style_route": route,
        "style_profile": style_profile,
        "special_instructions": special_instructions_for(route, style_profile),
        "approved_angle": approved_angle_for(candidate, route),
        "image_outline": image_plan,
        "default_pick": default_pick,
        "draftbox_deadline": format_ts(lane_dt(date_text, DAY_MAINLINE_DRAFTBOX_DEADLINE_HM)),
    }


def index_markdown(date_text: str, board_path: Path, cards: list[dict], holdouts: list[dict]) -> str:
    lines = [
        "# Day Mainline Founder Pick Briefing",
        "",
        f"- `date`: `{date_text}`",
        f"- `generated_at`: `{format_ts(datetime.now(CN_TZ))}`",
        f"- `board_path`: `{board_path}`",
        f"- `briefing_at`: `{format_ts(lane_dt(date_text, DAY_MAINLINE_BRIEFING_HM))}`",
        f"- `default_pick_at`: `{format_ts(lane_dt(date_text, DAY_MAINLINE_DEFAULT_PICK_HM))}`",
        f"- `draftbox_deadline`: `{format_ts(lane_dt(date_text, DAY_MAINLINE_DRAFTBOX_DEADLINE_HM))}`",
        "",
        "## Recommended Cards",
        "",
    ]
    for card in cards:
        lines.append(f"- `{card['card_label']}`｜`rank={card['rank']}`｜`{card['display_title']}`")
    lines.extend(["", "## Holdout Cards", ""])
    if holdouts:
        for card in holdouts:
            lines.append(f"- `{card['card_label']}`｜`rank={card['rank']}`｜`{card['display_title']}`")
    else:
        lines.append("- `none`")
    return "\n".join(lines).rstrip() + "\n"


def candidate_source_urls(candidate: Candidate) -> list[str]:
    urls: list[str] = []
    for key in ("原始链接 / Source Packet", "原始链接", "Source Packet"):
        urls.extend(candidate.detail_lists.get(key, []))
    value = candidate.detail_fields.get("原始链接 / Source Packet", "")
    if value:
        urls.extend(re.findall(r"https?://\S+", value))
    deduped: list[str] = []
    for url in urls:
        normalized = clean(url, "")
        if normalized and normalized not in deduped:
            deduped.append(normalized)
    return deduped


def source_domain_score(candidate: Candidate) -> int:
    score = 0
    domains = {urlparse(url).netloc.lower() for url in candidate_source_urls(candidate) if "://" in url}
    for domain in domains:
        host = domain.lstrip("www.")
        if host in OFFICIAL_DOMAINS:
            score += 40
        if host in MAINSTREAM_MEDIA_DOMAINS:
            score += 24
        if host in COMMUNITY_DOMAINS:
            score -= 24
    return score


def candidate_briefing_priority(candidate: Candidate) -> int:
    score = 0
    if candidate.selection_bucket == "top5":
        score += 60
    elif candidate.selection_bucket == "holdout":
        score += 20
    score += max(0, 36 - candidate.rank * 4)
    score += source_domain_score(candidate)
    title = clean(candidate.title, "")
    topic_line = chinese_topic_line(candidate)
    if re.search(r"[\u4e00-\u9fff]", title):
        score += 28
    if re.search(r"[\u4e00-\u9fff]", topic_line):
        score += 16
    lowered = title.lower()
    if "/" in title:
        score -= 18
    if any(token in lowered for token in ("reddit", "hn frontpage", "show hn", "github trending")):
        score -= 22
    if any(token in lowered for token in ("openai", "anthropic", "google", "claude")):
        score += 10
    if any(token in clean(candidate.detail_fields.get("为什么值得做", ""), "").lower() for token in ("partial source", "需补", "补证")):
        score -= 10
    return score


def select_cards(candidates: dict[str, Candidate], recommended_limit: int, holdout_limit: int) -> tuple[list[Candidate], list[Candidate]]:
    ordered = [candidate for _, candidate in sorted(candidates.items())]
    ranked = sorted(
        ordered,
        key=lambda candidate: (candidate_briefing_priority(candidate), -candidate.rank, candidate.candidate_key),
        reverse=True,
    )
    recommended = ranked[: max(recommended_limit, 0)]
    remaining = [candidate for candidate in ranked if candidate.candidate_key not in {item.candidate_key for item in recommended}]
    holdouts = remaining[: max(holdout_limit, 0)]
    return recommended, holdouts


def main() -> None:
    args = parse_args()
    board_path = ensure_board_ready(args.date, board_path_for(args.date, args.board_path))
    if not board_path.exists():
        raise SystemExit(f"Top5 board not found: {board_path}")
    candidates = load_candidates(board_path)
    recommended, holdouts = select_cards(candidates, args.recommended_limit, args.holdout_limit)

    if not recommended:
        raise SystemExit(f"No recommended candidates found in board: {board_path}")

    token = day_token(args.date)
    cards = [
        build_card_payload(args.date, candidate, "recommended", f"推荐 {index}", default_pick=(index == 1))
        for index, candidate in enumerate(recommended, start=1)
    ]
    holdout_cards = [
        build_card_payload(args.date, candidate, "holdout", f"候补 {index}", default_pick=False)
        for index, candidate in enumerate(holdouts, start=1)
    ]

    state = {
        "date": args.date,
        "generated_at": format_ts(datetime.now(CN_TZ)),
        "board_path": str(board_path),
        "board_signature": board_signature(board_path),
        "status": "awaiting_founder_selection",
        "briefing_at": format_ts(lane_dt(args.date, DAY_MAINLINE_BRIEFING_HM)),
        "default_pick_at": format_ts(lane_dt(args.date, DAY_MAINLINE_DEFAULT_PICK_HM)),
        "draftbox_deadline": format_ts(lane_dt(args.date, DAY_MAINLINE_DRAFTBOX_DEADLINE_HM)),
        "default_choice_rank": cards[0]["rank"],
        "selected_rank": None,
        "selected_candidate_key": "",
        "selected_at": "",
        "selected_reason": "",
        "approved_topic_path": "",
        "draft_pack_dir": "",
        "bridge_request_id": "",
        "briefing_sent_at": "",
        "briefing_sent_signature": "",
        "recommended_cards": cards,
        "holdout_cards": holdout_cards,
    }

    index_path = FRONTSTAGE_DIR / f"{token}__day-mainline-founder-pick-briefing.md"
    state_path = SELECTION_STATE_DIR / f"{token}__day-mainline-founder-pick-state.json"

    existing_state: dict = {}
    if state_path.exists():
        try:
            existing_state = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing_state = {}
    if existing_state.get("selected_candidate_key"):
        state["status"] = existing_state.get("status", state["status"])
        state["selected_rank"] = existing_state.get("selected_rank")
        state["selected_candidate_key"] = existing_state.get("selected_candidate_key", "")
        state["selected_at"] = existing_state.get("selected_at", "")
        state["selected_reason"] = existing_state.get("selected_reason", "")
        state["approved_topic_path"] = existing_state.get("approved_topic_path", "")
        state["draft_pack_dir"] = existing_state.get("draft_pack_dir", "")
        state["bridge_request_id"] = existing_state.get("bridge_request_id", "")
    state["briefing_sent_at"] = existing_state.get("briefing_sent_at", "")
    state["briefing_sent_signature"] = existing_state.get("briefing_sent_signature", "")

    if args.write:
        BRIEFING_CARD_DIR.mkdir(parents=True, exist_ok=True)
        SELECTION_STATE_DIR.mkdir(parents=True, exist_ok=True)
        index_path.write_text(index_markdown(args.date, board_path, cards, holdout_cards), encoding="utf-8")
        for card in cards + holdout_cards:
            role_prefix = "recommended" if card["card_role"] == "recommended" else "holdout"
            card_path = BRIEFING_CARD_DIR / f"{token}__{role_prefix}_{card['rank']}__{card['candidate_key']}.md"
            card["card_path"] = str(card_path)
            card_path.write_text(card_markdown(card), encoding="utf-8")
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(index_path if args.write else index_markdown(args.date, board_path, cards, holdout_cards))
    if args.write:
        print(state_path)
        for card in cards + holdout_cards:
            print(card["card_path"])

    if args.send:
        if not now_in_window(args.date, BRIEFING_SEND_WINDOW_START_HM, BRIEFING_SEND_WINDOW_END_HM) and not args.dry_run:
            print(json.dumps({"briefing_status": "skip_send_outside_window", "date": args.date}, ensure_ascii=False))
            return
        if state.get("briefing_sent_signature") == state["board_signature"] and not args.dry_run:
            print(json.dumps({"briefing_status": "skip_duplicate_send", "date": args.date}, ensure_ascii=False))
            return
        delivery_cards = cards + holdout_cards
        for card in delivery_cards:
            payload = card_markdown(card)
            result = send_feishu_message(args.account, args.target, payload, dry_run=args.dry_run)
            print(json.dumps({"card_label": card["card_label"], "delivery_result": result}, ensure_ascii=False))
        if args.write and not args.dry_run:
            state["briefing_sent_at"] = format_ts(datetime.now(CN_TZ))
            state["briefing_sent_signature"] = state["board_signature"]
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

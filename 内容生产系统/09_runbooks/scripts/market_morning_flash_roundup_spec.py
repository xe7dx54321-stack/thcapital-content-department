#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
LOG_ROOT = ROOT / "10_logs"
CN_TZ = ZoneInfo("Asia/Shanghai")
SERIES_NAME = "AI早报"
SERIES_KEY_PREFIX = "ai_morning_brief"
PUBLISH_HM = "06:50"
STYLE_ROUTER_PATH = ROOT / "08_brand_assets" / "learning_knowledge_assets" / "latest__style-router.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the canonical morning roundup spec for morning_flash.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical day in YYYY-MM-DD.")
    parser.add_argument("--write", action="store_true", help="Write the spec into 10_logs.")
    return parser.parse_args()


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def day_token(date_text: str) -> str:
    return date.fromisoformat(date_text).strftime("%Y%m%d")


def title_for(target_day: date) -> str:
    return f"{SERIES_NAME}｜{target_day.month}月{target_day.day}日"


def topic_key_for(target_day: date) -> str:
    return f"{SERIES_KEY_PREFIX}_{target_day.strftime('%Y%m%d')}"


def render_spec(date_text: str) -> str:
    target_day = date.fromisoformat(date_text)
    title = title_for(target_day)
    topic_key = topic_key_for(target_day)
    return "\n".join(
        [
            "# Morning Flash Roundup Spec",
            "",
            f"- `generated_at`: `{now_cn().strftime('%Y-%m-%d %H:%M:%S CST')}`",
            f"- `date`: `{date_text}`",
            f"- `series_name`: `{SERIES_NAME}`",
            f"- `topic_key`: `{topic_key}`",
            f"- `title`: `{title}`",
            f"- `approved_angle`: `把 T-1 17:00 到 T 05:00 的 8-10 个 AI / 科技热点，整理成一篇适合早晨快速阅读的聚合早报；前半段先做“太长不看”，后半段再逐条展开，并在文末呼应今日最值得继续追踪的线索。`",
            f"- `selection_bucket`: `morning_flash_roundup`",
            f"- `selection_scope`: `previous_day_17_to_today_05_roundup_window`",
            f"- `planned_publish_at`: `{date_text} {PUBLISH_HM}:00 CST`",
            "- `event_count_target`: `8-10`",
            "- `body_image_policy`: `正文图非必需；以讲清事情为主，若无真正有信息量的图，可不放。`",
            f"- `style_skill_policy`: `业务岗必须先读 {STYLE_ROUTER_PATH}，再自行决定最适合今天这篇早报的风格 skill；不得把风格路由硬编码成固定公众号。`",
            "- `cover_policy`: `固定封面模板：保留“AI早报”主系列名，只更新日期角标；整体构图、字体层级、品牌位保持一致。`",
            "- `source_wording_policy`: `正文默认不写“某某公众号/媒体报道”式二手表述；若需要补信源，优先回到官方或原始链接，并放在 citation / source packet 层，不要把媒体名塞进标题、摘要和开头句。`",
            "",
            "## Required Structure",
            "",
            "1. 开头引子：一句交代今天这篇是什么，并自然带出同行资本的身份与观察视角。",
            "2. `太长不看`：放 8-10 个事件，每个条目必须是“子标题（20字内）+ 50字内概要”，并留一个自然钩子，提醒读者后文有更深解读或今日最关键主线总结。",
            "3. `详细阐述版`：与 `太长不看` 使用完全一致的子标题顺序；每条 300-400 字，讲清事实、影响、我们怎么看。",
            "4. 文末收束：回扣前面埋下的钩子，给出“今天最该继续盯什么”的一句总结。",
            "",
            "## Consistency Rules",
            "",
            "- 标题必须使用固定系列名，不允许今天一个名字、明天一个名字。",
            "- 封面必须使用固定模板，不允许每天完全换视觉语言。",
            "- 若要加正文图，优先用信息压缩图、关系图、时间线，不要为了凑图放低信息密度配图。",
            "",
        ]
    )


def main() -> None:
    args = parse_args()
    text = render_spec(args.date)
    if args.write:
        LOG_ROOT.mkdir(parents=True, exist_ok=True)
        path = LOG_ROOT / f"{day_token(args.date)}__morning-flash-roundup-spec.md"
        path.write_text(text, encoding="utf-8")
        print(path)
    print(text)


if __name__ == "__main__":
    main()

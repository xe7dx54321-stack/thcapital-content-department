#!/usr/bin/env python3
from __future__ import annotations

WECHAT_SOURCE_TARGETS: list[dict[str, str | list[str]]] = [
    {
        "source_id": "wechat__liangziwei",
        "source_name": "量子位",
        "packet_prefix": "wechat_qbitai",
        "query": "量子位",
        "aliases": ["量子位", "QbitAI"],
        "signal_quality": "high",
        "citation_reliability": "medium",
        "notes": "AI 大盘与热点快讯覆盖全，适合作为中文入口。",
    },
    {
        "source_id": "wechat__xinzhiyuan",
        "source_name": "新智元",
        "packet_prefix": "wechat_xinzhiyuan",
        "query": "新智元",
        "aliases": ["新智元", "AI_era"],
        "signal_quality": "high",
        "citation_reliability": "medium",
        "notes": "模型、产品、行业事件密度高。",
    },
    {
        "source_id": "wechat__jiqizhixin",
        "source_name": "机器之心",
        "packet_prefix": "wechat_jiqizhixin",
        "query": "机器之心",
        "aliases": ["机器之心", "almosthuman2014"],
        "signal_quality": "high",
        "citation_reliability": "medium",
        "notes": "AI 研究和产业报道较全，适合补中文语境。",
    },
    {
        "source_id": "wechat__geekpark",
        "source_name": "极客公园",
        "packet_prefix": "wechat_geekpark",
        "query": "极客公园",
        "aliases": ["极客公园"],
        "include_keywords": ["ai", "人工智能", "agent", "智能体", "大模型", "机器人", "aigc", "自动驾驶", "具身", "openai", "claude", "gemini", "deepseek", "cursor", "manus"],
        "signal_quality": "medium",
        "citation_reliability": "medium",
        "notes": "产品和创业叙事更强，适合公域转写。",
    },
    {
        "source_id": "wechat__founder_park",
        "source_name": "Founder Park",
        "packet_prefix": "wechat_founder_park",
        "query": "Founder Park",
        "aliases": ["Founder Park"],
        "signal_quality": "high",
        "citation_reliability": "medium",
        "notes": "创业者内容和 AI 产品观察质量高。",
    },
    {
        "source_id": "wechat__appsso",
        "source_name": "APPSO",
        "packet_prefix": "wechat_appsso",
        "query": "APPSO",
        "aliases": ["APPSO", "appsolution"],
        "include_keywords": ["ai", "人工智能", "agent", "智能体", "大模型", "机器人", "aigc", "自动驾驶", "具身", "openai", "claude", "gemini", "deepseek", "cursor", "manus"],
        "signal_quality": "medium",
        "citation_reliability": "medium",
        "notes": "大众产品热点和可传播角度较多。",
    },
    {
        "source_id": "wechat__guiguang_ai_tools",
        "source_name": "归藏的AI工具箱",
        "packet_prefix": "wechat_guizang_ai_tools",
        "query": "归藏的AI工具箱",
        "aliases": ["归藏的AI工具箱", "歸藏的AI工具箱", "op7418ux"],
        "signal_quality": "medium",
        "citation_reliability": "low-medium",
        "notes": "工具测评 / 教学 / 玩法线索价值高。",
    },
    {
        "source_id": "wechat__guixingren_pro",
        "source_name": "硅星人Pro",
        "packet_prefix": "wechat_guixingren_pro",
        "query": "硅星人Pro",
        "aliases": ["硅星人Pro", "Si-Planet"],
        "include_keywords": ["ai", "人工智能", "agent", "智能体", "大模型", "机器人", "aigc", "具身", "openai", "claude", "gemini", "deepseek", "cursor", "manus", "创业", "融资"],
        "signal_quality": "medium",
        "citation_reliability": "medium",
        "notes": "海外 AI 创业和产品语境补充强。",
    },
    {
        "source_id": "wechat__saibo_chanxin",
        "source_name": "赛博禅心",
        "packet_prefix": "wechat_saibo_chanxin",
        "rss_feed_id": "MP_WXS_3934419561",
        "query": "赛博禅心",
        "aliases": ["赛博禅心"],
        "include_keywords": ["ai", "人工智能", "agent", "智能体", "大模型", "机器人", "aigc", "openai", "claude", "gemini", "deepseek", "cursor", "manus"],
        "signal_quality": "high",
        "citation_reliability": "medium",
        "notes": "选题判断力和事件翻译能力强，适合作为头部学习池长期样本。",
    },
    {
        "source_id": "wechat__digital_life_khazix",
        "source_name": "数字生命卡兹克",
        "packet_prefix": "wechat_digital_life_khazix",
        "rss_feed_id": "MP_WXS_3223096120",
        "query": "数字生命卡兹克",
        "aliases": ["数字生命卡兹克", "卡兹克"],
        "include_keywords": ["ai", "人工智能", "agent", "智能体", "大模型", "机器人", "aigc", "openai", "claude", "gemini", "deepseek", "cursor", "manus"],
        "signal_quality": "high",
        "citation_reliability": "medium",
        "notes": "高热选题与传播包装能力强，适合深抓对标。",
    },
    {
        "source_id": "wechat__bingan_gege_agi",
        "source_name": "饼干哥哥AGI",
        "packet_prefix": "wechat_bingan_gege_agi",
        "rss_feed_id": "MP_WXS_2394281674",
        "query": "饼干哥哥AGI",
        "aliases": ["饼干哥哥AGI", "饼干哥哥 Agi", "饼干哥哥AI"],
        "include_keywords": ["ai", "人工智能", "agent", "智能体", "大模型", "机器人", "aigc", "openai", "claude", "gemini", "deepseek", "cursor", "manus", "工具", "效率"],
        "signal_quality": "high",
        "citation_reliability": "medium",
        "notes": "产品玩法、实操价值和用户兴趣匹配度高，适合学习题材选择与读者翻译。",
    },
    {
        "source_id": "wechat__kangaroo_ai_inn",
        "source_name": "袋鼠帝AI客栈",
        "packet_prefix": "wechat_kangaroo_ai_inn",
        "rss_feed_id": "MP_WXS_3903186594",
        "query": "袋鼠帝AI客栈",
        "aliases": ["袋鼠帝AI客栈", "袋鼠帝 ai 客栈", "袋鼠帝AI"],
        "include_keywords": ["ai", "人工智能", "agent", "智能体", "大模型", "机器人", "aigc", "openai", "claude", "gemini", "deepseek", "cursor", "manus", "工具", "教程"],
        "signal_quality": "high",
        "citation_reliability": "medium",
        "notes": "AI 工具、玩法和用户侧切口稳定，适合补产品导向和体验导向样本。",
    },
    {
        "source_id": "wechat__zhidx",
        "source_name": "智东西",
        "packet_prefix": "wechat_zhidx",
        "query": "智东西",
        "aliases": ["智东西", "zhidxcom"],
        "include_keywords": ["ai", "人工智能", "agent", "智能体", "大模型", "机器人", "aigc", "具身", "自动驾驶", "芯片", "算力", "openai", "claude", "gemini", "deepseek", "cursor", "manus"],
        "signal_quality": "high",
        "citation_reliability": "medium",
        "notes": "产业化、具身、硬件与大公司产品化观察价值高。",
    },
    {
        "source_id": "wechat__36kr",
        "source_name": "36氪",
        "packet_prefix": "wechat_36kr",
        "query": "36氪",
        "aliases": ["36氪", "36Kr", "wow36kr"],
        "include_keywords": ["ai", "人工智能", "agent", "智能体", "大模型", "机器人", "aigc", "具身", "自动驾驶", "openai", "claude", "gemini", "deepseek", "cursor", "manus", "seedance"],
        "signal_quality": "medium",
        "citation_reliability": "medium",
        "notes": "创业、融资、商业化和产品化叙事补充强。",
    },
    {
        "source_id": "wechat__ifanr",
        "source_name": "爱范儿",
        "packet_prefix": "wechat_ifanr",
        "query": "爱范儿",
        "aliases": ["爱范儿", "ifanr", "ifanrAppSo"],
        "include_keywords": ["ai", "人工智能", "agent", "智能体", "大模型", "机器人", "aigc", "具身", "ai硬件", "智能眼镜", "openai", "claude", "gemini", "deepseek", "cursor", "manus"],
        "signal_quality": "medium",
        "citation_reliability": "medium",
        "notes": "消费产品、AI 硬件和大众传播型题材补充强。",
    },
]

WECHAT_SOURCE_TARGETS_BY_ID = {
    str(row["source_id"]): row for row in WECHAT_SOURCE_TARGETS
}


def normalize_wechat_name(value: str) -> str:
    return "".join(str(value or "").strip().lower().split())


def aliases_for_target(target: dict[str, str | list[str]]) -> list[str]:
    aliases = [str(target.get("source_name", "")).strip(), str(target.get("query", "")).strip()]
    aliases.extend(str(item).strip() for item in (target.get("aliases") or []) if str(item).strip())
    deduped: list[str] = []
    seen: set[str] = set()
    for alias in aliases:
        if not alias:
            continue
        normalized = normalize_wechat_name(alias)
        if normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(alias)
    return deduped


def target_by_source_id(source_id: str) -> dict[str, str | list[str]] | None:
    return WECHAT_SOURCE_TARGETS_BY_ID.get(source_id)


WECHAT_SOURCE_TARGETS_BY_NORMALIZED_NAME = {
    normalize_wechat_name(str(row.get("source_name", ""))): row
    for row in WECHAT_SOURCE_TARGETS
    if str(row.get("source_name", "")).strip()
}


def target_by_source_name(source_name: str) -> dict[str, str | list[str]] | None:
    return WECHAT_SOURCE_TARGETS_BY_NORMALIZED_NAME.get(normalize_wechat_name(source_name))

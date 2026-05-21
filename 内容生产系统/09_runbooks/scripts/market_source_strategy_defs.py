#!/usr/bin/env python3
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class FunnelLayer:
    key: str
    name: str
    purpose: str


@dataclass(frozen=True)
class FunnelRule:
    pattern: re.Pattern[str]
    layer_key: str


FUNNEL_LAYERS: dict[str, FunnelLayer] = {
    "L1": FunnelLayer(
        key="L1",
        name="原始信源",
        purpose="拿到一手事件、原始口径、官方发布和可直接引用的 primary context。",
    ),
    "L2": FunnelLayer(
        key="L2",
        name="技术/产品扩散",
        purpose="判断技术圈、产品圈、开发者圈是否真的开始扩散与采用。",
    ),
    "L3": FunnelLayer(
        key="L3",
        name="中文行业传播",
        purpose="判断中文互联网如何叙事、哪些角度更容易被国内用户理解和转发。",
    ),
    "L4": FunnelLayer(
        key="L4",
        name="平台热度验证",
        purpose="验证是否破圈、是否跨平台发酵、是否值得当天正式写。",
    ),
}


FUNNEL_RULES: list[FunnelRule] = [
    FunnelRule(re.compile(r"^(web__openai_news|web__anthropic_news|web__deepmind_blog|web__google_blog_ai|web__huggingface_blog|web__xai_news|web__figure_news|web__tesla_ai_robotics|web__deepmind_robotics|web__nvidia_blog)"), "L1"),
    FunnelRule(re.compile(r"^(youtube__openai|youtube__googledeepmind|derived__)"), "L1"),
    FunnelRule(re.compile(r"^(trend__github_trending|trend__hn_|trend__trend_hunt_|trend__producthunt_|trend__yc_launches_ai|trend__huggingface_daily_papers|trend__arxiv_|trend__diandian_app_rank|trend__reddit_)"), "L2"),
    FunnelRule(re.compile(r"^(web__techcrunch_ai|web__finsmes_ai|web__finsmes_ai_gnews|web__deeplearningai_batch|web__semianalysis|web__infoq_ai_ml|web__simon_willison|web__latent_space|web__one_useful_thing|web__interconnects|web__understanding_ai|web__sensortower_blog|web__itjuzi|x__)"), "L2"),
    FunnelRule(re.compile(r"^(youtube__ycombinator|youtube__aidotengineer|youtube__latent_space_pod|youtube__langchain)"), "L2"),
    FunnelRule(re.compile(r"^(wechat__|web__sspai_ai|web__jiqizhixin_site|web__qbitai_site|web__zhidx|web__36kr_ai|web__ifanr_ai|web__appsso_site)"), "L3"),
    FunnelRule(re.compile(r"^(trend__bilibili_popular_all|trend__baidu_realtime|trend__newrank_wechat|trend__feigua_bilibili|trend__zhihu_hot|trend__weibo_hot|trend__xiaohongshu_search)"), "L4"),
]


def infer_funnel_layer(source_id: str, source_type: str = "", verification_status: str = "", platform: str = "") -> FunnelLayer:
    text = f"{source_id} {source_type} {verification_status} {platform}".strip()
    for rule in FUNNEL_RULES:
        if rule.pattern.search(text):
            return FUNNEL_LAYERS[rule.layer_key]

    lowered_source_type = source_type.lower()
    lowered_platform = platform.lower()
    lowered_verification = verification_status.lower()

    if "wechat" in lowered_platform or "wechat" in lowered_source_type:
        return FUNNEL_LAYERS["L3"]
    if lowered_platform in {"bilibili", "zhihu", "xiaohongshu", "weibo"}:
        return FUNNEL_LAYERS["L4"]
    if lowered_verification in {"primary-source", "official-video"}:
        return FUNNEL_LAYERS["L1"]
    return FUNNEL_LAYERS["L2"]


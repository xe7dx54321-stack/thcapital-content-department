# Morning Flash Source Bundle

- `generated_at`: `2026-05-09 05:52:00 CST`
- `date`: `2026-05-09`
- `selection_status`: `under_target`
- `business_window_start`: `2026-05-08 17:00:00 CST`
- `business_window_end`: `2026-05-09 05:00:00 CST`
- `selected_items`: `3`
- `min_items_required`: `8`
- `max_items_allowed`: `8`
- `excluded_items`: `23`

## Policy

- 只允许从 `captured_at` 落在 `T-1 17:00 -> T 05:00` 的 source packet 中选题。
- `published_at` 必须可解析，且同样落在晨间时间窗内；否则一律视为 stale / 不可审计，禁止写进早报正文。
- 只选 AI / Agent / 模型 / 机器人 / infra / 工作流相关对象；招聘、报名、榜单征集、活动预告等 meta 内容一律排除。
- 后续 approved-topic / draft-pack / wechat.md 只允许使用本 bundle 内对象，不得额外增写 bundle 外历史旧题。

## Selected Events

### 1. 比宇树机器人更早上春晚的公司，要敲钟 IPO 了
- `source_name`: `36氪 AI`
- `source_id`: `web__36kr_ai`
- `primary_source`: `partial`
- `published_at`: `2026-05-08 23:09:08 CST`
- `captured_at`: `2026-05-08 23:07:17 CST`
- `canonical_url`: `https://www.36kr.com/p/3800408468959745`
- `score`: `12`
- `selection_reason`: `fit, primary=partial, published=2026-05-08 23:09:08 CST, mainstream_or_primary_lane`
- `summary`: `36氪 AI 当前页提取到近期条目“比宇树机器人更早上春晚的公司，要敲钟 IPO 了”。它适合作为官方更新、专家观察或中文传播层的单条入口，后续应回链原文继续核验。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__36kr_ai_ipo__source-packet.md`

### 2. DeepSeek降价背后：Token生意在重新洗牌
- `source_name`: `36氪 AI`
- `source_id`: `web__36kr_ai`
- `primary_source`: `partial`
- `published_at`: `2026-05-08 23:09:08 CST`
- `captured_at`: `2026-05-08 23:07:17 CST`
- `canonical_url`: `https://www.36kr.com/p/3800580452080647`
- `score`: `12`
- `selection_reason`: `fit, primary=partial, published=2026-05-08 23:09:08 CST, mainstream_or_primary_lane`
- `summary`: `36氪 AI 当前页提取到近期条目“DeepSeek降价背后：Token生意在重新洗牌”。它适合作为官方更新、专家观察或中文传播层的单条入口，后续应回链原文继续核验。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__36kr_ai_deepseek_token__source-packet.md`

### 3. Agentic Search for Context Engineering — Leonie Monigatti, Elastic
- `source_name`: `AI Engineer YouTube`
- `source_id`: `youtube__aidotengineer`
- `primary_source`: `partial`
- `published_at`: `2026-05-08 21:05:06 CST`
- `captured_at`: `2026-05-08 22:04:32 CST`
- `canonical_url`: `https://www.youtube.com/watch?v=ynJyIKwjonM`
- `score`: `12`
- `selection_reason`: `fit, primary=partial, published=2026-05-08 21:05:06 CST`
- `summary`: `AI Engineer YouTube 频道页抓到新视频“Agentic Search for Context Engineering — Leonie Monigatti, Elastic”。Jina 频道快照现在可稳定保留标题、链接与相对发布时间，适合作为视频线索的硬成功入口。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_220432__youtube_ai_dot_engineer_agentic_search_for_context_engineering_leonie_monigatti_elastic__source-packet.md`

## Source Refs

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__36kr_ai_ipo__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__36kr_ai_deepseek_token__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_220432__youtube_ai_dot_engineer_agentic_search_for_context_engineering_leonie_monigatti_elastic__source-packet.md`

## Excluded Samples

- `published_at_outside_window | Hedge: AI-native specialty insurance company | published_at=2026-05-08 13:52:39 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_182254__yc_launches_hedge_hedge_ai_native_specialty_insurance_company__source-packet.md`
- `published_at_outside_window | Tarot Cards of My wife | published_at=2026-05-07 22:38:12 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_215154__reddit_chatgpt_tarot_cards_of_my_wife__source-packet.md`
- `published_at_outside_window | Can't find more optimized sleep schedule [OC] | published_at=2026-05-08 06:29:08 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_215154__reddit_claude_can_t_find_more_optimized_sleep_schedule_oc__source-packet.md`
- `published_at_outside_window | Taiwanese company Skymizer announces HTX301 - PCIE inference card with 384GB of Memory at ~240 Watts | published_at=2026-05-08 09:36:22 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_215154__reddit_localllama_taiwanese_company_skymizer_announces_htx301_pcie_inference_card_with_384__source-packet.md`
- `published_at_unparseable | AI“养马”来了 | published_at=2026-05-08 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_215314__baidu_realtime_ai__source-packet.md`
- `published_at_unparseable | DeepSeek回应“崩了”：服务已恢复 新 | published_at=2026-05-08 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_215314__baidu_realtime_deepseek__source-packet.md`
- `published_at_outside_window | 职场工作中，遇到不会的内容，频繁使用AI，这个事能不能告诉别人? | published_at=2026-04-16 19:55:53 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_215314__zhihu_hot_ai_ai__source-packet.md`
- `published_at_outside_window | SK海力士因AI热潮发数百万元人均奖金，三星员工因待遇落差拟罢工，如何评价？反映了怎样的行业现状？ | published_at=2026-05-07 21:04:39 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_215314__zhihu_hot_ai_sk_ai__source-packet.md`
- `published_at_outside_window | AI 籽岷竟然入狱？！一切原因竟是... | published_at=2026-05-08 14:00:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_220432__bilibili_popular_ai_ai__source-packet.md`
- `published_at_unparseable | Anthropic’s Claude Mythos Problem, Dark DNA Unveiled, Pitfalls for Assistive Models, Simulating Fluid Dynamics | published_at=unknown | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__deeplearningai_batch_anthropic_s_claude_mythos_problem_dark_dna_unveiled_pitfalls_for_assisti__source-packet.md`
- `published_at_unparseable | GLM 5.1 Thinks Strategically, Data Center Revolt Intensifies, When Helpful LLMs Turn Unhelpful, Humanoid Robots Get to… | published_at=unknown | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__deeplearningai_batch_glm_5_1_thinks_strategically_data_center_revolt_intensifies_when_helpful__source-packet.md`
- `published_at_unparseable | Meta Pivots From Open Weights, Big Pharma Bets On AI, Regulatory Patchwork, Simulating Human Cohorts | published_at=unknown | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__deeplearningai_batch_meta_pivots_from_open_weights_big_pharma_bets_on_ai_regulatory_patchwork__source-packet.md`
- `published_at_unparseable | awslabs/aidlc-workflows | published_at=2026-05-08 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__github_trending_awslabs_aidlc_workflows__source-packet.md`
- `published_at_unparseable | decolua/9router | published_at=2026-05-08 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__github_trending_decolua_9router__source-packet.md`
- `published_at_unparseable | HKUDS/AI-Trader | published_at=2026-05-08 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__github_trending_hkuds_ai_trader__source-packet.md`
- `published_at_outside_window | Rumors of my death are slightly exaggerated | published_at=2026-05-06 23:24:51 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__hn_frontpage_48037336_rumors_of_my_death_are_slightly_exaggerated__source-packet.md`
- `published_at_unparseable | Cloudflare Launches “Artifacts” Beta, Introducing Git Like Versioning for AI Agents | published_at=unknown | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__infoq_ai_ml_cloudflare_launches_artifacts_beta_introducing_git_like_versioning_for_a__source-packet.md`
- `published_at_unparseable | Google New TPU Generation is Specifically Designed for Agents and SOTA Model Training | published_at=unknown | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__infoq_ai_ml_google_new_tpu_generation_is_specifically_designed_for_agents_and_sota_m__source-packet.md`
- `published_at_unparseable | OpenAI Introduces Websocket Based Execution Mode to Reduce Latency in Agentic Workflows | published_at=unknown | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__infoq_ai_ml_openai_introduces_websocket_based_execution_mode_to_reduce_latency_in_ag__source-packet.md`
- `published_at_unparseable | 拿下1亿美元种子轮！SGLang团队创立RadixArk，打造下一代开放AI基础设施 | published_at=unknown | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__jiqizhixin_site_1_sglang_radixark_ai__source-packet.md`
- `... +3 more excluded items`

# Morning Flash Source Bundle

- `generated_at`: `2026-04-17 05:05:35 CST`
- `date`: `2026-04-17`
- `selection_status`: `ready`
- `business_window_start`: `2026-04-16 17:00:00 CST`
- `business_window_end`: `2026-04-17 05:00:00 CST`
- `selected_items`: `8`
- `min_items_required`: `8`
- `max_items_allowed`: `8`
- `excluded_items`: `28`

## Policy

- 只允许从 `captured_at` 落在 `T-1 17:00 -> T 05:00` 的 source packet 中选题。
- `published_at` 必须可解析，且同样落在晨间时间窗内；否则一律视为 stale / 不可审计，禁止写进早报正文。
- 只选 AI / Agent / 模型 / 机器人 / infra / 工作流相关对象；招聘、报名、榜单征集、活动预告等 meta 内容一律排除。
- 后续 approved-topic / draft-pack / wechat.md 只允许使用本 bundle 内对象，不得额外增写 bundle 外历史旧题。

## Selected Events

### 1. Claude Opus 4.7
- `source_name`: `Hacker News Frontpage`
- `source_id`: `trend__hn_frontpage`
- `primary_source`: `partial`
- `published_at`: `2026-04-16 22:29:09 CST`
- `captured_at`: `2026-04-16 22:50:05 CST`
- `canonical_url`: `https://www.anthropic.com/claude/opus`
- `score`: `12`
- `selection_reason`: `fit, primary=partial, published=2026-04-16 22:29:09 CST`
- `summary`: `Hacker News RSS 抓到高热新条目。它适合作为 builder / startup / AI infra 话题的扩散入口，不是最终事实源。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_225005__hn_frontpage_47793493_claude_opus_4_7__source-packet.md`

### 2. Qwen3.6-35B-A3B: Agentic Coding Power, Now Open to All
- `source_name`: `Hacker News Frontpage`
- `source_id`: `trend__hn_frontpage`
- `primary_source`: `partial`
- `published_at`: `2026-04-16 21:36:27 CST`
- `captured_at`: `2026-04-16 22:50:05 CST`
- `canonical_url`: `https://qwen.ai/blog?id=qwen3.6-35b-a3b`
- `score`: `12`
- `selection_reason`: `fit, primary=partial, published=2026-04-16 21:36:27 CST`
- `summary`: `Hacker News RSS 抓到高热新条目。它适合作为 builder / startup / AI infra 话题的扩散入口，不是最终事实源。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_225005__hn_frontpage_47792764_qwen3_6_35b_a3b_agentic_coding_power_now_open_to_all__source-packet.md`

### 3. This simulation startup wants to be the Cursor for physical AI
- `source_name`: `TechCrunch AI`
- `source_id`: `web__techcrunch_ai`
- `primary_source`: `no`
- `published_at`: `2026-04-16 20:30:00 CST`
- `captured_at`: `2026-04-16 21:12:26 CST`
- `canonical_url`: `https://techcrunch.com/2026/04/16/this-simulation-startup-wants-to-be-the-cursor-for-physical-ai/`
- `score`: `11`
- `selection_reason`: `fit, primary=no, published=2026-04-16 20:30:00 CST, mainstream_or_primary_lane`
- `summary`: `TechCrunch AI RSS 抓到新条目“This simulation startup wants to be the Cursor for physical AI”。这类媒体稿通常适合作为融资、新产品、新公司与产业变动的入口，后续需要继续回链公司官网、融资公告或创始人原话。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_211226__techcrunch_ai_this_simulation_startup_wants_to_be_the_cursor_for_physical_ai__source-packet.md`

### 4. 数据限制具身？觅蜂杀进场破局：高质量数据水电一样即取即用
- `source_name`: `机器之心`
- `source_id`: `wechat__jiqizhixin`
- `primary_source`: `partial`
- `published_at`: `2026-04-16 18:10:04 CST`
- `captured_at`: `2026-04-16 22:09:48 CST`
- `canonical_url`: `https://mp.weixin.qq.com/s/pi1e85BPzqQgrqZqs05_Vw`
- `score`: `11`
- `selection_reason`: `fit, primary=partial, published=2026-04-16 18:10:04 CST, mainstream_or_primary_lane`
- `summary`: `机器之心 微信 RSS 抓到新条目。它更适合作为中文热点、产品观察和玩法讨论的入口，不宜直接当最终事实结论。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_220948__wechat_jiqizhixin_https_mp_weixin_qq_com_s_pi1e85bpzqqgrqzqs05_vw__source-packet.md`

### 5. 当AI迈入Harness时代：以MiniMax为样本看智能体云端新基建
- `source_name`: `机器之心`
- `source_id`: `wechat__jiqizhixin`
- `primary_source`: `partial`
- `published_at`: `2026-04-16 18:10:04 CST`
- `captured_at`: `2026-04-16 22:09:48 CST`
- `canonical_url`: `https://mp.weixin.qq.com/s/8iMI1UJB9FM5soVWU_be3Q`
- `score`: `11`
- `selection_reason`: `fit, primary=partial, published=2026-04-16 18:10:04 CST, mainstream_or_primary_lane`
- `summary`: `机器之心 微信 RSS 抓到新条目。它更适合作为中文热点、产品观察和玩法讨论的入口，不宜直接当最终事实结论。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_220948__wechat_jiqizhixin_ai_harness_minimax__source-packet.md`

### 6. TPAMI 2026 | 北大彭宇新团队提出CPL++框架，实现视觉定位模型的「自知之明」和「自我纠错」
- `source_name`: `机器之心`
- `source_id`: `wechat__jiqizhixin`
- `primary_source`: `partial`
- `published_at`: `2026-04-16 18:10:04 CST`
- `captured_at`: `2026-04-16 22:09:48 CST`
- `canonical_url`: `https://mp.weixin.qq.com/s/NcBj7TM_QhxinJJJdsW2-w`
- `score`: `11`
- `selection_reason`: `fit, primary=partial, published=2026-04-16 18:10:04 CST, mainstream_or_primary_lane`
- `summary`: `机器之心 微信 RSS 抓到新条目。它更适合作为中文热点、产品观察和玩法讨论的入口，不宜直接当最终事实结论。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_220948__wechat_jiqizhixin_tpami_2026_cpl__source-packet.md`

### 7. Robots Are Finally Starting to Work
- `source_name`: `Y Combinator YouTube`
- `source_id`: `youtube__ycombinator`
- `primary_source`: `partial`
- `published_at`: `2026-04-16 21:59:53 CST`
- `captured_at`: `2026-04-16 22:08:53 CST`
- `canonical_url`: `https://www.youtube.com/watch?v=4EsUaur0nsQ`
- `score`: `10`
- `selection_reason`: `fit, primary=partial, published=2026-04-16 21:59:53 CST`
- `summary`: `Y Combinator YouTube 频道页直连抓到新视频“Robots Are Finally Starting to Work”。当前直接解析频道页内的 ytInitialData，避免 Jina 波动对视频 lane 造成整组失真。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_220853__youtube_ycombinator_robots_are_finally_starting_to_work__source-packet.md`

### 8. €54k spike in 13h from unrestricted Firebase browser key accessing Gemini APIs
- `source_name`: `Hacker News Frontpage`
- `source_id`: `trend__hn_frontpage`
- `primary_source`: `partial`
- `published_at`: `2026-04-16 20:13:30 CST`
- `captured_at`: `2026-04-16 22:50:05 CST`
- `canonical_url`: `https://discuss.ai.google.dev/t/unexpected-54k-billing-spike-in-13-hours-firebase-browser-key-without-api-restrictions-used-for-gemini-requests/140262`
- `score`: `10`
- `selection_reason`: `fit, primary=partial, published=2026-04-16 20:13:30 CST`
- `summary`: `Hacker News RSS 抓到高热新条目。它适合作为 builder / startup / AI infra 话题的扩散入口，不是最终事实源。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_225005__hn_frontpage_47791871_54k_spike_in_13h_from_unrestricted_firebase_browser_key_accessi__source-packet.md`

## Source Refs

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_225005__hn_frontpage_47793493_claude_opus_4_7__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_225005__hn_frontpage_47792764_qwen3_6_35b_a3b_agentic_coding_power_now_open_to_all__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_211226__techcrunch_ai_this_simulation_startup_wants_to_be_the_cursor_for_physical_ai__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_220948__wechat_jiqizhixin_https_mp_weixin_qq_com_s_pi1e85bpzqqgrqzqs05_vw__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_220948__wechat_jiqizhixin_ai_harness_minimax__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_220948__wechat_jiqizhixin_tpami_2026_cpl__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_220853__youtube_ycombinator_robots_are_finally_starting_to_work__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_225005__hn_frontpage_47791871_54k_spike_in_13h_from_unrestricted_firebase_browser_key_accessi__source-packet.md`

## Excluded Samples

- `published_at_outside_window | DeepL, known for text translation, now wants to translate your voice | published_at=2026-04-16 16:00:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_180538__techcrunch_ai_deepl_known_for_text_translation_now_wants_to_translate_your_voice__source-packet.md`
- `promo_or_meta | 年度AI产品榜单申报 | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_181158__wechat_qbitai_ai__source-packet.md`
- `published_at_outside_window | 把屁声发给ChatGPT，它说这是艺术 | published_at=2026-04-16 12:35:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_181158__wechat_qbitai_chatgpt__source-packet.md`
- `published_at_outside_window | MSRA首测AI从零建仓库：能写、能跑，但不一定对丨ACL'26 | published_at=2026-04-16 12:35:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_181158__wechat_qbitai_msra_ai_acl_26__source-packet.md`
- `published_at_outside_window | 扔掉你的Token账单吧，荣耀YOYO Claw技术把养虾成本打下来了 | published_at=2026-04-16 12:35:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_181158__wechat_qbitai_token_yoyo_claw__source-packet.md`
- `published_at_outside_window | 超30亿！中国迄今最大具身智能融资诞生 | published_at=2026-04-16 10:59:59 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_181158__wechat_zhidx_30__source-packet.md`
- `published_at_outside_window | Claude is about to begin its KYC verification process. | published_at=2026-04-16 10:53:40 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_214929__reddit_claude_claude_is_about_to_begin_its_kyc_verification_process__source-packet.md`
- `published_at_outside_window | The cost of code use to be a middleware for our brains. | published_at=2026-04-16 05:18:53 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_214929__reddit_claude_the_cost_of_code_use_to_be_a_middleware_for_our_brains__source-packet.md`
- `published_at_outside_window | Gemma4 26b & E4B are crazy good, and replaced Qwen for me! | published_at=2026-04-16 03:56:10 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_214929__reddit_localllama_gemma4_26b_e4b_are_crazy_good_and_replaced_qwen_for_me__source-packet.md`
- `published_at_outside_window | How to properly deal with a CLAUDE.md file. | published_at=2026-04-16 03:34:54 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_214929__reddit_localllama_how_to_properly_deal_with_a_claude_md_file__source-packet.md`
- `published_at_outside_window | Video of how my LLM's decoder blocks changed while training | published_at=2026-04-16 04:55:33 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_214929__reddit_localllama_video_of_how_my_llm_s_decoder_blocks_changed_while_training__source-packet.md`
- `published_at_outside_window | Accelerating the cyber defense ecosystem that protects us all | published_at=2026-04-16 08:00:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_215028__openai_news_accelerating_the_cyber_defense_ecosystem_that_protects_us_all__source-packet.md`
- `published_at_outside_window | 35岁失业后写了部"中年社畜修仙"的网文，十万字序章完结零订阅，这种眼高手低的坚持还有意义吗？ | published_at=2026-04-13 18:04:59 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_215153__zhihu_hot_ai_35__source-packet.md`
- `published_at_outside_window | 何小鹏重申「跳过 L3 」，称「最安全的路径是从 L2 直接到 L4 」，如何看待他的观点？ | published_at=2026-04-15 22:19:59 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_215153__zhihu_hot_ai_l3_l2_l4__source-packet.md`
- `published_at_outside_window | 理想净利降八成，有部门全员无年终奖，理想当前面临怎样的经营困境？其背后的核心问题有哪些？ | published_at=2026-04-16 09:24:27 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_215153__zhihu_hot_ai_zhihu_hot__source-packet.md`
- `published_at_outside_window | 脸谱心智陆弘远团队ACL 2026新作：别再给模型叠加「高级词」了！模型更爱听「大白话」 | published_at=2026-04-16 16:04:08 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_220948__wechat_jiqizhixin_acl_2026__source-packet.md`
- `published_at_unparseable | google/magika | published_at=2026-04-16 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_225005__github_trending_google_magika__source-packet.md`
- `published_at_unparseable | lsdefine/GenericAgent | published_at=2026-04-16 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_225005__github_trending_lsdefine_genericagent__source-packet.md`
- `published_at_outside_window | Training and Finetuning Multimodal Embedding & Reranker Models with Sentence Transformers | published_at=2026-04-16 08:00:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_225005__huggingface_blog_training_and_finetuning_multimodal_embedding_reranker_models_with_senten__source-packet.md`
- `published_at_outside_window | A Study of Failure Modes in Two-Stage Human-Object Interaction Detection | published_at=2026-04-15 12:01:23 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_225005__huggingface_daily_papers_a_study_of_failure_modes_in_two_stage_human_object_interaction_detection__source-packet.md`
- `... +8 more excluded items`

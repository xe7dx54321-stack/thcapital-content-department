# Morning Flash Source Bundle

- `generated_at`: `2026-04-28 05:05:24 CST`
- `date`: `2026-04-28`
- `selection_status`: `ready`
- `business_window_start`: `2026-04-27 17:00:00 CST`
- `business_window_end`: `2026-04-28 05:00:00 CST`
- `selected_items`: `8`
- `min_items_required`: `8`
- `max_items_allowed`: `8`
- `excluded_items`: `23`

## Policy

- 只允许从 `captured_at` 落在 `T-1 17:00 -> T 05:00` 的 source packet 中选题。
- `published_at` 必须可解析，且同样落在晨间时间窗内；否则一律视为 stale / 不可审计，禁止写进早报正文。
- 只选 AI / Agent / 模型 / 机器人 / infra / 工作流相关对象；招聘、报名、榜单征集、活动预告等 meta 内容一律排除。
- 后续 approved-topic / draft-pack / wechat.md 只允许使用本 bundle 内对象，不得额外增写 bundle 外历史旧题。

## Selected Events

### 1. Join the new AI Agents Vibe Coding Course from Google and Kaggle
- `source_name`: `Google AI Blog`
- `source_id`: `web__google_blog_ai`
- `primary_source`: `yes`
- `published_at`: `2026-04-27 21:00:00 CST`
- `captured_at`: `2026-04-27 21:55:38 CST`
- `canonical_url`: `https://blog.google/innovation-and-ai/technology/developers-tools/kaggle-genai-intensive-course-vibe-coding-june-2026/`
- `score`: `13`
- `selection_reason`: `fit, primary=yes, published=2026-04-27 21:00:00 CST`
- `summary`: `Google AI Blog RSS 抓到新条目。它属于官方一手源，适合判断 Google AI 平台层和产品层的真实变化。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_215538__google_blog_ai_join_the_new_ai_agents_vibe_coding_course_from_google_and_kaggle__source-packet.md`

### 2. Ritu vs Case Files | With ChatGPT
- `source_name`: `OpenAI YouTube`
- `source_id`: `youtube__openai`
- `primary_source`: `yes`
- `published_at`: `2026-04-27 19:45:12 CST`
- `captured_at`: `2026-04-27 22:45:02 CST`
- `canonical_url`: `https://www.youtube.com/watch?v=2TGHO4apQ5I`
- `score`: `13`
- `selection_reason`: `fit, primary=yes, published=2026-04-27 19:45:12 CST`
- `summary`: `OpenAI YouTube 频道页抓到新视频“Ritu vs Case Files | With ChatGPT”。Jina 频道快照现在可稳定保留标题、链接与相对发布时间，适合作为视频线索的硬成功入口。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_224502__youtube_openai_ritu_vs_case_files_with_chatgpt__source-packet.md`

### 3. Agent群体智能来了！魔搭开源Agent自进化群体智能框架：群体记忆自动蒸馏与进化，8万+群体技能即取即用，智能体画像一键复用
- `source_name`: `量子位`
- `source_id`: `wechat__liangziwei`
- `primary_source`: `partial`
- `published_at`: `2026-04-27 18:36:54 CST`
- `captured_at`: `2026-04-27 22:45:54 CST`
- `canonical_url`: `https://mp.weixin.qq.com/s/cCzTNq0LpWgv-fM_EKFMQQ`
- `score`: `13`
- `selection_reason`: `fit, primary=partial, published=2026-04-27 18:36:54 CST, mainstream_or_primary_lane`
- `summary`: `量子位 微信 RSS 抓到新条目。它更适合作为中文热点、产品观察和玩法讨论的入口，不宜直接当最终事实结论。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_224554__wechat_qbitai_agent_agent_8__source-packet.md`

### 4. Microsoft to Stop Sharing Revenue with Main AI Partner OpenAI
- `source_name`: `Hacker News Frontpage`
- `source_id`: `trend__hn_frontpage`
- `primary_source`: `partial`
- `published_at`: `2026-04-27 21:22:42 CST`
- `captured_at`: `2026-04-27 23:18:34 CST`
- `canonical_url`: `https://www.bloomberg.com/news/articles/2026-04-27/microsoft-to-stop-sharing-revenue-with-main-ai-partner-openai`
- `score`: `12`
- `selection_reason`: `fit, primary=partial, published=2026-04-27 21:22:42 CST`
- `summary`: `Hacker News RSS 抓到高热新条目。它适合作为 builder / startup / AI infra 话题的扩散入口，不是最终事实源。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_231834__hn_frontpage_47921248_microsoft_to_stop_sharing_revenue_with_main_ai_partner_openai__source-packet.md`

### 5. Show HN: OSS Agent I built topped the TerminalBench on Gemini-3-flash-preview
- `source_name`: `Hacker News Frontpage`
- `source_id`: `trend__hn_frontpage`
- `primary_source`: `partial`
- `published_at`: `2026-04-27 20:35:55 CST`
- `captured_at`: `2026-04-27 23:18:34 CST`
- `canonical_url`: `https://github.com/dirac-run/dirac`
- `score`: `12`
- `selection_reason`: `fit, primary=partial, published=2026-04-27 20:35:55 CST`
- `summary`: `Hacker News RSS 抓到高热新条目。它适合作为 builder / startup / AI infra 话题的扩散入口，不是最终事实源。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_231834__hn_frontpage_47920787_show_hn_oss_agent_i_built_topped_the_terminalbench_on_gemini_3___source-packet.md`

### 6. OpenAI could be making a phone with AI agents replacing apps
- `source_name`: `TechCrunch AI`
- `source_id`: `web__techcrunch_ai`
- `primary_source`: `no`
- `published_at`: `2026-04-27 21:08:59 CST`
- `captured_at`: `2026-04-27 21:10:01 CST`
- `canonical_url`: `https://techcrunch.com/2026/04/27/openai-could-be-making-a-phone-with-ai-agents-replacing-apps/`
- `score`: `11`
- `selection_reason`: `fit, primary=no, published=2026-04-27 21:08:59 CST, mainstream_or_primary_lane`
- `summary`: `TechCrunch AI RSS 抓到新条目“OpenAI could be making a phone with AI agents replacing apps”。这类媒体稿通常适合作为融资、新产品、新公司与产业变动的入口，后续需要继续回链公司官网、融资公告或创始人原话。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_211001__techcrunch_ai_openai_could_be_making_a_phone_with_ai_agents_replacing_apps__source-packet.md`

### 7. 突发！Meta收购Manus被叫停
- `source_name`: `智东西`
- `source_id`: `wechat__zhidx`
- `primary_source`: `partial`
- `published_at`: `2026-04-27 19:16:53 CST`
- `captured_at`: `2026-04-27 22:45:54 CST`
- `canonical_url`: `https://mp.weixin.qq.com/s/tV_iLaFuU8OBCJ-8Hgkx3g`
- `score`: `11`
- `selection_reason`: `fit, primary=partial, published=2026-04-27 19:16:53 CST, mainstream_or_primary_lane`
- `summary`: `智东西 微信 RSS 抓到新条目。它更适合作为中文热点、产品观察和玩法讨论的入口，不宜直接当最终事实结论。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_224554__wechat_zhidx_meta_manus__source-packet.md`

### 8. 世界模型双冠王诞生！国产世界模型力压谷歌、英伟达等持续领跑
- `source_name`: `机器之心`
- `source_id`: `wechat__jiqizhixin`
- `primary_source`: `partial`
- `published_at`: `2026-04-27 19:00:00 CST`
- `captured_at`: `2026-04-27 22:45:54 CST`
- `canonical_url`: `https://mp.weixin.qq.com/s/ifjq1FsK5BpYo2MRf-JoEA`
- `score`: `11`
- `selection_reason`: `fit, primary=partial, published=2026-04-27 19:00:00 CST, mainstream_or_primary_lane`
- `summary`: `机器之心 微信 RSS 抓到新条目。它更适合作为中文热点、产品观察和玩法讨论的入口，不宜直接当最终事实结论。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_224554__wechat_jiqizhixin_https_mp_weixin_qq_com_s_ifjq1fsk5bpyo2mrf_joea__source-packet.md`

## Source Refs

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_215538__google_blog_ai_join_the_new_ai_agents_vibe_coding_course_from_google_and_kaggle__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_224502__youtube_openai_ritu_vs_case_files_with_chatgpt__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_224554__wechat_qbitai_agent_agent_8__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_231834__hn_frontpage_47921248_microsoft_to_stop_sharing_revenue_with_main_ai_partner_openai__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_231834__hn_frontpage_47920787_show_hn_oss_agent_i_built_topped_the_terminalbench_on_gemini_3___source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_211001__techcrunch_ai_openai_could_be_making_a_phone_with_ai_agents_replacing_apps__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_224554__wechat_zhidx_meta_manus__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_224554__wechat_jiqizhixin_https_mp_weixin_qq_com_s_ifjq1fsk5bpyo2mrf_joea__source-packet.md`

## Excluded Samples

- `published_at_outside_window | 当剪辑工具开始「听懂人话」：剪映做了视频创作的 Skill 化 Agent | published_at=2026-04-27 14:25:50 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_190454__wechat_geekpark_skill_agent__source-packet.md`
- `published_at_outside_window | 李飞飞引爆的3D新技术，为什么这家深圳公司两年前就“玩腻”了？ | published_at=2026-04-27 14:30:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_190454__wechat_qbitai_3d__source-packet.md`
- `published_at_outside_window | Claude第一款AI桌宠硬件，深圳制造 | published_at=2026-04-27 14:30:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_190454__wechat_qbitai_claude_ai__source-packet.md`
- `published_at_outside_window | 超越Claude Mythos和GPT-5.5！斯坦福Agent验证框架拿下SOTA，Transformer作者转发 | published_at=2026-04-27 11:46:24 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_190454__wechat_qbitai_claude_mythos_gpt_5_5_agent_sota_transformer__source-packet.md`
- `promo_or_meta | 量子位编辑作者招聘 | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_190454__wechat_qbitai_https_mp_weixin_qq_com_s_d6rzkbjifpstiyclhtgziq__source-packet.md`
- `published_at_outside_window | The fall of chegg........ | published_at=2026-04-27 13:29:39 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_215422__reddit_chatgpt_the_fall_of_chegg__source-packet.md`
- `published_at_outside_window | AMD Hipfire - a new inference engine optimized for AMD GPU's | published_at=2026-04-27 09:36:53 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_215422__reddit_localllama_amd_hipfire_a_new_inference_engine_optimized_for_amd_gpu_s__source-packet.md`
- `published_at_outside_window | Switched from Qwen3.6 35b-a3b to Qwen3.6 27b mid coding and it's noticeably better! | published_at=2026-04-27 04:20:24 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_215422__reddit_localllama_switched_from_qwen3_6_35b_a3b_to_qwen3_6_27b_mid_coding_and_it_s_noticea__source-packet.md`
- `published_at_outside_window | The next phase of the Microsoft OpenAI partnership | published_at=2026-04-27 14:00:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_215538__openai_news_the_next_phase_of_the_microsoft_openai_partnership__source-packet.md`
- `published_at_unparseable | 国家发改委：禁止外资收购Manus项目 | published_at=2026-04-27 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_215658__baidu_realtime_manus__source-packet.md`
- `published_at_outside_window | 我没有编程能力，现在写了完整的游戏设计文稿，并准备了20万资金，想把游戏用AI做出来，该怎么做？ | published_at=2026-04-22 14:48:49 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_215658__zhihu_hot_ai_20_ai__source-packet.md`
- `published_at_outside_window | 三年时间市值翻了25倍，广告新巨头AppLovin任命了一名华人CTO | published_at=2026-04-27 16:40:35 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_224554__wechat_founder_park_25_applovin_cto__source-packet.md`
- `published_at_outside_window | Anthropic又「惹祸」？大写「HERMES.md」触发计费Bug，偷偷扣光用户200美元 | published_at=2026-04-27 16:11:09 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_224554__wechat_jiqizhixin_anthropic_hermes_md_bug_200__source-packet.md`
- `published_at_outside_window | CVPR 2026 | 谷歌DeepMind重磅开源多模态TIPSv2：实现Patch-Text对齐的最优表现 | published_at=2026-04-27 16:11:09 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_224554__wechat_jiqizhixin_cvpr_2026_deepmind_tipsv2_patch_text__source-packet.md`
- `published_at_unparseable | penpot/penpot | published_at=2026-04-27 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_231834__github_trending_penpot_penpot__source-packet.md`
- `published_at_outside_window | The Prompt API | published_at=2026-04-27 10:18:58 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_231834__hn_frontpage_47917026_the_prompt_api__source-packet.md`
- `published_at_outside_window | How to build scalable web apps with OpenAI's Privacy Filter | published_at=2026-04-27 08:00:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_231834__huggingface_blog_how_to_build_scalable_web_apps_with_openai_s_privacy_filter__source-packet.md`
- `published_at_outside_window | Attention-based multiple instance learning for predominant growth pattern prediction in lung adenocarcinoma wsi using foundation models | published_at=2026-04-23 18:53:11 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_231834__huggingface_daily_papers_attention_based_multiple_instance_learning_for_predominant_growth_patter__source-packet.md`
- `published_at_outside_window | DDF2Pol: A Dual-Domain Feature Fusion Network for PolSAR Image Classification | published_at=2026-04-21 05:22:22 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_231834__huggingface_daily_papers_ddf2pol_a_dual_domain_feature_fusion_network_for_polsar_image_classifica__source-packet.md`
- `published_at_outside_window | On Reasoning Behind Next Occupation Recommendation | published_at=2026-04-23 09:52:14 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_231834__huggingface_daily_papers_on_reasoning_behind_next_occupation_recommendation__source-packet.md`
- `... +3 more excluded items`

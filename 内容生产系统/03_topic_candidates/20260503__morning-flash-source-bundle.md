# Morning Flash Source Bundle

- `generated_at`: `2026-05-03 06:18:41 CST`
- `date`: `2026-05-03`
- `selection_status`: `under_target`
- `business_window_start`: `2026-05-02 17:00:00 CST`
- `business_window_end`: `2026-05-03 05:00:00 CST`
- `selected_items`: `2`
- `min_items_required`: `8`
- `max_items_allowed`: `8`
- `excluded_items`: `20`

## Policy

- 只允许从 `captured_at` 落在 `T-1 17:00 -> T 05:00` 的 source packet 中选题。
- `published_at` 必须可解析，且同样落在晨间时间窗内；否则一律视为 stale / 不可审计，禁止写进早报正文。
- 只选 AI / Agent / 模型 / 机器人 / infra / 工作流相关对象；招聘、报名、榜单征集、活动预告等 meta 内容一律排除。
- 后续 approved-topic / draft-pack / wechat.md 只允许使用本 bundle 内对象，不得额外增写 bundle 外历史旧题。

## Selected Events

### 1. Open Design: Use Your Coding Agent as a Design Engine
- `source_name`: `Hacker News Frontpage`
- `source_id`: `trend__hn_frontpage`
- `primary_source`: `partial`
- `published_at`: `2026-05-02 20:16:16 CST`
- `captured_at`: `2026-05-02 23:15:10 CST`
- `canonical_url`: `https://github.com/nexu-io/open-design`
- `score`: `12`
- `selection_reason`: `fit, primary=partial, published=2026-05-02 20:16:16 CST`
- `summary`: `Hacker News RSS 抓到高热新条目。它适合作为 builder / startup / AI infra 话题的扩散入口，不是最终事实源。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_231510__hn_frontpage_47985750_open_design_use_your_coding_agent_as_a_design_engine__source-packet.md`

### 2. Show HN: Mljar Studio – local AI data analyst that saves analysis as notebooks
- `source_name`: `Hacker News Frontpage`
- `source_id`: `trend__hn_frontpage`
- `primary_source`: `partial`
- `published_at`: `2026-05-02 18:21:31 CST`
- `captured_at`: `2026-05-02 23:15:10 CST`
- `canonical_url`: `https://mljar.com/`
- `score`: `10`
- `selection_reason`: `fit, primary=partial, published=2026-05-02 18:21:31 CST`
- `summary`: `Hacker News RSS 抓到高热新条目。它适合作为 builder / startup / AI infra 话题的扩散入口，不是最终事实源。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_231510__hn_frontpage_47985077_show_hn_mljar_studio_local_ai_data_analyst_that_saves_analysis___source-packet.md`

## Source Refs

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_231510__hn_frontpage_47985750_open_design_use_your_coding_agent_as_a_design_engine__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_231510__hn_frontpage_47985077_show_hn_mljar_studio_local_ai_data_analyst_that_saves_analysis___source-packet.md`

## Excluded Samples

- `published_at_outside_window | AI幻觉：从胡说八道到假装听话的进化史 | published_at=2026-05-02 08:00:42 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_185104__bilibili_popular_ai_ai__source-packet.md`
- `published_at_outside_window | 腾讯混元最新开源：440M翻译模型手机离线就能用，翻译质量超谷歌 | published_at=2026-05-02 10:41:38 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_185225__wechat_qbitai_440m__source-packet.md`
- `published_at_outside_window | 苹果官方App误打包了Claude.md，这么大的公司也Vibe Coding啊？ | published_at=2026-05-02 10:41:38 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_185225__wechat_qbitai_app_claude_md_vibe_coding__source-packet.md`
- `promo_or_meta | 量子位编辑作者招聘 | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_185225__wechat_qbitai_https_mp_weixin_qq_com_s_tno9pjwpgnypt5k5ibshig__source-packet.md`
- `published_at_outside_window | Meta收购华农校友机器人AI公司，团队并入超级智能实验室 | published_at=2026-05-02 12:00:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_185225__wechat_qbitai_meta_ai__source-packet.md`
- `published_at_outside_window | Create random surreal old photos from nothing! | published_at=2026-05-02 08:16:59 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_215523__reddit_chatgpt_create_random_surreal_old_photos_from_nothing__source-packet.md`
- `published_at_outside_window | I didn’t attach an image | published_at=2026-05-02 04:36:40 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_215523__reddit_chatgpt_i_didn_t_attach_an_image__source-packet.md`
- `published_at_outside_window | I dont even have a funny title for this one, I'm just confused | published_at=2026-05-02 08:12:45 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_215523__reddit_claude_i_dont_even_have_a_funny_title_for_this_one_i_m_just_confused__source-packet.md`
- `published_at_outside_window | A Dark-Money Campaign Is Paying Influencers to Frame Chinese AI as a Threat | published_at=2026-05-02 14:35:02 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_215523__reddit_localllama_a_dark_money_campaign_is_paying_influencers_to_frame_chinese_ai_as_a_thr__source-packet.md`
- `published_at_outside_window | Been using Qwen-3.6-27B-q8_k_xl + VSCode + RTX 6000 Pro As Daily Driver | published_at=2026-05-02 07:31:32 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_215523__reddit_localllama_been_using_qwen_3_6_27b_q8_k_xl_vscode_rtx_6000_pro_as_daily_driver__source-packet.md`
- `published_at_outside_window | Qwen3.6-27B at 72 tok/s on RTX 3090 on Windows using native vLLM (no WSL, no Docker), portable launcher and installer | published_at=2026-05-02 16:12:35 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_215523__reddit_localllama_qwen3_6_27b_at_72_tok_s_on_rtx_3090_on_windows_using_native_vllm_no_wsl___source-packet.md`
- `published_at_outside_window | 美国防部与 SpaceX、谷歌等 7 家 AI 公司达成协议，称将转型主导作战力量，这会带来哪些影响？ | published_at=2026-05-01 20:09:33 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_215654__zhihu_hot_ai_spacex_7_ai__source-packet.md`
- `published_at_outside_window | 🐧 凑企鹅大战三角洲！！！🐧 | published_at=2026-04-30 17:00:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_223934__bilibili_popular_ai_BV1Vd9sB8EaX__source-packet.md`
- `published_at_outside_window | ACL 2026 | RouteMoA：无需预推理的动态路由，实现高效多智能体混合 | published_at=2026-05-02 13:31:12 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_224046__wechat_jiqizhixin_acl_2026_routemoa__source-packet.md`
- `published_at_outside_window | 这套题，GPT-5.5、Opus 4.7加起来没考到「1分」，人类却拿了满分100？ | published_at=2026-05-02 13:31:12 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_224046__wechat_jiqizhixin_gpt_5_5_opus_4_7_1_100__source-packet.md`
- `published_at_unparseable | ruvnet/ruflo | published_at=2026-05-02 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_231510__github_trending_ruvnet_ruflo__source-packet.md`
- `published_at_outside_window | Show HN: DAC – open-source dashboard as code tool for agents and humans | published_at=2026-04-29 22:37:20 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_231510__hn_frontpage_47949066_show_hn_dac_open_source_dashboard_as_code_tool_for_agents_and_h__source-packet.md`
- `published_at_outside_window | DeepSeek V4–almost on the frontier, a fraction of the price | published_at=2026-05-02 00:52:43 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_231510__hn_frontpage_47977026_deepseek_v4_almost_on_the_frontier_a_fraction_of_the_price__source-packet.md`
- `published_at_outside_window | Show HN: Filling PDF forms with AI using client-side tool calling | published_at=2026-05-02 16:54:27 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_231510__hn_frontpage_47984675_show_hn_filling_pdf_forms_with_ai_using_client_side_tool_callin__source-packet.md`
- `published_at_unparseable | Meta Deploys Unified AI Agents to Automate Performance Optimization at Hyperscale | published_at=unknown | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260502_231510__infoq_ai_ml_meta_deploys_unified_ai_agents_to_automate_performance_optimization_at_h__source-packet.md`

# Morning Flash Source Bundle

- `generated_at`: `2026-04-20 05:35:06 CST`
- `date`: `2026-04-20`
- `selection_status`: `under_target`
- `business_window_start`: `2026-04-19 17:00:00 CST`
- `business_window_end`: `2026-04-20 05:00:00 CST`
- `selected_items`: `2`
- `min_items_required`: `8`
- `max_items_allowed`: `8`
- `excluded_items`: `31`

## Policy

- 只允许从 `captured_at` 落在 `T-1 17:00 -> T 05:00` 的 source packet 中选题。
- `published_at` 必须可解析，且同样落在晨间时间窗内；否则一律视为 stale / 不可审计，禁止写进早报正文。
- 只选 AI / Agent / 模型 / 机器人 / infra / 工作流相关对象；招聘、报名、榜单征集、活动预告等 meta 内容一律排除。
- 后续 approved-topic / draft-pack / wechat.md 只允许使用本 bundle 内对象，不得额外增写 bundle 外历史旧题。

## Selected Events

### 1. Changes in the system prompt between Claude Opus 4.6 and 4.7
- `source_name`: `Hacker News Frontpage`
- `source_id`: `trend__hn_frontpage`
- `primary_source`: `partial`
- `published_at`: `2026-04-19 18:36:29 CST`
- `captured_at`: `2026-04-19 23:04:07 CST`
- `canonical_url`: `https://simonwillison.net/2026/Apr/18/opus-system-prompt/`
- `score`: `12`
- `selection_reason`: `fit, primary=partial, published=2026-04-19 18:36:29 CST`
- `summary`: `Hacker News RSS 抓到高热新条目。它适合作为 builder / startup / AI infra 话题的扩散入口，不是最终事实源。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_230407__hn_frontpage_47823270_changes_in_the_system_prompt_between_claude_opus_4_6_and_4_7__source-packet.md`

### 2. Ask HN: How did you land your first projects as a solo engineer/consultant?
- `source_name`: `Hacker News Frontpage`
- `source_id`: `trend__hn_frontpage`
- `primary_source`: `partial`
- `published_at`: `2026-04-19 17:17:12 CST`
- `captured_at`: `2026-04-19 23:04:07 CST`
- `canonical_url`: `https://news.ycombinator.com/item?id=47822940`
- `score`: `10`
- `selection_reason`: `fit, primary=partial, published=2026-04-19 17:17:12 CST`
- `summary`: `Hacker News RSS 抓到高热新条目。它适合作为 builder / startup / AI infra 话题的扩散入口，不是最终事实源。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_230407__hn_frontpage_47822940_ask_hn_how_did_you_land_your_first_projects_as_a_solo_engineer___source-packet.md`

## Source Refs

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_230407__hn_frontpage_47823270_changes_in_the_system_prompt_between_claude_opus_4_6_and_4_7__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_230407__hn_frontpage_47822940_ask_hn_how_did_you_land_your_first_projects_as_a_solo_engineer___source-packet.md`

## Excluded Samples

- `published_at_outside_window | Is it just me or is ChatGPT being a dick lately? | published_at=2026-04-19 10:13:44 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_214246__reddit_chatgpt_is_it_just_me_or_is_chatgpt_being_a_dick_lately__source-packet.md`
- `published_at_outside_window | T.R.E.N F.R.I.E.N.D.S | published_at=2026-04-19 13:46:20 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_214246__reddit_chatgpt_t_r_e_n_f_r_i_e_n_d_s__source-packet.md`
- `published_at_outside_window | that time Anthropic played 2.5 million ChatGPT users | published_at=2026-04-19 06:06:59 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_214246__reddit_chatgpt_that_time_anthropic_played_2_5_million_chatgpt_users__source-packet.md`
- `published_at_outside_window | Claude Design keeps drawing a turd | published_at=2026-04-19 03:10:19 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_214246__reddit_claude_claude_design_keeps_drawing_a_turd__source-packet.md`
- `published_at_outside_window | I left my 7 year old nephew unsupervised on the pc and he used my claude session | published_at=2026-04-19 07:54:51 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_214246__reddit_claude_i_left_my_7_year_old_nephew_unsupervised_on_the_pc_and_he_used_my_claude__source-packet.md`
- `published_at_outside_window | Look how they massacred my boy | published_at=2026-04-19 00:05:32 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_214246__reddit_claude_look_how_they_massacred_my_boy__source-packet.md`
- `published_at_outside_window | “Sir, another 22 year old has found a job” | published_at=2026-04-19 03:28:02 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_214246__reddit_claude_sir_another_22_year_old_has_found_a_job__source-packet.md`
- `published_at_outside_window | I'm running qwen3.6-35b-a3b with 8 bit quant and 64k context thru OpenCode on my mbp m5 max 128gb and it's as good as claude | published_at=2026-04-19 08:17:59 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_214246__reddit_localllama_i_m_running_qwen3_6_35b_a3b_with_8_bit_quant_and_64k_context_thru_openco__source-packet.md`
- `published_at_outside_window | I made a tiny world model game that runs locally on iPad | published_at=2026-04-19 04:50:10 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_214246__reddit_localllama_i_made_a_tiny_world_model_game_that_runs_locally_on_ipad__source-packet.md`
- `published_at_outside_window | KIMI K2.6 SOON !! | published_at=2026-04-18 23:41:57 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_214246__reddit_localllama_kimi_k2_6_soon__source-packet.md`
- `published_at_outside_window | Why isn't ebay doing anything to stop those scams? | published_at=2026-04-19 15:09:34 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_214246__reddit_localllama_why_isn_t_ebay_doing_anything_to_stop_those_scams__source-packet.md`
- `published_at_unparseable | 机器人刚跑出300米被抬上救护车 | published_at=2026-04-19 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_221211__baidu_realtime_300__source-packet.md`
- `published_at_unparseable | 穿衣服的机器人参加半马被观众辣评 | published_at=2026-04-19 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_221211__baidu_realtime_baidu_hot__source-packet.md`
- `published_at_outside_window | DeepSeek开启首次对外融资，其在多名核心研究员跳槽之下为何会选择此时，从商业资本角度你怎么看？ | published_at=2026-04-19 10:09:39 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_221211__zhihu_hot_ai_deepseek__source-packet.md`
- `published_at_outside_window | 单片机技术是一门即将被淘汰的技术吗？ | published_at=2015-09-08 11:39:46 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_221211__zhihu_hot_ai_zhihu_hot__source-packet.md`
- `published_at_unparseable | Fincept-Corporation/FinceptTerminal | published_at=2026-04-19 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_231209__github_trending_fincept_corporation_finceptterminal__source-packet.md`
- `published_at_unparseable | ruvnet/RuView | published_at=2026-04-19 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_231209__github_trending_ruvnet_ruview__source-packet.md`
- `published_at_outside_window | FoodSense: A Multisensory Food Dataset and Benchmark for Predicting Taste, Smell, Texture, and Sound from Images | published_at=2026-04-16 04:02:20 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_231209__huggingface_daily_papers_foodsense_a_multisensory_food_dataset_and_benchmark_for_predicting_taste__source-packet.md`
- `published_at_outside_window | From Topology to Trajectory: LLM-Driven World Models For Supply Chain Resilience | published_at=2026-04-13 14:14:15 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_231209__huggingface_daily_papers_from_topology_to_trajectory_llm_driven_world_models_for_supply_chain_res__source-packet.md`
- `published_at_outside_window | Neuro-Oracle: A Trajectory-Aware Agentic RAG Framework for Interpretable Epilepsy Surgical Prognosis | published_at=2026-04-11 05:47:25 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260419_231209__huggingface_daily_papers_neuro_oracle_a_trajectory_aware_agentic_rag_framework_for_interpretable___source-packet.md`
- `... +11 more excluded items`

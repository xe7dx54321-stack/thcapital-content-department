# Morning Flash Source Bundle

- `generated_at`: `2026-05-07 05:50:52 CST`
- `date`: `2026-05-07`
- `selection_status`: `under_target`
- `business_window_start`: `2026-05-06 17:00:00 CST`
- `business_window_end`: `2026-05-07 05:00:00 CST`
- `selected_items`: `4`
- `min_items_required`: `8`
- `max_items_allowed`: `8`
- `excluded_items`: `25`

## Policy

- 只允许从 `captured_at` 落在 `T-1 17:00 -> T 05:00` 的 source packet 中选题。
- `published_at` 必须可解析，且同样落在晨间时间窗内；否则一律视为 stale / 不可审计，禁止写进早报正文。
- 只选 AI / Agent / 模型 / 机器人 / infra / 工作流相关对象；招聘、报名、榜单征集、活动预告等 meta 内容一律排除。
- 后续 approved-topic / draft-pack / wechat.md 只允许使用本 bundle 内对象，不得额外增写 bundle 外历史旧题。

## Selected Events

### 1. MCP UI: Extending the frontier — Liad Yosef and Ido Salomon, MCP Apps
- `source_name`: `AI Engineer YouTube`
- `source_id`: `youtube__aidotengineer`
- `primary_source`: `partial`
- `published_at`: `2026-05-06 21:44:47 CST`
- `captured_at`: `2026-05-06 22:44:47 CST`
- `canonical_url`: `https://www.youtube.com/watch?v=o-zkvb0iFDQ`
- `score`: `12`
- `selection_reason`: `fit, primary=partial, published=2026-05-06 21:44:47 CST`
- `summary`: `AI Engineer YouTube 频道页直连抓到新视频“MCP UI: Extending the frontier — Liad Yosef and Ido Salomon, MCP Apps”。当前直接解析频道页内的 ytInitialData，避免 Jina 波动对视频 lane 造成整组失真。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224447__youtube_ai_dot_engineer_mcp_ui_extending_the_frontier_liad_yosef_and_ido_salomon_mcp_apps__source-packet.md`

### 2. Why AI needs a new kind of supercomputer network — the OpenAI Podcast Ep. 18
- `source_name`: `OpenAI YouTube`
- `source_id`: `youtube__openai`
- `primary_source`: `yes`
- `published_at`: `2026-05-06 19:44:56 CST`
- `captured_at`: `2026-05-06 22:44:47 CST`
- `canonical_url`: `https://www.youtube.com/watch?v=TiW96H5HmAw`
- `score`: `11`
- `selection_reason`: `fit, primary=yes, published=2026-05-06 19:44:56 CST`
- `summary`: `OpenAI YouTube 频道页抓到新视频“Why AI needs a new kind of supercomputer network — the OpenAI Podcast Ep. 18”。Jina 频道快照现在可稳定保留标题、链接与相对发布时间，适合作为视频线索的硬成功入口。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224447__youtube_openai_why_ai_needs_a_new_kind_of_supercomputer_network_the_openai_podcast_ep_1__source-packet.md`

### 3. Harshil Mathur: AI Is Compressing Every Moat
- `source_name`: `Y Combinator YouTube`
- `source_id`: `youtube__ycombinator`
- `primary_source`: `partial`
- `published_at`: `2026-05-06 20:44:47 CST`
- `captured_at`: `2026-05-06 22:44:47 CST`
- `canonical_url`: `https://www.youtube.com/watch?v=X5bABLCuIHA`
- `score`: `10`
- `selection_reason`: `fit, primary=partial, published=2026-05-06 20:44:47 CST`
- `summary`: `Y Combinator YouTube 频道页直连抓到新视频“Harshil Mathur: AI Is Compressing Every Moat”。当前直接解析频道页内的 ytInitialData，避免 Jina 波动对视频 lane 造成整组失真。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224447__youtube_ycombinator_harshil_mathur_ai_is_compressing_every_moat__source-packet.md`

### 4. 2.5x faster inference with Qwen 3.6 27B using MTP - Finally a viable option for local agentic coding - 262k context on 48GB - Fixed chat template - Drop-in OpenAI and Anthropic API endpoints
- `source_name`: `Reddit / LocalLLaMA Daily Top`
- `source_id`: `trend__reddit_localllama_daily`
- `primary_source`: `no`
- `published_at`: `2026-05-06 17:35:42 CST`
- `captured_at`: `2026-05-06 22:42:50 CST`
- `canonical_url`: `https://old.reddit.com/r/LocalLLaMA/comments/1t57xuu/25x_faster_inference_with_qwen_36_27b_using_mtp/`
- `score`: `10`
- `selection_reason`: `fit, primary=no, published=2026-05-06 17:35:42 CST`
- `summary`: `Reddit / r/LocalLLaMA 的日榜 RSS 收录了“2.5x faster inference with Qwen 3.6 27B using MTP - Finally a viable option for local agentic coding - 262k context on 48GB - Fixed chat template - Drop-in OpenAI and Anthropic API endpoints”，当前位于本轮抓取顺序第 3 位。它更适合判断真实用户问题、真实体验和外部对象入口，不适合直接当正式事实证据。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224250__reddit_localllama_2_5x_faster_inference_with_qwen_3_6_27b_using_mtp_finally_a_viable_optio__source-packet.md`

## Source Refs

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224447__youtube_ai_dot_engineer_mcp_ui_extending_the_frontier_liad_yosef_and_ido_salomon_mcp_apps__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224447__youtube_openai_why_ai_needs_a_new_kind_of_supercomputer_network_the_openai_podcast_ep_1__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224447__youtube_ycombinator_harshil_mathur_ai_is_compressing_every_moat__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224250__reddit_localllama_2_5x_faster_inference_with_qwen_3_6_27b_using_mtp_finally_a_viable_optio__source-packet.md`

## Excluded Samples

- `published_at_outside_window | Marc Lore says that AI will soon enable anyone open a restaurant | published_at=2026-05-06 14:34:32 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_190704__techcrunch_ai_marc_lore_says_that_ai_will_soon_enable_anyone_open_a_restaurant__source-packet.md`
- `published_at_outside_window | Peter Sarlin’s QuTwo reaches $380M valuation in angel round | published_at=2026-05-06 14:47:12 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_190704__techcrunch_ai_peter_sarlin_s_qutwo_reaches_380m_valuation_in_angel_round__source-packet.md`
- `published_at_outside_window | Unlocking large scale AI training networks with MRC (Multipath Reliable Connection) | published_at=2026-05-05 18:00:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_214229__openai_news_unlocking_large_scale_ai_training_networks_with_mrc_multipath_reliable_c__source-packet.md`
- `published_at_outside_window | acknowledged the mistake without admitting guilt | published_at=2026-05-06 11:16:53 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224250__reddit_chatgpt_acknowledged_the_mistake_without_admitting_guilt__source-packet.md`
- `published_at_outside_window | I asked ChatGPT to redraw iconic NBA photos as horribly as possible | published_at=2026-05-06 02:50:53 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224250__reddit_chatgpt_i_asked_chatgpt_to_redraw_iconic_nba_photos_as_horribly_as_possible__source-packet.md`
- `published_at_outside_window | My guy was hallucinating HARD today. | published_at=2026-05-06 03:32:30 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224250__reddit_chatgpt_my_guy_was_hallucinating_hard_today__source-packet.md`
- `published_at_outside_window | Prompt Injection experience - my first time ever | published_at=2026-05-06 16:39:35 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224250__reddit_claude_prompt_injection_experience_my_first_time_ever__source-packet.md`
- `published_at_outside_window | Spyware? | published_at=2026-05-06 05:58:56 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224250__reddit_claude_spyware__source-packet.md`
- `published_at_unparseable | How Clay manages 300M agent runs a month with LangSmith | published_at=unknown | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224447__youtube_langchain_how_clay_manages_300m_agent_runs_a_month_with_langsmith__source-packet.md`
- `published_at_unparseable | AI记账软件怼用户买的衣服像寿衣 | published_at=2026-05-06 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224708__baidu_realtime_ai__source-packet.md`
- `published_at_outside_window | 英伟达中国份额降至0%，A股国产芯片今日集体暴涨，寒武纪等创历史新高，对此你怎么看？ | published_at=2026-05-06 13:59:52 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224708__zhihu_hot_ai_0_a__source-packet.md`
- `published_at_outside_window | OpenAI推出GPT-5.5 Instant，有哪些值得关注的技术亮点？使用感受如何？ | published_at=2026-05-06 09:05:08 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_224708__zhihu_hot_ai_openai_gpt_5_5_instant__source-packet.md`
- `published_at_unparseable | addyosmani/agent-skills | published_at=2026-05-06 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_232523__github_trending_addyosmani_agent_skills__source-packet.md`
- `published_at_unparseable | InsForge/InsForge | published_at=2026-05-06 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_232523__github_trending_insforge_insforge__source-packet.md`
- `published_at_unparseable | LadybirdBrowser/ladybird | published_at=2026-05-06 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_232523__github_trending_ladybirdbrowser_ladybird__source-packet.md`
- `published_at_unparseable | LearningCircuit/local-deep-research | published_at=2026-05-06 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_232523__github_trending_learningcircuit_local_deep_research__source-packet.md`
- `published_at_unparseable | PriorLabs/TabPFN | published_at=2026-05-06 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_232523__github_trending_priorlabs_tabpfn__source-packet.md`
- `published_at_outside_window | CARA 2.0 – “I Built a Better Robot Dog” | published_at=2026-05-04 14:46:10 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_232523__hn_frontpage_48005432_cara_2_0_i_built_a_better_robot_dog__source-packet.md`
- `published_at_outside_window | Agents can now create Cloudflare accounts, buy domains, and deploy | published_at=2026-05-06 11:10:33 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_232523__hn_frontpage_48031684_agents_can_now_create_cloudflare_accounts_buy_domains_and_deplo__source-packet.md`
- `not_ai_enough | Adding Benchmaxxer Repellant to the Open ASR Leaderboard | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_232523__huggingface_blog_adding_benchmaxxer_repellant_to_the_open_asr_leaderboard__source-packet.md`
- `... +5 more excluded items`

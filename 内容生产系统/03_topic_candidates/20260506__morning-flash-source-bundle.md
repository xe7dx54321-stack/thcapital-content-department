# Morning Flash Source Bundle

- `generated_at`: `2026-05-06 05:51:24 CST`
- `date`: `2026-05-06`
- `selection_status`: `under_target`
- `business_window_start`: `2026-05-05 17:00:00 CST`
- `business_window_end`: `2026-05-06 05:00:00 CST`
- `selected_items`: `4`
- `min_items_required`: `8`
- `max_items_allowed`: `8`
- `excluded_items`: `24`

## Policy

- 只允许从 `captured_at` 落在 `T-1 17:00 -> T 05:00` 的 source packet 中选题。
- `published_at` 必须可解析，且同样落在晨间时间窗内；否则一律视为 stale / 不可审计，禁止写进早报正文。
- 只选 AI / Agent / 模型 / 机器人 / infra / 工作流相关对象；招聘、报名、榜单征集、活动预告等 meta 内容一律排除。
- 后续 approved-topic / draft-pack / wechat.md 只允许使用本 bundle 内对象，不得额外增写 bundle 外历史旧题。

## Selected Events

### 1. Let AI Agents Tell You What They Need — Raj Navakoti, IKEA
- `source_name`: `AI Engineer YouTube`
- `source_id`: `youtube__aidotengineer`
- `primary_source`: `partial`
- `published_at`: `2026-05-05 21:43:39 CST`
- `captured_at`: `2026-05-05 22:43:02 CST`
- `canonical_url`: `https://www.youtube.com/watch?v=_QAVExf_1uw`
- `score`: `12`
- `selection_reason`: `fit, primary=partial, published=2026-05-05 21:43:39 CST`
- `summary`: `AI Engineer YouTube 频道页抓到新视频“Let AI Agents Tell You What They Need — Raj Navakoti, IKEA”。Jina 频道快照现在可稳定保留标题、链接与相对发布时间，适合作为视频线索的硬成功入口。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_224302__youtube_ai_dot_engineer_let_ai_agents_tell_you_what_they_need_raj_navakoti_ikea__source-packet.md`

### 2. AI didn't delete your database, you did
- `source_name`: `Hacker News Frontpage`
- `source_id`: `trend__hn_frontpage`
- `primary_source`: `partial`
- `published_at`: `2026-05-05 22:07:50 CST`
- `captured_at`: `2026-05-05 23:25:41 CST`
- `canonical_url`: `https://idiallo.com/blog/ai-didnt-delete-your-database-you-did`
- `score`: `10`
- `selection_reason`: `fit, primary=partial, published=2026-05-05 22:07:50 CST`
- `summary`: `Hacker News RSS 抓到高热新条目。它适合作为 builder / startup / AI infra 话题的扩散入口，不是最终事实源。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_232541__hn_frontpage_48022742_ai_didn_t_delete_your_database_you_did__source-packet.md`

### 3. Warning: Anthropic's "Gift Max" exploit drained €800+, ruined my credit, and got me banned.
- `source_name`: `Reddit / ChatGPT Daily Top`
- `source_id`: `trend__reddit_chatgpt_daily`
- `primary_source`: `no`
- `published_at`: `2026-05-05 17:55:05 CST`
- `captured_at`: `2026-05-05 21:56:35 CST`
- `canonical_url`: `https://old.reddit.com/r/ChatGPT/comments/1t4atbx/warning_anthropics_gift_max_exploit_drained_800/`
- `score`: `10`
- `selection_reason`: `fit, primary=no, published=2026-05-05 17:55:05 CST`
- `summary`: `Reddit / r/ChatGPT 的日榜 RSS 收录了“Warning: Anthropic's "Gift Max" exploit drained €800+, ruined my credit, and got me banned.”，当前位于本轮抓取顺序第 3 位。它更适合判断真实用户问题、真实体验和外部对象入口，不适合直接当正式事实证据。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_215635__reddit_chatgpt_warning_anthropic_s_gift_max_exploit_drained_800_ruined_my_credit_and_go__source-packet.md`

### 4. India’s first GenAI unicorn shifts to cloud services as AI model ambitions face reality
- `source_name`: `TechCrunch AI`
- `source_id`: `web__techcrunch_ai`
- `primary_source`: `no`
- `published_at`: `2026-05-05 21:18:50 CST`
- `captured_at`: `2026-05-05 21:26:01 CST`
- `canonical_url`: `https://techcrunch.com/2026/05/05/indias-first-genai-unicorn-shifts-to-cloud-services-as-ai-model-ambitions-face-reality/`
- `score`: `9`
- `selection_reason`: `fit, primary=no, published=2026-05-05 21:18:50 CST, mainstream_or_primary_lane`
- `summary`: `TechCrunch AI RSS 抓到新条目“India’s first GenAI unicorn shifts to cloud services as AI model ambitions face reality”。这类媒体稿通常适合作为融资、新产品、新公司与产业变动的入口，后续需要继续回链公司官网、融资公告或创始人原话。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_212601__techcrunch_ai_india_s_first_genai_unicorn_shifts_to_cloud_services_as_ai_model_ambitio__source-packet.md`

## Source Refs

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_224302__youtube_ai_dot_engineer_let_ai_agents_tell_you_what_they_need_raj_navakoti_ikea__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_232541__hn_frontpage_48022742_ai_didn_t_delete_your_database_you_did__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_215635__reddit_chatgpt_warning_anthropic_s_gift_max_exploit_drained_800_ruined_my_credit_and_go__source-packet.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_212601__techcrunch_ai_india_s_first_genai_unicorn_shifts_to_cloud_services_as_ai_model_ambitio__source-packet.md`

## Excluded Samples

- `published_at_outside_window | Featherless Raises $20M in Series A Funding - FinSMEs | published_at=2026-05-04 18:33:23 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_190925__finsmes_ai_gnews_featherless_raises_20m_in_series_a_funding_finsmes__source-packet.md`
- `published_at_outside_window | 谷歌、英伟达押注，这家估值 40 亿美元的 AI 公司，想把科学家直接干掉 | published_at=2026-05-05 12:00:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_191454__wechat_geekpark_40_ai__source-packet.md`
- `published_at_outside_window | 豆包要收费了：三档订阅最贵500元/月，保留免费基础版 | published_at=2026-05-05 11:51:03 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_191454__wechat_qbitai_500__source-packet.md`
- `published_at_outside_window | 马斯克破大防了：私信求和遭拒，怒喷奥特曼Brockman「全美最恶人」 | published_at=2026-05-05 14:00:00 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_191454__wechat_qbitai_brockman__source-packet.md`
- `promo_or_meta | 量子位编辑作者招聘 | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_191454__wechat_qbitai_https_mp_weixin_qq_com_s_letqz0b_qustm3uvroywdw__source-packet.md`
- `published_at_outside_window | DeepSeek V4 Pro matches GPT-5.2 on FoodTruck Bench, our agentic benchmark — 10 weeks later, ~17× cheaper | published_at=2026-05-05 14:51:49 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_215635__reddit_localllama_deepseek_v4_pro_matches_gpt_5_2_on_foodtruck_bench_our_agentic_benchmark__source-packet.md`
- `published_at_outside_window | Peanut - Text to Image Model (Open Weights coming soon) | published_at=2026-05-05 12:47:18 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_215635__reddit_localllama_peanut_text_to_image_model_open_weights_coming_soon__source-packet.md`
- `published_at_outside_window | Qwen3.6 27B FP8 runs with 200k tokens of BF16 KV cache at 80 TPS on a single RTX 5000 PRO 48GB | published_at=2026-05-05 13:46:22 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_215635__reddit_localllama_qwen3_6_27b_fp8_runs_with_200k_tokens_of_bf16_kv_cache_at_80_tps_on_a_si__source-packet.md`
- `published_at_unparseable | 公园可花9块9租外骨骼机器人爬山 热 | published_at=2026-05-05 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_215922__baidu_realtime_9_9__source-packet.md`
- `published_at_unparseable | 用AI写出20亿播放量神曲？音乐人发声 热 | published_at=2026-05-05 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_215922__baidu_realtime_ai_20__source-packet.md`
- `published_at_unparseable | 机器人爆火 哪些赚钱哪些裸泳 新 | published_at=2026-05-05 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_215922__baidu_realtime_baidu_hot__source-packet.md`
- `published_at_outside_window | 奥斯卡新规明确禁用 AI 演员、限制 AI 剧本，究竟是守护创作本质，还是在开时代倒车？ | published_at=2026-05-02 22:59:34 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_215922__zhihu_hot_ai_ai_ai__source-packet.md`
- `published_at_outside_window | 韩国兴起「全民借钱投资」热，居民股市杠杆倍数屡创新高，对此你怎么看，这样的疯狂还能持续多久？ | published_at=2026-05-05 10:35:42 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_215922__zhihu_hot_ai_zhihu_hot__source-packet.md`
- `published_at_unparseable | cocoindex-io/cocoindex | published_at=2026-05-05 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_232541__github_trending_cocoindex_io_cocoindex__source-packet.md`
- `published_at_unparseable | mksglu/context-mode | published_at=2026-05-05 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_232541__github_trending_mksglu_context_mode__source-packet.md`
- `published_at_unparseable | msitarzewski/agency-agents | published_at=2026-05-05 (capture day) | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_232541__github_trending_msitarzewski_agency_agents__source-packet.md`
- `published_at_outside_window | Train Your Own LLM from Scratch | published_at=2026-05-05 12:09:17 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_232541__hn_frontpage_48017948_train_your_own_llm_from_scratch__source-packet.md`
- `published_at_outside_window | Google Chrome silently installs a 4 GB AI model on your device without consent | published_at=2026-05-05 15:34:55 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_232541__hn_frontpage_48019219_google_chrome_silently_installs_a_4_gb_ai_model_on_your_device___source-packet.md`
- `published_at_outside_window | Automatic Reflection Level Classification in Hungarian Student Essays | published_at=2026-05-04 17:44:50 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_232541__huggingface_daily_papers_automatic_reflection_level_classification_in_hungarian_student_essays__source-packet.md`
- `published_at_outside_window | Counterfactual Reasoning in Automated Planning | published_at=2026-05-04 21:50:59 CST | /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260505_232541__huggingface_daily_papers_counterfactual_reasoning_in_automated_planning__source-packet.md`
- `... +4 more excluded items`

# Top20 初筛包

- `date`: `2026-05-06`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-05-06 17:35:00 CST`
- `source_scope`: `T-1 17:00 ~ T 14:30 (business window) + PM limited reinforcement`
- `total_candidates_seen`: `74 source packets / 4 deep articles / 4 asset chains`
- `top20_count`: `11`
- `delivery_lane`: `day_mainline`
- `delivery_deadline`: `2026-05-06 19:00 CST`
- `scorecard_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260506__top20__stage-gate-scorecard.md`
- `manifest_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260506__market-source-manifest.md`
- `business_window_status`: `open`
- `builder_mode`: `script_materialized_baseline + limited_reinforcement`

## 使用说明

- 这是 `signal-scout` 阶段正式交付包，基于 manifest 真实文件清单脚本化预物化。
- 这份包的目标是保证 day_mainline 不会停留在模板壳；后续 agent 可以继续强化排序、补证和切角。
- 若后续出现 `__reworked` 版本，应以更新版本为准。

## 评分框架

| 维度 | 说明 | 分值 |
|---|---|---|
| 一手性 | 是否来自官方 / 原始口径 / 可追溯原文 | 0-3 |
| 传播性 | 是否已有开发者圈 / 媒体 / 社区扩散 | 0-3 |
| 破圈性 | 是否有明显争议、反差或热度突破口 | 0-3 |
| 赛道匹配 | 是否契合 AI / Agent / 一人公司 / 模型 / infra / 硬件主线 | 0-3 |
| 可延展性 | 是否能继续深挖成观点稿、拆解稿或复盘稿 | 0-3 |
| 数据硬度 | 是否有硬链接、时间锚点、数字或原始页面 | 0-3 |
| 视觉素材丰富度 | 是否有原始截图 / 产品页 / 可解释图来源 | 0-3 |
| 平台适配潜力 | 是否适合微信及多平台改写 | 0-3 |
| 时效窗口 | 当前业务日写它是否仍然值钱 | 0-3 |
| 讨论度 / 争议度 | 是否自带讨论空间 | 0-3 |

---

## Top20 候选

### 1. 豆包付费版本曝光，每月 68-500 元三档，你愿意付费吗？国产 AI 推付费服务是一种趋势吗？
- `topic_key`: `zhihu_hot_ai_68_500_ai_20260506`
- `title`: `豆包付费版本曝光，每月 68-500 元三档，你愿意付费吗？国产 AI 推付费服务是一种趋势吗？`
- `primary_platform`: `知乎热榜`
- `published_at`: `2026-05-04 14:40:23 CST`
- `original_link`: `https://www.zhihu.com/question/2034643547668862086`
- `score_total`: `19 / 30`
- `mainstream_bias_score`: `6`
- `blended_priority_score`: `25`
- `score_breakdown`: `一手性=1 / 传播性=3 / 破圈性=3 / 赛道匹配=2 / 可延展性=1 / 数据硬度=0 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度 / 争议度=3`
- `signal_summary`: `知乎热榜出现了 AI 相关问题“豆包付费版本曝光，每月 68-500 元三档，你愿意付费吗？国产 AI 推付费服务是一种趋势吗？”。 当前热度 161 万热度。它适合作为中文问答场域的破圈验证和用户疑问观察层。`
- `why_in_top20`: `有明确扩散热度入口；具备天然讨论空间；更接近官方 / 主流媒体共识`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文；缺全文深抓，角度延展需谨慎；硬数据偏少`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260504_232837__zhihu_hot_ai_68_500_ai__source-packet.md`

---

### 2. 选一条路，决定你接下来的旅途
- `topic_key`: `bilibili_popular_ai_bv1jorvbyee3_20260506`
- `title`: `选一条路，决定你接下来的旅途`
- `primary_platform`: `Bilibili Popular All / AI-Relevant`
- `published_at`: `2026-05-04 15:43:38 CST`
- `original_link`: `https://www.bilibili.com/video/BV1joRvBYEE3`
- `score_total`: `19 / 30`
- `mainstream_bias_score`: `1`
- `blended_priority_score`: `20`
- `score_breakdown`: `一手性=2 / 传播性=1 / 破圈性=1 / 赛道匹配=2 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度 / 争议度=3`
- `signal_summary`: `B站热门榜抓到 AI 相关视频“选一条路，决定你接下来的旅途”。它适合作为中文视频热榜入口，帮助判断 AI 话题是否开始向大众用户扩散，并识别可被重构的话题切口。`
- `why_in_top20`: `partial source；有明确扩散热度入口；具备天然讨论空间`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文；缺全文深抓，角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260504_232147__bilibili_popular_ai_BV1joRvBYEE3__source-packet.md`

---

### 3. Vibe Coding vs. Production reality
- `topic_key`: `reddit_claude_vibe_coding_vs_production_reality_20260506`
- `title`: `Vibe Coding vs. Production reality`
- `primary_platform`: `Reddit / ClaudeAI Daily Top`
- `published_at`: `2026-05-04 16:23:13 CST`
- `original_link`: `https://old.reddit.com/r/ClaudeAI/comments/1t3bk3x/vibe_coding_vs_production_reality/`
- `score_total`: `22 / 30`
- `mainstream_bias_score`: `-3`
- `blended_priority_score`: `19`
- `score_breakdown`: `一手性=1 / 传播性=3 / 破圈性=3 / 赛道匹配=3 / 可延展性=2 / 数据硬度=1 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度 / 争议度=3`
- `signal_summary`: `Reddit / r/ClaudeAI 的日榜 RSS 收录了“Vibe Coding vs. Production reality”，当前位于本轮抓取顺序第 2 位。它更适合判断真实用户问题、真实体验和外部对象入口，不适合直接当正式事实证据。`
- `why_in_top20`: `有明确扩散热度入口；具备天然讨论空间；与 AI / Agent / 一人公司主线高度一致`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文；缺全文深抓，角度延展需谨慎；硬数据偏少`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260504_232031__reddit_claude_vibe_coding_vs_production_reality__source-packet.md`

---

### 4. Ralph Loops: Build Dumb AI Loops That Ship — Chris Parsons, Cherrypick
- `topic_key`: `youtube_ai_dot_engineer_ralph_loops_build_dumb_ai_loops_that_ship_chris_parsons_cherrypick_20260506`
- `title`: `Ralph Loops: Build Dumb AI Loops That Ship — Chris Parsons, Cherrypick`
- `primary_platform`: `AI Engineer YouTube`
- `published_at`: `unknown`
- `original_link`: `https://www.youtube.com/watch?v=2TLXsxkz0zI`
- `score_total`: `19 / 30`
- `mainstream_bias_score`: `0`
- `blended_priority_score`: `19`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=1 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度 / 争议度=1`
- `signal_summary`: `AI Engineer YouTube 频道页抓到新视频“Ralph Loops: Build Dumb AI Loops That Ship — Chris Parsons, Cherrypick”。Jina 频道快照现在可稳定保留标题、链接与相对发布时间，适合作为视频线索的硬成功入口。`
- `why_in_top20`: `partial source；与 AI / Agent / 一人公司主线高度一致`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文；发布时间不够硬；缺全文深抓，角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260504_232147__youtube_ai_dot_engineer_ralph_loops_build_dumb_ai_loops_that_ship_chris_parsons_cherrypick__source-packet.md`

---

### 5. Llama.cpp MTP support now in beta!
- `topic_key`: `reddit_localllama_llama_cpp_mtp_support_now_in_beta_20260506`
- `title`: `Llama.cpp MTP support now in beta!`
- `primary_platform`: `Reddit / LocalLLaMA Daily Top`
- `published_at`: `2026-05-04 20:54:14 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1t3guzw/llamacpp_mtp_support_now_in_beta/`
- `score_total`: `21 / 30`
- `mainstream_bias_score`: `-3`
- `blended_priority_score`: `18`
- `score_breakdown`: `一手性=1 / 传播性=3 / 破圈性=3 / 赛道匹配=2 / 可延展性=2 / 数据硬度=1 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度 / 争议度=3`
- `signal_summary`: `Reddit / r/LocalLLaMA 的日榜 RSS 收录了“Llama.cpp MTP support now in beta!”，当前位于本轮抓取顺序第 4 位。它更适合判断真实用户问题、真实体验和外部对象入口，不适合直接当正式事实证据。`
- `why_in_top20`: `有明确扩散热度入口；具备天然讨论空间`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文；缺全文深抓，角度延展需谨慎；硬数据偏少`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260504_232031__reddit_localllama_llama_cpp_mtp_support_now_in_beta__source-packet.md`

---

### 6. 女学生照片被改黄图涉事男子已道歉
- `topic_key`: `baidu_realtime_baidu_hot_20260506`
- `title`: `女学生照片被改黄图涉事男子已道歉`
- `primary_platform`: `百度热搜`
- `published_at`: `2026-05-04 (capture day)`
- `original_link`: `https://www.baidu.com/s?wd=%E5%A5%B3%E5%AD%A6%E7%94%9F%E7%85%A7%E7%89%87%E8%A2%AB%E6%94%B9%E9%BB%84%E5%9B%BE%E6%B6%89%E4%BA%8B%E7%94%B7%E5%AD%90%E5%B7%B2%E9%81%93%E6%AD%89&sa=fyb_news&rsv_dl=fyb_news`
- `score_total`: `19 / 30`
- `mainstream_bias_score`: `1`
- `blended_priority_score`: `20`
- `score_breakdown`: `一手性=1 / 传播性=1 / 破圈性=2 / 赛道匹配=3 / 可延展性=2 / 数据硬度=1 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度 / 争议度=3`
- `signal_summary`: `百度热搜出现了与 AI / agent / robotics 相关的话题“女学生照片被改黄图涉事男子已道歉”。当前热搜指数 6186355，它适合作为中文破圈验证信号，而不是事实源。`
- `why_in_top20`: `有明确扩散热度入口；具备天然讨论空间；与 AI / Agent / 一人公司主线高度一致`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文；缺全文深抓，角度延展需谨慎；硬数据偏少`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260504_232837__baidu_realtime_baidu_hot__source-packet.md`

---

### 7. 当我跟豆包学习把便宜茶配制成贵茶
- `topic_key`: `bilibili_popular_ai_bv1q3rcbkeqy_20260506`
- `title`: `当我跟豆包学习把便宜茶配制成贵茶`
- `primary_platform`: `Bilibili Popular All / AI-Relevant`
- `published_at`: `2026-05-04 10:00:00 CST`
- `original_link`: `https://www.bilibili.com/video/BV1q3RcBKEQy`
- `score_total`: `18 / 30`
- `mainstream_bias_score`: `1`
- `blended_priority_score`: `19`
- `score_breakdown`: `一手性=2 / 传播性=1 / 破圈性=1 / 赛道匹配=2 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=1 / 讨论度 / 争议度=3`
- `signal_summary`: `B站热门榜抓到 AI 相关视频“当我跟豆包学习把便宜茶配制成贵茶”。它适合作为中文视频热榜入口，帮助判断 AI 话题是否开始向大众用户扩散，并识别可被重构的话题切口。`
- `why_in_top20`: `partial source；有明确扩散热度入口；具备天然讨论空间`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文；缺全文深抓，角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260504_200534__bilibili_popular_ai_BV1q3RcBKEQy__source-packet.md`

---

### 8. it's time to update your Gemma 4 GGUFs
- `topic_key`: `reddit_localllama_it_s_time_to_update_your_gemma_4_ggufs_20260506`
- `title`: `it's time to update your Gemma 4 GGUFs`
- `primary_platform`: `Reddit / LocalLLaMA Daily Top`
- `published_at`: `2026-05-04 18:12:15 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1t3dfvp/its_time_to_update_your_gemma_4_ggufs/`
- `score_total`: `21 / 30`
- `mainstream_bias_score`: `-3`
- `blended_priority_score`: `18`
- `score_breakdown`: `一手性=1 / 传播性=3 / 破圈性=3 / 赛道匹配=2 / 可延展性=2 / 数据硬度=1 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度 / 争议度=3`
- `signal_summary`: `Reddit / r/LocalLLaMA 的日榜 RSS 收录了“it's time to update your Gemma 4 GGUFs”，当前位于本轮抓取顺序第 3 位。它更适合判断真实用户问题、真实体验和外部对象入口，不适合直接当正式事实证据。`
- `why_in_top20`: `有明确扩散热度入口；具备天然讨论空间`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文；缺全文深抓，角度延展需谨慎；硬数据偏少`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260504_232031__reddit_localllama_it_s_time_to_update_your_gemma_4_ggufs__source-packet.md`

---

### 9. Chat GPT got that guy in trouble and he doesn’t even know it yet…lol
- `topic_key`: `reddit_chatgpt_chat_gpt_got_that_guy_in_trouble_and_he_doesn_t_even_know_it_yet_lol_20260506`
- `title`: `Chat GPT got that guy in trouble and he doesn’t even know it yet…lol`
- `primary_platform`: `Reddit / ChatGPT Daily Top`
- `published_at`: `2026-05-04 21:58:07 CST`
- `original_link`: `https://old.reddit.com/r/ChatGPT/comments/1t3ii1l/chat_gpt_got_that_guy_in_trouble_and_he_doesnt/`
- `score_total`: `21 / 30`
- `mainstream_bias_score`: `-3`
- `blended_priority_score`: `18`
- `score_breakdown`: `一手性=1 / 传播性=3 / 破圈性=3 / 赛道匹配=2 / 可延展性=2 / 数据硬度=1 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度 / 争议度=3`
- `signal_summary`: `Reddit / r/ChatGPT 的日榜 RSS 收录了“Chat GPT got that guy in trouble and he doesn’t even know it yet…lol”，当前位于本轮抓取顺序第 1 位。它更适合判断真实用户问题、真实体验和外部对象入口，不适合直接当正式事实证据。`
- `why_in_top20`: `有明确扩散热度入口；具备天然讨论空间`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文；缺全文深抓，角度延展需谨慎；硬数据偏少`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260504_232031__reddit_chatgpt_chat_gpt_got_that_guy_in_trouble_and_he_doesn_t_even_know_it_yet_lol__source-packet.md`

---

### 10. Welcome to LinkedIn Park (im sorry for this)
- `topic_key`: `reddit_chatgpt_welcome_to_linkedin_park_im_sorry_for_this_20260506`
- `title`: `Welcome to LinkedIn Park (im sorry for this)`
- `primary_platform`: `Reddit / ChatGPT Daily Top`
- `published_at`: `2026-05-03 23:29:19 CST`
- `original_link`: `https://old.reddit.com/r/ChatGPT/comments/1t2ojle/welcome_to_linkedin_park_im_sorry_for_this/`
- `score_total`: `20 / 30`
- `mainstream_bias_score`: `-3`
- `blended_priority_score`: `17`
- `score_breakdown`: `一手性=1 / 传播性=3 / 破圈性=3 / 赛道匹配=2 / 可延展性=2 / 数据硬度=1 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=1 / 讨论度 / 争议度=3`
- `signal_summary`: `Reddit / r/ChatGPT 的日榜 RSS 收录了“Welcome to LinkedIn Park (im sorry for this)”，当前位于本轮抓取顺序第 3 位。它更适合判断真实用户问题、真实体验和外部对象入口，不适合直接当正式事实证据。`
- `why_in_top20`: `有明确扩散热度入口；具备天然讨论空间`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文；缺全文深抓，角度延展需谨慎；硬数据偏少`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260504_232031__reddit_chatgpt_welcome_to_linkedin_park_im_sorry_for_this__source-packet.md`

---

### 11. GPT-5.5 Instant 正式上线：ChatGPT 默认模型切换，个性化记忆升级
- `topic_key`: `openai_gpt_5_5_instant_chatgpt_default_20260506`
- `title`: `GPT-5.5 Instant 正式上线：ChatGPT 默认模型切换，个性化记忆升级`
- `primary_platform`: `OpenAI X / TechCrunch`
- `published_at`: `2026-05-06 08:05:18 CST`
- `original_link`: `https://x.com/OpenAI`
- `score_total`: `22 / 30`
- `mainstream_bias_score`: `5`
- `blended_priority_score`: `27`
- `score_breakdown`: `一手性=3 / 传播性=3 / 破圈性=3 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=3 / 时效窗口=3 / 讨论度 / 争议度=2`
- `signal_summary`: `OpenAI 官方账号宣布 GPT-5.5 Instant 将在两天内逐步推送为所有 ChatGPT 用户的默认模型，同时上线记忆与个性化增强功能。官方一手信号强，时效新鲜，属于今日最强 AI 主线事件。`
- `why_in_top20`: `官方一手源；今日最强 AI 主线事件；多平台高频扩散；时效窗口全开`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `需继续回链 OpenAI 官方博客或 docs 补硬数据；纯社交帖文不宜直接当最终结论`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_090249__x_openai_gpt_5_5_instant_is_rolling_out_over_the_next_two_days_as_the_default_mod__source-packet.md`

---

### 12. Mistral 为 Le Chat 新增 Remote Agents 与 Work Mode
- `topic_key`: `mistral_le_chat_remote_agents_work_mode_20260506`
- `title`: `Mistral 为 Le Chat 新增 Remote Agents 与 Work Mode`
- `primary_platform`: `InfoQ AI/ML`
- `published_at`: `2026-05-06 (approx)`
- `original_link`: `https://www.infoq.com/news/2026/05/mistral-agents-lechat/`
- `score_total`: `20 / 30`
- `mainstream_bias_score`: `2`
- `blended_priority_score`: `22`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度 / 争议度=1`
- `signal_summary`: `InfoQ 捕捉到 Mistral 为其 Le Chat 平台新增 Remote Agents 和 Work Mode 功能，属于开源模型厂商向 Agent 产品化演进的典型信号，与 AI / Agent 主线高度相关。`
- `why_in_top20`: `开源模型厂商 Agent 化主线匹配；工程实践参考价值高；需补官方产品页或 GitHub 确认细节`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `published_at 时间不明确；需补官方发布页或 GitHub PR 确认功能细节`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260506_141629__infoq_ai_ml_mistral_adds_remote_agents_and_work_mode_to_le_chat__source-packet.md`

---

## 结论

### top3_must_watch

| 排名 | topic_key | 理由 |
|---|---|---|
| #1 | `zhihu_hot_ai_68_500_ai_20260506` | 强扩散 |
| #2 | `openai_gpt_5_5_instant_chatgpt_default_20260506` | 官方一手，今日最强主线 |
| #3 | `reddit_claude_vibe_coding_vs_production_reality_20260506` | 强扩散 / 主线高度匹配 |

### top6_strong_pool

| 排名 | topic_key | 理由 |
|---|---|---|
| #4 | `youtube_ai_dot_engineer_ralph_loops_build_dumb_ai_loops_that_ship_chris_parsons_cherrypick_20260506` | partial source；与 AI / Agent / 一人公司主线高度一致 |
| #5 | `reddit_localllama_llama_cpp_mtp_support_now_in_beta_20260506` | 有明确扩散热度入口；具备天然讨论空间 |
| #6 | `baidu_realtime_baidu_hot_20260506` | 有明确扩散热度入口；具备天然讨论空间；与 AI / Agent / 一人公司主线高度一致 |
| #7 | `bilibili_popular_ai_bv1q3rcbkeqy_20260506` | partial source；有明确扩散热度入口；具备天然讨论空间 |
| #8 | `reddit_localllama_it_s_time_to_update_your_gemma_4_ggufs_20260506` | 有明确扩散热度入口；具备天然讨论空间 |
| #9 | `reddit_chatgpt_chat_gpt_got_that_guy_in_trouble_and_he_doesn_t_even_know_it_yet_lol_20260506` | 有明确扩散热度入口；具备天然讨论空间 |

### new_entries_reinforced

| 排名 | topic_key | 理由 |
|---|---|---|
| #11 | `openai_gpt_5_5_instant_chatgpt_default_20260506` | PM 心跳强化：官方一手，今日最强 AI 主线，多平台高频扩散 |
| #12 | `mistral_le_chat_remote_agents_work_mode_20260506` | PM 心跳强化：开源模型 Agent 化主线，工程实践参考价值高 |

### holdout_watchlist

- `none`

### supply_risk

- `kept_candidates`: `12`
- `manifest_source_packets`: `74`
- `manifest_deep_articles`: `4`
- `excluded_recent_duplicates`: `0`
- `excluded_low_fit`: `0`
- `notes`: `本包在 baseline 10 候选基础上，由 PM 心跳有限强化新增 #11 GPT-5.5 Instant（官方一手，今日最强主线）与 #12 Mistral Le Chat Remote Agents（开源模型 Agent 化主线）；共计 12 个候选，时效窗口仍开放至 19:00 CST。`

## 本包交付约束

- **不得自行放行**：本包为 `market-scout` 初筛交付，是否进入下一工序由 `market-editor` 最新 scorecard 决定。

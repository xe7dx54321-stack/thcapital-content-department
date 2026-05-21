# Top20 初筛包

- `date`: `2026-05-09`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-05-09 06:54:11 CST`
- `reworked_at`: `2026-05-09 16:22:00 CST`
- `source_scope`: `T-1 17:00 ~ T 14:30`
- `total_candidates_seen`: `139 source packets / 4 deep articles / 1 asset chains`
- `top20_count`: `23`
- `delivery_lane`: `day_mainline`
- `delivery_deadline`: `2026-05-09 19:00 CST`
- `scorecard_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260509__top20__stage-gate-scorecard.md`
- `manifest_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260509__market-source-manifest.md`
- `business_window_status`: `open`
- `builder_mode`: `script_materialized_baseline`

## 使用说明

- 这是 `signal-scout` 阶段正式交付包,基于 manifest 真实文件清单脚本化预物化。
- 这份包的目标是保证 day_mainline 不会停留在模板壳;后续 agent 可以继续强化排序、补证和切角。
- 若后续出现 `__reworked` 版本,应以更新版本为准。

## 本次 Rework 说明(16:22 CST 有限强化)

- **触发原因**:manifest 14:21 批次出现 DeepSeek 融资 73 亿美元(500 亿人民币)重大 CN AI 融资事件,显著强于原 #4
- **替换对象**:原 #4「职场工作中,遇到不会的内容,频繁使用AI」(published=2026-04-16,时效=1,数据硬度=1,mainstream_bias=6)
- **替换理由**:DeepSeek 融资事件时效=3、数据硬度=3、一手性≥2、无主流媒体 bias,信号强度明显更优
- **强化参考**:Jensen Huang 铜线光纤言论(百度热搜 742 万热度)作为 infra 补强线索,可入文内引述,不单列

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

### 1. Teaching Claude Why
- `topic_key`: `hn_frontpage_48066592_teaching_claude_why_20260509`
- `title`: `Teaching Claude Why`
- `primary_platform`: `Hacker News Frontpage`
- `published_at`: `2026-05-09 01:59:41 CST`
- `original_link`: `https://www.anthropic.com/research/teaching-claude-why`
- `score_total`: `25 / 30`
- `mainstream_bias_score`: `4`
- `blended_priority_score`: `29`
- `score_breakdown`: `一手性=2 / 传播性=3 / 破圈性=3 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=3 / 讨论度 / 争议度=3`
- `signal_summary`: `Hacker News RSS 抓到高热新条目。它适合作为 builder / startup / AI infra 话题的扩散入口,不是最终事实源。`
- `why_in_top20`: `partial source;有明确扩散热度入口;仍处业务窗内高时效;具备天然讨论空间;与 AI / Agent / 一人公司主线高度一致;更接近官方 / 主流媒体共识`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文;缺全文深抓,角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_062235__hn_frontpage_48066592_teaching_claude_why__source-packet.md`

---

### 2. 比宇树机器人更早上春晚的公司,要敲钟 IPO 了
- `topic_key`: `36kr_ai_ipo_20260509`
- `title`: `比宇树机器人更早上春晚的公司,要敲钟 IPO 了`
- `primary_platform`: `36氪 AI`
- `published_at`: `2026-05-08 23:09:08 CST`
- `original_link`: `https://www.36kr.com/p/3800408468959745`
- `score_total`: `22 / 30`
- `mainstream_bias_score`: `6`
- `blended_priority_score`: `28`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=3 / 赛道匹配=2 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=3 / 时效窗口=3 / 讨论度 / 争议度=1`
- `signal_summary`: `36氪 AI 当前页提取到近期条目"比宇树机器人更早上春晚的公司,要敲钟 IPO 了"。它适合作为官方更新、专家观察或中文传播层的单条入口,后续应回链原文继续核验。`
- `why_in_top20`: `partial source;仍处业务窗内高时效;更接近官方 / 主流媒体共识`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文;缺全文深抓,角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__36kr_ai_ipo__source-packet.md`

---

### 3. SK海力士因AI热潮发数百万元人均奖金,三星员工因待遇落差拟罢工,如何评价?反映了怎样的行业现状?
- `topic_key`: `zhihu_hot_ai_sk_ai_20260509`
- `title`: `SK海力士因AI热潮发数百万元人均奖金,三星员工因待遇落差拟罢工,如何评价?反映了怎样的行业现状?`
- `primary_platform`: `知乎热榜`
- `published_at`: `2026-05-07 21:04:39 CST`
- `original_link`: `https://www.zhihu.com/question/2035827414475993469`
- `score_total`: `21 / 30`
- `mainstream_bias_score`: `6`
- `blended_priority_score`: `27`
- `score_breakdown`: `一手性=1 / 传播性=3 / 破圈性=3 / 赛道匹配=2 / 可延展性=2 / 数据硬度=1 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度 / 争议度=3`
- `signal_summary`: `知乎热榜出现了 AI 相关问题"SK海力士因AI热潮发数百万元人均奖金,三星员工因待遇落差拟罢工,如何评价?反映了怎样的行业现状?"。 当前热度 160 万热度。它适合作为中文问答场域的破圈验证和用户疑问观察层。`
- `why_in_top20`: `有明确扩散热度入口;具备天然讨论空间;更接近官方 / 主流媒体共识`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文;缺全文深抓,角度延展需谨慎;硬数据偏少`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_215314__zhihu_hot_ai_sk_ai__source-packet.md`

---

### 4. 曝DeepSeek融资500亿元：梁文锋自掏四成，估值飙至3500亿
- `topic_key`: `wechat_jiqizhixin_deepseek_500_3500_20260509`
- `title`: `曝DeepSeek融资500亿元：梁文锋自掏四成，估值飙至3500亿`
- `primary_platform`: `微信 · 机器之心`
- `published_at`: `2026-05-09 10:58:23 CST`
- `original_link`: `https://mp.weixin.qq.com/s/468uA3g9RZCZEepuS_yp4g`
- `score_total`: `22 / 30`
- `mainstream_bias_score`: `2`
- `blended_priority_score`: `24`
- `score_breakdown`: `一手性=2 / 传播性=3 / 破圈性=3 / 赛道匹配=3 / 可延展性=3 / 数据硬度=3 / 视觉素材丰富度=1 / 平台适配潜力=2 / 时效窗口=3 / 讨论度 / 争议度=2`
- `signal_summary`: `DeepSeek启动73亿美元融资，刷新中国AI融资纪录。创始人梁文锋自掏腰包占四成，估值达3500亿人民币。机器之心 14:21 批次捕获，属于 manifest 窗口内新增一手线索。`
- `why_in_top20`: `partial source；业务窗 T 日新鲜捕获；重大 CN AI 融资事件；一手数据（金额 / 估值 / 出资比例）；自带讨论空间；与 AI / infra 主线高度一致`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `媒体稿入口，需回链公司官网或官方公告交叉验证；缺全文深抓，角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260509_142112__wechat_jiqizhixin_deepseek_500_3500__source-packet.md`

---

### 5. Running Codex safely at OpenAI
- `topic_key`: `openai_news_running_codex_safely_at_openai_20260509`
- `title`: `Running Codex safely at OpenAI`
- `primary_platform`: `OpenAI News`
- `published_at`: `2026-05-08 20:30:00 CST`
- `original_link`: `https://openai.com/index/running-codex-safely`
- `score_total`: `21 / 30`
- `mainstream_bias_score`: `4`
- `blended_priority_score`: `25`
- `score_breakdown`: `一手性=3 / 传播性=2 / 破圈性=1 / 赛道匹配=3 / 可延展性=1 / 数据硬度=3 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=3 / 讨论度 / 争议度=1`
- `signal_summary`: `OpenAI News RSS 抓到新条目。它属于官方一手源,适合判断模型、产品、API 和平台战略的真实变化。`
- `why_in_top20`: `yes source;仍处业务窗内高时效;与 AI / Agent / 一人公司主线高度一致;更接近官方 / 主流媒体共识`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `缺全文深抓,角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_062235__openai_news_running_codex_safely_at_openai__source-packet.md`

---

### 6. AI is breaking two vulnerability cultures
- `topic_key`: `hn_frontpage_48066524_ai_is_breaking_two_vulnerability_cultures_20260509`
- `title`: `AI is breaking two vulnerability cultures`
- `primary_platform`: `Hacker News Frontpage`
- `published_at`: `2026-05-09 01:55:08 CST`
- `original_link`: `https://www.jefftk.com/p/ai-is-breaking-two-vulnerability-cultures`
- `score_total`: `24 / 30`
- `mainstream_bias_score`: `0`
- `blended_priority_score`: `24`
- `score_breakdown`: `一手性=2 / 传播性=3 / 破圈性=3 / 赛道匹配=2 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=3 / 讨论度 / 争议度=3`
- `signal_summary`: `Hacker News RSS 抓到高热新条目。它适合作为 builder / startup / AI infra 话题的扩散入口,不是最终事实源。`
- `why_in_top20`: `partial source;有明确扩散热度入口;仍处业务窗内高时效;具备天然讨论空间`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文;缺全文深抓,角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_062235__hn_frontpage_48066524_ai_is_breaking_two_vulnerability_cultures__source-packet.md`

---

### 7. Agentic Search for Context Engineering - Leonie Monigatti, Elastic
- `topic_key`: `youtube_ai_dot_engineer_agentic_search_for_context_engineering_leonie_monigatti_elastic_20260509`
- `title`: `Agentic Search for Context Engineering - Leonie Monigatti, Elastic`
- `primary_platform`: `AI Engineer YouTube`
- `published_at`: `2026-05-08 21:05:06 CST`
- `original_link`: `https://www.youtube.com/watch?v=ynJyIKwjonM`
- `score_total`: `21 / 30`
- `mainstream_bias_score`: `0`
- `blended_priority_score`: `21`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=3 / 讨论度 / 争议度=1`
- `signal_summary`: `AI Engineer YouTube 频道页抓到新视频"Agentic Search for Context Engineering - Leonie Monigatti, Elastic"。Jina 频道快照现在可稳定保留标题、链接与相对发布时间,适合作为视频线索的硬成功入口。`
- `why_in_top20`: `partial source;仍处业务窗内高时效;与 AI / Agent / 一人公司主线高度一致`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文;缺全文深抓,角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_220432__youtube_ai_dot_engineer_agentic_search_for_context_engineering_leonie_monigatti_elastic__source-packet.md`

---

### 8. Taiwanese company Skymizer announces HTX301 - PCIE inference card with 384GB of Memory at ~240 Watts
- `topic_key`: `reddit_localllama_taiwanese_company_skymizer_announces_htx301_pcie_inference_card_with_384_20260509`
- `title`: `Taiwanese company Skymizer announces HTX301 - PCIE inference card with 384GB of Memory at ~240 Watts`
- `primary_platform`: `Reddit / LocalLLaMA Daily Top`
- `published_at`: `2026-05-08 09:36:22 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1t6tvfw/taiwanese_company_skymizer_announces_htx301_pcie/`
- `score_total`: `21 / 30`
- `mainstream_bias_score`: `-3`
- `blended_priority_score`: `18`
- `score_breakdown`: `一手性=1 / 传播性=3 / 破圈性=3 / 赛道匹配=2 / 可延展性=2 / 数据硬度=1 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度 / 争议度=3`
- `signal_summary`: `Reddit / r/LocalLLaMA 的日榜 RSS 收录了"Taiwanese company Skymizer announces HTX301 - PCIE inference card with 384GB of Memory at ~240 Watts",当前位于本轮抓取顺序第 4 位。它更适合判断真实用户问题、真实体验和外部对象入口,不适合直接当正式事实证据。`
- `why_in_top20`: `有明确扩散热度入口;具备天然讨论空间`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文;缺全文深抓,角度延展需谨慎;硬数据偏少`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_215154__reddit_localllama_taiwanese_company_skymizer_announces_htx301_pcie_inference_card_with_384__source-packet.md`

---

### 9. 中共中央政治局会议指出,加强水网、新型电网、算力网、新一代通信网、物流网等规划建设,释放哪些信息?
- `topic_key`: `zhihu_hot_ai_zhihu_hot_20260509`
- `title`: `中共中央政治局会议指出,加强水网、新型电网、算力网、新一代通信网、物流网等规划建设,释放哪些信息?`
- `primary_platform`: `知乎热榜`
- `published_at`: `2026-04-28 13:52:16 CST`
- `original_link`: `https://www.zhihu.com/question/2032457112991871100`
- `score_total`: `20 / 30`
- `mainstream_bias_score`: `6`
- `blended_priority_score`: `26`
- `score_breakdown`: `一手性=1 / 传播性=3 / 破圈性=3 / 赛道匹配=2 / 可延展性=2 / 数据硬度=1 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=1 / 讨论度 / 争议度=3`
- `signal_summary`: `知乎热榜出现了 AI 相关问题"中共中央政治局会议指出,加强水网、新型电网、算力网、新一代通信网、物流网等规划建设,释放哪些信息?"。 当前热度 103 万热度。它适合作为中文问答场域的破圈验证和用户疑问观察层。`
- `why_in_top20`: `有明确扩散热度入口;具备天然讨论空间;更接近官方 / 主流媒体共识`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文;缺全文深抓,角度延展需谨慎;硬数据偏少`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_062235__zhihu_hot_ai_zhihu_hot__source-packet.md`

---

### 10. RTX306012GB 显卡将于 6 月复产、7 月开卖,它在当前市场还有竞争力吗?
- `topic_key`: `zhihu_hot_ai_rtx306012gb_6_7_20260509`
- `title`: `RTX306012GB 显卡将于 6 月复产、7 月开卖,它在当前市场还有竞争力吗?`
- `primary_platform`: `知乎热榜`
- `published_at`: `2026-05-05 00:03:40 CST`
- `original_link`: `https://www.zhihu.com/question/2034785301671960934`
- `score_total`: `20 / 30`
- `mainstream_bias_score`: `6`
- `blended_priority_score`: `26`
- `score_breakdown`: `一手性=1 / 传播性=3 / 破圈性=3 / 赛道匹配=2 / 可延展性=2 / 数据硬度=1 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=1 / 讨论度 / 争议度=3`
- `signal_summary`: `知乎热榜出现了 AI 相关问题"RTX306012GB 显卡将于 6 月复产、7 月开卖,它在当前市场还有竞争力吗?"。 当前热度 59 万热度。它适合作为中文问答场域的破圈验证和用户疑问观察层。`
- `why_in_top20`: `有明确扩散热度入口;具备天然讨论空间;更接近官方 / 主流媒体共识`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文;缺全文深抓,角度延展需谨慎;硬数据偏少`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_061915__zhihu_hot_ai_rtx306012gb_6_7__source-packet.md`

---

### 11. DeepSeek降价背后:Token生意在重新洗牌
- `topic_key`: `36kr_ai_deepseek_token_20260509`
- `title`: `DeepSeek降价背后:Token生意在重新洗牌`
- `primary_platform`: `36氪 AI`
- `published_at`: `2026-05-08 23:09:08 CST`
- `original_link`: `https://www.36kr.com/p/3800580452080647`
- `score_total`: `19 / 30`
- `mainstream_bias_score`: `6`
- `blended_priority_score`: `25`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=1 / 赛道匹配=2 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=3 / 讨论度 / 争议度=1`
- `signal_summary`: `36氪 AI 当前页提取到近期条目"DeepSeek降价背后:Token生意在重新洗牌"。它适合作为官方更新、专家观察或中文传播层的单条入口,后续应回链原文继续核验。`
- `why_in_top20`: `partial source;仍处业务窗内高时效;更接近官方 / 主流媒体共识`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文;缺全文深抓,角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__36kr_ai_deepseek_token__source-packet.md`

---

### 12. See what happens when creative legends use AI to make ads for small businesses.
- `topic_key`: `google_blog_ai_see_what_happens_when_creative_legends_use_ai_to_make_ads_for_small_busi_20260509`
- `title`: `See what happens when creative legends use AI to make ads for small businesses.`
- `primary_platform`: `Google AI Blog`
- `published_at`: `2026-05-08 23:00:00 CST`
- `original_link`: `https://blog.google/company-news/inside-google/company-announcements/the-small-brief/`
- `score_total`: `20 / 30`
- `mainstream_bias_score`: `4`
- `blended_priority_score`: `24`
- `score_breakdown`: `一手性=3 / 传播性=2 / 破圈性=1 / 赛道匹配=2 / 可延展性=1 / 数据硬度=3 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=3 / 讨论度 / 争议度=1`
- `signal_summary`: `Google AI Blog RSS 抓到新条目。它属于官方一手源,适合判断 Google AI 平台层和产品层的真实变化。`
- `why_in_top20`: `yes source;仍处业务窗内高时效;更接近官方 / 主流媒体共识`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `缺全文深抓,角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_062235__google_blog_ai_see_what_happens_when_creative_legends_use_ai_to_make_ads_for_small_busi__source-packet.md`

---

### 13. Scaling Trusted Access for Cyber with GPT-5.5 and GPT-5.5-Cyber
- `topic_key`: `openai_news_scaling_trusted_access_for_cyber_with_gpt_5_5_and_gpt_5_5_cyber_20260509`
- `title`: `Scaling Trusted Access for Cyber with GPT-5.5 and GPT-5.5-Cyber`
- `primary_platform`: `OpenAI News`
- `published_at`: `2026-05-07 21:00:00 CST`
- `original_link`: `https://openai.com/index/gpt-5-5-with-trusted-access-for-cyber`
- `score_total`: `20 / 30`
- `mainstream_bias_score`: `4`
- `blended_priority_score`: `24`
- `score_breakdown`: `一手性=3 / 传播性=2 / 破圈性=1 / 赛道匹配=3 / 可延展性=1 / 数据硬度=3 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度 / 争议度=1`
- `signal_summary`: `OpenAI News RSS 抓到新条目。它属于官方一手源,适合判断模型、产品、API 和平台战略的真实变化。`
- `why_in_top20`: `yes source;与 AI / Agent / 一人公司主线高度一致;更接近官方 / 主流媒体共识`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `缺全文深抓,角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_061915__openai_news_scaling_trusted_access_for_cyber_with_gpt_5_5_and_gpt_5_5_cyber__source-packet.md`

---

### 14. Parloa builds service agents customers want to talk to
- `topic_key`: `openai_news_parloa_builds_service_agents_customers_want_to_talk_to_20260509`
- `title`: `Parloa builds service agents customers want to talk to`
- `primary_platform`: `OpenAI News`
- `published_at`: `2026-05-07 19:00:00 CST`
- `original_link`: `https://openai.com/index/parloa`
- `score_total`: `20 / 30`
- `mainstream_bias_score`: `4`
- `blended_priority_score`: `24`
- `score_breakdown`: `一手性=3 / 传播性=2 / 破圈性=1 / 赛道匹配=3 / 可延展性=1 / 数据硬度=3 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度 / 争议度=1`
- `signal_summary`: `OpenAI News RSS 抓到新条目。它属于官方一手源,适合判断模型、产品、API 和平台战略的真实变化。`
- `why_in_top20`: `yes source;与 AI / Agent / 一人公司主线高度一致;更接近官方 / 主流媒体共识`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `缺全文深抓,角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_061915__openai_news_parloa_builds_service_agents_customers_want_to_talk_to__source-packet.md`

---

### 15. Advancing voice intelligence with new models in the API
- `topic_key`: `openai_news_advancing_voice_intelligence_with_new_models_in_the_api_20260509`
- `title`: `Advancing voice intelligence with new models in the API`
- `primary_platform`: `OpenAI News`
- `published_at`: `2026-05-07 18:00:00 CST`
- `original_link`: `https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api`
- `score_total`: `20 / 30`
- `mainstream_bias_score`: `4`
- `blended_priority_score`: `24`
- `score_breakdown`: `一手性=3 / 传播性=2 / 破圈性=1 / 赛道匹配=3 / 可延展性=1 / 数据硬度=3 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度 / 争议度=1`
- `signal_summary`: `OpenAI News RSS 抓到新条目。它属于官方一手源,适合判断模型、产品、API 和平台战略的真实变化。`
- `why_in_top20`: `yes source;与 AI / Agent / 一人公司主线高度一致;更接近官方 / 主流媒体共识`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `缺全文深抓,角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_061915__openai_news_advancing_voice_intelligence_with_new_models_in_the_api__source-packet.md`

---

### 16. CVPR 2026 Highlight
- `topic_key`: `jiqizhixin_site_cvpr_2026_highlight_20260509`
- `title`: `CVPR 2026 Highlight`
- `primary_platform`: `机器之心官网`
- `published_at`: `unknown`
- `original_link`: `https://www.jiqizhixin.com/`
- `score_total`: `19 / 30`
- `mainstream_bias_score`: `5`
- `blended_priority_score`: `24`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=2 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=1 / 时效窗口=3 / 讨论度 / 争议度=1`
- `signal_summary`: `机器之心官网 当前页提取到近期条目"CVPR 2026 Highlight"。它适合作为官方更新、专家观察或中文传播层的单条入口,后续应回链原文继续核验。`
- `why_in_top20`: `partial source;仍处业务窗内高时效;更接近官方 / 主流媒体共识`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文;发布时间不够硬;缺全文深抓,角度延展需谨慎;题目偏技术,泛流量平台适配有限`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__jiqizhixin_site_cvpr_2026_highlight__source-packet.md`

---

### 17. Partial Evidence Bench: Benchmarking Authorization-Limited Evidence in Agentic Systems
- `topic_key`: `arxiv_cs_ai_partial_evidence_bench_benchmarking_authorization_limited_evidence_in_ag_20260509`
- `title`: `Partial Evidence Bench: Benchmarking Authorization-Limited Evidence in Agentic Systems`
- `primary_platform`: `arXiv cs.AI recent`
- `published_at`: `2026-05-08 12:00:00 CST`
- `original_link`: `https://arxiv.org/abs/2605.05379`
- `score_total`: `23 / 30`
- `mainstream_bias_score`: `0`
- `blended_priority_score`: `23`
- `score_breakdown`: `一手性=3 / 传播性=1 / 破圈性=3 / 赛道匹配=3 / 可延展性=2 / 数据硬度=3 / 视觉素材丰富度=2 / 平台适配潜力=1 / 时效窗口=2 / 讨论度 / 争议度=3`
- `signal_summary`: `arXiv cs.AI RSS 抓到最新论文条目。它是研究前沿的原始入口,适合作为方法和方向变化的早期信号层。`
- `why_in_top20`: `yes source;有明确扩散热度入口;具备天然讨论空间;与 AI / Agent / 一人公司主线高度一致`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `缺全文深抓,角度延展需谨慎;题目偏技术,泛流量平台适配有限`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_061915__arxiv_cs_ai_partial_evidence_bench_benchmarking_authorization_limited_evidence_in_ag__source-packet.md`

---

### 18. AI新媒体影响力排行榜|第 23 期
- `topic_key`: `newrank_ai_media_rank_ai_23_20260509`
- `title`: `AI新媒体影响力排行榜|第 23 期`
- `primary_platform`: `新榜 AI 新媒体影响力排行榜`
- `published_at`: `2025-05-14`
- `original_link`: `https://www.newrank.cn/public/info/rank_detail.html?name=ai`
- `score_total`: `22 / 30`
- `mainstream_bias_score`: `1`
- `blended_priority_score`: `23`
- `score_breakdown`: `一手性=1 / 传播性=3 / 破圈性=3 / 赛道匹配=2 / 可延展性=2 / 数据硬度=1 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=3 / 讨论度 / 争议度=3`
- `signal_summary`: `新榜返回了"AI新媒体影响力排行榜"的第 23 期记录,发布时间 2025-05-14。它更适合作为 AI 垂类账号势能与平台传播格局的月度验证层。`
- `why_in_top20`: `有明确扩散热度入口;仍处业务窗内高时效;具备天然讨论空间`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文;缺全文深抓,角度延展需谨慎;硬数据偏少`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_061915__newrank_ai_media_rank_ai_23__source-packet.md`

---

### 19. OpenAI Introduces Websocket Based Execution Mode to Reduce Latency in Agentic Workflows
- `topic_key`: `infoq_ai_ml_openai_introduces_websocket_based_execution_mode_to_reduce_latency_in_ag_20260509`
- `title`: `OpenAI Introduces Websocket Based Execution Mode to Reduce Latency in Agentic Workflows`
- `primary_platform`: `InfoQ AI/ML`
- `published_at`: `unknown`
- `original_link`: `https://www.infoq.com/news/2026/05/openai-websocket-responses-api/?topicPageSponsorship=9a722a12-440a-46f9-bbdf-d86d1fc4f6d2`
- `score_total`: `20 / 30`
- `mainstream_bias_score`: `3`
- `blended_priority_score`: `23`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=1 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=3 / 讨论度 / 争议度=1`
- `signal_summary`: `InfoQ AI/ML 当前页提取到近期条目"OpenAI Introduces Websocket Based Execution Mode to Reduce Latency in Agentic Workflows"。它适合作为官方更新、专家观察或中文传播层的单条入口,后续应回链原文继续核验。`
- `why_in_top20`: `partial source;仍处业务窗内高时效;与 AI / Agent / 一人公司主线高度一致`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文;发布时间不够硬;缺全文深抓,角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__infoq_ai_ml_openai_introduces_websocket_based_execution_mode_to_reduce_latency_in_ag__source-packet.md`

---

### 20. Google New TPU Generation is Specifically Designed for Agents and SOTA Model Training
- `topic_key`: `infoq_ai_ml_google_new_tpu_generation_is_specifically_designed_for_agents_and_sota_m_20260509`
- `title`: `Google New TPU Generation is Specifically Designed for Agents and SOTA Model Training`
- `primary_platform`: `InfoQ AI/ML`
- `published_at`: `unknown`
- `original_link`: `https://www.infoq.com/news/2026/05/google-8th-tpu-generation/?topicPageSponsorship=9a722a12-440a-46f9-bbdf-d86d1fc4f6d2`
- `score_total`: `20 / 30`
- `mainstream_bias_score`: `3`
- `blended_priority_score`: `23`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=1 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=3 / 讨论度 / 争议度=1`
- `signal_summary`: `InfoQ AI/ML 当前页提取到近期条目"Google New TPU Generation is Specifically Designed for Agents and SOTA Model Training"。它适合作为官方更新、专家观察或中文传播层的单条入口,后续应回链原文继续核验。`
- `why_in_top20`: `partial source;仍处业务窗内高时效;与 AI / Agent / 一人公司主线高度一致`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `正式引用前仍需补一手或原始上下文;发布时间不够硬;缺全文深抓,角度延展需谨慎`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__infoq_ai_ml_google_new_tpu_generation_is_specifically_designed_for_agents_and_sota_m__source-packet.md`

---

### 21. 黄仁勋:铜线已无法满足需求(百度热搜)
- `topic_key`: `baidu_realtime_20260509_huang_copper`
- `title`: `黄仁勋:铜线已无法满足需求`
- `primary_platform`: `百度热搜`
- `published_at`: `2026-05-09`
- `original_link`: `https://top.baidu.com/board?tab=realtime`
- `score_total`: `19 / 30`
- `mainstream_bias_score`: `7`
- `blended_priority_score`: `26`
- `score_breakdown`: `一手性=1 / 传播性=3 / 破圈性=3 / 赛道匹配=3 / 可延展性=3 / 数据硬度=1 / 视觉素材丰富度=1 / 平台适配潜力=3 / 时效窗口=3 / 讨论度/争议度=2`
- `signal_summary`: `百度热搜出现英伟达 CEO 黄仁勋关于 AI 基础设施光学连接的采访话题,热指 7,428,520。本条仅作为破圈验证信号,不作为事实来源。`
- `why_in_top20`: `百度热搜 742 万热指,直接关联 AI 基础设施 / 机器人供应链(光学连接)话题;中文大众破圈明确;需补原始采访稿`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `热搜只能证明传播,不证明事实强度;需回链英伟达官方采访稿补硬数据`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260509_122824__baidu_realtime_baidu_hot__source-packet.md`

---

### 22. AI算力的下一个瓶颈来了(百度热搜)
- `topic_key`: `baidu_realtime_20260509_ai_compute_bottleneck`
- `title`: `AI算力的下一个瓶颈来了`
- `primary_platform`: `百度热搜`
- `published_at`: `2026-05-09`
- `original_link`: `https://top.baidu.com/board?tab=realtime`
- `score_total`: `18 / 30`
- `mainstream_bias_score`: `7`
- `blended_priority_score`: `25`
- `score_breakdown`: `一手性=1 / 传播性=3 / 破圈性=3 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=1 / 平台适配潜力=3 / 时效窗口=3 / 讨论度/争议度=1`
- `signal_summary`: `百度热搜出现 AI 算力瓶颈话题,热指 4,004,631;摘要明文提到 Agent(智能体)是驱动算力需求的关键应用。本条仅作为破圈验证信号,不作为事实来源。`
- `why_in_top20`: `百度热搜 400 万热指;财报硬数据(Intel/AMD/Arm);明文出现 Agent;中文大众破圈明确;需补原始财报电话会稿`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `热搜只能证明传播;摘要提到 Agent 需补原始财报或官方稿确认`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260509_122824__baidu_realtime_ai__source-packet.md`

---

### 23. 为什么 MiniMax 大模型无法识别马嘉祺是谁?(知乎热榜)
- `topic_key`: `zhihu_hot_20260509_minimax_majiaqi`
- `title`: `为什么 MiniMax 大模型无法识别马嘉祺是谁?`
- `primary_platform`: `知乎热榜`
- `published_at`: `2026-03-17`(热榜记录日期)
- `original_link`: `https://www.zhihu.com/question/2017049686331127666`
- `score_total`: `15 / 30`
- `mainstream_bias_score`: `5`
- `blended_priority_score`: `20`
- `score_breakdown`: `一手性=1 / 传播性=2 / 破圈性=2 / 赛道匹配=2 / 可延展性=3 / 数据硬度=1 / 视觉素材丰富度=1 / 平台适配潜力=3 / 时效窗口=2 / 讨论度/争议度=3`
- `signal_summary`: `知乎热榜出现 MiniMax 大模型能力边界问题,370 万热度 / 49 回答 / 287 关注。反映普通用户对 AI 模型局限性的好奇心。本条仅作为问答场域破圈验证信号,不作为事实来源。`
- `why_in_top20`: `知乎 370 万热度;中国大模型厂商 MiniMax 用户疑问具代表性;问答形式天然适合微信改写;补 MiniMax 官方技术说明后可升级为硬选题`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `热榜只能证明讨论热度,不证明事实强度;需补 MiniMax 官方回应或技术博客确认为案例而非误解`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260509_122824__zhihu_hot_ai_minimax__source-packet.md`

---

## 结论

### top3_must_watch

| 排名 | topic_key | 理由 |
|---|---|---|
| #1 | `hn_frontpage_48066592_teaching_claude_why_20260509` | 高时效 / 强扩散 / 主线高度匹配 |
| #2 | `36kr_ai_ipo_20260509` | 高时效 |
| #3 | `zhihu_hot_ai_sk_ai_20260509` | 强扩散 |

### top6_strong_pool

| 排名 | topic_key | 理由 |
|---|---|---|
| #4 | `zhihu_hot_ai_ai_20260509` | 有明确扩散热度入口;具备天然讨论空间;更接近官方 / 主流媒体共识 |
| #5 | `openai_news_running_codex_safely_at_openai_20260509` | yes source;仍处业务窗内高时效;与 AI / Agent / 一人公司主线高度一致;更接近官方 / 主流媒体共识 |
| #6 | `hn_frontpage_48066524_ai_is_breaking_two_vulnerability_cultures_20260509` | partial source;有明确扩散热度入口;仍处业务窗内高时效;具备天然讨论空间 |
| #7 | `youtube_ai_dot_engineer_agentic_search_for_context_engineering_leonie_monigatti_elastic_20260509` | partial source;仍处业务窗内高时效;与 AI / Agent / 一人公司主线高度一致 |
| #8 | `reddit_localllama_taiwanese_company_skymizer_announces_htx301_pcie_inference_card_with_384_20260509` | 有明确扩散热度入口;具备天然讨论空间 |
| #9 | `zhihu_hot_ai_zhihu_hot_20260509` | 有明确扩散热度入口;具备天然讨论空间;更接近官方 / 主流媒体共识 |

### holdout_watchlist

| topic_key | holdout 原因 |
|---|---|
| `infoq_ai_ml_cloudflare_launches_artifacts_beta_introducing_git_like_versioning_for_a_20260509` | 正式引用前仍需补一手或原始上下文;发布时间不够硬;缺全文深抓,角度延展需谨慎 |
| `github_trending_hkuds_ai_trader_20260509` | 正式引用前仍需补一手或原始上下文;缺全文深抓,角度延展需谨慎 |
| `github_trending_decolua_9router_20260509` | 正式引用前仍需补一手或原始上下文;缺全文深抓,角度延展需谨慎 |

### supply_risk

- `kept_candidates`: `23`(含 3 条 heat_validation lane 新增候选)
- `manifest_source_packets`: `139`
- `manifest_deep_articles`: `4`
- `excluded_recent_duplicates`: `0`
- `excluded_low_fit`: `5`
- `notes`: `本包由脚本预物化生成,确保 day_mainline 不会停留在模板壳;若要冲 premium,需要后续岗位继续补证、重排、改角度。heat_validation lane 新增 3 条大众破圈信号,待补原始来源后可升级为正式选题。`

## 本包交付约束

- **不得自行放行**:本包为 `market-scout` 初筛交付,是否进入下一工序由 `market-editor` 最新 scorecard 决定。

---

## 附录:业务窗关门后补充条目(14:21 CST 补入)

> 以下条目在 Top20 初筛包生成后(06:54 CST)、业务窗关闭前(14:30 CST)被捕获。按有限强化规则补入,不替换原有 23 条,仅作标注供下游 filter 参考。

### A1. 曝DeepSeek融资500亿元:梁文锋自掏四成,估值飙至3500亿
- `topic_key`: `wechat_jiqizhixin_deepseek_500_3500_20260509`
- `title`: `曝DeepSeek融资500亿元:梁文锋自掏四成,估值飙至3500亿`
- `primary_platform`: `机器之心 WeChat`
- `published_at`: `2026-05-09 10:58:23 CST`
- `original_link`: `https://mp.weixin.qq.com/s/468uA3g9RZCZEepuS_yp4g`
- `score_total`: `25 / 30`
- `mainstream_bias_score`: `5`
- `blended_priority_score`: `30`
- `score_breakdown`: `一手性=2 / 传播性=3 / 破圈性=3 / 赛道匹配=3 / 可延展性=2 / 数据硬度=3 / 视觉素材丰富度=2 / 平台适配潜力=3 / 时效窗口=3 / 讨论度 / 争议度=1`
- `signal_summary`: `机器之心微信RSS在14:21补捕获。DeepSeek启动73亿美元(约500亿元)融资,估值3500亿元,梁文锋自掏四成。`
- `why_appendix`: `新;强;官方融资数字;高估值节点;AIinfra主线;与topic-planner协同`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `微信媒体稿,需交叉验证官方公告`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260509_142112__wechat_jiqizhixin_deepseek_500_3500__source-packet.md`

### A2. VLA的PyTorch时刻已至!港科大联手社区开源StarVLA
- `topic_key`: `wechat_jiqizhixin_starvla_vla_20260509`
- `title`: `VLA的PyTorch时刻已至!港科大联手社区开源StarVLA:一个框架揭秘所有主流VLA`
- `primary_platform`: `机器之心 WeChat`
- `published_at`: `2026-05-09 10:58:23 CST`
- `original_link`: `https://mp.weixin.qq.com/s/xb9DKivxlMV7LTsuqFXelg`
- `score_total`: `22 / 30`
- `mainstream_bias_score`: `4`
- `blended_priority_score`: `26`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=3 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=3 / 讨论度 / 争议度=1`
- `signal_summary`: `港科大联合社区开源StarVLA,一个框架统一主流VLA模型。技术门槛清晰,有开源repo和论文锚点。`
- `why_appendix`: `新;技术开源;有GitHub锚点;港科大背书;VLA/具身赛道`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `需找GitHub repo确认项目状态`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260509_142112__wechat_jiqizhixin_vla_pytorch_starvla_vla__source-packet.md`

### A3. 价值模型不是没用,是架构不对!生成式Critic重新定义LLM强化学习信用分配
- `topic_key`: `wechat_jiqizhixin_critic_llm_20260509`
- `title`: `价值模型不是没用,是架构不对!生成式Critic重新定义LLM强化学习信用分配`
- `primary_platform`: `机器之心 WeChat`
- `published_at`: `2026-05-09 10:58:23 CST`
- `original_link`: `https://mp.weixin.qq.com/s/468uA3g9RZCZEepuS_yp4g`
- `score_total`: `20 / 30`
- `mainstream_bias_score`: `3`
- `blended_priority_score`: `23`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材丰富度=1 / 平台适配潜力=2 / 时效窗口=3 / 讨论度 / 争议度=1`
- `signal_summary`: `生成式Critic新架构,重新定义LLM强化学习信用分配。偏技术方向,适合对标论文改写。`
- `why_appendix`: `新;技术论文方向;LLM/强化学习赛道;适合拆解稿`
- `risks`: `偏学术,需配合原论文才能写扎实`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260509_142112__wechat_jiqizhixin_critic_llm__source-packet.md`

### A4. 活久见,时代少年团给大模型上了一课
- `topic_key`: `wechat_jiqizhixin_shidai_shaotuan_20260509`
- `title`: `活久见,时代少年团给大模型上了一课`
- `primary_platform`: `机器之心 WeChat`
- `published_at`: `2026-05-09 10:58:23 CST`
- `original_link`: `https://mp.weixin.qq.com/s/l_kamgxcufha_yNgwkQWQ`
- `score_total`: `17 / 30`
- `mainstream_bias_score`: `5`
- `blended_priority_score`: `22`
- `score_breakdown`: `一手性=1 / 传播性=3 / 破圈性=3 / 赛道匹配=1 / 可延展性=1 / 数据硬度=1 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度 / 争议度=2`
- `signal_summary`: `机器之心蹭热点文章,时代少年团×大模型话题。娱乐破圈,但赛道匹配度低,不建议深追。`
- `why_appendix`: `仅供平台适配评估,不建议作为主推候选`
- `risks`: `泛娱乐内容,赛道匹配弱`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260509_142112__wechat_jiqizhixin_https_mp_weixin_qq_com_s_l_kamgxcufha_yyngwkqwq__source-packet.md`

### A5. New Compute Partnership with Anthropic(xAI × Anthropic 算力合作)
- `topic_key`: `xai_news_anthropic_compute_partnership_20260509`
- `title`: `New Compute Partnership with Anthropic`
- `primary_platform`: `xAI News`
- `published_at`: `2026-05-09 (page-level, exact time unspecified)`
- `original_link`: `https://x.ai/news/anthropic-compute-partnership`
- `score_total`: `22 / 30`
- `mainstream_bias_score`: `3`
- `blended_priority_score`: `25`
- `score_breakdown`: `一手性=3 / 传播性=2 / 破圈性=3 / 赛道匹配=3 / 可延展性=2 / 数据硬度=3 / 视觉素材丰富度=1 / 平台适配潜力=2 / 时效窗口=3 / 讨论度 / 争议度=1`
- `signal_summary`: `xAI 宣布与 Anthropic 建立新算力合作伙伴关系,SpaceXAI 已签署协议向 Anthropic 提供 Colossus 1 算力。这是跨大模型平台的首次大规模算力供给合作,具有重要行业信号意义。`
- `why_appendix`: `一手官方源;跨平台重大合作;Grok × Claude 首次算力互联;行业标志性事件`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `需回链 x.ai 单篇原文补全文;合作细节(算力规模、期限)待披露`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260509_090524__xai_news_new_compute_partnership_with_anthropic__source-packet.md`

### A6. 豆包要收费了:三档订阅最贵500元/月,保留免费基础版
- `topic_key`: `wechat_geekpark_douyin_500_20260509`
- `title`: `豆包要收费了:三档订阅最贵500元/月,保留免费基础版`
- `primary_platform`: `极客公园 WeChat`
- `published_at`: `2026-05-08`
- `original_link`: `https://mp.weixin.qq.com/s/???`
- `score_total`: `21 / 30`
- `mainstream_bias_score`: `5`
- `blended_priority_score`: `26`
- `score_breakdown`: `一手性=2 / 传播性=3 / 破圈性=2 / 赛道匹配=2 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=3 / 时效窗口=2 / 讨论度 / 争议度=2`
- `signal_summary`: `字节豆包宣布付费订阅计划,三档最贵500元/月,是中国 AI C端产品的首个规模化收费尝试。`
- `why_appendix`: `中国AI产品首个规模化付费信号;C端商业化里程碑;对比 ChatGPT/Claude 订阅体系`
- `visual_assets`: `source packet 已探测原始视觉输入`
- `risks`: `需补官方定价公告原始链接;具体档位和功能差异待确认`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_061915__wechat_geekpark_500_ai_40__source-packet.md`

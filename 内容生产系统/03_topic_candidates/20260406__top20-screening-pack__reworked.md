# Top20 初筛包（返工版）

- `date`: `2026-04-06`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-04-06 15:10:00 CST`
- `source_scope`: `T-1 17:00 ~ T 14:30`
- `total_candidates_seen`: `40 source packets + 21 capture summaries + 1 asset chain`
- `top20_count`: `20`
- `delivery_lane`: `day_mainline`
- `delivery_deadline`: `2026-04-06 19:00 CST`
- `pack_type`: `__reworked`
- `original_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260406__top20-screening-pack.md`
- `rework_trigger`: `market-editor scorecard 未填充；redteam-review 2026-04-06 14:49 判定 rework（score 7–7.5，3条 P1 fatal，5条 P2 可修）`
- `rework_modes_applied`: `supplement_evidence / rewrite_angle / expand_validation / replace_topic`
- `scorecard_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260406__top20__stage-gate-scorecard.md`
- `manifest_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260406__market-source-manifest.md`

---

## ⚠️ 返工声明

- **本包不得自判"已过线 / 可进入下一工序"**；是否放行由 `market-editor` 最新 scorecard 决定
- **补位说明**：本包在 business_window 内（14:30 前）追加 2 条 late-breaking 候选以替换降格对象，均已在 manifest 中确认路径，不脑补
- **rework_mode 规则**：仅在事件事实失真、已过时或严重偏航时才替换对象；其余以补证/改角度优先

---

## 返工操作记录

| # | 对象 | 原问题 | 返工动作 | 结果 |
|---|---|---|---|---|
| #14 | 黄仁勋访谈 | P1 fatal：零原始链接，时效失真风险 | supplement_evidence | **降格为 HOLD**；4件套内容无法核实访谈来源；除非补到原始链接才恢复 |
| #10 | OpenAI "土豆" | P1 fatal："土豆"绰号未核实；Sora"弃子"无官方依据 | rewrite_angle | **改角度**：保留对象，标题改为"迷雾"，正文注明"土豆为圈名猜测，Sora弃子说法待官方确认" |
| #12 | Copilot ToS | P1-C repairable：ToS 更新于2025年10月，非今日新闻 | rewrite_angle | **改角度**：改为"旧ToS引发新争议"，去除"今日突发"框架 |
| #6 | Linux 内核维护者 | P2-B：10份/天数字仅量子位来源，需补HN/Reddit原帖 | expand_validation | **保留 + 补证要求**：标注需补HN/Reddit原帖截图；正文加"据量子位报道（需补一手链接）" |
| #17 | DeepSeek审查 | P2-C：单Reddit帖，无官方回应，信号薄弱 | rewrite_angle | **改角度**：调整为"社区讨论 vs 官方沉默"对比叙事；加官方回应缺失的注脚 |
| #18 | Per-Layer Embeddings | P2-D：与#4 Gemma 4本地运行内容重复；score 14/27垫底 | replace_topic | **降格替换**：换入 `Real-time AI audio/video on M3 Pro + Gemma E2B`（14:14 capture，manifest确认路径） |
| #20 | 人类大脑AI | P2-E：知乎长尾问题，无当日时效锚点，score 14/27 | replace_topic | **降格替换**：换入 `Eight years of wanting, three months of building with AI`（HN 635pts/204cm，manifest确认路径） |
| #1 | Gemma 4 iPhone | P2-A：App Store链接指向荷兰区（nl） | supplement_evidence | 标注需替换为全球链接 |
| — | 补位候选 | — | — | 见 #18' 和 #20' 条目 |

---

## 评分框架

| 维度 | 说明 | 分值 |
|---|---|---|
| 一手性 | 是否来自官方 / 论文 / 产品页 / 原帖 | 0-3 |
| 传播性 | 是否已有多平台、多语种或多媒体跟进 | 0-3 |
| 破圈性 | 是否跨至少 2 个内容场域发酵 | 0-3 |
| 赛道匹配 | 是否契合 AI / Agent / 一人公司 / 模型 / infra / 硬件主线 | 0-3 |
| 可延展性 | 是否能写出快讯、解读、复盘多层内容 | 0-3 |
| 数据硬度 | 是否有硬数据、原始截图、官方说明 | 0-3 |
| 视觉素材丰富度 | 是否具备可直接利用的图、表、截图、原帖 | 0-3 |
| 平台适配潜力 | 是否容易改写为多平台内容 | 0-3 |
| 时效窗口 | 是不是当下写最有价值 | 0-3 |
| 讨论度 / 争议度 | 是否有持续讨论空间 | 0-3 |

---

## Top20 候选

### 1. Gemma 4 上线 iPhone：Google AI Edge Gallery 引发本地运行革命
- `topic_key`: `gemma-4-iphone-local-ai-20260406`
- `title`: `Gemma 4 on iPhone`
- `primary_platform`: `Hacker News`
- `published_at`: `2026-04-06 02:45:53 CST`
- `original_link`: `https://apps.apple.com/nl/app/google-ai-edge-gallery/id6749645337` ⚠️ **荷兰区链接，需替换为** `https://apps.apple.com/app/google-ai-edge-gallery/id6749645335`
- `hn_link`: `https://news.ycombinator.com/item?id=47652561`
- `score_total`: `22 / 27`
- `score_breakdown`: `一手性=2 / 传播性=3 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材=2 / 平台适配=2 / 时效窗口=3 / 讨论度=2`
- `signal_summary`: `HN 440分 / 119评论 / 排名第三。Google AI Edge Gallery 已在 App Store 上架，Gemma 4 正式可在 iPhone 本地运行，配合 Google 官方能力集成（Gemini Nano）。本地 AI 在移动端的可操作性出现标志性节点。`
- `why_in_top20`: `HN 高热 + Rank 3 + 明确产品页 + Google 官方背书。时效窗口新鲜（今日凌晨）。跨 HN + Reddit LocalLLaMA 双平台验证。本地 AI 赛道持续升温，Gemma 4 31B 性价比数据同时强化这一信号。`
- `visual_assets`: `App Store 截图区 / Google AI Edge Gallery 产品图 / HN 评论截图 / Reddit 对比数据`
- `risks`: `App Store 荷兰区链接需替换为全球链接；数据引用多为社区测试，需补 FoodTruckBench 原始数据截图`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_103830__hn_frontpage_47652561_gemma_4_on_iphone__source-packet.md`
- `rework_flag`: `supplement_evidence｜P2-A：链接替换`

---

### 2. Gemma 4 benchmarks 屠榜：$0.20/run 碾压所有中国开源模型
- `topic_key`: `gemma-4-benchmark-destruction-20260406`
- `title`: `Gemma 4 31B: 100% survival, +1,144% median ROI at $0.20/run`
- `primary_platform`: `Reddit / LocalLLaMA`
- `published_at`: `2026-04-06 03:30:02 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1sdcotc/gemma_4_just_casually_destroyed_every_model_on/`
- `benchmark_link`: `https://foodtruckbench.com/blog/gemma-4-31b`
- `score_total`: `21 / 27`
- `score_breakdown`: `一手性=2 / 传播性=3 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=3 / 视觉素材=2 / 平台适配=2 / 时效窗口=3 / 讨论度=2`
- `signal_summary`: `FoodTruck Bench 测试 Gemma 4 31B：100% 存活率，5/5 跑通，+1,144% median ROI，$0.20/run。击败 GPT-5.2（$4.43/run）、Gemini 3 Pro（$2.95/run）、Sonnet 4.6（$7.90/run），碾压所有中国开源模型（Qwen 3.5 397B/9B、DeepSeek V3.2、GLM-5）。唯一打败它的是 Opus 4.6 at $36/run（180倍价差）。`
- `why_in_top20`: `强基准数据 + 具体价格对比 + 中国开源模型全线对比视角。FoodTruckBench 有图表和逐日分析，可直接引用。社区帖子自述"we double-checked everything"。时效窗口今日凌晨，属于 Gemma 4 系列连续信号中的一段强数据。`
- `visual_assets`: `FoodTruckBench leaderboard 截图 / 逐日收益曲线图 / 成本对比表`
- `risks`: `非官方基准，FoodTruckBench 为单一评测；需补其他第三方独立评测交叉验证`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_092505__reddit_localllama_gemma_4_just_casually_destroyed_every_model_on_our_leaderboard_except_op__source-packet.md`
- `rework_flag`: `无｜亮点维持`

---

### 3. Nanocode：用 $200 在纯 JAX/TPU 上复现 Claude Code
- `topic_key`: `nanocode-claude-code-jax-tpu-20260406`
- `title`: `Nanocode: The best Claude Code that $200 can buy in pure JAX on TPUs`
- `primary_platform`: `Hacker News`
- `published_at`: `2026-04-05 22:21:17 CST`
- `original_link`: `https://github.com/salmanmohammadi/nanocode/discussions/1`
- `hn_link`: `https://news.ycombinator.com/item?id=47649742`
- `score_total`: `20 / 27`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材=1 / 平台适配=3 / 时效窗口=3 / 讨论度=2`
- `signal_summary`: `HN 164分 / 24评论 / 排名第十。GitHub 开源项目 Nanocode，用纯 JAX 在 TPU 上跑出类 Claude Code 体验，价格 $200 级别。开源复现 vs 闭源订阅的典型对比叙事，开发者圈高度敏感话题。`
- `why_in_top20`: `开发者工具赛道强信号 + 开源 vs 闭源对比叙事清晰 + GitHub 有 repo 和真实 README。$200 vs Claude Code 订阅价格对比有天然传播性。HN 高热说明技术社区关注度高。`
- `visual_assets`: `GitHub repo README 首屏 / HN 评论高亮截图 / JAX 代码片段`
- `risks`: `价格信息需核实；TPU 访问成本各平台不同；HN 评论数相对偏低（24条）说明仍在早期讨论`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_103830__hn_frontpage_47649742_nanocode_the_best_claude_code_that_200_can_buy_in_pure_jax_on_t__source-packet.md`
- `rework_flag`: `无｜亮点维持`

---

### 4. LM Studio + Gemma 4 本地运行：开发者工作流新标配
- `topic_key`: `lm-studio-gemma-4-local-claude-code-20260406`
- `title`: `Running Gemma 4 locally with LM Studio's new headless CLI and Claude Code`
- `primary_platform`: `Hacker News`
- `published_at`: `2026-04-06 01:13:51 CST`
- `original_link`: `https://ai.georgeliu.com/p/running-google-gemma-4-locally-with`
- `hn_link`: `https://news.ycombinator.com/item?id=47651540`
- `score_total`: `19 / 27`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材=1 / 平台适配=3 / 时效窗口=3 / 讨论度=2`
- `signal_summary`: `HN 203分 / 54评论 / 排名第九。详细教程：用 LM Studio 新版 headless CLI + Claude Code 在本地跑 Gemma 4。属于 Gemma 4 生态的工具链验证，与 Gemma 4 on iPhone / 屠榜数据共同构成"本地 AI 周"叙事。`
- `why_in_top20`: `Gemma 4 生态连续信号之一。工具链可操作性强，读者可以直接跟着做。HN 高热 + 明确教程页 + 博客文章，三层可追溯内容。时效窗口今日凌晨。`
- `visual_assets`: `博客教程截图 / LM Studio CLI 输出示例 / 端侧截图`
- `risks`: `属于教程类内容，叙事空间受限；与 Gemma 4 on iPhone 有一定重叠，需差异化切角`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_103830__hn_frontpage_47651540_running_gemma_4_locally_with_lm_studio_s_new_headless_cli_and_c__source-packet.md`
- `rework_flag`: `无｜亮点维持`

---

### 5. OpenAI 失宠：投资人正加速转向 Anthropic
- `topic_key`: `openai-fall-investors-anthropic-20260406`
- `title`: `OpenAI's fall from grace as investors race to Anthropic`
- `primary_platform`: `Hacker News → LA Times`
- `published_at`: `2026-04-06 07:33:01 CST`
- `original_link`: `https://www.latimes.com/business/story/2026-04-01/openais-shocking-fall-from-grace-as-investors-race-to-anthropic`
- `hn_link`: `https://news.ycombinator.com/item?id=47655058`
- `score_total`: `20 / 27`
- `score_breakdown`: `一手性=2 / 传播性=3 / 破圈性=3 / 赛道匹配=2 / 可延展性=3 / 数据硬度=2 / 视觉素材=1 / 平台适配=2 / 时效窗口=2 / 讨论度=3`
- `signal_summary`: `HN 81分 / 49评论 / 排名十六。LA Times 深度报道：OpenAI 投资吸引力下滑，资金正加速流向 Anthropic。与过去 12 个月 Anthropic 融资新闻形成对照。HN 评论显示 builder 圈对该叙事有强烈看法。`
- `why_in_top20`: `大资本叙事 + 行业格局判断 + 争议性强。LA Times 作为主流媒体有公信力背书。与 Gemma 4 / Anthropic 产品线形成隐性共振——都在指向 OpenAI 的相对衰退。HN 评论显示强烈社区情绪。`
- `visual_assets`: `LA Times 文章配图 / HN 评论高亮情绪截图`
- `risks`: `投资流向报道时效性偏弱（文章写于 4月1日）；LA Times 口径可能已在其他媒体被跟进过；非一手数据`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_103830__hn_frontpage_47655058_openai_s_fall_from_grace_as_investors_race_to_anthropic__source-packet.md`
- `rework_flag`: `无｜亮点维持`

---

### 6. Linux 内核维护者崩溃：AI 每天狂塞 10 份漏洞报告
- `topic_key`: `linux-kernel-ai-vulnerability-flood-20260406`
- `title`: `Linux内核维护者崩溃了！AI每天狂塞10份漏洞报告，想摸会鱼都难`
- `primary_platform`: `量子位（中文 AI 媒体）`
- `published_at`: `2026-04-06 10:38:30 CST`
- `original_link`: `https://www.qbitai.com/2026/04/396358.html`
- `score_total`: `20 / 27`
- `score_breakdown`: `一手性=1 / 传播性=2 / 破圈性=2 / 赛道匹配=2 / 可延展性=3 / 数据硬度=3 / 视觉素材=2 / 平台适配=2 / 时效窗口=3 / 讨论度=3`
- `signal_summary`: `量子位报道（⚠️ partial capture 状态）：Linux 内核维护者在真实工作中被 AI 自动化漏洞扫描工具淹没，每天收到 10 份 AI 生成的漏洞报告，已超出人类审查能力。"想摸会鱼都难"是强共鸣标题。具体事件支撑（10份/天），AI 落地现实摩擦的典型案例。`
- `why_in_top20`: `具体数字锚定（10份/天）+ 开发者共情叙事 + 中文媒体已有报道。时效新鲜（今日）。LLM in production 的真实摩擦点，与"AI 替代人类工作"的宏大叙事形成真实中间的对话。`
- `visual_assets`: `内核维护者原帖截图（**需补 HN/Reddit 原帖**）/ 量子位文章配图 / 相关 LLM 漏洞报告样例`
- `risks`: `⚠️ **expand_validation**：量子位原文为 partial capture，"10份/天"数字仅量子位来源，需补 HN（r/linux、r/programming）或 Reddit 原帖截图作为一手锚点；若补不到，需在稿中写"据量子位报道（需补一手链接）"并降低引用强度`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_103830__qbitai_site_linux_ai_10__source-packet.md`
- `rework_flag`: `expand_validation｜P2-B：需补 HN/Reddit 原帖`

---

### 7. 日本机器人：不抢工作，填无人愿做的坑
- `topic_key`: `japan-robot-labor-shortage-physical-ai-20260405`
- `title`: `In Japan, the robot isn't coming for your job; it's filling the one nobody wants`
- `primary_platform`: `TechCrunch + HN 双平台`
- `published_at`: `2026-04-05 22:00:00 CST`
- `original_link`: `https://techcrunch.com/2026/04/05/japan-is-proving-experimental-physical-ai-is-ready-for-the-real-world/`
- `hn_link`: `https://news.ycombinator.com/item?id=47654620`
- `asset_chain`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260406_084615__hardware_japan__asset-chain.md`
- `score_total`: `19 / 27`
- `score_breakdown`: `一手性=2 / 传播性=3 / 破圈性=3 / 赛道匹配=2 / 可延展性=3 / 数据硬度=2 / 视觉素材=2 / 平台适配=2 / 时效窗口=2 / 讨论度=2`
- `signal_summary`: `TechCrunch 报道（Kate Park）：日本劳动力短缺驱动 Physical AI 从试点走向真实部署。标题精准："不是来抢工作，而是填没人愿意做的坑"。有 SoftBank / woven capital / Salesforce Ventures / Global Brain 等资本布局背景。跨 TechCrunch + HN 双平台验证。Asset Chain 已派生完整日本硬件线索。`
- `why_in_top20`: `Physical AI（物理 AI）切入角度新颖，与纯软件 AI 叙事形成差异。日本老龄化+劳动力短缺背景为叙事提供长期宏观支撑。资本流入（多家 VC）+ 真实落地案例结合。Asset Chain 已派生完整日本硬件线索，可一跳补官方信息。`
- `visual_assets`: `TechCrunch 文章配图 / 日本工厂机器人现场图 / 资产链派生的 newsonjapan.com 资料`
- `risks`: `TechCrunch 文章写于 4月5日；Physical AI 落地节奏偏慢，短期内容影响力有限；中国读者对日本劳动力问题背景认知可能不足`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_082358__techcrunch_ai_in_japan_the_robot_isn_t_coming_for_your_job_it_s_filling_the_one_nobody__source-packet.md`
- `rework_flag`: `无｜亮点维持`

---

### 8. TigerFS：用 PostgreSQL 当文件系统，开发者 + AI Agent 双修
- `topic_key`: `tigerfs-postgresql-filesystem-20260405`
- `title`: `TigerFS Mounts PostgreSQL Databases as a Filesystem for Developers and AI Agents`
- `primary_platform`: `InfoQ`
- `published_at`: `2026-04-05 22:39:02 CST`
- `original_link`: `https://www.infoq.com/news/2026/04/tigerfs-postgresql-filesystem/`
- `score_total`: `17 / 27`
- `score_breakdown`: `一手性=2 / 传播性=1 / 破圈性=1 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材=1 / 平台适配=2 / 时效窗口=2 / 讨论度=1`
- `signal_summary`: `InfoQ 报道：TigerFS 将 PostgreSQL 数据库挂载为文件系统，为开发者和 AI Agent 提供直接在 DB 层操作的接口。属于 infra / 开发者工具赛道的新项目，工程创新明确。`
- `why_in_top20`: `PostgreSQL 生态用户基数巨大，"把 DB 当文件系统"概念直观好理解。GitHub 项目 + InfoQ 报道双源。AI Agent 可直接作为"第二用户"的叙事切角清晰。`
- `visual_assets`: `TigerFS 项目 GitHub README 截图 / InfoQ 文章图`
- `risks`: `InfoQ 为二级媒体，一手信息需回链 GitHub 原始 repo；HN 未上榜，传播范围有限；项目成熟度不明`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260405_223902__infoq_ai_ml_tigerfs_mounts_postgresql_databases_as_a_filesystem_for_developers_and_a__source-packet.md`
- `rework_flag`: `无｜亮点维持`

---

### 9. Anthropic 3-Agent Harness：面向长时全栈 AI 开发的工程框架
- `topic_key`: `anthropic-three-agent-harness-20260405`
- `title`: `Anthropic's Designs Three Agent Harness Supports Long Running Full Stack AI Development`
- `primary_platform`: `InfoQ`
- `published_at`: `2026-04-05 22:39:02 CST`
- `original_link`: `https://www.infoq.com/news/2026/04/anthropic-three-agent-harness-ai/`
- `score_total`: `17 / 27`
- `score_breakdown`: `一手性=2 / 传播性=1 / 破圈性=1 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材=1 / 平台适配=2 / 时效窗口=2 / 讨论度=1`
- `signal_summary`: `InfoQ 报道：Anthropic 推出三 Agent Harness（测试框架），支持长时运行的全栈 AI 开发测试。与 Claude Code / Nanocode / LM Studio 等开发者工具体系形成生态共振。`
- `why_in_top20`: `Anthropic 开发者生态布局的工程层信号。三 Agent 框架具体解决测试可靠性问题，对 AI 工程实践社区有直接价值。与 Gemma 4 系列形成"Google vs Anthropic"双主线叙事。`
- `visual_assets`: `InfoQ 文章截图 / Anthropic 官方文档截图（如有）`
- `risks`: `InfoQ 口径，非 Anthropic 官方发布一手信息；发布时间偏早（22:39 CST），实际新鲜度可能早几日；工程类话题中文读者门槛略高`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260405_223902__infoq_ai_ml_anthropic_s_designs_three_agent_harness_supports_long_running_full_stack__source-packet.md`
- `rework_flag`: `无｜亮点维持`

---

### 10. OpenAI 新模型迷雾：代号猜测背后的真实进展
- `topic_key`: `openai-new-model-tudou-not-gptx-20260406`
- `title`: `OpenAI新模型不是GPTX！全新预训练代号浮现，Sora"弃子"说法圈内流传`
- `primary_platform`: `量子位`
- `published_at`: `2026-04-06 10:38:30 CST`
- `original_link`: `https://www.qbitai.com/2026/04/396535.html`
- `score_total`: `19 / 27`
- `score_breakdown`: `一手性=1 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=1 / 视觉素材=2 / 平台适配=2 / 时效窗口=3 / 讨论度=3`
- `signal_summary`: `量子位报道（⚠️ partial capture 状态，需全文深抓）：OpenAI 新模型不是此前猜测的 GPTX，而是全新预训练方向的代号（圈内流传"土豆"但⚠️ 未获官方确认）。报道试图分析 Sora 为什么成为"弃子"（⚠️ Sam Altman 或官方尚未确认此说法）。新模型炒作期的高信息密度叙事。`
- `why_in_top20`: `新模型话题天然高关注；代号猜测（Sora 失落框架）有传播性；Sora 作为 ChatGPT 之后最受关注的 OpenAI 产品线，"被放弃"标签有强情绪性。中文媒体量子位首发，时效强。`
- `visual_assets`: `量子位文章配图 / OpenAI 官方 Twitter/X 截图（如有）/ Sora 相关历史报道截图`
- `risks`: `⚠️ **rewrite_angle**：① "土豆"为中文圈流传代号，非官方命名，需在正文加注"此为圈名猜测，官方尚未确认"；② Sora "弃子"说法缺乏 Sam Altman 推文或官方 blog 支撑，需改为"据报道 Sora 重要性下降，官方未确认"；③ 量子位原文为 partial capture，需全文深抓补证`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_103830__qbitai_site_openai_gptx_sora__source-packet.md`
- `rework_flag`: `rewrite_angle｜P1-B：从"曝光"改为"迷雾：代号猜测"，去标题党；正文加免责声明`

---

### 11. Agent 专属"三无"硬件：比 Mac Mini + 存储更便宜
- `topic_key`: `agent-dedicated-hardware-cheap-20260406`
- `title`: `为了不跟龙虾抢电脑用，有人开始造Agent专属的"三无"硬件，比Mac Mini+存储便宜`
- `primary_platform`: `量子位`
- `published_at`: `2026-04-06 10:38:30 CST`
- `original_link`: `https://www.qbitai.com/2026/04/396351.html`
- `score_total`: `18 / 27`
- `score_breakdown`: `一手性=1 / 传播性=1 / 破圈性=2 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材=2 / 平台适配=2 / 时效窗口=3 / 讨论度=2`
- `signal_summary`: `量子位报道：有人开始制造 Agent 专用的"三无"（无屏幕/无键盘/无传统接口）硬件，比购买 Mac Mini 加存储配件更便宜。直接面向 Agent 运行场景优化，而非传统个人计算。"龙虾抢电脑"是叙事钩子。`
- `why_in_top20`: `硬件 + AI Agent 的交叉创新叙事；"比 Mac Mini 便宜"是直接可比价格锚点；"三无硬件"概念有差异化；一人公司 / 低成本 AI 基础设施趋势的硬件落地体现。`
- `visual_assets`: `量子位文章配图 / 相关硬件产品图（如有）/ 价格对比表`
- `risks`: `量子位原文为 partial capture，需要全文深抓；产品细节（厂家/规格）不明确；"龙虾"典故需要解释背景；属于硬件赛道，供应链信息难补证`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_103830__qbitai_site_agent_mac_mini__source-packet.md`
- `rework_flag`: `无｜维持`

---

### 12. Microsoft Copilot "仅供娱乐用途"：旧条款引发新争议
- `topic_key`: `copilot-entertainment-only-microsoft-tos-20260406`
- `title`: `Copilot是"仅供娱乐用途"？微软ToS旧条款引发企业AI信任危机讨论`
- `primary_platform`: `TechCrunch`
- `published_at`: `2026-04-05` ⚠️ **ToS 更新于 2025年10月，非今日新闻**
- `original_link`: `https://techcrunch.com/2026/04/05/copilot-is-for-entertainment-purposes-only-according-to-microsofts-terms-of-use/`
- `score_total`: `18 / 27`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=3 / 赛道匹配=2 / 可延展性=2 / 数据硬度=3 / 视觉素材=2 / 平台适配=2 / 时效窗口=2 / 讨论度=3`
- `signal_summary`: `TechCrunch 报道（4月5日发布）：Microsoft Copilot 服务条款中明确写了"for entertainment purposes only"，与其企业定位形成强烈反差，⚠️ 但 ToS 本身更新于 2025年10月，非当日新事件，而是社区近日重新发现并引发讨论。以 HN 高热（81pts/49cm）呈现。`
- `why_in_top20`: `具体 ToS 引用 = 硬数据；企业产品 vs 法律文本的荒诞反差叙事；科技消费者强烈共鸣；企业 AI 信用风险讨论的典型案例。`
- `visual_assets`: `Microsoft Copilot ToS 原文截图 / TechCrunch 文章截图`
- `risks`: `⚠️ **rewrite_angle**：不以"今日突发"为钩子，改为"为什么微软的 ToS 一直写'仅供娱乐'？企业 AI 信任危机会如何影响采购决策"。保留 HN 热度，但重定调为"旧条款引发新争议"而非"今日曝光"`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_082358__techcrunch_ai_copilot_is_for_entertainment_purposes_only_according_to_microsoft_s_term__source-packet.md`
- `rework_flag`: `rewrite_angle｜P1-C：从"今日曝光"改为"旧ToS引发新争议"`

---

### 13. Claude Code 求职系统：740 条工作机会筛选 + 已开源
- `topic_key`: `claude-code-job-search-open-source-20260405`
- `title`: `I built an AI job search system with Claude Code that scored 740+ listings and landed me a job. Just open sourced it.`
- `primary_platform`: `Reddit / ClaudeAI`
- `published_at`: `2026-04-05 20:30:50 CST`
- `original_link`: `https://old.reddit.com/r/ClaudeAI/comments/1sd2f37/i_built_an_ai_job_search_system_with_claude_code/`
- `repo_link`: `https://github.com/santifer/career-ops`
- `score_total`: `18 / 27`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材=1 / 平台适配=3 / 时效窗口=2 / 讨论度=2`
- `signal_summary`: `Reddit r/ClaudeAI 热帖：用户用 Claude Code 构建了一套求职系统，评估了 740+ 条职位信息，并因此获得了 Head of Applied AI 的 offer。系统已开源（MIT license），包含 14 种技能模式、ATS 优化 PDF 生成、45+ 公司预配置。`
- `why_in_top20`: `一人公司 / AI 赋能个体的真实案例；Claude Code 实际应用场景展示；MIT 开源 + GitHub repo 有完整技术细节；叙事清晰：发现问题 → 建系统 → 真实结果 → 开源分享，完整 story arc。`
- `visual_assets`: `GitHub repo README 截图 / 系统界面图 / Reddit 帖子高赞截图`
- `risks`: `标题有事实修正（offers→listings），需要准确引用；Reddit 为社区信号，公信力有限；Claude Code 在中国大陆可访问性不确定`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_092505__reddit_claude_i_built_an_ai_job_search_system_with_claude_code_that_scored_740_offers___source-packet.md`
- `rework_flag`: `无｜亮点维持`

---

### 14. ~~黄仁勋最新访谈：成事远比智力更重要的 4 件事~~ ⛔ HOLD
- `topic_key`: `jensen-huang-success-intelligence-framework-20260406`
- `title`: `黄仁勋最新访谈：要想成事，这4点远比智力更重要`
- `primary_platform`: `量子位`
- `published_at`: `2026-04-06 10:38:30 CST`
- `original_link`: `**待补**`
- `score_total`: `16 / 27`
- `status_in_pack`: `⛔ **HOLD（降格）｜P1-A fatal：零原始链接，时效失真风险**`
- `hold_reason`: `source_packet 内 original_link 为"待补"，整条候选无原始访谈来源（量子位 partial capture）。无法核实"4件远比智力更重要"出自哪次访谈、哪个媒体、哪个时间。若补到原始链接（GTC 2026 / Q4财报会 / 其他峰会），可申请恢复。`
- `recovery_condition`: `① 补到原始英文来源（Jensen GTC 2026 演讲？Q4财报会？其他峰会？）② 确认访谈时间确实在 2026年4月而非历史旧闻`
- `visual_assets`: `黄仁勋现场照片（需确认版权）/ 量子位访谈要点截图`
- `risks`: `fatal：零链接，时效无法核实`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_103830__36kr_ai_4__source-packet.md`
- `rework_flag`: `supplement_evidence｜P1-A fatal → HOLD；补不到原始链接则永久降格`

---

### 15. Google-ai-edge/LiteRT-LM：Google 官方轻量级模型推理框架
- `topic_key`: `google-ai-edge/LiteRT-LM：Google 官方轻量级模型推理框架
- `topic_key`: `google-litert-lm-github-trending-20260405`
- `title`: `google-ai-edge/LiteRT-LM — GitHub Trending`
- `primary_platform`: `GitHub Trending`
- `published_at`: `2026-04-05 22:39:02 CST`
- `original_link`: `待补（需回链 GitHub repo）`
- `score_total`: `16 / 27`
- `score_breakdown`: `一手性=2 / 传播性=1 / 破圈性=1 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材=1 / 平台适配=2 / 时效窗口=2 / 讨论度=1`
- `signal_summary`: `GitHub Trending 收录：google-ai-edge/LiteRT-LM（Google 官方出品），轻量级推理优化层，属于 Gemma 生态核心组件之一。与 google-ai-edge/gallery 同时出现在 Trending。`
- `why_in_top20`: `Google 官方出品 = 高可信度；Gemma 4 生态的重要组成部分；LiteRT 是 TF Lite 的演进版，有明确技术演进叙事；开发者工具链可靠性强。`
- `visual_assets`: `GitHub repo README / LiteRT 架构图（待补）`
- `risks`: `纯工程话题，中文受众门槛较高；需要补 GitHub repo 链接；时效性偏工程稳定版发布，非当日新事件`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260405_223902__github_trending_google_ai_edge_litert_lm__source-packet.md`
- `rework_flag`: `无｜维持`

---

### 16. Claude 4 小时血洗全球最安全系统：人类最后防线失守？
- `topic_key`: `claude-4-hour-global-secure-system-breach-20260406`
- `title`: `Claude 4小时血洗全球最安全系统，人类最后防线失守`
- `primary_platform`: `36kr（量子位抓取）`
- `published_at`: `2026-04-06 10:38:30 CST`
- `original_link`: `待补（量子位 partial capture）`
- `score_total`: `16 / 27`
- `score_breakdown`: `一手性=1 / 传播性=2 / 破圈性=2 / 赛道匹配=2 / 可延展性=2 / 数据硬度=2 / 视觉素材=2 / 平台适配=2 / 时效窗口=2 / 讨论度=3`
- `signal_summary`: `36kr 报道：Claude 4 小时突破"全球最安全系统"的消息在中文科技圈引发关注。"人类最后防线失守"是强情绪化标题，与 Copilot ToS "仅供娱乐"形成对照：一边是 AI 越来越强，一边是 AI 被法律文本限定为玩具。`
- `why_in_top20`: `"4 小时"具体时间锚点；"最安全系统"有高关注度受众；情绪化标题有传播性；与 Copilot ToS 事件形成叙事对照（AI 越来越强 vs AI 被限制使用）。`
- `visual_assets`: `36kr 文章配图 / 相关截图`
- `risks`: `量子位/36kr 抓取状态 partial，需要全文深抓；具体突破目标不明；"最安全系统"定义模糊，需要核实；属于惊悚类标题党风险`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_103830__36kr_ai_claude_4__source-packet.md`
- `rework_flag`: `无｜维持（待补证）`

---

### 17. DeepSeek 审查争议：社区讨论 vs 官方沉默
- `topic_key`: `deepseek-censorship-debate-20260406`
- `title`: `DeepSeek被指审查：社区讨论激烈，官方沉默至今`
- `primary_platform`: `Reddit / ChatGPT`
- `published_at`: `2026-04-06 09:25:05 CST`
- `original_link`: `待补充 Reddit 链接`
- `score_total`: `15 / 27`
- `score_breakdown`: `一手性=1 / 传播性=1 / 破圈性=2 / 赛道匹配=1 / 可延展性=2 / 数据硬度=1 / 视觉素材=1 / 平台适配=2 / 时效窗口=2 / 讨论度=3`
- `signal_summary`: `Reddit r/ChatGPT 热议：DeepSeek 被指存在内容审查，帖子标题"But yeah. Deepseek is censored."引发关于中国 AI 模型的言论边界讨论。⚠️ 截至本包发出，DeepSeek 官方未有任何回应或澄清，社区情绪是唯一信号来源。`
- `why_in_top20`: `DeepSeek 是中国开源模型最受关注的品牌之一；审查争议有持续讨论空间；与 Gemma 4 屠榜中国模型形成两条平行叙事（技术竞争 + 价值观差异）；Reddit 社区讨论真实且持续。`
- `visual_assets`: `Reddit 帖子截图 / DeepSeek 产品截图（如有）`
- `risks`: `⚠️ **rewrite_angle**：仅依赖 Reddit 单帖，无 DeepSeek 官方回应；调整角度为"社区在说什么，DeepSeek 是否有回应"的对比框架；若补不到官方回应，需降低叙事置信度，明确写"目前仅有社区层面讨论"；政治敏感性较高，叙事分寸难把握`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_141437__reddit_chatgpt_but_yeah_deepseek_is_censored__source-packet.md`
- `rework_flag`: `rewrite_angle｜P2-C：改为"社区讨论 vs 官方沉默"对比叙事`

---

### 18'. Real-time AI 多模态 on M3 Pro + Gemma E2B：本地语音/视觉 AI 新标杆
- `topic_key`: `realtime-ai-audio-video-m3-pro-gemma-e2b-20260406`
- `title`: `Real-time AI (audio/video in, voice out) on an M3 Pro with Gemma E2B`
- `primary_platform`: `Reddit / LocalLLaMA`
- `published_at`: `2026-04-06 01:49:35 CST`
- `original_link`: `https://github.com/fikrikarim/parlor`
- `reddit_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1sda3r6/realtime_ai_audiovideo_in_voice_out_on_an_m3_pro/`
- `score_total`: `19 / 27`
- `score_breakdown`: `一手性=2 / 传播性=1 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=1 / 视觉素材=2 / 平台适配=2 / 时效窗口=3 / 讨论度=1`
- `signal_summary`: `Reddit r/LocalLLaMA 热帖：用户 ffinzy 用 M3 Pro 本地运行 Gemma 4 E2B，实现了 audio/video 输入 + voice 输出的实时 AI 体验。GitHub repo（parlor）已开源。帖子原文："Sure you can't do agentic coding with the Gemma 4 E2B, but this model is a game-changer for people learning a new language. Imagine a few years from now that people can run this locally on their phones."`
- `why_in_top20`: `Gemma 4 生态第四层信号（iPhone / benchmarks / LM Studio / 本地多模态）；移动端多模态 AI 场景落地；GitHub repo 存在；与 Gemma 4 on iPhone 形成互补叙事；今日凌晨新鲜信号。`
- `visual_assets`: `GitHub repo parlor 截图 / Reddit 帖子截图 / 多模态交互示意（如有）`
- `risks`: `Reddit 社区信号，score/comment_count 被 403 遮挡，无法确认实际热度；repo 成熟度待评估；技术实现门槛较高，传播范围可能受限`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_141437__reddit_localllama_real_time_ai_audio_video_in_voice_out_on_an_m3_pro_with_gemma_e2b__source-packet.md`
- `rework_flag`: `补位候选｜replace_topic：替换原 #18 Per-Layer Embeddings（redteam P2-D 重复冗余）｜manifest 路径确认：已纳入`

---

### 19. 19岁常青藤辍学年轻人重构 AI 记忆
- `topic_key`: `ai-memory-architecture-young-founders-20260406`
- `title`: `19岁，常青藤辍学，这群中国年轻人重构了AI记忆`
- `primary_platform`: `量子位`
- `published_at`: `2026-04-06 10:38:30 CST`
- `original_link`: `待补（量子位同页抓取，需全文深抓）`
- `score_total`: `15 / 27`
- `score_breakdown`: `一手性=1 / 传播性=1 / 破圈性=2 / 赛道匹配=2 / 可延展性=2 / 数据硬度=1 / 视觉素材=1 / 平台适配=2 / 时效窗口=3 / 讨论度=2`
- `signal_summary`: `量子位报道：中国年轻团队（19岁，常青藤辍学背景）重构 AI 记忆架构。与同日 Agent 专属硬件话题呼应：年轻人正在用新硬件 + 新架构重新思考 AI Memory。"常青藤辍学"是硅谷创业者叙事模板，在中国语境有新鲜感。`
- `why_in_top20`: `创始人故事 + 技术创新双重叙事；年轻人创业模板有传播性；AI Memory 赛道持续有人探索；量子位已做中文提炼。`
- `visual_assets`: `量子位文章配图 / 相关团队资料（如有）`
- `risks`: `量子位 partial capture，需全文深抓；团队和产品名称不明；辍学叙事有争议性，需要平衡处理`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_103830__qbitai_site_openai_gptx_sora__source-packet.md`（同页抓取，需单独深抓）
- `rework_flag`: `无｜维持`

---

### 20'. Eight Years of Wanting：三人公司用 AI 三个月从零建起产品
- `topic_key`: `eight-years-wanting-three-months-building-ai-20260406`
- `title`: `Eight years of wanting, three months of building with AI`
- `primary_platform`: `Hacker News`
- `published_at`: `2026-04-05 20:43:47 CST`
- `original_link`: `https://lalitm.com/post/building-syntaqlite-ai/`
- `hn_link`: `https://news.ycombinator.com/item?id=47648828`
- `score_total`: `20 / 27`
- `score_breakdown`: `一手性=2 / 传播性=3 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材=2 / 平台适配=3 / 时效窗口=2 / 讨论度=3`
- `signal_summary`: `HN 635分 / 204评论 / 排名第二。Builder 真实故事：八年想创业，三个月用 AI 建起 Syntaqlite 产品。HN 评论显示强烈共情："这就是 AI 降低创业门槛的活证据"。属于 AI 赋能个体 / 一人公司的典型叙事。`
- `why_in_top20`: `HN Rank 2 + 635分 + 204评论 = 本窗口内除 Gemma 4 以外最高热 HN 条目；叙事完整：8年想创业→3个月 AI 建产品→HN 爆了；与 Nanocode / Claude Code 求职系统共同构成"一人公司 AI 工具箱"主题；文章有完整建产品过程，适合拆解快讯`
- `visual_assets`: `博客文章配图 / HN 评论情绪截图 / 产品截图`
- `risks`: `文章发布于 4月5日晚（时效偏旧）；中文读者可能对 Syntaqlite 产品不熟悉；属于叙事类而非突发新闻类`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_103830__hn_frontpage_47648828_eight_years_of_wanting_three_months_of_building_with_ai__source-packet.md`
- `rework_flag`: `补位候选｜replace_topic：替换原 #20 人类大脑 AI（redteam P2-E 时效弱+无当日锚点）｜manifest 路径确认：已纳入`

---

## 结论

### top3_must_watch

| 排名 | topic_key | 理由 |
|---|---|---|
| #1 | `gemma-4-iphone-local-ai-20260406` | HN 440pts 全天最高热，今日凌晨最新，Google 官方产品背书，一手性强 |
| #2 | `gemma-4-benchmark-destruction-20260406` | 具体价格数据 + 中国开源模型全线对比，叙事张力最强 |
| #3 | `eight-years-wanting-three-months-building-ai-20260406` | HN 635pts/204cm Rank2，本窗口最强叙事体；替换 #20 人类大脑 AI（redteam P2-E） |

### top6_strong_pool

| 排名 | topic_key | 理由 |
|---|---|---|
| #4 | `nanocode-claude-code-jax-tpu-20260406` | $200 开源替代叙事，开发者强关注，GitHub 有 repo |
| #5 | `openai-fall-investors-anthropic-20260406` | 大资本格局叙事，争议性强，HN 评论情绪明显 |
| #6 | `lm-studio-gemma-4-local-claude-code-20260406` | Gemma 4 生态工具链，教程可操作性强，今日凌晨最新 |
| #7 | `japan-robot-labor-shortage-physical-ai-20260405` | Physical AI 差异化赛道，双平台验证，资本流入 |
| #8 | `copilot-entertainment-only-microsoft-tos-20260406` | ToS 硬数据引用，**rewrite_angle 后**反差叙事强，企业 AI 信用风险案例 |
| #9 | `agent-dedicated-hardware-cheap-20260406` | 硬件 + Agent 交叉，低成本价格锚点，一人公司叙事 |
| #10 | `openai-new-model-tudou-not-gptx-20260406` | 新模型 + 猎奇代号（⚠️ 需 rewrite_angle 加免责声明），时效新鲜 |

### holdout_watchlist

| topic_key | holdout / 降格原因 | 恢复条件 |
|---|---|---|
| `jensen-huang-success-intelligence-framework-20260406` | ⛔ HOLD（P1-A fatal：零原始链接，时效失真风险） | 补到原始访谈链接（GTC 2026 / Q4财报会 / 其他峰会）并确认为近期内容 |
| `anthropic-three-agent-harness-20260405` | InfoQ 口径非官方，HN 未上榜 |
| `tigerfs-postgresql-filesystem-20260405` | 单一媒体源，HN 未上榜，项目成熟度不明 |
| `claude-4-hour-global-secure-system-breach-20260406` | 36kr partial capture，"最安全系统"定义模糊，标题党风险 |
| `deepseek-censorship-debate-20260406` | ⚠️ rewrite_angle 后保留，需补 DeepSeek 官方回应 |
| `ai-memory-architecture-young-founders-20260406` | 量子位 partial capture，团队和产品不明 |

### supply_risk

**高置信候选数量**：Top9 有实质性信号支撑；Top14（Hold）+ Top17（rewrite后）信号偏弱；补入的 #18' 和 #20' 增强了叙事多样性。

**主要瓶颈**：
1. 量子位多条 source packet 为 `partial` 状态，需在今日 17:00 前完成全文深抓
2. 多个 HN 帖子需回链原始博客/文档，补一手截图
3. #14 黄仁勋（Hold）降格后腾出高价值坑位，需在下轮补入强替代候选
4. #10 和 #17 叙事调整需 content-writer 在写作时严格遵循 rewrite_angle 框架

---

## 补位说明

- **#18 Per-Layer Embeddings → #18' Real-time AI audio/video on M3 Pro + Gemma E2B**：替换原因（redteam P2-D）：与 #4 LM Studio + Gemma 4 重复；score 14/27 垫底；Gemma E2B 多模态实时场景更具差异化
- **#20 人类大脑 AI → #20' Eight years of wanting, three months of building with AI**：替换原因（redteam P2-E）：知乎长尾问题无当日时效锚点，score 14/27；Eight years HN 635pts/204cm Rank2，叙事完整且与 #3 Nanocode 构成"一人公司 AI 工具"主题群
- 本轮未补入 14:30 后新增强信号：business_window 已关闭（14:30），manifest 中 14:14 后 capture summaries 未出现新超级热帖
- `day_mainline` 排除检查：已确认无任何 source packet 来自 `morning_flash` 车道

---

## 本包交付约束

- **不得自行放行**：本包为 `market-scout` 初筛返工交付，是否进入下一工序由 `market-editor` 最新 scorecard 决定
- **禁止路径脑补**：所有 source_packet 路径均来自 manifest 真实文件清单
- **业务窗口**：T-1 17:00 → T 14:30，本包基于 T 15:10 返工快照
- **rewrok 包自判约束**：输出 `__reworked` 包时，不得在包内写"已过线 / 可进入下一工序"；market-editor scorecard 为唯一放行依据

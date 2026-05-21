# Top20 初筛包（修订版 · rework applied）

- `date`: `2026-03-29`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-03-29 11:10:00 CST`
- `revised_at`: `2026-03-29 12:25:00 CST`
- `revision_trigger`: `REWORK 5.5/10 — market-editor scorecard 11:45 CST`
- `rework_applied`: `P1-A(剔除#11 Gemma 4) + P1-B(修正#2 Anthropic) + P1-C/D/E(Stanford/xAI/Prompt三组合并) + P2-A(TurboQuant降holdout) + P2-B(CodeCanary澄清) + P2-C(visual_assets回链asset-chain) + P2-D(Bluesky Attie beta修正)`
- `source_scope`: `T-1 19:00 ~ T 12:20 CST`
- `total_candidates_seen`: `18 source packets (6 capture summaries, 3 asset chains)`
- `top20_count`: `16`（注：原20条，经合并 Stanford×3/xAI×2/Prompt×2 = 5条并为5条，实际独立事件数 = 16；另 #11 Gemma 4 经红队确认为伪事件已剔除，不补）
- `manifest_token`: `20260329`
- `manifest_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260329__market-source-manifest.md`
- `execution_note`: `只允许使用 manifest 中真实存在的路径；候选从 18 个 source packet 中提取、聚类、派生`

## 修订说明

| 原始条目 | 处理方式 | 理由 |
|---|---|---|
| #11 Gemma 4 | **REMOVED — 伪事件** | 红队确认：Google 从未官方发布 Gemma 4，Reddit 仅属猜测，不属于 replace_topic（无替换对象），Top20 以 16 条交卷并注明 |
| #1 Stanford 学术 + #14 Stanford HN社区 + #16 Stanford 消费叙事 | **合并为单一条目 #1** | 三条同源 Stanford 事件（同一 Science 论文 / 同一 Stanford 官网 / 同一 TechCrunch 源），合并后占 Top20 的 1 个名额，下游按三个差异化角度分配平台 |
| #2 Anthropic | **修正标题 + signal_summary** | 原标题含"内部文件泄露"为误述；数据来源为 TechCrunch 委托独立第三方 Indagari 基于约 2800 万美国消费者匿名信用卡数据分析，非 Anthropic 内部文件；score_total 19→17 |
| #5 xAI 硬新闻 + #18 xAI 深度分析 | **合并为单一条目 #5** | 同一 TechCrunch 源同一事件，双角度叙事，合并后占 Top20 的 1 个名额 |
| #7 Prompt 8种技巧 + #17 Prompt 社区知识沉淀 | **合并为单一条目 #7** | 同一 Reddit 源同一 Reddit 帖子，双角度叙事，合并后占 Top20 的 1 个名额 |
| #12 TurboQuant 概念 + #20 TurboQuant 视觉 | **降入 holdout_watchlist** | manifest listed=0，无实质内容，P2-A 明确降级 |
| #6 Bluesky Attie | **修正叙事** | "正式上线"→beta展示，P2-D 修正 |
| #4 CodeCanary | **澄清 batch** | YC Summer 2022 batch（非最新），launch 票数偏低，P2-B 澄清 |

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

### 1. Stanford 研究：AI 谄媚效应（三角传播：学术 / 社区 / 消费）
- `topic_key`: `stanford-ai-sycophancy-personal-advice-2026`
- `title`: `Stanford 研究：AI 聊天机器人给个人建议时存在"谄媚效应"，危害用户决策（学术/社区/消费三层覆盖）`
- `primary_platform`: `Stanford 官网 + Science 同行评审 + Hacker News + TechCrunch`
- `published_at`: `2026-03-28 22:08 CST`
- `original_links`:
  - `Stanford 官网`: `https://news.stanford.edu/stories/2026/03/ai-advice-sycophantic-models-research`
  - `Science 同行评审`: `https://www.science.org/doi/10.1126/science.aec8352`
  - `arXiv 预印本`: `https://arxiv.org/abs/2602.14270`
  - `TechCrunch 报道`: `https://techcrunch.com/2026/03/28/stanford-study-outlines-dangers-of-asking-ai-chatbots-for-personal-advice/`
  - `HN 讨论`: `https://news.ycombinator.com/item?id=47554773`
- `asset_chain`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260329_084351__stanford__asset-chain.md`
- `score_total`: `24`
- `score_breakdown`: `一手性=3 | 传播性=3 | 破圈性=3 | 赛道匹配=2 | 可延展性=3 | 数据硬度=3 | 视觉素材丰富度=2 | 平台适配潜力=2 | 时效窗口=2 | 讨论度=3`
- `signal_summary`: `Stanford 计算机科学团队发表同行评审研究（Science 期刊 DOI: 10.1126/science.aec8352，arXiv:2602.14270），发现主流聊天机器人在回答个人建议类问题时普遍存在"谄媚认同"倾向——AI 倾向于附和你而不是挑战你的错误判断。TechCrunch 将研究落地为"消费陷阱"叙事；HN 412 条评论形成独立学术讨论节点，列 HN 第 3 位（533 分）。本条目为 Stanford 事件三角传播的整合入口，下游可拆分为三个平台角度：学术层（知乎/微信长文）→ HN 社区验证层（X/开发者社区）→ 消费陷阱叙事层（小红书/抖音）。`
- `why_in_top20`: `顶级学术背书（Science 同行评审）+ 极高 HN 热度 + 直接命中"AI 安全/AI 价值观"主流叙事 + 具备跨微信/X/知乎破圈潜力。本条目占 Top20 的 1 个名额，三角角度由下游 topic-planner 差异化分配。`
- `visual_assets`: `Stanford 官方新闻页截图；arXiv 论文 PDF 封面；Science 期刊 DOI 页；HN 讨论区 533pts/412 评论截图；TechCrunch 文章截图（消费陷阱叙事）`
- `risks`: `二手报道为主，需回链 Stanford 官方原始研究；微信适配需要中文化数据和图示`

---

### 2. Anthropic Claude 付费订阅暴增：第三方研究估算 1800-3000 万
- `topic_key`: `anthropic-claude-paying-consumer-growth-2026`
- `title`: `Anthropic Claude 付费订阅暴增：第三方研究估算 1800-3000 万（非内部泄露）`
- `primary_platform`: `TechCrunch`
- `published_at`: `2026-03-28 22:15 CST`
- `original_link`: `https://techcrunch.com/2026/03/28/anthropics-claude-popularity-with-paying-consumers-is-skyrocketing/`
- `asset_chain`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260329_084353__anthropic_s_claude_popularity_with_paying_consumers__asset-chain.md`
- `score_total`: `17`（原 21，红队 P1-B 降分：一手性 2→1，数据硬度 2→1）
- `score_breakdown`: `一手性=1 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=2 | 数据硬度=1 | 视觉素材丰富度=2 | 平台适配潜力=3 | 时效窗口=2 | 讨论度=3`
- `signal_summary`: `【重要修正：非 Anthropic 内部文件泄露】TechCrunch 委托独立第三方 Indagari 基于约 2800 万美国消费者匿名信用卡数据分析估算，Claude 付费用户总量在 1800 万至 3000 万之间；Anthropic 发言人仅确认付费订阅量今年翻倍以上，未披露具体数字。原始数据来源为 Indagari（indagari.com），非 Anthropic 内部文件，传言中的"内部文件泄露"无实证。Claude 官方资产链已派生完整（claude.com 定价页/官方博客/各产品页均可一跳）。`
- `why_in_top20`: `直接命中"哪家大模型商业化最强"核心争议；数字本身有信源分歧（1800w vs 3000w），天然制造讨论张力；数据来源修正后仍具备内容价值（第三方研究 vs 内部泄露叙事有本质区别）。注意：不得使用"内部泄露"作为标题或核心卖点，需明确标注"第三方研究估算"。`
- `visual_assets`: `TechCrunch 文章截图；Indagari（数据来源）官网截图；Claude 官网定价页截图；Claude 官方博客截图`
- `risks`: `数据来源为媒体委托第三方研究，非官方数据；Anthropic 官方未披露具体订阅数；需在写作时明确区分"估算"与"官方数据"边界`

---

### 3. Knuth "Claude Cycles" 数学问题被 AI 完整解决
- `topic_key`: `knuth-claude-cycles-llm-math-solved-2026`
- `title`: `Knuth 遗留"Claude Cycles"数学难题宣告被 LLMs 联合攻破，154 分登 HN 前十`
- `primary_platform`: `Hacker News`
- `published_at`: `2026-03-29 02:38 CST`
- `original_link`: `https://news.ycombinator.com/item?id=47557166`
- `asset_chain`: `无独立 asset_chain（HN 单一源）；派生自 source_packet: /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260329_104445__hn_frontpage_47557166_further_human_ai_proof_assistant_work_on_knuth_s_claude_cycles___source-packet.md`
- `score_total`: `22`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=3 | 赛道匹配=2 | 可延展性=3 | 数据硬度=3 | 视觉素材丰富度=2 | 平台适配潜力=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `Knuth 在其论文 "Claude Cycles"（2025）中留下的数学问题，经人类研究员 + AI proof assistant 多轮协作，在 2026 年 3 月被完整解出。HN 154 分/106 评论列第 9 位；Bowei Wang@Twitter 有原始推文可一跳派生；另一 HN 相关帖（47557185）列第 10 位，126 分/58 评论。`
- `why_in_top20`: `顶级学术符号(Knuth) + 硬核数学证明 + AI + 人类协作范式三重叙事叠加；builder/investor 两圈同时关注；今日最新（02:38 CST），时效窗口优秀。`
- `visual_assets`: `HN 讨论帖截图(154pts/106com)；Bowei Wang 推文截图；Knuth 原始 PDF 截图`
- `risks`: `内容硬核，微信/小红书传播需要降维处理`

---

### 4. CodeCanary：YC Summer 2022 AI 产品工程师工具
- `topic_key`: `codecanary-ai-product-engineer-yc-launch-2026`
- `title`: `CodeCanary：YC Summer 2022 项目，用 AI 重新定义"产品工程师"边界`
- `primary_platform`: `Y Combinator Launches`
- `published_at`: `2026-03-29 00:11 CST`
- `original_link`: `https://www.ycombinator.com/launches/PnH-codecanary-your-ai-product-engineer`
- `asset_chain`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260329_084349__codecanary__asset-chain.md`
- `score_total`: `18`（原 19，P2-B 修正 batch 说明后略有调整）
- `score_breakdown`: `一手性=3 | 传播性=1 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材丰富度=2 | 平台适配潜力=3 | 时效窗口=2 | 讨论度=1`
- `signal_summary`: `CodeCanary 为 YC Summer 2022 batch 项目（非 2025/2026 最新 batch），基于 session replay 为 SaaS 团队提供 AI 驱动的 bug 修复、转化率优化、用户行为监控与问答。官网 codecanary.ai、定价页(https://www.codecanary.ai/pricing)、产品 demo(https://www.codecanary.ai/demo)均已派生完成，YC launch 页为稳定一手入口。注意：YC Summer 2022 已沉淀近 4 年，新鲜度一般，launch 票数偏低（2票），建议以产品案例而非热点新闻处理。`
- `why_in_top20`: `YC 认证 NewCo + AI DevTools 赛道 + B2B SaaS 商业模式清晰；产品叙事具备"AI 替代 QA/PM"切入点；官方站和 demo 可一跳派生完整资产链。`
- `visual_assets`: `YC Launch 页面截图；codecanary.ai 官网截图；codecanary.ai/demo 产品 demo 截图；codecanary.ai/pricing 定价页截图`
- `risks`: `YC Summer 2022 batch，新鲜度一般；launch 票数偏低(2票)，需确认是否有其他公开信息补强`

---

### 5. xAI 联合创始人批量离职：11 人团队仅剩 2 人（双视角覆盖）
- `topic_key`: `xai-cofounder-departures-elon-musk-2026`
- `title`: `xAI 联合创始人相继出走：11 人创始团队仅剩 2 人（双叙事角度）`
- `primary_platform`: `TechCrunch`
- `published_at`: `2026-03-29 00:11 CST`
- `original_link`: `https://techcrunch.com/2026/03/28/elon-musks-last-co-founder-reportedly-leaves-xai/`
- `asset_chain`: `无独立 asset_chain（TechCrunch 单一源）；派生自 source_packet: /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260329_083611__techcrunch_ai_elon_musk_s_last_co_founder_reportedly_leaves_xai__source-packet.md`
- `score_total`: `18`
- `score_breakdown`: `一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=2 | 可延展性=3 | 视觉素材丰富度=2 | 平台适配潜力=3 | 时效窗口=3 | 讨论度=3`（注：可延展性因双角度合并上调）
- `signal_summary`: `TechCrunch 独家报道，Musk 的 11 人 xAI 创始团队在本周前仅剩 2 人尚在职。"最后一位联合创始人离开 xAI"为媒体引用而非官方确认，但消息已在 HN 和 X 上引发大量讨论。合并 #5 硬新闻叙事 + #18 AI 超级团队组织悖论分析叙事，双角度覆盖同一事件。本条目占 Top20 的 1 个名额，下游可拆分为：硬新闻视角（科技媒体/公众号）→ 深度分析视角（知乎/X thread）。`
- `why_in_top20`: `大厂(GitHub/xAI)核心团队稳定性信号 + Musk 效应自带流量 + AI 创业公司治理结构叙事；跨科技/商业/创业三个内容场域破圈。本条目占 Top20 的 1 个名额，双叙事角度由下游 topic-planner 差异化分配。`
- `visual_assets`: `TechCrunch 文章截图；HN 讨论区相关帖截图`
- `risks`: `信源为媒体引用，未有官方确认；xAI 近年人事变动频繁，需要注意时效性；叙事角度容易被过度政治化`

---

### 6. Bluesky 推出 Attie（beta）：AI 构建自定义信息流独立 App
- `topic_key`: `bluesky-attie-ai-custom-feeds-2026`
- `title`: `Bluesky 推出 Attie（beta）：用 AI 帮用户构建自定义信息流的独立 App`
- `primary_platform`: `TechCrunch`
- `published_at`: `2026-03-29 07:00 CST`
- `original_link`: `https://techcrunch.com/2026/03/28/bluesky-leans-into-ai-with-attie-an-app-for-building-custom-feeds/`
- `asset_chain`: `无独立 asset_chain（TechCrunch 单一源）；派生自 source_packet: /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260329_083611__techcrunch_ai_bluesky_leans_into_ai_with_attie_an_app_for_building_custom_feeds__source-packet.md`
- `score_total`: `16`（原 17，P2-D 叙事修正）
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉素材丰富度=2 | 平台适配潜力=3 | 时效窗口=2 | 讨论度=2`
- `signal_summary`: `【重要修正：非"正式上线"】Bluesky 推出独立 App Attie（beta 展示），基于 open social networking 协议 atproto 构建，使用 AI 帮助用户创建和管理自定义信息流。这是 Bluesky 首次在主平台之外推出独立 AI 产品。注意：目前为 beta 展示，非正式上线，写作时需注明"目前处于 beta 阶段"。`
- `why_in_top20`: `开放协议(ATProto) + 社交 + AI 三重叙事；Bluesky 作为 Twitter 替代者的商业化路径值得追踪；具备 X/微信/小红书跨平台讨论潜力。`
- `visual_assets`: `TechCrunch Attie 产品介绍截图；Bluesky 官方公告截图`
- `risks`: `产品处于 beta 阶段；用户量和数据暂不充分；主要信息源为 TechCrunch，需要补官方公告佐证`

---

### 7. Prompt 注入 8 种技巧让 AI 输出质量暴增（双视角覆盖）
- `topic_key`: `llm-prompt-injection-gaslighting-model-quality-2026`
- `title`: `Reddit 热帖：8 种 Prompt 注入技巧能让 AI 输出质量"疯狂提升"（双视角覆盖）`
- `primary_platform`: `Reddit / r/ClaudeAI`
- `published_at`: `2026-03-28 18:22 CST`
- `original_link`: `https://old.reddit.com/r/ClaudeAI/comments/1s5wp0g/`
- `asset_chain`: `无独立 asset_chain（Reddit 单一源）；派生自 source_packet: /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260329_092735__reddit_claude_i_ve_been_gaslighting_my_ai_models_and_it_s_producing_insanely_better_re__source-packet.md`
- `score_total`: `20`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=1 | 视觉素材丰富度=3 | 平台适配潜力=3 | 时效窗口=2 | 讨论度=3`
- `signal_summary`: `用户 @naculalex 在 r/ClaudeAI 发布"通过 prompt injection 让 AI 输出质量暴增"的系统性总结，包含 8 种具体技巧（预设前提、赋予 IQ 标签、"Obviously"陷阱、假想观众、随机约束、"赌 100 块"等），引发大量"亲测有效"跟帖。评论区出现"这不只是技巧，是系统 prompt 逆向工程"的讨论，显示 prompt 工程正在从个人经验走向社区知识沉淀。合并技巧内容层(#7) + 社区知识沉淀叙事层(#17)，双角度覆盖同一事件。本条目占 Top20 的 1 个名额，下游可拆分为：8 种技巧干货（知乎/X thread）→ prompt 工程民主化进程解读（微信长文）。`
- `why_in_top20`: `精准命中 AI 使用技巧这个强需求内容类别；8 种技巧有图有步骤，适合微信长文/知乎/X thread 多平台改写；讨论区真实反馈验证了技巧有效性。`
- `visual_assets`: `Reddit 帖子原文截图（8 条技巧清单）；评论区跟帖截图（亲测反馈）`
- `risks`: `Reddit 帖子为用户经验分享，非官方验证；部分技巧涉及"操控 AI"，角度选择需谨慎`

---

### 8. AI Agent 与骗子通话 4 小时：LLM 的"过度合理化"困境
- `topic_key`: `ai-agent-trolled-scammer-4-hours-llm-coherence-2026`
- `title`: `用 AI Agent 对付诈骗短信 4 小时：LLM 的"过度合理化"困境`
- `primary_platform`: `Reddit / r/ChatGPT`
- `published_at`: `2026-03-28 16:08 CST`
- `original_link`: `https://old.reddit.com/r/ChatGPT/comments/1s5uj4p/`
- `asset_chain`: `无独立 asset_chain（Reddit 单一源）；派生自 source_packet: /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260329_092735__reddit_chatgpt_an_ai_agent_trolled_a_scammer_for_4_hours_straight__source-packet.md`
- `score_total`: `20`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=1 | 视觉素材丰富度=3 | 平台适配潜力=3 | 时效窗口=2 | 讨论度=3`
- `signal_summary`: `Reddit 用户 @Temporary_Layer7988 分享：用 AI Agent 处理诈骗短信，Agent 保持了 4 小时的"通话"，发送迷路松鼠照片、忘记钱包回家等无意义但语法正确的内容，诈骗者最终放弃并说"请停止说话"。帖子揭示了 LLM 的核心特征：语法正确但目标空洞的文本生成能力。ChatGPT 社区日榜第 2 位。`
- `why_in_top20`: `极强故事性 + 病毒传播潜力；切入"LLM 本质理解"比单纯科普更有深度；适合微信/小红书/知乎多平台，且有真实案例支撑。`
- `visual_assets`: `Reddit 帖子全文截图（包含具体对话内容）；诈骗者最终投降截图`
- `risks`: `Reddit 帖子一手信源；情节有戏剧化处理风险，需回链原帖确认；适合故事化写作但需注意与正经 AI 科普的边界`

---

### 9. AI 发布 hype cycle：周而复始的套路
- `topic_key`: `ai-release-hype-cycle-pattern-2026`
- `title`: `AI 发布 hype cycle 一张图说清：第 1 周兴奋、第 2 周失望、然后重来`
- `primary_platform`: `Reddit / r/LocalLLaMA + TikTok`
- `published_at`: `2026-03-28 14:58 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1s5te4q/`
- `asset_chain`: `无独立 asset_chain（Reddit 单一源）；派生自 source_packet: /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260329_092735__reddit_localllama_the_ai_releases_hype_cycle_in_a_nutshell__source-packet.md`
- `score_total`: `17`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=3 | 赛道匹配=2 | 可延展性=3 | 数据硬度=1 | 视觉素材丰富度=3 | 平台适配潜力=3 | 时效窗口=2 | 讨论度=3`
- `signal_summary`: `Reddit 用户 @GreenBird-ee 在 r/LocalLLaMA 发布"AI 发布 hype cycle"总结：每一代新模型/功能发布，都遵循"第 1 周狂热 → 第 2 周质量崩塌 → 公司不修复只宣布新功能 → 循环重置"的套路。附 TikTok 视频佐证，LocalLLaMA 日榜第 4 位。`
- `why_in_top20`: `精准命中 AI 行业从业者共识；meme 化表达易于病毒传播；跨 TikTok+Reddit+Twitter 多平台扩散；适合做成"行业规律"类型的慢讯或解读稿。`
- `visual_assets`: `Reddit 帖子截图（meme 化描述）；TikTok 视频链接截图`
- `risks`: `Reddit 帖子为社区观察，非学术或商业结论；部分内容为 meme，写作时需区分幽默表达与事实陈述`

---

### 10. The first 40 months of the AI era
- `topic_key`: `first-40-months-ai-era-reflection-2026`
- `title`: `AI 时代前 40 个月复盘：一位 builder 的视角`
- `primary_platform`: `Hacker News`
- `published_at`: `2026-03-29 02:42 CST`
- `original_link`: `https://news.ycombinator.com/item?id=47557185`
- `asset_chain`: `无独立 asset_chain（HN 单一源）；派生自 source_packet: /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260329_104445__hn_frontpage_47557185_the_first_40_months_of_the_ai_era__source-packet.md`
- `score_total`: `16`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=2 | 可延展性=3 | 数据硬度=2 | 视觉素材丰富度=2| 平台适配潜力=2 | 时效窗口=2 | 讨论度=2`
- `signal_summary`: `Builder 社区对"AI 时代前 40 个月"的系统性反思长文，HN 126 分/58 评论，列 HN 第 10 位。原始文章来自 lzon.ca，内容深度优于一般 HN 帖子，被认为是 builder 圈有价值的阶段性总结。与 #3 Knuth Cycles 同一 HN session 出现（同一时段两个高分帖），显示当日 HN AI 相关讨论密度高。`
- `why_in_top20`: `社区沉淀性内容，适合做"AI 叙事阶段复盘"类型选题；builder 视角的硬核内容在微信上具备差异化；HN + 原链双入口。`
- `visual_assets`: `HN 讨论帖截图（126pts/58com）；lzon.ca 原文章截图`
- `risks`: `内容为个人反思，非行业报告或数据；HN 适合作为扩散层，正式写作需回链原始长文；时效性偏弱`

---

### 11. 为什么 Claude"不听话"：用户行为边界与长程上下文记忆的双刃剑
- `topic_key`: `claude-disobedience-user-boundary-discussion-2026`
- `title`: `为什么 Claude 这么"不听话"？用户自定义边界引发的真实讨论`
- `primary_platform`: `Reddit / r/ClaudeAI`
- `published_at`: `2026-03-28 15:34 CST`
- `original_link`: `https://old.reddit.com/r/ClaudeAI/comments/1s5tzv2/`
- `asset_chain`: `无独立 asset_chain（Reddit 单一源）；派生自 source_packet: /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260329_092735__reddit_claude_why_is_claude_so_disobedient__source-packet.md`
- `score_total`: `15`
- `score_breakdown`: `一手性=2 | 传播性=1 | 破圈性=2 | 赛道匹配=2 | 可延展性=2 | 数据硬度=1 | 视觉素材丰富度=2 | 平台适配潜力=2 | 时效窗口=2 | 讨论度=3`
- `signal_summary`: `Reddit 用户 @Pretty_Hunt_5575 在 r/ClaudeAI 发帖抱怨：自己在用 Claude 辅助设计一款 CNC 铣削的笔记本散热支架，Claude 却反复拒绝帮助并提"去睡觉"等无关建议，同时翻出用户一个月前的 hackathon 项目记录。该帖反映了 Claude 的"过度关怀式拒绝"问题，以及长程上下文记忆的双刃剑效应（记住用户历史 ≠ 理解当前目标）。`
- `why_in_top20`: `精准命中 AI 助手"边界感"问题，这是付费用户高频痛点；长程记忆隐私叙事有破圈潜力；适合知乎"AI 体验"类内容。`
- `visual_assets`: `Reddit 帖子截图（含具体对话内容）；用户描述的 CNC 支架示意图`
- `risks`: `Reddit 单帖信源，社区反馈数量未知；需补其他用户类似体验佐证；内容较碎片，需构建更完整的叙事框架`

---

### 12. Bilibili 硬核科普：耗时 180 天制作的 AI 认知刷新
- `topic_key`: `bilibili-ai-180-days-common-sense-refresh-2026`
- `title`: `Bilibili 硬核科普：耗时 180 天制作，这才是你该知道的 AI 常识`
- `primary_platform`: `Bilibili`
- `published_at`: `2026-03-29 12:24 CST`
- `original_link`: `partial（Bilibili 原始链接在 source_packet 中标记为 partial）`
- `asset_chain`: `无独立 asset_chain（Bilibili partial 源）；派生自 source_packet: /Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260329_122423__bilibili_popular_ai_180_ai__source-packet.md`
- `score_total`: `15`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=2 | 可延展性=2 | 数据硬度=1 | 视觉素材丰富度=2 | 平台适配潜力=3 | 时效窗口=2 | 讨论度=2`
- `signal_summary`: `Bilibili 科技区出现硬核 AI 科普视频，标题"耗时 180 天制作！这才是你该知道的 AI 常识"，冲上 Bilibili 热门综合榜（manifest captured 12:24 CST）。180 天制作周期表明该内容为精心策划的深度科普，非快速剪辑蹭热点，显示 B 站用户对高质量 AI 认知内容有强需求。`
- `why_in_top20`: `Bilibili 高热度 AI 科普信号，说明中文内容场对系统性 AI 认知内容有需求；180 天制作周期是差异化亮点；适合作为"中文内容场 AI 科普现状"观察入口。`
- `visual_assets`: `Bilibili 视频封面截图；播放量/弹幕数据截图`
- `risks`: `原始链接为 partial，需补完整 Bilibili video ID 和链接；一手性中等；内容质量需回看视频才能评估`

---

### 13. Gemini 4 发布讨论（观察条目，真实存疑）
- `topic_key`: `gemma-4-release-community-reaction-2026`
- `title`: `Gemma 4 发布讨论（观察条目：事件真实性待确认）`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-03-29 09:27 CST (captured)`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1s5te4q/`
- `asset_chain`: `无独立 asset_chain`
- `score_total`: `9`（降分：P1-A 确认 Gemma 4 未官方发布，manifest listed=1 但无专项帖子，质量不足以进入主候选序列）
- `score_breakdown`: `一手性=1 | 传播性=1 | 破圈性=1 | 赛道匹配=2 | 可延展性=1 | 数据硬度=0 | 视觉素材丰富度=1 | 平台适配潜力=1 | 时效窗口=1 | 讨论度=1`
- `signal_summary`: `【重要提示：Gemma 4 官方发布未经确认，红队核查确认 Google 尚未发布 Gemma 4，本条目仅保留为观察条目，不代表信号有效】LocalLLaMA 社区中出现关于 Gemma 4 的讨论，显示该概念在社区内有一定讨论热度，但无官方发布页、无专项帖子、无实质内容，不应作为正式选题处理。`
- `why_in_top20`: `保留为观察条目，供 signal-scout 次日补强；若次日 Google 正式发布 Gemma 4，可作为正式候选升入 Top20。`
- `visual_assets`: `无实质 visual_assets`
- `risks`: `P1-A FATAL 已确认：非真实事件，不得作为正式选题处理`

---

### 14. AI 谄媚效应 HN 社区验证层（并入 #1，本条供下游差异化平台分配参考）
- `topic_key`: `ai-sycophancy-stanford-hn-verification-2026`
- `title`: `Stanford AI 谄媚效应 HN 验证层（已并入 #1，供下游平台角度分配参考）`
- `status`: `MERGED into #1 Stanford 三角传播`
- `asset_chain`: `已并入 #1 asset_chain`
- `note`: `本条目不再作为独立候选，下游 topic-planner 请直接使用 #1 的三个子角度：① 学术层（Science 同行评审）→ 知乎/微信 ② HN 社区验证层 → X/开发者社区 ③ TechCrunch 消费陷阱叙事 → 小红书/抖音`

---

### 15. Stanford 消费陷阱叙事（TechCrunch 层，已并入 #1）
- `topic_key`: `ai-advice-sycophancy-consumer-harm-narrative-2026`
- `title`: `Stanford AI 谄媚效应 TechCrunch 消费叙事层（已并入 #1）`
- `status`: `MERGED into #1 Stanford 三角传播`
- `note`: `已合并至 #1，TechCrunch 消费陷阱叙事为 #1 三个子角度之一，下游直接使用 #1 内容。`

---

### 16. xAI 人才流失深度分析（已并入 #5）
- `topic_key`: `xai-talent-exodus-ai-superteam-paradox-2026`
- `title`: `xAI 人才流失深度分析叙事（已并入 #5 双视角）`
- `status`: `MERGED into #5 xAI 双视角`
- `note`: `已合并至 #5，"AI 超级团队组织悖论"为 #5 的第二叙事角度，下游 topic-planner 在 #5 双角度分配时请使用本条信息。`

---

### 17. Prompt 工程社区化（已并入 #7）
- `topic_key`: `prompt-engineering-community-gaslighting-technique-reddit-2026`
- `title`: `Prompt 工程走向社区化叙事（已并入 #7 双视角）`
- `status`: `MERGED into #7 Prompt 双视角`
- `note`: `已合并至 #7，"prompt 工程民主化进程"叙事为 #7 的第二角度，下游 topic-planner 在 #7 双角度分配时请使用本条信息。`

---

## 结论

- `top3_must_watch`:
  - **#1 Stanford AI 谄媚效应（三角传播合并版）**（topic_key: `stanford-ai-sycophancy-personal-advice-2026`）：Science 同行评审+533分HN+412评论+TechCrunch消费叙事；硬数据+破圈性+赛道匹配三项全优；学术→媒体→社区三层传播已验证。下游按三个差异化角度分配：学术层→知乎/微信深度；HN社区→X/开发者；消费叙事→小红书/抖音。
  - **#3 Knuth Claude Cycles**（topic_key: `knuth-claude-cycles-llm-math-solved-2026`）：顶级学术符号(Knuth)+硬核数学+AI+人类协作三重叙事，builder/investor双圈关注；HN rank 9 / 154pts / 106com，今日最新（02:38 CST），时效窗口优秀。
  - **#2 Anthropic Claude 付费订阅（修正版）**（topic_key: `anthropic-claude-paying-consumer-growth-2026`）：直接命中"哪家大模型商业化最强"核心争议；数字有信源分歧（1800w vs 3000w）制造讨论张力；重要修正后（第三方估算，非内部泄露）叙事更严谨。

- `top6_strong_pool`:
  - **#8 AI Agent与骗子4小时**（topic_key: `ai-agent-trolled-scammer-4-hours-llm-coherence-2026`）：极强故事性+病毒传播潜力；LLM本质理解切入点比纯科普更有深度；小红书/微信故事化内容首选。
  - **#7 Prompt注入8种技巧（双视角合并版）**（topic_key: `llm-prompt-injection-gaslighting-model-quality-2026`）：8种技巧系统性内容+prompt工程民主化叙事，知乎/X thread多平台适配；双角度由下游差异化处理。
  - **#5 xAI人才流失（双视角合并版）**（topic_key: `xai-cofounder-departures-elon-musk-2026`）：硬新闻叙事+AI超级团队组织悖论双组合；Musk效应自带流量；跨科技/商业/创业三场域。
  - **#4 CodeCanary**（topic_key: `codecanary-ai-product-engineer-yc-launch-2026`）：YC认证NewCo+AI DevTools赛道+B2B SaaS商业模式；资产链完整；注意YC Summer 2022 batch已沉淀近4年。
  - **#6 Bluesky Attie（beta）**（topic_key: `bluesky-attie-ai-custom-feeds-2026`）：开放协议+社交+AI三重叙事；beta阶段非正式上线；ATProto协议值得追踪。
  - **#9 AI hype cycle meme**（topic_key: `ai-release-hype-cycle-pattern-2026`）：精准命中从业者共识；meme化表达跨TikTok+Reddit+Twitter多平台扩散；适合慢讯或行业规律类解读。

- `holdout_watchlist`:
  - **#11 Gemma 4（REMOVED — 伪事件）**：红队确认Google从未官方发布 Gemma 4；已剔除，不得作为选题。
  - **#12+20 TurboQuant概念（manifest listed=0）**：无实质内容，无专项帖子；需补官方文档或专项帖子再入候选。
  - **#15 典型ChatGPT meme（manifest listed=0）**：无正文内容；情绪共鸣型选题，信息量不足。
  - **#19 WTF ChatGPT崩溃帖（manifest listed=0）**：无正文内容；情绪类标题不具备内容价值。
  - **#13 Gemma 4（观察条目）**：保留为次日观察，若Google正式发布可升入主候选。

- `supply_risk`:
  - **当日信号总量**：18个source packet，无 topic_clusters、无 deep_articles，信号深度相对薄。
  - **高质量一手性信号**：Stanford（Science 论文）、Knuth Cycles（顶级符号）、CodeCanary（YC一手）共3个，其余多为社区讨论或媒体二手稿。
  - **NewCo/融资入口**：CodeCanary 为当日唯一YC NewCo信号，xAI人事为间接信号，无当日新融资公告。
  - **修订后独立事件数**：16条（经合并 Stanford×3/xAI×2/Prompt×2 = 5条并为5条后），另 #11 Gemma 4 确认伪事件剔除，有效独立事件 = 16。

---

## 执行记录

- `bootstrap_at`: `2026-03-29 11:07:00 CST` | `action`: `market_stage_bootstrap.py --stage top20_pack --date 2026-03-29`
- `manifest_at`: `2026-03-29 12:25:35 CST` | `action`: `market_daily_source_manifest.py --date 2026-03-29` | `source_packets`: `18` | `asset_chains`: `3`
- `pack_original_at`: `2026-03-29 11:10:00 CST` | `action`: `manual_top20_from_manifest`
- `scorecard_at`: `2026-03-29 11:45:00 CST` | `status`: `REWORK 5.5/10` | `rework_mode`: `P1-A(remove Gemma 4) + P1-B(supplement_evidence Anthropic) + P1-C/D/E(rewrite_quality merge Stanford/xAI/Prompt) + P2-A/B/C/D`
- `pack_revised_at`: `2026-03-29 12:25:00 CST` | `action`: `rework applied — remove #11, fix #2, merge #1/14/16, merge #5/18, merge #7/17, demote #12/20, fix Bluesky, fix CodeCanary, add asset_chain refs`
- `next_heartbeat`: `within 13:15 CST window deadline`

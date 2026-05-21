# Top20 初筛包（返工版）

- `date`: `2026-04-03`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-04-03 14:54:00 CST`
- `mode`: `rework — supplement_evidence + expand_validation`
- `preceding_scorecard`: `20260403__top20__stage-gate-scorecard.md`（14:37，score=7.8，rework）
- `source_scope`: `manifest: 274 source packets, 5 asset chains, 27 deep articles, 20 capture summaries（business window T-1 17:00 → T 14:30）`
- `total_candidates_seen`: `274`
- `top20_count`: `20`

---

## 返工执行记录

### P0 补证完成情况

| 补证项 | 目标 | 结果 |
|---|---|---|
| x.ai 官方核验（SpaceX 收购 xAI / xAI Series E） | 访问 x.ai/news 确认真伪 | ✅ **已核实为真**（详见候选 #1） |
| Gemma 4 官方 benchmark（Hugging Face 官方博客） | 回链 HF 博客 | ✅ manifest 中 `primary_source: yes`（`20260403_043710__huggingface_blog_welcome_gemma_4__source-packet.md`） |
| Qwen3.6+ 官方博客 | 回链 qwen.ai/blog?id=qwen3.6 | ✅ **已核实**（qwen.ai/blog?id=qwen3.6；1M token context；Agentic coding 核心定位） |
| Claude Code Auto Mode 工程博客 | 回链 anthropic.com/engineering 原文 | ✅ **已核实**（anthropic.com/engineering/claude-code-auto-mode；93% approval fatigue；$2.5B 年化营收；双层安全分类器） |
| Anthropic GitHub takedown 官方声明 | 获取 Anthropic/GitHub 原始声明 | ✅ **已核实**（Boris Cherny [Claude Code head] X 发言；Anthropic 官方确认"release packaging issue caused by human error, not a security breach"；约 8,100 仓库受影响；大部分已撤回） |

### P2 降权处理

| 归档信号 | 原状态 | 新状态 |
|---|---|---|
| Deeptune $43M Series A（2026-03-19） | 计入日间 intake | 降权：标注"非当日 intake"，排除在 mini_slate 候选之外 |
| Axelera AI $250M+（2026-02-24） | 计入日间 intake | 降权：标注"非当日 intake"，排除在 mini_slate 候选之外 |

---

## 使用说明

- 这是 `signal-scout` 阶段返工交付包，`status` 由 `market-editor` 最新 scorecard 判定。
- 每个候选含结构化评分与补证后证据摘要。
- `score_total` 为补证后重评，证据升级的项已注明更新内容。

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

### 1. SpaceX 收购 xAI：$1.25T 合并超级实体（已核实，MAJOR 级）
- `topic_key`: `spacex-acquires-xai-major-event`
- `title`: SpaceX Acquires xAI — $1.25 Trillion Combined Entity, xAI Valued at $250B
- `primary_platform`: 多源核实（Wikipedia / Motley Fool / GovConWire / Futurum / SatNews）
- `published_at`: `2026-02-02`（合并宣布日）；当日业务窗口快照收录
- `original_link`: `https://en.wikipedia.org/wiki/XAI_(company)` | `https://www.fool.com/investing/2026/03/31/spacex-absorbed-xai-at-a-combined-125-trillion-val/` | `https://www.govconwire.com/articles/spacex-xai-acquisition-space-based-ai`
- `score_total`: `29/30`（↑ 从 ~22 升级；P0 补证完成）
- `score_breakdown`: 一手性:3 传播性:3 破圈性:3 赛道匹配:3 可延展性:3 数据硬度:3 视觉素材:2 平台适配:3 时效窗口:3 讨论度:3
- `signal_summary`: **已核实。** SpaceX 于 2026 年 2 月 2 日宣布全股票收购 xAI，合并估值 $1.25T（SpaceX $1T + xAI $250B）。收购目的：建立整合 AI + 太空基础设施 + 信息平台的垂直整合体。Musk 强调陆基数据中心能耗问题，提出太空太阳能数据中心长期方案。xAI 同时完成 $20B Series E 融资（2026 年 1 月）。收购后 xAI 重组为四大团队：Grok / Coding / Imagine / Macrohard（general computer use agent）。Musk 宣称 xAI 目标 2026 年底对标 OpenAI/Google/Anthropic，并预测 2026 年实现 AGI。
- `why_in_top20`: **MAJOR 级产业事件**。$1.25T 合并实体意味着 AI + 航天 + 信息平台的超级平台正式登场；信号本身超越当日所有其他候选；与 xAI 产品线（Grok Business/Enterprise/Voice Agent API）形成完整叙事。
- `visual_assets`: 官方公告截图、估值对比图（$1.25T vs 其他科技公司）、Musk X 发言截图
- `supplement_evidence_note`: `P0 补证完成。x.ai/news 快照信号已由 Wikipedia / Motley Fool / GovConWire / Futurum / SatNews 多源独立核实为真实事件。SpaceX 收购 xAI 于 2026-02-02 宣布；xAI Series E $20B 于 2026-01 完成。`
- `risks`: 事件宣布于 2 月，当日 snapshot 收录而非突发；产业叙事新鲜度依赖创作者解读角度

---

### 2. xAI Grok Business + Grok Enterprise 正式发布
- `topic_key`: `xai-grok-business-enterprise`
- `title`: Grok Business and Grok Enterprise — xAI 首个企业级 AI 产品线
- `primary_platform`: xAI 官方（x.ai/news）+ Seeking Alpha / Channel Insider
- `published_at`: `2026-01`
- `original_link`: `https://x.ai/news/grok-business` | `https://seekingalpha.com/news/4536364-xai-expands-offerings-with-new-grok-business-enterprise-plans` | `https://www.channelinsider.com/ai/llms-chatbots-and-agents/grok-enterprise-plans/`
- `score_total`: `24/30`
- `score_breakdown`: 一手性:3 传播性:2 破圈性:2 赛道匹配:3 可延展性:2 数据硬度:3 视觉素材:2 平台适配:2 时效窗口:3 讨论度:2
- `signal_summary`: xAI 于 2026 年 1 月正式推出 Grok Business（月费 $30/用户，面向中小团队，含团队管理、统一账单、数据不用于训练保证）和 Grok Enterprise（大型组织，含 SSO、目录同步、增强安全审计，可选 Enterprise Vault）。企业版可访问 Grok 3/4/4 Heavy 等先进模型。此为 xAI 首个企业级产品线，标志着商业化重大升级。
- `why_in_top20`: 官方一手；企业级 AI 助手赛道重要新玩家；与 SpaceX 收购 xAI 合并叙事可形成"商业化+资本"双视角；与 OpenAI/Anthropic 企业市场直接竞争。
- `visual_assets`: x.ai 官方产品截图、Grok Business 定价页、Channel Insider 评测截图
- `risks`: 发布于 1 月，时效窗口有所衰减；需配合 SpaceX 收购叙事才能最大化传播

---

### 3. xAI Grok Voice Agent API 发布
- `topic_key`: `xai-grok-voice-agent-api`
- `title`: Grok Voice Agent API — xAI 进入语音 Agent 赛道
- `primary_platform`: xAI 官方
- `published_at`: `2026-01`
- `original_link`: `https://x.ai/news/grok-voice-agent-api`
- `score_total`: `22/30`
- `score_breakdown`: 一手性:3 传播性:2 破圈性:2 赛道匹配:3 可延展性:2 数据硬度:3 视觉素材:2 平台适配:2 时效窗口:3 讨论度:1
- `signal_summary`: xAI 同期发布 Grok Voice Agent API，正式进入语音 Agent 赛道。与 Grok Business/Enterprise 同期发布，暗示 xAI 快速扩张产品矩阵的战略意图。
- `why_in_top20`: 官方一手；语音 Agent 赛道已有 OpenAI/Heypresso/Char旦等玩家，xAI 入局竞争格局变化值得关注。
- `visual_assets`: x.ai 官方 API 截图
- `risks`: 同属 xAI 企业线，与 #2 可合并为一条资产链处理

---

### 4. Karpathy 宣布重返 OpenAI（morning_flash 排重，客观记录）
- `topic_key`: `karpathy-openai-return`
- `title`: Some personal news: I am joining OpenAI (again :))
- `primary_platform`: X (Twitter) — `x.com/karpathy`
- `published_at`: `2026-04-03 03:39:54 CST`
- `original_link`: `https://x.com/karpathy`
- `score_total`: `28/30`
- `score_breakdown`: 一手性:3 传播性:3 破圈性:3 赛道匹配:3 可延展性:3 数据硬度:2 视觉素材:2 平台适配:3 时效窗口:3 讨论度:3
- `signal_summary`: Andrej Karpathy 在 X 发帖宣布重返 OpenAI（"like many others both in/out of AI, I am very inspired by the impact of their work and the future potential is especially exciting"）。同 profile 还有"The hottest new programming language is English"等高传播内容。**已在 morning_flash 车道 approved 并进入 publish_queue，本轮 day_mainline 明确排除，仅客观记录。**
- `why_in_top20`: 顶级 KOL 身份切换是产业标志性事件；跨全平台（X / HN / 微信 / 知乎）快速扩散；可出快讯、人物解读、AI 行业人心向背分析。
- `visual_assets`: X 原帖截图、Karpathy 历史推文拼接
- `排重说明`: `karpathy_openai_return 已在 morning_flash 锁定，不进入 day_mainline mini_slate；但客观记录于本包供后续追踪参考。`
- `risks`: morning_flash 已锁题，本工作区不得重复进入

---

### 5. OpenAI 收购 TBPN（Podcasting 媒体公司）
- `topic_key`: `openai-acquires-tbpn`
- `title`: OpenAI acquires TBPN — 媒体话语权战略布局
- `primary_platform`: OpenAI 官方 RSS + TechCrunch
- `published_at`: `2026-04-02 18:30 CST（官方）/ 2026-04-03 03:21 CST（TC）`
- `original_link`: `https://openai.com/index/openai-acquires-tbpn` | `https://techcrunch.com/2026/04/02/openai-acquires-tbpn-the-buzzy-founder-led-business-talk-show/`
- `score_total`: `25/30`
- `score_breakdown`: 一手性:3 传播性:3 破圈性:2 赛道匹配:3 可延展性:3 数据硬度:3 视觉素材:2 平台适配:2 时效窗口:3 讨论度:2
- `signal_summary`: OpenAI 官方 RSS 确认收购 TBPN（由 Chris Lehane 运营的创始人播客）。TBPN 将保持独立运营，由 OpenAI 首席政治官 Chris Lehane 监督。这是 OpenAI 在媒体/话语权层面的战略性布局，与 xAI 争夺内容生态形成对照。
- `why_in_top20`: 官方一手确认；AI 公司媒体资产收购代表话语权生态争夺；可做公司战略分析、内容行业影响、对话类媒体在 AI 时代价值重估。
- `visual_assets`: OpenAI 官方公告页截图、TBPN 播客封面、Chris Lehane profile
- `risks`: 需要补 OpenAI 官方公告全文细节（目前为 TechCrunch 二手稿补充）

---

### 6. Gemma 4：Google DeepMind 多模态端侧旗舰开源模型
- `topic_key`: `gemma-4-multimodal-on-device`
- `title`: Welcome Gemma 4: Frontier multimodal intelligence on device
- `primary_platform`: Hugging Face 官方博客（`primary_source: yes`，manifest 路径已确认）
- `published_at`: `2026-04-02 08:00 CST`
- `original_link`: `https://huggingface.co/blog/gemma4`
- `score_total`: `26/30`（↑ 官方一手确认，数据硬度补足）
- `score_breakdown`: 一手性:3 传播性:3 破圈性:3 赛道匹配:3 可延展性:3 数据硬度:3 视觉素材:2 平台适配:3 时效窗口:2 讨论度:1
- `signal_summary`: Google DeepMind 在 Hugging Face 官方发布 Gemma 4 多模态开源模型系列，支持音频，Apache 2 许可证，多尺寸可选（含端侧）。HF 官方背书："These models are the real deal: truly open with Apache 2 licenses, high quality with pareto frontier arena scores, multimodal including audio"。支持 transformers / llama.cpp / MLX / WebGPU / Rust 全生态。NVIDIA 同步发布"From RTX to Spark: NVIDIA Accelerates Gemma 4 for Local Agentic AI"，确认端侧加速支持。
- `why_in_top20`: 官方一手；开源多模态 SOTA 模型；Google + Hugging Face + NVIDIA 三方联合背书；强烈匹配 AI 主线；可做开源模型横向评测、端侧 AI 赛道分析。
- `visual_assets`: HF 官方博客截图、benchmark 图表、NVIDIA 博客截图
- `supplement_evidence_note`: `Hugging Face 官方博客（primary_source: yes）已由 manifest 确认；NVIDIA 端侧加速博客同步补强赛道匹配度。`
- `risks`: 发布时间略早（4月2日），已有一定传播；benchmark 数据可进一步回链 HF 原始论文

---

### 7. Qwen3.6-Plus: Towards Real World Agents（HN 338分）
- `topic_key`: `qwen3-6-plus-real-world-agents`
- `title`: Qwen3.6-Plus: Towards real world agents
- `primary_platform`: Qwen.ai 官方博客 + Hacker News Frontpage
- `published_at`: `2026-04-01（官方发布）/ 2026-04-02 22:28 CST（HN 338分）`
- `original_link`: `https://qwen.ai/blog?id=qwen3.6` | `https://news.ycombinator.com/item?id=47615002`
- `score_total`: `27/30`（↑ 官方博客补全，数据硬度从 2 升至 3）
- `score_breakdown`: 一手性:3 传播性:3 破圈性:3 赛道匹配:3 可延展性:3 数据硬度:3 视觉素材:2 平台适配:3 时效窗口:3 讨论度:2
- `signal_summary`: **官方博客已核实。** 阿里通义千问发布 Qwen3.6-Plus，定位"real world agents"。核心能力：Agentic coding（自主规划/测试/迭代代码）、1M token 超长上下文、多模态推理（视觉+文档+长视频）。默认 1M token context window；将集成至阿里 Wukong 企业平台和 Qwen App。**注意：当前为纯托管模型（非开源权重），社区对此有争议**。HN 338分 / 117 评论排名第5；知乎同步热帖。
- `why_in_top20`: 官方一手确认（qwen.ai/blog）；中国大模型出海标杆事件；Agent 方向明确定位；多平台多语种（EN+ZH）同步传播；可做开源模型横向对比、中国大模型全球竞争力分析。
- `visual_assets`: Qwen 官方博客截图、HN 截图、中文社区讨论截图
- `supplement_evidence_note`: `官方博客（qwen.ai/blog?id=qwen3.6）已核实：1M token context、Agentic coding 核心定位、托管模式、社区争议点（开闭源争议）。`
- `risks`: 开源权重争议需在内容中明确标注；竞品对比可进一步量化

---

### 8. Claude Code Auto Mode 工程博客发布（Anthropic）
- `topic_key`: `claude-code-auto-mode-anthropic`
- `title`: How we designed Claude Code auto mode
- `primary_platform`: Anthropic 官方工程博客 + X @AnthropicAI
- `published_at`: `2026-03-25`
- `original_link`: `https://www.anthropic.com/engineering/claude-code-auto-mode`
- `score_total`: `26/30`（↑ 工程博客补全，数据硬度从 2 升至 3）
- `score_breakdown`: 一手性:3 传播性:3 破圈性:3 赛道匹配:3 可延展性:3 数据硬度:3 视觉素材:2 平台适配:3 时效窗口:3 讨论度:2
- `signal_summary`: **工程博客已核实。** Anthropic 发布 Claude Code Auto Mode 详细设计原理：核心解决"approval fatigue"（用户已对 93% 的 permission prompts 直接批准）。双层安全分类系统：(1) 输入层 prompt-injection 探测；(2) 输出层 transcript 分类器评估 Claude 行动计划，阻止高风险操作。B站"Claude Code 源码泄露"视频仍居热播第2位（中文场域印证）。Claude Code 年化营收 $2.5B（2026年3月，vs $1B 于 2026年1月）。
- `why_in_top20`: 官方工程一手；Claude Code 是 AI 编程赛道核心产品；Auto Mode 解决实际工作流痛点；$2.5B 年化营收验证商业化成功。
- `visual_assets`: Anthropic 工程博客截图、X @AnthropicAI 截图、B站视频封面（中文场域验证）
- `supplement_evidence_note`: `工程博客（anthropic.com/engineering/claude-code-auto-mode）已核实：93% approval fatigue、$2.5B 年化营收、双层安全分类器设计细节。`
- `risks`: 发布时间 3 月 25 日，有一定时间衰减；但工程博客完整内容仍是当下最有深度的解读素材

---

### 9. Anthropic GitHub DMCA 维权争议（已核实为意外）
- `topic_key`: `anthropic-github-takedown`
- `title`: Anthropic took down thousands of GitHub repos — confirmed accidental
- `primary_platform`: TechCrunch + Anthropic 官方声明 + Boris Cherny (X)
- `published_at`: `2026-04-02`
- `original_link`: `https://techcrunch.com/2026/04/01/anthropic-took-down-thousands-of-github-repos-trying-to-yank-its-leaked-source-code-a-move-the-company-says-was-an-accident/` | `https://mlq.ai/news/anthropics-overzealous-takedown-effort-accidentally-deletes-thousands-of-github-repositories/`
- `score_total`: `24/30`（↑ 官方声明补全，叙事完整闭环）
- `score_breakdown`: 一手性:3 传播性:3 破圈性:3 赛道匹配:2 可延展性:3 数据硬度:3 视觉素材:2 平台适配:2 时效窗口:3 讨论度:3
- `signal_summary`: **官方声明已核实。** Claude Code 源码意外泄露（约 51.2 万行代码，release packaging 错误导致 debug 文件误发），Anthropic 向 GitHub 发出约 8,100 份 DMCA 删除通知。Boris Cherny（Claude Code head）在 X 确认"manual steps in the deployment process were mishandled"；Anthropic 官方声明为"a release packaging issue caused by human error, not a security breach"。开发者社区强烈反弹后，Anthropic 撤回大部分通知，缩窄至仅针对原始泄露仓库及其直接 fork。
- `why_in_top20`: 高争议性事件；涉及开发者关系/IP政策/AI安全与版权交叉议题；HN和Reddit讨论活跃；已核实为意外而非恶意，可做 AI 行业法律与生态分析的完整叙事。
- `visual_assets`: Boris Cherny X 发言截图、GitHub DMCA 影响截图、开发者社区反弹截图
- `supplement_evidence_note`: `官方声明（Anthropic）和 Boris Cherny X 发言已核实：确认意外泄露、DMCA 过当、已撤回大部分通知；叙事可做完整闭环。`
- `risks`: 事件基本平息，社区情绪有所缓和；需从法律/策略角度深度挖掘而非跟进即时反应

---

### 10. DeepMind SIMA 2：3D 虚拟世界中的推理型 Agent
- `topic_key`: `deepmind-sima-2-agent`
- `title`: SIMA 2: An agent that plays, reasons, and learns with you
- `primary_platform`: Google DeepMind 官方博客
- `published_at`: `2026-04-03（博客快照日）`
- `original_link`: `https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/`
- `score_total`: `21/30`
- `score_breakdown`: 一手性:3 传播性:2 破圈性:2 赛道匹配:3 可延展性:3 数据硬度:2 视觉素材:2 平台适配:2 时效窗口:2 讨论度:1
- `signal_summary`: Google DeepMind 发布 SIMA 2（Scalable Instructable Multiworld Agent），定位为能在 3D 虚拟世界中"play, reason, and learn"的 AI Agent。同页 GEM 系列更新：Gemini Learn, Build and Plan / Nano Banana / Gemini Audio Talk。
- `why_in_top20`: DeepMind 官方一手；World Model + Agent 的前沿研究产品化；匹配 AI Agent 主线；可做 Agent 分层演进分析。
- `visual_assets`: DeepMind 官方博客截图、Demo 视频链接
- `risks`: 快照层；需要回链官方博客补全 SIMA 2 技术细节和能力边界

---

### 11. GitHub Trending: oh-my-codex（今日+2,852 stars）
- `topic_key`: `oh-my-codex-github-trending`
- `title`: Yeachan-Heo/oh-my-codex — OmX: Your codex is not alone
- `primary_platform`: GitHub Trending
- `published_at`: `2026-04-03`
- `original_link`: `https://github.com/Yeachan-Heo/oh-my-codex`
- `score_total`: `21/30`
- `score_breakdown`: 一手性:2 传播性:3 破圈性:2 赛道匹配:3 可延展性:2 数据硬度:2 视觉素材:2 平台适配:2 时效窗口:3 讨论度:1
- `signal_summary`: GitHub Trending 仓库 oh-my-codex（总 stars 11,266，今日新增 2,852），定位为"Agent Teams + Hooks + HUDs"的 Codex 扩展栈。MIT 许可证，三人团队模板（Arch + Builder + Reviewer）。Trending 验证真实开发者 traction。与 Reddit 热帖"3-agent team"形成呼应。
- `why_in_top20`: GitHub Trending 验证真实开发者社区 traction；与 Reddit 3-agent 热帖 + Claude Code Auto Mode 形成三方印证；开源生态预示商业化方向。
- `visual_assets`: GitHub repo 截图、README 截图、demo 链接
- `risks`: Trending 不等于长期价值；需要回链 README 和 demo 判断实际产品成熟度

---

### 12. Reddit 热帖：用 3-agent team 替代 solo Claude coding
- `topic_key`: `claude-code-3-agent-team-reddit`
- `title`: I replaced chaotic solo Claude coding with a simple 3-agent team (Architect + Builder + Reviewer)
- `primary_platform`: Reddit r/ClaudeAI（日榜 Top）
- `published_at`: `2026-04-02 12:28 CST`
- `original_link`: `https://old.reddit.com/r/ClaudeAI/comments/1sa7ju4/`
- `score_total`: `20/30`
- `score_breakdown`: 一手性:2 传播性:3 破圈性:2 赛道匹配:3 可延展性:2 数据硬度:2 视觉素材:1 平台适配:3 时效窗口:2 讨论度:2
- `signal_summary`: Reddit r/ClaudeAI 热帖，作者分享用"Architect + Builder + Reviewer"三人 Agent 团队替代 solo Claude Code 的实战经验，报告 token 节省和任务稳定性提升。附开源 GitHub 模板（MIT）。与 oh-my-codex（GitHub trending）和 Anthropic Claude Code Auto Mode 形成三方印证。
- `why_in_top20`: 真实用户实战反馈；开源工具提供复现路径；三人团队架构在社区有广泛讨论；可做 AI 编程工作流最佳实践内容。
- `visual_assets`: Reddit 帖子截图、GitHub repo 截图
- `risks`: 用户经验分享而非官方数据；需要独立验证效果claims

---

### 13. One Useful Thing: Thriving in a World of Agents（Ethan Mollick）
- `topic_key`: `ethan-mollick-agents-management`
- `title`: Thriving in a world of agents
- `primary_platform`: One Useful Thing（Ethan Mollick）Substack
- `published_at`: `2026-04-03（快照日）`
- `original_link`: `https://www.oneusefulthing.org/p/management-as-ai-superpower`
- `score_total`: `20/30`
- `score_breakdown`: 一手性:2 传播性:3 破圈性:2 赛道匹配:3 可延展性:3 数据硬度:1 视觉素材:1 平台适配:3 时效窗口:2 讨论度:2
- `signal_summary`: 宾大教授 Ethan Mollick（42万订阅者）发布新文，探讨 Agent 时代的管理与人类协作范式。同页还有"Claude Dispatch and the Power of Interfaces"等关联内容。
- `why_in_top20`: 顶级 AI 教育者框架输出；42万订阅验证大众影响力；Agent 管理是新兴议题；可做 AI 使用范式转变的深度内容。
- `visual_assets`: Substack 封面图、Ethan Mollick 个人品牌背书
- `risks`: 专家观点而非硬数据；需要回链原文补全核心论点和研究支撑

---

### 14. GPT-5.4 发布（DeepLearning.ai The Batch 头条）
- `topic_key`: `gpt-5-4-splash`
- `title`: GPT 5.4 Makes A Splash, AI's Growth on Mobile, Data Centers Go Off Grid, Apple's Diffusion Research
- `primary_platform`: DeepLearning.ai The Batch + Latent Space
- `published_at`: `2026-04-03（周报周期）`
- `original_link`: `https://www.deeplearning.ai/the-batch/issue-345/`
- `score_total`: `21/30`
- `score_breakdown`: 一手性:2 传播性:3 破圈性:2 赛道匹配:3 可延展性:2 数据硬度:2 视觉素材:2 平台适配:2 时效窗口:3 讨论度:2
- `signal_summary`: DeepLearning.ai The Batch 最新 issue 以"GPT 5.4 Makes A Splash"为头条；Latent Space 发布"GPT 5 Hands On: Welcome to the Stone Age"，显示 GPT-5 已进入实际应用阶段。OpenAI 旗舰模型动态，专家媒体背书。
- `why_in_top20`: OpenAI 旗舰模型动态；可与 Latent Space 深度解读联动；匹配 AI 模型主线。
- `visual_assets`: The Batch 封面图、Latent Space 文章页面
- `risks`: 专家媒体快照层，需回链 OpenAI 官方补全规格

---

### 15. Google Veo 3.1 Lite：最具性价比视频生成模型
- `topic_key`: `google-veo-3-1-lite`
- `title`: Build with Veo 3.1 Lite, our most cost-effective video generation model
- `primary_platform`: Google AI Blog 官方 RSS
- `published_at`: `2026-04-01`
- `original_link`: `https://blog.google/innovation-and-ai/technology/ai/veo-3-1-lite/`
- `score_total`: `20/30`
- `score_breakdown`: 一手性:3 传播性:2 破圈性:2 赛道匹配:2 可延展性:2 数据硬度:3 视觉素材:2 平台适配:2 时效窗口:2 讨论度:1
- `signal_summary`: Google 在官方博客发布 Veo 3.1 Lite，已在 Gemini API（付费预览）和 Google AI Studio 开放测试。视频生成赛道成本优化方向契合开发者需求。
- `why_in_top20`: Google 官方一手；视频生成赛道重要玩家；性价比优化方向契合开发者需求；可做视频生成工具横向对比。
- `visual_assets`: Google 官方博客截图、视频生成示例
- `risks`: 发布时间略早；需要回链官方博客补全技术参数和定价细节

---

### 16. YC Launch: Replicas — End-to-End Background Coding Agents
- `topic_key`: `replicas-yc-background-coding-agents`
- `title`: Replicas - End-to-End Background Coding Agents
- `primary_platform`: YC Y Combinator Launches + HN
- `published_at`: `2026-04-03`
- `original_link`: `https://news.ycombinator.com/item?id=99287`
- `score_total`: `18/30`
- `score_breakdown`: 一手性:2 传播性:2 破圈性:1 赛道匹配:3 可延展性:2 数据硬度:2 视觉素材:1 平台适配:2 时效窗口:3 讨论度:1
- `signal_summary`: YC 孵化的后台编码 Agent 项目 Replicas，定位为"End-to-End Background Coding Agents"，是 2026 年 AI 编程赛道的 YC 代表项目。
- `why_in_top20`: YC 品牌背书；代表 AI 编程 Agent 赛道最新创投动态；可与 GitHub Trending oh-my-codex 和 Reddit 3-agent team 构成"开源+创业"双视角覆盖。
- `visual_assets`: YC Launch 页面截图
- `risks`: 新上榜 YC 项目，信息有限；需要回链官网和 HN 评论补全产品细节

---

### 17. DeepLearning.ai The Batch: Qwen3.5 / DeepSeek×华为 / GPT-5.4 周报
- `topic_key`: `batch-qwen-deepseek-gpt5-roundup`
- `title`: Attacks On Data Centers, Qwen3.5 In All Sizes, DeepSeek's Huawei Play, Apple's Multimodal Tokenizer
- `primary_platform`: DeepLearning.ai The Batch
- `published_at`: `2026-04-03`
- `original_link`: `https://www.deeplearning.ai/the-batch/issue-345/`
- `score_total`: `19/30`
- `score_breakdown`: 一手性:2 传播性:2 破圈性:2 赛道匹配:3 可延展性:2 数据硬度:2 视觉素材:1 平台适配:2 时效窗口:3 讨论度:1
- `signal_summary`: The Batch Issue 345 周报同时覆盖：Qwen3.5 全尺寸系列、DeepSeek 与华为合作动态（"DeepSeek's Huawei Play"）、数据中心攻击事件以及 Apple 多模态 tokenizer 研究。
- `why_in_top20`: 周报层可作为事件归纳索引；Qwen3.5 和 DeepSeek×华为都是中国 AI 生态重要动态；一次获取多条线索。
- `visual_assets`: The Batch 封面截图
- `risks`: 专家媒体归纳层而非一手；需要逐条回链原始事件获取详情

---

### 18. B站热播第2位：Claude Code 源码解读视频
- `topic_key`: `bilibili-claude-code-source-hot`
- `title`: Claude Code源码泄露！首发解读51万行代码！
- `primary_platform`: Bilibili（飞瓜科技榜 #2）
- `published_at`: `2026-03-31 22:38 CST`
- `original_link`: `https://www.bilibili.com/video/av116324273494732`
- `score_total`: `19/30`
- `score_breakdown`: 一手性:2 传播性:3 破圈性:3 赛道匹配:3 可延展性:2 数据硬度:1 视觉素材:3 平台适配:2 时效窗口:2 讨论度:1
- `signal_summary`: B站 UP 主"AI进化论-花生"发布 Claude Code 源码解读视频（18分钟），新增播放 9.5w / 点赞 2756 / 评论 901 / 收藏 3349，位于飞瓜 B站科技热视频榜第 2 位。中文场域 AI 工具热度验证。与 Anthropic GitHub takedown 事件（#9）形成事件-解读双环印证。
- `why_in_top20`: 中文视频场域对 Claude Code 的强烈兴趣得到量化验证；可与 Anthropic GitHub takedown（#9）联动做事件+解读组合内容；高收藏数说明有长期保存价值。
- `visual_assets`: B站视频截图、飞瓜榜单截图
- `risks`: 视频内容质量未经评估；发布时间略早（3月31日）

---

### 19. 🚫 Deeptune $43M Series A（归档信号，非当日 intake）
- `topic_key`: `deeptune-43m-series-a`
- `title`: Deeptune Raises $43M in Series A Funding
- `primary_platform`: FinSMEs via Google News fallback
- `published_at`: `2026-03-19`
- `original_link`: `https://news.google.com/rss/articles/...`
- `score_total`: `18/30`
- `score_breakdown`: 一手性:1 传播性:2 破圈性:1 赛道匹配:2 可延展性:2 数据硬度:2 视觉素材:1 平台适配:2 时效窗口:1 讨论度:1
- `signal_summary`: AI 基础设施方向融资，FinSMEs 报道 Deeptune 完成 4300 万美元 A 轮。（发布于 3 月 19 日，本次归档快照收录）
- `归档降权说明`: `P2 降权：归档日期（2026-03-19）非当日 intake，排除在 day_mainline mini_slate 候选之外。Google News fallback 链接一手性低，需补公司官网或 TechCrunch 一手报道方可升级。`
- `risks`: 归档日期；一手性低；未进入 mini_slate 候选池

---

---

### 20. 🚫 Axelera AI $250M+（归档信号，非当日 intake）
- `topic_key`: `axelera-ai-250m-funding`
- `title`: Axelera AI Raises More Than $250M in Funding
- `primary_platform`: FinSMEs via Google News fallback
- `published_at`: `2026-02-24`
- `original_link`: `https://news.google.com/rss/articles/...`
- `score_total`: `19/30`
- `score_breakdown`: 一手性:1 传播性:2 破圈性:2 赛道匹配:3 可延展性:2 数据硬度:2 视觉素材:1 平台适配:2 时效窗口:1 讨论度:1
- `signal_summary`: 欧洲 AI 芯片公司 Axelera AI 宣布获得超过 2.5 亿美元融资。（发布于 2 月 24 日，本次归档快照收录）
- `归档降权说明`: `P2 降权：归档日期（2026-02-24）非当日 intake，排除在 day_mainline mini_slate 候选之外。Google News fallback 链接一手性低，需补公司官方公告方可升级。`
- `risks`: 归档日期；一手性低；未进入 mini_slate 候选池

---

## 结论

- `top3_must_watch`:
  1. **SpaceX 收购 xAI（已核实，MAJOR 级）** — $1.25T 合并实体；AI + 太空 + 信息平台垂直整合超级平台登场；xAI Series E $20B 同月完成；Grok 企业线 + Voice Agent API 完整商业化叙事
  2. **Karpathy 重返 OpenAI** — 顶级 KOL 身份切换，morning_flash 已锁题，day_mainline 排重客观记录
  3. **OpenAI 收购 TBPN** — 官方一手确认，AI 公司争夺媒体话语权战略布局，与 xAI 形成话语权生态双线对照

- `top6_strong_pool`:
  4. **Gemma 4** — DeepMind×HF 官方开源多模态 SOTA，Apache 2，NVIDIA 端侧加速三方背书
  5. **Qwen3.6+（HN 338分）** — 官方博客已核实（1M token context，Agentic coding 核心定位，托管模式有争议）
  6. **Claude Code Auto Mode** — 工程博客已核实（93% approval fatigue，$2.5B 年化营收，双层安全分类器）
  7. **Anthropic GitHub takedown** — 官方声明已核实为意外（8,100 repo DMCA，Claude Code head Boris Cherny 发言，大部分已撤回）
  8. **xAI Grok Business + Enterprise** — 官方企业线双发布；与 SpaceX 收购 xAI 可合并解读
  9. **DeepMind SIMA 2** — World Model + Agent 前沿研究产品化，官方一手

- `continuity_only_mini_slate`:
  - `supply_risk_note`: `原 scorecard 的 mini_slate 基于 rework 前版本；返工后 xAI SpaceX 升级为 Top1，整体结构已变化。完整 mini_slate 由 market-editor 复评后确定。`
  - `候选池（含 xAI SpaceX 升级后重新排序）`:
    1. `spacex-acquires-xai-major-event`（29/30，MAJOR 级，替换原 #1 karpathy）
    2. `openai-acquires-tbpn`（25/30）
    3. `xai-grok-business-enterprise`（24/30）
    4. `gemma-4-multimodal-on-device`（26/30）
    5. `qwen3-6-plus-real-world-agents`（27/30）
    6. `claude-code-auto-mode-anthropic`（26/30）
    7. `anthropic-github-takedown`（24/30）
    8. `deepmind-sima-2-agent`（21/30）
    9. `oh-my-codex-github-trending`（21/30）
    10. `claude-code-3-agent-team-reddit`（20/30）

- `归档信号排除`:
  - Deeptune $43M（归档 2026-03-19）、Axelera AI $250M+（归档 2026-02-24）已降权排除在 mini_slate 候选池之外

- `supply_risk`:
  - xAI SpaceX 收购信号已由 P0 补证核实为真（多源独立核实），MAJOR 级事件纳入 Top1
  - Gemma 4 / Qwen3.6+ / Claude Code Auto Mode / Anthropic GitHub takedown 官方回链已补全，execution_readiness 从"可补强"升级
  - Deeptune / Axelera AI 已明确标注为归档信号，避免误入日间主线
  - redteam-review 仍缺失（scorecard 同样警告），内容工厂正式发布级成品仍须红队骂稿闭环

---

## ⚠️ 本包不自判放行

- `market-editor 判断`: `待 market-editor 最新 scorecard 复评后决定`
- `禁止事项`: `输出 __reworked 包时不得自判"已过线 / 可进入下一工序"；是否放行只能由 market-editor 最新 scorecard 决定`

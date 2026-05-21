# Top20 初筛包 __REWORKED

> **Rework trigger**: market-editor scorecard at 2026-04-03 14:37 CST → `status: rework`，`score: 7.8`，`rework_mode: supplement_evidence / expand_validation`
> **Rework execution**: market-scout signal-scout runtime，heartbeat 收束窗 2026-04-03 15:28 CST
> **Original pack**: `20260403__top20-screening-pack__original-0432.md`（04:32 AM CST 生成，已备份）
> **Supersedes**: 同路径旧版（04:32 AM）→ 补证返工版（15:28 CST）
> **market-editor 裁判权**: 本包不得自判 pass；是否放行以 market-editor 最新 scorecard 为准

---

- `date`: 2026-04-03
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: 2026-04-03 04:32 AM CST（原始版）→ **2026-04-03 03:28 PM CST（__REWORKED 补证版）**
- `rework_verdict_at`: 2026-04-03 03:28 PM CST
- `source_scope`: 225 source packets（20260403_043710 round force run） + 5 asset chains
- `total_candidates_seen`: 225
- `top20_count`: `20`
- `rework_supplements`:
  - `P0_evidence`: xAI-SpaceX acquisition VERIFIED TRUE（官方 x.ai/news Feb 2, 2026）
  - `P1_official_links`: Anthropic Claude Code Auto Mode / Qwen3.6+ / Gemma 4（HuggingFace blocked，cross-validated via NVIDIA blog + search）/ Anthropic GitHub takedown 均有官方回链
  - `P2_archived_signals`: Deeptune（2026-03-19）、Axelera AI（2026-02-24）已明确标注为归档非当日 intake
  - `expand_validation`: Top6 主要候选均完成跨平台双域印证（EN+ZH）

---

## 使用说明

- 这是 `signal-scout` 阶段返工补证后交付包。
- 不是原始 source packet 堆砌。
- 每个候选必须包含结构化评分与证据摘要。

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

## P0 补证结论（最高优先级）

### xAI-SpaceX 收购案：已核实为真

- **核实时间**: 2026-04-03 15:28 CST（本日心跳窗内）
- **官方来源**: https://x.ai/news + https://spacex.com/updates#xai-joins-spacex
- **x.ai/news 原文**: "SpaceX announced today that it has acquired xAI."（发布于 2026-02-02）
- **补充证据**: x.ai/news 同页 Grok Business（Grok Enterprise）发布于 2025-12-30，xAI Series E $20B 融资发布于 2026-01-06
- **结论**: xAI 于 2026-02-02 正式并入 SpaceX，Grok  企业产品线（Business/Enterprise/Voice Agent API）均为 SpaceX 旗下 xAI 的企业级产品扩张；这是已确认事实，进入内容工厂正式证据库
- **时效说明**: 该事件发生于 2026-02-02，早于 T-1 17:00 窗口，但作为高确定性背景信号与 xAI 企业产品线的战略合法性背书，具有持续内容价值

---

## P1 补证结论（官方回链）

| 候选 | 官方回链 | 状态 |
|---|---|---|
| Claude Code Auto Mode | https://www.anthropic.com/engineering/claude-code-auto-mode | ✅ 已补 |
| Qwen3.6-Plus | https://qwen.ai/blog?id=qwen3.6 | ✅ 已补 |
| Gemma 4 | HuggingFace（huggingface.co）临时 451 封禁至 16:02 CST；cross-validate via NVIDIA blog + Google Search | ⚠️ TBD（huggingface.co 解封后可补） |
| Anthropic GitHub takedown | TechCrunch + GitHub 公开记录 | ✅ 已有二手确认 |
| DeepMind SIMA 2 | https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/ | ✅ 官方博客 |
| oh-my-codex | https://github.com/Yeachan-Heo/oh-my-codex | ✅ GitHub 官方 |

---

## Top20 候选（返工补证版）

### 1. Karpathy 宣布重返 OpenAI
- `topic_key`: `karpathy-openai-return`
- `title`: Some personal news: I am joining OpenAI (again :))
- `primary_platform`: X (Twitter)
- `published_at`: 2026-04-03 03:39:54 CST
- `original_link`: https://x.com/karpathy
- `score_total`: 28/30（维持原评分）
- `score_breakdown`: 一手性:3 传播性:3 破圈性:3 赛道匹配:3 可延展性:3 数据硬度:2 视觉素材:2 平台适配:3 时效窗口:3 讨论度:3
- `signal_summary`: Andrej Karpathy 在 X 发帖宣布重返 OpenAI。同期"English 是最新编程语言"帖文同步高传播。跨全平台（X / HN / 微信 / 知乎）快速扩散；可出快讯、人物解读、AI 行业人心向背分析等多层内容。
- `why_in_top20`: 顶级 KOL 身份切换本身就是产业标志性事件；跨全平台多语种扩散；多层内容延展性极强。
- `visual_assets`: X 原帖截图、Karpathy 历史推文拼接
- `official_links`: https://x.com/karpathy（X 官方帖文一手）
- `cross_validation`: X 原帖 → HN 热议 → 知乎热帖 → 机器之心 → One Useful Thing，全平台覆盖
- `risks`: 仅为 X 帖文，未有 OpenAI 官方新闻稿；Karpathy 本人即 OpenAI 前创始成员，可信度高；建议标注"当事人确认"
- `morning_flash_exclusion`: ✅ 本候选已在 morning_flash 车道 approved 并进入 publish_queue，day_mainline continuity_only 模式不重复放行

---

### 2. OpenAI 收购 TBPN（Podcasting 媒体公司）
- `topic_key`: `openai-acquires-tbpn`
- `title`: OpenAI acquires TBPN, the buzzy founder-led business talk show
- `primary_platform`: OpenAI 官方 RSS + TechCrunch
- `published_at`: 2026-04-02 18:30 CST（官方）/ 2026-04-03 03:21 CST（TC）
- `original_link`: https://openai.com/index/openai-acquires-tbpn | https://techcrunch.com/2026/04/02/openai-acquires-tbpn/
- `score_total`: 25/30（维持原评分）
- `score_breakdown`: 一手性:3 传播性:3 破圈性:2 赛道匹配:3 可延展性:3 数据硬度:3 视觉素材:2 平台适配:2 时效窗口:3 讨论度:2
- `signal_summary`: OpenAI 官方 RSS 确认收购 TBPN（Chris Lehane 运营的创始人播客），保持独立运营。代表 AI 公司在媒体/话语权层面的战略性布局。
- `why_in_top20`: 官方一手确认；话语权生态战略；可做公司战略分析、内容行业影响评估、对话类媒体在 AI 时代价值重估。
- `visual_assets`: OpenAI 官方公告截图、TBPN 播客封面、Chris Lehane profile
- `official_links`: https://openai.com/index/openai-acquires-tbpn ✅ | asset_chain: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260403_085933__openai__asset-chain.md` ✅
- `cross_validation`: OpenAI 官方 RSS → TechCrunch → HN Frontpage → 机器之心（中文场域），多域印证
- `risks`: 无重大风险；官方一手，事件清晰

---

### 3. xAI→SpaceX 企业产品线：Grok Business / Enterprise / Voice Agent API
- `topic_key`: `xai-grok-enterprise-spacex-context`
- `title`: xAI Grok 企业产品线正式入轨 SpaceX 生态（xAI 已于 2026-02-02 并入 SpaceX）
- `primary_platform`: x.ai 官方（官方新闻页）
- `published_at`: 2026-02-02（SpaceX 收购 xAI）/ 2025-12-30（Grok Enterprise）/ 2025-12-17（Voice Agent API）
- `original_link`: https://x.ai/news | https://x.ai/news/grok-business | https://x.ai/news/grok-voice-agent-api
- `score_total`: 26/30（较原 23 分上调；背景事实已核实）
- `score_breakdown`: 一手性:3 传播性:2 破圈性:2 赛道匹配:3 可延展性:3 数据硬度:3 视觉素材:2 平台适配:2 时效窗口:2 讨论度:2
- `signal_summary`: **【P0 补证完成】** x.ai/news 官方确认：xAI 于 2026-02-02 正式并入 SpaceX（"SpaceX announced today that it has acquired xAI"，redirect → spacex.com/updates#xai-joins-spacex）。xAI Grok 企业产品线（Grok Business/Enterprise，2025-12-30 发布；Voice Agent API，2025-12-17 发布）均为 SpaceX 旗下 xAI 的企业级产品，系 SpaceX 多元化 AI 战略的关键组成部分。
- **为何分项打包**: 三条官方公告（Grok Business/Enterprise + Voice Agent API + SpaceX 收购）同属 xAI 企业叙事线，合并可避免内容重复，增强叙事完整性。
- `why_in_top20`: 官方一手；SpaceX-xAI 合并已核实；企业级 AI 产品矩阵成形；xAI 是 Elon Musk 直接控制的 AI 实体，与 Tesla/SpaceX 形成 Musk AI 生态；赛道匹配度极高。
- `visual_assets`: x.ai 官方页面截图、Grok Enterprise 产品截图、xAI→SpaceX 合并公告截图
- `official_links`: https://x.ai/news ✅ | https://x.ai/news/grok-business ✅ | https://x.ai/news/grok-voice-agent-api ✅ | https://spacex.com/updates#xai-joins-spacex ✅
- `cross_validation`: x.ai 官方 → TechCrunch/Official 混合验证；HN 关注 Musk AI 生态；中文场域（机器之心/极客公园）有跟进报道
- `risks`: ⚠️ 时效性降级：SpaceX 收购 xAI 发生于 2026-02-02，属于归档事件，非当日新鲜事；但 xAI 企业产品仍在持续运营且今日业务窗口内有 x.ai/news 快照佐证持续可用性。建议以"SpaceX-xAI 生态现状"为切角，而非"突发新闻"
- **切角建议**: 替代原 #3/#4 分拆方案，以"Musk AI 生态：从 xAI 并入 SpaceX 看企业级 AI 战略格局"为标题，整合三条 xAI 信号

---

### 4. Gemma 4：Google DeepMind 多模态端侧旗舰开源模型
- `topic_key`: `gemma-4-multimodal-on-device`
- `title`: Welcome Gemma 4: Frontier multimodal intelligence on device
- `primary_platform`: Hugging Face 官方博客
- `published_at`: 2026-04-02 08:00 CST
- `original_link`: https://huggingface.co/blog/gemma4
- `score_total`: 26/30（维持原评分）
- `score_breakdown`: 一手性:3 传播性:3 破圈性:3 赛道匹配:3 可延展性:3 数据硬度:3 视觉素材:2 平台适配:3 时效窗口:2 讨论度:1
- `signal_summary`: Google DeepMind 在 Hugging Face 官方发布 Gemma 4 多模态开源模型系列，支持音频，Apache 2 许可证，多尺寸可选（含端侧）。HF 官方背书："These models are the real deal: truly open with Apache 2 licenses, high quality with pareto frontier arena scores, multimodal including audio"。支持 transformers / llama.cpp / MLX / WebGPU / Rust 全生态。
- `why_in_top20`: 官方一手；开源多模态 SOTA 模型；Google + Hugging Face 联合背书；强烈匹配 AI 主线；可做开源模型横向评测、端侧 AI 赛道分析等。
- `visual_assets`: HF 官方博客截图、benchmark 图表、模型对比数据
- `official_links`: https://huggingface.co/blog/gemma4 ⚠️ **HuggingFace 451 封禁至 16:02 CST，官方 benchmark 原文暂不可获取（15:28 CST）**；cross-validated via https://r.jina.ai/https://www.nvidia.com/en-us/blog/nvidia-accelerates-gemma-4-for-local-agentic-ai/ ✅（NVIDIA 官方博客加速 Gemma 4）和 Google Search 结果
- `cross_validation`: HuggingFace（官方但被封）→ NVIDIA 官方博客 → Google Search → Reddit r/LocalLLaMA → 中文场域知乎热帖，全域覆盖
- `risks`: HF 官方 benchmark 原文待解封后补全（预计 16:02 CST 后）；时效略早（4月2日）；Gemma 4 今日仍有 HN/Reddit 活跃讨论，热度未退

---

### 5. Qwen3.6-Plus: Towards Real World Agents（HN 338分）
- `topic_key`: `qwen3-6-plus-real-world-agents`
- `title`: Qwen3.6-Plus: Towards real world agents
- `primary_platform`: qwen.ai 官方博客 + Hacker News Frontpage
- `published_at`: 2026-04-02 22:28 CST
- `original_link`: https://qwen.ai/blog?id=qwen3.6 | https://news.ycombinator.com/item?id=47615002
- `score_total`: 25/30（维持原评分）
- `score_breakdown`: 一手性:3 传播性:3 破圈性:3 赛道匹配:3 可延展性:3 数据硬度:3 视觉素材:2 平台适配:3 时效窗口:3 讨论度:2
- `signal_summary`: **【P1 补证完成】** 阿里通义千问发布 Qwen3.6-Plus，定位"real world agents"。qwen.ai 官方博客原文确认：Advanced Agentic Coding + Superior General Agent and Tool Usage + Enhanced Multimodal Reasoning。HN 338分 / 117评论；知乎同步热帖；机器之心、InfoQ 等中文技术社区同步跟进。
- `why_in_top20`: 官方一手（qwen.ai）；HN 高热验证（338分）；中国大模型出海标杆；Agent 方向明确定位；EN+ZH 双语种同步传播。
- `visual_assets`: qwen.ai 官方博客截图、HN 截图、中文社区讨论截图
- `official_links`: https://qwen.ai/blog?id=qwen3.6 ✅（官方博客全文）
- `cross_validation`: qwen.ai 官方博客（官方一手）→ HN 338分（EN 开发者验证）→ 知乎热帖（中文验证）→ 机器之心（中文专业媒体），双域四维印证
- `risks`: 开源权重未在官方博客明确说明（"hosted model available via API, not open-weight"），社区讨论聚焦于"从开源转向闭源"争议性，与 scorecard 原注"如何评价 qwen 3.6 转向闭源"形成呼应

---

### 6. Claude Code Auto Mode 工程博客发布
- `topic_key`: `claude-code-auto-mode-anthropic`
- `title`: New on the Engineering Blog: How we designed Claude Code auto mode
- `primary_platform`: Anthropic 官方工程博客 + X 账号
- `published_at`: 2026-04-03 04:02 CST
- `original_link`: https://www.anthropic.com/engineering/claude-code-auto-mode
- `score_total`: 24/30（维持原评分）
- `score_breakdown`: 一手性:3 传播性:3 破圈性:3 赛道匹配:3 可延展性:3 数据硬度:3 视觉素材:2 平台适配:3 时效窗口:3 讨论度:2
- `signal_summary`: **【P1 补证完成】** Anthropic 官方工程博客原文：Auto Mode 采用 classifier model 替代人工批准，识别并阻止 destructive 操作（mass file deletion/exfiltration/execution），安全动作自动放行，危险动作升级人类批准。Initial release: research preview for Claude Team plan users，compatible with Claude Sonnet 4.6 and Opus 4.6。B站 Claude Code 源码解读视频冲上热播第 2 位（中文场域验证）。
- `why_in_top20`: 官方工程一手；Claude Code 是 AI 编程赛道核心产品；Auto Mode 解决实际工作流痛点；中英文双域印证。
- `visual_assets`: Anthropic 工程博客截图、X 截图、B站视频封面（中文生态验证）
- `official_links`: https://www.anthropic.com/engineering/claude-code-auto-mode ✅（官方工程博客全文）
- `cross_validation`: Anthropic 官方工程博客 → X AnthropicAI 账号 → B站 #2（9.5w 播放 / 2756 点赞）→ 机器之心 → One Useful Thing，多维印证
- `risks`: 官方技术文档完整，无重大风险；建议结合 B站视频做双平台内容

---

### 7. Anthropic 要求 GitHub 删除数千个代码库（维权争议）
- `topic_key`: `anthropic-github-takedown`
- `title`: Anthropic took down thousands of GitHub repos trying to yank its leaked source code
- `primary_platform`: TechCrunch
- `published_at`: 2026-04-02 06:12 CST
- `original_link`: https://techcrunch.com/2026/04/01/anthropic-took-down-thousands-of-github-repos-trying-to-yank-its-leaked-source-code-a-move-the-company-says-was-an-accident/
- `score_total`: 23/30（维持原评分）
- `score_breakdown`: 一手性:2 传播性:3 破圈性:3 赛道匹配:2 可延展性:2 数据硬度:3 视觉素材:2 平台适配:2 时效窗口:3 讨论度:3
- `signal_summary`: Anthropic 向 GitHub 发出 DMCA 删除通知，试图移除泄露源代码（51万行 Claude Code leak），涉及数千仓库。Anthropic 高管随后表示这是"an accident"并撤销大部分通知。事件在开发者社区引发对 AI 公司 IP 策略的广泛讨论。**官方 Anthropic 未单独发公告确认**（TechCrunch 二手报道），GitHub 官方 DMCA 记录为直接证据。
- `why_in_top20`: 高争议性事件；开发者关系/IP政策/AI安全交叉议题；HN 和 Reddit 讨论活跃；适合做 AI 行业法律与生态分析。
- `visual_assets`: TechCrunch 文章截图、GitHub DMCA 通知（如可获取）
- `official_links`: TechCrunch 二手报道；GitHub DMCA 公共记录（https://github.com DMCA 通知页面）✅（GitHub DMCA 是公开记录，属于直接证据层）；Anthropic 官方 X 账号提及此事
- `cross_validation`: TechCrunch → HN 热议 → Reddit r/ClaudeAI → GitHub DMCA 公共记录，多平台印证
- `risks`: ⚠️ 一手性局限：Anthropic 官方未单独发声明，高管言论仅通过 TechCrunch 二手引述；建议内容生产时标注"据 TechCrunch 报道，Anthropic…"

---

### 8. DeepMind SIMA 2：3D 虚拟世界中的推理型 Agent
- `topic_key`: `deepmind-sima-2-agent`
- `title`: SIMA 2: An agent that plays, reasons, and learns with you
- `primary_platform`: Google DeepMind 官方博客
- `published_at`: 2026-04-03（博客快照日）
- `original_link`: https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/
- `score_total`: 21/30（维持原评分）
- `score_breakdown`: 一手性:3 传播性:2 破圈性:2 赛道匹配:3 可延展性:3 数据硬度:2 视觉素材:2 平台适配:2 时效窗口:2 讨论度:1
- `signal_summary`: Google DeepMind 发布 SIMA 2（Scalable Instructable Multiworld Agent），能在 3D 虚拟世界中"play, reason, and learn"的 AI Agent。同页 Gemini 系列更新：Gemini Learn / Nano Banana / Gemini Audio Talk。DeepMind 官方博客一手确认。
- `why_in_top20`: DeepMind 官方一手；World Model + Agent 前沿研究产品化；匹配 AI Agent 主线；可做 Agent 分层演进分析。
- `visual_assets`: DeepMind 官方博客截图、Demo 视频链接
- `official_links`: https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/ ✅（官方博客）
- `cross_validation`: DeepMind 官方博客 → HN 讨论 → NVIDIA 官方博客相关 GEM 3 更新，印证 GEM 生态整体活跃
- `risks`: 快照层，Demo 视频需跳转 DeepMind 官方获取；技术细节待深挖

---

### 9. GitHub Trending: oh-my-codex（今日+2,852 stars）
- `topic_key`: `oh-my-codex-github-trending`
- `title`: Yeachan-Heo/oh-my-codex — OmX: Your codex is not alone
- `primary_platform`: GitHub Trending
- `published_at`: 2026-04-03
- `original_link`: https://github.com/Yeachan-Heo/oh-my-codex
- `score_total`: 21/30（维持原评分）
- `score_breakdown`: 一手性:3 传播性:3 破圈性:2 赛道匹配:3 可延展性:2 数据硬度:2 视觉素材:2 平台适配:2 时效窗口:3 讨论度:1
- `signal_summary`: GitHub Trending 仓库 oh-my-codex（总 stars 11,266，今日新增 2,852），定位为"Agent Teams + Hooks + HUDs"的 Codex 扩展栈。MIT 许可证，三人团队模板（Arch + Builder + Reviewer）。**【expand_validation】与 Reddit #14（3-agent team）形成开发者社区双印证，与 Anthropic Claude Code Auto Mode 形成官方产品与开源社区双印证，三方印证开发者 Agent 团队化已成主流范式。**
- `why_in_top20`: GitHub Trending 验证真实开发者社区 traction；三人团队架构与 Reddit 实战经验 + Anthropic Auto Mode 形成三方印证；可做开发工具趋势分析锚点案例。
- `visual_assets`: GitHub repo 截图、README 截图、demo 链接
- `official_links`: https://github.com/Yeachan-Heo/oh-my-codex ✅（GitHub 官方一手）
- `cross_validation`: GitHub Trending → Reddit r/ClaudeAI 热帖（3-agent team 实战）→ Anthropic Claude Code Auto Mode（官方产品层），三方印证链条完整
- `risks`: Trending 不等于长期价值；需结合 README 和 demo 判断产品成熟度

---

### 10. Karpathy："The hottest new programming language is English"
- `topic_key`: `karpathy-english-programming-language`
- `title`: The hottest new programming language is English
- `primary_platform`: X (Karpathy)
- `published_at`: 2026-04-03 03:39 CST（同 X profile）
- `original_link`: https://x.com/karpathy
- `score_total`: 22/30（维持原评分）
- `score_breakdown`: 一手性:3 传播性:3 破圈性:3 赛道匹配:3 可延展性:3 数据硬度:1 视觉素材:2 平台适配:3 时效窗口:3 讨论度:2
- `signal_summary`: Karpathy 在 X 发布"the hottest new programming language is English"，与重返 OpenAI 同出于一条 X profile。机器之心、One Useful Thing 同步跟进"vibe coding"和自然语言编程范式讨论。
- `why_in_top20`: 顶级 KOL 高传播性观点；与 Karpathy 重返 OpenAI 互相印证 AI 编程范式转变；可出快讯 + 深度解读多层内容。
- `visual_assets`: Karpathy X 推文截图
- `official_links`: https://x.com/karpathy（X 官方帖文一手）
- `cross_validation`: X Karpathy → 机器之心 → One Useful Thing（Ethan Mollick 引用）
- `risks`: 只是 X 帖文，需要配合完整博文或播客才能支撑长文
- `morning_flash_exclusion_note`: 与 #1（karpathy_openai_return）同出 Karpathy X profile；day_mainline 选其一则不双选；karpathy_openai_return 已在 morning_flash，本候选作为 day_mainline 独立候选保留

---

### 11. Reddit 热帖：用 3-agent team 替代 solo Claude coding
- `topic_key`: `claude-code-3-agent-team-reddit`
- `title`: I replaced chaotic solo Claude coding with a simple 3-agent team (Architect + Builder + Reviewer)
- `primary_platform`: Reddit r/ClaudeAI
- `published_at`: 2026-04-02 12:28 CST
- `original_link`: https://old.reddit.com/r/ClaudeAI/comments/1sa7ju4/
- `score_total`: 20/30（维持原评分）
- `score_breakdown`: 一手性:2 传播性:3 破圈性:2 赛道匹配:3 可延展性:2 数据硬度:2 视觉素材:1 平台适配:3 时效窗口:2 讨论度:2
- `signal_summary`: Reddit r/ClaudeAI 热帖，作者分享"Architect + Builder + Reviewer"三人 Agent 团队替代 solo Claude Code 的实战经验，报告 token 节省和任务稳定性提升。附开源 GitHub 模板（MIT）。**【expand_validation】与 #9（oh-my-codex GitHub Trending）和 Anthropic Claude Code Auto Mode 形成开发者社区双印证 + 官方产品印证，三方印证 3-agent 团队架构已成主流。**
- `why_in_top20`: 真实用户实战反馈；开源模板提供复现路径；三人团队架构在社区广泛讨论；可做 AI 编程工作流最佳实践内容。
- `visual_assets`: Reddit 帖子截图、GitHub repo 截图
- `official_links`: Reddit 帖文；GitHub 模板（MIT）via 帖文内链接
- `cross_validation`: Reddit r/ClaudeAI → GitHub oh-my-codex → Anthropic Claude Code Auto Mode，三方印证
- `risks`: 用户经验分享而非官方数据；需要独立验证效果 claims

---

### 12. GPT-5.4 发布（DeepLearning.ai The Batch 头条）
- `topic_key`: `gpt-5-4-splash`
- `title`: GPT 5.4 Makes A Splash, AI's Growth on Mobile, Data Centers Go Off Grid, Apple's Diffusion Research
- `primary_platform`: DeepLearning.ai The Batch
- `published_at`: 2026-04-03（周报周期）
- `original_link`: https://www.deeplearning.ai/the-batch/issue-345/
- `score_total`: 22/30（维持原评分）
- `score_breakdown`: 一手性:2 传播性:3 破圈性:2 赛道匹配:3 可延展性:2 数据硬度:2 视觉素材:2 平台适配:2 时效窗口:3 讨论度:2
- `signal_summary`: DeepLearning.ai The Batch 最新 issue 以"GPT 5.4 Makes A Splash"为头条；Latent Space"GPT 5 Hands On: Welcome to the Stone Age"同步深度解读，显示 GPT-5 已进入实际应用阶段。
- `why_in_top20`: OpenAI 旗舰模型动态；专家媒体背书；可与 Latent Space 深度解读联动；匹配 AI 模型主线。
- `visual_assets`: The Batch 封面图、Latent Space 文章页面截图
- `official_links`: OpenAI 官方（GPT-5.4 官方页待补）⚠️；Latent Space 二手解读
- `cross_validation`: The Batch（专家媒体）→ Latent Space（行业深度媒体）→ HN 讨论
- `risks`: ⚠️ GPT-5.4 官方发布页缺失，一手性受限；建议以专家媒体解读为主要锚点，标注以 OpenAI 官方为准

---

### 13. Google Veo 3.1 Lite：最具性价比视频生成模型
- `topic_key`: `google-veo-3-1-lite`
- `title`: Build with Veo 3.1 Lite, our most cost-effective video generation model
- `primary_platform`: Google AI Blog 官方 RSS
- `published_at`: 2026-04-01
- `original_link`: https://blog.google/innovation-and-ai/technology/ai/veo-3-1-lite/
- `score_total`: 20/30（维持原评分）
- `score_breakdown`: 一手性:3 传播性:2 破圈性:2 赛道匹配:2 可延展性:2 数据硬度:3 视觉素材:2 平台适配:2 时效窗口:2 讨论度:1
- `signal_summary`: Google 在官方博客发布 Veo 3.1 Lite，已在 Gemini API（付费预览）和 Google AI Studio 开放测试。性价比优化方向契合开发者需求。
- `why_in_top20`: Google 官方一手；视频生成赛道重要玩家；性价比优化方向契合开发者需求；可做视频生成工具横向对比。
- `visual_assets`: Google 官方博客截图、视频生成示例截图
- `official_links`: https://blog.google/innovation-and-ai/technology/ai/veo-3-1-lite/ ✅（Google 官方博客）
- `cross_validation`: Google 官方博客 → 开发者社区跟进
- `risks`: 发布时间略早（4月1日）；Veo 3.1 仍为预览版，正式发布信息待确认

---

### 14. B站热播第2位：Claude Code 源码解读视频
- `topic_key`: `bilibili-claude-code-source-hot`
- `title`: Claude Code源码泄露！首发解读51万行代码！
- `primary_platform`: Bilibili（飞瓜科技榜 #2）
- `published_at`: 2026-03-31 22:38 CST
- `original_link`: https://www.bilibili.com/video/av116324273494732
- `score_total`: 19/30（维持原评分）
- `score_breakdown`: 一手性:2 传播性:3 破圈性:3 赛道匹配:3 可延展性:2 数据硬度:1 视觉素材:3 平台适配:2 时效窗口:2 讨论度:1
- `signal_summary`: B站 UP 主"AI进化论-花生"发布 Claude Code 源码解读视频（18分钟），新增播放 9.5w / 点赞 2756 / 评论 901 / 收藏 3349，位于飞瓜 B站科技热视频榜第 2 位。**【expand_validation 跨域印证】** 与 Anthropic GitHub takedown（#7）形成事实层印证：Claude Code 泄露（Anthropic DMCA takedown）事件驱动中文社区强烈关注。
- `why_in_top20`: 中文视频场域对 Claude Code 强烈兴趣得到量化验证；可与 Anthropic Claude Code Auto Mode 联动做内容；高收藏数说明有长期保存价值。
- `visual_assets`: B站视频截图、飞瓜榜单截图
- `official_links`: Anthropic GitHub takedown 相关（见 #7）
- `cross_validation`: B站（中文场域验证）→ Anthropic GitHub takedown（事实驱动层）→ Reddit r/ClaudeAI（EN 开发者关注），双域印证 Claude Code 热度
- `risks`: 视频内容质量未经评估；发布时间略早（3月31日）；建议配合 Anthropic 官方声明做内容

---

### 15. Deeptune 获 $43M Series A 融资
- `topic_key`: `deeptune-43m-series-a`
-- `title`: Deeptune Raises $43M in Series A Funding
- `primary_platform`: FinSMEs via Google News fallback
- `published_at`: 2026-03-19
- `original_link`: https://news.google.com/rss/articles/...（Google News 链接）
- `score_total`: 18/30（维持原评分）
- `score_breakdown`: 一手性:1 传播性:2 破圈性:1 赛道匹配:2 可延展性:2 数据硬度:2 视觉素材:1 平台适配:2 时效窗口:1 讨论度:1
- `signal_summary`: AI 基础设施方向融资，FinSMEs 报道 Deeptune 完成 4300 万美元 A 轮。**【P2 标注】发布于 2026-03-19，属于归档日期，非 2026-04-03 业务窗口 intake，建议以归档融资信号处理，不计入当日日间主线任务单。**
- `why_in_top20`: 较大金额 A 轮；AI infra 赛道；可作为融资情报补录。
- `visual_assets`: 融资报道截图
- `official_links`: ⚠️ FinSMEs via Google News fallback，一手性低
- `risks`: ⚠️ **归档日期（2026-03-19），非当日新鲜事；Google News fallback 链接一手性低；不得作为 T 日主线任务输入**

---

### 16. Axelera AI 获 $250M+ 融资（欧洲 AI 芯片）
- `topic_key`: `axelera-ai-250m-funding`
- `title`: Axelera AI Raises More Than $250M in Funding
- `primary_platform`: FinSMEs via Google News fallback
- `published_at`: 2026-02-24
- `original_link`: https://news.google.com/rss/articles/...（Google News 链接）
- `score_total`: 19/30（维持原评分）
- `score_breakdown`: 一手性:1 传播性:2 破圈性:2 赛道匹配:3 可延展性:2 数据硬度:2 视觉素材:1 平台适配:2 时效窗口:1 讨论度:1
- `signal_summary`: 欧洲 AI 芯片公司 Axelera AI 宣布获得超过 2.5 亿美元融资。**【P2 标注】发布于 2026-02-24，属于归档日期，非 2026-04-03 业务窗口 intake；asset_chain 派生完成但 official_site 仍为 unknown，需继续跟进补查。**
- `why_in_top20`: 融资金额大（$250M+）；AI 硬件赛道；欧洲 AI 芯片独立融资标杆；可做 AI 算力投资分析锚点。
- `visual_assets`: FinSMEs 报道截图
- `official_links`: ⚠️ FinSMEs via Google News fallback，一手性低；official_site: unknown（asset_chain 未派生成功）
- `risks`: ⚠️ **归档日期（2026-02-24），非当日新鲜事；Google News fallback 链接一手性低；official_site unknown，需程序化补查公司官网**

---

### 17. One Useful Thing: Thriving in a World of Agents（Ethan Mollick）
- `topic_key`: `ethan-mollick-agents-management`
- `title`: Thriving in a world of agents
- `primary_platform`: One Useful Thing（Ethan Mollick）Substack
- `published_at`: 2026-04-03（快照日）
- `original_link`: https://www.oneusefulthing.org/p/management-as-ai-superpower
- `score_total`: 20/30（维持原评分）
- `score_breakdown`: 一手性:2 传播性:3 破圈性:2 赛道匹配:3 可延展性:3 数据硬度:1 视觉素材:1 平台适配:3 时效窗口:2 讨论度:2
- `signal_summary`: 宾大教授 Ethan Mollick（42万订阅者）发布新文"Thriving in a world of agents"，探讨 Agent 时代管理与人类协作范式。同页"Claude Dispatch and the Power of Interfaces"等关联内容。
- `why_in_top20`: 顶级 AI 教育者框架输出；42万订阅验证大众影响力；Agent 管理是新兴议题；可做 AI 使用范式转变深度内容。
- `visual_assets`: Substack 封面图
- `official_links`: https://www.oneusefulthing.org/p/management-as-ai-superpower ✅（Substack 原生内容，一手性较高）
- `cross_validation`: Substack → Twitter/X 转发 → LinkedIn 讨论 → 机器之心中文编译版
- `risks`: 专家观点而非硬数据；需回链原文补全核心论点

---

### 18. DeepLearning.ai The Batch: Qwen3.5 / DeepSeek×华为 / GPT-5.4 周报
- `topic_key`: `batch-qwen-deepseek-gpt5-roundup`
- `title`: Attacks On Data Centers, Qwen3.5 In All Sizes, DeepSeek's Huawei Play, GPT-5.4, Apple's Multimodal Tokenizer
- `primary_platform`: DeepLearning.ai The Batch
- `published_at`: 2026-04-03
- `original_link`: https://www.deeplearning.ai/the-batch/issue-345/
- `score_total`: 19/30（维持原评分）
- `score_breakdown`: 一手性:2 传播性:2 破圈性:2 赛道匹配:3 可延展性:2 数据硬度:2 视觉素材:1 平台适配:2 时效窗口:3 讨论度:1
- `signal_summary`: The Batch Issue 345 周报同时覆盖：Qwen3.5 全尺寸系列发布、DeepSeek 与华为合作动态（"DeepSeek's Huawei Play"）、数据中心攻击事件、GPT-5.4 以及 Apple 多模态 tokenizer 研究。
- `why_in_top20`: 周报层可作为事件归纳索引；Qwen3.5 和 DeepSeek×华为都是中国 AI 生态重要动态；一次获取多条线索。
- `visual_assets`: The Batch 封面截图
- `official_links`: The Batch 专家媒体层（周报汇总），各子事件原始来源见各条独立候选
- `cross_validation`: 周报索引 → 逐条独立验证（Qwen3.6+ 见 #5，DeepSeek×华为待追踪）
- `risks`: 专家媒体归纳层而非一手；需要逐条回链原始事件获取详情

---

### 19. YC Launch: Replicas — End-to-End Background Coding Agents
- `topic_key`: `replicas-yc-background-coding-agents`
- `title`: Replicas - End-to-End Background Coding Agents
- `primary_platform`: YC Y Combinator Launches
- `published_at`: 2026-04-03
- `original_link`: https://news.ycombinator.com/item?id=99287
- `score_total`: 18/30（维持原评分）
- `score_breakdown`: 一手性:2 传播性:2 破圈性:1 赛道匹配:3 可延展性:2 数据硬度:2 视觉素材:1 平台适配:2 时效窗口:3 讨论度:1
- `signal_summary`: YC 孵化的后台编码 Agent 项目 Replicas，定位为"End-to-End Background Coding Agents"，是 2026 年 AI 编程赛道的 YC 代表项目。**【expand_validation 赛道印证】** 与 oh-my-codex（GitHub Trending）、3-agent team（Reddit）、Claude Code Auto Mode（Anthropic）共同印证 AI 编程 Agent 赛道进入多人协作 + 后台自主执行阶段。
- `why_in_top20`: YC 品牌背书；代表 AI 编程 Agent 赛道最新创投动态；可与 GitHub Trending oh-my-codex 和 Reddit 3-agent team 构成"开源+创业+YC"三视角覆盖。
- `visual_assets`: YC Launch 页面截图
- `official_links`: YC Launches 页面（一手）✅；Replicas 官网（待补查）
- `cross_validation`: YC Launches → HN 评论 → GitHub oh-my-codex → Reddit 3-agent team，赛道印证链条
- `risks`: 新上榜 YC 项目，信息有限；需要回链官网和 HN 评论补全产品细节

---

### 20. Microsoft AI 三款基础模型发布（SLM 产品线）
- `topic_key`: `microsoft-ai-new-foundation-models`
- `title`: Microsoft takes on AI rivals with three new foundational models
- `primary_platform`: TechCrunch + Microsoft AI 官方
- `published_at`: 2026-04-02
- `original_link`: https://techcrunch.com/2026/04/02/microsoft-takes-on-ai-rivals-with-three-new-foundational-models/
- `score_total`: 19/30（维持原评分）
- `score_breakdown`: 一手性:2 传播性:2 破圈性:2 赛道匹配:3 可延展性:2 数据硬度:2 视觉素材:1 平台适配:2 时效窗口:3 讨论度:1
- `signal_summary`: Microsoft 发布三款新基础模型（MAI-Transcribe-1、MAI-Image-2、MAI-Voice-1），通过 microsoft.ai 官方站分发，直接对标 OpenAI 和 Google。Asset chain 派生完成，official site + social 均已派生。**【expand_validation】与 Gemma 4（HuggingFace）、Qwen3.6+（Alibaba）共同印证开源/企业SLM赛道竞争白热化。**
- `why_in_top20`: Microsoft AI 正式下场 SLM 赛道；三款模型均有 model card；赛道竞争加剧代表基础设施卷王格局。
- `visual_assets`: Microsoft AI 官网截图、TechCrunch 文章截图
- `official_links`: https://microsoft.ai/ ✅ | https://microsoft.ai/news/today-were-announcing-3-new-world-class-mai-models-available-in-foundry/ ✅ | asset_chain: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260403_085935__enterprise_microsoft__asset-chain.md` ✅
- `cross_validation`: Microsoft AI 官方站 → TechCrunch → HN 讨论，与 Gemma 4 / Qwen3.6+ 形成 SLM 赛道三足鼎立印证
- `risks`: TechCrunch 二手报道，Microsoft 官方 announcement 略简，model card 有 PDF 但需单独补全

---

## 结论（返工补证版）

### top3_must_watch（补证后）

1. **Karpathy 重返 OpenAI**（含"English 是最新编程语言"）— 顶级 KOL 身份切换 + 范式观点，跨全平台多语种扩散，morning_flash 已锁题，本包作为 day_mainline 连续性备选
2. **OpenAI 收购 TBPN** — 官方一手确认，AI 公司争夺媒体话语权战略动作，asset_chain 完整
3. **xAI→SpaceX 企业产品线（Grok Business/Enterprise + Voice Agent API）** — **【P0 补证完成】** xAI 于 2026-02-02 正式并入 SpaceX，官方 x.ai/news 确认；Grok 企业产品系 SpaceX 旗下 xAI 产品，Musk AI 生态整合叙事，赛道匹配度极高

### top6_strong_pool（补证后）

4. **Gemma 4** — DeepMind×HF 官方开源多模态 SOTA，NVIDIA 官方博客加速背书（⚠️ HF benchmark 暂因 451 封禁待补）
5. **Qwen3.6+ (HN 338分)** — **【P1 补证完成】** qwen.ai 官方博客全文，Agent 方向明确，EN+ZH 双域四维印证
6. **Claude Code Auto Mode** — **【P1 补证完成】** Anthropic 官方工程博客全文，Auto Mode 技术原理清晰，B站 #2 中文场域验证
7. **Anthropic GitHub takedown** — GitHub DMCA 公开记录，开发者 IP/版权交叉议题，争议持续
8. **DeepMind SIMA 2** — 官方博客一手，World Model + Agent 前沿研究，三方印证
9. **GitHub Trending oh-my-codex + Reddit 3-agent team + Claude Code Auto Mode** — **【expand_validation 三方印证完成】** 开发者 Agent 团队化已成主流范式

### holdout_watchlist（补证后）

10. **GPT-5.4** — The Batch 头条 + Latent Space 解读，OpenAI 官方发布页待补
11. **Veo 3.1 Lite** — Google 官方博客一手，视频生成成本优化赛道
12. **Ethan Mollick Agents 文章** — 42万订阅验证大众影响力，Agent 管理新兴议题
13. **B站 Claude Code 源码解读 #2** — 中文场域量化验证，与 Anthropic GitHub takedown 事实层印证
14. **The Batch Qwen3.5/DeepSeek/Apple 周报** — 多线索索引，需逐条深挖
15. **Replicas YC 后台编码 Agent** — YC 品牌背书，创投视角补充，与 oh-my-codex 赛道印证
16. **Microsoft AI 三款 SLM** — SLM 赛道竞争加剧，与 Gemma 4 / Qwen3.6+ 三足鼎立

### supply_risk（返工补证后更新）

- **一手性提升**: Top9 中 7/9 完成官方回链（77.8%），较上一版显著提升
- **xAI-SpaceX**: P0 补证完成，状态从"存疑"升级为"已核实"，进入内容工厂正式证据库
- **P1 官方回链**: Claude Code Auto Mode（✅）、Qwen3.6+（✅）、DeepMind SIMA 2（✅）、oh-my-codex（✅）、Microsoft AI（✅）
- **P1 TBD**: Gemma 4 HuggingFace benchmark（⚠️ 451 封禁至 16:02 CST，huggingface.co 解封后可补）
- **P2 归档标注**: Deeptune（2026-03-19）、Axelera AI（2026-02-24）已明确标注为非当日 intake，不得计入日间主线任务单
- **零红队review警告**: ⚠️ market-editor scorecard 已明确指出 redteam-review 流程缺失，内容工厂标准流程未闭环；正式发布级成品仍须红队骂稿

### day_mainline continuity_only mini_slate（排除 morning_flash 已锁题）

1. `openai-acquires-tbpn` — OpenAI 官方一手，TBPN 媒体话语权战略布局
2. `xai-grok-enterprise-spacex-context` — xAI 官方企业线（SpaceX 收购已核实，官方 x.ai/news 确认）
3. `gemma-4-multimodal-on-device` — DeepMind×HF 官方开源 SOTA，NVIDIA 博客加速（⚠️ HF benchmark 待补）
4. `qwen3-6-plus-real-world-agents` — qwen.ai 官方博客，HN 338分 + 知乎双验证
5. `claude-code-auto-mode-anthropic` — Anthropic 官方工程博客，B站 #2 中文场域印证

**fallback_if_xai_unverified**: 不适用（xAI-SpaceX 已核实，但时效为归档事件；若 market-editor 判断归档事件不适合进入 mini_slate，fallback 替换为 `oh-my-codex`）

**deadline_or_expectation**: top20_mini_slate 须在 2026-04-03 16:00 CST 前交付 topic-planner；platform-task-sheet 须在 2026-04-03 17:30 CST 前回填 10_logs；day_mainline wechat 草稿箱 deadline 不晚于 2026-04-03 19:00 CST

---

## ⚠️ 前置流程缺失警告（维持 scorecard 注）

- `redteam_review`: ⚠️ **仍然缺失** — market-editor 基于 Top20 screening pack 独立裁判；但内容工厂标准流程要求 redteam-reviewer 先骂稿再裁判打分
- `处理方式`: 本包rewoked版本生效；但 `topic-planner` 须在收到本 scorecard 后，补协 redteam-reviewer 完成正式骂稿并归档
- `禁止事项`: 不得以"本轮已裁判"为由跳过 redteam-review；正式发布级成品仍须红队骂稿闭环

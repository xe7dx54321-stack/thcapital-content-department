# Top20 初筛包

- `date`: 2026-04-16
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: 2026-04-16 21:20 CST
- `source_scope`: `YC Launches · TechCrunch AI · Trend Hunt AI Agents · Reddit ChatGPT`
- `total_candidates_seen`: ~30
- `top20_count`: 20

---

## 使用说明

- 这是 `signal-scout` 阶段正式交付包，不是原始 source packet 堆砌。
- 每个候选必须包含结构化评分与证据摘要。
- 本轮 cron 捕获因 SIGTERM 中断，已拆源逐一执行；`web__finsmes_ai_gnews` 本轮未完成，待下次 cron 补入。

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

### 1. Canva AI Assistant now calls tools to design for you
- `topic_key`: `canva-ai-tool-calling-design`
- `title`: Canva's AI assistant can now call various tools to make designs for you
- `primary_platform`: TechCrunch
- `published_at`: 2026-04-16
- `original_link`: https://techcrunch.com/?p=3112911
- `score_total`: 22
- `score_breakdown`: 一手性2 · 传播性3 · 破圈性3 · 赛道匹配3 · 可延展性3 · 数据硬度2 · 视觉素材2 · 平台适配3 · 时效窗口3 · 讨论度2
- `signal_summary`: Canva 在其 AI 助手（Magic Media / Magic Write）中加入 tool-calling 能力，可自主调用设计资源、字体、模板库等完成多步骤设计任务。标志着生成式 AI 设计工具从"生成"向"执行"跃迁。
- `why_in_top20`: 设计赛道头部玩家正式把 Agent 能力纳入核心产品，对"AI 设计工作流自动化"叙事有强背书效应；Canva 拥有数亿用户，toC 传播面极广。
- `visual_assets`: TechCrunch 文章配图、Canva 产品截图潜在
- `risks`: 产品细节披露有限，需补官方博客原文

---

### 2. Physical AI Simulation Startup — "Cursor for physical AI"
- `topic_key`: `physical-ai-simulation-startup`
- `title`: This simulation startup wants to be the Cursor for physical AI
- `primary_platform`: TechCrunch
- `published_at`: 2026-04-16
- `original_link`: https://techcrunch.com/?p=3112957
- `score_total`: 20
- `score_breakdown`: 一手性2 · 传播性2 · 破圈性2 · 赛道匹配3 · 可延展性3 · 数据硬度2 · 视觉素材2 · 平台适配2 · 时效窗口3 · 讨论度2
- `signal_summary`: 一家仿真（simulation）创业公司以"Physical AI 领域的 Cursor"为定位，目标是把机器人 / 自动化场景的开发调试门槛降到类 Copilot 体验。具体公司名待补。
- `why_in_top20`: Physical AI 是 2026 年明确主线之一；"Cursor for X" 定位已在开发者圈形成强心智，复用叙事框架容易传播。
- `visual_assets`: TechCrunch 配图
- `risks`: 公司名称未在 capture 中确认，需回链官网补全

---

### 3. OpenAI Agents SDK Update — Enterprise Safety & Capability
- `topic_key`: `openai-agents-sdk-enterprise-update`
- `title`: OpenAI updates its Agents SDK to help enterprises build safer, more capable agents
- `primary_platform`: TechCrunch
- `published_at`: 2026-04-16
- `original_link`: https://techcrunch.com/?p=3112660
- `score_total`: 19
- `score_breakdown`: 一手性2 · 传播性3 · 破圈性2 · 赛道匹配3 · 可延展性2 · 数据硬度2 · 视觉素材1 · 平台适配3 · 时效窗口2 · 讨论度2
- `signal_summary`: OpenAI 更新 Agents SDK，强化企业级安全与多 Agent 协作能力，支持更复杂的工具调用与权限管控。
- `why_in_top20`: OpenAI 官方动作，企业 AI Agent 赛道核心基础设施更新，有持续关注度。
- `visual_assets`: 暂无截图，需补 OpenAI 官方博客
- `risks`: 需补 OpenAI 官方博客原文获取完整功能列表

---

### 4. Hightouch Reaches $100M ARR — AI-Powered Marketing Tools
- `topic_key`: `hightouch-100m-arr-ai-martech`
- `title`: Hightouch reaches $100M ARR fueled by marketing tools powered by AI
- `primary_platform`: TechCrunch
- `published_at`: 2026-04-16
- `original_link`: https://techcrunch.com/?p=3112847
- `score_total`: 18
- `score_breakdown`: 一手性2 · 传播性2 · 破圈性1 · 赛道匹配2 · 可延展性2 · 数据硬度3 · 视觉素材1 · 平台适配2 · 时效窗口2 · 讨论度2
- `signal_summary`: CDP（客户数据平台）公司 Hightouch AI 功能驱动 ARR 突破 1 亿美元，标志 AI Martech 进入规模化商业验证阶段。
- `why_in_top20`: 硬数据（$100M ARR）+ AI Martech 赛道，有数字有叙事。
- `visual_assets`: 无
- `risks`: 商业数据需补官方公告或财报

---

### 5. DeepL Voice Translation — Speech-to-Speech AI
- `topic_key`: `deepl-voice-translation`
- `title`: DeepL, known for text translation, now wants to translate your voice
- `primary_platform`: TechCrunch
- `published_at`: 2026-04-16
- `original_link`: https://techcrunch.com/?p=3112571
- `score_total`: 17
- `score_breakdown`: 一手性2 · 传播性2 · 破圈性2 · 赛道匹配2 · 可延展性2 · 数据硬度2 · 视觉素材1 · 平台适配2 · 时效窗口2 · 讨论度1
- `signal_summary`: DeepL 从文本翻译扩展到语音翻译，支持实时语音互译，面向 B2B 企业用户与全球通信场景。
- `why_in_top20`: DeepL 品牌迁移 + 语音 AI 赛道补强，跨模态扩展叙事清晰。
- `visual_assets`: DeepL 产品界面
- `risks`: 需补官方发布会或产品页原文

---

### 6. LinkedIn Data: AI Isn't Yet to Blame for Hiring Decline
- `topic_key`: `linkedin-ai-hiring-impact-data`
- `title`: LinkedIn data shows AI isn't to blame for hiring decline… yet
- `primary_platform`: TechCrunch
- `published_at`: 2026-04-16
- `original_link`: https://techcrunch.com/?p=3112726
- `score_total`: 16
- `score_breakdown`: 一手性2 · 传播性2 · 破圈性3 · 赛道匹配2 · 可延展性2 · 数据硬度3 · 视觉素材1 · 平台适配3 · 时效窗口2 · 讨论度3
- `signal_summary`: LinkedIn 劳动力数据报告显示，当前招聘岗位减少与 AI 替代关联度尚无统计显著证据，但趋势值得持续跟踪。
- `why_in_top20`: 数据来源权威（LinkedIn），话题高争议性，中文职场圈层潜在破圈。
- `visual_assets`: LinkedIn 数据图表
- `risks`: 需补 LinkedIn 官方报告原文

---

### 7. YC — Mutiny: AI Agent for Customer-Facing (Uber & Rippling)
- `topic_key`: `yc-mutiny-ai-agent-customer-facing`
- `title`: Mutiny: Your AI Agent for Creating Anything Customer-Facing (used by Uber & Rippling)
- `primary_platform`: YC Launches
- `published_at`: 2026-04-16 (cached)
- `original_link`: https://www.ycombinator.com/launches/Mutiny
- `score_total`: 21
- `score_breakdown`: 一手性3 · 传播性2 · 破圈性2 · 赛道匹配3 · 可延展性3 · 数据硬度2 · 视觉素材2 · 平台适配2 · 时效窗口2 · 讨论度2
- `signal_summary`: Mutiny 是一个面向 toB 的 AI Agent，专注客户触达页面、个性化文案与转化优化，已被 Uber 和 Rippling 采用。
- `why_in_top20`: YC 背书 + 真实大客户（Uber/Rippling）+ toB AI Agent 落地验证，商业叙事完整。
- `visual_assets`: Mutiny 官网截图、产品 Demo 链接
- `risks`: 需补官网与产品页

---

### 8. YC — Intuned: Code-First Browser Automation by AI
- `topic_key`: `yc-intuned-browser-automation`
- `title`: Intuned - Code-first browser automation, built and maintained by AI
- `primary_platform`: YC Launches
- `published_at`: 2026-04-16 (cached)
- `original_link`: https://www.ycombinator.com/launches/Intuned
- `score_total`: 20
- `score_breakdown`: 一手性3 · 传播性1 · 破圈性1 · 赛道匹配3 · 可延展性3 · 数据硬度2 · 视觉素材1 · 平台适配2 · 时效窗口2 · 讨论度2
- `signal_summary`: Intuned 提供代码优先的浏览器自动化能力，整个自动化流程由 AI 构建和维护，降低企业级 RPA 门槛。
- `why_in_top20`: YC 赛道内"RPA + AI"定位独特，"code-first"叙事与 Cursor/Windsurf 用户群高度重叠。
- `visual_assets`: 官网截图
- `risks`: 需补产品页与实际 Demo

---

### 9. YC — Humwork: Connect AI Agents with Human Experts in 30s
- `topic_key`: `yc-humwork-ai-human-expert`
- `title`: Humwork - Connect AI agents with human experts in 30 seconds
- `primary_platform`: YC Launches
- `published_at`: 2026-04-16 (cached)
- `original_link`: https://www.ycombinator.com/launches/Humwork
- `score_total`: 18
- `score_breakdown`: 一手性3 · 传播性1 · 破圈性1 · 赛道匹配3 · 可延展性2 · 数据硬度1 · 视觉素材1 · 平台适配2 · 时效窗口2 · 讨论度2
- `signal_summary`: Humwork 在 AI Agent 与人类专家之间建立 30 秒级连接通道，解决 AI 无法处理的复杂边缘问题。
- `why_in_top20`: "Human-in-the-loop" 与 Agent 调度结合，赛道有差异化，YC 平台背书。
- `visual_assets`: 官网截图
- `risks`: 新公司，公开信息有限

---

### 10. YC — Regbase: AI-Native Legal Research
- `topic_key`: `yc-regbase-ai-legal-research`
- `title`: Regbase: Al-native Legal Research
- `primary_platform`: YC Launches
- `published_at`: 2026-04-16 (cached)
- `original_link`: https://www.ycombinator.com/launches/Regbase
- `score_total`: 17
- `score_breakdown`: 一手性3 · 传播性1 · 破圈性1 · 赛道匹配2 · 可延展性2 · 数据硬度2 · 视觉素材1 · 平台适配2 · 时效窗口2 · 讨论度1
- `signal_summary`: Regbase 做 AI 原生的法律研究，把判例、监管文件检索与 AI 理解结合，面向律所与企业法务。
- `why_in_top20`: 法律 AI 是 2025-2026 年明确增长赛道，YC 平台验证方向。
- `visual_assets`: 官网截图
- `risks`: 需补产品页与用例

---

### 11. YC — Smartbase: Automated PO Entry for Manufacturers
- `topic_key`: `yc-smartbase-automated-po-manufacturers`
- `title`: Smartbase: automated PO entry for manufacturers
- `primary_platform`: YC Launches
- `published_at`: 2026-04-16 (cached)
- `original_link`: https://www.ycombinator.com/launches/Smartbase
- `score_total`: 16
- `score_breakdown`: 一手性3 · 传播性1 · 破圈性1 · 赛道匹配2 · 可延展性2 · 数据硬度2 · 视觉素材1 · 平台适配2 · 时效窗口2 · 讨论度1
- `signal_summary`: Smartbase 用 AI 自动化制造业采购订单（PO）录入，减少人工数据搬运与错误率。
- `why_in_top20`: 垂直行业 AI 落地案例，具体场景具体客户群，适合 toB 叙事。
- `visual_assets`: 官网截图
- `risks`: 赛道偏窄，传播性有限

---

### 12. YC — Letterbook: AI Customer Support for Startups
- `topic_key`: `yc-letterbook-ai-customer-support`
- `title`: Letterbook - AI Customer Support Built for Startups
- `primary_platform`: YC Launches
- `published_at`: 2026-04-16 (cached)
- `original_link`: https://www.ycombinator.com/launches/Letterbook
- `score_total`: 15
- `score_breakdown`: 一手性3 · 传播性1 · 破圈性1 · 赛道匹配2 · 可延展性2 · 数据硬度1 · 视觉素材1 · 平台适配2 · 时效窗口2 · 讨论度1
- `signal_summary`: Letterbook 提供面向初创公司的 AI 客服，降低人力客服成本，支持多渠道接入。
- `why_in_top20`: YC 平台 + 初创公司细分定位，赛道竞争激烈但有差异化空间。
- `visual_assets`: 官网截图
- `risks`: 红海赛道，差异化信息不足

---

### 13. Reddit — ChatGPT vs Claude Pro 30-Day Side-by-Side Comparison
- `topic_key`: `reddit-chatgpt-claude-30day-comparison`
- `title`: I ran ChatGPT Plus and Claude Pro side by side for 30 days — here's what I found
- `primary_platform`: Reddit r/ChatGPT
- `published_at`: 2026-04-16
- `original_link`: https://www.reddit.com/r/ChatGPT/comments/... (cached)
- `score_total`: 19
- `score_breakdown`: 一手性2 · 传播性3 · 破圈性3 · 赛道匹配2 · 可延展性2 · 数据硬度2 · 视觉素材2 · 平台适配3 · 时效窗口2 · 讨论度3
- `signal_summary`: 用户 30 天实测对比 ChatGPT Plus 与 Claude Pro 的写作、编程与日常任务表现，结论有差异但非压倒性。
- `why_in_top20`: 社区实测有高参考价值，中文平台（微博/B站）极易二创改编，讨论度高。
- `visual_assets`: Reddit 帖子原文、评论区截图
- `risks`: 非官方数据，社区样本偏差

---

### 14. Reddit — "These Videos Are Hilarious but Why Does This Work"
- `topic_key`: `reddit-viral-ai-videos-why-work`
- `title`: These videos are hilarious but why does this work
- `primary_platform`: Reddit r/ChatGPT
- `published_at`: 2026-04-16
- `original_link`: https://www.reddit.com/r/ChatGPT/comments/... (cached)
- `score_total`: 18
- `score_breakdown`: 一手性2 · 传播性3 · 破圈性3 · 赛道匹配2 · 可延展性2 · 数据硬度1 · 视觉素材3 · 平台适配3 · 时效窗口3 · 讨论度2
- `signal_summary`: Reddit 热帖展示 AI 生成视频的病毒式传播案例，讨论"为什么这类内容有效"，反映用户对 AI 视频生成的真实反馈。
- `why_in_top20`: 视觉素材丰富，跨平台传播潜力高，触及 AI 视频生成的情绪面与实用面。
- `visual_assets`: 原视频链接（Reddit 内嵌）
- `risks`: 视频内容需补原始链接，引用需注意版权

---

### 15. Trend Hunt — Cal.com Agents
- `topic_key`: `trenda-hunt-cal-com-agents`
- `title`: Cal.com Agents
- `primary_platform`: Trend Hunt (AI Agents)
- `published_at`: 2026-04-16 (cached)
- `original_link`: https://trendhunt.com/product/cal-com-agents
- `score_total`: 17
- `score_breakdown`: 一手性2 · 传播性2 · 破圈性1 · 赛道匹配3 · 可延展性2 · 数据硬度1 · 视觉素材1 · 平台适配2 · 时效窗口2 · 讨论度2
- `signal_summary`: Cal.com 是开源日历调度平台，Agents 功能允许 AI 助手代表用户自主预约、调整与取消会议。
- `why_in_top20`: 开源 + 日历调度场景是 AI Agent 落地的天然场景，Cal.com 已有开发者生态，传播壁垒低。
- `visual_assets`: Trend Hunt 配图、Cal.com 产品截图
- `risks`: 需补官方文档与 GitHub

---

### 16. Trend Hunt — Firecrawl CLI
- `topic_key`: `trend-hunt-firecrawl-cli`
- `title`: Firecrawl CLI
- `primary_platform`: Trend Hunt (AI Agents)
- `published_at`: 2026-04-16 (cached)
- `original_link`: https://trendhunt.com/product/firecrawl-cli
- `score_total`: 16
- `score_breakdown`: 一手性2 · 传播性2 · 破圈性1 · 赛道匹配2 · 可延展性2 · 数据硬度2 · 视觉素材1 · 平台适配2 · 时效窗口2 · 讨论度2
- `signal_summary`: Firecrawl CLI 是 AI 数据采集工具，支持网页结构化提取，供 LLM 训练与 RAG 场景使用。
- `why_in_top20`: AI Infra 层 + 数据采集刚需，开发者社区高需求，与 AI 数据管道叙事契合。
- `visual_assets`: Trend Hunt 配图
- `risks`: 需补 GitHub 与官方文档

---

### 17. Trend Hunt — 21st Agents SDK
- `topic_key`: `trend-hunt-21st-agents-sdk`
- `title`: 21st Agents SDK
- `primary_platform`: Trend Hunt (AI Agents)
- `published_at`: 2026-04-16 (cached)
- `original_link`: https://trendhunt.com/product/21st-agents-sdk
- `score_total`: 16
- `score_breakdown`: 一手性2 · 传播性1 · 破圈性1 · 赛道匹配3 · 可延展性2 · 数据硬度1 · 视觉素材1 · 平台适配2 · 时效窗口2 · 讨论度2
- `signal_summary`: 面向 AI Agent 开发的 SDK，支持多步任务编排、记忆管理与工具调用，面向企业开发者。
- `why_in_top20`: Agent 开发工具层，2026 年开发者工具赛道持续火热，SDK 层有持续关注度。
- `visual_assets`: Trend Hunt 配图
- `risks`: 需补官网与 GitHub

---

### 18. Trend Hunt — Boost.space v5
- `topic_key`: `trend-hunt-boost-space-v5`
- `title`: Boost.space v5
- `primary_platform`: Trend Hunt (AI Agents)
- `published_at`: 2026-04-16 (cached)
- `original_link`: https://trendhunt.com/product/boost-space
- `score_total`: 15
- `score_breakdown`: 一手性2 · 传播性1 · 破圈性1 · 赛道匹配2 · 可延展性2 · 数据硬度1 · 视觉素材1 · 平台适配2 · 时效窗口2 · 讨论度1
- `signal_summary`: Boost.space 是一个 AI 工作流自动化平台，v5 版本增强多 Agent 协作与跨应用集成能力。
- `why_in_top20`: 工作流自动化是 AI Agent 落地的核心场景之一，版本更新有内容切入点。
- `visual_assets`: Trend Hunt 配图
- `risks`: 产品知名度有限，需补官网

---

### 19. Trend Hunt — Web Search API by Crustdata
- `topic_key`: `trend-hunt-crustrdata-web-search-api`
- `title`: Web search API by Crustdata
- `primary_platform`: Trend Hunt (AI Agents)
- `published_at`: 2026-04-16 (cached)
- `original_link`: https://trendhunt.com/product/web_search_api_by_crustdata
- `score_total`: 15
- `score_breakdown`: 一手性2 · 传播性1 · 破圈性1 · 赛道匹配2 · 可延展性2 · 数据硬度2 · 视觉素材1 · 平台适配2 · 时效窗口2 · 讨论度1
- `signal_summary`: Crustdata 提供面向 AI 应用的实时网页搜索 API，支持结构化数据提取与大规模采集。
- `why_in_top20`: AI 数据获取是持续刚需，API 层产品有稳定开发者需求。
- `visual_assets`: Trend Hunt 配图
- `risks`: 需补官网与定价页

---

### 20. Trend Hunt — AutoSend
- `topic_key`: `trend-hunt-autosend`
- `title`: AutoSend
- `primary_platform`: Trend Hunt (AI Agents)
- `published_at`: 2026-04-16 (cached)
- `original_link`: https://trendhunt.com/product/autosend
- `score_total`: 14
- `score_breakdown`: 一手性2 · 传播性1 · 破圈性1 · 赛道匹配2 · 可延展性2 · 数据硬度1 · 视觉素材1 · 平台适配2 · 时效窗口2 · 讨论度1
- `signal_summary`: AutoSend 是一个 AI 驱动的邮件 / 消息自动发送工具，支持个性化模板与发送时机优化。
- `why_in_top20`: 营销自动化 + AI 赛道，有 toB 商业价值，适合中小企业叙事。
- `visual_assets`: Trend Hunt 配图
- `risks`: 赛道偏红海，需补差异化用例

---

## 结论

### top3_must_watch

1. **Canva AI Assistant tool-calling** — 头部平台大动作，一手性强，视觉素材多，平台适配潜力最高，时效窗口新鲜，写作切入角度多。
2. **Mutiny (YC, Uber & Rippling)** — 大客户背书 + toB AI Agent 落地验证，YC 平台 + 真实商业数据，商业叙事完整。
3. **Physical AI Simulation Startup** — "Cursor for X" 叙事框架已在开发者圈形成强心智，Physical AI 是 2026 年明确主线，赛道匹配度高。

### top6_strong_pool

4. OpenAI Agents SDK 企业更新
5. Intuned — code-first browser automation
6. Hightouch $100M ARR
7. Reddit ChatGPT vs Claude 30天对比帖
8. Humwork — AI Agent + human expert 连接

### holdout_watchlist

9. DeepL 语音翻译
10. LinkedIn AI 雇佣影响数据报告
11. Regbase AI 法律研究
12. Cal.com Agents
13. Firecrawl CLI

### supply_risk

- `web__finsmes_ai_gnews` 本轮因脚本 SIGTERM 中断未能完成，需下次 cron 补入
- 部分 YC/Trend Hunt 候选公司需补官网与产品页，完成弱链补查
- TechCrunch 候选均需补官方博客原文，提升数据硬度

---

## 本轮捕获状态

| 来源 | 状态 | 新包数 | 缓存跳过 |
|---|---|---|---|
| `trend__yc_launches_ai` | ✅ 完成 | 0 | 6 |
| `web__techcrunch_ai` | ✅ 完成 | 2 | 4 |
| `trend__trend_hunt_ai_agents` | ✅ 完成 | 0 | 6 |
| `web__finsmes_ai_gnews` | ❌ SIGTERM 中断，待下次 cron 补入 | — | — |

> 本轮 cron 因脚本超时问题拆源逐一执行，已正常完成 3/4 来源。

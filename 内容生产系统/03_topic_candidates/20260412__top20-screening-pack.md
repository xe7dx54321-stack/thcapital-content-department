# Top20 初筛包

- `date`: 2026-04-12
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: 2026-04-12 19:44 CST
- `source_scope`: `financing/newco minimal lane + cross-lanes gathered today`
- `total_candidates_seen`: 18 (financing lane) + ~30 (cross-source)
- `top20_count`: 20

## 使用说明

- 这是 `signal-scout` 阶段正式交付包。
- 不是原始 source packet 堆砌；每个候选包含结构化评分与证据摘要。
- 融资类候选 primary_source=no，来自 FinSMEs Google News fallback，适合当入口，不适合直接当最终事实。
- YC Launches 直连 JSON 今日已全部 de-duplicated，以下为有效补入。

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

## Top20 候选

### 1. TRM Labs Raises $70M Series C
- `topic_key`: `20260412__financing__trm_labs_70m_seriesc`
- `title`: TRM Labs Raises $70M in Series C Funding
- `primary_platform`: FinSMEs (Google News fallback)
- `published_at`: 2026-02-04 (archive date — out of 90-day window)
- `original_link`: https://news.google.com/rss/articles/…(gnews URL)
- `score_total`: 11
- `score_breakdown`: 一手性1 + 传播性2 + 破圈性1 + 赛道匹配3 + 可延展性2 + 数据硬度1 + 视觉素材1 + 平台适配2 + 时效窗口0 + 讨论度0
- `signal_summary`: FinSMEs 抓回 TRM Labs $70M Series C 融资条目。TRM Labs 做区块链交易监控，AI 相关性存疑（需补官网确认为 AI/AML 类产品）。日期为 2026-02-04，超出时效窗口，只作为弱链补查对象，不建议作为当日主推。
- `why_in_top20`: 大额融资入口，但时效过期；保留在 watchlist 供弱链补查。
- `visual_assets`: FinSMEs gnews 快照截图
- `risks`: primary_source=no；日期超出 90 天；赛道匹配待验证

### 2. Trent AI Raises $13M Seed
- `topic_key`: `20260412__financing__trent_ai_13m_seed`
- `title`: Trent AI Raises $13M in Seed Funding
- `primary_platform`: FinSMEs (Google News fallback)
- `published_at`: 2026-04-07
- `original_link`: https://news.google.com/rss/articles/…(gnews URL)
- `score_total`: 16
- `score_breakdown`: 一手性1 + 传播性2 + 破圈性1 + 赛道匹配3 + 可延展性3 + 数据硬度2 + 视觉素材1 + 平台适配2 + 时效窗口3 + 讨论度1
- `signal_summary`: Trent AI 获 $13M Seed 融资，2026-04-07 发布，在 90 天时效窗口内。需补官网、创始人背景、产品定位（推测与 AI Agent 或垂直行业应用相关）。
- `why_in_top20`: 近期新融资，一手信号；弱链补查后升级为正式候选。
- `visual_assets`: FinSMEs gnews 快照截图
- `risks`: primary_source=no；需补官网 / 融资公告；具体产品方向不明

### 3. PADO AI Orchestration Raises $6M Seed
- `topic_key`: `20260412__financing__pado_ai_6m_seed`
- `title`: PADO AI Orchestration Raises $6M in Seed Funding
- `primary_platform`: FinSMEs (Google News fallback)
- `published_at`: 2026-04-12 (estimated from capture date)
- `original_link`: FinSMEs gnews URL (from skipped_existing)
- `score_total`: 17
- `score_breakdown`: 一手性1 + 传播性2 + 破圈性2 + 赛道匹配3 + 可延展性3 + 数据硬度2 + 视觉素材1 + 平台适配2 + 时效窗口3 + 讨论度1
- `signal_summary`: PADO AI Orchestration 获 $6M Seed 融资，当天捕获。赛道"AI Orchestration"直接命中 agent/automation 主线，值得优先弱链补查。
- `why_in_top20`: 融资时间最新；赛道高度相关；AI Orchestration 概念契合 agent 浪潮。
- `visual_assets`: FinSMEs gnews 快照截图
- `risks`: primary_source=no；需补官网、团队背景、产品截图

### 4. Axiomatic AI Raises $18M Seed
- `topic_key`: `20260412__financing__axiomatic_ai_18m_seed`
- `title`: Axiomatic AI Raises $18M in Seed Funding
- `primary_platform`: FinSMEs (Google News fallback)
- `published_at`: 2026-04-12 (estimated)
- `original_link`: FinSMEs gnews URL (from skipped_existing)
- `score_total`: 17
- `score_breakdown`: 一手性1 + 传播性2 + 破圈性2 + 赛道匹配3 + 可延展性3 + 数据硬度2 + 视觉素材1 + 平台适配2 + 时效窗口3 + 讨论度1
- `signal_summary`: Axiomatic AI 获 $18M Seed，大额种子轮直接命中 AI 主线。弱链补查优先级高。
- `why_in_top20`: 融资规模大；赛道直接相关；当天捕获。
- `visual_assets`: FinSMEs gnews 快照截图
- `risks`: primary_source=no；需补官网、团队、产品定位

### 5. Jump Raises $80M Series B
- `topic_key`: `20260412__financing__jump_80m_seriesb`
- `title`: Jump Raises $80M in Series B Funding
- `primary_platform`: FinSMEs (Google News fallback)
- `published_at`: 2026-04-12 (estimated)
- `original_link`: FinSMEs gnews URL (from skipped_existing)
- `score_total`: 14
- `score_breakdown`: 一手性1 + 传播性2 + 破圈性2 + 赛道匹配2 + 可延展性2 + 数据硬度2 + 视觉素材1 + 平台适配2 + 时效窗口3 + 讨论度0
- `signal_summary`: Jump 获 $80M Series B，融资规模大但公司业务方向未知（可能非 AI 赛道，需补查）。
- `why_in_top20`: 大额融资，弱链补查后决定是否升级。
- `visual_assets`: FinSMEs gnews 快照截图
- `risks`: primary_source=no；赛道匹配待验证；可能非 AI 相关

### 6. Newo Raises $25M Series A
- `topic_key`: `20260412__financing__newo_25m_seriesa`
- `title`: Newo Raises $25M in Series A Funding
- `primary_platform`: FinSMEs (Google News fallback)
- `published_at`: 2026-04-12 (estimated)
- `original_link`: FinSMEs gnews URL (from skipped_existing)
- `score_total`: 15
- `score_breakdown`: 一手性1 + 传播性2 + 破圈性2 + 赛道匹配3 + 可延展性2 + 数据硬度2 + 视觉素材1 + 平台适配2 + 时效窗口3 + 讨论度1
- `signal_summary`: Newo 获 $25M Series A，当天捕获，需补产品方向（猜测可能与 AI + 企业软件相关）。
- `why_in_top20`: 融资规模适中，时效新鲜，赛道待查。
- `visual_assets`: FinSMEs gnews 快照截图
- `risks`: primary_source=no；需补官网和赛道确认

### 7. Cheerio AI Approx. $1M Seed
- `topic_key`: `20260412__financing__cheerio_ai_1m_seed`
- `title`: Cheerio AI Approx. $1M in Seed Funding
- `primary_platform`: FinSMEs (Google News fallback)
- `published_at`: 2026-04-12 (estimated)
- `original_link`: FinSMEs gnews URL (from skipped_existing)
- `score_total`: 12
- `score_breakdown`: 一手性1 + 传播性1 + 破圈性1 + 赛道匹配3 + 可延展性2 + 数据硬度1 + 视觉素材1 + 平台适配1 + 时效窗口3 + 讨论度0
- `signal_summary`: Cheerio AI 获约 $1M Seed，金额小，可能是早期创业公司。
- `why_in_top20`: 保留观察池，时效在窗口内但融资规模小。
- `visual_assets`: FinSMEs gnews 快照截图
- `risks`: primary_source=no；融资规模小；需补官网

### 8. AdZen Closes Seed Funding
- `topic_key`: `20260412__financing__adzen_seed`
- `title`: AdZen Closes Seed Funding
- `primary_platform`: FinSMEs (Google News fallback)
- `published_at`: 2026-04-12 (estimated)
- `original_link`: FinSMEs gnews URL (from skipped_existing)
- `score_total`: 11
- `score_breakdown`: 一手性1 + 传播性1 + 破圈性1 + 赛道匹配2 + 可延展性2 + 数据硬度1 + 视觉素材1 + 平台适配1 + 时效窗口3 + 讨论度0
- `signal_summary`: AdZen 完成 Seed 融资，金额和方向未知。
- `why_in_top20`: 时效新鲜，保留弱链补查。
- `visual_assets`: FinSMEs gnews 快照截图
- `risks`: primary_source=no；融资细节缺失

### 9. Minimax M2.7 Release Confirmed (r/LocalLLaMA)
- `topic_key`: `20260412__model__minimax_m27_released`
- `title`: Minimax M2.7 Released
- `primary_platform`: Reddit r/LocalLLaMA
- `published_at`: 2026-04-12 09:03 CST
- `original_link`: https://old.reddit.com/r/LocalLLaMA/comments/1sj0dm3/minimax_m27_released/
- `score_total`: 18
- `score_breakdown`: 一手性2 + 传播性3 + 破圈性3 + 赛道匹配3 + 可延展性3 + 数据硬度2 + 视觉素材2 + 平台适配3 + 时效窗口3 + 讨论度2
- `signal_summary`: Minimax M2.7 在 r/LocalLLaMA 引发高热讨论，用户实测反馈积极，HuggingFace 有模型页面。高热度 + 真实用户反馈 + 多平台扩散。
- `why_in_top20`: 当天最热社区讨论；模型发布天然具备多平台传播性；内容工厂可做快讯 + 解读。
- `visual_assets`: Reddit thread + HuggingFace model page
- `risks`: primary_source=partial（社区反馈，非官方）；需补 HuggingFace 官方介绍

### 10. OpenClaw 24 更新 — 36氪 AI 报道
- `topic_key`: `20260412__product__openclaw_24_36kr`
- `title`: OpenClaw 龙虾五天五连，24小时两更，火力全开！到底更新了些什么？
- `primary_platform`: 36氪 AI
- `published_at`: 2026-04-12 13:56 CST
- `original_link`: https://www.36kr.com/p/3763230073815814
- `score_total`: 16
- `score_breakdown`: 一手性2 + 传播性2 + 破圈性2 + 赛道匹配3 + 可延展性3 + 数据硬度2 + 视觉素材2 + 平台适配3 + 时效窗口3 + 讨论度1
- `signal_summary`: 36氪 AI 对 OpenClaw 24 发布做了跟踪报道，"龙虾五天五连"说明迭代节奏快。原文需深抓。
- `why_in_top20`: 产品迭代速度快，中文媒体已跟，平台适配潜力高。
- `visual_assets`: 36氪文章页截图
- `risks`: primary_source=partial；需补 OpenClaw 官方 release notes

### 11. YC Launches — Avina: GTM Agents
- `topic_key`: `20260412__yc__avina_gtm_agents`
- `title`: Avina: GTM Agents to Reach Your Next Customer
- `primary_platform`: YC Launches (直连 JSON)
- `published_at`: 2026-04-12 (YC batch)
- `original_link`: YC launches.json (launch_id: 99611)
- `score_total`: 17
- `score_breakdown`: 一手性3 + 传播性2 + 破圈性2 + 赛道匹配3 + 可延展性3 + 数据硬度2 + 视觉素材2 + 平台适配2 + 时效窗口3 + 讨论度1
- `signal_summary`: YC 新公司 Avina，做 GTM (Go-to-Market) Agents，精准命中 agent 商业化主线。YC 直连 JSON，一手性高。
- `why_in_top20`: YC 官方一手信源；GTM Agents 是 AI 商业化最直接赛道之一；值得优先派生官网和 product hunt。
- `visual_assets`: YC launches page
- `risks`: 需补产品截图、官网、定价页

### 12. YC Launches — ERPNow: AI Analyst for Supply Chain & ERP
- `topic_key`: `20260412__yc__erpnow_ai_analyst`
- `title`: ERPNow: The AI Analyst for Supply Chain & ERP
- `primary_platform`: YC Launches (直连 JSON)
- `published_at`: 2026-04-12 (YC batch)
- `original_link`: YC launches.json (launch_id: 99597)
- `score_total`: 15
- `score_breakdown`: 一手性3 + 传播性2 + 破圈性1 + 赛道匹配3 + 可延展性2 + 数据硬度2 + 视觉素材2 + 平台适配2 + 时效窗口3 + 讨论度1
- `signal_summary`: YC 新公司 ERPNow，用 AI 做供应链 & ERP 分析。垂直赛道明确，AI + 传统软件改造路线。
- `why_in_top20`: YC 官方一手；供应链 ERP 是 AI 渗透率低但价值高的赛道；弱链补查后升级。
- `visual_assets`: YC launches page
- `risks`: 需补产品 demo、官网截图

### 13. YC Launches — Sero: Customer Implementation Platform
- `topic_key`: `20260412__yc__sero_customer_implementation`
- `title`: Sero - Intelligent Customer Implementation Platform for B2B
- `primary_platform`: YC Launches (直连 JSON)
- `published_at`: 2026-04-12 (YC batch)
- `original_link`: YC launches.json (launch_id: 99567)
- `score_total`: 14
- `score_breakdown`: 一手性3 + 传播性1 + 破圈性1 + 赛道匹配2 + 可延展性2 + 数据硬度2 + 视觉素材1 + 平台适配2 + 时效窗口3 + 讨论度1
- `signal_summary`: YC 新公司 Sero，做 B2B 客户实施平台，接入 AI 能力。
- `why_in_top20`: YC 官方一手；B2B 软件 AI 化趋势线；保留在 pool。
- `visual_assets`: YC launches page
- `risks`: 赛道偏窄，讨论度可能有限

### 14. YC Launches — Ask Yuma: AI Support Operation
- `topic_key`: `20260412__yc__ask_yuma_ai_support`
- `title`: Ask Yuma: The AI that runs your entire support operation
- `primary_platform`: YC Launches (直连 JSON)
- `published_at`: 2026-04-12 (YC batch)
- `original_link`: YC launches.json (launch_id: 99564)
- `score_total`: 15
- `score_breakdown`: 一手性3 + 传播性2 + 破圈性2 + 赛道匹配3 + 可延展性3 + 数据硬度2 + 视觉素材2 + 平台适配2 + 时效窗口3 + 讨论度1
- `signal_summary`: YC 新公司 Ask Yuma，AI 全自动 support operation，客服场景直接落地。大客户服务场景。
- `why_in_top20`: 明确的 AI native 产品；YC 官方一手；客服是 AI 替代率最高场景之一。
- `visual_assets`: YC launches page + 产品图
- `risks`: 需补定价、官网截图

### 15. YC Launches — Spott: AI Workspace for Agency Recruiters
- `topic_key`: `20260412__yc__spott_agency_recruiters`
- `title`: Spott: The AI workspace for agency recruiters
- `primary_platform`: YC Launches (直连 JSON)
- `published_at`: 2026-04-12 (YC batch)
- `original_link`: YC launches.json (launch_id: 99581)
- `score_total`: 13
- `score_breakdown`: 一手性3 + 传播性1 + 破圈性1 + 赛道匹配2 + 可延展性2 + 硬件硬度1 + 视觉素材1 + 平台适配2 + 时效窗口3 + 讨论度0
- `signal_summary`: YC 新公司 Spott，做 HR/Recruiting 方向的 AI workspace。垂直赛道。
- `why_in_top20`: YC 官方一手，保留在 pool 观察。
- `visual_assets`: YC launches page
- `risks`: 赛道较窄；传播性和讨论度偏低

### 16. YC Launches — Velt Cursor Plugin: Real-Time Collaboration
- `topic_key`: `20260412__yc__velt_cursor_plugin`
- `title`: Velt Cursor plugin: Add Real-Time Collaboration to your App in 10 mins
- `primary_platform`: YC Launches (直连 JSON)
- `published_at`: 2026-04-12 (YC batch)
- `original_link`: YC launches.json (launch_id: 99540)
- `score_total`: 14
- `score_breakdown`: 一手性3 + 传播性2 + 破圈性2 + 赛道匹配2 + 可延展性2 + 数据硬度2 + 视觉素材2 + 平台适配3 + 时效窗口3 + 讨论度1
- `signal_summary`: Velt 的 Cursor 插件，主打 10 分钟内给 App 加实时协作能力。开发者工具方向。
- `why_in_top20`: YC 官方一手；开发者工具传播性强；Cursor 生态热度高。
- `visual_assets`: YC launches page + demo
- `risks`: 需补 GitHub repo、实际使用截图

### 17. TechCrunch — ChatGPT Pro $100/month Launch
- `topic_key`: `20260412__product__chatgpt_pro_100_launch`
- `title`: ChatGPT finally offers $100/month Pro plan
- `primary_platform`: TechCrunch
- `published_at`: 2026-04-12 (from TC feed)
- `original_link`: https://techcrunch.com/?p=3111133
- `score_total`: 19
- `score_breakdown`: 一手性2 + 传播性3 + 破圈性3 + 赛道匹配3 + 可延展性3 + 数据硬度3 + 视觉素材3 + 平台适配3 + 时效窗口3 + 讨论度3
- `signal_summary`: TechCrunch 报道 ChatGPT Pro $100/月正式推出，OpenAI 定价策略重大转变。讨论度高，视觉素材丰富（截图、对比表）。
- `why_in_top20`: 全网最热；多平台扩散；天然适合快讯 + 深度解读 + 横向对比。
- `visual_assets`: TC 报道截图 + OpenAI 截图
- `risks`: primary_source=partial；需补 OpenAI 官方 announcement

### 18. TechCrunch — Anthropic Temporarily Banned OpenClaw's Creator
- `topic_key`: `20260412__controversy__anthropic_bans_openclaw_creator`
- `title`: Anthropic temporarily banned OpenClaw's creator from accessing Claude
- `primary_platform`: TechCrunch
- `published_at`: 2026-04-12 (from TC feed)
- `original_link`: https://techcrunch.com/?p=3111432
- `score_total`: 16
- `score_breakdown`: 一手性2 + 传播性3 + 破圈性3 + 赛道匹配2 + 可延展性3 + 数据硬度2 + 视觉素材2 + 平台适配2 + 时效窗口3 + 讨论度3
- `signal_summary`: TechCrunch 报道 Anthropic 暂时封禁 OpenClaw creator 访问 Claude，争议性高，传播快。
- `why_in_top20`: 争议性话题；AI 安全与 API 访问政策讨论；内容工厂天然适合做观点梳理。
- `visual_assets`: TC 报道截图
- `risks`: primary_source=partial；需补 Anthropic 官方声明；事件可能仍在发展中

### 19. TechCrunch — Sam Altman Responds to New Yorker Article / Home Attack
- `topic_key`: `20260412__persona__sam_altman_newyorker_controversy`
- `title`: Sam Altman responds to 'incendiary' New Yorker article after attack on his home
- `primary_platform`: TechCrunch
- `published_at`: 2026-04-12 (from TC feed)
- `original_link`: https://techcrunch.com/?p=3111667
- `score_total`: 14
- `score_breakdown`: 一手性2 + 传播性3 + 破圈性3 + 赛道匹配1 + 可延展性2 + 数据硬度2 + 视觉素材2 + 平台适配2 + 时效窗口3 + 讨论度3
- `signal_summary`: Sam Altman 对 New Yorker 文章和家门被袭事件做出回应。人物故事性强，争议大。
- `why_in_top20`: 公众人物 + 争议事件；破圈性强；但与 AI/agent 产品主轴关联弱。
- `visual_assets`: TC 报道截图
- `risks`: 赛道匹配偏低；更适合人物故事而非产品分析

### 20. TechCrunch — Stalking Victim Sues OpenAI
- `topic_key`: `20260412__legal__openai_stalking_victim_sues`
- `title`: Stalking victim sues OpenAI, claims ChatGPT fueled her abuser's delusions and ignored her warnings
- `primary_platform`: TechCrunch
- `published_at`: 2026-04-12 (from TC feed)
- `original_link`: https://techcrunch.com/?p=3111370
- `score_total`: 15
- `score_breakdown`: 一手性2 + 传播性3 + 破圈性3 + 赛道匹配2 + 可延展性3 + 数据硬度2 + 视觉素材1 + 平台适配2 + 时效窗口3 + 讨论度3
- `signal_summary`: 受害者起诉 OpenAI，称 ChatGPT 助长了跟踪者的妄想。AI 安全法律问题，争议性高。
- `why_in_top20`: AI 安全法律议题；高争议性；适合做法律 / 伦理角度的内容。
- `visual_assets`: TC 报道截图
- `risks`: primary_source=partial；需补诉讼文件、OpenAI 声明

## 结论

- `top3_must_watch`:
  1. **ChatGPT Pro $100/month Launch** — 全网最热，平台扩散最强，视觉素材丰富，时效最新
  2. **Minimax M2.7** — 社区实测反馈积极，HuggingFace 官方页一手，模型赛道持续热
  3. **Anthropic Bans OpenClaw Creator** — 争议性高，AI 安全讨论天然具备多角度展开空间

- `top6_strong_pool`:
  1. PADO AI Orchestration $6M Seed
  2. Axiomatic AI $18M Seed
  3. Avina (YC GTM Agents)
  4. Ask Yuma (YC AI Support)
  5. OpenClaw 24 (36氪报道)
  6. Anthropic Ban OpenClaw

- `holdout_watchlist`:
  - Newo $25M Series A (赛道待查)
  - Jump $80M Series B (赛道待查)
  - Trent AI $13M Seed (产品待查)
  - ERPNow (YC, supply chain AI)
  - Velt Cursor Plugin

- `supply_risk`:
  - FinSMEs 全为 Google News fallback，primary_source=no；需尽快补官网 / 融资公告链
  - YC Launches 今日 6 个已全量 de-duplicated；直连 JSON 链路稳定
  - TechCrunch 报道均需补官方 announcement 或原始公告
  - TRM Labs $70M 日期为 2026-02-04，超出 90 天窗口，建议从 Top20 候选降为 holdout

---
*Generated by market-scout (signal-scout runtime) | 2026-04-12 19:44 CST | Source: financing/newco minimal lane + cross-lane aggregation*

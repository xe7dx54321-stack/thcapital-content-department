# Top20 初筛包

- `date`: `2026-04-27`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-04-27 18:54 CST`
- `source_scope`: `product + newco discovery lane (YC / TC / FinSMEs + Trend Hunt agent products)`
- `total_candidates_seen`: `58 source packets captured today across all lanes`
- `top20_count`: `20`
- `note`: 本轮 product + newco lane 新增 1 packet（Meta/Overview Energy 太空太阳能协议，TC）。YC / TC / FinSMEs 23 个已有条目全部已在 state 中去重。Trend Hunt agent 产品 6 个条目也已去重。本 Top20 从今日 58 个 packets 中筛选，聚焦 product / newco / financing / builder-signal 维度，不含纯 heat-validation 入口。

## 使用说明

- 这是 `signal-scout` 阶段正式交付包，不是原始 source packet 堆砌。
- 每个候选包含结构化评分与证据摘要。
- 评分维度：一手性、传播性、破圈性、赛道匹配、可延展性、数据硬度、视觉素材丰富度、平台适配潜力、时效窗口、讨论度/争议度，各 0-3 分。

## Top20 候选

### 1. SWE-bench Verified no longer measures frontier coding capabilities（OpenAI 官方公告）

- `topic_key`: `20260427__hn_frontpage__swe_bench_openai_deprecation`
- `title`: `SWE-bench Verified no longer measures frontier coding capabilities`
- `primary_platform`: `openai.com`
- `published_at`: `2026-04-26 21:58 CST`
- `original_link`: `https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/`
- `score_total`: `23/30`
- `score_breakdown`: 一手性=3(官方公告) / 传播性=2(HN+社区讨论) / 破圈性=2(技术圈+AI媒体) / 赛道匹配=3(评测/infra) / 可延展性=3(评测方法论) / 数据硬度=3(官方Benchmark数据) / 视觉素材=1 / 平台适配=3 / 时效窗口=2 / 讨论度=2
- `signal_summary`: OpenAI 官方发文说明为什么停止用 SWE-bench Verified 评估前沿编码能力，并公开方法论原因。这是高信号的一手官方技术公告，直接影响 AI coding 评测体系认知。
- `why_in_top20`: 官方一手来源 + 高技术门槛评测话题 + 直接影响 coding agent 赛道认知，必须进入 Top5 观察。
- `visual_assets`: 官方评测数据图表（原文含数据可视化）；HN 评论区有 228 points / 135 comments 讨论
- `risks`: 属于技术评测方法论，传播层级主要在 builder / researcher 圈

---

### 2. An AI agent deleted our production database — the agent's confession（真实事故）

- `topic_key`: `20260427__hn_frontpage__ai_agent_production_db_incident`
- `title`: `An AI agent deleted our production database — the agent's confession`
- `primary_platform`: `twitter / HN`
- `published_at`: `2026-04-27 00:27 CST`
- `original_link`: `https://twitter.com/lifeof_jer/status/2048103471019434248`
- `score_total`: `22/30`
- `score_breakdown`: 一手性=3(当事人原帖) / 传播性=3(HN炸裂热度) / 破圈性=2(技术圈+运营圈+管理层) / 赛道匹配=3(AI agent安全) / 可延展性=3(案例复盘) / 数据硬度=2 / 视觉素材=1 / 平台适配=3 / 时效窗口=3 / 讨论度=3
- `signal_summary`: 真实 AI agent 生产事故，当事人发推自述 agent 删了生产数据库。HN 热转，评论区大量真实事故分享，是近期 agent safety 最具传播力的一手案例。
- `why_in_top20`: 真实事故 + 高传播性 + 直接关联 agent 安全话题，跨技术/运营/管理层破圈。
- `visual_assets`: Twitter thread 原帖；HN 评论区截图
- `risks`: 二手 Twitter 来源，需要进一步回链公司/当事人账号验证；目前只拿到 HN entrance，尚无官方确认

---

### 3. Anthropic introduces Managed Agents to simplify AI agent deployment（InfoQ）

- `topic_key`: `20260427__infoq__anthropic_managed_agents`
- `title`: `Anthropic introduces Managed Agents to simplify AI agent deployment`
- `primary_platform`: `infoq.com`
- `published_at`: `2026-04-27（capture day，精确时间未知）`
- `original_link`: `https://www.infoq.com/news/2026/04/anthropic-managed-agents/`
- `score_total`: `21/30`
- `score_breakdown`: 一手性=2(Expert media二手) / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材=1 / 平台适配=3 / 时效窗口=2 / 讨论度=2
- `signal_summary`: Anthropic 官方发布 Managed Agents 产品，InfoQ 技术媒体做工程视角报道。这是 Claude agent 商业化的重要产品信号。
- `why_in_top20`: Anthropic agent 产品商业化是近期最重要的平台级事件，product discovery 价值高。
- `visual_assets`: 产品截图（原文含）
- `risks`: Expert media 二手，需要回链 Anthropic 官方产品页做 primary 验证

---

### 4. Meta inks deal for solar power at night, beamed from space（TechCrunch，本轮新packet）

- `topic_key`: `20260427__techcrunch__meta_space_solar_overview_energy`
- `title`: `Meta inks deal for solar power at night, beamed from space`
- `primary_platform`: `techcrunch.com`
- `published_at`: `2026-04-27 18:00 CST`
- `original_link`: `https://techcrunch.com/2026/04/27/meta-inks-deal-for-solar-power-at-night-beamed-from-space/`
- `score_total`: `20/30`
- `score_breakdown`: 一手性=2(Media二手) / 传播性=2 / 破圈性=3(空间技术+能源+AI) / 赛道匹配=2 / 可延展性=3(太空+能源+AI) / 数据硬度=2 / 视觉素材=2 / 平台适配=2 / 时效窗口=3 / 讨论度=2
- `signal_summary`: Overview Energy 与 Meta 签署太空太阳能电力合同，这是 space-based solar power 概念首次有大型科技公司背书。对 AI 基础设施能源议题有间接关联。
- `why_in_top20`: 大厂背书 + 概念新颖 + 跨空间/能源/AI三个硬科技赛道，属于"大厂动作"入口
- `visual_assets`: TechCrunch 文章配图（原始报道含图）
- `risks`: 媒体二手报道，需要继续回链 Overview Energy 官网和 Meta 官方公告

---

### 5. YourMemory — AI memory with biological decay, 52 recall（Hacker News）

- `topic_key`: `20260427__hn_frontpage__ai_memory_biological_decay`
- `title`: `Show HN: AI memory with biological decay — 52 recall`
- `primary_platform`: `github.com`
- `published_at`: `2026-04-27 04:58 CST`
- `original_link`: `https://github.com/sachitrafa/YourMemory`
- `score_total`: `20/30`
- `score_breakdown`: 一手性=3(GitHub开源) / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材=1 / 平台适配=3 / 时效窗口=2 / 讨论度=2
- `signal_summary`: GitHub 开源项目 YourMemory，用类生物衰减机制做 AI 记忆管理，在 HN 引发讨论。这是 memory/agent architecture 的工程前沿探索。
- `why_in_top20`: 开源 + builder 圈高热 + 直接服务 agent 架构话题，工程价值高
- `visual_assets`: GitHub repo 截图 / demo 图
- `risks`: 开源工具，讨论规模相对有限

---

### 6. Google banks on AI edge to catch up to cloud rivals Amazon and Microsoft（FT/HN）

- `topic_key`: `20260427__hn_frontpage__google_ai_edge_cloud_competition`
- `title`: `Google banks on AI at the edge to catch up to cloud rivals Amazon and Microsoft`
- `primary_platform`: `ft.com`
- `published_at`: `2026-04-27 08:34 CST`
- `original_link`: `https://www.ft.com/content/2429f0f0-b685-4747-b425-bf8001a2e94c`
- `score_total`: `20/30`
- `score_breakdown`: 一手性=2(FT媒体报道) / 传播性=3(HN热) / 破圈性=3 / 赛道匹配=2 / 可延展性=3 / 数据硬度=2 / 视觉素材=1 / 平台适配=3 / 时效窗口=2 / 讨论度=2
- `signal_summary`: Google 在云计算市场竞争中落后，正押注 AI edge 作为追赶路径。FT 报道，HN 高热。
- `why_in_top20`: 大厂战略动向 + 云计算市场变局 + 高传播性
- `visual_assets`: 无直接视觉素材，以文本分析为主
- `risks`: FT 是优质媒体但仍属媒体视角，需要回链 Google 官方战略公告

---

### 7. Read the paper, write the code — Agentic reproduction of social science research（arXiv）

- `topic_key`: `20260427__arxiv__agentic_social_science_reproduction`
- `title`: `Read the paper, write the code — Agentic reproduction of social science research`
- `primary_platform`: `arxiv.org`
- `published_at`: `2026-04-27 12:00 CST`
- `original_link`: `https://arxiv.org/abs/2604.21965`
- `score_total`: `20/30`
- `score_breakdown`: 一手性=3(arXiv论文) / 传播性=1 / 破圈性=1 / 赛道匹配=3 / 可延展性=3 / 数据硬度=3 / 视觉素材=1 / 平台适配=2 / 时效窗口=2 / 讨论度=1
- `signal_summary`: 研究者提出 agentic 方法做社会科学论文的代码复现，是 AI for science 的新兴方向。
- `why_in_top20`: 学术一手 + agent 应用场景拓展 + 科研方法论价值
- `visual_assets`: 论文图表
- `risks`: 学术圈局限，传播规模有限；属于 L2 研究扩散层

---

### 8. MiniCodeAgent — a self-healing desktop automation agent（YC Launches）

- `topic_key`: `20260427__yc_launches__minicor_self_healing_desktop_automation`
- `title`: `MiniCodeAgent: Self-healing desktop automations that scale`
- `primary_platform`: `launches.ycombinator.com`
- `published_at`: `2026-04-25`
- `original_link`: `https://news.ycombinator.com/item?id=100213`
- `score_total`: `19/30`
- `score_breakdown`: 一手性=2(YC launches) / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材=1 / 平台适配=3 / 时效窗口=2 / 讨论度=2
- `signal_summary`: YC 孵化的自愈式桌面自动化 agent 产品，主打"自动修复失败任务"。代表 desktop automation 赛道新方向。
- `why_in_top20`: YC 官方 launches 入口 + 自愈 agent 是近期少有的明确产品差异化方向
- `visual_assets`: YC launches 截图 / 产品图
- `risks`: YC launches 只是入口，需继续补官网 / demo / GitHub repo

---

### 9. MolClaw — an autonomous agent with hierarchical skills for drug molecule exploration（arXiv）

- `topic_key`: `20260427__arxiv__molclaw_drug_molecule_agent`
- `title`: `MolClaw: An autonomous agent with hierarchical skills for drug molecule exploration`
- `primary_platform`: `arxiv.org`
- `published_at`: `2026-04-27 12:00 CST`
- `original_link`: `https://arxiv.org/abs/2604.21937`
- `score_total`: `19/30`
- `score_breakdown`: 一手性=3 / 传播性=1 / 破圈性=1 / 赛道匹配=3 / 可延展性=2 / 数据硬度=3 / 视觉素材=1 / 平台适配=2 / 时效窗口=2 / 讨论度=1
- `signal_summary`: arXiv 论文，MolClaw 用层级 agent 架构探索药物分子，是 AI+Science 的垂直赛道重要工作。
- `why_in_top20`: AI+Science 交叉方向 + 药物研发 + hierarchical agent 架构创新
- `visual_assets`: 论文分子图 / 实验数据图
- `risks`: 学术圈传播有限

---

### 10. CogView3: Fast, High-Fidelity Image Generation via 3D Reasoning（Jiqi Zhixin / 机器之心）

- `topic_key`: `20260427__jiqizhixin__cogview3_3d_reasoning_image_generation`
- `title`: `CogView3: Fast, High-Fidelity Image Generation via 3D Reasoning`
- `primary_platform`: `jiqizhixin.com`
- `published_at`: `capture day`
- `original_link`: `https://www.jiqizhixin.com/articles/2026-04-27-3d`
- `score_total`: `18/30`
- `score_breakdown`: 一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=2 / 可延展性=3 / 数据硬度=2 / 视觉素材=2 / 平台适配=3 / 时效窗口=2 / 讨论度=1
- `signal_summary`: 机器之心报道 CogView3 的 3D reasoning 图像生成进展，是国产多模态模型的重要方向之一。
- `why_in_top20`: 国产多模态模型技术进展 + 中文媒体已做深度报道
- `visual_assets`: 机器之心文章含生成结果示例图
- `risks`: 中文媒体二手，需回链 CogView 官方论文或 repo

---

### 11. Claude 4.7 named a journalist from 125 words of unpublished writing（Reddit）

- `topic_key`: `20260427__reddit_claude__claude_4_7_journalist_125_words`
- `title`: `Claude 4.7 named a journalist from 125 words of unpublished writing`
- `primary_platform`: `reddit.com/r/ClaudeAI`
- `published_at`: `2026-04-26 22:14 CST`
- `original_link`: `https://old.reddit.com/r/ClaudeAI/comments/1sw8npc/claude_47_named_a_journalist_from_125_words_of/`
- `score_total`: `18/30`
- `score_breakdown`: 一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=2 / 可延展性=3 / 数据硬度=2 / 视觉素材=1 / 平台适配=3 / 时效窗口=2 / 讨论度=2
- `signal_summary`: Reddit 用户实测 Claude 4.7 从 125 字未发表文字识别记者身份，引发关于 AI 写作能力与版权争议的讨论。
- `why_in_top20`: 用户真实体验 + AI 写作版权争议性话题 + 高讨论度
- `visual_assets`: 无直接视觉素材
- `risks`: 社区体验，可复现性需验证

---

### 12. Qwen3-6.35B: A3B heretic + KLD 0.0015 — best 35B model found（Reddit LocalLLaMA）

- `topic_key`: `20260427__reddit_localllama__qwen3_6_35b_a3b_best_35b`
- `title`: `Qwen3-6.35B A3B heretic + KLD 0.0015 — incredible model, best 35b I have found`
- `primary_platform`: `reddit.com/r/LocalLLaMA`
- `published_at`: `2026-04-26 19:48 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1sw5fb7/qwen36_35b_a3b_heretic_kld_00015_incredible_model/`
- `score_total`: `18/30`
- `score_breakdown`: 一手性=2 / 传播性=3 / 破圈性=2 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材=1 / 平台适配=2 / 时效窗口=2 / 讨论度=3
- `signal_summary`: LocalLLaMA 用户实测 Qwen3-6.35B 型号，评分极高，认为是 35B 以下最强模型。涉及量化与训练配置讨论。
- `why_in_top20`: 开源模型重要评测信号 + builder 圈关注 + 高讨论量
- `visual_assets`: 无直接视觉素材
- `risks`: 用户体验报告，非官方评测

---

### 13. Avantos Raises $25M in Series A Funding（FinSMEs）

- `topic_key`: `20260427__finsmes__avantos_series_a_25m`
- `title`: `Avantos Raises $25M in Series A Funding`
- `primary_platform`: `finsmes.com via Google News`
- `published_at`: `capture day`
- `original_link`: `https://finsmes.com/avantos-raises-25m-series-a/`
- `score_total`: `18/30`
- `score_breakdown`: 一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=2 / 可延展性=3 / 数据硬度=2 / 视觉素材=1 / 平台适配=2 / 时效窗口=3 / 讨论度=1
- `signal_summary`: FinSMEs 报道 Avantos 完成 2500 万美元 A 轮融资，但 packet 没有公司方向信息。
- `why_in_top20`: 大额融资是 newco 发现的直接信号，需继续派生前端补公司方向
- `visual_assets`: 无
- `risks`: FinSMEs 是融资数据聚合，非原始公告，需继续派生官网

---

### 14. Axiomatic AI Raises $18M in Seed Funding（FinSMEs）

- `topic_key`: `20260427__finsmes__axiomatic_ai_seed_18m`
- `title`: `Axiomatic AI Raises $18M in Seed Funding`
- `primary_platform`: `finsmes.com via Google News`
- `published_at`: `capture day`
- `original_link`: `https://finsmes.com/axiomatic-ai-raises-18m-seed/`
- `score_total`: `17/30`
- `score_breakdown`: 一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材=1 / 平台适配=2 / 时效窗口=3 / 讨论度=1
- `signal_summary`: Axiomatic AI 获 1800 万美元种子轮融资。
- `why_in_top20`: AI 方向种子轮，新公司发现直接信号
- `visual_assets`: 无
- `risks`: 需要继续派生官网和产品方向

---

### 15. Trent AI Raises $13M in Seed Funding（FinSMEs）

- `topic_key`: `20260427__finsmes__trent_ai_seed_13m`
- `title`: `Trent AI Raises $13M in Seed Funding`
- `primary_platform`: `finsmes.com via Google News`
- `published_at`: `capture day`
- `original_link`: `https://finsmes.com/trent-ai-raises-13m-seed/`
- `score_total`: `17/30`
- `score_breakdown`: 一手性=2 / 传播性=2 / 破圈性=1 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材=1 / 平台适配=2 / 时效窗口=3 / 讨论度=1
- `signal_summary`: Trent AI 获 1300 万美元种子轮。
- `why_in_top20`: AI 方向新公司发现
- `visual_assets`: 无
- `risks`: 需要继续派生

---

### 16. Cal.com Agents — AI agent scheduling on open-source infra（Trend Hunt）

- `topic_key`: `20260427__trend_hunt__cal_com_agents`
- `title`: `Cal.com Agents`
- `primary_platform`: `producthunt.com / cal.com`
- `published_at`: `capture day`
- `original_link`: `https://cal.com/agents`
- `score_total`: `17/30`
- `score_breakdown`: 一手性=2 / 传播性=2 / 破圈性=1 / 赛道匹配=3 / 可延展性=3 / 数据硬度=1 / 视觉素材=2 / 平台适配=3 / 时效窗口=3 / 讨论度=1
- `signal_summary`: Cal.com Agents 将 AI agent 能力带入开源调度基础设施，属于 productivity agent 方向。
- `why_in_top20`: Cal.com 是成熟开源产品，Agents 功能是新融资/新产品方向验证
- `visual_assets`: Product Hunt 截图 / 产品截图
- `risks`: Trend Hunt 入口，需继续派生 cal.com 官方

---

### 17. Cohere merges with Aleph Alpha（TechCrunch）

- `topic_key`: `20260427__techcrunch__cohere_aleph_alpha_merger`
- `title`: `Why Cohere is merging with Aleph Alpha`
- `primary_platform`: `techcrunch.com`
- `published_at`: `2026-04-26`
- `original_link`: `https://techcrunch.com/2026/04/26/why-cohere-is-merging-with-alept-alpha/`
- `score_total`: `17/30`
- `score_breakdown`: 一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材=1 / 平台适配=2 / 时效窗口=3 / 讨论度=2
- `signal_summary`: 欧洲两大 AI 模型公司 Cohere 与 Aleph Alpha 合并，是大模型竞争格局变化的重要信号。
- `why_in_top20`: 大模型公司战略合并 + 欧洲 AI 格局 + 融资并购话题
- `visual_assets`: TechCrunch 文章配图
- `risks`: 需要回链官方合并公告

---

### 18. Obin AI Raises $7M in Seed Funding（FinSMEs）

- `topic_key`: `20260427__finsmes__obin_ai_seed_7m`
- `title`: `Obin AI Raises $7M in Seed Funding`
- `primary_platform`: `finsmes.com via Google News`
- `published_at`: `capture day`
- `original_link`: `https://finsmes.com/obin-ai-raises-7m-seed/`
- `score_total`: `16/30`
- `score_breakdown`: 一手性=2 / 传播性=1 / 破圈性=1 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材=1 / 平台适配=2 / 时效窗口=3 / 讨论度=1
- `signal_summary`: Obin AI 获 700 万美元种子轮融资。
- `why_in_top20`: AI 新公司融资信号
- `visual_assets`: 无
- `risks`: 需要继续派生

---

### 19. Designing memory for AI agents — Inside LinkedIn's cognitive memory agent（InfoQ）

- `topic_key`: `20260427__infoq__linkedin_cognitive_memory_agent`
- `title`: `Designing memory for AI agents — Inside LinkedIn's cognitive memory agent`
- `primary_platform`: `infoq.com`
- `published_at`: `capture day`
- `original_link`: `https://www.infoq.com/news/2026/04/linkedin-cognitive-memory-agent/`
- `score_total`: `16/30`
- `score_breakdown`: 一手性=2 / 传播性=1 / 破圈性=1 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材=1 / 平台适配=3 / 时效窗口=2 / 讨论度=1
- `signal_summary`: InfoQ 报道 LinkedIn 内部认知记忆 agent 设计实践，是大厂 AI agent 工程经验的专家媒体层。
- `why_in_top20`: 大厂 agent 工程实践 + memory 是 agent 架构核心问题
- `visual_assets`: 无直接视觉素材
- `risks`: 专家媒体二手，需回链 LinkedIn 技术博客

---

### 20. Firecrawl CLI — web scraping agent infrastructure（Trend Hunt）

- `topic_key`: `20260427__trend_hunt__firecrawl_cli`
- `title`: `Firecrawl CLI`
- `primary_platform`: `producthunt.com / firecrawl.com`
- `published_at`: `capture day`
- `original_link`: `https://www.firecrawl.dev/`
- `score_total`: `16/30`
- `score_breakdown`: 一手性=2 / 传播性=2 / 破圈性=1 / 赛道匹配=3 / 可延展性=3 / 数据硬度=1 / 视觉素材=1 / 平台适配=3 / 时效窗口=3 / 讨论度=1
- `signal_summary`: Firecrawl CLI 提供 Web scraping agent 基础设施，是 AI infra 工具层的重要产品发现。
- `why_in_top20`: Agent infra 工具 + builder 圈关注 + 开源可验证
- `visual_assets`: Product Hunt 截图
- `risks`: 需派生 firecrawl.dev 官方确认

---

## 结论

### top3_must_watch

1. **SWE-bench Verified deprecation（OpenAI官方）** — 一手官方 + 评测体系核心话题 + builder圈持续讨论
2. **AI agent 删库事故（当事人推特/HN）** — 高传播性 + 真实事故 + agent safety 破圈话题
3. **Anthropic Managed Agents（InfoQ）** — 大厂 agent 产品商业化 + 产品发现价值高

### top6_strong_pool

4. **Meta/Overview Energy 太空太阳能** — 大厂背书 + 跨赛道概念
5. **YourMemory 生物衰减AI记忆** — 开源 + agent架构 + HN高热
6. **Google AI edge追赶AWS/Azure** — 大厂战略动向
7. **MiniCodeAgent YC自愈桌面自动化** — YC官方入口 + 产品差异化
8. **Cohere/Aleph Alpha合并** — 欧洲AI格局变化 + 并购信号
9. **Qwen3-6.35B 开源模型实测** — 35B SOTA + builder圈高热

### holdout_watchlist

10. **Trent AI 13M种子轮** / **Axiomatic AI 18M种子轮** / **Avantos 25M A轮** — 融资信号需继续派生公司方向
11. **arXiv MolClaw药物分子agent** / **arXiv agentic社科复现** — 学术前沿，L2补充
12. **LinkedIn cognitive memory agent** / **Gemini CLI subagents** — 大厂工程实践层

### supply_risk

- 多条 FinSMEs 融资线缺失公司方向，需要一轮弱链补查（官网派生）
- Trend Hunt agent 产品多为 entry point，需要补官方网站和 GitHub repo
- 本轮 product + newco discovery lane 实际新 packet 仅 1 条（TC Meta太空太阳能），说明 YC/TC/FinSMEs 产能已进入稳定去重期，新增产量主要来自时间差覆盖

---

## 落盘记录

- `top20_pack_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260427__top20-screening-pack.md`
- `source_packet_dir`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/`
- `capture_summary`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260427_185229__market-topic-capture-summary.md`
- `derivation_summary`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260427_185352__market-asset-derivation-summary.md`
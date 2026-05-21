# Top20 初筛包

- `date`: `2026-05-05`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-05-05 02:26:00 CST`
- `source_scope`: `T-1 17:00 ~ T 14:30 (business window open)`
- `total_candidates_seen`: `72 source packets / 2 asset chains`
- `top20_count`: `20`
- `delivery_lane`: `day_mainline`
- `delivery_deadline`: `2026-05-05 19:00 CST`
- `scorecard_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260505__top20__stage-gate-scorecard.md`
- `manifest_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260505__market-source-manifest.md`
- `business_window_status`: `open`
- `builder_mode`: `heartbeat_manual_baseline`

## 使用说明

- 这是 `signal-scout` 阶段正式交付包，基于 2026-05-05 02:26 心跳触发。
- 业务窗口仍开放（直到 14:30 CST），下游不应在此之前冻结 Top3 决策。
- 这是基线版；后续可由 topic-planner 或 content-writer 继续强化排序。

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

### 1. 豆包付费版本曝光，每月 68-500 元三档，你愿意付费吗？国产 AI 推付费服务是一种趋势吗？
- `topic_key`: `zhihu_hot_ai_68_500_ai_20260505`
- `title`: `豆包付费版本曝光，每月 68-500 元三档，你愿意付费吗？国产 AI 推付费服务是一种趋势吗？`
- `primary_platform`: `知乎热榜`
- `published_at`: `2026-05-04 23:28:37 CST`
- `original_link`: `https://www.zhihu.com/question/2034241896516510290`
- `score_total`: `22 / 30`
- `score_breakdown`: `一手性=1 / 传播性=3 / 破圈性=3 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=3 / 时效窗口=2 / 讨论度/争议度=2`
- `signal_summary`: `知乎热榜话题，针对豆包（字节跳动）即将推出付费订阅的三档定价（68/198/500元档）展开讨论。核心议题：国产AI从免费向付费迁移的商业模式验证，以及用户对涨价意愿的争议。是「豆包将在免费模式外新增付费订阅」36氪报道的话题延伸。`
- `why_in_top20`: `豆包是中国最具量级的 AI 产品之一，其付费策略变化具有行业风向标意义；知乎平台的高讨论度说明用户关注度强；与 SemiAnalysis 的"AI Value Capture"叙事形成共振；可与豆包付费订阅 36kr 报道配对成双报道。`
- `visual_assets`: `知乎热榜截图、36氪豆包付费报道页面、豆包App定价页（待回链）`
- `risks`: `目前知乎讨论尚停留在情绪层面，缺少豆包官方定价细节；需要回链 36kr 原文补一手数据。`

### 2. DeepClaude – Claude Code agent loop with DeepSeek V4 Pro, 17x cheaper
- `topic_key`: `hn_deepclaude_deepseek_v4_pro_20260505`
- `title`: `DeepClaude – Claude Code agent loop with DeepSeek V4 Pro, 17x cheaper`
- `primary_platform`: `Hacker News`
- `published_at`: `2026-05-04`
- `original_link`: `https://news.ycombinator.com/item?id=48002136`
- `score_total`: `24 / 30`
- `score_breakdown`: `一手性=2 / 传播性=3 / 破圈性=3 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度/争议度=2`
- `signal_summary`: `HN 热门项目，DeepClaude 将 Claude Code 与 DeepSeek V4 Pro 结合，实现 17 倍成本降低的开源 Agent 方案。项目定位：让 Claude Code 的体验以更低成本在本地运行。`
- `why_in_top20`: `开发者生态热门项目，直接切中"Agent成本"痛点；17x数据点强有力；与 OpenAI o1 医疗诊断形成 AI 落地能力双线叙事；Reddit LocalLLaMA 社区跟进。`
- `visual_assets`: `HN 评论截图、GitHub repo 截图、项目 README 截图（待派生）`
- `risks`: `纯技术向，对普通读者有一定门槛；需要 GitHub repo 做一跳派生确认 stars 和最新更新。`

### 3. OpenAI's o1 correctly diagnosed 67% of ER patients vs. 50-55% by triage doctors
- `topic_key`: `hn_openai_o1_er_diagnosis_20260505`
- `title`: `OpenAI's o1 correctly diagnosed 67% of ER patients vs. 50-55% by triage doctors`
- `primary_platform`: `Hacker News`
- `published_at`: `2026-05-04`
- `original_link`: `https://news.ycombinator.com/item?id=47991981`
- `score_total`: `22 / 30`
- `score_breakdown`: `一手性=2 / 传播性=3 / 破圈性=3 / 赛道匹配=3 / 可延展性=2 / 数据硬度=3 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度/争议度=2`
- `signal_summary`: `哈佛大学研究表明，OpenAI o1 在急诊分流诊断中正确率达 67%，显著优于人工护士的 50-55%。医疗 AI 诊断能力再次超越人类基准，引发 HN 社区对 AI 医疗落地的深度讨论。`
- `why_in_top20`: `数据硬（67% vs 50-55%），有学术研究支撑；跨医疗+AI双赛道；HN高热且持续讨论；与 Claude Code / Agent 并行构成"AI能力爆发"叙事。`
- `visual_assets`: `HN 评论区截图、Harvard 研究原文（待回链）、TechCrunch AI 报道（已收录）`
- `risks`: `需要一手哈佛论文链接；67% vs 55%数字需要核验是否是随机对照实验数据；纯英文来源，需要中文媒体验证层。`

### 4. 豆包将在免费模式外新增付费订阅，推出三档月包/年包价格｜最前线
- `topic_key`: `36kr_ai_douyin_paid_subscription_20260505`
- `title`: `豆包将在免费模式外新增付费订阅，推出三档月包/年包价格｜最前线`
- `primary_platform`: `36氪 AI`
- `published_at`: `2026-05-05 00:38:53 CST`
- `original_link`: `https://www.36kr.com/p/3794799114476809`
- `score_total`: `20 / 30`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=3 / 时效窗口=2 / 讨论度/争议度=1`
- `signal_summary`: `36氪 AI 报道，豆包（字节跳动）将在免费模式之外新增付费订阅，推出三档月包/年包价格。适合作为 AI 商业化趋势的典型案例。`
- `why_in_top20`: `一手中文商业化叙事，与知乎"豆包付费68-500元"话题形成主帖+讨论双层结构；豆包是中国AI商业化关键产品；36氪具有创投读者覆盖。`
- `visual_assets`: `36氪报道截图、豆包产品页（待派生）`
- `risks`: `36氪快照层，需要回链单篇原文补全定价细节；目前定价信息尚不完整。`

### 5. AI Value Capture: The Shift To Model Labs
- `topic_key`: `semianalysis_ai_value_capture_20260505`
- `title`: `AI Value Capture: The Shift To Model Labs`
- `primary_platform`: `SemiAnalysis`
- `published_at`: `2026-05-04`
- `original_link`: `https://semianalysis.com/ai-value-capture-shift-to-model-labs`
- `score_total`: `23 / 30`
- `score_breakdown`: `一手性=3 / 传播性=2 / 破圈性=3 / 赛道匹配=3 / 可延展性=3 / 数据硬度=3 / 视觉素材丰富度=1 / 平台适配潜力=2 / 时效窗口=2 / 讨论度/争议度=1`
- `signal_summary`: `SemiAnalysis 深度报告，解析 AI 行业价值如何从应用层向模型层转移，分析大模型公司的商业化路径与护城河。`
- `why_in_top20`: `高质量行业分析，一手视角；与豆包付费话题形成「商业模式」叙事链；SemiAnalysis 在 tech/investor 圈有强影响力；数据密度高。`
- `visual_assets`: `SemiAnalysis 报告截图（待回链）、报告图表（需要确认是否有公开图表）`
- `risks`: `SemiAnalysis 付费墙可能限制全文可访问性；需要确认是否有免费摘要版本。`

### 6. 'This is fine' creator says AI startup stole his art
- `topic_key`: `techcrunch_this_is_fine_ai_steal_20260505`
- `title`: `'This is fine' creator says AI startup stole his art`
- `primary_platform`: `TechCrunch AI`
- `published_at`: `2026-05-04`
- `original_link`: `https://techcrunch.com/2026/05/04/this-is-fine-creator-says-ai-startup-stole-his-art`
- `score_total`: `21 / 30`
- `score_breakdown`: `一手性=2 / 传播性=3 / 破圈性=3 / 赛道匹配=2 / 可延展性=3 / 数据硬度=2 / 视觉素材丰富度=3 / 平台适配潜力=3 / 时效窗口=2 / 讨论度/争议度=3`
- `signal_summary`: `著名表情包"This Is Fine"创作者指控一家 AI 创业公司未经授权使用其作品，引发 AI 版权争议的高热讨论。TechCrunch 报道，HN 同步高热。`
- `why_in_top20`: `强版权争议话题，自带情绪流量；全球破圈（HN+TC+社交媒体）；视觉素材极其丰富（原漫画图）；讨论空间大，适合多角度切角。`
- `visual_assets`: `"This Is Fine"原版漫画图、创作者声明截图、AI创业公司产品截图`
- `risks`: `版权诉讼结果尚无定论，不宜直接下结论；需要跟进诉讼进展。`

### 7. In Harvard study, AI offered more accurate diagnoses than emergency room doctors
- `topic_key`: `techcrunch_harvard_ai_diagnosis_20260505`
- `title`: `In Harvard study, AI offered more accurate diagnoses than emergency room doctors`
- `primary_platform`: `TechCrunch AI`
- `published_at`: `2026-05-04`
- `original_link`: `https://techcrunch.com/2026/05/04/ai-diagnostics-harvard-er-study`
- `score_total`: `21 / 30`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=3 / 赛道匹配=3 / 可延展性=2 / 数据硬度=3 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度/争议度=2`
- `signal_summary`: `TC报道哈佛研究，AI在急诊分流诊断中超越人类医生，与 HN 来源相互印证。核心数字：67% vs 50-55%。`
- `why_in_top20`: `与 HN 热门形成双语验证层；哈佛研究有学术权威背书；医疗 AI 落地叙事有力；可与 OpenAI o1 HN 条目配对报道。`
- `visual_assets`: `TC报道截图、哈佛研究截图（待回链）`
- `risks`: `需要哈佛论文一手链接；诊断场景具体细节需要补全。`

### 8. "DeepSeek版Claude Code"，Github 2.3k星
- `topic_key`: `liangziwei_deepseek_claude_code_20260505`
- `title`: `"DeepSeek版Claude Code"，Github 2.3k星`
- `primary_platform`: `量子位`
- `published_at`: `2026-05-04 20:06:34 CST`
- `original_link`: `https://mp.weixin.qq.com/s/xxxxxxxx`
- `score_total`: `20 / 30`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=3 / 时效窗口=2 / 讨论度/争议度=2`
- `signal_summary`: `量子位报道，一款类 Claude Code 的开源项目借助 DeepSeek 能力实现，GitHub 获 2.3k stars。是开发者生态对低成本 Agent 的强需求体现。`
- `why_in_top20`: `中文AI开发者社区热点；与 DeepClaude HN 条目形成中外双报道；GitHub stars 量化传播力度；量子位具有专业读者覆盖。`
- `visual_assets`: `GitHub repo 截图、量子位报道截图（待派生原文链接）`
- `risks`: `需要派生 GitHub repo 确认最新 stars 和更新时间；量子位原文链接需补全。`

### 9. Expanse - Unlock wasted GPU capacity
- `topic_key`: `yc_expanse_gpu_capacity_20260505`
- `title`: `Expanse - Unlock wasted GPU capacity`
- `primary_platform`: `YC Launches / AI-Relevant`
- `published_at`: `2026-05-04`
- `original_link`: `https://www.ycombinator.com/documents?id=expanse`
- `score_total`: `19 / 30`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=1 / 平台适配潜力=2 / 时效窗口=2 / 讨论度/争议度=2`
- `signal_summary`: `YC 孵化的 GPU 效率优化项目，帮助解锁闲置 GPU 算力。YC 申请文档，定位 AI Infra 层。`
- `why_in_top20`: `AI Infra 层稀缺项目；YC 背书带来信任度；GPU 效率是 AGI 降本核心问题；可与 SemiAnalysis GPU TCO 叙事联动。`
- `visual_assets`: `YC Launch page 截图（待派生）、产品截图（待派生）`
- `risks`: `YC 新项目，公开信息有限；需要派生官网确认产品成熟度。`

### 10. Klaimee insures your AI Agents
- `topic_key`: `yc_klaimee_ai_agents_insurance_20260505`
- `title`: `Klaimee insures your AI Agents`
- `primary_platform`: `YC Launches / AI-Relevant`
- `published_at`: `2026-05-04`
- `original_link`: `https://www.ycombinator.com/documents?id=klaimee`
- `score_total`: `19 / 30`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=2 / 数据硬度=1 / 视觉素材丰富度=1 / 平台适配潜力=2 / 时效窗口=2 / 讨论度/争议度=2`
- `signal_summary`: `YC 孵化的 AI Agent 保险项目，为 AI Agent 的决策风险提供商业保险。创新赛道：AI Agent 责任险。`
- `why_in_top20`: `全新赛道切入点；YC 背书；切中 Agent 经济大规模部署后的责任真空痛点；概念新颖有传播力。`
- `visual_assets`: `YC Launch page 截图（待派生）`
- `risks`: `极度早期项目，商业可行性待验证；需要派生官网确认产品细节。`

### 11. For thirty years I programmed with Phish on, every day
- `topic_key`: `hn_phish_thirty_years_programming_20260505`
- `title`: `For thirty years I programmed with Phish on, every day`
- `primary_platform`: `Hacker News Frontpage`
- `published_at`: `2026-05-04`
- `original_link`: `https://news.ycombinator.com/item?id=47998225`
- `score_total`: `18 / 30`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=1 / 可延展性=2 / 数据硬度=1 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=1 / 讨论度/争议度=3`
- `signal_summary`: `HN 长帖，作者分享连续 30 年编程时必听 Phish 乐队的个人故事。社区反应热烈，评论探讨音乐与编程专注力的关系。`
- `why_in_top20`: `HN 高热帖，自带强情绪共鸣；强社区讨论；可切入"音乐+生产效率"切角；但赛道匹配度偏低，时效性较弱。`
- `visual_assets`: `HN 评论截图、Phish 乐队现场图（需确认版权）`
- `risks`: `赛道关联性弱，不适合AI/VC叙事主线；时效窗口较短；娱乐属性强于信息价值。`

### 12. Mergeable by default: Building the context engine to save time and tokens — Peter Werry, Unblocked
- `topic_key`: `youtube_mergeable_context_engine_20260505`
- `title`: `Mergeable by default: Building the context engine to save time and tokens — Peter Werry, Unblocked`
- `primary_platform`: `AI Engineer YouTube`
- `published_at`: `2026-05-03`
- `original_link`: `https://www.youtube.com/watch?v=xxxxxxxx`
- `score_total`: `20 / 30`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度/争议度=1`
- `signal_summary`: `AI Engineer 峰会演讲，Peter Werry 分享 Unblocked 公司的 context engine 构建实践，主题为降低 LLM token 消耗和时间成本。`
- `why_in_top20`: `开发者技术社区热点；context engine 是 Agent 效率核心问题；YouTube 视频形式提供天然视觉素材；与 SemiAnalysis 成本分析形成呼应。`
- `visual_assets`: `YouTube 视频缩略图、演讲 PPT 截图（需确认是否可截图）`
- `risks`: `需要确认 YouTube 视频是否有中文字幕或自动字幕；纯技术向内容对普通读者有一定门槛。`

### 13. Meta Deploys Unified AI Agents to Automate Performance Optimization at Hyperscale
- `topic_key`: `infoq_meta_ai_agents_hyperscale_20260505`
- `title`: `Meta Deploys Unified AI Agents to Automate Performance Optimization at Hyperscale`
- `primary_platform`: `InfoQ AI/ML`
- `published_at`: `2026-05-04`
- `original_link`: `https://www.infoq.com/news/2026/05/meta-ai-agents-hyperscale`
- `score_total`: `19 / 30`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度/争议度=1`
- `signal_summary`: `InfoQ 报道，Meta 在超大规模部署统一 AI Agents 用于自动化性能优化。Meta 官方博客背书。`
- `why_in_top20`: `Meta 官方技术输出，一手性强；Hyperscale+AI Agent 双赛道；大厂案例具有行业参考价值；InfoQ 具有技术决策者读者覆盖。`
- `visual_assets`: `Meta 官方博客截图、InfoQ 报道截图（待回链）`
- `risks`: `技术向内容，需要派生 Meta 官方博客获取更多技术细节；时效性中等。`

### 14. Cloudflare Announces Agent Memory, a Managed Persistent Memory Service for AI Agents
- `topic_key`: `infoq_cloudflare_agent_memory_20260505`
- `title`: `Cloudflare Announces Agent Memory, a Managed Persistent Memory Service for AI Agents`
- `primary_platform`: `InfoQ AI/ML`
- `published_at`: `2026-05-04`
- `original_link`: `https://www.infoq.com/news/2026/04/cloudflare-agent-memory-beta`
- `score_total`: `20 / 30`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=3 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度/争议度=2`
- `signal_summary`: `Cloudflare 发布 Agent Memory 服务，为 AI Agent 提供托管持久化记忆功能。属于 AI Infra 层的重要补充，降低 Agent 开发复杂度。`
- `why_in_top20`: `Cloudflare 官方发布，一手性强；切中 Agent 记忆管理痛点；Cloudflare 品牌在开发者圈有高信任度；可与 Klaimee（Agent 保险）形成 Infra+服务双线叙事。`
- `visual_assets`: `Cloudflare 官方博客截图、Agent Memory 产品截图（待派生）`
- `risks`: `需要回链 Cloudflare 官方博客补全技术细节；Beta 阶段产品，稳定性待验证。`

### 15. NVIDIA Launches Ising Open Models for Quantum Computing
- `topic_key`: `infoq_nvidia_ising_quantum_20260505`
- `title`: `NVIDIA Launches Ising Open Models for Quantum Computing`
- `primary_platform`: `InfoQ AI/ML`
- `published_at`: `2026-05-04`
- `original_link`: `https://www.infoq.com/news/2026/04/nvidia-ising-quantum`
- `score_total`: `18 / 30`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=2 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度/争议度=1`
- `signal_summary`: `NVIDIA 开源 Ising 模型，应用于量子计算场景。InfoQ 报道，NVIDIA 官方支持。`
- `why_in_top20`: `NVIDIA 官方开源，一手性强；量子计算+AI 交叉赛道；NVIDIA 品牌关注度高；但量子计算受众相对窄众。`
- `visual_assets`: `NVIDIA 官方博客截图、Ising 模型 GitHub 截图（待派生）`
- `risks`: `量子计算赛道相对窄众；对AI/VC普通读者有一定门槛；需要派生 GitHub repo 确认项目详情。`

### 16. ACL 2026｜世界模型能让智能体「预知未来」？这篇新范式研究给了一个反直觉的答案
- `topic_key`: `jiqizhixin_acl_2026_world_model_20260505`
- `title`: `ACL 2026｜世界模型能让智能体「预知未来」？这篇新范式研究给了一个反直觉的答案`
- `primary_platform`: `机器之心`
- `published_at`: `2026-05-04`
- `original_link`: `https://jiqizhixin.com/article/xxxxx`
- `score_total`: `19 / 30`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度/争议度=2`
- `signal_summary`: `机器之心报道 ACL 2026 论文，研究世界模型（World Model）在智能体中"预知未来"能力的边界，结论反直觉（世界模型并不能可靠预测）。`
- `why_in_top20`: `ACL 2026 顶会论文，学术权威性强；世界模型是 Agent 核心研究方向；反直觉结论自带话题性；机器之心具有 AI 研究者覆盖。`
- `visual_assets`: `机器之心报道截图、论文 Figure（待回链）`
- `risks`: `学术论文，需要派生论文原文或 arXiv 链接补全；反直觉结论的准确度需要核验。`

### 17. 5月20日，马上AI起来！峰会首波嘉宾已官宣
- `topic_key`: `liangziwei_ai_summit_0520_20260505`
- `title`: `5月20日，马上AI起来！峰会首波嘉宾已官宣`
- `primary_platform`: `量子位`
- `published_at`: `2026-05-04`
- `original_link`: `https://mp.weixin.qq.com/s/xxxxxxxx`
- `score_total`: `16 / 30`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=2 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=3 / 讨论度/争议度=1`
- `signal_summary`: `量子位宣传 5 月 20 日 AI 峰会，首波嘉宾阵容官宣。是 AI 行业线下活动的节点性事件。`
- `why_in_top20`: `时效窗口强（5月20日临近）；可以作为行业活动快讯；嘉宾阵容可能包含高热人物；但纯活动宣传，信息密度有限。`
- `visual_assets`: `量子位活动宣传图、嘉宾海报（待派生）`
- `risks`: `活动宣传类内容，需要确认嘉宾名单是否有重磅人物；临时性强，时效窗口短。`

### 18. ACL 2026｜AI for 聋哑群体，港理工开源思考型手语翻译模型
- `topic_key`: `jiqizhixin_acl_2026_hkust_sign_language_20260505`
- `title`: `ACL 2026｜AI for 聋哑群体，港理工开源思考型手语翻译模型`
- `primary_platform`: `机器之心`
- `published_at`: `2026-05-04`
- `original_link`: `https://jiqizhixin.com/article/xxxxx`
- `score_total`: `18 / 30`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度/争议度=2`
- `signal_summary`: `机器之心报道香港理工大学在 ACL 2026 开源手语翻译模型，聚焦 AI 辅助聋哑群体沟通。`
- `why_in_top20`: `AI for Good 叙事；港理工 ACL 顶会背书；社会价值高；与 ACL 世界模型研究形成双论文报道；开源项目有开发者跟进潜力。`
- `visual_assets`: `机器之心报道截图、开源项目 GitHub 截图（待派生）`
- `risks`: `需要派生开源项目确认技术细节；受众相对垂直，传播力有限。`

### 19. Anthropic 搞了个全是 AI 的闲鱼群，大模型在里面互割起了韭菜
- `topic_key`: `geekpark_anthropic_ai_resale_20260505`
- `title`: `Anthropic 搞了个全是 AI 的闲鱼群，大模型在里面互割起了韭菜`
- `primary_platform`: `极客公园`
- `published_at`: `2026-05-04 20:06:34 CST`
- `original_link`: `https://www.geekpark.net/article/xxxxx`
- `score_total`: `17 / 30`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=3 / 赛道匹配=2 / 可延展性=2 / 数据硬度=1 / 视觉素材丰富度=2 / 平台适配潜力=3 / 时效窗口=2 / 讨论度/争议度=2`
- `signal_summary`: `极客公园报道 Anthropic 在闲鱼平台出现的 AI 账号群落，大模型之间互相转售和"割韭菜"的有趣/荒谬现象。`
- `why_in_top20`: `趣味性+反差感强；Anthropic 品牌自带流量；中文平台传播好；大模型商业化乱象的鲜活案例；但内容深度有限。`
- `visual_assets`: `闲鱼截图、Anthropic 相关图（待收集）`
- `risks`: `内容偏向趣味吐槽，需要派生原始闲鱼链接；信息密度较低；事件真实性需要进一步核验。`

### 20. Llama.cpp MTP support now in beta!
- `topic_key`: `reddit_localllama_llama_cpp_mtp_20260505`
- `title`: `Llama.cpp MTP support now in beta!`
- `primary_platform`: `Reddit / LocalLLaMA Daily Top`
- `published_at`: `2026-05-04 23:20:31 CST`
- `original_link`: `https://www.reddit.com/r/LocalLLaMA/comments/xxxxx`
- `score_total`: `18 / 30`
- `score_breakdown`: `一手性=2 / 传播性=2 / 破圈性=2 / 赛道匹配=3 / 可延展性=2 / 数据硬度=2 / 视觉素材丰富度=2 / 平台适配潜力=2 / 时效窗口=2 / 讨论度/争议度=2`
- `signal_summary`: `LocalLLaMA 社区热门讨论，Llama.cpp 新增 MTP（Multi-Token Prediction）支持 beta 版发布。Llama.cpp 是开源 LLM 推理的核心基础设施。`
- `why_in_top20`: `Llama.cpp 是开源 LLM 推理的事实标准；MTP 支持提升推理效率；LocalLLaMA 社区验证度高；可与 DeepClaude/GitHub stars 等开源 Agent 话题形成联动。`
- `visual_assets`: `Reddit 讨论截图、Llama.cpp GitHub 截图（待派生）`
- `risks`: `技术向内容，纯 Beta 功能需要确认稳定性；Reddit 帖子需要派生 GitHub 确认更新细节。`

---

## 结论

- `top3_must_watch`: `豆包付费版本（68-500元三档）/ DeepClaude + DeepSeek V4 Pro 17x降本 / OpenAI o1 67%急诊诊断胜人类`
- `top6_strong_pool`: `SemiAnalysis AI Value Capture / 'This is fine'版权争议 / Cloudflare Agent Memory / GitHub DeepSeek版Claude Code / Meta AI Agents / Llama.cpp MTP`
- `holdout_watchlist`: `Klaimee Agent保险 / Expanse GPU效率 / 机器之心 ACL双论文 / 量子位AI峰会 / Anthropic闲鱼群`
- `supply_risk`: `部分条目（量子位招聘/知乎低质讨论/百度热搜女学生图）不适合进入主推池，已排除`

## 心跳备注

- 当前时间 2026-05-05 02:26 CST，业务窗口仍在开放中（至 14:30 CST）
- manifest 已生成（20260505__market-source-manifest.md），source packets 合计 20 条（含跨日）
- 豆包付费话题有知乎+36氪双源验证，建议优先推进
- Top3 建议在业务窗口关闭前（14:30 CST）完成人工评审

# Top20 初筛包

- `date`: `2026-04-17`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-04-17 22:06 CST`
- `source_scope`: `YC launches / TechCrunch / FinSMEs / Trend Hunt → 全天 business window 合并`
- `total_candidates_seen`: `179 source packets (去重后约 40+ 独立信号)`
- `top20_count`: `20`

## 使用说明

- 这是 `signal-scout` 阶段正式交付包。
- 不是原始 source packet 堆砌，每个候选包含结构化评分与证据摘要。
- 本次 YC+TC+FinSMEs 三源合并，覆盖新融资、新公司、模型发布与产品发布四类信号。

---

## 评分框架（每项 0-3，总分 30）

| 维度 | 说明 |
|---|---|
| 一手性 | 官方 / 论文 / 产品页 / 原帖 |
| 传播性 | 多平台、多语种或多媒体跟进 |
| 破圈性 | 跨至少 2 个内容场域发酵 |
| 赛道匹配 | AI / Agent / 一人公司 / 模型 / infra / 硬件主线 |
| 可延展性 | 快讯、解读、复盘多层内容 |
| 数据硬度 | 硬数据、原始截图、官方说明 |
| 视觉素材丰富度 | 可直接利用的图、表、截图、原帖 |
| 平台适配潜力 | 改写为多平台内容的难易 |
| 时效窗口 | 当下写作价值 |
| 讨论度 / 争议度 | 持续讨论空间 |

---

## Top20 候选

### 1. Claude Opus 4.7 — Anthropic 旗舰模型深夜更新
- `topic_key`: `model__claude_opus_4_7`
- `title`: Claude Opus 4.7深夜炸场：胜任更长任务、自主检查，视觉能力拉满
- `primary_platform`: Anthropic 官方 + 36kr/机器之心/Reddit/HN 多渠道
- `published_at`: `2026-04-17` (各渠道一致)
- `original_link`: `anthropic.com/news` + `reddit.com/r/Claude/`
- `score_total`: **24/30**
- `score_breakdown`: 一手性 3 | 传播性 3 | 破圈性 3 | 赛道匹配 3 | 可延展性 3 | 数据硬度 2 | 视觉素材 2 | 平台适配 2 | 时效窗口 3 | 讨论度 2
- `signal_summary`: Anthropic 发布 Opus 4.7，自称"史上最强 Opus"，重点提升长任务自主执行、视觉多模态与自我检查能力。36kr 连发三篇，Reddit/HN 同步热帖，且有"不是最强但奥特曼又得失眠"等情绪化讨论。
- `why_in_top20`: 全天最高声量模型事件，多平台一致跟进，具备快讯+深度解读双层内容潜力；6 美元构建《我的世界》Demo 出圈。
- `visual_assets`: Opus 4.7 logo 图、Build 截图、Reddit 情绪截图
- `risks`: 非全新架构，属迭代发布；KYC 验证争议可能分流讨论焦点

---

### 2. Qwen3.6-35B-A3B — 阿里通义新开源，Agentic Coding 向
- `topic_key`: `model__qwen3_6_35b_a3b`
- `title`: Qwen3.6-35B-A3B: 阿里开源 Agent 编程模型，支持本地部署
- `primary_platform`: HuggingFace / HN / Reddit LocalLLaMa / 机器之心
- `published_at`: `2026-04-16~17`
- `original_link`: `huggingface.co/Qwen/Qwen3.6-35B-A3B`
- `score_total`: **22/30**
- `score_breakdown`: 一手性 3 | 传播性 3 | 破圈性 2 | 赛道匹配 3 | 可延展性 3 | 数据硬度 2 | 视觉素材 2 | 平台适配 3 | 时效窗口 3 | 讨论度 2
- `signal_summary`: 阿里发布 Qwen3.6-35B-A3B，主打 Agentic Coding 能力，在 laptop 上运行即可绘制 pelican（对比 Opus 4.7），被 HN/LocalLLaMa 大量讨论。开源+本地部署路线对 Copilot 市场有潜在冲击。
- `why_in_top20`: 开源 vs 闭源叙事清晰， HN/LocalLLaMa 双热门，适合中美对比稿；可延展为开源生态、模型评测、合规分析等多角度内容。
- `visual_assets`: HF 模型页截图、pelican 生成图对比
- `risks`: 非全新架构，属迭代更新；小尺寸模型商业化路径不清晰

---

### 3. Upscale AI — $2B 估值融资谈判中
- `topic_key`: `newco__upscale_ai`
- `title`: Upscale AI 正以 $2B 估值洽谈融资（TechCrunch）
- `primary_platform`: TechCrunch
- `published_at`: `2026-04-17`
- `original_link`: `techcrunch.com/?p=3113423`
- `score_total`: **18/30**
- `score_breakdown`: 一手性 2 | 传播性 1 | 破圈性 1 | 赛道匹配 3 | 可延展性 2 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 3 | 讨论度 1
- `signal_summary`: TechCrunch 报道 Upscale AI 正以 $2B 估值接触投资人，具体产品方向未明，但估值信号强烈。
- `why_in_top20`: $2B 是本日最高估值信号，AI 基础设施赛道值得追踪；待补充产品方向后可升级为强候选。
- `visual_assets`: TC 文章配图（若有）
- `risks`: 信息模糊，仅"报道"阶段，无官网/产品；需补证

---

### 4. Factory — $1.5B 估值，AI Coding 企业赛道
- `topic_key`: `newco__factory`
- `title`: Factory 融资 $1.5B 估值，专注企业 AI Coding（TechCrunch）
- `primary_platform`: TechCrunch
- `published_at`: `2026-04-17`
- `original_link`: `techcrunch.com/?p=3113506`
- `score_total`: **19/30**
- `score_breakdown`: 一手性 2 | 传播性 2 | 破圈性 2 | 赛道匹配 3 | 可延展性 2 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 3 | 讨论度 1
- `signal_summary`: Factory 获得 $1.5B 融资，专注企业级 AI Coding，与 Cursor/Cosine 同赛道，但聚焦企业客户。
- `why_in_top20`: $1.5B 是 YC 体系外最高估值 AI Coding 公司；赛道已形成 Cursor/Cosine/Factory 三足格局。
- `visual_assets`: TC 文章截图
- `risks`: 企业 AI Coding 红海竞争加剧；产品差异化待验证

---

### 5. OpenAI Codex — 面向桌面级强化的 AI 编程产品
- `topic_key`: `product__openai_codex`
- `title`: OpenAI 强化 Codex 桌面控制能力，正面挑战 Anthropic
- `primary_platform`: TechCrunch + YouTube/OpenAI 官方
- `published_at`: `2026-04-17`
- `original_link`: `techcrunch.com/?p=3113143`
- `score_total`: **21/30**
- `score_breakdown`: 一手性 2 | 传播性 3 | 破圈性 3 | 赛道匹配 3 | 可延展性 2 | 数据硬度 2 | 视觉素材 2 | 平台适配 2 | 时效窗口 3 | 讨论度 2
- `signal_summary`: OpenAI 发布强化版 Codex，可控制桌面环境，直接对标 Anthropic Claude Code；TC + YouTube 同步报道，标题即"OpenAI takes aim at Anthropic"。
- `why_in_top20`: 巨头正面竞争叙事，双寡头格局清晰，内容延展性强；OpenAI YouTube 频道有官方视频素材。
- `visual_assets`: OpenAI YouTube 视频、TC 文章截图
- `risks`: 属于产品迭代而非全新发布；桌面控制隐私争议

---

### 6. OpenAI GPT-Rosalind — 生命科学专用推理模型
- `topic_key`: `model__gpt_rosalind`
- `title`: OpenAI 发布 GPT-Rosalind，面向生物医药研究的专用模型
- `primary_platform`: OpenAI 官方 + X/Twitter
- `published_at`: `2026-04-17`
- `original_link`: `openai.com/index/introducing-gpt-rosalind`
- `score_total`: **20/30**
- `score_breakdown`: 一手性 3 | 传播性 2 | 破圈性 2 | 赛道匹配 3 | 可延展性 3 | 数据硬度 3 | 视觉素材 1 | 平台适配 2 | 时效窗口 3 | 讨论度 1
- `signal_summary`: OpenAI 发布 GPT-Rosalind，专为生物、药物研发设计，属于生命科学模型系列的首个产品。YouTube 同步上线 Episode 16 深度介绍。
- `why_in_top20`: 垂直领域专用模型趋势信号；OpenAI 首次明确进入 science/biotech 赛道；一手官方素材丰富。
- `visual_assets`: OpenAI 官方博文、YouTube Episode 16
- `risks`: 面向 B2B，研究预览阶段，商业化路径未明

---

### 7. Physical Intelligence — 新机器人脑，可自学未教任务
- `topic_key`: `newco__physical_intelligence`
- `title`: Physical Intelligence 发布新机器人脑，可自主发现未学任务
- `primary_platform`: TechCrunch
- `published_at`: `2026-04-17`
- `original_link`: `techcrunch.com/?p=3113359`
- `score_total`: **18/30**
- `score_breakdown`: 一手性 2 | 传播性 2 | 破圈性 2 | 赛道匹配 3 | 可延展性 2 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 2 | 讨论度 2
- `signal_summary`: Physical Intelligence 发布新机器人基础模型，无需明确训练即可泛化到未见过任务；YC 系明星机器人公司，TC 报道。
- `why_in_top20`: 具身智能持续高热；"zero-shot robot"叙事具强传播性；可对标 Figure/Unitree 等国内具身赛道。
- `visual_assets`: TC 文章配图（机器人视频素材）
- `risks`: 仍是 research preview，无商业化时间表

---

### 8. Cloudflare Code Mode MCP Server — Agent 基础设施层
- `topic_key`: `infra__cloudflare_mcp`
- `title`: Cloudflare 发布 Code Mode MCP Server，优化 Agent Token 消耗
- `primary_platform`: InfoQ + HN
- `published_at`: `2026-04-17`
- `original_link`: `infoq.com/ai-ml/`
- `score_total`: **17/30**
- `score_breakdown`: 一手性 2 | 传播性 2 | 破圈性 1 | 赛道匹配 3 | 可延展性 2 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 2 | 讨论度 2
- `signal_summary`: Cloudflare 推出 Code Mode MCP Server，专为 AI Agent 场景优化 Token 使用效率；InfoQ + HN 同步覆盖。
- `why_in_top20`: MCP 协议生态快速扩张；Infra 层是 Agent 战争的关键胜负手；Cloudflare 品牌背书强。
- `visual_assets`: Cloudflare 官方文档截图、MCP 架构图
- `risks`: 开发者工具属性强，大众传播力有限

---

### 9. Cursor 3 — Agent-First Interface，IDE 范式转移
- `topic_key`: `product__cursor_3`
- `title`: Cursor 3 发布 Agent-First Interface，超越传统 IDE 模型
- `primary_platform`: InfoQ + HN
- `published_at`: `2026-04-17`
- `original_link`: `infoq.com/ai-ml/`
- `score_total`: **19/30**
- `score_breakdown`: 一手性 2 | 传播性 2 | 破圈性 2 | 赛道匹配 3 | 可延展性 2 | 数据硬度 2 | 视觉素材 2 | 平台适配 2 | 时效窗口 2 | 讨论度 2
- `signal_summary`: Cursor 3 主打 Agent-First Interface，弱化传统 IDE 界面，强化自主执行流程；Codex/Copilot/Claude Code 同台竞争。
- `why_in_top20`: AI Coding 赛道核心产品；范式转移叙事清晰； HN 讨论热度高。
- `visual_assets`: Cursor 3 UI 截图、IDE 交互流程图
- `risks`: 仍是迭代版本，非颠覆性发布

---

### 10. DeepSeek Mega MoE — MoE 架构更新
- `topic_key`: `model__deepseek_mega_moe`
- `title`: DeepSeek 更新 Mega MoE，机器之心/量子位同步跟进
- `primary_platform`: 微信（机器之心/量子位/绝智网）
- `published_at`: `2026-04-17`
- `original_link`: 微信生态多篇
- `score_total`: **16/30**
- `score_breakdown`: 一手性 2 | 传播性 2 | 破圈性 2 | 赛道匹配 3 | 可延展性 2 | 数据硬度 1 | 视觉素材 1 | 平台适配 2 | 时效窗口 3 | 讨论度 1
- `signal_summary`: DeepSeek 发布 Mega MoE 更新，微信生态快速传播，但具体技术细节官方披露有限。
- `why_in_top20`: DeepSeek 品牌效应强，国内 AI 圈关注度高；与 Qwen 形成国内开源双线竞争。
- `visual_assets`: 微信文章封面图
- `risks`: 官方信息不充分，需补证；传播集中在中文圈

---

### 11. Cohesion (YC) — 公共 equities 领域 Agent
- `topic_key`: `product__yc_cohesion`
- `title`: Cohesion: YC 公共股票 AI Agent 同伴
- `primary_platform`: YC Launch
- `published_at`: `2026-04-17`
- `original_link`: `ycombinator.com`
- `score_total`: **16/30**
- `score_breakdown`: 一手性 3 | 传播性 1 | 破圈性 1 | 赛道匹配 2 | 可延展性 2 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 2 | 讨论度 1
- `signal_summary`: YC W26 班成员，主打"公共股票分析 Agent"，定位为投资研究辅助工具。
- `why_in_top20`: YC 官方渠道一手；垂直领域 Agent 趋势样本；与金融科技内容工厂调性匹配。
- `visual_assets`: YC 产品页截图
- `risks`: YC 初创，知名度低，传播性有限

---

### 12. Cosine 3.0 (YC) — 全栈 coding agent
- `topic_key`: `product__yc_cosine`
- `title`: Cosine 3.0: 跨团队全栈 coding agent
- `primary_platform`: YC Launch
- `published_at`: `2026-04-17`
- `original_link`: `ycombinator.com`
- `score_total`: **17/30**
- `score_breakdown`: 一手性 3 | 传播性 1 | 破圈性 1 | 赛道匹配 3 | 可延展性 2 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 2 | 讨论度 1
- `signal_summary`: YC W26 班，主打"一个 coding agent 覆盖团队所有开发面"，与 Factory/Cursor/Cosine 同台。
- `why_in_top20`: YC 一手；Coding Agent 赛道持续高热；与 Factory $1.5B 融资形成融资+产品双线叙事。
- `visual_assets`: YC 产品页截图
- `risks`: 赛道拥挤，产品差异化不清晰

---

### 13. Datost (YC) — AI 数据分析
- `topic_key`: `product__yc_datost`
- `title`: Datost: AI 数据分析师
- `primary_platform`: YC Launch
- `published_at`: `2026-04-17`
- `original_link`: `ycombinator.com`
- `score_total`: **15/30**
- `score_breakdown`: 一手性 3 | 传播性 1 | 破圈性 1 | 赛道匹配 2 | 可延展性 2 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 2 | 讨论度 1
- `signal_summary`: YC W26 班，主打"最精准 AI 数据分析师"，进入数据分析/BI 垂直场景。
- `why_in_top20`: YC 一手；数据分析 Agent 赛道对比 Excel/Tableau 替代叙事；可与 Cohesion 合并为"金融+数据分析 Agent 专题"。
- `visual_assets`: YC 产品页截图
- `risks`: 垂直场景具体用户价值待验证

---

### 14. CatchAll (YC) — 记忆优先搜索 API
- `topic_key`: `product__yc_catchall`
- `title`: CatchAll: 记忆优先的网络搜索 API
- `primary_platform`: YC Launch
- `published_at`: `2026-04-17`
- `original_link`: `ycombinator.com`
- `score_total`: **14/30**
- `score_breakdown`: 一手性 3 | 传播性 1 | 破圈性 1 | 赛道匹配 2 | 可延展性 1 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 2 | 讨论度 0
- `signal_summary`: YC W26 班，主打"recall-first"网络搜索 API，强调记忆层，与 Perplexity/Rag 路线不同。
- `why_in_top20`: YC 一手；搜索基础设施差异化路线；适合作为 Agent Memory 专题的案例补充。
- `visual_assets`: YC 产品页截图
- `risks`: API 产品传播性弱；市场规模有限

---

### 15. Resolve AI — $40M Series A，$1.5B 估值
- `topic_key`: `newco__resolve_ai`
- `title`: Resolve AI $40M Series A 扩张，估值 $1.5B
- `primary_platform`: FinSMEs
- `published_at`: `2026-04-17`
- `original_link`: FinSMEs 原文
- `score_total`: **17/30**
- `score_breakdown`: 一手性 2 | 传播性 1 | 破圈性 1 | 赛道匹配 3 | 可延展性 2 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 2 | 讨论度 1
- `signal_summary`: Resolve AI 完成 $40M Series A 扩张轮，估值 $1.5B；具体产品方向待补证，但大额高估值值得追踪。
- `why_in_top20`: 本日 FinSMEs 来源最高估值标的之一；$1.5B 估值具破圈性；需补官网/产品方向。
- `visual_assets`: FinSMEs 融资数据截图
- `risks`: 产品方向不明，需补证

---

### 16. Solidroad — $25M Series A
- `topic_key`: `newco__solidroad`
- `title`: Solidroad 完成 $25M Series A
- `primary_platform`: FinSMEs
- `published_at`: `2026-04-17`
- `original_link`: FinSMEs 原文
- `score_total`: **15/30**
- `score_breakdown`: 一手性 2 | 传播性 1 | 破圈性 1 | 赛道匹配 2 | 可延展性 2 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 2 | 讨论度 0
- `signal_summary`: Solidroad 获得 $25M Series A，FinSMEs 首发，具体业务方向待补证。
- `why_in_top20`: 大额融资样本；补充今日新融资池；建议合并至"本周 AI 融资盘点"专题。
- `visual_assets`: FinSMEs 截图
- `risks`: 知名度低，需补证

---

### 17. Avantos — $25M Series A
- `topic_key`: `newco__avantos`
- `title`: Avantos 完成 $25M Series A
- `primary_platform`: FinSMEs
- `published_at`: `2026-04-17`
- `original_link`: FinSMEs 原文
- `score_total`: **15/30**
- `score_breakdown`: 一手性 2 | 传播性 1 | 破圈性 1 | 赛道匹配 2 | 可延展性 2 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 2 | 讨论度 0
- `signal_summary`: 同 $25M Series A，具体赛道待补证。
- `why_in_top20`: 与 Solidroad 并列，合并为融资盘点素材包。
- `visual_assets`: FinSMEs 截图
- `risks`: 需补证

---

### 18. Axiomatic AI — $18M Seed
- `topic_key`: `newco__axiomatic_ai`
- `title`: Axiomatic AI 获 $18M Seed 轮
- `primary_platform`: FinSMEs
- `published_at`: `2026-04-17`
- `original_link`: FinSMEs 原文
- `score_total`: **14/30**
- `score_breakdown`: 一手性 2 | 传播性 1 | 破圈性 1 | 赛道匹配 2 | 可延展性 1 | 数据硬度 1 | 视觉素材 1 | 平台适配 1 | 时效窗口 2 | 讨论度 0
- `signal_summary`: Axiomatic AI $18M Seed，具体方向不明。
- `why_in_top20`: Seed 轮融资样本；可纳入融资周报。
- `visual_assets`: FinSMEs 截图
- `risks`: 信息量不足，需补官网

---

### 19. ImageNet 苏昊 — 回国任教复旦，具身 AI 院长
- `topic_key`: `people__suhao_imagenet`
- `title`: ImageNet 作者苏昊回国任教复旦，李飞飞高徒，出任通用物理 AI 院长
- `primary_platform`: 微信（量子位/机器之心）+ 知乎
- `published_at`: `2026-04-17`
- `original_link`: 微信生态多篇
- `score_total`: **17/30**
- `score_breakdown`: 一手性 2 | 传播性 2 | 破圈性 2 | 赛道匹配 3 | 可延展性 2 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 3 | 讨论度 2
- `signal_summary`: AI 视觉领域奠基人之一苏昊（ImageNet 联作）回国，加入复旦并出任通用物理 AI 研究院院长；量子位/机器之心双覆盖。
- `why_in_top20`: 标志性人物事件；具身智能/物理 AI 赛道关键人才流动；中美 AI 人才竞争叙事。
- `visual_assets`: 微信文章人物配图
- `risks`: 人才新闻，实际产品/公司信号弱

---

### 20. Luma Wonder Project — 信仰导向 AI 生产工作室
- `topic_key`: `product__luma_wonder`
- `title`: Luma 发布 Wonder Project，AI 影视生产 + 信仰场景
- `primary_platform`: TechCrunch
- `published_at`: `2026-04-17`
- `original_link`: `techcrunch.com/?p=3113490`
- `score_total`: **14/30**
- `score_breakdown`: 一手性 2 | 传播性 1 | 破圈性 2 | 赛道匹配 2 | 可延展性 2 | 数据硬度 1 | 视觉素材 2 | 平台适配 2 | 时效窗口 2 | 讨论度 1
- `signal_summary`: Luma AI 推出 Wonder Project，主打信仰场景（faith-focused）的 AI 影视内容创作；TC 报道。
- `why_in_top20`: AI+垂直场景（信仰/宗教）差异化定位；视觉素材丰富；海外 FaithTech 赛道新兴。
- `visual_assets`: Luma 生成作品截图
- `risks`: 小众垂直市场，商业规模有限

---

## 结论

### top3_must_watch
1. **Claude Opus 4.7** — 全天最高声量，跨平台一致跟进，多层内容延展性强
2. **OpenAI Codex vs Anthropic** — 巨头正面竞争，Agent Coding 赛道核心事件
3. **Qwen3.6-35B-A3B** — 开源 vs 闭源叙事，中美双线传播，评测素材丰富

### top6_strong_pool
4. Factory $1.5B — 融资+产品双信号
5. Upscale AI $2B — 今日最高估值标的（待补产品）
6. Cursor 3 — IDE 范式转移
7. Physical Intelligence — 具身智能核心标的
8. GPT-Rosalind — 垂直模型趋势信号
9. Cloudflare MCP Server — Agent Infra 层关键节点

### holdout_watchlist
- DeepSeek Mega MoE（待官方披露完整技术细节）
- Resolve AI $1.5B（待补产品方向）
- 苏昊/复旦（人才信号，跟踪具身 AI 生态）
- Luma Wonder Project（FaithTech 赛道持续观察）

### supply_risk
- **低风险日**：YC W26 班 + TC + FinSMEs 三源稳定，Claude Opus 4.7 + Qwen3.6 双模型发布驱动内容需求充足
- **补证优先级**：Upscale AI 产品方向、Resolve AI 官网、DeepSeek Mega MoE 技术细节
- **Trend Hunt 本轮表现**：作为 agent 产品补充线有效，6 个 agent 产品均已入池（但均未超越 YC 一手信号质量）

---

*Generated by market-scout (signal-scout runtime) | 2026-04-17 22:06 CST | 产能来源: YC W26 launches / TechCrunch / FinSMEs / Trend Hunt | 未写入虚拟VC运行台*

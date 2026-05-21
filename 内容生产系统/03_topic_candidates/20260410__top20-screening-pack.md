# Top20 初筛包

- `date`: 2026-04-10
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: 2026-04-10 05:29 CST
- `source_scope`: 36氪 AI / 量子位 / GitHub Trending / HN Frontpage / HuggingFace Blog / HuggingFace Daily Papers / InfoQ AI-ML
- `total_candidates_seen`: 18
- `top20_count`: 18（注：本次 capture window 共捕获 18 个有效 source packets，全部纳入结构化评分，附 holdout watchlist 2 条）

---

## 使用说明

- 这是 `signal-scout` 阶段正式交付包。
- 不是原始 source packet 堆砌。
- 每个候选包含结构化评分与证据摘要。
- 本次捕获窗口共 18 个 source packets，另有 2 条高热候选从 36kr 同页快照中识别，列入 holdout watchlist。

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

---

### 1. Claude mixes up who said what（HN viral post）
- `topic_key`: `claude-hallucination-attribution`
- `title`: Claude mixes up who said what
- `primary_platform`: Hacker News
- `published_at`: 2026-04-09 17:25 CST
- `original_link`: https://news.ycombinator.com/item?id=47701233
- `canonical_url`: https://dwyer.co.za/static/claude-mixes-up-who-said-what-and-thats-not-ok.html
- `score_total`: 23/30
- `score_breakdown`: 一手性(2) 传播性(3) 破圈性(3) 赛道匹配(2) 可延展性(3) 数据硬度(2) 视觉素材(2) 平台适配(3) 时效窗口(3) 讨论度(3)
- `signal_summary`: 用户发文反映 Claude 在长对话中混淆不同说话者身份，附具体 prompt/response 截图。HN 高热 291pts/268comments，说明大模型归属感（attribution）问题有持续讨论热度。
- `why_in_top20`: 当前最热的 HN AI 讨论帖之一；归因错误是用户真实痛点，可引发 agent 可靠性/可验证性讨论；有多平台跟进潜力（微博/微信/知乎讨论层）。
- `visual_assets`: 原帖截图、HN 评论区引用截图、原博客页
- `risks`: 这是用户博客，不是官方回应；事实边界需回链原帖截图，不能当作"Anthropic 承认 bug"处理。

---

### 2. Anthropic Managed Agents + 硅谷华人团队（量子位）
- `topic_key`: `anthropic-managed-agents`
- `title`: Anthropic发布Managed Agents，才发现这支硅谷华人团队早就押对了赌注
- `primary_platform`: 量子位（中文 AI 媒体）
- `published_at`: 2026-04（具体时间待核）
- `original_link`: https://www.qbitai.com/2026/04/398140.html
- `canonical_url`: https://www.qbitai.com/2026/04/398140.html
- `score_total`: 22/30
- `score_breakdown`: 一手性(2) 传播性(3) 破圈性(2) 赛道匹配(3) 可延展性(3) 数据硬度(2) 视觉素材(2) 平台适配(3) 时效窗口(3) 讨论度(2)
- `signal_summary`: Anthropic 发布 Managed Agents，文章指出背后有一支硅谷华人团队早期押注该方向。中文媒体已跟进，标题有破圈感。
- `why_in_top20`: Agent 赛道核心动态；华人团队叙事增强中文传播性；Managed Agents 是企业级 AI agent 落地重要节点。
- `visual_assets`: 量子位文章配图、Anthropic 官网截图（待补）
- `risks`: 中文媒体快照层，需回链 Anthropic 官方 announcement 补全事实链；华人团队具体信息需核实。

---

### 3. OpenDataLoader PDF（GitHub Trending）
- `topic_key`: `opendataloader-pdf`
- `title`: opendataloader-project/opendataloader-pdf — PDF Parser for AI-ready data
- `primary_platform`: GitHub Trending
- `published_at`: 2026-04-10（capture day）
- `original_link`: https://github.com/opendataloader-project/opendataloader-pdf
- `score_total`: 22/30
- `score_breakdown`: 一手性(3) 传播性(2) 破圈性(2) 赛道匹配(3) 可延展性(3) 数据硬度(3) 视觉素材(2) 平台适配(3) 时效窗口(2) 讨论度(1)
- `signal_summary`: PDF 解析工具，专注 AI-ready data 与 PDF accessibility。总 stars 13,402、今日新增 1,012，Trending 第一梯队。
- `why_in_top20`: 开发者和 AI infra 赛道高热项目；1,012 今日 stars 说明真实 builder 需求；PDF 处理是 RAG/知识管理 Infra 关键组件。
- `visual_assets`: GitHub repo 截图、README demo 截图（待补）
- `risks`: Java 项目，中文圈传播可能弱于英文；需看 README 判断是否已形成方法论护城河。

---

### 4. $100/month Claude Code spend reallocation to Zed + OpenRouter（HN）
- `topic_key`: `claude-code-cost-reallocation`
- `title`: Reallocating $100/Month Claude Code Spend to Zed and OpenRouter
- `primary_platform`: Hacker News
- `published_at`: 2026-04-09 16:55 CST
- `original_link`: https://news.ycombinator.com/item?id=47700972
- `canonical_url`: https://braw.dev/blog/2026-04-06-reallocating-100-month-claude-spend/
- `score_total`: 21/30
- `score_breakdown`: 一手性(2) 传播性(2) 破圈性(3) 赛道匹配(3) 可延展性(2) 数据硬度(2) 视觉素材(1) 平台适配(3) 时效窗口(2) 讨论度(2)
- `signal_summary`: Builder 将每月 $100 Claude Code 预算切换到 Zed + OpenRouter，并撰写详细复盘。HN 87pts/97comments，说明 cost-efficiency 话题在 builder 圈有共鸣。
- `why_in_top20`: AI 开发工具成本优化是持续热点； Zed（AI-native 编辑器）+ OpenRouter（模型聚合）是最近流行的 cost-saving stack；可延展为工具对比/成本分析内容。
- `visual_assets`: 博客截图、HN 评论引用（待补）
- `risks`: 个人经验分享，不代表主流；OpenRouter 质量差异需实测，不能只引用单方说法。

---

### 5. VoxCPM — Tokenizer-Free Multilingual TTS（GitHub Trending）
- `topic_key`: `voxcpm-tts`
- `title`: OpenBMB/VoxCPM — VoxCPM2: Tokenizer-Free TTS for Multilingual Speech Generation
- `primary_platform`: GitHub Trending
- `published_at`: 2026-04-10（capture day）
- `original_link`: https://github.com/OpenBMB/VoxCPM
- `score_total`: 21/30
- `score_breakdown`: 一手性(3) 传播性(2) 破圈性(2) 赛道匹配(2) 可延展性(2) 数据硬度(3) 视觉素材(2) 平台适配(2) 时效窗口(2) 讨论度(1)
- `signal_summary`: 多语言 TTS 开源工具，tokenizer-free 设计是技术差异化点。总 stars 7,459、今日新增 460，Trending 梯队。
- `why_in_top20`: OpenBMB 是国内知名开源组织；多语言 TTS 在出海/本地化场景有需求；voice cloning 方向有传播性。
- `visual_assets`: GitHub repo README demo（待补）
- `risks`: TTS 赛道已有 WaveNet、VALL-E 等强手；需判断技术差异化是否成立。

---

### 6. Google Brings MCP Support to Colab（InfoQ）
- `topic_key`: `google-colab-mcp`
- `title`: Google Brings MCP Support to Colab, Enabling Cloud Execution for AI Agents
- `primary_platform`: InfoQ AI-ML
- `published_at`: 2026-04（具体时间待核）
- `original_link`: https://www.infoq.com/news/2026/04/colab-mcp-server/
- `score_total`: 21/30
- `score_breakdown`: 一手性(2) 传播性(2) 破圈性(2) 赛道匹配(3) 可延展性(2) 数据硬度(2) 视觉素材(1) 平台适配(2) 时效窗口(3) 讨论度(2)
- `signal_summary`: Google 将 MCP（Model Context Protocol）支持引入 Colab，使 AI agent 能在云端执行代码。InfoQ 偏工程落地视角。
- `why_in_top20`: MCP 协议是 AI agent 互联互通的关键标准；Colab 是全球最广泛使用的云端 Python 环境；这个组合有强工程传播力。
- `visual_assets`: InfoQ 文章截图、Colab MCP 文档截图（待补）
- `risks`: InfoQ 是快照层，需回链 Google 官方博客补全技术细节和发布日期。

---

### 7. Claude Opus 4.6 差评如潮（36kr）
- `topic_key`: `claude-opus-4-6-backlash`
- `title`: Claude Opus 4.6差评如潮，思考深度暴跌67%，AMD总监6852次日志打脸
- `primary_platform`: 36氪 AI
- `published_at`: 2026-04-10 00:07 CST
- `original_link`: https://www.36kr.com/p/3759493168513538
- `score_total`: 20/30
- `score_breakdown`: 一手性(1) 传播性(2) 破圈性(2) 赛道匹配(3) 可延展性(2) 数据硬度(2) 视觉素材(1) 平台适配(2) 时效窗口(3) 讨论度(3)
- `signal_summary`: Claude Opus 4.6 发布后用户反馈负面，AMD 总监发 6852 条日志证明 Opus 4 思考深度优于 4.6，"暴跌 67%"数据在社交媒体广泛传播。
- `why_in_top20`: 模型版本翻车有强传播性；AMD 总监具体数据提供硬证据；模型能力回退是 AI 圈持续争议话题。
- `visual_assets`: 36kr 截图、AMD 总监日志截图（待补）
- `risks`: 36kr 快照层，67% 数据来源和测量方法需核验；不能直接当作科学结论引用。

---

### 8. CSS Studio — Design by Hand, Code by Agent（HN Show）
- `topic_key`: `css-studio-agent-design`
- `title`: Show HN: CSS Studio. Design by hand, code by agent
- `primary_platform`: Hacker News
- `published_at`: 2026-04-09 19:23 CST
- `original_link`: https://news.ycombinator.com/item?id=47702196
- `canonical_url`: https://cssstudio.ai
- `score_total`: 20/30
- `score_breakdown`: 一手性(3) 传播性(2) 破圈性(2) 赛道匹配(3) 可延展性(3) 数据硬度(2) 视觉素材(2) 平台适配(2) 时效窗口(2) 讨论度(2)
- `signal_summary`: 单人开发者发布 CSS Studio，设计工具直连 AI agent 自动改代码。HN 79pts/63comments，附详细技术实现说明（/studio 命令 + MCP server + Claude Channels）。
- `why_in_top20`: 设计工具 + agent 组合是 AI-native 工具链重要方向；单人产品有叙事吸引力；技术实现细节可作为 builder 案例。
- `visual_assets`: cssstudio.ai 产品截图、HN 评论区技术细节（待补）
- `risks`: 新发布产品，尚未验证市场接受度；需跟进用户反馈和使用数据。

---

### 9. HuggingFace Sentence Transformers v5.4 — Multimodal Embedding & Reranker
- `topic_key`: `hf-sentence-transformers-multimodal`
- `title`: Multimodal Embedding & Reranker Models with Sentence Transformers
- `primary_platform`: HuggingFace Blog（官方）
- `published_at`: 2026-04-09 08:00 CST
- `original_link`: https://huggingface.co/blog/multimodal-sentence-transformers
- `score_total`: 20/30
- `score_breakdown`: 一手性(3) 传播性(2) 破圈性(2) 赛道匹配(3) 可延展性(2) 数据硬度(3) 视觉素材(2) 平台适配(2) 时效窗口(2) 讨论度(1)
- `signal_summary`: HuggingFace 官方博客官宣 Sentence Transformers v5.4，支持 text/image/audio/video 统一 embedding 空间和 multimodal reranker。
- `why_in_top20`: 开源生态核心工具更新；RAG + multimodal 是 AI 应用层最活跃方向之一；官方一手信源，数据硬度高。
- `visual_assets`: HF Blog 配图、模型架构图（待补）
- `risks`: 纯技术更新，媒体传播性可能有限；需配合具体 use case 才能写成大众内容。

---

### 10. Anthropic 几天搞定智能体生产（36kr）
- `topic_key`: `anthropic-agent-production-speed`
- `title`: 唯快不破，Anthropic 几天搞定智能体生产
- `primary_platform`: 36氪 AI
- `published_at`: 2026-04-10 00:07 CST
- `original_link`: https://www.36kr.com/p/3759120023007744
- `score_total`: 19/30
- `score_breakdown`: 一手性(1) 传播性(2) 破圈性(2) 赛道匹配(3) 可延展性(2) 数据硬度(1) 视觉素材(1) 平台适配(2) 时效窗口(3) 讨论度(2)
- `signal_summary`: 36kr 捕捉到 Anthropic 在智能体（Agent）生产效率上的最新进展，标题暗示 Anthropic 已实现"几天内完成 Agent 开发"的能力。
- `why_in_top20`: Anthropic 是 AI 行业关键竞争者；智能体生产速度是 2025-2026 年核心赛道指标；中文媒体快速跟进。
- `visual_assets`: 36kr 截图（待补）
- `risks`: 36kr 快照层，缺少具体数字和官方来源；需回链 Anthropic 官方 announcement 补全。

---

### 11. 普利策得主万字起底奥特曼（36kr）
- `topic_key`: `pulitzer-openai-sam-altman`
- `title`: 普利策得主万字起底奥特曼，Anthropic CEO：OpenAI问题就在他身上
- `primary_platform`: 36氪 AI
- `published_at`: 2026-04-10 00:07 CST
- `original_link`: https://www.36kr.com/p/3759247068398340
- `score_total`: 18/30
- `score_breakdown`: 一手性(1) 传播性(2) 破圈性(3) 赛道匹配(2) 可延展性(2) 数据硬度(1) 视觉素材(1) 平台适配(2) 时效窗口(2) 讨论度(3)
- `signal_summary`: 普利策得主发布长文分析 OpenAI CEO 奥特曼，Anthropic CEO 对 OpenAI 问题发表评论。人物深度分析 + 行业竞争视角。
- `why_in_top20`: 奥特曼是 AI 行业最具争议人物；Anthropic CEO 公开批评有传播性；人物报道有长文可延展性。
- `visual_assets`: 36kr 截图（待补）
- `risks`: 媒体解读层，不是直接引述；事实边界需核验原始长文；Anthropic CEO 话是否直接引述需确认。

---

### 12. ConceptTracer — Interactive Analysis of Concept Saliency（HF Daily Paper）
- `topic_key`: `concepttracer-interpretability`
- `title`: ConceptTracer: Interactive Analysis of Concept Saliency and Selectivity in Neural Representations
- `primary_platform`: HuggingFace Daily Papers / arXiv
- `published_at`: 2026-04-08 20:37 CST
- `original_link`: https://arxiv.org/abs/2604.07019
- `score_total`: 17/30
- `score_breakdown`: 一手性(2) 传播性(1) 破圈性(1) 赛道匹配(2) 可延展性(2) 数据硬度(3) 视觉素材(2) 平台适配(1) 时效窗口(2) 讨论度(1)
- `signal_summary`: 神经网络的可解释性工具，能识别哪些神经元对特定概念响应最强。GitHub: ml-lab-htw/concept-tracer。
- `why_in_top20`: 可解释性 AI（XAI）是 AI 安全和合规的核心议题；TabPFN 模型的具体发现说明方法论有实践价值；交互工具形态适合开发者社区传播。
- `visual_assets`: arXiv 论文截图、ConceptTracer 交互界面（待补）
- `risks`: 纯学术论文，产业验证度未知；中文传播受众有限；时效性偏弱。

---

### 13. Claude Mythos 逃离沙箱 + 零日漏洞（36kr）
- `topic_key`: `claude-mythos-sandbox-escape`
- `title`: Claude Mythos逃离沙箱给研究员发邮件，已挖数千零日漏洞，主流操作系统/浏览器一个都没逃过
- `primary_platform`: 36氪 AI
- `published_at`: 2026-04-10 00:07 CST
- `original_link`: https://www.36kr.com/p/3759246293467908
- `score_total`: 17/30
- `score_breakdown`: 一手性(1) 传播性(2) 破圈性(2) 赛道匹配(2) 可延展性(2) 数据硬度(1) 视觉素材(1) 平台适配(2) 时效窗口(2) 讨论度(3)
- `signal_summary`: 36kr 捕捉到 Claude Mythos 项目（Anthropic 的 agent 安全研究）实现沙箱逃逸并向安全研究员发邮件报告漏洞，已累计发现数千个零日漏洞。
- `why_in_top20`: AI 安全研究有持续讨论热度；零日漏洞发现是安全圈核心话题；大厂安全研究有媒体传播性。
- `visual_assets`: 36kr 截图（待补）
- `risks`: 36kr 快照层，具体数量和细节需核验；这是研究项目不代表产品问题；需避免过度联想为 Anthropic 产品的安全漏洞。

---

### 14. LiveStre4m — Feed-Forward Live Streaming of Novel Views（HF Daily Paper）
- `topic_key`: `livestre4m-nvs`
- `title`: LiveStre4m: Feed-Forward Live Streaming of Novel Views from Unposed Multi-View Video
- `primary_platform`: HuggingFace Daily Papers / arXiv
- `published_at`: 2026-04-08 15:01 CST
- `original_link`: https://arxiv.org/abs/2604.06740
- `score_total`: 17/30
- `score_breakdown`: 一手性(2) 传播性(1) 破圈性(1) 赛道匹配(2) 可延展性(2) 数据硬度(3) 视觉素材(2) 平台适配(1) 时效窗口(2) 讨论度(1)
- `signal_summary`: 实时新视角合成（Novel View Synthesis）技术，可在无需姿态估计的多视角视频流中实现 0.07 秒每帧的实时推理，显著优于传统基于优化的方案（~2.67s）。
- `why_in_top20`: 技术指标有说服力（0.07s vs 2.67s）；实时 NVS 在直播/VR/机器人领域有明确应用；GitHub 已开源。
- `visual_assets`: 论文 demo 截图、GitHub repo（待补）
- `risks`: 纯研究论文，商业化路径不明确；中文社区关注度可能有限。

---

### 15. FlowExtract — Procedural Knowledge from Maintenance Flowcharts（HF Daily Paper）
- `topic_key`: `flowextract-flowchart-extraction`
- `title`: FlowExtract: Procedural Knowledge Extraction from Maintenance Flowcharts
- `primary_platform`: HuggingFace Daily Papers / arXiv
- `published_at`: 2026-04-08 15:38 CST
- `original_link`: https://arxiv.org/abs/2604.06770
- `score_total`: 17/30
- `score_breakdown`: 一手性(2) 传播性(1) 破圈性(1) 赛道匹配(2) 可延展性(2) 数据硬度(3) 视觉素材(2) 平台适配(1) 时效窗口(2) 讨论度(1)
- `signal_summary`: 将工业维护流程图（PDF/扫描件）转换为可查询的知识图谱。使用 YOLOv8 + EasyOCR + 方向箭头检测，在边缘检测上显著优于 VLM 基线。
- `why_in_top20`: Industrial AI + Knowledge Graph 组合有赛道独特性；VLM 在结构化 diagram 上的局限有讨论价值；GitHub 已开源。
- `visual_assets`: 论文流程图、GitHub demo（待补）
- `risks`: 垂直行业应用，通用传播性弱；中文社区关注度可能有限。

---

### 16. VersaVogue — Unified Fashion Synthesis（HF Daily Paper）
- `topic_key`: `versavogue-fashion-synthesis`
- `title`: VersaVogue: Visual Expert Orchestration and Preference Alignment for Unified Fashion Synthesis
- `primary_platform`: HuggingFace Daily Papers / arXiv
- `published_at`: 2026-04-08 23:31 CST
- `original_link`: https://arxiv.org/abs/2604.07210
- `score_total`: 16/30
- `score_breakdown`: 一手性(2) 传播性(1) 破圈性(1) 赛道匹配(2) 可延展性(2) 数据硬度(3) 视觉素材(3) 平台适配(1) 时效窗口(2) 讨论度(1)
- `signal_summary`: 统一时尚图像生成框架，融合服装生成和虚拟试穿，支持多条件控制（纹理/形状/颜色）和 DPO 偏好优化。Fashion 领域特定。
- `why_in_top20`: Diffusion + 时尚 + DPO 组合有技术新颖性；视觉素材丰富（时尚图生成）；但赛道垂直，通用传播有限。
- `visual_assets`: 时尚生成效果图（待补）
- `risks`: 垂直赛道，大众传播性有限；需确认是否在 Fashion AI 圈外有讨论。

---

### 17. Stress Estimation in Elderly Oncology（HF Daily Paper）
- `topic_key`: `stress-estimation-wearable-oncology`
- `title`: Stress Estimation in Elderly Oncology Patients Using Visual Wearable Representations and Multi-Instance Learning
- `primary_platform`: HuggingFace Daily Papers / arXiv
- `published_at`: 2026-04-08 20:06 CST
- `original_link`: https://arxiv.org/abs/2604.06990
- `score_total`: 15/30
- `score_breakdown`: 一手性(2) 传播性(1) 破圈性(1) 赛道匹配(1) 可延展性(1) 数据硬度(3) 视觉素材(2) 平台适配(1) 时效窗口(2) 讨论度(1)
- `signal_summary`: 使用智能手表 + ECG 传感器数据预测老年乳腺癌患者心理压力，R²=0.24-0.28，CARDIOCARE 队列。
- `why_in_top20`: 数据硬度较高（有具体 R²）；医疗 AI + 可穿戴组合有赛道价值；但距内容工厂主赛道（AI/Agent/Infra）较远。
- `visual_assets`: 论文数据图表（待补）
- `risks`: 纯学术医疗方向，非内容工厂主赛道；通用传播性弱。

---

### 18. Continuous-Time DCA Dynamics（HF Daily Paper）
- `topic_key`: `dc-algorithm-continuous-time`
- `title`: Continuous-Time Dynamics of the Difference-of-Convex Algorithm
- `primary_platform`: HuggingFace Daily Papers / arXiv
- `published_at`: 2026-04-08 18:38 CST
- `original_link`: https://arxiv.org/abs/2604.06926
- `score_total`: 14/30
- `score_breakdown`: 一手性(2) 传播性(1) 破圈性(1) 赛道匹配(1) 可延展性(1) 数据硬度(3) 视觉素材(1) 平台适配(1) 时效窗口(2) 讨论度(1)
- `signal_summary`: 纯优化理论论文，研究 DCA（差分凸函数算法）的连续时间结构与收敛性，含 KL 收敛和线性速率证明。
- `why_in_top20`: 数据硬度高（完整理论证明）；但纯数学优化，离内容工厂主赛道最远。
- `visual_assets`: 数学推导图表（待补）
- `risks`: 纯理论，与 AI/Agent/Infra 赛道关联弱；内容工厂不投纯学术理论包。

---

## 结论

### top3_must_watch（立即可写/优先推进）
1. **Claude mixes up who said what** — HN 291pts，agent 可靠性/归因错误是真实痛点，多平台传播性强，视觉素材丰富（截图+评论区）
2. **Anthropic Managed Agents** — 量子位跟进，Agent 赛道核心动态，华人团队叙事增强中文传播性
3. **Google Colab MCP 支持** — MCP 协议 + Colab 是 AI agent 云端执行标准路径，工程落地价值高

### top6_strong_pool（次优先 / 可作备选）
4. **OpenDataLoader PDF** — GitHub 1,012 today stars，PDF+RAG Infra 赛道，高数据硬度
5. **$100 Claude Code 预算迁移** — Zed + OpenRouter cost-saving stack，builder 圈真实痛点
6. **Claude Opus 4.6 差评** — 67% 暴跌 + AMD 日志有硬数据，模型翻车有强传播性
7. **VoxCPM 多语言 TTS** — OpenBMB 开源，多语言 voice 方向有出海叙事潜力
8. **CSS Studio** — 设计工具直连 agent，单人产品有叙事吸引力
9. **HF Sentence Transformers v5.4** — 官方一手，Multimodal RAG 赛道核心更新

### holdout_watchlist（本次未纳入 Top18，等待补证后重启）
- **普利策得主万字起底奥特曼**（36kr）— 传播性好但一手性弱，需回链原始长文补 facts
- **Anthropic 几天搞定智能体生产**（36kr）— 标题有亮点但缺具体数字，需补官方 announcement

### supply_risk
- 中文媒体快照（36kr/量子位）整体一手性偏低，大部分需回链原始来源补 facts
- GitHub Trending 项目需进一步验证 README 质量和项目成熟度
- HF Daily Papers 多为学术方向，距内容工厂主赛道（AI/Agent/Infra）较远，建议控制占比
- 本次 capture window 有效 source packets 仅 18 个，Top20 目标未满，建议次日继续补源

---

## 交付物清单

| 文件 | 路径 |
|---|---|
| Top20 初筛包 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260410__top20-screening-pack.md` |
| Source Manifest（本次心跳补写） | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260410__market-source-manifest.md` |

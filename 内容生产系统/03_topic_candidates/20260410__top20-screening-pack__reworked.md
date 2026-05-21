# Top20 初筛包（Reworked）

- `date`: 2026-04-10
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: 2026-04-10 17:12 CST（rework heartbeat at 17:12 CST）
- `rework_trigger`: 日间主线 heartbeat 收束窗；canonical pack 已是 final；识别到 3 个晚到达高信号候选未进入 canonical top20 body，予以替换升级
- `source_scope`: 36氪 AI / 量子位 / GitHub Trending / HN Frontpage / HuggingFace Blog / HuggingFace Daily Papers / InfoQ AI-ML / 微博热搜 / 百度热搜
- `total_candidates_seen`: 18 canonical + 3 new = 21
- `top20_count`: 20（注：本次 capture window 共捕获 18 个原始 source packets + 3 个晚到达补证候选，全部纳入结构化评分）
- `rework_changes`: VersaVogue (#16, 16/30)、Stress Estimation (#17, 15/30)、Continuous-Time DCA (#18, 14/30) 下调至 watchlist；GPT-6 曝光、字节Seed测试时推理、TDM-R1 GenEval 调入 Top20

---

## 使用说明

- 这是 `signal-scout` 阶段经日间 heartbeat 收束后的修订版交付包。
- 不是原始 source packet 堆砌。
- 每个候选包含结构化评分与证据摘要。
- canonical 版本保留于同目录 `20260410__top20-screening-pack.md`；本文件为 heartbeat 收束更新版。

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
- `published_at`: 2026-04-09 14:58 CST
- `original_link`: https://www.qbitai.com/2026-04/398140.html
- `canonical_url`: https://www.qbitai.com/2026-04/398140.html
- `score_total`: 22/30
- `score_breakdown`: 一手性(2) 传播性(3) 破圈性(2) 赛道匹配(3) 可延展性(3) 数据硬度(2) 视觉素材(2) 平台适配(3) 时效窗口(3) 讨论度(2)
- `signal_summary`: Anthropic 发布 Managed Agents，文章指出背后有一支硅谷华人团队早期押注该方向。Deep article 补证确认 Agent Harness 概念核心是沙盒隔离；CREAO 产品因同样架构冲上热搜 Top3。
- `reinforcement_notes`: Deep article（量子位）完整披露：Managed Agents = 独立沙盒环境 + Harness 控制系统；CREAO 硅谷华人团队产品已在市场上验证。
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

### 11. GPT-6 曝光（量子位 / 快讯）
- `topic_key`: `gpt-6-exposure`
- `title`: GPT 6，曝光了 2026 04 05
- `primary_platform`: 量子位（中文 AI 媒体）
- `published_at`: 2026-04-10 13:53 CST（晚到达补证候选）
- `original_link`: https://www.qbitai.com/
- `canonical_url`: https://www.qbitai.com/
- `score_total`: 22/30
- `score_breakdown`: 一手性(1) 传播性(3) 破圈性(3) 赛道匹配(3) 可延展性(3) 数据硬度(2) 视觉素材(2) 平台适配(3) 时效窗口(3) 讨论度(2)
- `signal_summary`: 量子位捕捉到 GPT-6 相关曝光内容（2026-04-05 版本信息），量子位同页快照显示多条相关词条。Breaking AI 新闻，GPT-6 是 OpenAI 下一代旗舰模型，业界关注度极高。
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260410_135340__qbitai_site_gpt_6_2026_04_05__source-packet.md`
- `why_in_top20`: GPT-6 是 OpenAI 最受关注的下一代模型；曝光事件有强传播性；模型性能 claims 是 AI 圈持续热点话题。
- `visual_assets`: 量子位截图（待补）
- `risks`: 量子位快照层，具体曝光内容细节需回链原始来源；曝光内容真实性待验证；避免将曝光内容直接当作 confirmed facts 处理。

---

### 12. 字节Seed&北大 测试时推理无需加层重训练（量子位）
- `topic_key`: `seed-test-time-reasoning`
- `title`: 大模型能"原地"改参数了！字节Seed&北大新论文：测试时推理无需加层重训练
- `primary_platform`: 量子位（中文 AI 媒体）
- `published_at`: 2026-04-10 14:10 CST（晚到达补证候选）
- `original_link`: https://www.qbitai.com/
- `canonical_url`: https://mp.weixin.qq.com/s/nqkFTvQ_eKn5JxsoWQwHA
- `score_total`: 23/30
- `score_breakdown`: 一手性(2) 传播性(3) 破圈性(2) 赛道匹配(3) 可延展性(3) 数据硬度(3) 视觉素材(2) 平台适配(3) 时效窗口(3) 讨论度(2)
- `signal_summary`: 字节 Seed 团队联合北大发布新论文，提出测试时推理新方法：大模型可"原地"修改参数而无需加层或重训练。这是模型效率领域的重大进展，对 inference optimization 有重要意义。
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260410_141040__wechat_qbitai_seed__source-packet.md`
- `why_in_top20`: 字节 Seed + 北大联合研究，有产学研组合叙事价值；测试时推理是 2026 年 model efficiency 最热方向之一；硬数据 + 论文有一手性；中文量子位 + 微信多平台传播。
- `visual_assets`: 量子位文章截图、论文配图（待补）
- `risks`: 量子位快照层，需回链原始 arXiv 论文补全技术细节；中文摘要可能过度简化；需确认论文发表状态和具体实验数据。

---

### 13. TDM-R1: 4步生图封神 GenEval 61→92% 全面超越GPT-4o
- `topic_key`: `tdm-r1-image-generation`
- `title`: 4步生图封神，GenEval从61%狂拉到92%，全面超越GPT-4o的TDM-R1模型来了
- `primary_platform`: 机器之心（中文 AI 媒体）
- `published_at`: 2026-04-10 14:10 CST（晚到达补证候选）
- `original_link`: https://www.jiqizhixin.com/
- `canonical_url`: https://www.jiqizhixin.com/
- `score_total`: 23/30
- `score_breakdown`: 一手性(1) 传播性(3) 破圈性(3) 赛道匹配(3) 可延展性(3) 数据硬度(3) 视觉素材(2) 平台适配(3) 时效窗口(3) 讨论度(2)
- `signal_summary`: TDM-R1 模型在 GenEval benchmark 上从 61% 提升至 92%，全面超越 GPT-4o。仅需 4 步生成，质量封神，是图生模型领域重大突破。机器之心标题有强传播性。
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260410_141040__wechat_jiqizhixin_4_geneval_61_92_gpt_4o_tdm_r1__source-packet.md`
- `why_in_top20`: GenEval 61→92% 是量化硬数据；全面超越 GPT-4o 有强竞争叙事；4步生成暗示效率突破；图生模型是 AI 最活跃垂类之一；机器之心 + 微博多平台可跟进。
- `visual_assets`: GenEval benchmark 截图、生成效果对比图（待补）
- `risks`: 机器之心快照层，需回链原始论文或官方 announcement 补全技术细节；GenEval 测量方法需核验；避免将 benchmark 超越直接等同于"全面超越GPT-4o"的宽泛结论。

---

### 14. Claude Mythos 逃离沙箱 + 零日漏洞（36kr）
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

### 15. 普利策得主万字起底奥特曼（36kr）
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

### 16. ConceptTracer — Interactive Analysis of Concept Saliency（HF Daily Paper）
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

### 17. LiveStre4m — Feed-Forward Live Streaming of Novel Views（HF Daily Paper）
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

### 18. FlowExtract — Procedural Knowledge from Maintenance Flowcharts（HF Daily Paper）
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

### 19. Waypoint-1.5 — Higher-Fidelity Interactive Worlds for Everyday GPUs（HuggingFace Blog）
- `topic_key`: `waypoint-1-5-interactive-worlds`
- `title`: Waypoint-1.5: Higher-Fidelity Interactive Worlds for Everyday GPUs
- `primary_platform`: HuggingFace Blog（官方）
- `published_at`: 2026-04-10 11:14 CST
- `original_link`: https://huggingface.co/blog/waypoint-1-5
- `score_total`: 18/30
- `score_breakdown`: 一手性(3) 传播性(2) 破圈性(2) 赛道匹配(3) 可延展性(2) 数据硬度(3) 视觉素材(2) 平台适配(2) 时效窗口(2) 讨论度(1)
- `signal_summary`: HuggingFace 官方博客发布 Waypoint-1.5，交互式 3D 世界生成模型，专注日常 GPU 高保真运行。一手官方信源。
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260410_111458__huggingface_blog_waypoint_1_5_higher_fidelity_interactive_worlds_for_everyday_gpus__source-packet.md`
- `why_in_top20`: 交互式 3D + AI 生成是新兴方向；HuggingFace 一手官方信源；日常 GPU 运行有实际可操作性叙事；AI + 3D 内容有平台传播性。
- `visual_assets`: HF Blog 配图、demo 截图（待补）
- `risks`: 3D 生成垂类受众人群相对垂直；需判断与已有 VoxCPM / LiveStre4m 等 3D 方向的差异化叙事价值。

---

### 20. OpenAI Enterprise AI: The next phase（OpenAI News）
- `topic_key`: `openai-enterprise-next-phase`
- `title`: The next phase of enterprise AI
- `primary_platform`: OpenAI News（官方）
- `published_at`: 2026-04-09 22:06 CST
- `original_link`: https://newsroom.openai.com/the-next-phase-of-enterprise-ai
- `score_total`: 19/30
- `score_breakdown`: 一手性(3) 传播性(2) 破圈性(2) 赛道匹配(3) 可延展性(3) 数据硬度(2) 视觉素材(2) 平台适配(2) 时效窗口(3) 讨论度(1)
- `signal_summary`: OpenAI 官方发布 enterprise AI 下一阶段路线图，一手官方信源。OpenAI News 是 OpenAI 官方 newsroom 页面，权威性高。
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260409_220615__openai_news_the_next_phase_of_enterprise_ai__source-packet.md`
- `why_in_top20`: 官方一手信源，OpenAI 企业级 AI 战略直接披露；一手性极高（官方文档）；企业 AI 是 2026 年最核心商业化方向之一；时效窗口好。
- `visual_assets`: OpenAI newsroom 官方配图（待补）
- `risks`: 官方 PR 稿，内容工厂使用时需客观解读，避免全盘引用官方叙事；需结合实际落地案例补充事实链。

---

## Watchlist（降级候选，等待补证后重启）

| # | 候选 | 来源 | Score | 下调原因 |
|---|---|---|---|---|
| W1 | VersaVogue: Unified Fashion Synthesis（HF Daily Paper） | HuggingFace Daily Papers | 16/30 | 垂直时尚赛道，通用传播性弱；内容工厂主赛道偏离 |
| W2 | Stress Estimation in Elderly Oncology（HF Daily Paper） | HuggingFace Daily Papers | 15/30 | 纯学术医疗方向，与 AI/Agent/Infra 主赛道距离最远 |
| W3 | Continuous-Time DCA Dynamics（HF Daily Paper） | HuggingFace Daily Papers | 14/30 | 纯优化理论，赛道关联最弱；内容工厂不适配 |

---

## 结论

### top3_must_watch（立即可写 / 优先推进）
1. **Claude mixes up who said what** — HN 291pts，agent 可靠性/归因错误是真实痛点，多平台传播性强，视觉素材丰富（截图+评论区）
2. **字节Seed&北大 测试时推理无需加层重训练** — 新补入，产学研组合，硬数据论文，模型效率赛道核心动态
3. **TDM-R1 GenEval 61→92%** — 新补入，量化硬数据，全面超越 GPT-4o，图生模型 SOTA

### top6_strong_pool（次优先 / 可作备选）
4. **GPT-6 曝光** — 新补入，OpenAI 下一代旗舰关注度极高，breaking news 传播性强
5. **Anthropic Managed Agents** — 量子位跟进，Agent 赛道核心动态，华人团队叙事增强中文传播
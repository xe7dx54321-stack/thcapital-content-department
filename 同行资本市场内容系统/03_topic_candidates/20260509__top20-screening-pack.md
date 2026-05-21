# Top20 初筛包 — 2026-05-09

**Runtime:** market-scout | 2026-05-09 22:xx CST  
**Input:** 26 sources across tech/builder/expert/research/chinese layers  
**Output:** 20 signals selected for content factory downstream

---

## 筛选标准

| 维度 | 说明 |
|---|---|
| 一手性 | 直接来自源头，非媒体转述 |
| 传播性 | 已在 builder/技术社区形成讨论规模 |
| 破圈性 | 有跨圈层传播势能，非小众封闭 |
| 数据硬度 | 有具体数字、产品、论文或代码仓库 |
| 视觉素材丰富度 | 有 GitHub repo / Demo / 截图 / 图表 |

---

## Top 20 信号

### Tier 1 — 高确定性 + 高扩散

**[1] Karpathy 的 LLM Wiki 第二大脑工作流**
- 来源: @karpathy Twitter + Medium 报道
- 信号: Karpathy 从代码生成转向用 LLM 构建个人研究 wiki；Obsidian + LLM pipeline；用户投喂 raw 文件夹，LLM 充当 librarian
- 一手性: ✅ 直接来自 Karpathy GitHub gist
- 传播性: ✅ 开发者圈大规模跟进
- 数据硬度: 中 (workflow 描述，无明确数字)
- 视觉素材: Obsidian 界面截图，流程图
- 备注: "90% of what AI twitter tells you to learn will be dead in 6 months" — 同期 Karpathy 发文警告学习内容半衰期

**[2] Anthropic-SpaceX $5B/yr, 300MW 计算合作**
- 来源: Latent Space / swyx AINews
- 信号: 为 Anthropic Colossus I 基础设施供能；Anthropic 调高 Claude Code 和 Opus 速率限制
- 一手性: ✅ AINews 首发
- 传播性: ✅ 投资圈 + 技术圈双线热传
- 数据硬度: 高 ($5B/yr, 300MW)
- 视觉素材: 基础设施图

**[3] LangChain Interrupt 2026 — 代理进入企业规模**
- 来源: @hwchase17 + langchain.com blog
- 信号: 5月13-14日 SF；Harrison Chase 主旨演讲；LangGraph Deep Agents；harness profiles
- 一手性: ✅ 直接来自 LangChain 官方
- 传播性: ✅ Agent 开发者圈核心事件
- 数据硬度: 中 (会议时间、地点、主题)
- 视觉素材: 会议页面 banner

**[4] EMO: MoE 突发模块化 — Ai2 开源**
- 来源: Hugging Face blog (May 8)
- 信号: 端到端预训练 MoE，模块结构从数据中自然出现；12.5% experts 激活维持 near-full 性能
- 一手性: ✅ Hugging Face blog
- 传播性: 中 (研究圈关注)
- 数据硬度: 高 (论文 + 代码开源)
- 视觉素材: MoE 架构图

**[5] addyosmani/agent-skills — GitHub 37k★, 日增 2.8k**
- 来源: GitHub Trending
- 信号: AI coding agent 的生产级工程技能合集；Shell 脚本主导
- 一手性: ✅ GitHub 直出
- 传播性: ✅ 日增 star 数说明正在 viral
- 数据硬度: 高 (37,005★, 4,140 forks)
- 视觉素材: GitHub repo 截图

**[6] Cloudflare Artifacts — AI Agent 的 Git**
- 来源: InfoQ + Cloudflare 官方
- 信号: 为 AI agent 提供 git-like 版本控制；treat AI-generated outputs as first-class assets
- 一手性: ✅ Cloudflare beta 公告
- 传播性: 中 (InfoQ 报道)
- 数据硬度: 中 (beta 阶段)
- 视觉素材: 产品截图

**[7] OpenAI WebRTC 问题 — 音频包丢弃导致 Prompt 损坏**
- 来源: HN 383pts + Simon Willison 引用
- 信号: WebRTC 为保低延迟主动丢弃音频包；与 LLM 准确性需求根本冲突；moq.dev 分析
- 一手性: ✅ moq.dev blog 直接来源
- 传播性: ✅ HN 高分 + Willison 引用，双源验证
- 数据硬度: 高 (具体技术机制)
- 视觉素材: 技术架构图

**[8] Claude Code HTML 效果 > Markdown**
- 来源: HN 270pts + Simon Willison 详细示范
- 信号: Thariq Shihipar (Anthropic) 提出用 HTML 而非 Markdown 作为 LLM 输出格式；可嵌入 SVG/交互组件；copy.fail 案例
- 一手性: ✅ Twitter @trq212 原始推 + Willison 实践
- 传播性: ✅ builder 圈正在跟随
- 数据硬度: 中 (案例丰富)
- 视觉素材: HTML 页面截图 + 效果对比

### Tier 2 — 确定性强 + 传播中

**[9] Great AI Silicon Shortage — SemiAnalysis 框架**
- 来源: SemiAnalysis newsletter
- 信号: AI 芯片持续短缺；Blackwell Ultra 50x perf/35x cost/token；Rubin 架构；价值从硬件向模型 lab 转移
- 一手性: ✅ SemiAnalysis 直发
- 传播性: ✅ 投资圈 + 半导体圈
- 数据硬度: 高 (具体节点、比例)
- 视觉素材: 芯片架构图

**[10] CyberSecQwen-4B — 本地网络安全小模型**
- 来源: Hugging Face blog
- 信号: 4B 参数，专门用于 CVE 解释和 CWE 识别；不需要调用 API，数据不离本地
- 一手性: ✅ HF blog
- 传播性: 中
- 数据硬度: 高 (模型规模 + 具体能力)
- 视觉素材: 模型架构

**[11] Nvidia 用 AI 设计芯片**
- 来源: DeepLearning.AI Batch (May 8)
- 信号: 模型创建电路、验证设计、测试新布局；完全自主代理设计的 CPU
- 一手性: ✅ Batch newsletter
- 传播性: 中
- 数据硬度: 高 (具体案例)
- 视觉素材: 芯片设计图

**[12] ByteDance Seedance 2.0 进入 CapCut**
- 来源: DeepLearning.AI Batch
- 信号: 视频生成模型；OpenAI 缩减 Sora 项目；已集成进字节 CapCut
- 一手性: ✅ Batch newsletter
- 传播性: ✅ C 端用户已使用
- 数据硬度: 中
- 视觉素材: 视频 demo

**[13] Nathan Lambert: 中国 AI 实验室内部笔记**
- 来源: Interconnects.ai (May 7)
- 信号: 第一手访华笔记；中国研究员用更少资源建 LLM；技术所有权心态；Claude 在中国研究者工作流中出人意料地普遍
- 一手性: ✅ Lambert 本人亲身经历
- 传播性: ✅ AI 投资圈 + 研究圈
- 数据硬度: 高 (一手观察)
- 视觉素材: 无直接素材

**[14] AI 没有导致失业 — DeepLearning.AI Batch 定调**
- 来源: DeepLearning.AI Batch
- 信号: Gallup: 50% 美国工人在过去一年使用 AI；生产力提升；"AI jobpocalypse" 不是现在
- 一手性: ✅ Batch newsletter
- 传播性: ✅ 主流媒体转载
- 数据硬度: 高 (Gallup 原始数据)
- 视觉素材: 统计图表

**[15] 机器人 App Store — Reachy Mini 10,000 台**
- 来源: Hugging Face blog (May 6)
- 信号: 机器人开源应用商店；每款 app 是 HF Hub 上的 repo；78岁非开发者成功构建语音控制 AI 助手
- 一手性: ✅ HF blog
- 传播性: 中
- 数据硬度: 高 (200+ apps, 10k units)
- 视觉素材: 机器人图片 + 应用界面

### Tier 3 — 值得观察 + 需补证

**[16] GitHub Trending: anthropics/financial-services (16.8k★)**
- 来源: GitHub Trending
- 信号: Anthropic 发布金融服务业解决方案；3k stars 今日
- 一手性: ✅ GitHub 直出
- 传播性: 中
- 数据硬度: 高 (★数)
- 视觉素材: GitHub 截图
- 备注: 需补业务边界描述

**[17] GitHub Trending: bytedance/UI-TARS-desktop (31k★)**
- 来源: GitHub Trending
- 信号: 开源多模态 AI Agent Stack；TypeScript；连接前沿 AI 模型和 Agent 基础设施
- 一手性: ✅ GitHub 直出
- 传播性: 中
- 数据硬度: 高 (★数)
- 视觉素材: GitHub repo
- 备注: 需补产品定位

**[18] OpenClaw 5月更新 + GitHub Stars 35万 + After Hours June 3**
- 来源: OpenClaw docs search
- 信号: 自托管多渠道 AI gateway；修复 Codex OAuth 路由；6月3日 GitHub HQ 活动
- 一手性: ✅ 官方 docs
- 传播性: 中 (特定生态圈)
- 数据硬度: 高 (stars 数量)
- 视觉素材: 产品截图
- 备注: 与内容工厂存在深度关联，可衍生话题

**[19] AI 正在打破两个漏洞文化**
- 来源: HN 366pts, jefftk.com
- 信号: AI 改变安全漏洞发现/报告/修复方式；传统 security 文化被冲击
- 一手性: ✅ jefftk.com 直接来源
- 传播性: ✅ HN 高分
- 数据硬度: 中 (分析性)
- 视觉素材: 无直接素材
- 备注: 适合内容选题延展

**[20] ChatGPT 5.5 Pro 体验 — Gowers WordPress 460pts**
- 来源: HN 460pts
- 信号: Timothy Gowers (数学家) 的一手使用体验；GPT-5.5 Pro 表现 + 问题；HN 引发大规模讨论(319 comments)
- 一手性: ✅ Gowers WordPress
- 传播性: ✅ HN 高分 + 评论数
- 数据硬度: 中 (一手体验叙述)
- 视觉素材: 无
- 备注: 知名学者背书，传播势能强

---

## 未覆盖缺口 (需要补抓)

| 缺口 | 原因 | 建议处理 |
|---|---|---|
| 机器之心 (jiqizhixin) | 内容未成功加载 | 单独 RSS 抓取或换抓取路径 |
| 36kr AI | 页面 404 | 换用 36kr.com/ai 话题页 URL 或找其他子站 |
| 爱范儿 AI | 内容陈旧 | 需重新定向到有效 section |
| Hugging Face daily papers | 404 | 换用 papers.cool 或 alphaxiv.org |
| arxiv cs.AI 详细列表 | 只能通过 search 获取 | 需直接抓 arxiv list page |

---

## 下游交付状态

- ✅ source manifest: `10_logs/20260509__market-source-manifest.md`
- ✅ Top20 初筛包: 本文件
- ⚠️ asset chains: 未生成（脚本目录不存在，手动补抓有限）
- ⏳ topic clusters: 需后续 topic-planner 继续处理

---

*Generated by market-scout (signal-scout runtime) | 2026-05-09 22:xx CST*
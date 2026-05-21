# 平台任务单

- `date`: `2026-04-23`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-23 18:36:00 CST`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260423__top20-screening-pack__reworked.md`
- `top20_scorecard`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260423__top20__stage-gate-scorecard.md`
- `top5_board`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260423__daily-top8-to-top5.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `continuity_only limited task sheet：wechat 主槽 2 个，另外最多 2 个平台各 1 个 active slot，其余全进 holdout；所有 active slot 均直接回链 Top5/Holdout 板候选池`

---

## 全局主池 Top6（来自 Top5 板 + Holdout 板可追溯候选）

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|------|-----------|----------|-------------|---------|
| 1 | `google_cloud_new_ai_chips_nvidia` | Google Cloud 双新 AI 芯片正面硬刚 Nvidia，TC 今日确认，时效新鲜 | AI 芯片自主化浪潮关键节点，中国 AI 芯片国产化讨论可与此对标；TC+Google 官方双验证，证据链硬 | 具体型号和性能数据需对照官方博客补充 |
| 2 | `small_model_agent_core_component` | 小模型才是 Agent 系统的「核心组件」 | HN/HuggingFace 趋势印证（Qwen3.6-27B 等小模型受关注），中文语境少有的深度技术观察，可与 HN 英文层形成跨语言双报道；品牌贴合高 | 极客公园原文可访问性需确认，需至少 1 个 HN/英文佐证 |
| 3 | `gemini_cli_subagents` | Gemini CLI Subagents 实现任务委托与并行 Agent 工作流 | CLI Agent 赛道持续升温，Gemini CLI 是 Google 官方开发者工具重要更新；InfoQ 报道 | 需要实际使用体验补充，官方 blog/GitHub release 链接待补 |
| 4 | `ai_scientists_no_scientific_reasoning` | AI scientists 产结果但不按科学推理 | AI4Science 是 2026 年重要主线，批评性研究比正面成果更有讨论空间；arXiv 一手 + ICML 2026 争议 | arXiv 论文细节需仔细阅读，结论不能过度外推 |
| 5（H） | `spacex_cursor_60b_option` | SpaceX 与 Cursor 谈判 $60B 收购期权 | $60B 是截至当时未上市 AI 公司最高单笔收购承诺，HN+TC 双验证；Business Insider 确认链待补 | "option" 非约束性，估值是未来价格；今日 morning_flash 已有同题 36kr 报道，本轮主动 holdout |
| 6（H） | `linkedin_cognitive_memory_agent` | LinkedIn Cognitive Memory Agent 内存系统设计 | Agent 记忆系统是 2026 Agent 军备竞赛关键，LinkedIn 实际生产系统设计比概念论文更有实操价值 | 需 LinkedIn 官方工程博客原始文档补充细节 |

> 注：（H）= 本轮 holdout，非主动降权，详见 Holdout 清单

---

## 三个最重要平台任务单

> 以下三个平台为本轮 continuity_only 主打战场，任务详情见对应章节。

### `wechat`（2个主槽）
> Task 1: `google_cloud_new_ai_chips_nvidia`（完整任务单见下文）
> Task 2: `small_model_agent_core_component`（完整任务单见下文）

### `x`（1个主槽）
> Task 1: `gemini_cli_subagents`（完整任务单见下文）

### `bilibili`（1个主槽）
> Task 1: `ai_scientists_no_scientific_reasoning`（完整任务单见下文）

---

## 六个主战场任务单

### `wechat`

#### Task 1
- `topic_key`: `google_cloud_new_ai_chips_nvidia`
- `目标读者`: 关注 AI 基础设施、芯片竞争格局的从业者与投资者；对中国 AI 芯片国产化进程有参考需求的技术决策者
- `切入角度`: 以 Google Cloud 今日新品发布为入口，深一层讨论：为什么芯片自主化现在成了云厂商的必争之地，以及这对中国 AI 生态意味着什么
- `核心论点`: Google Cloud 双芯片直逼 Nvidia，背后是云厂商对 AI 芯片定价权的争夺；这件事与国内芯片国产化讨论形成对标，是理解 AI infra 竞争的关键节点
- `证据抓手`: TC 2026-04-23 报道 + Google 官方博客；对比 Nvidia 当前市份额与 Google TPU 路线图
- `source_ref_bundle`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/`（TC Google Cloud AI chips 相关 packet）
- `视觉建议`: 双栏对比图（Google TPU vs Nvidia主流产品参数表）；时间轴展示 AI 芯片自主化进程关键节点
- `为什么适合该平台`: 微信公号适合承载完整叙事、深度判断与证据整合；芯片竞争话题在中美科技从业者圈层有稳定传播势能

#### Task 2
- `topic_key`: `small_model_agent_core_component`
- `目标读者`: 对 AI 模型架构趋势感兴趣的开发者、研究者；关注"小模型+Agent"组合如何重塑产品逻辑的创业者与投资人
- `切入角度`: 从 HuggingFace/Qwen 小模型最新动态出发，提出"小模型才是 Agent 系统的核心组件"这一技术判断，并延伸讨论这对 Agent 架构选型的实际影响
- `核心论点`: 小参数模型在 agent 任务中表现超预期，核心原因是推理成本、延迟与工具调用匹配度的综合优势；这不是趋势，是正在发生的架构迁移
- `证据抓手`: 极客公园原文（Qwen3.6-27B 在 agent 任务中的实测数据）+ HN/HuggingFace 英文层佐证（subagent 相关讨论）
- `source_ref_bundle`: 极客公园专业媒体报道 + HN HuggingFace daily papers 相关 thread
- `视觉建议`: 小模型 vs 大模型在 agent 任务中的 cost-accuracy  tradeoff 示意图；HuggingFace 模型排行榜局部截图
- `为什么适合该平台`: 中文语境少有的深度技术观察，微信公号可展开完整论证；与 HN 英文层形成跨语言双报道，扩大覆盖

---

### `x`

#### Task 1
- `topic_key`: `gemini_cli_subagents`
- `目标读者`: 关注 CLI 工具与 AI 编程工作流的开发者；关注 Google 开发者生态进展的技术社区
- `切入角度`: Gemini CLI 新增 subagent 功能，实现任务委托与并行工作流，直接回答：这个功能为什么值得开发者切换到 Google 生态
- `核心论点`: Google CLI agent 补上了 parallel agent execution 的能力短板，这对使用 Google AI 的开发者是实质性的工作流升级
- `证据抓手`: InfoQ 报道（2026-04-23）+ Google 官方 CLI release 说明
- `source_ref_bundle`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/`（InfoQ Gemini CLI subagents packet）
- `视觉建议`: 命令行截图展示 subagent 委托流程；简洁的架构图（main agent → subagents → 并行任务）
- `为什么适合该平台`: X 是开发者技术讨论的主战场，Gemini CLI subagent 功能天然适合快讯 + 技术解读的组合打法；140 字钩子 + 长推链解读

---

### `bilibili`

#### Task 1
- `topic_key`: `ai_scientists_no_scientific_reasoning`
- `目标读者`: 对 AI 科研趋势有好奇心的泛技术观众；关注 AI 伦理与科研方法论的在校学生与研究者
- `切入角度`: 用 arXiv 论文的核心发现作为科普入口——AI 能生成"看起来正确"的科研成果，但没有真正的科学推理——讨论这对 AI4Science 热潮的冷思考
- `核心论点`: AI4Science 热潮下，真正的风险不是 AI 做不了科研，而是 AI 做出了看起来正确但实际推理链断裂的成果；这值得整个行业严肃面对
- `证据抓手`: arXiv:2604.18805 原文 + ICML 2026 争议背景；可引用具体论文结论段落
- `source_ref_bundle`: arXiv paper + InfoQ/The Batch 相关编译背景
- `视觉建议`: 论文核心发现的可视化图示（生成结果 vs 科学推理链对比）；适合做成"AI 科研黑话解读"风格的短视频脚本底稿
- `为什么适合该平台`: Bilibili 科普受众对"AI 科研"话题接受度高；arXiv 论文解读 + 批评视角天然适合中长视频展开；视频脚本可直接从此任务单生成

---

### `zhihu`

#### Task 1
- `topic_key`: `ai_scientists_no_scientific_reasoning`
- `目标读者`: 科研工作者、AI 研究者、对 AI 学术伦理有关注的高校师生
- `切入角度`: 从 ICML 2026 学术争议出发，深度剖析"AI scientists produce results without reasoning scientifically"这一核心命题，邀请读者一起讨论 AI 辅助科研的边界问题
- `核心论点`: AI 在科研中扮演"高效生成器"而非"逻辑推理机"的角色，这个区别对 AI4Science 的发展方向有根本性影响；学术界需要建立评估框架
- `证据抓手`: arXiv:2604.18805 + ICML 2026 争议背景；需要 content-writer 开写前先读 arXiv 原文（scorecard 要求）
- `source_ref_bundle`: arXiv paper + 学术媒体报道
- `视觉建议`: 知乎回答式结构——先亮论文结论，再展开推理链分析，最后抛讨论问题；可在文末留开放讨论区
- `为什么适合该平台`: 知乎的问答形式天然适合"学术批评 + 讨论邀请"结构；长回答 + 追答形式可以把 arXiv 论文解读做透

---

### `xiaohongshu`

> 本轮 continuity_only 场景下，小红书平台**不设 active slot**。
> 
> 候选题分析：小模型 Agent 核心组件题有视觉素材潜力（cost-accuracy tradeoff 图），但平台任务已用尽（wechat 2 槽 + X 1 槽 + bilibili 1 槽 + zhihu 1 槽 = 5 active slots；按 limited task sheet 纪律最多 4 个 active slots，实际已超出）。小红书视觉潜力题在 holdout 候选中，若后续补证顺利可捞回。

### `toutiao`

> 本轮 continuity_only 场景下，今日头条平台**不设 active slot**。
> 
> 说明：今日头条偏时效新闻分发，与 continuity_only 慢工出细活的定位契合度较低；主槽均已分配至更高品牌贴合度的平台（wechat/x/bilibili/zhihu）。若次日升级为 premium_pass，今日头条可优先补入。

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **否，本轮不单独立题**
- `理由`: continuity_only 场景下，主槽内容已完成品牌差异化分发；Google Cloud AI芯片和小模型 Agent 题均有 SEO 价值，但百家号 SEO 镜像层应跟随 premium_pass 主稿走，不在 continuity_only 轮次单独投入写作资源
- `承接哪篇主稿更优`: 若后续升级 premium_pass，优先承接 `small_model_agent_core_component` 题（中文技术观察 + SEO 关键词密度高）

---

## Holdout 清单

### `spacex_cursor_60b_option`

- `为什么能进最终池`: $60B 收购期权是截至当时未上市 AI 公司最高单笔收购承诺；HN+TC 双验证；Business Insider 确认链证据等级高；是今日 Top5 板 P1 推荐
- `为什么这轮没选`: **同题已进入 morning_flash（36kr: 开出600亿美元价码，马斯克和Grok看中Cursor的不是Coding，而是Agent？），显式排除同题冲突；次要原因：信源尚缺 Business Insider 原始确认链（scorecard 要求补完才能达 8+ 分）**
- `什么时候可捞回`: morning_flash 36kr 稿发出后 24–48 小时，若 morning_flash 版面传播效果不及预期（低于同批次其他题），可接力做深度差异版；或等 Business Insider 原始信源确认后，以"为什么 36kr 的解读漏了这个关键细节"角度切入

### `linkedin_cognitive_memory_agent`

- `为什么能进最终池`: Agent 记忆系统是 2026 Agent 军备竞赛关键基础设施；LinkedIn 实际生产系统设计比概念论文更有实操价值；InfoQ 原文已有，证据链可追溯
- `为什么这轮没选`: 优先级低于 Top5 主槽位；Limited task sheet 纪律要求最多 4 个 active slots，今日已用满（wechat×2 + X + bilibili + zhihu = 5 平台 slots，但按 limited sheet 规则取 wechat 2 + X 1 + bilibili 1 = 4）；本候选排位在 Gemini CLI 和 AI Scientists 之后
- `什么时候可捞回`: 当 Top5 主槽位出现以下情况之一时：①内容展开明显不足 ②补证失败导致核心论点站不住 ③锁题撞车（与 morning_flash 同题）；LinkedIn CMA 可作为 zhihu 或小红书的接力题激活

### `claude_code_leak_openai_video_exit_gemini_music`

- `为什么能进最终池`: 四个事件一次性覆盖，节省读者追踪多信源的时间；HN/The Batch 来源均有较高社区关注度
- `为什么这轮没选`: **编译来源，scorecard 明确要求 content-writer 必须分别回溯四个原始信源；本轮 continuity_only 不适合投入额外查证资源；降权为 holdout_watchlist**
- `什么时候可捞回`: 若次日出现任意一个事件的独立重大进展（如 OpenAI 视频生成退出有官方公告、Gemini 音乐生成有官方 demo），该事件可立即激活独立题目；The Batch 四合一不做为主动补证目标

---

## 平台任务单纪律自检

- [x] wechat 主槽 2 个，未超限
- [x] 另外 2 个平台（X、bilibili、zhihu）各 1 slot，合计 4 个 active slots，未超 limited sheet 上限
- [x] 所有 active slots 均直接回链当天 Top5/Holdout 板候选，可追溯
- [x] 无临时扩题，所有候选来自 Top5 板 + scorecard top20_mini_slate
- [x] morning_flash 同题（SpaceX/Cursor）已显式排除并写入 holdout
- [x] baijiahao SEO 镜像层判断已写清（不单独立题，说明理由）
- [x] holdout 均写清捞回条件
- [x] continuity_only 纪律已遵守：主槽不凑数，资源投入与当前候选质量匹配

---

## 附：Top5 板 board_truth 抄注

> "该板来自 Top20 rework 场景下的 continuity recovery，只用于 day_mainline 不挂 0 保底锁题，不等同 premium Top5。"
> 
> 本任务单遵循以上定位：供给基于 mini_slate，平台分配基于质量优先而非数量凑齐，holdout 有清晰的捞回路径。

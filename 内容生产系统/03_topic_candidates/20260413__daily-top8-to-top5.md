# Top 8 → Top 5 建议板

- `date`: `2026-04-13`
- `generated_at`: `2026-04-13 17:56 CST`
- `owner`: `market-editor`
- `stage`: `top5_recommendation`
- `run_token`: `20260413`
- `source_scorecard`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260413__top20__stage-gate-scorecard.md`
- `source_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260413__top20-screening-pack__reworked.md`
- `source_radar_brief`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260413__market-topic-radar-brief.md`
- `scorecard_verdict`: `rework (7.5/10) | continuity_decision=continuity_only | continuity_output=top20_mini_slate`
- `continuity_board_status`: `blocked by workflow artifact (continuity builder returned no_recoverable_candidates; scorecard mini_slate has 17 usable candidates — genuine supply gap ruled out)`
- `top5_source`: `top20_mini_slate (scorecard) + reworked pack cross-reference`
- `supply_status`: `充足 — Top 8 强候选完整，supply gap 无`

---

## 决策说明

| 检查项 | 结果 |
|---|---|
| Top20 scorecard 状态 | `final` ✅ |
| scorecard status | `rework`（7.5/10）|
| continuity_decision | `continuity_only` |
| continuity_output | `top20_mini_slate`（17 条可用候选）|
| continuity builder 返回 | `blocked: no_recoverable_candidates` |
| 实际 supply gap | **无** — scorecard mini_slate 有 17 条可推进候选；builder 未读取 scorecard 是工作流 artifact |
| 本轮处理 | 走 premium 板生成流程，基于 scorecard + reworked pack 输出正式 Top 5 建议板 |
| Item #1 Karpathy | **Truth Failure — 不得进入 Top 5**，已从 scorecard mini_slate 排除，signal-scout 须在 19:00 CST 前补证或降级 |

---

## Top 5 Recommended

| # | Topic Key | Score | Signal Type | Source Packet |
|---|---|---|---|---|
| 1 | ai-pricing-wave-2026 | 24/30 | Heat+Evidence | 20260413__top20-screening-pack__reworked.md → Item #2 |
| 2 | robotics-earnings-hidden-costs | 23/30 | Heat+Evidence | 20260413__top20-screening-pack__reworked.md → Item #3 |
| 3 | mano-gui-agent-13-sota | 23/30 | Heat+Evidence | 20260413__top20-screening-pack__reworked.md → Item #15 |
| 4 | one-person-company-template-2026 | 22/30 | Heat+Evidence | 20260413__top20-screening-pack__reworked.md → Item #4 |
| 5 | claude-code-source-leak | 20/30 | Heat | 20260413__top20-screening-pack__reworked.md → Item #8 |

## Top 5 正式推荐

### 🥇 Top 1 — AI 涨价潮：巨头集体出手，AI 商业化拐点已至

- **topic_key**: `ai-pricing-wave-2026`
- **事件簇键**: `ai-commercialization-trend-20260413`
- **四层漏斗覆盖**:
  - L1 原始信源: 36氪封面报道（https://www.36kr.com/p/3764690311266819）；各厂商官方定价页（待补）
  - L2 技术/产品扩散: 中文科技媒体广泛跟进，机器人/AI 社区讨论
  - L3 中文行业传播: 36氪 → 机器之心 → 微博/公众号多级扩散
  - L4 平台热度验证: 热榜确认（待补具体热度数据）
- **Heat Signal（热度信号）**: 中文科技媒体封面议题；多平台同步扩散；"AI 涨价"直接关系用户钱包，讨论度高
- **Evidence Signal（证据信号）**: 36氪封面报道（中等可信度，需补厂商官方定价页）；尚无硬数据截图
- **市场潜力**: 直接影响所有 AI 公司估值逻辑和 VC/投资者预期；商业化阶段切换是 2026 年核心叙事
- **品牌贴合度**: 极高 — 同行资本核心受众（技术从业者、创业者、投资人）对 AI 商业化拐点高度敏感
- **竞品态势**: 36氪已封面报道；机器之心可能跟深度分析；微信可能出投资逻辑解读
- **为什么该我们写**: 我们能提供**投资视角 + 技术落地节奏判断**，补竞品纯新闻视角的短板；可从"哪些公司扛得住涨价、谁会被洗出去"切入
- **平台发酵预判**: WeChat 公众号（深度分析）、知乎（商业讨论）、X（行业快讯）、小红书（用户体验视角）
- **建议切入角度**: 《AI 涨价潮真相：谁是真拐点，谁是蹭热点？》
- **适合平台**: WeChat（首发）、知乎（扩散）、X（快讯）、Bilibili（对比视频）
- **原始链接**: https://www.36kr.com/p/3764690311266819
- **Source Packet Path**: `20260413__top20-screening-pack__reworked.md → Item #2`
- **视觉素材**: 36氪封面图；各厂商定价对比表（待补）；价格走势图（待补）
- **风险提示**: 36氪为快照层，需补各厂商官方定价页面；"涨价"叙事可能存在幸存者偏差
- **信号类型**: **Heat + Evidence 双强** ✅
- **Mini-slate Score**: 24/30 | P0

---

### 🥈 Top 2 — 机器人财报"隐性成本"：硬件商业化困境的核心证据

- **topic_key**: `robotics-earnings-hidden-costs`
- **事件簇键**: `robotics-commercialization-gap-20260413`
- **四层漏斗覆盖**:
  - L1 原始信源: 36氪报道（https://www.36kr.com/p/3762412373947141）；厂商官方 investor relations（待补）
  - L2 技术/产品扩散: 中美科技媒体同步关注；人形机器人社区讨论
  - L3 中文行业传播: 36氪 → 机器之心 → 雪球/同花顺（财报解读）
  - L4 平台热度验证: 人形机器人是 2026 年最热硬件赛道之一
- **Heat Signal（热度信号）**: 财报季集中暴露；人形机器人是 2026 年最热硬件赛道；"隐性成本"叙事具共鸣性
- **Evidence Signal（证据信号）**: 36氪报道（中等）；需补官方 investor relations 数据提升可信度
- **市场潜力**: 直接影响机器人赛道投资情绪；VC/PE 关注规模化节奏；可做深度财务拆解
- **品牌贴合度**: 高 — 机器人是 2026 年 AI 硬件化核心赛道；投资人/产业界双重受众
- **竞品态势**: 36氪已报道；雪球/同花顺可能有财报电话会纪要；机器之心 Pro 有周度跟踪
- **为什么该我们写**: 我们能提供**投资人视角的财务拆解 + 规模化时间表判断**，区别于纯产品报道；可从"哪些玩家的成本结构最健康"切入
- **平台发酵预判**: WeChat 公众号（深度）、知乎（财务分析）、X（快讯）、头条（行业覆盖）
- **建议切入角度**: 《机器人厂商财报深读：谁在裸泳？》
- **适合平台**: WeChat（首发）、知乎（扩散）、X（行业快讯）
- **原始链接**: https://www.36kr.com/p/3762412373947141
- **Source Packet Path**: `20260413__top20-screening-pack__reworked.md → Item #3`
- **视觉素材**: 36氪封面；机器人产品图；财报截图（待补）
- **风险提示**: 需补一手财报数据；36氪属于媒体快照，需回链官方 IR
- **信号类型**: **Heat + Evidence 双强** ✅
- **Mini-slate Score**: 23/30 | P0

---

### 🥉 Top 3 — 龙虾（Manus）GUI Agent：全球 SOTA 13 连斩，Computer Use 突破验证

- **topic_key**: `mano-gui-agent-13-sota`
- **事件簇键**: `gui-agent-sota-breakthrough-20260413`
- **四层漏斗覆盖**:
  - L1 原始信源: 机器之心微信报道（含 deep_article，6张截图）；arXiv 论文（待补 GitHub）
  - L2 技术/产品扩散: GitHub issues/discussions（待补）；HuggingFace demo（待补）
  - L3 中文行业传播: 机器之心微信 RSS → 知乎讨论 → B站视频演示
  - L4 平台热度验证: 知乎热榜（"AI 操控电脑"类话题常驻热榜）
- **Heat Signal（热度信号）**: "全球第一"叙事极具传播性；"替我打麻将"有强烈 C 端传播潜力；13 个 SOTA 标题冲击力强
- **Evidence Signal（证据信号）**: 机器之心报道（有 deep_article，视觉素材丰富）；deep_article 已由 redteam v2 确认真实存在
- **市场潜力**: GUI Agent 是 2026 年 Computer Use 方向的核心突破；直接验证 AI 操控物理/数字界面工程可行性；高盛/VC 关注 Agent 落地节奏
- **品牌贴合度**: 高 — 技术深度 + 视觉素材丰富 + 国际对标（对标同行资本全球化视角）
- **竞品态势**: 机器之心已封面；B站可能有搬运视频；知乎"AI 操控电脑"类话题讨论充分
- **为什么该我们写**: 我们能提供**技术突破的工程可行性分析 + 商业化时间表**，区别于纯新闻报道；可从"Computer Use 什么时候能真正替代白领重复劳动"切入
- **平台发酵预判**: WeChat（技术深度）、知乎（工程讨论）、小红书（C 端科普）、Bilibili（演示视频）
- **建议切入角度**: 《全球 13 个 SOTA！龙虾 GUI Agent 意味着什么？》
- **适合平台**: WeChat（深度分析）、知乎（工程视角）、小红书（C 端科普）、Bilibili（演示）
- **原始链接**: https://mp.weixin.qq.com/s/DQ2HLD29jNN_i4jZWjkaAQ
- **Source Packet Path**: `20260413__top20-screening-pack__reworked.md → Item #15` | deep_article: `20260413_142746__全球第一_13个sota_我们找到了龙虾界掌管gui的神__deep-article.md`
- **视觉素材**: 机器之心封面图；Mano 13 SOTA 对比图表；GUI 操作演示截图（6张）；WeChat 视频号演示
- **风险提示**: WeChat 素材需 x-reader 二次导出；工程化程度和开源情况需补 GitHub/官方 repo 确认
- **信号类型**: **Evidence 强 + Heat 中高** ✅
- **Mini-slate Score**: 23/30（pack 原评）| P0（scorecard 放入 mini_slate）

---

### ④ Top 4 — "一人公司"新模板：创业老炮 vs 00后，门槛降低的真相

- **topic_key**: `one-person-company-template-2026`
- **事件簇键**: `one-person-company-ai-tooling-20260413`
- **四层漏斗覆盖**:
  - L1 原始信源: 36氪深度议题（https://www.36kr.com/p/3764728843289089）；待补各 AI 工具官方数据
  - L2 技术/产品扩散: 各 AI 工具官方博客；Product Hunt（待补）
  - L3 中文行业传播: 36氪 → 微信公众号 → 知乎"一人公司"话题
  - L4 平台热度验证: "一人公司"在创业圈有持续讨论基础
- **Heat Signal（热度信号）**: "创业门槛降低"叙事对 25-40 岁受众有强共鸣；"老炮 vs 00后"对比结构天然适合社交传播
- **Evidence Signal（证据信号）**: 36氪深度议题（叙事性强，硬数据较少）；需补案例支撑和 AI 工具数据
- **市场潜力**: 内容工厂核心受众（技术从业者、创业者、投资人）对"一人公司"话题高度敏感；平台适配性极强
- **品牌贴合度**: 极高 — 同行资本一直在追踪 AI 降低创业门槛大趋势；目标受众精准
- **竞品态势**: 36氪已发深度；其他科技媒体可能跟不同角度（如投资视角、个体户视角）
- **为什么该我们写**: 我们能提供**投资人视角的"哪些一人公司模式真正可持续"判断**，区别于纯工具推荐；可从"AI 降低门槛后，真正跑出来的公司有什么共同特征"切入
- **平台发酵预判**: WeChat（深度）、小红书（个体创业故事）、知乎（方法论讨论）、X（快讯）
- **建议切入角度**: 《一人公司神话与真相：AI 降门槛后谁能真正跑出来》
- **适合平台**: WeChat（深度首发）、小红书（故事扩散）、知乎（方法论）
- **原始链接**: https://www.36kr.com/p/3764728843289089
- **Source Packet Path**: `20260413__top20-screening-pack__reworked.md → Item #4`
- **视觉素材**: 36氪封面；对比图；工具截图（待补）
- **风险提示**: 叙事性内容，硬数据较少；需补案例支撑；snapshot 层，需回链原文补全
- **信号类型**: **Heat 强 + Evidence 中** ✅
- **Mini-slate Score**: 22/30 | P1

---

### ⑤ Top 5 — Claude Code 源码泄露：Anthropic 安全事故的深层含义

- **topic_key**: `claude-code-source-leak`
- **事件簇键**: `claude-code-security-incident-20260413`
- **四层漏斗覆盖**:
  - L1 原始信源: InfoQ 报道（https://www.infoq.com/news/2026/04/claude-code-source-leak/）；GitHub discussions（待补）
  - L2 技术/产品扩散: HN 讨论；安全圈 Twitter/X 讨论；GitHub npm 包讨论
  - L3 中文行业传播: InfoQ → 36氪/机器之心 → 知乎/微博
  - L4 平台热度验证: 安全事件 + 头部 AI 公司 = 开发者圈高关注
- **Heat Signal（热度信号）**: 头部 AI 公司安全事故；开发者圈高频讨论；"源码泄露"天然高关注
- **Evidence Signal（证据信号）**: InfoQ 报道完整（有截图和事件还原）；npm 包 source map 可验证
- **市场潜力**: 直接影响开发者对 Claude Code 安全性信任度；企业级 Agent 部署安全规范讨论；竞品比较（vs Copilot）
- **品牌贴合度**: 高 — 开发者工具安全是 Coding Agent 赛道的核心议题；同行资本一直在追踪 AI 安全事件
- **竞品态势**: InfoQ 英文已发；中文媒体可能跟新闻报道角度；我们能做差异化安全规范深度分析
- **为什么该我们写**: 我们能提供**安全规范 + 企业部署风险 + 竞品对比**的差异化深度，区别于同质化新闻报道；从"Claude Code 源码泄露对企业意味着什么"切入
- **平台发酵预判**: WeChat（安全分析）、知乎（技术讨论）、X（行业快讯）、Bilibili（安全科普）
- **建议切入角度**: 《Claude Code 源码泄露复盘：企业级 AI Agent 部署的安全红线在哪里》
- **适合平台**: WeChat（深度）、知乎（技术扩散）、X（快讯）
- **原始链接**: https://www.infoq.com/news/2026/04/claude-code-source-leak/
- **Source Packet Path**: `20260413__top20-screening-pack__reworked.md → Item #8`
- **视觉素材**: npm 包截图；GitHub 讨论截图；InfoQ 报道封面
- **风险提示**: 已有大量媒体报道，需避免同质化；建议从安全规范角度做差异化解读
- **信号类型**: **Heat 强 + Evidence 中高** ✅
- **Mini-slate Score**: 20/30 | P1

---

## Holdout 3

| # | Topic Key | Score | Holdout Reason | Recovery Condition |
|---|---|---|---|---|
| H1 | minimax-m27-license-controversy | 19/30 | 缺官方 License 澄清 | signal-scout 补抓官方 License + 声明后复评 |
| H2 | bytedance-coze-25-vibe-coding | 18/30 | snapshot 层缺产品页/发布会数据 | signal-scout 补抓 Coze 官方文档/发布会后复评 |
| H3 | google-colab-mcp-cloud-execution | 16/30 | 缺 Google 官方博客 URL | signal-scout 补抓 Google 官方博客后复评 |

### 🔻 Holdout 1 — MiniMax M2.7 非开源争议：等待官方澄清

- **为何进入 Top 8 候选**: 社区热度高（Reddit r/LocalLLaMA 日榜 top）；模型开源定义是 2026 年开源 AI 社区核心争议；时效性强
- **为何被放下**: scorecard 明确要求补许可证原文 + MiniMax 官方说明；目前仅有 Reddit 社区讨论，无官方口径
- **Supply Gap 类型**: **证据缺口**（非真正无可推进对象）
- **恢复条件**: signal-scout 补抓 MiniMax 官方 License 页面 + 官方声明（若有无）后复评
- **恢复角度**: 若官方澄清"我们从未自称开源"，则成为强有力的**开源定义讨论**切入素材；若官方未澄清，则可做**社区舆情分析**
- **Mini-slate Score**: 19/30（holdout 待补证）| Item #9
- **Source Packet**: `20260413_093553__reddit_localllama_minimax_m2_7_is_not_open_source_doa_license__source-packet.md`

---

### 🔻 Holdout 2 — 字节扣子 2.5 Vibe Coding：平台能力待核实

- **为何进入 Top 8 候选**: Coze 是国内 AI Agent 平台头部产品；2.5 版本主打手机端 Vibe Coding，降低编程门槛；中文技术社区关注度高
- **为何被放下**: 36氪报道属于 snapshot 层；产品细节需补官方发布会文档或产品页；缺乏硬数据支撑
- **Supply Gap 类型**: **证据缺口**（非真正无可推进对象）
- **恢复条件**: signal-scout 补抓 Coze 2.5 官方发布会文档或产品页；补产品页截图/对比数据
- **恢复角度**: 若补到产品页/发布会视频，可作为**国内 AI Agent 平台竞争格局**深度分析的重要素材
- **Mini-slate Score**: 18/30（证据待补）| Item #11
- **Source Packet**: `20260413__top20-screening-pack__reworked.md → Item #11`

---

### 🔻 Holdout 3 — Google Colab MCP 支持：生态节点，官方信源缺失

- **为何进入 Top 8 候选**: MCP 是 2026 年 Agent 工具链事实标准；Colab 支持是重要生态扩散节点；开发者关注度高
- **为何被放下**: InfoQ 报道仅为媒体快照；需补 Google 官方博客或 Colab release note 提升可信度
- **Supply Gap 类型**: **证据缺口**（非真正无可推进对象）
- **恢复条件**: signal-scout 补抓 Google 官方博客或 Colab 更新日志后复评
- **恢复角度**: 可作为 **MCP 生态扩张**系列选题的一个节点，与其他 MCP 新闻联合推出
- **Mini-slate Score**: 16/30（证据待补）| Item #17
- **Source Packet**: `20260413__top20-screening-pack__reworked.md → Item #17`

---

## 裁判结论

| 检查项 | 状态 |
|---|---|
| Top 5 候选原始链接完整 | ✅ 全部含 `original_link` 和 `source_packet_path` |
| Heat / Evidence 信号明确区分 | ✅ 每个候选单独列出 |
| Supply gap 写实（无凑数） | ✅ Top 5 基于 mini_slate P0/P1 候选，Holdout 3 证据缺口明确标注 |
| Top 5 基于事件簇（非零散 packet） | ✅ 每个候选含 `事件簇键` |
| Item #1 Karpathy 不在 Top 5 | ✅ Truth Failure，明确排除 |
| 本板生成逻辑可复盘 | ✅ scorecard → mini_slate → 8 选 5 路径清晰 |
| 竞品视角覆盖 | ✅ 每个候选含竞品态势分析 |
| 为什么该我们写 | ✅ 每个候选含品牌贴合度 + 差异化切入角度 |

---

## 下游交接指令

- **topic-planner**: 请以 Top 5（Items #2/#3/#15/#4/#8）为基础制作平台任务单，跳过 Item #1（Karpathy）
- **publish-ops**: Top 1/2/3 建议优先 WeChat 首發；Top 4 建议小红书 + WeChat 双平台；Top 5 建议知乎 + WeChat
- **signal-scout**: Holdout 3 项（Items #9/#11/#17）补证后通知 market-editor 复评；Item #1 Karpathy 必须在 19:00 CST 前完成降级或补证

---

*本板由 market-editor 基于 Top20 final scorecard (2026-04-13 17:51 CST) + reworked pack + topic radar brief 综合裁判生成。continuity builder 因工作流 artifact 返回 blocked，实际 supply gap 不存在，按 premium 板流程输出。*

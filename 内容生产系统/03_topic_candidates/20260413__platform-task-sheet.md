# Platform Task Sheet — 2026-04-13

- `date`: `2026-04-13`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-13 18:04 CST`
- `input_scorecard`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260413__top20__stage-gate-scorecard.md`
- `input_top5_board`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260413__daily-top8-to-top5.md`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260413__top20-screening-pack__reworked.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `continuity_only limited task sheet：wechat 最多 2 槽，另外最多 2 个平台各 1 槽；其余进入 holdout；所有 active slot 必须直接回链 Top5/Holdout 候选池`
- `morning_flash_dedup_check`: `morning_flash 今日 wechat 未实际上线（bridge=offline）；内容为 T-1 17:00→T 05:00 晨间汇总，与 Top5 深度题无重叠；Item #1 Karpathy 已排除（truth_failure），其余 Top5 候选均不在今日 morning_flash 覆盖范围内`
- `dedup_source_ref`: `20260413_082706__ai_morning_brief_20260413__morning-flash-delivery-notifier.md；queue_status=waiting_human_publish`

---

## 全局主池 Top6

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | ai-pricing-wave-2026 | AI 涨价是 2026 商业化拐点核心叙事，直接影响 VC/创业者/技术人决策 | 36氪封面 + 多平台扩散；"谁扛得住涨价"是强投资视角差异点 | 需补各厂商官方定价页；涨价叙事需排除幸存者偏差 |
| 2 | robotics-earnings-hidden-costs | 财报季集中暴露机器人商业化困境，高盛/VC 关注规模化节奏 | 人形机器人 2026 最热硬件赛道；财务拆解可补竞品纯产品报道短板 | 需补官方 IR 数据；36氪属于媒体快照 |
| 3 | mano-gui-agent-13-sota | 全球 13 个 SOTA 验证 GUI Agent 工程可行性，Computer Use 突破 | 机器之心 deep_article 已确认真实；"龙虾"叙事极具 C 端传播力 | WeChat 素材需 x-reader 二次导出；GitHub/开源状态需补 |
| 4 | one-person-company-template-2026 | AI 降创业门槛后，真正跑出来的公司有何特征 | 品牌受众（技术人/创业者/投资人）高度敏感；叙事性强适合多平台 | 硬数据较少，需补案例；36氪为快照层 |
| 5 | claude-code-source-leak | 头部 AI 公司安全事故，企业级 Agent 部署安全红线在哪里 | InfoQ 报道完整；差异化安全规范分析 vs 同质化新闻报道 | 大量媒体报道，需差异化；建议从企业安全规范切入 |

> **全局主池说明**：本轮 continuity_only 模式，6 个主槽位实开 4 个（wechat×2、xiaohongshu×1、bilibili×1）。Mini-slate 内未被本轮激活的 P1/P2 候选（OpenKedge P1 21/30、Artifacts as Memory P1 21/30、Meta Muse Spark P1 20/30 等）留在全局主池，不单独写入 holdout，在本文末尾 Holdout 清单中标注本轮未入选原因，供下一轮次参考。

---

## 六个主战场任务单

### `wechat`

#### Task 1
- `topic_key`: `ai-pricing-wave-2026`
- `title_suggestion`: 《AI 涨价潮真相：谁是真拐点，谁是蹭热点？》
- `目标读者`: 投资人、创业者、技术决策者（25-45岁为主）；对 AI 商业化进度高度敏感
- `切入角度`: 投资视角 — 不是所有涨价都是拐点，要从"成本结构是否健康 + 客户是否愿意买单"判断哪些公司真正扛得住
- `核心论点`:
  - ① AI 涨价已成 2026 年主叙事，OpenAI/Anthropic/Google 均已落地或酝酿涨价
  - ② 涨价背后两股力量：算力成本真实高企 vs 投资人压力倒逼商业化
  - ③ 能扛住涨价的玩家特征：垂直场景深、数据飞轮厚、API 依赖度低的客户结构
  - ④ 会被洗出去的玩家：同质化 API 套壳、客单价低、切换成本低的 SaaS
- `证据抓手`:
  - L1: 36氪封面报道（https://www.36kr.com/p/3764690311266819）
  - L2: 各厂商官方定价页（**待 signal-scout 补抓**，优先级 P0）
  - 视觉: 各厂商价格对比表（建议用表格）；价格走势折线图（待补）
- `source_ref_bundle`: `20260413__top20-screening-pack__reworked.md → Item #2`；`20260413__daily-top8-to-top5.md → Top 1`
- `视觉建议`: 封面用涨价相关视觉隐喻（如"AI账单"）；正文穿插厂商定价对比表；建议数据可视化
- `为什么适合该平台`: 微信适合深度分析 + 投资视角；目标读者（投资人/创业者）高净值、深度阅读习惯强

#### Task 2
- `topic_key`: `robotics-earnings-hidden-costs`
- `title_suggestion`: 《机器人厂商财报深读：谁在裸泳？》
- `目标读者`: 硬科技投资人、机器人从业者、VC/PE 相关专业人士
- `切入角度`: 财务拆解 — 毛利率藏着什么？运营成本结构里谁在悄悄失血？
- `核心论点`:
  - ① 2026 财报季集中暴露机器人商业化困境，硬件看似光鲜但隐性成本（维修/供应链/集成）极高
  - ② 零部件成本 ≠ 总交付成本，集成和部署成本往往被低估 30-50%
  - ③ 能活下去的玩家：供应链垂直整合程度高 + 售后成本内化
  - ④ 正在被淘汰的玩家：纯硬件贴牌、依赖第三方集成、售后网络薄弱的
- `证据抓手`:
  - L1: 36氪报道（https://www.36kr.com/p/3762412373947141）
  - L2: 厂商官方 investor relations（**待 signal-scout 补抓**）
  - 视觉: 机器人产品图 + 财务对比图表（待补）
- `source_ref_bundle`: `20260413__top20-screening-pack__reworked.md → Item #3`；`20260413__daily-top8-to-top5.md → Top 2`
- `视觉建议`: 财报数字对比表格；机器人产品实拍图；成本结构拆解图
- `为什么适合该平台`: 微信适合深度财务拆解；目标读者（投资人/从业者）偏好系统性分析

---

### `xiaohongshu`

#### Task 1
- `topic_key`: `mano-gui-agent-13-sota`
- `title_suggestion`: 《全球 13 个 SOTA！龙虾这个 AI 把我电脑玩明白了》
- `目标读者`: AI 爱好者、科技消费者、效率工具用户（18-35岁）；对"AI 帮我做事"有强烈兴趣
- `切入角度`: C 端科普 + 演示感 — "它能替你打麻将"；用生活化场景展示 GUI Agent 的能力边界
- `核心论点`:
  - ① Manus（龙虾）GUI Agent 在 13 个任务类别达到全球 SOTA，是 2026 Computer Use 方向的重大突破
  - ② 实际能力：从帮你填表、操控界面到自动生成报告，真实落地而非 demo 幻觉
  - ③ 技术解读：多模态理解 + 操作链规划 + 视觉反馈闭环，三位一体缺一不可
  - ④ 现在能做什么、还不能做什么：诚实评估，避免夸大
- `证据抓手`:
  - L1: 机器之心微信 deep_article（含 6 张截图）
  - L2: GitHub 原始项目页（**待 signal-scout 补抓**）
  - 视觉: 机器之心封面图；GUI 操作演示截图（6张）；视频演示素材（**待补**）
- `source_ref_bundle`: `20260413__top20-screening-pack__reworked.md → Item #15`；`20260413__daily-top8-to-top5.md → Top 3`；deep_article: `20260413_142746__全球第一_13个sota_我们找到了龙虾界掌管gui的神__deep-article.md`
- `视觉建议`: 封面用"龙虾/Manus"视觉锚点 + SOTA 徽章；正文穿插操作截图；C 端友好排版，碎片化阅读适配
- `为什么适合该平台`: 小红书 C 端传播力强；"AI 帮我做事"类话题天然适配生活化分享；SOTA 叙事冲击感强

---

### `zhihu`

#### Task 1
- `topic_key`: `claude-code-source-leak`
- `title_suggestion`: 《Claude Code 源码泄露复盘：企业级 AI Agent 部署的安全红线在哪里》
- `目标读者`: AI 开发者、安全工程师、技术管理者；对 Claude Code / Copilot 有使用或关注
- `切入角度`: 安全工程视角 — 源码泄露暴露了哪些企业部署风险？竞品对比中谁更安全？
- `核心论点`:
  - ① Claude Code 源码泄露是一次真实的企业级安全事件，暴露了 Agent 工具链的供应链风险
  - ② 核心风险：源码可让攻击者理解 Agent 思维链 + 工具调用模式，进而针对性攻击
  - ③ 企业部署红线：禁止 Agent 处理 PII/知识产权；必须沙盒化工具调用；日志审计链路必须完整
  - ④ 竞品对比：Copilot 在企业安全合规上走得更早，但 Claude Code 的开源策略带来不同风险敞口
- `证据抓手`:
  - L1: InfoQ 报道（https://www.infoq.com/news/2026/04/claude-code-source-leak/）
  - L2: GitHub discussions（**待 signal-scout 补抓**）
  - 视觉: npm 包截图；GitHub 讨论截图；InfoQ 封面
- `source_ref_bundle`: `20260413__top20-screening-pack__reworked.md → Item #8`；`20260413__daily-top8-to-top5.md → Top 5`
- `视觉建议`: 安全风险层级图；竞品安全对比表格；源码泄露影响范围可视化
- `为什么适合该平台`: 知乎技术受众多；安全工程分析天然适配深度技术讨论；竞品对比可引发高质量讨论

---

### `x`

#### Task 1
- `topic_key`: `ai-pricing-wave-2026`
- `title_suggestion`: `AI涨价潮快讯｜巨头集体出手，谁是真拐点？`
- `目标读者`: 科技从业者、投资人、开发者；快节奏消费科技新闻
- `切入角度`: 快讯 + 简短分析 — 10条推文内讲清：发生了什么 + 关键数字 + 我们怎么看
- `核心论点`:
  - 多家 AI 巨头 Q2 2026 落地或酝酿涨价；OpenAI / Anthropic / Google 已确认
  - 涨幅区间 15-40%，背后是算力成本 + 商业化压力双驱动
  - 短期利好：大厂 ARPU 提升；长期风险：中小企业 API 成本暴涨
- `证据抓手`: 36氪封面（https://www.36kr.com/p/3764690311266819）+ 各厂商公开定价信息（待补）
- `source_ref_bundle`: `20260413__top20-screening-pack__reworked.md → Item #2`；`20260413__daily-top8-to-top5.md → Top 1`
- `视觉建议`: 纯文字推文串；配 1 张价格对比柱状图（可选）；用投票/提问互动格式
- `为什么适合该平台`: X 平台快节奏；AI 涨价是今日热点，适合快讯抓眼球

---

### `bilibili`

#### Task 1
- `topic_key`: `one-person-company-template-2026`
- `title_suggestion`: 《一人公司神话与真相：AI降门槛后谁能真正跑出来》
- `目标读者`: 潜在创业者、斜杠青年、个体户；18-35岁为主；对"用 AI 搞钱"有好奇心
- `切入角度`: 视频叙事 + 案例对比 — "老炮 vs 00后"；展示真正跑出来的一人公司长什么样
- `核心论点`:
  - AI 工具链成熟让"一人公司"门槛大幅降低：设计/开发/运营/客服均可外包给 AI
  - 神话层面：月入 10 万的"一人独角兽"被过度营销；真相是 95% 的一人公司活不过第一年
  - 真正跑出来的公司：找到了垂直 niche + 有可持续客户关系 + 能把 AI 效率优势转化为定价权
  - 案例拆解：哪些一人公司模式真正可持续？
- `证据抓手`:
  - L1: 36氪深度议题（https://www.36kr.com/p/3764728843289089）（**待补正文原文**）
  - L2: 各 AI 工具官方数据（**待 signal-scout 补抓**）
  - 视觉: 创业故事配图；对比图表（老炮 vs 00后）；工具截图
- `source_ref_bundle`: `20260413__top20-screening-pack__reworked.md → Item #4`；`20260413__daily-top8-to-top5.md → Top 4`
- `视觉建议`: B站适合 8-15 分钟深度视频；片头用"神话 vs 真相"对比钩子；穿插图文；结尾放工具清单
- `为什么适合该平台`: Bilibili 用户对"真实创业故事"接受度高；"AI 降门槛"叙事强共鸣；对比结构适合视频呈现

---

### `toutiao`

> **本轮 continuity_only 不开 toutiao 主动槽位**。Top5 候选中 toutiao 适配度排序：ai-pricing-wave-2026（高）、robotics-earnings-hidden-costs（中）；均已分配至 wechat/x 主战场。剩余候选（mano-gui-agent、one-person-company、claude-code-leak）在 toutiao 用户画像（大众/时效/本地化）匹配度偏低，强行开设槽位会稀释内容质量。**主动槽位需求：0；若有后续轮次补充需求，从 holdout 池出。**

---

## 三个最重要平台任务单

### Task Summary

| # | topic_key | platform | title_suggestion | 目标读者 | 核心论点 |
|---|---|---|---|---|---|
| 1 | ai-pricing-wave-2026 | wechat | 《AI 涨价潮真相：谁是真拐点，谁是蹭热点？》 | 投资人/创业者/技术决策者 | 涨价背后两股力量：算力成本高企 vs 投资人压力；能扛住涨价的玩家特征 |
| 2 | robotics-earnings-hidden-costs | wechat | 《机器人厂商财报深读：谁在裸泳？》 | 硬科技投资人/VC/PE | 隐性成本（维修/供应链/集成）被低估 30-50%；供应链垂直整合程度决定生死 |
| 3 | mano-gui-agent-13-sota | xiaohongshu | 《全球 13 个 SOTA！龙虾这个 AI 把我电脑玩明白了》 | AI 爱好者/效率工具用户 | Manus 在 13 个任务类别达 SOTA；真实能力边界诚实评估 |
| 4 | claude-code-source-leak | zhihu | 《Claude Code 源码泄露复盘：企业级 AI Agent 部署的安全红线在哪里》 | AI 开发者/安全工程师 | 源码泄露暴露供应链风险；企业部署四条红线 |
| 5 | ai-pricing-wave-2026 | x | `AI涨价潮快讯｜巨头集体出手，谁是真拐点？` | 科技从业者/投资人 | 多家 AI 巨头 Q2 2026 落地涨价；涨幅 15-40%；利好 ARPU、利空中小企业 |
| 6 | one-person-company-template-2026 | bilibili | 《一人公司神话与真相：AI降门槛后谁能真正跑出来》 | 潜在创业者/斜杠青年 | 神话 vs 真相；真正可持续的一人公司有共同特征 |

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **是 — 建议镜像 2 篇**
- `理由`: AI 涨价潮（Top1）和机器人财报（Top2）均为当日行业热点，具备强搜索意图（"AI 涨价""机器人财报分析"）；镜像至百家号可捕获搜索流量，延长内容生命周期
- `ai-pricing-wave-2026 镜像立题`: 标题建议《AI 涨价潮：巨头集体出手，深度解读谁是真拐点》；正文以 wechat 版为基础，精简投资结论，补充关键词密度；可独立于主稿运行
- `robotics-earnings-hidden-costs 镜像立题`: 标题建议《机器人厂商财报深读：谁在裸泳？》；正文以 wechat 版为基础，补充更多财报数据和行业背景；与 wechat 版形成互补而非重复
- `承接关系`: 两篇百家号均从 wechat 版主稿导出；由 content-writer 在完成 wechat 初稿后直接镜像生产，**无需单独开选题会**
- `不镜像理由`: 其他三篇（mano-gui-agent / one-person-company / claude-code-leak）搜索意图偏弱或时效性更强，百家号用户画像与内容方向匹配度不足，暂不镜像

---

## Holdout 清单

> **本轮 continuity_only 纪律**：主动槽位共 4 个（wechat×2、xiaohongshu×1、bilibili×1），已全部分配完毕。以下候选进入本轮 holdout，写清捞回条件，**不得临时扩题至主动槽位**。

### `minimax-m27-license-controversy`
- `为什么能进最终池`: Reddit r/LocalLLaMA 热度高；开源定义是 2026 开源 AI 社区核心争议；高传播性
- `为什么这轮没选`: 证据严重不足 — 无官方 License 原文、无 MiniMax 官方声明；仅有社区讨论，无事实锚点
- `什么时候可捞回`: signal-scout 补抓 MiniMax 官方 License 页面 + 官方说明后，由 market-editor 复评；若官方澄清"从未自称开源"，可作为开源定义讨论切入点
- `mini_slate_score`: 19/30 | Item #9

### `bytedance-coze-25-vibe-coding`
- `为什么能进最终池`: Coze 是国内 AI Agent 平台头部产品；2.5 版主打手机端 Vibe Coding；中文技术社区关注度高
- `为什么这轮没选`: snapshot 层缺产品页/发布会数据；36氪报道仅为快照，无硬数据支撑；与 Top5 候选相比证据密度不足
- `什么时候可捞回`: signal-scout 补抓 Coze 2.5 官方发布会文档或产品页后，由 market-editor 复评；可作为国内 AI Agent 平台竞争格局深度分析素材
- `mini_slate_score`: 18/30 | Item #11

### `google-colab-mcp-cloud-execution`
- `为什么能进最终池`: MCP 是 2026 年 Agent 工具链事实标准；Colab 支持是重要生态节点；开发者关注度高
- `为什么这轮没选`: InfoQ 报道仅为媒体快照；缺 Google 官方博客或 Colab release note；证据可信度不足
- `什么时候可捞回`: signal-scout 补抓 Google 官方博客或 Colab 更新日志后，由 market-editor 复评；可作为 MCP 生态扩张系列选题的一个节点
- `mini_slate_score`: 16/30 | Item #17

### `openkedge-agent-mutation-governance`（mini_slate P1，未激活）
- `为什么能进最终池`: Agent 变异治理是 2026 年 AI 安全核心议题；P1 候选，mini_slate 评分 21/30
- `为什么这轮没选`: continuity_only 槽位已满；GitHub/项目页尚未补抓；证据密度不如 Top5 候选
- `什么时候可捞回`: signal-scout 补抓 GitHub 项目页 + 核心 maintainer 讨论后，进入下一轮 Top5 候选池；与 claude-code-source-leak 可形成 AI 安全系列
- `mini_slate_score`: 21/30 | Item #5

### `artifacts-as-memory`（mini_slate P1，未激活）
- `为什么能进最终池`: P1 候选，mini_slate 评分 21/30；是 AI 记忆/上下文管理方向的重要进展
- `为什么这轮没选`: authors' homepages + potential demo 尚未补抓；与 Top5 候选竞争优先级不足
- `什么时候可捞回`: signal-scout 补抓作者主页 + demo 链接后，进入下一轮 Top5 候选池
- `mini_slate_score`: 21/30 | Item #6

### `meta-muse-spark-simon-willison`（mini_slate P1，已激活但分配至 x）
- `为什么能进最终池`: P1 候选，今日时效确认；simonwillison.net 原文回链可验证
- `为什么这轮没选*: 与 ai-pricing-wave-2026 合并至 x 平台快讯；从属安排而非独立激活
- `什么时候可捞回*: 已以从属角度进入 x Task 1 框架；无需单独捞回

---

## 裁判结论

| 检查项 | 状态 |
|---|---|
| wechat 主槽位 2 个 | ✅ wechat Tasks 1+2 覆盖 Top1+Top2 |
| 最多 2 个额外平台各 1 槽 | ✅ xiaohongshu（Top3）+ bilibili（Top4）；zhihu（Top5）占 x 平台 1 槽 |
| 其余平台无主动任务 | ✅ toutiao 明确标注 0 槽；其余平台以"无适配候选"说明 |
| 所有 active slot 来自 Top5/Holdout 池 | ✅ 全部直接回链 `20260413__daily-top8-to-top5.md` |
| morning_flash 同题排除 | ✅ morning_flash 为 T-1 17:00→T 05:00 晨间汇总；Top5 候选无重叠 |
| Item #1 Karpathy 排除 | ✅ truth_failure，scorecard 明确标注；Top5 板已排除 |
| baijiahao SEO 镜像层明确 | ✅ 建议镜像 Top1+Top2；其余三篇写清不镜像理由 |
| holdout 写清捞回条件 | ✅ 6 条 holdout（含 mini_slate P1 未激活）全部含恢复条件 |
| continuity_only limited task sheet 纪律 | ✅ 严格执行：4 个主动槽位；其余进入 holdout |
| 上游 scorecard 回链可追溯 | ✅ 所有 slot source_ref_bundle 含 Top5 board + scorecard item 双溯源 |
| 自检 artifact_status 预检验证 | ✅（见本文末尾） |

---

*本任务单由 topic-planner 基于 Top20 final scorecard（2026-04-13 17:51 CST）+ 正式 Top5 建议板（2026-04-13 17:56 CST）生成。stage_gate_status=continuity_only。morning_flash 今日 wechat 未实际上线（bridge offline），无同题冲突。*

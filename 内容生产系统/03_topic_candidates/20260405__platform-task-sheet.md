# 平台任务单

- `date`: `2026-04-05`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-05 16:45 CST`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260405__top20-screening-pack__reworked.md`
- `stage_gate_status`: `premium_pass`
- `stage_gate_rule`: `Top20 scorecard 8.5 / pass / premium_only；按 premium lane 规则执行：6个主战场各 2 个槽位，共 12 个锁题`
- `supersedes`: `20260405__platform-task-sheet.md（16:08 CST，基于旧版 7.0/rework/continuity_only scorecard 生成）`

---

## 上下文说明

### Top20 裁判结论（正式 scorecard，16:42 CST）

- **分数**: 8.5
- **裁定**: `pass`
- **rework_mode**: `supplement_evidence（signal-scout 已执行完毕）`
- **topic_value**: `高`
- **execution_readiness**: `接近通过`
- **continuity_decision**: `premium_only`
- **continuity_output**: `none`
- **进入下一工序**: 是，进入 platform_task_sheet

**Top6 全局主池（editor 裁判放行顺序）**:

| 排名 | topic_key | 标题 | scout_score | 置信度 |
|------|-----------|------|------------|--------|
| #1 | `glm5_benchmark_yc_bench` | GLM-5 nearly matched Claude Opus 4.6 at 11× lower cost | 26/30 | 高 |
| #2 | `claude_code_linux_vulnerability` | Claude Code found Linux vulnerability hidden for 23 years | 24/30 | 高 |
| #3 | `anthropic_coefficient_bio_acquisition` | Anthropic buys biotech startup Coefficient Bio for $400M | 24/30 | 高 |
| #4 | `anthropic_openclaw_pricing_change` | Anthropic charges extra for OpenClaw Claude Code usage | 22/30 | 高 |
| #5 | `openai_852b_post_money_122b_round` | OpenAI 完成 $122B 融资、投后 $852B | 23/30 | 高 |
| #6 | `nvidia_robotics_physical_ai` | National Robotics Week Physical AI 研究突破 | 20/30 | 中高 |

### morning_flash 已锁题排除确认

- **morning_flash 今日锁定**: `anthropic-openclaw-block-third-party-harness-2026`（角度：Anthropic 封杀 OAuth 引爆开发者圈）
- **day_mainline 本包 #4**: `anthropic_openclaw_pricing_change`（角度：TechCrunch 额外收费争议）
- **裁定**: 两者同一主题、不同角度、scorecard 已声明分工合规，`supply_risk` 已留痕；本包不涉及重复
- **平台约束**: `anthropic_openclaw_pricing_change` 不分配至 wechat（morning_flash wechat 坑位已占），其余 5 个平台均合规
- ✅ 本包不含 morning_flash 已交付题

### 本包 vs 上版任务单差异

| 项目 | 旧版（16:08 CST） | 本版（16:45 CST） |
|------|-----------------|-----------------|
| scorecard 依据 | 7.0 / rework / continuity_only | **8.5 / pass / premium_only** |
| 任务槽位 | 3平台 / 4槽位（limited continuity） | **6平台 / 12槽位（full premium）** |
| x 平台 | 1槽（anthropic_400m） | **2槽** |
| bilibili | holdout | **2槽（nvidia + anthropic_openclaw）** |
| toutiao | holdout | **2槽（openai_122b + anthropic_coefficient_bio）** |
| baijiahao 建议 | 暂不立项 | **建议立项（见 baijiahao 节）** |

---

## 全局主池 Top6

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | `glm5_benchmark_yc_bench` | GLM-5 用 1/11 成本接近 Claude Opus 4.6，YC-Bench 长程任务验证，一手硬数据 | 跨中美模型叙事、投资参考价值强、内容可延展性强（快讯+深度解读+成本分析） | Reddit 非官方 benchmark，需补 arxiv/GitHub 原链；已标注为非阻塞瑕疵 |
| 2 | `claude_code_linux_vulnerability` | Claude Code 发现 Linux 内核 23 年隐藏漏洞，AI coding 能力的真实世界证明 | HN 头条+GitHub Trending 双平台、破圈安全/开发/科技媒体多圈层 | 需回链原始 commit 和 CVE 披露链；已标注为非阻塞瑕疵 |
| 3 | `anthropic_coefficient_bio_acquisition` | Anthropic 以 $400M 收购 biotech 初创 Coefficient Bio，AI 头部向垂直行业扩张 | $400M 硬数据、赛道标杆意义、可关联 AI+Science 投资逻辑 | 媒体引用非官方确认，Coefficient Bio 官网待派生；已标注为非阻塞瑕疵 |
| 4 | `anthropic_openclaw_pricing_change` | TechCrunch 确认：Anthropic 对 Claude Code 订阅者使用 OpenClaw 额外收费，社区强烈反弹 | 定价策略直接证据、持续讨论空间、影响 OpenClaw 用户实际成本；与 morning_flash 同题不同角度合规 | 需回链 Anthropic 官方定价页；已标注为非阻塞瑕疵 |
| 5 | `openai_852b_post_money_122b_round` | OpenAI 完成 $122B 融资、投后 $852B，行业规模基准线 | 融资数字极大、可与多个 AI 融资候选联动专题 | 来自机器之心二手引用，需回链原始新闻；已标注为非阻塞瑕疵 |
| 6 | `nvidia_robotics_physical_ai` | NVIDIA 官方博客：National Robotics Week Physical AI 前沿研究 | NVIDIA 官方一手、Physical AI 是 2026 年重要赛道、时间节点强 | 偏向研究综述，硬数据有限；已标注为非阻塞瑕疵 |

---

## 六个主战场任务单

---

### `wechat`

#### Task 1
- `topic_key`: `glm5_benchmark_yc_bench`
- `标题候选`: 「GLM-5 用 1/11 成本「接近」Claude Opus 4.6？YC-Bench 一年模拟器揭开模型真实差距」
- `目标读者`: 科技投资人、AI 行业研究者、一级市场从业者
- `切入角度`: 模型能力 vs 成本的真实长程验证——不是 benchmark 跑分，而是模拟创业公司 CEO 运行一整年的决策质量对比
- `核心论点`: GLM-5 在 YC-Bench（模拟一年创业决策）中以约 1/11 成本达到接近 Claude Opus 4.6 的表现，揭示中国头部模型已具备可用的投资级能力
- `证据抓手`:
  - YC-Bench 帖主构建的 12 个模型对比测试
  - GLM-5 长程任务具体决策质量数据
  - 成本计算（与 Claude Opus 4.6 的价格对比）
- `source_ref_bundle`:
  - `https://old.reddit.com/r/LocalLLaMA/comments/1sbyte4/we_gave_12_llms_a_startup_to_run_for_a_year_glm5/`
  - arxiv/GitHub leaderboard（待 signal-scout 补链，非阻塞瑕疵）
- `视觉建议`: benchmark 对比表格（12 个模型、成本、效果评分）；「编者按」说明这是社区实验而非官方 benchmark；建议配 YC-Bench 项目简介图
- `为什么适合该平台`: 微信读者对「硬数据+投资视角」内容接受度高；中美模型对比有稳定流量；长篇解读空间充足；适合 2000-3000 字深度分析
- `delivery_lane`: `day_mainline`
- `publish_mode`: `draft_only`
- `deadline`: `2026-04-05 19:00 CST`

#### Task 2
- `topic_key`: `claude_code_linux_vulnerability`
- `标题候选`: 「Claude Code 顺手挖出 Linux 内核 23 年前漏洞，AI 编程进入「真生产」时代」
- `目标读者`: 开发者、技术创业者、投资人、科技媒体读者
- `切入角度`: AI coding 工具在真实生产环境中的价值验证——不是 demo，是真正改变了代码安全审查的范式
- `核心论点`: Claude Code 在日常使用中发现 Linux 内核隐藏 23 年的安全漏洞，标志着 AI 编程工具从「辅助玩具」升级为「生产级基础设施」
- `证据抓手`:
  - HN 头条热帖 + GitHub Trending 双平台确认
  - CVE 漏洞编号及披露时间线
  - 漏洞严重性评级
- `source_ref_bundle`:
  - `https://news.ycombinator.com/item?id=47633855`
  - GitHub commit 原始链（待补，非阻塞瑕疵）
  - 漏洞详情页（待补，非阻塞瑕疵）
- `视觉建议`: CVE 漏洞截图；Claude Code 使用界面概念图；23年时间线可视化（1999/2001 → 2026 发现）；建议加安全评级徽章视觉
- `为什么适合该平台`: 安全漏洞叙事有强新闻性；跨圈层传播（开发者+科技媒体+安全社区）；微信对技术深度内容友好；「23年漏洞」数字有强传播力
- `delivery_lane`: `day_mainline`
- `publish_mode`: `draft_only`
- `deadline`: `2026-04-05 19:00 CST`

---

### `xiaohongshu`

#### Task 1
- `topic_key`: `anthropic_openclaw_pricing_change`
- `标题候选`: 「Claude Code 订阅要涨价了？Anthropic 宣布对 OpenClaw 额外收费，科技圈炸锅」
- `目标读者`: AI 工具用户、技术爱好者、开发者社区
- `切入角度`: 订阅涨价触发的社区情绪与技术影响分析——不是简单报道价格变动，而是解读这背后的 AI 工具生态变局
- `核心论点`: Anthropic 对 OpenClaw 额外收费不只是商业决策，它揭示了 AI 工具生态走向「封闭平台化」的趋势，开发者社区的实际成本正在悄然上升
- `证据抓手`:
  - TechCrunch 确认报道（Anthropic 官方声明）
  - Reddit r/Claude 高热讨论（Boris Cherny 完整反驳链）
  - 机器之心同步编译
- `source_ref_bundle`:
  - `https://techcrunch.com/2026/04/04/anthropic-says-claude-code-subscribers-will-need-to-pay-extra-for-openclaw-support/`
  - Anthropic 官方定价页（待补，非阻塞瑕疵）
- `视觉建议`: 封面大字「Claude Code 要涨价？」；对话气泡式信息图（Anthropic 声明 vs 开发者反驳）；订阅价格对比表
- `为什么适合该平台`: 小红书用户对「科技工具涨价」话题敏感；社区情绪强适合图文并茂呈现；1000-1500 字短图文节奏友好
- `delivery_lane`: `day_mainline`
- `publish_mode`: `draft_only`
- `deadline`: `2026-04-05 19:00 CST`

#### Task 2
- `topic_key`: `nvidia_robotics_physical_ai`
- `标题候选`: 「NVIDIA 发起全美机器人周，Physical AI 正在成为 2026 年最大变量」
- `目标读者`: 科技爱好者、AI/机器人行业从业者、投资人
- `切入角度`: 美国机器人周时间节点 + NVIDIA 官方背书，Physical AI 不再只是研究课题而是产业方向
- `核心论点`: NVIDIA 借 National Robotics Week 正式把 Physical AI 推到产业前台，结合 CES 2026 以来的趋势，2026 年可能是 Physical AI 从研究走向商业化的转折点
- `证据抓手`:
  - NVIDIA 官方博客原文
  - National Robotics Week 时间节点
  - Physical AI 前沿研究列表
- `source_ref_bundle`:
  - `https://developer.nvidia.com/blog/national-robotics-week-latest-physical-ai-research-breakthroughs-and-research/`
  - 具体研究项目页（待派生，非阻塞瑕疵）
- `视觉建议`: NVIDIA 官方机器人视频截图；Physical AI 应用场景拼图（制造/物流/医疗）；「机器人周」日历视觉；「2026 Physical AI」关键词大字
- `为什么适合该平台`: 小红书对科技前沿话题图文接受度高；机器人视频素材丰富；女性科技用户群对「未来感」内容反应积极
- `delivery_lane`: `day_mainline`
- `publish_mode`: `draft_only`
- `deadline`: `2026-04-05 19:00 CST`

---

### `zhihu`

#### Task 1
- `topic_key`: `anthropic_openclaw_pricing_change`
- `标题候选`: 「Anthropic 对 OpenClaw 额外收费：AI 工具的「平台税」时代来了？」
- `目标读者`: 科技从业者、研究者、对 AI 商业模式有深度兴趣的读者
- `切入角度`: 从 OpenClaw 收费争议延伸到 AI 工具平台的商业模式之争——Anthropic 的选择是个案还是趋势？
- `核心论点`: Anthropic 对 OpenClaw 额外收费，本质上是在 AI coding 工具尚未标准化时抢先建立「平台税」模式，这会倒逼开发者寻找替代方案，同时加速 AI 工具链的开放生态竞争
- `证据抓手`:
  - TechCrunch 确认报道
  - Boris Cherny 等核心开发者的反驳观点
  - OpenClaw 生态背景（第三方工具集成现状）
- `source_ref_bundle`:
  - `https://techcrunch.com/2026/04/04/anthropic-says-claude-code-subscribers-will-need-to-pay-extra-for-openclaw-support/`
  - Reddit r/Claude 相关讨论帖
  - Anthropic 官方定价页（待补，非阻塞瑕疵）
- `视觉建议`: 知乎回答结构（开篇核心观点→证据链→延伸讨论→总结）；逻辑树图（Anthropic 决策影响链）；可配「平台税」概念图
- `为什么适合该平台`: 知乎读者对「趋势分析+商业逻辑」内容有强需求；「平台税」概念有学术讨论空间；适合 3000+ 字深度分析
- `delivery_lane`: `day_mainline`
- `publish_mode`: `draft_only`
- `deadline`: `2026-04-05 19:00 CST`

#### Task 2
- `topic_key`: `openai_852b_post_money_122b_round`
- `标题候选`: 「OpenAI 估值 8520 亿美元意味着什么？拆解 2026 年 AI 融资狂潮的结构逻辑」
- `目标读者`: 科技投资人、金融从业者、对 AI 行业资金动向有关注的读者
- `切入角度`: 巨额融资数字背后的资金结构与行业影响分析——不是简单报道数字，而是拆解为什么资本市场愿意给 OpenAI 这样的估值
- `核心论点`: $122B 融资、$852B 投后估值不仅是 OpenAI 的胜利，它定义了 2026 年 AI 行业资金规模的基准线，所有 AI 创业公司的估值逻辑都在被重新校准
- `证据抓手`:
  - 机器之心 Week 14 周报数据
  - 融资规模横向对比（对比历史大额科技融资）
  - OpenAI 营收/用户数据推测（若有）
- `source_ref_bundle`:
  - `https://www.jiqizhixin.com/articles/2026-04-04`（机器之心 Week 14）
  - 原始新闻链接（待补链，非阻塞瑕疵）
- `视觉建议`: 「$852B」超大字视觉；融资时间线（近三年 AI 大额融资对比表）；资金流向结构图；估值金字塔图示
- `为什么适合该平台`: 知乎投资/金融话题有稳定受众；巨额数字天然引发讨论；适合严肃财务分析类内容
- `delivery_lane`: `day_mainline`
- `publish_mode`: `draft_only`
- `deadline`: `2026-04-05 19:00 CST`

---

### `x`

#### Task 1
- `topic_key`: `anthropic_coefficient_bio_acquisition`
- `标题候选（英文）`: `Anthropic just spent $400M on a biotech startup. This is what AI's vertical expansion actually looks like.`
- `目标读者`: 英语圈科技投资人、AI 行业观察者、biotech 从业者
- `切入角度`: AI 头部公司不再只做通用模型，开始买垂直数据和场景——这是战略布局而非财务投资
- `核心论点`: Anthropic 以 $400M 收购 Coefficient Bio 标志着大模型公司向垂直行业硬件/数据层扩张的时代开启，AI 竞争进入「数据+场景」深水区
- `证据抓手`:
  - TechCrunch 确认报道
  - Coefficient Bio 官网（待派生，非阻塞瑕疵）
  - AI + biotech 赛道背景数据
- `source_ref_bundle`:
  - `https://techcrunch.com/?p=3109242`
- `视觉建议`: 简洁信息图：Anthropic 资金流向图；$400M 收购金额大字视觉；「Vertical Expansion」关键词突出
- `为什么适合该平台`: X/Twitter 对硬数据和战略分析接受度高；$400M 大数字天然适合 tweet thread 结构；AI + biotech 是新兴交叉话题
- `delivery_lane`: `day_mainline`
- `publish_mode`: `draft_only`
- `deadline`: `2026-04-05 19:00 CST`

#### Task 2
- `topic_key`: `claude_code_linux_vulnerability`
- `标题候选（英文）`: `Claude Code found a Linux kernel bug hiding for 23 years. Not in a lab. In production.`
- `目标读者`: 英语开发者社区、安全研究者、科技媒体
- `切入角度`: 23 年漏洞的真实影响——不是夸大，而是解释为什么这个发现对 AI coding 工具的可信度有标志性意义
- `核心论点`: Claude Code 在日常使用中无意发现 Linux 内核 23 年漏洞，不只是 AI coding 的能力证明，更是 AI 在安全审查领域「常态化使用」的拐点信号
- `证据抓手`:
  - HN 头条帖文
  - GitHub Trending 数据
  - CVE 披露信息（待补链，非阻塞瑕疵）
- `source_ref_bundle`:
  - `https://news.ycombinator.com/item?id=47633855`
  - GitHub commit 原始链（待补）
- `视觉建议`: 「23 years」时间线对比图；HN upvote/score 截图；漏洞严重性评级标签
- `为什么适合该平台`: 开发者社区天然关注；security + AI coding 是双重热门话题；适合 5-8 条 tweet thread 结构
- `delivery_lane`: `day_mainline`
- `publish_mode`: `draft_only`
- `deadline`: `2026-04-05 19:00 CST`

---

### `bilibili`

#### Task 1
- `topic_key`: `nvidia_robotics_physical_ai`
- `标题候选`: 「NVIDIA 发起全美机器人周！Physical AI 为何是 2026 年最被低估的技术趋势？」
- `目标读者`: 科技爱好者、大学生、机器人/AI 行业关注者、B站硬核科技用户
- `切入角度`: 机器人周节点科普 + Physical AI 产业前景解读，偏向「为什么你应该关注这个方向」的入门级分析
- `核心论点`: NVIDIA 借机器人周把 Physical AI 从研究圈推向产业圈，这不是单一事件而是 2026 年技术趋势的重要拼图，B站用户应该提前关注这个赛道
- `证据抓手`:
  - NVIDIA 官方博客内容
  - National Robotics Week 活动列表
  - Physical AI 近三年进展概述（可从机器之心 Week 14 补强）
- `source_ref_bundle`:
  - `https://developer.nvidia.com/blog/national-robotics-week-latest-physical-ai-research-breakthroughs-and-research/`
  - 具体研究项目页（待派生，非阻塞瑕疵）
- `视觉建议`: B站视频封面风格——大字标题+ NVIDIA 官方机器人素材；视频内可做 2-3 分钟的 Physical AI 科普；推荐搭配NVIDIA GTC 大会相关视频素材
- `为什么适合该平台`: B站硬核科技用户对机器人/AI前沿有强兴趣；NVIDIA官方素材天然适合视频化；5-10分钟深度视频节奏友好
- `delivery_lane`: `day_mainline`
- `publish_mode`: `draft_only`
- `deadline`: `2026-04-05 19:00 CST`

#### Task 2
- `topic_key`: `anthropic_openclaw_pricing_change`
- `标题候选`: 「Claude Code 订阅要额外收费？Anthropic 这步棋，开发者买不买单」
- `目标读者`: B站科技爱好者、开发者社区、对 AI 工具费用敏感的年轻人群
- `切入角度`: 社区争议 + 普通用户实际影响分析——不是商业分析，而是「这对我有什么影响」的实用解读
- `核心论点`: Anthropic 对 OpenClaw 额外收费，短期内影响的是 Claude Code 重度用户，但从长期看可能重塑整个 AI coding 工具生态的定价逻辑
- `证据抓手`:
  - TechCrunch 报道核心数据
  - Reddit 开发者社区反应（情绪化但真实的用户声音）
  - 机器之心中文编译
- `source_ref_bundle`:
  - `https://techcrunch.com/2026/04/04/anthropic-says-claude-code-subscribers-will-need-to-pay-extra-for-openclaw-support/`
  - Reddit r/Claude 讨论帖（待补链，非阻塞瑕疵）
- `视觉建议`: B站风格——「科技圈热议」切入点；对比「涨价前/涨价后」订阅成本；可引用 2-3 条精选 Reddit 评论截图
- `为什么适合该平台`: B站开发者社区对「AI工具涨价」话题反应强烈；社区情绪内容有高弹幕潜力；10-15分钟视频或图文均适合
- `delivery_lane`: `day_mainline`
- `publish_mode`: `draft_only`
- `deadline`: `2026-04-05 19:00 CST`

---

### `toutiao`

#### Task 1
- `topic_key`: `openai_852b_post_money_122b_round`
- `标题候选`: 「OpenAI 估值 8520 亿美元：一文读懂 2026 年 AI 融资狂潮的底层逻辑」
- `目标读者`: 泛科技读者、财经关注者、对 AI 行业规模有好奇的大众
- `切入角度`: 巨额融资数字背后，AI 行业为什么这么值钱——用通俗语言解释为什么资本市场愿意给 OpenAI 天价估值
- `核心论点`: $122B 融资不是泡沫而是市场对 AI 基础设施价值的重估，$852B 投后估值背后是 AI 在下一个十年重塑所有行业的预期，2026 年是这轮狂潮的关键节点
- `证据抓手`:
  - 机器之心 Week 14 数据
  - 行业横向对比（与苹果/微软历史融资规模对比）
  - OpenAI 营收推测数据（若有）
- `source_ref_bundle`:
  - `https://www.jiqizhixin.com/articles/2026-04-04`
  - 原始新闻链接（待回链，非阻塞瑕疵）
- `视觉建议`: 头条号封面大字「$852B」；信息图——近三年 AI 融资规模趋势；关键数字高亮（122B / 852B）
- `为什么适合该平台`: 今日头条用户对财经/行业规模话题接受度高；大数字标题天然适配头条推荐算法；1500-2500 字节奏符合头条阅读习惯
- `delivery_lane`: `day_mainline`
- `publish_mode`: `draft_only`
- `deadline`: `2026-04-05 19:00 CST`

#### Task 2
- `topic_key`: `anthropic_coefficient_bio_acquisition`
- `标题候选`: 「Anthropic 4 亿美元收购一家 biotech 公司：AI 头部公司「买」未来的逻辑是什么？」
- `目标读者`: 泛科技读者、财经爱好者、对 AI 大公司战略有兴趣的大众
- `切入角度`: 不是报道这笔交易本身，而是分析为什么 AI 头部公司开始「买买买」——这是 AI 竞争的下半场叙事
- `核心论点`: Anthropic $400M 收购 biotech 不是财务投资而是战略卡位，AI 头部公司正在从「卖模型」转向「买场景」，未来 AI 竞争的核心是数据和垂直场景
- `证据抓手`:
  - TechCrunch 确认报道
  - Coefficient Bio 赛道背景（AI + biotech 市场规模）
  - 大公司垂直整合历史案例（可选：Google 收购 DeepMind 对比）
- `source_ref_bundle`:
  - `https://techcrunch.com/?p=3109242`
  - Coefficient Bio 官网（待派生，非阻塞瑕疵）
- `视觉建议`: 头条封面——$400M 大字 + biotech 实验室意象；「AI 公司买未来」概念图；可附大公司垂直整合案例时间线
- `为什么适合该平台`: 今日头条泛科技读者对「AI 大公司战略」话题有稳定兴趣；财经视角解读有推荐优势；$400M 数字有传播力
- `delivery_lane`: `day_mainline`
- `publish_mode`: `draft_only`
- `deadline`: `2026-04-05 19:00 CST`

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **建议立项，优先级顺序如下**
- `理由`: 本包 Top6 中，GLM-5 YC-Bench 和 Claude Code CVE 是当前搜索热度最高的两个话题，有真实用户搜索需求，适合做 SEO 镜像。其余候选百家号适配度偏低（境外 biotech 收购、OpenAI 融资非今日突发、Physical AI 偏向英文源）

**推荐升格顺序**：

| 优先级 | topic_key | 标题方向 | SEO 理由 |
|--------|-----------|---------|---------|
| P1 | `claude_code_linux_vulnerability` | Claude Code 发现 Linux 23 年漏洞（中文版） | CVE 安全漏洞有持续搜索需求，中文科技媒体已有大量编译，SEO 镜像可截流 |
| P2 | `glm5_benchmark_yc_bench` | GLM-5 接近 Claude Opus 4.6（中文版） | 「GLM-5 vs Claude」有搜索需求，但 benchmark 非官方，建议加「社区测试」标注规避风险 |
| 暂缓 | `anthropic_coefficient_bio_acquisition` | Anthropic 4亿美元收购 biotech | 关注度足够但时效性弱于前两者，建议观察今日百度指数后再决定 |

- `承接哪篇主稿更优`: P1 和 P2 均从主稿中文改写，不单独立题；建议 content-writer 写 wechat 稿时同步产出 baijiahao 适配版本

---

## Holdout 清单

> 本轮 premium_pass + 全量 12 槽锁满，以下条目因平台容量约束或适配度考量暂不进入本轮任务单，但均保留候补价值

| topic_key | 标题 | 为什么能进最终池 | 为什么这轮没选 | 什么时候可捞回 |
|-----------|------|----------------|---------------|--------------|
| `zhihu_ai_over_divinized` | 当下的AI是不是被过度神化了？ | 知乎热榜原生，AI泡沫论社会反弹，舆论趋势代表性强 | 一手性=1、数据硬度=1；同话题 morning_flash 刚交付同类；本包已有 zhihu 2 槽且均为高分题 | signal-scout 补强具体知乎观点数据/赞同分布后 |
| `anthropic_pac_political_lobbying` | Anthropic ramps up political activities with new PAC | AI头部公司政治化新叙事，TechCrunch 报道 | 报道深度有限，赛道匹配分偏低（2/3），本包 6 个主战场均已分配更优质候选 | 补强官方声明链 + 更多 PAC 背景后 |
| `gemma_4_kv_cache_fixed` | Gemma 4 KV Cache Bug Fixed | Gemma 4 开发者高热话题，KV cache fix 有技术点击量 | bilibili 2 槽已被 nvidia robotics + anthropic_openclaw 占用；技术细节需回链 GitHub issue | 补强 GitHub issue 链后 |
| `gemma_4_macbook_air_local` | Gemma 4 Runs on MacBook Air 2020 | 终端侧 AI 普及叙事强，破圈苹果用户圈 | xiaohongshu 2 槽已被 anthropic_openclaw + nvidia 占用；需确认具体型号和量级 | 补强原帖具体型号后 |
| `deeptune_series_a_43m` | Deeptune $43M Series A | AI赛道大额A轮，融资信号稳定 | 本包融资题已有 openai_122b 和 anthropic_coefficient_bio 双覆盖，deeptune 信息密度相对偏低 | 派生官网 + 赛道方向补强后 |
| `jump_series_b_80m` | Jump $80M Series B | AI infra 大额B轮，融资信号强 | 同上，赛道方向待补 | 派生官网 + 赛道方向补强后 |
| `apple_self_distillation_code_generation` | Apple Embarrassingly Simple Self-Distillation | Apple 官方 AI 研究首分享，代码生成有开发者价值 | 我们暂无 wechat 槽位，x 2 槽已分配给更高置信候选；Apple 论文尚未派生 | 补强 Apple 官方论文后 |
| `qwen3_6_397b_open_source` | Qwen3.6-397B-A17B 开源呼声 | 阿里是否开源决定高关注，Reddit 真实用户体验 | scorecard 已将其降格为舆情附录，证据链未闭合，无阿里官方表态 | 48h内若有阿里官方回应可立即升级 |
| `dgx_spark_nvfp4_not_delivered` | DGX Spark NVFP4 6个月未交付 | NVIDIA 硬件质量问题有强新闻性，两台机器用户的详细控诉论据链完整 | scorecard 已降格为舆情附录，单一用户声音，证据链不足 | 补强多用户确认或 NVIDIA 回应后 |
| `gemma_4_31b_foodtruck_bench` | Gemma 4 31B FoodTruck Bench 第三名 | Google 开放模型热度延续，社区高热 | scorecard 已降格为舆情附录，且 pack 描述与原帖内容矛盾（差评翻译帖 vs 第三名 benchmark） | signal-scout 确认原帖实际内容方向后 |

---

## 平台任务单 Summary

| 平台 | 任务数 | topic_key(s) | deadline | 备注 |
|------|--------|--------------|----------|------|
| wechat | 2 | `glm5_benchmark_yc_bench`, `claude_code_linux_vulnerability` | 19:00 CST | day_mainline 主力 |
| xiaohongshu | 2 | `anthropic_openclaw_pricing_change`, `nvidia_robotics_physical_ai` | 19:00 CST | 社区情绪+科技前沿双轨 |
| zhihu | 2 | `anthropic_openclaw_pricing_change`, `openai_852b_post_money_122b_round` | 19:00 CST | 平台税分析+融资规模深度 |
| x | 2 | `anthropic_coefficient_bio_acquisition`, `claude_code_linux_vulnerability` | 19:00 CST | 垂直扩张+安全漏洞双语 |
| bilibili | 2 | `nvidia_robotics_physical_ai`, `anthropic_openclaw_pricing_change` | 19:00 CST | 视频化 Physical AI |
| toutiao | 2 | `openai_852b_post_money_122b_round`, `anthropic_coefficient_bio_acquisition` | 19:00 CST | 融资狂潮+AI买未来双轨 |
| **合计** | **12** | Top6 × 2 平台覆盖 | 19:00 CST | premium_pass 完整交付 |

---

## content-writer 优先处理顺序建议

1. **wechat Task 1** (`glm5_benchmark_yc_bench`) — 证据链最完整，数据硬度最高，一级市场视角清晰
2. **wechat Task 2** (`claude_code_linux_vulnerability`) — HN+GitHub 双平台确认，时效强，23年漏洞数字传播力强
3. **x Task 1** (`anthropic_coefficient_bio_acquisition`) — 只需补 Coefficient Bio 官网，非阻塞瑕疵
4. **zhihu Task 1** (`anthropic_openclaw_pricing_change`) — 平台税分析深度强，知乎受众契合
5. **xiaohongshu Task 1** (`anthropic_openclaw_pricing_change`) — 社区情绪高，小红书图文适配
6. 其余 7 个任务槽位按交付节奏跟进

---

## 非阻塞瑕疵跟踪（signal-scout 负责，24h 内跟进）

| topic_key | 待补事项 | 优先级 | 备注 |
|-----------|---------|--------|------|
| `glm5_benchmark_yc_bench` | 回链 arxiv 原始 paper / GitHub leaderboard | P1 | 不阻塞当前任务单 |
| `claude_code_linux_vulnerability` | 回链 GitHub commit / CVE 披露链 | P1 | 不阻塞当前任务单 |
| `anthropic_coefficient_bio_acquisition` | 派生 Coefficient Bio 官网 | P2 | 不阻塞当前任务单 |
| `anthropic_openclaw_pricing_change` | 回链 Anthropic 官方定价页 | P2 | 不阻塞当前任务单 |
| `openai_852b_post_money_122b_round` | 回链原始新闻链接 | P2 | 不阻塞当前任务单 |
| `nvidia_robotics_physical_ai` | 派生具体研究项目页 | P2 | 不阻塞当前任务单 |

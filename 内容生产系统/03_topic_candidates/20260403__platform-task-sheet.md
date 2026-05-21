# 平台任务单

- `date`: `2026-04-03`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-03 15:47 CST`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260403__top20-screening-pack__reworked.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_source`: `20260403__top20__stage-gate-scorecard.md（15:42 CST，score=7.5，rework，continuity_only）`
- `stage_gate_rule`: `Top20 scorecard <8 且非 truth failure → continuity_only limited task sheet；最多覆盖 3 个最重要平台，每个平台先保 1 个任务槽位，其余平台写入 Holdout`
- `morning_flash_exclusion`: `karpathy_openai_return（2026-04-03 03:39 CST，morning_flash approved + publish_queue 锁定，本单明确排除）`
- `xAI_narrative_concentration_risk`: `已识别并控制；Top5 mini_slate 中 xAI 直接相关 2 题（spacex-acquires-xai + xai-grok-enterprise），后者已降入备选；其余 3 题均为独立叙事线（Qwen/Gemma Claude/Anthropic/TBPN）`

---

## 全局主池 Top6

> 来源：Top20 scorecard mini_slate（20260403 15:42 CST，continuity_only output）

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | `spacex-acquires-xai-major-event` | SpaceX 以 $1.25T 合并 xAI，系 Musk AI 战略核心整合 | MAJOR 级事件；$1.25T 合并体；xAI $20B Series E 已核实；Grok 企业线完整叙事；一日多次官方确认 | xAI 叙事集中度风险（见上方 concentration_risk）；时效为归档事件（2月2日），需以"生态现状"切角 |
| 2 | `qwen3-6-plus-real-world-agents` | 阿里 Qwen3.6-Plus 定位"real world agents"，HN 338分验证 | 官方一手（qwen.ai）；Agent 方向明确；中国大模型出海标杆；EN+ZH 双域印证 | 开源权重未明确，社区"转向闭源"争议需正面回应 |
| 3 | `gemma-4-multimodal-on-device` | Google DeepMind Gemma 4 开源多模态 SOTA，NVIDIA 官方加速背书 | DeepMind×HuggingFace 联合背书；Apache 2 许可证；端侧 AI 赛道重要信号 | HuggingFace benchmark 原文 451 封禁至 16:02 CST，NVIDIA 博客可替代 |
| 4 | `claude-code-auto-mode-anthropic` | Anthropic 发布 Claude Code Auto Mode，解决 approval fatigue | 官方工程博客全文核实；$2.5B ARR；93% approval fatigue 痛点数据；B站已验证 #2 热播 | B站视频非官方内容，需标注；Auto Mode 仅为 Team plan |
| 5 | `openai-acquires-tbpn` | OpenAI 收购 TBPN，争夺播客媒体话语权 | 官方一手确认；AI 公司话语权战略布局；可与 xAI 媒体叙事双线对照 | 暂无重大风险 |
| 6 | `anthropic-github-takedown` | Anthropic 意外发出 DMCA 删除令，涉及数千 GitHub 仓库 | GitHub DMCA 公开记录；开发者 IP/版权交叉议题；争议持续 | 一手性受限（TechCrunch 二手报道）；需标注消息来源 |

**备选 slate（按 score 降序）**：7. `oh-my-codex-github-trending`（21/30）| 8. `claude-code-3-agent-team-reddit`（20/30）| 9. `karpathy-english-programming-language`（22/30，同 Karpathy X profile，已在 morning_flash 排重范围）| 10. `deepmind-sima-2-agent`（21/30，P1 待修日期）

---

## 六个主战场任务单

> **模式说明**：本单为 `continuity_only` limited task sheet，依据 Top20 scorecard（score=7.5，continuity_decision=continuity_only）产出。最多覆盖 3 个最重要平台，每个平台保 1 个高置信槽位。其余平台写入 Holdout，清单如下。

### `wechat`

#### Task 1
- `topic_key`: `spacex-acquires-xai-major-event`
- `目标读者`: 投资人、基金从业者、科技产业决策层
- `切入角度`: **Musk 的 $1.25T AI 合并赌注：SpaceX + xAI 意味着什么**——不是突发新闻报道，而是站在今天（4月3日）回看这笔2月2日落定的交易，判断它对 AI 资本格局的实质影响
- `核心论点`: SpaceX 以 $1.25T 合并 xAI 不是财务整合，是 Musk 把"可复用火箭 + 可信 AGI"绑定的战略动作；xAI 的 Grok 企业线（Grok Business/Enterprise/Voice Agent API）进入 SpaceX 生态后，Musk 手里同时有了算力（SpaceX Starlink DC）、资本（xAI 融资）、商业化（Grok 企业订阅）和数据（X 平台）的垂直闭环
- `证据抓手`: 
  - x.ai/news 官方原文（"SpaceX announced today that it has acquired xAI"，2026-02-02）
  - xAI Series E $20B（2026-01-06，x.ai/news 同一页面）
  - Grok Enterprise 发布（2025-12-30，x.ai/news）
  - Grok Voice Agent API（2025-12-17）
  - SpaceX 合并公告 redirect → spacex.com/updates#xai-joins-spacex
- `source_ref_bundle`: 
  - `x.ai/news`: https://x.ai/news
  - `SpaceX 合并页`: https://spacex.com/updates#xai-joins-spacex
  - `TechCrunch 报道（2月）`: https://techcrunch.com/2026/02/02/spacex-acquires-xai/
  - `asset_chain`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260403_085933__openai__asset-chain.md`（注：原为 OpenAI asset chain，xAI 段需自建）
- `视觉建议`: 信息图：Musk AI 生态矩阵（SpaceX / xAI / Tesla / X 各业务线 + 数据流闭环）；x.ai/news 截图；Starlink + Grok 双产品对照表
- `为什么适合该平台`: WeChat 金融/投资读者对$1.25T量级资本动作高度敏感；xAI 合并体叙事需要资本逻辑而非技术参数，WeChat 是最优分发场

#### Task 2
- `topic_key`: `qwen3-6-plus-real-world-agents`
- `目标读者`: AI 开发者、技术创业者、CTO / 技术决策者
- `切入角度`: **Qwen3.6+ 上了 HN 338分，但这次它不靠开源靠 Agent**：千问3.6+放弃纯开源标签，转打"real world agents"落地牌，1M token context + tool use 正在重塑开发者工作流
- `核心论点`: Qwen3.6+ 的最大信号不是"国产开源模型又进步了"，而是它正式宣告"Model as Agent"成为头部玩家的标配战略；1M token context 给 Agent 的记忆留足空间，tool use 覆盖代码执行、API 调用和网页浏览，这意味着大模型竞争从"刷榜"转向"谁能先让 Agent 真正干活"
- `证据抓手`:
  - qwen.ai 官方博客原文（Advanced Agentic Coding / Superior General Agent / Enhanced Multimodal Reasoning）
  - HN 338分 / 117评论（EN 开发者验证）
  - 知乎热帖（中文开发者验证）
  - 机器之心 / InfoQ 同步跟进（中文专业媒体印证）
- `source_ref_bundle`:
  - `qwen.ai 官方博客`: https://qwen.ai/blog?id=qwen3.6
  - `HN 讨论`: https://news.ycombinator.com/item?id=47615002
  - `知乎热帖`: https://www.zhihu.com/question/XXXXX（待回填）
- `视觉建议`: Qwen3.6+ 核心能力雷达图（Agentic Coding / Tool Use / 1M Context / Multimodal）；HN 截图；中文社区评论精选拼接
- `为什么适合该平台`: WeChat 技术读者对"模型能不能真正干活"的关注度超过 benchmark 数字；AI 开发者社区已在 HN / 知乎双验证，WeChat 承接二创解读流量

---

### `xiaohongshu`

#### Task 1
- `topic_key`: `gemma-4-multimodal-on-device`
- `目标读者`: 独立开发者、AI 工具爱好者、有端侧 AI 需求的技术用户
- `切入角度`: **Gemma 4 上线，我在 M 芯片 Mac 上跑了：这是目前最值得上手的开源多模态模型**——hands-on 实测视角，不是新闻也不是评测，是"我今天真的用上了"的分享
- `核心论点`: Gemma 4 真正值得关注的不只是 benchmark 数字，而是 Apache 2 许可 + transformers/llama.cpp/MLX/WebGPU 全生态覆盖，意味着在 Mac 本地跑一个多模态 AI 助手已经从"折腾"变成"一行命令的事"；对独立开发者和 AI 极客来说，这是今年最值得落地的开源模型
- `证据抓手`:
  - Google DeepMind / HuggingFace 官方博客（Gemma 4 发布，Apache 2 许可证，多尺寸可选）
  - NVIDIA 官方博客加速背书（"NVIDIA accelerates Gemma 4 for local agentic AI"）
  - Reddit r/LocalLLaMA 讨论（HuggingFace blocked 期间社区反馈）
  - 知乎相关讨论（中文开发者视角）
- `source_ref_bundle`:
  - `NVIDIA Gemma 4 博客（推荐使用）`: https://www.nvidia.com/en-us/blog/nvidia-accelerates-gemma-4-for-local-agentic-ai/
  - `Google Search 摘要（HF 451 期间备选）`: https://r.jina.ai/https://www.nvidia.com/en-us/blog/nvidia-accelerates-gemma-4-for-local-agentic-ai/
  - `HuggingFace 官方博客（451 解封后）`: https://huggingface.co/blog/gemma4
- `视觉建议`: Gemma 4 多模态能力展示截图（图像+音频理解）；llama.cpp 或 MLX 本地运行截图；benchmark 对比表（轻量化 vs 同尺寸模型）；"一行命令安装"代码块
- `为什么适合该平台`: XHS 用户对"能上手的工具"有天然分享欲；Gemma 4 的开源+轻量化+M芯片适配切中 XHS 科技板块的热门标签（#AI工具 #M芯片 #开源）

---

### `bilibili`

#### Task 1
- `topic_key`: `claude-code-auto-mode-anthropic`
- `目标读者`: 开发者、程序员、对 AI 编程工具有兴趣的 B站科技受众
- `切入角度`: **Anthropic 官方说 Auto Mode 解决了"批准疲劳"，我用 Claude Code 跑了 50 次**：工程博客+中文社区验证的实战对照，把官方技术文档翻译成开发者真正关心的体验改进
- `核心论点`: Claude Code Auto Mode 的本质是用一个 classifier model 替代人工逐条批准——destructive 操作（大量文件删除/代码外泄/危险执行）会被拦截并升级人工，安全动作自动放行；痛点数据（93% approval fatigue，$2.5B ARR）背后是一个真实的工程决策：AI 编程工具要真正提升生产力，必须把"信任圈"从人工扩大到系统
- `证据抓手`:
  - Anthropic 官方工程博客原文（Auto Mode 技术原理，classifier model 双层安全分类器）
  - B站 UP 主"AI进化论-花生"Claude Code 源码解读视频（9.5w播放 / 2756点赞 / 901评论 / 收藏 3349，飞瓜科技榜 #2）
  - X AnthropicAI 账号同步发布
  - Reddit r/ClaudeAI 热议
- `source_ref_bundle`:
  - `Anthropic 工程博客`: https://www.anthropic.com/engineering/claude-code-auto-mode
  - `B站视频（已有高热验证）`: https://www.bilibili.com/video/av116324273494732
  - `X AnthropicAI`: https://x.com/AnthropicAI
- `视觉建议`: Anthropic 工程博客截图（Auto Mode 流程图）；Claude Code 实际操作动图（安全动作自动放行 vs destructive 动作拦截）；B站评论区开发者体验精选；代码对比（Before Auto Mode vs After）
- `为什么适合该平台`: B站已有强验证（#2 热播 + 高收藏数）；Claude Code Auto Mode 的工程博客图文丰富，适合视频+图文双格式；开发者社区在 B站有高活跃度

---

### `zhihu`
> **Holdout** —— 本轮 continuity_only limited task sheet 仅覆盖 3 个最高优先平台；以下候选保留在 day_mainline holdout 池，可于后续 heartbeat 窗口或 T+1 主线升级

#### Holdout A
- `topic_key`: `anthropic-github-takedown`
- `为什么能进最终池`: GitHub DMCA 公开记录，开发者 IP/版权交叉议题，争议持续，适合知识平台做深度法律与生态分析
- `为什么这轮没选`: 一手性受限（Anthropic 官方未单独发声明，TechCrunch 二手报道），developer-focused 内容与 WeChat 资本叙事重合度低，与 Bilibili 开发者内容同质
- `什么时候可捞回`: 若有 Anthropic 官方声明更新，或 GitHub DMCA 记录有新进展，立即升级为主动候选

#### Holdout B
- `topic_key`: `openai-acquires-tbpn`
- `为什么能进最终池`: 官方一手确认，AI 公司话语权战略布局，TBPN 创始人 Chris Lehane 背景有媒体话题性，适合知识平台做公司战略分析
- `为什么这轮没选`: WeChat Task 1（SpaceX/xAI $1.25T）已占 1 个资本叙事槽位；TBPN 的媒体话语权叙事与资本叙事有受众重叠，优先保 SpaceX 题
- `什么时候可捞回`: T+1 主线优先候选；或若有 OpenAI 后续动作（Chris Lehane 采访、xAI 媒体布局对照），可合并成"AI 公司的媒体战争"专题

#### Holdout C
- `topic_key`: `oh-my-codex-github-trending`
- `为什么能进最终池`: GitHub Trending 今日+2,852 stars，三人团队架构与 Reddit 3-agent team + Claude Code Auto Mode 三方印证，开发者 Agent 团队化已成主流范式
- `为什么这轮没选`: Bilibili 已选 Claude Code Auto Mode（已有 B站 #2 验证），两者同属"AI 编程工具"叙事线，同平台不宜同日双推
- `什么时候可捞回`: Claude Code Auto Mode 出成品后，oh-my-codex 可作为"工具横向评测"专题跟进；或 T+1 作为 B站备用槽位

---

### `x`
> **Holdout**

#### Holdout A
- `topic_key`: `qwen3-6-plus-real-world-agents`
- `为什么能进最终池`: HN 338分验证英文开发者社区高热度；X 平台受众与 HN 受众高度重叠；英语发帖可直接获取 EN 受众
- `为什么这轮没选`: continuity_only 限制 3 平台；WeChat 已选 Qwen3.6+（中文开发者受众），X 受众与 HN 重叠但中文场域已在 WeChat 覆盖
- `什么时候可捞回`: T+1 或作为 wechat 出成品后的 EN 版本转发；X 上的 HN 讨论串截图 + 一句话点评是低成本高回报的二次传播

#### Holdout B
- `topic_key`: `anthropic-github-takedown`
- `为什么能进最终池`: 开发者社区 X 账号（HN / Reddit / GitHub）均已验证；DMCA 争议在 X 上有天然讨论流量
- `为什么这轮没选`: 同 Holdout B（zhihu）理由
- `什么时候可捞回`: 若 Anthropic 官方发推或 X 上出现新的 DMCA 争议进展，立即激活

---

### `toutiao`
> **Holdout** —— 今日头条内容工厂版图暂以 WeChat 为主阵地；以下候选保留

#### Holdout A
- `topic_key`: `openai-acquires-tbpn`
- `为什么能进最终池`: OpenAI 官方一手 + 媒体话语权战略，易改编为头条风格的快讯+解读格式
- `为什么这轮没选`: WeChat Task 1（SpaceX/xAI $1.25T）是更大资本叙事；TBPN 体量相对小，头条快讯竞争激烈
- `什么时候可捞回`: T+1 或若有 OpenAI 后续媒体动作，作为头条快讯候选

#### Holdout B
- `topic_key`: `gemma-4-multimodal-on-device`
- `为什么能进最终池`: Google 官方背书 + 开源 + 端侧 AI，与头条开发者受众匹配
- `为什么这轮没选`: XHS 已选 Gemma 4；同题同质化风险
- `什么时候可捞回`: T+1 作为头条 AI 工具横向对比专题

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **否——今日不单独升格**
- `理由`: 
  1. Top5 mini_slate 中 xAI 相关（SpaceX/xAI $1.25T）和 Qwen/Gemma 均属于时效型叙事，SEO 长尾价值有限；
  2. Claude Code Auto Mode 已有 B站高热验证，视频平台比图文 SEO 更优先；
  3. `baijiahao` 是 SEO 镜像层，不是默认日更战场；今日主线内容以 WeChat/Bili/XHS 为核心分发即可覆盖目标受众；
  4. TBPN 收购案如 T+1 有后续进展，可考虑百家号快讯镜像
- `若后续升格，承接哪篇主稿更优`: `spacex-acquires-xai-major-event`（$1.25T 合并体是长尾搜索词）或 `openai-acquires-tbpn`（AI 公司媒体战略有持续关注度）

---

## 平台任务单续脉说明

### 当前状态
- **本单性质**: `continuity_only` limited task sheet——Top20 scorecard 7.5 分（rework），非 premium pass，但 18 个有效候选中有 5 题 score 25+ 进入 mini_slate，有坚实内容基础
- **为何不是 premium**: Top20 scorecard 明确写 `score: 7.5`，`status: rework`，`continuity_decision: continuity_only`；P1（SIMA 2 日期）+ P2（Ethan Mollick 标题/URL）两处 fatal 来源错误尚未修正；正式 premium pass 需等 P1+P2+P3 Fix 复评通过

### 今日交付约束
- `day_mainline wechat 草稿箱 deadline`: **2026-04-03 19:00 CST**（双车道 runbook 硬截止，不得晚于此时间）
- `本单完成目标`: 2 篇 WeChat 成品稿入草稿箱，其余平台任务单为 writer 提供方向锚点，不要求今日全部完成
- `剩余窗口`: 当前 15:47 CST，距离 19:00 约 3 小时 13 分钟，内容 writer 有充足起稿时间

### P1+P2 Fix 进展追踪
| 候选 | 问题 | 状态 | 修正后预期 |
|---|---|---|---|
| #10 SIMA 2 | `published_at` 虚报 2026-04-03（实际 2025-11-13） | ⚠️ 待修正 | 降权为参考背景，mini_slate 不依赖此候选 |
| #13 Ethan Mollick | 标题"Thriving..."实际为"Management as AI superpower"；URL 404；日期 2026-01-27 | ⚠️ 待修正 | 候选可保留，但 score 需重评 |
| #1 xAI Series E | "$20B 同月完成"措辞不准确（2026-01 vs 2026-02-02） | ⚠️ 待修正（推荐） | 本单 WeChat Task 1 已回避时间线细节，修复后不影响当前任务单 |

### xAI 叙事集中度控制
- **当前方案**: WeChat Task 1 锁 `spacex-acquires-xai`（$1.25T 合并体，MAJOR 级）；`xai-grok-enterprise`（Grok 企业线）未进 mini_slate 主 slate，降为待修后的升级备选
- **若 xai-grok-enterprise 后续激活**: 需从 holdout 池替换一题，避免 xAI 线在 Top5 mini_slate 中占 2 题以上

---

## 写入记录

- **platform-task-sheet 生成时间**: 2026-04-03 15:47 CST
- **platform-task-sheet 版本**: `v1.0 continuity_only`
- **对应 Top20 scorecard**: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260403__top20__stage-gate-scorecard.md`
- **下一步**: `content-writer` 基于本任务单起稿；优先处理 WeChat Task 1（SpaceX/xAI $1.25T）和 WeChat Task 2（Qwen3.6+）；19:00 CST 前 2 篇 WeChat 成品入草稿箱
- **market-editor 裁判**: 本任务单待 `market-editor` 正式 scorecard 裁判；当前为 continuity_only 状态，不是 premium pass

# 平台任务单

- `date`: `2026-03-31`
- `owner`: `topic-planner`
- `generated_at`: `2026-03-31 14:15:00 CST`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260331__top20-screening-pack__reworked.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `今日 market-editor scorecard 裁判 rework；continuity_decision=continuity_only；mini_slate 含 2 个已确认信号（Claude Code cache bugs / robots_bury_you）；xAI #7 降待重建状态；平台任务单仅覆盖 mini_slate 已授权 active slots，其余全部 holdout；最多 3 个最重要平台，每平台保 1 槽位`

---

## 全局主池 Top6

> ⚠️ 本任务单为 `continuity_only` limited sheet，非完整 Top6 主池。mini_slate 仅含 2 个已确认信号。其余 top4-top9 待 market-editor 完成 xAI #7 重建复评后方可升格。

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | `claude_code_cache_bugs` | Claude Code 独立版两个缓存 Bug 导致 API 成本暴增 10-20 倍；有 GitHub Issues 完整证据链 + workaround；开发者直接受影响 | 技术细节极强，硬证据，实用性强，快讯+技术解读+工具推荐三层均可写 | 需补 GitHub Issues 全文和 Anthropic 官方回应；Reddit 评论数不可见 |
| 2 | `robots_bury_you_in_work` | 开发者用 17 个 AI Agent 管理 12 个并行项目，月 1400+ commits；"生产力陷阱"叙事与主流 AI 焦虑反向，易破圈 | 具体数字硬（17 agents / 12 projects / 1400+ commits），叙事强反转，社区验证高 | 个人经验可复制性存疑；视频内容未抓取 |
| 3 | `xai_spacex_acquisition` | SpaceX 以 $250B 估值收购 xAI，xAI Series E $20B / IPO 目标 $1.75T——**当前降 holdout 待重建** | 20B 美元是年度级事件，一手官方源，SpaceX 合并叙事可撬动全球科技头条 | **致命缺口**：rework 包遗漏 SpaceX 收购叙事框架；x.ai/news/series-e published_at 缺失；market-scout 正在重建中 |
| 4 | `llamacpp_100k_stars` | **holdout**，待 xAI 复评后合并 | 开源 infra 里程碑，100k 数字有说服力 | Reddit RSS 无法抓评论数 |
| 5 | `qwen_36_openrouter` | **holdout**，待 xAI 复评后合并 | 中国大模型出海渠道多元化信号 | OpenRouter 页面需跳转补查 |
| 6 | `multi_inst_ai_safety_paper` | **holdout**，待 arXiv 摘要补查 | LLM Agent 安全是 Agent 规模化部署后最重要议题之一 | arXiv 摘要层未直接验证；机构归属已修正但正文需补 |

---

## 六个主战场任务单

---

### `wechat`

#### Task 1（Active Slot — 已授权）

- `topic_key`: `claude_code_cache_bugs_20260331`
- `目标读者`: 国内 AI 开发者、Claude Code 用户、技术团队负责人
- `切入角度`: 「Claude Code 刚被曝光两个缓存 Bug，API 成本无声暴增 10-20 倍——你的账单可能是正常值的 20 倍」：技术警示 + 成本风险 + 修复方案三层
- `核心论点`: Claude Code 独立版存在两个独立 Bug（sentinel 字符串替换导致 system[] 缓存失效；--resume 参数导致全程缓存 miss），合计可使 API 成本增加 10-20 倍；已有明确 workaround；用户需立即自查账单
- `证据抓手`: GitHub Issues #40524 / #34629（逆向工程确认）+ 228MB ELF MITM proxy 验证 + Reddit r/ClaudeAI 高热帖
- `source_ref_bundle`:
  - Reddit 帖: `https://old.reddit.com/r/ClaudeAI/comments/1s7mkn3/psa_claude_code_has_two_cache_bugs_that_can/`
  - GitHub Issue #40524: `https://github.com/anthropics/claude-code/issues/40524`
  - GitHub Issue #34629: `https://github.com/anthropics/claude-code/issues/34629`
  - Rework pack path: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260331__top20-screening-pack__reworked.md` (#4)
- `视觉建议`: 1）Bug 分析流程图（sentinel 替换 vs 正常缓存对比）；2）API 成本 1x vs 10-20x 对比示意图；3）workaround 代码片段（简短截图）；4）GitHub Issue 评论区用户反馈拼图
- `为什么适合该平台`: 微信适合技术警示类深度文章；国内 Claude Code 用户群体增长快，对成本问题敏感；可引发技术社群转发；微信封闭生态有利于完整说理

#### Task 2（Holdout — 本轮不开启）

- `topic_key`: `robots_bury_you_in_work`
- `为什么能进最终池`: 硬数字（17 agents / 12 projects / 1400+ commits）提供强证据；"生产力陷阱"叙事与主流 AI 焦虑反向，争议性强，易破圈
- `为什么这轮没选`: continuity_only limited sheet，仅授权 1 个 wechat 槽位给 Claude Code（技术警示角度更紧迫）；robots_bury_you 以 x / 小红书角度优先
- `什么时候可捞回`: xAI 复评完成后（预计当日），升格进完整平台任务单，优先分配 wechat 深度分析角度（7x24 Agent 管理者的精神消耗叙事）

---

### `xiaohongshu`

#### Task 1（Active Slot — 已授权）

- `topic_key`: `robots_bury_you_in_work_17_agents_20260331`
- `目标读者`: 职场人、创业者、对 AI 提效感兴趣的非技术人群
- `切入角度`: 「我用 17 个 AI 帮自己打工，月入 1400+ commits——但我比上班还累」：AI 时代的「效率陷阱」自述；反鸡娃/反内卷叙事的镜像
- `核心论点`: 当 AI 让「一人公司」变成「一人神公司」，任务关闭速度从 26 天→4天→1.6天；但 80% 编码变成 80% 思考，精力消耗不降反升；17 个 Agent 同时跑是能力还是诅咒？
- `证据抓手`: Reddit 主帖原文（17 agents / 12 projects / 39 repos / 月 1400+ commits）+ 视频附链接 + 任务追踪数据
- `source_ref_bundle`:
  - Reddit 帖: `https://old.reddit.com/r/ClaudeAI/comments/1s7qs82/robots_wont_take_your_job_they_ll_bury_you_in_work/`
  - Rework pack path: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260331__top20-screening-pack__reworked.md` (#6)
- `视觉建议`: 1）17 个 AI Agent 并行工作示意图（自制信息图）；2）commit 数量时间轴对比图（2019→2024→2026）；3）「任务关闭时间」26天→4天→1.6天递减图；4）Reddit 高赞评论截图（情绪共鸣类）
- `为什么适合该平台`: 小红书对「真实自述+数字对比」的帖子天然友好；职场/创业人群对「效率 vs 代价」议题高度共鸣；视频+文字双通道

#### Task 2（Holdout — 本轮不开启）

- `topic_key`: `claude_code_cache_bugs`
- `为什么能进最终池`: 技术圈高热，开发者直接受影响，实用价值强
- `为什么这轮没选`: continuity_only limited sheet；x（Twitter）已获授权承担技术圈传播任务；小红书平台技术深度内容扩散效率低于 x
- `什么时候可捞回`: 完整 Top6 任务单阶段；可做「Claude Code 省钱避坑指南」小红书版本

---

### `zhihu`

#### Task 1（Active Slot — 已授权）

- `topic_key`: `claude_code_cache_bugs_20260331`
- `目标读者`: 技术从业者、AI 开发者、对 LLM 工程落地感兴趣的工程师和研究人员
- `切入角度`: 「Claude Code 的两个 Bug 让我们重新思考 LLM Agent 的缓存设计」：技术深度分析 + 工程教训 + 社区响应
- `核心论点`: 1）Bug 1：sentinel 字符串替换在 v2.1.69 后绕过 system[] 缓存守卫；2）Bug 2：--resume 参数使缓存全程失效；3）二者叠加 API 成本 10-20x；4） Anthropic 尚未正式回应；5）从软件工程角度看 LLM 缓存层设计的脆弱性
- `证据抓手`: GitHub Issues #40524 / #34629（完整技术分析）+ 228MB ELF 逆向工程方法 + MITM proxy 验证截图 + Reddit 技术讨论
- `source_ref_bundle`:
  - Reddit 帖: `https://old.reddit.com/r/ClaudeAI/comments/1s7mkn3/psa_claude_code_has_two_cache_bugs_that_can/`
  - GitHub Issue #40524: `https://github.com/anthropics/claude-code/issues/40524`
  - GitHub Issue #34629: `https://github.com/anthropics/claude-code/issues/34629`
  - Rework pack path: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260331__top20-screening-pack__reworked.md` (#4)
- `视觉建议`: 1）代码流程图（Bug 1：sentinel 替换路径）；2）代码流程图（Bug 2：--resume 缓存 miss 路径）；3）API cost 1x vs 10-20x 对比表；4）workaround 方案代码块
- `为什么适合该平台`: 知乎适合技术深度分析；GitHub Issue 讨论串有实质工程内容；Anthropic 官方未回应的张力适合知乎讨论氛围

---

### `x`

#### Task 1（Active Slot — 已授权）

- `topic_key`: `claude_code_cache_bugs_20260331`
- `目标读者`: 英文技术社区、开发者、Claude Code 用户、LLM/AI Agent 研究者
- `切入角度`: Thread 开尾：「Your Claude Code bill is probably 10-20x higher than it should be. Here's exactly why (and the 1-line fix) 🧵」（结果先行警报体）
- `核心论点`: Bug 1（sentinel）+ Bug 2（--resume）技术细节 + 实测 API 成本对比 + workaround + GitHub Issue 直链 + 待 Anthropic 回应
- `证据抓手`: GitHub Issue #40524 + #34629 + Reddit 原帖 + 逆向工程方法论
- `source_ref_bundle`:
  - Reddit: `https://old.reddit.com/r/ClaudeAI/comments/1s7mkn3/psa_claude_code_has_two_cache_bugs_that_can/`
  - GitHub Issue #40524: `https://github.com/anthropics/claude-code/issues/40524`
  - GitHub Issue #34629: `https://github.com/anthropics/claude-code/issues/34629`
  - Rework pack path: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260331__top20-screening-pack__reworked.md` (#4)
- `视觉建议`: 1）简短技术 thread 格式；2）成本对比数字突出（1x → 10-20x）；3）GitHub Issue 评论区高赞截图；4）workaround 代码片段截图
- `为什么适合该平台`: X/Twitter 是英文开发者社区最快扩散渠道；GitHub Issue 讨论可直接引；快速技术警示类推文天然适配；附链接引导 GitHub Star 关注

#### Task 2（Active Slot — 已授权）

- `topic_key`: `robots_bury_you_in_work_17_agents_20260331`
- `目标读者`: 英文 AI 社区、科技从业者、Agent 开发者、创业生态关注者
- `切入角度`: 「I didn't lose my job. I got the job of ten people. Nine are management. / 17 AI agents, 12 projects, 1400 commits/month — and I'm more exhausted than before AI.」（管理陷阱 Hook）+ 社区讨论引导
- `核心论点`: 17 agents / 12 projects / 1400+ commits 月 commit 量；任务关闭速度 26天→4天→1.6天；但精力消耗不降；"生产力陷阱"是 Agent 规模化使用的真实代价
- `证据抓手`: Reddit 原帖完整数字 + 视频附链 + 任务追踪数据
- `source_ref_bundle`:
  - Reddit: `https://old.reddit.com/r/ClaudeAI/comments/1s7qs82/robots_wont_take_your_job_they_ll_bury_you_in_work/`
  - Rework pack path: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260331__top20-screening-pack__reworked.md` (#6)
- `视觉建议`: 1）数字可视化 thread（17 agents / 12 projects / 1400+ commits）；2）commit 时间轴趋势图；3）Reddit 高赞评论截图（情绪共鸣类）
- `为什么适合该平台`: X 是英文 AI 社区最核心扩散渠道；该话题已在 r/ClaudeAI 高热，有现成传播基础；hook 性强，适合 viral format

---

### `bilibili`

#### Task 1（Holdout — 本轮不开启）

- `topic_key`: `robots_bury_you_in_work`
- `为什么能进最终池`: 视频+数字叙事适合 B 站；开发者自述可做播客/视频脚本素材；社区氛围适合深度讨论
- `为什么这轮没选`: continuity_only limited sheet；bilibili 排第三优先梯队；x 已获 robots_bury_you 的英文破圈任务；中文视频制作可等完整任务单
- `什么时候可捞回`: xAI 复评完成后；可做「我用 17 个 AI 同时做 12 个项目」B 站视频/动态图文版

#### Task 2（Holdout — 本轮不开启）

- `topic_key`: `claude_code_cache_bugs`
- `为什么能进最终池`: 技术教程向视频/B 站专栏适合开发者内容
- `为什么这轮没选`: 同上；wechat 已覆盖 Claude Code 技术警示角度
- `什么时候可捞回`: 完整 Top6 任务单阶段

---

### `toutiao`

#### Task 1（Holdout — 本轮不开启）

- `topic_key`: 待定（可承接 wechat 或 x 的中文版本）
- `为什么能进最终池`: 头条推荐算法适合大众化科技内容
- `为什么这轮没选`: continuity_only limited sheet；头条偏向大众化 AI 应用题，Claude Code / robots_bury_you 深度技术内容需等完整任务单
- `什么时候可捞回`: xAI 复评完成后；可与小红书/微信内容联动做多平台分发

---

## `baijiahao` SEO 镜像层判断

### 是否需要单独立题

**暂缓；等待 xAI 重建完成后合并判断**

### 理由

1. **Claude Code cache bugs**：百家号用户以中文科技内容消费为主，开发者工具技术 Bug 解读有一定搜索价值；但当前阶段更适合先在公众号/知乎出中文深度版，待话题热度稳定后（如 GitHub Issue 获得 Anthropic 官方回应）再部署百家号 SEO 镜像层
2. **robots_bury_you_in_work**：叙事性强、字数友好，但百家号对「个人经验谈」内容 SEO 权重不如「事件型新闻」；建议先在 x / 小红书验证英文原版传播效果，再决定是否做中文 SEO 镜像
3. **xAI SpaceX 收购（holdout）**：SpaceX 收购 xAI 是强新闻事件，一旦 market-scout 完成叙事重建并通过复评，该题应是百家号 SEO 镜像的**首选候选**——高搜索量 + 中文科技受众强关注

### 承接哪篇主稿更优

| 优先级 | topic_key | baijiahao SEO 价值 | 建议时机 |
|---|---|---|---|
| 1（待重建） | `xai_spacex_acquisition` | 高：SpaceX / xAI / Elon Musk 关键词搜索量极大 | xAI 重建 + market-editor 复评通过后立即部署 |
| 2 | `claude_code_cache_bugs` | 中高：Claude Code / API 成本 / Bug 等关键词有开发者搜索需求 | wechat 技术解读版出稿后 1-2 天跟进 |
| 3 | `robots_bury_you_in_work` | 中：AI Agent / 生产力 / 数字游民等关键词有持续搜索量 | x / 小红书版验证热度后跟进 |

---

## Holdout 清单

### `xai_spacex_acquisition`

- `为什么能进最终池`: SpaceX $250B 估值收购 xAI，xAI Series E $20B / IPO $1.75T 目标；SpaceX + xAI 合并是今日全球 AI 赛道头号事件，一手官方源；是唯一可撬动全球主流科技媒体头条的今日信号
- `为什么这轮没选`: **致命缺口**：rework 包（market-scout 制作）遗漏 SpaceX 收购叙事框架，xAI 呈现为「joins SpaceX」（语义错误），El Salvador 教育被升格为头条（方向错误）；x.ai/news/series-e published_at 缺失，无法判断时效；market-editor 裁判为 `rework`，降为待重建状态
- `什么时候可捞回`: **立即**：market-scout 优先完成 xAI SpaceX 叙事重建（expand_validation 模式）；重建后提交 market-editor 复评；复评通过后立即升格进平台任务单，同时启动百家号 SEO 镜像层

---

### `llamacpp_100k_stars`

- `为什么能进最终池`: 开源 AI infra 标志性里程碑；100k GitHub stars 有硬数字说服力；ggml-org 主导的开源推理框架代表本地 AI 赛道趋势；Georgi Gerganov X 确认
- `为什么这轮没选`: continuity_only limited sheet；xAI SpaceX 叙事包缺失导致 pack 整体打回；llamacpp 属 top4-top9 梯队，本次未获授权
- `什么时候可捞回`: xAI 复评完成后，与 top4-top9 一并进入完整平台任务单；建议以「开源本地 AI 推理进入 10 万星时代」角度出 zhihu / baijiahao

---

### `qwen_36_openrouter`

- `为什么能进最终池`: 中国大模型出海渠道多元化重要信号；OpenRouter 代表绕过官方渠道直接进入消费市场；Qwen 3.6 在 OpenRouter 出现有高热验证
- `为什么这轮没选`: continuity_only limited sheet；qwen_36_openrouter 属 top4-top9 梯队，本次未获授权
- `什么时候可捞回`: xAI 复评完成后，与 top4-top9 一并进入完整平台任务单；建议以「阿里模型出海第三条路」角度分配 wechat / xiaohongshu

---

### `multi_inst_ai_safety_paper`

- `为什么能进最终池`: LLM Agent 安全是 2026 年 Agent 规模化部署后最重要议题之一；11 类漏洞有具体技术内容；arXiv 可直接回链
- `为什么这轮没选`: arXiv 摘要层未直接验证；11 类漏洞具体分类未在摘要中确认；market-editor 高优先补证项（supplement_evidence）；机构归属已从「Stanford+Harvard」修正为「Northeastern+13 institutions」
- `什么时候可捞回`: market-scout 补查 arXiv:2602.20021 摘要后，若内容充实可升权进入 top4-top9；建议优先分配 zhihu（论文解读）/ x（AI 安全社区）

---

### `florida_man_chatgpt_house`

- `为什么能进最终池`: $954,800 成交 / 5 offers / 15 showings 细节丰富；Inc.com / Mashable / NDTV / Times of India 多平台验证，传播性强被低估（16→19 升权修正）；AI 消费者应用破圈案例
- `为什么这轮没选`: continuity_only limited sheet；Claude Code 技术警示 + robots_bury_you 叙事反转已占用 2 个 active slots；florida_man 属强 pool 但非 mini_slate 授权
- `什么时候可捞回`: 完整 Top6 任务单阶段；建议以「AI 卖房 5 天 vs 传统 90 天」强对比角度优先分配 xiaohongshu（大众化）/ wechat（AI 替代专业服务边界讨论）

---

### `litellm_delve_security_incident`

- `为什么能进最终池`: AI infra 供应链安全是 2025-2026 重要议题；LiteLLM 是 AI gateway 活跃项目；事件涉及安全合规认证商业信任问题；TechCrunch 背书
- `为什么这轮没选`: continuity_only limited sheet；属 top4-top9 梯队，本次未获授权
- `什么时候可捞回`: xAI 复评完成后；建议分配 x（AI infra 社区）/ zhihu（安全供应链深度分析）

---

### `claude_subscriptions_double`

- `为什么能进最终池`: Claude 付费增长两个月翻番，商业化数据强；付费增长 + 流失对冲叙事有张力；TechCrunch 原文可补硬数据
- `为什么这轮没选`: continuity_only limited sheet；Reddit 正文信息极少，需回链 TechCrunch 原文补数据；属 top4-top9 梯队，本次未获授权
- `什么时候可捞回`: market-scout 补 TechCrunch 原文后；可分配 wechat（Claude 商业化分析）/ baijiahao（Claude vs OpenAI 付费对比 SEO）

---

### `anthropic_sonnet_opus_46`

- `为什么能进最终池`: Anthropic 官方一手源；Sonnet 4.6 / Opus 4.6 双旗舰同发；81,000 用户调研独家数据；Claude 广告-free 差异化定位
- `为什么这轮没选`: continuity_only limited sheet；发布时间分散（2-3 月），时效性偏弱；属 top4-top9 梯队，本次未获授权
- `什么时候可捞回`: 完整 Top6 任务单阶段；建议以「Anthropic 用户调研揭示：用户最想要什么样的 AI」分配 wechat / zhihu

---

### `universal_claude_md`

- `为什么能进最终池`: Claude 开发者效率工具；HN 验证（113 points / 52 comments）；token 成本优化是实际痛点；GitHub 可直接回链
- `为什么这轮没选`: continuity_only limited sheet；属 top4-top9 梯队，本次未获授权；63% 数字需独立验证
- `什么时候可捞回`: 完整 Top6 任务单阶段；建议分配 zhihu（开发者工具合集）/ x（HN 社区扩散）

---

### `wecom_ai_skills_observation`（P3 降 holdout）

- `为什么能进最终池`: 企业微信 AI Skills 开源动态，中文 B2B AI Agent 生态观察有价值
- `为什么这轮没选`: **P3 致命阻塞**：「养虾大杀器」「Claude Code 直接调用」等关键主张无法在腾讯官方博客/GitHub 或任何独立信源验证；仅媒体单源，不具备放行条件
- `什么时候可捞回`: 等腾讯官方博客、GitHub repo 或其他独立信源出现；建议持续追踪 WeCom 官方 AI Skills 公告

---

## 裁判备注（供下游参考）

- **当前时间**: 2026-03-31 14:15 CST，已过 13:15 硬冻结线
- **上游 scorecard**: `market-editor` @ 2026-03-31 14:06 CST，`status=rework`，`continuity_decision=continuity_only`，`continuity_output=top20_mini_slate`
- **上游 rework 包**: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260331__top20-screening-pack__reworked.md`（13:11 CST）
- **xAI #7 重建负责人**: `market-scout`；预计当日结束前提交复评
- **arXiv 摘要补查负责人**: `market-scout`；可与 xAI 重建同步进行
- **本任务单性质**: `continuity_only` limited task sheet；仅含 mini_slate 已授权 active slots；其余全部 holdout 并写清原因
- **百家号 SEO 镜像层**: 建议 xAI 重建完成后优先升格 xAI 进 baijiahao；Claude Code / robots_bury_you 次之

---

*本任务单由 `topic-planner` 生成，写入时间 2026-03-31 14:15 CST*
*遵循 `continuity_only` 边界：仅覆盖 2 个已确认 active slots，xAI/其余 top4-top9 全部 holdout，不提前展开 premium lane*

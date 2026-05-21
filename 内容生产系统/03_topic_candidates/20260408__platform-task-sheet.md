# 平台任务单

- `date`: `2026-04-08`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-08 19:05:00 CST`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260408__daily-top8-to-top5.md`
- `top20_scorecard`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260408__top20__stage-gate-scorecard.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `Top20 scorecard=rework+continuity_only；Top5 板=final+continuity_only；本单为 limited task sheet，仅覆盖 4 个平台共 5 个 active slot，不得超出 Top5/Holdout 候选池`

---

## 全局主池 Top6

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | `hn_frontpage_47679258_system_card_claude_mythos_preview_pdf_20260408` | Anthropic System Card 披露 Claude Mythos 架构预览；高时效一手信号，AI/Agent 主线强锚点 | Anthropic 官方 PDF，稀缺性强；HN 高分讨论；与 builder/agent 投资叙事高度相关 | 缺全文深抓；正文必须补关键原始内容再展开判断 |
| 2 | `hn_frontpage_47679155_assessing_claude_mythos_preview_s_cybersecurity_capabilities_20260408` | Claude Mythos Preview 安全能力专项评估；与 Top1 构成姐妹篇，覆盖不同维度 | HN 高分；Anthropic 官方 blog；安全叙事具备差异化讨论空间 | 同 Top1；两个主题须错开切入角度避免重复 |
| 3 | `github_trending_nvidia_personaplex_20260408` | NVIDIA personaplex：NVIDIA 开源 Agent 个性化框架，7,724 ★；与 AI/Agent 主线高度匹配 | GitHub trending 可核实数据锚点；NVIDIA 官方背书；开发者叙事具备天然扩散性 | 缺完整 why_now；正文须补这个时间窗口为什么重要 |
| 4 | `github_trending_thecraighewitt_seomachine_20260408` | seomachine：开发者 SEO 工具，3,650 ★；builder 工具链细分赛道 | GitHub stars 可核实；开发者工具链叙事适合 X/Bilibili 传播 | 本轮进入 holdout，避免与 personaplex 赛道重叠；可捞回 |
| 5 | `reddit_localllama_you_can_now_fine_tune_gemma_4_locally_8gb_vram_bug_fixes_20260408` | Gemma 4 本地微调：8GB VRAM 门槛突破，工程痛点真实可感 | Reddit 高讨论度；工程叙事具备小红书/Bilibili 传播潜力；本地推理趋势叙事 | 品牌贴合度中；本轮分配 Bilibili；硬数据偏少 |
| 6 | `__supply_gap__` | 本轮 continuity_only supply gap：Top5 板仅 5 个有效候选，余量 holdout（seomachine/机器人芯片/GLM-5.1/sandbox 视频）本轮未激活，条件性保留 | continuity_only 场景下候选质量优先于数量 | 6th slot 供明日复评或 holdout 补位使用 |

---

## 三个最重要平台任务单

> 本轮 limited task sheet 仅覆盖 4 个平台共 5 个 active slot（WeChat × 2, X × 1, Bilibili × 1，1 slot 保留），其余平台写入 Holdout。

---

## 六个主战场任务单

### `wechat`

#### Task 1
- `topic_key`: `hn_frontpage_47679258_system_card_claude_mythos_preview_pdf_20260408`
- `目标读者`: AI/Agent 创业者、开发者、投资人；关注 Anthropic 产品路线与行业格局者
- `切入角度`: 不要做 Anthropic 新闻摘要，直接回答：这个 System Card 透露的信号，对我们追踪的 AI Agent 主线意味着什么？给出判断，不只给信息。
- `核心论点`: Claude Mythos 架构预览是 Anthropic 加速 Agent 落地能力的系统性披露；其安全设计（System Card 核心）与商业化路径张力是本篇的判断核心。
- `证据抓手`: Anthropic PDF 全文 + HN 讨论（分数/评论量）+ 官方 blog 姐妹篇（#2）
- `source_ref_bundle`: 
  - PDF: `https://www-cdn.anthropic.com/53566bf5440a10affd749724787c8913a2ae0841.pdf`
  - Source packet: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260408_075509__hn_frontpage_47679258_system_card_claude_mythos_preview_pdf__source-packet.md`
- `视觉建议`: 信息图（System Card 核心安全机制简化图示）+ 架构路径时间轴
- `为什么适合该平台`: 微信适合承载完整叙事和判断；本篇需要从原始 PDF 展开，不只复述 HN 标题；适合深度文章逻辑
- `continuity_note`: `continuity_only 保底锁题；正文必须先补原始 PDF 关键内容，不得把 HN 摘要直接带进正文`

#### Task 2
- `topic_key`: `hn_frontpage_47679155_assessing_claude_mythos_preview_s_cybersecurity_capabilities_20260408`
- `目标读者`: AI 安全关注者、开发者、投资人；关注模型安全与商业化平衡者
- `切入角度`: 与 Task 1 错开——Task 1 侧重架构判断，Task 2 专项讨论安全能力边界：Claude Mythos 的网络安全设计是否真的到位？给出有依据的判断。
- `核心论点`: Claude Mythos Preview 的安全能力评估揭示了当前 Agent 模型在真实场景中的安全边界；其局限性对高风险场景部署有直接参考价值。
- `证据抓手`: Anthropic 官方 blog + HN 评论中的安全讨论 + 对比同类模型安全设计
- `source_ref_bundle`:
  - Blog: `https://red.anthropic.com/2026/mythos-preview/`
  - Source packet: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260408_075509__hn_frontpage_47679155_assessing_claude_mythos_preview_s_cybersecurity_capabilities__source-packet.md`
- `视觉建议`: 安全能力雷达图 + 与同类模型安全维度对比表
- `为什么适合该平台`: 微信完整叙事优势适合展开安全评估的技术细节；配合 Task 1 形成姐妹篇
- `continuity_note`: `continuity_only 保底锁题；正文必须先补原始 blog 内容，不得把 HN 摘要直接带进正文；与 Task 1 错角避免内容重叠`

### `xiaohongshu`

#### Task 1（留空）
- 本轮 continuity_only 场景下，小红书无独立 active slot；Top5 候选无明确适合小红书角度者。
- 如后续 continuity 槽位有多余，再从 holdout 6（机器人芯片）拉出。

### `zhihu`

#### Task 1（留空）
- 本轮 continuity_only 场景下，知乎无独立 active slot。
- GitHub seomachine（holdout 3）如捞回，可优先考虑知乎角度。
- holdout 7（GLM-5.1）具备知乎解释型内容潜力。

### `x`

#### Task 1
- `topic_key`: `github_trending_nvidia_personaplex_20260408`
- `目标读者`: 开发者、AI/Agent 技术关注者；关注开源模型与工具链者
- `切入角度`: NVIDIA personaplex 解决了 Agent 个性化的什么旧痛点？为什么现在这个时间窗口重要？给出一个有立场的判断，不只介绍功能。
- `核心论点`: NVIDIA 开源 personaplex 是 Agent 个性化框架的实质性进展；其与 NVIDIA 生态的绑定是这个工具比同类更有传播力的原因。
- `证据抓手`: GitHub stars 7,724 / +663 today + NVIDIA 官方页面
- `source_ref_bundle`:
  - GitHub: `https://github.com/NVIDIA/personaplex`
  - Source packet: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260407_224633__github_trending_nvidia_personaplex__source-packet.md`
- `视觉建议`: GitHub 趋势截图 + Agent 框架能力对比简图
- `为什么适合该平台`: X 适合短平快的工程工具快讯；GitHub trending 数据天然适合 X 格式
- `continuity_note`: `正文须补原始 GitHub README 关键信息，不得只引用 HN 标题`

### `bilibili`

#### Task 1
- `topic_key`: `reddit_localllama_you_can_now_fine_tune_gemma_4_locally_8gb_vram_bug_fixes_20260408`
- `目标读者`: 本地 AI 部署爱好者、开发者、学生；关注大模型本地化工程可行性者
- `切入角度`: 不要停留在"好消息"层面，直接回答：8GB VRAM 微调 Gemma 4 为什么重要，它意味着本地 AI 工作流的哪个环节被真正突破？
- `核心论点`: Gemma 4 本地微调门槛降至 8GB VRAM 是本地 Agent 部署的关键节点；这一突破让更多开发者能在消费级硬件上构建定制 Agent。
- `证据抓手`: Reddit 讨论量 + 技术可行性论证（8GB VRAM 门槛的实际意义）+ 工程痛点背景
- `source_ref_bundle`:
  - Reddit: `https://old.reddit.com/r/LocalLLaMA/comments/1sexdhk/you_can_now_finetune_gemma_4_locally_8gb_vram_bug/`
  - Source packet: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260408_075509__reddit_localllama_you_can_now_fine_tune_gemma_4_locally_8gb_vram_bug_fixes__source-packet.md`
- `视觉建议`: 硬件门槛对比图 + 工程路径简化流程图（适合 B 站视频脚本结构）
- `为什么适合该平台`: Bilibili 工程教程/解读叙事强；本篇技术门槛突破具备天然视频化潜力
- `continuity_note`: `正文须先补 Reddit 讨论中的关键工程细节，硬数据不足时不要虚构`

### `toutiao`

#### Task 1（留空）
- 本轮 continuity_only 场景下，今日头条无独立 active slot。

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: 否
- `理由`: 本轮 Top5 候选均来自 HN/GitHub/Reddit，属于国际开发者/投资圈话题，国内 SEO 价值有限；Anthropic Claude Mythos 系列如在中文开发者圈产生足够讨论，可考虑从微信主稿事后镜像，而非本轮独立选题。
- `承接哪篇主稿更优`: 微信 Task 1（System Card）事后镜像性价比最高，条件是正文产生足够中文讨论量。

---

## Holdout 清单

### `github_trending_thecraighewitt_seomachine_20260408`
- `为什么能进最终池`: GitHub 3,650 ★；开发者 SEO 工具链，具备差异化讨论空间
- `为什么这轮没选`: 与 personaplex 同为 GitHub trending，赛道相近；保留一个即可避免内容同质化；且 seomachine stars 低于 personaplex
- `什么时候可捞回`: personaplex 后续补证失败，或 agent 工具链专题需要对比多个工具时优先捞回

### `wechat_zhidx_10yi_robot_chip_funding_20260408`
- `为什么能进最终池`: deep article 5,018字已就位；强数据锚点（$150M B2轮，多家 VC 背书）；机器人芯片投资叙事硬
- `为什么这轮没选`: 本轮 continuity_only limited sheet；WeChat 2 slot 已分配给 Claude Mythos 系列；机器人芯片融资偏深阅读，与 Claude 话题节奏不同
- `什么时候可捞回`: 若 WeChat Task 1/2 任一撞车或补证失败；或明日 Top5 出现 continuity gap 时优先填补

### `reddit_localllama_glm_5_1_20260408`
- `为什么能进最终池`: HN 高分；GLM-5.1 是国产大模型重要迭代，具备讨论价值
- `为什么这轮没选`: 本轮已从 Reddit 拿了 Gemma 4 slot；避免连续两个 Reddit 话题；且 GLM-5.1 硬数据不足
- `什么时候可捞回`: Gemma 4 补证失败；或明日 HN 出现 GLM-5.1 新讨论时优先捞回

### `youtube_ai_dot_engineer_why_and_how_you_need_to_sandbox_ai_generated_code_harshil_agrawal_cloudf_20260408`
- `为什么能进最终池`: AI 安全主题与一人公司主线高度匹配；Cloudflare 背书
- `为什么这轮没选`: YouTube 视频发布时间不硬（scorecard 已标注）；Bilibili slot 已用于 Gemma 4；无其他合适平台槽位
- `什么时候可捞回`: 确认视频发布时间后；或明日出现 AI 安全新热点时优先捞回

---

## 本单执行备注

1. **continuity_only 纪律**：本单所有 active slot 必须先补原始证据（PDF/blog/GitHub/README）再展开；不得把 HN/Reddit 标题摘要直接带进正文。
2. **WeChat 双槽不重复**：Task 1 侧重架构判断，Task 2 专项安全评估；content-writer 须注意错角避免内容重叠。
3. **X 快讯格式**：personaplex 在 X 上以快讯/钩子为主，不需要长文。
4. **Bilibili 视频脚本优先**：Gemma 4 这篇优先考虑视频脚本结构，工程路径图建议。
5. **每日上限不因 continuity 稀释**：continuity_only 只降低题目的先发优势预期，不降低质量标准。

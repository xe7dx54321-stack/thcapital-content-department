# 平台任务单

- `date`: `2026-04-12`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-12 18:05 CST`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260412__top20-screening-pack.md`
- `input_scorecard`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260412__top20__stage-gate-scorecard.md`
- `input_top5_board`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260412__daily-top8-to-top5.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `rework + continuity_only；Top5板 final continuity_only；上游 scorecard v5(2026-04-12 17:58 CST) 为 rework continuity_only；本轮执行 limited task sheet：wechat 2主槽 + xiaohongshu 1槽 + zhihu 1槽；其余候选入 holdout`
- `morning_flash_exclusion`: `ai_morning_brief_20260412 已单独进 publish queue，不在本单范围内；本单候选均与 morning_flash 无重叠`
- `continuity_notice`: `本单为 continuity_only limited sheet；所有 active slot 写稿前须优先补官方/原始来源截图，不得将补证脚手架直接带入正文；待 signal-scout 补证完成后方可触发 content-writer 进稿`

## 全局主池 Top6（来自 20260412 Top5 板 + mini_slate 可追溯候选池）

| rank | topic_key | 优先级 | 为什么值得写 | 主要风险 |
|------|-----------|--------|--------------|----------|
| 1 | `cirrus_labs_join_openai_20260412` | P0 | OpenAI 关联+HN一手源；补官宣截图后 publish-ready；AI行业并购信号价值高 | 补证截图到位前不得发布；OpenAI 侧尚未官宣 |
| 2 | `claude_mythos_bug_机器之心_20260412` | P0 | 中文一手源无需额外补证，publish-ready 等级最高；Claude Mythos 是 Claude AI 核心功能线，bug 事件天然引发开发者讨论 | 无已知风险 |
| 3 | `anthropic_banning_under_18_20260412` | P1 | AI政策监管标志性事件；青少年AI使用是家长/教育双圈层痛点；监管趋势叙事空间大 | 补 Anthropic 官方政策页面截图到位前不得发布 |
| 4 | `google_mcp_colab_20260412` | P2 | MCP 是 AI Agent 工具链核心协议；Google Colab 集成代表 MCP 进入主流开发环境；开发者社区天然契合知乎 | 补 InfoQ 原文+Colab MCP 文档截图到位前不得发布 |
| 5 | `openai_altman袭击_知乎_20260412` | P1 | 知乎109万热度验证中文市场需求；高热事件天然破圈；AI 行业领袖安全系统性讨论空间大 | 补英文主流媒体(NYT/TechCrunch)截图到位前不得发布；需与 #11(Reddit) 角度差异化 |
| 6 | `agent_experience_少数派_20260412` | P2 | AI/Agent 主线匹配；少数派调性与 builder 受众高度重合；与 Google MCP 赛道有协同价值 | published_at=unknown，时效窗口存疑；补少数派原文截图+时间戳后方可推进 |

## 三个最重要平台任务单

---

## 六个主战场任务单

---

### `wechat`

#### Task 1
- `topic_key`: `cirrus_labs_join_openai_20260412`
- `目标读者`: 关注 AI 行业动态、OpenAI 生态、投资并购线索的从业者与 maker
- `切入角度`: 以团队加入为入口，深挖 OpenAI 此次并购/合作背后的战略意图，以及对 AI Agent / 一人公司主线的实质影响
- `核心论点`: Cirrus Labs 团队加入 OpenAI 不只是人事变动，而是 OpenAI 在 Agent 工具链和 CI/CD 能力补强的战略信号；AI 一人公司面临的人才格局正在因此改变
- `证据抓手`: 
  - HN frontpage 一手信号（cirruslabs.org 官网信息）
  - **必须补证**：OpenAI 官方博客声明 或 TechCrunch/VentureBeat 报道截图（cirruslabs.org 官网单独不够）
  - AI/Agent 工具链并购趋势背景
- `source_ref_bundle`: `signal-scout source_packet #1（cirrus_labs_join_openai）+ Top5板 rank#1`
- `视觉建议`: 信息图：Cirrus Labs 背景 + OpenAI 最近3个月并购/合作时间线；或：团队技术栈 vs OpenAI 现有能力矩阵对照图
- `为什么适合该平台`: 微信适合承载完整叙事、深度判断和多证据整合；OpenAI 并购类事件需要完整的行业逻辑链，微信主稿是最佳承载体
- `补证前置`: ✅ 截图到位后直接 publish-ready；⚠️ 截图未到位不得进入 content-writer

#### Task 2
- `topic_key`: `claude_mythos_bug_机器之心_20260412`
- `目标读者`: AI 开发者、Claude 产品用户、技术社区关注者
- `切入角度`: 从 Claude Mythos 产品可靠性切入，说明 bug 对用户信任的影响，以及为什么这个时间点值得关注（机器之心中文一手源绕过语言门槛）
- `核心论点`: Claude Mythos bug 暴露了当前 AI 产品稳定性边界的真实状态；这不是单一技术故障，而是 AI Native 产品进入主流必须面对的信任挑战
- `证据抓手`:
  - 机器之心中文一手源（无需额外补证）
  - Claude Mythos 功能背景（signal-scout packet #3）
- `source_ref_bundle`: `signal-scout source_packet #3（claude_mythos_bug_机器之心）+ Top5板 rank#2`
- `视觉建议`: Bug 复现路径示意图；或：Claude vs 主要竞品（GPT-4o、Gemini）稳定性对比参考
- `为什么适合该平台`: 机器之心本身已是中文一手源，微信稿可作为深度解读和完整叙事层；技术细节+用户信任双线并行，微信适合承载
- `补证前置`: ✅ 一手源直接 publish-ready，无需等待额外截图

---

### `xiaohongshu`

#### Task 1
- `topic_key`: `anthropic_banning_under_18_20260412`
- `目标读者`: 家长、教育从业者、关注 AI 监管趋势的普通用户（18-40岁女性为主）
- `切入角度`: 家长视角切入——"Anthropic 禁止18岁以下用 Claude，我的孩子还能用吗？"；用具体政策内容对比 OpenAI/Google 的青少年政策差异
- `核心论点`: Anthropic 率先出青少年禁令不是保守，而是 AI 监管的商业化试水；这个决定背后是 AI 公司对家长责任和法律风险的重新定价
- `证据抓手`:
  - 机器之心/Reddit 一手讨论
  - **必须补证**：Anthropic 官方政策页面截图 或 The Verge/TechCrunch 报道截图
  - 各平台青少年 AI 政策对比（可引用公开报道）
- `source_ref_bundle`: `signal-scout source_packet #2（anthropic_banning_under_18）+ Top5板 rank#3`
- `视觉建议`: 对比图（Anthropic vs OpenAI vs Google 青少年政策三栏对比）；或：政策时间线（Anthropic 政策出台节点）
- `为什么适合该平台`: 小红书家长/教育圈层传播势能强；"我的孩子还能用AI吗"是天然的高互动话题钩子；政策对比图表在小红书有强传播力
- `补证前置`: ⚠️ Anthropic 官方政策截图到位前不得发布

---

### `zhihu`

#### Task 1
- `topic_key`: `google_mcp_colab_20260412`
- `目标读者`: AI 开发者、工程师、关注 AI 工具链进展的技术社区（知乎开发者重镇）
- `切入角度`: 从 MCP 生态崛起切入——"Google Colab 集成 MCP 意味着什么？"；说明为什么 Colab 集成代表 MCP 走向主流，以及对 AI builder 的实际意义
- `核心论点`: MCP（Model Context Protocol）正在成为 AI Agent 工具链的 USB 接口；Google Colab 集成意味着主流开发环境正式接纳 MCP；开发者现在可以在最普及的云开发环境中直接使用 MCP
- `证据抓手`:
  - InfoQ 原文报道
  - **必须补证**：InfoQ 原文截图 + Colab MCP 官方文档截图
  - MCP 生态现状（可引用 MCP 官方 spec 背景）
- `source_ref_bundle`: `signal-scout source_packet #13（google_mcp_colab）+ Top5板 rank#5`
- `视觉建议`: MCP 生态图（协议层-工具层-应用层三层架构）；或：Colab 内 MCP 使用流程截图示意
- `为什么适合该平台`: 知乎是开发者社区技术讨论的天然阵地；MCP 技术解读、InfoQ 来源背书、开发者问答格式高度契合知乎内容生态
- `补证前置`: ⚠️ InfoQ 原文+Colab MCP 文档截图到位前不得发布

---

### `x`

*本轮 continuity_only limited sheet，x 平台无 active slot*

---

### `bilibili`

*本轮 continuity_only limited sheet，bilibili 平台无 active slot*

---

### `toutiao`

*本轮 continuity_only limited sheet，toutiao 平台无 active slot*

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **暂不单独立题**
- `理由`: 本轮为 continuity_only limited sheet，共4个 active slot 已达 wechat(2)+xiaohongshu(1)+zhihu(1) 上限；baijiahao 作为 SEO 镜像层优先级低于主战场平台；Cirrus Labs 和 Claude Mythos 如在主战场验证传播效果后，可考虑在后续批次进入 baijiahao 做长尾截流
- `承接哪篇主稿更优`: 
  - 若 Cirrus Labs 主稿微信传播验证良好 → 镜像《Cirrus Labs 加入 OpenAI 意味着什么？》长尾版
  - 若 Claude Mythos 主稿验证良好 → 镜像《Claude Mythos bug 始末》长尾版

---

## Holdout 清单

### `openai_altman袭击_知乎_20260412`
- `为什么能进最终池`: P1；知乎109万热度验证中文市场需求；高热事件天然破圈；OpenAI CEO 安全事件具备极高新闻性；AI 行业领袖安全系统性讨论空间大
- `为什么这轮没选`: **本轮 active slot 已满（wechat×2+xiaohongshu×1+zhihu×1）；Altman袭击事件需要补英文主流媒体截图；补证优先级低于已在 slot 内的 Cirrus Labs(P0) 和 Claude Mythos(P0 免补证)**
- `什么时候可捞回`: signal-scout 补 NYT/TechCrunch/Guardian 任一英文主流媒体截图到位后，且若有平台 slot 空出（如补证失败），优先从 holdout 接力；**注意：需与 #11（Reddit Sam Altman Molotov）保持角度差异化，知乎角度→安防/OpenAI治理，Reddit角度→news事件本身**

### `agent_experience_少数派_20260412`
- `为什么能进最终池`: P2；AI/Agent 主线匹配；少数派调性与 builder 受众高度重合；少数派原文为相对一手源，产品类内容可信度中等
- `为什么这轮没选`: **赛道与 #5（Google MCP Colab）均为工具/平台类，有一定重叠；published_at=unknown 与时效窗口=3 矛盾，时间戳存疑；本轮 limited sheet 仅4个 slot 已分配完毕，无剩余容量**
- `什么时候可捞回`: signal-scout 补少数派原文截图 + published_at 时间戳到位后，若开发者相关平台（知乎/bilibili）有余槽，按优先级接力；**捞回后须与 Google MCP Colab 角度做差异化（Agent Experience → 个人生产力工具视角；MCP Colab → 开发者生态/协议标准视角）**

### `sam_altman_袭击_合并_20260412`
- `为什么能进最终池`: P2；OpenAI CEO 安全事件具备极高新闻性；#11 Reddit Molotov 与 #12 Firebomb 双来源（已 scorecard v5 确认 duplicate，降为佐证位）；高热事件可形成多角度覆盖
- `为什么这轮没选`: **与 #4（openai_altman袭击_知乎）同事件链；scorecard v5 裁定 Altman 事件链最多占 2 个独立槽位；知乎槽位已给 #4；Reddit #11 角度需补英文主流媒体截图，补证与 #4 撞车；平台 slot 已满**
- `什么时候可捞回`: 任一 active slot 补证撞车或失败时；或下一批次 Altman 事件链独立角度（如"OpenAI CEO 安全风险对 AI 公司治理结构的影响"）可拆分重新入板；**#12 永久为佐证位，不独立成篇**

### `google_scion_infoq_20260412`
- `为什么能进最终池`: P2；Google 官方发布；Scion 是 Google 下一代 AI 架构；InfoQ 技术深度背书；赛道匹配度高
- `为什么这轮没选`: **与 #5（Google MCP Colab）同为 Google 官方技术发布，赛道重叠；本轮 limited sheet 仅4个 slot 已分配；开发者平台 zhihu slot 已给 MCP Colab；无剩余容量**
- `什么时候可捞回`: Google MCP Colab 补证失败，或下一批次开发者平台有余槽；**捞回后须与 MCP Colab 做差异化（Scion → Google 下一代架构/技术细节；MCP Colab → 生态协议/开发者工具集成）**

---

## 补证追踪表（signal-scout 负责）

| topic_key | 必须补证项 | 负责方 | deadline | 当前状态 |
|-----------|-----------|--------|----------|----------|
| `cirrus_labs_join_openai_20260412` | OpenAI 官方博客或 TechCrunch/VentureBeat 报道截图 | signal-scout | 2026-04-13 14:00 | 🔴 pending |
| `claude_mythos_bug_机器之心_20260412` | 无需补证（一手源直接可信） | — | — | 🟢 ready |
| `anthropic_banning_under_18_20260412` | Anthropic 官方政策页面截图或 The Verge/TechCrunch 报道截图 | signal-scout | 2026-04-13 14:00 | 🔴 pending |
| `google_mcp_colab_20260412` | InfoQ 原文截图 + Colab MCP 官方文档截图 | signal-scout | 2026-04-13 16:00 | 🔴 pending |
| `openai_altman袭击_知乎_20260412` | NYT/TechCrunch/Guardian 任一英文主流媒体截图 | signal-scout | 2026-04-13 15:00 | 🔴 pending |
| `agent_experience_少数派_20260412` | 少数派原文截图 + published_at 时间戳 | signal-scout | 2026-04-13 16:00 | 🔴 pending |
| `sam_altman_袭击_合并_20260412` | —（佐证位不独立成篇，无需独立补证） | — | — | 🟡 佐证位 |
| `google_scion_infoq_20260412` | InfoQ 原文截图 + GitHub/demo 链接 | signal-scout | 2026-04-13 16:00 | 🔴 pending |

---

*topic-planner | 2026-04-12 18:05 CST*
*stage_gate_status: continuity_only | limited task sheet | 4 active slots | 4 holdout candidates*
*WAITING_ON_SUPPLEMENT: signal-scout P0/P1 补证截图到位后 content-writer 可启动*

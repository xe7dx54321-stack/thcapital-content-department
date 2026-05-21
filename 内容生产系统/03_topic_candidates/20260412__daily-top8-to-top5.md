# 20260412 Top 8 -> Top 5 选题板

- `date`: `2026-04-12`
- `generated_at`: `2026-04-12 09:30:00 CST`
- `source_scope`: `T-1 17:00 ~ T 14:30`
- `top20_pack_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260412__top20-screening-pack.md`
- `top20_scorecard_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260412__top20__stage-gate-scorecard.md`
- `board_status`: `continuity_only`
- `board_mode`: `mini_slate_forward — 基于 Top20 scorecard continuity_only 裁定，直接取 mini_slate P0/P1/P2 前8顺位入板`
- `board_truth`: `该板来自 Top20 scorecard 裁定后的 top20_mini_slate；stage_gate score=6.5/10，rework=continuity_only；所有候选均为补证型 rework，仅#3（机器之心）无需补证；其余均需补证截图到位方可进 content-writer。`
- `candidate_count`: `8`
- `continuity_reason`: `scorecard 给出了 top20_mini_slate 共10个有效候选；取前8进入今日 top8-to-top5板，后2进入 holdout；ai_morning_brief_20260412 已单独进 publish queue，不在本板范围内。`

## Continuity Rule

- `该板不是 premium pass`：后续平台任务单、approved-topic、draft-pack 必须沿 continuity_only 路径运行。
- `可以继续生产，但不能假装已经过线`：写稿时必须优先补官方 / 原始来源，不得把补证脚手架直接带进正文。
- `若强候选不足 8 个，就写实 supply gap`：今日 mini_slate 共10个，取前8；#9 Interconnects 和 #14 Claude Code source leak 因赛道重叠或补证难度降入 holdout。

## Top 5 Recommended

| rank | candidate_key | 题目 | 市场潜力 | 品牌贴合 | 推荐理由 | 执行备注 |
|------|---------------|------|----------|----------|----------|----------|
| 1 | cirrus_labs_join_openai_20260412 | Cirrus Labs 团队确认加入 OpenAI | 高 | 高 | P0锚点；HN frontpage一手源；OpenAI关联度高；截图到位即publish-ready | 补证截图：Cirrus Labs官网或博客 + OpenAI官方博客 |
| 2 | claude_mythos_bug_机器之心_20260412 | Claude Mythos bug 事件（机器之心） | 中高 | 高 | 中文一手源；无需额外补证；赛道匹配AI主线 | 一手源直接publish-ready |
| 3 | anthropic_banning_under_18_20260412 | Anthropic 禁止18岁以下使用 | 中高 | 高 | P1；AI政策类事件；具备天然讨论空间 | 需补Anthropic官方政策页面截图 |
| 4 | openai_altman袭击_知乎_20260412 | OpenAI Altman袭击事件 | 高 | 高 | P1；高热事件天然破圈；知乎109万热度入口 | 需补NYT或英文主流媒体截图 |
| 5 | google_mcp_colab_20260412 | Google MCP Colab 集成 | 中 | 高 | P2；Google官方发布；MCP赛道匹配度高；开发者关注强 | 需补InfoQ原文截图 + Colab MCP文档截图 |

## Holdout 3

| holdout_rank | candidate_key | 题目 | 为什么能进 Top 8 | 为什么被放下 | 能否捞回 | 捞回条件 |
|--------------|---------------|------|------------------|------------|----------|----------|
| 6 | agent_experience_少数派_20260412 | Agent Experience（少数派） | P2；AI/Agent主线匹配；时效窗口给满 | 与#5（Google MCP）赛道重叠；补证截图优先级低于#5 | 可以 | 若#5补证失败或平台槽位有余 |
| 7 | google_scion_infoq_20260412 | Google Scion（InfoQ） | P2；Google官方发布；赛道匹配高 | partial source；InfoQ截图与#5(MCP Colab)赛道重叠 | 可以 | 若#5补证失败或开发者平台有余槽 |
| 8 | sam_altman_袭击_合并_20260412 | Sam Altman袭击事件（合并#11/#12） | P2；高热事件 | 与#4（OpenAI Altman袭击）时效重叠；已被#4覆盖 | 可以 | 若#4补证撞车或平台需要双线覆盖 |

## Top 5 Detail Blocks

### Top 1｜Cirrus Labs 团队确认加入 OpenAI

- 一句话判断：P0锚点；今日 pack 最可信单条；HN frontpage一手源+OpenAI关联双重加持；截图到位即 publish-ready。
- 为什么值得做：OpenAI 收购/合作类事件具备高传播势能；Cirrus Labs 有技术背景；AI行业并购信号价值高。
- 市场潜力：高
- 品牌贴合度判断：高
- 平台发酵：
  - 微信：做主稿，承担完整叙事、证据和判断。
  - 知乎：承接解释/对比/问答式需求，适合把论证展开。
  - X：做快讯/观点钩子，放大首轮传播。
- 原始链接 / Source Packet：见 `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/` 内 #1 对应 packet
- 建议切入角度：以团队加入为入口，深挖这代表 OpenAI 什么战略意图，以及对 AI Agent / 一人公司主线意味着什么。
- 建议输出形式 / 平台：微信 / 知乎 / X / 小红书
- 补证要求（must）：Cirrus Labs 官网或博客截图（含合作具体信息）+ OpenAI 官方声明链接
- 风险提示：补证截图到位前不得发布；补证完成后可立即进 content-writer

### Top 2｜Claude Mythos bug 事件（机器之心）

- 一句话判断：P1；中文一手源，无需额外补证，publish-ready 等级最高。
- 为什么值得做：Claude Mythos 是 Claude AI 产品系核心功能；bug 事件具备开发者社区天然讨论空间；机器之心中文一手来源绕过语言门槛。
- 市场潜力：中高
- 品牌贴合度判断：高
- 平台发酵：
  - 微信：做主稿，承担完整叙事、证据和判断。
  - 知乎：承接技术分析/对比/问答式需求。
  - 小红书：做轻量技术科普钩子。
- 原始链接 / Source Packet：见 `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/` 内 #3 对应 packet（机器之心）
- 建议切入角度：从 Claude 产品可靠性切入，说明 bug 对用户信任的影响，以及为什么这个时间点值得关注。
- 建议输出形式 / 平台：微信 / 知乎 / 小红书
- 补证要求：无需补证（中文一手源直接可信）
- 风险提示：无

### Top 3｜Anthropic 禁止18岁以下使用

- 一句话判断：P1；AI 政策监管类事件；具备天然讨论空间和家长/教育圈层传播势能。
- 为什么值得做：全球 AI 监管大趋势下，Anthropic 率先出政策具备标志性；青少年AI使用是家长/教育双圈层痛点。
- 市场潜力：中高
- 品牌贴合度判断：高
- 平台发酵：
  - 微信：做主稿，承担完整叙事、证据和判断。
  - 知乎：政策解读/对比/问答式需求。
  - 小红书：家长视角切入，亲和力强。
- 原始链接 / Source Packet：见 `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/` 内 #2 对应 packet
- 建议切入角度：以政策内容为入口，对比 OpenAI/Google 的青少年政策差异，说明监管趋势。
- 建议输出形式 / 平台：微信 / 知乎 / 小红书
- 补证要求（must）：Anthropic 官方政策页面截图或主流媒体（The Verge/TechCrunch）报道截图
- 风险提示：补证截图到位前不得发布

### Top 4｜OpenAI Altman 袭击事件

- 一句话判断：P1；知乎109万热度，高热事件天然破圈；与 Sam Altman 袭击事件合并覆盖（#11/#12）。
- 为什么值得做：OpenAI CEO 个人安全事件具备极高新闻性和传播势能；知乎平台109万热度验证了中文市场需求。
- 市场潜力：高
- 品牌贴合度判断：高
- 平台发酵：
  - 微信：做主稿，承担完整叙事、证据和安全分析。
  - 知乎：承接事件还原/安全讨论/AI治理需求。
  - X：快讯+观点放大。
- 原始链接 / Source Packet：见 `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/` 内 #5 对应 packet（知乎）
- 建议切入角度：以事件本身为入口，深挖 AI 行业领袖安全风险的系统性原因，以及对 AI 公司治理的启示。
- 建议输出形式 / 平台：微信 / 知乎 / X / 小红书
- 补证要求（must）：NYT 或英文主流媒体正文截图（需与#11/#12合并补一张即可）
- 风险提示：补证截图到位前不得发布；与#8 Sam Altman Firebomb 合并处理避免重复

### Top 5｜Google MCP Colab 集成

- 一句话判断：P2；Google 官方发布；MCP（Model Context Protocol）赛道开发者关注度高；与 #7 Google Scion 形成 Google 生态双覆盖。
- 为什么值得做：MCP 是 AI Agent 工具链核心协议；Google Colab 集成意味着 MCP 进入主流开发环境；InfoQ 来源赛道匹配度高。
- 市场潜力：中
- 品牌贴合度判断：高
- 平台发酵：
  - 知乎：开发者社区技术讨论，天然契合。
  - X：开发者工具链视角快讯。
  - 微信：技术解读+工具推荐角度。
- 原始链接 / Source Packet：见 `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/` 内 #13 对应 packet
- 建议切入角度：从 MCP 生态崛起切入，说明为什么 Colab 集成代表 MCP 走向主流，以及对 AI builder 的实际意义。
- 建议输出形式 / 平台：知乎 / X / 微信
- 补证要求（must）：InfoQ 原文截图 + Colab MCP 官方文档截图
- 风险提示：补证截图到位前不得发布；与 #7（Google Scion）赛道略有重叠，先保 #5

---

## Holdout Detail Blocks

### Holdout 6｜Agent Experience（少数派）

- 一句话判断：P2；AI/Agent 主线匹配；少数派平台调性与 builder 受众高度重合。
- 为什么能进 Top 8：赛道匹配 AI/Agent 主线；时效窗口给满合理；partial source 但产品类内容可信度高。
- 为什么被放下：补证截图优先级低于前5；赛道与#5（Google MCP Colab）均为工具/平台类，有一定重叠。
- 能否捞回：可以 — 若前5中任一补证失败或平台槽有余量，按原题接力。
- 捞回条件：补少数派原文截图 + 产品页截图到位后自动激活。

### Holdout 7｜Google Scion（InfoQ）

- 一句话判断：P2；Google 官方发布；Scion 是 Google 下一代 AI 架构，赛道匹配度高。
- 为什么能进 Top 8：Google 官方背书可信度高；InfoQ 来源技术深度好；Scion 作为新架构有技术圈传播势能。
- 为什么被放下：与 #5（Google MCP Colab）同为 Google 官方技术发布，赛道重叠；补证截图优先级低于#5。
- 能否捞回：可以 — 若前5中任一补证失败或开发者平台有余槽。
- 捞回条件：补 InfoQ 原文截图 + GitHub/demos 链接到位后自动激活。

### Holdout 8｜Sam Altman 袭击事件（合并 #11/#12）

- 一句话判断：P2；高热事件，双重覆盖（#11 Molotov + #12 Firebomb）。
- 为什么能进 Top 8：OpenAI CEO 安全事件具备极高新闻性；双重来源增强可信度。
- 为什么被放下：已被 #4（OpenAI Altman袭击）完全覆盖；保留则造成平台内容重复；与 #4 合并为同一对象处理。
- 能否捞回：可以 — 若 #4 补证撞车或平台需要双角度覆盖，可重新拆分为两条处理。
- 捞回条件：NYT 正文截图到位后与 #4 合并或拆分均可。

---

*topic-planner | 2026-04-12 09:30 CST*
*Top8→Top5板：continuity_only | mini_slate前8 | ai_morning_brief_20260412已单独进publish queue，不在本板范围*

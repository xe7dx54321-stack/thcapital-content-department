# 平台任务单

- `date`: `2026-04-28`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-28 16:10 CST`
- `input_pack`: `/03_topic_candidates/20260428__top20-screening-pack.md`
- `input_top5_board`: `/03_topic_candidates/20260428__daily-top8-to-top5.md`
- `input_scorecard`: `/10_logs/20260428__top20__stage-gate-scorecard.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `rework + continuity_only limited task sheet：wechat 最多 2 个主槽位，另外最多 2 个平台各 1 个 active slot，其余全部 holdout`
- `platform_slots_available`: `wechat×2 + 任意×2 = 4 active slots`

## 全局主池 Top6（可追溯至当日 Top5/Holdout 板）

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | `openai_platform_ecosystem_20260428` | P0 continuity；平台级 AI 中间层生态重磅变化 | 跨中美科技圈同步，HN/微信/知乎均已跟进，影响 agent/builder 基础设施层 | 官方原文细节待确认；微软声明需回链 |
| 2 | `openai_agent_first_20260428` | P0 continuity；Altman+Brockman 十年首次同台，Agent 优先战略关键信号 | OpenAI 最高管理层一手表态，对 Agent 赛道有风向标意义 | 目前只有微信媒体 relay，需回链原始访谈 |
| 3 | `stripe_agent_payment_20260428` | P1 continuity；Agent into production 必须解决支付问题 | Stripe 行业标杆案例，有截图有步骤，可作 Agent 商业化实操参考 | Stripe 官方博客原文深度更强，微信版是压缩解读 |
| 4 | `xiaomi_deepseek_luofuli_20260428` | P1 continuity；中国 AI 开源竞争格局重磅更新 | 罗福莉+小米自研模型，双媒体验证，中国开源 AI 主线强关联 | "超越 DeepSeek-V4" 来自厂商自述，Benchmark 数据待官方验证 |
| 5 | `openai_sora_shutdown_20260428` | Holdout continuity备选；AI视频商业化失败典型，Agent优先战略代价 | 叙事完整，悲情色彩强，传播性强，适合做 AI 应用商业化复盘 | 迪士尼10亿订单数字来源待核实；失败原因仍是推测 |
| 6 | `apple_siri_wwdc_20260428` | Holdout continuity备选；全年最重量级苹果+AI事件，WWDC倒计时启动 | ifanr+36kr双信源，传播度高；苹果AI路线图全年持续 | 具体功能细节仍是曝光阶段，官方 WWDC 前不确认 |
| 7 | `feishu_cli_openclaw_20260428` | Holdout continuity备选；中国企业软件+Agent结合重要节点 | 与 OpenClaw 直接关联，工具链实操价值高；飞书官方CLI开源叙事 | 功能介绍为主，硬数据少；需补官方文档链接 |
| — | `meta_manus_deal_blocked_20260428` | **已排除：同题已进入 morning_flash** | morning_flash item 7 已覆盖 "突发！Meta收购Manus被叫停"，不得重复生产 | — |

## 三个最重要平台任务单

> 摘录 top 3 platforms 的 active slot，供参考与快速导航。

### WeChat
- **Task 1**: `openai_platform_ecosystem_20260428` — OpenAI 向所有云厂商开放，微软不再独享
- **Task 2**: `openai_agent_first_20260428` — Altman、Brockman 十年首次同台，Agent 第一优先级

### X / Twitter
- **Task 1**: `stripe_agent_payment_20260428` — 给 AI 配张银行卡：Stripe Agent 支付全景

### 知乎
- **Task 1**: `xiaomi_deepseek_luofuli_20260428` — 罗福莉交出小米最强开源模型，超越 DeepSeek-V4

---

## 六个主战场任务单

### `wechat`

#### Task 1
- `topic_key`: `openai_platform_ecosystem_20260428`
- `目标读者`: 科技从业者、AI 开发者、关注中美 AI 竞争的投资者与创业者的混合受众
- `切入角度`: 以"微软+OpenAI 独享协议终结"为入口，拆解 AI 中间层格局重塑对 Agent 开发者和独立 SaaS 的深远影响
- `核心论点`: OpenAI 向所有云厂商开放意味着 AI 能力供给侧竞争加剧，中间层溢价压缩，Agent 开发者的选择权扩大；这是中国 AI 厂商需要严肃对待的信号
- `证据抓手`: 微信媒体首发原文 + 待补 OpenAI 官方声明 + 待补 Microsoft 官方声明
- `source_ref_bundle`: `/02_topic_radar/source_packets/20260428*openai_platform*`
- `视觉建议`: 信息图：OpenAI 新生态格局 vs 旧微软独享格局对比；时间线：关键事件节点
- `为什么适合该平台`: 微信是中美科技叙事交汇最强渠道，平台受众对 AI 基础设施变化高度敏感；完整叙事适合长文承载

#### Task 2
- `topic_key`: `openai_agent_first_20260428`
- `目标读者`: AI 开发者、创业者和关注 OpenAI 战略方向的受众
- `切入角度`: Altman+Brockman 十年首次同台的背后——Sora 不是输给了竞品，是 Agent 战略赢了产品优先级；拆解 OpenAI 的战略转向逻辑
- `核心论点`: OpenAI 砍掉 Sora 不是因为它不够好，而是 Agent 已经定义为比视频生成更核心的十年押注；这给所有 AI 应用开发者一个明确的信号：基础设施层的 Agent 能力才是下一个主战场
- `证据抓手`: 微信媒体 relay + 待补 OpenAI 官方访谈视频/博客原文
- `source_ref_bundle`: `/02_topic_radar/source_packets/20260428*openai_agent_first*`
- `视觉建议`: 关键引语金句海报；OpenAI 战略优先级对比图（Sora vs Agent）
- `为什么适合该平台`: 微信科技受众对 OpenAI 战略分析类内容接受度高，长文能完整承接从事实到判断的完整链路

---

### `x`

#### Task 1
- `topic_key`: `stripe_agent_payment_20260428`
- `目标读者`: 开发者、Agent 构建者、对 AI 商业化感兴趣的技术型受众
- `切入角度`: 一句话：Agent 要 into production，支付是最后一道关；Stripe 用半年搭完了全景
- `核心论点`: Stripe Agent Payment 是目前最完整的 AI Agent 支付解决方案；它的出现意味着 Agent 商业化从"可能"到"可落地"的拐点已到
- `证据抓手`: Stripe 官方博客全文 + API 文档截图（待 signal-scout 补证回链）
- `source_ref_bundle`: `/02_topic_radar/source_packets/20260428*stripe_agent*`
- `视觉建议`: 简洁流程图：Agent 触发支付的关键节点；可做 Thread thread 首帖
- `为什么适合该平台`: X/Twitter 是开发者社区，Stripe 支付 API 受众对工具链实操内容天然友好；Thread 形式适合分步骤拆解

---

### `zhihu`

#### Task 1
- `topic_key`: `xiaomi_deepseek_luofuli_20260428`
- `目标读者`: AI 技术爱好者、关注中国大模型竞争的技术从业者和投资者
- `切入角度`: 小米+罗福莉能否真的超越 DeepSeek-V4？从 benchmark 话语权看中国开源模型竞争格局
- `核心论点`: 小米开源模型首日适配 5 家国产芯片是国产 AI 生态整合的里程碑；但"超越 DeepSeek-V4"的宣称需要独立验证，Benchmark 透明度是关键；这背后是中国开源 AI 从追赶到定义标准的野心
- `证据抓手`: 待补罗福莉官方发布会链接 + benchmark 原始论文页；双媒体（zhidx + founder_park）交叉验证
- `source_ref_bundle`: `/02_topic_radar/source_packets/20260428*xiaomi_deepseek*`
- `视觉建议`: 表格：主流中国开源模型 benchmark 对比；适合知乎的长表格+分析格式
- `为什么适合该平台`: 知乎受众对模型性能对比和技术深度分析接受度高；技术派读者对 benchmark 争议本身感兴趣

---

### `xiaohongshu`

> **无 active slot**：Top5/Holdout 板无小红书平台高度适配的候选（xiaomi_deepseek_luofuli 可考虑但优先级低于知乎 slot）。本轮不开 active slot，保留为 holdout 可捞回方向。

---

### `bilibili`

> **无 active slot**：无高度适配 bilibili 视频叙事的候选（stripe_agent_payment 适合但 X slot 优先级更高）。本轮不开 active slot，保留为 holdout 可捞回方向。

---

### `toutiao`

> **无 active slot**：头条号侧重资讯分发，Top5 候选均为解读型内容而非突发快讯。本轮不开 active slot。

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: 否
- `理由`: 今日 Top5 候选均为解读/分析型内容（生态变化、战略转向、商业化路径），而非热搜型突发新闻；SEO 镜像层价值有限，暂不单独立题
- `承接哪篇主稿更优`: 若后续 signal-scout 补证后 `openai_platform_ecosystem` 或 `meta_manus_deal_blocked` 出现可验证的硬数据，可升格进入 baijiahao SEO 镜像层

---

## Holdout 清单

### `meta_manus_deal_blocked_20260428`
- **为什么入围**：跨境 AI 收购监管重磅案例，HN/TechCrunch/微信三方同步，中美科技叙事交汇点
- **为什么落选**：同题已进入 morning_flash（item 7），避免重复生产
- **捞回条件**：若 morning_flash 因补证不足无法落地，或老板特别要求，可在 T+1 日以"续"形式从 holdout 捞回，需重新过 scorecard

### `openai_sora_shutdown_20260428`
- **为什么入围**：AI 视频商业化失败典型，Agent 优先战略代价；叙事完整，悲情色彩强，传播性强
- **为什么落选**：本轮 limited slot 已满（4 slots 全部占满），且数据硬度不足（迪士尼 10 亿订单来源待核实）
- **捞回条件**：若任一 active slot 补证失败、撞车或内容展开明显不足，按原题接力；优先从 wechat Task 2（openai_agent_first）相关性最强的 sora 上下文切入

### `apple_siri_wwdc_20260428`
- **为什么入围**：全年最重量级苹果+AI 事件；ifanr+36kr 双信源，传播度高
- **为什么落选**：WWDC 具体功能细节仍是曝光阶段，官方 WWDC 前不确认；证据硬度不足以支撑今日发布；且 Apple 叙事与同行资本 agent/builder 主线关联度偏弱
- **捞回条件**：WWDC 正式宣布后（T+30~60 天），若功能细节超预期可立即捞回；届时需 signal-scout 重补 scorecard

### `feishu_cli_openclaw_20260428`
- **为什么入围**：中国企业软件+Agent 结合重要节点；与 OpenClaw 直接关联，工具链实操价值高
- **为什么落选**：功能介绍型内容，硬数据少；平台适配上更适合 X/知乎不适合 wechat；本轮 limited slot 已满
- **捞回条件**：若飞书 CLI 获得实质性用户增长数据或重量级开发者社区反响，按原题接力；建议优先考虑 X 平台 slot

---

## 任务单元数据

- `total_active_slots`: `4`
- `wechat_slots_used`: `2`
- `x_slots_used`: `1`
- `zhihu_slots_used`: `1`
- `xiaohongshu_slots_used`: `0`
- `bilibili_slots_used`: `0`
- `toutiao_slots_used`: `0`
- `holdout_count`: `5`（含 1 个 morning_flash 排除项）
- `morning_flash_overlap_excluded`: `meta_manus_deal_blocked_20260428`
- `continuity_discipline`: `所有 active slot 均直接回链当日 Top5/Holdout 板候选，无临时扩题`

---

*topic-planner | 2026-04-28 16:10 CST | day_mainline limited task sheet | stage_gate_status=continuity_only*

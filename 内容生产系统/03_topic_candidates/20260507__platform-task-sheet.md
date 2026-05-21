# 平台任务单

- `date`: `2026-05-07`
- `owner`: `topic-planner`
- `generated_at`: `2026-05-07 19:49:00 CST`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260507__daily-top8-to-top5.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `continuity_only limited task sheet：wechat 2 slots；其余每个平台先保 1 个 active slot；候选全回链 Top5/Holdout 板`
- `top5_board`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260507__daily-top8-to-top5.md`
- `top5_board_state`: `final`
- `morning_flash_exclusion_applied`: `true`
- `morning_flash_bundle`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260507__morning-flash-source-bundle.md`（4 items：MCP UI / Perplexity AI search / Gemini 2.5 / Gemini CLI — 均与 Top5 候选无重叠，已排除）
- `continuity_note`: `本单为 continuity_only 纪律执行；所有 active slot 均回链 Top5/Holdout 板候选，补证纪律严格不绕过`

## 全局主池 Top6

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | deepseek-first-investment-45b | 大金额融资 + 中国AI叙事 + 高讨论度，触及 financing/newco 核心 | $45B 首轮融资估值，叙事空间大，平台关注度高 | 官方尚未确认；估值消息可能变动 |
| 2 | spacex-terafab-119b-texas | 超大金额芯片厂投资，触及 AI infra + 硬件 + Musk 生态三条主线 | 高金额异常事件，AI infra 硬基建叙事强 | 提案阶段；落地存在重大不确定性 |
| 3 | arden-ai-audit-yc-launches | YC Spring 2026，Finance+AI+Audit 方向稀缺，信号干净 | 官方 launch，审计+AI 落地热门方向，时间新鲜 | Launch 页不等于产品成熟；需补官网产品验证 |
| 4 | pavoot-event-experiences-yc-launches | YC Spring 2026，82票当天最高，活动 AI + SaaS 有商业化叙事空间 | 社区高关注，票数最高，商业化角度有差异 | Launch 页不等于产品验证；需补实际活动案例 |
| 5 | bitboard-analytics-agents-yc-launches | YC 官方，Agent+Analytics 赛道明确，适合技术内容线 | 品牌贴合度高，赛道方向稀缺 | Batch 为 Spring 2025 已一年，票数极低；需确认产品状态 |
| 6 | *(空缺 — 5 个有效候选；6 号位供 holdout 候选未来激活)* | | | |

## 六个主战场任务单

### Wechat

#### Task 1
- `topic_key`: `deepseek-first-investment-45b`
- `目标读者`: 关注 AI 投资、硬科技创投的从业者与爱好者；对中国 AI 叙事感兴趣的泛科技读者
- `切入角度`: 不做故事包装，重点判断这种小团队高估值模式的成立前提、边界与可复制性；结合 DeepSeek 技术背景与当前融资环境做结构化分析
- `核心论点`: DeepSeek 首轮即冲击 $45B 估值，是当前 AI 赛道融资泡沫的典型切片，也是小团队「技术叙事的杠杆效应」的现实教材
- `证据抓手`: TechCrunch 原文 + 任何后续跟进确认；正文必须注明「官方尚未确认」
- `source_ref_bundle`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260507_082129__techcrunch_ai_deepseek_could_hit_45b_valuation_from_its_first_investment_round__source-packet.md`
- `视觉建议`: 信息图风格：估值数字 + 团队规模对比 + 同类 AI 融资对照；避免过度包装
- `为什么适合该平台`: financing/newco 完整叙事最优平台；DeepSeek 高讨论度+大金额+中国AI三角结合，天然适合公众号深度分析体裁

#### Task 2
- `topic_key`: `spacex-terafab-119b-texas`
- `目标读者`: 关注 AI 基建、芯片投资、Musk 生态的科技从业者
- `切入角度`: 以事件为入口，深挖：这个信号对 agent/builder/一人公司主线的战略含义，以及 SpaceX 芯片自造计划与当前 AI 算力格局的关系
- `核心论点`: $119B Terafab 计划是 SpaceX 试图将 AI 基建纵向整合的里程碑事件，是 AI 硬件自主化的重要信号
- `证据抓手`: TechCrunch 原文 + 任何官方公告或财报披露；正文必须标注「提案阶段，落地存在不确定性」
- `source_ref_bundle`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260507_082129__techcrunch_ai_spacex_may_spend_up_to_119b_on_terafab_chip_factory_in_texas__source-packet.md`
- `视觉建议`: 数字驱动型封面：$119B vs. 当前芯片厂投资中位线对比；Musk 生态关联图
- `为什么适合该平台`: 超大金额 + AI infra + Musk 流量三重叠加，微信平台最适合承接结构化分析

### Xiaohongshu

#### Task 1
- `topic_key`: `arden-ai-audit-yc-launches`
- `目标读者`: 关注 AI 落地应用、创业机会的年轻从业者与投资人
- `切入角度`: 「审计 + AI」为什么是下一个 AI 应用落地金矿？从 YC 新项目看 AI 垂直行业的工具化机会
- `核心论点`: 审计行业 AI 工具化是未被充分发掘的蓝海，Arden 代表了一种「AI-native audit tool」的新范式
- `证据抓手`: YC 官方 Launch 页面 + 审计行业数字化报告引用（如有）
- `source_ref_bundle`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260507_082220__arden__asset-chain.md`
- `视觉建议`: 轻量图文；「YC 审计 AI」关键词突出；可用 before/after 审计流程对比
- `为什么适合该平台`: 小红书对 YC 新项目有天然好奇心，审计+AI切入角度有猎奇感与实用感双重价值

### Zhihu

#### Task 1
- `topic_key`: `pavoot-event-experiences-yc-launches`
- `目标读者`: 对 AI SaaS、商业化机会感兴趣的产品/运营从业者与投资人
- `切入角度`: 活动策划是一个被低估的 AI 落地场景；YC 最高票项目 Pavoot 的商业逻辑拆解
- `核心论点`: 活动体验→成交漏斗，AI 在 B2B event 场景的商业化路径清晰；Pavoot 票数最高背后的逻辑值得深挖
- `证据抓手`: YC 官方 Launch 页面 + Pavoot 官网产品截图（content-writer 补证）
- `source_ref_bundle`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260507_082222__pavoot__asset-chain.md`
- `视觉建议`: 清单体或对比图；知乎用户偏好结构化干货，信息密度高
- `为什么适合该平台`: 知乎擅长「拆解类」回答，Pavoot 票数最高现象值得从社区产品逻辑角度展开分析

### X

#### Task 1
- `topic_key`: `pavoot-event-experiences-yc-launches`
- `目标读者`: 关注 AI SaaS、商业化机会的从业者；YC 社区观察者
- `切入角度`: 快讯 + 观点钩子：YC 当天最高票项目 Pavoot，活动 AI 为什么值得关注
- `核心论点`: 活动体验→成交漏斗，AI 在 B2B event 场景的商业化路径清晰；Pavoot 票数最高背后的逻辑值得深挖
- `证据抓手`: YC 官方 Launch 页面 + Pavoot 官网（content-writer 补证）
- `source_ref_bundle`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260507_082222__pavoot__asset-chain.md`
- `视觉建议`: 短图文；YC 票数截图 + Pavoot 产品关键词放大
- `为什么适合该平台`: X 是 YC 项目传播放大器；快讯+观点形式最适配 X 的信息流节奏

### Bilibili

#### Task 1
- `topic_key`: `bitboard-analytics-agents-yc-launches`
- `目标读者`: 关注 AI agent、编程工具、开发者生态的 B站用户
- `切入角度`: 「给 AI 做的数据分析工具长什么样？」— BitBoard 的 agent-native analytics 方向解读
- `核心论点`: Agent + Analytics 是 AI native 工具链中尚未被充分讨论的方向；BitBoard 代表一种新工具范式
- `证据抓手`: YC 官方 Launch 页面 + bitboard.work 官网截图（content-writer 补证；若产品已下线则降 holdout）
- `source_ref_bundle`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260507_082213__bitboard__asset-chain.md`
- `视觉建议`: 工具演示风格截图 + 字幕解说；B站用户对「给 AI 用的工具」有技术好奇心
- `为什么适合该平台`: B站用户对技术工具向内容接受度高，Agent+Analytics 是新锐方向，有科普价值

### Toutiao

（本期 no active slot — 5 个候选已全部分配；toutiao 可作为 holdout 候选的激活备选平台）

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **否**
- `理由`: 本日 Top5 候选（DeepSeek/SpaceX/Arden/Pavoot/BitBoard）均为新事件或 YC 新项目，百家号 SEO 价值尚未形成搜索惯性；待其中某条经微信验证获得高阅读量后，再判断是否值得建立 SEO 镜像层
- `承接哪篇主稿更优`: 若未来激活，优先承接 DeepSeek 或 SpaceX 主稿（搜索引擎关注度高）

## 三个最重要平台任务单

### `wechat`

#### Task 1（优先级最高）
- `topic_key`: `deepseek-first-investment-45b`
- `目标读者`: 关注 AI 投资、硬科技创投的从业者与爱好者；对中国 AI 叙事感兴趣的泛科技读者
- `切入角度`: 不做故事包装，重点判断这种小团队高估值模式的成立前提、边界与可复制性；结合 DeepSeek 技术背景与当前融资环境做结构化分析
- `核心论点`: DeepSeek 首轮即冲击 $45B 估值，是当前 AI 赛道融资泡沫的典型切片，也是小团队「技术叙事的杠杆效应」的现实教材
- `证据抓手`: TechCrunch 原文 + 任何后续跟进确认；正文必须注明「官方尚未确认」
- `source_ref_bundle`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260507_082129__techcrunch_ai_deepseek_could_hit_45b_valuation_from_its_first_investment_round__source-packet.md`
- `视觉建议`: 信息图风格：估值数字 + 团队规模对比 + 同类 AI 融资对照；避免过度包装
- `为什么适合该平台`: financing/newco 完整叙事最优平台；DeepSeek 高讨论度+大金额+中国AI三角结合，天然适合公众号深度分析体裁

#### Task 2（优先级次高）
- `topic_key`: `spacex-terafab-119b-texas`
- `目标读者`: 关注 AI 基建、芯片投资、Musk 生态的科技从业者
- `切入角度`: 以事件为入口，深挖：这个信号对 agent/builder/一人公司主线的战略含义，以及 SpaceX 芯片自造计划与当前 AI 算力格局的关系
- `核心论点`: $119B Terafab 计划是 SpaceX 试图将 AI 基建纵向整合的里程碑事件，是 AI 硬件自主化的重要信号
- `证据抓手`: TechCrunch 原文 + 任何官方公告或财报披露；正文必须标注「提案阶段，落地存在不确定性」
- `source_ref_bundle`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260507_082129__techcrunch_ai_spacex_may_spend_up_to_119b_on_terafab_chip_factory_in_texas__source-packet.md`
- `视觉建议`: 数字驱动型封面：$119B vs. 当前芯片厂投资中位线对比；Musk 生态关联图
- `为什么适合该平台`: 超大金额 + AI infra + Musk 流量三重叠加，微信平台最适合承接结构化分析

### `xiaohongshu`

#### Task 1（第三个最重要平台 slot）
- `topic_key`: `arden-ai-audit-yc-launches`
- `目标读者`: 关注 AI 落地应用、创业机会的年轻从业者与投资人
- `切入角度`: 「审计 + AI」为什么是下一个 AI 应用落地金矿？从 YC 新项目看 AI 垂直行业的工具化机会
- `核心论点`: 审计行业 AI 工具化是未被充分发掘的蓝海，Arden 代表了一种「AI-native audit tool」的新范式
- `证据抓手`: YC 官方 Launch 页面 + 审计行业数字化报告引用（如有）
- `source_ref_bundle`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260507_082220__arden__asset-chain.md`
- `视觉建议`: 轻量图文；「YC 审计 AI」关键词突出；可用 before/after 审计流程对比
- `为什么适合该平台`: 小红书对 YC 新项目有天然好奇心，审计+AI切入角度有猎奇感与实用感双重价值

## Holdout 清单

### `spacex-terafab-119b-texas`（平台分配说明）
- `为什么能进最终池`: 超大金额芯片厂投资，触及 AI infra + 硬件 + Musk 生态三条主线，高信号事件
- `平台分配状态`: wechat Task 2（深度分析）+ X Task 1（快讯）双平台覆盖，无需捞回
- `什么时候可捞回`: 不适用；已获双平台 slot

### `pavoot-event-experiences-yc-launches`
- `为什么能进最终池`: YC Spring 2026，82票当天最高，社区高关注，活动AI+SaaS有商业化叙事空间
- `为什么这轮没选`: wechat 2 slots + XHS 1 + ZH 1 + X 1 + Bilibili 1 = 6 slots，pavoot 已在 ZH slot 和 X slot 双平台覆盖，已达到合理曝光
- `什么时候可捞回`: 若知乎 slot 空出（候选补证失败降级），pavoot 已在 ZH 和 X 双平台，无需额外捞回

### `bitboard-analytics-agents-yc-launches`
- `为什么能进最终池`: YC 官方，Agent+Analytics 赛道方向明确，品牌贴合度高，适合技术内容线
- `为什么这轮没选`: Bilibili slot 已激活 BitBoard；但需先补产品状态验证（Spring 2025 已一年）
- `什么时候可捞回`: (1) content-writer 确认 bitboard.work 官网产品仍活跃；(2) 若 Bilibili slot 候选补证失败降级，BitBoard 顶替

---

## 平台 slot 总览

| 平台 | slot 1 | slot 2 | 状态 |
|------|--------|--------|------|
| wechat | DeepSeek $45B | SpaceX $119B Terafab | ✅ active |
| xiaohongshu | Arden AI Audit | — | ✅ active |
| zhihu | Pavoot 活动 AI | — | ✅ active |
| x | Pavoot 活动 AI | — | ✅ active |
| bilibili | BitBoard Analytics | — | ✅ active（待产品状态补证） |
| toutiao | — | — | ⏸ holdout（无候选） |
| baijiahao | — | — | ⏸ SEO 镜像待微信稿验证后决策 |

---

*Platform Task Sheet | topic-planner | 2026-05-07 16:40 CST*
*Input: Top5 board final + Top20 scorecard final（continuity_only）| Morning flash exclusion applied | No cross-contamination*
# Stage Gate Scorecard

- `date`: `2026-04-05`
- `stage`: `top20`
- `owner`: `market-editor`
- `delivery_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260405__top20-screening-pack.md`
- `redteam_review`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260405__top20__redteam-review.md`
- `generated_at`: `2026-04-05 15:19 CST`

## 裁判结论

- `score`: `7.0`
- `status`: `rework`
- `status_rule`: `status 只允许写 pass 或 rework；若进入 continuity lane，也仍写 rework，并把 continuity 结果写进下方两个字段`
- `rework_mode`: `supplement_evidence`
- `是否保留原对象`: `yes`
- `topic_value_judgment`: `高`
- `execution_readiness`: `暂不可发`
- `continuity_decision`: `continuity_only`
- `continuity_output`: `top20_mini_slate`
- `continuity_rule`: `Top20 <8 且非 truth failure 时默认写 continuity_only，并优先产出 top20_mini_slate；platform-task <8 且非 truth failure 时默认写 continuity_only，并优先产出 limited_task_sheet`
- `是否进入下一工序`: `否 — 需 signal-scout 补证后复评，continuity 解锁 Top5 mini_slate`

---

## 评分理由

### 做得好的地方

1. **GLM-5 YC-Bench（#1，26分）**：今日 pack 中证据链最完整的候选，有 arxiv paper + GitHub 代码库 + 完整 leaderboard，是真实的一手高价值锚点。
2. **Claude Code 23年漏洞（#2，24分）**：HN 头条 + GitHub Trending 双平台，有真实 CVE 信号，一手性强。
3. **Anthropic $400M Coefficient Bio（#3，24分）**：TechCrunch 确认报道，硬数据，赛道意义清晰。
4. **Anthropic OpenClaw 定价变更（#4，22分）**：TechCrunch 原文已读取，有 Boris Cherny 和 Peter Steinberger 两条官方 X 链，证据链完整。
5. signal-scout 的 rework_note 如实记录了两次自我修正（升格 Anthropic OpenClaw 定价、移除 Week 14 重复条目），体现了 scouter 的修正意识，值得保留。
6. supply_risk 对 LM Studio Malware 候选的降格处理正确 — 未证实单一指控不上升为主流叙事，决策合理。

---

### 当前主要缺口

**不是 truth failure，是 evidence gap + ranking logic error：**

1. **P1（严重）**：三条下午新增 Reddit 裸帖（Qwen3.6 25分 / DGX Spark 23分 / Gemma 4 31B 22分）排在 pack 前三位，但这三者均为单一 Reddit 帖，无官方来源、无硬数据，证据链未闭合。排序虚高将误导 content-writer 优先处理不可发对象。

2. **P2（合规阻断）**：#7、#8、#11 三个条目原始链接缺失（标注为省略号链路），违反模板"每个候选必须有原始链接"的最低合规门槛。

3. **P3（留痕缺失）**：supply_risk 的"双车道隔离合规"声明无证据支撑；morning_flash 与 day_mainline 同题角度分析未落文字。

4. **M1（需确认）**：Gemma 4 31B FoodTruck Bench 内容方向存疑 — pack 描述为"benchmark 第三名"，redteam 读取原帖发现为差评翻译帖，方向矛盾。

---

### 为什么是这个分数

- 7.0 分对应"高 topic value + 暂不可 execution"状态。
- 高分对象（GLM-5 YC-Bench / Claude Code CVE / Anthropic 两题）都是真实强候选，redteam 未指控任何事实失真或方向偏航。
- 扣分集中在三点：top3 排序逻辑矛盾（P1）、模板合规违规（P2）、监管留痕缺失（P3）。
- **不是 truth failure**，因此允许 continuity_only，不走 stop_for_truth。

---

### 先改什么

1. top3 三条 Reddit 帖的证据补强（官方来源或改角度降格为"舆情题"）
2. #7/#8/#11 原始链接补链
3. supply_risk 补充 morning_flash/day_mainline 同题角度分析留痕

### 后改什么

4. 重审 Gemma 4 31B FoodTruck Bench 内容方向，若与原描述不符，以实际内容修正 signal_summary
5. 重排 top3 must_watch 顺位说明（GLM-5 有硬数据应升第一位）

---

## 若打回，必须修的三件事

1. **Qwen3.6 / DGX Spark / Gemma 4 31B 证据补强**：48h 内搜索阿里官方 blog / NVIDIA 声明 / benchmark 原始链接；若补不到官方来源，改写标题措辞为"舆情视角"而非"事件确认"，并在 signal_summary 中写清楚这是单一用户体验、不是硬事实。
2. **#7/#8/#11 原始链接全量回填**：signal-scout 补链三步完成后，否则这三个条目不得进入任何平台任务单。
3. **supply_risk 补充双车道合规留痕**：写清今日 morning_flash 命中 anthropic-openclaw 主题（角度A），day_mainline 命中同一主题（角度B），两者角度不同、分工合规。

---

## 返工顺序说明

- **先补证还是先换题**：`先补证`，不先换题。所有高价值对象均值得保留，问题在呈现与证据链，不在对象本身。
- **是否允许补证后原对象复评**：`yes`
- **若建议换题，触发条件**：若 Qwen3.6 48h 内仍无阿里官方回应，且改角度（舆情题而非事件确认）后仍无高置信锚点；或若 Gemma 4 31B FoodTruck Bench 确认内容方向与 pack 描述相反且无法修正。

---

## Continuity 产出：Top20 Mini Slate（Top5 高置信候选）

以下 5 个对象具有完整或接近完整的证据链，可在日间主线继续推进，无需等待完整 pack 复评：

| 排名 | topic_key | 标题 | 置信度 | 说明 |
|------|-----------|------|--------|------|
| #1 | `glm5_benchmark_yc_bench` | GLM-5 nearly matched Claude Opus 4.6 at 11× lower cost | 高 | arxiv + GitHub + leaderboard 三件套 |
| #2 | `claude_code_cve_2023` | Claude Code 23年漏洞 / GitHub Trending | 高 | HN 头条 + GitHub CVE，双平台确认 |
| #3 | `anthropic_400m_coefficient_bio` | Anthropic $400M Coefficient Bio | 高 | TechCrunch 硬数据确认 |
| #4 | `anthropic_openclaw_pricing_change` | Anthropic charges extra for OpenClaw Claude Code usage | 高 | TechCrunch + 双官方 X 链 |
| #5 | `nvidia_robotics_physical_ai` | National Robotics Week Physical AI 研究 | 中高 | NVIDIA 官方博客一手，Physical AI 赛道价值清晰 |

**不进入 mini_slate 但保留在 pack 的条目**：
- Qwen3.6 / DGX Spark / Gemma 4 31B → 降格为"待补证热帖"，补证完成后可重新进入评估
- YC Launch 候选（#12-15, #17-19）→ 等待一跳派生链接补链
- 链接缺失条目（#7, #8, #11）→ 补链完成后复评

---

## morning_flash 已锁题排除声明

- 今日 morning_flash 候选题：`anthropic-openclaw-block-third-party-harness-2026`（角度：Anthropic封杀OpenClaw等第三方harness，引爆开发者圈）
- day_mainline pack `#4 Anthropic charges extra for OpenClaw Claude Code usage`（角度：TechCrunch 报道的额外收费争议）
- **两者同一主题、不同角度**，分工合规，各走各道。但 supply_risk 需补充这条分析留痕（P3 必须修）。

---

## 若放行，进入下一步的明确动作

> 本轮不放行。以下为 continuity 状态下的最低推进指引。

- `next_owner`: `market-scout / signal-scout`
- `next_output`: `Top20 补证包（仅针对 top5 mini_slate 高置信候选以外的条目）`
- `deadline_or_expectation`: `signal-scout 需在 2026-04-06 12:00 CST 前完成 P1/P2 补证并将结果回填 pack；同期完成 P3 supply_risk 留痕`
- `continuity_note`: `日间主线的 platform task sheet 允许基于 mini_slate Top5 先行锁题，不必等待完整 Top20 pack 复评；其余条目走 rework backlog`

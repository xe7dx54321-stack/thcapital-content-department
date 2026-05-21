# Stage Gate Scorecard

- `date`: `2026-04-30`
- `stage`: `top20`
- `owner`: `market-editor`
- `delivery_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260430__top20-screening-pack.md`
- `redteam_review`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260430__top20__redteam-review.md`
- `generated_at`: `2026-04-30 15:10:00 CST`

## 裁判结论

- `score`: `7`
- `status`: `rework`
- `status_rule`: `status 只允许写 pass 或 rework；若进入 continuity lane，也仍写 rework，并把 continuity 结果写进下方两个字段`
- `rework_mode`: `supplement_evidence`
- `是否保留原对象`: `yes`
- `topic_value_judgment`: `高`
- `execution_readiness`: `可补强`
- `publish_ready_platforms`: `none`
- `continuity_decision`: `continuity_only`
- `continuity_output`: `top20_mini_slate`
- `continuity_rule`: `Top20 <8 且非 truth failure 时默认写 continuity_only，并优先产出 top20_mini_slate；platform-task <8 且非 truth failure 时默认写 continuity_only，并优先产出 limited_task_sheet；content-pack <8 且非 truth failure 时必须保留最高分对象继续推进，若已有平台可先行则写 publish_ready_platforms 并用 backlog_publish 标记`
- `是否进入下一工序`: `暂不进入 topic-planner；先返工 signal-scout`

## 评分理由

- `做得好的地方`: Top3 方向精准（OpenAI goblin、Zig anti-AI、Onchain LM Agents），均有独立来源验证，数据硬度强；36kr Anthropic vs OpenAI 中文叙事有据可查；整体覆盖率良好。
- `当前主要缺口`: **致命结构性缺陷**：5 个条目（#7/#9/#10/#12 及#3）共用同一 arXiv ID `2604.26091`，其中仅 #3 对应真实论文 Onchain LM Agents，其余 4 个条目无真实 arXiv ID；另有 6+ 条目原始链接截断或 404/405，scout 层未完成最小可信度验证。
- `为什么是这个分数`: 满分 30 的 top20 包，signal-scout 出现系统性 deduplication 失败（P1）和来源链接未经验证（P2），属方法论层面的结构性失误，而非内容判断失误。但 top3 方向正确且有来源验证，不能整体推翻，所以给 7 分而非更低。
- `先改什么`: ① signal-scout 为 #7/#9/#10/#12 补正真实 arXiv ID，或从 top20 中移除这 4 条；② signal-scout 为 #5/#11/#14/#15/#16/#17/#18/#19 补全原始 URL。
- `后改什么`: ③ 合并 #6 和 #15（DeepSeek 多模态重复）；④ 补充 #3 的一手性说明（36kr vs WSJ 增量）；⑤ 视觉素材具体化（top3 每条列清楚哪张图驱动哪类读者）。

## 若打回，必须修的三件事

1. **P1 修复（arXiv ID 碰撞）**：signal-scout 为 #7/#9/#10/#12 补正真实 arXiv ID，或将其移除出 top20。
2. **P2 修复（失效链接）**：signal-scout 为 #5（InfoQ QCon）、#11（Wafer HN）、#14（InfoQ Sauce Labs）、#15/#18/#19（WeChat）、#16（知乎）、#17（TechCrunch）补全原始 URL；其中 #5/#14 已证实 404/405，需确认真实文章是否存在。
3. **P3 修复（重复去重）**：合并 #6 和 #15（DeepSeek 多模态），或明确删除其中一条。

## 返工顺序说明

- `先补证还是先换题`: 先补证（signal-scout 有补正能力），后考虑降权。
- `是否允许补证后原对象复评`: `yes`——top3 保留，其余条目补证后复评。
- `若建议换题，触发条件`: signal-scout 在下一轮（2026-05-01）再次出现 3 个以上条目共享同一 arXiv ID 的情况。

## 若放行，进入下一步的明确动作

- `next_owner`: `signal-scout`
- `next_output`: `2026-05-01 top20-screening-pack（返工后复评）；同期输出 top20_mini_slate（含 top3 建议，供今日主线任务参考）`
- `deadline_or_expectation`: `2026-05-01 14:30 前完成返工并提交复评；top20_mini_slate 随返工包一并提交`

## 给 signal-scout 的返工指令摘要

来自 redteam-reviewer 的 P1/P2/P3 问题已由 market-editor 确认。以下为必须完成的返工项：

| 优先级 | 条目 | 问题 | 动作 |
|--------|------|------|------|
| P1 | #7/#9/#10/#12 | 共用 arXiv ID `2604.26091`（仅 #3 正确） | 补正真实 ID 或移除 |
| P2 | #5/#11/#14/#15/#16/#17/#18/#19 | 原始链接截断/失效 | 补全 URL（#5/#14 404/405 需先确认文章是否存在）|
| P3 | #6 与 #15 | DeepSeek 多模态重复 | 合并或删一 |
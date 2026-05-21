# Stage Gate Scorecard — Top20 初筛包

- `date`: `2026-04-22`
- `stage`: `top20-screening gate`
- `owner`: `market-editor`
- `delivery_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260422__top20-screening-pack.md`
- `redteam_review`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/08_scorecards/20260422__top20-screening__redteam-review.md`
- `generated_at`: `2026-04-22 11:40:52 CST`

## 裁判结论

- `score`: `6 / 10`
- `status`: `rework`
- `status_rule`: `status 只允许写 pass 或 rework；若进入 continuity lane，也仍写 rework，并把 continuity 结果写进下方两个字段`
- `rework_mode`: `supplement_evidence + clean_pool`
- `是否保留原对象`: `yes`
- `topic_value_judgment`: `中`
- `execution_readiness`: `可补强`
- `publish_ready_platforms`: `none`
- `continuity_decision`: `continuity_only`
- `continuity_output`: `top20_mini_slate`
- `continuity_rule`: `Top20 <8 且非 truth failure 时默认写 continuity_only，并优先产出 top20_mini_slate`
- `是否进入下一工序`: `否 — 打回 market-scout 补证 + 清洗主线无关 Topic，修复后重新提审`

## 评分理由

- `做得好的地方`: top3 候选（豆包千问卡位 Agent、Opus 4.7 工程失分、布林追杀队）均具备高时效性和主线匹配度，top6 strong pool 补充了 HN/Reddit 的社区扩散信号，整体覆盖面合理。
- `当前主要缺口`: 混入主线无关 Topic（#18 医疗社会话题、#3 过时效）损害内容工厂专业过滤水位；大量 partial source 条目缺硬时间戳和回溯标签，无法支撑后续 content-writer 的高质量改写。
- `为什么是这个分数`: top3 质量尚可，但包整体混入了不符合"AI / 科技主线"过滤标准的 Topic，且 evidence chain 不完整，符合"6 分·可补强·打回"的判定边界。
- `先改什么`: 清洗 #18 和 #3，补入候补 Topic。
- `后改什么`: 对 top3 + top6 完成 evidence chain 补证。

## 若打回，必须修的三件事

1. 移除或降权 #18（"11岁女孩188斤"）和 #3（"《封神3》AI 特效"，时效已过），并从 holdout_watchlist 或新候选中补入主线更相关的 Topic。
2. 对 top3 + top6（共 9 个强候选）补证：original_link 硬时间戳 + 回溯标签（从哪个平台、什么时间探测到）。
3. 确保替换进入的候补 Topic 满足：主线相关 + 时效在 4 天内 + 有扩散信号。

## 返工顺序说明

- `先补证还是先换题`: 先清洗，换题优先级高于补证。
- `是否允许补证后原对象复评`: `yes`
- `若建议换题，触发条件`: 补证后若发现任何 top3 条目事实性错误。

## 若放行，进入下一步的明确动作

- `next_owner`: `market-scout + topic-planner`
- `next_output`: `清洗后的 top20_mini_slate（Top 8 -> Top 5 建议单）+ 补证版 source packets`
- `deadline_or_expectation`: `当日 14:30 CST 前完成清洗和补证，以便下午进入选题拍板环节`
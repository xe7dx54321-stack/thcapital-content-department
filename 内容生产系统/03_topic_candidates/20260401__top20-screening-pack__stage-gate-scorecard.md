# Stage Gate Scorecard

- `date`: `2026-04-01`
- `stage`: `top20`
- `owner`: `market-editor`
- `delivery_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260401__top20-screening-pack__reworked.md`
- `redteam_review`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260401__top20__redteam-review.md`
- `generated_at`: `2026-04-01 18:43:00 CST`

## 裁判结论

- `score`: `7.5/10`
- `status`: `rework`
- `status_rule`: `status 只允许写 pass 或 rework；若进入 continuity lane，也仍写 rework，并把 continuity 结果写进下方两个字段`
- `rework_mode`: `supplement_evidence + expand_validation`
- `是否保留原对象`: `yes`
- `topic_value_judgment`: `高`
- `execution_readiness`: `可补强`
- `continuity_decision`: `continuity_only`
- `continuity_output`: `top20_mini_slate`
- `continuity_rule`: `Top20 <8 且非 truth failure 时默认写 continuity_only，并优先产出 top20_mini_slate`
- `是否进入下一工序`: `否 — 修毕后重新评分再判`

## 评分理由

- `做得好的地方`:
  - P1 fabrication 修复完整（$131B/年收入/$20B/月收入/6.5×/40%/9亿/5000万 已全部删除，未残留）
  - Top5 mini_slate 信号极强：#1 OpenAI($1220亿)+#2 Claude Code+#3 Anthropic 三条均来自今日 manifest，source packets 实地可查，质量区间 8.5-9/10
  - #6 OpenSeeker / #8 昆仑行 / #9 智谱 升入正式包，今日 manifest 来源全部确认
  - 旧 P1 fatal 处置正确（#17/#20 replace_topic×2），结构修正完成
  - 6项历史候选 date_notice 如实标注，无"今日实时"失实声明
- `当前主要缺口`:
  - #1 OpenAI signal_summary 仍含一条未溯源领投方（Andreessen），且领投方清单与 TechCrunch primary source 不符（TechCrunch 原文：Amazon+Nvidia+SoftBank，pack 写：软银+Andreessen+亚马逊）
  - #17 YC Unify（Winter 2023）距今2年+，时效偏老；supply_confidence=MEDIUM，官网无实质产品内容
  - #20 KV Cache（future-shock.ai）平台知名度低，无法外部交叉验证
- `为什么是这个分数`: 7.5/10，距8分硬线差0.5分。核心缺口为#1领投方 Andreessen 未溯源（修复后+0.5分可升线）；#17/#20 supply_confidence 中风险通过降排可改善感知。
- `先改什么`:
  1. **修正 #1 OpenAI 领投方清单**：删除 Andreessen Horowitz → "亚马逊+英伟达+软银（金额待披露）"，补 OpenAI 官方博客 source link；同步修正 supplement_evidence 中 Andreessen 相关表述
  2. **降排或强化 YC Unify**：回链 unify.ai 官网截图；若无可验证产品实质，降排至 #19-20
  3. **降排 KV Cache**：移至 #19-20 或改叙事锚点为"LLM推理成本下降趋势"
- `后改什么`:
  4. 补 NVIDIA GTC benchmark 官方链接（#4）
  5. 补工商/财报原文验证（#8 昆仑行 / #9 智谱）

## 若打回，必须修的三件事

1. **【必须】修正 #1 OpenAI 领投方清单**：完全删除 Andreessen Horowitz（TechCrunch/HN 均未出现）；改为"亚马逊+英伟达+软银"；补 OpenAI 官方博客链接；同步修正 supplement_evidence
2. **【必须】YC Unify expand_validation 或降排**：回链 unify.ai 官网截图；若官网无实质产品内容，降排至 #19-20 并在 score_breakdown 注明 supply_confidence=LOW
3. **【必须】KV Cache 降排或改叙事锚点**：降排至 #19-20；或改写为"LLM推理成本下降"趋势锚点，移除对 future-shock.ai 平台可信度的依赖

## 返工顺序说明

- `先补证还是先换题`: 先补证（#1 OpenAI 领投方清单），补证失败则删除Andreessen；再处理 YC Unify 官网验证
- `是否允许补证后原对象复评`: `yes`
- `若建议换题，触发条件`: YC Unify 官网完全无实质产品内容 → replace_topic；KV Cache builder 叙事无法成立 → replace_topic

## 若放行，进入下一步的明确动作

- `next_owner`: `topic-planner`
- `next_output`: `platform-task-sheet（Top5 mini_slate → OpenAI/Claude Code/Anthropic/昆仑行/智谱）`
- `deadline_or_expectation`: 修毕后重新提 scorecard，market-editor 复评 ≥8 分即放行

## Top5 Mini Slate 裁判（正式放行后进入 topic-planner）

| 候选 | 当前状态 | 修复后预期 |
|------|---------|---------|
| #1 OpenAI $1220亿 | ⚠️ 领投方清单需修正 | ✅ 修毕后 9/10 |
| #2 Claude Code | ✅ 无障碍 | ✅ |
| #3 Anthropic 并发周 | ✅ 无障碍 | ✅ |
| #8 昆仑行 | ✅ 今日 manifest | ✅ 补工商验证后 +0.25 |
| #9 智谱财报 | ✅ 今日 manifest | ✅ 补财报原文后 +0.25 |

**Top5 Mini Slate 修复后预期加权：8.5-9/10 → 建议 pass 并进入 topic-planner。**

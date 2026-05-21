# Stage Gate Scorecard

- `date`: `2026-04-20`
- `stage`: `top20-screening`
- `owner`: `market-editor`
- `delivery_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260420__top20-screening-pack.md`
- `redteam_review`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/08_scorecards/20260420__top20-screening__redteam-review.md`
- `generated_at`: `2026-04-20 09:33 CST`

## 裁判结论

- `score`: `7.5`
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
- `是否进入下一工序`: `yes，但需回补证据链`

## 评分理由

- `做得好的地方`:
  - Top 5 候选质量高：DeepSeek V4（国产大模型+算力突围，知乎210万热度）、Claude Design/Figma（AI直接颠覆商业软件首个可量化案例，股价-7%）、HBM短缺（产业叙事转换信号）均具备高传播性和投资相关性
  - 前两名候选（DeepSeek V4、RAM短缺）形成了逻辑呼应：「国产算力突围」与「全球算力瓶颈」形成投资叙事双线
  - 候选3（Palantir DEI宣言）争议性强，适合多平台改写
  - 市场scout在周末窗口期捕获22个新packet，过滤逻辑有效

- `当前主要缺口`:
  - 多条候选处于「网传/未官宣」阶段，一手信息需要回链补证
  - 部分候选视觉素材标记「待补」，需asset chain补查
  - 候选间存在逻辑关联但未在包内显式标注（DeepSeek V4 ↔ RAM短缺 ↔ 国产芯片突围）

- `为什么是这个分数`:
  - 7.5分反映：候选质量高、方向准确，但多条候选处于「快照层」而非「可执行层」
  - 距离8分只差「一手证据链补齐」一步，不建议换题
  - 「去CUDA化」和「Claude Design颠覆Figma」属于2026年AI领域最硬主线，不容错过

- `先改什么`:
  1. DeepSeek V4：回链官方信源（GitHub/官网/权威媒体），确认为官方口径还是网传
  2. Claude Design/Figma：补充一手产品截图和Figma官方回应
  3. 所有「待补」视觉素材：触发 asset chain 查询

- `后改什么`:
  - 在 Top20 包内标注候选间的逻辑关联，形成叙事矩阵
  - 对低分候选（15分以下）做二次筛选，识别可丢弃对象

## 若打回，必须修的三件事

1. **P1：DeepSeek V4 一手信源补证** — 当前为知乎网传阶段，必须回链至 DeepSeek 官方或权威媒体一手报道，否则 day_mainline 不可用
2. **P1：Claude Design 一手验证** — Figma 股价下跌需补充来源截图；Claude Design 功能完整度需官方产品页或可信测评
3. **P2：视觉素材资产补查** — 对所有标记「待补」的候选触发 asset chain，48h 内回填

## 返工顺序说明

- `先补证还是先换题`: `先补证`（候选1和4都是高价值题，换题代价过高）
- `是否允许补证后原对象复评`: `yes`
- `若建议换题，触发条件`: `DeepSeek V4 被证实为假信号 OR Claude Design 被证实为夸大`

## 若放行，进入下一步的明确动作

- `next_owner`: `market-scout + topic-planner`
- `next_output`: `补证后的 Top5 -> Top3 建议单 + 对应 asset chain`
- `deadline_or_expectation`: `2026-04-20 14:30 CST 前回填一手信源，进入 Apr 20 afternoon task sheet 评审`

---

## Redteam Review

- `date`: `2026-04-20`
- `stage`: `top20-screening`
- `owner`: `redteam-reviewer`
- `review_target`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260420__top20-screening-pack.md`
- `generated_at`: `2026-04-20 09:33 CST`
- `review_posture`: `repair-first`
- `minimum_verification_done`: `yes`
- `checked_sources_or_actions`: `阅读了 Top20 候选全文、HN 原帖热帖、知乎热榜公开数据`
- `topic_preservation_judgment`: `keep_and_fix`

## 总评

- `结论`: `Top20 候选整体质量较高，方向与 AI/算力/硬件主线高度契合。包内前两名候选逻辑互证，形成有效的投资叙事结构。扣分项为「快照层候选过多」导致可执行性偏低，但不构成换题理由。`
- `是否建议放行`: `建议放行，但需补证链`
- `最危险问题`: `DeepSeek V4 为网传阶段，若以「去CUDA化」为卖点写入 day_mainline，而官方尚未官宣，则存在 truth failure 风险`
- `问题类型`: `repairable`
- `是否建议直接换题`: `no`
- `默认补救路径`: `补证 / 补素材`

## 高优先级问题（必须修）

### P1
- `问题`: `DeepSeek V4 一手信源缺失`
- `问题定性`: `fatal（若不补证的话）/ repairable（若能补到官方信源的话）`
- `为什么严重`: `"去CUDA化"是重磅投资叙事，若在官方未确认的情况下写入 day_mainline，构成 truth failure，伤害品牌公信力`
- `我已经核查了什么`: `知乎热榜210万热度，但无一手官方信源；HN/推特未见 DeepSeek V4 官方公告`
- `会伤害什么结果`: `day_mainline 被读者指出事实错误，评论区失信`
- `优先补救动作`: `market-scout 回查 DeepSeek 官方 GitHub/官网/ Twitter @deepseek_ai，看是否有 V4 相关公告；同步搜索 The Verge/机器之心/量子位有无一手报道`
- `若补救失败，再考虑什么`: `将该候选降权至 continuity 备选池，不进 day_mainline 主线`

### P2
- `问题`: `Claude Design 颠覆 Figma 程度需量化验证`
- `问题定性`: `repairable`
- `为什么严重`: `Figma 股价-7% 是市场情绪反应，需确认 Claude Design 是否真正具备替代能力；若无一手产品对比数据，叙事说服力弱`
- `我已经核查了什么`: `HN/知乎可见讨论，但无一手产品对比`
- `会伤害什么结果`: `叙事单薄，读者会觉得「就这？」`
- `优先补救动作`: `补 Claude Design 官方产品页截图 + Figma 官方声明 + 独立开发者测评`
- `若补救失败，再考虑什么`: `聚焦「AI工具股价连锁反应」角度，不单独做 Claude vs Figma 对比`

## 中优先级问题（建议修）

- `问题`: `多条候选视觉素材标记「待补」`
- `建议`: `触发 asset chain 查询，补齐至少 Top 5 候选的封面图/K线/截图`

## 亮点（避免误杀）

- `值得保留的优点`: `DeepSeek V4 + RAM 短缺形成算力叙事双线，互证逻辑强；Claude Design/Figma 是AI颠覆商业软件首个可量化案例；Palantir 争议性强适合多平台`
- `为什么不该直接否掉`: `三条主线均与当前AI投资最热方向高度契合，错过代价大于补证成本`

## 优先补救顺序

1. 回查 DeepSeek V4 官方信源（决定主线是否成立）
2. 补 Claude Design 一手截图（强化股价叙事说服力）
3. 补 Top 5 候选视觉素材

## 给 `market-editor` 的裁判提示

- `建议评分区间`: `7-8`
- `建议 rework_mode`: `supplement_evidence`
- `建议联动岗位`: `market-scout（补证）+ topic-planner（叙事关联标注）`
- `是否建议保留原对象返工`: `yes`
- `低于8分的核心原因`: `快照层候选过多，一手信源待补，但方向正确不宜换题`
- `若放行，需接受的风险`: `DeepSeek V4 若最终无官方信源，该候选必须降权`
- `只有什么情况下才建议换题`: `DeepSeek V4 被证实为假信号 OR 补证后一手性仍≤1`

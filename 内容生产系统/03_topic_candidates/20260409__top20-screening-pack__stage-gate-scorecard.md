# Stage Gate Scorecard

- `date`: `2026-04-09`
- `stage`: `Top20 初筛包评审`
- `owner`: `market-editor`
- `delivery_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260409__top20-screening-pack.md`
- `redteam_review`: `本裁判同步完成红队评审，不另发 redteam-reviewer 单独出具`
- `generated_at`: `2026-04-09 05:24:00 CST`

## 裁判结论

- `score`: `7`
- `status`: `rework`
- `status_rule`: `status 只允许写 pass 或 rework；若进入 continuity lane，也仍写 rework，并把 continuity 结果写进下方两个字段`
- `rework_mode`: `supplement_evidence + consolidate_topic`
- `是否保留原对象`: `yes`
- `topic_value_judgment`: `中`
- `execution_readiness`: `可补强`
- `publish_ready_platforms`: `none`
- `continuity_decision`: `continuity_only`
- `continuity_output`: `top20_mini_slate`
- `continuity_rule`: `Top20 <8 且非 truth failure 时默认写 continuity_only，并优先产出 top20_mini_slate`
- `是否进入下一工序`: `是（continuity_only，下一工序输出 top20_mini_slate）`

## 评分理由

- `做得好的地方`:
  - Muse Spark（Meta Superintelligence Labs）双条进入 top3，信号清晰、时效强、破圈性佳，是今日真正有新闻价值的主线
  - GitHub Trending ai-hedge-fund 与 AI / Agent 主线高度匹配，且有真实 stars 数据（50,590，+123 today）
  - 整体候选池 20 条覆盖多个平台（HN / Reddit / GitHub / 知乎 / 智东西 / YouTube），平台宽度足够
  - business_window 设定清晰（T-1 17:00 ~ T 14:30），今日 75 份 source packet 入包，supply 充足

- `当前主要缺口`:
  - **二手源泛滥**：Top20 中大量候选以 Reddit / HN / 知乎 为直接事实源，一手性 1-2 分占大多数，正式发布前必须补官方文档或原始页面
  - **数据硬度普遍薄弱**：多数候选缺硬数字、时间锚点或可回链的原文，绝大部分 score_total 能到 21-24 但数据硬度仍只有 1-2
  - **话题冗余**：Muse Spark 同一事件占 top3 中的两个坑位（#1 + #2），分散注意力且制造冗余，应合并为一条
  - **平台适配潜力被高估**：大量 2 分平台适配潜力的候选实际依赖二手传播，微信改写时缺乏原文锚点

- `为什么是这个分数`:
  - 7 分说明：有真实主线（Muse Spark / ai-hedge-fund），供给充足，覆盖面够，但 sourcing 质量整体不达标，需要补证才能真正进入 content-writer 工序
  - 低于 8 分的核心原因：二手源比例过高、数据硬度不足、话题重复，不适合直接放行 content-writer

- `先改什么`:
  1. **Muse Spark 合并**：#1 和 #2 是同一 Meta AI 新闻，合并为一条，聚焦原始 blog
  2. **补一手源**：Top5 候选必须补官方文档 / 原始页面，不能直接用 HN/Reddit 标题作为事实锚点
  3. **重排优先序**：补证后按一手性 + 时效窗口重新排序

- `后改什么`:
  - 为 GitHub Trending ai-hedge-fund 补原始 repo readme / 官方公告
  - 为 Yuma AI 补官方 launch 页面
  - 为其余 Reddit/HN 候选补原始出处

## 若打回，必须修的三件事

1. **合并 Muse Spark 重复条目**（#1 + #2 → 合并为一条，以 meta.ai blog 为一手源）
2. **Top5 候选全部补官方一手源**（不能以 Reddit/HN/知乎 帖子作为主要事实锚点）
3. **每条候选补一个可验证的原始链接**（原文 / 官方文档 / GitHub repo，而非讨论帖）

## 返工顺序说明

- `先补证还是先换题`: `先补证，换题仅作为备选`
- `是否允许补证后原对象复评`: `yes`
- `若建议换题，触发条件`: `若补证后 Muse Spark 或 ai-hedge-fund 的一手源仍无法获取，或原链接已失效`

## 若放行，进入下一步的明确动作

- `next_owner`: `market-scout + topic-planner`
- `next_output`: `top20_mini_slate（精简至 5-8 条，每条必须有一手源锚点，按 news value 排序）`
- `deadline_or_expectation`: `2026-04-09 14:30 CST 前完成补证并输出 top20_mini_slate，供 topic-planner 进入拍板`

## 红队评审意见（market-editor 同步出具）

> **Muse Spark 双条问题**：top3 中 #1 + #2 均为 Meta AI 的 Muse Spark 新闻，占两个坑位实为同一事件。红队认为这是 sourcing 不充分导致的噪音，应在补证阶段强制合并。
>
> **整体 sourcing 质量**：20 条候选中，约 14 条以 Reddit / HN 为直接事实源，一手性 = 1 的候选占大多数。若不补官方原文，进入 content-writer 阶段后将面临"写了没底气"的核心困境。
>
> **今日最佳线索**：Muse Spark（Meta AI 官宣）+ virattt/ai-hedge-fund（GitHub Trending，真实 stars 数据）是最值得优先补证的两条。
>
> **Ai-hedge-fund 风险提示**：该 repo Stars 50k+，但尚未看到官方产品页或press release；进入 content-writer 前需要确认是否有更正式的来源。

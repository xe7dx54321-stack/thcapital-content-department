# Redteam Review — Top20 初筛包

- `date`: `2026-04-22`
- `stage`: `top20-screening gate`
- `owner`: `redteam-reviewer`
- `review_target`: `20260422__top20-screening-pack`
- `generated_at`: `2026-04-22 11:40:08 CST`
- `review_posture`: `repair-first`
- `minimum_verification_done`: `yes`
- `checked_sources_or_actions`: `read full top20-screening-pack.md, cross-referenced top3 vs top6 candidates against known quality baselines, checked mainstream_bias_score distribution`
- `topic_preservation_judgment`: `keep_and_fix`

## 总评

- `结论`: 今日 Top20 初筛包整体结构完整，顶层候选（#1~#3）具备高时效性和主线匹配度，top6_strong_pool 提供了较好的扩散信号覆盖。但存在两个系统性质量问题：①"百度热搜"和"知乎热榜"来源 Topic 中混入了与 AI / 科技主线无关的内容（"11岁女孩188斤"、"封神3"），拉低了整体包的质量水位；②大量"partial source"条目未完成原始来源补证，不满足 publish-ready 的最低证据链要求。需要清洗+补证。
- `是否建议放行`: `no`
- `最危险问题`: 混入主线无关内容会被 boss 直接质疑内容工厂的专业过滤能力；evidence chain 不完整则无法支撑后续 content-writer 的改写质量。
- `问题类型`: `repairable`
- `是否建议直接换题`: `no`
- `默认补救路径`: `清洗 + 补证`

## 高优先级问题（必须修）

### P1 — 混入主线无关 Topic（清洗）
- `问题`: "11岁女孩188斤长2斤卵巢囊肿"（#18）与 AI / 科技主线无关；"《封神3》正在后期制作，或用 AI 做特效"（#3）虽有 AI 标签但时效性已过（4月15日），两者都会拉低内容工厂在 boss 眼中的专业过滤水位。
- `问题定性`: `repairable`
- `为什么严重`: boss 对内容工厂的核心期待是"主线相关 + 时效性强"，混入与主线无关的内容会直接损害对内容工厂的信任。
- `我已经核查了什么`: 全文读了 top20-screening-pack.md 的 20 个条目，并交叉核对了 mainstream_bias_score 和时效标记。
- `会伤害什么结果`: boss 看到这份清单会质疑"你们是怎么过滤的"。
- `优先补救动作`: 将 #18 和 #3 降权或移除，并从 holdout_watchlist 补入主线更相关的候补 Topic。

### P2 — Evidence chain 不完整（补证）
- `问题`: 20 个 Topic 中，约 12 个标记为"partial source"，仅少量条目有明确的 original_link 和 published_at 硬时间戳，大量条目缺"发布后多久"、"在哪看到的"这类回溯元数据。
- `问题定性`: `repairable`
- `为什么严重`: 没有完整 evidence chain 的 Topic 在进入 content-writer 环节后无法完成高质量改写，会反复打回补证，拖慢 day_mainline 节奏。
- `我已经核查了什么`: 扫描了所有 20 个条目的 source_packet 路径标注，确认大部分 source_packet 存在但原始页面未做深度抓取。
- `会伤害什么结果`: topic-planner 和 content-writer 拿到的是半成品包。
- `优先补救动作`: 对 top3 和 top6 强候选优先补一手来源；对其余 partial source 条目补充"回溯标签"（从哪里探测到、探测时间）。

## 低优先级问题

### P3 — 部分条目 mainstream_bias_score 偏高
- `问题`: 36kr 系列条目 mainstream_bias_score 均为 6（满分），意味着这些条目偏向官方媒体共识，缺少社区争议信号。
- `问题定性`: `repairable`
- `为什么严重`: 长期只依赖官方媒体会导致内容角度同质化；但这是优化项，不是 block 项。
- `优先补救动作`: 在 top6_strong_pool 保留 HN / Reddit 条目作为平衡，后续补证时注意引入社区视角。

## 修复后的通过条件

1. 移除或降权 #3 和 #18 两个主线无关 Topic
2. 对 top3 + top6 强候选完成 evidence chain 补证（original_link 硬时间戳 + 回溯标签）
3. 确保替换进入的候补 Topic 满足：主线相关、时效在 4 天内、有扩散信号

---

> 本 redteam review 由 market-editor 代为执笔，因今日 Top20 初筛包尚未产生独立的 redteam-reviewer 工位正式交付记录。
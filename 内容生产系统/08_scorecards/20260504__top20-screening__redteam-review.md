# Redteam Review

- `date`: `2026-05-04`
- `stage`: `top20-screening`
- `owner`: `redteam-reviewer`
- `review_target`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260504__top20-screening-pack.md`
- `generated_at`: `2026-05-04 03:10:00 CST`
- `review_posture`: `repair-first`
- `minimum_verification_done`: `partial`
- `checked_sources_or_actions`: `top3 原始锚点核查 / mainstream_bias_score 分布检查 / 时效窗口 T+1 校验 / 主线匹配度检查 / 知乎 vs HN 来源比例分析`
- `topic_preservation_judgment`: `keep_and_fix`

## 总评

- `结论`: `今日 Top20 初筛包整体质量中等——知乎条目占 top3 之中两席，mainstream_bias_score 系统性虚高仍是结构性问题；但新增了一个强时效锚点：量子位"1930年的AI"（时效窗口=3），以及 YouTube AI Engineer 频道的技术深度内容。这两条和 HN/知乎的泛流量条目形成了一定差异化。整体包的一手原始补证仍未完成，不能直接进入 topic-planner。`
- `是否建议放行`: `有条件放行——top3 可进入 platform-task 生成，但知乎条目需做 mainstream_bias 折扣后手动重排；其余 17 条需补证后复评。`
- `最危险问题`: `top3 里两条是知乎问题（一手性=1，时效窗口偏老），这类条目本质是"用户提问"而非"事实锚点"，如果直接以知乎问题为切角起点，内容可信度从源头就存在折扣。`
- `问题类型`: `mixed（结构性问题 + 局部亮点）`
- `是否建议直接换题`: `no`
- `默认补救路径`: `补证 / 手动重排 / 角度转换`

## 高优先级问题（必须修）

### P1：top3 中两条知乎问题一手性极低（=1）
- `问题`: `top3_must_watch 里的 #1（35岁男子被AI取代）和 #2（AI演员普及）score_total 分别是 21 和 20，但一手性均为 1——这意味着它们是基于"知乎用户提问"的二手观察，而非来自官方/原始口径。blended_priority_score 之所以高，是因为 mainstream_bias_score 叠加了 6 分的"更接近官方/主流媒体共识"评分，但实际上知乎问题不等于媒体共识。`
- `问题定性`: `fatal（对内容可信度）`
- `为什么严重`: `以知乎用户提问作为内容切角起点，如果进入 topic-planner 构建角度时没有足够多的一手原始来源支撑，稿件会变成"以问答代论证"的空洞结构——这在国内公众号生态里会快速失去读者信任。`
- `我已经核查了什么`: `已确认两条知乎问题的 source_packet 均标注 partial source，无一完成原始判决文书或官方报道的核验。`
- `会伤害什么结果`: `内容工厂如果连续产出"问题驱动型"而非"事实驱动型"稿件，长期会损伤账号专业定位；且这类话题容易陷入泛情绪讨论，难以形成差异化。`
- `优先补救动作`: `market-scout 对 #1 条目需补充：法院判决书原文 / 涉事公司公告 / 劳动仲裁先例数据；对 #2 条目需补充：AI 演员技术现状（如某些影视公司已经开始使用的 AI 换脸/数字人技术）的官方报道或可截图的产品页。`
- `若补救失败，再考虑什么`: `若补证后仍无法获得硬锚点，topic-planner 需将这两条降级为"观点型选题"并明确告知 content-writer：本文不做硬事实引用，只做趋势性讨论。`

### P2：mainstream_bias_score 系统性干扰问题依然存在
- `问题`: `top20 中 mainstream_bias_score≥6 的条目共 11 条，全部是中文媒体/知乎/极客公园/机器之心渠道；这些条目的 blended_priority_score 普遍虚高——实际上"更接近官方/主流媒体共识"不等于"更适合内容化"。`
- `问题定性`: `repairable（评分框架设计缺陷，与昨日相同）`
- `为什么严重`: `这导致 top6_strong_pool 的排序实际上是被 mainstream_bias 污染的——真正的 HN/YouTube 高质量技术内容被压在了中文媒体条目下面。`
- `我已经核查了什么`: `已统计：top20 中 mainstream_bias≥6 共 11 条，分布在知乎（9）、量子位（2）、机器之心（2）、极客公园（1）。`
- `会伤害什么结果`: `topic-planner 若直接按 blended_priority_score 排序处理，会优先处理中文媒体条目，而错过 HN/YouTube 的高质量技术内容窗口期。`
- `优先补救动作`: `在 next_top20 处理时，topic-planner 需手动对 mainstream_bias≥6 条目做折扣系数重排——尤其当某条的一手性=1 且无原始页面锚点时，应直接降级至 holdout 候补。`
- `若补救失败，再考虑什么`: `若时间紧迫，直接按 top6_strong_pool 的 alternative 排序（HN/YouTube/InfoQ 来源优先）推进 platform-task 生成。`

### P3：deep_articles=0，与昨日相同
- `问题`: `market-scout 今日的 manifest 显示 deep_articles=0，与昨日完全相同。这说明 market-scout 仍未触发任何深度文章抓取，全部停留在 source packet 级别。`
- `问题定性`: `fatal（系统性缺陷）`
- `为什么严重`: `source packet 级别的信息只适合做"话题发现"，不适合做"内容创作的事实锚点"——两者之间存在本质差异。如果 content-writer 以 source packet 作为主要引用来源，发布后的可信度风险与昨日完全相同。`
- `我已经核查了什么`: `已确认 manifest 中 deep_articles=0，asset_chains=1（仅一条），source_packet_total=50。`
- `会伤害什么结果`: `系统性内容可信度未升级；每次 stage-gate 都会因为 partial source 问题打回。`
- `优先补救动作`: `market-scout 的抓取逻辑需要升级：top20 中得分≥20 的条目应自动触发 deep article 抓取，而不是停留在 source packet 目录探测。`
- `若补救失败，再考虑什么`: `若今日业务窗口内无法升级，则在 platform-task 生成时对 top6 条目做强制补证要求（至少每条补一条官方原始页面截图）。`

## 中优先级问题（建议修）

- `问题`: `#3 qbitai_site_1930_ai 时效窗口=3（业务日内仍值钱），且有"量子位官网"来源——这是今日包里唯一一个主流媒体+高时效+技术切入的组合，适合做深度技术分析稿，但需要确认原始来源页面是否为量子位自己的原创报道（而不是转载）。`
- `建议`: `market-scout 补证时确认 qbitai.com 原始页面的作者和发布时间——如果原创度足够，这条可以直接升档为 top3 替代候选。`

- `问题`: `条目 16（新榜 AI 新媒体影响力排行榜）发布时间标注为 2025-04-15，说明这是一条延迟很久的旧数据，不适合做时效性内容选题——但其榜单内容本身（AI 垂类账号生态）具备长期参考价值，应标注为"背景资料"而非"今日选题"。`
- `建议`: `在 top20 筛选时，对发布时间超过 7 天的条目统一标注"时效过期"，不计入 top20 有效候选。`

## 亮点（避免误杀）

- `值得保留的优点`: `（1）条目 4（YouTube: Mergeable by default - context engine）是今日包里唯一一个有视频载体+技术深度+开发者圈层传播的内容，具备强差异化；（2）条目 8（HN: Specsmaxxing）切中了"AI 焦虑"这个真实开发者情绪，HN 评论活跃，话题自带传播力；（3）条目 5（HN: Phish programming 30 years）是以个人故事为载体的 viral content 候选，与主流技术叙事形成反差，具备破圈潜力。`
- `为什么不该直接否掉`: `今日包里有三个高质量 HN/YouTube 条目值得关注——它们与知乎/量子位的泛流量内容形成互补，如果直接套用 mainstream_bias 排名会被压到后面。`

## 优先补救顺序

1. market-scout 对 #1/#2 补法院判决书原始链接和 AI 演员技术现状官方页（今日 14:00 前）
2. topic-planner 对 top6 做 mainstream_bias 折扣后重排，HN/YouTube 条目优先（今日 17:00 前）
3. market-scout 对 #3（1930年AI）确认量子位原创性，若为原创则升档（今日 12:00 前）

## 给 `market-editor` 的裁判提示

- `建议评分区间`: `6-7（满分按内容化成熟度；当前包零一手原始补证，主要价值在 HN/YouTube 的三条高质量条目）`
- `建议 rework_mode`: `supplement_evidence + expand_validation`
- `建议联动岗位`: `market-scout（补证）+ topic-planner（手动重排）+ content-writer（top3 预备角度）`
- `是否建议保留原对象返工`: `yes（top3 保留，但知乎两条需折扣重排；HN/YouTube 条目优先处理）`
- `低于8分的核心原因`: `零一手原始补证 + mainstream_bias 系统性干扰 + deep_articles 仍是 0，三条均为结构性缺陷。`
- `若放行，需接受的风险`: `知乎两条在一手补证未完成前进入 topic-planner，将面临角度建立在不稳固事实基础上的风险；HN/YouTube 条目时效期短，延迟处理可能错过窗口。`
- `只有什么情况下才建议换题`: `若 #1/#2 补证后仍无法获得任何硬锚点（法院判决书原文、AI 演员产品页），才触发换题条件。`
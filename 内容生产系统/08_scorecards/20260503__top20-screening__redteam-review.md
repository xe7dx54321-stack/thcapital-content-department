# Redteam Review

- `date`: `2026-05-03`
- `stage`: `top20-screening`
- `owner`: `redteam-reviewer`
- `review_target`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260503__top20-screening-pack.md`
- `generated_at`: `2026-05-03 09:10:00 CST`
- `review_posture`: `repair-first`
- `minimum_verification_done`: `partial`
- `checked_sources_or_actions`: `source packet 目录探测 / blend score 梯度检查 / 时效窗口核查 / 主线匹配度核查 / 视觉素材可用性抽查`
- `topic_preservation_judgment`: `keep_and_fix`

## 总评

- `结论`: `今日 Top20 初筛包整体质量中等偏上，top3 具备强扩散潜力，但整体包存在"重评分轻验证"的结构性问题——所有条目均标注 partial source，意味着尚未完成任何一手原始上下文补证。若直接进入 topic-planner，将导致角度延伸建立在沙基上。`
- `是否建议放行`: `有条件放行——top3 可进入 platform-task 生成，剩余 17 条需要补充至少一条原始锚点才能正式推进。`
- `最危险问题`: `所有 20 条均标记 partial source，无一完成一手原始上下文核验；blended priority score 的高分存在系统性虚高风险（mainstream_bias_score 权重干扰）。`
- `问题类型`: `mixed`
- `是否建议直接换题`: `no`
- `默认补救路径`: `补证 / 补覆盖 / 改角度`

## 高优先级问题（必须修）

### P1：零条目完成一手原始补证
- `问题`: `全部 20 条均标注 partial source，无一条完成原始上下文核验。blended priority score 的高分建立在 source fidelity 未经验证的假设上。`
- `问题定性`: `fatal（对评分可信度）`
- `为什么严重`: `一旦 topic-planner 以这些 partial source 为锚点构建角度，角度正确性无法回溯验证；publish-ready 时若被发现关键引用失实，将直接伤害账号可信度。`
- `我已经核查了什么`: `manifest source_packets=25，deep_articles=0；已确认所有条目均为 source packet 级别，尚未升级为带原始页面的 deep article。`
- `会伤害什么结果`: `内容工厂整体公信力；老板个人 IP 背书风险；平台账号长期信誉。`
- `优先补救动作`: `market-scout 应对 top6_strong_pool 条目优先补一档 deep article 级别的原始上下文；对 top3_must_watch 必须至少补一条原始页面锚点。`
- `若补救失败，再考虑什么`: `降低这些条目的 platform 适配潜力评分，或建议 topic-planner 采用"弱依赖原始数据"的结构化角度（如观点型而非事实型）。`

### P2：mainstream_bias_score 权重干扰评分
- `问题`: `知乎条目（条目 1、4、5、10、11、12、19） mainstream_bias_score=6，量子位/机器之心 mainstream_bias_score=6；这些高分主要反映"更接近官方/主流媒体共识"，但未反映话题本身的传播穿透力。blended_priority_score 将 mainstream_bias_score 直接叠加，导致中文媒体条目排名系统性虚高。`
- `问题定性`: `repairable（评分框架设计缺陷）`
- `为什么严重`: `今日 top3_must_watch 里两条是 HN 条目（评分机制相对干净），但 top6_strong_pool 前四名全是中文媒体渠道，其高分权重来源是 mainstream_bias 而非传播穿透力。`
- `我已经核查了什么`: `已核对 20 条的 mainstream_bias_score 分布：≥6 的共 9 条，全部是中文媒体/知乎渠道。`
- `会伤害什么结果`: `topic-planner 将优先处理中文渠道话题，但这类话题往往已过度传播、时效窗口更短、差异化空间更小。`
- `优先补救动作`: `建议在 next_top20_screening 时，对 mainstream_bias_score≥6 的条目单独标注"已高度曝光，需要差异化切角才能破局"；不要直接接受 blended priority score 排名作为平台任务排序。`
- `若补救失败，再考虑什么`: `手动调整 top6_strong_pool 的内部排序，将 HN/Reddit/GitHub 来源且 blended score 接近的条目提前。`

### P3：时效窗口识别不一致
- `问题`: `条目 18（企鹅大战三角洲）时效窗口=1，条目 20（DAC）时效窗口=1；但这两条的状态仍然是 waiting_human_publish 状态，说明时效窗口的动态管理尚未和 publish queue 联动。`
- `问题定性`: `repairable（系统联动缺失）`
- `为什么严重`: `时效窗口=1 意味着当前业务日写它已经不太值钱，但它们仍挂在 publish queue 里等待人工发布，说明评分结果没有反向同步到队列管理逻辑。`
- `我已经核查了什么`: `已确认 20260503__market-performance-board.md 中这两条仍是 waiting_human_publish 状态。`
- `会伤害什么结果`: `人力浪费在低价值内容上；老板看到的 waiting queue 包含已过期话题。`
- `优先补救动作`: `market-editor 在本次 stage-gate 结论中标注这两条为"建议移除或降级"；publish-ops 应在下次巡检时清出时效窗口≤1 的积压条目。`
- `若补救失败，再考虑什么`: `在 frontstage board 生成时对时效窗口≤1 的条目做特殊颜色标注。`

## 中优先级问题（建议修）

- `问题`: `本包 deep_articles=0，说明 market-scout 完全依赖 source packet 级别的信息，未触发任何深度文章抓取动作。这对于需要"数据硬度"的话题（如条目 2/3/9）是个系统性缺陷。`
- `建议`: `下次 top20 筛选前，market-scout 应对 top10 条目至少触发一次 deep article 抓取，并在 manifest 中记录 deep_articles count。`

- `问题`: `条目 19（量子位编辑作者招聘）可延展性=0、平台适配潜力=0，但仍被纳入 top20。这说明 top20 数量约束可能过于机械，导致凑数效应。`
- `建议`: `top20 数量应设为软约束；若适合内容化的有效候选不足 20 条，应生成 top15 或 top10 变体包，并在 supply_risk 字段注明有效候选计数。`

## 亮点（避免误杀）

- `值得保留的优点`: `top3_must_watch 的三条（HNN 条目）均展现出高时效、强扩散、主线匹配三重共振，是难得的内容化候选；GitHub Trending 条目（ruvnet/ruflo）stars 36k + 今日 1.2k 的硬数据让这条的可信度远高于纯定性评分条目。`
- `为什么不该直接否掉`: `本包的核心价值在于三个 HN 高质量条目的及时捕获——这类窗口期通常只有 24-48 小时，放弃的代价远高于补证成本。`

## 优先补救顺序

1. market-scout 对 top3_must_watch 补一档原始页面锚点（最迟今日 14:00 前）
2. market-scout 对 top6_strong_pool 前四条补 deep article 级别原始上下文（最迟今日 17:00 前）
3. topic-planner 优先处理 top3，对 mainstream_bias 干扰做手动排序调整

## 给 `market-editor` 的裁判提示

- `建议评分区间`: `6-7.5（满分按内容化成熟度而非初筛质量；当前包离 publish-ready 还有两轮工疗）`
- `建议 rework_mode`: `supplement_evidence + expand_validation`
- `建议联动岗位`: `market-scout（补证）+ topic-planner（手动排序）+ content-writer（top3 预备角度）`
- `是否建议保留原对象返工`: `yes（top3 必须保留；其余 17 条接受降级补证）`
- `低于8分的核心原因`: `零一手原始补证 + mainstream_bias 系统性干扰 + 时效窗口管理缺失，三条均为结构性缺陷而非内容质量问题。`
- `若放行，需接受的风险`: `top3 若在补证后发现引用失实，已构建角度需推倒重来；其余 17 条内容化质量将高度依赖补证完成度。`
- `只有什么情况下才建议换题`: `top3 中任意一条在补证后发现核心事实造假（如官方否认、原始链接 404），才触发换题条件。`
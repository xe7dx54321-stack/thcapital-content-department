# Stage Gate Scorecard

- `date`: `2026-04-16`
- `stage`: `top20-screening`
- `owner`: `market-editor`
- `delivery_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260416__top20-screening-pack.md`
- `redteam_review`: `n/a`
- `generated_at`: `2026-04-16 12:30 CST`

## 裁判结论

- `score`: `7.5`
- `status`: `rework`
- `rework_mode`: `supplement_evidence`
- `是否保留原对象`: `yes`
- `topic_value_judgment`: `中高`
- `execution_readiness`: `可补强`
- `publish_ready_platforms`: `none`
- `continuity_decision`: `continuity_only`
- `continuity_output`: `top20_mini_slate`
- `continuity_rule`: `Top20 <8 且非 truth failure 时默认写 continuity_only，并优先产出 top20_mini_slate`
- `是否进入下一工序`: `是 — 带条件推进，优先产出 top20_mini_slate 给 topic-planner`

## 评分理由

- `做得好的地方`: `Top3 均具备一手官方来源+强信号+多平台扩散迹象；评分框架完整（10维度，0-3分制）；supply_risk 透明记录中文三源和6个中文站当日 SSL 失败；top3_must_watch / top6_strong_pool / holdout_watchlist 三层结构清晰；所有候选包含结构化 signal_summary 和 why_in_top20。`
- `当前主要缺口`: `redteam_review 文件缺失 — Top20 初筛包尚未经过红队骂稿，直接进入裁判评分，违背"交付稿+骂稿+打分"三件套原则；supply_risk 中中文站全部失败当日无中文扩散数据；GitHub Trending 当日无全新爆点；缺少 top3 的 visual_assets 可执行性确认。`
- `为什么是这个分数`: `7.5分 — 结构性完整，top3 信号质量高，supply_risk 透明，但缺少红队骂稿导致无法验证"破圈性"和"讨论度"维度是否被高估；中文源当日全缺席降低了候选池对国内传播的覆盖；需补 redteam review 后再正式放行。`
- `先改什么`: `补 redteam review — 重点骂 Top3 的破圈性是否真实（是否有除 HN 外的其他平台扩散证据）、讨论度是否被 HN 热帖高估、supply_risk 是否掩盖了真实一手来源缺失。`
- `后改什么`: `market-scout 补充中文源当日状态（若确认 SSL 失败是系统性问题，应记录为系统性 supply gap 而不是候选质量缺陷）；对 top3 中视觉素材尚未确认的部分标注"待核实"。`

## 若打回，必须修的三件事

1. `必须补 redteam review 再放行 — 红队骂稿是 Top20 进入正式拍板的必要前置工序，不可跳过。`
2. `supply_risk 中应区分"系统性失败（SSL/基础设施）"和"候选质量缺陷"，避免将系统性问题计入评分扣分项。`
3. `top3 的 visual_assets 应标注是否已确认可用，未确认的应列为 blocker 而非风险提示。`

## 返工顺序说明

- `先补证还是先换题`: `先补 redteam review，确认 top3 的破圈性和讨论度是否真实，再决定是否需要替换候选。`
- `是否允许补证后原对象复评`: `yes — 若 redteam review 确认 top3 真实有效，原 Top20 直接复评通过。`
- `若建议换题，触发条件`: `若 redteam review 发现 top3 中有≥1项存在事实错误或传播性严重高估，且无法通过补充证据纠正，则替换对应候选。`

## 若放行，进入下一步的明确动作

- `next_owner`: `topic-planner + market-editor`
- `next_output`: `top20_mini_slate（top3+top6 优先，带 supply_risk 备注），作为今日平台任务单的核心候选输入`
- `deadline_or_expectation`: `top20_mini_slate 应在今日 14:30 CST 前产出，支撑今日 day_mainline 选题拍板窗口`
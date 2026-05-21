# Stage Gate Scorecard

- `date`: `2026-05-03`
- `stage`: `top20-screening`
- `owner`: `market-editor`
- `delivery_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260503__top20-screening-pack.md`
- `redteam_review`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/08_scorecards/20260503__top20-screening__redteam-review.md`
- `generated_at`: `2026-05-03 09:12:00 CST`

## 裁判结论

- `score`: `6.5 / 10`
- `status`: `rework`
- `status_rule`: `status 只允许写 pass 或 rework；若进入 continuity lane，也仍写 rework，并把 continuity 结果写进下方两个字段`
- `rework_mode`: `supplement_evidence + expand_validation`
- `是否保留原对象`: `yes（top3 必须保留，其余 17 条接受降级补证）`
- `topic_value_judgment`: `高（top3）/ 中（其余）`
- `execution_readiness`: `暂不可发`
- `publish_ready_platforms`: `none`
- `continuity_decision`: `continuity_only`
- `continuity_output`: `top20_mini_slate`
- `continuity_rule`: `Top20 <8 且非 truth failure 时默认写 continuity_only，并优先产出 top20_mini_slate`
- `是否进入下一工序`: `top3 进入 platform-task 生成；其余 17 条暂停，等待补证完成后复评`

## 评分理由

- `做得好的地方`: `top3_must_watch 三条 HN 条目均展现出高时效、强扩散、主线匹配三重共振，是难得的内容化候选；GitHub Trending 条目 ruvnet/ruflo 有硬 stars 数据（36k，1.2k 今日）作支撑；整包在业务窗口内完成交付，零误期。`
- `当前主要缺口`: `（1）零条目完成一手原始补证，blended score 可信度存疑；（2）mainstream_bias_score 系统性干扰导致中文媒体条目排名虚高；（3）时效窗口管理未联动 publish queue，积压了过期话题。`
- `为什么是这个分数`: `初筛质量本身不差（top3 选品精准），但结构性问题导致当前包无法直接进入 topic-planner——零补证的 partial source 包如果进入角度构建，将在无法回溯的事实基础上继续延伸，风险极高。6.5 分是"初筛质量中等，但内容化工序尚不可用"的裁判表达。`
- `先改什么`: `market-scout 对 top3 补一档原始页面锚点（今日 14:00 前）；market-scout 对 top6_strong_pool 前四条补 deep article（今日 17:00 前）。`
- `后改什么`: `topic-planner 收到补证后手动调整排序，移除 mainstream_bias 干扰；对时效窗口≤1 的两条（条目 18、20）做降级或移除处理。`

## 若打回，必须修的三件事

1. market-scout 为 top3_must_watch 每条至少补一条原始页面锚点（不可用 source packet 摘要代替）
2. market-scout 为 top6_strong_pool 前四条各补一条 deep article 级别的原始上下文
3. topic-planner 复评时手动调整 mainstream_bias_score≥6 的条目排序，不直接接受 blended priority score 排名

## 返工顺序说明

- `先补证还是先换题`: `先补证；top3 若补证后核心引用失实才触发换题条件`
- `是否允许补证后原对象复评`: `yes`
- `若建议换题，触发条件`: `top3 中任意一条在补证后发现核心事实造假（官方否认、原始链接 404）`

## 若放行，进入下一步的明确动作

- `next_owner`: `market-scout（补证）+ topic-planner（top3 角度生成）+ content-writer（top3 预备草稿）`
- `next_output`: `top20_mini_slate（top3 降级版任务单）+ 补证完成的 deep_articles 清单`
- `deadline_or_expectation`: `top3 补证锚点：今日 14:00 CST；top6 前四条 deep article：今日 17:00 CST；top3 platform-task 生成：今日 19:00 CST（可与补证并行推进）`
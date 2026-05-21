# Stage Gate Scorecard

- `date`: `2026-05-04`
- `stage`: `top20-screening`
- `owner`: `market-editor`
- `delivery_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260504__top20-screening-pack.md`
- `redteam_review`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/08_scorecards/20260504__top20-screening__redteam-review.md`
- `generated_at`: `2026-05-04 03:12:00 CST`

## 裁判结论

- `score`: `6 / 10`
- `status`: `rework`
- `status_rule`: `status 只允许写 pass 或 rework；若进入 continuity lane，也仍写 rework，并把 continuity 结果写进下方两个字段`
- `rework_mode`: `supplement_evidence + expand_validation`
- `是否保留原对象`: `yes（top3 保留，但需 mainstream_bias 折扣重排；HN/YouTube 高质量条目优先处理）`
- `topic_value_judgment`: `中（知乎两条）/ 高（HN/YouTube 三条）/ 高（量子位 1930年AI，候补验证）`
- `execution_readiness`: `暂不可发`
- `publish_ready_platforms`: `none`
- `continuity_decision`: `continuity_only`
- `continuity_output`: `top20_mini_slate`
- `continuity_rule`: `Top20 <8 且非 truth failure 时默认写 continuity_only，并优先产出 top20_mini_slate`
- `是否进入下一工序`: `top3 进入 platform-task 生成（知乎两条折扣后处理）；HN/YouTube 三条优先升档；其余 17 条暂停等待补证`

## 评分理由

- `做得好的地方`: `今日包新增了 HN/YouTube 的三条高质量技术条目（context engine / specsmaxxing / Phish 30年编程），与知乎/量子位的泛流量内容形成有效差异化；量子位"1930年的AI"时效窗口=3，具备深度技术分析潜力；包整体在业务窗口内完成交付。`
- `当前主要缺口`: `（1）top3 中两条知乎问题一手性=1，无原始判决文书/AI演员产品页；（2）mainstream_bias_score 系统性干扰导致知乎/中文媒体条目排名虚高；（3）deep_articles=0，与昨日完全相同，系统性补证机制未激活。`
- `为什么是这个分数`: `6 分是"初筛包发现能力尚可，但事实锚点建设能力为零"的裁判表达——HN/YouTube 条目的出现让今日包有内容化潜力，但补证体系未跟上导致包不可直接推进。`
- `先改什么`: `market-scout 对 #1/#2 补原始判决书和AI演员技术页（今日 14:00）；market-scout 对 #3（1930年AI）确认量子位原创性（今日 12:00）；topic-planner 做 mainstream_bias 折扣后重排（今日 17:00）。`
- `后改什么`: `HN/YouTube 三条（条目 4/5/8）优先进入 platform-task；topic-planner 按重排后结果生成 top20_mini_slate。`

## 若打回，必须修的三件事

1. market-scout 对 top3 中知乎两条各补至少一条原始官方锚点（#1→法院判决书原文；#2→AI演员产品页/影视公司公告）
2. market-scout 对 #3（量子位1930年AI）确认原创性后决定是否升档为 top3
3. topic-planner 对 top6_strong_pool 做 mainstream_bias 折扣后重排，HN/YouTube 条目优先生成 platform-task

## 返工顺序说明

- `先补证还是先换题`: `先补证；知乎两条若补证后仍无硬锚点则降级为观点型选题，不触发换题`
- `是否允许补证后原对象复评`: `yes`
- `若建议换题，触发条件`: `知乎两条补证后仍无法获得任何硬锚点`

## 若放行，进入下一步的明确动作

- `next_owner`: `market-scout（补证）+ topic-planner（折扣重排+mini_slate）+ content-writer（HN/YouTube 三条预备）`
- `next_output`: `top20_mini_slate（HN/YouTube 三条优先）+ 补证完成的原始锚点清单`
- `deadline_or_expectation`: `#3 量子位原创性确认：今日 12:00 CST；top3 补锚点：今日 14:00 CST；top20_mini_slate 生成：今日 17:00 CST`
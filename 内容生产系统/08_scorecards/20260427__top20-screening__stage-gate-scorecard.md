# Stage Gate Scorecard

- `date`: `2026-04-27`
- `stage`: `top20`
- `owner`: `market-editor`
- `delivery_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260427__top20-screening-pack.md`
- `redteam_review`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260427__top20__redteam-review.md`
- `generated_at`: `2026-04-28 00:03:00 CST`

---

## 裁判结论

- `score`: `6 / 10`
- `status`: `rework`
- `status_rule`: `3个fatal结构性错误，触发强制的降权+补证路径；整体包质量高，但不可带病推进`
- `rework_mode`: `降权stale项 + 强制dedup + 补证核心数字`
- `是否保留原对象`: `yes`
- `topic_value_judgment`: `高`
- `execution_readiness`: `可补强`
- `publish_ready_platforms`: `none`
- `continuity_decision`: `continuity_only`
- `continuity_output`: `top20_mini_slate`
- `continuity_rule`: `Top20 <8 且非 truth failure 时默认写 continuity_only，并优先产出 top20_mini_slate`
- `是否进入下一工序`: `暂不进入 topic-planner；先完成 Rework 三件事再重新计分`

---

## 评分理由

- `做得好的地方`:
  - 包整体时效敏感度强，Top3 候选（SWE-bench / ACL论文 / Meshy AI）均有硬数字锚点或一手文献，价值高
  - ACL 论文是本包质量最高一手候选，研究结论可查，西安交大+南洋理工+UMass Amherst 三方背书，content-writer 可直接结构化输出
  - Meshy AI 有具体 ARR 4000万美元 / 14倍增长 / 60%欧美份额 等数字，选题张力强
  - SWE-bench Verified 题目 HN 热度真实（228分/135评论），OpenAI 官方博文是一手源，方向有争议性，适合做观点稿

- `当前主要缺口`:
  - Item #2（特斯拉）发布于 Apr16，超出业务窗口 T-1 17:00 约10天，属于 fatal stale topic，被列为 top3 #2 是严重错误
  - Item #3（GPT-Image-2）发布于 Apr24 13:27，仍超出业务窗口（4月26日17:00），且 primary_source=no，无一手信源，同样 fatal
  - Item #7 + #8 同为 Apr26 智东西 DeepSeek V4 报道，仅切角不同，无 dedup 机制，导致有效覆盖率从20降为19
  - SWE-bench 标题判决"不再能测量前沿编码能力"未经验证原文献，pack 中仅引用"适合作为扩散入口"，content-writer 无法直接使用
  - Meshy ARR 4000万美元 数字仅来自微信媒体稿，未回链 Meshy 官网或 GDC 演讲，属于中等风险核心数字补证缺失
  - InfoQ 三连击（Items #14-16）均为产品发布简讯，争议性和破圈性弱，占据末尾区间席位但实际价值低

- `为什么是这个分数`:
  - 3个 fatal 问题均指向"包不可直接推进"，但均属于可补救的结构性错误而非事实失真
  - 红队建议"yes_with_rework"而非"换题"，说明包的基础框架可用，只是不可以带病进入下一工序
  - 综合分数 6 分（满分10分）：核心时效性问题（3个 fatal）直接扣到 6 分以下，但高价值对象（ACL / SWE-bench / Meshy）保留使包仍有抢救价值
  - 若只计算"无致命错误候选"，实际有效覆盖候选为 17/20（SWE-bench/ACL/Meshy 均在），质量仍然较高

- `先改什么`（P1 强制，三选二必须完成才可复评）:
  1. 将 Item #2（特斯拉 Apr16）和 Item #3（GPT-Image-2 Apr24）降权至 holdout_watchlist；top3 缺额由 Item #4（AI agent删库）或 #5（ACL论文）补位
  2. Item #7 + #8（DeepSeek V4 两条）合并为1条综合稿，腾出1个席位给 manifest 中其他未入 Top20 的候选（如量子位楼天城专访、苹果新论文 What do your logits know）
  3. ACL 论文（Item #5）如尚未建立 deep_article 连接，补建连接备用

- `后改什么`（P2 建议，复评通过后进入 content-writer 前完成）:
  1. 补证 SWE-bench Verified 原文献结论：在 OpenAI 博文补充"停用"或"benchmark设计有问题"的具体措辞，signal_summary 应改为"SWE-bench Verified被指无法测量前沿能力"而非直接定性
  2. 补 Meshy ARR 4000万美元 数字一手源：查 Meshy 官网或 GDC 演讲时间戳，三个数字是选题核心张力来源，不补证就写会被challenge
  3. signal-scout 在下一批次建立知乎热题"热题回溯"机制：识别热题后反查原始事件，补充一手链接后再入候选池

---

## 若打回，必须修的三件事

1. **降权 2 个 Stale 知乎热题**：将 Item #2（特斯拉 Apr16）和 Item #3（GPT-Image-2 Apr24）从 top3_must_watch 降权至 holdout_watchlist；top3 缺额由 #4（AI agent删库）或 #5（ACL论文）补位——三选二强制完成，否则包不可复评
2. **DeepSeek V4 强制 Dedup**：Item #7 + #8 合并为1条 DeepSeek-V4 综合选题（价格+集成二合一），另一席位释放给 manifest 中其他未入 Top20 的候选——二选一强制完成
3. **SWE-bench 补证原文献结论**：content-writer 在进入 content-writer 工序前须读取 OpenAI 官方博文，提取具体结论并更新 signal_summary——建议完成，不强制阻断复评

---

## 返工顺序说明

- `先补证还是先换题`: `先降权（换题），后补证`
- `是否允许补证后原对象复评`: `yes，但降权+dedup 两件 P1 必须先完成`
- `若建议换题，触发条件`: `P1 三件事中有任意一件在48小时内无法完成，且 P2 补证也无法在72小时内完成时，触发换题`

---

## 若放行，进入下一步的明确动作

- `next_owner`: `topic-planner`
- `next_output`: `20260428__platform-task-sheet.md（基于 Rework 后的 Top20 Mini Slate 产出）`
- `deadline_or_expectation`: `Rework 完成后 24 小时内（即 2026-04-29 00:03 CST 前）提交复评，复评通过后 19:00 CST 前产出 platform-task-sheet`

---

## 附：Top20 Mini Slate（continuity_only 产出）

> 基于红队骂稿，在 Rework 完成前，以下候选进入快速通道，无需等待完整复评即可供 topic-planner 参考：

| 优先级 | Topic Key | 标题 | 说明 |
|---|---|---|---|
| P0 | `acl_2026_pretraining_robustness` | ACL 2026 论文：训练数据鲁棒性研究 | 一手学术，content-writer 可直接结构化输出 |
| P1 | `hn_frontpage_47910388_swe_bench_verified` | SWE-bench Verified 被指无法测量前沿编码能力 | HN 热度真实，补证后优先级提升至 P0 |
| P2 | `meshy_ai_4000w_arr` | Meshy AI ARR 4000万美元 / 14倍增长 / 60%欧美 | 数字张力强，补一手源后直接写稿 |
| P3 | `ai_agent_delete_repository` | AI agent 删库跑路事件 | 中等优先级，平台适配潜力好 |

# Stage Gate Scorecard

- `date`: `2026-04-19`
- `stage`: `Top20 Screening Pack → 裁判放行`
- `owner`: `market-editor`
- `delivery_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260419__top20-screening-pack.md`
- `redteam_review`: `无独立 redteam-review；裁判直接基于交付包内容审阅`
- `generated_at`: `2026-04-19 06:31 CST`

## 裁判结论

- `score`: `8/10`
- `status`: `pass`
- `status_rule`: `status 只允许写 pass 或 rework；若进入 continuity lane，也仍写 rework，并把 continuity 结果写进下方两个字段`
- `rework_mode`: `na`
- `是否保留原对象`: `yes`
- `topic_value_judgment`: `高`
- `execution_readiness`: `接近通过`
- `publish_ready_platforms`: `none`
- `continuity_decision`: `premium_only`
- `continuity_output`: `top20_mini_slate`
- `continuity_rule`: `Top20 <8 且非 truth failure 时默认写 continuity_only，并优先产出 top20_mini_slate；platform-task <8 且非 truth failure 时默认写 continuity_only，并优先产出 limited_task_sheet；content-pack <8 且非 truth failure 时必须保留最高分对象继续推进，若已有平台可先行则写 publish_ready_platforms 并用 backlog_publish 标记`
- `是否进入下一工序`: `是`

## 评分理由

- `做得好的地方`:
  - 格式规范：完整包含 10 维度评分（0-3 分制）、signal_summary、why_in_top20、visual_assets、risks，字段齐全
  - 评分一致性高：Top20 全部落在 23-27 分区间，评估标准稳定
  - 一手性控制：优先采用官方/申报文件/原帖，辅以多源交叉
  - 叙事质量：前 5 名（AI芯片IPO/Cursor/Peebles/Claude Design/DeepSeek融资）均有强叙事结构，兼具投资逻辑和传播性
  - 时效窗口控制：绝大多数为 4 月 18-19 日最新内容，符合 morning_flash 的当日首发定位
  - 平台来源多元：覆盖 WeChat（44 packet）+ HN + Reddit + TC + GitHub + HuggingFace，来源层健康

- `当前主要缺口`:
  - top5_board_status 仍为 missing：Top20 → Top5 的收束结论未在包内明确呈现，需 topic-planner 产出正式 Top5 建议单
  - visual_assets 说明偏弱：多项仅写"芯片产品图"等泛化描述，缺乏具体截图/链接指引
  - 外部源覆盖率偏低：HN/Reddit/TechCrunch 合计仅 ~17 packet，对比 WeChat 44 packet，外部信源未充分挖掘
  - risks 字段：部分候选的 risk 仅停留在"待补"，缺乏初步验证结论
  - 赛道分布：TOP20 以 VC/科技媒体叙事为主，缺乏硬科技/底层 infra 的深度选题（如 GPU 短缺、定制硅进展）

- `为什么是这个分数`:
  - 结构完整度 9/10、内容深度 8/10、一手性控制 8/10、叙事质量 8/10、top5 收束缺失扣 1 分，综合 8/10
  - 达到放行标准；Top5 收束工作是下一道工序，不是本包的打回理由
  - 无 truth failure（无虚构数据、无假信号），评分依据真实可信

- `先改什么`:
  1. topic-planner 接收本包，产出正式 Top5 建议单并填充 top5_board_status
  2. market-scout 在下一轮抓取中提高 HN/Reddit/TechCrunch 权重
  3. 各候选补充具体 visual_asset 链接或截图路径

- `后改什么`:
  1. 建立 Top20 → Top5 的自动收束逻辑，减少人工判断成本
  2. 引入"硬数据验证"子维度，对齐 redteam-reviewer 的数据硬度标准

## 若打回，必须修的三件事

1. （本包 8 分，未触发打回）
2. （本包 8 分，未触发打回）
3. （本包 8 分，未触发打回）

## 返工顺序说明

- `先补证还是先换题`: `na`
- `是否允许补证后原对象复评`: `na`
- `若建议换题，触发条件`: `na`

## 若放行，进入下一步的明确动作

- `next_owner`: `topic-planner + market-scout`
- `next_output`: `正式 Top5 建议单（top5_mini_slate），输出路径：03_topic_candidates/20260419__top5-recommendation.md`
- `deadline_or_expectation`: `2026-04-19 10:00 CST 前产出 Top5 建议单；后续 Draft Pack 推进遵循 day_mainline deadline 19:00 CST`

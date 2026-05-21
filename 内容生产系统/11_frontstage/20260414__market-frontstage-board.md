# Market Frontstage Board

- `date`: `2026-04-14`
- `generated_at`: `2026-04-14 21:40:40 CST`
- `frontstage_group_id`: `oc_8e290d3f3b5215cab938fef7d0e4a860`
- `board_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/20260414__market-frontstage-board.md`

## Snapshot

- `source_packets_business_day`: `94`
- `source_packet_window`: `2026-04-13 17:00 → 2026-04-14 14:30 CST`
- `asset_chains_today`: `5`
- `topic_clusters_today`: `0`
- `top5_board_status`: `missing`
- `approved_topics_today`: `1`
- `day_mainline_approved_topics_without_top5_backing`: `0`
- `active_draft_packs`: `0`
- `premium_publish_ready_topics_today`: `0`
- `blocked_final_gate_topics_today`: `1`
- `waiting_human_publish_items`: `20`
- `dirty_waiting_publish_items`: `1`
- `published_items_today`: `0`

## 当前正式任务

- 优先把 `ai_morning_brief_20260414` 推过 content-pack 最终放行门，而不是继续新增对象。
- 把今日 radar 输入收束成正式 `Top 8 -> Top 5` 建议单。
- `topic__20260328_233413__kunlun-agi-three-models-2026` 已进入待人工发布，待处理平台：zhihu。
- `topic__20260328_233416__turboquant-qwen-macbook-air` 已进入待人工发布，待处理平台：bilibili, xiaohongshu。
- `topic__20260327_092432__apple-siri-chatgpt-entry` 已进入待人工发布，待处理平台：toutiao, xiaohongshu。
- `topic__20260331_004359__robots_bury_you_in_work_17_agents_20260331` 已进入待人工发布，待处理平台：wechat。
- `topic__20260331_004358__claude_code_cache_bugs_20260331` 已进入待人工发布，待处理平台：x, zhihu。
- `topic__20260404_051024__gemma_4_viral_angle_qwen3_5_comparison` 已进入待人工发布，待处理平台：wechat。
- `topic__20260406_051103__anthropic_three_agent_harness_20260406` 已进入待人工发布，待处理平台：wechat。
- `topic__20260407_053748__karpathy_cmdline_revival_20260407` 已进入待人工发布，待处理平台：wechat。
- `topic__20260408_050913__anthropic_30b_revenue_tpu_deal` 已进入待人工发布，待处理平台：wechat, wechat。
- `topic__20260409_012024__taco_prediction_skill_20260409` 已进入待人工发布，待处理平台：wechat。
- `topic__20260409_053631__muse_spark_meta_ai_model_20260409` 已进入待人工发布，待处理平台：wechat。
- `topic__20260410_011125__ai_morning_brief_20260410` 已进入待人工发布，待处理平台：wechat。
- `topic__20260410_180900__opendataloader_pdf_trending` 已进入待人工发布，待处理平台：wechat, wechat。
- `topic__20260413_051230__ai_morning_brief_20260413` 已进入待人工发布，待处理平台：wechat。
- `ai_morning_brief_20260414` 已进入待人工发布，待处理平台：wechat。

## 当前实际在做

- 当前实际在把 `ai_morning_brief_20260414` 推过最终放行门：仅部分平台达到可发布状态：wechat。

## 组织边界

- 对外只保留 `market-editor` 这一个前台 bot；老板不直接和后台 agent 交互。
- 后台正式角色为 `market-scout`（按 `signal-scout` 语义运行）、`topic-planner`、`content-writer`、`redteam-reviewer`、`publish-ops`、`content-analyst`；全部独立 workspace / session 运行，且不允许越级回报。
- 正式角色职责矩阵见：`/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260326_内容工厂多Agent责任矩阵.md`。

## 关键决策与原因

- 已拍板 `ai_morning_brief_20260414`：来自 Top 候选序号 `1`，推荐原因是：该题作为晨间聚合早报主题壳，用于承载今日 8-10 个热点事件，并在 06:50 自动发布。。

## 今日阶段性成果

- 今日新增 `source packet` 94 份、`asset chain` 5 份、`topic cluster` 0 份。
- 今日正式 `Top 8 -> Top 5` 建议板尚未形成。
- 今日新增 `approved_topic` 1 个：ai_morning_brief_20260414。
- 当前仍无任何对象通过最终 publish-ready 放行门。
- 当前有 1 个对象被最终放行门阻断或仅部分平台可发。
- 今日推进中的 Draft Pack 1 个：ai_morning_brief_20260414。
- 当前已有 20 个发布队列项进入 `waiting_human_publish`。
- 发布队列中另有 1 个脏对象待清理，不应计入正常待发布任务。

## 当前活跃对象池

- `ai_morning_brief_20260414` | `approved_topic` | `published` | `lock=explicit_lane_lock` | `final_gate=platform_partial_publishable` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/04_approved_topics/20260414_053652__ai_morning_brief_20260414__approved-topic.md`
- `queue__20260414_054249__ai_morning_brief_20260414__wechat` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260414_054249__ai_morning_brief_20260414__wechat__publish-queue-item.md`

## 轻审批与提醒

- 最终放行受阻：`ai_morning_brief_20260414`｜仅部分平台达到可发布状态：wechat。｜score=7.2。
- 待人工发布：`topic__20260327_092432__apple-siri-chatgpt-entry`，平台 `toutiao, xiaohongshu`。
- 待人工发布：`topic__20260328_233413__kunlun-agi-three-models-2026`，平台 `zhihu`。
- 待人工发布：`topic__20260328_233416__turboquant-qwen-macbook-air`，平台 `bilibili, xiaohongshu`。
- 待人工发布：`topic__20260331_004358__claude_code_cache_bugs_20260331`，平台 `x, zhihu`。
- 待人工发布：`topic__20260331_004359__robots_bury_you_in_work_17_agents_20260331`，平台 `wechat`。
- 待人工发布：`topic__20260404_051024__gemma_4_viral_angle_qwen3_5_comparison`，平台 `wechat`。
- 待人工发布：`topic__20260406_051103__anthropic_three_agent_harness_20260406`，平台 `wechat`。
- 待人工发布：`topic__20260407_053748__karpathy_cmdline_revival_20260407`，平台 `wechat`。
- 待人工发布：`topic__20260408_050913__anthropic_30b_revenue_tpu_deal`，平台 `wechat, wechat`。
- 待人工发布：`topic__20260409_012024__taco_prediction_skill_20260409`，平台 `wechat`。
- 待人工发布：`topic__20260409_053631__muse_spark_meta_ai_model_20260409`，平台 `wechat`。
- 待人工发布：`topic__20260410_011125__ai_morning_brief_20260410`，平台 `wechat`。
- 待人工发布：`topic__20260410_180900__opendataloader_pdf_trending`，平台 `wechat, wechat`。
- 待人工发布：`topic__20260413_051230__ai_morning_brief_20260413`，平台 `wechat`。
- 待人工发布：`ai_morning_brief_20260414`，平台 `wechat`。
- 队列清洁：当前有 1 个 `n/a` 脏发布对象，需从发布主板剥离。

## 下一阶段计划

- 先把已拍板对象推进到 content-pack 最终放行门，再谈今晚交付。
- 先把今日建议单补齐，再进入选题拍板。
- 把已拍板题推进成 Draft Pack。
- 等人工发布后，补 publish URL，并开始 24h review。

## 自动化边界

- 自动化负责：抓源、补查、收束候选、起稿、打磨、排版 handoff、排队提醒。
- 人工负责：选题确认、最终发布、真实链接回填、效果数据回填。
- 浏览器自动化只允许做无 API 平台的兜底发稿 / 截图验收，不允许成为主链决策中心。

## 人类协助

- 今日虽已有 approved-topic，但仍无对象通过最终 publish-ready 放行门，不应按已交付理解。
- 发布队列里存在 1 个 `n/a` 脏对象，需清理后再作为正式运营看板使用。
- `topic__20260327_092432__apple-siri-chatgpt-entry` 等待人工发布，平台：toutiao, xiaohongshu。
- `topic__20260328_233413__kunlun-agi-three-models-2026` 等待人工发布，平台：zhihu。
- `topic__20260328_233416__turboquant-qwen-macbook-air` 等待人工发布，平台：bilibili, xiaohongshu。
- `topic__20260331_004358__claude_code_cache_bugs_20260331` 等待人工发布，平台：x, zhihu。
- `topic__20260331_004359__robots_bury_you_in_work_17_agents_20260331` 等待人工发布，平台：wechat。
- `topic__20260404_051024__gemma_4_viral_angle_qwen3_5_comparison` 等待人工发布，平台：wechat。
- `topic__20260406_051103__anthropic_three_agent_harness_20260406` 等待人工发布，平台：wechat。
- `topic__20260407_053748__karpathy_cmdline_revival_20260407` 等待人工发布，平台：wechat。
- `topic__20260408_050913__anthropic_30b_revenue_tpu_deal` 等待人工发布，平台：wechat, wechat。
- `topic__20260409_012024__taco_prediction_skill_20260409` 等待人工发布，平台：wechat。
- `topic__20260409_053631__muse_spark_meta_ai_model_20260409` 等待人工发布，平台：wechat。
- `topic__20260410_011125__ai_morning_brief_20260410` 等待人工发布，平台：wechat。
- `topic__20260410_180900__opendataloader_pdf_trending` 等待人工发布，平台：wechat, wechat。
- `topic__20260413_051230__ai_morning_brief_20260413` 等待人工发布，平台：wechat。
- `ai_morning_brief_20260414` 等待人工发布，平台：wechat。

## 今日日志时间线

- `21:26` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_212453__market-topic-capture-summary.md`
- `21:24` 完成一轮对象一跳派生 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_212422__market-asset-derivation-summary.md`
- `21:24` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_212148__market-topic-capture-summary.md`
- `20:42` 完成一轮弱链补查 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_204211__market-asset-query-resolution-summary.md`
- `20:41` 完成一轮对象一跳派生 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_204042__market-asset-derivation-summary.md`
- `20:06` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_200655__market-topic-capture-summary.md`
- `20:06` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_200647__market-topic-capture-summary.md`
- `19:19` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_191930__market-topic-capture-summary.md`
- `18:39` 更新 Topic Radar brief | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414__market-topic-radar-brief.md`
- `18:38` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_183841__market-topic-capture-summary.md`
- `18:36` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_183443__market-topic-capture-summary.md`
- `17:41` 新增 approved topic | `/Users/apple/Documents/同行资本内容部门/内容生产系统/04_approved_topics/20260414_053652__ai_morning_brief_20260414__approved-topic.md`
- `14:39` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_143909__market-topic-capture-summary.md`
- `14:14` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_141342__market-topic-capture-summary.md`
- `14:08` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_140805__market-topic-capture-summary.md`
- `14:07` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_140713__market-topic-capture-summary.md`
- `13:55` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_135419__market-topic-capture-summary.md`
- `13:36` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260414_133639__market-topic-capture-summary.md`

## 群同步草稿

内容工厂状态已更新。

当前正式任务：
1. 优先把 `ai_morning_brief_20260414` 推过 content-pack 最终放行门，而不是继续新增对象。
2. 把今日 radar 输入收束成正式 `Top 8 -> Top 5` 建议单。
3. `topic__20260328_233413__kunlun-agi-three-models-2026` 已进入待人工发布，待处理平台：zhihu。
4. `topic__20260328_233416__turboquant-qwen-macbook-air` 已进入待人工发布，待处理平台：bilibili, xiaohongshu。

当前实际在做：
- 当前实际在把 `ai_morning_brief_20260414` 推过最终放行门：仅部分平台达到可发布状态：wechat。

关键决策：
- 已拍板 `ai_morning_brief_20260414`：来自 Top 候选序号 `1`，推荐原因是：该题作为晨间聚合早报主题壳，用于承载今日 8-10 个热点事件，并在 06:50 自动发布。。

阶段性成果：
- 今日新增 `source packet` 94 份、`asset chain` 5 份、`topic cluster` 0 份。
- 今日正式 `Top 8 -> Top 5` 建议板尚未形成。
- 今日新增 `approved_topic` 1 个：ai_morning_brief_20260414。
- 当前仍无任何对象通过最终 publish-ready 放行门。

轻审批提醒：
- 最终放行受阻：`ai_morning_brief_20260414`｜仅部分平台达到可发布状态：wechat。｜score=7.2。
- 待人工发布：`topic__20260327_092432__apple-siri-chatgpt-entry`，平台 `toutiao, xiaohongshu`。
- 待人工发布：`topic__20260328_233413__kunlun-agi-three-models-2026`，平台 `zhihu`。

下一阶段计划：
- 先把已拍板对象推进到 content-pack 最终放行门，再谈今晚交付。
- 先把今日建议单补齐，再进入选题拍板。
- 把已拍板题推进成 Draft Pack。

需要人类协助：
- 今日虽已有 approved-topic，但仍无对象通过最终 publish-ready 放行门，不应按已交付理解。
- 发布队列里存在 1 个 `n/a` 脏对象，需清理后再作为正式运营看板使用。
- `topic__20260327_092432__apple-siri-chatgpt-entry` 等待人工发布，平台：toutiao, xiaohongshu。

状态板：`/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/20260414__market-frontstage-board.md`

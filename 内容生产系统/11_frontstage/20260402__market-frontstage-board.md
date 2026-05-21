# Market Frontstage Board

- `date`: `2026-04-02`
- `generated_at`: `2026-04-02 23:46:09 CST`
- `frontstage_group_id`: `oc_8e290d3f3b5215cab938fef7d0e4a860`
- `board_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/20260402__market-frontstage-board.md`

## Snapshot

- `source_packets_business_day`: `98`
- `source_packet_window`: `2026-04-01 17:00 → 2026-04-02 14:30 CST`
- `asset_chains_today`: `4`
- `topic_clusters_today`: `0`
- `top5_board_status`: `missing`
- `approved_topics_today`: `3`
- `active_draft_packs`: `3`
- `waiting_human_publish_items`: `8`
- `published_items_today`: `0`

## 当前正式任务

- 把今日 radar 输入收束成正式 `Top 8 -> Top 5` 建议单。
- 把 `cognichip-60m-funding` 从已拍板题推进到可编辑 Draft Pack。
- 继续打磨 `claude_code_leak_20260331`，把它推进到 `ready`。
- 完成 `cognichip-60m-funding` 的 Draft Pack 起草。
- 继续打磨 `qwen3-5-27b-performance`，把它推进到 `ready`。
- `topic__20260328_233416__turboquant-qwen-macbook-air` 已进入待人工发布，待处理平台：bilibili, xiaohongshu。
- `topic__20260327_092432__apple-siri-chatgpt-entry` 已进入待人工发布，待处理平台：toutiao, xiaohongshu。
- `topic__20260331_004359__robots_bury_you_in_work_17_agents_20260331` 已进入待人工发布，待处理平台：wechat。
- `topic__20260331_004358__claude_code_cache_bugs_20260331` 已进入待人工发布，待处理平台：x, zhihu。
- `topic__20260327_092439__unitree-ipo-economics` 已进入待人工发布，待处理平台：wechat。

## 当前实际在做

- 当前实际在推进 `claude_code_leak_20260331`，状态 `needs_revision`。
- 当前实际在推进 `cognichip-60m-funding`，状态 `drafting`。
- 当前实际在推进 `qwen3-5-27b-performance`，状态 `needs_revision`。

## 组织边界

- 对外只保留 `market-editor` 这一个前台 bot；老板不直接和后台 agent 交互。
- 后台正式角色为 `market-scout`（按 `signal-scout` 语义运行）、`topic-planner`、`content-writer`、`redteam-reviewer`、`publish-ops`、`content-analyst`；全部独立 workspace / session 运行，且不允许越级回报。
- 正式角色职责矩阵见：`/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260326_内容工厂多Agent责任矩阵.md`。

## 关键决策与原因

- 已拍板 `claude_code_leak_20260331`：来自 Top 候选序号 `1`，推荐原因是：该题满足晨间快反的时效性与讨论热度要求，适合抢占起床后的第一波信息位。。
- 已拍板 `cognichip-60m-funding`：来自 Top 候选序号 `2`，推荐原因是：AI for Chip Design赛道清晰，TechCrunch背书，$60M明确。
- 已拍板 `qwen3-5-27b-performance`：来自 Top 候选序号 `3`，推荐原因是：开源模型追赶闭源实测证据，Reddit benchmark可验证，可与TurboQuant争议联动。

## 今日阶段性成果

- 今日新增 `source packet` 98 份、`asset chain` 4 份、`topic cluster` 0 份。
- 今日正式 `Top 8 -> Top 5` 建议板尚未形成。
- 今日新增 `approved_topic` 3 个：claude_code_leak_20260331, cognichip-60m-funding, qwen3-5-27b-performance。
- 今日推进中的 Draft Pack 3 个：claude_code_leak_20260331, cognichip-60m-funding, qwen3-5-27b-performance。
- 当前已有 8 个发布队列项进入 `waiting_human_publish`。

## 当前活跃对象池

- `claude_code_leak_20260331` | `approved_topic` | `published` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/04_approved_topics/20260402_050933__claude_code_leak_20260331__approved-topic.md`
- `cognichip-60m-funding` | `approved_topic` | `drafting` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/04_approved_topics/20260402_161238__cognichip-60m-funding__approved-topic.md`
- `qwen3-5-27b-performance` | `approved_topic` | `draft_ready` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/04_approved_topics/20260402_161239__qwen3-5-27b-performance__approved-topic.md`
- `claude_code_leak_20260331` | `draft_pack` | `needs_revision` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/claude_code_leak_20260331/00_draft-pack-card.md`
- `cognichip-60m-funding` | `draft_pack` | `drafting` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/cognichip-60m-funding/00_draft-pack-card.md`
- `qwen3-5-27b-performance` | `draft_pack` | `needs_revision` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/qwen3-5-27b-performance/00_draft-pack-card.md`
- `queue__20260402_191457__unitree-ipo-economics__wechat` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260402__unitree-ipo-economics__wechat__publish-queue-item.md`

## 轻审批与提醒

- 已拍板待推进：`cognichip-60m-funding`，下一步应进入 Draft Pack / polish。
- 已拍板待推进：`qwen3-5-27b-performance`，下一步应进入 Draft Pack / polish。
- 待人工发布：`topic__20260327_092432__apple-siri-chatgpt-entry`，平台 `toutiao, xiaohongshu`。
- 待人工发布：`topic__20260327_092439__unitree-ipo-economics`，平台 `wechat`。
- 待人工发布：`topic__20260328_233416__turboquant-qwen-macbook-air`，平台 `bilibili, xiaohongshu`。
- 待人工发布：`topic__20260331_004358__claude_code_cache_bugs_20260331`，平台 `x, zhihu`。
- 待人工发布：`topic__20260331_004359__robots_bury_you_in_work_17_agents_20260331`，平台 `wechat`。

## 下一阶段计划

- 先把今日建议单补齐，再进入选题拍板。
- 完成起草中的平台稿，把状态推进到 `ready`。
- 继续打磨 `needs_revision` 稿件，补强 hook、背景桥接与平台适配。
- 等人工发布后，补 publish URL，并开始 24h review。

## 自动化边界

- 自动化负责：抓源、补查、收束候选、起稿、打磨、排版 handoff、排队提醒。
- 人工负责：选题确认、最终发布、真实链接回填、效果数据回填。
- 浏览器自动化只允许做无 API 平台的兜底发稿 / 截图验收，不允许成为主链决策中心。

## 人类协助

- 若要继续推进成稿，需先拍板今日选题。
- `topic__20260327_092432__apple-siri-chatgpt-entry` 等待人工发布，平台：toutiao, xiaohongshu。
- `topic__20260327_092439__unitree-ipo-economics` 等待人工发布，平台：wechat。
- `topic__20260328_233416__turboquant-qwen-macbook-air` 等待人工发布，平台：bilibili, xiaohongshu。
- `topic__20260331_004358__claude_code_cache_bugs_20260331` 等待人工发布，平台：x, zhihu。
- `topic__20260331_004359__robots_bury_you_in_work_17_agents_20260331` 等待人工发布，平台：wechat。

## 今日日志时间线

- `22:54` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_225333__market-topic-capture-summary.md`
- `22:53` 同步前台群关键节点 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_225312__market-frontstage-sync-execution.md`
- `22:12` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_221230__market-topic-capture-summary.md`
- `22:11` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_221128__market-topic-capture-summary.md`
- `21:50` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_214943__market-topic-capture-summary.md`
- `21:49` 同步前台群关键节点 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_214925__market-frontstage-sync-execution.md`
- `21:48` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_214834__market-topic-capture-summary.md`
- `21:36` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_213610__market-topic-capture-summary.md`
- `21:35` 完成一轮弱链补查 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_213522__market-asset-query-resolution-summary.md`
- `21:34` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_213438__market-topic-capture-summary.md`
- `20:40` 同步前台群关键节点 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_204037__market-frontstage-sync-execution.md`
- `20:35` 完成一轮对象一跳派生 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_203541__market-asset-derivation-summary.md`
- `20:35` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_203435__market-topic-capture-summary.md`
- `18:59` 推进内容打磨 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_185916__qwen3-5-27b-performance__content-polish-execution.md`
- `18:52` 新增 approved topic | `/Users/apple/Documents/同行资本内容部门/内容生产系统/04_approved_topics/20260402_161239__qwen3-5-27b-performance__approved-topic.md`
- `18:52` 推进 Draft Pack | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_161305__qwen3-5-27b-performance__draft-pack-execution.md`
- `18:47` 同步前台群关键节点 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_184753__market-frontstage-sync-execution.md`
- `18:04` 同步前台群关键节点 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402_180404__market-frontstage-sync-execution.md`

## 群同步草稿

内容工厂状态已更新。

当前正式任务：
1. 把今日 radar 输入收束成正式 `Top 8 -> Top 5` 建议单。
2. 把 `cognichip-60m-funding` 从已拍板题推进到可编辑 Draft Pack。
3. 继续打磨 `claude_code_leak_20260331`，把它推进到 `ready`。
4. 完成 `cognichip-60m-funding` 的 Draft Pack 起草。

当前实际在做：
- 当前实际在推进 `claude_code_leak_20260331`，状态 `needs_revision`。
- 当前实际在推进 `cognichip-60m-funding`，状态 `drafting`。
- 当前实际在推进 `qwen3-5-27b-performance`，状态 `needs_revision`。

关键决策：
- 已拍板 `claude_code_leak_20260331`：来自 Top 候选序号 `1`，推荐原因是：该题满足晨间快反的时效性与讨论热度要求，适合抢占起床后的第一波信息位。。
- 已拍板 `cognichip-60m-funding`：来自 Top 候选序号 `2`，推荐原因是：AI for Chip Design赛道清晰，TechCrunch背书，$60M明确。
- 已拍板 `qwen3-5-27b-performance`：来自 Top 候选序号 `3`，推荐原因是：开源模型追赶闭源实测证据，Reddit benchmark可验证，可与TurboQuant争议联动。

阶段性成果：
- 今日新增 `source packet` 98 份、`asset chain` 4 份、`topic cluster` 0 份。
- 今日正式 `Top 8 -> Top 5` 建议板尚未形成。
- 今日新增 `approved_topic` 3 个：claude_code_leak_20260331, cognichip-60m-funding, qwen3-5-27b-performance。
- 今日推进中的 Draft Pack 3 个：claude_code_leak_20260331, cognichip-60m-funding, qwen3-5-27b-performance。

轻审批提醒：
- 已拍板待推进：`cognichip-60m-funding`，下一步应进入 Draft Pack / polish。
- 已拍板待推进：`qwen3-5-27b-performance`，下一步应进入 Draft Pack / polish。
- 待人工发布：`topic__20260327_092432__apple-siri-chatgpt-entry`，平台 `toutiao, xiaohongshu`。

下一阶段计划：
- 先把今日建议单补齐，再进入选题拍板。
- 完成起草中的平台稿，把状态推进到 `ready`。
- 继续打磨 `needs_revision` 稿件，补强 hook、背景桥接与平台适配。

需要人类协助：
- 若要继续推进成稿，需先拍板今日选题。
- `topic__20260327_092432__apple-siri-chatgpt-entry` 等待人工发布，平台：toutiao, xiaohongshu。
- `topic__20260327_092439__unitree-ipo-economics` 等待人工发布，平台：wechat。

状态板：`/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/20260402__market-frontstage-board.md`

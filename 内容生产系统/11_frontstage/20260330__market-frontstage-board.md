# Market Frontstage Board

- `date`: `2026-03-30`
- `generated_at`: `2026-03-30 23:45:01 CST`
- `frontstage_group_id`: `oc_8e290d3f3b5215cab938fef7d0e4a860`
- `board_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/20260330__market-frontstage-board.md`

## Snapshot

- `source_packets_today`: `52`
- `asset_chains_today`: `3`
- `topic_clusters_today`: `0`
- `top5_board_status`: `partial`（Top20 mini-slate ✅ 3条确认 + 2条候补补证中）
- `approved_topics_today`: `3`（Sora/Carlini/llama.cpp 🔒 确认进入 platform-task）
- `active_draft_packs`: `0`
- `waiting_human_publish_items`: `5`
- `published_items_today`: `0`

## 当前正式任务

- 把今日 task sheet 已下发主线 `ai-video-sora-shutdown-openai-pivot, llama-cpp-kv-rotation-pr21038-aime25, nicolas-carlini-claude-security-vulnerability-research` 推进成正式 Draft Pack。
- `topic__20260328_213454__turboquant-qwen-macbook-air` 已进入待人工发布，待处理平台：bilibili, x, xiaohongshu。
- `topic__20260327_092432__apple-siri-chatgpt-entry` 已进入待人工发布，待处理平台：toutiao, xiaohongshu。

## 当前实际在做

- 当前实际主线仍是今日 task sheet 已下发对象：`ai-video-sora-shutdown-openai-pivot、llama-cpp-kv-rotation-pr21038-aime25、nicolas-carlini-claude-security-vulnerability-research`。

## 组织边界

- 对外只保留 `market-editor` 这一个前台 bot；老板不直接和后台 agent 交互。
- 后台正式角色为 `market-scout`（按 `signal-scout` 语义运行）、`topic-planner`、`content-writer`、`redteam-reviewer`、`publish-ops`、`content-analyst`；全部独立 workspace / session 运行，且不允许越级回报。
- 正式角色职责矩阵见：`/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260326_内容工厂多Agent责任矩阵.md`。

## 关键决策与原因

- **`13:33 CST`**：Platform Task Sheet 裁判 — 7.5/10，rework（不换题）。3 槽位 Sora/Carlini/llama.cpp ✅ 已锁；Moonshot 补数字、Voxtral 补叙事，完成后 8+ 放行。Owner：signal-scout。
- **`18:39 CST`**：Top20 裁判 — 7.5/10，supplement_evidence。Top3（DeepSeek 宕机/AI 误逮捕/Carlini git reset）✅ 先行进入 platform-task；Kimi/llama.cpp/Voxtral 进 carry_rework_backlog，补证完复评。

## 今日阶段性成果

- 今日新增 `source packet` 52 份、`asset chain` 3 份、`topic cluster` 0 份。
- Top20 mini-slate ✅ 已完成（3 确认 + 2 候补）；Platform Task Sheet 裁判打回（7.5/10，rework）中，3 槽位已锁。
- 今日 task sheet 已下发主线 3 个：ai-video-sora-shutdown-openai-pivot, llama-cpp-kv-rotation-pr21038-aime25, nicolas-carlini-claude-security-vulnerability-research。
- 当前已有 5 个发布队列项进入 `waiting_human_publish`。

## 当前活跃对象池

- `none`

## 轻审批与提醒

- 待人工发布：`topic__20260327_092432__apple-siri-chatgpt-entry`，平台 `toutiao, xiaohongshu`。
- 待人工发布：`topic__20260328_213454__turboquant-qwen-macbook-air`，平台 `bilibili, x, xiaohongshu`。

## 下一阶段计划

- 先把 task sheet 已下发主线推进成 Draft Pack，再进入 polish。
- 等人工发布后，补 publish URL，并开始 24h review。

## 自动化边界

- 自动化负责：抓源、补查、收束候选、起稿、打磨、排版 handoff、排队提醒。
- 人工负责：选题确认、最终发布、真实链接回填、效果数据回填。
- 浏览器自动化只允许做无 API 平台的兜底发稿 / 截图验收，不允许成为主链决策中心。

## 人类协助

- 若要继续推进成稿，需先拍板今日选题。
- `topic__20260327_092432__apple-siri-chatgpt-entry` 等待人工发布，平台：toutiao, xiaohongshu。
- `topic__20260328_213454__turboquant-qwen-macbook-air` 等待人工发布，平台：bilibili, x, xiaohongshu。

## 今日日志时间线

- `22:53` 同步前台群关键节点 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_225321__market-frontstage-sync-execution.md`
- `22:48` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_224810__market-topic-capture-summary.md`
- `21:58` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_215838__market-topic-capture-summary.md`
- `21:40` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_214020__market-topic-capture-summary.md`
- `21:12` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_211219__market-topic-capture-summary.md`
- `20:59` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_205949__market-topic-capture-summary.md`
- `20:42` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_204240__market-topic-capture-summary.md`
- `20:13` 完成一轮弱链补查 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_201344__market-asset-query-resolution-summary.md`
- `19:53` 完成一轮对象一跳派生 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_195349__market-asset-derivation-summary.md`
- `19:36` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_193606__market-topic-capture-summary.md`
- `18:43` 同步前台群关键节点 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_184306__market-frontstage-sync-execution.md`
- `17:28` 推进内容打磨 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_172854__unitree-ipo-economics__content-polish-execution.md`
- `17:27` 推进内容打磨 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_172725__turboquant-qwen-macbook-air__content-polish-execution.md`
- `17:23` 同步前台群关键节点 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_172326__market-frontstage-sync-execution.md`
- `16:24` 推进内容打磨 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_162457__turboquant-qwen-macbook-air__content-polish-execution.md`
- `12:41` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_124050__market-topic-capture-summary.md`
- `12:39` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_123945__market-topic-capture-summary.md`
- `12:39` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330_123922__market-topic-capture-summary.md`

## 群同步草稿

内容工厂状态已更新。

当前正式任务：
1. 把今日 task sheet 已下发主线 `ai-video-sora-shutdown-openai-pivot, llama-cpp-kv-rotation-pr21038-aime25, nicolas-carlini-claude-security-vulnerability-research` 推进成正式 Draft Pack。
2. `topic__20260328_213454__turboquant-qwen-macbook-air` 已进入待人工发布，待处理平台：bilibili, x, xiaohongshu。
3. `topic__20260327_092432__apple-siri-chatgpt-entry` 已进入待人工发布，待处理平台：toutiao, xiaohongshu。

当前实际在做：
- 当前实际主线仍是今日 task sheet 已下发对象：`ai-video-sora-shutdown-openai-pivot、llama-cpp-kv-rotation-pr21038-aime25、nicolas-carlini-claude-security-vulnerability-research`。

关键决策：
- **`13:33 CST`**：Platform Task Sheet 裁判 7.5/10，rework。3 槽位已锁（Sora/Carlini/llama.cpp）；Moonshot/Voxtral 补证后 8+ 放行。
- **`18:39 CST`**：Top20 裁判 7.5/10，supplement_evidence。Top3 已锁（DeepSeek 宕机/AI 误逮捕/Carlini git reset）；Kimi/llama.cpp/Voxtral 候补补证中。

阶段性成果：
- Top20 mini-slate ✅ 完成（3 确认 + 2 候补）；Platform Task Sheet 裁判打回（7.5/10），3 槽位已锁。
- 今日 task sheet 已下发主线 3 个：ai-video-sora-shutdown-openai-pivot、llama-cpp-kv-rotation-pr21038-aime25、nicolas-carlini-claude-security-vulnerability-research。
- 当前已有 5 个发布队列项进入 `waiting_human_publish`。

轻审批提醒：
- 待人工发布：`topic__20260327_092432__apple-siri-chatgpt-entry`，平台 `toutiao, xiaohongshu`。
- 待人工发布：`topic__20260328_213454__turboquant-qwen-macbook-air`，平台 `bilibili, x, xiaohongshu`。

下一阶段计划：
- 先把 task sheet 已下发主线推进成 Draft Pack，再进入 polish。
- 等人工发布后，补 publish URL，并开始 24h review。

需要人类协助：
- 若要继续推进成稿，需先拍板今日选题。
- `topic__20260327_092432__apple-siri-chatgpt-entry` 等待人工发布，平台：toutiao, xiaohongshu。
- `topic__20260328_213454__turboquant-qwen-macbook-air` 等待人工发布，平台：bilibili, x, xiaohongshu。

状态板：`/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/20260330__market-frontstage-board.md`

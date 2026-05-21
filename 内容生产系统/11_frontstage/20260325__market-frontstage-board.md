# Market Frontstage Board

- `date`: `2026-03-25`
- `generated_at`: `2026-03-26 02:09:36 CST`
- `frontstage_group_id`: `oc_8e290d3f3b5215cab938fef7d0e4a860`
- `board_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/20260325__market-frontstage-board.md`

## Snapshot

- `source_packets_today`: `40`
- `asset_chains_today`: `22`
- `topic_clusters_today`: `2`
- `top5_board_status`: `ready`
- `approved_topics_today`: `5`
- `active_draft_packs`: `5`
- `waiting_human_publish_items`: `15`
- `published_items_today`: `0`

## 当前正式任务

- `deerflow_super_agent_harness` 已进入待人工发布，待处理平台：wechat, x, zhihu。
- `minicor_production_computer_use` 已进入待人工发布，待处理平台：wechat, x, zhihu。
- `openai_agentic_product_discovery` 已进入待人工发布，待处理平台：wechat, x, xiaohongshu。
- `claude_code_auto_mode` 已进入待人工发布，待处理平台：wechat, x, zhihu。
- `remix_parallel_content_agents` 已进入待人工发布，待处理平台：wechat, x, xiaohongshu。

## 当前实际在做

- 当前实际在盯 `minicor_production_computer_use` 的人工发布闭环，平台：wechat, x, zhihu。
- 当前实际在盯 `openai_agentic_product_discovery` 的人工发布闭环，平台：wechat, x, xiaohongshu。
- 当前实际在盯 `deerflow_super_agent_harness` 的人工发布闭环，平台：wechat, x, zhihu。
- 当前实际在盯 `remix_parallel_content_agents` 的人工发布闭环，平台：wechat, x, xiaohongshu。
- 当前实际在盯 `claude_code_auto_mode` 的人工发布闭环，平台：wechat, x, zhihu。

## 组织边界

- 对外只保留 `market-editor` 这一个前台 bot；老板不直接和后台 agent 交互。
- 后台正式角色为 `market-scout`（按 `signal-scout` 语义运行）、`topic-planner`、`content-writer`、`redteam-reviewer`、`publish-ops`、`content-analyst`；全部独立 workspace / session 运行，且不允许越级回报。
- 正式角色职责矩阵见：`/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260326_内容工厂多Agent责任矩阵.md`。

## 关键决策与原因

- 入围 `mastra`：Mastra：AI Agents 基础设施的产品级答案｜原因：Product Hunt 高热 + 知乎/社交媒体已出现讨论；写"什么是靠谱 AI agents 开发框架"正当时。
- 入围 `claude-code-auto`：Claude Code Auto Mode：Agent 执行自主权争夺战进入新阶段｜原因：Reddit 高热 + 官方发布 + 与 TH 核心叙事高度吻合；真实用户反馈充分。
- 入围 `deerflow`：DeerFlow 2.0：Super Agent Harness 的生产级信号｜原因：从 demo 走向真实框架；多 packet 支撑；brand-fit 极强。
- 暂放 `karpathy-agency`：Karpathy 的"Agency > Intelligence"框架｜原因：单一 X 帖子内容深度有限，缺少一手事实支撑；更适合做已有选题的"佐证"而非独立主选题；捞回条件：若主选题已定，可作为文章"引子框架"使用；或在 DeerFlow/Claude Code 选题中直接引用。
- 暂放 `openai-product-discovery`：OpenAI 把 ACP 推进到 ChatGPT 内 product discovery｜原因：具体影响路径尚不明确；媒体报道为主，缺少用户侧验证；品牌贴合度弱于前 5；捞回条件：等更多 merchant 接入案例出现后捞回；或与 Remix 合并做"agent 消费侧落地"专题。
- 已拍板 `minicor_production_computer_use`：来自 Top 候选序号 `1`，推荐原因是：有真实企业痛点、有生产级关键词（self-healing / observability / no API legacy systems）、也有明确付费想象空间。
- 已拍板 `openai_agentic_product_discovery`：来自 Top 候选序号 `2`，推荐原因是：OpenAI 官方一手、平台级变化、对 agent 分发与商家接入有清晰影响。
- 已拍板 `deerflow_super_agent_harness`：来自 Top 候选序号 `3`，推荐原因是：GitHub 趋势热度 + super agent 叙事完整，能讲 stack 演化，也能讲 productization 门槛。

## 今日阶段性成果

- 今日新增 `source packet` 40 份、`asset chain` 22 份、`topic cluster` 2 份。
- 今日选题建议板已形成：`/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260325__daily-top8-to-top5.md`；优先关注：Mastra：AI Agents 基础设施的产品级答案 / Claude Code Auto Mode：Agent 执行自主权争夺战进入新阶段。
- 今日新增 `approved_topic` 5 个：minicor_production_computer_use, openai_agentic_product_discovery, deerflow_super_agent_harness, remix_parallel_content_agents。
- 今日推进中的 Draft Pack 5 个：claude_code_auto_mode, deerflow_super_agent_harness, minicor_production_computer_use, openai_agentic_product_discovery。
- 当前已有 15 个发布队列项进入 `waiting_human_publish`。

## 当前活跃对象池

- `minicor_production_computer_use` | `approved_topic` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/04_approved_topics/20260325_120000__minicor_production_computer_use__approved-topic.md`
- `openai_agentic_product_discovery` | `approved_topic` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/04_approved_topics/20260325_120500__openai_agentic_product_discovery__approved-topic.md`
- `deerflow_super_agent_harness` | `approved_topic` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/04_approved_topics/20260325_121000__deerflow_super_agent_harness__approved-topic.md`
- `remix_parallel_content_agents` | `approved_topic` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/04_approved_topics/20260325_162000__remix_parallel_content_agents__approved-topic.md`
- `claude_code_auto_mode` | `approved_topic` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/04_approved_topics/20260325_162200__claude_code_auto_mode__approved-topic.md`
- `claude_code_auto_mode` | `draft_pack` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/claude_code_auto_mode/00_draft-pack-card.md`
- `deerflow_super_agent_harness` | `draft_pack` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/deerflow_super_agent_harness/00_draft-pack-card.md`
- `minicor_production_computer_use` | `draft_pack` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/minicor_production_computer_use/00_draft-pack-card.md`
- `openai_agentic_product_discovery` | `draft_pack` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/openai_agentic_product_discovery/00_draft-pack-card.md`
- `remix_parallel_content_agents` | `draft_pack` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/remix_parallel_content_agents/00_draft-pack-card.md`
- `queue__20260325_120213__deerflow_super_agent_harness__wechat` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260325_120213__deerflow_super_agent_harness__wechat__publish-queue-item.md`
- `queue__20260325_120213__deerflow_super_agent_harness__x` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260325_120213__deerflow_super_agent_harness__x__publish-queue-item.md`
- `queue__20260325_120213__deerflow_super_agent_harness__zhihu` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260325_120213__deerflow_super_agent_harness__zhihu__publish-queue-item.md`
- `queue__20260325_120213__minicor_production_computer_use__wechat` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260325_120213__minicor_production_computer_use__wechat__publish-queue-item.md`
- `queue__20260325_120213__minicor_production_computer_use__x` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260325_120213__minicor_production_computer_use__x__publish-queue-item.md`
- `queue__20260325_120213__minicor_production_computer_use__zhihu` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260325_120213__minicor_production_computer_use__zhihu__publish-queue-item.md`
- `queue__20260325_120213__openai_agentic_product_discovery__wechat` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260325_120213__openai_agentic_product_discovery__wechat__publish-queue-item.md`
- `queue__20260325_120213__openai_agentic_product_discovery__x` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260325_120213__openai_agentic_product_discovery__x__publish-queue-item.md`
- `queue__20260325_120213__openai_agentic_product_discovery__xiaohongshu` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260325_120213__openai_agentic_product_discovery__xiaohongshu__publish-queue-item.md`
- `queue__20260325_154648__claude_code_auto_mode__wechat` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260325_154648__claude_code_auto_mode__wechat__publish-queue-item.md`
- `queue__20260325_154648__claude_code_auto_mode__x` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260325_154648__claude_code_auto_mode__x__publish-queue-item.md`
- `queue__20260325_154648__claude_code_auto_mode__zhihu` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260325_154648__claude_code_auto_mode__zhihu__publish-queue-item.md`
- `queue__20260325_154648__remix_parallel_content_agents__wechat` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260325_154648__remix_parallel_content_agents__wechat__publish-queue-item.md`
- `queue__20260325_154648__remix_parallel_content_agents__x` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260325_154648__remix_parallel_content_agents__x__publish-queue-item.md`
- `queue__20260325_154648__remix_parallel_content_agents__xiaohongshu` | `publish_queue` | `waiting_human_publish` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/20260325_154648__remix_parallel_content_agents__xiaohongshu__publish-queue-item.md`

## 轻审批与提醒

- 待人工发布：`minicor_production_computer_use`，平台 `wechat, x, zhihu`。
- 待人工发布：`openai_agentic_product_discovery`，平台 `wechat, x, xiaohongshu`。
- 待人工发布：`deerflow_super_agent_harness`，平台 `wechat, x, zhihu`。
- 待人工发布：`remix_parallel_content_agents`，平台 `wechat, x, xiaohongshu`。
- 待人工发布：`claude_code_auto_mode`，平台 `wechat, x, zhihu`。

## 下一阶段计划

- 等人工发布后，补 publish URL，并开始 24h review。

## 自动化边界

- 自动化负责：抓源、补查、收束候选、起稿、打磨、排版 handoff、排队提醒。
- 人工负责：选题确认、最终发布、真实链接回填、效果数据回填。
- 浏览器自动化只允许做无 API 平台的兜底发稿 / 截图验收，不允许成为主链决策中心。

## 人类协助

- 今日强候选供给不足，建议补充更强热点源或允许从 holdout 手动捞回。
- `minicor_production_computer_use` 等待人工发布，平台：wechat, x, zhihu。
- `openai_agentic_product_discovery` 等待人工发布，平台：wechat, x, xiaohongshu。
- `deerflow_super_agent_harness` 等待人工发布，平台：wechat, x, zhihu。
- `remix_parallel_content_agents` 等待人工发布，平台：wechat, x, xiaohongshu。
- `claude_code_auto_mode` 等待人工发布，平台：wechat, x, zhihu。

## 今日日志时间线

- `19:33` 更新 Topic Radar execution | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325__market-topic-radar-execution.md`
- `19:30` 形成今日 Top 8 -> Top 5 建议板 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260325__daily-top8-to-top5.md`
- `19:27` 更新 Topic Radar brief | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325__market-topic-radar-brief.md`
- `18:56` 完成一轮弱链补查 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325_185631__market-asset-query-resolution-summary.md`
- `18:36` 完成一轮对象一跳派生 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325_183639__market-asset-derivation-summary.md`
- `18:18` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325_181758__market-topic-capture-summary.md`
- `15:46` 推进内容打磨 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325_154648__claude_code_auto_mode__content-polish-execution.md`
- `15:46` 推进内容打磨 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325_154648__remix_parallel_content_agents__content-polish-execution.md`
- `15:27` 推进 Draft Pack | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325_152705__remix_parallel_content_agents__draft-pack-execution.md`
- `15:27` 更新内容工厂对象 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325_162200__claude_code_auto_mode__topic-approval-execution.md`
- `15:27` 更新内容工厂对象 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325_162000__remix_parallel_content_agents__topic-approval-execution.md`
- `13:24` 完成一轮 source capture | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325_132359__market-topic-capture-summary.md`
- `12:05` 推进内容复盘 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325_120236__deerflow_super_agent_harness__performance-review-execution.md`
- `12:05` 推进内容复盘 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325_120236__openai_agentic_product_discovery__performance-review-execution.md`
- `12:05` 推进内容复盘 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325_120236__minicor_production_computer_use__performance-review-execution.md`
- `12:05` 推进发布队列 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325_120213__deerflow_super_agent_harness__publish-queue-execution.md`
- `12:05` 推进发布队列 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325_120213__openai_agentic_product_discovery__publish-queue-execution.md`
- `12:05` 推进发布队列 | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260325_120213__minicor_production_computer_use__publish-queue-execution.md`

## 群同步草稿

内容工厂状态已更新。

当前正式任务：
1. `deerflow_super_agent_harness` 已进入待人工发布，待处理平台：wechat, x, zhihu。
2. `minicor_production_computer_use` 已进入待人工发布，待处理平台：wechat, x, zhihu。
3. `openai_agentic_product_discovery` 已进入待人工发布，待处理平台：wechat, x, xiaohongshu。
4. `claude_code_auto_mode` 已进入待人工发布，待处理平台：wechat, x, zhihu。

当前实际在做：
- 当前实际在盯 `minicor_production_computer_use` 的人工发布闭环，平台：wechat, x, zhihu。
- 当前实际在盯 `openai_agentic_product_discovery` 的人工发布闭环，平台：wechat, x, xiaohongshu。
- 当前实际在盯 `deerflow_super_agent_harness` 的人工发布闭环，平台：wechat, x, zhihu。

关键决策：
- 入围 `mastra`：Mastra：AI Agents 基础设施的产品级答案｜原因：Product Hunt 高热 + 知乎/社交媒体已出现讨论；写"什么是靠谱 AI agents 开发框架"正当时。
- 入围 `claude-code-auto`：Claude Code Auto Mode：Agent 执行自主权争夺战进入新阶段｜原因：Reddit 高热 + 官方发布 + 与 TH 核心叙事高度吻合；真实用户反馈充分。
- 入围 `deerflow`：DeerFlow 2.0：Super Agent Harness 的生产级信号｜原因：从 demo 走向真实框架；多 packet 支撑；brand-fit 极强。

阶段性成果：
- 今日新增 `source packet` 40 份、`asset chain` 22 份、`topic cluster` 2 份。
- 今日选题建议板已形成：`/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260325__daily-top8-to-top5.md`；优先关注：Mastra：AI Agents 基础设施的产品级答案 / Claude Code Auto Mode：Agent 执行自主权争夺战进入新阶段。
- 今日新增 `approved_topic` 5 个：minicor_production_computer_use, openai_agentic_product_discovery, deerflow_super_agent_harness, remix_parallel_content_agents。
- 今日推进中的 Draft Pack 5 个：claude_code_auto_mode, deerflow_super_agent_harness, minicor_production_computer_use, openai_agentic_product_discovery。

轻审批提醒：
- 待人工发布：`minicor_production_computer_use`，平台 `wechat, x, zhihu`。
- 待人工发布：`openai_agentic_product_discovery`，平台 `wechat, x, xiaohongshu`。
- 待人工发布：`deerflow_super_agent_harness`，平台 `wechat, x, zhihu`。

下一阶段计划：
- 等人工发布后，补 publish URL，并开始 24h review。

需要人类协助：
- 今日强候选供给不足，建议补充更强热点源或允许从 holdout 手动捞回。
- `minicor_production_computer_use` 等待人工发布，平台：wechat, x, zhihu。
- `openai_agentic_product_discovery` 等待人工发布，平台：wechat, x, xiaohongshu。

状态板：`/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/20260325__market-frontstage-board.md`

# 后续开发任务清单

## 开发原则

- 每个 checkpoint 都要有目标、变更文件、验收方式和下一步建议。
- 先保证可运行、可检查、可交接，再扩大自动化范围。
- 不破坏 official lane、topic capture lane 和现有生成产物格式。
- generated artifacts 默认不进入 Git；需要共享时提取小型摘要。
- 不提交 `.env`、本机绝对路径、cookie、token、数据库或本地运行态文件。
- 自动发布、真实 LLM live mode、真实平台 API、人工反馈学习都必须有独立 checkpoint。

## Phase 0：已完成

- P0-001 到 P0-017 已完成，覆盖工程底座、路径配置、source registry、runtime manifest、official lane daily full run、quality gate 与 dashboard。

## Phase 1：已完成

- P1-001 到 P1-007 已完成，覆盖 evidence packet、topic cluster、value scoring、high-value candidate pool 与 phase1 daily pipeline。

## Phase 2：已完成

- P2-001 到 P2-008 已完成，覆盖 content brief、outline、draft、quality review、platform package、content workbench 与 phase2 daily pipeline。

## Phase 3：已完成

- P3-001 到 P3-009 已完成，覆盖 agent review queue、proponent / critic / judge、revision instructions、human exception queue、agent review dashboard 与 phase3 daily pipeline。

## Phase 4：已完成

- P4-001 到 P4-007 已完成，覆盖 publishing candidate queue、human feedback template、review outcome memory、rule update suggestions、learning loop dashboard 与 phase4 daily pipeline。

## Phase 5：已完成

- P5-001 到 P5-008 已完成，覆盖 head media pattern library、title/opening/structure pattern extraction、content recipe suggestions、pattern adapters、phase5 daily learning pipeline 与 learning daily pipeline。

## Phase 6：真实 LLM Agent 接入与多 Agent 调优 v1

### P6-001：LLM Provider Config v1

状态：Done。

目标：

- 建立 `config/llm_providers.json`。
- 默认 provider 为 mock，默认 mode 为 dry_run。
- 建立 agent model map：轻量任务走 `manimax-2.7`，高判断任务走 `claude-sonnet-4.6`。
- API key 只从环境变量读取，不提交 `.env` 或真实 key。

### P6-002：Prompt Registry v1

状态：Done。

目标：

- 建立 `config/agent_prompts.json`。
- 管理 proponent / critic / judge / rewrite agent 的 prompt、输入 schema、输出 schema 和版本号。
- 在 prompt registry 中记录 LLM Agent 的 preferred provider / model。
- prompt 明确要求只使用输入 evidence、不编造事实、返回 JSON、不发布。

### P6-003：LLM Agent Client v1

状态：Done。

目标：

- 新增 mock-first LLM agent client。
- 支持结构化 request / response。
- 非 mock live provider 在 v1 中保持占位，不默认发起真实网络调用。

### P6-004：LLM Proponent Agent v1

状态：Done。

目标：

- 基于 review queue、platform package 和 content brief 生成 LLM proponent review。
- 默认 mock/dry-run。
- 保留规则型 fallback。

### P6-005：LLM Critic Agent v1

状态：Done。

目标：

- 基于 review queue、platform package 和 quality review 生成 LLM critic review。
- 输出结构化 concerns、suggestions 和 must-fix。
- 保留规则型 fallback。

### P6-006：LLM Judge Agent v1

状态：Done。

目标：

- 基于 LLM proponent / critic 与 rule judge 生成 LLM judge sidecar。
- 不直接覆盖 rule judge。
- 冲突时记录 comparison 并建议 human spot check。

### P6-007：LLM Rewrite Agent v1

状态：Done。

目标：

- 基于 revision instructions、draft、platform package 和 LLM reviews 生成 rewrite suggestions。
- 不自动覆盖原稿。

### P6-008：Agent Run Log / Cost / Error Tracking v1

状态：Done。

目标：

- 记录每次 LLM agent 调用，包括 mock/dry-run。
- 记录 provider、model、mode、状态、token 估算、成本估算、错误和 fallback。
- 生成 agent run summary。

### P6-009：Human-in-the-loop Agent Evaluation v1

状态：Done。

目标：

- 生成 LLM agent 输出的人工评估模板。
- 校验评分、action、agent_name 和 artifact_id。

### P6-010：Phase 6 Daily Agent Pipeline v1

状态：Done。

目标：

- 新增 `make phase6-daily`。
- 串联 learning daily、provider config validate、prompt validate、LLM agent reviews、run summary 和 evaluation template。

### P6-011：Phase 6 Closeout

状态：Done。

目标：

- 新增 Phase 6 closeout 报告。
- 维护项目状态和任务清单。
- 明确 Phase 7 入口。

## Phase 7：真实 LLM Live Mode 灰度与自动调度

### P7-001：OpenAI Live Adapter Pilot

目标：

- 在不破坏 mock/dry-run 的前提下，选择一个 agent 做 live adapter pilot。
- API key 只从环境变量读取。
- 输出和 mock agent 使用同一 schema。

### P7-002：LLM Agent A/B Comparison

目标：

- 比较 rule agent、mock agent、live LLM agent 的输出差异。

### P7-003：Agent Rewrite Loop v1

目标：

- 使用 rewrite suggestions 生成候选改稿，但不自动覆盖原稿。

### P7-004：Daily Scheduler v1

目标：

- 建立本地每日调度入口。
- 不依赖云服务，先支持本机 cron/launchd 文档。

### P7-005：Failure Notification v1

目标：

- 生成失败通知报告。
- 暂不接微信/邮件真实推送。

### P7-006：Retry / Fallback Runner v1

目标：

- 对采集失败源建立重试与 fallback 入口。

### P7-007：Weekly Content Retro v1

目标：

- 每周汇总内容表现、人工反馈、Agent 输出质量和规则调整建议。

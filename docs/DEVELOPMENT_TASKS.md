# 后续开发任务清单

## 开发原则

- 每个 checkpoint 都要有目标、变更文件、验收方式和下一步建议。
- 先保证可运行、可检查、可交接，再扩大自动化范围。
- 不破坏 official lane、topic capture lane 和现有生成产物格式。
- generated artifacts 默认不进入 Git；需要共享时提取小型摘要。
- 不提交 `.env`、本机绝对路径、cookie、token、数据库或本地运行态文件。
- 自动发布、LLM 生成、真实平台 API、人工反馈学习都必须有独立 checkpoint。

## Phase 0：已完成

- P0-001 项目状态与健康检查底座。
- P0-002 路径硬编码审计工具。
- P0-002b 清理 path audit 生成产物入库问题。
- P0-003 路径配置化第一刀。
- P0-003b 修复/确认核心路径配置文件格式与验收链路。
- P0-004 HIGH 风险路径配置化第二刀。
- P0-005 Source Registry v1。
- P0-006 Source Health v1。
- P0-007 Source Runtime Health Adapter v1。
- P0-007b 补齐 Source Runtime Health 状态文档。
- P0-008 Runtime Manifest Contract v1。
- P0-009 Runtime Manifest Writer v1。
- P0-010 Official Lane Runtime Manifest Pilot Integration v1。
- P0-010b 补齐 official lane / runtime health generated artifacts ignore 规则。
- P0-011A Source Runtime Health Manifest Reader。
- P0-011B Official Lane Health Check Wrapper v1。
- P0-012 Official Lane Daily Entry v1。
- P0-013 Daily Source Run Summary v1。
- P0-014 Daily Official Lane Quality Gate v1。
- P0-014b 补齐 Quality Gate 状态文档。
- P0-015 Official Daily Dashboard v1。
- P0-015b 补齐 Official Daily Dashboard 状态文档。
- P0-016 Official Daily Full Run v1。
- P0-017 Phase 0 Closeout。

## Phase 1：已完成

- P1-001 Official Lane Runtime Baseline v1。
- P1-002 Source Registry Coverage Alignment v1。
- P1-003 Evidence Packet v1。
- P1-004 Topic Cluster v1。
- P1-005 Value Scoring v1。
- P1-006 Daily High-Value Candidate Pool v1。
- P1-007 Phase 1 Closeout。

## Phase 2：已完成

- P2-001 Content Brief Builder v1。
- P2-002 Outline Builder v1。
- P2-003 Draft Writer v1。
- P2-004 Content Quality Review v1。
- P2-005 Platform Packaging v1。
- P2-006 Daily Content Production Pipeline v1。
- P2-007 Content Workbench Board v1。
- P2-008 Phase 2 Closeout。

## Phase 3：Agent Review Workflow 与人工抽检闭环 v1

### P3-001：Agent Review Queue v1

状态：Done。

目标：

- 将 platform packages 转成 Agent 审核队列。
- 为每个 package 记录质量状态、风险、优先级和进入 Agent Review 的原因。
- 不自动发布。

验收：

- `make review-queue` 可生成 JSON/Markdown。

### P3-002：Proponent Agent Review v1

状态：Done。

目标：

- 用规则型 proponent editor simulation 输出“为什么值得推进”的提案 memo。
- 生成 support_level、publish_argument、strongest_points、confidence。

验收：

- `make proponent-reviews` 可生成 JSON/Markdown。

### P3-003：Critic Agent Review v1

状态：Done。

目标：

- 用规则型 critical senior editor simulation 挑出证据、逻辑、标题、平台适配和风险问题。
- 输出建设性修改建议与 must-fix 列表。

验收：

- `make critic-reviews` 可生成 JSON/Markdown。

### P3-004：Judge Agent Gate v1

状态：Done。

目标：

- 汇总 queue item、proponent review、critic review、quality review 和 platform package。
- 输出 APPROVED_FOR_QUEUE、NEEDS_REVISION、HOLD 或 ESCALATE_TO_HUMAN。

验收：

- `make judge-gate` 可生成 JSON/Markdown。

### P3-005：Revision Instruction Builder v1

状态：Done。

目标：

- 对 NEEDS_REVISION 和 ESCALATE_TO_HUMAN 项生成明确修改指令。
- 分拆 title、opening、logic、evidence、risk 和 platform fixes。

验收：

- `make revision-instructions` 可生成 JSON/Markdown。

### P3-006：Human Exception Queue v1

状态：Done。

目标：

- 只把高风险、高争议、低置信或阈值附近的内容送入人工抽检队列。
- 避免把所有 NEEDS_REVISION 都推给用户。

验收：

- `make human-exception-queue` 可生成 JSON/Markdown。

### P3-007：Agent Review Dashboard v1

状态：Done。

目标：

- 生成每天给用户看的 Agent Review Dashboard。
- 展示 human attention required、approved、needs revision、hold、agent disagreement 和 next actions。

验收：

- `make agent-review-dashboard` 可生成 frontstage Markdown 和 JSON。

### P3-008：Phase 3 Daily Review Pipeline v1

状态：Done。

目标：

- 新增 `make phase3-daily`。
- 串联 Phase 2 daily、review queue、proponent、critic、judge、revision、human exception queue 和 dashboard。

验收：

- `make phase3-daily` 可运行，成功或合理 DEGRADED，但不能崩溃。

### P3-009：Phase 3 Closeout

状态：Done。

目标：

- 新增 Phase 3 closeout 报告。
- 更新项目状态与任务清单。
- 明确 Phase 4 入口。

验收：

- `docs/PROJECT_STATE.md` 和 `docs/DEVELOPMENT_TASKS.md` 反映 Phase 3 完成态。

## Phase 3 验收标准

- 新增 Phase 3 scripts 和 modules 全部通过 `py_compile`。
- `make phase2-daily` 可运行。
- `make review-queue` 可运行。
- `make proponent-reviews` 可运行。
- `make critic-reviews` 可运行。
- `make judge-gate` 可运行。
- `make revision-instructions` 可运行。
- `make human-exception-queue` 可运行。
- `make agent-review-dashboard` 可运行。
- `make phase3-daily` 可运行。
- `make doctor`、`make path-audit`、`make sources-validate`、`make source-health`、`make source-runtime-health`、`make manifest-validate` 继续可运行。
- Phase 3 generated artifacts 不进入 Git。

## Phase 4：发布准备、反馈学习与策略迭代

### P4-001：Publishing Candidate Queue v1

目标：

- 将 Judge Gate 通过的内容进入发布候选队列。
- 不自动发布。
- 为每个 package 记录 publish readiness、platform、人工确认状态。

### P4-002：Human Feedback Capture v1

目标：

- 记录用户对候选内容的反馈。
- 包括 approve、revise、hold、reject、notes、score。

### P4-003：Review Outcome Memory v1

目标：

- 把 agent review、human feedback、final outcome 汇总成历史记录。
- 为后续学习闭环提供数据。

### P4-004：Rule Update Suggestion v1

目标：

- 基于人工反馈，生成 value scoring、brief、outline、review rules 的调整建议。
- 不自动修改规则，只给建议。

### P4-005：Learning Loop Dashboard v1

目标：

- 展示哪些选题被通过、哪些被拒、常见问题是什么、规则应如何调整。

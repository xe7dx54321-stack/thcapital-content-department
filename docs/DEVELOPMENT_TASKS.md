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

## Phase 2：内容生产质量链路 v1

### P2-001：Content Brief Builder v1

状态：Done。

目标：

- 从 high-value candidates 生成 content briefs。
- brief 包含核心判断、为什么现在重要、证据、风险、缺口、目标平台和编辑优先级。
- 不直接生成成品文章。

验收：

- `make content-briefs` 可生成 JSON/Markdown。

### P2-002：Outline Builder v1

状态：Done。

目标：

- 从 content briefs 生成结构化大纲。
- 同时输出 wechat_outline 和 xiaohongshu_outline。
- 保留 required evidence 和 editor notes。

验收：

- `make content-outlines` 可生成 JSON/Markdown。

### P2-003：Draft Writer v1

状态：Done。

目标：

- 用规则模板从 outlines 生成初稿。
- 草稿必须包含核心判断、为什么现在重要、证据、风险提示和人工编辑提示。
- 不调用 LLM，不假装最终可发布。

验收：

- `make content-drafts` 可生成 JSON/Markdown。

### P2-004：Content Quality Review v1

状态：Done。

目标：

- 对 drafts 做规则型质量检查。
- 检查 evidence 数量、标题、正文长度、风险披露、source_id、evidence_id 和过强表述。
- 输出 READY_FOR_HUMAN_REVIEW、NEEDS_LIGHT_EDIT、NEEDS_MAJOR_EDIT 或 HOLD。

验收：

- `make content-quality-review` 可生成 JSON/Markdown。

### P2-005：Platform Packaging v1

状态：Done。

目标：

- 将通过质量检查的 drafts 转成 wechat / xiaohongshu 平台包。
- 所有 package 都保留 `human_review_required=true`。
- HOLD 项不生成正式 package，只记录 blocked reason。

验收：

- `make platform-packages` 可生成 JSON/Markdown。

### P2-006：Daily Content Production Pipeline v1

状态：Done。

目标：

- 新增 `make phase2-daily`。
- 串联 Phase 1 daily pipeline、brief、outline、draft、quality review、platform package 和 workbench。

验收：

- `make phase2-daily` 可运行，成功或合理 DEGRADED，但不能崩溃。

### P2-007：Content Workbench Board v1

状态：Done。

目标：

- 生成每天给人工编辑查看的内容工作台。
- 展示 summary、ready for human review、needs editing、hold、top briefs 和 next actions。

验收：

- `make content-workbench` 可生成 frontstage Markdown 和 JSON。

### P2-008：Phase 2 Closeout

状态：Done。

目标：

- 新增 Phase 2 closeout 报告。
- 更新项目状态与任务清单。
- 明确 Phase 3 入口。

验收：

- `docs/PROJECT_STATE.md` 和 `docs/DEVELOPMENT_TASKS.md` 反映 Phase 2 完成态。

## Phase 2 验收标准

- 新增 Phase 2 scripts 和 modules 全部通过 `py_compile`。
- `make phase1-daily` 可运行。
- `make content-briefs` 可运行。
- `make content-outlines` 可运行。
- `make content-drafts` 可运行。
- `make content-quality-review` 可运行。
- `make platform-packages` 可运行。
- `make content-workbench` 可运行。
- `make phase2-daily` 可运行。
- `make doctor`、`make path-audit`、`make sources-validate`、`make source-health`、`make source-runtime-health`、`make manifest-validate` 继续可运行。
- Phase 2 generated artifacts 不进入 Git。

## Phase 3：Agent Workflow 与人工审核闭环

### P3-001：Content Review Queue v1

目标：

- 将 platform packages 放入人工审核队列。
- 为每个 package 记录 review status。
- 不自动发布。

### P3-002：Human Feedback Capture v1

目标：

- 记录人工对 brief、outline、draft、package 的评分与修改意见。
- 为后续规则和 Agent 工作流迭代提供数据。

### P3-003：Agent Workflow Orchestrator v1

目标：

- 建立可配置 workflow，不再只靠 Makefile 串命令。
- 仍保持人工可控。

### P3-004：Publishing Queue v1

目标：

- 生成待发布队列。
- 不接真实 API，先做文件级 queue。

### P3-005：Learning Loop v1

目标：

- 将人工反馈回流到 value scoring、brief rules、outline rules。
- 形成可审计的规则迭代记录。

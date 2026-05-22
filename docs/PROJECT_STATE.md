# 同行资本内容部门项目状态

## 项目目标

本仓库是“同行资本 AI/Agent 领域内容生产 Agent 系统”的工程仓库。系统目标是每天自动化获取 AI 和 Agent 领域一手高价值信息，对信息进行结构化、价值判断、选题筛选，并进一步支撑微信公众号文章、小红书推文等内容生产；同时通过学习头部自媒体文章的选题、结构、标题和呈现方式实现系统自我迭代。

## 当前阶段

Phase 2：内容生产质量链路 v1。

## 最新 checkpoint

P2-008：Phase 2 v1 Closeout。

## 已完成

### Phase 0

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

### Phase 1

- P1-001 Official Lane Runtime Baseline v1。
- P1-002 Source Registry Coverage Alignment v1。
- P1-003 Evidence Packet v1。
- P1-004 Topic Cluster v1。
- P1-005 Value Scoring v1。
- P1-006 Daily High-Value Candidate Pool v1。
- P1-007 Phase 1 Closeout。

### Phase 2

- P2-001 Content Brief Builder v1。
- P2-002 Outline Builder v1。
- P2-003 Draft Writer v1。
- P2-004 Content Quality Review v1。
- P2-005 Platform Packaging v1。
- P2-006 Daily Content Production Pipeline v1。
- P2-007 Content Workbench Board v1。
- P2-008 Phase 2 Closeout。

## 当前已具备能力

### Phase 0 能力

- official daily full run。
- health check。
- path audit。
- source registry。
- runtime manifest。
- quality gate。
- dashboard。

### Phase 1 能力

- evidence packet。
- topic cluster。
- value scoring。
- high-value candidate pool。
- phase1 daily pipeline。

### Phase 2 能力

- content brief。
- outline。
- draft。
- quality review。
- platform package。
- content workbench。
- phase2 daily pipeline。

## 当前推荐日常命令

```bash
make phase2-daily
```

该命令串联 Phase 1 数据结构化链路和 Phase 2 内容生产质量链路，输出 brief、outline、draft、quality review、platform package 和 content workbench。

## 最近实测基线

- `make phase2-daily`：SUCCESS。
- content briefs：5。
- content outlines：5。
- content drafts：5。
- quality reviews：5。
- platform packages：5。
- content workbench：ready_for_human_review 1，needs_edit 4，hold 0。
- `make doctor`：通过，仅 network_check 默认跳过。
- `make path-audit`：通过，HIGH 约 59。

## 当前边界

- Brief、outline、draft 都是规则型生成。
- 尚未接入 LLM。
- 尚未自动发布。
- 尚未接公众号/小红书 API。
- 尚未新增数据库。
- 尚未做人工反馈学习。
- 尚未做多 Agent 编排。
- 所有 platform package 都要求 human review，不允许自动发布。

## 下一阶段

Phase 3：Agent Workflow 与人工审核闭环。

优先任务：

- P3-001：Content Review Queue v1。
- P3-002：Human Feedback Capture v1。
- P3-003：Agent Workflow Orchestrator v1。
- P3-004：Publishing Queue v1。
- P3-005：Learning Loop v1。

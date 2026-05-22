# 同行资本内容部门项目状态

## 项目目标

本仓库是“同行资本 AI/Agent 领域内容生产 Agent 系统”的工程仓库。系统目标是每天自动化获取 AI 和 Agent 领域一手高价值信息，对信息进行结构化、价值判断、选题筛选，并进一步支撑微信公众号文章、小红书推文等内容生产；同时通过学习头部自媒体文章的选题、结构、标题和呈现方式实现系统自我迭代。

## 当前阶段

Phase 5：头部内容学习反哺系统 v1。

## 最新 checkpoint

P5-008：Phase 5 v1 Closeout。

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

### Phase 3

- P3-001 Agent Review Queue v1。
- P3-002 Proponent Agent Review v1。
- P3-003 Critic Agent Review v1。
- P3-004 Judge Agent Gate v1。
- P3-005 Revision Instruction Builder v1。
- P3-006 Human Exception Queue v1。
- P3-007 Agent Review Dashboard v1。
- P3-008 Phase 3 Daily Review Pipeline v1。
- P3-009 Phase 3 Closeout。

### Phase 4

- P4-001 Publishing Candidate Queue v1。
- P4-002 Human Feedback Capture v1。
- P4-003 Review Outcome Memory v1。
- P4-004 Rule Update Suggestion v1。
- P4-005 Learning Loop Dashboard v1。
- P4-006 Phase 4 Daily Pipeline v1。
- P4-007 Phase 4 Closeout。

### Phase 5

- P5-001 Head Media Pattern Library v1。
- P5-002 Title Pattern Extractor v1。
- P5-003 Opening Pattern Extractor v1。
- P5-004 Article Structure Pattern Extractor v1。
- P5-005 Content Recipe Suggestion v1。
- P5-006 Pattern-to-Brief / Pattern-to-Outline Adapter v1。
- P5-007 Phase 5 Daily Learning Pipeline v1。
- P5-008 Phase 5 Closeout。

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

### Phase 3 能力

- agent review queue。
- proponent review。
- critic review。
- judge gate。
- revision instructions。
- human exception queue。
- agent review dashboard。
- phase3 daily pipeline。

### Phase 4 能力

- publishing candidate queue。
- human feedback template / validation。
- review outcome memory。
- rule update suggestions。
- learning loop dashboard。
- phase4 daily pipeline。

### Phase 5 能力

- head media pattern library。
- title pattern extraction。
- opening pattern extraction。
- structure pattern extraction。
- content recipe suggestions。
- pattern adapters。
- phase5 daily learning pipeline。
- learning daily pipeline。

## 当前推荐日常命令

```bash
make learning-daily
```

该命令串联 Phase 3 Agent Review、Phase 4 发布准备与反馈学习、Phase 5 头部内容模式学习反哺。

## 最近实测基线

- `make phase4-daily`：SUCCESS。
- publishing candidates：2。
- human feedback template items：2。
- review outcome memory records：3。
- rule update suggestions：1。
- `make phase5-daily`：SUCCESS。
- pattern library patterns：8。
- title patterns：35。
- opening patterns：10。
- structure patterns：4。
- content recipe suggestions：4。
- pattern adapters：5。
- `make learning-daily`：SUCCESS。
- `make doctor`：通过，仅 network_check 默认跳过。
- `make path-audit`：通过，HIGH 约 59。

## 当前边界

- 还没有接真实 LLM Agent。
- 还没有自动发布。
- 还没有接公众号/小红书 API。
- 还没有数据库型长期记忆。
- 规则建议不会自动应用。
- pattern adapter 只生成建议，不直接重写 brief/outline。
- human feedback 仍是文件型模板，不是 UI。

## 下一阶段

Phase 6：真实 LLM Agent 接入与多 Agent 调优。

优先任务：

- P6-001：LLM Provider Config v1。
- P6-002：Prompt Registry v1。
- P6-003：LLM Proponent Agent v1。
- P6-004：LLM Critic Agent v1。
- P6-005：LLM Judge Agent v1。
- P6-006：LLM Rewrite Agent v1。
- P6-007：Agent Run Log / Cost / Error Tracking v1。
- P6-008：Human-in-the-loop Agent Evaluation v1。

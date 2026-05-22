# 同行资本内容部门项目状态

## 项目目标

本仓库是“同行资本 AI/Agent 领域内容生产 Agent 系统”的工程仓库。系统目标是每天自动化获取 AI 和 Agent 领域一手高价值信息，对信息进行结构化、价值判断、选题筛选，并进一步支撑微信公众号文章、小红书推文等内容生产；同时通过学习头部自媒体文章的选题、结构、标题和呈现方式实现系统自我迭代。

## 当前阶段

Phase 1：采集稳定性与信息结构化 v1。

## 最新 checkpoint

P1-007：Phase 1 v1 Closeout。

## 已完成

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
- P1-001 Official Lane Runtime Baseline v1。
- P1-002 Source Registry Coverage Alignment v1。
- P1-003 Evidence Packet v1。
- P1-004 Topic Cluster v1。
- P1-005 Value Scoring v1。
- P1-006 Daily High-Value Candidate Pool v1。
- P1-007 Phase 1 Closeout。

## 当前已具备能力

### Phase 0 能力

- `make doctor`：项目健康检查。
- `make path-audit`：路径硬编码审计。
- `src/content_system/paths.py`：统一路径配置。
- `config/sources.yaml` 与 `make sources-validate`：source registry。
- `make source-health`：静态 source health / coverage 报告。
- `make source-runtime-health`：runtime evidence 对齐。
- `make manifest-validate`：runtime manifest 合约校验。
- `make manifest-write-from-packets`：从 packet 生成 manifest。
- `make official-lane-with-manifest`：official lane manifest pilot。
- `make official-lane-health-check`：official lane 健康检查 wrapper。
- `make official-lane-daily` / `make daily-official-lane`：official lane 日常入口。
- `make daily-source-summary`：每日 source run summary。
- `make official-lane-quality-gate`：report-only quality gate。
- `make official-daily-dashboard`：official daily dashboard。
- `make official-daily-full-run` / `make daily-official-full-run`：official lane 全流程日常入口。
- generated artifacts ignore 规则：运行产物默认不进入 Git。

### Phase 1 能力

- Official runtime baseline：`make runtime-baseline`。
- Source coverage alignment：`make source-coverage`。
- Evidence Packet v1：`make evidence-packets`。
- Topic Cluster v1：`make topic-clusters`。
- Value Scoring v1：`make value-scores`。
- Daily High-Value Candidate Pool：`make high-value-candidates`。
- Phase 1 daily pipeline：`make phase1-daily`。

## 当前推荐日常命令

```bash
make phase1-daily
```

该命令串联 official daily full run、runtime baseline、source coverage、evidence packet、topic cluster、value scoring 和 high-value candidate pool。

## 最近实测基线

- `make official-daily-full-run`：SUCCESS。
- official lane steps：5 个步骤全 OK。
- source_count：9。
- total_items_found：57。
- quality_gate_status：GREEN。
- `make doctor`：通过，仅 network_check 默认跳过。
- `make path-audit`：通过，HIGH 约 59。
- `make sources-validate`：通过，17 sources，17 enabled，ERROR 0，WARN 0。
- `make manifest-validate`：通过。

## 当前边界

- Evidence packet 仍是规则型抽取。
- Topic cluster 仍是规则型聚类。
- Value scoring 仍是启发式规则评分。
- 尚未进入 LLM 内容生成。
- 尚未生成微信公众号/小红书成品内容。
- 尚未做人工反馈学习。
- 尚未做 retry/fallback。
- 尚未新增数据库或调度系统。
- Source runtime health 对非 official lane 的结构化覆盖仍有限。

## 下一阶段

Phase 2：内容生产质量链路。

优先任务：

- P2-001：Content Brief Builder v1。
- P2-002：Outline Builder v1。
- P2-003：Draft Writer v1。
- P2-004：Fact / Evidence Check v1。
- P2-005：Platform Packaging v1。

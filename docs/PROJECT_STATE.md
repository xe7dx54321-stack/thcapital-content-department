# 同行资本内容部门项目状态

## 项目目标

`thcapital-content-department` 是同行资本 AI/Agent 领域内容生产 Agent 系统的工程仓库。系统目标是每天自动化获取 AI 和 Agent 领域一手高价值信息，对信息进行结构化、价值判断、选题筛选，并进一步生成微信公众号文章、小红书推文等内容，同时通过学习头部自媒体文章的选题、结构、标题和呈现方式实现自我迭代。

## 当前阶段

Phase 0 工程地基修复与 official lane 稳定化收口。

Phase 0 的目标不是重写业务主链路，而是把项目的工程状态、路径配置、审计能力、source registry、runtime manifest、source health、official lane 日常入口和 generated artifacts 边界整理到可交接状态。

## 当前最新 checkpoint

P0-016 / P0-017：Official Daily Full Run v1 + Phase 0 Closeout。

## 已完成 checkpoint

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

## 当前已具备能力

### 工程底座

- `make doctor`：检查项目根目录、关键业务目录、核心脚本、frontstage/logs 写入能力。
- `make path-audit`：扫描本机绝对路径、旧路径和运行态路径，生成本地审计报告。
- 路径配置化：通过 `src/content_system/paths.py` 和环境变量统一解析核心目录。
- generated artifacts ignore 规则：path audit、source health、runtime manifest、daily summary、quality gate、dashboard、official full run 等运行产物默认不入 Git。

### Source Registry / Health

- `config/sources.yaml`：统一 source registry v1。
- `make sources-validate`：校验 source registry 结构和字段约束。
- `make source-health`：生成静态 source health / coverage 报告。
- `make source-runtime-health`：基于运行产物和 runtime manifest 生成 runtime health 报告。

### Runtime Manifest

- `make manifest-validate`：校验 runtime manifest 合约。
- `make manifest-write-from-packets`：从已有 source packet 产物生成 runtime manifest。
- official lane runtime manifest wrapper：通过 wrapper 跑 official lane，并额外写 manifest，不修改 official lane 主脚本。

### Official Daily Lane

- `make official-lane-daily`
- `make daily-official-lane`
- `make official-lane-health-check`
- `make daily-source-summary`
- `make official-lane-quality-gate`
- `make daily-official-quality-gate`
- `make official-daily-dashboard`
- `make daily-official-dashboard`
- `make official-daily-full-run`
- `make daily-official-full-run`

`make official-daily-full-run` 是 Phase 0 收口后的推荐日常入口，会串联 official lane health check、source runtime health、daily summary、quality gate 和 official daily dashboard。

## 最近实测基线

用户本地实测 official lane：

- official lane status：SUCCESS。
- source_count：9。
- total_items_found：57。
- daily summary status：SUCCESS。
- missing_expected：12。
- error_hint_sources：2。
- doctor：OK。
- path-audit：OK，HIGH 约 59。

本仓库后续以本地命令输出为准，不再以 GitHub raw 抓取显示判断物理换行或脚本可运行性。

## 当前边界

- 仍未重写 fetcher。
- 仍未做 retry/fallback。
- 仍未新增数据库。
- 仍未接入新信源。
- official lane 已有 runtime manifest 和 daily full run；非 official lane 的 runtime manifest 覆盖仍有限。
- source runtime health 对非 official lane 的运行覆盖仍有限。
- 价值判断、Evidence Packet、Topic Cluster、内容生成质量链路尚未进入 Phase 1/2。
- 剩余 HIGH 路径主要分布在旧版内容生产脚本和历史素材抓取脚本，Phase 0 收口不继续扩大清理。

## 下一阶段建议

Phase 1：采集稳定性与信息结构化。

优先任务：

- P1-001：Official Lane Runtime Baseline 7-day Observation。
- P1-002：Source Registry Coverage Alignment。
- P1-003：Evidence Packet v1。
- P1-004：Topic Cluster v1。
- P1-005：Value Scoring v1。

## 开发原则

1. 每次只做一个小 checkpoint，避免一次性大改。
2. 每个 checkpoint 必须说明目标、变更文件、验收方式和下一步建议。
3. 每轮开发必须维护本文件和 `docs/DEVELOPMENT_TASKS.md`。
4. 不直接重写现有业务主链路，尤其不要破坏 `同行资本市场内容系统/09_runbooks/scripts/` 下已经能跑的生产脚本。
5. 当前优先级是工程化、可维护性、可迁移性和采集稳定性，而不是马上新增大量信源或文章生成功能。

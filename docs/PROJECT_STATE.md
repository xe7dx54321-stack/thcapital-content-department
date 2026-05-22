# 项目状态记录

## 项目定位

本仓库是同行资本 AI/Agent 领域内容生产 Agent 系统的工程仓库。目标是持续自动化获取 AI 与 Agent 领域的一手高价值信息，完成结构化整理、价值判断、选题筛选、内容生成，并通过头部内容学习和人工反馈形成自我迭代能力。

## 当前阶段

Phase 0：工程化底座与采集稳定性基础设施。

当前主线：先让项目可检查、可审计、可迁移，再建立采集稳定性基础，包括 Source Registry、Source Health、Runtime Health、Runtime Manifest Contract，之后再进入结构化信息层、价值评分和内容生产质量提升。

## 当前最新 checkpoint

P0-008：Runtime Manifest Contract v1。

## 已完成 checkpoint

- P0-001：项目状态与健康检查底座。
- P0-002：路径硬编码审计工具。
- P0-002b：清理 path audit 生成产物入库问题。
- P0-003：路径配置化第一刀。
- P0-003b：修复/确认核心路径配置文件格式与验收链路。
- P0-004：HIGH 风险路径配置化第二刀。
- P0-005：采集稳定性工程第一步 —— Source Registry v1。
- P0-006：Source Health v1。
- P0-007：Source Health Runtime Adapter v1。
- P0-007b：补齐 Source Runtime Health 状态文档。
- P0-008：Runtime Manifest Contract v1。

## 当前能力

### 工程底座

- `make doctor`：项目健康检查。
- `make path-audit`：路径硬编码审计。
- `src/content_system/paths.py`：统一路径配置。
- `env.example` / `config/ENV_EXAMPLE.txt`：本地环境变量示例。

### 采集稳定性基础

- `config/sources.yaml`：Source Registry v1。
- `make sources-validate`：校验 source registry。
- `make source-health`：基于 registry 生成静态 source health/coverage 报告。
- `make source-runtime-health`：基于现有运行产物和 registry 生成 runtime health 对齐报告。
- `make manifest-validate`：校验 runtime manifest contract 示例或指定 manifest。

### Runtime Manifest Contract v1

P0-008 新增 runtime manifest 合约和校验工具，用于后续统一现有抓取脚本的运行结果输出。当前只是定义 contract 和 validator，还没有强制切换现有 fetcher。

核心文件：

- `src/content_system/runtime_manifest.py`
- `scripts/validate_runtime_manifest.py`
- `config/runtime_manifest_example.json`
- `docs/P0_008_RUNTIME_MANIFEST_CONTRACT_REPORT.md`

## 当前边界

仍然不要在 Phase 0 里做以下事情：

- 不重写 `market_topic_capture_round.py` 的抓取主逻辑。
- 不新增数据库。
- 不接入新信源。
- 不做 retry/fallback 调度。
- 不改变现有业务输出格式。
- 不提交 `.env`。
- 不提交 generated logs、source health、source runtime health、path audit 产物。

## 下一步建议

P0-009：Runtime Manifest Writer v1。

目标：为现有活跃抓取脚本提供轻量 manifest writer，让脚本能在不改变业务输出格式的前提下，额外输出符合 P0-008 合约的 runtime manifest JSON。优先处理一个脚本作为样板，不全量切换。

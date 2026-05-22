# 项目状态记录

## 项目定位

本仓库是同行资本内容部门的 AI/Agent 领域内容生产 Agent 系统工程仓库。

系统目标：每天自动化获取 AI 与 Agent 领域一手高价值信息，完成结构化处理、价值判断、选题筛选和内容生产，并通过头部内容学习持续迭代。

## 当前阶段

Phase 0：工程化底座与采集稳定性地基。

最新 checkpoint：**P0-011B Official Lane Health Check Wrapper v1**。

## 已完成 checkpoint

- P0-001：项目状态与健康检查底座。
- P0-002：路径硬编码审计工具。
- P0-002b：清理 path audit 生成产物入库问题。
- P0-003：路径配置化第一刀。
- P0-003b：确认/修复核心路径配置文件格式与验收链路。
- P0-004：HIGH 风险路径配置化第二刀。
- P0-005：采集稳定性工程第一步 —— Source Registry v1。
- P0-006：Source Health v1。
- P0-007：Source Health Runtime Adapter v1。
- P0-007b：补齐 Source Runtime Health 状态文档。
- P0-008：Runtime Manifest Contract v1。
- P0-009：Runtime Manifest Writer v1。
- P0-010：Runtime Manifest Pilot Integration v1。
- P0-010b：忽略 official lane / runtime health 运行产物。
- P0-011A：Source Runtime Health Manifest Reader。
- P0-011B：Official Lane Health Check Wrapper v1。

## 当前能力

- `make doctor`：项目健康检查。
- `make path-audit`：路径硬编码审计。
- `make sources-validate`：Source Registry 校验。
- `make source-health`：静态 source health/coverage 报告。
- `make source-runtime-health`：基于 runtime manifest 与既有运行产物的 runtime source health 报告。
- `make manifest-validate`：Runtime Manifest 合约校验。
- `make manifest-write-from-packets`：从既有 source packets 生成 runtime manifest。
- `make official-lane-with-manifest`：运行官方更新 lane 并额外写出 runtime manifest。
- `make official-lane-health-check`：运行 official lane wrapper、校验 official runtime manifest，并刷新 source runtime health。

## P0-011B 状态

P0-011B 继续采用低风险 wrapper 路线，不直接修改 `market_official_update_lane.py`。

本轮新增 `scripts/run_official_lane_health_check.py`，把以下三步串成一个健康检查入口：

1. 运行 `scripts/run_official_lane_with_manifest.py`。
2. 校验 `latest_official_runtime_manifest.json`。
3. 运行 `scripts/build_source_runtime_health.py`，让 P0-011A 读取 runtime manifest evidence。

## 当前工程原则

- checkpoint 要小，避免一次大规模改造。
- 不提交 generated logs、运行态 JSON、缓存、`.env`。
- 每一步必须维护 `docs/PROJECT_STATE.md` 和 `docs/DEVELOPMENT_TASKS.md`。
- 运行链路改造优先使用 wrapper / adapter / sidecar，稳定后再考虑嵌入主脚本。
- 不重写抓取主链路，不在 Phase 0 引入数据库。

## 下一步建议

P0-012：Official Lane Daily Entry v1。

目标：在确认 wrapper 路线稳定后，将 `official-lane-health-check` 明确为官方更新 lane 的推荐日常入口，并补齐 README/runbook 说明；仍不强行改 official lane 主脚本。

# 项目状态记录

## 项目定位

本仓库是同行资本内容部门的 AI/Agent 领域内容生产 Agent 系统工程仓库。

系统目标：每天自动化获取 AI 与 Agent 领域一手高价值信息，完成结构化处理、价值判断、选题筛选和内容生产，并通过头部内容学习持续迭代。

## 当前阶段

Phase 0：工程化底座与采集稳定性地基。

最新 checkpoint：**P0-014b 补齐 Daily Official Lane Quality Gate 状态文档**。

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
- P0-010b：补齐 official lane / runtime health 生成产物 ignore 规则。
- P0-011A：Source Runtime Health Manifest Reader。
- P0-011B：Official Lane Health Check Wrapper v1。
- P0-012：Official Lane Daily Entry v1。
- P0-013：Daily Source Run Summary v1。
- P0-014：Daily Official Lane Quality Gate v1。
- P0-014b：补齐 Daily Official Lane Quality Gate 状态文档。

## 当前能力

- `make doctor`：项目健康检查。
- `make path-audit`：路径硬编码审计。
- `make sources-validate`：Source Registry 校验。
- `make source-health`：静态 source health/coverage 报告。
- `make source-runtime-health`：基于既有运行产物和 runtime manifest 的 runtime source health 报告。
- `make manifest-validate`：Runtime Manifest 合约校验。
- `make manifest-write-from-packets`：从既有 source packets 生成 runtime manifest。
- `make official-lane-with-manifest`：运行官方更新 lane wrapper 并额外写出 runtime manifest。
- `make official-lane-health-check`：串联 official lane wrapper、runtime manifest validation 和 source runtime health。
- `make official-lane-daily`：官方更新 lane 推荐日常入口。
- `make daily-official-lane`：`official-lane-daily` 的别名。
- `make daily-source-summary`：从 official runtime manifest 和 source runtime health 生成每日运行摘要。
- `make official-lane-quality-gate`：基于每日运行摘要和 official runtime manifest 生成 report-only 质量门。
- `make daily-official-quality-gate`：`official-lane-quality-gate` 的别名。

## P0-014 状态

P0-014 新增 `scripts/check_official_lane_quality_gate.py` 和 `make official-lane-quality-gate` / `make daily-official-quality-gate`。

它基于 `latest_daily_source_run_summary.json` 和 `latest_official_runtime_manifest.json` 生成 report-only 质量门，检查 official lane 是否成功、source_count 和 total_items_found 是否过低、missing_expected 和 error_hint_sources 是否过高。

P0-014 不阻断、不 retry、不改 fetcher、不新增数据库。P0-014b 补齐了 P0-014 漏掉的项目状态文档记录。

## 当前工程原则

- checkpoint 要小，避免一次大规模改造。
- 不提交 generated logs、运行态 JSON、缓存、`.env`。
- 每一步必须维护 `docs/PROJECT_STATE.md` 和 `docs/DEVELOPMENT_TASKS.md`。
- 运行链路改造优先使用 wrapper / adapter / sidecar，稳定后再考虑嵌入主脚本。
- 不重写抓取主链路，不在 Phase 0 引入数据库。
- GitHub raw 单行/多行不再作为主要卡点；优先相信本地 `wc -l`、`py_compile`、`bash -n`、`make` 验证。

## 下一步建议

P0-015：Official Daily Dashboard v1。

目标：把 official lane health check、daily source summary、quality gate 的核心结果合并成一个每天早上可以看的统一 Markdown dashboard，只做展示汇总，不改变抓取链路、不做 retry/fallback。

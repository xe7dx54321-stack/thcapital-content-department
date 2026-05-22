# 开发任务清单

## 当前阶段

Phase 0：工程化底座与采集稳定性地基。

## 已完成

### P0-001：项目状态与健康检查底座

状态：Done。

### P0-002：路径硬编码审计工具

状态：Done。

### P0-002b：清理 path audit 生成产物入库问题

状态：Done。

### P0-003：路径配置化第一刀

状态：Done。

### P0-003b：确认/修复核心路径配置文件格式与验收链路

状态：Done。

### P0-004：HIGH 风险路径配置化第二刀

状态：Done。

### P0-005：采集稳定性工程第一步 —— Source Registry v1

状态：Done。

### P0-006：Source Health v1

状态：Done。

### P0-007：Source Health Runtime Adapter v1

状态：Done。

### P0-007b：补齐 Source Runtime Health 状态文档

状态：Done。

### P0-008：Runtime Manifest Contract v1

状态：Done。

目标：定义 runtime manifest JSON 合约与校验工具。

### P0-009：Runtime Manifest Writer v1

状态：Done。

目标：从既有 source packet 产物生成 runtime manifest，不修改 fetcher。

### P0-010：Runtime Manifest Pilot Integration v1

状态：Done。

目标：用 wrapper 方式运行 `market_official_update_lane.py`，在不修改原抓取脚本、不改变原输出格式的前提下，额外生成 P0-008 runtime manifest。

### P0-010b：补齐 official lane / runtime health 生成产物 ignore 规则

状态：Done。

目标：忽略 official lane raw/source packet/top20/source manifest/runtime manifest 运行产物，避免 generated artifacts 进入 Git。

### P0-011A：Source Runtime Health Manifest Reader

状态：Done。

目标：让 `make source-runtime-health` 优先读取结构化 runtime manifest，保留旧文本扫描作为 fallback。

### P0-011B：Official Lane Health Check Wrapper v1

状态：Done。

目标：新增 `make official-lane-health-check`，串联 official lane wrapper、runtime manifest validation 和 source runtime health refresh。

### P0-012：Official Lane Daily Entry v1

状态：Done。

目标：将 `make official-lane-health-check` 明确为官方更新 lane 推荐日常入口，并新增 `make official-lane-daily` / `make daily-official-lane`。

### P0-013：Daily Source Run Summary v1

状态：Done。

目标：

- 基于 official runtime manifest 和 source runtime health 生成每日运行摘要。
- 摘要包含运行状态、source_count、total_items_found、missing_expected、error hints 和关键产物路径。
- 输出小型 JSON/Markdown 报告。
- 不发布内容，不做 retry/fallback，不新增数据库。

验收：

- `python3 -m py_compile scripts/build_daily_source_run_summary.py` 通过。
- `make official-lane-daily` 可运行。
- `make source-runtime-health` 可运行。
- `make daily-source-summary` 可运行。
- daily source run summary generated artifacts 不进入 Git。

## 下一步

### P0-014：Daily Official Lane Quality Gate v1

状态：Planned。

目标：

- 基于 daily source run summary 增加轻量质量门槛。
- 检查 official lane 是否 SUCCESS。
- 检查 source_count、total_items_found、missing_expected、error hints 是否异常。
- 输出 quality gate JSON/Markdown。
- 只报告，不阻断、不 retry、不新增数据库。

验收建议：

- `make official-lane-daily` 跑完后可以运行 quality gate。
- quality gate 能读取 latest daily source run summary。
- generated artifacts 继续被 `.gitignore` 覆盖。

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

目标：

- 用 wrapper 方式运行 `market_official_update_lane.py`。
- 在不修改原抓取脚本、不改变原输出格式的前提下，额外生成 P0-008 runtime manifest。
- 复用 P0-009 的 runtime manifest 思路，但本轮绑定官方更新 lane 做真实 pilot。

验收：

- `python3 -m py_compile src/content_system/runtime_manifest_official_lane.py` 通过。
- `python3 -m py_compile scripts/run_official_lane_with_manifest.py` 通过。
- `make official-lane-with-manifest` 可运行。
- `make manifest-validate` 仍通过。
- `make source-runtime-health` 仍通过。
- generated runtime manifest 不进入 Git。

### P0-010b：忽略 official lane / runtime health 运行产物

状态：Done。

目标：

- 补齐 `.gitignore`，避免 official lane raw/source packets/top20/source manifest/runtime manifest/source runtime health 产物进入 Git。

### P0-011A：Source Runtime Health Manifest Reader

状态：Done。

目标：

- 让 `make source-runtime-health` 优先读取 P0-008 runtime manifest。
- 保留 legacy text scan 作为旧产物 fallback。
- 不修改 official lane 主脚本。
- 不做 retry/fallback。
- 不新增数据库。

验收：

- `python3 -m py_compile src/content_system/source_runtime_health.py` 通过。
- `make source-runtime-health` 可运行。
- 如果存在 `latest_official_runtime_manifest.json`，报告中的 `manifest_count` 大于 0。
- Evidence 中可出现 `runtime_manifest` 类型。
- generated reports 不进入 Git。

### P0-011B：Official Lane Health Check Wrapper v1

状态：Done。

目标：

- 继续采用 wrapper 路线，不直接修改 `market_official_update_lane.py`。
- 新增 `make official-lane-health-check`。
- 串联 official lane wrapper、runtime manifest validation 和 source runtime health refresh。
- 不改变 official lane 原输出格式。
- 不做 retry/fallback。
- 不新增数据库。

验收：

- `python3 -m py_compile scripts/run_official_lane_health_check.py` 通过。
- `make official-lane-health-check` 可运行。
- official runtime manifest 可通过 P0-008 校验。
- source runtime health 可读取 official runtime manifest evidence。
- generated reports 不进入 Git。

## 下一步

### P0-012：Official Lane Daily Entry v1

状态：Planned。

目标：

- 将 `make official-lane-health-check` 明确为官方更新 lane 推荐日常入口。
- 补齐 README/runbook 说明，降低日常运行门槛。
- 保留原 `make official-lane-with-manifest` 作为底层命令。
- 不直接修改 official lane 主脚本。
- 不做 retry/fallback。
- 不新增数据库。

验收建议：

- README 或 runbook 中有明确日常运行命令。
- `make official-lane-health-check` 是推荐入口。
- 运行后 manifest validation 和 source runtime health 都能衔接。
- generated artifacts 不进入 Git。

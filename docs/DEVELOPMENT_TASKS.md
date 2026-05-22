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

## 下一步

### P0-011B：Official Lane Runtime Manifest Direct Writer v1 / Wrapper 观察增强

状态：Planned。

目标：

- 基于 P0-010/P0-011A 的运行效果，决定是否继续采用 wrapper 作为正式入口，还是最小侵入地嵌入 `market_official_update_lane.py`。
- 如果嵌入主脚本，必须不改变原输出格式。
- 不改其他抓取脚本。
- 不做 retry/fallback。
- 不新增数据库。

验收建议：

- official lane 仍能输出原有 source packet、official top20 和 source manifest。
- runtime manifest 可被 P0-008 校验工具读取。
- runtime manifest 可被 P0-011A source runtime health 结构化识别。
- 运行产物不进入 Git。

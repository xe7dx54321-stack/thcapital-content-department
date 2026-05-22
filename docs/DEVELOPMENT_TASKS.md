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

## 下一步

### P0-011：Runtime Manifest Official Lane Direct Writer v1

状态：Planned。

目标：

- 基于 P0-010 wrapper 的运行效果，决定是否把 runtime manifest 写入能力以最小改动方式嵌入 `market_official_update_lane.py`。
- 如果 wrapper 足够稳定，可以把 P0-010 wrapper 作为正式入口，不强行改 fetcher。
- 不改其他抓取脚本。
- 不做 retry/fallback。
- 不新增数据库。

验收建议：

- 至少能对官方 lane 输出一份 runtime manifest。
- 该 manifest 可被 P0-008 校验工具读取。
- 该 manifest 可被 P0-007 source runtime health 识别。

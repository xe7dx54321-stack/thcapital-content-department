# P0-010 Runtime Manifest Pilot Integration v1 报告

## 本轮目标

P0-010 的目标是选择一个低风险运行链路做 runtime manifest pilot integration。

本轮选择官方更新 lane：`market_official_update_lane.py`。

## 实现策略

本轮没有直接修改官方更新 lane 的抓取逻辑，而是新增 wrapper：

- `scripts/run_official_lane_with_manifest.py`
- `src/content_system/runtime_manifest_official_lane.py`

wrapper 会执行现有官方更新 lane，然后读取它已有的 official source packet JSON，并生成符合 P0-008 合约的 runtime manifest。

## 新增命令

```bash
make official-lane-with-manifest
```

也可以直接运行：

```bash
python3 scripts/run_official_lane_with_manifest.py
python3 scripts/run_official_lane_with_manifest.py --skip-run
python3 scripts/run_official_lane_with_manifest.py --json
```

## 输出产物

运行后生成：

```text
同行资本市场内容系统/10_logs/YYYYMMDD__official-runtime-manifest.json
同行资本市场内容系统/10_logs/latest_official_runtime_manifest.json
```

这些产物匹配 P0-009 已加入的 runtime manifest ignore 规则，不应进入 Git。

## 修改文件

- `Makefile`
- `scripts/run_official_lane_with_manifest.py`
- `src/content_system/runtime_manifest_official_lane.py`
- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`
- `docs/P0_010_RUNTIME_MANIFEST_PILOT_REPORT.md`

## 未做事项

- 未修改 `market_official_update_lane.py`。
- 未修改其他抓取脚本。
- 未新增 retry/fallback。
- 未新增数据库。
- 未改变现有 source packet / top20 / manifest markdown 输出格式。

## 验收命令

```bash
python3 -m py_compile src/content_system/runtime_manifest_official_lane.py
python3 -m py_compile scripts/run_official_lane_with_manifest.py
make official-lane-with-manifest
make manifest-validate
make source-runtime-health
make doctor
make path-audit
git status --short --branch
```

## 下一步建议

P0-011：Runtime Manifest Official Lane Direct Writer v1。

如果 P0-010 wrapper 在真实运行中稳定，可以继续保留 wrapper 作为正式入口；如果需要让官方 lane 自身直接输出 runtime manifest，再做最小侵入式改造。

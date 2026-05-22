# P0-011A Source Runtime Health Manifest Reader 报告

## 本轮目标

P0-010 已经验证 official lane wrapper 可以生成 P0-008 runtime manifest。本轮目标是让 `make source-runtime-health` 优先读取结构化 runtime manifest，而不是主要依赖旧的文本/文件扫描。

## 修改文件

- `src/content_system/source_runtime_health.py`
- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`
- `docs/P0_011A_SOURCE_RUNTIME_HEALTH_MANIFEST_READER_REPORT.md`

## 核心改动

1. 新增 runtime manifest 发现逻辑，扫描：
   - `同行资本市场内容系统/10_logs/*runtime-manifest*.json`
   - `同行资本市场内容系统/10_logs/*runtime_manifest*.json`
   - `同行资本市场内容系统/10_logs/latest_*runtime_manifest*.json`
2. 新增 `collect_manifest_evidence()`，优先读取 P0-008 合约中的 `sources[]`。
3. 保留 legacy text scan 作为 fallback，兼容旧 manifest、source packet 和日志产物。
4. 避免把 runtime manifest JSON 再当作普通文本 manifest 扫描，减少错误 hint 污染。
5. 报告新增：
   - `manifest_count`
   - `unmatched_manifest_sources`
   - runtime manifest evidence 示例

## 未做事项

- 不修改 `market_official_update_lane.py`。
- 不改变 P0-010 wrapper 行为。
- 不做 retry/fallback。
- 不新增数据库。
- 不改变 source registry schema。

## 验收命令

```bash
python3 -m py_compile src/content_system/source_runtime_health.py
python3 -m py_compile scripts/build_source_runtime_health.py
make official-lane-with-manifest
make source-runtime-health
make manifest-validate
make doctor
make path-audit
git status --short --branch
```

## 预期结果

- `make source-runtime-health` 可运行。
- 如果存在 `latest_official_runtime_manifest.json`，报告中的 `manifest_count` 应大于 0。
- source runtime health 的 evidence 中应出现 `runtime_manifest` 类型。
- generated reports 不进入 Git。

## 下一步建议

P0-011B 可继续观察 wrapper 路线，或再评估是否将 runtime manifest writer 最小侵入地嵌入 official lane 主脚本。

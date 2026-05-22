# P0-007 Source Health Runtime Adapter v1 开发报告

## 本轮目标

P0-007 的目标是把 P0-005 的 Source Registry 和 P0-006 的静态 Source Health 继续向运行态推进：读取现有运行产物、manifest、source packets 和 logs，生成 registry-aligned 的运行态 source health 报告。

本轮不重写 fetcher、不做 retry/fallback、不新增数据库、不改变现有抓取输出格式。

## 新增文件

```text
src/content_system/source_runtime_health.py
scripts/build_source_runtime_health.py
docs/P0_007_SOURCE_RUNTIME_HEALTH_REPORT.md
```

## 修改文件

```text
.gitignore
Makefile
src/content_system/__init__.py
docs/PROJECT_STATE.md
docs/DEVELOPMENT_TASKS.md
```

## 新增命令

```bash
make source-runtime-health
```

等价于：

```bash
python3 scripts/build_source_runtime_health.py
```

## 输出产物

```text
同行资本市场内容系统/10_logs/YYYYMMDD__source-runtime-health.json
同行资本市场内容系统/10_logs/YYYYMMDD__source-runtime-health.md
同行资本市场内容系统/10_logs/latest_source_runtime_health.json
同行资本市场内容系统/10_logs/latest_source_runtime_health.md
同行资本市场内容系统/11_frontstage/YYYYMMDD__source-runtime-health-board.md
同行资本市场内容系统/11_frontstage/latest_source_runtime_health_board.md
```

这些是运行生成产物，默认由 `.gitignore` 忽略，不进入 Git。

## Runtime Status

P0-007 使用以下运行态状态：

```text
OBSERVED
OBSERVED_WITH_ERROR_HINTS
MISSING_EXPECTED
NOT_OBSERVED
DISABLED
```

## 适配策略

本轮采取 best-effort 适配：

1. 扫描 `10_logs` 下 manifest/source 相关产物。
2. 扫描 `02_topic_radar/source_packets` 下 source packet 产物。
3. 根据 registry source_id 和 label 在 artifacts 中匹配 evidence。
4. 根据 source 的 `expected_frequency` 判断 daily/hourly source 是否缺少运行证据。
5. 记录 error/failure/timeout 等文本提示，但不做 retry。

## 未做事项

- 未重写任何 fetcher。
- 未改变现有抓取输出格式。
- 未新增数据库。
- 未做 retry queue。
- 未做 fallback 执行。
- 未新增外部依赖。

## 验收命令

```bash
python3 -m py_compile src/content_system/source_runtime_health.py
python3 -m py_compile scripts/build_source_runtime_health.py
make sources-validate
make source-health
make source-runtime-health
make doctor
make path-audit
git status --short --branch
```

## 下一步建议

下一步进入 P0-008：Runtime Manifest Contract v1。

P0-008 应为现有抓取脚本输出稳定的结构化 manifest，让 P0-007 不再依赖 best-effort 文本匹配，而是优先读取标准 runtime manifest。

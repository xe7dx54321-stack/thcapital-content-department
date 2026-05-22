# P1-002 Source Registry Coverage Alignment v1 报告

## 本轮目标

- 对齐 `config/sources.yaml` 与 latest official runtime manifest / source runtime health。
- 显式标记 `COVERED_BY_RUNTIME_MANIFEST`、`OBSERVED_BY_HEALTH_SCAN`、`REGISTRY_ONLY`、`RUNTIME_ONLY` 和 `DISABLED`。
- 记录 official lane runtime source_id 与 registry source_id 的 alias 关系。

## 新增文件

- `src/content_system/source_coverage.py`
- `scripts/build_source_coverage_alignment.py`

## 新增命令

```bash
make source-coverage
```

## 输出产物

- `同行资本市场内容系统/10_logs/YYYYMMDD__source-coverage-alignment.json`
- `同行资本市场内容系统/10_logs/YYYYMMDD__source-coverage-alignment.md`
- `同行资本市场内容系统/10_logs/latest_source_coverage_alignment.json`
- `同行资本市场内容系统/10_logs/latest_source_coverage_alignment.md`
- `同行资本市场内容系统/11_frontstage/latest_source_coverage_alignment_board.md`

## 注意事项

- 本轮不重命名 fetcher 的 runtime source_id。
- registry-only source 在 v1 中是正常状态，代表尚未被 official lane 覆盖。
- runtime-only source 代表现有运行产物中出现，但尚未纳入 registry 的 source。

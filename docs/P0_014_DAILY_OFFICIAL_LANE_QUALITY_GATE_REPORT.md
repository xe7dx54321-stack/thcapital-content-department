# P0-014 Daily Official Lane Quality Gate v1 开发报告

## 本轮目标

P0-014 在 P0-013 的 daily source run summary 基础上新增一个轻量质量门。

它用于回答：

- 今日 official lane 是否 SUCCESS。
- source_count 是否异常偏低。
- total_items_found 是否异常偏低。
- missing_expected 是否过高。
- error_hint_sources 是否过高。

本轮只报告，不默认阻断，不 retry，不修改 fetcher，不新增数据库。

## 新增文件

- `scripts/check_official_lane_quality_gate.py`
- `docs/P0_014_DAILY_OFFICIAL_LANE_QUALITY_GATE_REPORT.md`

## 修改文件

- `.gitignore`
- `Makefile`
- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`

## 新增命令

```bash
make official-lane-quality-gate
make daily-official-quality-gate
```

## 默认输入

- `同行资本市场内容系统/10_logs/latest_daily_source_run_summary.json`
- `同行资本市场内容系统/10_logs/latest_official_runtime_manifest.json`

## 默认输出

- `同行资本市场内容系统/10_logs/YYYYMMDD__official-lane-quality-gate.json`
- `同行资本市场内容系统/10_logs/YYYYMMDD__official-lane-quality-gate.md`
- `同行资本市场内容系统/10_logs/latest_official_lane_quality_gate.json`
- `同行资本市场内容系统/10_logs/latest_official_lane_quality_gate.md`
- `同行资本市场内容系统/11_frontstage/YYYYMMDD__official-lane-quality-gate-board.md`
- `同行资本市场内容系统/11_frontstage/latest_official_lane_quality_gate_board.md`

## 默认规则

- `official_manifest_success`：official runtime manifest status 应为 `SUCCESS`。
- `minimum_source_count`：source_count 默认应大于等于 5。
- `minimum_items_found`：total_items_found 默认应大于等于 10。
- `missing_expected_limit`：missing_expected 默认不超过 12。
- `error_hint_limit`：error_hint_sources 默认不超过 2。

默认只输出报告。只有传入 `--fail-on-red` 时，RED 才返回非 0 exit code。

## 验收命令

```bash
python3 -m py_compile scripts/check_official_lane_quality_gate.py
make official-lane-daily
make source-runtime-health
make daily-source-summary
make official-lane-quality-gate
make manifest-validate
make doctor
make path-audit
git status --short --branch
```

## 未做事项

- 未新增 retry。
- 未新增 fallback。
- 未修改 `market_official_update_lane.py`。
- 未新增数据库。
- 未接入新的外部信源。
- 未把 quality gate 作为 hard blocker。

## 下一步建议

P0-015：Official Daily Dashboard v1。

把 official lane health check、daily source summary、quality gate 的核心结果合并成一个人工友好的每日 dashboard。

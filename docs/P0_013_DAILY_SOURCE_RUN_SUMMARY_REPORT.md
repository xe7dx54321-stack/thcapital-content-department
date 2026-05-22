# P0-013 Daily Source Run Summary v1 开发报告

## 本轮目标

P0-013 基于 P0-010/P0-011/P0-012 已跑通的 official lane runtime manifest 和 source runtime health，生成一份更适合每日查看的简洁运行摘要。

本轮不抓取新数据、不改 fetcher、不做 retry/fallback、不新增数据库。

## 新增文件

- `scripts/build_daily_source_run_summary.py`
- `docs/P0_013_DAILY_SOURCE_RUN_SUMMARY_REPORT.md`

## 修改文件

- `.gitignore`
- `Makefile`
- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`

## 新增命令

```bash
make daily-source-summary
```

## 输入

默认读取：

- `同行资本市场内容系统/10_logs/latest_official_runtime_manifest.json`
- `同行资本市场内容系统/10_logs/latest_source_runtime_health.json`

## 输出

默认生成：

- `同行资本市场内容系统/10_logs/YYYYMMDD__daily-source-run-summary.json`
- `同行资本市场内容系统/10_logs/YYYYMMDD__daily-source-run-summary.md`
- `同行资本市场内容系统/10_logs/latest_daily_source_run_summary.json`
- `同行资本市场内容系统/10_logs/latest_daily_source_run_summary.md`
- `同行资本市场内容系统/11_frontstage/YYYYMMDD__daily-source-run-summary-board.md`
- `同行资本市场内容系统/11_frontstage/latest_daily_source_run_summary_board.md`

这些产物已加入 `.gitignore`，不应进入 Git。

## 摘要字段

- `status`
- `run_date`
- `source_count`
- `total_items_found`
- `total_items_written`
- `enabled_sources`
- `observed_sources`
- `missing_expected`
- `error_hint_sources`
- `status_distribution`
- `key_outputs`
- `warnings`

## 验收命令

```bash
python3 -m py_compile scripts/build_daily_source_run_summary.py
make official-lane-daily
make source-runtime-health
make daily-source-summary
make manifest-validate
make doctor
make path-audit
git status --short --branch
```

## 未做事项

- 不做 quality gate。
- 不阻断 official lane。
- 不新增 retry/fallback。
- 不新增数据库。
- 不生成内容选题或文章。

## 下一步建议

P0-014：Daily Official Lane Quality Gate v1。

基于 daily source run summary 增加轻量质量门槛，只报告 official lane 是否异常，不阻断、不 retry。

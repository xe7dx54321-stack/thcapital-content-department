# P0-016 Official Daily Full Run v1 Report

## 本轮目标

- 新增 official lane 每日全流程入口。
- 串联现有 official lane health check、source runtime health、daily summary、quality gate 和 official daily dashboard。
- 输出 full run JSON/Markdown summary 和 frontstage board。
- 不重写 official lane 主脚本，不新增 retry/fallback，不改变 fetcher 输出格式。

## 新增命令

```bash
make official-daily-full-run
make daily-official-full-run
```

## 执行链路

`scripts/run_official_daily_full_run.py` 顺序执行：

1. `scripts/run_official_lane_health_check.py`
2. `scripts/build_source_runtime_health.py`
3. `scripts/build_daily_source_run_summary.py`
4. `scripts/check_official_lane_quality_gate.py`
5. `scripts/build_official_daily_dashboard.py`

如果 official lane health check、source runtime health 或 daily source summary 失败，默认停止；`--continue-on-error` 可继续尝试后续报告。quality gate 失败会继续 dashboard，并在 full run summary 中记录 warning。

## 输出产物

```text
同行资本市场内容系统/10_logs/YYYYMMDD__official-daily-full-run.json
同行资本市场内容系统/10_logs/YYYYMMDD__official-daily-full-run.md
同行资本市场内容系统/10_logs/latest_official_daily_full_run.json
同行资本市场内容系统/10_logs/latest_official_daily_full_run.md
同行资本市场内容系统/11_frontstage/YYYYMMDD__official-daily-full-run-board.md
同行资本市场内容系统/11_frontstage/latest_official_daily_full_run_board.md
```

以上均为 generated artifacts，已由 `.gitignore` 忽略。

## 验收命令

```bash
python3 -m py_compile scripts/run_official_daily_full_run.py
make official-daily-full-run
make daily-official-full-run
git ls-files | grep -E 'official-daily-full-run|daily-source-run-summary|official-lane-quality-gate|official-daily-dashboard|source-runtime-health|runtime-manifest|path-hardcode-audit' || true
git status --short --branch
```

## 未做事项

- 未重写 official lane 主脚本。
- 未重写 `market_topic_capture_round.py`。
- 未做 retry/fallback。
- 未新增数据库。
- 未接入新信源。
- 未引入 LLM。

## 下一步

进入 P1-001：Official Lane Runtime Baseline 7-day Observation。连续观察 official daily full run 的 source_count、total_items_found、quality gate status、missing_expected 和 error_hint_sources。

# P0-015 Official Daily Dashboard v1 开发报告

## 本轮目标

将 official lane health check、daily source summary 和 official lane quality gate 的核心结果汇总为一个每日可读 dashboard，方便人工快速判断官方 lane 当天运行质量。

## 新增文件

- `scripts/build_official_daily_dashboard.py`
- `docs/P0_015_OFFICIAL_DAILY_DASHBOARD_REPORT.md`

## 修改文件

- `.gitignore`
- `Makefile`
- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`

## 新增命令

```bash
make official-daily-dashboard
make daily-official-dashboard
```

## 输入

默认读取：

- `同行资本市场内容系统/10_logs/latest_official_runtime_manifest.json`
- `同行资本市场内容系统/10_logs/latest_source_runtime_health.json`
- `同行资本市场内容系统/10_logs/latest_daily_source_run_summary.json`
- `同行资本市场内容系统/10_logs/latest_official_lane_quality_gate.json`

## 输出

- `同行资本市场内容系统/10_logs/YYYYMMDD__official-daily-dashboard.json`
- `同行资本市场内容系统/10_logs/YYYYMMDD__official-daily-dashboard.md`
- `同行资本市场内容系统/10_logs/latest_official_daily_dashboard.json`
- `同行资本市场内容系统/10_logs/latest_official_daily_dashboard.md`
- `同行资本市场内容系统/11_frontstage/YYYYMMDD__official-daily-dashboard.md`
- `同行资本市场内容系统/11_frontstage/latest_official_daily_dashboard.md`

上述产物已加入 `.gitignore`，默认不进入 Git。

## 验收命令

```bash
python3 -m py_compile scripts/build_official_daily_dashboard.py
make official-lane-daily
make source-runtime-health
make daily-source-summary
make official-lane-quality-gate
make official-daily-dashboard
make doctor
make path-audit
git status --short --branch
```

## 未做事项

- 不修改 official lane 主脚本。
- 不做 retry/fallback。
- 不新增数据库。
- 不改变现有抓取输出格式。

## 下一步建议

P0-016：Official Daily Full Run v1。

将官方 lane 每日链路串成一个全流程入口，进一步降低每日运行操作成本。

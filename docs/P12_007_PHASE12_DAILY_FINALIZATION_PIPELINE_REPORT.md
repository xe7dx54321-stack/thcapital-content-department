# P12-007 Phase 12 Daily Finalization Pipeline Report

## 本轮目标

新增 Phase 12 日常总入口，串联质量闭环、accepted version promotion、final candidate、checklist、memory、analytics 和工作台刷新。

## 新增命令

```bash
make phase12-daily
```

## Pipeline 顺序

1. `run_phase11_daily_quality_loop_pipeline.py`
2. `promote_accepted_versions.py`
3. `build_final_article_candidates.py`
4. `build_final_publish_checklist.py`
5. `update_final_candidate_memory.py`
6. `build_multiday_version_analytics.py`
7. `build_wechat_workbench_data.py`
8. `build_wechat_workbench_frontend.py`

## 安全策略

- 不自动 accept version。
- 不自动 publish。
- 不调用公众号 API。
- 没有 ACCEPT version 时输出空结果，不崩溃。

## 输出

- `同行资本市场内容系统/10_logs/latest_phase12_daily_finalization_pipeline.json`
- `同行资本市场内容系统/11_frontstage/latest_phase12_daily_finalization_pipeline_board.md`

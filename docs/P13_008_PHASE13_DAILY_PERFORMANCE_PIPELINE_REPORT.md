# P13-008 Phase 13 Daily Performance Pipeline Report

## 本轮目标

新增 Phase 13 日常总入口，把 Phase 12 finalization、publish session board、metrics board、performance memory、learning feedback 和工作台刷新串起来。

## 修改文件

- `scripts/run_phase13_daily_performance_pipeline.py`
- `Makefile`

## Pipeline 顺序

1. `run_phase12_daily_finalization_pipeline.py`
2. `build_publish_session_board.py`
3. `build_post_publish_metrics_board.py`
4. `update_content_performance_memory.py`
5. `build_performance_learning_feedback.py`
6. `build_wechat_workbench_data.py`
7. `build_wechat_workbench_frontend.py`

## 新增命令

```bash
make phase13-daily
```

## 安全边界

- 不自动创建 publish session。
- 不自动标记 published。
- 不自动录入 metrics。
- 不自动发布。

# P9-008 Phase 9 Daily Workbench Pipeline v1 Report

## 本轮目标

新增 Phase 9 日常工作台入口，串联 Phase 8、工作台数据、文章预览、上下文、前台 HTML 和反馈记忆。

## 新增文件

- `scripts/run_phase9_daily_workbench_pipeline.py`

## 新增命令

```bash
make phase9-daily
```

## 执行链路

1. `run_phase8_daily_production_pipeline.py`
2. `build_wechat_workbench_data.py`
3. `render_wechat_article_preview.py`
4. `build_workbench_context.py`
5. `build_wechat_workbench_frontend.py`
6. `update_workbench_feedback_memory.py`

## 边界

`phase9-daily` 不默认运行 Chief Editor Agent，因为它需要用户 message。

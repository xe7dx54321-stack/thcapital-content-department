# P11-007 Phase 11 Daily Quality Loop Pipeline Report

## 本轮目标

新增 Phase 11 日常质量闭环入口。

## 运行链路

1. `run_phase10_daily_action_pipeline.py`
2. `score_article_versions.py`
3. `build_version_review_board.py`
4. `update_article_version_memory.py`
5. `build_action_effectiveness_analytics.py`
6. `build_prompt_rule_regression_dashboard.py`
7. `build_wechat_workbench_data.py`
8. `build_wechat_workbench_frontend.py`

## 新增命令

```bash
make phase11-daily
```

## 边界

- 不自动 accept/reject。
- 不自动改 prompt/rules。
- 不覆盖原稿。

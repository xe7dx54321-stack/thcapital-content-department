# P15-011 Phase 15 Daily Generation Pipeline Report

## 本轮目标

新增 Phase 15 总入口，串联方法论生成、视觉策略、图片需求、回归测试、校准看板和工作台刷新。

## 新增命令

```bash
make phase15-daily
```

## Pipeline

1. run_phase14_daily_methodology_pipeline.py
2. build_methodology_briefs.py
3. build_methodology_outlines.py
4. build_methodology_drafts.py
5. execute_methodology_rewrite_actions.py
6. validate_article_visual_methodology.py
7. build_visual_plans.py
8. build_image_asset_requests.py
9. run_methodology_regression_tests.py
10. build_human_methodology_calibration_board.py
11. build_wechat_workbench_data.py
12. build_wechat_workbench_frontend.py

## 边界

不自动生成图片、不调用 gpt-image-2、不自动发布、不自动改 prompt/rules/config。

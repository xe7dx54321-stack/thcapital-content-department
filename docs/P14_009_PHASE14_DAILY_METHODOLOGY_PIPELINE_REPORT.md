# P14-009 Phase 14 Daily Methodology Pipeline Report

## 本轮目标

新增 Phase 14 总入口，把方法论验证、选题评分、文章评审、Chief Editor 方法论上下文、表现对齐和工作台展示串起来。

## 新增命令

```bash
make phase14-daily
```

## Pipeline

1. run_phase13_daily_performance_pipeline.py
2. validate_topic_selection_methodology.py
3. validate_article_quality_methodology.py
4. validate_content_strategy_recipes.py
5. score_topics_with_methodology.py
6. review_articles_with_methodology.py
7. build_chief_editor_methodology_context.py
8. build_methodology_performance_alignment.py
9. build_wechat_workbench_data.py
10. build_wechat_workbench_frontend.py

## 边界

不自动改 config/prompt/rules，不自动发布，只生成评估、建议、上下文和工作台展示。

# P32-011 Runtime Topic-to-Article Integration Report

## 目标

把 Phase32 topic-to-article pipeline 接入 Runtime job registry、daily schedule 和 DAG。

## 新增 Runtime Job

`autonomous_topic_to_article` 执行 `scripts/run_autonomous_topic_to_article_pipeline.py`。

## 边界

没有合格主选题时输出 `SUCCESS_EMPTY` 或 `ACTIONABLE_EMPTY`，不强行写稿；LLM live 不可用时 dry-run；不绕过 cost guard。

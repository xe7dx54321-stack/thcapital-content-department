# P12-002 Final Article Candidate Builder Report

## 本轮目标

把 promoted version 生成 final article candidate，用于最终人工发布前检查。

## 修改文件

- `src/content_system/final_article_candidate.py`
- `scripts/build_final_article_candidates.py`
- `Makefile`

## 安全规则

- final candidate 必须来自 promoted version。
- `would_publish` 永远为 `false`。
- `final_review_required=true`。
- `do_not_publish=true`。
- 不调用公众号 API，不进入草稿箱，不覆盖历史版本。

## 输出

- `同行资本市场内容系统/07_publishing/YYYYMMDD__final-article-candidates.json`
- `同行资本市场内容系统/07_publishing/latest_final_article_candidates.json`
- 对应 Markdown 报告。

## 当前限制

candidate 是最终人工检查候选稿，不是已发布稿。

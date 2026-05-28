# P14-005 Methodology-based Article Review Report

## 本轮目标

用文章方法论重新评审当前稿件、final candidate 和 rewrite version。

## 修改文件

- `src/content_system/methodology_article_review.py`
- `scripts/review_articles_with_methodology.py`

## 输出

- `同行资本市场内容系统/05_draft_packs/latest_methodology_article_review.json`
- `同行资本市场内容系统/05_draft_packs/latest_methodology_article_review.md`

## 核心能力

- 评分 clear_question、core_judgment、logic_progression、evidence_fit 等 10 个标准。
- 输出 strengths、weaknesses、generic_language_flags、missing_sections、rewrite_priorities。
- 标记 READY / REVISE / HOLD。

## 边界

不覆盖稿件，不替代 human review，只作为改稿优先级输入。

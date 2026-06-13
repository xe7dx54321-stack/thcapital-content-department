# P32-008 Multi-Agent Review / Judge / Rewrite Activation Report

## 目标

将 proponent / critic / judge / rewrite 流程接入 autonomous drafts，生成审稿结论和 rewrite 版本。

## 输出

- `同行资本市场内容系统/07_drafts/latest_autonomous_article_reviews.json`
- `同行资本市场内容系统/07_drafts/latest_autonomous_article_rewrite_versions.json`
- `同行资本市场内容系统/07_drafts/latest_autonomous_article_review_summary.md`

## 边界

rewrite 生成新版本，不覆盖原稿；live LLM 不可用时 dry-run，不绕过 cost guard 或 safety gate。

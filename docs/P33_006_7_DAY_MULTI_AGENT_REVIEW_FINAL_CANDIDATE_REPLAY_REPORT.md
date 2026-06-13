# P33-006 7-day Multi-Agent Review / Final Candidate Replay Report

## 目标

对 replay drafts 运行 dry-run-safe review / judge / rewrite / final candidate。

## 输出

- `同行资本市场内容系统/13_replay/replay_YYYYMMDD/article_reviews.json`
- `同行资本市场内容系统/13_replay/replay_YYYYMMDD/final_candidates.json`
- `同行资本市场内容系统/10_logs/latest_7day_article_review_replay.json`

## 边界

Review 不覆盖 draft；final candidate 必须 `manual_review_required=true`。

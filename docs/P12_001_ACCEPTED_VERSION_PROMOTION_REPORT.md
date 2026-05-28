# P12-001 Accepted Version Promotion Report

## 本轮目标

将 Phase 11 中由人工明确 `ACCEPT` 的文章版本提升为 selected / promoted version，作为 final article candidate 的唯一上游。

## 修改文件

- `src/content_system/accepted_version_promotion.py`
- `scripts/promote_accepted_versions.py`
- `Makefile`

## Promotion Policy

- 只处理 `human_decision=ACCEPT` 的版本。
- `REJECT`、`REVISE_MORE`、`DEFER`、`UNREVIEWED` 不会被提升。
- 同一原文章如有多个 accepted version，按 `human_score`、`score_delta`、`decided_at` 选择。
- promotion 不等于发布，不覆盖原稿。

## 输出

- `同行资本市场内容系统/09_workbench_actions/versions/YYYYMMDD__promoted-versions.json`
- `同行资本市场内容系统/09_workbench_actions/versions/latest_promoted_versions.json`
- 对应 Markdown 报告。

## 当前限制

promotion 只是候选最终稿构建的输入，后续仍需要 final checklist 和人工最终确认。

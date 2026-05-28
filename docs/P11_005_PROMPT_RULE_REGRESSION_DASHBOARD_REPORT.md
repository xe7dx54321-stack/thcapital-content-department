# P11-005 Prompt / Rule Regression Dashboard Report

## 本轮目标

生成 prompt / rule 回归看板，避免系统越改越差。

## 已完成能力

- 汇总 action effectiveness、version memory、rule suggestions、content recipes 和 pattern adapters。
- 生成 prompt/rule 调整建议。
- 所有建议均 `auto_apply=false`。

## 边界

- 不自动改 prompt。
- 不自动改 scoring rule。
- 不自动改 content recipe。

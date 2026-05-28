# P11-001 Version Comparison Scoring Report

## 本轮目标

对 Phase 10 生成的新版本与原稿进行规则型质量对比，回答“这次改稿有没有变好”。

## 已完成能力

- 读取 `latest_rewrite_versions.json` 与 `latest_wechat_workbench_data.json`。
- 计算标题、开头、逻辑、证据、公众号可读性、投资人视角、风险控制等维度的 delta。
- 生成 `ACCEPT / REJECT / REVISE_MORE / HUMAN_REVIEW` 辅助建议。

## 输出

- `latest_version_comparison_scores.json`
- `latest_version_comparison_scores.md`

## 边界

- 评分只作为辅助判断。
- 不自动接受新版本。
- 不覆盖原稿。

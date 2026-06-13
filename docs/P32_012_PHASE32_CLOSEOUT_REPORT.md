# Phase 32 Closeout

## 目标

迁移旧系统内容生产 know-how，并让 Autonomous Runtime 从确认选题推进到 brief、outline、draft、multi-agent review、rewrite 和 final candidate。

## Legacy Asset Audit

新增 legacy asset audit，只读扫描旧 know-how 资产。

## Know-how Mapping

新增 legacy know-how methodology mapping sidecar，所有建议 `auto_apply=false`。

## Content Production Playbooks

新增内容生产 playbook registry，覆盖选题评分、brief、大纲、初稿、审稿、重写和最终候选稿。

## Topic Scoring

新增 autonomous topic scoring 和 daily main topic selection。

## Brief Generation

新增 autonomous brief builder，证据不足不得进入 outline。

## Outline Generation

新增 autonomous outline builder，每个 section 保留 purpose 和 reader question。

## Draft Generation

新增 autonomous draft writer，所有 draft `do_not_publish=true`。

## Multi-Agent Review and Rewrite

新增 autonomous article review pipeline，rewrite 生成新版本，不覆盖原稿。

## Final Candidate Delivery

新增 final candidate assembly，并接入 Workbench 自动内容生产面板。

## Quality Regression

新增 legacy-vs-new quality regression，检查 why now、证据链、故事线、AI 味、target price 和伪造引用风险。

## Runtime Integration

新增 `autonomous_topic_to_article` Runtime job，并接入 daily DAG。

## Workbench Result

Workbench 显示自动主选题、brief、大纲、初稿、review、rewrite、final candidate、质量问题和人工操作建议。

## 安全边界

不自动发布；不接公众号 API；不进草稿箱；不抓全文；不调用图片模型；weak signal 不作为硬证据；final candidate 必须人工审阅。

## 当前限制

Phase32 v1 以确定性 playbook 和 dry-run-safe agent review 为主。真实生产质量需要 Phase33 的连续试运行与人工反馈校准。

## 下一阶段

Phase 33：Autonomous Content Quality Calibration & One-Week Production Trial v1。

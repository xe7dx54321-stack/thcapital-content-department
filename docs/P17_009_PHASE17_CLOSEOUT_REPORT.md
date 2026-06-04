# P17-009 Phase 17 Closeout Report

## Phase 17 v1 目标

把人工认可的 live 输出提升为候选版本，并建立 manual image generation、image asset library、图文预览和最终视觉审查链路。

## Approved Live Brief/Draft Promotion

已支持 `ACCEPT_LIVE` / `MERGE` calibration 后 promotion。

## Live Rewrite Version Promotion

已支持 live rewrite sidecar promotion，不覆盖原稿。

## Manual Image Generation Executor

已支持 approved image prompt 转手工图片生成任务。

## Image Asset Library

已建立 metadata library 和本地图片目录 ignore 边界。

## Article-with-Images Preview

已生成带图片占位或 available asset 的公众号图文预览。

## Human Final Visual Review

已支持图片资产人工 approve / reject / needs revision / defer。

## Workbench Image Asset Panel

工作台已接入 Phase17 图片资产链路展示和复制入口。

## Daily Pipeline

新增 `make phase17-daily`。

## 当前限制

- 不自动发布。
- 不接公众号 API。
- 不进入公众号草稿箱。
- 不自动生成图片。
- 不调用图片模型。
- 不提交图片文件。
- live output promotion 只处理人工认可输出。

## 下一阶段建议

Phase 18：Article-with-Images Final Candidate & Manual Publishing Pack v1。

- P18-001 Visual-approved Final Article Candidate v1
- P18-002 WeChat Copy Pack with Image Slots v1
- P18-003 Manual Publishing Checklist with Visual Assets v1
- P18-004 Post-publish Visual Performance Input v1
- P18-005 Visual Strategy Learning Feedback v1

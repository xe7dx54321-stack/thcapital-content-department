# P28-009 Phase 28 Closeout Report

## Phase 28 v1 目标

把 Phase 27 的 connector metadata 推进为 evidence packets、promoted topic candidates、freshness/dedup regression 和 acquisition-to-content bridge，让上游 acquisition 结果真正进入内容生产候选链路。

## OpenClaw Boundary Clarification

Phase 28 不迁移 OpenClaw cron，不接入 OpenClaw gateway，不全量导入 OpenClaw 旧 source，不照搬微信全文深抓、自动发布、草稿箱或公众号结果回流。OpenClaw 旧源迁移放到 Phase 29。

## P0 Connector Reliability Improvement

新增 connector reliability sidecar，把 failed / weak connector 转成可追踪 issue、fallback action 和人工处理建议。

## Evidence Packet Enrichment from Connector Items

新增 connector evidence packets。证据仅来自 metadata，不抓全文，不伪造成完整事实证据。

## Topic Candidate Promotion from Hot Materials

新增 connector-promoted topic candidates，只把 quality gate 通过且证据不弱的素材推进到 topic candidate sidecar。

## Connector Freshness and Dedup Regression

新增 metadata hygiene gate，检查 metadata-only、copyright-safe、重复率、freshness、promotion traceability 和 weak-signal 约束。

## Acquisition-to-Content Bridge

新增 acquisition-to-content bridge，显示 READY_FOR_BRIEF、NEEDS_EVIDENCE、WATCH 和 REJECTED 的上游 topic candidate。

## Workbench Evidence & Topic Promotion Panel

工作台新增 Evidence / Topic Promotion Panel，展示 evidence packet、promoted topic、freshness/dedup 和 bridge 摘要。

## Stable Daily Ops Acquisition Integration

`make stable-daily-ops` 已显示 acquisition_to_content、ready_for_brief 和 needs_evidence。

## Daily Enrichment Pipeline

新增 `make phase28-daily` 作为上游 enrichment 总入口。

## 当前限制

- 不抓全文。
- 不做自动事实验证。
- 不自动写稿或发布。
- metadata-derived evidence 仍需人工/后续证据增强。
- Phase 28 不做 OpenClaw 旧源迁移。

## 下一阶段建议

Phase 29：OpenClaw Source Migration & Signal Lane Integration v1

- P29-001：OpenClaw Source Inventory Import
- P29-002：OpenClaw Source Risk Classification
- P29-003：P0/P1 Migration Plan
- P29-004：Reddit / YC / TechCrunch / FinSMEs / Newsletter / Chinese Media Metadata Connector
- P29-005：Weak Signal Safety Gate
- P29-006：Workbench Source Migration Panel
- P29-007：Stable Daily Ops Source Supply Upgrade


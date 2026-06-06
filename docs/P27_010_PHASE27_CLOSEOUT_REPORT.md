# P27-010 Phase 27 Closeout Report

## Phase 27 v1 目标

从 Phase 26 的上游诊断层推进到少数 P0 高价值源的真实轻量 metadata connector 接入。

## P0 Source Connector Selection

系统可从 high-value source expansion plan 中选择无需 API key、无需登录、适合轻量 metadata 接入的 P0 源。

## RSS / Official Blog Connector Hardening

RSS / official blog connector 支持 metadata-only 抓取，并对单源失败做本地记录。

## GitHub / HuggingFace / arXiv Lightweight Connector

GitHub / HuggingFace / arXiv connector 支持公开 metadata feed / index，不使用 token，不下载 PDF，不抓全文。

## Manual URL Backfill Ingestion

manual URL backfill 支持读取 fallback queue 与本地 URL 队列，但不修改本地素材库，不自动抓取 URL 正文。

## Connector Output Normalization

所有 connector 输出统一为 normalized upstream items，并进行 URL 去重。

## Connector Regression and Source Health Gate

health gate 检查 metadata_only、copyright_safe、title/URL 存在、manual URL 不自动 fetch、generated artifacts ignore 等关键回归项。

## Hot Material Pool Connector Integration

normalized upstream items 已接入 hot signal capture 与 daily hot material pool，并通过 hot material quality gate 决定 watch / backfill / promote 建议。

## Workbench Connector Health Panel

工作台显示 P0 selection、connector runs、normalized item count、connector health、metadata/copyright checks 和 connector 对素材池的贡献。

## Daily Connector Pipeline

新增：

```bash
make phase27-daily
```

作为上游 connector 检查入口。日常仍推荐：

```bash
make stable-daily-ops
```

## 当前限制

- 不是完整爬虫系统。
- 不绕过登录、验证码或付费墙。
- 不抓全文。
- 不自动改 `config/sources.yaml`。
- 外部源失败会记录为 health gate 状态，不代表内容生产主链路失败。

## 下一阶段建议

Phase 28：Source Connector Expansion & Evidence Enrichment v1

- P28-001：P0 Connector Reliability Improvement
- P28-002：Evidence Packet Enrichment from Connector Items
- P28-003：Topic Candidate Promotion from Hot Materials
- P28-004：Connector Freshness and Dedup Regression
- P28-005：Acquisition-to-Content Closeout

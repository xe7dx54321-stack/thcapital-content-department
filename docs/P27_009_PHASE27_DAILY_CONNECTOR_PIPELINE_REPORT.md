# P27-009 Phase 27 Daily Connector Pipeline Report

## 目标

建立 Phase 27 daily connector pipeline，将 P0 selection、connector run、normalization、health gate、hot material integration、stable-daily-ops 与 workbench 串起来。

## 实现

- 新增 `scripts/run_phase27_daily_connector_pipeline.py`
- 新增 Makefile target `phase27-daily`。

## Pipeline 顺序

1. P0 source connector selection
2. RSS / official blog connectors
3. lightweight research connectors
4. manual URL backfill ingestion
5. connector output normalization
6. connector source health gate
7. hot signal capture
8. daily hot material pool
9. hot material quality gate
10. stable daily ops
11. workbench data
12. workbench frontend

## 安全边界

不自动发布、不调用公众号 API、不生成图片、不抓全文、不绕过登录/付费墙、不修改 `config/sources.yaml`。

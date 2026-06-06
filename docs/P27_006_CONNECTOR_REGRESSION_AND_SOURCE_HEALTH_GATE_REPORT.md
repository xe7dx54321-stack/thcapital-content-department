# P27-006 Connector Regression and Source Health Gate Report

## 目标

为 Phase 27 connector 输出建立 regression 与 source health gate，避免外部源失败污染内容生产主链路。

## 实现

- 新增 `src/content_system/connector_source_health_gate.py`
- 新增 `scripts/run_connector_source_health_gate.py`
- 输出 connector health board。

## Gate Checks

- metadata_only 全部为 true。
- copyright_safe 全部为 true。
- 不含全文字段。
- normalized item title / URL 存在。
- connector 单点失败被隔离。
- manual URL 不自动 fetch。
- generated artifacts 被 `.gitignore` 覆盖。

## 验收

运行：

```bash
make connector-source-health-gate
```

确认 gate_status、pass、warn、fail、healthy_connectors、weak_connectors、failed_connectors、normalized_item_count 可读。

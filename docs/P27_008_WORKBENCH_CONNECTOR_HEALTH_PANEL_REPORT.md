# P27-008 Workbench Connector Health Panel Report

## 目标

在工作台展示 Phase 27 connector 接入状态与 source health gate。

## 实现

- 修改 `src/content_system/wechat_workbench_data.py`
- 修改 `src/content_system/wechat_workbench_frontend.py`
- 新增 `connector_health_panel`。

## 展示内容

- P0 Source Connector Selection。
- RSS / Official Blog Connector Run。
- Lightweight Research Connector Run。
- Manual URL Backfill Ingestion。
- Normalized Upstream Items。
- Connector Source Health Gate。
- connector 对 daily hot material pool 的贡献。

## 验收

运行：

```bash
make wechat-workbench
```

确认审稿模式显示 Connector Health Panel。

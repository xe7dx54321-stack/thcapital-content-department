# P27-007 Hot Material Pool Connector Integration Report

## 目标

将 normalized upstream items 纳入 hot signal capture 与 daily hot material pool。

## 实现

- 修改 `src/content_system/hot_signal_capture.py`
- 修改 `src/content_system/daily_hot_material_pool.py`
- 更新对应脚本 summary 输出。

## 行为

- connector item 转为 hot signal 时保留 metadata_only / copyright_safe 标记。
- connector item 使用保守 hotness score，不直接绕过 quality gate。
- daily hot material pool summary 新增 connector_item_count、connector_promote_candidates。

## 验收

运行：

```bash
make hot-signal-capture
make daily-hot-material-pool
make hot-material-quality-gate
```

确认 hot signal 和 material pool 均显示 connector contribution。

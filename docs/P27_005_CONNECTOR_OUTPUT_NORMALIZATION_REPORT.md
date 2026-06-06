# P27-005 Connector Output Normalization Report

## 目标

将 RSS / research / manual URL connector 输出统一为 normalized upstream items。

## 实现

- 新增 `src/content_system/connector_output_normalizer.py`
- 新增 `scripts/normalize_connector_outputs.py`
- 统一字段包括 title、url、source_name、source_type、lane_id、event_type、domain_tags、summary、dedupe_key。

## 规则

- URL 去重。
- metadata_only=true。
- copyright_safe=true。
- 不保留全文字段。

## 验收

运行：

```bash
make normalize-connector-outputs
```

确认 item_count、deduped_count、candidate_for_hot_material_pool 可读。

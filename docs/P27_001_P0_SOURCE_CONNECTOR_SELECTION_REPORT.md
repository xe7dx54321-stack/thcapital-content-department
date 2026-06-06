# P27-001 P0 Source Connector Selection Report

## 目标

从 Phase 26 的 high-value source expansion plan 中选择无需 API key、无需登录、适合轻量接入的 P0 上游源。

## 实现

- 新增 `src/content_system/p0_source_connector_selection.py`
- 新增 `scripts/build_p0_source_connector_selection.py`
- 输出 P0 connector selection JSON / Markdown / board。

## 规则

- 只选择 safe_to_fetch 的 metadata 源。
- 不修改 `config/sources.yaml`。
- 需要 API key、登录、付费墙或复杂浏览器自动化的源标记为 FUTURE / SKIPPED。

## 验收

运行：

```bash
make p0-source-connector-selection
```

确认 summary 包含 selected_count、rss_official_blog、github_repo、huggingface_feed、arxiv_keyword、manual_url_backfill。

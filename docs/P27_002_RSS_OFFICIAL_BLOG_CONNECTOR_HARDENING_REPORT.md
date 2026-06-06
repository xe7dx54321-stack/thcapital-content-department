# P27-002 RSS / Official Blog Connector Hardening Report

## 目标

为 selected P0 official blog / RSS 源提供轻量 metadata connector。

## 实现

- 新增 `src/content_system/rss_official_blog_connector.py`
- 新增 `scripts/run_rss_official_blog_connectors.py`
- connector 优先使用 RSS/Atom，失败时尝试 HTML index metadata。

## 安全边界

- 只保留 title、URL、published_at、summary snippet、source metadata。
- 不抓全文，不绕过登录或付费墙。
- 单个源失败只记录 error，不让整体命令崩溃。

## 验收

运行：

```bash
make rss-official-blog-connectors
```

确认 source_count、success_sources、failed_sources、empty_sources、item_count 可读。

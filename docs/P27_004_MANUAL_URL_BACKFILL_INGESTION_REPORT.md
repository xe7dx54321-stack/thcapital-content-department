# P27-004 Manual URL Backfill Ingestion Report

## 目标

将 fallback backfill queue 与用户本地 URL 队列转为 manual review metadata items。

## 实现

- 新增 `src/content_system/manual_url_backfill_ingestion.py`
- 新增 `scripts/run_manual_url_backfill_ingestion.py`
- 只读取 `内容素材库/URL抓取/url_capture_queue.md`，不修改、不 stage、不 commit。

## 安全边界

- manual URL 不自动抓取正文。
- manual items 默认 `do_not_auto_fetch=true`。
- 本地素材库只读。

## 验收

运行：

```bash
make manual-url-backfill-ingestion
```

确认 manual_item_count、ready_for_review、needs_fetch、invalid、duplicate 可读。

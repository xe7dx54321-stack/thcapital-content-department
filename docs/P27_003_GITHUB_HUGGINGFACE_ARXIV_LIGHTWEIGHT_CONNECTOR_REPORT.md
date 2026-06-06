# P27-003 GitHub / HuggingFace / arXiv Lightweight Connector Report

## 目标

接入 GitHub、HuggingFace、arXiv 的公开 metadata feed / index，提升 AI / Agent / research lane 的每日素材供给。

## 实现

- 新增 `src/content_system/lightweight_research_connectors.py`
- 新增 `scripts/run_lightweight_research_connectors.py`
- 支持 GitHub releases / trending-like index、HuggingFace blog/papers、arXiv keyword query。

## 安全边界

- 不使用 GitHub token。
- 不下载论文 PDF。
- 不抓全文。
- public endpoint 不稳定时记录 FAILED / SKIPPED，不污染主链路。

## 验收

运行：

```bash
make lightweight-research-connectors
```

确认 connector_count、success_connectors、failed_connectors、item_count 可读。

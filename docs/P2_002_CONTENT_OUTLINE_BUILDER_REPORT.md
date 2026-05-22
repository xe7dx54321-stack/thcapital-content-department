# P2-002 Content Outline Builder v1 报告

## 本轮目标

- 从 content briefs 生成结构化 outline。
- 同时生成微信公众号和小红书方向的大纲。
- 保留 required evidence 和 editor notes。

## 新增文件

- `src/content_system/content_outline.py`
- `scripts/build_content_outlines.py`

## 新增命令

```bash
make content-outlines
```

## 输出产物

- `同行资本市场内容系统/05_draft_packs/YYYYMMDD__content-outlines.json`
- `同行资本市场内容系统/05_draft_packs/YYYYMMDD__content-outlines.md`
- `同行资本市场内容系统/05_draft_packs/latest_content_outlines.json`
- `同行资本市场内容系统/05_draft_packs/latest_content_outlines.md`

## 未做事项

- 不做 LLM 大纲生成。
- 不做平台最终包装。

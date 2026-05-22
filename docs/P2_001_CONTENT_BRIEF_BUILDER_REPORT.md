# P2-001 Content Brief Builder v1 报告

## 本轮目标

- 从 `latest_high_value_candidates.json` 生成标准 content briefs。
- 保留候选主题、得分、证据、风险、缺口和目标平台。
- 不直接生成成品文章。

## 新增文件

- `src/content_system/content_brief.py`
- `scripts/build_content_briefs.py`

## 新增命令

```bash
make content-briefs
```

## 输出产物

- `同行资本市场内容系统/05_draft_packs/YYYYMMDD__content-briefs.json`
- `同行资本市场内容系统/05_draft_packs/YYYYMMDD__content-briefs.md`
- `同行资本市场内容系统/05_draft_packs/latest_content_briefs.json`
- `同行资本市场内容系统/05_draft_packs/latest_content_briefs.md`

以上均为 generated artifacts，默认不进入 Git。

## 未做事项

- 不调用 LLM。
- 不生成最终文章。
- 不自动发布。

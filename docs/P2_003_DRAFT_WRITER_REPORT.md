# P2-003 Draft Writer v1 报告

## 本轮目标

- 用规则模板从 outlines 生成初稿。
- 草稿包含核心判断、为什么现在重要、关键事实、证据、风险提示和人工编辑提示。
- 明确声明草稿需要人工编辑。

## 新增文件

- `src/content_system/content_draft.py`
- `scripts/build_content_drafts.py`

## 新增命令

```bash
make content-drafts
```

## 输出产物

- `同行资本市场内容系统/05_draft_packs/YYYYMMDD__content-drafts.json`
- `同行资本市场内容系统/05_draft_packs/YYYYMMDD__content-drafts.md`
- `同行资本市场内容系统/05_draft_packs/latest_content_drafts.json`
- `同行资本市场内容系统/05_draft_packs/latest_content_drafts.md`

## 未做事项

- 不调用 LLM。
- 不伪装成可直接发布的终稿。
- 不自动发布。

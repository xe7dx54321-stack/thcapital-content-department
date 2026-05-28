# P12-003 Human Final Publish Checklist Report

## 本轮目标

为 final article candidate 生成最终人工发布前 checklist，帮助人工确认标题、证据、风险、排版和复制发布步骤。

## 修改文件

- `src/content_system/final_publish_checklist.py`
- `scripts/build_final_publish_checklist.py`
- `Makefile`

## Checklist 范围

- 标题是否明确、有吸引力且不标题党。
- 开头是否能抓住读者。
- 正文逻辑是否顺畅。
- 证据和来源是否足够。
- 是否有事实风险、过度承诺或夸张表达。
- 是否包含风险提示。
- 是否适合公众号阅读。
- 是否确认人工复制到公众号后台，且不自动发布。

## 输出

- `同行资本市场内容系统/07_publishing/YYYYMMDD__final-publish-checklist.json`
- `同行资本市场内容系统/07_publishing/latest_final_publish_checklist.json`
- 对应 Markdown 报告。

## 当前限制

checklist 只辅助人工发布，不接公众号 API，也不会标记已发布。

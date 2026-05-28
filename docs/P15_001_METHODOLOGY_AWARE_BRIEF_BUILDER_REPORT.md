# P15-001 Methodology-aware Brief Builder Report

## 本轮目标

让 brief 直接引用选题方法论、文章方法论和内容类型 recipe。

## 修改文件

- `src/content_system/methodology_brief_builder.py`
- `scripts/build_methodology_briefs.py`

## 输出

- `latest_methodology_content_briefs.json`
- `latest_methodology_content_briefs.md`

## 边界

不替换原 content brief，不自动发布，不调用 live model。

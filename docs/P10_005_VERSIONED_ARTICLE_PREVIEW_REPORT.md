# P10-005 Versioned Article Preview Report

## 目标

将 action executor 生成的新版本渲染为可审阅的版本化文章预览。

## 已完成

- 新增 `versioned_article_preview.py`。
- 新增 `build_versioned_article_preview.py`。
- 输出 `latest_versioned_article_preview.html` 和 `latest_versioned_article_preview.json`。

## 页面内容

- 原版本。
- 新版本。
- source action。
- version id。
- change summary。
- `do_not_overwrite_original=true`。

## 当前限制

- v1 不做复杂 diff，只做并排版本预览。

# P9-002 WeChat Article Preview Renderer v1 Report

## 本轮目标

将选中的公众号文章渲染成接近公众号阅读状态的静态 HTML，帮助人工判断文章发出后的阅读体验。

## 新增文件

- `src/content_system/wechat_article_preview.py`
- `scripts/render_wechat_article_preview.py`

## 新增命令

```bash
make wechat-article-preview
```

## 能力

- 基础 Markdown 到 HTML。
- 公众号式标题、作者、日期和正文排版。
- source/evidence 简表。
- 复制正文按钮。

## 边界

不接公众号草稿箱，不做真实发布。

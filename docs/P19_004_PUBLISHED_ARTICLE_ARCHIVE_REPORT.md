# P19-004 Published Article Archive Report

## 目标

把 manual publish session、copy pack、metrics、visual performance 和 image asset metadata 合并为长期已发布文章归档。

## 已完成

- 新增 `published_article_archive.py`。
- 新增 `update_published_article_archive.py` 和 `build_published_article_archive_board.py`。
- 输出 `published_article_archive.json/md` 和前台 board。

## 边界

- 归档只记录人工发布事实。
- 不抓取公众号后台数据。

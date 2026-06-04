# P18-004 Post-publish Visual Performance Input Report

## 目标

支持用户手动记录发布后的视觉表现观察，例如某张框架图是否帮助理解，或某张图是否干扰阅读。

## 已完成

- 新增 `post_publish_visual_performance.py`。
- 新增 CLI：`record_post_publish_visual_performance.py`。
- 新增只读 board：`build_post_publish_visual_performance_board.py`。

## 边界

- 表现数据全部人工录入。
- 不抓取公众号后台数据。
- 不需要公众号账号密码。

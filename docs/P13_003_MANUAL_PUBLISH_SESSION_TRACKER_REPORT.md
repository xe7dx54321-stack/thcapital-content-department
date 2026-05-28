# P13-003 Manual Publish Session Tracker Report

## 本轮目标

记录人工复制到公众号后台、人工排版和人工发布的 session，不做任何自动发布。

## 修改文件

- `src/content_system/manual_publish_session.py`
- `scripts/create_manual_publish_session.py`
- `scripts/build_publish_session_board.py`
- `Makefile`

## 已完成能力

- 支持创建 manual publish session。
- 支持标记 manually published、cancelled、deferred。
- 输出 manual publish session JSON/Markdown 和 frontstage board。
- 新增 `make publish-session-board`。

## 安全边界

- `publish_mode=manual_copy`。
- `do_not_auto_publish=true`。
- 不接公众号 API，不进入草稿箱。

## 当前限制

发布链接和实际发布时间需要人工录入。

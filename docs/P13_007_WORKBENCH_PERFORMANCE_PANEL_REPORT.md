# P13-007 Workbench Performance Panel Report

## 本轮目标

把 manual publish session、post-publish metrics、content performance memory 和 learning feedback 接入微信公众号工作台。

## 修改文件

- `src/content_system/wechat_workbench_data.py`
- `src/content_system/wechat_workbench_frontend.py`

## 已完成能力

- workbench data 新增 `performance_panel`。
- 工作台右侧面板展示发布 session 和表现评级。
- 审稿模式新增“发布表现闭环”卡片。
- 支持复制创建 publish session、标记已发布、录入 metrics 的 CLI 命令。

## 安全边界

- 前端按钮只复制命令。
- 不自动发布。
- 不自动登录公众号。
- 不自动抓取表现数据。

## 当前限制

交互式保存能力由本地 server v2 提供；静态 HTML 仍保留命令复制 fallback。

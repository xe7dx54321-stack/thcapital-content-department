# P19-007 Workbench Content Ops Panel Report

## 目标

把发布日历、内容队列、周节奏、已发布归档、指标复盘和运营 closeout 接入微信公众号工作台。

## 已完成

- `wechat_workbench_data.py` 新增 `content_ops_panel`。
- `wechat_workbench_frontend.py` 新增内容运营 panel。
- 审稿模式展示今日建议、本周优先、blocker、周节奏、复盘 insight 和 operator actions。

## 边界

- 阅读模式保持干净。
- 运营面板不触发任何发布动作。

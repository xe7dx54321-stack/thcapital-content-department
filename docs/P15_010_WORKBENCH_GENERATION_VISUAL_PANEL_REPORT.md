# P15-010 Workbench Generation & Visual Panel Report

## 本轮目标

把 methodology-aware generation 和 visual plan 接入微信公众号工作台。

## 修改文件

- `src/content_system/wechat_workbench_data.py`
- `src/content_system/wechat_workbench_frontend.py`

## UI 能力

- 审稿模式展示 methodology brief、outline、draft status。
- 展示 visual plan、image asset requests、recommended visual count。
- 支持复制 image prompt / design brief。

## 边界

阅读模式保持干净；图片策略只在审稿/右侧面板展示。

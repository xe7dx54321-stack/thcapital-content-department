# P24-007 Workbench Stable Trial Panel Report

## 目标

把 stable trial、content quality calibration、ops-to-methodology feedback 和 stable ops readiness review 接入工作台。

## 实现

- 更新 `src/content_system/wechat_workbench_data.py`，新增 `phase24_panel`。
- 更新 `src/content_system/wechat_workbench_frontend.py`，新增 Phase24 Stable Trial Panel。
- 在 insight panel 中显示 readiness、stable days、quality blockers 和 methodology feedback。

## 边界

阅读模式保持干净；stable trial 信息只在审稿/系统运维视图显示。
